#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : redis
# @Time         : 2024/3/26 11:21
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
from meutils.pipe import *

from redis import Redis, ConnectionPool
from redis.asyncio import Redis as AsyncRedis, ConnectionPool as AsyncConnectionPool

from meutils.request_utils.ip import get_myip

REDIS_NAME = "REDIS_URL" if get_myip() else "OVERSEAS_REDIS_URL"  # 自动判断海外

kwargs = dict(
    # --- 关键配置：保活与自动恢复 ---

    # [最大连接数] 防止高并发下创建过多连接把 Redis 撑爆
    # 异步环境下，协程数可能远大于连接数，这个限制很有必要
    max_connections=128,

    # [健康检查] 关键参数！
    # 获取连接时，如果连接空闲超过 30 秒，发送 PING 检查。
    # 如果 PING 失败，自动回收坏连接并创建新连接。
    health_check_interval=25,

    # [TCP 保活] 操作系统层面的 Keepalive，防止僵尸连接
    socket_keepalive=True,

    # [连接超时] 建立 TCP 连接的最大等待时间
    socket_connect_timeout=5,

    # 断线重连
    retry_on_timeout=True,
    # retry_on_error=[ConnectionError, TimeoutError],
    # retry=Retry(ExponentialBackoff(cap=2, base=0.1), 3),  # 最多重试3次
)

if REDIS_URL := os.getenv(REDIS_NAME) or os.getenv("REDIS_URL"):  # 默认国内
    logger.debug(REDIS_URL)

    pool = ConnectionPool.from_url(REDIS_URL, **kwargs)
    redis_client = Redis.from_pool(pool)

    async_pool = AsyncConnectionPool.from_url(REDIS_URL, **kwargs)
    redis_aclient = AsyncRedis.from_pool(async_pool)
    # redis_client = Redis.from_url(REDIS_URL, **kwargs)
    # redis_aclient = AsyncRedis.from_url(REDIS_URL, **kwargs)

else:
    redis_client = Redis(**kwargs)  # decode_responses=True
    redis_aclient = AsyncRedis(**kwargs)


async def sadd(name, *values, ttl: int = 0):
    await redis_aclient.sadd(name, *values)

    if ttl:
        await redis_aclient.expire(name, ttl)


