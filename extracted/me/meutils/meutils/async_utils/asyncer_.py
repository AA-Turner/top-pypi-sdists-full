#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : x
# @Time         : 2024/11/28 19:30
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://github.com/fastapi/asyncer

from meutils.pipe import *
import time

import anyio
from asyncer import asyncify, syncify

@asyncify
def do_sync_work(name: str):
    time.sleep(1)
    return f"Hello, {name}"


@syncify
async def do_async_work(name: str):
    await asyncio.sleep(1)
    return f"Hello, a{name}"

async def main():
    message = await asyncify(do_sync_work)(name="World")
    print(message)


if __name__ == '__main__':


    # arun(do_sync_work('xx'))
    arun(do_async_work('xxx'))