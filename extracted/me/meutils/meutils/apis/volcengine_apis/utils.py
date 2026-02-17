#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : utils
# @Time         : 2026/2/12 16:53
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.io.files_utils import to_url, to_base64, to_bytes
from openai import AsyncOpenAI
from meutils.caches import rcache

"""
curl --location --request POST 'https://arkbff-cn-beijing.console.volcengine.com/api/2024-10-01/UploadArkTosFile' \
--header 'priority: u=1, i' \
--header 'Cookie: ve_doc_history=82379%2C6269%2C6256%2C85128%2C86081%2C6348%2C85621%2C6260;_qimei_fingerprint=dd38b822c43601e30b795b0bb06bc28b;hasUserBehavior=1;monitor_huoshan_web_id=7467761534115284489;referrer_title=%E5%88%9B%E5%BB%BA%E8%A7%86%E9%A2%91%E7%94%9F%E6%88%90%E4%BB%BB%E5%8A%A1%20API--%E7%81%AB%E5%B1%B1%E6%96%B9%E8%88%9F%E5%A4%A7%E6%A8%A1%E5%9E%8B%E6%9C%8D%E5%8A%A1%E5%B9%B3%E5%8F%B0-%E7%81%AB%E5%B1%B1%E5%BC%95%E6%93%8E;AccountID=2104716667;user_locale=zh;signin_i18next=zh;monitor_session_id_flag=1;monitor_traceid_base_cookie=1418;volcengineLoginMethod=pwd;_tea_utm_cache_3569={%22utm_source%22:%22coopensrc%22%2C%22utm_medium%22:%22github%22%2C%22utm_campaign%22:%22doubao%22%2C%22utm_term%22:%22project%22%2C%22utm_content%22:%22aidrawio%22};volcfe-uuid=0701f6f2-a611-4599-a2fc-57cb015ff828;userInfo=eyJhbGciOiJSUzI1NiIsImtpZCI6ImE5YzBkZmFjYmZiNDExZjA4OWMwMDAxNjNlMDcwOGJkIn0.eyJhY2NfaSI6MjEwNDcxNjY2NywiYXVkIjpbImNvbnNvbGUudm9sY2VuZ2luZS5jb20iXSwiZXhwIjoxNzczNDc3MzIxLCJpIjoiYzUxNTFmMzUwN2VkMTFmMTllYTUzNDM2YWMxMjAwYzciLCJpZF9uIjoiODQzMuaJi-acuueUqOaItyNaY1JzUnkiLCJtc2ciOm51bGwsInBpZCI6IjBkMDQ2ZDlkLTg4NTYtNDhiNy1iZGMzLWQ0OTI4ODQ3Njc2YiIsInNzX24iOiI4NDMy5omL5py655So5oi3I1pjUnNSeSIsInQiOiJBY2NvdW50IiwidG9waWMiOiJzaWduaW5fdXNlcl9pbmZvIiwidmVyc2lvbiI6InYxIiwiemlwIjoiIn0.gfVFCXMedtkYoGFpObMWKulX5QPrdSDadKKyxMl7TecUX4gxF53E4NaZjMfDruLDu7gIlIEhbLyUzMvOJtUFyVtP1VIZDXD1zOLf7T-nKO4WH4MEEHf6F-ERzjMabSQfotnaEeMyysjbetQJ38UEA6hF_C70zo-hv_sIKdMVMTqLt2J7Sf1ry0qNDGEMBQzOB6hNB5amF6NB9GByLZEl-RjovAbB3SkarTSpWLnekrUxyJXD-SIdN80kKOrnlugyMFCE_NPVuZ4ZFgTyKJt1o0Yp_-jb1GBJDUeY2Tq-vDjalIvT9q-PJE4MCw9Bb4VIkaVFfobO1sDiOocvu00gTg;__tea_cache_tokens_3569={%22web_id%22:%227467761534115284489%22%2C%22user_unique_id%22:%227467761534115284489%22%2C%22timestamp%22:1770885409545%2C%22_type_%22:%22default%22};volc-design-locale=zh;_qimei_h38=47aeffd76da9e4a25cf291fa0300000d619a11;finance-hub-sdk-lang=zh;p_c_check=1;volc_platform_clear_user_locale=1;__spti=11_000JnXNrWATPtPrMwlQ3ilQxfn2UtC;__sptiho=0B11_000JnXNrWATPtPrMwlQ3ilQxfn2UtC_bEv/KoxCOM4AcC;_qimei_i_1=5ac22586920b058d97c3f9360fd57ab5f3bfa6f4410d018bb5d979582593206c616363933980b3ddd790cf8f;_qimei_i_3=57ca79d3970c52d9c497aa625d8027e5a6bcf0f71a5b04d4e0872b502092276d32633f973989e28184b1;_qimei_uuid42=19c180a1723100cab20e31b701a4124555c551b916;_tea_utm_cache_520918={%22utm_source%22:%22coopensrc%22%2C%22utm_medium%22:%22github%22%2C%22utm_campaign%22:%22doubao%22%2C%22utm_term%22:%22project%22%2C%22utm_content%22:%22aidrawio%22};csrfToken=b6b2764fc8bf2869340ddeaa2d5b81ac;digest=eyJhbGciOiJSUzI1NiIsImtpZCI6ImE5YzBkZmFjYmZiNDExZjA4OWMwMDAxNjNlMDcwOGJkIn0.eyJhdWQiOlsiY29uc29sZS52b2xjZW5naW5lLmNvbSJdLCJleHAiOjE3NzEwNTgxMjEsImlhdCI6MTc3MDg4NTMyMSwiaXNzIjoiaHR0cHM6Ly9zaWduaW4udm9sY2VuZ2luZS5jb20iLCJqdGkiOiIwZDA0NmQ5ZC04ODU2LTQ4YjctYmRjMy1kNDkyODg0NzY3NmIiLCJtc2ciOiJINHNJQUFBQUFBQUMvK0tTNDJMeFM4eE5GZUl5TWpRd01UYzBNek16bHppMGNOc1pOb1dUSUZMSW40dmRNVGs1dnpTdlJPRDNyYk92MmFYRUxVeU1qWjUxZGorYnMrdjVsQlhQT3JZclJ5VUhGUWRWS29ITjBXSkx6cy9OemMvendxVU1FQUFBLy8vSzNjZTVjUUFBQUE9PSIsIm5hbWUiOiI4NDMy5omL5py655So5oi3I1pjUnNSeSIsInN1YiI6IjIxMDQ3MTY2NjciLCJ0b3BpYyI6InNpZ25pbl9jcmVkZW50aWFsIiwidHJuIjoidHJuOmlhbTo6MjEwNDcxNjY2Nzpyb290IiwidmVyc2lvbiI6InYxIiwiemlwIjoiZ3ppcCJ9.Z-eEz3F4-7zEBTycZtzF2L0DjTnNMvmWMai7yfbsbK4VAvzlw8l0XJ4qxzch9RcIZKvK_Hp_iKzitotsFQHQHhmElcF1l5X3CgGhB4bM4DHKbvU1Q8rwn2IqMZeVjPnVcaA9U6G9nCCYtmgdWfiilPO3EyC7Wirx7TBhRkW2IcFtZhO_Ft5IN25A7TVWioaWuRTqAlKUsFujENgx23uQ2VPhKx6q8_vp4vbmRC-vshFM2osYq-3o_shi3bKS-S-eZjLdOKqfRlY5qsf_SBDpv08yXVIntzGlHKAO1jzrBxwDRQZp5aDv4J6RYtoJKsyE9-ISbrb_p3BD4h2kbuIHQA;gfkadpd=520918,36088|3569,42874;i18next=zh;isIntranet=0;login_scene=11;monitor_session_id=0137731691764811011;monitor_utm=%257B%2522utm_campaign%2522%253A%2522doubao%2522%252C%2522utm_content%2522%253A%2522aidrawio%2522%252C%2522utm_medium%2522%253A%2522github%2522%252C%2522utm_source%2522%253A%2522coopensrc%2522%252C%2522utm_term%2522%253A%2522project%2522%257D;s_v_web_id=verify_mjjfj194_6wx9uxHT_RbvK_42dT_BQQF_Am4VHcR3e6qJ;top_region=;vcloudWebId=0d8e34f9-2a27-4f3b-a86a-10cb562dbf67;VOLCFE_im_uuid=1770641165069598896' \
--form 'file=@"/Users/betterme/Downloads/cat_2.png"' \
--form 'security="true"' \
--form 'type="image"' \
--form 'modelName="doubao-seedance-2-0"' \
--form 'modelVersion="260128"' \
--form 'biz="experience_video"'


{
    "ResponseMetadata": {
        "RequestId": "3c263fbd-458f-9e80-85d1-3f4c4d970f9e",
        "Action": "UploadArkTosFile",
        "Version": "2024-10-01",
        "Service": "ark",
        "Region": "cn-beijing"
    },
    "Result": {
        "Bucket": "ark-common-storage-prod-cn-beijing",
        "Prefix": "experience_video/2104716667/0/20260212/8bba9493-3867-449b-9384-6ec2054cacaa.png",
        "Token": "8uWFirGh9Uxyu7UanFFzvieV0Fu77XJjDMecXN7WwR5Xg8O-HQQKNW7GIILVthMKIitHDnZ0wnIbtOwtV_PHBOtBt_JU-eD7lcJ14uX4Rdg",
        "Url": "https://ark-common-storage-prod-cn-beijing.tos-cn-beijing.volces.com/experience_video/2104716667/0/20260212/8bba9493-3867-449b-9384-6ec2054cacaa.png?X-Tos-Algorithm=TOS4-HMAC-SHA256&X-Tos-Credential=AKLTMjgxMzUwNzliYzdlNDE4MTllYjJjZGVlOWQ3N2M1ZDY/20260212/cn-beijing/tos/request&X-Tos-Date=20260212T085325Z&X-Tos-Expires=604800&X-Tos-Signature=f07057c096ae56d09a0574162a37302a14f13853901e7721d1c42f34c50d02d6&X-Tos-SignedHeaders=host",
        "SecurityInfo": null,
        "FirstFramePrefix": "",
        "FirstFrameUrl": ""
    }
}
"""

