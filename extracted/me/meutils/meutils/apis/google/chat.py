#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : common
# @Time         : 2025/4/2 13:03
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://ai.google.dev/gemini-api/docs/openai?hl=zh-cn
# genai => openai
# https://googleapis.github.io/python-genai/genai.html#module-genai.models


from meutils.pipe import *
from meutils.decorators.retry import retrying

from meutils.io.files_utils import to_url, to_bytes, guess_mime_type
from meutils.str_utils.regular_expression import parse_url

from meutils.schemas.image_types import ImageRequest, ImagesResponse
from meutils.schemas.openai_types import chat_completion, chat_completion_chunk, CompletionRequest, CompletionUsage

from meutils.config_utils.lark_utils import get_next_token_for_polling
from google import genai
from google.genai import types
from google.genai.types import Part, HttpOptions, HarmCategory, HarmBlockThreshold
from google.genai.types import UploadFileConfig, ThinkingConfig, GenerateContentConfig

from google.genai.types import UserContent, ModelContent, Content
from google.genai.types import Tool, GoogleSearch

FEISHU_URL = "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=bK9ZTt"  # 200

"""
Gemini 1.5 Pro 和 1.5 Flash 最多支持 3,600 个文档页面。文档页面必须采用以下文本数据 MIME 类型之一：

PDF - application/pdf
JavaScript - application/x-javascript、text/javascript
Python - application/x-python、text/x-python
TXT - text/plain
HTML - text/html
CSS - text/css
Markdown - text/md
CSV - text/csv
XML - text/xml
RTF - text/rtf

- 小文件
- 大文件: 需要等待处理
"""
tools = [
    Tool(
        google_search=GoogleSearch()
    )
]


# UploadFileConfig(
#     http_options=HttpOptions(
#         timeout=120,
#     )
# )

