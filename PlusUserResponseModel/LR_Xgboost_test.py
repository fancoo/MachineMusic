# coding: utf-8

import time
import sys

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
import xgboost as xgb

# def read_data(train_file, test_file):
#     start = time.time()
#     train_x, train_y = load_svmlight_file(train_file)
#     test_x, test_y = load_svmlight_file(test_file)
#
#     print('read data from corpus use time: %.2f secs' % (time.time()-start))
#     return train_x, train_y, test_x, test_y
#
# def run_grid_search(train_x, train_y, test_x, test_y):
#     param_grid = {
#         'loss': ['ls', 'lad', 'huber'],
#         'n_estimators': [100, 200, 400, 600],
#         'learning_rate': [1.0, 0.1, 0.05],
#         'max_depth': [1, 3],
#         'min_samples_leaf': [1, 3, 10],
#     }
#
#

def eval_pred(pred_y, pred_y_int, test_y):
	assert len(test_y) == len(pred_y)

	true_r = sum(test_y) * 100.0 / len(test_y)

	mse = mean_squared_error(test_y, pred_y)
	rmse = mse ** 0.5
	res_str = 'true_r=%.2f%%, mse=%.4f, rmse=%.4f' % (true_r, mse, rmse)

	prec = precision_score(test_y, pred_y_int)
	recall = recall_score(test_y, pred_y_int)
	f1 = f1_score(test_y, pred_y_int)
	acc = accuracy_score(test_y, pred_y_int)

	fpr, tpr, _ = roc_curve(test_y, pred_y, pos_label=1)
	auc_r = auc(fpr, tpr)

	res_str += ', prec=%.2f%%, recall=%.2f%%, f1-score=%.2f%%, acc=%.2f%%, auc=%.3f' % (prec * 100, recall * 100, f1 * 100, acc * 100, auc_r)
	return res_str


start = time.time()

dtrain = xgb.DMatrix('matrix/train.csv.norm')
train_size = dtrain.num_row()
print('load data finished: train_size=%d, use time: %.2f secs' % (train_size, time.time() - start))

start = time.time()
dtest = xgb.DMatrix('matrix/test.csv.norm')
test_size = dtest.num_row()
print('load data finished: test_size=%d, use time: %.2f secs' % (test_size, time.time() - start))

start = time.time()
param = {'num_round': 100, 'colsample_bytree': 0.5, 'subsample': 1, 'eta': 0.1, 'objective': 'binary:logistic', 'max_depth': 3}
plst = param.items()
plst += [('eval_metric', 'auc')]
evallist = [(dtest,'eval'), (dtrain,'train')]
bst = xgb.train(plst, dtrain, evallist, early_stopping_rounds=10)
print('train finished: use time: %.2f secs' % (time.time() - start))

start = time.time()
pred_y = bst.predict(dtest)
pred_y_int = map(lambda x: 1 if x >= 0.5 else 0, pred_y)
test_y = dtest.get_label()
eval_str = eval_pred(pred_y, pred_y_int, test_y)

importance = xgb

print ('train predict finished: train_size=%d, param=%s, best_iteration=%d/%d, eval=%s, use_time=%.2fsecs' % \
	                 (train_size, param, bst.best_iteration, param['num_round'], eval_str, time.time() - start))


