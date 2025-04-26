#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : videos
# @Time         : 2024/9/24 10:14
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 


from meutils.pipe import *
from meutils.io.files_utils import to_bytes
from meutils.apis.kuaishou import klingai, klingai_video
from meutils.apis.kling.images import get_task

from meutils.schemas.kling_types import STATUSES, send_message
from meutils.schemas.kling_types import VideoRequest, Task, TaskResponse
from meutils.schemas.kuaishou_types import KlingaiVideoRequest, Camera


async def create_task(request: VideoRequest, vip: bool = False):
    url = tail_image_url = None

    if request.image:
        file = await to_bytes(request.image)
        file_task = await klingai.upload(file)
        url = file_task.url

    if request.image_tail:
        file = await to_bytes(request.image)
        file_task = await klingai.upload(file)
        tail_image_url = file_task.url

    camera_control = Camera(type=request.camera_control.type, **request.camera_control.config.model_dump())

    request = KlingaiVideoRequest(
        url=url,
        tail_image_url=tail_image_url,
        camera=camera_control,
        **request.model_dump(exclude_none=True)
    )

    logger.debug(request.model_dump_json(exclude_none=True, indent=4))

    task_response = await klingai_video.create_task_plus(request, vip=vip)
    return task_response


if __name__ == '__main__':
    # 文生图
    request = VideoRequest(
        model="kling-v1",
        prompt="多肉植物，带着水珠，潮玩盲盒风格，皮克斯，3D质感，温馨的环境，丰富的场景，最佳画质，超精细，Octane渲染",
    )
    # task = arun(create_task(request, vip=True))

    image = "https://oss.ffire.cc/files/old.jpg"
    request = VideoRequest(
        prompt="互相拥抱",
        image=image
    )
    task = arun(create_task(request, vip=True))

    print(task.model_dump_json(exclude_none=True, indent=4))

    arun(get_task(task.data.task_id, task.system_fingerprint))
