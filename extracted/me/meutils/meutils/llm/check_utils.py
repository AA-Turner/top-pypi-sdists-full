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
from meutils.caches import rcache
from meutils.decorators.retry import retrying
from meutils.config_utils.lark_utils import get_next_token

from httpx import TimeoutException

from openai import OpenAI, AsyncOpenAI, APIStatusError


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
async def check_token_for_modelscope(api_key, threshold: float = 0):
    if not isinstance(api_key, str):
        return await check_tokens(api_key, check_token_for_modelscope)

    base_url = 'https://api-inference.modelscope.cn/v1'
    try:
        client = AsyncOpenAI(
            base_url=base_url,
            api_key=api_key,
        )
        _ = await client.chat.completions.create(
            model="Qwen/Qwen3-0.6B",
            messages=[{'role': 'user', 'content': "hi"}],
            max_tokens=1,
            extra_body={"enable_thinking": False}
        )
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
@rcache(ttl=300 * 24 * 3600, skip_cache_func=skip_cache_func)
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
async def check_token_for_ppinfra(api_key, threshold: float = 1):  # 1块钱 10000
    if not isinstance(api_key, str):
        return await check_tokens(api_key, partial(check_token_for_ppinfra, threshold=threshold))
    try:
        client = AsyncOpenAI(base_url="https://api.ppinfra.com/v3/user", api_key=api_key.strip())
        data = await client.get("", cast_to=object)
        logger.debug(data)  # credit_balance
        return data["credit_balance"] >= threshold
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
        print(await client.models.list())
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
# @rcache(ttl=7 * 24 * 3600, skip_cache_func=skip_cache_func)
async def check_token_for_volc(api_key, threshold: float = 1, purpose: str = ""):
    if not isinstance(api_key, str):
        logger.error(api_key)
        return await check_tokens(
            api_key,
            partial(check_token_for_volc, purpose=purpose)
        )

    try:
        base_url = os.getenv("VOLC_BASE_URL") or "https://ark.cn-beijing.volces.com/api/v3"
        client = AsyncOpenAI(base_url=base_url, api_key=api_key, timeout=30)

        if purpose.startswith("doubao-seedance"):
            url = "https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks"

            payload = {
                # "model": "doubao-seedance-1-0-pro-250528",
                # "model": "doubao-seedance-1-0-lite-t2v-250428",
                "model": purpose,
                # "service_tier": "flex",
                "generate_audio": False,

                "content": [
                    {
                        "type": "text",
                        "text": "无人机以极快速度穿越复杂障碍或自然奇观，带来沉浸式飞行体验  --resolution 480p  --duration 4 --camerafixed false"
                    }
                ]
            }
            headers = {
                'Authorization': f'Bearer {api_key}',
                'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
                'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, json=payload)
            logger.debug(response.json())

            if "not activated" in str(response.json()): return False

            response.raise_for_status()

            return True

        elif purpose and purpose.startswith(("doubao-seed")):
            response = await client.images.generate(
                model=purpose,
                prompt="鱼眼镜头，一只猫咪的头部，画面呈现出猫咪的五官因为拍摄方式扭曲的效果。",
                size="1024x1024",
                response_format="url"
            )
            logger.debug(response.json())
            return True

        elif purpose == "ModelNotOpen":
            model = "doubao-seed-1-6-flash-250828"
            response = await client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": "hi"}],
                max_tokens=1
            )
            return False

        else:
            model = "kimi-k2-thinking-251104"
            response = await client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": "hi"}],
                max_tokens=1
            )
            # logger.debug(response)
            return True
    except TimeoutException as e:
        raise

    except Exception as e:
        logger.error(f"Error: {e}\n{api_key}")

        # if purpose == "ModelNotOpen" and "not activated" in str(e):
        #     return False

        return False


@rcache(ttl=15 * 60, skip_cache_func=skip_cache_func)
async def check_token_for_volc_with_cache(api_key, threshold: float = 1, purpose: Optional[str] = None):
    return await check_token_for_volc(api_key, threshold=threshold, purpose=purpose)


