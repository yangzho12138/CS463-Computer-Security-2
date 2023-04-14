import os
import json
import pickle
import traceback

import sklearn
import numpy as np


def dump_json(data, output_dir, filename, overwrite=True):
    dump_data('json', data, output_dir, filename, overwrite)


def dump_data(protocol, data, output_dir, filename, overwrite=True):
    file_mode = 'w' if protocol == 'json' else 'wb'
    fname = os.path.join(output_dir, filename)
    print(f'Dumping data to {fname}...')
    if overwrite or not os.path.exists(fname):
        with open(fname, file_mode) as f:
            if protocol == 'json':
                json.dump(data, f, indent=4)
            else:
                # pickle.dump(data, f)
                pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)


def evaluate_classifier_perf(model):
    y_train_pred = model.clf.predict(model.X_train)
    y_pred = model.clf.predict(model.X_test)

    with open(f'pred_vs_true.csv', 'w') as f:
        for m, p, t in zip(model.m_test, y_pred, model.y_test):
            f.write(f'{m["sha256"]},{p},{t}\n')

    report_train = calculate_base_metrics(model.y_train, y_train_pred)
    report_test = calculate_base_metrics(model.y_test, y_pred)

    return report_train, report_test


def calculate_base_metrics(y_test, y_pred):
    """Calculate F1, Precision and Recall for given scores.
    Args:
        y_test: Array of ground truth labels aligned with `y_pred` and `y_scores`.
        y_pred: Array of predicted labels, aligned with `y_scores` and `model.y_test`.
        output_dir: The directory used for dumping output.

    Returns:
        dict: Model performance stats.
    """
    acc, f1, precision, recall, fpr = -1, -1, -1, -1, -1
    cm = sklearn.metrics.confusion_matrix(y_test, y_pred)
    if np.all(y_test == 0) and np.all(y_pred == 0):
        TN = len(y_test)
        TP, FP, FN = 0, 0, 0
    elif np.all(y_test == 1) and np.all(y_pred == 1):
        TP = len(y_test)
        TN, FP, FN = 0, 0, 0
    else:
        TN = cm[0][0]
        FN = cm[1][0]
        TP = cm[1][1]
        FP = cm[0][1]
    try:
        f1 = sklearn.metrics.f1_score(y_test, y_pred)
        precision = sklearn.metrics.precision_score(y_test, y_pred)
        recall = sklearn.metrics.recall_score(y_test, y_pred)
        acc = sklearn.metrics.accuracy_score(y_test, y_pred)
    except:
        print(traceback.format_exc())

    try:
        fpr = FP / (FP + TN)
    except:
        pass

    return {
        'model_performance': {
            'acc': acc,
            'f1': f1,
            'precision': precision,
            'recall': recall,
            'fpr': fpr,
            'cm': cm
        }
    }
