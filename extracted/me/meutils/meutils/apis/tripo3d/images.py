#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : images
# @Time         : 2024/10/28 15:15
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

from meutils.schemas.tripo3d_types import BASE_URL, FEISHU_URL

from meutils.schemas.tripo3d_types import ImageRequest, TaskResponse
from meutils.config_utils.lark_utils import get_next_token_for_polling

from meutils.notice.feishu import send_message as _send_message, IMAGES

send_message = partial(
    _send_message,
    title=__name__,
    url=IMAGES
)


# @retrying(predicate=lambda r: r.base_resp.status_code in {1000061, })  # 限流
async def create_task(request: ImageRequest, token: Optional[str] = None, vip: Optional[bool] = True):
    token = token or await get_next_token_for_polling(FEISHU_URL)

    payload = request.model_dump()

    headers = {
        "Authorization": f"Bearer {token}"
    }
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=60) as client:
        response = await client.post("/v2/web/task", json=payload)
        response.raise_for_status()
        data = response.json()

        return TaskResponse(**data, system_fingerprint=token)


async def get_task(task_id: str, token: str):
    # task_id = task_id.rsplit('-', 1)[-1]

    headers = {
        "Authorization": f"Bearer {token}"
    }
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=60) as client:
        response = await client.get(f"/v2/web/task/{task_id}")
        response.raise_for_status()
        data = response.json()
        return data

        # {
        #     "code": 0,
        #     "data": {
        #         "task_id": "41df5dd5-19c2-4df4-9f4f-71d0cf63d83e",
        #         "type": "text_to_model",
        #         "status": "running",
        #         "progress": 99,
        #         "input": {
        #             "prompt": "一只活泼的柴犬，戴着红白相间的头巾，叼着一根魔法棒，眼睛闪烁着星星，正在表演马戏团特技",
        #             "model_version": "v2.0-20240919"
        #         },
        #         "name": "一只活泼的柴犬，戴着红白相间的头巾，叼着一根魔法棒，眼睛闪烁着星星，正在表演马戏团特技",
        #         "create_time": 1730099666,
        #         "prompt": "一只活泼的柴犬，戴着红白相间的头巾，叼着一根魔法棒，眼睛闪烁着星星，正在表演马戏团特技",
        #         "queuing_num": -1,
        #         "running_left_time": 1,
        #         "is_owner": true,
        #         "pbr_model": "https://tripo-data.cdn.bcebos.com/tcli_ba9f78ef47fd4c559801b2e57f54d26d/20241028/41df5dd5-19c2-4df4-9f4f-71d0cf63d83e/tripo_pbr_model_41df5dd5-19c2-4df4-9f4f-71d0cf63d83e.glb?auth_key=1730099847-XQdJD3SG-0-95f98da862962563cb68b1c0beed395b",
        #         "rendered_sequence": "https://tripo   -data.cdn.bcebos.com/tcli_ba9f78ef47fd4c559801b2e57f54d26d/20241028/41df5dd5-19c2-4df4-9f4f-71d0cf63d83e/composite_spin_frame_41df5dd5-19c2-4df4-9f4f-71d0cf63d83e.webp?auth_key=1730099847-1vfLjTnM-0-d8178772aad0d0f682ed9bddfa9b7804"
        #     }
        # }


async def check_token(token: str, threshold: int = 0):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    try:
        async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=60) as client:
            response = await client.get("/v2/web/billing/wallet/all")
            response.raise_for_status()
            data = response.json()
            logger.debug(bjson(data))
            return data['data']['total_balance'] > threshold


    except Exception as e:
        logger.error(e)
        return False


if __name__ == '__main__':
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6ImQwbDJldGdSeEd5Q19FVFZyOGgzRG9LMWxqa3ZCN0puQ1pPbTVwUFRyelkifQ.eyJzdWIiOiI2NzFmMzk0ZjQ3ZmUyZDg0ZjNjMGRhMzEiLCJhdWQiOiI2NWIyNTAzMjAxZjQwODZjMDQzZDcxMWYiLCJzY29wZSI6ImFkZHJlc3MgZW1haWwgcHJvZmlsZSBwaG9uZSBvcGVuaWQiLCJpYXQiOjE3MzAwOTk1NDAsImV4cCI6MTczMTMwOTE0MCwianRpIjoiQ2ZoZ2I0cHROcmVCM2RXSzJwZjhwX3N2eUZjSkZrcmpHY0haV0FoSVotLSIsImlzcyI6Imh0dHBzOi8vdHJpcG8td2ViLnVzLmF1dGhpbmcuY28vb2lkYyJ9.P2q1Y82VGem-0PSIP7A9etnclK73IfWbGcBrBa-NrxBH-CJNRHQy-eehCcLEaIPX879dqZeeTzCWwKc07rw3M4jfLj4Gqm7hrdFHZxGi4gT0vwgkKpxEU_iwn773Yx6L3N5aMpXsMqDoj_i2cuIU2mt6PET0rhErE1i1hqM1rh_BSZBuRpYZTKMOwMbcay7xn2SAcsGX0nHKXcv0nmRWXoMpn_-RbYOoddVO2cAe5SCPe168-OJ7RQN-I2lV-VE7ZQp_wCy2pxOVdY8iekKCp42wnutYHHE1kSgEN_ac6v0CINqx9CFw0TT6qBVYlsPUliq4tCX2YRwiaYZtqI8RRw"

    # arun(check_token(token))
    # arun(get_task("e25d3012-ec08-482f-90a9-fd9b356df6ed", token))

    request = ImageRequest(
        prompt="一只活泼的柴犬，戴着红白相间的头巾，叼着一根魔法棒，眼睛闪烁着星星，正在表演马戏团特技",
    )
    arun(create_task(request))  # 60*100