# files = [
#     ('file', ('cat_2.png', open('/Users/betterme/Downloads/cat_2.png', 'rb'), 'image/png'))
# ]

base_url = "https://arkbff-cn-beijing.console.volcengine.com/api/2024-10-01"


# @rcache(ttl=300)
async def upload(file, api_key: str):
    if isinstance(file, list):
        return await asyncio.gather(*(upload(i, api_key) for i in file))

    if not file: return

    file_bytes = await to_bytes(file)
    files = [
        ('file', file_bytes),
        ('security', (None, 'true')),
        ('type', (None, 'image')),
        ('modelName', (None, 'doubao-seedance-2-0')),
        ('modelVersion', (None, '260128')),
        ('biz', (None, 'experience_video')),
    ]

    extra_headers = {
        "Content-Type": "multipart/form-data",
        "cookie": api_key
    }
    client = AsyncOpenAI(base_url=base_url, default_headers=extra_headers)
    response = await client.post("/UploadArkTosFile", files=files, cast_to=object)

    logger.debug(response)
    """
    {
        "BucketName": "ark-common-storage-prod-cn-beijing",
        "ObjectKey": "experience_video/2119812478/0/20260211/8097768e-a5ae-47a4-858a-09993f8a5213.jpg",
        "Url": "https://ark-common-storage-prod-cn-beijing.tos-cn-beijing.volces.com/experience_video/2119812478/0/20260211/8097768e-a5ae-47a4-858a-09993f8a5213.jpg?X-Tos-Algorithm=TOS4-HMAC-SHA256&X-Tos-Credential=AKLTMjgxMzUwNzliYzdlNDE4MTllYjJjZGVlOWQ3N2M1ZDY%2F20260211%2Fcn-beijing%2Ftos%2Frequest&X-Tos-Date=20260211T042107Z&X-Tos-Expires=604800&X-Tos-Signature=372556f8b7e9b97a895eebe14b6eee9ae02aca0d450bb8124a13864d90244304&X-Tos-SignedHeaders=host"
    }
    Bucket": "ark-common-storage-prod-cn-beijing",
        "Prefix": "experience_video/2104716667/0/20260212/a775536e-1df2-4e15-83fe-769178f57ebb.png",
        "Token": "8uWFirGh9Uxyu7UanFFzvieV0Fu77XJjDMecXN7WwR4rAUyHDgXnpIbAHzls24RQtou7ycXp_o-OCLy-R3T0VTkpvj2Bv31_w88N6vsB6Dc",
        "Url": "https://ark-common-storage-prod-cn-beijing.tos-cn-beijing.volces.com/experience_video/2104716667/0/20260212/a775536e-1df2-4e15-83fe-769178f57ebb.png?X-Tos-Algorithm=TOS4-HMAC-SHA256&X-Tos-Credential=AKLTMjgxMzUwNzliYzdlNDE4MTllYjJjZGVlOWQ3N2M1ZDY%2F20260212%2Fcn-beijing%2Ftos%2Frequest&X-Tos-Date=20260212T105101Z&X-Tos-Expires=604800&X-Tos-Signature=ea2c925bb9dd1e2153fbdbfe833fc32f67978c742de9eb1e8a2e03f32a91061f&X-Tos-SignedHeaders=host",
        "SecurityInfo": null,
        "FirstFramePrefix": "",
        "FirstFrameUrl": ""
    """
    if url := (response.get('Result') or {}).get('Url'):
        return {
            "BucketName": response['Result']['Bucket'],
            "ObjectKey": response['Result']['Prefix'],
            "Url": url
        }
    else:
        raise ValueError(f"Upload failed: {response}")