class Completions(object):
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key
        self.base_url = base_url or "https://g.chatfire.cn"
        self.client = None  ####

    async def create_for_search(self, request: CompletionRequest):
        self.client = self.client or await self.get_client()

        if request.model.endswith("-search"):
            request.model = request.model.replace("-search", "")

        chat = self.client.aio.chats.create(
            model=request.model,
            config=GenerateContentConfig(
                tools=tools,
                system_instruction=request.system_instruction or "请根据用户的语言偏好自动调整回复语言",
                # thinking_config=ThinkingConfig(include_thoughts=True, thinking_budget=24576)
            ),
        )
        # print(response.candidates[0].grounding_metadata.search_entry_point.rendered_content)
        # print(response.candidates[0].grounding_metadata.grounding_chunks)

        chunks = await chat.send_message_stream(request.last_user_content)
        async for chunk in chunks:
            if chunk.candidates and chunk.candidates[0].content:
                parts = chunk.candidates[0].content.parts or []
                for part in parts:
                    # logger.debug(part)
                    if part.text:
                        yield part.text

            if chunk.candidates and chunk.candidates[0].grounding_metadata:
                grounding_chunks = chunk.candidates[0].grounding_metadata.grounding_chunks or []
                for grounding_chunk in grounding_chunks:
                    if grounding_chunk.web:
                        yield f"\n\n[{grounding_chunk.web.title}]({grounding_chunk.web.uri})"

    async def create_for_files(self, request: CompletionRequest):
        """todo: 大文件解析"""
        self.client = self.client or await self.get_client()

        contents = []
        if urls := sum(request.last_urls.values(), []):
            logger.debug(urls)
            # https://ai.google.dev/gemini-api/docs/document-processing?hl=zh-cn&lang=python
            file_objects = await self.upload(urls)
            for file_object in file_objects:
                self.check_file(file_object)

            contents += file_objects
            contents.append(request.last_user_content)

        elif request.last_user_content.startswith("http"):
            url, user_content = request.last_user_content.split(maxsplit=1)

            yield "> `⏳️Uploading`\n"
            file_object = await self.upload(url)
            yield f"```json\n{file_object.model_dump_json(indent=4)}\n```\n\n"

            s = time.time()

            yield "[Thinking]("
            for i in range(100):
                file_object = self.client.files.get(
                    name=file_object.name,
                    config={"http_options": {"timeout": 300 * 1000}}
                )

                logger.debug(file_object)

                if file_object.state.name in {"ACTIVE", }:
                    yield f"100%) ✅️✅️✅️{time.time() - s:.2f}s.\n\n"
                    break
                else:
                    yield f"{min(i * 5, 99)}%"

                await asyncio.sleep(3)

            # {'error': {'code': 400,
            #            'message': 'The File cwjpskscrjd79hjezu7dhb is not in an ACTIVE state and usage is not allowed.',
            #            'status': 'FAILED_PRECONDITION'}}
            #
            # while file_object.state.name == "ACTIVE":
            #     logger.debug(file_object)
            #     await asyncio.sleep(1)

            contents += [file_object, user_content]
        else:
            contents.append(request.last_user_content)

        logger.debug(contents)

        if any(i in request.model for i in {"gemini-2.5-pro", "gemini-2.5-flash"}):  # 默认开启思考
            request.reasoning_effort = "low"

        chat = self.client.aio.chats.create(
            model=request.model,
            config=GenerateContentConfig(
                response_modalities=['Text'],
                system_instruction=request.system_instruction or "请根据用户的语言偏好自动调整回复语言",
                thinking_config=ThinkingConfig(thinking_budget=request.reasoning_effort and 1024 or 0),
                # thinking_config=ThinkingConfig(thinking_budget=1024),
            )
        )
        for i in range(5):
            try:
                chunks = await chat.send_message_stream(contents)
                async for chunk in chunks:
                    if chunk.candidates and chunk.candidates[0].content:
                        parts = chunk.candidates[0].content.parts or []
                        for part in parts:
                            # logger.debug(part)
                            if part.text:
                                yield part.text

                break

            except Exception as e:
                logger.debug(f"重试{i}: {e}")
                if "The model is overloaded." in str(e):
                    await asyncio.sleep(1)
                    continue
                else:

                    yield e
                    raise e

    @retrying(title=__name__)
    async def generate(self, request: ImageRequest):  # OpenaiD3
        request.model = "gemini-2.0-flash-exp-image-generation"
        image, prompt = request.image_and_prompt
        parts = [Part.from_text(text=prompt)]
        if image:
            data = await to_bytes(image)
            parts.append(Part.from_bytes(data=data, mime_type="image/png"))

        self.client = self.client or await self.get_client()
        chat = self.client.aio.chats.create(
            model=request.model,
            config=GenerateContentConfig(
                response_modalities=['Text', 'Image'],
            )
        )
        image_response = ImagesResponse()

        response = await chat.send_message(parts)
        if response.candidates and response.candidates[0].content:
            parts = response.candidates[0].content.parts or []
            for part in parts:
                if part.inline_data:
                    image_url = await to_url(part.inline_data.data, mime_type=part.inline_data.mime_type)
                    image_response.data.append({"url": image_url, "revised_prompt": part.text})

        return image_response

    async def create_for_images(self, request: CompletionRequest):
        request.model = "gemini-2.0-flash-exp-image-generation"  ####### 目前是强行

        messages = await self.to_image_messages(request)

        if len(messages) > 1:
            history = messages[:-1]
            message = messages[-1].parts
        else:
            history = []
            message = messages[-1].parts

        self.client = self.client or await self.get_client()
        chat = self.client.aio.chats.create(  # todo: system_instruction
            model=request.model,
            config=GenerateContentConfig(
                response_modalities=['Text', 'Image'],
                # system_instruction=request.system_instruction
            ),
            history=history
        )

        # logger.debug(message)

        # message = [
        #     Part.from_text(text="画条狗")
        # ]

        for i in range(5):
            try:
                chunks = await chat.send_message_stream(message)
                async for chunk in chunks:

                    if chunk.candidates and chunk.candidates[0].content:
                        parts = chunk.candidates[0].content.parts or []
                        for part in parts:
                            # logger.debug(part)
                            if part.text:
                                yield part.text

                            if part.inline_data:
                                image_url = await to_url(
                                    part.inline_data.data,
                                    mime_type=part.inline_data.mime_type
                                )
                                yield f"![image_url]({image_url})"
                break

            except Exception as e:
                logger.debug(f"重试{i}: {e}")
                if "The model is overloaded." in str(e):
                    await asyncio.sleep(1)
                    continue
                else:
                    yield e
                    raise e

    async def to_image_messages(self, request: CompletionRequest):
        # 两轮即可连续编辑图片

        messages = []
        for m in request.messages or []:
            contents = m.get("content")
            if m.get("role") == "assistant":
                assistant_content = str(contents)
                if urls := parse_url(assistant_content):  # assistant
                    datas = await asyncio.gather(*map(to_bytes, urls))

                    parts = [
                        Part.from_bytes(
                            data=data,
                            mime_type="image/png"
                        )
                        for data in datas
                    ]
                    parts += [
                        Part.from_text(
                            text=request.last_assistant_content
                        ),
                    ]
                    messages.append(ModelContent(parts=parts))

            elif m.get("role") == "user":
                if isinstance(contents, list):
                    parts = []
                    for content in contents:
                        if content.get("type") == "image_url":
                            image_url = content.get("image_url", {}).get("url")
                            data = await to_bytes(image_url)

                            parts += [
                                Part.from_bytes(data=data, mime_type="image/png")
                            ]

                        elif content.get("type") == "text":
                            text = content.get("text")
                            if text.startswith('http'):
                                image_url, text = text.split(maxsplit=1)
                                data = await to_bytes(image_url)

                                parts += [
                                    Part.from_bytes(data=data, mime_type="image/png"),
                                    Part.from_text(text=text)
                                ]
                            else:
                                parts += [
                                    Part.from_text(text=text)
                                ]

                    messages.append(UserContent(parts=parts))

                else:  # str
                    if str(contents).startswith('http'):  # 修正提问格式， 兼容 url
                        image_url, text = str(contents).split(maxsplit=1)
                        data = await to_bytes(image_url)
                        parts = [
                            Part.from_bytes(data=data, mime_type="image/png"),
                            Part.from_text(text=text)
                        ]
                    else:
                        parts = [
                            Part.from_text(text=str(contents)),
                        ]
                    messages.append(UserContent(parts=parts))

        return messages

    @retrying(title=__name__)
    async def upload(self, files: Union[str, List[str]]):  # => openai files
        self.client = self.client or await self.get_client()

        if isinstance(files, list):
            return await asyncio.gather(*map(self.upload, files))

        file_config = {
            "name": f"{shortuuid.random().lower()}",
            "mime_type": guess_mime_type(files),
            "http_options": {"timeout": 300 * 1000}
        }

        return await self.client.aio.files.upload(file=io.BytesIO(await to_bytes(files)), config=file_config)

    async def get_client(self):
        api_key = self.api_key or await get_next_token_for_polling(feishu_url=FEISHU_URL, from_redis=True)

        logger.info(f"GeminiClient: {api_key}")

        return genai.Client(
            api_key=api_key,
            http_options=HttpOptions(
                base_url=self.base_url,
                timeout=300 * 1000,
            )
        )

    def check_file(self, file_object):

        for i in range(100):
            file_object = self.client.files.get(
                name=file_object.name,
                config={"http_options": {"timeout": 300 * 1000}}
            )

            logger.debug(file_object)
            if file_object.state.name in {"ACTIVE", }:  # FAILED_PRECONDITION
                break

            time.sleep(3)


