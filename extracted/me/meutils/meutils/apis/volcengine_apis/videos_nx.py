#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : videos
# @Time         : 2025/6/11 15:13
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : todo 官方格式

from meutils.pipe import *
from meutils.io.files_utils import to_url, to_base64
from meutils.decorators.retry import retrying
from meutils.apis.oneapi.utils import polling_keys
from meutils.apis.volcengine_apis.utils import upload

from meutils.llm.clients import AsyncClient
from meutils.schemas.openai_types import CompletionRequest
from meutils.schemas.video_types import SoraVideoRequest, Video

BASE_URL = "https://ml-platform-api.console.volcengine.com/ark/bff/api/cn-beijing/2024-01-29"


# "https://ml-platform-api.console.volcengine.com/ark/bff/api/cn-beijing/2024-01-29/CreateVideoGenTask"

class Tasks(object):

    def __init__(self, api_key):
        self.api_key = api_key
        self.csrf_token = api_key.split("csrfToken=")[1].split(';')[0]

        default_headers = {
            "x-csrf-token": self.csrf_token,
            "Cookie": api_key
        }
        self.client = AsyncClient(base_url=BASE_URL, default_headers=default_headers)

    async def create(self, request: SoraVideoRequest):
        payload = {
            "Watermark": False,

            # "CallbackUrl": f"""{os.getenv("WEBHOOK_URL")}/sd1""",
            # "callback_url": f"""{os.getenv("WEBHOOK_URL")}/sd11""",
            # "CallbackURL": f"""{os.getenv("WEBHOOK_URL")}/sd111""",

            "Name": "doubao-seedance-2-0",
            "Prompt": "飞起来",
            "TaskType": "BasicMode",
            "VideoTaskType": "text_to_video",

            "ModelName": "doubao-seedance-2-0",
            "ModelVersion": "260128",
            "Ratio": "adaptive",
            "Resolution": "480p",
            "GroupId": "1-1770783676576",
            "Duration": 5,
            "Seed": -1,
            "EndpointID": "doubao-seedance-2-0-260128",

            "GenerationTimeout": 48,
            "GenerateAudio": True,
            "DurationMode": "duration",
            "OptimizePromptOptions": {
                "EnableWebSearch": False
            },

            # "FirstFrameImageTosLocation": {
            #     "BucketName": "ark-common-storage-prod-cn-beijing",
            #     "ObjectKey": "experience_video/2119812478/0/20260211/3fb89957-0040-4cee-bf55-94214196c1d0.png",
            #     "Url": "https://ark-common-storage-prod-cn-beijing.tos-cn-beijing.volces.com/experience_video/2119812478/0/20260211/3fb89957-0040-4cee-bf55-94214196c1d0.png?X-Tos-Algorithm=TOS4-HMAC-SHA256&X-Tos-Credential=AKLTMjgxMzUwNzliYzdlNDE4MTllYjJjZGVlOWQ3N2M1ZDY%2F20260211%2Fcn-beijing%2Ftos%2Frequest&X-Tos-Date=20260211T042100Z&X-Tos-Expires=604800&X-Tos-Signature=3de95294198e2da85a0d8fc3a7f9c626ad873ceb0b5578eabcc9fefebc7bcf5e&X-Tos-SignedHeaders=host"
            # },
            # "LastFrameImageTosLocation": {
            #     "BucketName": "ark-common-storage-prod-cn-beijing",
            #     "ObjectKey": "experience_video/2119812478/0/20260211/8097768e-a5ae-47a4-858a-09993f8a5213.jpg",
            #     "Url": "https://ark-common-storage-prod-cn-beijing.tos-cn-beijing.volces.com/experience_video/2119812478/0/20260211/8097768e-a5ae-47a4-858a-09993f8a5213.jpg?X-Tos-Algorithm=TOS4-HMAC-SHA256&X-Tos-Credential=AKLTMjgxMzUwNzliYzdlNDE4MTllYjJjZGVlOWQ3N2M1ZDY%2F20260211%2Fcn-beijing%2Ftos%2Frequest&X-Tos-Date=20260211T042107Z&X-Tos-Expires=604800&X-Tos-Signature=372556f8b7e9b97a895eebe14b6eee9ae02aca0d450bb8124a13864d90244304&X-Tos-SignedHeaders=host"
            # },
        }
        ### 映射
        payload["Prompt"] = request.prompt
        payload["Duration"] = int(request.seconds or 4)

        if request.resolution:
            payload["Resolution"] = request.resolution

        if request.aspect_ratio:
            payload["Ratio"] = request.aspect_ratio

        if not request.generate_audio:
            payload["GenerateAudio"] = request.generate_audio

        if request.enhance_prompt:
            payload["OptimizePromptOptions"]["EnableWebSearch"] = True

        if urls := request.input_reference:
            # 不支持参考图
            # payload["ReferenceImages"] = [
            #     {
            #         "BucketName": "ark-common-storage-prod-cn-beijing",
            #         "ObjectKey": f"presets/experience/gen_video/materials/自定义/{i}",
            #         "Url": url,
            #         "Label": f"image_{i}_{i}"
            #     }
            #     for i, url in enumerate(urls, 1)
            # ]
            urls = await upload(urls, api_key=api_key)

            if len(urls) == 1:
                payload["VideoTaskType"] = "first_frame"
                payload["FirstFrameImageTosLocation"] = urls[0]
            elif len(urls) >= 2:
                payload["VideoTaskType"] = "first_last_frame"
                payload["FirstFrameImageTosLocation"] = urls[0]
                payload["LastFrameImageTosLocation"] = urls[1]

        if request.first_frame_image:
            payload["VideoTaskType"] = "first_frame"
            payload["FirstFrameImageTosLocation"] = await upload(request.first_frame_image, api_key=api_key)

        if request.last_frame_image:
            payload["VideoTaskType"] = "first_last_frame"
            payload["LastFrameImageTosLocation"] = await upload(request.last_frame_image, api_key=api_key)

        logger.debug(bjson(payload))

        response = await self.client.post("/CreateVideoGenTask", body=payload, cast_to=object)
        logger.debug(bjson(response))
        """
        {'ResponseMetadata': {'Action': 'CreateVideoGenTask',
                      'Duration': 448,
                      'Error': {'Code': 'CreateExperienceVisionTaskFailed',
                                'CodeN': 1009000,
                                'Message': '{"error":{"code":"InvalidParameter","message":"The '
                                           'parameter '
                                           '`execution_expires_after` '
                                           'specified in the request is not '
                                           'valid: the specified '
                                           'execution_expires_after 345600 '
                                           'does not support content '
                                           'generation. Request id: '
                                           '0217708948167874d1a7bd4cdfcf1811296cf68db8d43d8aa0100","param":"execution_expires_after","type":"BadRequest"}}'},
                      'Region': 'cn-beijing',
                      'RequestId': '202602121913367C8697C6C18BB919E2FD',
                      'Service': 'ark',
                      'Version': '2024-01-29'},
 'Result': None}
 
 {'ResponseMetadata': {'Action': 'CreateVideoGenTask',
                      'Duration': 629,
                      'Region': 'cn-beijing',
                      'RequestId': '202602121916218D56A5423FB9761137C0',
                      'Service': 'ark',
                      'Version': '2024-01-29'},
 'Result': {'Id': 'cgt-20260212191621-b9l7b'}}
        """
        if task_id := (response.get("Result") or {}).get("Id"):
            if "seedance" not in request.model:
                task_id = f"{request.model}::{task_id}"

                payload['Ratio'] = "720p"
                if "veo" in request.model:
                    payload['Duration'] = 8

                elif "sora" in request.model:  # sora-2-4s sora-2-8s sora-2-12s sora-2-15s
                    if request.model.endswith('s'):  # 逆向
                        payload['Duration'] = int(request.model.split('-')[-1].replace("s", ""))
                    elif request.model == "sora-2":  # 逆向
                        payload['Duration'] = 15

            video = Video(id=task_id)
            return video

        elif e := response.get("ResponseMetadata", {}).get("Error"):
            error = {
                "code": e.get("Code", "400"),
                "message": e.get("Message", str(e))
            }
            if "QuotaExceeded" in str(e):  # 切备用渠道
                error = "未知错误，请重试"
                raise ValueError(error)

            video = Video(status="failed", error=error)

            return video

    async def get(self, task_id: str):
        transfer = False
        if "::" in task_id:
            task_id = task_id.split("::")[-1]
            transfer = True

        response = await self.client.post("/GetVideoGenTask", body={"Id": task_id}, cast_to=object)
        # logger.debug(bjson(response))

        if url := (response.get("Result") or {}).get("VideoUrl"):
            logger.debug(bjson(response))

            if transfer:
                url = await to_url(url, filename=f'{shortuuid.random()}.mp4')  # 避免重复转存

            return Video(id=task_id, video_url=url, status="completed", progress=100)
        else:
            return Video(id=task_id)


