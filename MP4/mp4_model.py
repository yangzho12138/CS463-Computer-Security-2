import os
import numpy as np
# import ujson as json
import json
import pickle
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_selection import SelectFromModel

class SVMModel:
    """Base class for SVM-like classifiers."""

    def __init__(self, X_filename, y_filename, meta_filename, num_features=None, save_folder='./SVM_models'):
        self.X_filename = X_filename
        self.y_filename = y_filename
        self.meta_filename = meta_filename
        self._num_features = num_features
        self.save_folder = save_folder
        self.clf, self.vec = None, None
        self.column_idxs = [] # feature indexes after feature selection
        self.X_train, self.y_train, self.m_train = [], [], []
        self.X_test, self.y_test, self.m_test = [], [], []
        self.feature_index_positive = None
        self.feature_index_negative = None

    def generate(self, save=True):
        X_train, X_test, y_train, y_test, m_train, m_test, self.vec, train_test_random_state = load_features(
            self.X_filename, self.y_filename, self.meta_filename)

        self.column_idxs = self.perform_feature_selection(X_train, y_train)
        self.X_train = X_train[:, self.column_idxs]
        self.X_test = X_test[:, self.column_idxs]
        self.y_train, self.y_test = y_train, y_test
        self.m_train, self.m_test = m_train, m_test
        self.clf = self.fit(self.X_train, self.y_train)

        if save:
            self.save_to_file()

    def perform_feature_selection(self, X_train, y_train):
        # After feature election, the model achieves better results
        # 1. a model which uses too many features may lead to a overfitting problem
        # 2. some features may not be benefit for the model prediction which could be seen as noise, and removing them can improve the model performance
        
        ##############TODO: this can be the part implemented by the students#########
        # Perform L2-penalty feature selection
        cols = None
        if self._num_features is not None:
            # TODO how to determine the C value?
            sel = SelectFromModel(LinearSVC(C=0.1, penalty='l2'), max_features=self._num_features)
            sel.fit(X_train, y_train)
            cols = sel.get_support(indices=True)
            # get the feature weights
            feature_weights = sel.estimator_.coef_
            selected_feature_weights = feature_weights[:, cols]
            self.feature_index_positive = selected_feature_weights.argsort()[0][-300:][::-1]
            self.feature_index_negative = selected_feature_weights.argsort()[0][:300]
        else:
            cols = np.arange(X_train.shape[1])

        return cols

    def save_to_file(self):
        create_parent_folder(self.model_name)
        with open(self.model_name, 'wb') as f:
            pickle.dump(self, f, protocol=4)


class SVM(SVMModel):
    """Standard linear SVM using scikit-learn implementation."""

    def __init__(self, X_filename, y_filename, meta_filename, save_folder='./mp4_SVM_models', num_features=None, svm_c=1, max_iter=1000):
        super().__init__(X_filename, y_filename, meta_filename, num_features, save_folder)
        self.model_name = self.generate_model_name()
        self.svm_c = svm_c
        self.max_iter = max_iter

    def fit(self, X_train, y_train):
        ##############TODO: implement me #########
        # return the classifier
        clf = LinearSVC(C=self.svm_c, max_iter=self.max_iter)
        clf.fit(X_train, y_train)
        
        return clf

    def generate_model_name(self):
        model_name = f'svm'
        model_name += '.p' if self._num_features is None else '-f{}.p'.format(self._num_features)
        return os.path.join(self.save_folder, model_name)

def create_parent_folder(file_path):
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))

def load_features(X_filename, y_filename, meta_filename):
    train_test_random_state = 137 #hard coded to split the training set and testing set.
    with open(X_filename, 'rt') as f:
        X = json.load(f)
        try:
            [o.pop('sha256') for o in X]
        except:
            pass
    with open(y_filename, 'rt') as f:
        y = json.load(f)
    with open(meta_filename, 'rt') as f:
        meta = json.load(f)

    X, y, vec = vectorize(X, y)
    train_idxs, test_idxs = train_test_split(
        range(X.shape[0]),
        stratify=y,
        test_size=0.33,
        random_state=train_test_random_state)

    X_train = X[train_idxs]
    X_test = X[test_idxs]
    y_train = y[train_idxs]
    y_test = y[test_idxs]
    m_train = [meta[i] for i in train_idxs]
    m_test = [meta[i] for i in test_idxs]

    return X_train, X_test, y_train, y_test, m_train, m_test, vec, train_test_random_state

def vectorize(X, y):
    vec = DictVectorizer(sparse=True)
    X = vec.fit_transform(X)
    y = np.asarray(y)
    return X, y, vec