if __name__ == '__main__':
    file = "https://oss.ffire.cc/files/kling_watermark.png"

    api_key = os.getenv("GOOGLE_API_KEY")

    # arun(GeminiClient(api_key=api_key).upload(file))
    # arun(GeminiClient(api_key=api_key).upload([file] * 2))
    # arun(GeminiClient(api_key=api_key).create())
    url = "https://oss.ffire.cc/files/nsfw.jpg"
    content = [

        # {"type": "text", "text": "https://oss.ffire.cc/files/nsfw.jpg 移除右下角的水印"},
        # {"type": "text", "text": "https://oss.ffire.cc/files/kling_watermark.png 总结下"},
        # {"type": "text", "text": "https://oss.ffire.cc/files/nsfw.jpg 总结下"},
        {"type": "text", "text": "https://lmdbk.com/5.mp4 总结下"},
        # {"type": "text", "text": "https://v3.fal.media/files/penguin/Rx-8V0MVgkVZM6PJ0RiPD_douyin.mp4 总结下"},

        # {"type": "text", "text": "总结下"},
        # {"type": "image_url", "image_url": {"url": url}},

        # {"type": "text", "text": "总结下"},
        # {"type": "video_url", "video_url": {"url": "https://lmdbk.com/5.mp4"}},
        # {"type": "video_url", "video_url": {"url": "https://lmdbk.com/5.mp4"}},

        # {"type": "video_url", "video_url": {"url": "https://v3.fal.media/files/penguin/Rx-8V0MVgkVZM6PJ0RiPD_douyin.mp4"}}

    ]

    # content = "亚洲多国回应“特朗普关税暂停”"

    # content = "https://oss.ffire.cc/files/nsfw.jpg 移除右下角的水印"

    #
    request = CompletionRequest(
        # model="qwen-turbo-2024-11-01",
        # model="gemini-all",
        # model="gemini-2.0-flash-exp-image-generation",
        model="gemini-2.0-flash",
        # model="gemini-2.5-flash-preview-04-17",
        # model="gemini-2.5-flash-preview-04-17",

        messages=[
            {
                'role': 'user',
                'content': content
            },

        ],
        stream=True,
    )

    # arun(Completions(api_key=api_key).create_for_search(request))

    # arun(Completions(api_key=api_key).create_for_images(request))
    arun(Completions().create_for_files(request))

    # arun(Completions(api_key=api_key).create_for_files(request))

    # request = ImageRequest(
    #     prompt="https://oss.ffire.cc/files/nsfw.jpg 移除右下角 白色的水印",
    #     # prompt="画条可爱的狗",
    #
    # )
    #
    # arun(Completions(api_key=api_key).generate(request))
