#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : lip_sync
# @Time         : 2025/1/3 16:17
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
"""
1. 上传图片 image_to_avatar检测
2. 上传视频 video_to_avatar检测
3. 上传音频+创建任务

"""
import asyncio
import json

from meutils.apis.jimeng.doubao_utils import generate_jimeng_params
from meutils.pipe import *
from meutils.str_utils.json_utils import json_path

from meutils.schemas.jimeng_types import BASE_URL
from meutils.schemas.video_types import SoraVideoRequest

from meutils.schemas.task_types import TaskResponse
from meutils.apis.jimeng.common import get_headers, check_token
from meutils.apis.jimeng.files import upload_for_image, upload_for_video

from fake_useragent import UserAgent

ua = UserAgent()


async def get_task(task_id: str, token: str = "916fed81175f5186a2c05375699ea40d"):
    task_ids = task_id.split()

    url = "/mweb/v1/mget_generate_task"
    url = "/mweb/v1/get_history_queue_info"
    headers = get_headers(url, token)

    payload = {"task_id_list": task_ids}
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=60) as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        logger.debug(bjson(data))

        if video_urls := json_path(data, "$..video_url"):  # 角色检测 create_realman_avatar

            task_data = dict(zip(["video"] * len(video_urls), video_urls))
            response = TaskResponse(task_id=task_id, data=task_data, status="success")
            return response

        else:
            response = TaskResponse(task_id=task_id)
            if (
                    (fail_codes := json_path(data, "$..fail_code"))
                    and fail_codes[-1] != "0"
                    and (messages := json_path(data, "$..fail_msg"))
            ):
                response.message = f"{str(messages).lower().replace('success', '')}:{fail_codes}"
                response.status = "fail"
                return response

            if will_cost := json_path(data, "$..will_cost"):
                response.will_cost = will_cost[0]

            if video_urls := json_path(data, "$..[360p,480p,720p].video_url"):
                response.data = [{"video": _} for _ in video_urls]
                response.status = "success"

            response.fail_code = fail_codes and fail_codes[-1]
            return response


