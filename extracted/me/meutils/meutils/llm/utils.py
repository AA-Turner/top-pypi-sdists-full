#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : utils
# @Time         : 2024/6/20 09:08
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from contextlib import asynccontextmanager

from meutils.pipe import *
from meutils.llm.clients import AsyncOpenAI, OpenAI, AsyncStream
from meutils.schemas.oneapi import MODEL_PRICE
from meutils.notice.feishu import send_message
from meutils.apis.oneapi.utils import get_user_quota


async def ppu(
        model: str = 'ppu',
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
):
    if model not in MODEL_PRICE:
        send_message(f"模型未找到{model}，ppu-1默认", title=__name__)
        model = "ppu-1"

    client = AsyncOpenAI(api_key=api_key, base_url=base_url)
    r = await client.chat.completions.create(messages=[{'role': 'user', 'content': 'hi'}], model=model)


@asynccontextmanager
async def ppu_flow(
        api_key: str,
        base_url: Optional[str] = None,

        model: str = "ppu-1",  # 后计费

        n: float = 1,  # 计费次数

        **kwargs
):
    """
    查余额
    失败，先扣费
    成功，充足，后扣费
    成功，不足，报错
    """
    n = int(np.ceil(n))  # 0 不计费

    if n:  # 计费
        try:
            money = await get_user_quota(api_key)
            logger.debug(f"PREPAY: USER 余额 {money}")
        except Exception as e:
            logger.error(e)
            money = None

        if money and money > MODEL_PRICE.get(model, 0.1):
            yield  # 先执行

        # 执行计费逻辑
        await asyncio.gather(*[ppu(model, api_key=api_key, base_url=base_url) for _ in range(n)])

        if money is None:
            yield  # 后执行

    else:  # 不计费
        yield


def oneturn2multiturn(messages, template: Optional[str] = None):
    """todo: https://github.com/hiyouga/LLaMA-Factory/blob/e898fabbe3efcd8b44d0e119e7afaed4542a9f39/src/llmtuner/data/template.py#L423-L427

    _register_template(
    name="qwen",
    format_user=StringFormatter(slots=["<|im_start|>user\n{{content}}<|im_end|>\n<|im_start|>assistant\n"]),
    format_system=StringFormatter(slots=["<|im_start|>system\n{{content}}<|im_end|>\n"]),
    format_observation=StringFormatter(slots=["<|im_start|>tool\n{{content}}<|im_end|>\n<|im_start|>assistant\n"]),
    format_separator=EmptyFormatter(slots=["\n"]),
    default_system="You are a helpful assistant.",
    stop_words=["<|im_end|>"],
    replace_eos=True,
)
    :return:
    """
    # from jinja2 import Template, Environment, PackageLoader, FileSystemLoader
    #
    # system_template = Template("<|im_start|>system\n{{content}}<|im_end|>\n")  # .render(content='xxxx')
    # user_template = Template("<|im_start|>user\n{{content}}<|im_end|>\n")  # 最后<|im_start|>assistant\n
    # assistant_template = Template("<|im_start|>assistant\n{{content}}<|im_end|>\n")

    # todo: [{"type": "image_url", "image_url": {"url": ""}}]] 单独处理
    # 混元不是很感冒
    # context = "\n"
    # for message in messages:
    #     role, content = message.get("role"), message.get("content")
    #     context += f"<|im_start|>{role}\n{content}<|im_end|>\n"
    # context += "<|im_start|>assistant\n"
    if len(messages) == 1:
        return messages[0].get("content")

    context = "\n"
    for message in messages:
        role = message.get("role")
        content = message.get("content")
        if isinstance(content, list):  # content: {'type': 'text', 'text': ''}
            content = content[-1].get('text', '')

        context += f"{role}:\n{content}\n\n"
    context += "assistant:\n"
    return context



if __name__ == '__main__':
    async def main():
        with timer():
            try:
                async with ppu_flow(
                        api_key="sk-OYK4YxtTlWauT2TdGR5FTAJpkRmSnDwPly4cve0cAvMcrBkZ",
                        model="api-oss",
                        n=1):
                    logger.debug("消费了哦")

            except Exception as e:
                pass
                logger.error(e)
                # logger.debug(e.response.status_code)
                # logger.debug(e.response.text)


    arun(main())
