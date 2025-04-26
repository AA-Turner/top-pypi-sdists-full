#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : x
# @Time         : 2024/11/25 12:23
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from gradio_client import Client, handle_file

client = Client("https://s5k.cn/api/v1/studio/Kwai-Kolors/Kolors-Virtual-Try-On/gradio/",
                # hf_token="9f8db42c-1a54-4e72-9640-46f12754853f"
                hf_token="8ee3c18e-9804-413f-b960-45d23f409281"

                )
result = client.predict(
		person_img=handle_file('https://raw.githubusercontent.com/gradio-app/gradio/main/test/test_files/bus.png'),
		garment_img=handle_file('https://raw.githubusercontent.com/gradio-app/gradio/main/test/test_files/bus.png'),
		seed=0,
		randomize_seed=True,
		api_name="/tryon"
)
print(result)