async def create_task(request: SoraVideoRequest, token: Optional[str] = None):
    url = "/mweb/v1/aigc_draft/generate"

    headers = get_headers(url, token)
    params = generate_jimeng_params()

    request.duration = int(request.seconds or 1)

    payload = {
        "extend": {
            "root_model": "dreamina_seedance_40_pro",
            "m_video_commerce_info": {
                "benefit_type": "dreamina_video_seedance_20_pro",
                "resource_id": "generate_video",
                "resource_id_type": "str",
                "resource_sub_type": "aigc"
            },
            "m_video_commerce_info_list": [
                {
                    "benefit_type": "dreamina_video_seedance_20_pro",
                    "resource_id": "generate_video",
                    "resource_id_type": "str",
                    "resource_sub_type": "aigc"
                }
            ]
        },
        "submit_id": "9c50c667-41a1-4c54-a517-4be96919e85b",
        "metrics_extra": "{\"promptSource\":\"custom\",\"isDefaultSeed\":1,\"originSubmitId\":\"9c50c667-41a1-4c54-a517-4be96919e85b\",\"isRegenerate\":false,\"enterFrom\":\"click\",\"position\":\"page_bottom_box\",\"functionMode\":\"first_last_frames\",\"sceneOptions\":\"[{\\\"type\\\":\\\"video\\\",\\\"scene\\\":\\\"BasicVideoGenerateButton\\\",\\\"modelReqKey\\\":\\\"dreamina_seedance_40_pro\\\",\\\"videoDuration\\\":9,\\\"reportParams\\\":{\\\"enterSource\\\":\\\"generate\\\",\\\"vipSource\\\":\\\"generate\\\",\\\"extraVipFunctionKey\\\":\\\"dreamina_seedance_40_pro\\\",\\\"useVipFunctionDetailsReporterHoc\\\":true},\\\"materialTypes\\\":[]}]\"}",
        "draft_content": "{\"type\":\"draft\",\"id\":\"94aa382f-ce99-4308-3acd-6c6d33c780e5\",\"min_version\":\"3.0.5\",\"min_features\":[],\"is_from_tsn\":true,\"version\":\"3.3.9\",\"main_component_id\":\"9bdf4947-1f2b-87aa-9b23-240faa0bef8f\",\"component_list\":[{\"type\":\"video_base_component\",\"id\":\"9bdf4947-1f2b-87aa-9b23-240faa0bef8f\",\"min_version\":\"1.0.0\",\"aigc_mode\":\"workbench\",\"metadata\":{\"type\":\"\",\"id\":\"90515d13-4557-23c3-9dca-6f6fb6194d40\",\"created_platform\":3,\"created_platform_version\":\"\",\"created_time_in_ms\":\"1770692785855\",\"created_did\":\"\"},\"generate_type\":\"gen_video\",\"abilities\":{\"type\":\"\",\"id\":\"e2458f1a-0615-50a4-44d7-0350cac452b8\",\"gen_video\":{\"type\":\"\",\"id\":\"6ad3bae5-4562-2cb8-eaa3-9582ddf5fac8\",\"text_to_video_params\":{\"type\":\"\",\"id\":\"3fe8633d-0e29-3a58-5648-7221bd7f9378\",\"video_gen_inputs\":[{\"type\":\"\",\"id\":\"47410404-3b72-6e26-474a-9896806c9f38\",\"min_version\":\"3.0.5\",\"prompt\":\"a cat\",\"video_mode\":2,\"fps\":24,\"duration_ms\":9000,\"idip_meta_list\":[]}],\"video_aspect_ratio\":\"16:9\",\"seed\":301214761,\"model_req_key\":\"dreamina_seedance_40_pro\",\"priority\":0},\"video_task_extra\":\"{\\\"promptSource\\\":\\\"custom\\\",\\\"isDefaultSeed\\\":1,\\\"originSubmitId\\\":\\\"9c50c667-41a1-4c54-a517-4be96919e85b\\\",\\\"isRegenerate\\\":false,\\\"enterFrom\\\":\\\"click\\\",\\\"position\\\":\\\"page_bottom_box\\\",\\\"functionMode\\\":\\\"first_last_frames\\\",\\\"sceneOptions\\\":\\\"[{\\\\\\\"type\\\\\\\":\\\\\\\"video\\\\\\\",\\\\\\\"scene\\\\\\\":\\\\\\\"BasicVideoGenerateButton\\\\\\\",\\\\\\\"modelReqKey\\\\\\\":\\\\\\\"dreamina_seedance_40_pro\\\\\\\",\\\\\\\"videoDuration\\\\\\\":9,\\\\\\\"reportParams\\\\\\\":{\\\\\\\"enterSource\\\\\\\":\\\\\\\"generate\\\\\\\",\\\\\\\"vipSource\\\\\\\":\\\\\\\"generate\\\\\\\",\\\\\\\"extraVipFunctionKey\\\\\\\":\\\\\\\"dreamina_seedance_40_pro\\\\\\\",\\\\\\\"useVipFunctionDetailsReporterHoc\\\\\\\":true},\\\\\\\"materialTypes\\\\\\\":[]}]\\\"}\"}},\"process_type\":1}]}",
        "http_common_info": {
            "aid": 513695
        }
    }

    payload['submit_id'] = str(uuid.uuid4())

    scene_options = [
        {
            "type": "video",
            "scene": "BasicVideoGenerateButton",
            "modelReqKey": "dreamina_seedance_40_pro",
            "videoDuration": request.duration,
            "reportParams": {
                "enterSource": "generate",
                "vipSource": "generate",
                "extraVipFunctionKey": "dreamina_seedance_40_pro",
                "useVipFunctionDetailsReporterHoc": True
            },
            "materialTypes": []
        }
    ]
    metrics_extra = {
        "promptSource": "custom",
        "isDefaultSeed": 1,
        "originSubmitId": payload['submit_id'],
        "isRegenerate": False,
        "enterFrom": "click",
        "position": "page_bottom_box",
        "functionMode": "first_last_frames",
        "sceneOptions": json.dumps(scene_options)
    }

    payload["metrics_extra"] = json.dumps(metrics_extra)

    video_task_extra = {
        "promptSource": "custom",
        "isDefaultSeed": 1,
        "originSubmitId": payload['submit_id'],
        "isRegenerate": False,
        "enterFrom": "click",
        "position": "page_bottom_box",
        "functionMode": "first_last_frames",
        "sceneOptions": metrics_extra["sceneOptions"]
    }
    #
    main_component_id = str(uuid.uuid4())
    #
    draft_content = {
        "type": "draft",
        "id": str(uuid.uuid4()),
        "min_version": "3.0.5",
        "min_features": [],
        "is_from_tsn": True,
        "version": "3.3.9",
        "main_component_id": main_component_id,
        "component_list": [
            {
                "type": "video_base_component",
                "id": main_component_id,
                "min_version": "1.0.0",
                "aigc_mode": "workbench",
                "metadata": {
                    "type": "",
                    "id": str(uuid.uuid4()),
                    "created_platform": 3,
                    "created_platform_version": "",
                    "created_time_in_ms": "1770691641752",
                    "created_did": ""
                },
                "generate_type": "gen_video",
                "abilities": {
                    "type": "",
                    "id": str(uuid.uuid4()),
                    "gen_video": {
                        "type": "",
                        "id": str(uuid.uuid4()),
                        "text_to_video_params": {
                            "type": "",
                            "id": str(uuid.uuid4()),
                            "video_gen_inputs": [
                                {
                                    "type": "",
                                    "id": str(uuid.uuid4()),
                                    "min_version": "3.0.5",
                                    "prompt": request.prompt,
                                    "video_mode": 2,
                                    "fps": 24,
                                    "duration_ms": request.duration * 1000,
                                    "idip_meta_list": []
                                }
                            ],
                            "video_aspect_ratio": request.aspect_ratio,
                            "seed": 2868096692,
                            "model_req_key": "dreamina_seedance_40_pro",
                            "priority": 0
                        },
                        "video_task_extra": json.dumps(video_task_extra)
                    }
                },
                "process_type": 1
            }
        ]
    }

    payload["draft_content"] = json.dumps(draft_content)

    # if request.image_url:
    #     # image_url = "tos-cn-i-tb4s082cfz/a116c6a9dcbc41b889f9aabdef645456"
    #     image_url = await upload_for_image(request.image_url, token, biz="video")
    #     # vid, uri = await upload_for_video(request.image_url, token)
    #     # logger.debug(f"vid: {vid}, uri: {uri}")
    #     payload['input'].pop('video_aspect_ratio', None)
    #     payload['input']['video_gen_inputs'][0]['first_frame_image'] = {
    #         "width": 1024,
    #         "height": 1024,
    #         "image_uri": image_url
    #     }

    logger.debug(bjson(payload))

    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=60) as client:
        response = await client.post(url, json=payload, params=params)
        response.raise_for_status()
        data = response.json()
        logger.debug(bjson(data))

    if task_ids := json_path(data, "$..task.task_id"):
        task_id = task_ids[0]
        return TaskResponse(task_id=task_id, system_fingerprint=token)

    else:
        """
       {
           "ret": "1018",
           "errmsg": "account punish limit ai generate",
           "systime": "1749027488",
           "logid": "202506041658081AB86654C66682A7DE2E",
           "data": null
       }
        """

        raise Exception(data)


if __name__ == '__main__':
    token = None
    api_key = token = "4a7a0a0515b0a972a879170a065c795e"

    request = SoraVideoRequest(
        model="dreamina_seedance_40_pro",
        prompt="笑起来",
        # image_url="https://oss.ffire.cc/files/kling_watermark.png",  # 图生有问题
    )

    # with timer():
    #     r = arun(create_task(request, token=api_key))
    #     print(r)

    # arun(get_task(r.task_id))
    # arun(get_task(r.task_id, "d2d142fc877e696484cc2fc521127b36"))
    task_id = "9022527206924"

    arun(get_task(task_id, token))
