#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : commom
# @Time         : 2024/5/30 11:20
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

import tiktoken
from contextlib import asynccontextmanager
from openai import AsyncOpenAI, OpenAI, AsyncStream
from meutils.llm.clients import AsyncOpenAI, OpenAI, AsyncStream

from meutils.pipe import *
from meutils.async_utils import achain, async_to_sync
from meutils.notice.feishu import send_message

from meutils.apis.oneapi.user import get_user_money, get_api_key_log
from meutils.apis.oneapi.token import get_api_key_money

from meutils.schemas.oneapi import MODEL_PRICE
from meutils.schemas.openai_types import CompletionRequest, ChatCompletionRequest, TTSRequest, STTRequest
from meutils.schemas.openai_types import ChatCompletion, ChatCompletionChunk, CompletionUsage
from meutils.schemas.openai_types import chat_completion, chat_completion_chunk, chat_completion_chunk_stop  # todo

from meutils.schemas.image_types import ImageRequest

token_encoder = tiktoken.get_encoding('cl100k_base')
token_encoder_with_cache = lru_cache(maxsize=1024)(token_encoder.encode)

CHAT_COMPLETION_PARAMS = get_function_params()
IMAGES_GENERATE_PARAMS = get_function_params(fn=OpenAI(api_key='').images.generate)
AUDIO_SPEECH_PARAMS = get_function_params(fn=OpenAI(api_key='').audio.speech.create)
AUDIO_TRANSCRIPTIONS_PARAMS = get_function_params(fn=OpenAI(api_key='').audio.transcriptions.create)


def to_openai_params(
        request: Union[dict, CompletionRequest, ChatCompletionRequest, ImageRequest, TTSRequest, STTRequest],
        redirect_model: Optional[str] = None,
) -> dict:
    data = copy.deepcopy(request)
    if not isinstance(request, dict):
        data = request.model_dump(exclude_none=True)

    PARAMS = CHAT_COMPLETION_PARAMS
    if isinstance(request, ChatCompletionRequest):
        PARAMS = CHAT_COMPLETION_PARAMS
    elif isinstance(request, ImageRequest):
        PARAMS = IMAGES_GENERATE_PARAMS
    elif isinstance(request, TTSRequest):
        PARAMS = AUDIO_SPEECH_PARAMS
    elif isinstance(request, STTRequest):
        PARAMS = AUDIO_TRANSCRIPTIONS_PARAMS

    extra_body = {}
    for key in list(data):
        if key not in PARAMS:
            extra_body.setdefault(key, data.pop(key))

    data['extra_body'] = extra_body  # 拓展字段
    data['model'] = redirect_model or data['model']

    if request.model.startswith(("gemini",)):
        data.pop("extra_body", None)
        data.pop("presence_penalty", None)
        data.pop("frequency_penalty", None)

    return data


def to_openai_completion_params(
        request: Union[dict, ChatCompletionRequest],
        redirect_model: Optional[str] = None,
) -> dict:
    data = copy.deepcopy(request)
    if isinstance(request, ChatCompletionRequest):
        data = request.model_dump(exclude_none=True)

    extra_body = {}
    for key in list(data):
        if key not in CHAT_COMPLETION_PARAMS:
            extra_body.setdefault(key, data.pop(key))

    data['extra_body'] = extra_body  # 拓展字段
    data['model'] = redirect_model or data['model']

    return data


def to_openai_images_params(
        request: Union[dict, ImageRequest],
        redirect_model: Optional[str] = None
) -> dict:
    data = copy.deepcopy(request)
    if not isinstance(request, dict):
        data = request.model_dump(exclude_none=True)

    extra_body = {}
    for key in list(data):
        if key not in IMAGES_GENERATE_PARAMS:
            extra_body.setdefault(key, data.pop(key))

    data['extra_body'] = extra_body  # 拓展字段
    data['model'] = redirect_model or data.get('model')

    return data


def ppu(model='ppu', api_key: Optional[str] = None):
    client = OpenAI(api_key=api_key)
    return client.chat.completions.create(messages=[{'role': 'user', 'content': 'hi'}], model=model)


async def appu(
        model='ppu',
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
):
    if model not in MODEL_PRICE:
        _ = f"模型未找到「{model}」，默认ppu-1"

        logger.warning(_)
        send_message(_, title=__name__)
        model = "ppu-1"

    client = AsyncOpenAI(api_key=api_key, base_url=base_url)
    response = await client.chat.completions.create(messages=[{'role': 'user', 'content': 'hi'}], model=model)


