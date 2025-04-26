#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : yezi
# @Time         : 2024/6/28 09:23
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# todo: 接码平台
# @Description  : https://github.com/Thekers/Get_OpenaiKey/blob/9d174669d7778ea32d1132bedd5167597912dcfb/Add_01AI_Token.py
# https://note.youdao.com/ynoteshare/index.html?id=543e0ee9d51faf3d4c33d792971d9de9&type=note&_time=1719535893843
import os

import httpx

from meutils.pipe import *

"http://api.sqhyw.net:90/api/get_myinfo?token=xxxxxxx"

BASE_URL = "http://api.sqhyw.net:90"


class Request(BaseModel):
    token: str
    project_id: str
    loop: str = 1
    operator: str = 4  # 0=默认 1=移动 2=联通 3=电信 4=实卡 5=虚卡
    phone_num: Optional[str] = None  # 指定取号的话 这里填要取的手机号
    scope: Optional[str] = None  # 指定号段 最多支持号码前5位. 例如可以为165，也可以为16511address
    address: Optional[str] = None  # 归属地选择 例如 湖北 甘肃 不需要带省字
    scope_black: Optional[str] = None  # 排除号段最长支持7位且可以支持多个,最多支持20个号段。用逗号分隔 比如150,1511111,15522
    api_id: Optional[str] = None  # 如果是开发者,此处填写你的用户ID才有收益，注意是用户ID不是登录账号


@alru_cache()
async def get_access_token():
    username, password = os.getenv("YEZI_USER").split('|')
    payload = {
        "username": username,
        "password": password
    }
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/api/logins", params=payload)
        if response.is_success:
            logger.debug(response.json())
            return response.json().get("token")


async def get_mobile(project_id: str = "806053"):
    token = await get_access_token()
    payload = Request(token=token, project_id=project_id).model_dump()

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/api/get_mobile", params=payload)
        if response.is_success:
            logger.debug(response.json())
            return response.json().get("mobile")


async def get_message(project_id, phone_num):
    token = await get_access_token()
    payload = Request(token=token, project_id=project_id, phone_num=phone_num).model_dump()

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        s = time.time()
        while 1:
            await asyncio.sleep(1)
            response = await client.get("/api/get_message", params=payload)
            if response.is_success and (code := response.json().get("code")):
                logger.debug(response.json())
                return code
            if time.time() - s > 120:
                logger.error("获取短信验证码失败")
                break


async def free_mobile(project_id, phone_num: Optional[str] = None):  # 释放所有
    token = await get_access_token()
    payload = Request(token=token, project_id=project_id, phone_num=phone_num).model_dump()

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/api/free_mobile", params=payload)
        if response.is_success:
            logger.debug("释放")


async def get_code(project_id):
    phone_num = await get_mobile(project_id)
    code = await get_message(project_id, phone_num)
    await free_mobile(project_id, phone_num)
    return code


if __name__ == '__main__':
    # print(arun(get_access_token()))
    # print(arun(get_mobile()))
    print(arun(get_message(project_id="806053", phone_num="19211569315")))
