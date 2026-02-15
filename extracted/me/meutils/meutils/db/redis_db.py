#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : redis
# @Time         : 2024/3/26 11:21
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
# from meutils.pipe import *

import os
from redis import Redis, ConnectionPool
from redis.asyncio import Redis as AsyncRedis, ConnectionPool as AsyncConnectionPool
from meutils.request_utils.ip import get_myip

REDIS_NAME = "REDIS_URL" if get_myip() else "OVERSEAS_REDIS_URL"  # 自动判断海外

kwargs = dict(
    # --- 关键配置：保活与自动恢复 ---

    # [最大连接数] 防止高并发下创建过多连接把 Redis 撑爆
    # 异步环境下，协程数可能远大于连接数，这个限制很有必要
    max_connections=1024,

    # [健康检查] 关键参数！
    # 获取连接时，如果连接空闲超过 30 秒，发送 PING 检查。
    # 如果 PING 失败，自动回收坏连接并创建新连接。
    health_check_interval=30,

    # [TCP 保活] 操作系统层面的 Keepalive，防止僵尸连接
    socket_keepalive=True,

    # [连接超时] 建立 TCP 连接的最大等待时间
    socket_connect_timeout=5,

    # [读写超时] (可选) 防止网络卡死导致协程一直挂起
    # socket_timeout=2.0
)

