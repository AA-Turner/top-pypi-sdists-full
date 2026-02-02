#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : async_tasks
# @Time         : 2025/7/28 16:00
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.db.redis_db import redis_aclient
from meutils.io.files_utils import to_bytes

from meutils.apis.utils import make_request_httpx
from meutils.schemas.gitee_types import FEISHU_URL, BASE_URL
from meutils.schemas.image_types import ImageRequest, ImagesResponse

from meutils.config_utils.lark_utils import get_next_token_for_polling

"""
curl https://ai.gitee.com/v1/async/image-to-3d \
	-X POST \
	-H "Authorization: Bearer XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" \
	-F "image=@path/to/image.jpg" \
	-F "type=glb" \
	-F "model=Hi3DGen" \
	-F "seed=1234" \
	-F "file_format=glb"
	
	
texture=true 带纹理
"""


async def get_task(task_id):
    if api_key := await redis_aclient.get(task_id):
        api_key = api_key.decode()

        headers = {
            "Authorization": f"Bearer {api_key}",
        }
        response = await make_request_httpx(
            base_url=BASE_URL,
            path=f"/task/{task_id}",
            headers=headers,
        )
        """
        {'completed_at': 1753692159067,
 'created_at': 1753692151094,
 'output': {'file_url': 'https://gitee-ai.su.bcebos.com/serverless-api/2025-07-28/GB84DX8LK6NUJ0WHZLUNRCXDBFKMVVFH.glb?authorization=bce-auth-v1%2FALTAKZc1TWR1oEpkHMlwBs5YXU%2F2025-07-28T08%3A42%3A38Z%2F604800%2F%2F2799bb11463d736d0eb0fd656c944e02012f7359ca22e8397811f59d306ec353'},
 'started_at': 1753692151358,
 'status': 'success',
 'task_id': 'GB84DX8LK6NUJ0WHZLUNRCXDBFKMVVFH',
 'urls': {'cancel': 'https://ai.gitee.com/api/v1/task/GB84DX8LK6NUJ0WHZLUNRCXDBFKMVVFH/cancel',
          'get': 'https://ai.gitee.com/api/v1/task/GB84DX8LK6NUJ0WHZLUNRCXDBFKMVVFH'}}
        """
        response.pop('urls', None)
        return response


async def create_task(image, data: Optional[dict] = None, api_key: Optional[str] = None):
    api_key = api_key or await get_next_token_for_polling(FEISHU_URL)
    headers = {
        "Authorization": f"Bearer {api_key}",
    }

    # (filename, file_bytes, mime_type) = image

    response = await make_request_httpx(
        base_url=BASE_URL,
        path="/async/image-to-3d",
        headers=headers,
        files={
            "image": image,
        },
        data=data,
    )
    """
    {'created_at': 1753691466227,
 'status': 'waiting',
 'task_id': 'AXA5X0GFGXS96T4ALPYHCTCHAAYANL4U',
 'urls': {'cancel': 'https://ai.gitee.com/api/v1/task/AXA5X0GFGXS96T4ALPYHCTCHAAYANL4U/cancel',
          'get': 'https://ai.gitee.com/api/v1/task/AXA5X0GFGXS96T4ALPYHCTCHAAYANL4U'}}

{'task_id': 'GB84DX8LK6NUJ0WHZLUNRCXDBFKMVVFH'}

    """
    logger.debug(response)
    if task_id := response.get("task_id"):
        await redis_aclient.set(task_id, api_key, ex=24 * 3600)
        return {"task_id": response.get("task_id")}


async def generate(request: ImageRequest, api_key: Optional[str] = None):
    payload = request.model_dump(exclude_none=True, exclude={"extra_fields", "controls"})

    payload = {
        "type": "glb",
        "model": request.model,
        "file_format": request.response_format if request.response_format in ["glb", "stl"] else "glb",

        **payload,
        **(request.extra_fields or {})
    }

    image = await to_bytes(payload.pop('image'))

    logger.debug(payload)
    response = await create_task(image=image, data=payload, api_key=api_key)
    if response:
        for i in range(100):
            await asyncio.sleep(3)
            _ = await get_task(response['task_id'])
            logger.debug(bjson(_))
            if file_url := (_.get("output") or {}).get("file_url"):
                return ImagesResponse(data=[{"url": file_url}])


if __name__ == '__main__':
    image = "/Users/betterme/PycharmProjects/AI/test.png"
    # arun(get_task('GB84DX8LK6NUJ0WHZLUNRCXDBFKMVVFH'))
    # image = ('x.png', open(image, 'rb').read(), 'image/png')
    image = open(image, 'rb').read()
    image = "https://s3.ffire.cc/files/christmas-tree.png"

    # image = None
    arun(
        create_task(
            # image=open(image, 'rb'),
            image=image,

            data={
                "type": "glb",
                "model": "Hunyuan3D-2",
                "file_format": "glb",
            }
        ))

    # arun(generate(
    #     ImageRequest(
    #         model="Hunyuan3D-2",
    #         response_format="glb",
    #         extra_fields={
    #             "image": image,
    #
    #             "texture": True,
    #         }
    #     )
    # )
    # )