if __name__ == '__main__':
    # from meutils.pipe import *

    # print(arun(redis_aclient.get("")))
    # print(redis_client.lrange("https://api.moonshot.cn/v1",0, -1))

    # print(redis_client.lrange("https://api.deepseek.com/v1",0, -1))
    # print(redis_client.exists("https://api.deepseek.com/v1"))

    # print(type(redis_aclient.get("test")))

    # print(redis_client.delete("https://api.deepseek.com/v1"))
    feishu_url = "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=79272d"
    feishu_url = "https://xchatllm.feishu.cn/sheets/GYCHsvI4qhnDPNtI4VPcdw2knEd?sheet=EYgZ8c"

    # with timer():
    #     print(feishu_url in redis_client)
    #
    # with timer():
    #     redis_client.exists(feishu_url)
    # with timer():
    #     print(redis_client.llen(feishu_url))

    # print(redis_client.set('a', 'xx21212'))
    # print(redis_client.set('b', b'xx21212'))
    #
    # print(redis_client.get('a'))
    # print(redis_client.get('b'))

    #
    # print(redis_client.type(feishu))
    # _ = redis_client.lrange(feishu, 0, -1)
    # print(len(eval(_)))

    task_id = "celery-task-meta-ca94c602-a2cc-4db5-afe4-763f30df8a18"

    # arun(redis_aclient.get('celery-task-meta-72d59447-1f88-4727-8067-8244c2268faa'))
    #
    # arun(redis_aclient.select(1))

    # async def main():
    #     r = await redis_aclient.select(1)
    #     return await redis_aclient.get(task_id)
    #
    #
    # arun(main())

    # async def main():
    #     return await redis_aclient.lpop("redis_key")

    # arun(main())

    # r = redis_client.sadd('set1', 'a', 'b', 'c')
    # r = redis_client.sadd('set1', 'd')
    # k="meutils.config_utils.lark_utils.commonaget_spreadsheet_values()[(＇feishu_url＇, ＇https://xchatllm.feishu.cn/sheets/GYCHsvI4qhnDPNtI4VPcdw2knEd?sheet=Gvm9dt＇), (＇to_dataframe＇, True)]	"
    # redis_client.delete(k)
    # print(redis_client.get('test'))

    # print(redis_client.delete("k"))

    # print(type(redis_client.type('pods').decode()))
    # print(redis_client.get('xxsadasd').decode())

    # redis_client.set("pods", "10.219.11.231 114.66.55.228")

    # for i in ["cgt-20260227134919-t68t8",]
    from meutils.apis.oneapi.tasks import get_tasks

    cookie = "ve_doc_history=84458%2C82379%2C6737%2C6269%2C6256%2C85128%2C86081%2C6348%2C85621%2C6260;_qimei_fingerprint=efbb885a22f7d4e5589008c28bc8e7ba;hasUserBehavior=1;monitor_huoshan_web_id=7467761534115284489;referrer_title=%E6%A8%A1%E5%9E%8B%E8%B4%B9%E7%94%A8--%E6%89%A3%E5%AD%90-%E7%81%AB%E5%B1%B1%E5%BC%95%E6%93%8E;AccountID=2119872855;user_locale=zh;signin_i18next=zh;monitor_session_id_flag=1;monitor_traceid_base_cookie=1526;volcengineLoginMethod=pwd;_tea_utm_cache_3569={%22utm_source%22:%22coopensrc%22%2C%22utm_medium%22:%22github%22%2C%22utm_campaign%22:%22doubao%22%2C%22utm_term%22:%22project%22%2C%22utm_content%22:%22aidrawio%22};volcfe-uuid=0701f6f2-a611-4599-a2fc-57cb015ff828;userInfo=eyJhbGciOiJSUzI1NiIsImtpZCI6ImE5ZDM1YTQ4YmZiNDExZjA4OWMwMDAxNjNlMDcwOGJkIn0.eyJhY2NfaSI6MjExOTg3Mjg1NSwiYXVkIjpbImNvbnNvbGUudm9sY2VuZ2luZS5jb20iXSwiZXhwIjoxNzc0Nzc2MTg5LCJpIjoiZWU4OGExY2QxM2JkMTFmMTg4ODIzNDM2YWMxMjAwYjEiLCJpZF9uIjoiOUdxIzNuI1VrNTgiLCJtc2ciOm51bGwsInBpZCI6ImZhYmRhNzEzLTQ2ZDItNGYwYy1hNGM2LWRkNTA4Njk0MTFiOSIsInNzX24iOiI5R3EjM24jVWs1OCIsInQiOiJBY2NvdW50IiwidG9waWMiOiJzaWduaW5fdXNlcl9pbmZvIiwidmVyc2lvbiI6InYxIiwiemlwIjoiIn0.fqSdE3Upi0nqi1o3Oau5qbZRaEzrDYOaX1cxC2nV53Zbdant-vCEIKX8PlnVE3uzs1RnX0uAKvq0oQNajnPSMWK08fBN6NthVxmpPnbgIeZ4lDG_V6EW1yC95qXCoefZN_4t-5M_fozxZaVRXqYSdXWLkmrnqHOzbWxx4TAn6qZHNdT364_Dt7226vGF1aamKxEE3JbGSSlCDSbZxY73zQDJphATulUgf4wYaleREqw5M2fgAErxA8uRZ3o0STnAr_jBE-RwWR1fo_PU_Ky5JO8_YmsrTYQAaF240DNtvxreB_X6iNqWuW44hjMJbLSXtraa2cXJtL1iou_s2Rn9hw;__tea_cache_tokens_3569={%22web_id%22:%227467761534115284489%22%2C%22user_unique_id%22:%227467761534115284489%22%2C%22timestamp%22:1772184191039%2C%22_type_%22:%22default%22};volc-design-locale=zh;_qimei_h38=94cee221b20e31b701a412450300000ce19c18;finance-hub-sdk-lang=zh;p_c_check=1;volc_platform_clear_user_locale=1;__spti=11_000JnXNrWATPtPrMwlQ3ilQxfn2UtC;__sptiho=0B11_000JnXNrWATPtPrMwlQ3ilQxfn2UtC_bEv/KoxCOM4AcC;_qimei_i_1=76d3738b9109058ec395ff62598426e3f6bca3f1130a0783b68b2d582593206c616364c03980b1ddde83ccd2;_qimei_i_3=57ca79d3970c52d9c497aa625d8027e5a6bcf0f71a5b04d4e0872b502092276d32633f973989e28184b1;_qimei_uuid42=19c180a1723100cab20e31b701a4124555c551b916;_tea_utm_cache_520918={%22utm_source%22:%22coopensrc%22%2C%22utm_medium%22:%22github%22%2C%22utm_campaign%22:%22doubao%22%2C%22utm_term%22:%22project%22%2C%22utm_content%22:%22aidrawio%22};csrfToken=552a2771ef2bd2065a71909f68ae3f95;digest=eyJhbGciOiJSUzI1NiIsImtpZCI6ImE5ZDM1YTQ4YmZiNDExZjA4OWMwMDAxNjNlMDcwOGJkIn0.eyJhdWQiOlsiY29uc29sZS52b2xjZW5naW5lLmNvbSJdLCJleHAiOjE3NzIzNTY5ODksImlhdCI6MTc3MjE4NDE4OSwiaXNzIjoiaHR0cHM6Ly9zaWduaW4udm9sY2VuZ2luZS5jb20iLCJqdGkiOiJmYWJkYTcxMy00NmQyLTRmMGMtYTRjNi1kZDUwODY5NDExYjkiLCJtc2ciOiJINHNJQUFBQUFBQUMvK0tTNTJMeFM4eE5GZUsyZEM5VU5zNVREczAydFpCNGNxVDFMSnZDWHhBcFpNN0Y3cGljbkYrYVZ5SncvZEdyVCt4U3lDcVZ3SnExMkpMemMzUHo4N3lRcFFBQkFBRC8vMzgwRkh4YUFBQUEiLCJuYW1lIjoiOUdxIzNuI1VrNTgiLCJzdWIiOiIyMTE5ODcyODU1IiwidG9waWMiOiJzaWduaW5fY3JlZGVudGlhbCIsInRybiI6InRybjppYW06OjIxMTk4NzI4NTU6cm9vdCIsInZlcnNpb24iOiJ2MSIsInppcCI6Imd6aXAifQ.IjYSlUVBHTMm2DblZD1M3n9X2TASeut2U-1eCva9kyeoOv0vUuxPK6x_SDw4ykGM0Ozs2lYRYSGIvS1-TRPpImCGjrkwGBIh45zWep3cAfsba36ssnE9CMjDBY8MMuu5VR0BTzIYL6RYnm2hOSvG-FQ2a4JjofqUdCXbB-hLteA635p6PpIZ9qUr4nHK-y2RexukOP4TmvIU57MeCw_15RbLi18oZQGbELNtOYP1Yhfc6pedkrCoZumdS1GPMxQVE7hTg6PlxxhATU_NsGbaSedh8MZbHZfb41z-at41E2AF1sp9PeYkTroB1iftaUf0rD1Xbwzq5k_Cwqbiad_3aQ;gfkadpd=3569,42874|520918,36088;i18next=zh;isIntranet=0;login_scene=11;monitor_session_id=9081223115845153279;monitor_utm=%257B%2522utm_campaign%2522%253A%2522doubao%2522%252C%2522utm_content%2522%253A%2522aidrawio%2522%252C%2522utm_medium%2522%253A%2522github%2522%252C%2522utm_source%2522%253A%2522coopensrc%2522%252C%2522utm_term%2522%253A%2522project%2522%257D;s_v_web_id=verify_mlxcna5b_OPnHmJyI_isi9_4Wph_AE1g_IryXIJgAqHFs;top_region=;vcloudWebId=0d8e34f9-2a27-4f3b-a86a-10cb562dbf67;VOLCFE_im_uuid=1771893239908012284"

    REDIS_URL = "redis://:chatfirechatfire@110.42.51.201:6379"
    async_pool = AsyncConnectionPool.from_url(REDIS_URL, **kwargs)
    _redis_aclient = AsyncRedis.from_pool(async_pool)

    async def main():
        # ids = await get_tasks("", channel_id="21464", status="UNFINISHED", return_ids=True)
        ids = ["s86datc4ndrmt0cwpb7ba7xycm", "h412gwj6nhrmt0cwp9arz3579m"]
        print(ids)

        for i in ids:
            # redis_client.set(i, cookie)
            _ = await _redis_aclient.get(i)
            await redis_aclient.set(i, _, ex=10000)


    # arun(main())
