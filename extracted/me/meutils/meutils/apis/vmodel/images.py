#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : images
# @Time         : 2025/10/21 17:22
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 


from meutils.pipe import *
from meutils.caches import rcache
from meutils.llm.clients import AsyncClient
from meutils.decorators.retry import retrying, IgnoredRetryException

from meutils.llm.openai_utils import to_openai_params
from meutils.io.files_utils import to_png, to_url_fal, to_url
from meutils.notice.feishu import send_message_for_images
from meutils.schemas.image_types import ImageRequest, ImagesResponse

base_url = "https://api.vmodel.ai"

"""

curl -X POST https://api.vmodel.ai/api/tasks/v1/create \
-H "Authorization: Bearer XeK1-4Pr11MjHlaliUN7fTsCSitgacf699wCvnBbbrgUKxX2VIcihYRVkGNx2y_mwJkfe8wlbqehsGPoXK1GvA==" \
-H "Content-Type: application/json" \
-d '{
"version": "6bb2912c9d6eb56fd49bc7a384a0cdf588258237b4f13402102b6b6ca93e587a",
"input": {
    "prompt": "Make this a 90s cartoon",
    "input_image": [
            "https://vmodel.ai/data/model/vmodel/nano-banana/nano1.png",
            "https://vmodel.ai/data/model/vmodel/nano-banana/nano2.png"
        ],
    
    "aspect_ratio": "match_input_image",
    "output_format": "jpg",
    "safety_tolerance": 2,
    "disable_safety_checker": false
}
}'


curl https://api.vmodel.ai/api/tasks/v1/get/ddnvhe2k0oxbshplob \
-H "Authorization: Bearer XeK1-4Pr11MjHlaliUN7fTsCSitgacf699wCvnBbbrgUKxX2VIcihYRVkGNx2y_mwJkfe8wlbqehsGPoXK1GvA=="




  curl -X POST https://api.vmodel.ai/api/tasks/v1/create
    -H "Authorization: Bearer $VModel_API_TOKEN"
    -H "Content-Type: application/json"
    -d '{
    "version": "6ee81ffe35d342a8fecaa47854824401caf367808090fa39eb78e781516419f2",
    "input": {
        "prompt": "Make the letters 3D, floating in space on a city street",
        "input_image": "https://vmodel.ai/data/model/vmodel/flux-kontext-max/flux-kontext-max-input.webp",
        "aspect_ratio": "match_input_image",
        "output_format": "png",
        "safety_tolerance": 6,
        "disable_safety_checker": false,
        "seed": 888,
        "prompt_upsampling": true
    }
}'
    
    

  curl -X POST https://api.vmodel.ai/api/tasks/v1/create
    -H "Authorization: Bearer $VModel_API_TOKEN"
    -H "Content-Type: application/json"
    -d '{
    "version": "44b9310748ecdccd1dfa60d68efe35b4a6291453d5edfad417075890d55a208f",
    "input": {
        "prompt": "Make the sheets in the style of the logo. Includes this logo's color. Make the scene natural.",
        "image_input": [
            "https://vmodel.ai/data/model/vmodel/nano-banana/nano1.png",
            "https://vmodel.ai/data/model/vmodel/nano-banana/nano2.png"
        ],
        "output_format": "jpg",
        "disable_safety_checker": false
    }
}'
    
    
  
  curl -X POST https://api.vmodel.ai/api/tasks/v1/create
    -H "Authorization: Bearer $VModel_API_TOKEN"
    -H "Content-Type: application/json"
    -d '{
    "version": "6ee81ffe35d342a8fecaa47854824401caf367808090fa39eb78e781516419f2",
    "input": {
        "prompt": "Make the letters 3D, floating in space on a city street",
        "input_image": "https://vmodel.ai/data/model/vmodel/flux-kontext-max/flux-kontext-max-input.webp",
        "aspect_ratio": "match_input_image",
        "output_format": "jpg",
        "safety_tolerance": 2,
        "disable_safety_checker": false
    }
}'
    
    
    
"""


