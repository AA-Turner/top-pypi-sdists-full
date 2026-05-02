import os
import logging
from logging.handlers import TimedRotatingFileHandler

logger_dict = {}


def get_logger(file_name=None):
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_dir = os.path.join(project_dir, 'logs')
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    if "log" in logger_dict:
        return logger_dict["log"]
    else:
        # 第一步，创建一个logger
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)  # Log等级总开关

        # 第二步，创建一个handler，用于写入日志文件
        logfile = os.path.join(log_dir, file_name or 'ChGraphLog.log')
        fh = TimedRotatingFileHandler(logfile, when='MIDNIGHT', interval=1, backupCount=30)
        fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关

        # 第三步，再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.WARNING)  # 输出到console的log等级的开关

        # 第四步，定义handler的输出格式
        formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 第五步，将logger添加到handler里面
        logger.addHandler(fh)
        logger.addHandler(ch)
        logger_dict["log"] = logger
    return logger
