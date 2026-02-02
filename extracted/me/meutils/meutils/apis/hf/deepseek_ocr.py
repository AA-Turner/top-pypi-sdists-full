#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : deepseek_ocr
# @Time         : 2025/10/21 15:54
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.apis.hf.gradio import create_client, handle_file

from gradio_client import Client, handle_file

# client = create_client("khang119966/DeepSeek-OCR-DEMO")

with timer('xx'):
    client = Client("axiilay/DeepSeek-OCR-Demo")
# result = client.predict(
#     image=handle_file('https://s3.ffire.cc/files/pdf_to_markdown.jpg'),
#     model_size="Gundam (Recommended)",
#     task_type="📄 Convert to Markdown",
#     ref_text="Hello!!",
#     api_name="/process_ocr_task"
# )
# print(result)
# client = Client("khang119966/DeepSeek-OCR-DEMO")
# # client = Client("axiilay/DeepSeek-OCR-Demo")
# result = client.predict(
#     image=handle_file('https://s3.ffire.cc/files/pdf_to_markdown.jpg'),
#     model_size="Gundam (Recommended)",
#     task_type="📄 Convert to Markdown",
#     ref_text="Hello!!",
#     api_name="/process_ocr_task",
#
# )
# print(result)


# client.view_api(all_endpoints=True)
