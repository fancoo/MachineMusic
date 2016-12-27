#!usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import random
import time
from sklearn import metrics
import numpy as np
import cPickle as pickle
from sklearn.datasets import load_svmlight_file


# Multinomial Naive Bayes Classifier
def naive_bayes_classifier(train_x, train_y):
    from sklearn.naive_bayes import MultinomialNB
    model = MultinomialNB(alpha=0.01)
    model.fit(train_x, train_y)
    return model


# KNN Classifier
def knn_classifier(train_x, train_y):
    from sklearn.neighbors import KNeighborsClassifier
    model = KNeighborsClassifier()
    model.fit(train_x, train_y)
    return model


# Logistic Regression Classifier
def logistic_regression_classifier(train_x, train_y):
    from sklearn.linear_model import LogisticRegression
    model = LogisticRegression(penalty='l2')
    model.fit(train_x, train_y)
    return model


# Random Forest Classifier
def random_forest_classifier(train_x, train_y):
    from sklearn.ensemble import RandomForestClassifier
    model = RandomForestClassifier(n_estimators=8)
    model.fit(train_x, train_y)
    return model


# Decision Tree Classifier
def decision_tree_classifier(train_x, train_y):
    from sklearn import tree
    model = tree.DecisionTreeClassifier()
    model.fit(train_x, train_y)
    return model


# GBDT(Gradient Boosting Decision Tree) Classifier
def gradient_boosting_classifier(train_x, train_y):
    from sklearn.ensemble import GradientBoostingClassifier
    model = GradientBoostingClassifier(n_estimators=200)
    model.fit(train_x, train_y)
    return model


# SVM Classifier
def svm_classifier(train_x, train_y):
    from sklearn.svm import SVC
    model = SVC(kernel='rbf', probability=True)
    model.fit(train_x, train_y)
    return model

# SVM Classifier using cross validation
def svm_cross_validation(train_x, train_y):
    from sklearn.grid_search import GridSearchCV
    from sklearn.svm import SVC
    model = SVC(kernel='rbf', probability=True)
    param_grid = {'C': [1e-3, 1e-2, 1e-1, 1, 10, 100, 1000], 'gamma': [0.001, 0.0001]}
    grid_search = GridSearchCV(model, param_grid, n_jobs=1, verbose=1)
    grid_search.fit(train_x, train_y)
    best_parameters = grid_search.best_estimator_.get_params()
    for para, val in best_parameters.items():
        print para, val
    model = SVC(kernel='rbf', C=best_parameters['C'], gamma=best_parameters['gamma'], probability=True)
    model.fit(train_x, train_y)
    return model


def split_data(csv_file, train_file, test_file):
    f_csv = open(csv_file, 'r')
    f_train = open(train_file, 'w')
    f_test = open(test_file, 'w')

    for line in f_csv:
        t = random.random()
        if t > 0.3:
            f_train.write(line.strip() + '\n')
        else:
            f_test.write(line.strip() + '\n')

    f_train.close()
    f_test.close()
    f_csv.close()


def normalize(train_file, test_file):
	fv = [0] * 1000

	for line in open(train_file):
		toks = line.strip().split(' ')
		for tok in toks[1:] :
			k,v = tok.split(':')
			k = int(k)
			v = float(v)
			if fv[k] < v :
				fv[k] = v
	for line in open(test_file) :
		toks = line.strip().split(' ')
		for tok in toks[1:] :
			k,v = tok.split(':')
			k = int(k)
			v = float(v)
			if fv[k] < v :
				fv[k] = v

	f_out = open(train_file + '.norm', 'w')
	for line in open(train_file) :
		toks = line.strip().split(' ')
		line = toks[0]

		vs = map(lambda x: x.split(':'), toks[1:])
		vs = map(lambda x: (int(x[0]), float(x[1])), vs)
		vs = map(lambda x: '%d:%.3f'%(x[0], x[1]/fv[x[0]]), vs)
		line = '%s %s\n'%(toks[0], ' '.join(vs))
		f_out.write(line)
	f_out.close()

	f_out = open(test_file + '.norm', 'w')
	for line in open(test_file):
		toks = line.strip().split(' ')
		line = toks[0]

		vs = map(lambda x: x.split(':'), toks[1:])
		vs = map(lambda x: (int(x[0]), float(x[1])), vs)
		vs = map(lambda x: '%d:%.3f'%(x[0], x[1]/fv[x[0]]), vs)
		line = '%s %s\n'%(toks[0], ' '.join(vs))
		f_out.write(line)
	f_out.close()


def read_data(train_file, test_file):
    X_train, y_train = load_svmlight_file(train_file)
    X_test, y_test = load_svmlight_file(test_file)
    return X_train, y_train, X_test, y_test

if __name__ == '__main__':
    # data_file = "mnist.pkl.gz"
    # thresh = 0.5
    # model_save_file = None
    # model_save = {}

    # test_classifiers = ['NB', 'KNN', 'LR', 'RF', 'DT', 'SVM', 'GBDT']
    test_classifiers = ['NB', 'LR', 'RF', 'DT', 'SVM', 'GBDT']
    # test_classifiers = ['NB', 'LR', 'RF', 'DT']
    classifiers = {'NB':naive_bayes_classifier,
                  # 'KNN':knn_classifier,
                   'LR':logistic_regression_classifier,
                   'RF':random_forest_classifier,
                   'DT':decision_tree_classifier,
                  'SVM':svm_classifier,
                'SVMCV':svm_cross_validation,
                 'GBDT':gradient_boosting_classifier
    }

    print 'reading training and testing data...'

    csv_file = '../data/train_data.csv'
    train_file = '../matrix/train.csv'
    test_file = '../matrix/test.csv'
    split_data(csv_file, train_file, test_file)
    normalize(train_file, test_file)
    train_x, train_y, test_x, test_y = read_data(train_file + '.norm', test_file + '.norm')
    num_train, num_feat = train_x.shape
    num_test, num_feat = test_x.shape
    is_binary_class = (len(np.unique(train_y)) == 2)
    print '******************** Data Info *********************'
    print '#training data: %d, #testing_data: %d, dimension: %d' % (num_train, num_test, num_feat)

    for classifier in test_classifiers:
        print '******************* %s ********************' % classifier
        start_time = time.time()
        model = classifiers[classifier](train_x, train_y)
        print 'training took %fs!' % (time.time() - start_time)
        predict = model.predict(test_x)
        print 'predict success!'

        if is_binary_class:
            precision = metrics.precision_score(test_y, predict)
            recall = metrics.recall_score(test_y, predict)
            f1_score = metrics.f1_score(test_y, predict)
            auc_score = metrics.roc_auc_score(test_y, predict)
            print 'precision: %.2f%%, recall: %.2f%%, f1_score: %.2f%%' % (100 * precision, 100 * recall, 100 * f1_score)
        accuracy = metrics.accuracy_score(test_y, predict)
        print 'accuracy: %.2f%%\n' % (100 * accuracy)
        print 'auc_score: %.2f%%\n' % (100 * auc_score)

    # if model_save_file != None:
    #     pickle.dump(model_save, open(model_save_file, 'wb'))
