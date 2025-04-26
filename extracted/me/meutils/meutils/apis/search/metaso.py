#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : meta
# @Time         : 2024/11/11 17:03
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : todo 重构

from meutils.pipe import *
from meutils.schemas.metaso_types import FEISHU_URL, BASE_URL, MetasoRequest, MetasoResponse
from meutils.decorators.retry import retrying
from meutils.config_utils.lark_utils import get_next_token_for_polling
from meutils.apis.proxy.ips import FEISHU_URL_METASO, get_one_proxy, get_proxies
from meutils.schemas.openai_types import ChatCompletionRequest, CompletionRequest
from meutils.notice.feishu import send_message

from urllib.parse import quote_plus

token = "wr8+pHu3KYryzz0O2MaBSNUZbVLjLUYC1FR4sKqSW0p19vmcZAoEmHC72zPh/fHtOhYhCcR5GKXrxQs9QjN6dulxfOKfQkLdVkLMahMclPPjNVCPE8bLQut3zBABECLaSqpI0fVWBrdbJptnhASrSw=="

MODELS = {

    "ai-search": "detail",
    "ai-search-pro": "research",

    "ai-search:scholar": "detail",
    "ai-search-pro:scholar": "research",

    "deepseek-r1-metasearch": "strong-research",

    "meta-research": "strong-research",
    "meta-deepresearch": "strong-research",
    "deepseek-r1-metaresearch": "strong-research",
}

""
# pattern = re.compile('\[\[(\d+)\]\]')
pattern = re.compile(r'\[\[(\d+)\]\]')


def replace_ref(match):
    ref_num = match.group(1)
    return f'[^{ref_num}]'  # [[1]] -> [^1]


async def get_session_id(request: MetasoRequest, headers: Optional[dict] = None, proxy: Optional[str] = None):
    if proxy:
        logger.debug(proxy)

    headers = headers or {
        # "cookie": "uid=65fe812a09727c19a54b0328; sid=eb6f4fe9034b4c9497fceca7ff6bafdd",
        # "cookie": f"uid={shortuuid.random(24).lower()}; sid={shortuuid.random(32).lower()}"

        # "cookie": "JSESSIONID=8B267A5E2299C2BF46EB354104AACF76; tid=b103b947-be89-40b8-b162-80fdcda60807; aliyungf_tc=8cfbed3e5fd53c2a81605c7dcb63d45d3114b94750922ef63e04cb5a6ceccba1; s=bdpc; traceid=d21e97f303b546c0; hideLeftMenu=1; usermaven_id_UMO2dYNwFz=1y1t3p1t2t; uid=65fe812a09727c19a54b0328; sid=eb6f4fe9034b4c9497fceca7ff6bafdd; newSearch=false"

        # "token": "wr8+pHu3KYryzz0O2MaBSNUZbVLjLUYC1FR4sKqSW0p19vmcZAoEmHC72zPh/fHtxcdjbUPQpQ+cHJxaEajSgJMlmjIlIUew+aPZMEcnIqI1j3rHg9aAsbcYX/MF8lyJ+zJimUWQ2SOBo4yJQ6yUOQ=="
    }

    payload = request.model_dump(exclude_none=True)
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=30, proxy=proxy) as client:
        response = await client.post("/api/session", json=payload)
        response.raise_for_status()
        data = response.json()

        logger.debug(bjson(data))
        # {
        #     "errCode": 4001,
        #     "errMsg": "搜索次数超出限制"
        # }
        if data.get("errCode", 0) == 4001:
            logger.debug(data)
            # request_kwargs = {
            #     "proxies": await get_one_proxy(headers.get("cookie"), exclude_ips="154.40.54.76154.12.35.201"),
            #     # "proxies": proxies,
            # }
            # continue

        return data.get("data", {}).get("id")


@alru_cache(ttl=5 * 60)
@retrying(min=3, predicate=lambda r: r is False)
async def get_access_token(session_id: Optional[str] = None):
    pattern = r'<meta\s+id="meta-token"\s+content="([^"]+)"\s*/>'
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=30) as client:  # 测试token过期时间
        response = await client.get(f"/search/{session_id}")
        response.raise_for_status()

        tokens = re.findall(pattern, response.text)
        if not tokens:
            send_message(response.text, __name__)

        return tokens and tokens[0]


