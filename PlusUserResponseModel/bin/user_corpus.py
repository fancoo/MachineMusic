# coding: utf-8

import random
import time
import config
import format_data
import user_feature
import datetime

from logger import LoggerFactory
LoggerFactory.addLogger('P1', 'user_corpus_log.txt')
logger = LoggerFactory.getLogger('P1')

"""
拿到每个用户60天之前~昨天的历史数据当做训练样本,今天的数据当做测试样本。
"""


def make_user_corpus(feature, user_invite, register_date, user_login, user_chat, date, day_no):
    """为给定用户构造语料(包括确定其正负样本属性）"""
    # feature -- 特征构造对象
    # user_invite -- 收到邀约记录
    # register_date -- 用户注册时间
    # user_login -- 用户登录记录
    # user_chat -- 用户聊天记录
    # date -- 日期
    # day_no -- 天数

    vecs = []
    labels = []

    dsecs = 86400
    invite_cursor = 0  # 收到邀约的游标
    chat_cursor = 0    # 聊天游标
    login_cursor = 0   # 登录游标
    start_d = date - day_no * dsecs

    for i in xrange(day_no):
        curr_d = start_d + i * dsecs
        if curr_d < register_date:
            continue

        # 游标移动到该天
        while invite_cursor < len(user_invite) and user_invite[invite_cursor][0] < curr_d:
            invite_cursor += 1

        while chat_cursor < len(user_chat) and user_chat[chat_cursor][0] < curr_d:
            chat_cursor += 1

        while login_cursor < len(user_login) and user_login[login_cursor][0] < curr_d:
            login_cursor += 1

        label = 0
        # 统计当天的反馈率
        curr_invite = [x[1] for x in user_invite if x[0] == curr_d]
        curr_chat = [x[1] for x in user_chat if x[0] == curr_d]
        curr_reply_invite = [x[1] for x in user_invite if x[0] == curr_d and x[1] == 1]
        curr_reply_chat = [x[1] for x in user_chat if x[0] == curr_d and x[1] == 1]

        """
        if len(curr_invite) != 0 or len(curr_chat) != 0:
            # 1. 回应率大于0.5才行
            reply_percent = float((len(curr_reply_chat) + len(curr_reply_invite))) / (len(curr_invite) + len(curr_chat))
            # 当天邀约聊天总回应率>=0.5记为正样本
            if reply_percent >= 0.5:
                label = 1
        """

        # 2. 当天只要回应了就行
        if len(curr_reply_invite) or len(curr_reply_chat):
            label = 1

        if label == 0 and random.random() > config.sample_ratio:   # 负例按概率随机取样（负例太多了，舍弃一些）
            continue

        previous_invite_record = user_invite[:invite_cursor - 1] if invite_cursor > 0 else []
        previous_chat_record = user_chat[:chat_cursor - 1] if chat_cursor > 0 else []
        previous_login_record = user_login[:login_cursor - 1] if login_cursor > 0 else []

        vec = feature.make_user_feature(previous_invite_record, previous_chat_record, previous_login_record, register_date, curr_d)
        vecs.append(vec)
        labels.append(label)

    return labels, vecs


def make_train_corpus(feature, ud, curr_d, out_file):
    # 构造训练语料, 用于train模型
    # ud -- user-data

    start = time.time()

    user_invite = ud.user_invite
    user_chat = ud.user_chat
    user_login = ud.user_login
    plus_user_register = ud.plus_user_register

    sample_no = 0
    f_out = open(out_file, 'w')

    # 对每个用户，拿到他在最近60天每天的(共计60个)特征矩阵, labels, vecs.
    for user, register_date in plus_user_register.iteritems():
        login_record = user_login[user] if user in user_login else []
        chat_record = user_chat[user] if user in user_chat else []
        invite_record = user_invite[user] if user in user_invite else []

        labels, vecs = make_user_corpus(feature, invite_record, register_date, login_record, chat_record, curr_d, config.login_days)
        assert len(labels) == len(vecs)

        for i, vec in enumerate(vecs):
            label = labels[i]
            vec_str = map(lambda x: '%d:%.3f' % (x[0], x[1]), vec)
            vec_str = ' '.join(vec_str)
            f_out.write('%d %s\n' % (label, vec_str))
        sample_no += len(vecs)

    f_out.close()
    logger.info('create train corpus finished: <%d> samples, <%d> users, <%d> days, uses time: %.2f secs' % \
                (sample_no, len(plus_user_register), config.login_days, time.time() - start))


def make_predict_corpus(feature, ud, curr_d, out_file):
    # 构造预测语料， 预测用户在当前日期的投递意愿
    start = time.time()

    user_invite = ud.user_invite
    user_chat = ud.user_chat
    user_login = ud.user_login
    plus_user_register = ud.plus_user_register

    f_out = open(out_file, 'w')
    f_uid = open("userid.txt", 'w')
    for user, register_date in plus_user_register.iteritems():
        login_record = user_login[user] if user in user_login else []
        chat_record = user_chat[user] if user in user_chat else []
        invite_record = user_invite[user] if user in user_invite else []

        pass


def main():
    login_file = '../raw/login_feature.txt'
    invite_file = '../raw/invite_feature.txt'
    chat_file = '../raw/chat_feature.txt'
    register_file = '../raw/user_register.txt'
    feature_name_file = '../raw/feature_name.txt'
    ud = format_data.UserData(login_file, invite_file, chat_file, register_file)
    uf = user_feature.FeatureBuild()
    curr_d = time.mktime(datetime.datetime.strptime('20161125', '%Y%m%d').timetuple())
    out_file = '../data/train_data.csv'
    make_train_corpus(uf, ud, curr_d, out_file)
    uf.save_feature_name(feature_name_file)


if __name__ == '__main__':
    main()