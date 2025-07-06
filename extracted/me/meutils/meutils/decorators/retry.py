#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : retry
# @Time         : 2021/3/18 2:57 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from tenacity import retry, stop_after_attempt, before_sleep_log
from tenacity import wait_fixed, wait_exponential, wait_incrementing, wait_exponential_jitter  # Wait strategy
from tenacity import retry_if_result, RetryCallState  # 重试策略
from tenacity import retry_if_exception, retry_if_exception_type, retry_if_not_exception_type

# 不兼容异步
from meutils.notice.feishu import send_message


class IgnoredRetryException(Exception):
    pass


def default_retry_error_callback(retry_state: RetryCallState, title: Optional[str] = None):
    """return the result of the last call attempt"""
    # logger.debug(f"最后一次重试仍然失败调用的函数: {retry_state.outcome}")
    logger.debug(f"最后一次重试仍然失败调用的函数: {retry_state}")

    send_message(f"""{retry_state}""", title)

    # logger.debug(retry_state.outcome.result())

    exc = retry_state.outcome.exception()  # 最后抛出错误
    if exc:
        raise exc  # 最后返回结果


def not_in_status_codes(exception):
    """451不触发重试"""
    # logger.debug(exception)

    if isinstance(exception, httpx.HTTPStatusError):
        # logger.debug(f"status_code: {exception.response.status_code}")

        status_code = exception.response.status_code
        return status_code not in {451}
    return True


def retrying(
        max_retries=2,
        exp_base=2,
        min: int = 0,
        max: int = 100000,
        retry_error_callback: Optional[Callable[[RetryCallState], Any]] = None,
        predicate: Callable[[Any], bool] = lambda r: False,
        title: Optional[str] = None,
        ignored_exception_types: Optional[typing.Union[
            typing.Type[BaseException],
            typing.Tuple[typing.Type[BaseException], ...],
        ]] = None,  # 该错误类型不重试
):
    import logging

    logger = logging.getLogger()

    retry_error_callback = retry_error_callback or partial(default_retry_error_callback, title=title)

    # 抛错或者返回结果判断为True重试 就重试
    retry_reasons = (
            (
                    retry_if_exception_type()
                    & retry_if_exception(not_in_status_codes)
            )
            | retry_if_result(predicate)
    )
    if ignored_exception_types:
        retry_reasons = retry_reasons & retry_if_not_exception_type(ignored_exception_types)

    _retry_decorator = retry(
        reraise=True,
        stop=stop_after_attempt(max_retries),
        wait=wait_exponential(multiplier=1.0, exp_base=exp_base, min=min, max=max),  # max=max_seconds
        retry=retry_reasons,
        # before_sleep=before_sleep_log(logger, 30),
        retry_error_callback=retry_error_callback,
    )

    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        return _retry_decorator(wrapped)(*args, **kwargs)

    return wrapper


def create_retry_decorator() -> Callable[[Any], Any]:  # todo: Retrying
    """
    @create_retry_decorator()
    def fn():
        pass

    :return:
    """
    import openai
    max_retries = 3
    min_seconds = 4
    max_seconds = 10
    # Wait 2^x * 1 second between each retry starting with
    # 4 seconds, then up to 10 seconds, then 10 seconds afterwards
    return retry(
        reraise=True,
        stop=stop_after_attempt(max_retries),
        wait=wait_exponential(multiplier=1, min=min_seconds, max=max_seconds),
        retry=(
                retry_if_exception_type(openai.error.Timeout)
                | retry_if_exception_type(openai.error.APIError)
                | retry_if_exception_type(openai.error.APIConnectionError)
                | retry_if_exception_type(openai.error.RateLimitError)
                | retry_if_exception_type(openai.error.ServiceUnavailableError)
        ),
        before_sleep=before_sleep_log(logger, 30),
    )


def wait_retry(n=3):
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        @retry(wait=wait_fixed(n))
        def wait():
            logger.warning("retry")
            if wrapped(*args, **kwargs):  # 知道检测到True终止
                return True

            raise Exception

        return wait()

    return wrapper


# from meutils.cmds import HDFS
# HDFS.check_path_isexist()


if __name__ == '__main__':
    # s = time.time()  # 1616145296
    # print(s)
    # e1 = s + 10
    # e2 = e1 + 10
    #
    #
    # @wait_retry(5)
    # def f(e):
    #     return time.time() > e  # 变的
    #
    #
    # def run(e):
    #     f(e)
    #     print(f"task {e}")
    #
    #
    # # for e in [e2, e1]:
    # #     print(run(e))
    # #
    # # print("耗时", time.time() - s)
    #
    # [e1, e2, 1000000000000] | xProcessPoolExecutor(run, 2)

    # class retry_state:
    #     attempt_number = 0
    #
    #
    # for i in range(1, 10):
    #     retry_state.attempt_number = i
    #     # print(wait_incrementing(100, -10)(retry_state))
    #     print(wait_exponential(1, exp_base=2)(retry_state))

    # @retrying(3)
    # async def f():
    #     logger.debug("retry")
    #     pass
    #     # 1 / 0
    #     raise Exception('xx')

    # try:
    #     f()
    #
    # except Exception as e:
    #     print(e)
    #     print(type(e))

    # @retrying(3)
    # def f():
    #     # async def f():
    #     logger.debug("retry")
    #     for i in range(10):
    #         yield ""
    #         if i == 8:
    #             raise Exception('xx')

    # arun(f())

    # f()

    # 示例使用
    class CustomError1(Exception):
        pass


    class CustomError2(Exception):
        pass


    @retrying(
        max_retries=3,
        ignored_exception_types=(CustomError1, IgnoredRetryException)
    )
    def my_function():
        logger.debug(1)
        # 模拟抛出异常
        raise IgnoredRetryException("This is a custom error")


    def main():
        try:
            my_function()
        except Exception as e:
            print(f"Operation failed after all retries: {e}")


    main()
