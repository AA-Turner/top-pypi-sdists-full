#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : contextmanagers
# @Time         : 2024/1/9 08:36
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.notice.feishu import send_message_for_try_catch

from contextlib import contextmanager, asynccontextmanager
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError


@contextmanager
def timer(task="Task"):
    """https://www.kaggle.com/lopuhin/mercari-golf-0-3875-cv-in-75-loc-1900-s
        # 其他装饰器可学习这种写法
        with timer() as t:
            time.sleep(3)

        @timer()
        def f():
            print('sleeping')
            time.sleep(6)
            return 6
    """

    logger.info(f"{task} started")
    s = time.perf_counter()
    yield
    e = time.perf_counter()
    logger.info(f"{task} done in {e - s:.3f} s")


@contextmanager
def try_catcher(task="Task", fallback: Callable = None, is_trace: bool = False):
    try:
        yield
    except Exception as e:
        error = traceback.format_exc() if is_trace else e
        logger.error(f"{task}: {error}")
        if fallback:
            yield fallback()


@asynccontextmanager
async def atry_catcher(task="Task", fallback: Callable = None, is_trace: bool = False):
    try:
        yield
    except Exception as e:
        error = traceback.format_exc() if is_trace else e
        logger.error(f"{task}: {error}")

        if fallback:
            yield await fallback()


@contextmanager
def timeout_task_executor(timeout: float = 3, max_workers: int = None):
    """
    一个上下文管理器，用于执行任务并设置超时时间。
    :param timeout: 超时时间（秒）。
    :param max_workers: 线程池的最大工作线程数，默认为 None（由系统决定）。
    """
    executor = ThreadPoolExecutor(max_workers=max_workers)

    def execute_task(task: Callable[[], Any]) -> Any:
        """
        在上下文中执行任务，并设置超时时间。
        :param task: 要执行的任务函数。
        :return: 任务的结果。如果超时，抛出 TimeoutError。
        """
        future = executor.submit(task)
        try:
            return future.result(timeout=timeout)
        except TimeoutError:
            logger.error(f"Task was terminated due to timeout after {timeout} seconds.")
            return None

    try:
        yield execute_task  # 返回一个可调用对象，用于执行任务
    finally:
        executor.shutdown(wait=False)  # 不等待未完成的任务，直接关闭


@asynccontextmanager
async def atry_catcher(task="Task", fallback: Callable = None, is_trace: bool = False):
    try:
        yield
    except Exception as e:
        error = traceback.format_exc() if is_trace else e
        logger.error(f"{task}: {error}")
        if fallback:
            yield await fallback()


@asynccontextmanager
async def atry_catch(
        task: Optional[str] = None,
        callback: Optional[Callable] = None,
        is_trace: bool = False,  # 变量必须用
        **kwargs,
):
    try:
        yield
    except Exception as e:
        task = task or "Unnamed TryCatch Task"

        callback = callback or send_message_for_try_catch

        data = {
            "task": task,
            "error": f"""{traceback.format_exc()}""" if is_trace else f"{e}"
        }
        for k, v in kwargs.items():
            if isinstance(v, BaseModel):
                v = v.model_dump(exclude_none=True)

            if ";base64," not in str(v):  # 忽略base64
                data[k] = v

        # logger.debug(data)

        callback(data)
        raise


@contextmanager
def try_catch(
        task: Optional[str] = None,
        callback: Optional[Callable] = None,
        is_trace: bool = False,
        **kwargs,
):
    try:
        yield
    except Exception as e:
        task = task or "Unnamed TryCatch Task"

        callback = callback or send_message_for_try_catch

        data = {
            "task": task,
            "error": f"""{traceback.format_exc()}""" if is_trace else f"{e}"

        }
        for k, v in kwargs.items():
            if isinstance(v, BaseModel):
                v = v.model_dump(exclude_none=True)
            data[k] = v

        # logger.debug(data)

        callback(data)
        raise


if __name__ == '__main__':
    # async def f():
    #     return 1/0
    #
    #
    # with try_catcher("test"):
    #     arun(f())

    # def example_task():
    #     print("Starting task...")
    #     time.sleep(4)  # 模拟耗时任务
    #     print("Task completed!")
    #     return "Done"
    #
    #
    # with timeout_task_executor(timeout=3) as execute:
    #     try:
    #         result = execute(example_task)
    #         print(f"Task result: {result}")
    #     except TimeoutError:
    #         print("Task did not complete in time.")
    async def main():
        async with atry_catch("test", a=1):
            1 / 0


    arun(main())
