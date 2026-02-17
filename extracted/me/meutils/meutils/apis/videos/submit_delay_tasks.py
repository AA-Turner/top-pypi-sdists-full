#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : run_delay_tasks
# @Time         : 2026/2/16 13:39
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

from meutils.db.redis_db import redis_aclient
from meutils.apis.volcengine_apis import videos_nx
from meutils.schemas.video_types import SoraVideoRequest, Video

from meutils.apis.videos.videos import OpenAIVideos  # todo

from meutils.apis.oneapi.tasks import get_tasks

base_url = 'delay'


async def create(api_key: Optional[str] = None):
    remote_task_ids = []

    task_ids = await get_tasks(platform="", channel_id="21496", status="UNFINISHED", return_ids=True,
                               end_timestamp=int(time.time()))

    task_ids = [i for i in task_ids if i.startswith("request:")]
    logger.debug(f"任务数量: {len(task_ids)}")

    if not api_key: return task_ids

    for task_id in task_ids:
        if request := await redis_aclient.get(task_id):
            request = SoraVideoRequest.model_validate_json(request)

            # 创建任务
            # if any(i in str(e) for i in ["NotLogin", "QuotaExceeded"]):
            video = await OpenAIVideos(api_key, base_url).create(request)
            remote_task_ids.append(video.id)

    return remote_task_ids


async def get(task_id, api_key: Optional[str] = None):
    if isinstance(task_id, list):
        return asyncio.gather(*map(get, task_id))

    # 获取任务
    if api_key:
        video = await OpenAIVideos(api_key, base_url).get(task_id)
        if video.status in ["completed", "failed"]:  # 监听 写入 redis
            await redis_aclient.set(f"response:{task_id}", video.model_dump_json(exclude_none=True), ex=3600)
    else:
        video = Video(id=task_id, status="failed")

        await redis_aclient.set(f"response:{task_id}", video.model_dump_json(), ex=3600)


