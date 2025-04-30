#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : openai_types
# @Time         : 2024/6/7 17:30
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://github.com/Calcium-Ion/new-api/tree/main/dto

from meutils.pipe import *

from openai.types.chat import ChatCompletion as _ChatCompletion, ChatCompletionChunk as _ChatCompletionChunk
from openai.types.chat.chat_completion import Choice as _Choice, ChatCompletionMessage as _ChatCompletionMessage, \
    CompletionUsage as _CompletionUsage
from openai.types.chat.chat_completion_chunk import Choice as _ChunkChoice, ChoiceDelta
from openai._types import FileTypes
from openai.types import ImagesResponse as _ImagesResponse
from openai.types.shared_params import FunctionDefinition
from openai.types.chat import ChatCompletionToolParam

TOOLS = [
    {"type": "web_browser"},
    {"type": "code_interpreter"},
    {"type": "drawing_tool"},
]

BACKUP_MODEL = os.getenv("BACKUP_MODEL", "glm-4")


class Tool(BaseModel):
    # {"id": "", "type": "web_browser", "function": {}} => {"type": "web_browser", "function": None}
    function: Optional[dict] = None  # FunctionDefinition
    type: str

    def __init__(self, /, **data: Any):
        super().__init__(**data)
        self.function = self.function or None


class CompletionUsage(_CompletionUsage):
    prompt_tokens: int = 1000
    completion_tokens: int = 1000
    total_tokens: int = 2000


class ChatCompletionMessage(_ChatCompletionMessage):
    role: Literal["assistant"] = "assistant"
    """The role of the author of this message."""


class Choice(_Choice):
    index: int = 0
    finish_reason: Literal["stop", "length", "tool_calls", "content_filter", "function_call"] = None


class ChatCompletion(_ChatCompletion):
    id: str = Field(default_factory=lambda: f"chatcmpl-{shortuuid.random()}")
    created: int = Field(default_factory=lambda: int(time.time()))
    model: str = ""
    object: str = "chat.completion"
    usage: CompletionUsage = CompletionUsage()


class ChunkChoice(_ChunkChoice):
    index: int = 0


class ChatCompletionChunk(_ChatCompletionChunk):
    id: str = Field(default_factory=lambda: f"chatcmpl-{shortuuid.random()}")
    created: int = Field(default_factory=lambda: int(time.time()))
    model: str = ""
    object: str = "chat.completion.chunk"


chat_completion = ChatCompletion(
    choices=[Choice(message=ChatCompletionMessage(reasoning_content="", content=""))]
)
chat_completion_chunk = ChatCompletionChunk(
    choices=[ChunkChoice(delta=ChoiceDelta(reasoning_content="", content=""))]
)
chat_completion_chunk_stop = ChatCompletionChunk(
    choices=[ChunkChoice(delta=ChoiceDelta(reasoning_content="", content=""), finish_reason="stop")]
)


# chat_completion.choices[0].message.content = "*"
# chat_completion_chunk.choices[0].delta.content = "*"

