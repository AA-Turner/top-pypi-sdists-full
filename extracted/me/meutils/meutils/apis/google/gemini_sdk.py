#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : st
# @Time         : 2025/4/3 15:24
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.async_utils import async_to_sync

from meutils.io.files_utils import to_url, to_bytes
from meutils.schemas.openai_types import CompletionRequest

from google import genai
from google.genai.types import HttpOptions, GenerateContentConfig, Content, HarmCategory, HarmBlockThreshold, Part, \
    ThinkingConfig
from google.genai.chats import _is_part_type

config = GenerateContentConfig(

    temperature=0.7,
    top_p=0.8,
    response_modalities=['Text', 'Image'],
)

# self._http_options.base_url = 'https://generativelanguage.googleapis.com/'
# self._http_options.api_version = 'v1beta'
client = genai.Client(
    api_key="AIzaSyCa8PYURpxFKz7yOtQB_O_wRfrX0gYh9L4",
    http_options=HttpOptions(
        base_url="https://all.chatfire.cc/genai"
    )
)

if __name__ == '__main__':
    model = "gemini-2.0-flash-exp-image-generation"
    model = "gemini-2.5-flash-preview-04-17"

    request = CompletionRequest(
        model=model,
        messages=[
            {
                "role": "user", "content": [
                {
                    "type": "text",
                    "text": "一句话总结"
                },
                {
                    "type": "image_url",
                    "image_url": {

                        "url": "https://oss.ffire.cc/files/kling_watermark.png"

                    }
                }
            ]
            }],

    )

    response = client.aio.chats.create(
        model=model,
        config=GenerateContentConfig(
            system_instruction=None,
            max_output_tokens=None,
            # response_modalities=['Text', 'Image'],

            thinking_config=ThinkingConfig(include_thoughts=True, thinking_budget=24576),
        ),

        # history=[
        #
        #     Content(
        #         role="user",
        #         parts=[
        #             Part.from_text(
        #                 text="画条狗"
        #             )
        #         ]
        #     ),
        #     Content(
        #         role="model",
        #         parts=[
        #             Part.from_text(
        #                 text="Ok"
        #             ),
        #
        #             Part.from_bytes(
        #                 data=async_to_sync(to_bytes)("https://oss.ffire.cc/files/kling_watermark.png"),
        #                 mime_type="image/png"
        #             ),
        #         ]
        #     )
        #
        # ]
    )

    # "mime_type": "image/png"

    p = Part.from_uri(file_uri="https://oss.ffire.cc/files/kling_watermark.png", mime_type="image/png")
    pp = Part.from_bytes(
        data=async_to_sync(to_bytes)("https://oss.ffire.cc/files/kling_watermark.png"),
        mime_type="image/png"
    )


    # pt = Part.from_text(text="文本")

    # {'video_metadata': None,
    #  'thought': None,
    #  'code_execution_result': None,
    #  'executable_code': None,
    #  'file_data': {'file_uri': 'https://oss.ffire.cc/files/kling_watermark.png',
    #                'mime_type': 'image/png'},
    #  'function_call': None,
    #  'function_response': None,
    #  'inline_data': None,
    #  'text': None}

    #
    async def main():
        message = [
            Part.from_text(text="1+1"),
            # pp
        ]

        print(_is_part_type(message))
        chunks = await response.send_message_stream(message)

        async for chunk in chunks:
            logger.debug(chunk)
            if chunk.candidates:
                parts = chunk.candidates[0].content.parts
                for part in parts or []:
                    if len(str(part)) < 500:
                        logger.debug(part)
                    if part.inline_data:
                        image_url = await to_url(part.inline_data.data, mime_type=part.inline_data.mime_type)
                        logger.info(image_url)

                    if part.text:
                        logger.info(part.text)
            # print(i.model_dump_json(indent=4, exclude_none=True))  # inline_data


    # response = client.models.generate_content(
    #     model="gemini-2.0-flash-exp-image-generation",
    #     contents=['画条狗'],
    #
    #     # model="gemini-2.5-pro-exp-03-25",
    #     # model="gemini-2.0-flash",
    #
    #     # contents=[
    #     #     Part.from_uri(file_uri='https://generativelanguage.googleapis.com/v1beta/files/test', mime_type='image/png'),
    #     #
    #     #           "一句话总结"],
    #     config=config
    # )
    #
    # # client.aio.
    # # client.aio.chats.create()
    #
    # if __name__ == '__main__':
    #     arun(file_object)

    arun(main())

# ValueError: Message must be a valid part type: typing.Union[google.genai.types.File, google.genai.types.Part, PIL.Image.Image, str] or typing.Union[google.genai.types.File, google.genai.types.Part, PIL.Image.Image, str, google.genai.types.PartDict], got <class 'list'>

"""
curl "https://all.chatfire.cc/genai/v1beta/models/gemini-2.5-flash-preview-04-17:generateContent?key=AIzaSyCa8PYURpxFKz7yOtQB_O_wRfrX0gYh9L4" \
-H 'Content-Type: application/json' \
-X POST \
-d '{
  "contents": [
    {
      "parts": [
        {
          "text": "9.8 9.11 哪个大"
        }
      ]
    }
  ],
  "generationConfig": {
    "thinkingConfig": {
        "includeThoughts": true,
          "thinkingBudget": 1024
    }
  }
}'
"""
