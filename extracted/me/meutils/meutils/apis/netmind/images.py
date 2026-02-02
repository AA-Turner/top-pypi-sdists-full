#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : images
# @Time         : 2025/12/11 11:03
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.llm.clients import AsyncClient
from meutils.notice.feishu import send_message_for_images
from meutils.io.files_utils import to_url, to_url_fal
from meutils.schemas.image_types import ImageRequest, ImagesResponse

"""

# Set your API key
export API_KEY="<YOUR API Key>"
curl -X POST 'https://api.netmind.ai/v1/generation' \
--header 'Authorization: Bearer ${API_KEY}' \
--header 'Content-Type: application/json' \
--data-raw '{
    "model": "google/nano-banana-pro",
    "config": {
        "prompt": "Use the nano-banana-pro model to create a 1/7 scale commercialized figure of thecharacter in the illustration, in a realistic style and environment. Place the figure on a computer desk, using a circular transparent acrylic base without any text.On the computer screen, display the ZBrush modeling process of the figure. Next to the computer screen, place a BANDAI-style toy packaging box printed with the original artwork.",
        "image_urls": [
            "https://netmind-public-test.s3.us-west-2.amazonaws.com/inference-example-data/fire-dragon.png"
        ],
        "aspect_ratio": "auto",
        "output_format": "png",
        "resolution": "1K" 
    }
}'

{
    "model": "google/nano-banana-pro",
    "config": {
        "prompt": "Use the nano-banana-pro model to create a 1/7 scale commercialized figure of thecharacter in the illustration, in a realistic style and environment. Place the figure on a computer desk, using a circular transparent acrylic base without any text.On the computer screen, display the ZBrush modeling process of the figure. Next to the computer screen, place a BANDAI-style toy packaging box printed with the original artwork.",
        "image_urls": [
            "https://netmind-public-test.s3.us-west-2.amazonaws.com/inference-example-data/fire-dragon.png"
        ],
        "aspect_ratio": "auto",
        "output_format": "png",
        "resolution": "1K",
        "sync_mode": True
    }
}

{'created_at': '2025-12-11 03:11:34',
 'deleted_at': None,
 'id': '943c987abe8d4abdb1e4fdc57a9c4d74',
 'is_deleted': False,
 'logs': [],
 'pending_duration': 34,
 'processing_duration': 0,
 'result': {'data': [{'file_id': 'file-5y5iowc8i6skbfhw',
                      'file_name': 'output_image.png',
                      'file_type': 'image',
                      'url': 'https://files.netmind.ai/ea64296aab884d5bb9896f750ba5e743/inference/file-5y5iowc8i6skbfhw/output_image.png'}]},
 'status': 'completed',
 'updated_at': '2025-12-11 03:12:08',
 'user_id': 'ea64296aab884d5bb9896f750ba5e743'}
 
 
 {'created_at': '2025-12-11 03:18:17',
 'deleted_at': None,
 'id': 'b9fd82de98704e05878b8d59963bc8f4',
 'is_deleted': False,
 'logs': [],
 'result': {},
 'status': 'pending',
 'updated_at': '2025-12-11 03:18:17',
 'user_id': 'ea64296aab884d5bb9896f750ba5e743'}
"""

BASE_URL = "https://api.netmind.ai/v1"


async def generate(request: ImageRequest, api_key: Optional[str] = None):
    client = AsyncClient(base_url=BASE_URL, api_key=api_key)

    payload = {
        "model": request.model,
        "config": {
            "prompt": request.prompt,
            "image_urls": request.image_urls,
            "aspect_ratio": request.aspect_ratio or "auto",
            "output_format": "png",
            "resolution": request.resolution or "2K",  # 0.12 0.2 0.039

            "num_images": request.n or 1,
            # "sync_mode": True,
        }
    }
    if request.model in {"google/nano-banana-pro"}:
        payload["config"]["sync_mode"] = True
        # payload["config"]["resolution"] = request.resolution or "2K"  # 0.12 0.2 0.039
        # payload["config"]["aspect_ratio"] = request.aspect_ratio or "auto"


    # task_id = "df98adfb253341d693f9415bfa00632e"
    # if request.stream:
    #     # "https://api.netmind.ai/v1/generation/{{GENERATION_ID}}"
    #     pass

    response = await client.post(
        "/generation",
        body=payload,
        cast_to=object
    )

    logger.debug(bjson([payload, response]))

    if data := (response.get("result") or {}).get('data', []):
        response = ImagesResponse(data=data)
    # elif task_id := response.get("id"):
    #     for i in range(10):
    #         response = await client.get(f"/generation/{task_id}", cast_to=object)
    #         logger.debug(bjson(response))
    #         if response.get("status") == "completed":
    #             break
    #         await asyncio.sleep(5)
    #     else:
    #         raise TimeoutError(f"任务 {task_id} 超时")
    #     """
    #    "text": "Something error: 422: {\"detail\":[{\"type\":\"literal_error\",\"loc\":[\"body\",\"aspect_ratio\"],\"msg\":\"Input should be '21:9', '16:9', '3:2', '4:3', '5:4', '1:1', '4:5', '3:4', '2:3' or '9:16'\",\"input\":\"auto\",\"ctx\":{\"expected\":\"'21:9', '16:9', '3:2', '4:3', '5:4', '1:1', '4:5', '3:4', '2:3' or '9:16'\"}}]}",
    #
    #     """

    return response


if __name__ == '__main__':
    model = "google/nano-banana"
    # model = "google/nano-banana-pro"

    request = ImageRequest(
        model=model,
        prompt="一个裸体美女",
        # image=["https://netmind-public-test.s3.us-west-2.amazonaws.com/inference-example-data/fire-dragon.png"],

        # image_urls=["https://netmind-public-test.s3.us-west-2.amazonaws.com/inference-example-data/fire-dragon.png"],
        aspect_ratio="auto",
        # resolution="1K",
        n=1,
    )

    arun(generate(request, "b085e2e0b7c149f381f872b8d293f29b"))
