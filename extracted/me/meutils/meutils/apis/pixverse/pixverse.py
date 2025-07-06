#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : pixverse
# @Time         : 2024/7/24 13:14
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import uuid

from meutils.pipe import *
from meutils.decorators.retry import retrying
from meutils.schemas.pixverse_types import BASE_URL, PixverseRequest, EXAMPLES
from meutils.schemas.task_types import Task

from meutils.notice.feishu import send_message as _send_message
from meutils.config_utils.lark_utils import get_next_token_for_polling

FEISHU_URL = "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=f5db6a"

send_message = partial(
    _send_message,
    title=__name__,
    url="https://open.feishu.cn/open-apis/bot/v2/hook/dc1eda96-348e-4cb5-9c7c-2d87d584ca18"
)


# url = "https://app-api.pixverse.ai/creative_platform/media/getMediaDetail"
# "https://app-api.pixverse.ai/creative_platform/task/createVideoGenerateTask"
@retrying(max_retries=6, predicate=lambda r: not r)
async def create_task(request: Union[PixverseRequest, dict], token: Optional[str] = None):
    token = token or await get_next_token_for_polling(FEISHU_URL)
    ai_sign, token = token.split('|')

    headers = {
        'ai-sign': ai_sign,
        # 'ai-trace-id': '8a6cddbb-3cf0-4d44-a558-7ac777ab1f70', # uuid.uuid4()
        'token': token,
    }

    payload = request if isinstance(request, dict) else request.model_dump(exclude_none=True)

    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=30) as client:
        url = "/task/createImg2VideoGenerateTask" if payload.get("ImgUrl") else "/task/createVideoGenerateTask"
        response = await client.post(url, json=payload)

        logger.debug(response.status_code)
        logger.debug(response.text)

        if response.is_success:
            data = response.json()
            send_message([payload, data])
            return Task(status=1, data=data, system_fingerprint=token)

        else:
            # 触发重试
            if (
                    any(response.status_code == code for code in {401, 429})
                    # or any(i in response.text for i in {"enough credits"})
            ):
                return
            else:
                send_message(f"{response.text}\n\n{token}")

                return Task(status=0, data=response.text, system_fingerprint=token)


async def get_task(task_id: str, token: str):  # 1ee02f7b-42df-4926-b034-f56e4c4e2d31
    task_id = isinstance(task_id, str) and task_id.split("-", 1)[-1]
    ai_sign, token = token.split('|')

    payload = {
        "Type": 1,
        "MediaId": int(task_id)
    }

    headers = {
        'ai-sign': ai_sign,
        # 'ai-trace-id': '8a6cddbb-3cf0-4d44-a558-7ac777ab1f70', # uuid.uuid4()
        'token': token,
    }
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=30) as client:
        response = await client.post(f"/media/getMediaDetail", json=payload)

        logger.debug(response.text)
        logger.debug(response.status_code)

        if response.is_success:
            return response.json()

        response.raise_for_status()


@retrying()  # 触发重试
async def upload(file: bytes, filename: Optional[str] = None, token: Optional[str] = None):  # 应该不绑定cookie
    ai_sign, token = token.split('|')

    filename = f"{uuid.uuid4()}.png"
    payload = {
        "images": [
            {
                "name": filename,
                "size": len(file),
                "path": f"upload/{filename}"
            }
        ]
    }
    headers = {
        # 'ai-sign': ai_sign,
        # 'ai-trace-id': '8a6cddbb-3cf0-4d44-a558-7ac777ab1f70',  # uuid.uuid4()
        'Token': token,
    }
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=30) as client:
        response = await client.post("/getUploadToken")
        if response.is_success:
            resp = response.json().get("Resp")  # Ak Sk Token
            headers = {
                "Authorization": f"OSS {resp.get('Ak')}",
                'X-Oss-Security-Token': resp.get('Token')
            }
            # files = [('file', file_or_url)]
            oss_url = f"https://pixverse-fe-upload.oss-accelerate.aliyuncs.com/upload/{filename}"
            response = await client.put(oss_url, files={"file": file}, headers=headers)

            # response = await client.post("/media/batch_upload_media", json=payload)

            logger.debug(response.text)
            logger.debug(response.status_code)

            if response.is_success:
                logger.debug(response.text)
                return response.json()

            response.raise_for_status()


if __name__ == '__main__':
    token = "9d6332337b5d6976c3305ad3e0d8cd44eab6c0554d741a2fde856dff82f33cb7|eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJBY2NvdW50SWQiOjI4NjA1NDYzMzkyNDY3MiwiRXhwaXJlVGltZSI6MTcyMjQwMjI2OCwiVXNlcm5hbWUiOiIxODU1MDI4ODIzMyJ9.wiIBgmGACw8XTDf3eQ3jwGk33n8rl_hcceScasjKsIw"
    arun(get_task('286085978032192', token)) #

    # request = PixverseRequest(
    #     Prompt="开花过程",
    #     ImgUrl="https://dgss0.bdstatic.com/5bVWsj_p_tVS5dKfpU_Y_D3/res/r/image/2017-09-27/297f5edb1e984613083a2d3cc0c5bb36.png",
    #     # ImgUrl="https://media.pixverse.ai/upload%2F3597df25-8161-4eea-99a4-502ac2b49227.png"
    # )

    # arun(create_task(request))
    # file = Path('/Users/betterme/PycharmProjects/AI/test.png').read_bytes()
    # arun(upload(file, token=token))