@retrying()
async def check_token_for_zhipu(api_key, threshold: float = 1, resource_package_name: str = "glm-4.5-flash"):
    if not isinstance(api_key, str):
        return await check_tokens(
            api_key,
            partial(check_token_for_zhipu, threshold=threshold, resource_package_name=resource_package_name)
        )
    try:

        if not resource_package_name.startswith("glm-"):
            client = AsyncOpenAI(base_url="https://bigmodel.cn/api/biz/tokenAccounts/list", api_key=api_key)

            data = await client.get("", cast_to=object)
            logger.debug(bjson(data))
            # print(str(data))
            # if """glm-4.5""" not in str(data): return False

            # "resourcePackageName": "【新用户专享】200万通用模型资源包",
            # "resourcePackageName": "【新用户专享】400次图像、视频生成、搜索工具次包",
            # "resourcePackageName": "【新用户专享】200万通用模型资源包",
            # "resourcePackageName": "【新用户专享】200万GLM-Z1-Air推理资源包",
            # "resourcePackageName": "【新用户专享】30次Vidu系列视频生成次包",
            for d in data["rows"]:
                if resource_package_name.lower() in d["resourcePackageName"].lower() and d['status'] != "EXPIRED":
                    logger.debug(bjson(d))
                    return d["tokenBalance"] >= threshold
        else:
            client = AsyncOpenAI(base_url="https://open.bigmodel.cn/api/paas/v4", api_key=api_key)

            response = await client.chat.completions.create(
                model=resource_package_name,
                messages=[{"role": "user", "content": "嗨"}],
                max_tokens=3
            )
            logger.debug(response)
            return True



    except TimeoutException as e:
        raise

    except Exception as e:
        logger.error(f"Error: {e}\n{api_key}")
        return False


@retrying()
# @rcache(ttl=1 * 24 * 3600, skip_cache_func=skip_cache_func)
async def check_token_for_fal(api_key, threshold: float = 0):
    if not isinstance(api_key, str):
        return await check_tokens(api_key, check_token_for_fal)
    try:
        # data = await AsyncClient(key=token).upload(b'', '', '')
        from fal_client.client import AsyncClient
        data = await AsyncClient(key=api_key).run(
            "fal-ai/any-llm/enterprise",
            arguments={
                "model": "meta-llama/llama-3.2-1b-instruct",
                "prompt": "1+1=",
                "max_tokens": 1,
            },
        )
        # fal - ai / any - llm / enterprise
        logger.debug(data)
        return True

    except TimeoutException as e:
        raise

    except Exception as exc:
        logger.error(exc)
        return False


@retrying()
@rcache(ttl=1 * 24 * 3600, skip_cache_func=skip_cache_func)
async def check_token_for_gitee(api_key, threshold: float = 1):
    if not isinstance(api_key, str):
        return await check_tokens(api_key, check_token_for_volc)

    try:
        base_url = "https://ai.gitee.com/v1"
        client = AsyncOpenAI(base_url=base_url, api_key=api_key)
        _ = await client.embeddings.create(
            model="Qwen3-Embedding-0.6B",
            input="hi"
        )
        return True
    except TimeoutException as e:
        raise

    except Exception as e:
        logger.error(f"Error: {e}\n{api_key}")
        return False


@retrying()
# @rcache(ttl=1 * 24 * 3600, skip_cache_func=skip_cache_func)
async def check_token_for_openrouter(api_key, threshold: float = 1):
    if not isinstance(api_key, str):
        return await check_tokens(api_key, check_token_for_openrouter)

    try:
        # {"data": {"total_credits": 215.00205323, "total_usage": 215.20147321775545}} %
        client = AsyncOpenAI(base_url=os.getenv("OPENROUTER_BASE_URL"), api_key=api_key)
        data = await client.get("/credits", cast_to=object)
        # logger.debug(data)
        # data = await client.get("/models/user", cast_to=object)
        # logger.debug(bjson(data))

        #
        # logger.debug(bjson(data))

        return True
    except TimeoutException as e:
        raise

    except Exception as e:
        logger.error(f"Error: {e}\n{api_key}")
        return False


async def get_valid_token_for_fal(feishu_url: Optional[str] = None):
    feishu_url = feishu_url or "https://xchatllm.feishu.cn/sheets/Z59Js10DbhT8wdt72LachSDlnlf?sheet=iFRwmM"
    _ = await get_next_token(feishu_url, check_token_for_fal, ttl=600)
    logger.debug(_)
    return _


@retrying()
async def check_token_for_runware(api_key, threshold: float = 5):
    base_url = "https://api.runware.ai/v1"
    if not isinstance(api_key, str):
        return await check_tokens(api_key, partial(check_token_for_runware, threshold=threshold))

    payload = [
        {
            "taskType": "accountManagement",
            "taskUUID": str(uuid.uuid4()),
            "operation": "getDetails"
        }
    ]
    try:
        client = AsyncOpenAI(base_url=base_url, api_key=api_key)
        data = await client.post(
            "/",
            body=payload,
            cast_to=object
        )
        balance = data['data'][0]['balance']
        logger.debug(balance)

        if threshold < 0:
            return balance < - threshold

        return balance >= threshold

    except TimeoutException as e:
        raise

    except Exception as e:
        logger.error(f"Error: {e}\n{api_key}")
        return False


