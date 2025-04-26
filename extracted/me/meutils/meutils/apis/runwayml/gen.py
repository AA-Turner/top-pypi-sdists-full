#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : video
# @Time         : 2024/7/16 10:47
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 


from meutils.pipe import *
from meutils.decorators.retry import retrying
from meutils.schemas.runwayml_types import BASE_URL, RunwayRequest, EXAMPLES
from meutils.schemas.task_types import Task

from meutils.notice.feishu import send_message as _send_message
from meutils.config_utils.lark_utils import get_next_token_for_polling

FEISHU_URL = "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=cx0SGO"

send_message = partial(
    _send_message,
    title=__name__,
    url="https://open.feishu.cn/open-apis/bot/v2/hook/dc1eda96-348e-4cb5-9c7c-2d87d584ca18"
)


# @retrying(max_retries=3, predicate=lambda x: not x)
async def get_access_token(token: Optional[str] = None):  # 暂时好像用不到待定
    token = token or await get_next_token_for_polling(FEISHU_URL)
    headers = {
        'Authorization': f'Bearer {token}',
    }
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=30) as client:
        response = await client.post('/short_jwt')
        if response.is_success:
            return response.json().get('token')


@retrying(max_retries=6, predicate=lambda r: not r)
async def create_task(request: Union[RunwayRequest, dict], token: Optional[str] = None) -> object:
    token = token or await get_next_token_for_polling(FEISHU_URL)

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-type': 'application/json'
    }

    payload = request if isinstance(request, dict) else request.model_dump(exclude_none=True)

    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=30) as client:
        response = await client.post("/tasks", json=payload)

        # logger.debug(response.text)

        if response.is_success:
            data = response.json()
            send_message(bjson(data))

            try:
                tass_id = data.get("task").get("id")
                return Task(id=tass_id, data=data, system_fingerprint=token)

            except Exception as e:
                logger.error(e)
                send_message(f"未知错误：{e}")
        else:
            logger.debug(response.status_code)
            # 触发重试
            if (
                    any(response.status_code == code for code in {401, 429})
                    # or any(i in response.text for i in {"enough credits"})
            ):
                return
            else:
                send_message(f"{response.text}\n\n{token}")

                return Task(status=0, data=response.text)


@retrying(predicate=lambda r: not r)  # 触发重试
async def get_task(task_id: str, token: str):  # 1ee02f7b-42df-4926-b034-f56e4c4e2d31
    task_id = isinstance(task_id, str) and task_id.split("-", 1)[-1]

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-type': 'application/json'
    }
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=30) as client:
        response = await client.get(f"/tasks/{task_id}")

        logger.debug(response.text)
        logger.debug(response.status_code)

        if response.is_success:
            return response.json()
        else:
            return {"task": response.json()}  # 400 {"error":"id: The id specified in this URL must be a UUID"}


# 排队

# https://api.runwayml.com/v1/assets_pending?asTeamId=16871062&privateInTeam=true
# {
#     "pendingAssets": [
#         {
#             "id": "b218fed7-cd5f-4f8e-afc8-ac2b6365c9f0",
#             "createdAt": "2024-07-30T02:50:12.084Z",
#             "updatedAt": "2024-07-30T02:51:02.062Z",
#             "name": "Gen-2 8s, 227015205, M 5",
#             "previewUrls": [],
#             "mediaType": "video",
#             "mediaSubtype": null,
#             "isUserUpload": false,
#             "username": "niyudintg",
#             "progressRatio": "0.33",
#             "progressText": null
#         },
#         {
#             "id": "f7027b60-3fb8-4803-a830-44435deace81",
#             "createdAt": "2024-07-30T02:49:57.061Z",
#             "updatedAt": "2024-07-30T02:51:05.264Z",
#             "name": "Gen-2 8s, 3227464482, M 5",
#             "previewUrls": [],
#             "mediaType": "video",
#             "mediaSubtype": null,
#             "isUserUpload": false,
#             "username": "niyudintg",
#             "progressRatio": "0.41",
#             "progressText": null
#         }
#     ]
# }
if __name__ == '__main__':
    pass
    # print(arun(get_access_token()))
    print(arun(create_task(EXAMPLES[1])))
    # print(arun(create_task(RunwayRequest(**text2video_payload))))
    # token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTcyNDk1NTMsImVtYWlsIjoicGtmZ2JtbDc2NzBAb3V0bG9vay5jb20iLCJleHAiOjE3MjM2ODc5MTkuOTA5LCJpYXQiOjE3MjEwOTU5MTkuOTA5LCJzc28iOmZhbHNlfQ.CZLGYU0FXraU5zT-GY1CpbfQMOi9Srdo2QOXzob38PU"
    # task_id = "1ee02f7b-42df-4926-b034-f56e4c4e2d31"
    # task_id = "b7658f8a-6205-48ad-8655-4ad9b1ff856d"
    # print(arun(get_task(task_id, token)))
