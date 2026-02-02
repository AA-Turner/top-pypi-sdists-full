#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : videos
# @Time         : 2024/10/21 20:17
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://platform.minimaxi.com/document/video_generation?key=66d1439376e52fcee2853049
# https://useapi.net/docs/start-here/setup-minimax
# token 过期时间一个月: 看下free hailuo
# https://jwt.io/
import os

# todo: check token

import oss2

from meutils.pipe import *
from meutils.hash_utils import md5
from meutils.io.files_utils import to_bytes, to_image
from meutils.io.image import image_resize

from meutils.jwt_utils import decode_jwt_token
from meutils.schemas.hailuo_types import BASE_URL_ABROAD as BASE_URL

from meutils.schemas.hailuo_types import VideoRequest, VideoResponse
from meutils.decorators.retry import retrying
from meutils.notice.feishu import send_message as _send_message, VIDEOS

from meutils.apis.hailuoai.yy import get_yy
from meutils.apis.hailuoai.utils import PARAMS as params, get_access_token, upload
from meutils.apis.hailuoai import openai_images

from meutils.schemas.video_types import SoraVideoRequest, Video
from meutils.schemas.image_types import ImageRequest

send_message = partial(
    _send_message,
    title=__name__,
    url=VIDEOS
)

APP_ID = '3001'
VERSION_CODE = '22203'

MODEL_MAPPING = {
    # video-01 video-01 video-01-live2d S2V-01

    "t2v-01": "23000",  # 23010
    "t2v-01-director": "23010",

    "i2v-01": "23001",
    "i2v-01-live": "23011",
    "video-01-live2d": "23011",
    "s2v-01": "23021",

    # "23210" # 要积分
}


class Tasks(object):

    def __init__(self, base_url: Optional[str] = None, api_key: str = None):
        self.api_key = api_key

    async def create(self, request: SoraVideoRequest):
        if request.model.startswith(("image", "nano", "seedream", "gpt-image")):
            image_request = ImageRequest(
                model=request.model,
                prompt=request.prompt,
                size=request.size,
                aspect_ratio=request.aspect_ratio,
                resolution=request.resolution,
                image=request.input_reference,
            )
            logger.debug(image_request)
            return await openai_images.generate(image_request, api_key=self.api_key, is_async=True)
        else:
            return await create_task(request, self.api_key)

    async def get(self, task_id: str):
        logger.debug(task_id)

        return await get_task(task_id, self.api_key)


# @retrying(predicate=lambda r: r.base_resp.status_code in {1000061, 1500009})  # 限流
async def create_task(request: SoraVideoRequest, token: Optional[str] = None):
    refresh_token = token or os.getenv("HAILUOAI_API_KEY")
    token = await get_access_token(refresh_token)

    if request.model.startswith("veo"):
        request.seconds = 8
        request.aspect_ratio = request.aspect_ratio or "16:9"

        if image_urls := request.input_reference:
            request.input_reference = await to_image(image_urls)

    elif request.model.startswith("sora"):
        request.seconds = int(request.seconds or 4)
        if request.seconds not in {4, 8, 12}:
            request.seconds = 4
            # request.seconds = min({4, 8, 12}, key=lambda x: x - request.seconds)

        if request.model in {"sora-2-4s", "sora-2-8s", "sora-2-12s"}:  # sora2-i2v 逆向按次
            request.seconds = request.model.rsplit('-', 1)[-1].strip("s")
            request.model = "sora2-i2v"

        request.size = request.size or "16x9"
        w, h = map(int, request.size.split('x'))
        request.aspect_ratio = "16:9" if w > h else "9:16"

        if image_urls := request.input_reference:
            logger.debug(f"request.size: {request.size}")

            _ = await to_image(image_urls[0], response_format="bytes")
            _ = await image_resize(_, request.size, "url")
            request.input_reference = [_]

    if image_urls := request.input_reference or request.first_frame_image or request.last_frame_image:
        request.model = request.model.replace('t2v', 'i2v')

        if request.model.startswith('232'):  # 2.x 首帧 首尾帧   文生统一 23204
            if request.last_frame_image or len(image_urls) == 2:
                request.model = "23210"  # 首尾帧 2.0

            elif request.first_frame_image or len(image_urls) == 1:
                request.model = "23218"  # 首帧 2.3-fast

        elif request.model.startswith('230'):  # 1.0 文生 23000
            request.seconds = 6
            if image_urls:
                request.model = "23001"

    else:
        request.model = request.model.replace('i2v', 't2v')

    payload = {
        "quantity": 1,
        "parameter": {
            "modelID": request.model,
            "desc": request.prompt,
            "fileList": [],
            "useOriginPrompt": False if request.enhance_prompt else True,
            "duration": int(request.seconds or 4),
            "resolution": (request.resolution or "720").rstrip('p').rstrip('P'),
            "aspectRatio": ""
        },
        # "videoExtra": {
        #     "promptStruct": "{\"value\":[{\"type\":\"paragraph\",\"children\":[{\"text\":\"a cat\"}]}],\"length\":5,\"plainLength\":5,\"rawLength\":5}"
        # }
    }

    if request.aspect_ratio:
        payload['parameter']['aspectRatio'] = request.aspect_ratio

    # 图片比例过小，请上传1280x720或720x1280以上规格图片 todo
    if images := request.input_reference:  # todo 处理 file

        payload['parameter']['fileList'] = [
            {
                "frameType": i,
                "url": url,
                # "type": "jpeg",
            }
            for i, url in enumerate(images)
        ]

    if url := request.first_frame_image:
        url = await to_image(url)

        payload['parameter']['fileList'] += [{"url": url, "frameType": 0}]

    if url := request.last_frame_image:
        url = await to_image(url)

        payload['parameter']['fileList'] += [{"url": url, "frameType": 1}]

    logger.debug(bjson(payload))

    path = "/v2/api/multimodal/generate/video"

    headers = {
        'Content-Type': 'application/json',
        'token': token,
        'yy': get_yy(payload, params, path),
    }

    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=60) as client:
        response = await client.post(path, params=params, content=json.dumps(payload))
        response.raise_for_status()

        data = response.json()

        logger.debug(bjson(data))

        if task_id := data.get("data", {}).get("id"):
            return Video(id=task_id, status=data)
        else:
            return Video(status='failed', error=data.get("statusInfo"))


