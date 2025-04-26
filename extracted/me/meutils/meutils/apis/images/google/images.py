#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : images
# @Time         : 2025/4/1 14:11
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import os

from meutils.pipe import *
import base64
from openai import OpenAI
from PIL import Image
from io import BytesIO

client = OpenAI(
    api_key=os.getenv("GOOGLE_API_KEY"),
    base_url=os.getenv("GOOGLE_BASE_URL"),
)

response = client.images.generate(
    model="imagen-3.0-generate-002",
    prompt="a portrait of a sheepadoodle wearing a cape",
    response_format='b64_json',
    n=1,
)
#
# for image_data in response.data:
#     image = Image.open(BytesIO(base64.b64decode(image_data.b64_json)))
#     image.show()
