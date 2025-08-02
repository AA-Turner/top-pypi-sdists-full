import datetime
import inspect
import logging
import sys
from logging import Logger

import requests
import time

from sidecar.const import Const
import multiprocessing.pool


class Utils:
    @staticmethod
    def str_to_bool(value: str) -> bool:
        if value.lower() == 'true':
            return True
        else:
            return False

    @staticmethod
    def stop_on_debug():
        while not sys.gettrace():
            time.sleep(0.5)

    @staticmethod
    def read_log(app_name: str) -> str:
        file_path = Const.get_app_log_file(app_name)
        with open(file_path, 'r') as application_log:
            return application_log.read()

    @staticmethod
    def get_timestamp():
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def wait_for(func, interval_sec: int = 10, max_retries: int = 10, error: str = "", silent: bool = False):
        current_retry = 0
        while current_retry < max_retries:
            try:
                if func():
                    return
                else:
                    if not silent:
                        print('re-try {} out of {}'.format(current_retry, max_retries))
                    time.sleep(interval_sec)
                    current_retry += 1
                    if current_retry >= max_retries:
                        raise Exception('max retries for wait_for is exhausted with message: {}'.format(error))
            except Exception as e:
                raise Exception('wait_for function exited due to an exception: {}'.format(e))

    @staticmethod
    def retry_on_exception(func,
                           logger: Logger = None,
                           logger_msg: str = "",
                           interval_in_sec: int = 1,
                           log_every_n_attempts: int = 0,
                           timeout_in_sec: float = 10):
        start = datetime.datetime.now()
        attempt_number = 1
        while True:
            try:
                res = func()
                if logger:
                    elapsed = datetime.datetime.now() - start
                    logger.info(f"Succeeded {logger_msg} (after {elapsed.total_seconds():.3f}s and {attempt_number} attempts)")
                return res
            except requests.exceptions.ConnectionError as e:
                if "Failed to establish a new connection: [Errno -2] Name or service not known'" in str(e):
                    logger.fatal("logger shut down, no access to cloud provider.", exc_info=True)
                    Utils._reset_logger()
                    raise e
                Utils._handle_exception(attempt_number, e, logger, logger_msg, start, timeout_in_sec, interval_in_sec, log_every_n_attempts)
            except Exception as e:
                Utils._handle_exception(attempt_number, e, logger, logger_msg, start, timeout_in_sec, interval_in_sec, log_every_n_attempts)
            finally:
                time.sleep(interval_in_sec)
            attempt_number += 1

    @staticmethod
    def _handle_exception(attempt_number, ce, logger, logger_msg, start, timeout_in_sec, interval_in_sec, log_every_n_attempts):
        elapsed = datetime.datetime.now() - start
        in_seconds = int(elapsed.total_seconds())
        msg = f"Failed {logger_msg} (after {in_seconds:.3f}s and {attempt_number} attempts)"
        if in_seconds > timeout_in_sec:
            if logger:
                logger.info(f'{msg}. Giving up :(')
            raise ce
        elif log_every_n_attempts and attempt_number % log_every_n_attempts == 0:
            if logger:
                logger.info(f'{msg}. Trying again in {interval_in_sec}s ...')

    @staticmethod
    def _reset_logger():
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        logging.basicConfig()

    @staticmethod
    def convert_date_time_to_isoformat(date_time: datetime):
        return date_time.isoformat()

    @staticmethod
    def get_utc_now_in_isoformat() -> str:
        utc_now = datetime.datetime.now(datetime.timezone.utc)
        return Utils.convert_date_time_to_isoformat(utc_now)


class CallsLogger:
    logger = None

    @classmethod
    def set_logger(cls, logger):
        cls.logger = logger

    @classmethod
    def wrap(cls, func):
        def decorator(*args, **kwargs):
            bound_args = inspect.signature(func).bind(*args, **kwargs)
            bound_args.apply_defaults()

            args_list = ["{}: '{}'".format(k, v) for (k, v) in bound_args.arguments.items()]
            if len(bound_args.arguments) > 0 and bound_args.arguments.get('self'):
                args_list = args_list[1:]
            result_str = ''

            try:
                result = func(**bound_args.arguments)
                result_str = str(result)
                return result
            except Exception as e:
                result_str = str(e)
                raise
            finally:
                if cls.logger:
                    result_str = result_str if len(result_str) < 20 else result_str[:17]+'...'
                    cls.logger.info(func.__qualname__ + "(" + ", ".join(args_list) + ") -> "+result_str)

        return decorator


class TimeoutUtils:
    # This is the Timeout decorator.
    # Example of use:
    #
    # import TimeoutUtils
    # ....
    #
    # @TimeoutUtils.timeout(2)
    # def myFunc:
    # ....
    #
    @staticmethod
    def timeout(timeout_in_seconds: int):
        def timeout_decorator(func):
            def func_wrapper(*args, **kwargs):
                pool = multiprocessing.pool.ThreadPool(processes=1)
                async_result = pool.apply_async(func, args, kwargs)
                try:
                    return async_result.get(timeout_in_seconds)
                except Exception as ex:
                    raise ex
                finally:
                    pool.close()
            return func_wrapper
        return timeout_decorator
