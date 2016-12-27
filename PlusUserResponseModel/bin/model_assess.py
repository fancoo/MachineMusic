# coding: utf-8

import time
import datetime
import gc
import xgboost as xgb
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score, mean_squared_error, roc_curve, auc
from sklearn.cross_validation import train_test_split
import user_feature
import extract_data
import format_data
import config
import logger
import user_feature
import random
from sklearn.datasets import load_svmlight_file


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







def evaluate(pred_y, pred_y_int, test_y):
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


def train_model(train_file, model_file):
    start = time.time()

    dtrain = xgb.DMatrix(train_file)