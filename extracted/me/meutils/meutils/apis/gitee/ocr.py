#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : ocr
# @Time         : 2025/10/22 20:57
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 


"""
curl https://ai.gitee.com/v1/async/images/ocr \
	-X POST \
	-H "Authorization: Bearer XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" \
	-F "image=@path/to/image.webp" \
	-F "model=DeepSeek-OCR" \
	-F "prompt=<image>\n<|grounding|>Convert the document to markdown." \
	-F "model_size=Gundam"
"""

from meutils.pipe import *
from meutils.llm.clients import AsyncClient
from meutils.schemas.openai_types import CompletionRequest
from meutils.io.files_utils import to_file, to_bytes

from meutils.db.redis_db import redis_aclient
from meutils.caches import rcache

from meutils.apis.utils import make_request_httpx

BASE_URL = "https://ai.gitee.com/v1"


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
        if output := response.get("output"):
            return output


@rcache(ttl=3600)
async def create_task(image, data: Optional[dict] = None, api_key: Optional[str] = None):
    image = await to_bytes(image)

    headers = {
        "Authorization": f"Bearer {api_key}",
    }

    # (filename, file_bytes, mime_type) = image

    response = await make_request_httpx(
        base_url=BASE_URL,
        path="/async/images/ocr",
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
    if hasattr(response, "get") and (task_id := response.get("task_id")):
        await redis_aclient.set(task_id, api_key, ex=24 * 3600)
        return task_id


# {'task_id': 'DBMIQSBXWKNCKNJLDPHEYRML4QNBRXIA'}
class Completions(object):

    def __init__(
            self,
            base_url: Optional[str] = None,
            api_key: Optional[str] = None,
    ):
        self.api_key = api_key

    async def create(self, request: CompletionRequest):
        prompt = """
        <image>\n<|grounding|>Convert the document to markdown.
        <image>\nParse the figure.
        <image>\nLocate <|ref|> the teacher<|/ref|> in the image.
        <image>\nFree OCR.
        """
        system_instruction = None
        if request.system_instruction and request.system_instruction in prompt:
            system_instruction = request.system_instruction

        if not (image_urls := request.last_urls.get("image_url")):
            yield "# Image is required"
            return
        image = image_urls[0]

        data = {
            "model": request.model,  # "DeepSeek-OCR"
            "prompt": system_instruction or "<image>\nFree OCR.",
            "model_size": "Gundam" if not hasattr(request, "model_size") else request.model_size,
        }
        if task_id := await create_task(image=image, data=data, api_key=self.api_key):
            if request.stream:
                yield f"`Task ID: {task_id}`\n\n"

            for i in range(30):
                await asyncio.sleep(3)
                if output := await get_task(task_id=task_id):
                    logger.debug(output)

                    if not request.stream:
                        yield json.dumps(output)
                        return

                    text_result = output['text_result']
                    yield f"""{text_result}\n\n"""

                    if result_image := output.get('result_image'):
                        yield f"""![result_image]({result_image})"""

                    return
                else:
                    if request.stream:
                        yield "### 处理中\n"


if __name__ == '__main__':
    """
    <image>\n<|grounding|>Convert the document to markdown.
    <image>\nParse the figure.
    <image>\nLocate <|ref|> the teacher<|/ref|> in the image.
    <image>\nFree OCR.
    """
    api_key = "NWVXUPI38OQVXZGOEL3D23I9YUQWZPV23GVVBW1X"
    data = {
        "model": "DeepSeek-OCR",
        "prompt": "<image>\n<|grounding|>Convert the document to markdown.",
        "model_size": "Gundam",
    }

    image = "https://s3.ffire.cc/files/pdf_to_markdown.jpg"

    # arun(create_task(image=image, data=data, api_key=api_key))

    arun(get_task(task_id='BX4LLL1CJW0CASHKDFDDYBAVNSLI0TQK'))
