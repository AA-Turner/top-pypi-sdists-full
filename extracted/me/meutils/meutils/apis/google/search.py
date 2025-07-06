#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : search
# @Time         : 2025/4/2 11:19
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from google import genai
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch, HttpOptions, ToolCodeExecution, Retrieval

client = genai.Client(
    api_key="AIzaSyD19pv1qsYjx4ZKbfH6qvNdYzHMV2TxmPU",
    http_options=HttpOptions(
        base_url="https://all.chatfire.cc/genai"
    )
)

google_search_tool = Tool(
    google_search=GoogleSearch(),
)

# google_search_tool = {'function_declarations': None, 'retrieval': None, 'google_search': {}, 'google_search_retrieval': None, 'code_execution': None}
print(google_search_tool.model_dump())
model_id = "gemini-2.0-flash"

response = client.models.generate_content(
    model=model_id,
    contents="亚洲多国回应“特朗普关税暂停”",
    config=GenerateContentConfig(
        tools=[google_search_tool],
        system_instruction="用中文回答",
        # response_modalities=["TEXT"],
    )
)

for each in response.candidates[0].content.parts:
    print(each.text)
# Example response:
# The next total solar eclipse visible in the contiguous United States will be on ...

# To get grounding metadata as web content.
print(response.candidates[0].grounding_metadata.search_entry_point.rendered_content)
print(response.candidates[0].grounding_metadata.grounding_chunks)
# response.candidates[0].grounding_metadata.grounding_chunks[0].web