@asynccontextmanager
async def ppu_flow(
        api_key: str,
        base_url: Optional[str] = None,

        n: Optional[float] = 1,  # 计费倍率
        post: str = "ppu-1",  # 后计费

        pre: str = "ppu-0001",  # 前置判断，废弃
        **kwargs
):
    """
    查余额
    失败，先扣费
    成功，充足，后扣费
    成功，不足，报错
    """
    if n is not None and n > 0:  # todo: 跳过某些用户
        try:
            user_money, api_key_money = await asyncio.gather(*[get_user_money(api_key), get_api_key_money(api_key)])
            money = min(user_money or 1, api_key_money or 1)
            logger.debug(f"PREPAY: api-key余额 {money}")
        except Exception as e:
            logger.error(e)
            money = None

        if money and money > MODEL_PRICE.get(post, 0.1):  # 后扣费
            yield

        # 计费逻辑
        n = int(np.round(n)) or 1  # np.ceil(n)
        await asyncio.gather(*[appu(post, api_key=api_key, base_url=base_url) for _ in range(n)])

        if money is None:  # 先扣费
            yield

    else:  # 不计费
        yield


def create_chat_completion(
        completion: Union[str, Iterable[str]],
        redirect_model: str = '',
        chat_id: Optional[str] = None
):
    if isinstance(completion, Iterable):  # ChatCompletion
        completion = ''.join(completion)

    chat_completion.choices[0].message.content = completion

    chat_completion.id = chat_id or shortuuid.random()
    chat_completion.created = int(time.time())

    chat_completion.model = redirect_model or chat_completion.model
    return chat_completion


async def create_chat_completion_chunk(
        completion_chunks: Union[
            Coroutine,
            AsyncStream[ChatCompletionChunk],
            Iterator[Union[str, ChatCompletionChunk]],
            AsyncIterator[Union[str, ChatCompletionChunk]]
        ],
        redirect_model: str = ' ',  # todo: response_model
        chat_id: Optional[str] = None
):
    """ todo： 替换 前缀
        async def main():
            data = {}
            _ = AsyncOpenAI().chat.completions.create(**data)
            async for i in create_chat_completion_chunk(_):
                print(i)
    """

    # logger.debug(type(completion_chunks))
    # logger.debug(isinstance(completion_chunks, Coroutine))

    if isinstance(completion_chunks, Coroutine):  # 咋处理
        completion_chunks = await completion_chunks
        # logger.debug(type(completion_chunks))

    chat_completion_chunk.id = chat_id or f"chatcmpl-{shortuuid.random()}"
    chat_completion_chunk_stop.id = chat_completion_chunk.id
    async for completion_chunk in achain(completion_chunks):

        # logger.debug(completion_chunk)
        chat_completion_chunk.created = int(time.time())
        if isinstance(completion_chunk, str):
            chat_completion_chunk.choices[0].delta.content = completion_chunk
            chat_completion_chunk.model = redirect_model or chat_completion_chunk.model
            yield chat_completion_chunk.model_dump_json()
        else:  # todo: AttributeError: 'tuple' object has no attribute 'model'
            try:
                chat_completion_chunk_stop.id = completion_chunk.id  ##############
                completion_chunk.model = redirect_model or completion_chunk.model
                chat_completion_chunk_stop.usage = completion_chunk.usage  ############## 需要判断 usage？
                yield completion_chunk.model_dump_json()
            except Exception as e:
                from meutils.notice.feishu import send_message
                send_message(f"{type(completion_chunks)}\n\n{completion_chunks}\n\n{completion_chunk}", title=str(e))

    yield chat_completion_chunk_stop.model_dump_json()
    yield "[DONE]"  # 兼容标准格式


if __name__ == '__main__':
    # print(ppu())
    # print(appu())
    # print(arun(appu()))

    # print(create_chat_completion('hi'))
    # print(create_chat_completion('hi', redirect_model='@@'))
    #
    #
    # async def main():
    #     async for i in create_chat_completion_chunk(['hi', 'hi'], redirect_model='@@'):
    #         print(i)
    #
    #
    # arun(main())

    # encode = lru_cache()(token_encoder.encode)
    # # encode = token_encoder.encode
    #
    # with timer('xx'):
    #     encode("xxxxxxxxxxxxxxxxx" * 1000)
    #
    # with timer('xx'):
    #     encode("xxxxxxxxxxxxxxxxx" * 1000)
    #
    # with timer('xx'):
    #     encode("xxxxxxxxxxxxxxxxx" * 1000)

    # print(CHAT_COMPLETION_PARAMS)
    # print(IMAGES_GENERATE_PARAMS)
    # from openai.types.chat import ChatCompletionToolParam
    #
    # print(ChatCompletionToolParam.__annotations__)
    #
    # ChatCompletionToolParam(**{'function': '', 'type': ''})

    async def main():
        with timer():
            try:
                async with ppu_flow(api_key="sk-OYK4YxtTlWauT2TdGR5FTAJpkRmSnDwPly4cve0cAvMcrBkZ", post="api-oss",
                                    n=1):
                    logger.debug("消费了哦")

            except Exception as e:
                pass
                logger.error(e)
                # logger.debug(e.response.status_code)
                # logger.debug(e.response.text)


    arun(main())

    # to_openai_params(ChatCompletionRequest())

    print(token_encoder.encode('hi'))
