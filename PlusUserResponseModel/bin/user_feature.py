# coding: utf-8

import math
import datetime


class FeatureBuild:
    def __init__(self):
        self.vector = [0] * 100
        self.vi = 0

        self.feature_name = [''] * 100  # feature name
        self.flag = 1

    def add(self, value, fname):
        self.vector[self.vi] = value

        if self.flag:
            self.feature_name[self.vi] = fname

        self.vi += 1

    def save_feature_name(self, feature_name_file):
        fn = filter(lambda x: x != '', self.feature_name)
        fn = map(lambda x: '%d\t%s' % (x[0], x[1]), enumerate(fn))
        fnf = open(feature_name_file, 'w')
        fnf.write('\n'.join(fn))

    def clear(self):
        self.vector = [0] * 100
        self.vi = 0

    def make_user_feature(self, invite_record, chat_record, login_record, register_time, date):
        """
        calculate feature matrix for certain user,certain date
        """
        descs = 86400
        all_invite_no = len(invite_record)
        all_chat_no = len(chat_record)
        all_login_no = len(login_record)

        # 最近30天数据
        month_invite_record = [x for x in invite_record if x[0] >= date - 30]
        month_chat_record = [x for x in chat_record if x[0] >= date - 30]
        month_login_record = [x for x in login_record if x[0] >= date - 30]

        # 最近7天数据
        week_invite_record = [x for x in invite_record if x[0] >= date - 7]
        week_chat_record = [x for x in chat_record if x[0] >= date - 7]
        week_login_record = [x for x in login_record if x[0] >= date - 7]

        if register_time > date:
            return []

        self.clear()

        # 距离注册天数
        day_no = (date - register_time) / descs + 1
        self.add(math.log(day_no + 1, 2), 'days_from_register_log')

        login_no = 0
        if len(login_record) > 0:
            login_no = reduce(lambda x, y: x + y, map(lambda x: x[1], login_record))

        #########
        # 总的统计
        #########
        # [次数]之前收到邀约数&收到消息数&登录次数
        self.add(math.log(all_invite_no + 1, 2), 'invite_no_log')
        self.add(math.log(all_chat_no + 1, 2), 'chat_no_log')
        self.add(math.log(login_no + 1, 2), 'login_no_log')

        # [平均次数]之前平均每天登录次数
        self.add(login_no * 1.0 / day_no, 'avg_login_no')

        # [天数]之前收到邀约天数&收到消息天数&登录天数
        invite_date_list = []
        for item in invite_record:
            if item[0] not in invite_date_list:
                invite_date_list.append(item[0])
        invite_days_no = len(invite_date_list)

        chat_date_list = []
        for item in chat_record:
            if item[0] not in chat_date_list:
                chat_date_list.append(item[0])
        chat_days_no = len(chat_date_list)

        self.add(invite_days_no, 'invite_days_no')
        self.add(chat_days_no, 'chat_days_no')
        self.add(all_login_no, 'login_days_no')

        # # [平均天数]之前收到邀约&消息&登录的平均天数
        # self.add(all_invite_no * 1.0 / day_no, 'avg_invite_day_no')
        # self.add(all_chat_no * 1.0 / day_no, 'avg_chat_day_no')
        # self.add(all_login_no * 1.0 / day_no, 'avg_login_day_no')

        # [回应数]总邀约回应数&消息回应数
        reply_invite_record = [x for x in invite_record if x[1] == 1]
        reply_chat_record = [x for x in chat_record if x[1] == 1]
        reply_invite_no = len(reply_invite_record)
        reply_chat_no = len(reply_chat_record)

        self.add(reply_invite_no, 'invite_reply_no')
        self.add(reply_chat_no, 'chat_reply_no')

        # [回应率]总邀约回应率&消息回应率
        self.add(reply_invite_no * 1.0 / all_invite_no if all_invite_no > 0 else 0.1, 'invite_reply_per')
        self.add(reply_chat_no * 1.0 / all_chat_no if all_chat_no > 0 else 0.6, 'chat_reply_per')

        ########
        # [最近一个月]
        ########
        month_invite_no = len(month_invite_record)
        month_chat_no = len(month_chat_record)
        month_login_no = len(month_login_record)

        # [最近一个月收到]消息数&邀约数&登录数
        self.add(math.log(month_invite_no + 1, 2), 'month_invite_no_log')
        self.add(math.log(month_chat_no + 1, 2), 'month_chat_no_log')
        self.add(math.log(month_login_no + 1, 2), 'month_login_no_log')

        # [最近一个月回应]回应邀约数&回应消息数
        month_reply_invite = [x for x in month_invite_record if x[1] == 1]
        month_reply_chat = [x for x in month_chat_record if x[1] == 1]
        month_reply_invite_no = len(month_reply_invite)
        month_reply_chat_no = len(month_reply_chat)

        self.add(math.log(month_reply_invite_no + 1, 2), 'month_invite_reply_no_log')
        self.add(math.log(month_reply_chat_no + 1, 2), 'month_chat_reply_no_log')

        # [最近一个月回应率]邀约回应率&消息回应率
        self.add(month_reply_invite_no * 1.0 / month_invite_no if month_invite_no > 0 else 0.1, 'month_invite_reply_per')
        self.add(month_reply_chat_no * 1.0 / month_chat_no if month_chat_no > 0 else 0.6, 'month_chat_reply_per')

        ########
        # [最近一周]
        ########
        week_invite_no = len(week_invite_record)
        week_chat_no = len(week_chat_record)
        week_login_no = len(week_login_record)

        # [最近一周收到]消息数&邀约数&登录数
        self.add(math.log(week_invite_no + 1, 2), 'week_invite_no_log')
        self.add(math.log(week_chat_no + 1, 2), 'week_chat_no_log')
        self.add(math.log(week_login_no + 1, 2), 'week_login_no_log')

        # [最近一周回应]回应邀约数&回应消息数
        week_reply_invite = [x for x in week_invite_record if x[1] == 1]
        week_reply_chat = [x for x in week_chat_record if x[1] == 1]
        week_reply_invite_no = len(week_reply_invite)
        week_reply_chat_no = len(week_reply_chat)

        self.add(math.log(week_reply_invite_no + 1, 2), 'week_invite_reply_no_log')
        self.add(math.log(week_reply_chat_no + 1, 2), 'week_chat_reply_no_log')

        # [最近一周回应率]邀约回应率&消息回应率
        self.add(week_reply_invite_no * 1.0 / week_invite_no if week_invite_no > 0 else 0.1, 'week_invite_reply_per')
        self.add(week_reply_chat_no * 1.0 / week_chat_no if week_chat_no > 0 else 0.6, 'week_chat_reply_per')

        ###########
        # [最近一次]
        ###########
        # 距离最近一次收到邀约&消息天数&登录天数
        last_invite_days = (date - invite_record[-1][0]) / descs + 1 if all_invite_no > 0 else day_no
        last_chat_days = (date - chat_record[-1][0]) / descs + 1 if all_chat_no > 0 else day_no
        last_login_days = (date - login_record[-1][0]) / descs + 1 if all_login_no > 0 else day_no

        self.add(math.log(last_invite_days, 2), 'days_from_last_invite_log')
        self.add(math.log(last_chat_days, 2), 'days_from_last_chat_log')
        self.add(math.log(last_login_days, 2), 'days_from_last_login_log')

        # [最近一次]距离最近一次回应邀约&消息天数
        last_reply_invite_days = (date - reply_invite_record[-1][0]) / descs + 1 if reply_invite_no > 0 else day_no
        last_reply_chat_days = (date - reply_chat_record[-1][0]) / descs + 1 if reply_chat_no > 0 else day_no

        self.add(math.log(last_reply_invite_days, 2), 'days_from_last_invite_reply_log')
        self.add(math.log(last_reply_chat_days, 2), 'days_from_last_chat_reply_log')

        # ###########
        # # [上上次]
        # ###########
        # #  [收到]上上次收到邀约&消息&登录天数
        # days_from_last_2_invite = (date - invite_record[-2][0]) / descs + 1 if all_invite_no > 1 else day_no
        # days_from_last_2_chat = (date - invite_record[-2][0]) / descs + 1 if all_chat_no > 1 else day_no
        # days_from_last_2_login = (date - invite_record[-2][0]) / descs + 1 if all_login_no > 1 else day_no
        #
        # self.add(math.log(days_from_last_2_invite, 2), 'days_from_last_2_invite_log')
        # self.add(math.log(days_from_last_2_chat, 2), 'days_from_last_2_chat_log')
        # self.add(math.log(days_from_last_2_login, 2), 'days_from_last_2_login_log')
        #
        #
        #
        #
        # days_between_last_2_invite = (date - invite_record[-2][0]) / descs + 1 if all_invite_no > 0 else day_no
        # last_chat_days = (date - chat_record[-1][0]) / descs + 1 if all_chat_no > 0 else day_no
        # last_login_days = (date - login_record[-1][0]) / descs + 1 if all_login_no > 0 else day_no
        #
        # self.add(math.log(last_invite_days, 2), 'days_from_last_invite_log')
        # self.add(math.log(last_chat_days, 2), 'days_from_last_chat_log')
        # self.add(math.log(last_login_days, 2), 'days_from_last_login_log')
        #
        # # [回应]上上次回应邀约&消息天数
        # last_reply_invite_days = (date - reply_invite_record[-1][0]) / descs + 1 if reply_invite_no > 0 else day_no
        # last_reply_chat_days = (date - reply_chat_record[-1][0]) / descs + 1 if reply_chat_no > 0 else day_no
        #
        # self.add(math.log(last_reply_invite_days, 2), 'days_from_last_invite_reply_log')
        # self.add(math.log(last_reply_chat_days, 2), 'days_from_last_chat_reply_log')

        # 公司特征(共8维，未融资,天使轮,A轮,B轮,C轮,D轮及以上,上市公司,不需要融资)  [暂时不加]

        # 结合统计公式的值
        base = 0.5
        a = 0.5
        b = 0.7
        c = 0.6
        d = 4
        lamb = 0.6

        user_socre = 0
        if all_invite_no == 0 and all_chat_no == 0:
            user_score = 0
        elif (all_invite_no == 0 and all_chat_no != 0) or (all_invite_no != 0 and all_chat_no == 0):
            reply_percent = float(reply_invite_no + reply_chat_no) / float(all_invite_no + all_chat_no)
            user_score = (base + a * reply_percent)/(b + c * math.log(1 + all_invite_no + all_chat_no - reply_invite_no - reply_chat_no, d))

        else:
            reply_resume_percent = float(reply_invite_no) / float(all_invite_no)
            reply_msg_percent = float(reply_chat_no) / float(all_chat_no)
            user_score = (base + a * (lamb * reply_resume_percent + (1-lamb) * reply_msg_percent))/(b + c * math.log(1 + all_invite_no + all_chat_no - reply_invite_no - reply_chat_no, d))
        self.add(user_score, 'user_score_based_statistics')

        # 当天星期几
        weekday = datetime.datetime.fromtimestamp(date).strftime('%w')
        weekday = int(weekday)
        self.add(weekday, 'weekday')

        vi = self.vi
        vector = filter(lambda x: x[1] != 0, enumerate(self.vector[:vi]))

        return vector

