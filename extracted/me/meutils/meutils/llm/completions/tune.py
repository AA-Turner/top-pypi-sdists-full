#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : tune
# @Time         : 2024/9/20 13:51
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.apis.proxy.ips import get_one_proxy
from meutils.decorators.retry import retrying
from meutils.str_utils.regular_expression import remove_date_suffix
from meutils.notice.feishu import send_message as _send_message
from meutils.config_utils.lark_utils import aget_spreadsheet_values, get_next_token_for_polling

from meutils.llm.utils import oneturn2multiturn
from meutils.schemas.openai_types import chat_completion, chat_completion_chunk, ChatCompletionRequest, CompletionUsage

BASE_URL = "https://chat.tune.app"
FEISHU_URL_VIP = "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=gCrlN4"
FEISHU_URL_API = "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=9HwQtX"
"https://chat.tune.app/api/models"
# r = requests.get("https://chat.tune.app/tune-api/appConfig")
# r = requests.get("https://chat.tune.app/api/guestLogin")

# https://chat.tune.app/api/models?noCache=true

send_message = partial(
    _send_message,
    url="https://open.feishu.cn/open-apis/bot/v2/hook/e0db85db-0daf-4250-9131-a98d19b909a9",
    title=__name__
)

# data = httpx.get("https://chat.tune.app/api/models?noCache=true", timeout=30).json()
# models = jsonpath.jsonpath(data, expr='$..id')
#
# DEFAULT_MODEL = "openai/gpt-4o-mini"  # "kaushikaakash04/tune-blob"
# MODELS = {model.split('/')[-1]: model for model in models}

# logger.debug(bjson(MODELS))


DEFAULT_MODEL = "openai/gpt-4o-mini"
MODELS = {
    "o1-mini": "openai/o1-mini",
    "o1-preview": "openai/o1-preview",
    "o1-mini-2024-09-12": "openai/o1-mini",
    "o1-preview-2024-09-12": "openai/o1-preview",
    "gpt-4o": "openai/gpt-4o",
    "gpt-4o-mini": "openai/gpt-4o-mini",

    "claude-3.5-sonnet": "anthropic/claude-3.5-sonnet",
    "claude-3.5-haiku": "anthropic/claude-3.5-haiku",
    "claude-3-haiku": "anthropic/claude-3-haiku",

    "claude-3.5-sonnet-20240620": "anthropic/claude-3.5-sonnet",
    "claude-3.5-sonnet-20241022": "anthropic/claude-3.5-sonnet",
    "claude-3.5-haiku-20241022": "anthropic/claude-3.5-haiku",

    "gemini-flash-1.5-8b": "google/gemini-flash-1.5-8b",

    "tune-blob": "kaushikaakash04/tune-blob",
    "llama-3.1-8b-instruct": "meta/llama-3.1-8b-instruct",
    "pixtral-12B-2409": "mistral/pixtral-12B-2409",
    "qwen-2.5-coder-32b": "qwen/qwen-2.5-coder-32b",
    "llama-3.1-70b-instruct": "meta/llama-3.1-70b-instruct",
    "llama-3.2-90b-vision": "meta/llama-3.2-90b-vision",
    "llama3.1-euryale-70b": "sao10k/llama3.1-euryale-70b",
    "qwen-2.5-72b": "qwen/qwen-2.5-72b",
    "openrouter-goliath-120b-4k": "rohan/openrouter-goliath-120b-4k",
    "mistral-large": "mistral/mistral-large",
    "llama-3.1-405b-instruct": "meta/llama-3.1-405b-instruct",
    "mixtral-8x7b-instruct": "mistral/mixtral-8x7b-instruct",
    "hermes-3-llama-3.1-405b": "nousresearch/hermes-3-llama-3.1-405b",
    "tune-wizardlm-2-8x22b": "rohan/tune-wizardlm-2-8x22b",

    "tune-mythomax-l2-13b": "rohan/tune-mythomax-l2-13b",
    "qwen-2-vl-72b": "qwen/qwen-2-vl-72b",
}


#
# html_content = httpx.get(url).text
#
# # 正则表达式匹配以 "/_next/static/chunks/7116-" 开头的 JS 文件
# pattern = r'(/_next/static/chunks/7116-[^"]+\.js)'
#
# # 使用 re.findall() 找到所有匹配项
# matches = re.findall(pattern, html_content)


#
# "/_next/static/chunks/7116-aed224a0caaab94c.js"
#
# # 打印结果
# for match in matches:
#     print(match)


@alru_cache(ttl=1000)
@retrying(predicate=lambda r: r is None)
async def get_access_token():
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=30) as client:
        response = await client.get("/api/guestLogin")

        logger.debug(response.status_code)
        logger.debug(response.text)

        if response.is_success:
            return response.json()["accessToken"]


