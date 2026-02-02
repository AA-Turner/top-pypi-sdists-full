#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : videos
# @Time         : 2025/12/22 14:56
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 


from meutils.pipe import *
from meutils.schemas.video_types import SoraVideoRequest, Video
from meutils.io.image import image_resize

import replicate


class Tasks(object):

    def __init__(self, base_url: Optional[str] = None, api_key: str = None):
        api_key = api_key or os.getenv("REPLICATE_API_KEY")
        self.client = replicate.client.Client(api_token=api_key)

    async def create(self, request: SoraVideoRequest):
        payload = {}
        if request.model.startswith("openai/sora-2"):
            payload = {
                "prompt": request.prompt,
                "seconds": int(request.seconds or 4),
                "aspect_ratio": "landscape",
            }
            # Portrait is 720x1280, landscape is 1280x720
            request.size = request.size or "1280x720"
            w, h = map(int, request.size.split('x'))
            if w < h:
                payload["aspect_ratio"] = "portrait"

            if request.resolution:  # openai/sora-2-pro
                payload['resolution'] = request.resolution  # high 1024p 0.3 0.5

            if image_urls := request.input_reference:
                image_urls[0] = await image_resize(image_urls[0], request.size, "url")
                payload["input_reference"] = image_urls[0]

        elif request.model.startswith("kwaivgi/kling-v2.6-motion-control"):
            payload = {
                "mode": "std",
                "image": request.model,
                "video": request.video,
                "prompt": request.prompt,
                "keep_original_sound": True,
                "character_orientation": "image"
            }
            if request.character_orientation:
                payload["character_orientation"] = request.character_orientation

            if request.keep_audio is not None:
                payload["keep_original_sound"] = request.keep_audio

            if request.model.endswith("-pro"):  # pro
                payload["mode"] = "pro"
                request.model = request.model.strip("-pro")

        elif request.model.startswith("kwaivgi/kling-v2.6"):
            payload = {
                "duration": int(request.seconds or 5),

                "prompt": request.prompt,
                "negative_prompt": "",
                "generate_audio": True,
            }

            if request.generate_audio is not None:
                payload["generate_audio"] = request.keep_audio

            if request.first_frame_image:
                payload["start_image"] = request.first_frame_image

            if image_urls := request.input_reference:
                payload["start_image"] = image_urls[0]

        # payload = {
        #     "prompt": request.prompt,
        #     "duration": int(request.seconds),
        #     "resolution": request.resolution,
        #     "multi_shots": False,
        #     "negative_prompt": "",
        #     "enable_prompt_expansion": True,
        #     # "image": "https://replicate.delivery/pbxt/OF1th8iUuEue0j7p1dces9rrhbss2tri6zIrvWxFSUEAaiVw/replicate-prediction-gbdjrctjksrme0cv4m58vwtdtr.jpg",
        #
        # }
        #
        # if request.size:
        #     # if "x" not in request.size:
        #     #     raise ValueError(f"size must be in format of 1280x720")
        #     w, h = 16, 9
        #     if 'x' in request.size:
        #         w, h = map(int, request.size.split('x'))
        #     elif ':' in request.size:
        #         w, h = map(int, request.size.split(':'))
        #     elif '*' in request.size:
        #         w, h = map(int, request.size.split('*'))
        #
        #     if request.resolution in {"720p", None}:
        #         payload["size"] = "1280*720" if w > h else "720*1280"
        #     elif request.resolution == "1080p":
        #         payload["size"] = "1920*1080" if w > h else "1080*1920"
        #
        # if request.input_reference:
        #     request.model = request.model.replace("t2v", "i2v")
        #     payload["image"] = request.input_reference[0]
        #
        # if request.audio:
        #     payload["audio"] = request.audio

        logany(bjson(payload))

        response = await self.client.predictions.async_create(
            model=request.model,
            input=payload
        )
        """
        Prediction(id='vzykqfxg2hrmt0cv8khte3g11g', model='wan-video/wan-2.6-i2v', version='hidden', status='starting', input={'duration': 5, 'enable_prompt_expansion': True, 'image': 'https://replicate.delivery/pbxt/OF1th8iUuEue0j7p1dces9rrhbss2tri6zIrvWxFSUEAaiVw/replicate-prediction-gbdjrctjksrme0cv4m58vwtdtr.jpg', 'multi_shots': False, 'negative_prompt': '', 'prompt': 'The vintage clock on the table starts ticking, gears visibly turning inside the glass case, pendulum swinging smoothly, dust particles floating in sunlight beams, close-up macro shot with shallow depth of field.', 'resolution': '720p'}, output=None, logs='', error=None, metrics=None, created_at='2025-12-22T07:08:51.092Z', started_at=None, completed_at=None, urls={'cancel': 'https://api.replicate.com/v1/predictions/vzykqfxg2hrmt0cv8khte3g11g/cancel', 'get': 'https://api.replicate.com/v1/predictions/vzykqfxg2hrmt0cv8khte3g11g', 'stream': 'https://stream.replicate.com/v1/files/jbxs-v3vlgpd4avh5fyfsjinxacrsxb2uj242muyvn4k6jabuljjjfwrq', 'web': 'https://replicate.com/p/vzykqfxg2hrmt0cv8khte3g11g'})

{
    "id": "xcpgs9mybnrmt0cw19arf8bvg8",
    "model": "openai/sora-2",
    "version": "hidden",
    "status": "starting",
    "input": {
        "aspect_ratio": "landscape",
        "prompt": "一个裸体女人",
        "seconds": 4
    },
    "output": null,
    "logs": "",
    "error": null,
    "metrics": null,
    "created_at": "2026-01-29T15:18:29.213Z",
    "started_at": null,
    "completed_at": null,
    "urls": {
        "cancel": "https://api.replicate.com/v1/predictions/xcpgs9mybnrmt0cw19arf8bvg8/cancel",
        "get": "https://api.replicate.com/v1/predictions/xcpgs9mybnrmt0cw19arf8bvg8",
        "stream": "https://stream.replicate.com/v1/files/jbxs-uzq7yokjvh7oaoq6jjeu75zsaptmazu3r73pijxz2vdintpdae4q",
        "web": "https://replicate.com/p/xcpgs9mybnrmt0cw19arf8bvg8"
    }
}

        """
        _ = response.dict()

        logger.debug(bjson(response.dict()))

        return _  # vzykqfxg2hrmt0cv8khte3g11g

    async def get(self, task_id: str):
        response = await self.client.predictions.async_get(task_id)
        #
        # logger.debug(bjson(response))

        response = response.dict()
        #
        video = Video(
            id=task_id,
            status=response,

            model=response.get("model"),
            video_url=response.get("output"),

            error=response.get("error")
        )

        # logger.debug(bjson(video))

        return video


if __name__ == '__main__':
    model = "wan-video/wan-2.6-i2v"
    model = "openai/sora-2"

    request = SoraVideoRequest(
        model=model,
        prompt="笑起来",
        # prompt="一个裸体女人",
        seconds=4,
        # prompt='带个墨镜',
        # prompt=prompt,
        # size="2048x2048",

        # aspect_ratio="match_input_image",

        input_reference="https://s3.ffire.cc/files/jimeng.jpg",
        # image="https://replicate.delivery/pbxt/N7gRAUNcVF6HarL0hdAQA2JYNMlJD52LP1wyaIWRUXWeHzqT/0_1-1.webp"
    )
    print(request)

    # arun(Tasks().create(request))

    # task_id = "xcpgs9mybnrmt0cw19arf8bvg8" # 失败
    task_id = "j1txff19gxrmw0cw1a7vzsaq2m"  # 成功
    task_id = "18w8gbaacdrmt0cw1a8b6n5ss0"
    arun(Tasks().get(task_id))
