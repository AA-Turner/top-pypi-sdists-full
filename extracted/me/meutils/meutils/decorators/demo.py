#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : demo
# @Time         : 2021/4/2 3:54 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 
import asyncio
import traceback
from typing import Optional, Callable
from contextlib import asynccontextmanager, contextmanager

from meutils.notice.feishu import send_message_for_try_catch


@asynccontextmanager
async def atry_catch(
        task: Optional[str] = None,
        callback: Optional[Callable] = None,
        is_trace: bool = False,
):
    callback = callback or send_message_for_try_catch

    task_name = task or "Unnamed TryCatch Task"

    data = {
        "task_name": task_name,
    }

    # logger.debug(data)

    try:
        yield
    except Exception as e:
        if is_trace:
            error_msg = f"""{task_name}:\n{traceback.format_exc()}"""
        else:
            error_msg = f"{task_name}: {e}"

        data["error"] = error_msg

        callback(data)
        raise


@contextmanager
def try_catch(
        task: Optional[str] = None,
        callback: Optional[Callable] = None,
        is_trace: bool = False,
):
    callback = callback or send_message_for_try_catch

    task_name = task or "Unnamed TryCatch Task"

    data = {
        "task_name": task_name,
    }

    # logger.debug(data)

    try:
        yield
    except Exception as e:
        if is_trace:
            error_msg = f"""{task_name}:\n{traceback.format_exc()}"""
        else:
            error_msg = f"{task_name}: {e}"

        data["error"] = error_msg

        callback(data)
        raise


if __name__ == '__main__':
    from meutils.pipe import *


    async def f():
        return 1


    async def main():
        # with atry_catch_context(task="test", is_trace=True):
        #     1 / 0
        with try_catch(task="test", is_trace=True):
            logger.debug(await f())
            1 / 0


    asyncio.run(main())