# 执行异步函数
if __name__ == "__main__":
    api_key = """ve_doc_history=82379%2C6269%2C6256%2C85128%2C86081%2C6348%2C85621%2C6260;_qimei_fingerprint=dd38b822c43601e30b795b0bb06bc28b;hasUserBehavior=1;monitor_huoshan_web_id=7467761534115284489;referrer_title=%E5%88%9B%E5%BB%BA%E8%A7%86%E9%A2%91%E7%94%9F%E6%88%90%E4%BB%BB%E5%8A%A1%20API--%E7%81%AB%E5%B1%B1%E6%96%B9%E8%88%9F%E5%A4%A7%E6%A8%A1%E5%9E%8B%E6%9C%8D%E5%8A%A1%E5%B9%B3%E5%8F%B0-%E7%81%AB%E5%B1%B1%E5%BC%95%E6%93%8E;AccountID=2104716667;user_locale=zh;signin_i18next=zh;monitor_session_id_flag=1;monitor_traceid_base_cookie=1418;volcengineLoginMethod=pwd;_tea_utm_cache_3569={%22utm_source%22:%22coopensrc%22%2C%22utm_medium%22:%22github%22%2C%22utm_campaign%22:%22doubao%22%2C%22utm_term%22:%22project%22%2C%22utm_content%22:%22aidrawio%22};volcfe-uuid=0701f6f2-a611-4599-a2fc-57cb015ff828;userInfo=eyJhbGciOiJSUzI1NiIsImtpZCI6ImE5YzBkZmFjYmZiNDExZjA4OWMwMDAxNjNlMDcwOGJkIn0.eyJhY2NfaSI6MjEwNDcxNjY2NywiYXVkIjpbImNvbnNvbGUudm9sY2VuZ2luZS5jb20iXSwiZXhwIjoxNzczNDc3MzIxLCJpIjoiYzUxNTFmMzUwN2VkMTFmMTllYTUzNDM2YWMxMjAwYzciLCJpZF9uIjoiODQzMuaJi-acuueUqOaItyNaY1JzUnkiLCJtc2ciOm51bGwsInBpZCI6IjBkMDQ2ZDlkLTg4NTYtNDhiNy1iZGMzLWQ0OTI4ODQ3Njc2YiIsInNzX24iOiI4NDMy5omL5py655So5oi3I1pjUnNSeSIsInQiOiJBY2NvdW50IiwidG9waWMiOiJzaWduaW5fdXNlcl9pbmZvIiwidmVyc2lvbiI6InYxIiwiemlwIjoiIn0.gfVFCXMedtkYoGFpObMWKulX5QPrdSDadKKyxMl7TecUX4gxF53E4NaZjMfDruLDu7gIlIEhbLyUzMvOJtUFyVtP1VIZDXD1zOLf7T-nKO4WH4MEEHf6F-ERzjMabSQfotnaEeMyysjbetQJ38UEA6hF_C70zo-hv_sIKdMVMTqLt2J7Sf1ry0qNDGEMBQzOB6hNB5amF6NB9GByLZEl-RjovAbB3SkarTSpWLnekrUxyJXD-SIdN80kKOrnlugyMFCE_NPVuZ4ZFgTyKJt1o0Yp_-jb1GBJDUeY2Tq-vDjalIvT9q-PJE4MCw9Bb4VIkaVFfobO1sDiOocvu00gTg;__tea_cache_tokens_3569={%22web_id%22:%227467761534115284489%22%2C%22user_unique_id%22:%227467761534115284489%22%2C%22timestamp%22:1770885409545%2C%22_type_%22:%22default%22};volc-design-locale=zh;_qimei_h38=47aeffd76da9e4a25cf291fa0300000d619a11;finance-hub-sdk-lang=zh;p_c_check=1;volc_platform_clear_user_locale=1;__spti=11_000JnXNrWATPtPrMwlQ3ilQxfn2UtC;__sptiho=0B11_000JnXNrWATPtPrMwlQ3ilQxfn2UtC_bEv/KoxCOM4AcC;_qimei_i_1=5ac22586920b058d97c3f9360fd57ab5f3bfa6f4410d018bb5d979582593206c616363933980b3ddd790cf8f;_qimei_i_3=57ca79d3970c52d9c497aa625d8027e5a6bcf0f71a5b04d4e0872b502092276d32633f973989e28184b1;_qimei_uuid42=19c180a1723100cab20e31b701a4124555c551b916;_tea_utm_cache_520918={%22utm_source%22:%22coopensrc%22%2C%22utm_medium%22:%22github%22%2C%22utm_campaign%22:%22doubao%22%2C%22utm_term%22:%22project%22%2C%22utm_content%22:%22aidrawio%22};csrfToken=b6b2764fc8bf2869340ddeaa2d5b81ac;digest=eyJhbGciOiJSUzI1NiIsImtpZCI6ImE5YzBkZmFjYmZiNDExZjA4OWMwMDAxNjNlMDcwOGJkIn0.eyJhdWQiOlsiY29uc29sZS52b2xjZW5naW5lLmNvbSJdLCJleHAiOjE3NzEwNTgxMjEsImlhdCI6MTc3MDg4NTMyMSwiaXNzIjoiaHR0cHM6Ly9zaWduaW4udm9sY2VuZ2luZS5jb20iLCJqdGkiOiIwZDA0NmQ5ZC04ODU2LTQ4YjctYmRjMy1kNDkyODg0NzY3NmIiLCJtc2ciOiJINHNJQUFBQUFBQUMvK0tTNDJMeFM4eE5GZUl5TWpRd01UYzBNek16bHppMGNOc1pOb1dUSUZMSW40dmRNVGs1dnpTdlJPRDNyYk92MmFYRUxVeU1qWjUxZGorYnMrdjVsQlhQT3JZclJ5VUhGUWRWS29ITjBXSkx6cy9OemMvendxVU1FQUFBLy8vSzNjZTVjUUFBQUE9PSIsIm5hbWUiOiI4NDMy5omL5py655So5oi3I1pjUnNSeSIsInN1YiI6IjIxMDQ3MTY2NjciLCJ0b3BpYyI6InNpZ25pbl9jcmVkZW50aWFsIiwidHJuIjoidHJuOmlhbTo6MjEwNDcxNjY2Nzpyb290IiwidmVyc2lvbiI6InYxIiwiemlwIjoiZ3ppcCJ9.Z-eEz3F4-7zEBTycZtzF2L0DjTnNMvmWMai7yfbsbK4VAvzlw8l0XJ4qxzch9RcIZKvK_Hp_iKzitotsFQHQHhmElcF1l5X3CgGhB4bM4DHKbvU1Q8rwn2IqMZeVjPnVcaA9U6G9nCCYtmgdWfiilPO3EyC7Wirx7TBhRkW2IcFtZhO_Ft5IN25A7TVWioaWuRTqAlKUsFujENgx23uQ2VPhKx6q8_vp4vbmRC-vshFM2osYq-3o_shi3bKS-S-eZjLdOKqfRlY5qsf_SBDpv08yXVIntzGlHKAO1jzrBxwDRQZp5aDv4J6RYtoJKsyE9-ISbrb_p3BD4h2kbuIHQA;gfkadpd=520918,36088|3569,42874;i18next=zh;isIntranet=0;login_scene=11;monitor_session_id=0137731691764811011;monitor_utm=%257B%2522utm_campaign%2522%253A%2522doubao%2522%252C%2522utm_content%2522%253A%2522aidrawio%2522%252C%2522utm_medium%2522%253A%2522github%2522%252C%2522utm_source%2522%253A%2522coopensrc%2522%252C%2522utm_term%2522%253A%2522project%2522%257D;s_v_web_id=verify_mjjfj194_6wx9uxHT_RbvK_42dT_BQQF_Am4VHcR3e6qJ;top_region=;vcloudWebId=0d8e34f9-2a27-4f3b-a86a-10cb562dbf67;VOLCFE_im_uuid=1770641165069598896"""

    api_key = """ve_doc_history=82379%2C6269%2C6256%2C85128%2C86081%2C6348%2C85621%2C6260;_qimei_fingerprint=dd38b822c43601e30b795b0bb06bc28b;hasUserBehavior=1;monitor_huoshan_web_id=7467761534115284489;referrer_title=%E5%88%9B%E5%BB%BA%E8%A7%86%E9%A2%91%E7%94%9F%E6%88%90%E4%BB%BB%E5%8A%A1%20API--%E7%81%AB%E5%B1%B1%E6%96%B9%E8%88%9F%E5%A4%A7%E6%A8%A1%E5%9E%8B%E6%9C%8D%E5%8A%A1%E5%B9%B3%E5%8F%B0-%E7%81%AB%E5%B1%B1%E5%BC%95%E6%93%8E;AccountID=2109091919;user_locale=zh;signin_i18next=zh;monitor_session_id_flag=1;monitor_traceid_base_cookie=1419;volcengineLoginMethod=pwd;_tea_utm_cache_3569={%22utm_source%22:%22coopensrc%22%2C%22utm_medium%22:%22github%22%2C%22utm_campaign%22:%22doubao%22%2C%22utm_term%22:%22project%22%2C%22utm_content%22:%22aidrawio%22};volcfe-uuid=0701f6f2-a611-4599-a2fc-57cb015ff828;userInfo=eyJhbGciOiJSUzI1NiIsImtpZCI6ImE5YzBkZmFjYmZiNDExZjA4OWMwMDAxNjNlMDcwOGJkIn0.eyJhY2NfaSI6MjEwOTA5MTkxOSwiYXVkIjpbImNvbnNvbGUudm9sY2VuZ2luZS5jb20iXSwiZXhwIjoxNzczNDk5Mzk0LCJpIjoiMjk2OTc3MmEwODIxMTFmMTlhZjEzNDM2YWMxMjAwM2YiLCJpZF9uIjoiMDQzNeaJi-acuueUqOaItyN5SFNrTXQiLCJtc2ciOm51bGwsInBpZCI6ImNkNDlmYTg3LWI3NzUtNDQwNS1iOTkzLTVmOTA0NTMyNDg5MSIsInNzX24iOiIwNDM15omL5py655So5oi3I3lIU2tNdCIsInQiOiJBY2NvdW50IiwidG9waWMiOiJzaWduaW5fdXNlcl9pbmZvIiwidmVyc2lvbiI6InYxIiwiemlwIjoiIn0.cdpiB9xgcokJBJzG-S_BIdllMusycBqNLL8VNEnmlFI5i0fYstJUbAvLC-nbouHZjLhX9XzT45RjIqbFa-f1dnQHE6SmMf_CCPuxoZOpd7UnJTbCqQiKO_KRkdshxpuIxx7mV74ziS3UQWcNARIH663BxmsMsPWFx7Tntx3QOCdu_zljgJkjbxJZhcBhGOqGC2CMZXocr0MorPpcEVtXPOsRi9ulCBMSSH4kI5z4iigbliLyoYcsD3vNCmGO_vTOPDAdyEwGE395FwAnlB62JGnwVAreHvdPLE3YFMBII2JdDT03TGOrb1VFP6tLj2xOAWCDlVJnxRkW2fDZ16d71Q;__tea_cache_tokens_3569={%22web_id%22:%227467761534115284489%22%2C%22user_unique_id%22:%227467761534115284489%22%2C%22timestamp%22:1770907429996%2C%22_type_%22:%22default%22};volc-design-locale=zh;_qimei_h38=94cee221b20e31b701a412450300000ce19c18;finance-hub-sdk-lang=zh;p_c_check=1;volc_platform_clear_user_locale=1;__spti=11_000JnXNrWATPtPrMwlQ3ilQxfn2UtC;__sptiho=0B11_000JnXNrWATPtPrMwlQ3ilQxfn2UtC_bEv/KoxCOM4AcC;_qimei_i_1=5eea2c8b9109058ec395ff62598426e3f6bca3f1130a0783b68b2d582593206c616364c03980b1ddde92f7cc;_qimei_i_3=57ca79d3970c52d9c497aa625d8027e5a6bcf0f71a5b04d4e0872b502092276d32633f973989e28184b1;_qimei_uuid42=19c180a1723100cab20e31b701a4124555c551b916;_tea_utm_cache_520918={%22utm_source%22:%22coopensrc%22%2C%22utm_medium%22:%22github%22%2C%22utm_campaign%22:%22doubao%22%2C%22utm_term%22:%22project%22%2C%22utm_content%22:%22aidrawio%22};csrfToken=499beb4542dac5d353afbb1fffd981eb;digest=eyJhbGciOiJSUzI1NiIsImtpZCI6ImE5ZDM1YTQ4YmZiNDExZjA4OWMwMDAxNjNlMDcwOGJkIn0.eyJhdWQiOlsiY29uc29sZS52b2xjZW5naW5lLmNvbSJdLCJleHAiOjE3NzEwODAxOTQsImlhdCI6MTc3MDkwNzM5NCwiaXNzIjoiaHR0cHM6Ly9zaWduaW4udm9sY2VuZ2luZS5jb20iLCJqdGkiOiJjZDQ5ZmE4Ny1iNzc1LTQ0MDUtYjk5My01ZjkwNDUzMjQ4OTEiLCJtc2ciOiJINHNJQUFBQUFBQUMvK0tTNDJMeFM4eE5GZUl5TWpTd05MQTB0RFMwbFBoNWR2c1pOb1dtYzl2UHNBbjVjN0U3SmlmbmwrYVZDSngvY09NdHU1UzRnWW14NmJQTzdtZHpkajJmc3VKWngzYmxTby9nYk44U0piQTVXbXpKK2JtNStYbGV1SlFCQWdBQS8vOTdrMG13Y1FBQUFBPT0iLCJuYW1lIjoiMDQzNeaJi-acuueUqOaItyN5SFNrTXQiLCJzdWIiOiIyMTA5MDkxOTE5IiwidG9waWMiOiJzaWduaW5fY3JlZGVudGlhbCIsInRybiI6InRybjppYW06OjIxMDkwOTE5MTk6cm9vdCIsInZlcnNpb24iOiJ2MSIsInppcCI6Imd6aXAifQ.fw4LobnAByUwIaCOWhOOvF5igRzIo_l5lBme2SmfeT5vwky01EI2iBDBayuv_O39Uvl-MzS5Gmg2-tXFN7tqEyH2ERa1ymuZETFkFu3P-su9Uqb1VZnFpkaZsjHzhCTWIxvwDLmBCZM0aLN_LOBjhDyoRjd6agYr8XLrTM3UzVRb-MUg_yYBBSttvUpZdM4pLQ3magTu0xJQY0OfLg4IBTezfg84XsQJkh0wGaJI1N-_aXTTXTFBOBahMS8fKJrNG-mgV52xMxBqS_pt3piGwn3ssMVeD5JD5K474FMKxIhgwJUkdePfsVACAjBhaLmV6AmYX4UXo7lTmjHHIZnp3Q;gfkadpd=520918,36088|3569,42874;i18next=zh;isIntranet=0;login_scene=11;monitor_session_id=0008375069127979375;monitor_tracing_cookie=[];monitor_utm=%257B%2522utm_campaign%2522%253A%2522doubao%2522%252C%2522utm_content%2522%253A%2522aidrawio%2522%252C%2522utm_medium%2522%253A%2522github%2522%252C%2522utm_source%2522%253A%2522coopensrc%2522%252C%2522utm_term%2522%253A%2522project%2522%257D;s_v_web_id=verify_mjjfj194_6wx9uxHT_RbvK_42dT_BQQF_Am4VHcR3e6qJ;top_region=;vcloudWebId=0d8e34f9-2a27-4f3b-a86a-10cb562dbf67;VOLCFE_im_uuid=1770641165069598896"""
    request = SoraVideoRequest(
        # prompt="【图片 1】【图片 2】融合起",
        prompt="孙悟空",

        # seconds=4,
        # resolution="480p",

        seconds=15,
        resolution="720p",
        # aspect_ratio="adaptive",
        # input_reference=[
        #     "https://storage.googleapis.com/falserverless/example_inputs/nano-banana-edit-input.png",
        #     "https://storage.googleapis.com/falserverless/example_inputs/nano-banana-edit-input-2.png"
        # ]

        # first_frame_image="https://storage.googleapis.com/falserverless/example_inputs/nano-banana-edit-input.png",
        # last_frame_image="https://storage.googleapis.com/falserverless/example_inputs/nano-banana-edit-input-2.png"

    )
    task_ids = []
    # for i in range(120):
    #     request.prompt = f"孙悟空大声叫 {i}"
    #     video = arun(Tasks(api_key).create(request))
    #     task_ids.append(video.id)

    # arun(Tasks(api_key).create(request))
    # # task_id = "cgt-20260212191621-b9l7b"
    # # task_id = "cgt-20260212193527-b7xll"
    # # task_id = "cgt-20260212194710-gwzpn"
    # # task_id = "cgt-20260212200601-474df" # 首尾帧
    # task_id = "cgt-20260212202542-mjzbb"
    task_id = "sora-2::cgt-20260212224451-6nrdn"
    arun(Tasks(api_key).get(task_id))

    t = ['cgt-20260212202400-zrkm4',
         'cgt-20260212202401-8ppjx',
         'cgt-20260212202402-4s2lq',
         'cgt-20260212202403-vd9mh',
         'cgt-20260212202404-czg7k',
         'cgt-20260212202405-tmd9k',
         'cgt-20260212202406-frjnv',
         'cgt-20260212202407-ml7zz',
         'cgt-20260212202407-4j6ws',
         'cgt-20260212202409-9znbd',
         'cgt-20260212202410-fll8p',
         'cgt-20260212202411-6jbp9',
         'cgt-20260212202412-l464s',
         'cgt-20260212202413-8vkkg',
         'cgt-20260212202413-j2m4q',
         'cgt-20260212202414-rs7wz',
         'cgt-20260212202415-s642l',
         'cgt-20260212202416-9jj9p',
         'cgt-20260212202417-qnb6z',
         'cgt-20260212202417-2gb8f',
         'cgt-20260212202418-7l9kr',
         'cgt-20260212202419-wfmpf',
         'cgt-20260212202420-j9pqw',
         'cgt-20260212202421-h7fj9',
         'cgt-20260212202422-lfvgw',
         'cgt-20260212202422-xfs4c',
         'cgt-20260212202423-66krj',
         'cgt-20260212202424-qvbzd',
         'cgt-20260212202425-b9nns',
         'cgt-20260212202426-pwhlq',
         'cgt-20260212202427-rjmwn',
         'cgt-20260212202427-q9gjw',
         'cgt-20260212202428-m2gsg',
         'cgt-20260212202429-9z8c7',
         'cgt-20260212202430-6dx2l',
         'cgt-20260212202431-mjgpl',
         'cgt-20260212202432-lgxnb',
         'cgt-20260212202432-6f4pb',
         'cgt-20260212202433-b8chd',
         'cgt-20260212202434-5647k',
         'cgt-20260212202435-4prdm',
         'cgt-20260212202436-99rcw',
         'cgt-20260212202437-ztlzw',
         'cgt-20260212202437-dkvbh',
         'cgt-20260212202438-k64sd',
         'cgt-20260212202439-lq4km',
         'cgt-20260212202440-jf7m4',
         'cgt-20260212202441-2tb8c',
         'cgt-20260212202442-j55nz',
         'cgt-20260212202442-qjqlh',
         'cgt-20260212202443-rtdl5',
         'cgt-20260212202444-4wrcf',
         'cgt-20260212202445-hsxdp',
         'cgt-20260212202446-z2k2z',
         'cgt-20260212202447-7cb6f',
         'cgt-20260212202448-ld76h',
         'cgt-20260212202448-vp4k6',
         'cgt-20260212202449-xlgcf',
         'cgt-20260212202450-qcczc',
         'cgt-20260212202451-qfdzg',
         'cgt-20260212202452-xbpvf',
         'cgt-20260212202453-bzv7s',
         'cgt-20260212202454-rn9n7',
         'cgt-20260212202454-jv4gs',
         'cgt-20260212202455-28wl2',
         'cgt-20260212202456-rhnq8',
         'cgt-20260212202457-hrqsb',
         'cgt-20260212202458-4mdns',
         'cgt-20260212202459-mmm89',
         'cgt-20260212202459-27rmp',
         'cgt-20260212202500-mvn7v',
         'cgt-20260212202501-hbgfs',
         'cgt-20260212202502-kvvf8',
         'cgt-20260212202503-s5qjm',
         'cgt-20260212202504-p4kkd',
         'cgt-20260212202504-94cfr',
         'cgt-20260212202505-8nj6p',
         'cgt-20260212202506-h6zr4',
         'cgt-20260212202507-n9vm6',
         'cgt-20260212202507-w6hh5',
         'cgt-20260212202508-xtqg7',
         'cgt-20260212202509-tp5p6',
         'cgt-20260212202510-9ls7l',
         'cgt-20260212202511-mfwct',
         'cgt-20260212202512-7lnrs',
         'cgt-20260212202513-q84ss',
         'cgt-20260212202514-rgpmq',
         'cgt-20260212202514-nng8d',
         'cgt-20260212202515-rsmgq',
         'cgt-20260212202516-c8th4',
         'cgt-20260212202517-g694z',
         'cgt-20260212202518-kj8bl',
         'cgt-20260212202519-nf82w',
         'cgt-20260212202520-vslgd',
         'cgt-20260212202521-lsvgp',
         'cgt-20260212202521-6g6ps',
         'cgt-20260212202522-mrhpf',
         'cgt-20260212202523-hvn48',
         'cgt-20260212202524-h2pqp',
         'cgt-20260212202525-67z4s',
         'cgt-20260212202526-z2tng',
         'cgt-20260212202527-sdrfp',
         'cgt-20260212202527-c9w7q',
         'cgt-20260212202528-2frs4',
         'cgt-20260212202529-fdl4z',
         'cgt-20260212202530-4sg92',
         'cgt-20260212202531-cpq9z',
         'cgt-20260212202532-hg448',
         'cgt-20260212202532-cbx92',
         'cgt-20260212202533-nsrpf',
         'cgt-20260212202534-blpk9',
         'cgt-20260212202535-hj2rj',
         'cgt-20260212202536-nrvpb',
         'cgt-20260212202537-9glbk',
         'cgt-20260212202538-8qldz',
         'cgt-20260212202538-dv6r5',
         'cgt-20260212202539-j2s2z',
         'cgt-20260212202540-pkwrj',
         'cgt-20260212202541-8tnd8',
         'cgt-20260212202542-mjzbb']
