import logging
import logging.config
import os
import traceback

from mag_tools.utils.data.string_utils import StringUtils

from mag_tools.config.sys_config import SysConfig
from mag_tools.exception.app_exception import AppException
from mag_tools.enums.log_type import LogType


class Logger:
    __instance = None

    def __init__(self):
        """
        初始化 Logger 实例，配置日志记录器和日志文件路径。
        """
        log_dir = SysConfig.get('logDir')
        if log_dir is None:
            log_dir = os.path.join(SysConfig.root_dir(), 'data', 'log')


        os.makedirs(log_dir, exist_ok=True)

        logging.config.fileConfig(SysConfig.logging_conf(),
                                  encoding='utf-8',
                                  defaults={'logdir': str(log_dir)})

        self.root_logger = logging.getLogger()
        self.frame_logger = logging.getLogger('frame')
        self.dao_logger = logging.getLogger('dao')
        self.service_logger = logging.getLogger('service')
        self.performance_logger = logging.getLogger('performance')

    @classmethod
    def __get_instance(cls):
        if not cls.__instance:
            cls.__instance = cls()
        return cls.__instance

    @classmethod
    def debug(cls, *args):
        """
        记录调试级别的日志信息。

        :param args: 日志信息参数，可以是单个消息或 (logger_type, message) 元组
        """
        if len(args) == 1:
            message = args[0]
            cls.__get_instance().__debug(LogType.FRAME, message)
        elif len(args) == 2:
            log_type, message = args
            cls.__get_instance().__debug(log_type, message)
        else:
            raise ValueError("Invalid number of arguments")

    @classmethod
    def info(cls, *args):
        """
        记录信息级别的日志信息。

        :param args: 日志信息参数，可以是单个消息、(logger_type, message) 或 (logger_type, message, is_highlight) 元组
        """
        if len(args) == 1:
            message = args[0]
            cls().__info(LogType.FRAME, message)
        elif len(args) == 2:
            logger_type, message = args
            cls().__info(logger_type, message)
        elif len(args) == 3:
            logger_type, message, is_highlight = args
            if is_highlight:
                cls().__info(logger_type, '*' * (StringUtils.get_print_width(message) + 8))
                cls.__get_instance().__info(logger_type, f'*** {message} ***')
                cls.__get_instance().__info(logger_type, '*' * (StringUtils.get_print_width(message) + 8))
            else:
                cls().__info(logger_type, message)
        else:
            raise ValueError("Invalid number of arguments")

    @classmethod
    def warning(cls, *args):
        """
        记录警告级别的日志信息。

        :param args: 日志信息参数，可以是单个消息或 (logger_type, message) 元组
        """
        if len(args) == 1:
            message = args[0]
            cls.__get_instance().__warning(LogType.FRAME, message)
        elif len(args) == 2:
            logger_type, message = args
            cls.__get_instance().__warning(logger_type, message)
        else:
            raise ValueError("Invalid number of arguments")

    @classmethod
    def error(cls, *args):
        """
        记录错误级别的日志信息。

        :param args: 日志信息参数，可以是单个消息或 (logger_type, message) 元组
        """
        if len(args) == 1:
            message = str(args[0]) if isinstance(args[0], Exception) else args[0]
            cls.__get_instance().__error(LogType.FRAME, message)
        elif len(args) == 2:
            logger_type, message = args
            message = str(message) if isinstance(message, Exception) else message
            cls.__get_instance().__error(logger_type, message)
        else:
            raise ValueError("Invalid number of arguments")

    @classmethod
    def throw(cls, *args):
        Logger.error(args)

        if len(args) == 1:
            message = str(args[0]) if isinstance(args[0], Exception) else args[0]
        elif len(args) == 2:
            logger_type, message = args
            message = str(message) if isinstance(message, Exception) else message
        else:
            raise ValueError("Invalid number of arguments")

        raise AppException(message)

    def __debug(self, logger_type: LogType, message: str):
        """
        内部方法，记录调试级别的日志信息。

        :param logger_type: 日志类型
        :param message: 日志消息
        """
        self.root_logger.debug(message)

        if logger_type == LogType.FRAME:
            self.frame_logger.debug(message)
        elif logger_type == LogType.DAO:
            self.dao_logger.debug(message)
        elif logger_type == LogType.SERVICE:
            self.service_logger.debug(message)
        elif logger_type == LogType.PERFORMANCE:
            self.performance_logger.debug(message)

    def __info(self, logger_type: LogType, message: str):
        """
        内部方法，记录信息级别的日志信息。

        :param logger_type: 日志类型
        :param message: 日志消息
        """
        self.root_logger.info(message)

        if logger_type == LogType.FRAME:
            self.frame_logger.info(message)
        elif logger_type == LogType.DAO:
            self.dao_logger.info(message)
        elif logger_type == LogType.SERVICE:
            self.service_logger.info(message)
        elif logger_type == LogType.PERFORMANCE:
            self.performance_logger.info(message)

    def __warning(self, logger_type: LogType, message: str):
        """
        内部方法，记录警告级别的日志信息。

        :param logger_type: 日志类型
        :param message: 日志消息
        """
        self.root_logger.warning(message)

        if logger_type == LogType.FRAME:
            self.frame_logger.warning(message)
        elif logger_type == LogType.DAO:
            self.dao_logger.warning(message)
        elif logger_type == LogType.SERVICE:
            self.service_logger.warning(message)
        elif logger_type == LogType.PERFORMANCE:
            self.performance_logger.warning(message)

    def __error(self, logger_type: LogType, message: str):
        """
        内部方法，记录错误级别的日志信息。

        :param logger_type: 日志类型
        :param message: 日志消息
        """
        error_message = f"{message}\n{traceback.format_exc()}"
        self.root_logger.error(error_message)

        if logger_type == LogType.FRAME:
            self.frame_logger.error(error_message)
        elif logger_type == LogType.DAO:
            self.dao_logger.error(error_message)
        elif logger_type == LogType.SERVICE:
            self.service_logger.error(error_message)
        elif logger_type == LogType.PERFORMANCE:
            self.performance_logger.error(error_message)