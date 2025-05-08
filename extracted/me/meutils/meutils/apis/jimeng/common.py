#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : common
# @Time         : 2024/12/16 18:19
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://github.com/LLM-Red-Team/jimeng-free-api/commit/acd362a4cecd115938bf4bc9bbb0067738aa0d5b#diff-e6a7354ac1431dc3751e91efaf1799200c1ce2fa8abe975a49c32644290988baR121
from openai import AsyncClient

from meutils.pipe import *
from meutils.hash_utils import md5
from meutils.schemas.openai_types import TTSRequest

from meutils.schemas.jimeng_types import BASE_URL, MODELS_MAP, FEISHU_URL
from meutils.caches.redis_cache import cache

from fake_useragent import UserAgent

ua = UserAgent()


@lru_cache()
def get_headers(url, token: str = "693701c43e477b7c405cc7e2fef0ddbd"):
    device_time = f"{int(time.time())}"
    sign = md5(
        # f"9e2c|receive|7|5.8.0|{device_time}||11ac"
        f"9e2c|{url[-7:]}|7|5.8.0|{device_time}||11ac"
    )

    headers = {
        'appid': '513695',
        'appvr': '5.8.0',
        'device-time': device_time,
        'pf': '7',
        'sign': sign,
        'sign-ver': '1',
        'Cookie': f'sid_guard={token}|{device_time}|5184000|Fri,+14-Feb-2025+00:51:51+GMT',
        'User-Agent': ua.random,

        'content-type': 'application/json',
        # "Referer": "https://jimeng.jianying.com/ai-tool/image/generate",
    }
    return headers


