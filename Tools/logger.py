import logging
import time
import os

class Logger(object):
    def __init__ ( self, name: object = None ) -> object:
        # 创建一个logger
        print("logger init!")
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # 创建日志目录、名称
        rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
        # os.getcwd()获取当前文件的路径，os.path.dirname()获取指定文件路径的上级路径
        log_path = os.path.dirname(os.getcwd())+'\\Logs\\'
        if not os.path.isdir(log_path):
            os.makedirs(log_path)
        log_name = log_path + rq + '.log'

        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(log_name)
        fh.setLevel(logging.DEBUG)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
        # 关闭打开的文件
        fh.close()
        ch.close()

    def getlog ( self ):
        return self.logger