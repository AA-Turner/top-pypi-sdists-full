#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : audios
# @Time         : 2025/4/2 11:00
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://platform.openai.com/docs/guides/audio?example=audio-in

from meutils.pipe import *
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : openai_siliconflow
# @Time         : 2024/6/26 10:42
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import os

from meutils.pipe import *
from openai import OpenAI
from openai import OpenAI, APIStatusError
from meutils.schemas.openai_types import ChatCompletionRequest
from meutils.llm.openai_utils import to_openai_completion_params
from meutils.io.files_utils import to_base64

# base64_audio = arun(to_base64("https://oss.ffire.cc/files/lipsync.mp3"))



client = OpenAI(
    # api_key=os.getenv("GOOGLE_API_KEY"),
    api_key="AIzaSyAQAt73dfL5-v3zaAHtXajZalZxfiumMOU",
    base_url=os.getenv("GOOGLE_BASE_URL"),
)

# print(client.models.list().model_dump_json(indent=4))

print(client.files.list())

# {
#     "gemini-2.0-pro-exp": "models/gemini-2.0-pro-exp",
#     "gemini-2.0-pro-exp-02-05": "models/gemini-2.0-pro-exp-02-05",
#     "gemini-2.5-pro-exp-03-25": "models/gemini-2.5-pro-exp-03-25",
#     "gemini-2.0-flash-thinking-exp": "models/gemini-2.0-flash-thinking-exp",
#     "gemini-2.0-flash": "models/gemini-2.0-flash"
#
# }


if __name__ == '__main__':
    # messages = [
    #
    #             {
    #                 "role": "user", "content": [
    #                 {
    #                     "type": "text",
    #                     "text": "一句话总结"
    #                 },
    #                 {
    #                     "type": "image_url",
    #                     "image_url": {
    #                         "url": "https://oss.ffire.cc/files/kling_watermark.png"
    #                     }
    #                 }
    #             ]
    #             }
    #
    #         ]
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "一句话总结",
                },
                {
                    "type": "input_audio",
                    "input_audio": {
                        "data": base64_audio,
                        "format": "wav"
                    }
                }
            ],
        }
    ]



    try:
        completion = client.chat.completions.create(
            # model="models/gemini-2.5-pro-exp-03-25",
            model="models/gemini-2.0-flash",
            # model="models/gemini-2.0-flash-exp-image-generation",
            messages=messages,
            # top_p=0.7,
            top_p=None,
            temperature=None,
            # stream=True,
            stream=False,

            max_tokens=None,
        )
    except APIStatusError as e:
        print(e.status_code)

        print(e.response)
        print(e.message)
        print(e.code)
    print(completion)
    for chunk in completion:  # 剔除extra body
        print(chunk)
        if chunk.choices:
            print(chunk.choices[0].delta.content)