#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : luca
# @Time         : 2024/8/20 10:39
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.config_utils.lark_utils import get_spreadsheet_values, get_next_token_for_polling
from meutils.notice.feishu import send_message as _send_message
from meutils.schemas.task_types import TaskType, Task, FileTask
from meutils.io.files_utils import base64_to_bytes

from fastapi import status, HTTPException

FEISHU_URL = 'https://xchatllm.feishu.cn/sheets/GYCHsvI4qhnDPNtI4VPcdw2knEd?sheet=P5wJMA'
BASE_URL = "https://luca.cn"

send_message = partial(
    _send_message,
    title=__name__,
    url="https://open.feishu.cn/open-apis/bot/v2/hook/dc1eda96-348e-4cb5-9c7c-2d87d584ca18"
)


async def upload(file: bytes, token: Optional[str] = None):
    token = token or await get_next_token_for_polling(feishu_url=FEISHU_URL)

    files = [('file', ('x.png', file, 'image/png'))]

    headers = {
        'token': token,
    }
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=100) as client:
        response = await client.post("/api/img/v1/uploadImg", files=files)

        logger.debug(response.status_code)
        logger.debug(response.text)

        if response.is_success:
            data = response.json()
            file_id = data['data']['imageId']
            if file_id:
                return FileTask(id=file_id, data=data, system_fingerprint=token)
        raise HTTPException(status_code=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS, detail="触发内容审核")


async def create_chat(prompt, image_data, token: Optional[str] = None):
    token = token or await get_next_token_for_polling(feishu_url=FEISHU_URL)

    # image_data: base64 url bytes/path
    file = None
    if isinstance(image_data, bytes): # todo: 抽象成通用
        file = image_data

    elif len(image_data) < 512 and Path(image_data).is_file():  # base64
        file = Path(image_data).read_bytes()

    elif image_data.startswith('data:'):  # base64
        file = base64_to_bytes(image_data)

    elif image_data.startswith('http'):
        resp = await httpx.AsyncClient(timeout=100, follow_redirects=True).get(image_data)
        file = resp.content

    file_id = (await upload(file, token)).id

    headers = {
        'token': token,
    }
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=100) as client:
        payload = {"title": "新会话"}
        response = await client.post("/api/chat/v1/createConv", json=payload)

        # logger.debug(response.status_code)
        # logger.debug(response.text)

        conversationId = response.json()['data']

        payload = {
            "generateType": "NORMAL",
            "conversationId": conversationId,
            "parentMessageId": "",
            "chatMessage": [
                {
                    "role": "USER",
                    "contents": [
                        {
                            "type": "IMAGE",
                            "imageId": file_id,
                            "pairs": "",

                        },
                        {
                            "type": "TEXT",
                            "imageId": "",
                            "pairs": prompt,
                        }
                    ],

                    "id": "",
                    "parentMsgId": "",

                    # "contentLayout": "<p><img src=\"blob:https://luca.cn/86f60c82-b283-4f55-8445-36b86381729a\" alt=\"\" data-href=\"Dn6AUbGGW7UXATs86M9rV\" style=\"\"/>总结下</p><p><br></p>",
                }
            ]
        }
        response = await client.post("/api/chat/v1/submitMsg", json=payload)
        data = response.json()
        logger.debug(data)

        messageId = data['data']['childMsgId']
        payload = {
            "conversationId": conversationId,
            "messageId": messageId
        }
        for i in range(10):
            await asyncio.sleep(1)
            response = await client.post('/api/chat/v1/queryMsg', json=payload)
            # logger.debug(response.status_code)
            # logger.debug(response.json())
            # logger.debug(response.json()['data'].get('output'))
            if _ := response.json()['data'].get('output'): return _


if __name__ == '__main__':
    # file = open("/Users/betterme/PycharmProjects/AI/11.jpg", 'rb').read()
    # arun(upload(file))
    # arun(create_chat("图片里有什么", "/Users/betterme/PycharmProjects/AI/11.jpg"))

    url = 'https://dss2.bdstatic.com/5bVYsj_p_tVS5dKfpU_Y_D3/res/r/image/2021-3-4/hao123%20logo.png'
    arun(create_chat("图片里有什么", url))

    # arun(get_next_token_for_polling(feishu_url=FEISHU_URL))
