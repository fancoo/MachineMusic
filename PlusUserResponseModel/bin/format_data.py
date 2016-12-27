# coding:utf-8

import time
import datetime

from logger import LoggerFactory
LoggerFactory.addLogger('P1', 'data_process_log.txt')
logger = LoggerFactory.getLogger('P1')


class UserData:
    def __init__(self, login_file, invite_file, chat_file, register_file):
        self.login_file = login_file
        self.invite_file = invite_file  # 简历邀约
        self.chat_file = chat_file  # hr聊天
        self.register_file = register_file  # 注册文件
        self.user_login = {}
        self.user_invite = {}
        self.user_chat = {}
        self.user_register = {}
        self.plus_user_register = {}

        self.parse_login_file()
        self.parse_invite_file()
        self.parse_chat_file()
        self.parse_register_file()
        self.parse_plus_user_file()

    def parse_login_file(self):
        start = time.time()
        user_login = self.user_login

        for line in open(self.login_file):
            toks = line.strip().split('\t')
            uid = int(toks[0])

            login = line.strip().split('\t')[1:]
            login = map(lambda x: x.split(':'), login)
            login = map(lambda x: (time.mktime(datetime.datetime.strptime(x[0].replace('-', ''), '%Y%m%d').timetuple()),
                                   int(x[1])), login)

            user_login[uid] = login

        logger.info('read <%d> login users from file <%s>, use time: %.2f secs' %
                    (len(user_login), self.login_file, time.time()-start))

    def parse_invite_file(self):
        start = time.time()
        user_invite = self.user_invite

        for line in open(self.invite_file):
            toks = line.strip().split('\t')
            uid = int(toks[0])
            if uid not in self.user_login:
                continue

            invite = line.strip().split('\t')[1:]
            invite = map(lambda x: x.split(':'), invite)
            invite = map(lambda x: (time.mktime(datetime.datetime.strptime(x[0], '%Y%m%d').timetuple()), int(x[1]),
                                    int(x[2]), int(x[3])), invite)
            user_invite[uid] = invite

            """
            for tok in toks[1:]:
                invite_time, response, com_scale, weekday = tok.split(':')
                time_stamp = time.mktime(datetime.datetime.strptime(invite_time, '%Y%m%d').timetuple())
                if uid in user_invite:
                    user_invite[uid].append((time_stamp, int(response), int(com_scale), int(weekday)))
                else:
                    user_invite[uid] = [(time_stamp, int(response), int(com_scale), int(weekday))]
            """
        logger.info('read <%d> invite users from file <%s>, use time: %.2f secs' %
                    (len(user_invite), self.invite_file, time.time()-start))

    def parse_chat_file(self):
        start = time.time()
        user_chat = self.user_chat

        for line in open(self.chat_file):
            toks = line.strip().split('\t')
            uid = int(toks[0])
            if uid not in self.user_login:
                continue

            chat = line.strip().split('\t')[1:]
            chat = map(lambda x: x.split(':'), chat)
            chat = map(lambda x: (time.mktime(datetime.datetime.strptime(x[0], '%Y%m%d').timetuple()), int(x[1]),
                                  int(x[2]), int(x[3])), chat)
            user_chat[uid] = chat

        logger.info('read <%d> chat users from file <%s>, use time: %.2f secs' %
                    (len(user_chat), self.chat_file, time.time()-start))

    def parse_register_file(self):
        start = time.time()
        user_register = self.user_register

        for line in open(self.register_file):
            toks = line.strip().split('\t')
            uid = int(toks[0])
            register_time = toks[2].split()[0].replace('-', '')
            # print register_time
            # 有一个异常数据，1970年注册的用户。。
            if int(register_time) < 20101225:
                register_time = '20130722'
            user_register[uid] = time.mktime(datetime.datetime.strptime(register_time, '%Y%m%d').timetuple())

        logger.info('read <%d> register users from file <%s>, use time: %.2f secs' %
                    (len(user_register), self.register_file, time.time()-start))

    def parse_plus_user_file(self):
        # 只选择invite_no > 0 or chat_no > 0 的用户当做样本
        start = time.time()
        for user in self.user_invite:
            if user not in self.user_register:
                continue
            if user not in self.plus_user_register:
                self.plus_user_register[user] = self.user_register[user]

        for user in self.user_chat:
            if user not in self.user_register:
                continue
            if user not in self.plus_user_register:
                self.plus_user_register[user] = self.user_register[user]

        logger.info('select user whose invite_no > 0 or chat_no > 0, use time: %.2f secs' %
                    (time.time()-start))


if __name__ == '__main__':
    login_file = '../raw/login_feature.txt'
    invite_file = '../raw/invite_feature.txt'
    chat_file = '../raw/chat_feature.txt'
    register_file = '../raw/user_register.txt'
    ud = UserData(login_file, invite_file, chat_file, register_file)
    ud.parse_plus_user_file()