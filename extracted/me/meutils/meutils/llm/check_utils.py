#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : check_utils
# @Time         : 2024/9/30 13:18
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import os

from meutils.pipe import *
from meutils.decorators.retry import retrying
from meutils.caches import rcache
from httpx import TimeoutException

from openai import OpenAI, AsyncOpenAI


def skip_cache_func(*args, **kwargs):
    is_valid = args[0]  # 无效key 缓存
    return is_valid

    # return False  # True不缓存 False缓存


async def check_tokens(tokens, check_token: Callable):
    r = []
    for batch in tqdm(list(tokens) | xgroup(32)):
        bools = await asyncio.gather(*map(check_token, batch))
        r += list(itertools.compress(batch, bools))
    return r


@retrying()
@rcache(ttl=30 * 24 * 3600, skip_cache_func=skip_cache_func)
async def check_token_for_siliconflow(api_key, threshold: float = 0):
    if not isinstance(api_key, str):
        return await check_tokens(api_key, check_token_for_siliconflow)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json"
    }
    try:

        client = AsyncOpenAI(base_url=os.getenv("SILICONFLOW_BASE_URL"), api_key=api_key)
        # _ = await client.chat.completions.create(
        #     model="Qwen/Qwen3-8B",
        #     messages=[{'role': 'user', 'content': "hi"}],
        #     max_tokens=1)
        # print(_)
        if models := (await client.models.list()).data:
            if threshold <= 0: return True  # 有效key

            async with httpx.AsyncClient(headers=headers, timeout=60) as client:
                response: httpx.Response = await client.get("https://api.siliconflow.cn/v1/user/info")
                response.raise_for_status()

                logger.debug(response.text)
                logger.debug(response.status_code)

                if response.is_success:
                    logger.debug(api_key)
                    total_balance = response.json()['data']['totalBalance']
                    return float(total_balance) >= threshold
        else:
            return False
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
        logger.debug(data)  # credit_balance
        return data["credit_balance"] > threshold
    except TimeoutException as e:
        raise

    except Exception as e:
        logger.error(f"Error: {e}\n{api_key}")
        return False


@retrying()
# @rcache(ttl=120)
async def check_token_for_sophnet(api_key, threshold: float = 1):
    if not isinstance(api_key, str):
        return await check_tokens(api_key, check_token_for_sophnet)

    try:
        client = AsyncOpenAI(base_url=os.getenv("SOPHNET_BASE_URL"), api_key=api_key)
        data = await client.chat.completions.create(
            model="DeepSeek-v3",
            messages=[{"role": "user", "content": "hi"}],
            stream=True,
            max_tokens=1
        )
        return True
    except TimeoutException as e:
        raise

    except Exception as e:
        logger.error(f"Error: {e}\n{api_key}")
        return False


#
@retrying()
@rcache(ttl=3600, skip_cache_func=skip_cache_func)
async def check_token_for_volc(api_key, threshold: float = 1, purpose: Optional[str] = None):
    if not isinstance(api_key, str):
        return await check_tokens(api_key, check_token_for_volc)

    try:
        base_url = os.getenv("VOLC_BASE_URL") or "https://ark.cn-beijing.volces.com/api/v3"
        client = AsyncOpenAI(base_url=base_url, api_key=api_key)

        if purpose:
            response = client.images.generate(
                model="doubao-seedream-3-0-t2i-250415",
                prompt="鱼眼镜头，一只猫咪的头部，画面呈现出猫咪的五官因为拍摄方式扭曲的效果。",
                size="1024x1024",
                response_format="url"
            )
        else:

            response = await client.chat.completions.create(
                model="deepseek-v3-250324",
                messages=[{"role": "user", "content": "hi"}],
                max_tokens=1
            )
        return True
    except TimeoutException as e:
        raise

    except Exception as e:
        logger.error(f"Error: {e}\n{api_key}")
        return False


@retrying()
async def check_token_for_zhipu(api_key, threshold: float = 1, resource_package_name: Optional[str] = None):
    if not isinstance(api_key, str):
        return await check_tokens(api_key, check_token_for_ppinfra)
    try:
        client = AsyncOpenAI(base_url="https://bigmodel.cn/api/biz/tokenAccounts/list", api_key=api_key)
        data = await client.get("", cast_to=object)
        logger.debug(bjson(data))

        if resource_package_name:
            # "resourcePackageName": "【新用户专享】200万通用模型资源包",
            # "resourcePackageName": "【新用户专享】400次图像、视频生成、搜索工具次包",
            # "resourcePackageName": "【新用户专享】200万通用模型资源包",
            # "resourcePackageName": "【新用户专享】200万GLM-Z1-Air推理资源包",
            # "resourcePackageName": "【新用户专享】30次Vidu系列视频生成次包",
            for d in data["rows"]:
                if resource_package_name.lower() in d["resourcePackageName"].lower():
                    logger.debug(bjson(d))
                    return d["tokenBalance"] >= threshold
        else:
            logger.debug(bjson(data))
            return True

    except TimeoutException as e:
        raise

    except Exception as e:
        logger.error(f"Error: {e}\n{api_key}")
        return False


@retrying()
@rcache(ttl=1 * 24 * 3600, skip_cache_func=skip_cache_func)
async def check_token_for_fal(token, threshold: float = 0):
    try:
        # data = await AsyncClient(key=token).upload(b'', '', '')
        from fal_client.client import AsyncClient
        data = await AsyncClient(key=token).run(
            "fal-ai/any-llm",
            arguments={
                "model": "meta-llama/llama-3.2-1b-instruct",
                "prompt": "1+1=",
                "max_tokens": 1,
            },
        )
        logger.debug(data)
        return True
    except Exception as exc:
        logger.error(exc)
        return False


if __name__ == '__main__':
    from meutils.config_utils.lark_utils import get_next_token_for_polling, get_series

    check_valid_token = partial(check_token_for_siliconflow, threshold=-1)

    # arun(check_valid_token("sk-voxrapfsyirpibnjksblyjznfpxfgkyiyazcrjvmjxdcossh"))

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

    # arun(check_token_for_ppinfra("sk_DkIaRrPq7sTiRPevhjV9WFZN3FvLk6WhCXOj1JAwu6c"))

    # from meutils.config_utils.lark_utils import get_next_token_for_polling, get_series
    #
    # arun(get_series("https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=PP1PGr"))

    # arun(check_token_for_sophnet(["gzHpp_zRtGaw1IjpepCiWu_ySyke3Hu5wR5VNNYMLyXwAESqZoZWUZ4T3tiWUxtac6n9Hk-kRRo4_jPQmndo-g"]))

    # arun(check_token_for_ppinfra("sk_F0kgPyCMTzmOH_-VCEJucOK8HIrbnLGYm_IWxBToHZQ"))

    # arun(check_token_for_volc("f1f394db-59e9-4cdd-9d12-b11d50173efc"))
    # arun(check_token_for_ppinfra("sk_mCb5sRGTi6GXkSRp5F679Rbs0V_Hfee3p85lccGXCOo"))

    # arun(check_token_for_zhipu(api_key="e130b903ab684d4fad0d35e411162e99.PqyXq4QBjfTdhyCh",
    #                            resource_package_name='vidu'))

    # arun(check_token_for_fal("56d8a95e-2fe6-44a6-8f7d-f7f9c83eec24:537f06b6044770071f5d86fc7fcd6d6f"))

    arun(check_token_for_ppinfra("sk_NdGt2jb_QSEW_1cauXnWK-qShGIJ_irWgtG-DEBVs4A"))