async def get_task(task_id: str, token: str):
    payload = {
        "batchInfoList": [
            {
                "batchID": task_id,
                "batchType": 0  # video
            },
            {
                "batchID": task_id,
                "batchType": 1  # image
            }
        ],
        "type": 1
    }

    # {"batchInfoList": [{"batchID": "472359176514654211", "batchType": 0}], "type": 1}

    path = "/v4/api/multimodal/video/processing"
    headers = {
        'Content-Type': 'application/json',
        'token': token,
        'yy': get_yy(payload, params, url=path),
    }

    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=60) as client:
        response = await client.post(path, params=params, content=json.dumps(payload)
                                     )
        response.raise_for_status()
        data = response.json()

        logger.debug(bjson(data))

        # if any(i in str(data) for i in {"内容生成失败", "请求异常"}):
        #     raise Exception(f"invalid image: {task_id} \n\n {request.prompt[:1000]}")

        if batchs := data['data']['batchVideos']:
            for batch in batchs:
                if batch["batchID"] == task_id:
                    _ = batch["assets"][0]
                    logger.debug(bjson(_))

                    # 1: "Processing",
                    # 2: "Success",
                    error = None
                    status = "queued"

                    if _.get("status") == 12:
                        status = "queued"
                    elif _.get("status") == 1:
                        status = "in_progress"
                    elif _.get("status") == 2:
                        status = "completed"
                    elif _.get("status") in {3, 5, 7, 14}:  # 失败枚举值
                        status = "failed"
                        error = {"code": _.get("status"), "message": f"""{_.get("message", "")}\n{_.get("desc")}"""}

                    video = Video(
                        id=task_id,
                        video_url=_.get("downloadURL"),

                        progress=min(_.get("percent", 11), 99),

                        created_at=_.get("createTime"),

                        status=status,
                        error=error,
                        # metadata=error and _ or None

                        metadata={"prompt": _.get("desc")}
                    )

                    if video.video_url:
                        video.progress = 100

                    return video
        return Video(id=task_id)