class CompletionRequest(BaseModel):
    """
    prompt_filter_result.content_filter_results
    choice.content_filter_results

    todo: ['messages', 'model', 'frequency_penalty', 'function_call', 'functions', 'logit_bias', 'logprobs', 'max_tokens', 'n', 'presence_penalty', 'response_format', 'seed', 'stop', 'stream', 'temperature', 'tool_choice', 'tools', 'top_logprobs', 'top_p', 'user']
    """
    model: str = ''  # "gpt-3.5-turbo-file-id"

    # [{'role': 'user', 'content': 'hi'}]
    # [{'role': 'user', 'content':  [{"type": "text", "text": ""}]]
    # [{'role': 'user', 'content': [{"type": "image_url", "image_url": ""}]}] # 也兼容文件
    # [{'role': 'user', 'content': [{"type": "image_url", "image_url": {"url": ""}}]}] # 也兼容文件
    # [{'role': 'user', 'content':  [{"type": "file", "file_url": ""}]]
    messages: Optional[List[Dict[str, Any]]] = None  # 标准化

    stream: Optional[bool] = False
    stream_options: Optional[dict] = None

    top_p: Optional[float] = 0.7
    temperature: Optional[float] = 0.7

    n: Optional[int] = 1
    max_tokens: Optional[int] = None
    stop: Optional[Union[str, List[str]]] = None

    frequency_penalty: Optional[float] = None
    user: Optional[str] = None

    reasoning_effort: Optional[Literal["low", "medium", "high"]] = None

    # 拓展字段

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @cached_property
    def system_instruction(self):
        # [{'role': 'system', 'content':  [{"type": "text", "text": ""}]]

        if message := self.messages and self.messages[0]:
            if message.get("role") == "system":
                return str(message.get("content", "")) or None

    @cached_property
    def last_message(self):
        return self.messages and self.messages[-1]

    @cached_property
    def last_user_content(self) -> str:
        """text"""
        for i, message in enumerate(self.messages[::-1], 1):
            if message.get("role") == "user":
                contents = message.get("content")
                if isinstance(contents, list):
                    for content in contents:
                        if content.get("type") == "text":
                            return content.get('text', "")

                else:
                    return str(contents)
        return ""

    @cached_property
    def last_assistant_content(self) -> str:
        """text"""
        for i, message in enumerate(self.messages[::-1], 1):
            if message.get("role") == "assistant":
                contents = message.get("content")
                if isinstance(contents, list):
                    for content in contents:
                        if content.get("type") == "text":
                            return content.get('text', "")
                else:
                    return str(contents)
        return ""

    @cached_property
    def last_urls(self):  # file_url 多轮对话需要  sum(request.last_urls.values(), [])
        """最新一轮的 user url 列表"""
        content_types = {
            "image_url",

            "file", "file_url",

            "audio_url", "input_audio",

            "video_url",
        }
        for i, message in enumerate(self.messages[::-1], 1):
            data = {}
            if message.get("role") == "user":  # 每一轮还要处理
                user_contents = message.get("content")
                if isinstance(user_contents, list):  # 用户 url
                    for content in user_contents:
                        content_type = content.get("type")
                        if content_type in content_types:
                            # logger.debug(content)
                            if _url := content.get(content_type, {}):  # {"type": "file", "file": fileid}
                                if isinstance(_url, str):  # 兼容了spark qwenai
                                    url = _url
                                else:
                                    url = _url.get("url") or _url.get("data")
                                url and data.setdefault(content_type, []).append(url)

            if data: return data
        return {}

    # def create_message(self, text: str, content_type: Optional[str] = None):
    #     """
    #     消息生成器
    #     :param text:
    #     :param content_type:
    #     :return:
    #     """
    #     message = {
    #         'role': 'user',
    #         'content': [
    #             {
    #                 "type": "text",
    #                 "text": text
    #             },
    #         ]
    #     }
    #
    #     return message

    class Config:
        extra = "allow"

        json_schema_extra = {
            "examples": [
                {
                    "model": "deepseek-chat",
                    "messages": [
                        {
                            "role": "user",
                            "content": "hi"
                        }
                    ],
                    "stream": True
                },
            ]
        }


