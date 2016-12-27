# coding: utf-8

import os
import sys
import time
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score, mean_squared_error, roc_curve, auc
import datetime
from sklearn.datasets import load_svmlight_file
from sklearn.ensemble import GradientBoostingRegressor,GradientBoostingClassifier
from sklearn.ensemble import RandomForestRegressor,RandomForestClassifier
from sklearn.ensemble import BaggingRegressor,BaggingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import mean_squared_error
from sklearn.grid_search import GridSearchCV
from sklearn.ensemble.forest import ExtraTreesRegressor,ExtraTreesClassifier
from sklearn.ensemble.weight_boosting import AdaBoostRegressor,AdaBoostClassifier
from sklearn.metrics import f1_score,accuracy_score,precision_score,recall_score,roc_curve,auc


def read_corpus(train_file, test_file, train_num=-1, test_num=-1):
        t0 = time.time()
        train_x, train_y = load_svmlight_file(train_file)
        test_x, test_y = load_svmlight_file(test_file)

        if train_num > 0 :
                train_x = train_x[:train_num]
                train_y = train_y[:train_num]

        if test_num > 0 :
                test_x = test_x[:test_num]
                test_y = test_y[:test_num]

        train_x = train_x.toarray()
        test_x = test_x.toarray()
        t1 = time.time()
        print('read data from corpus use time: %.2f secs'%(t1-t0))

        return (train_x, train_y, test_x, test_y)


def run_grid_search(train_x, train_y, test_x, test_y):
	param_grid = {
			'loss': ['ls', 'lad', 'huber'],
			'n_estimators': [100, 200, 400, 600],
			'learning_rate': [1.0, 0.1, 0.05],
              		'max_depth': [1, 3],
                	'min_samples_leaf': [1, 3, 10],
                 	#'max_features': [1.0, 0.3, 0.1] ## not possible in our example (only 1 fx)
              	}
	t1 = time.time()
	clf = GradientBoostingRegressor(n_estimators=200)
	gs = GridSearchCV(clf, param_grid, n_jobs=8, scoring=rmse_loss).fit(train_x, train_y)
	for grid_score in gs.grid_scores_ :
		print grid_score
	print 'best score:', gs.best_score_
	print 'best_params:', gs.best_params_
	t2 = time.time()

	clf = GradientBoostingRegressor(**gs.best_params_).fit(train_x, train_y)
	pred_y = clf.predict(test_x)
	pred_y_prob = pred_y[:]
	pred_y = map(lambda x: 1 if x>=0.15 else 0, pred_y)
        t3 = time.time()

        train_size = len(train_x)
        test_size = len(test_x)
        time_str = 'grid_search:%.2fs, best_predict:%.2fs; train_size:%d,vec_size:%d,test_size:%d, params:%s'%(t2-t1, t3-t2, train_size, train_x.shape[1], test_size, str(gs.best_params_))
        print_predict_res(test_y, pred_y, pred_y_prob, time_str)


def run_clf(train_x, train_y, test_x, test_y, method=0, mode=0):
        '''
                method: 0=gbdt; 1=random forest;
                mode:   0=regressor; 1=classifier;
        '''
        t1 = time.time()
        clf = None
        params = {}

        if method == 0 :
                if mode == 1 :
                        #params = {'n_estimators':200, 'learning_rate':1.0, 'max_depth':1, 'random_state':0}
                        params = {'n_estimators':400, 'learning_rate':0.1, 'max_depth':3, 'min_samples_leaf':10}
                        clf = GradientBoostingRegressor(**params)
                else :
                        params = {'n_estimators': 400, 'learning_rate': 0.1, 'max_depth': 3, 'min_samples_leaf': 10}
                        clf = GradientBoostingClassifier(**params)
        elif method == 1 :
                if mode == 1 :
                        params = {'n_estimators':600, 'max_features':0.6, 'min_samples_leaf':3}
                        clf = RandomForestRegressor(**params)
                else :
                        params = {'n_estimators':100, 'max_features':0.6, 'min_samples_leaf':3}
                        #params = {'n_estimators':100, 'max_features':'sqrt', 'min_samples_leaf':3}
                        clf = RandomForestClassifier(**params)
	elif method == 2 :
		params = {'C': 0.1, 'penalty': 'l1'}
		clf = LogisticRegression(**params)
        else :
                print 'wrong parameter: method=%d, exit'%method
                sys.exit()

        clf = clf.fit(train_x, train_y)
        t2 = time.time()

	if method != 2 and mode != 0:
        	pred_y = clf.predict(test_x)
		print_fea_importance('fnames.txt', clf.feature_importances_)
	else :
		pred_y = clf.predict_proba(test_x)
		pred_y = pred_y[:,1]

	pred_y_prob = pred_y[:]
	pred_y = map(lambda x: 1 if x>=0.15 else 0, pred_y)

        #pred_y_prob = []
        #if mode == 0 :
        #        pred_y_prob = clf.predict_proba(test_x)
        #        pred_y_prob = [y[1] for y in pred_y_prob]
        t3 = time.time()

        train_size = len(train_x)
        test_size = len(test_x)
        time_str = 'train:%.2fs, predict:%.2fs; train_size:%d,vec_size:%d,test_size:%d, params:%s'%(t2-t1, t3-t2, train_size, train_x.shape[1], test_size, params)
        print_predict_res(test_y, pred_y, pred_y_prob, time_str)

	'''
        t0 = time.time()
        model_file = train_file + '.model'
        f_model = open(model_file, 'wb')
        pickle.dump(clf, f_model)
        mylog.log_trace('dump model finished: use %.2f secs'%(time.time()-t0))
	'''

        return clf

