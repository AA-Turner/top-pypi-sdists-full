#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : images_nx
# @Time         : 2026/2/13 11:16
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.schemas.image_types import ImageRequest, ImagesResponse
from meutils.apis.volcengine_apis.utils import upload

from openai import AsyncClient

BASE_URL = "https://ml-platform-api.console.volcengine.com/ark/bff/api/cn-beijing/2024"


async def generate(request: ImageRequest, api_key: Optional[str] = None):
    default_headers = {
        "x-csrf-token": api_key.split("csrfToken=")[1].split(';')[0],
        "Cookie": api_key
    }
    client = AsyncClient(base_url=BASE_URL, default_headers=default_headers)

    payload = {
        "From": "pc",
        "Model": "doubao-seedream-5-0",
        "EndpointId": "doubao-seedream-5-0-260128",
        "Type": "normal",
        # "Images": [
        #     {
        #         "BucketName": "ark-seedream-4",
        #         "ObjectKey": "ark-seedream-4",
        #         "Url": "https://lf3-static.bytednsdoc.com/obj/eden-cn/LM-STH-hahK/ljhwZthlaukjlkulzlp/ark/seedream/seedream-4-5-03-in-01.png"
        #     },
        #     {
        #         "BucketName": "ark-seedream-4",
        #         "ObjectKey": "ark-seedream-4",
        #         "Url": "https://lf3-static.bytednsdoc.com/obj/eden-cn/LM-STH-hahK/ljhwZthlaukjlkulzlp/ark/seedream/seedream-4-5-03-in-02.png"
        #     },
        #     {
        #         "BucketName": "ark-seedream-4",
        #         "ObjectKey": "ark-seedream-4",
        #         "Url": "https://lf3-static.bytednsdoc.com/obj/eden-cn/LM-STH-hahK/ljhwZthlaukjlkulzlp/ark/seedream/seedream-4-5-03-in-03.png"
        #     }
        # ],
        "Prompt": request.prompt,
        "Ratio": "adaptive",
        "Size": "2048x2048",
        "ImageCount": request.n,
        "Seed": -1,

        "Stream": False,
        "Watermark": False
    }
    if request.resolution or request.size:
        payload["Size"] = request.resolution or request.size


    if request.aspect_ratio:
        payload["Ratio"] = request.aspect_ratio

    if request.image_urls:
        payload["Images"] = await upload(request.image_urls, api_key)

    logger.debug(bjson(payload))
    response = await client.post("/CreateImageGeneration", body=payload, cast_to=object, stream=True)
    logger.debug(bjson(response))

    data = []
    async for chunk in response:
        logger.debug(chunk)
        if items := chunk.get("items", []):
            data += [{"url": item.get("Url") for item in items}]

    return ImagesResponse(data=data)


