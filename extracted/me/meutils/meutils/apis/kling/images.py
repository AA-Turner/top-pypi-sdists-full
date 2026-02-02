#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : images
# @Time         : 2024/9/24 10:14
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.io.files_utils import to_bytes

from meutils.apis.kuaishou import klingai

from meutils.schemas.kling_types import STATUSES, send_message
from meutils.schemas.kling_types import ImageRequest, Task, TaskResponse
from meutils.schemas.kuaishou_types import BASE_URL, KlingaiImageRequest
from meutils.schemas.image_types import KlingImageRequest


async def create_task(request: ImageRequest, vip: bool = False):
    url = None
    if request.image:
        file = await to_bytes(request.image)
        file_task = await klingai.upload(file)
        url = file_task.url
        # return url

    logger.debug(request.model_dump_json(exclude_none=True, indent=4))

    request = KlingaiImageRequest(url=url, **request.model_dump())
    task_response = await klingai.create_task_plus(request, vip=vip)

    return task_response

    # {
    #     "code": 0,
    #     "message": "string",
    #     "request_id": "string",
    #     "data": {
    #         "task_id": "string",
    #         "task_status": "string",
    #         "created_at": 0,
    #         "updated_at": 0
    #     }
    # }


async def get_task(task_id: str, token: str, oss: Optional[str] = None):
    vip = "mini" not in task_id
    task_type = "images" if 'image' in task_id else "videos"

    result = await klingai.get_task_plus(task_id, token)

    data = result['data']
    message = result['message']
    status_code = result['status']

    task = None
    try:
        works = data['works']
        urls = [work['resource']['resource'] for work in works]

        items = [
            {
                "id": f"{uuid.uuid4()}",  # work['workId'],
                "url": url,
                "duration": f"{work['resource']['duration'] / 1000:.1f}",
            } for work, url in zip(works, urls)
        ]

        task_result = {task_type: items}
        task = Task(
            task_id=str(data['task']['id']),
            task_status=STATUSES.get(data['status'], data['status']),
            task_status_msg=data['message'],
            task_result=task_result
        )

        if data['status'] not in STATUSES:
            send_message(f"未知状态：{data['status']}")
            send_message(data)

    except Exception as e:
        logger.error(e)
        send_message(f"task_id:{task_id} 失败\n{e}")
        send_message(data)

    response = TaskResponse(
        code=status_code,
        message=message,
        data=task,
    )
    return response


# {
#     "code": 0,
#     "message": "string",
#     "request_id": "string",
#     "data": {
#         "task_id": "string",
#         "task_status": "string",
#         "task_status_msg": "string",
#         "created_at": 1722769557708,
#         "updated_at": 1722769557708,
#         "task_result": {
#             "videos": [
#                 {
#                     "id": "string",
#                     "url": "string",
#                     "duration": "string"
#                 }
#             ]
#         }
#     }
# }


async def generate(request: KlingImageRequest):
    request = ImageRequest(**request.model_dump(exclude_none=True))
    task = await create_task(request, vip=True)

    for i in range(1, 15):
        await asyncio.sleep(15 / i)
        try:
            data = await get_task(task.data.task_id, task.system_fingerprint)
            images = data.data.task_result.get('images', [])
            return {"data": images}

        except Exception as e:
            logger.debug(e)
            continue


if __name__ == '__main__':
    request = ImageRequest(
        prompt="多肉植物，带着水珠，潮玩盲盒风格，皮克斯，3D质感，温馨的环境，丰富的场景，最佳画质，超精细，Octane渲染",
        aspect_ratio="1:1",
        image_fidelity=0.5,
        n=2,
        negative_prompt="",
    )


    # task = arun(create_task(request, vip=True))
    # task = arun(create_task(request, vip=False))

    # image = "https://oss.ffire.cc/files/old.jpg"
    # request = ImageRequest(
    #     prompt="互相拥抱",
    #     image=image
    # )
    # task = arun(create_task(request, vip=False))

    # print(task.model_dump_json(exclude_none=True, indent=4))


    request = KlingImageRequest(
        prompt="多肉植物，带着水珠，潮玩盲盒风格，皮克斯，3D质感，温馨的环境，丰富的场景，最佳画质，超精细，Octane渲染",
        aspect_ratio="1:1",
        image_fidelity=0.5,
        n=2,
        negative_prompt="",
    )
    arun(generate(request))

    # arun(get_task(task.data.task_id, task.system_fingerprint, oss='kling'))
    # arun(get_task(task.data.task_id, task.system_fingerprint))

    # arun(get_task("kling-image-pro-56994904", task.system_fingerprint, oss='kling'))

    # arun(get_task(task.data.task_id, task.system_fingerprint, oss='kling'))
