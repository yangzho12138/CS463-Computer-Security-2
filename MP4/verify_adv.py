import mp4_model as models
import numpy as np
import json
from scipy.sparse import csr_matrix

input_file_folder = f'data'
X_file_name = f'{input_file_folder}/apg-X.json'
y_file_name = f'{input_file_folder}/apg-y.json'
meta_file_name = f'{input_file_folder}/apg-meta.json'

A_file_name = f'49875A9C25EB18945A8E7F27C8188834CFF48070413604D477763EC7A20E9C4A.json'
B_file_name = f'5E06B7510B55B52C94D2AB0D7BB94AAA454860C6F8729BA2842438D92CDB8EEE.json'

def generate_feature_name():
    svm_model = models.SVM(X_file_name, y_file_name, meta_file_name, num_features=5000)
    svm_model.generate()

    ''' generate all the feature names used by current mode '''
    # 5000 features
    feature_name_list = [svm_model.vec.feature_names_[i] for i in svm_model.column_idxs]
    
    # generate the list of 49875A
    with open(A_file_name, 'rt') as f:
        A_feature = json.load(f)
    
    A_feature_list = []
    for i in feature_name_list:
        if i in A_feature.keys():
            A_feature_list.append(1)
        else:
            A_feature_list.append(0)
    
    # generate the list of 5E06B
    with open(B_file_name, 'rt') as f:
        B_feature = json.load(f)

    B_feature_list = []
    for i in feature_name_list:
        if i in B_feature.keys():
            B_feature_list.append(1)
        else:
            B_feature_list.append(0)
    
    arr1 = np.array([A_feature_list])
    arr1 = arr1.reshape(-1, 1).T
    arr2 = np.array([B_feature_list])
    arr2 = arr2.reshape(-1, 1).T
    arr = np.vstack([arr1, arr2])
    apk_test = csr_matrix(arr)

    y_pred = svm_model.clf.predict(apk_test)
    print("Before create the adversarial samples ", y_pred) #[1 0]

    
    # use SVM to make an explation on the feature weights

    # features contributes more to malicious judgement
    choose_feature_list_positive = []
    if svm_model.feature_index_positive is not None:
        # top300 effective features that contribute more to malicious judgement
        choose_feature_list_positive = [i for i in svm_model.feature_index_positive if feature_name_list[i].startswith('app_permission') or feature_name_list[i].startswith('api_perssion')]
        # choose 30 features
        if len(choose_feature_list_positive) > 30:
            choose_feature_list_positive = choose_feature_list_positive[:30]

    # features contributes more to benign judgement  
    choose_feature_list_negative = []
    if svm_model.feature_index_negative is not None:
        # top300 effective features that contribute more to benign judgement
        choose_feature_list_negative = [i for i in svm_model.feature_index_negative if feature_name_list[i].startswith('app_permission') or feature_name_list[i].startswith('api_perssion')]
        # choose 30 features
        if len(choose_feature_list_negative) > 30:
            choose_feature_list_negative = choose_feature_list_negative[:30]



    # add features to the two apks
    # in the choose_feature_list_negative, the features' weights are close to -1, which means that the features are more likely to be used by benign apks (contributes more to benign judgement)
    # by adding these features, 49875A apk will be more likely to be judged as benign
    with open("added-features-49875A.txt", "w") as f:
        for index in choose_feature_list_negative:
            if A_feature_list[index] == 0:
                A_feature_list[index] = 1
                f.write(feature_name_list[index] + "\n")
    
    # in the choose_feature_list_positive, the features' weights are close to 1, which means that the features are more likely to be used by malicious apks (contributes more to malicious judgement)
    # by adding these features, 5E06B apk will be more likely to be judged as malicious
    with open("added-features-5E06B7.txt", "w") as f:
        for index in choose_feature_list_positive:
            if B_feature_list[index] == 0:
                B_feature_list[index] = 1
                f.write(feature_name_list[index] + "\n")
    
    arr1 = np.array([A_feature_list])
    arr1 = arr1.reshape(-1, 1).T
    arr2 = np.array([B_feature_list])
    arr2 = arr2.reshape(-1, 1).T
    arr = np.vstack([arr1, arr2])
    apk_test = csr_matrix(arr)

    y_pred = svm_model.clf.predict(apk_test)
    print("After create the adversarial samples ", y_pred) #[0 1]

if __name__ == '__main__':
    generate_feature_name()
