#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : common
# @Time         : 2024/5/6 08:52
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : httpx重试 transport = httpx.AsyncHTTPTransport(retries=3) # response.raise_for_status()

from meutils.pipe import *
from meutils.caches import rcache

from meutils.decorators.retry import retrying
from meutils.decorators.contextmanagers import try_catcher
from meutils.notice.feishu import send_message
from meutils.db.redis_db import redis_client, redis_aclient
from typing import Optional, Union

from urllib.parse import urlparse, parse_qs

FEISHU_BASE_URL = "https://open.feishu.cn/open-apis/"


def get_app_access_token():
    payload = {
        "app_id": os.getenv("FEISHU_APP_ID", "cli_a60cfd9cad76100b"),
        "app_secret": os.getenv("FEISHU_APP_SECRET")
    }
    response = httpx.post(
        "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal",
        json=payload,
        timeout=30,
    )

    # logger.debug(response.json())

    return response.json().get("app_access_token")


@retrying(max_retries=3, predicate=lambda x: not x)
async def aget_app_access_token():
    """不加缓存，access_token会提前失效
    该报错是因为开发者本次调用过程中使用的 Tenant Access Token 已经失效或有误，飞书开放平台无法判断当前请求是否来自一个可信的用户，因此拦截了情况。
    :return:
    """
    payload = {
        "app_id": os.getenv("FEISHU_APP_ID"),
        "app_secret": os.getenv("FEISHU_APP_SECRET")
    }
    # logger.debug(payload)
    kwargs = {
        # "proxy": np.random.choice(["http://110.42.51.223:38443", None])
    }
    async with httpx.AsyncClient(base_url=FEISHU_BASE_URL, timeout=30, **kwargs) as client:
        response = await client.post("/auth/v3/app_access_token/internal", json=payload)

        return response.is_success and response.json().get("app_access_token")  # False / None


def get_spreadsheet_values(
        spreadsheet_token: Optional[str] = None,
        sheet_id: Optional[str] = None,
        feishu_url=None,
        to_dataframe: Optional[bool] = False
):
    if feishu_url and feishu_url.startswith("http"):
        parsed_url = urlparse(feishu_url)
        spreadsheet_token = parsed_url.path.split('/')[-1]
        sheet_id = parsed_url.query.split('=')[-1]

    url = f"https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/values/{sheet_id}"

    headers = {
        "Authorization": f"Bearer {get_app_access_token()}"
    }
    response = httpx.get(url, headers=headers, timeout=30)
    _ = response.json()
    return _ if not to_dataframe else pd.DataFrame(_.get('data').get('valueRange').get('values'))


@alru_cache(ttl=600)
@rcache(ttl=600, serializer='pickle')  # 缓存
async def aget_spreadsheet_values(
        spreadsheet_token: Optional[str] = None,
        sheet_id: Optional[str] = None,
        feishu_url: Optional[str] = None,
        to_dataframe: Optional[bool] = False
):
    if feishu_url and feishu_url.startswith("http"):
        parsed_url = urlparse(feishu_url)
        spreadsheet_token = parsed_url.path.split('/')[-1]
        sheet_id = parsed_url.query.split('=')[-1]

    access_token = await aget_app_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    async with httpx.AsyncClient(base_url=FEISHU_BASE_URL, timeout=30, headers=headers) as client:
        response = await client.get(f"/sheets/v2/spreadsheets/{spreadsheet_token}/values/{sheet_id}")
        if response.is_success:
            data = response.json()
            if to_dataframe:
                # values = data.get('data').get('valueRange').get('values')
                # [value | xmap(lambda x: x['text']) | xjoin('') for value in values]

                return pd.DataFrame(data.get('data').get('valueRange').get('values'))
            return data
        else:
            send_message(
                f"{response.status_code}\n\n{access_token}\n\n{response.text}",
                '飞书为啥为none: 已经去掉缓存了'
            )
            return get_spreadsheet_values(spreadsheet_token, sheet_id, feishu_url, to_dataframe)