class ChatCompletionRequest(BaseModel):
    """
    prompt_filter_result.content_filter_results
    choice.content_filter_results

    todo: ['messages', 'model', 'frequency_penalty', 'function_call', 'functions', 'logit_bias', 'logprobs', 'max_tokens', 'n', 'presence_penalty', 'response_format', 'seed', 'stop', 'stream', 'temperature', 'tool_choice', 'tools', 'top_logprobs', 'top_p', 'user']
    """
    model: str = ''  # "gpt-3.5-turbo-file-id"

    # [{'role': 'user', 'content': 'hi'}]
    # [{'role': 'user', 'content':  [{"type": "text", "text": ""}]]
    # [{'role': 'user', 'content': [{"type": "image_url", "image_url": ""}]}] # 也兼容文件
    # [{'role': 'user', 'content': [{"type": "image_url", "image_url": {"url": ""}}]}] # 也兼容文件
    # [{'role': 'user', 'content':  [{"type": "file", "file_url": ""}]]
    messages: Optional[List[Dict[str, Any]]] = None

    stream: Optional[bool] = False
    stream_options: Optional[dict] = None

    top_p: Optional[float] = 0.7
    temperature: Optional[float] = 0.7

    n: Optional[int] = 1
    max_tokens: Optional[int] = None
    stop: Optional[Union[str, List[str]]] = None

    presence_penalty: Optional[float] = 0.0
    frequency_penalty: Optional[float] = None
    user: Optional[str] = None

    # tools
    response_format: Optional[Any] = None
    function_call: Optional[Any] = None
    functions: Optional[Any] = None
    tools: Optional[List[Tool]] = None  # 为了兼容 oneapi
    tool_choice: Optional[Any] = None
    parallel_tool_calls: Optional[Any] = None

    # 拓展字段
    system_messages: Optional[list] = None
    last_content: Optional[Any] = None
    urls: List[str] = []

    system_fingerprint: Optional[str] = "🔥"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.messages = self.messages or [{'role': 'user', 'content': 'hi'}]
        self.system_messages = [m for m in self.messages if m.get("role") == "system"]

        # 移除 不支持的 content type: 优雅处理多轮

        last_message = self.messages[-1]
        self.last_content = last_message.get("content", "")  # 大部分时间等价于user_content
        """[{'role': 'user', 'content':  [{"type": "text", "text": ""}]]"""
        if isinstance(self.last_content, list) and self.last_content:
            # 多模态 'text','image_url','video_url' and 'video'
            urls = (
                    jsonpath.jsonpath(self.last_content, expr='$..url')
                    or jsonpath.jsonpath(self.last_content, expr='$..image_url')
                # or jsonpath.jsonpath(self.last_content, expr='$..audio_url')
                # or jsonpath.jsonpath(self.last_content, expr='$..video_url')
                # or jsonpath.jsonpath(self.last_content, expr='$..file_url')
            )
            self.urls = self.urls or urls or []

            # 取最后一个文本提示词
            texts = jsonpath.jsonpath(self.last_content, expr='$..text') or []
            self.last_content = '\n'.join(texts)

        # 兼容 glm-4
        self.top_p = self.top_p is not None and np.clip(self.top_p, 0.01, 0.99)
        self.temperature = self.temperature is not None and np.clip(self.temperature, 0.01, 0.99)

        if self.model.startswith('o1'):
            self.top_p = 1
            self.temperature = 1

        if self.max_tokens:
            self.max_tokens = min(self.max_tokens, 4096)

    class Config:
        extra = "allow"

        json_schema_extra = {
            "examples": [
                {
                    "model": "gpt-3.5-turbo",
                    "messages": [
                        {
                            "role": "user",
                            "content": "hi"
                        }
                    ],
                    "stream": False
                },

                {
                    "model": "gpt-3.5-turbo",
                    "messages": [
                        {
                            "role": "user",
                            "content": "请按照下面标题，写一篇400字的文章\n王志文说，一个不熟的人找你借饯，说明他已经把熟人借遍了。除非你不想要了，否则不要借"
                        }
                    ],
                    "stream": False
                },

                # url
                {
                    "model": "url-gpt-3.5-turbo",
                    "messages": [
                        {
                            "role": "user",
                            "content": "总结一下https://mp.weixin.qq.com/s/Otl45GViytuAYPZw3m7q9w"
                        }
                    ],
                    "stream": False
                },

                # rag
                {
                    "messages": [
                        {
                            "content": "分别总结这两篇文章",
                            "role": "user"
                        }
                    ],
                    "model": "gpt-3.5-turbo",
                    "stream": False,
                    "file_ids": ["cn2a0s83r07am0knkeag", "cn2a3ralnl9crebipv4g"]
                }

            ]
        }


class ImageRequest(BaseModel):
    prompt: str

    model: str = 'pro'
    n: int = 1
    quality: str = 'hd'
    response_format: Literal["url", "b64_json"] = "url"
    size: str = '1024x1024'  # 测试默认值
    # sd: 768x1024 1024x576
    style: Union[str, Literal["vivid", "natural"]] = "natural"

    # 拓展参数
    guidance_scale: float = Field(default=5, alias="guidance")

    # https://blog.csdn.net/qq_37508554/article/details/133975130
    num_inference_steps: int = Field(default=20, alias="steps")

    seed: Optional[int] = None
    negative_prompt: Optional[str] = None

    # 拓展字段
    nsfw_level: str = "2"  # 小于等于6
    url: Optional[str] = None
    image: Optional[str] = None  # url/base64

    prompt_enhancement: bool = False

    def __init__(self, /, **data: Any):
        super().__init__(**data)
        if self.model.lower().__contains__('stabilityai'):
            self.num_inference_steps = 25
            self.guidance_scale = 7.5
        elif any(i in self.model.lower() for i in {"turbo", "lightning"}):
            self.num_inference_steps = 4
            self.guidance_scale = 1

    class Config:
        # frozen = True
        populate_by_name = True

        json_schema_extra = {
            "examples": [
                {
                    "model": "stable-diffusion-3-medium",  # sd3
                    "prompt": "画条狗",
                },
            ]
        }