if __name__ == '__main__':
    api_key = """ve_doc_history=82379%2C6269%2C6256%2C85128%2C86081%2C6348%2C85621%2C6260;_qimei_fingerprint=dd38b822c43601e30b795b0bb06bc28b;hasUserBehavior=1;monitor_huoshan_web_id=7467761534115284489;referrer_title=%E5%88%9B%E5%BB%BA%E8%A7%86%E9%A2%91%E7%94%9F%E6%88%90%E4%BB%BB%E5%8A%A1%20API--%E7%81%AB%E5%B1%B1%E6%96%B9%E8%88%9F%E5%A4%A7%E6%A8%A1%E5%9E%8B%E6%9C%8D%E5%8A%A1%E5%B9%B3%E5%8F%B0-%E7%81%AB%E5%B1%B1%E5%BC%95%E6%93%8E;AccountID=2109091919;user_locale=zh;signin_i18next=zh;monitor_session_id_flag=1;monitor_traceid_base_cookie=1419;volcengineLoginMethod=pwd;_tea_utm_cache_3569={%22utm_source%22:%22coopensrc%22%2C%22utm_medium%22:%22github%22%2C%22utm_campaign%22:%22doubao%22%2C%22utm_term%22:%22project%22%2C%22utm_content%22:%22aidrawio%22};volcfe-uuid=0701f6f2-a611-4599-a2fc-57cb015ff828;userInfo=eyJhbGciOiJSUzI1NiIsImtpZCI6ImE5YzBkZmFjYmZiNDExZjA4OWMwMDAxNjNlMDcwOGJkIn0.eyJhY2NfaSI6MjEwOTA5MTkxOSwiYXVkIjpbImNvbnNvbGUudm9sY2VuZ2luZS5jb20iXSwiZXhwIjoxNzczNDk5Mzk0LCJpIjoiMjk2OTc3MmEwODIxMTFmMTlhZjEzNDM2YWMxMjAwM2YiLCJpZF9uIjoiMDQzNeaJi-acuueUqOaItyN5SFNrTXQiLCJtc2ciOm51bGwsInBpZCI6ImNkNDlmYTg3LWI3NzUtNDQwNS1iOTkzLTVmOTA0NTMyNDg5MSIsInNzX24iOiIwNDM15omL5py655So5oi3I3lIU2tNdCIsInQiOiJBY2NvdW50IiwidG9waWMiOiJzaWduaW5fdXNlcl9pbmZvIiwidmVyc2lvbiI6InYxIiwiemlwIjoiIn0.cdpiB9xgcokJBJzG-S_BIdllMusycBqNLL8VNEnmlFI5i0fYstJUbAvLC-nbouHZjLhX9XzT45RjIqbFa-f1dnQHE6SmMf_CCPuxoZOpd7UnJTbCqQiKO_KRkdshxpuIxx7mV74ziS3UQWcNARIH663BxmsMsPWFx7Tntx3QOCdu_zljgJkjbxJZhcBhGOqGC2CMZXocr0MorPpcEVtXPOsRi9ulCBMSSH4kI5z4iigbliLyoYcsD3vNCmGO_vTOPDAdyEwGE395FwAnlB62JGnwVAreHvdPLE3YFMBII2JdDT03TGOrb1VFP6tLj2xOAWCDlVJnxRkW2fDZ16d71Q;__tea_cache_tokens_3569={%22web_id%22:%227467761534115284489%22%2C%22user_unique_id%22:%227467761534115284489%22%2C%22timestamp%22:1770907429996%2C%22_type_%22:%22default%22};volc-design-locale=zh;_qimei_h38=94cee221b20e31b701a412450300000ce19c18;finance-hub-sdk-lang=zh;p_c_check=1;volc_platform_clear_user_locale=1;__spti=11_000JnXNrWATPtPrMwlQ3ilQxfn2UtC;__sptiho=0B11_000JnXNrWATPtPrMwlQ3ilQxfn2UtC_bEv/KoxCOM4AcC;_qimei_i_1=5eea2c8b9109058ec395ff62598426e3f6bca3f1130a0783b68b2d582593206c616364c03980b1ddde92f7cc;_qimei_i_3=57ca79d3970c52d9c497aa625d8027e5a6bcf0f71a5b04d4e0872b502092276d32633f973989e28184b1;_qimei_uuid42=19c180a1723100cab20e31b701a4124555c551b916;_tea_utm_cache_520918={%22utm_source%22:%22coopensrc%22%2C%22utm_medium%22:%22github%22%2C%22utm_campaign%22:%22doubao%22%2C%22utm_term%22:%22project%22%2C%22utm_content%22:%22aidrawio%22};csrfToken=499beb4542dac5d353afbb1fffd981eb;digest=eyJhbGciOiJSUzI1NiIsImtpZCI6ImE5ZDM1YTQ4YmZiNDExZjA4OWMwMDAxNjNlMDcwOGJkIn0.eyJhdWQiOlsiY29uc29sZS52b2xjZW5naW5lLmNvbSJdLCJleHAiOjE3NzEwODAxOTQsImlhdCI6MTc3MDkwNzM5NCwiaXNzIjoiaHR0cHM6Ly9zaWduaW4udm9sY2VuZ2luZS5jb20iLCJqdGkiOiJjZDQ5ZmE4Ny1iNzc1LTQ0MDUtYjk5My01ZjkwNDUzMjQ4OTEiLCJtc2ciOiJINHNJQUFBQUFBQUMvK0tTNDJMeFM4eE5GZUl5TWpTd05MQTB0RFMwbFBoNWR2c1pOb1dtYzl2UHNBbjVjN0U3SmlmbmwrYVZDSngvY09NdHU1UzRnWW14NmJQTzdtZHpkajJmc3VKWngzYmxTby9nYk44U0piQTVXbXpKK2JtNStYbGV1SlFCQWdBQS8vOTdrMG13Y1FBQUFBPT0iLCJuYW1lIjoiMDQzNeaJi-acuueUqOaItyN5SFNrTXQiLCJzdWIiOiIyMTA5MDkxOTE5IiwidG9waWMiOiJzaWduaW5fY3JlZGVudGlhbCIsInRybiI6InRybjppYW06OjIxMDkwOTE5MTk6cm9vdCIsInZlcnNpb24iOiJ2MSIsInppcCI6Imd6aXAifQ.fw4LobnAByUwIaCOWhOOvF5igRzIo_l5lBme2SmfeT5vwky01EI2iBDBayuv_O39Uvl-MzS5Gmg2-tXFN7tqEyH2ERa1ymuZETFkFu3P-su9Uqb1VZnFpkaZsjHzhCTWIxvwDLmBCZM0aLN_LOBjhDyoRjd6agYr8XLrTM3UzVRb-MUg_yYBBSttvUpZdM4pLQ3magTu0xJQY0OfLg4IBTezfg84XsQJkh0wGaJI1N-_aXTTXTFBOBahMS8fKJrNG-mgV52xMxBqS_pt3piGwn3ssMVeD5JD5K474FMKxIhgwJUkdePfsVACAjBhaLmV6AmYX4UXo7lTmjHHIZnp3Q;gfkadpd=520918,36088|3569,42874;i18next=zh;isIntranet=0;login_scene=11;monitor_session_id=0008375069127979375;monitor_tracing_cookie=[];monitor_utm=%257B%2522utm_campaign%2522%253A%2522doubao%2522%252C%2522utm_content%2522%253A%2522aidrawio%2522%252C%2522utm_medium%2522%253A%2522github%2522%252C%2522utm_source%2522%253A%2522coopensrc%2522%252C%2522utm_term%2522%253A%2522project%2522%257D;s_v_web_id=verify_mjjfj194_6wx9uxHT_RbvK_42dT_BQQF_Am4VHcR3e6qJ;top_region=;vcloudWebId=0d8e34f9-2a27-4f3b-a86a-10cb562dbf67;VOLCFE_im_uuid=1770641165069598896"""

    api_key = """vcloudWebId=628549cd-c3d3-4cb8-936e-1539cee70c5a; monitor_huoshan_web_id=1935614982602037754; monitor_session_id_flag=1; connect.sid=s%3Af8e672eb-e208-489f-8e0c-9a777c81136a.ARdtNAOSZ0LqN1l%2FJ7UvQy7QqPiMkqiVDF2OK2Ug2CE; connect.sid=s%3Af8e672eb-e208-489f-8e0c-9a777c81136a.ARdtNAOSZ0LqN1l%2FJ7UvQy7QqPiMkqiVDF2OK2Ug2CE; i18next=zh; volc-design-locale=zh; volc_platform_clear_user_locale=1; p_c_check=1; user_locale=zh; monitor_session_id=9612063839874964093; isIntranet=0; VOLCFE_im_uuid=1770961291284332747; monitor_traceid_base_cookie=2; digest=eyJhbGciOiJSUzI1NiIsImtpZCI6ImE5YzBkZmFjYmZiNDExZjA4OWMwMDAxNjNlMDcwOGJkIn0.eyJhdWQiOlsiY29uc29sZS52b2xjZW5naW5lLmNvbSJdLCJleHAiOjE3NzExMzQxMTUsImlhdCI6MTc3MDk2MTMxNSwiaXNzIjoiaHR0cHM6Ly9zaWduaW4udm9sY2VuZ2luZS5jb20iLCJqdGkiOiIwMzFjZWY1OC04N2IzLTQ3NTQtOTlkNi1lNDA4NDUzMWEwNmMiLCJtc2ciOiJINHNJQUFBQUFBQUMvK0tTNDJMeFM4eE5GZUl5TWpTd05MQTB0RFMwbEdqN3ZPc01tOEppRUNua3o4WHVtSnljWDVwWEluRCt3WTIzN0ZMaUJpYkdwczg2dTUvTjJmVjh5b3BuSGR1Vkt6MkNzMzFMbE1EbWFMRWw1K2ZtNXVkNTRWSUdDQUFBLy8vY0JpcE1jUUFBQUE9PSIsIm5hbWUiOiIwNDM15omL5py655So5oi3I3lIU2tNdCIsInN1YiI6IjIxMDkwOTE5MTkiLCJ0b3BpYyI6InNpZ25pbl9jcmVkZW50aWFsIiwidHJuIjoidHJuOmlhbTo6MjEwOTA5MTkxOTpyb290IiwidmVyc2lvbiI6InYxIiwiemlwIjoiZ3ppcCJ9.xLvOC-sKCi_a-wQuc-CkkN4D26G4Nf-R6O2oGPwYrUOSvyoxP-j_0Ms7qzKAGYE-_kHHnlk-DGji69INIAKsTUvJaesiCoreKJ-ObJfKp16eLiRCKZYceYnWgDHJBo9GdlNAYTuPj8GEb1pf1YAL-wBCFe4zrhrspQL0cV7UbAV0qEQBmpzN1I98I07a7tCT0zovJTq6WWHVjxborHEaN6LPB12vBJUjQOdtyYkOehBFSFI-JR-w-cidA-UFHhX3RyZeMxqFeF22XqlORzUp3uSbMwYPyf2-dQMAz1wC8E5Rt3-ymmHGgeeMEambLzVjlunruXuQD8IYLsaRcnT68w; digest=eyJhbGciOiJSUzI1NiIsImtpZCI6ImE5YzBkZmFjYmZiNDExZjA4OWMwMDAxNjNlMDcwOGJkIn0.eyJhdWQiOlsiY29uc29sZS52b2xjZW5naW5lLmNvbSJdLCJleHAiOjE3NzExMzQxMTUsImlhdCI6MTc3MDk2MTMxNSwiaXNzIjoiaHR0cHM6Ly9zaWduaW4udm9sY2VuZ2luZS5jb20iLCJqdGkiOiIwMzFjZWY1OC04N2IzLTQ3NTQtOTlkNi1lNDA4NDUzMWEwNmMiLCJtc2ciOiJINHNJQUFBQUFBQUMvK0tTNDJMeFM4eE5GZUl5TWpTd05MQTB0RFMwbEdqN3ZPc01tOEppRUNua3o4WHVtSnljWDVwWEluRCt3WTIzN0ZMaUJpYkdwczg2dTUvTjJmVjh5b3BuSGR1Vkt6MkNzMzFMbE1EbWFMRWw1K2ZtNXVkNTRWSUdDQUFBLy8vY0JpcE1jUUFBQUE9PSIsIm5hbWUiOiIwNDM15omL5py655So5oi3I3lIU2tNdCIsInN1YiI6IjIxMDkwOTE5MTkiLCJ0b3BpYyI6InNpZ25pbl9jcmVkZW50aWFsIiwidHJuIjoidHJuOmlhbTo6MjEwOTA5MTkxOTpyb290IiwidmVyc2lvbiI6InYxIiwiemlwIjoiZ3ppcCJ9.xLvOC-sKCi_a-wQuc-CkkN4D26G4Nf-R6O2oGPwYrUOSvyoxP-j_0Ms7qzKAGYE-_kHHnlk-DGji69INIAKsTUvJaesiCoreKJ-ObJfKp16eLiRCKZYceYnWgDHJBo9GdlNAYTuPj8GEb1pf1YAL-wBCFe4zrhrspQL0cV7UbAV0qEQBmpzN1I98I07a7tCT0zovJTq6WWHVjxborHEaN6LPB12vBJUjQOdtyYkOehBFSFI-JR-w-cidA-UFHhX3RyZeMxqFeF22XqlORzUp3uSbMwYPyf2-dQMAz1wC8E5Rt3-ymmHGgeeMEambLzVjlunruXuQD8IYLsaRcnT68w; AccountID=2109091919; AccountID=2109091919; userInfo=eyJhbGciOiJSUzI1NiIsImtpZCI6ImE5YzBkZmFjYmZiNDExZjA4OWMwMDAxNjNlMDcwOGJkIn0.eyJhY2NfaSI6MjEwOTA5MTkxOSwiYXVkIjpbImNvbnNvbGUudm9sY2VuZ2luZS5jb20iXSwiZXhwIjoxNzczNTUzMzE1LCJpIjoiYjRiNjJlYmUwODllMTFmMWFhZDUzNDM2YWMxMjAwZTkiLCJpZF9uIjoiMDQzNeaJi-acuueUqOaItyN5SFNrTXQiLCJtc2ciOm51bGwsInBpZCI6IjAzMWNlZjU4LTg3YjMtNDc1NC05OWQ2LWU0MDg0NTMxYTA2YyIsInNzX24iOiIwNDM15omL5py655So5oi3I3lIU2tNdCIsInQiOiJBY2NvdW50IiwidG9waWMiOiJzaWduaW5fdXNlcl9pbmZvIiwidmVyc2lvbiI6InYxIiwiemlwIjoiIn0.auz54eQxWqgK22fBNidnPyxOeL2BbGla5hMlUlxYFAuGkayZZsJaSk0MMMlDpoV3YNbK0T7Qegyt6-vY3O8j2oRBFzEy28rOeKNgFZVrgWWwcVuIlLtwcsVtVeec95_gy6SsaYB31jwZS_1lgD-ObA9m24IuHMXqlaBChTvRFmvbpeChRPJ4Mh5Zzz2doPe4brd-coNIRy4oQN8FKsbcw6rbbuJgvT4B-E3ftuEdx69s2qQKXx6KNf_pFL6FTmItJVSMTAIqciDvWXoxPqrJ48OEzhavR00z4iKjalHoaIpuJswDU_6FlsMGJrg9bpBaiFUhNpMEajNWVpU2jlW0Cw; login_scene=11; volcengineLoginMethod=pwd; csrfToken=bebb2ad0f9bc027de95b0d2f18450aa9; csrfToken=bebb2ad0f9bc027de95b0d2f18450aa9; gfkadpd=520918,36088; __tea_cache_tokens_3569={%22web_id%22:%227606220745165375022%22%2C%22user_unique_id%22:%227606220745165375022%22%2C%22timestamp%22:1770961317447%2C%22_type_%22:%22default%22}; s_v_web_id=verify_mlkgnbq9_5AbTkXNC_EYAi_4bTQ_9qnK_aJ8hRAcPggyM"""
    model = "doubao-seed"
    prompt = "鸭子放在T恤上"
    image = [
            "https://v3.fal.media/files/penguin/XoW0qavfF-ahg-jX4BMyL_image.webp",
             "https://v3.fal.media/files/tiger/bml6YA7DWJXOigadvxk75_image.webp"
  ]

    request = ImageRequest(
        model=model, n=1,
        prompt=prompt,
                           size='4096x2048',

        image=image
                           )

    arun(generate(request=request, api_key=api_key))