async def spreadsheet_values_append(
        spreadsheet_token: Optional[str] = None,
        sheet_id: Optional[str] = None,
        feishu_url=None,
        range: Optional[str] = None,
        values: Optional[list] = None
):
    """ https://open.feishu.cn/document/server-docs/docs/sheets-v3/data-operation/append-data

        https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/:spreadsheetToken/values_prepend
        https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/:spreadsheetToken/values_append
        https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/:spreadsheetToken/values_image

    :param spreadsheet_token:
    :param sheet_id:
    :param feishu_url:
    :param values:
    :return:
    """

    if feishu_url and feishu_url.startswith("http"):
        parsed_url = urlparse(feishu_url)
        spreadsheet_token = parsed_url.path.split('/')[-1]
        sheet_id = parsed_url.query.split('=')[-1]

    access_token = await aget_app_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; charset=utf-8",

    }
    payload = {
        "valueRange": {
            # https://open.feishu.cn/document/server-docs/docs/sheets-v3/overview
            # "range": f"{sheet_id}!A:B",  # <sheetId>!<开始列>:<结束列>
            # "range": f"{sheet_id}!A1:E3",  # <sheetId>!<开始单元格>:<结束列>
            # "range": f"{sheet_id}",  # 非空的最大行列范围内的数据

            "range": f"{sheet_id}!{range}" if range else sheet_id,
            "values": values
        }
    }

    async with httpx.AsyncClient(base_url=FEISHU_BASE_URL, timeout=30, headers=headers) as client:
        # 默认覆盖 ?insertDataOption=OVERWRITE
        response = await client.post(f"/sheets/v2/spreadsheets/{spreadsheet_token}/values_append", json=payload)
        return response.is_success and response.json() or response.text


def create_document(title: str = "一篇新文档🔥", folder_token: Optional[str] = None):
    payload = {
        "title": title,
        "folder_token": folder_token,
    }

    url = "https://open.feishu.cn/open-apis/docx/v1/documents"
    headers = {
        "Authorization": f"Bearer {get_app_access_token()}"
    }
    response = httpx.post(url, headers=headers, timeout=30, json=payload)
    return response.json()


def get_doc_raw_content(document_id: str = "BxlwdZhbyoyftZx7xFbcGCZ8nah"):
    url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{document_id}/raw_content"
    headers = {
        "Authorization": f"Bearer {get_app_access_token()}"
    }
    response = httpx.get(url, headers=headers, timeout=30)
    return response.json()


async def get_next_from_redis(redis_key):
    if api_key := await redis_aclient.lpop(redis_key):
        await redis_aclient.rpush(redis_key, api_key)
        return api_key


async def get_next_token(
        feishu_url,
        check_token: Optional[Callable] = None,
        min_points: float = 0,  # vidu min_points=4
        ttl: Optional[int] = None,
):
    for i in range(10):  # 避免死循环
        if i > 5:
            send_message(f"重复同步了{i}次\n\n{feishu_url}", title="更新tokens")

        if token := await redis_aclient.lpop(feishu_url):
            token = token.decode()

            if check_token is None:
                logger.info("写回队列「跳过核验」")

                await redis_aclient.rpush(feishu_url, token)
                return token
            elif await check_token(token, threshold=min_points):
                logger.info("写回队列「大于最小消耗」")

                await redis_aclient.rpush(feishu_url, token)
                return token
            elif await check_token(token):
                logger.info("不写回队列「最后一次消耗」")

                return token

            logger.info("不写回队列「积分不够」")

        else:  # 更新tokens到redis
            df = await aget_spreadsheet_values(feishu_url=feishu_url, to_dataframe=True)
            # api_keys = [k for k in df[0] if isinstance(k, str)]  # 过滤空值, 避免 list： 一般超链接造成的
            api_keys = []
            for api_key in df[0]:
                if api_key:
                    if isinstance(api_key, str):
                        api_keys.append(api_key)
                    else:
                        api_key = "".join(map(lambda x: x.get('text', ""), api_key))
                        api_keys.append(api_key)

            # 初始化
            if check_token:
                bools = await asyncio.gather(*map(check_token, api_keys))  # todo: 提前过滤一遍, 减少初始化次数
                api_keys = list(itertools.compress(api_keys, bools))

            if not api_keys:  # 全部失效
                logger.debug(f"全部无效：{feishu_url}")
                break

            await redis_aclient.delete(feishu_url)
            num = await redis_aclient.rpush(feishu_url, *api_keys)

            send_message(f"新增：{num}\n\n{feishu_url}", title="更新tokens")

            if ttl:
                await redis_aclient.expire(feishu_url, ttl)  # Redis 的 RPUSH 命令本身不支持直接设置过期时间


