#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : common
# @Time         : 2021/9/10 上午10:45
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  :
import os
import sys
import time
import wrapt
import asyncio
import inspect
import schedule
import threading
import traceback
import importlib

from loguru import logger
from tqdm.auto import tqdm
from functools import wraps
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from contextlib import contextmanager, asynccontextmanager
from typing import *
# ME
from meutils.decorators.decorator import decorator


@decorator
def clear_cuda_cache(func, device='cuda', bins=1, *args, **kwargs):  # todo: 后端运行
    """

    :param device:
    :param bins: 每次都清，bins=2表示每隔一秒（每两秒）一清
    :param args:
    :param kwargs:
    :return:
    """
    if int(time.time()) % bins == 0:
        import torch
        if torch.cuda.is_available():
            with torch.cuda.device(device):  # torch.cuda.current_device()
                torch.cuda.empty_cache()
                torch.cuda.ipc_collect()

        elif torch.backends.mps.is_available():
            try:
                from torch.mps import empty_cache
                empty_cache()
            except Exception as e:
                logger.warning(f"仅支持pytorch2.x: {e}")
    return func(*args, **kwargs)


@decorator
def return2log(func, sink=sys.stderr, logkwargs=None, *args, **kwargs):
    """
        from asgiref.sync import sync_to_async

        @sync_to_async
        def sink(m):
            time.sleep(3)
            print(m)

        @return2log(sink=sink)
        def f(x):
            return x
    """
    if logkwargs is None:
        logkwargs = {}
    logger.remove()
    logger.add(sink, enqueue=True, **logkwargs)
    _ = func(*args, **kwargs)
    logger.info(_)
    return func(*args, **kwargs)


@contextmanager
def timer(task="Task", notice_fn: Optional[Callable] = None):
    """https://www.kaggle.com/lopuhin/mercari-golf-0-3875-cv-in-75-loc-1900-s
        # 其他装饰器可学习这种写法
        with timer() as t:
            time.sleep(3)

        @timer()
        def f():
            print('sleeping')
            time.sleep(6)
            return 6


        from meutils.notice import feishu
        feishu.send_message
    """

    logger.info(f"{task} started")
    s = time.perf_counter()
    yield
    e = time.perf_counter()
    msg = f"{task} done in {e - s:.3f} s"
    logger.info(msg)  # feishu

    # notice
    if notice_fn: notice_fn(msg)


@asynccontextmanager
async def async_timer(task="Task", notice_fn: Optional[Callable] = None):
    """
    Async context manager for timing tasks.

    Usage:
    ```python
    async with async_timer() as t:
        await asyncio.sleep(3)

    @async_timer()
    async def f():
        print('sleeping')
        await asyncio.sleep(6)
        return 6
    ```
    """
    logger.info(f"{task} started")
    s = time.perf_counter()
    yield
    e = time.perf_counter()
    msg = f"{task} done in {e - s:.3f} s"
    logger.info(msg)  # feishu

    # notice
    if notice_fn:
        await notice_fn(msg)


@contextmanager
def tryer(task, is_trace=False):
    try:
        yield
    except Exception as e:
        error = traceback.format_exc() if is_trace else e
        logger.error(error)


@decorator
def do_nothing(func, *args, **kwargs):
    return func(*args, **kwargs)


@decorator
def timeout(func, seconds=1, *args, **kwargs):
    future = ThreadPoolExecutor(1).submit(func, *args, **kwargs)
    return future.result(timeout=seconds)


@decorator
def fork(task, *args, **kwargs):
    """
    def task():
        logger.info(f"task进程：{os.getpid()}")

        for i in range(10) | xtqdm:
            time.sleep(1)
    fork(task)()
    """
    logger.info(f"父进程：{os.getppid()}")

    pid = os.fork()

    if pid < 0:
        logger.error("子进程建立失败")
    elif pid == 0:  # 在子进程中的返回值
        task(*args, **kwargs)
        logger.info(f"{task.__name__} 进程：{os.getpid()}")
    else:  # 在父进程中的返回值
        task(*args, **kwargs)
        logger.info(f"{task.__name__} 进程：{os.getpid()}")


@decorator
def pylock(func, lock=threading.Lock(), *args, **kwargs):
    """https://baijiahao.baidu.com/s?id=1714105650396326932&wfr=spider&for=pc"""
    with lock:
        # lock.acquire()
        _ = func(*args, **kwargs)
        # lock.release()
        return _


