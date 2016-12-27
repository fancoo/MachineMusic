# coding: utf-8
import ConfigParser


# 配置文件读取模块
class Config4Py:
    def __init__(self, conf_fpath):
        self.path = conf_fpath
        self.config = ConfigParser.ConfigParser()
        self.config.read(self.path)

    def get(self, section, option):
        return self.config.get(section, option)

    def getint(self, section, option):
        return self.config.getint(section, option)

    def set_conf(self, section, option, value):
        return self.config.set(section, option, value)


if __name__ == '__main__':
    pc = Config4Py('../conf/user_reply.conf')
    print pc.get('global', 'candidate_no')
