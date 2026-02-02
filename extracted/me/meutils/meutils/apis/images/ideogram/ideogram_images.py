#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : images
# @Time         : 2024/8/23 10:26
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
from meutils.config_utils.lark_utils import get_next_token_for_polling
from meutils.decorators.retry import retrying
from meutils.oss.minio_oss import Minio
from meutils.pipe import *

from meutils.schemas.openai_types import ImageRequest, ImagesResponse
from meutils.schemas.image_types import ASPECT_RATIOS

FEISHU_URL = "https://xchatllm.feishu.cn/sheets/GYCHsvI4qhnDPNtI4VPcdw2knEd?sheet=IN01qU"

from urllib.parse import urlencode

STYLES = {'AUTO', 'DEFAULT', 'PHOTO', 'ANIME', 'ILLUSTRATION', 'RENDER_3D'}


# @alru_cache(ttl=600)
# @retrying()
async def get_access_token(refresh_token: Optional[str] = None):
    refresh_token = refresh_token or await get_next_token_for_polling(FEISHU_URL)

    refresh_token, cookie = refresh_token.strip().split('\n', maxsplit=1)

    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }

    data = urlencode(payload)

    headers = {
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://ideogram.ai',
        'priority': 'u=1, i',
        'referer': 'https://ideogram.ai/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        # 'x-client-data': 'CI22yQEIo7bJAQipncoBCNqFywEIlKHLAQiGoM0BCJ2szgEYj87NAQ==',
        'x-client-version': 'Chrome/JsCore/10.12.3/FirebaseCore-web'
    }

    base_url = "https://ideogram.chatfire.cc"
    base_url = "https://securetoken.googleapis.com"
    params = {"key": "AIzaSyBwq4bRiOapXYaKE-0Y46vLAw1-fzALq7Y"}
    async with httpx.AsyncClient(base_url=base_url, headers=headers, timeout=30) as client:
        response = await client.post('/v1/token', content=data, params=params)
        # logger.debug(response.status_code)
        # logger.debug(response.text)
        data = response.json()

        user_id = data['user_id']
        access_token = data['access_token']

        return user_id, access_token, cookie


@retrying(max_retries=8, max=5, predicate=lambda x: x is True)
async def create(request: ImageRequest, refresh_token: Optional[str] = None):
    user_id, access_token, cookie = await get_access_token(refresh_token)

    width, height = ASPECT_RATIOS.get(request.size, request.size).split('x') | xmap(int)

    payload = {
        "sampling_speed": 2,  # 2 是快速 0 是中速 -2 高质量

        "prompt": request.prompt,
        "user_id": "",
        # "model_version": "V_1_5",
        # "model_version": "V_0_3",
        "model_version": request.model,

        "use_autoprompt_option": "AUTO",
        "style_expert": request.style if request.style in STYLES else "AUTO",

        "resolution": {
            "width": width,
            "height": height
        },
        # "resolution": {
        #     "width": 1152,
        #     "height": 864
        # },
        # "resolution": {
        #     "width": 1280,
        #     "height": 960
        # },

        # "resolution": {
        #     "width": 1024,
        #     "height": 512
        # }
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "user_id": user_id,

        "Cookie": cookie,

        "Host": "ideogram.ai",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://ideogram.ai/u/test1014/generated",
        "Content-Type": "application/json",
        "Alt-Used": "ideogram.ai",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "TE": "trailers"
    }

    base_url = "https://ideogram.ai"
    async with httpx.AsyncClient(base_url=base_url, headers=headers, timeout=30) as client:
        response = await client.post('/api/images/sample', json=payload)
        logger.debug(response.status_code)
        # logger.debug(response.text)
        if response.status_code in {401, 403}:
            return True

        if response.is_success:
            data = response.json()
            payload = {
                "request_ids": [data['request_id']]
            }

            for i in range(10):
                await asyncio.sleep(5)
                logger.debug(f'获取结果 「{i}」')
                response = await client.post("/api/gallery/retrieve-requests", json=payload)

                logger.debug(response.status_code)
                # logger.debug(response.text)

                if response.is_success:
                    data = response.json()
                    if data['sampling_requests'][0]['is_completed']:
                        image_responses = data['sampling_requests'][0]['responses']
                        tasks = []
                        for image_resp in image_responses:
                            url = f"https://ideogram.ai/api/images/direct/{image_resp['response_id']}"

                            image_resp['raw_url'] = url

                            task = await Minio().put_object_for_openai(
                                file=url,
                                filename=f"{shortuuid.random()}.jpeg",

                                headers=headers, follow_redirects=True
                            )

                            tasks.append(task)
                            await asyncio.sleep(1)

                        # file_objects = await asyncio.gather(*tasks)

                        file_objects = tasks
                        for file_object, image_resp in zip(file_objects, image_responses):
                            image_resp['url'] = file_object.filename

                        return ImagesResponse.construct(data=image_responses)


if __name__ == '__main__':
    # arun(get_access_token(refresh_token))  # 88uwVq1nbyctFsgAOWytFefTAW02
    with timer():
        arun(
            create(
                ImageRequest(
                    model='V_0_3',

                    prompt='一位性感的中国美女',

                    style=''
                ))
        )
