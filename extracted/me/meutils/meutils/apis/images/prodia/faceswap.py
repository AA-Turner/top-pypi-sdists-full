#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : faceswap
# @Time         : 2024/8/14 14:22
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.decorators.retry import retrying

from meutils.schemas.task_types import TaskType, Task
from meutils.schemas.prodia_types import BASE_URL, FEISHU_URL, FaceswapRequest

from meutils.config_utils.lark_utils import get_next_token_for_polling
from meutils.notice.feishu import send_message as _send_message

send_message = partial(
    _send_message,
    title=__name__,
    url="https://open.feishu.cn/open-apis/bot/v2/hook/dc1eda96-348e-4cb5-9c7c-2d87d584ca18"
)


@retrying(max_retries=8, max=8, predicate=lambda r: r is True)  # 触发重试
async def create_task(request: FaceswapRequest, token: Optional[str] = None):
    token = token or await get_next_token_for_polling(FEISHU_URL)

    payload = request.model_dump()

    headers = {
        "X-Prodia-Key": token
    }
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=60) as client:
        response = await client.post("/faceswap", json=payload)
        logger.debug(response.text)

        if response.status_code in {429}:  # 触发重试
            return True

        if response.is_success:
            data = response.json()
            task_id = f"{TaskType.faceswap}-{data['job']}"
            return Task(id=task_id, data=data, system_fingerprint=token)
        else:
            logger.debug(token)
            return Task(data=response.text, status=0, status_code=response.status_code)


async def get_task(task_id: str, token: str):
    task_id = task_id.split(f"{TaskType.faceswap}-", 1)[-1]

    headers = {
        "X-Prodia-Key": token
    }
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=100) as client:
        response = await client.get(f"/job/{task_id}")

        logger.debug(response.text)
        logger.debug(response.status_code)

        if response.is_success:
            data = response.json()
            return data


if __name__ == '__main__':
    request = FaceswapRequest(
        sourceUrl='https://oss.ffire.cc/files/source.jpg',
        targetUrl='https://oss.ffire.cc/files/target.jpg'
    )
    arun(create_task(request))

    arun(get_task('e40e290f-71b6-4755-a4e8-d5201462d9d4', 'fbb99c65-3ac9-4077-8a3c-67387442f48b'))
