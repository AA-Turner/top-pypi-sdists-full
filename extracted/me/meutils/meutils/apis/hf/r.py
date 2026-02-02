#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : r
# @Time         : 2024/9/2 14:39
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://swanhub.co/cunyue/person-modnet/demo
from meutils.pipe import *
from meutils.request_utils import create_request

from meutils.io.image import image_to_base64

from gradio_client import Client, handle_file

client = Client("gokaygokay/KolorsPlusPlus")
result = client.predict(
    image=None,
    text_prompt="一条狗",
    vlm_model_choice="Florence-2",
    use_enhancer=False,
    model_choice="Long",
    negative_prompt="",
    seed=0,
    randomize_seed=True,
    width=1024,
    height=1024,
    guidance_scale=5,
    num_inference_steps=20,
    num_images_per_prompt=1,
    api_name="/process_workflow"
)
print(result)

#
# from gradio_client import Client, handle_file
#
# client = Client("Kwai-Kolors/Kolors")
# result = client.predict(
#     prompt="画条狗",
#     ip_adapter_image=None,
#     ip_adapter_scale=0.5,
#     negative_prompt="",
#     seed=0,
#     randomize_seed=True,
#     width=1024,
#     height=1024,
#     guidance_scale=5,
#     num_inference_steps=25,
#     api_name="/infer"
# )
# print(result)
