# coding:utf-8
import datetime
import time


SCALE = {
    '未融资': 1,
    '天使轮': 2,
    'A轮': 3,
    'B轮': 4,
    'C轮': 5,
    'D轮及以上': 6,
    '上市公司': 7,
    '不需要融资': 8
}

RESUME_STATUS = {
    'WAIT': 0,
    'DEAL': 1,
    'DELIVER': 1
}


# change data from 1403040254 to 2016-1-1 22:10
def date_change(fin, fout):
    ctime_file = open(fin, 'r')
    date_file = open(fout, 'w')
    for line in ctime_file:
        toks = line.split()
        uid = toks[0]
        time_stamp = toks[1:]
        date_time = []
        if len(time_stamp):
            for item in time_stamp:
                print item
                date_num = int(item) / 1000
                ltime = time.localtime(date_num)
                timeStr = time.strftime("%Y%m%d %H:%M:%S", ltime)
                date_time.append(timeStr)
        date_str = '\t'.join(date_time)
        date_file.write(uid + '\t' + date_str + '\n')
    date_file.close()
    ctime_file.close()


# change hrid from 4503599627370496 to 23345.
def convert_hrid(chat_file, out_file):
    cf = open(chat_file, 'r')
    of = open(out_file, 'w')
    for line in cf:
        line = line.strip()
        toks = line.split('\t')
        hrid = int(toks[0])
        if 4503599627370496 < hrid < 9000000000000000:
            hrid -= 2 ** 52
            toks[0] = str(int(hrid))
        line_str = '\t'.join(str(i) for i in toks)
        of.write(line_str + '\n')
    of.close()
    cf.close()


# change login_record.txt to {'uid':((time1, times), (time2, times),...)...)
def user_login(raw, out):
    fin = open(raw, 'r')
    fout = open(out, 'w')
    for line in fin:
        toks = line.strip().split('\t')
        uid = toks[0]
        time_list = toks[1:]
        time_count = {}
        for i in time_list:
            date = int(i.split()[0])
            if date not in time_count:
                time_count[date] = 0
            time_count[date] += 1
        time_sequence = sorted(time_count.items(), lambda x, y: cmp(x[0], y[0]))
        # print time_sequence
        cout_str = '\t'.join('%s:%d' % (val[0], val[1]) for val in time_sequence)
        fout.write(uid + '\t' + cout_str + '\n')


# invite data structure
def invite_feature(invite_record, position_com, out):
    f1 = open(invite_record, 'r')
    f2 = open(position_com, 'r')
    fout = open(out, 'w')
    position_dict = {}
    invite_dict = {}
    for line in f2:
        toks = line.strip().split('\t')
        # print toks
        if len(toks) < 3:
            continue
        pid = toks[0]
        com_stage = toks[2]
        if com_stage not in SCALE:
            position_dict[pid] = 1
        else:
            position_dict[pid] = SCALE[com_stage]

    for line in f1:
        toks = line.strip().split()
        uid = toks[1]
        position_id = toks[2]
        if position_id not in position_dict:
            print position_id
            position_dict[position_id] = 1
        com_stage = position_dict[position_id]
        receive_time = toks[4]
        date_format = datetime.date.fromtimestamp(time.mktime(time.strptime(receive_time, "%Y-%m-%d")))
        weekday = datetime.datetime.weekday(date_format) + 1   # 当天是星期几
        time_int = int(receive_time.replace('-', ''))
        resume_status = RESUME_STATUS[toks[3]]
        if uid in invite_dict:
            invite_dict[uid].append((time_int, resume_status, com_stage, weekday))
        else:
            invite_dict[uid] = [(time_int, resume_status, com_stage, weekday)]

        invite_sequence = sorted(invite_dict[uid], lambda x, y: cmp(x[0], y[0]))
        d_str = '\t'.join('%d:%d:%d:%d' % (x[0], x[1], x[2], x[3]) for x in invite_sequence)
        fout.write('%s\t%s\n' % (uid, d_str))
    fout.close()
    f2.close()
    f1.close()


def chat_feature(chat_file, position_file, company_file, out_file):
    fpos = open(position_file, 'r')
    fcom = open(company_file, 'r')
    fchat = open(chat_file, 'r')
    fout = open(out_file, 'w')

    hr_dict = {}
    for line in fpos:
        toks = line.strip().split()
        assert len(toks) == 3
        com_id = toks[1]
        hr_id = toks[2]
        hr_dict[hr_id] = com_id

    com_stage = {}
    for line in fcom:
        toks = line.strip().split()
        if len(toks) != 2:
            continue
        com_id = toks[0]
        if toks[1] not in SCALE:
            continue
        com_stage[com_id] = SCALE[toks[1]]

    # merge hr_dict with com_stage
    hr_stage = {}
    for hr_id in hr_dict:
        com_id = hr_dict[hr_id]
        if com_id in com_stage:
            hr_stage[hr_id] = com_stage[com_id]

    # build feature
    chat_dict = {}
    for line in fchat:
        toks = line.strip().split()
        assert len(toks) == 5
        uid = toks[1]
        hr_id = str(int(toks[0]) - 2 ** 52)
        if hr_id in hr_stage:
            com_stage = hr_stage[hr_id]
        else:
            com_stage = str(1)
        receive_time = toks[3]
        date_format = datetime.date.fromtimestamp(time.mktime(time.strptime(receive_time, "%Y-%m-%d")))
        weekday = datetime.datetime.weekday(date_format) + 1   # 当天是星期几
        time_int = int(receive_time.replace('-', ''))
        chat_status = (int(toks[2]) > 0) or 0
        if uid in chat_dict:
            chat_dict[uid].append((time_int, int(chat_status), int(com_stage), weekday))
        else:
            chat_dict[uid] = [(time_int, int(chat_status), int(com_stage), weekday)]

        chat_sequence = sorted(chat_dict[uid], lambda x, y: cmp(x[0], y[0]))
        d_str = '\t'.join('%d:%d:%d:%d' % (x[0], x[1], x[2], x[3]) for x in chat_sequence)
        fout.write('%s\t%s\n' % (uid, d_str))

    fout.close()

if __name__ == '__main__':
    # fin = 'raw/logindata.txt'
    # fout = 'raw/login_record.txt'
    # date_change(fin, fout)
    # fin = 'raw/login_record.txt'
    # fout = 'raw/login_feature.txt'
    # user_login(fin, fout)
    # f1 = 'raw/resume_invite.txt'
    # f2 = 'raw/position_id_to_com_scale.txt'
    # fout = 'raw/invite_feature.txt'
    # invite_feature(f1, f2, fout)
    # chat_file = 'raw/chat_session_raw.txt'
    # out_file = 'chat_session.txt'
    # convert_hrid(chat_file, out_file)
    f1 = 'raw/chat_session_raw.txt'
    f2 = 'raw/position.txt'
    f3 = 'raw/company.txt'
    fout = 'raw/chat_feature.txt'
    chat_feature(f1, f2, f3, fout)