@retrying()
async def check_token_for_aimlapi(api_key, threshold: float = 10000):
    base_url = "https://billing.aimlapi.com/v1"
    if not isinstance(api_key, str):
        return await check_tokens(api_key, check_token_for_aimlapi)

    try:
        client = AsyncOpenAI(base_url=base_url, api_key=api_key)
        data = await client.get("/billing/balance", cast_to=object)
        logger.debug(bjson(data))

        return data['balance'] > threshold

    except TimeoutException as e:
        raise

    except Exception as e:
        logger.error(f"Error: {e}\n{api_key}")
        return False


@retrying()
async def check_token_for_aimlapi(api_key, threshold: float = 10000):
    base_url = "https://billing.aimlapi.com/v1"
    if not isinstance(api_key, str):
        return await check_tokens(api_key, check_token_for_aimlapi)

    try:
        client = AsyncOpenAI(base_url=base_url, api_key=api_key)
        data = await client.get("/billing/balance", cast_to=object)
        logger.debug(bjson(data))

        return data['balance'] > threshold

    except TimeoutException as e:
        raise

    except Exception as e:
        logger.error(f"Error: {e}\n{api_key}")
        return False


@retrying()
async def check_token_for_aiping(api_key, threshold: float = 0):
    base_url = "https://aiping.cn/api/v1"
    if not isinstance(api_key, str):
        return await check_tokens(
            api_key,
            partial(check_token_for_aiping, threshold=threshold)
        )

    try:
        client = AsyncOpenAI(base_url=base_url, api_key=api_key)
        data = await client.get("/user/remain/points", cast_to=object)
        logger.debug(bjson(data))

        return data['data']['total_remain'] > threshold

    except TimeoutException as e:
        raise

    except Exception as e:
        logger.error(f"Error: {e}\n{api_key}")
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

    # arun(check_token_for_volc(["827b41d2-7e8c-46e2-9854-0720ca1bd2e4"]))
    # r = arun(check_token_for_volc_with_cache(["1"]))

    # arun(check_token_for_volc("5f211bf8-3f7d-4c68-9346-ca103f9e6862"))
    # arun(check_token_for_volc_with_cache("c53afe3c-ea60-4d87-a676-ccd49d26da2c"))
    # arun(check_token_for_volc("76e3bf6d-ac4b-4fce-bbc3-90bef9ff0c30", purpose='seedance'))
    # arun(check_token_for_volc("16ccf1b7-b42c-4f86-81d8-48c5864eaaf0"))

    # arun(check_token_for_ppinfra("sk_mCb5sRGTi6GXkSRp5F679Rbs0V_Hfee3p85lccGXCOo"))

    # arun(check_token_for_zhipu(api_key="e130b903ab684d4fad0d35e411162e99.PqyXq4QBjfTdhyCh"))

    # arun(check_token_for_fal("f0283d1c-864c-41b1-9fcb-1d853d7db9d9:8266d413f11252c96a02e7d9507474db"))

    # arun(check_token_for_ppinfra("sk_4Ja29OIUBVwKo5GWx-PRTsRcTyxxRjZDpYxSdPg75QU", threshold=18000))

    # arun(check_token_for_gitee("NWVXUPI38OQVXZGOEL3D23I9YUQWZPV23GVVBW1X"))

    # arun(get_valid_token_for_fal())

    # api_key = "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"
    # # api_key = None
    # arun(check_token_for_openrouter(api_key=api_key or os.getenv("OPENROUTER_API_KEY")))

    # api_key = "P8nkXmMKfoPlSR3iR48Jbl4vs8aLP1TT"

    # arun(check_token_for_runware(api_key))

    api_key = "603051fc1d7e49e19de2c67521d4a30e"
    # api_key = "f63aeefc6db54ba1ad51166ef5e4ab5f"
    # api_key="0b42a4a4019b4123a80b715f968fdaf6"

    # arun(check_token_for_aimlapi(api_key))
    # api_key="12a23dae-5d7e-41c5-b624-16fc0d682da1"
    # api_key = os.getenv("MODELSCOPE_API_KEY")
    # arun(check_token_for_modelscope(api_key))

    api_key = "QC-bf5cc6f65c2cf7dc1c9cfa03c55b21e3-5aaaa10f8720eac3713b64ee58919941"
    arun(check_token_for_aiping(api_key=api_key))


