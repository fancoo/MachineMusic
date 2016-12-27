# coding: utf-8

import os
import sys
from pyconf import Config4Py


def create_path(path):
    if not os.path.exists(path):
        os.mkdirs(path)

# 模块名
module_name = 'user_reply'

# 项目根目录
# root_path = os.getcwd()
# # bin路径
# bin_path = '%s/bin' % (root_path)
# # conf路径
# conf_path = '%s/conf' % (root_path)
# # conf文件
conf_fpath = '../conf/user_reply.conf'

mypc = Config4Py(conf_fpath)

# log路径
# log_path = mypc.get('global', 'log_path')
# # 日志文件
# log_fpath = '%s/%s/%s.log' % (root_path, log_path, module_name)
# # data路径
# data_r = mypc.get('global', 'data_path')
# data_path = '%s/%s' % (root_path, data_r)
#
#
# create_path(log_path)
# create_path(data_path)
#
# # 日志级别
# log_level = mypc.getint('global', 'log.level')
# log_level_name = mypc.get('global', 'data_path')

# 业务配置
# login_file = data_path + mypc.get('global', 'login_file')
# deliver_file = data_path + mypc.get('global', 'deliver_file')
# act_file = data_path + mypc.get('global', 'act_file')

# 模型相关配置
login_days = mypc.getint('global', 'login_days')
sample_ratio = float(mypc.get('global', 'sample_ratio'))
# train_param = mypc.get('global', 'train_param')

