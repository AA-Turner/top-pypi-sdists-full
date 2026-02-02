#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : check_api_key
# @Time         : 2024/6/17 08:42
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *


@alru_cache()
async def check(api_key_or_token, check_url):
    headers = {
        "Authorization": f"Bearer {api_key_or_token}",
        "Accept": "application/json"
    }
    payload = {
        "token": api_key_or_token
    }
    try:
        async with httpx.AsyncClient(headers=headers, timeout=60) as client:

            if api_key_or_token.startswith("ey"):

                response: httpx.Response = await client.post(check_url, json=payload)  # free-api: POST /token/check
            else:
                response: httpx.Response = await client.get(check_url)

            # todo: 可扩展

            logger.debug(response.text)
            logger.debug(response.status_code)

            return (
                    response.is_success
                    and response.json().get("is_available")  # deepseek
                    or response.json().get("status", False)  # moonshot、siliconflow
                    or response.json().get("live", False)  # free-api: POST /token/check
            )

    except httpx.RequestError as exc:
        logger.error(exc)
        return False


async def check_api_key_or_token(
        api_keys: Union[str, List[str]],
        check_url: Optional[str] = "https://api.deepseek.com/user/balance",
        return_api_keys: bool = True
):
    """
        {
        "is_available": false,
        "balance_infos": [
            {
                "currency": "CNY",
                "total_balance": "-0.00",
                "granted_balance": "0.00",
                "topped_up_balance": "-0.00"
            }
        ]
        }
    """
    if isinstance(api_keys, str):
        api_keys = [api_keys]

    if not check_url: return api_keys

    tasks = map(partial(check, check_url=check_url), tqdm(api_keys))
    responses = await asyncio.gather(*tasks, return_exceptions=True)
    # responses = await asyncio.gather(*tasks)
    if return_api_keys:
        responses = [k for k, v in zip(api_keys, responses) if v is True]

    return responses




if __name__ == '__main__':
    from meutils.config_utils.lark_utils import get_spreadsheet_values, get_next_token_for_polling

    #
    # api_keys = get_spreadsheet_values(feishu_url="https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=lVghgx", to_dataframe=True)[0].tolist()
    # print(arun(check_deepseek_api_key(api_keys)))

    # api_keys = os.getenv("DEEPSEEK_API_KEY")
    #
    # # arun(check_api_key_or_token(api_keys))
    #
    # # print(arun(check_deepseek_api_key(api_keys)))
    # # print(arun(check('sk-f42b2fdc036247e79cd471ab63b1142d', "https://api.deepseek.com/user/balance")))
    #
    # api_keys = os.getenv("SILICONFLOW_API_KEY").split()
    # for api_key in api_keys:
    #     arun(check(api_key, "https://api.siliconflow.cn/v1/user/info"))

    # api_keys = get_spreadsheet_values(feishu_url="https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=EOZuBW", to_dataframe=True)[0].tolist()

    # kimi
    api_keys = get_spreadsheet_values(feishu_url="https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=Y7HVfo", to_dataframe=True)[0].tolist()
    l = []
    for api_key in api_keys:
        if api_key:
            if arun(check(api_key, "https://all.chatfire.cn/kimi/token/check")):
                l.append(api_key)

    print('\n'.join(l))