async def generate(request: ImageRequest, api_key: Optional[str] = None, base_url: Optional[str] = None):
    task_id = await create_task(request, api_key)

    for i in tqdm(range(20)):
        if data := await get_task(task_id, api_key):
            return data

        await asyncio.sleep(3)


@retrying(ignored_exception_types=IgnoredRetryException)
async def get_task(task_id, api_key):
    client = AsyncClient(api_key=api_key, base_url=base_url)

    response = await client.get(f"/api/tasks/v1/get/{task_id}", cast_to=object)

    logger.debug(bjson(response))

    if error := response.get("result", {}).get("error"):
        raise IgnoredRetryException(error)

    if images := response.get("result", {}).get("output"):
        return ImagesResponse(image=images, **response.get("result"))

    """
    {
    "code": 200,
    "result": {
        "task_id": "ddnxnz9cyhyr67vpd4",
        "user_id": 10061,
        "version": "44b9310748ecdccd1dfa60d68efe35b4a6291453d5edfad417075890d55a208f",
        "error": "The input or output was flagged as sensitive. Please try again with different inputs. (E005) (uIJ6l3ruRD)", #####
        "total_time": 5.0,
        "predict_time": null,
        "logs": null,
        "output": [],
        "status": "failed",
        "create_at": null,
        "completed_at": null
    },
    "message": {}
}



    """


@rcache(ttl=3600)
async def create_task(request: ImageRequest, api_key: Optional[str] = None):
    payload = {
        "version": request.model,
        "input": {
            "prompt": request.prompt,
            "aspect_ratio": request.aspect_ratio or "match_input_image",

            "output_format": "png",
            "safety_tolerance": 6,
            "disable_safety_checker": True,
            "seed": request.seed,
            "prompt_upsampling": True
        }
    }

    if request.image_urls and request.model in {
        "6bb2912c9d6eb56fd49bc7a384a0cdf588258237b4f13402102b6b6ca93e587a",
        "6ee81ffe35d342a8fecaa47854824401caf367808090fa39eb78e781516419f2"
    }:
        payload["input"]["input_image"] = request.image_urls[0]


    else:
        payload["input"]["image_input"] = request.image_urls

    client = AsyncClient(api_key=api_key, base_url=base_url)

    response = await client.post(
        "/api/tasks/v1/create",
        body=payload,
        cast_to=object
    )

    logger.debug(bjson(response))

    if "Payment Required" in str(response):
        raise IgnoredRetryException("insufficient")

    if task_id := response.get("result", {}).get("task_id"):
        """
        {'code': 200,
 'message': {'en': 'Task created successfully'},
 'result': {'task_cost': 4000, 'task_id': 'ddnx54u1uqwetge0zy'}}
        
        """
        return task_id

    raise Exception(f"Create Task Failed: {response}")


if __name__ == '__main__':
    api_key = "cmJVYe4mNVLD3QJUTJ-mLq1rm52qgoOw_P_iB96Rjh6_uBFqjUD1RCVIKEgdMoQ_6gFnz66HS-uIa7lVZKA2MQ=="
    model = "44b9310748ecdccd1dfa60d68efe35b4a6291453d5edfad417075890d55a208f"
    model = "e2b7b93da2dcc13bb51c48fb8372667ad4c1cb18a7bca18f5b5d06a27d2863bb"

    request = ImageRequest(
        model=model,
        # prompt="Make the sheets in the style of the logo. Includes this logo's color. Make the scene natural.",
        # prompt="一个裸体女人",
        prompt='a cat',

        image_urls=[
            "https://vmodel.ai/data/model/vmodel/nano-banana/nano1.png",
            "https://vmodel.ai/data/model/vmodel/nano-banana/nano2.png"
        ],
        # aspect_ratio="match_input_image",
        seed=888,
    )

    # arun(create_task(request, api_key=api_key))
    # arun(get_task("ddnxnz9cyhyr67vpd4"))

    arun(generate(request, api_key=api_key))
