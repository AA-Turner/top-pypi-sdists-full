#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : images
# @Time         : 2024/11/13 16:08
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://replicate.com/docs/reference/http#predictions.create

from meutils.pipe import *
from meutils.schemas.image_types import ImageRequest
from meutils.schemas.replicate_types import ReplicateRequest

from meutils.llm.openai_utils import to_openai_images_params, to_openai_params
from meutils.io.files_utils import to_bytes


from openai import AsyncClient, Client


# /v1/predictions

# /images/generations

class ReplicateRequest(BaseModel):
    ref: str
    input: Optional[Dict[str, Any]] = None  # {"prompt": "A majestic lion", "num_outputs": 2}


async def generate(request: ReplicateRequest):
    """
    import replicate
    output = replicate.run(
        "black-forest-labs/flux-schnell",
        input={"prompt": "an iguana on the beach, pointillism"}
    )

    # Save the generated image
    with open('output.png', 'wb') as f:
        f.write(output[0].read())

    print(f"Image saved as output.png")
    """

    prompt = request.input.get('prompt')
    n = request.input.get('num_outputs')

    request = ImageRequest(
        model=request.ref,
        prompt=prompt,
        n=n,
        response_format='url'
    )

    params = to_openai_params(request)

    response = await AsyncClient().images.generate(**params)

    data = await to_bytes(response.data[0].url)

    return data



import replicate
output = replicate.run(
    "black-forest-labs/flux-schnell",
    input={"prompt": "an iguana on the beach, pointillism"}
)

# Save the generated image
with open('output.png', 'wb') as f:
    f.write(output[0].read())

print(f"Image saved as output.png")


replicate.predictions.create()