if __name__ == '__main__':
    token = None
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NzIzNTA5NjUsInVzZXIiOnsiaWQiOiI0Njk4ODIxOTY3NDM1Mjg0NDkiLCJuYW1lIjoiYWZzbCBkcnF2IiwiYXZhdGFyIjoiIiwiZGV2aWNlSUQiOiIzMTE2NzAxODUwMDg0ODg0NTIiLCJpc0Fub255bW91cyI6ZmFsc2V9fQ.3pO0O36-um2fQs0ML0eHwpi0D7rV5yjmnjcpuiZcNKw"

    model = "veo3.1-t2v-fast"
    model = "23000"
    # model = "23218"
    #
    model = "veo3.1-i2v-fast_1080p"
    # model = "veo3.1-i2v-fast_3840"
    # model = "sora2-i2v"

    model = "sora-2-4s"

    # 23010
    # 472553170574090241

    MODEL_MAPPING = {
        # video-01 video-01 video-01-live2d S2V-01

        "t2v-01": "23000",  # 23010
        "i2v-01": "23001",

        "01-director": "23102",
        "01-live": "23011",

        "s2v-01": "23021",

        # 23200 # 2.0 文生
        # 23210 # 2.0

        # 23204 # 2.3 文生
        # 23217 # 2.3

        # 23218 # 2.3-fast
    }

    request = SoraVideoRequest(
        # model="t2v-01",
        model=model,
        # model="S2V-01-live",
        seconds=61,

        # prompt="smile",  # 307145017365086216
        # prompt="把小黄鸭放在衣服上",  # 307145017365086216
        # prompt="一个裸体少女",  # 307145017365086216
        prompt="A whimsical flying elephant soaring over a vibrant candy-colored cityscape at sunset, with rainbow trails behind its wings, playful monkeys riding on its back throwing confetti, in a whimsical animated style like a Pixar movie, camera panning smoothly from ground level to aerial view",
        # 307145017365086216

        # enhance_prompt=True,

        # input_reference="https://cdn.hailuoai.video/moss/prod/2026-01-26-18/user/multi_chat_file/8ac50491-63ec-46fc-9f98-94d287552003.jpeg"

        input_reference=["https://s3.ffire.cc/files/jimeng.jpg"] * 1,
        # first_frame_image="https://s3.ffire.cc/files/jimeng.jpg",
        # last_frame_image="https://cdn.hailuoai.video/moss/prod/2026-01-26-18/user/multi_chat_file/8ac50491-63ec-46fc-9f98-94d287552003.jpeg",

        # first_frame_image="https://v3.fal.media/files/penguin/XoW0qavfF-ahg-jX4BMyL_image.webp",
        # last_frame_image="https://v3.fal.media/files/tiger/bml6YA7DWJXOigadvxk75_image.webp",

        # resolution="768P"

        # size="16:9"
        # size="720x1280"
        size="16x9"
    )

    data = {
        "model": "veo3.1-i2v-fast",
        "prompt": "第一人称视角ASMR视频，画幅比例9:16，沉浸式体验切割物体的声音。切割时，物体表面坚硬，需要用力才能切入，伴随清晰的开裂脆响。当工具穿透表层的瞬间，内部的金币猛地爆开飞溅，发出密集的金属碰撞声与清脆的掉落声。随着工具完全切开，物体裂成两半并重重砸落在桌面上，大量金币从切口处喷涌而出、散落四周，营造出充满惊喜与满足感的听觉体验",
        "seconds": 8,
        "input_reference": [
            "https://s3.ffire.cc/cdn/20260131/sNQLXjrfPFph26no3Jizvs.jpeg"
        ],
        "resolution": "720",
        "size": "16:9"

    }

    request = SoraVideoRequest(**data)

    # "图片上传失败，长宽比需在 5:2 和 2:5 之间"

    r = arun(create_task(request, token=token))

    # task_id = "hailuoai-469852272096808964"

    # {"quantity": 1, "parameter": {"modelID": "sora2-i2v", "desc": "笑起来啊", "fileList": [{"id": "469914687591321600",
    #                                                                                         "url": "https://cdn.hailuoai.video/moss/prod/2026-01-20-15/user/multi_chat_file/997398be-fe17-4af1-ac9f-7057a54e5587.jpeg?x-oss-process=image/resize,p_50/format,webp",
    #                                                                                         "name": "cropped_1768892531810.jpeg",
    #                                                                                         "type": "jpeg",
    #                                                                                         "frameType": 0}],
    #                               "useOriginPrompt": true, "resolution": "720", "duration": 4, "aspectRatio": "16:9"},
    #  "videoExtra": {
    #      "promptStruct": "{\"value\":[{\"type\":\"paragraph\",\"children\":[{\"text\":\"笑起来啊\"}]}],\"length\":4,\"plainLength\":4,\"rawLength\":4}"}}

    # data = {
    #     "model": "video-01",
    #     "prompt": "画面中两个人非常缓慢地拥抱在一起",
    #     "prompt_optimizer": True,
    #     # "first_frame_image": "https://hg-face-domestic-hz.oss-cn-hangzhou.aliyuncs.com/avatarapp/ai-cache/54883340-954c-11ef-8920-db8e7bfa3fdf.jpeg"
    # }
    # request = VideoRequest(**data)
    # task_id = "472543767246442500"
    # task_id = "472553541371510788"
    # task_id = "472555135056019456"
    # 472564985043406853

    # task_id = "472565145953669122"
    #
    # task_id = "472565145957863429"
    #
    # "data": {
    #     "id": "472567022007164928",
    #     "task": {
    #         "batchID": "472567022002970627",
    #         "videoIDs": [
    #             "472567022007164928"
    #         ]
    #     },
    #     "isFirstGenerate": false,

    task_id = "472578691764686853"
    task_id = "472578758479253512"
    task_id = "472581277544718343"
    task_id = "472752130559369221"
    # arun(get_task(task_id=task_id, token=token))