if REDIS_URL := os.getenv(REDIS_NAME) or os.getenv("REDIS_URL"):  # 默认国内
    # logger.debug(REDIS_URL)

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

    # redis_client.get("sora")

    api_key = "volc_platform_clear_user_locale=1; p_c_check=1; vcloudWebId=9e9d3005-3692-4a5a-a46d-1566df974868; user_locale=zh; monitor_huoshan_web_id=8861308256730147452; monitor_session_id_flag=1; volc-design-locale=zh; login_scene=11; volcengineLoginMethod=pwd; __spti=11_000J3JIXW12PtPrMwlQ3ilQxfn2UtC; __sptiho=7F11_000J3JIXW12PtPrMwlQ3ilQxfn2UtC_bEv/KoxCOM4AcC; __spti=11_000J3JIXW12PtPrMwlQ3ilQxfn2UtC; __sptiho=7F11_000J3JIXW12PtPrMwlQ3ilQxfn2UtC_bEv/KoxCOM4AcC; finance-hub-sdk-lang=zh; i18next=zh; s_v_web_id=verify_ml5bnfec_o579jXU9_eFa6_4ZIz_99Xg_epAghEE6DzaY; ve_doc_history=6256; isIntranet=0; VOLCFE_im_uuid=1770823408338649820; gfkadpd=3569,42874|520918,36088; monitor_session_id=1700628337432992243; monitor_traceid_base_cookie=22; verify_ml5bnfec_o579jXU9_eFa6_4ZIz_99Xg_epAghEE6DzaY=1; digest=eyJhbGciOiJSUzI1NiIsImtpZCI6ImE5ZDM1YTQ4YmZiNDExZjA4OWMwMDAxNjNlMDcwOGJkIn0.eyJhdWQiOlsiY29uc29sZS52b2xjZW5naW5lLmNvbSJdLCJleHAiOjE3NzEyMDc4NTYsImlhdCI6MTc3MTAzNTA1NiwiaXNzIjoiaHR0cHM6Ly9zaWduaW4udm9sY2VuZ2luZS5jb20iLCJqdGkiOiJiOGJkMzE3Yi01YTg2LTRhN2UtYjFhYS1jODU5MGY0MGYwZGUiLCJtc2ciOiJINHNJQUFBQUFBQUMvK0tTNDJMeFM4eE5GZUl5TWpTd05EY3hOakl4bDFpd2VmOFpOb1VOSUZMSW40dmRNVGs1dnpTdlJLRC9ZTU03ZGlseEV3c2p3MmVkM2MvbTdIbytaY1d6anUzS3BWRjVKU0hGU21CenROaVM4M056OC9POGNDa0RCQUFBLy8vSkoxbWFjUUFBQUE9PSIsIm5hbWUiOiI0ODIx5omL5py655So5oi3I3VabnRUcyIsInN1YiI6IjIxMDk3NDMyNDciLCJ0b3BpYyI6InNpZ25pbl9jcmVkZW50aWFsIiwidHJuIjoidHJuOmlhbTo6MjEwOTc0MzI0Nzpyb290IiwidmVyc2lvbiI6InYxIiwiemlwIjoiZ3ppcCJ9.Q2yl-BUu_LMSsGV4aPtwdXhPbHI_tscGCpwhjWCj0sJxii75qehGN7W0bshbBl3xDKgTU0p-ZLv4PkU8uKdYESCFafmK11aeIpVewThl2A_c_vp3GbmSKwR9HHvnyTNVcLRVcC-09tfqVBOHpHZkuJoUbyOU4jzUJ0OEAtpV2Sj3FTm8CDQEeFAq410RLPrnRM2kl0Jzh_e30FJWoLy5YHGm4MtjpqcmYqUBq-OCeT7KbuS-9cpw5r1jmPJpPq7y56m564te8-sDJu57pRiTux3V_r8Gs3U3iRJzUlMZZ-LYWyN_pVJyS2Zu7VWGkBdWm1WPN2IQCXA3nxTxLzVLvQ; digest=eyJhbGciOiJSUzI1NiIsImtpZCI6ImE5ZDM1YTQ4YmZiNDExZjA4OWMwMDAxNjNlMDcwOGJkIn0.eyJhdWQiOlsiY29uc29sZS52b2xjZW5naW5lLmNvbSJdLCJleHAiOjE3NzEyMDc4NTYsImlhdCI6MTc3MTAzNTA1NiwiaXNzIjoiaHR0cHM6Ly9zaWduaW4udm9sY2VuZ2luZS5jb20iLCJqdGkiOiJiOGJkMzE3Yi01YTg2LTRhN2UtYjFhYS1jODU5MGY0MGYwZGUiLCJtc2ciOiJINHNJQUFBQUFBQUMvK0tTNDJMeFM4eE5GZUl5TWpTd05EY3hOakl4bDFpd2VmOFpOb1VOSUZMSW40dmRNVGs1dnpTdlJLRC9ZTU03ZGlseEV3c2p3MmVkM2MvbTdIbytaY1d6anUzS3BWRjVKU0hGU21CenROaVM4M056OC9POGNDa0RCQUFBLy8vSkoxbWFjUUFBQUE9PSIsIm5hbWUiOiI0ODIx5omL5py655So5oi3I3VabnRUcyIsInN1YiI6IjIxMDk3NDMyNDciLCJ0b3BpYyI6InNpZ25pbl9jcmVkZW50aWFsIiwidHJuIjoidHJuOmlhbTo6MjEwOTc0MzI0Nzpyb290IiwidmVyc2lvbiI6InYxIiwiemlwIjoiZ3ppcCJ9.Q2yl-BUu_LMSsGV4aPtwdXhPbHI_tscGCpwhjWCj0sJxii75qehGN7W0bshbBl3xDKgTU0p-ZLv4PkU8uKdYESCFafmK11aeIpVewThl2A_c_vp3GbmSKwR9HHvnyTNVcLRVcC-09tfqVBOHpHZkuJoUbyOU4jzUJ0OEAtpV2Sj3FTm8CDQEeFAq410RLPrnRM2kl0Jzh_e30FJWoLy5YHGm4MtjpqcmYqUBq-OCeT7KbuS-9cpw5r1jmPJpPq7y56m564te8-sDJu57pRiTux3V_r8Gs3U3iRJzUlMZZ-LYWyN_pVJyS2Zu7VWGkBdWm1WPN2IQCXA3nxTxLzVLvQ; AccountID=2109743247; AccountID=2109743247; userInfo=eyJhbGciOiJSUzI1NiIsImtpZCI6ImE5ZDM1YTQ4YmZiNDExZjA4OWMwMDAxNjNlMDcwOGJkIn0.eyJhY2NfaSI6MjEwOTc0MzI0NywiYXVkIjpbImNvbnNvbGUudm9sY2VuZ2luZS5jb20iXSwiZXhwIjoxNzczNjI3MDU2LCJpIjoiNjViYjU2ODkwOTRhMTFmMTgyZjczNDM2YWMxMjAwZDUiLCJpZF9uIjoiNDgyMeaJi-acuueUqOaItyN1Wm50VHMiLCJtc2ciOm51bGwsInBpZCI6ImI4YmQzMTdiLTVhODYtNGE3ZS1iMWFhLWM4NTkwZjQwZjBkZSIsInNzX24iOiI0ODIx5omL5py655So5oi3I3VabnRUcyIsInQiOiJBY2NvdW50IiwidG9waWMiOiJzaWduaW5fdXNlcl9pbmZvIiwidmVyc2lvbiI6InYxIiwiemlwIjoiIn0.YvcmTBC8noujEglgqAI0DCpw6m8e95WSREw0Ia6h7wmV7LjvkQYojLyhG-Z4YWonH5PBJL9YSNTi6Vv4uabb4QkmzV9tdqsUhOuh4tLd__2B9Ectc86fW7BLr87Y3iOicdyRcMoW3M0xf7Zy3Nu6P9wNyAPCccdN4TWmOePLJmmp7OjJY9axGdV41wg2MgL1o_kWAPHJ5tQq4e7SpLWj8Xu25zNUBoH5X7hv6icTADAabwj-quL4It-u5bxhVg9hK17lHMiXZlTvGhQfp6Y_nX_hUl_AQ3EBHLP-jrlMRjjc3-2U4OD29gHJqlaPEVGqQ8Nf5XiiXv_-GQbW73Wf6g; csrfToken=c17ddde3a843471d8e15b96d9ca31d8e; csrfToken=c17ddde3a843471d8e15b96d9ca31d8e; __tea_cache_tokens_3569={%22web_id%22:%227602288869463918123%22%2C%22user_unique_id%22:%227602288869463918123%22%2C%22timestamp%22:1771035057618%2C%22_type_%22:%22default%22}"
    api_key = "monitor_huoshan_web_id=1103721958171764557; i18next=zh; volcfe-uuid=fa216a73-440b-4276-948a-428ebf17bf5b; connect.sid=s%3A1a0e396c-53bc-483f-9dcb-505a17592539.zbX3SGrTAcR9I5%2BKZCIfouz%2B1YH1Ih9fnEtsViMLSAk; connect.sid=s%3A1a0e396c-53bc-483f-9dcb-505a17592539.zbX3SGrTAcR9I5%2BKZCIfouz%2B1YH1Ih9fnEtsViMLSAk; volc_platform_clear_user_locale=1; p_c_check=1; vcloudWebId=794ce10e-a200-4010-aaa2-9463cb09b0f6; user_locale=zh; monitor_session_id=9364100436495974741; monitor_session_id_flag=1; volc-design-locale=zh; isIntranet=0; s_v_web_id=verify_mllorwgx_iDQfRmNw_icyg_42mA_9O5h_5Y5wyImZCbO4; VOLCFE_im_uuid=1771035442133049694; monitor_traceid_base_cookie=1; verify_mllorwgx_iDQfRmNw_icyg_42mA_9O5h_5Y5wyImZCbO4=1; digest=eyJhbGciOiJSUzI1NiIsImtpZCI6ImE5ZDM1YTQ4YmZiNDExZjA4OWMwMDAxNjNlMDcwOGJkIn0.eyJhdWQiOlsiY29uc29sZS52b2xjZW5naW5lLmNvbSJdLCJleHAiOjE3NzEyMDgyNjIsImlhdCI6MTc3MTAzNTQ2MiwiaXNzIjoiaHR0cHM6Ly9zaWduaW4udm9sY2VuZ2luZS5jb20iLCJqdGkiOiIwMzI0MWQ4Yy01OTFiLTRjYzctYjUxZi0xZTJhNThhNTdmM2YiLCJtc2ciOiJINHNJQUFBQUFBQUMvK0tTNDJMeFM4eE5GZUl5TWpTd05EZXhORFF3a2RpNGJmOFpOb1ZqSUZMSW40dmRNVGs1dnpTdlJPRER1NFozN0ZMaVpvWkdGczg2dTUvTjJmVjh5b3BuSGR1VjA3S3lQSU9qbE1EbWFMRWw1K2ZtNXVkNTRWSUdDQUFBLy85cEtkT0NjUUFBQUE9PSIsIm5hbWUiOiI2MTI45omL5py655So5oi3I2ZqaklTWiIsInN1YiI6IjIxMDk3NDkxMDQiLCJ0b3BpYyI6InNpZ25pbl9jcmVkZW50aWFsIiwidHJuIjoidHJuOmlhbTo6MjEwOTc0OTEwNDpyb290IiwidmVyc2lvbiI6InYxIiwiemlwIjoiZ3ppcCJ9.iu3Z7sa-fMdMgmBYHHjU9A4TDB1h5Ua6i0XaumQJw9VD--ze63I94AN6e8dd4pyQP3Z8kgA1q1aIoOz0Bv1F7RQt0_1jWf4H2D_Qz2FzjtRyjZJh217yLtMPnyFD8Cv4rUziP4jWSbLGRlQICFeEUfJAu4qSkYJnlhG8i7bTVg8f8jlIJMtdOjOdiey29qjp9f0_8HoxsPpsLSW-R1Im8QQ8GTgVPjpHRwbn4q2eJk33fli8yx2SycXQMD50XjgA_Kjnq1UX4KnEDL06aoimXxlQuuVsJjls8Or-yp7Wovn08iw4QbE_qo9viOPbfisfV1EnxJwyzRFdB_C0wUWWig; digest=eyJhbGciOiJSUzI1NiIsImtpZCI6ImE5ZDM1YTQ4YmZiNDExZjA4OWMwMDAxNjNlMDcwOGJkIn0.eyJhdWQiOlsiY29uc29sZS52b2xjZW5naW5lLmNvbSJdLCJleHAiOjE3NzEyMDgyNjIsImlhdCI6MTc3MTAzNTQ2MiwiaXNzIjoiaHR0cHM6Ly9zaWduaW4udm9sY2VuZ2luZS5jb20iLCJqdGkiOiIwMzI0MWQ4Yy01OTFiLTRjYzctYjUxZi0xZTJhNThhNTdmM2YiLCJtc2ciOiJINHNJQUFBQUFBQUMvK0tTNDJMeFM4eE5GZUl5TWpTd05EZXhORFF3a2RpNGJmOFpOb1ZqSUZMSW40dmRNVGs1dnpTdlJPRER1NFozN0ZMaVpvWkdGczg2dTUvTjJmVjh5b3BuSGR1VjA3S3lQSU9qbE1EbWFMRWw1K2ZtNXVkNTRWSUdDQUFBLy85cEtkT0NjUUFBQUE9PSIsIm5hbWUiOiI2MTI45omL5py655So5oi3I2ZqaklTWiIsInN1YiI6IjIxMDk3NDkxMDQiLCJ0b3BpYyI6InNpZ25pbl9jcmVkZW50aWFsIiwidHJuIjoidHJuOmlhbTo6MjEwOTc0OTEwNDpyb290IiwidmVyc2lvbiI6InYxIiwiemlwIjoiZ3ppcCJ9.iu3Z7sa-fMdMgmBYHHjU9A4TDB1h5Ua6i0XaumQJw9VD--ze63I94AN6e8dd4pyQP3Z8kgA1q1aIoOz0Bv1F7RQt0_1jWf4H2D_Qz2FzjtRyjZJh217yLtMPnyFD8Cv4rUziP4jWSbLGRlQICFeEUfJAu4qSkYJnlhG8i7bTVg8f8jlIJMtdOjOdiey29qjp9f0_8HoxsPpsLSW-R1Im8QQ8GTgVPjpHRwbn4q2eJk33fli8yx2SycXQMD50XjgA_Kjnq1UX4KnEDL06aoimXxlQuuVsJjls8Or-yp7Wovn08iw4QbE_qo9viOPbfisfV1EnxJwyzRFdB_C0wUWWig; AccountID=2109749104; AccountID=2109749104; userInfo=eyJhbGciOiJSUzI1NiIsImtpZCI6ImE5YzBkZmFjYmZiNDExZjA4OWMwMDAxNjNlMDcwOGJkIn0.eyJhY2NfaSI6MjEwOTc0OTEwNCwiYXVkIjpbImNvbnNvbGUudm9sY2VuZ2luZS5jb20iXSwiZXhwIjoxNzczNjI3NDYyLCJpIjoiNTdhYThjNjAwOTRiMTFmMWE3YTEzNDM2YWMxMjAxMWYiLCJpZF9uIjoiNjEyOOaJi-acuueUqOaItyNmampJU1oiLCJtc2ciOm51bGwsInBpZCI6IjAzMjQxZDhjLTU5MWItNGNjNy1iNTFmLTFlMmE1OGE1N2YzZiIsInNzX24iOiI2MTI45omL5py655So5oi3I2ZqaklTWiIsInQiOiJBY2NvdW50IiwidG9waWMiOiJzaWduaW5fdXNlcl9pbmZvIiwidmVyc2lvbiI6InYxIiwiemlwIjoiIn0.TKvUytDLabxktts9JfeloFjJrcYGo89ZEFSU5npHe24qPkKMIAVoxSag1mZCjeMOINblKruD7XaGq1k_t9rwfQsdW0gN1gUGH_haxlOhVoBgv5nwEjz596EW5QmDGGNdFxtKx1rcTv_7zBNfscntGJeFdzyY5gr1tqLJf8OFhKpd0EgheTKzf3PyN6wBXaRJ1kTGKBqedC9Vr8t2Ti4ll8znOWmF-D5WyIJpDhnE0x8YLfOLOxrV08LT1x8_kRRWCrliB40q17gWHvYf_vSHJ_NJ96GEf6-BqXBg-77J6XWMchQiTFmypMSbDv4IejIQUB6q0ZFxR1-1kDClzEWy1g; login_scene=11; volcengineLoginMethod=pwd; csrfToken=b9b23f35da9791e6c0f44d6ac0e95551; csrfToken=b9b23f35da9791e6c0f44d6ac0e95551; gfkadpd=520918,36088; __tea_cache_tokens_3569={%22web_id%22:%227606539240382678591%22%2C%22user_unique_id%22:%227606539240382678591%22%2C%22timestamp%22:1771035463604%2C%22_type_%22:%22default%22}"