async def get_next_token_for_polling(
        feishu_url,
        check_token: Optional[Callable] = None,
        max_size: Optional[int] = 10,
        from_redis: Optional[bool] = False,
        min_points: float = 0
):
    if from_redis:
        return await get_next_token(feishu_url, check_token, ttl=7 * 24 * 3600, min_points=min_points)

        # 轮询
    max_size = max_size or 10000
    df = await aget_spreadsheet_values(feishu_url=feishu_url, to_dataframe=True)

    api_keys = []
    for api_key in df[0]:
        if api_key:
            if isinstance(api_key, str):
                api_keys.append(api_key)
            else:
                logger.debug("feishu表格数据: 非字符串")
                api_key = "".join(map(lambda x: x.get('text', ""), api_key))
                api_keys.append(api_key)

    api_keys = np.random.choice(api_keys, size=min(max_size, len(api_keys)))

    num = len(api_keys)
    logger.debug(f"重复数：{num - len(set(list(api_keys)))}")

    if check_token:
        with try_catcher("CHECK_TOKEN"):
            tasks = map(check_token, api_keys)
            api_keys = [k for k, v in zip(api_keys, await asyncio.gather(*tasks)) if v]

            prob = len(api_keys) / num
            logger.debug(f"过滤前：{num} 过滤后：{len(api_keys)}，存活率：{prob:.2%}")
            if prob < 0.3:
                send_message(f"存活率 ≤ {prob}，及时更新", title=__name__)  # todo: 提醒

    return np.random.choice(api_keys)


@alru_cache(ttl=3600)
async def get_dataframe(iloc_tuple: Optional[tuple] = None, feishu_url: Optional[str] = None, ):  # 系统配置
    feishu_url = feishu_url or "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=bl4jYm"
    df = await aget_spreadsheet_values(feishu_url=feishu_url, to_dataframe=True)

    if iloc_tuple:
        return df.iloc._getitem_tuple(iloc_tuple)  # df.iloc._getitem_tuple((0, 1))
    return df


async def get_series(feishu_url: str, index: int = 0, duplicated: bool = False):  # 系统配置
    df = await aget_spreadsheet_values(feishu_url=feishu_url, to_dataframe=True)
    series = df[index]
    values = [i for i in series if i]  # todo: 非标准字符串处理
    if duplicated:  # 有序去重
        values = values | xUnique

    return values


if __name__ == '__main__':
    # print(get_app_access_token())
    # print(get_spreadsheet_values("Qy6OszlkIhwjRatkaOecdZhOnmh", "0f8eb3"))
    # pprint(get_spreadsheet_values("Bmjtst2f6hfMqFttbhLcdfRJnNf", "Y9oalh"))
    # pd.DataFrame(
    #     get_spreadsheet_values("Bmjtst2f6hfMqFttbhLcdfRJnNf", "79272d").get('data').get('valueRange').get('values'))

    # print(get_doc_raw_content("TAEFdXmzyobvgUxKM3lcLfc2nxe"))
    # print(create_document())
    # "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=79272d"

    # r = get_spreadsheet_values(feishu_url="https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=79272d",
    #                            to_dataframe=True)
    # print(list(filter(None, r[0])))
    # print(get_spreadsheet_values("Bmjtst2f6hfMqFttbhLcdfRJnNf", "79272d"))

    print(arun(aget_app_access_token()))
    # df = arun(aget_spreadsheet_values(
    #     feishu_url="https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=5i64gO",
    #     to_dataframe=True
    #
    # ))
    # print(df)

    from inspect import iscoroutinefunction

    # print(filter(lambda x: x and x.strip(), df[0]) | xlist)

    # func = aget_app_access_token()

    # print(alru_cache(ttl=300)(sync_to_async(aget_app_access_token))())

    # for i in tqdm(range(10)):
    #     # print(aget_app_access_token())
    #     print(arun(aget_app_access_token()))
    #     # print(get_app_access_token())

    # values = [
    #     [
    #         "2023/12/25",
    #         "收入",
    #         "微信",
    #         "100",
    #         "帐号 老表max"
    #     ],
    #     [
    #         "2023/12/25",
    #         "支出",
    #         "支付宝",
    #         "10",
    #         "买东西 老表max"
    #     ],
    #     [
    #         "2023/12/26",
    #         "支出",
    #         "支付宝",
    #         "19.9",
    #         "买东西 老表max"
    #     ],
    # ]
    #
    # _ = spreadsheet_values_append(
    #     feishu_url="https://xchatllm.feishu.cn/sheets/BPxjsmNj7hZr7Ytwk9uccvOKn6Z?sheet=7ce4e3",
    #
    #     range="A1:E3",
    #     values=values
    #
    # )
    #
    # print(arun(_))
    #
    # print(create_document())
    # arun(get_dataframe(iloc_tuple=(1, 0)))
    # feishu_url = "https://xchatllm.feishu.cn/sheets/GYCHsvI4qhnDPNtI4VPcdw2knEd?sheet=EYgZ8c"
    # feishu_url = "https://xchatllm.feishu.cn/sheets/GYCHsvI4qhnDPNtI4VPcdw2knEd?sheet=V84y6z"
    # with timer():
    #     token = arun(get_next_token(feishu_url))

    # FEISHU_URL = "https://xchatllm.feishu.cn/sheets/XfjqszII3hZAEvtTOgecOgv2nye?sheet=c14b34"
    # print(arun(get_series(FEISHU_URL)))