@cache(ttl=3600 // 2)
async def get_upload_token(token, biz: Optional[str] = None):  # 3600 跨账号？

    if biz == "video":
        url = "/mweb/v1/get_upload_token"  # ?aid=513695&da_version=3.2.0&aigc_features=app_lip_sync

        payload = {"scene": 2}
        client = AsyncClient(base_url=BASE_URL)
        response = await client.post(url, body=payload, cast_to=object)
        logger.debug(bjson(response))
        return response

    url = "/artist/v2/tools/get_upload_token"
    headers = get_headers(url, token)

    payload = {"scene": 2}
    client = AsyncClient(base_url=BASE_URL, default_headers=headers)
    response = await client.post(url, body=payload, cast_to=object)
    logger.debug(bjson(response))
    return response


@alru_cache(12 * 3600)
async def receive_credit(token):
    # token = "eb4d120829cfd3ee957943f63d6152ed"  # y
    # token = "9ba826acc1a4bf0e10912eb01beccfe0"  # w
    url = "/commerce/v1/benefits/credit_receive"
    headers = get_headers(url, token)
    payload = {"time_zone": "Asia/Shanghai"}
    client = AsyncClient(base_url=BASE_URL, default_headers=headers)
    response = await client.post(url, body=payload, cast_to=object)
    logger.debug(bjson(response))


async def get_credit(token):
    # token = "eb4d120829cfd3ee957943f63d6152ed"  # y
    # token = "9ba826acc1a4bf0e10912eb01beccfe0"  # w

    url = "/commerce/v1/benefits/user_credit"
    headers = get_headers(url, token)

    payload = {}
    client = AsyncClient(base_url=BASE_URL, default_headers=headers)
    response = await client.post(url, body=payload, cast_to=object)
    if response['data']['credit']['gift_credit'] == 0:  # 签到
        await receive_credit(token)

    logger.debug(bjson(response))
    return response


async def check_token(token, threshold: int = 1):  # todo: 失效还是没积分
    try:
        response = await get_credit(token)
        logger.debug(bjson(response))
        # logger.error(f"{token}")

        credits = sum(response['data']['credit'].values())
        return credits >= threshold
    except Exception as e:
        logger.error(e)
        return False


def create_photo_lip_sync(request: TTSRequest):
    # 映射
    tts_info = {
        "name": request.voice or "魅力姐姐",
        "text": request.input,  # "永远相信美好的事情即将发生"
        "speed": request.seed or 1,
        "source_type": "text-to-speech",
        "tone_category_id": 0,
        "tone_category_key": "all",
        "tone_id": "7382879492752019995",
        "toneKey": request.voice or "魅力姐姐",
    }
    payload = {
        "promptSource": "photo_lip_sync",
        "generateTimes": 1,
        "lipSyncInfo": tts_info,
        "isUseAiGenPrompt": False,
        "batchNumber": 1
    }

    return {
        "submit_id": "",
        "task_extra": json.dumps(payload),
        "http_common_info": {
            "aid": 513695
        },
        "input": {
            "seed": 1834980836,
            "video_gen_inputs": [
                {
                    "v2v_opt": {},
                    "i2v_opt": {
                        "realman_avatar": {
                            "enable": True,
                            "origin_image": {
                                "width": 480,
                                "height": 270,
                                "image_uri": "tos-cn-i-tb4s082cfz/fae8f746367b40f5a708bf0f1e84de11",
                                "image_url": ""  ########## https://oss.ffire.cc/files/kling_watermark.png
                            },
                            "resource_id_loopy": "34464cac-5e3e-46be-88ff-ccbc7da4d742",
                            "resource_id_std": "2f66b408-37c3-4de5-b8a4-ba15c104612e",
                            "origin_audio": {
                                "duration": 3.216,
                                "vid": "v02bc3g10000ctrpqrfog65purfpn7a0"
                            },
                            "tts_info": json.dumps(tts_info)
                        }
                    },
                    "audio_vid": "v02bc3g10000ctrpqrfog65purfpn7a0",
                    "video_mode": 4
                }
            ]
        },
        "mode": "workbench",
        "history_option": {},
        "commerce_info": {
            "resource_id": "generate_video",
            "resource_id_type": "str",
            "resource_sub_type": "aigc",
            "benefit_type": "lip_sync_avatar_std"
        },
        "scene": "lip_sync_image",
        "client_trace_data": {},
        "submit_id_list": [
            "d4554e2c-707f-4ebe-b4e6-93aa6687d1c1"
        ]
    }


if __name__ == '__main__':
    from meutils.config_utils.lark_utils import aget_spreadsheet_values, get_series

    token = "693701c43e477b7c405cc7e2fef0ddbd"
    token = "eb4d120829cfd3ee957943f63d6152ed"
    token = "dcf7bbc31faed9740b0bf748cd4d2c74"
    token = "38d7d300b5e0a803431ef88d8d2acfef"
    token = "916fed81175f5186a2c05375699ea40d"
    token = "7c5e148d9fa858e3180c42f843c20454"
    token = "1c21a9fe6a4230609d7ff13e5cec41ec"
    token = "34438eb03d165737122180caf62a8058"
    token = "ffeee346fbd19eceebb79a7bfbca4bfe"
    # token = "b8bb4cb67dba6c0d1048bdc0596bc461"
    # token = "34438eb03d165737122180caf62a8058"
    # token = "a521dd578adcfb191fad38dd4baab498"
    token = "7d9969ffd8ad2edda7da8fff11cb9434"
    token = "1513337bdba08a1a77fedad95c03bc6c"
    token = "b1cd6317e4d161bbb3889b9defd769ff"
    token = "ed16bb360a4744696f88a7b52b7c10a3"
    # arun(check_token(token))

    arun(get_upload_token(token, 'video'))

    # print(arun(aget_spreadsheet_values(feishu_url=FEISHU_URL, to_dataframe=True))[0].tolist())
    # tokens = arun(get_series(FEISHU_URL))
    # arun(get_credit(token))
    # arun(check_token(token))
    # _ = []
    # for token in tokens:
    #     if not arun(check_token(token)):
    #         logger.debug(f"无效 {token}")
    #         _.append(token)

    # arun(get_upload_token(token))
    #
    # request = ImageRequest(prompt='https://oss.ffire.cc/files/kling_watermark.png笑起来')
    # arun(create_draft_content(request, token))
