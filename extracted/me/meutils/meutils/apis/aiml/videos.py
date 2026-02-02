#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : videos
# @Time         : 2025/11/5 18:01
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : todo https://docs.aimlapi.com/api-references/video-models/minimax/hailuo-02

# todo hailuo2.0 首尾帧

from meutils.pipe import *
from openai import AsyncOpenAI
from meutils.schemas.video_types import SoraVideoRequest, Video
from meutils.io.files_utils import to_base64, to_url_fal
from meutils.io.image import image_resize

"""
model
undefined · enum
Possible values: alibaba/wan2.5-i2v-preview
prompt
string · min: 1 · max: 800
The text description of the scene, subject, or action to generate in the video.

image_url
string · uri
A direct link to an online image or a Base64-encoded local image that will serve as the visual base or the first frame for the video.

resolution
string · enum
An enumeration where the short side of the video frame determines the resolution.

Default: 720p
Possible values: 480p720p1080p
duration
integer · enum
The length of the output video in seconds.

Possible values: 510
negative_prompt
string
The description of elements to avoid in the generated video.

enable_prompt_expansion
boolean
Whether to enable prompt expansion.

Default: true
seed
integer
Varying the seed integer is a way to get different results for the same other request parameters. Using the same value for an identical request will produce similar results. If unspecified, a random number is chosen.
"""


class Tasks(object):

    def __init__(self, base_url: Optional[str] = None, api_key: str = None):
        base_url = "https://api.aimlapi.com/v2"
        self.client = AsyncOpenAI(base_url=base_url, api_key=api_key)

    async def create(self, request: SoraVideoRequest):
        payload = {
            "model": request.model,
            "prompt": request.prompt,

            **(request.metadata or {})
        }

        if request.seconds:
            payload["duration"] = int(request.seconds)

        if request.resolution:
            payload['resolution'] = request.resolution

        if request.ratio:
            payload["aspect_ratio"] = request.ratio

        if request.generate_audio is not None:
            payload["generate_audio_switch"] = request.generate_audio

        if request.style is not None:
            payload["style"] = request.style

        if image_urls := request.input_reference:
            if any(i in request.model for i in {'sora', }):
                logger.debug(bjson(payload))

                if 'sora' in request.model:
                    w, h = map(int, request.size.split('x'))
                    payload["aspect_ratio"] = "16:9" if w > h else "9:16"

                image_urls[0] = await image_resize(image_urls[0], request.size, "url")

                logger.debug(image_urls)

            elif 'luma' in request.model:
                payload["keyframes"] = {
                    f"frame{i}": {
                        "type": "image",
                        "url": url
                    }

                    for i, url in enumerate(image_urls)}

            elif 'runway' in request.model:
                payload["references"] = [
                    {
                        "type": "image",
                        "url": url
                    }

                    for i, url in enumerate(image_urls)
                ]

            payload['model'] = request.model.replace("text-to-video", "image-to-video").replace("t2v", "i2v")

            # if len(image_urls) > 1:
            #     payload["image_list"] = image_urls
            # else:
            #     payload["image_url"] = image_urls[0]

            payload["image_url"] = image_urls[0]
            payload["image_list"] = image_urls

            # https://aimlapi.com/models/veo-3-1-reference-to-video
            # 模型区分 参考图 首尾帧
            # if any( i in request.model for i in {"veo"}):

            # klingai/video-o1-reference-to-video image_list
            # klingai/video-o1-image-to-video image_url last_image_url

        else:
            payload['model'] = request.model.replace("image-to-video", "text-to-video").replace("i2v", "t2v")

        # 首尾帧
        if request.first_frame_image:
            if request.model.startswith(("klingai/video-o1",)):
                payload['model'] = "klingai/video-o1-image-to-video"

            payload["image_url"] = request.first_frame_image
            payload["first_frame_image"] = request.first_frame_image

        if request.last_frame_image:
            payload["last_image_url"] = request.last_frame_image

        # 数字人 对口型
        if request.audio and any(i in request.model for i in {"omnihuman", 'avatar'}):
            payload['image_url'] = request.image
            payload['audio_url'] = request.audio

        if request.video:
            if request.model.startswith(("alibaba/wan-2-6",)):
                payload["video_urls"] = [request.video]
                payload['model'] = "alibaba/wan-2-6-r2v"

            elif request.model.startswith(("runway",)):
                payload['frame_size'] = (request.size or "1280:720").replace('x', ':')
                payload["video_url"] = request.video


            else:
                payload["video_url"] = request.video
                payload['keep_audio'] = True

                if request.model.endswith('edit'):  # kling
                    payload['model'] = "klingai/video-o1-video-to-video-edit"
                else:
                    payload['model'] = "klingai/video-o1-video-to-video-reference"

        logany(bjson(payload))

        response = await self.client.post(
            path="/video/generations",
            body=payload,
            cast_to=object
        )
        """
        {
    "id": "9913239d-4fa8-47ea-b51d-d313e29caba5:alibaba/wan2.5-i2v-preview",
    "status": "queued",
    "meta": {
        "usage": {
            "tokens_used": 105000
        }
    }
    
    {
    "generation_id": "339995387916622:minimax/hailuo-02",
    "status": "queued",
    "meta": {
        "usage": {
            "tokens_used": 588000
        }
    }
}
}
        """

        logger.debug(bjson(response))

        return response

    async def get(self, task_id: str):
        logger.debug(task_id)

        response = await self.client.get(
            path=f"/video/generations?generation_id={task_id}",
            cast_to=object
        )
        """
        {
    "id": "9913239d-4fa8-47ea-b51d-d313e29caba5:alibaba/wan2.5-i2v-preview",
    "status": "completed",
    "video": {
        "url": "https://cdn.aimlapi.com/alpaca/1d/dd/20251107/30b07d9c/42740107-9913239d-4fa8-47ea-b51d-d313e29caba5.mp4?Expires=1762593280&OSSAccessKeyId=LTAI5tBLUzt9WaK89DU8aECd&Signature=Guk6apyEnKeuniLv0mcBJhkHO%2FI%3D"
    }
}

{
    "id": "",
    "status": "unknown",
    "error": {
        "name": "Error",
        "message": "invalid params, task_id cannot by empty"
    }
}

        """
        logger.debug(bjson(response))

        status = response
        if response.get('error'):
            status = 'failed'

        video = Video(
            id=task_id,
            status=status,
            video_url=(response.get("video") or {}).get("url"),

            error=response.get("error")
        )

        # logger.debug(bjson(video))

        return video