@decorator
def timeout(func, seconds=1, *args, **kwargs):
    future = ThreadPoolExecutor(1).submit(func, *args, **kwargs)
    return future.result(timeout=seconds)


@decorator
def background_task(func, max_workers=1, *args, **kwargs):
    # pool.shutdown(wait=False)  # 不等待
    # pool.shutdown(wait=True)  # 等待

    # with ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix='🐶') as pool: # 失去异步效果
    pool = ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix='🐶')
    future = pool.submit(func, *args, **kwargs)  # pool.map(fun4, ips)
    future.add_done_callback(
        lambda x: logger.error(f"future.exception()\n{traceback.format_exc()}") if future.exception() else None
    )
    # future.add_done_callback()

    # pool.shutdown(wait=False)  # 不等待

    return future.running()  # future.done()


background = background_task


@decorator
def background_task_plus(func, *args, **kwargs):
    pool = ThreadPoolExecutor(max_workers=1, thread_name_prefix='🐶')
    future = pool.submit(func, *args, **kwargs)  # pool.map(fun4, ips)
    future.add_done_callback(lambda x: logger.error(f"{future.exception()}") if future.exception() else None)
    # 详细错误 traceback.format_exc()
    return future.running()  # future.done()


# @backend
@decorator
def scheduler(func, scheduler_=schedule.every(2).seconds, stop_func=lambda: False, *args, **kwargs):
    """设置调度的参数，这里是每2秒执行一次

        t = time.time() + 10
        def f():
            time.sleep(1)
            return time.time() > t


        @scheduler(stop_func=f)
        def job(arg):
            print(f"{arg}: a simple scheduler in python.")

        @backend
        @scheduler(stop_func=lambda: False)
        def job():
            global d
            d = {}
            d['t'] = time.ctime() # 后台更新全局变量

    :param func:
    :param scheduler_:
    :param stop_func:
    :param args:
    :param kwargs:
    :return:
    """
    # 先初始化一次
    logger.info(f"{func.__name__} 调度初始化: {func(*args, **kwargs)}")

    # 正式调度
    scheduler_.do(func, *args, **kwargs)

    while True:
        schedule.run_pending()

        if stop_func():
            logger.info(f"{func.__name__} 调度终止")
            break


def add_start_docstrings(*docstr):
    def docstring_decorator(fn):
        fn.__doc__ = "".join(docstr) + (fn.__doc__ if fn.__doc__ is not None else "")
        return fn

    return docstring_decorator


def dependency_exists(dependency):
    try:
        importlib.import_module(dependency)
    except ImportError as e:
        # Check to make sure this isn't some unrelated import error.
        if dependency in repr(e):
            return False
    return True


def requires_dependencies(
        dependencies: Union[str, List[str]],
        extras: Optional[str] = None,
):
    if isinstance(dependencies, str):
        dependencies = [dependencies]

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            missing_deps = []
            for dep in dependencies:
                if not dependency_exists(dep):
                    missing_deps.append(dep)
            if len(missing_deps) > 0:
                raise ImportError(
                    f"Following dependencies are missing: {', '.join(missing_deps)}. "
                    + (
                        f"""Please install them using `pip install "unstructured[{extras}]"`."""
                        if extras
                        else f"Please install them using `pip install {' '.join(missing_deps)}`."
                    ),
                )
            return func(*args, **kwargs)

        return wrapper

    return decorator


def ratelimit(
        name: str = "ratelimit",
        weight: int = 1,
        rates: Optional[List[Any]] = None,
):
    """ https://github.com/vutran1710/PyrateLimiter
    :param name:
    :param weight:
    :param rates:
    :return:
    """
    from pyrate_limiter import Duration, Rate, Limiter, BucketFullException

    rates = rates or [
        Rate(1, Duration.SECOND),
        Rate(2, Duration.SECOND * 15),
        Rate(2 ** 2, Duration.MINUTE),
        Rate(2 ** 4, Duration.HOUR),
        Rate(2 ** 8, Duration.DAY)
    ]
    limiter = Limiter(rates)

    def name2weight(*args, **kwargs):  # 动态限频 limiter.try_acquire(self, name: str, weight: int = 1)
        return name, weight

    limiter_decorator = limiter.as_decorator()(name2weight)

    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        try:
            return limiter_decorator(wrapped)(*args, **kwargs)
        except BucketFullException as e:
            return e.meta_info

    return wrapper