if __name__ == '__main__':
    api_key = None
    api_key = "ve_doc_history=82379%2C6269%2C6256%2C85128%2C86081%2C6348%2C85621%2C6260;_qimei_fingerprint=806c1f7b65af4e75c90d884b4816e760;hasUserBehavior=1;monitor_huoshan_web_id=7467761534115284489;referrer_title=;AccountID=2119312619;user_locale=zh;signin_i18next=zh;monitor_session_id_flag=1;monitor_traceid_base_cookie=1452;volcengineLoginMethod=pwd;_tea_utm_cache_3569={%22utm_source%22:%22coopensrc%22%2C%22utm_medium%22:%22github%22%2C%22utm_campaign%22:%22doubao%22%2C%22utm_term%22:%22project%22%2C%22utm_content%22:%22aidrawio%22};volcfe-uuid=0701f6f2-a611-4599-a2fc-57cb015ff828;userInfo=eyJhbGciOiJSUzI1NiIsImtpZCI6ImE5ZDM1YTQ4YmZiNDExZjA4OWMwMDAxNjNlMDcwOGJkIn0.eyJhY2NfaSI6MjExOTMxMjYxOSwiYXVkIjpbImNvbnNvbGUudm9sY2VuZ2luZS5jb20iXSwiZXhwIjoxNzczODE1OTk3LCJpIjoiNGY0MWQzODUwYjAyMTFmMWE5ODkzNDM2YWMxMjA1OTAiLCJpZF9uIjoiNjE4M-aJi-acuueUqOaItyNDcU1BZXUiLCJtc2ciOm51bGwsInBpZCI6IjBmNDc0NzQwLWY5OGMtNGE3MS1hZDRmLTdiYTYwMGJhNGJjYiIsInNzX24iOiI2MTgz5omL5py655So5oi3I0NxTUFldSIsInQiOiJBY2NvdW50IiwidG9waWMiOiJzaWduaW5fdXNlcl9pbmZvIiwidmVyc2lvbiI6InYxIiwiemlwIjoiIn0.E71D2DPFNMxbUNDXj6Vo9Vc4_ueSJhcD_7isy0OGVMj4sLYu5br9eRioUykQgLvcdO5Qwkz4azm4B2QllWtfkL_aKqVwKM7Mt_6FN5X44xEQIdlxoT4nJMhntHHFqSU2MKx4ogk6Axg8CwMtf84_b-V5OuRdObkKjr5sxTQwynFpPm6RCCnPvurHxPhny7eOaQKXzRjyPBmnCjpxlo_pgk4BdTb0t2Y2XZjBfRybL4jkLTotdY2yY5cL_zmHIBUHOGKPpn3kZsfhTEydxpdyh0O-Xv2kLCMfDaQYxGd99ZMnWkYyxW3GpVdCApA6WO1W_04tRcITxVHm9g_-prDzdg;__tea_cache_tokens_3569={%22web_id%22:%227467761534115284489%22%2C%22user_unique_id%22:%227467761534115284489%22%2C%22timestamp%22:1771225171866%2C%22_type_%22:%22default%22};volc-design-locale=zh;_qimei_h38=94cee221b20e31b701a412450300000ce19c18;finance-hub-sdk-lang=zh;verify_mjjfj194_6wx9uxHT_RbvK_42dT_BQQF_Am4VHcR3e6qJ=1;p_c_check=1;volc_platform_clear_user_locale=1;__spti=11_000JnXNrWATPtPrMwlQ3ilQxfn2UtC;__sptiho=0B11_000JnXNrWATPtPrMwlQ3ilQxfn2UtC_bEv/KoxCOM4AcC;_qimei_i_1=7bfd468b9109058ec395ff62598426e3f6bca3f1130a0783b68b2d582593206c616364c03980b1dddefdeee2;_qimei_i_3=57ca79d3970c52d9c497aa625d8027e5a6bcf0f71a5b04d4e0872b502092276d32633f973989e28184b1;_qimei_uuid42=19c180a1723100cab20e31b701a4124555c551b916;_tea_utm_cache_520918={%22utm_source%22:%22coopensrc%22%2C%22utm_medium%22:%22github%22%2C%22utm_campaign%22:%22doubao%22%2C%22utm_term%22:%22project%22%2C%22utm_content%22:%22aidrawio%22};csrfToken=a08fbdda90f7660c1ef67ad04726c890;digest=eyJhbGciOiJSUzI1NiIsImtpZCI6ImE5ZDM1YTQ4YmZiNDExZjA4OWMwMDAxNjNlMDcwOGJkIn0.eyJhdWQiOlsiY29uc29sZS52b2xjZW5naW5lLmNvbSJdLCJleHAiOjE3NzEzOTY3OTcsImlhdCI6MTc3MTIyMzk5NywiaXNzIjoiaHR0cHM6Ly9zaWduaW4udm9sY2VuZ2luZS5jb20iLCJqdGkiOiIwZjQ3NDc0MC1mOThjLTRhNzEtYWQ0Zi03YmE2MDBiYTRiY2IiLCJtc2ciOiJINHNJQUFBQUFBQUMvK0tTNDJMeFM4eE5GZUl5TWpTME5EWTBNak8wbE5qKy9kUVpOb1c5SUZMSW40dmRNVGs1dnpTdlJPRDF5Uk9mMktYRXpRd3RqSjkxZGorYnMrdjVsQlhQT3JZck94ZjZPcWFXS29ITjBXSkx6cy9OemMvendxVU1FQUFBLy85N0pBUzFjUUFBQUE9PSIsIm5hbWUiOiI2MTgz5omL5py655So5oi3I0NxTUFldSIsInN1YiI6IjIxMTkzMTI2MTkiLCJ0b3BpYyI6InNpZ25pbl9jcmVkZW50aWFsIiwidHJuIjoidHJuOmlhbTo6MjExOTMxMjYxOTpyb290IiwidmVyc2lvbiI6InYxIiwiemlwIjoiZ3ppcCJ9.kpeqPNK8x34lsxPZVMRYRGQ_kcxzzXe3IL3Qxcrcanzcf2qbdS0E5zxap4jrZW1XjgopKw_w5m9EV-7RIDg_lDmetk1gZnEQ-X_aQ9Ducy1JNtna34zfhEfo1BWNpijW_q7ns6MYomxSpo0gzbBpxV54A02X4pFqXKhE1CB990rrBbtDa8D0abyTpT3imCTibxKTVHueDMJwZAJB9GA9SkuLSGjtJ9_YXmtBA4bK39xbuwKL6_HKDHltZ0Z_oLBu1OA2yzYDLffl_OgL3g7q9Ryo1jnZUM9a3zUhyd6VFvHuK3wSBIaWsJfRU3QzSFIhyzBM0BBQMREI5FShPl2TKg;gfkadpd=3569,42874|520918,36088;i18next=zh;isIntranet=0;login_scene=11;monitor_session_id=1869954474805973562;monitor_utm=%257B%2522utm_campaign%2522%253A%2522doubao%2522%252C%2522utm_content%2522%253A%2522aidrawio%2522%252C%2522utm_medium%2522%253A%2522github%2522%252C%2522utm_source%2522%253A%2522coopensrc%2522%252C%2522utm_term%2522%253A%2522project%2522%257D;s_v_web_id=verify_mjjfj194_6wx9uxHT_RbvK_42dT_BQQF_Am4VHcR3e6qJ;top_region=;user_locale=zh;vcloudWebId=0d8e34f9-2a27-4f3b-a86a-10cb562dbf67;VOLCFE_im_uuid=1770641165069598896"
    remote_task_ids = arun(create(api_key))


    # task_ids = "request:oZbBDx8JYBwhGfw7rmm5US"
    # arun(get(task_ids))