if __name__ == "__main__":
    api_key = "603051fc1d7e49e19de2c67521d4a30e"
    # a63443199c3e42ea90003e0261ccb246
    api_key = "a63443199c3e42ea90003e0261ccb246"

    model = "alibaba/wan2.5-i2v-preview"
    model = "minimax/hailuo-02"
    # model = "minimax/hailuo-02_1080P"
    # model = "minimax/hailuo-2.3-fast"
    # model = "minimax/hailuo-2.3-fast_768P"

    # model = "alibaba/wan2.5-i2v-preview_480p"

    # model = "kling-video-o1"
    # model = "kling-video-o1-video-to-video-edit" => "klingai/video-o1-video-to-video-edit"

    # model = "klingai/video-o1-reference-to-video"

    #         "model": "klingai/video-o1-video-to-video-reference",
    #         "model": "klingai/video-o1-video-to-video-edit",

    # model = "alibaba/wan-2-6-t2v_720p"

    # model = "openai/sora-2-pro-i2v"
    # model = "openai/sora-2-i2v"

    # 数字人
    # model = "klingai/avatar-standard"
    # model = "klingai/avatar-pro"
    # model = "bytedance/omnihuman/v1.5"

    # luma
    # model = "luma/ray-2"
    # model = "luma/ray-flash-2"
    #
    # # runway
    # model = "runway/gen4_turbo"
    # model = "runway/gen4_aleph"
    #
    # model = "pixverse/v5-5-image-to-video"

    # todo klingai/video-v2-6-pro-motion-control

    data = {
        "model": model,
        "prompt": '''Mona Lisa nervously puts on glasses with her hands and asks her off-screen friend to the left: ‘Do they suit me?’ She then tilts her head slightly to one side and then the other, so the unseen friend can better judge.''',
        "input_reference": "https://s2-111386.kwimgs.com/bs2/mmu-aiplatform-temp/kling/20240620/1.jpeg",
        # "resolution": "480p",
        "seconds": "4",
    }

    data = {
        "model": model,
        "prompt": '''Mona Lisa nervously puts on glasses with her hands and asks her off-screen friend to the left: ‘Do they suit me?’ She then tilts her head slightly to one side and then the other, so the unseen friend can better judge.''',
        "input_reference": "https://ark-project.tos-cn-beijing.volces.com/doc_image/seepro_first_frame.jpeg,https://ark-project.tos-cn-beijing.volces.com/doc_image/seepro_last_frame.jpeg",
        # "resolution": "480p",
        "seconds": "5",
    }

    data = {
        "model": model,
        "prompt": "A graceful ballerina dancing outside a circus tent on green grass, with colorful wildflowers swaying around her as she twirls and poses in the meadow.",
        # "input_reference": [
        #     "https://storage.googleapis.com/falserverless/example_inputs/veo31-r2v-input-1.png",
        #     "https://storage.googleapis.com/falserverless/example_inputs/veo31-r2v-input-2.png",
        #     # "https://storage.googleapis.com/falserverless/example_inputs/veo31-r2v-input-3.png"
        # ],
        "first_frame_image": "https://storage.googleapis.com/falserverless/example_inputs/veo31-r2v-input-1.png",
        "last_frame_image": "https://storage.googleapis.com/falserverless/example_inputs/veo31-r2v-input-2.png",

        # "video": "https://zovi0.github.io/public_misc/kling-v2-master-t2v-racoon.mp4",

        # "size": "1792x1024",
        # "size": "720x1280",
        # "size": "1280x720",

        # "size": "16:9",

        "seconds": "6",
        # "resolution": "720p"
    }

    data = {"prompt": "飞起来", "model": model,
            "size": "1920x1080",
            "seconds": "6",
            "first_frame_image": "https://111-1318855541.cos.ap-guangzhou.myqcloud.com/mirrorsea-flow/20260125/f2e1ee1e302e4bc5a0d813e72a2de1f6.jpg",
            "last_frame_image": "https://111-1318855541.cos.ap-guangzhou.myqcloud.com/mirrorsea-flow/20260125/b148adc981ba4bb9b85b6e2e1801c730.jpg"}
    # data = {
    #     "model": model,
    #     "prompt": "A graceful ballerina dancing outside a circus tent on green grass, with colorful wildflowers swaying around her as she twirls and poses in the meadow.",
    #     # "input_reference": [
    #     #     "https://storage.googleapis.com/falserverless/example_inputs/veo31-r2v-input-1.png",
    #     #     "https://storage.googleapis.com/falserverless/example_inputs/veo31-r2v-input-2.png",
    #     #     # "https://storage.googleapis.com/falserverless/example_inputs/veo31-r2v-input-3.png"
    #     # ],
    #
    #     "first_frame_image": "https://storage.googleapis.com/falserverless/example_inputs/veo31-r2v-input-1.png",
    #     "last_frame_image": "https://storage.googleapis.com/falserverless/example_inputs/veo31-r2v-input-2.png",
    #
    #     # "size": "1792x1024",
    #     # "size": "720x1280",
    #     # "size": "1280x720",
    #
    #     # "size": "16:9",
    #
    #     "seconds": "5",
    #     # "resolution": "720p"
    # }
    # data = {
    #     "model": model,
    #     "prompt": "A powerful, matte black jeep, its robust frame contrasting with the lush green surroundings, navigates a winding jungle road, kicking up small clouds of dust and loose earth from its tires.",
    #     "video": "https://storage.googleapis.com/falserverless/example_inputs/krea_wan_14b_v2v_input.mp4"
    # }

    # {
    #     "model": "klingai/video-o1-image-to-video",
    #     "prompt": "A jellyfish in the ocean",
    #     "image_url": "https://upload.wikimedia.org/wikipedia/commons/3/35/Maldivesfish2.jpg",
    # }
    # {
    #     "model": "klingai/video-o1-video-to-video-edit",
    #     "prompt": "A powerful, matte black jeep, its robust frame contrasting with the lush green surroundings, navigates a winding jungle road, kicking up small clouds of dust and loose earth from its tires.",
    #     "video_url": "https://storage.googleapis.com/falserverless/example_inputs/krea_wan_14b_v2v_input.mp4"
    # }
    #

    # }

    # {
    #     "model": "klingai/video-v2-6-pro-image-to-video",
    #     "prompt": "A jellyfish in the ocean",
    #     "image_url": "https://upload.wikimedia.org/wikipedia/commons/3/35/Maldivesfish2.jpg",
    # }
    #
    #
    # data = {
    #     "model": "klingai/video-v2-6-pro-text-to-video",
    #     "prompt": "A DJ on the stand is playing, around a World War II battlefield, lots of explosions, thousands of dancing soldiers, between tanks shooting, barbed wire fences, lots of smoke and fire, black and white old video: hyper realistic, photorealistic, photography, super detailed, very sharp, on a very white background"
    # }

    # data = {
    #     "model": model,
    #     "image": "https://s2-111386.kwimgs.com/bs2/mmu-aiplatform-temp/kling/20240620/1.jpeg",
    #     "audio": "https://storage.googleapis.com/falserverless/example_inputs/omnihuman_audio.mp3"
    # }

    request = SoraVideoRequest(**data)

    logger.debug(bjson(request))

    tasks = Tasks(api_key=api_key)
    # arun(tasks.create(request))

    # 8ScCA7OzgWOHmwol1YMtJ

    # task_id = "9913239d-4fa8-47ea-b51d-d313e29caba5:alibaba/wan2.5-i2v-preview"
    # task_id = "nltmquwNYRj6xNz-0PSaC"
    task_id = "AaNgOpmRIehrLgl1kjYVG"
    arun(tasks.get(task_id))
