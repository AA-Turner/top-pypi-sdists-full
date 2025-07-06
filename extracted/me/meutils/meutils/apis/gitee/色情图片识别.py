#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : x
# @Time         : 2024/9/25 10:42
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://ai.gitee.com/hf-models/giacomoarienti/nsfw-classifier/api

from meutils.pipe import *
from meutils.hash_utils import md5

# md5("8daf5c4765c493e2")
from openai import OpenAI

client = OpenAI(
	base_url="https://ai.gitee.com/v1",
	api_key="WPCSA3ZYD8KBQQ2ZKTAPVUA059J2Q47TLWGB2ZMQ",
	default_headers={"X-Package":"1910"},
)

response = client.moderations.create(
	model="nsfw-classifier",
	input=[
		{
			"type": "image_url",
			"image_url": {
				"url": "https://oss.ffire.cc/files/kling_watermark.png"
			}
		}
	],
)