#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : images
# @Time         : 2024/11/13 15:44
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import os

from meutils.pipe import *

import fal_client
from fal_client import AsyncClient, SyncClient

# client = AsyncClient(key=os.getenv("FAL_KEY"))
client = SyncClient(key=os.getenv("FAL_KEY"))

application = "fal-ai/recraft-v3"




handler = client.submit(
    application=application,
    arguments={
        "prompt": "a red panda eating a bamboo in front of a poster that says \"recraft V3 now available at fal\""
    },
)

# 任务id
request_id = handler.request_id
client.get_handle(application, request_id)
client.get_handle(application, request_id).get()



from openai import AsyncClient, Client

resp = Client().images.generate(
    model="dall-e-3",
    prompt="a red panda eating a bamboo in front of a poster that says \"recraft V3 now available at fal\"",
    size="1024x1024",
    quality="standard",
    n=1,
) # {"data": [{"url": '...'}]}


# /replicate/ {

#     openai
#
# }

#
# from
#
# import replicate
#
# output = replicate.run(
#     "black-forest-labs/flux-schnell",
#     input={"prompt": "an iguana on the beach, pointillism"}
# )
#
# # Save the generated image
# with open('output.png', 'wb') as f:
#     f.write(output[0].read())
#
# print(f"Image saved as output.png")


