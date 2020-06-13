import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
from sklearn.preprocessing import StandardScaler



def prep_data():
    #df = pd.read_csv('out_nat_first_test.csv')
    df = pd.read_csv('out_nat_second_test.csv')
    x = df.iloc[:, 5:]
    class_name = ['IOS', 'windows', 'android', 'linux']
    df['label_num'] = [class_name.index(class_str)
                       for class_str in df['label'].values]


    y = df.loc[:, ['label']]
    y = pd.get_dummies(y['label'])
    x['upstream_ssl_v'] = x.upstream_ssl_v.apply(lambda x: int(x, 16))
    return x,y


def main():
    x,y = prep_data()
    x_train,x_test,y_train,y_test = train_test_split(x,y)
    x_train = np.nan_to_num(x_train)
    x_test = np.nan_to_num(x_test)
    y_train = np.nan_to_num(y_train)
    y_test = np.nan_to_num(y_test)
    print("K Nearest Neigbors: ")
    KNN(x_test, x_train, y_test, y_train)
    print('\n\n')
    print("Random Forest: ")
    RandomForest(x_test, x_train, y_test, y_train)


def KNN(x_test, x_train, y_test, y_train):
    x_train, x_test = FeatureScaling(x_test, x_train)
    classifier = KNeighborsClassifier(n_neighbors=5, metric='minkowski', p=2)
    classifier.fit(x_train, y_train)
    y_pred = classifier.predict(x_test)
    cm = confusion_matrix(y_test.argmax(axis=1), y_pred.argmax(axis=1))
    print('Conf. Mat.:')
    print(cm)
    print('Acc.:')
    print(accuracy_score(y_test, y_pred))
    print('Prec.:')
    print(precision_score(y_test, y_pred, average=None))
    print('Recall:')
    print(recall_score(y_test, y_pred, average=None))
    print('F1:')
    print(f1_score(y_test, y_pred, average=None))


def FeatureScaling(x_test, x_train):
    sc = StandardScaler()
    X_train = sc.fit_transform(x_train)
    X_test = sc.transform(x_test)
    return X_train,X_test


def RandomForest(x_test, x_train, y_test, y_train):
    classifier = RandomForestClassifier(n_estimators=10, criterion='entropy', random_state=0)
    classifier.fit(x_train, y_train)
    y_pred = classifier.predict(x_test)
    cm = confusion_matrix(y_test.argmax(axis=1), y_pred.argmax(axis=1))
    print('Conf. Mat.:')
    print(cm)
    print('Acc.:')
    print(accuracy_score(y_test, y_pred))
    print('Prec.:')
    print(precision_score(y_test, y_pred, average=None))
    print('Recall:')
    print(recall_score(y_test, y_pred, average=None))
    print('F1:')
    print(f1_score(y_test, y_pred, average=None))



if __name__ == "__main__":
    main()