def ratelimiter(limit_value: str = '3/1', callback=None):
    from ratelimiter import RateLimiter

    callback = callback or (lambda x: logger.debug(f"Rate limited: {limit_value}"))

    limiter = RateLimiter(*map(int, limit_value.split('/')), callback=callback)

    @wrapt.decorator
    def inner(wrapped, instance, args, kwargs):
        with limiter:
            return wrapped(*args, **kwargs)

    return inner


def limit(limit_value: str = '1/second', key_func: Callable[..., str] = None, error_message=None):
    """https://github.com/alisaifee/limits"""
    from limits import storage, strategies, parse
    memory_storage = storage.MemoryStorage()
    limiter = strategies.FixedWindowRateLimiter(memory_storage)
    item = parse(limit_value)

    @wrapt.decorator
    def inner(wrapped, instance, args, kwargs):
        # logger.debug(args)
        # logger.debug(kwargs)

        identifier = args[0]
        identifier = key_func and key_func(identifier)  # 根据这个标识限流：比如限制微信用户请求

        if limiter.hit(item, identifier):  # :param identifiers: variable list of strings to uniquely identify this
            return wrapped(*args, **kwargs)
        else:
            return {"error": f"Rate limited: {error_message or item}"}

    return inner


def try_catch(
        task: Optional[str] = None,
        callback: Optional[Callable] = None,
        is_trace: bool = False,
):
    from meutils.notice.feishu import send_message_for_try_catch

    callback = callback or send_message_for_try_catch  # logger.error

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            task_name = task or f"{func.__module__}.{func.__name__}"

            data = {
                "task_name": task_name,
                # "args": args,
                # "kwargs": kwargs,
                # "defined_args": inspect.getfullargspec(func).args,  # .varargs
            }

            logger.debug(data)

            async def async_wrapper():
                try:
                    if asyncio.iscoroutinefunction(func):
                        return await func(*args, **kwargs)
                    else:
                        return func(*args, **kwargs)
                except Exception as e:

                    if is_trace:
                        error_msg = f"{task_name}:\n{traceback.format_exc()}"
                    else:
                        error_msg = f"{task_name}: {e}"

                    data["error"] = error_msg
                    callback(data)

                    raise

            if asyncio.iscoroutinefunction(func):
                return async_wrapper()
            else:
                try:
                    return asyncio.get_event_loop().run_until_complete(async_wrapper())
                except RuntimeError:
                    # 如果没有事件循环（例如在同步环境中），则直接运行
                    return async_wrapper()

        return wrapper

    return decorator


if __name__ == '__main__':
    import time

    # @timeout()
    # def ff():
    #     import time
    #     time.sleep(30)
    #     return "OK"
    #
    #
    # print(ff())
    #
    #
    # def func():
    #     print(f"开始循环: {time.time()}")
    #     for i in range(10):
    #         time.sleep(1)
    #         print(f"{i}: {time.time()}")
    #
    #
    # @do_more(do_more_func=func)
    # def func_main():
    #     return "hhh"
    #
    #
    # print(func_main())
    # #
    # #
    #
    # def _do_more():
    #     print(f"开始: {time.time()}")
    #     executor = ThreadPoolExecutor(1)
    #     future = executor.submit(func)
    #
    #     # 主逻辑
    #     print(f"结束: {time.time()}")
    #
    #     return "do_more"
    #
    #
    # print(_do_more())

    # @timer()
    # def ff():
    #     import time
    #     time.sleep(3)
    #     return "OK"
    #
    #
    # ff()

    # @ratelimiter()
    # def fn(x):
    #     return x

    # @limit(limit_value='3/second', key_func=lambda x: str(x))
    # def fn(x, y):
    #     return x, y
    #
    #
    # for i in range(5):
    #     print(fn(1, 1))
    #     print(fn(i, 1))

    # @background_task_plus
    # def f():
    #     while 1:
    #         time.sleep(1)
    #         print('####')
    #
    #
    # f()
    # while 1:
    #     pass

    # def f():
    #     return 1 / 0
    #     # return 1
    #
    #
    # with tryer('try'):
    #     a = f()
    # print(a)

    from meutils.pipe import *
    from meutils.notice.feishu import send_message_for_try_catch


    @try_catch(is_trace=False)
    async def my_async_function(x=1, y=1):
        # 您的异步函数代码
        pass
        1 / 0


    async def main():
        await my_async_function(x=111, y=10000)


    # @async_try_catch(task="Custom Task Name", fallback=some_fallback_function)
    # async def another_async_function():
    #     # 另一个异步函数的代码
    #     pass

    arun(main())