@alru_cache(ttl=60)
@retrying(predicate=lambda r: r is None)
async def create_conversation_id(token: str):
    headers = {
        "authorization": token
    }
    conversation_id = str(uuid.uuid4())  # shortuuid.random()
    # conversation_id = "af306c40-8f85-47a7-a027-185da084c6cc"
    params = {
        "conversation_id": conversation_id,
        "organization_id": "undefined",
        "model": "anthropic/claude-3.5-sonnet",  # "kaushikaakash04/tune-blob",
        "currency": "USD"
    }
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=30) as client:
        response = await client.post("/api/new", params=params)
        logger.debug(response.status_code)
        logger.debug(response.text)
        return conversation_id

        # response = await client.get(f"/?id={conversation_id}", headers=headers)
        # html_content = response.text
        # pattern = r'(/_next/static/chunks/7116-[^"]+\.js)'
        # js = re.findall(pattern, html_content)[-1]
        #
        # logger.debug(js)
        #
        # response = await client.get(js)
        #
        # logger.debug(response.status_code)
        # next_action = response.text.split(',A=(0,a.$)("')[1][:40]
        # logger.debug(next_action)  # 2bc738a7215e149dbd4601a440f3b6df45089338 过期时间
        #
        # headers = {
        #     'next-action': next_action,
        #     'Cookie': f"AccessToken={token}",
        #
        #     'content-type': 'text/plain;charset=UTF-8',
        # }
        # payload = "[]"
        # response = await client.post(f"/?id={conversation_id}", headers=headers, content=payload)
        #
        # logger.debug(response.status_code)
        # logger.debug(response.text)
        #
        # return conversation_id


@retrying(max_retries=3)
async def create(request: ChatCompletionRequest, token: Optional[str] = None, vip: Optional[bool] = False):
    request.model = remove_date_suffix(request.model)

    if vip:
        token = await get_next_token_for_polling(feishu_url=FEISHU_URL_VIP)

    token = token or await get_access_token()
    conversation_id = await create_conversation_id(token)

    logger.debug(conversation_id)

    use_search = False
    if request.messages[0].get('role') != 'system':  # 还原系统信息
        request.messages.insert(0, {'role': 'system', 'content': f'You are {request.model}'})

    if request.model.startswith("net-") or request.model.endswith("all"):
        request.model = "kaushikaakash04/tune-blob"
        use_search = True
    else:
        request.model = MODELS.get(request.model, DEFAULT_MODEL)
    logger.debug(request)

    headers = {
        "authorization": token,
        # 'Cookie': f"AccessToken={token};",
        "content-type": "text/plain;charset=UTF-8",

    }
    params = {
        # "organization_id": "undefined",
        # "organization_id": "eb0fb996-2317-467b-9847-15f6c40000b7",
        "retry": 2,
    }
    payload = {
        # "query": request.last_content,
        "query": oneturn2multiturn(request.messages),
        # "images": request.urls,  # todo: 兼容base64

        "conversation_id": conversation_id,
        "model_id": request.model,  # "kaushikaakash04/tune-blob"
        "browseWeb": use_search,
        "attachement": "",
        "attachment_name": "",
        # "messageId": "4a33e497-efb7-4d8f-ae45-9aa7d2c1c5af1726811555410",
        # "prevMessageId": "4a33e497-efb7-4d8f-ae45-9aa7d2c1c5af1726811555410",

        "check": "286600"
    }

    yield "\n"  # 提升首字速度
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=300) as client:
        async with client.stream("POST", "/api/prompt", json=payload, params=params) as response:
            logger.debug(response.status_code)
            # logger.debug(response.text)

            async for chunk in response.aiter_lines():
                # logger.debug(chunk)

                # if chunk == '{"value":""}':
                #     async for _chunk in create(request, token, vip):
                #         yield _chunk
                #     return

                if chunk and chunk.startswith("{"):
                    chunk = (
                        chunk.replace("Blob", "OpenAI")
                        .replace("TuneAI", "OpenAI")
                        .replace("TuneStudio", "OpenAI")
                        .replace("Tune", "OpenAI")
                        .replace("https://studio.tune.app", "https://openai.com")
                        .replace("https://tunehq.ai", "https://openai.com")
                        .replace("https://chat.tune.app", "https://openai.com")
                    )

                    try:
                        chunk = json.loads(chunk)
                        chunk = chunk.get('value', "")
                        yield chunk
                        # break

                    except Exception as e:
                        _ = f"{e}\n{chunk}"
                        logger.error(_)
                        send_message(_)
                        yield ""
                elif chunk.strip():
                    logger.debug(chunk)

            # {"value": "完成"}


if __name__ == '__main__':
    # arun(get_access_token())
    # arun(create_conversation_id(None))

    # model = "claude-3.5-sonnet"
    # model = "net-anthropic/claude-3.5-sonnet"
    # model = "all"

    model = "kaushikaakash04/tune-blob"
    # model = "openai/o1-mini"
    # model = "o1-mini-0609"

    # model = "openai/gpt-4o-mini"

    url = "https://d2e931syjhr5o9.cloudfront.net/bb5cc8e4-5cc2-45c5-8307-585b7ec6eada_1731634172097.png"

    request = ChatCompletionRequest(model=model, messages=[
        {'role': 'user', 'content': '你的知识库截止的几月份'},
        # {
        #     'role': 'user', 'content': [
        #     {"type": "text", "text": "解释下这张图片"},
        #     {"type": "image_url", "image_url": {"url": url}},
        # ]
        # }
    ])

    # arun(create(request, token=token, vip=True))
    # arun(create(request, vip=True))
    # arun(create(request, vip=False))
    arun(create(request))
