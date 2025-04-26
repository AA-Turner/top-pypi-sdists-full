#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : kolors
# @Time         : 2024/7/10 13:13
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://kolors.kuaishou.com/


import jsonpath

from meutils.pipe import *
from meutils.decorators.retry import retrying
from meutils.schemas.kuaishou_types import KolorsRequest
from meutils.notice.feishu import send_message as _send_message
from meutils.config_utils.lark_utils import get_next_token_for_polling

BASE_URL = "https://kolors.kuaishou.com"
OSS_URL = "https://s2-111386.kwimgs.com/bs2/mmu-kolors-public"
# https://s2-111386.kwimgs.com/bs2/mmu-kolors-public/5f9c7b42688fe95c4b8d9ebd1dba3431.png?x-oss-process=image/resize,m_mfit,w_305
# https://s2-111386.kwimgs.com/bs2/mmu-kolors-public/mmu-kolors-4243501072-1720596454510-1a862f8dbde042349b97445fc45ec231 # upload

FEISHU_URL = "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=I9NCss"

send_message = partial(
    _send_message,
    title=__name__,
    url="https://open.feishu.cn/open-apis/bot/v2/hook/dc1eda96-348e-4cb5-9c7c-2d87d584ca18"
)


@retrying(predicate=lambda r: not isinstance(r, str))  # 触发重试
async def upload(file_or_url: Union[bytes, str], cookie: Optional[str] = None):  # todo: 垫图
    cookie = cookie or await get_next_token_for_polling(FEISHU_URL)

    headers = {
        'Cookie': cookie,
    }

    files = params = None
    if isinstance(file_or_url, bytes):
        files = [('file', file_or_url)]

    else:
        params = {
            'url': file_or_url
        }

    # files = [
    #     ('file', ('v的副本.jpg', open('/Users/betterme/Downloads/v的副本.jpg', 'rb'), 'image/jpeg'))
    # ]

    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=100) as client:
        response = await client.post("/api/kolors/uploadToBlobStore", params=params, files=files)

        logger.debug(response.text)

        if response.is_success:
            data = response.json()
            send_message(data)

            try:
                rawKeys = jsonpath.jsonpath(data, "$..rawKey")
                if rawKeys:
                    url = f"{OSS_URL}/{rawKeys[0]}?x-oss-process=image/resize,m_mfit,w_1024"
                    return url

            except Exception as e:  # 429
                logger.error(e)

            else:
                return data


@retrying(max_retries=5, predicate=lambda r: not r)
async def create_task(request: KolorsRequest, cookie: Optional[str] = None):
    cookie = cookie or await get_next_token_for_polling(FEISHU_URL)

    headers = {
        'Cookie': cookie,
        'Content-Type': 'application/json;charset=UTF-8'
    }

    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=60) as client:
        response = await client.post("/api/kolors/textToImage", json=request.model_dump())

        logger.debug(response.text)
        logger.info(response.status_code)

        if response.is_success:
            data = response.json()
            send_message(data)

            if data.get("code") == 500:
                return data  # 不重试
                # raise Exception(data)

            if any(i in str(data) for i in {"页面未找到", "请求超限"}):
                send_message(f"{data}\n\n{cookie}")
                return  # 404 429 重试

            # {"code":500,"result":{"status":"ERROR","code":33001,"reason":""}} 可能是内容审核的问题
            try:
                requestIds = jsonpath.jsonpath(data, "$..requestId")
                if requestIds:
                    logger.info(f"requestId or taskId: {requestIds[0]}")
                    response = await client.get("/api/kolors/queryAsyncTaskResult", params={"requestId": requestIds[0]})
                    logger.debug(response.text)

                    if response.is_success:
                        return requestIds[0]
                    else:
                        response.raise_for_status()

            except Exception as e:  # 429
                logger.error(e)

            else:
                return data


@retrying(max_retries=16, exp_base=1.1, min=2, predicate=lambda r: r == "RETRYING")  # 触发重试
async def get_task(task_id, cookie: str):
    headers = {
        'Cookie': cookie,
        'Content-Type': 'application/json;charset=UTF-8'
    }

    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=60) as client:
        response = await client.get(f"/api/kolors/requests/{task_id}", params={"withWatermark": False})
        if response.is_success:
            data = response.json()

            logger.debug(data)

            if not task_id or "ERROR" in str(data): return "TASK_FAILED"  # 跳出条件

            urls = jsonpath.jsonpath(data, '$..imageBlobKey')
            if urls and all(urls):
                images = [{"url": f"{OSS_URL}/{url.replace('mmu:kolors-public:', '')}"} for url in urls]
                return images
            else:
                return "RETRYING"  # 重试


@retrying(max_retries=3, predicate=lambda r: r == "TASK_FAILED")
async def create_image(request: KolorsRequest, file: Optional[bytes] = None):
    cookie = await get_next_token_for_polling(FEISHU_URL)

    if file:
        request.referImage = await upload(file, cookie)

    logger.info(request)

    task_id = await create_task(request, cookie)
    logger.info(f"taskId: {task_id}")
    if isinstance(task_id, dict):
        return task_id

    data = await get_task(task_id, cookie)

    return data


if __name__ == '__main__':
    cookie = "kuaishou.dmo.ketu_ph=f711fb055f50eeb21fdb39bd6e05cc611744;kuaishou.dmo.ketu_st=ChRrdWFpc2hvdS5kbW8ua2V0dS5zdBKgAULU9RPZzOXOMUukfVPm51Ghgxee3d2ZFqxfGxQ4WRIWWbZ8omUKzDni1d_3R0s3hv9RfvRU7g0dW9v1lKXIMX23-ctLJ10YovTsS6HDb_A6zzruMKa6qLFOiRWf4RvJ0DB07y7UbxuNlof78rWMMKftZEKSZzDVSSQnGhEf0-V-4WWRcEzOaAImqyJZccV3lqcMr6UHfqnJmaJG3ufNw2gaEtBzrwEitKSmOEU59oMJzRgeLSIgvpsGbded8NVshgwPYn9xkkH1dsTLZct7SIl-I82yHDQoBTAB;did=web_e022fde52721456f43cb66d90a7d6f14e462;userId=742626779;weblogger_did=web_47164250171DB527"
    request = KolorsRequest(prompt="阳光下", imageCount=4)
    request = KolorsRequest(prompt="a cat", imageCount=4)

    # print(arun(create_task(request, cookie)))

    # print(arun(get_task(851793, cookie)))
    url = "https://s2-111386.kwimgs.com/bs2/mmu-kolors-public/5f9c7b42688fe95c4b8d9ebd1dba3431.png?x-oss-process=image/resize,m_mfit,w_305"
    # print(arun(upload(url)))
    #
    # request = KolorsRequest(referImage="mmu-kolors-742626779-1720600931170-5ebc098c01b14baf965f3ea9e2a60228")
    # request = KolorsRequest(referImage="https://s2-111386.kwimgs.com/bs2/mmu-kolors-public/mmu-kolors-742626779-1720760149252-f276504646014593a73f5b36c88ccafa?x-oss-process=image/resize,m_mfit,w_1000")
    # print(request)

    # file = open("/Users/betterme/PycharmProjects/AI/x.jpg", "rb").read()
    #
    # pprint(arun(upload(file_or_url=file, cookie=cookie)))

    # url = "https://s2-111386.kwimgs.com/bs2/mmu-kolors-public/a1bf746085fa4bf39b0b299e91d267fd.png"

    # pprint(arun(create_image(request, file)))
    arun(create_image(request))
