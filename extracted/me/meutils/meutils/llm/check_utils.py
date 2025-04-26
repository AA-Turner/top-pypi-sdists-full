#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : check_utils
# @Time         : 2024/9/30 13:18
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.decorators.retry import retrying
from meutils.caches import rcache
from httpx import TimeoutException

from openai import OpenAI, AsyncOpenAI


async def check_tokens(tokens, check_token: Callable):
    r = []
    for batch in tqdm(list(tokens) | xgroup(32)):
        bools = await asyncio.gather(*map(check_token, batch))
        r += list(itertools.compress(batch, bools))
    return r


@retrying()
@rcache(ttl=1 * 3600)
async def check_token_for_siliconflow(api_key, threshold: float = 0):
    if not isinstance(api_key, str):
        return await check_tokens(api_key, check_token_for_siliconflow)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json"
    }
    try:
        async with httpx.AsyncClient(headers=headers, timeout=60) as client:
            response: httpx.Response = await client.get("https://api.siliconflow.cn/v1/user/info")
            response.raise_for_status()

            logger.debug(response.text)
            logger.debug(response.status_code)

            if response.is_success:
                logger.debug(api_key)
                total_balance = response.json()['data']['totalBalance']
                return float(total_balance) >= threshold
    except TimeoutException as e:
        # logger.error(traceback.format_exc().strip())

        logger.error("Timeout")

        return True

    except Exception as e:
        logger.error(f"Error: {e}\n{api_key}")
        return False


@retrying()
async def check_token_for_openai(api_key, base_url="https://api.stepfun.cn/v1"):
    try:
        client = AsyncOpenAI(
            base_url=base_url,
            api_key=api_key,
        )
        models = await client.models.list()
        logger.debug(models)
        return True

    except Exception as e:
        logger.error(e)
        return False


@retrying()
async def check_token_for_jina(api_key, threshold=1000):
    if not isinstance(api_key, str):
        return await check_tokens(api_key, check_token_for_jina)

    params = {
        "api_key": api_key,  # "jina_c8da77fed9704d558c8def39837960edplTLkNYrsPTJHBF1HcYg_RkRVh0X"
    }

    try:
        async with httpx.AsyncClient(base_url="https://embeddings-dashboard-api.jina.ai/api/v1", timeout=60) as client:
            response: httpx.Response = await client.get("/api_key/user", params=params)
            response.raise_for_status()

            logger.debug(response.text)
            logger.debug(response.status_code)

            if response.is_success:
                data = response.json()
                total_balance = data['wallet']['total_balance']
                return float(total_balance) >= threshold

    except Exception as e:
        logger.error(f"Error: {e}\n{api_key}")
        return False


@retrying()
async def check_token_for_moonshot(api_key, threshold: float = 0):
    if not isinstance(api_key, str):
        return await check_tokens(api_key, check_token_for_jina)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json"
    }

    try:
        async with httpx.AsyncClient(base_url="https://api.moonshot.cn/v1", headers=headers, timeout=60) as client:
            response: httpx.Response = await client.get("/users/me/balance")
            response.raise_for_status()

            logger.debug(response.text)
            logger.debug(response.status_code)

            if response.is_success:
                data = response.json()
                logger.debug(data)
                balance = data['data']['available_balance']
                return float(balance) >= threshold

    except Exception as e:
        logger.error(f"Error: {e}\n{api_key}")
        return False


@retrying()
async def check_token_for_gemini(api_key):
    if not isinstance(api_key, str):
        return await check_tokens(api_key, check_token_for_gemini)
    try:
        client = AsyncOpenAI(
            api_key=api_key,
            base_url=os.getenv("GOOGLE_BASE_URL"),
        )
        await client.models.list()
        return True
    except TimeoutException as e:
        raise

    except Exception as e:
        logger.error(f"Error: {e}\n{api_key}")
        return False


@retrying()
async def check_token_for_ppinfra(api_key, threshold: float = 1):
    if not isinstance(api_key, str):
        return await check_tokens(api_key, check_token_for_ppinfra)
    try:
        client = AsyncOpenAI(base_url="https://api.ppinfra.com/v3/user", api_key=api_key)
        data = await client.get("", cast_to=object)
        # logger.debug(data)  # credit_balance
        return data["credit_balance"] > threshold
    except TimeoutException as e:
        raise

    except Exception as e:
        logger.error(f"Error: {e}\n{api_key}")
        return False


if __name__ == '__main__':
    from meutils.config_utils.lark_utils import get_next_token_for_polling

    check_valid_token = partial(check_token_for_siliconflow, threshold=-1)

    pass
    # arun(check_valid_token("sk-LlB4W38z9kv5Wy1c3ceeu4PHeIWs6bbWsjr8Om31jYvsucRv", threshold=0.1))

    # FEISHU_URL = "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=KVClcs"

    # b = arun(check_token_for_openai(os.getenv("STEP_API_KEY")))

    # arun(get_next_token_for_polling(check_token=check_token_for_openai, feishu_url=FEISHU_URL))

    # arun(check_token_for_jina(["jina_c8da77fed9704d558c8def39837960edplTLkNYrsPTJHBF1HcYg_RkRVh0X"]*10))

    # arun(check_token_for_siliconflow("sk-jcsgbsqkdctaxunqljmghdahokavyliamkcgbhosfsoyaeln"))
    # "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=79272d"
    # arun(check_token_for_moonshot("sk-iabLMgfFvuahlh5u3oM7kk84pjIciRzqCbNTDt15PVxQM78K"))
    # sk-kk7ALp38EG63yPzJtmind5sEPiHipCcI2NbqW97QlWcvJfiW

    # arun(check_token_for_moonshot("sk-Qnr87vtf2Q6MEfc2mVNkVZ4qaoZg3smH9527I25QgcFe7HrT"))

    arun(check_token_for_ppinfra("sk_DkIaRrPq7sTiRPevhjV9WFZN3FvLk6WhCXOj1JAwu6c"))