def print_predict_res(test_y, pred_y, pred_y_prob=None, time_str=''):
	res_file = 'predict.res'
        f_out = open(res_file, 'w')

	test_lines = open('feas.test.uid').readlines()
        for i,y in enumerate(pred_y) :
		if pred_y_prob is not None :
                	f_out.write('%s\t%d\t%d\t%.4f\n'%(test_lines[i].strip(), test_y[i], y, pred_y_prob[i]))
		else :
			f_out.write('%s\t%d\t%d\n'%(test_lines[i].strip(), test_y[i], y))

        f_out.close()

        mse = mean_squared_error(test_y, pred_y)
        rmse = mse ** 0.5
        res_str = 'mse=%.4f, rmse=%.4f'%(mse, rmse)

        prec = precision_score(test_y, pred_y)
        recall = recall_score(test_y, pred_y)
        f1 = f1_score(test_y, pred_y)
        acc = accuracy_score(test_y, pred_y)

	if pred_y_prob is None :
		fpr, tpr, thresholds = roc_curve(test_y, pred_y, pos_label=1)
	else :
		fpr, tpr, thresholds = roc_curve(test_y, pred_y_prob, pos_label=1)
	print type(fpr)
	f_pt = open('fpr.txt', 'w')
	f_pt.write(str(fpr.tolist()) + '\n')
	f_pt.write(str(tpr.tolist()) + '\n')
	f_pt.close()
	ax = auc(fpr, tpr)
        res_str += ', prec=%.2f%%, recall=%.2f%%, f1-score=%.2f%%, acc=%.2f%%, auc=%.3f'%(prec*100, recall*100, f1*100, acc*100, ax)

        res_str = res_str + ' use time:' + time_str
        print res_str

	f_res = open('res.txt', 'a+')
	f_res.write(res_str + '\n')
	f_res.close()

def rmse_loss(est, test_x, test_y) :
	pred_y = est.predict(test_x)
	return (mean_squared_error(test_y, pred_y) ** 0.5) * -1

def print_fea_importance(fname_file, clf_fea_imps):
        fea_list = []
        for line in open(fname_file) :
                fea_list.append(line.strip())

        print 'feature size: ', len(fea_list), len(clf_fea_imps)
        if len(fea_list) != len(clf_fea_imps) :
                print 'feature size does not match: %d != %d'%(len(fea_list), len(clf_fea_imps))
                return

        fea_imps = [(imp, fea_list[i]) for i,imp in enumerate(clf_fea_imps)]
        fea_imps = filter(lambda x: x[0] > 0.0, fea_imps)
        fea_imps.sort(reverse=True)
        fea_imps_str = '\n'.join(map(lambda x: '%d\t%.4f\t%s'%(x[0], x[1][0], x[1][1]), enumerate(fea_imps)))
        print fea_imps_str

	open('fnames.imp', 'w').write(fea_imps_str)


train_x, train_y, test_x, test_y = read_corpus('../matrix/train.csv.norm', '../matrix/test.csv.norm', -1, -1)
run_clf(train_x, train_y, test_x, test_y, method=0)