async def create(request: Union[ChatCompletionRequest, CompletionRequest]):
    if isinstance(request, CompletionRequest):
        request = ChatCompletionRequest(**request.model_dump())

    if request.last_content == 'ping':
        yield "pong"
        return

    system_fingerprint = request.system_fingerprint

    engine_type = ''
    if ":" in request.model:
        _, engine_type = request.model.split(':')

    model = None
    if request.model.startswith(("deepseek",)):
        model = "ds-r1"
        system_fingerprint = "deepseek-r1"

    request = MetasoRequest(
        model=model,
        mode=MODELS.get(request.model, "detail"),
        question=request.last_content,
    )

    logger.debug(request.model_dump_json(indent=4))

    headers = {}
    if "research" in request.mode:  # 登录
        cookie = await get_next_token_for_polling(FEISHU_URL)
        headers["cookie"] = cookie
        logger.debug(cookie)

    proxy = None
    # proxies = await get_proxies()
    session_id = await get_session_id(request, headers=headers, proxy=proxy)
    # session_id = None
    if session_id is None:  # 走代理: 随机轮询

        proxy = await get_one_proxy(feishu_url=FEISHU_URL_METASO)
        session_id = await get_session_id(request, headers=headers, proxy=proxy)

    token = await get_access_token(session_id)

    params = request.model_dump(exclude_none=True)
    params['token'] = token

    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, params=params, proxy=proxy, timeout=100) as client:
        async with client.stream(method="GET", url="/api/searchV2") as response:
            response.raise_for_status()

            references = []
            async for chunk in response.aiter_lines():

                if (chunk := chunk.strip()) and chunk != "data:[DONE]":
                    # logger.debug(chunk)

                    try:
                        response = MetasoResponse(chunk=chunk)
                        references += response.references

                        if len(response.content) == 1 and response.content.startswith('秘'):  # 替换 模型水印
                            response.content = f"{system_fingerprint} AI搜索，它是一款能够深入理解您的问题的AI搜索引擎。"
                            yield response.content
                            break

                        _ = pattern.sub(replace_ref, response.content)
                        yield _

                    except Exception as e:
                        logger.error(e)
                        logger.debug(response)
            if references:
                for i, ref in enumerate(references, 1):
                    title = ref.get("title")
                    url = ref.get("link") or ref.get("url") or ref.get("file_meta", {}).get("url", "")
                    url = quote_plus(url)

                    yield f"\n[^{i}]: [{title}]({url})\n"

                # logger.debug(bjson(references))


if __name__ == '__main__':
    # request = MetasoRequest(question="东北证券", mode='research')
    # request = MetasoRequest(question="你是谁", mode='detail', return_raw=True)  # concise
    # request = MetasoRequest(question="Chatfire", mode='concise', return_raw=False)  # concise

    # request = MetasoRequest(question="Chatfire", mode='detail', return_raw=False)  # concise
    # request = MetasoRequest(question="Chatfire", mode='research', response_format=False)  # concise

    # arun(get_session_id(request))
    # arun(get_access_token(request))
    """
    metasearch-
    """

    request = ChatCompletionRequest(
        # model="deepseek-search",
        # model="deepseek-r1-search",
        # model="11meta-deepresearch",
        model="meta-search",

        # model="ai-search",
        # model="ai-search:scholar",
        # model="ai-search-pro:scholar",

        # model="search-pro",

        # messages=[{'role': 'user', 'content': '今天南京天气怎么样'}]
        # messages=[{'role': 'user', 'content': '1+1'}]
        messages=[{'role': 'user', 'content': '周杰伦'}]

    )

    arun(create(request))

    # with timer():
    #     request = MetasoRequest(
    #         model='ds-r1',
    #         mode="research",
    #         question="南京今天天气",
    #
    #     )
    #     arun(get_session_id(request))
    # session_id = "8544840144331366400"
    #
    # arun(get_access_token(session_id))

    # wr8+pHu3KYryzz0O2MaBSNUZbVLjLUYC1FR4sKqSW0p19vmcZAoEmHC72zPh/fHtOhYhCcR5GKXrxQs9QjN6dulxfOKfQkLdVkLMahMclPPjNVCPE8bLQut3zBABECLaSqpI0fVWBrdbJptnhASrSw==