class ImagesResponse(_ImagesResponse):
    created: int = Field(default_factory=lambda: int(time.time()))


class TTSRequest(BaseModel):
    input: str
    model: Optional[Union[str, Literal["tts-1", "tts-1-hd"]]] = 'tts'
    voice: Optional[Union[str, Literal["alloy", "echo", "fable", "onyx", "nova", "shimmer"]]] = ""
    speed: Optional[float] = None

    response_format: Literal["mp3", "opus", "aac", "flac", "wav", "pcm"] = "mp3"

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "model": "tts-1",
                    "voice": "7f92f8afb8ec43bf81429cc1c9199cb1",
                    "input": "你好，我是AI助手",
                }
            ]
        }


class STTRequest(BaseModel):  # ASR
    file: Union[bytes, str]
    model: str = "whisper-1"
    prompt: Optional[str] = None
    response_format: Literal["text", "srt", "verbose_json", "vtt"] = "text"
    language: Optional[str] = None
    temperature: Optional[float] = None
    timestamp_granularities: Optional[List[Literal["word", "segment"]]] = None


if __name__ == '__main__':
    pass

    # print(ChatCompletion(choices=[Choice(message=ChatCompletionMessage(content="ChatCompletion"))]))
    # print(ChatCompletionChunk(choices=[ChunkChoice(delta=ChoiceDelta(content="ChatCompletionChunk"))]))
    #
    # print(chat_completion)
    # print(chat_completion_chunk)
    # print(chat_completion_chunk_stop)

    # print(ChatCompletionRequest(temperature=0, top_p=1))
    # print(ChatCompletionRequest(temperature=1, top_p=0))

    # file = UploadFile(open("/Users/betterme/PycharmProjects/AI/ChatLLM/chatllm/api/routers/cocopilot.py", "rb"))
    # #
    # print(AudioRequest(file=file))
    # print(ImagesResponse(data=[]))
    # print(ChatCompletionRequest(tools=[
    #     {
    #         # "id": "",
    #         "type": "web_browser",
    #         # "function": {}
    #     }
    # ],
    #     max_tokens=None,
    # ).model_dump_json(indent=4))

    # 创建实例
    # req1 = ImageRequest(guidance_scale=5.0, prompt="画条狗")
    # req2 = ImageRequest(guidance=5.0, prompt="画条狗")
    #
    # print(req1.guidance_scale)  # 输出: 5.0
    # print(req2.guidance_scale)  # 输出: 5.0
    #
    # # 两种方式都可以访问这个值
    # print(req1.model_dump())  # 输出: {'guidance_scale': 5.0}
    # print(req1.model_dump(by_alias=True))  # 输出: {'guidance': 5.0}

    # class A(BaseModel):
    #     n: int = Field(1, ge=1, le=0)
    #
    #
    # print(A(n=11))
    messages = [
        {'role': 'user',
         'content': [{"type": "image_url", "image_url": "https://oss.ffire.cc/files/kling_watermark.png"}]},
        {'role': 'assistant', 'content': [{"type": "image_url", "image_url": "这是个图片链接"}]},

        {'role': 'assistant', 'content': [{"type": "image_url", "image_url": "这是个图片链接"}]},

        {'role': 'user', 'content': [
            {"type": "image_url", "image_url": {"url": "这是个图片链接1"}},
            {"type": "file_url", "file_url": {"url": "这是个file_url"}},
            {"type": "file_url", "file_url": {"url": "这是个file_url"}},
            {"type": "file", "file": "这是个fileid"},

            {"type": "audio_url", "audio_url": {"url": "这是个file_url"}},
            {"type": "video_url", "video_url": {"url": "这是个video_url"}}
        ]},

        {'role': 'assistant', 'content': [{"type": "image_url", "image_url": "这是个图片链接"}]},
        {'role': 'user', 'content': [
            {"type": "text", "text": "这是个文本"},
            {"type": "image_url", "image_url": "这是个图片链接"}
        ]},
    ]

    messages = [{'role': 'system',
                 'content': 'undefined\n Current date: 2025-03-13'},
                {'role': 'user',
                 'content': [{'type': 'text', 'text': '解读'},
                             {'type': 'image_url',
                              'image_url': 'https://ai.chatfire.cn/files/images/xx-1741850404348-339a12ba3.png'}]},
                {},
                {'role': 'user', 'content': '总结一下'}]

    messages = [{'role': 'system',
                 'content': 'undefined\n Current date: 2025-03-13'},
                {'role': 'user',
                 'content': [{'type': 'text', 'text': '解读'},
                             {'type': 'image_url',
                              'image_url': 'https://ai.chatfire.cn/files/images/xx-1741850404348-339a12ba3.png'}]},
                {},
                {'role': 'user', 'content': '总结一下'}]

    messages = [{'role': 'system',
                 'content': 'undefined\n Current date: 2025-03-13'},
                {'role': 'user',
                 'content': [{'type': 'text', 'text': '一句话总结'},
                             {'type': 'image_url',
                              'image_url': 'https://ai.chatfire.cn/files/images/uniacess删除-1741849647273-c3f3be340.txt'}]},
                {},
                {'role': 'user', 'content': '总结'}]

    messages = [{'role': 'system',
                 'content': 'undefined\n Current date: 2025-03-13'},
                {'role': 'user',
                 'content': [{'type': 'text', 'text': '一句话总结'},
                             {'type': 'image_url',
                              'image_url': 'https://ai.chatfire.cn/files/images/uniacess删除-1741853464016-b176842ad.txt'}]},
                {},
                {'role': 'user',
                 'content': [{'type': 'text', 'text': '一句话总结'},
                             {'type': 'image_url',
                              'image_url': 'https://ai.chatfire.cn/files/images/uniacess删除-1741853464016-b176842ad.txt'}]},
                {},
                {'role': 'assistant',
                 'content': [{'type': 'text', 'text': '一句话总结'},
                             {'type': 'image_url',
                              'image_url': 'https://ai.chatfire.cn/files/images/uniacess删除-1741853464016-b176842ad.txt'}]},
                {},
                {'role': 'user',
                 'content': [{'type': 'text', 'text': '一句话总结'},
                             {'type': 'image_url',
                              'image_url': 'https://ai.chatfire.cn/files/images/uniacess删除-1741853464016-b176842ad.txt'}]},
                {},
                {'role': 'user',
                 'content': [{'type': 'text', 'text': '一句话总结'},
                             {'type': 'image_url',
                              'image_url': 'https://ai.chatfire.cn/files/images/uniacess删除-1741853464016-b176842ad.txt'}]},
                {},
                {'role': 'user',
                 'content': [
                     {'type': 'image_url',
                      'image_url': 'https://ai.chatfire.cn/files/images/uniacess删除-1741853464016-b176842ad.txt'},
                     {
                         "type": "input_audio",
                         "input_audio": {
                             "data": "base64_audio",
                             "format": "wav"
                         }
                     },
                     {'type': 'text', 'text': '一句话总结'},

                 ],

                 },
                {},
                # {'role': 'user', 'content': '总结'}
                ]
    #
    # r = ChatCompletionRequest(model="gpt-3.5-turbo", messages=messages)
    # r.messages[-1]['content'] = [{"type": "image_url", "image_url": {"url": r.urls[-1]}}]
    # print(r)

    # print(chat_completion_chunk)
    # print(chat_completion)
    # print(chat_completion_chunk_stop)

    # print(CompletionRequest(messages=messages).last_urls)
    print(CompletionRequest(messages=messages).last_urls)

    # print(mesages)
    # print(CompletionRequest(messages=messages).last_assistant_content)

    # print(chat_completion_chunk)
    # print(chat_completion)


    chat_completion_chunk.usage = dict(
        completion_tokens=10,
        prompt_tokens=10,
        total_tokens=20,
    )

    print(chat_completion_chunk)