if __name__ == '__main__':
    api_key = """
volc_platform_clear_user_locale=1; p_c_check=1; vcloudWebId=c521e550-d06c-45f1-9285-4fbe8342eb89; user_locale=zh; monitor_huoshan_web_id=6202964249524884595; monitor_session_id_flag=1; volc-design-locale=zh; isIntranet=0; VOLCFE_im_uuid=1771005318779470069; login_scene=11; volcengineLoginMethod=pwd; i18next=zh; s_v_web_id=verify_mll6uvlz_MUc2o4xZ_44Xz_4xtY_9XHk_5xnWBhV8jRTv; __spti=11_000J3dBxOXvPtPrMwlQ3ilQxfn2UtC; __sptiho=4F11_000J3dBxOXvPtPrMwlQ3ilQxfn2UtC_bEv/KoxCOM4AcC; __spti=11_000J3dBxOXvPtPrMwlQ3ilQxfn2UtC; __sptiho=4F11_000J3dBxOXvPtPrMwlQ3ilQxfn2UtC_bEv/KoxCOM4AcC; finance-hub-sdk-lang=zh; gfkadpd=3569,42874|520918,36088; monitor_session_id=7399769837190435174; monitor_traceid_base_cookie=9; digest=eyJhbGciOiJSUzI1NiIsImtpZCI6ImE5ZDM1YTQ4YmZiNDExZjA4OWMwMDAxNjNlMDcwOGJkIn0.eyJhdWQiOlsiY29uc29sZS52b2xjZW5naW5lLmNvbSJdLCJleHAiOjE3NzEzOTkxNzAsImlhdCI6MTc3MTIyNjM3MCwiaXNzIjoiaHR0cHM6Ly9zaWduaW4udm9sY2VuZ2luZS5jb20iLCJqdGkiOiIxODkxNmQzMS05YTk3LTRiOTAtODJlZi0zOTBjOWQwZjlkNWIiLCJtc2ciOiJINHNJQUFBQUFBQUMvK0tTNDJMeFM4eE5GZUl5TWpRME5iWXdOVGEwbFBqYmVmb01tMEp6MStremJFTCtYT3lPeWNuNXBYa2xBcy9mMy9qQUxpVnViR0JrOEt5eis5bWNYYytuckhqV3NWMDVLTFhBc2RoWkNXeU9GbHR5Zm01dWZwNFhMbVdBQUFBQS8vLzNIU1FuY1FBQUFBPT0iLCJuYW1lIjoiMzAyMOaJi-acuueUqOaItyNSZXBBc0MiLCJzdWIiOiIyMTE1Mzg1MzE5IiwidG9waWMiOiJzaWduaW5fY3JlZGVudGlhbCIsInRybiI6InRybjppYW06OjIxMTUzODUzMTk6cm9vdCIsInZlcnNpb24iOiJ2MSIsInppcCI6Imd6aXAifQ.a2kW_5TgcD4_cPB9FpV6WtL01v5yZlzBnSXnS46Uyur8qt32S92crDJHk_eSDkdWFvIbBmEz8rxxS2qdS6Fy4BrFuXISRTllQFi6cMNHoEeRAxLDus356vTUYNltnZNSa6kdL45QPEMY-5-2CEi3t-ZiVOJTlucGtUkMPZfCMqpDZjm1fqC5x0vADNCa6beEtwDhDoxJbD4gqsdYFptXIkDwf72VK11-9ls3ueam0ne1dnFAXuVZqLTAPig_9KSoLfBa7NMmH4T8hwFus32lzPiBOoT2h7EOiJElfnP6o7tVWdJV6zIOhTD5gKigUCmxMsKELp4PJQIeufXDlzyx5A; digest=eyJhbGciOiJSUzI1NiIsImtpZCI6ImE5ZDM1YTQ4YmZiNDExZjA4OWMwMDAxNjNlMDcwOGJkIn0.eyJhdWQiOlsiY29uc29sZS52b2xjZW5naW5lLmNvbSJdLCJleHAiOjE3NzEzOTkxNzAsImlhdCI6MTc3MTIyNjM3MCwiaXNzIjoiaHR0cHM6Ly9zaWduaW4udm9sY2VuZ2luZS5jb20iLCJqdGkiOiIxODkxNmQzMS05YTk3LTRiOTAtODJlZi0zOTBjOWQwZjlkNWIiLCJtc2ciOiJINHNJQUFBQUFBQUMvK0tTNDJMeFM4eE5GZUl5TWpRME5iWXdOVGEwbFBqYmVmb01tMEp6MStremJFTCtYT3lPeWNuNXBYa2xBcy9mMy9qQUxpVnViR0JrOEt5eis5bWNYYytuckhqV3NWMDVLTFhBc2RoWkNXeU9GbHR5Zm01dWZwNFhMbVdBQUFBQS8vLzNIU1FuY1FBQUFBPT0iLCJuYW1lIjoiMzAyMOaJi-acuueUqOaItyNSZXBBc0MiLCJzdWIiOiIyMTE1Mzg1MzE5IiwidG9waWMiOiJzaWduaW5fY3JlZGVudGlhbCIsInRybiI6InRybjppYW06OjIxMTUzODUzMTk6cm9vdCIsInZlcnNpb24iOiJ2MSIsInppcCI6Imd6aXAifQ.a2kW_5TgcD4_cPB9FpV6WtL01v5yZlzBnSXnS46Uyur8qt32S92crDJHk_eSDkdWFvIbBmEz8rxxS2qdS6Fy4BrFuXISRTllQFi6cMNHoEeRAxLDus356vTUYNltnZNSa6kdL45QPEMY-5-2CEi3t-ZiVOJTlucGtUkMPZfCMqpDZjm1fqC5x0vADNCa6beEtwDhDoxJbD4gqsdYFptXIkDwf72VK11-9ls3ueam0ne1dnFAXuVZqLTAPig_9KSoLfBa7NMmH4T8hwFus32lzPiBOoT2h7EOiJElfnP6o7tVWdJV6zIOhTD5gKigUCmxMsKELp4PJQIeufXDlzyx5A; AccountID=2115385319; AccountID=2115385319; userInfo=eyJhbGciOiJSUzI1NiIsImtpZCI6ImE5YzBkZmFjYmZiNDExZjA4OWMwMDAxNjNlMDcwOGJkIn0.eyJhY2NfaSI6MjExNTM4NTMxOSwiYXVkIjpbImNvbnNvbGUudm9sY2VuZ2luZS5jb20iXSwiZXhwIjoxNzczODE4MzcwLCJpIjoiZDY0NGYzYWYwYjA3MTFmMTg5YmUzNDM2YWMxMjAwMmYiLCJpZF9uIjoiMzAyMOaJi-acuueUqOaItyNSZXBBc0MiLCJtc2ciOm51bGwsInBpZCI6IjE4OTE2ZDMxLTlhOTctNGI5MC04MmVmLTM5MGM5ZDBmOWQ1YiIsInNzX24iOiIzMDIw5omL5py655So5oi3I1JlcEFzQyIsInQiOiJBY2NvdW50IiwidG9waWMiOiJzaWduaW5fdXNlcl9pbmZvIiwidmVyc2lvbiI6InYxIiwiemlwIjoiIn0.uam5wLNffBCiTnTjLg3zsfkDEWHcnZi5p7pH1n-suxp8zsRKK7vrP9QGosyY11f7h8vrF0D9LfEVmp4BMQeIq_FjG4tVMUvVwIMqC0UZNuWA3N9bvhljafKQN2oSpRqvSW8zmDFaCGLj_uAya2lwI7YeKKNSjDxcuJmM9JXcjx0P5ztmbnbdPZ5OvyBZlYbaK01pd4o6XcaaFar_2igkL4Vw5kBhiE5LnKirZGtnKgFLRxsZiOHl6YdyW7oOnQQtOsyQ0PQ98t7OdCW4LzEPUDNmkX3m3h17xtjBw05adaEd5hvERreLnyiSdB0SavDUSJFnJo6TXItm6gYf6lu6KQ; csrfToken=bc6b79ed872be2ea4307428a60ae162f; csrfToken=bc6b79ed872be2ea4307428a60ae162f; user_locale=zh; __tea_cache_tokens_3569={%22web_id%22:%227606409831347963446%22%2C%22user_unique_id%22:%227606409831347963446%22%2C%22timestamp%22:1771226379481%2C%22_type_%22:%22default%22}
    """.strip()

    arun(upload(['https://cos.imyaigc.com/video/seedance/1ce61a50-2b2a-435a-8a01-0b0a4bc5ac2b.png'] * 2, api_key=api_key))
