#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : videos
# @Time         : 2025/6/11 15:13
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : todo 官方格式  todo 加代理

from meutils.pipe import *
from meutils.io.files_utils import to_url, to_base64
from meutils.decorators.retry import retrying
from meutils.apis.oneapi.utils import polling_keys
from meutils.apis.volcengine_apis.utils import upload

from meutils.llm.clients import AsyncClient
from meutils.schemas.openai_types import CompletionRequest
from meutils.schemas.video_types import SoraVideoRequest, Video, VolcVideoResponse
from meutils.str_utils import parse_command_string

BASE_URL = "https://ml-platform-api.console.volcengine.com/ark/bff/api/cn-beijing/2024-01-29"


# "https://ml-platform-api.console.volcengine.com/ark/bff/api/cn-beijing/2024-01-29/CreateVideoGenTask"

class Tasks(object):

    def __init__(self, api_key: str):
        self.api_key = api_key

        self.user_id = ""
        if "AccountID=" in api_key:
            self.user_id = api_key.split("AccountID=")[1].split(';')[0]
            logger.debug(f"user_id: {self.user_id}")

        default_headers = {
            "x-csrf-token": api_key.split("csrfToken=")[1].split(';')[0],
            "Cookie": api_key
        }
        self.client = AsyncClient(base_url=BASE_URL, default_headers=default_headers)

    async def get_for_volc(self, task_id: str):
        video = await self.get(task_id)

        volc_video = VolcVideoResponse(id=task_id)
        if video.status == "completed":
            volc_video.status = "succeeded"
            for i in ["ratio", "resolution", "duration", "content", "usage"]:
                setattr(volc_video, i, getattr(video, i))

        elif video.status == "failed":
            volc_video.status = "failed"

        return volc_video

    async def create_for_volc(self, request: CompletionRequest):  # 5s 10s 15s
        # 兼容 官方格式

        """
        # 创建 图生视频 任务
        curl -X POST https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks \
              -H "Content-Type: application/json" \
              -H "Authorization: Bearer $ARK_API_KEY" \
              -d '{
                "model": "doubao-seedance-1-5-pro-251215",
                "content": [
                     {
                        "type": "text",
                        "text": "图中女孩对着镜头说“茄子”，360度环绕运镜"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "https://ark-project.tos-cn-beijing.volces.com/doc_image/seepro_first_frame.jpeg"
                        },
                        "role": "first_frame"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "https://ark-project.tos-cn-beijing.volces.com/doc_image/seepro_last_frame.jpeg"
                        },
                        "role": "last_frame"
                    }
                ],
                "generate_audio":true,
                "ratio": "adaptive",
                "duration": 5,
                "watermark": false
            }'
        """
        video_request = SoraVideoRequest(model="doubao-seedance-2-0-260128")
        if request.messages:  # chat doubao-seedance-1-5-pro-251215_5s_720p
            video_request.prompt = request.last_user_content
            if '_' not in request.model:
                request.model += "_4s_480p"
            duration, video_request.resolution = request.model.split('_')[-2:]
            video_request.seconds = int(duration.replace('s', ''))

            if image_urls := request.last_urls.get("image_url"):
                video_request.input_reference = image_urls

            return await self.create(video_request)

        elif hasattr(request, 'content'):
            video_request.input_reference = []
            for i in request.content:
                if i.get("type") == "text":
                    video_request.prompt = i.get("text")

                elif i.get("type") == "image_url":
                    url = i.get("image_url", {}).get("url")
                    role = i.get("role")
                    if role == "first_frame":
                        video_request.first_frame_image = url
                    elif role == "last_frame":
                        video_request.last_frame_image = url
                    else:
                        video_request.input_reference.append(url)

            request = request.model_dump()
            if _ := request.get("duration"):
                video_request.seconds = _

            if _ := request.get("resolution"):
                video_request.resolution = _

            if _ := request.get("ratio"):
                video_request.aspect_ratio = _

            if _ := request.get("generate_audio"):
                video_request.generate_audio = _

            video = await self.create(video_request)
            """
             "ResponseMetadata": {
        "RequestId": "202602132223495898AADDDC1C34119EED",
        "Action": "CreateVideoGenTask",
        "Version": "2024-01-29",
        "Service": "ark",
        "Region": "cn-beijing",
        "Duration": 390,
        "Error": {
            "Message": "Your account has exhausted its free trial quota for the doubao-seedance-2-0 model.",
            "Code": "QuotaExceeded",
            "CodeN": 1009000
        }
    },
            """
            return {"id": video.id}

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
        payload["Duration"] = min(int(request.seconds or 4), 15)

        logger.debug(request)
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
            urls = await upload(urls, api_key=self.api_key)

            if len(urls) == 1:
                payload["VideoTaskType"] = "first_frame"
                payload["FirstFrameImageTosLocation"] = urls[0]
            elif len(urls) >= 2:
                payload["VideoTaskType"] = "first_last_frame"
                payload["FirstFrameImageTosLocation"] = urls[0]
                payload["LastFrameImageTosLocation"] = urls[1]

        if request.first_frame_image or request.last_frame_image:
            first_frame_image, last_frame_image = await upload(
                [request.first_frame_image, request.last_frame_image],
                api_key=self.api_key
            )
            if first_frame_image:
                payload["VideoTaskType"] = "first_frame"
                payload["FirstFrameImageTosLocation"] = first_frame_image

                if last_frame_image:
                    payload["VideoTaskType"] = "first_last_frame"
                    payload["LastFrameImageTosLocation"] = last_frame_image

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

            # 拼接用户id
            # task_id = f"{self.user_id}::{task_id}"
            video = Video(id=task_id)
            return video

        elif e := response.get("ResponseMetadata", {}).get("Error"):
            if any(i in str(e) for i in {"QuotaExceeded", "NotLogin"}):
                raise Exception(f"QuotaExceeded")  # 走兜底

            error = {
                "code": e.get("Code", "400"),
                "message": e.get("Message", str(e))
            }

            video = Video(status="failed", error=error)

            return video

    async def get(self, task_id: str):
        transfer = False
        if "::" in task_id:
            task_id = task_id.split("::")[-1]
            transfer = True

        if len(task_id) == 36 and "cgt-" not in task_id.lower():
            return Video(id=task_id, status="failed")

        response = await self.client.post("/GetVideoGenTask", body={"Id": task_id}, cast_to=object)
        logger.debug(response.get("Result"))

        if (result := (response.get("Result") or {})) and (error := result.get("Error")):
            # logger.debug(bjson(response))

            return Video(id=task_id, status="failed", error=error)
        elif "failed" in str(response.get("Status")).lower():
            logger.debug(bjson(response))

            return Video(id=task_id, status="failed", error=str(response))  # todo 根据id判断

        elif url := result.get("VideoUrl"):
            logger.debug(bjson(response))

            if transfer:
                url = await to_url(url, filename=f'{shortuuid.random()}.mp4')  # 避免重复转存

            _ = {
                "ratio": result.get("Ratio"),
                "resolution": result.get("Resolution", "720p"),
                "duration": result.get("Duration", 5),
                "content": {
                    "video_url": url
                },
            }
            total_tokens = _["duration"] * int(_['resolution'][:-1]) * 24 * 2
            _['usage'] = {
                "completion_tokens": total_tokens,
                "total_tokens": total_tokens
            }

            return Video(id=task_id, video_url=url, status="completed", progress=100, **_)
        else:
            return Video(id=task_id)


# 执行异步函数
if __name__ == "__main__":
    api_key = """ve_doc_history=82379%2C6269%2C6256%2C85128%2C86081%2C6348%2C85621%2C6260;_qimei_fingerprint=dd38b822c43601e30b795b0bb06bc28b;hasUserBehavior=1;monitor_huoshan_web_id=7467761534115284489;referrer_title=%E5%88%9B%E5%BB%BA%E8%A7%86%E9%A2%91%E7%94%9F%E6%88%90%E4%BB%BB%E5%8A%A1%20API--%E7%81%AB%E5%B1%B1%E6%96%B9%E8%88%9F%E5%A4%A7%E6%A8%A1%E5%9E%8B%E6%9C%8D%E5%8A%A1%E5%B9%B3%E5%8F%B0-%E7%81%AB%E5%B1%B1%E5%BC%95%E6%93%8E;AccountID=2104716667;user_locale=zh;signin_i18next=zh;monitor_session_id_flag=1;monitor_traceid_base_cookie=1418;volcengineLoginMethod=pwd;_tea_utm_cache_3569={%22utm_source%22:%22coopensrc%22%2C%22utm_medium%22:%22github%22%2C%22utm_campaign%22:%22doubao%22%2C%22utm_term%22:%22project%22%2C%22utm_content%22:%22aidrawio%22};volcfe-uuid=0701f6f2-a611-4599-a2fc-57cb015ff828;userInfo=eyJhbGciOiJSUzI1NiIsImtpZCI6ImE5YzBkZmFjYmZiNDExZjA4OWMwMDAxNjNlMDcwOGJkIn0.eyJhY2NfaSI6MjEwNDcxNjY2NywiYXVkIjpbImNvbnNvbGUudm9sY2VuZ2luZS5jb20iXSwiZXhwIjoxNzczNDc3MzIxLCJpIjoiYzUxNTFmMzUwN2VkMTFmMTllYTUzNDM2YWMxMjAwYzciLCJpZF9uIjoiODQzMuaJi-acuueUqOaItyNaY1JzUnkiLCJtc2ciOm51bGwsInBpZCI6IjBkMDQ2ZDlkLTg4NTYtNDhiNy1iZGMzLWQ0OTI4ODQ3Njc2YiIsInNzX24iOiI4NDMy5omL5py655So5oi3I1pjUnNSeSIsInQiOiJBY2NvdW50IiwidG9waWMiOiJzaWduaW5fdXNlcl9pbmZvIiwidmVyc2lvbiI6InYxIiwiemlwIjoiIn0.gfVFCXMedtkYoGFpObMWKulX5QPrdSDadKKyxMl7TecUX4gxF53E4NaZjMfDruLDu7gIlIEhbLyUzMvOJtUFyVtP1VIZDXD1zOLf7T-nKO4WH4MEEHf6F-ERzjMabSQfotnaEeMyysjbetQJ38UEA6hF_C70zo-hv_sIKdMVMTqLt2J7Sf1ry0qNDGEMBQzOB6hNB5amF6NB9GByLZEl-RjovAbB3SkarTSpWLnekrUxyJXD-SIdN80kKOrnlugyMFCE_NPVuZ4ZFgTyKJt1o0Yp_-jb1GBJDUeY2Tq-vDjalIvT9q-PJE4MCw9Bb4VIkaVFfobO1sDiOocvu00gTg;__tea_cache_tokens_3569={%22web_id%22:%227467761534115284489%22%2C%22user_unique_id%22:%227467761534115284489%22%2C%22timestamp%22:1770885409545%2C%22_type_%22:%22default%22};volc-design-locale=zh;_qimei_h38=47aeffd76da9e4a25cf291fa0300000d619a11;finance-hub-sdk-lang=zh;p_c_check=1;volc_platform_clear_user_locale=1;__spti=11_000JnXNrWATPtPrMwlQ3ilQxfn2UtC;__sptiho=0B11_000JnXNrWATPtPrMwlQ3ilQxfn2UtC_bEv/KoxCOM4AcC;_qimei_i_1=5ac22586920b058d97c3f9360fd57ab5f3bfa6f4410d018bb5d979582593206c616363933980b3ddd790cf8f;_qimei_i_3=57ca79d3970c52d9c497aa625d8027e5a6bcf0f71a5b04d4e0872b502092276d32633f973989e28184b1;_qimei_uuid42=19c180a1723100cab20e31b701a4124555c551b916;_tea_utm_cache_520918={%22utm_source%22:%22coopensrc%22%2C%22utm_medium%22:%22github%22%2C%22utm_campaign%22:%22doubao%22%2C%22utm_term%22:%22project%22%2C%22utm_content%22:%22aidrawio%22};csrfToken=b6b2764fc8bf2869340ddeaa2d5b81ac;digest=eyJhbGciOiJSUzI1NiIsImtpZCI6ImE5YzBkZmFjYmZiNDExZjA4OWMwMDAxNjNlMDcwOGJkIn0.eyJhdWQiOlsiY29uc29sZS52b2xjZW5naW5lLmNvbSJdLCJleHAiOjE3NzEwNTgxMjEsImlhdCI6MTc3MDg4NTMyMSwiaXNzIjoiaHR0cHM6Ly9zaWduaW4udm9sY2VuZ2luZS5jb20iLCJqdGkiOiIwZDA0NmQ5ZC04ODU2LTQ4YjctYmRjMy1kNDkyODg0NzY3NmIiLCJtc2ciOiJINHNJQUFBQUFBQUMvK0tTNDJMeFM4eE5GZUl5TWpRd01UYzBNek16bHppMGNOc1pOb1dUSUZMSW40dmRNVGs1dnpTdlJPRDNyYk92MmFYRUxVeU1qWjUxZGorYnMrdjVsQlhQT3JZclJ5VUhGUWRWS29ITjBXSkx6cy9OemMvendxVU1FQUFBLy8vSzNjZTVjUUFBQUE9PSIsIm5hbWUiOiI4NDMy5omL5py655So5oi3I1pjUnNSeSIsInN1YiI6IjIxMDQ3MTY2NjciLCJ0b3BpYyI6InNpZ25pbl9jcmVkZW50aWFsIiwidHJuIjoidHJuOmlhbTo6MjEwNDcxNjY2Nzpyb290IiwidmVyc2lvbiI6InYxIiwiemlwIjoiZ3ppcCJ9.Z-eEz3F4-7zEBTycZtzF2L0DjTnNMvmWMai7yfbsbK4VAvzlw8l0XJ4qxzch9RcIZKvK_Hp_iKzitotsFQHQHhmElcF1l5X3CgGhB4bM4DHKbvU1Q8rwn2IqMZeVjPnVcaA9U6G9nCCYtmgdWfiilPO3EyC7Wirx7TBhRkW2IcFtZhO_Ft5IN25A7TVWioaWuRTqAlKUsFujENgx23uQ2VPhKx6q8_vp4vbmRC-vshFM2osYq-3o_shi3bKS-S-eZjLdOKqfRlY5qsf_SBDpv08yXVIntzGlHKAO1jzrBxwDRQZp5aDv4J6RYtoJKsyE9-ISbrb_p3BD4h2kbuIHQA;gfkadpd=520918,36088|3569,42874;i18next=zh;isIntranet=0;login_scene=11;monitor_session_id=0137731691764811011;monitor_utm=%257B%2522utm_campaign%2522%253A%2522doubao%2522%252C%2522utm_content%2522%253A%2522aidrawio%2522%252C%2522utm_medium%2522%253A%2522github%2522%252C%2522utm_source%2522%253A%2522coopensrc%2522%252C%2522utm_term%2522%253A%2522project%2522%257D;s_v_web_id=verify_mjjfj194_6wx9uxHT_RbvK_42dT_BQQF_Am4VHcR3e6qJ;top_region=;vcloudWebId=0d8e34f9-2a27-4f3b-a86a-10cb562dbf67;VOLCFE_im_uuid=1770641165069598896"""

    api_key = """ve_doc_history=82379%2C6269%2C6256%2C85128%2C86081%2C6348%2C85621%2C6260;_qimei_fingerprint=dd38b822c43601e30b795b0bb06bc28b;hasUserBehavior=1;monitor_huoshan_web_id=7467761534115284489;referrer_title=%E5%88%9B%E5%BB%BA%E8%A7%86%E9%A2%91%E7%94%9F%E6%88%90%E4%BB%BB%E5%8A%A1%20API--%E7%81%AB%E5%B1%B1%E6%96%B9%E8%88%9F%E5%A4%A7%E6%A8%A1%E5%9E%8B%E6%9C%8D%E5%8A%A1%E5%B9%B3%E5%8F%B0-%E7%81%AB%E5%B1%B1%E5%BC%95%E6%93%8E;AccountID=2109091919;user_locale=zh;signin_i18next=zh;monitor_session_id_flag=1;monitor_traceid_base_cookie=1419;volcengineLoginMethod=pwd;_tea_utm_cache_3569={%22utm_source%22:%22coopensrc%22%2C%22utm_medium%22:%22github%22%2C%22utm_campaign%22:%22doubao%22%2C%22utm_term%22:%22project%22%2C%22utm_content%22:%22aidrawio%22};volcfe-uuid=0701f6f2-a611-4599-a2fc-57cb015ff828;userInfo=eyJhbGciOiJSUzI1NiIsImtpZCI6ImE5YzBkZmFjYmZiNDExZjA4OWMwMDAxNjNlMDcwOGJkIn0.eyJhY2NfaSI6MjEwOTA5MTkxOSwiYXVkIjpbImNvbnNvbGUudm9sY2VuZ2luZS5jb20iXSwiZXhwIjoxNzczNDk5Mzk0LCJpIjoiMjk2OTc3MmEwODIxMTFmMTlhZjEzNDM2YWMxMjAwM2YiLCJpZF9uIjoiMDQzNeaJi-acuueUqOaItyN5SFNrTXQiLCJtc2ciOm51bGwsInBpZCI6ImNkNDlmYTg3LWI3NzUtNDQwNS1iOTkzLTVmOTA0NTMyNDg5MSIsInNzX24iOiIwNDM15omL5py655So5oi3I3lIU2tNdCIsInQiOiJBY2NvdW50IiwidG9waWMiOiJzaWduaW5fdXNlcl9pbmZvIiwidmVyc2lvbiI6InYxIiwiemlwIjoiIn0.cdpiB9xgcokJBJzG-S_BIdllMusycBqNLL8VNEnmlFI5i0fYstJUbAvLC-nbouHZjLhX9XzT45RjIqbFa-f1dnQHE6SmMf_CCPuxoZOpd7UnJTbCqQiKO_KRkdshxpuIxx7mV74ziS3UQWcNARIH663BxmsMsPWFx7Tntx3QOCdu_zljgJkjbxJZhcBhGOqGC2CMZXocr0MorPpcEVtXPOsRi9ulCBMSSH4kI5z4iigbliLyoYcsD3vNCmGO_vTOPDAdyEwGE395FwAnlB62JGnwVAreHvdPLE3YFMBII2JdDT03TGOrb1VFP6tLj2xOAWCDlVJnxRkW2fDZ16d71Q;__tea_cache_tokens_3569={%22web_id%22:%227467761534115284489%22%2C%22user_unique_id%22:%227467761534115284489%22%2C%22timestamp%22:1770907429996%2C%22_type_%22:%22default%22};volc-design-locale=zh;_qimei_h38=94cee221b20e31b701a412450300000ce19c18;finance-hub-sdk-lang=zh;p_c_check=1;volc_platform_clear_user_locale=1;__spti=11_000JnXNrWATPtPrMwlQ3ilQxfn2UtC;__sptiho=0B11_000JnXNrWATPtPrMwlQ3ilQxfn2UtC_bEv/KoxCOM4AcC;_qimei_i_1=5eea2c8b9109058ec395ff62598426e3f6bca3f1130a0783b68b2d582593206c616364c03980b1ddde92f7cc;_qimei_i_3=57ca79d3970c52d9c497aa625d8027e5a6bcf0f71a5b04d4e0872b502092276d32633f973989e28184b1;_qimei_uuid42=19c180a1723100cab20e31b701a4124555c551b916;_tea_utm_cache_520918={%22utm_source%22:%22coopensrc%22%2C%22utm_medium%22:%22github%22%2C%22utm_campaign%22:%22doubao%22%2C%22utm_term%22:%22project%22%2C%22utm_content%22:%22aidrawio%22};csrfToken=499beb4542dac5d353afbb1fffd981eb;digest=eyJhbGciOiJSUzI1NiIsImtpZCI6ImE5ZDM1YTQ4YmZiNDExZjA4OWMwMDAxNjNlMDcwOGJkIn0.eyJhdWQiOlsiY29uc29sZS52b2xjZW5naW5lLmNvbSJdLCJleHAiOjE3NzEwODAxOTQsImlhdCI6MTc3MDkwNzM5NCwiaXNzIjoiaHR0cHM6Ly9zaWduaW4udm9sY2VuZ2luZS5jb20iLCJqdGkiOiJjZDQ5ZmE4Ny1iNzc1LTQ0MDUtYjk5My01ZjkwNDUzMjQ4OTEiLCJtc2ciOiJINHNJQUFBQUFBQUMvK0tTNDJMeFM4eE5GZUl5TWpTd05MQTB0RFMwbFBoNWR2c1pOb1dtYzl2UHNBbjVjN0U3SmlmbmwrYVZDSngvY09NdHU1UzRnWW14NmJQTzdtZHpkajJmc3VKWngzYmxTby9nYk44U0piQTVXbXpKK2JtNStYbGV1SlFCQWdBQS8vOTdrMG13Y1FBQUFBPT0iLCJuYW1lIjoiMDQzNeaJi-acuueUqOaItyN5SFNrTXQiLCJzdWIiOiIyMTA5MDkxOTE5IiwidG9waWMiOiJzaWduaW5fY3JlZGVudGlhbCIsInRybiI6InRybjppYW06OjIxMDkwOTE5MTk6cm9vdCIsInZlcnNpb24iOiJ2MSIsInppcCI6Imd6aXAifQ.fw4LobnAByUwIaCOWhOOvF5igRzIo_l5lBme2SmfeT5vwky01EI2iBDBayuv_O39Uvl-MzS5Gmg2-tXFN7tqEyH2ERa1ymuZETFkFu3P-su9Uqb1VZnFpkaZsjHzhCTWIxvwDLmBCZM0aLN_LOBjhDyoRjd6agYr8XLrTM3UzVRb-MUg_yYBBSttvUpZdM4pLQ3magTu0xJQY0OfLg4IBTezfg84XsQJkh0wGaJI1N-_aXTTXTFBOBahMS8fKJrNG-mgV52xMxBqS_pt3piGwn3ssMVeD5JD5K474FMKxIhgwJUkdePfsVACAjBhaLmV6AmYX4UXo7lTmjHHIZnp3Q;gfkadpd=520918,36088|3569,42874;i18next=zh;isIntranet=0;login_scene=11;monitor_session_id=0008375069127979375;monitor_tracing_cookie=[];monitor_utm=%257B%2522utm_campaign%2522%253A%2522doubao%2522%252C%2522utm_content%2522%253A%2522aidrawio%2522%252C%2522utm_medium%2522%253A%2522github%2522%252C%2522utm_source%2522%253A%2522coopensrc%2522%252C%2522utm_term%2522%253A%2522project%2522%257D;s_v_web_id=verify_mjjfj194_6wx9uxHT_RbvK_42dT_BQQF_Am4VHcR3e6qJ;top_region=;vcloudWebId=0d8e34f9-2a27-4f3b-a86a-10cb562dbf67;VOLCFE_im_uuid=1770641165069598896"""
    api_key = """ve_doc_history=82379%2C6269%2C6256%2C85128%2C86081%2C6348%2C85621%2C6260;_qimei_fingerprint=dd38b822c43601e30b795b0bb06bc28b;hasUserBehavior=1;monitor_huoshan_web_id=7467761534115284489;referrer_title=%E7%81%AB%E5%B1%B1%E5%BC%95%E6%93%8E-%E4%BD%A0%E7%9A%84AI%E4%BA%91;AccountID=2109743247;user_locale=zh;signin_i18next=zh;monitor_session_id_flag=1;monitor_traceid_base_cookie=1423;volcengineLoginMethod=pwd;_tea_utm_cache_3569={%22utm_source%22:%22coopensrc%22%2C%22utm_medium%22:%22github%22%2C%22utm_campaign%22:%22doubao%22%2C%22utm_term%22:%22project%22%2C%22utm_content%22:%22aidrawio%22};volcfe-uuid=0701f6f2-a611-4599-a2fc-57cb015ff828;userInfo=eyJhbGciOiJSUzI1NiIsImtpZCI6ImE5YzBkZmFjYmZiNDExZjA4OWMwMDAxNjNlMDcwOGJkIn0.eyJhY2NfaSI6MjEwOTc0MzI0NywiYXVkIjpbImNvbnNvbGUudm9sY2VuZ2luZS5jb20iXSwiZXhwIjoxNzczNTk2MTI5LCJpIjoiNjQ2MDRkNTIwOTAyMTFmMTlmYjgzNDM2YWMxMjAwYmUiLCJpZF9uIjoiNDgyMeaJi-acuueUqOaItyN1Wm50VHMiLCJtc2ciOm51bGwsInBpZCI6ImE4ZTk5MzUyLTBmNDUtNDRjMS04YTg1LWQ2Mzg3MmI0YzUxYyIsInNzX24iOiI0ODIx5omL5py655So5oi3I3VabnRUcyIsInQiOiJBY2NvdW50IiwidG9waWMiOiJzaWduaW5fdXNlcl9pbmZvIiwidmVyc2lvbiI6InYxIiwiemlwIjoiIn0.VFX4bvxf8qrFPQe3oZYtoUAX2WL0KpBEUZJyV5YlwPW3bDinK2QCV0i9njwGlUv-NOWiRd6qCmUtlWyX61wGKFjDIEs0luZt-LTpDntz219D2FDxim3Ez2hEA9c95D0Kymvcm_snfmx21QXIBHy4AFNpOWXcXanXHRP1rsjzItk56iGz_uCEqiXqGvDf_Z6WTMe-5U668tQhEV8izFI1CZqHVqHz0aMMfNWU8vKqGLaQZ42YFHtO1bY387UxXn7v4Hdl7zHUbRwxuUVG9x8ZeNzBHZnfD-hsVzWqi0koEX-bh3bjGhWrk6VkVIbVZBkTgXU5KURrPKq9ktKAvN7P3g;__tea_cache_tokens_3569={%22web_id%22:%227467761534115284489%22%2C%22user_unique_id%22:%227467761534115284489%22%2C%22timestamp%22:1771030034253%2C%22_type_%22:%22default%22};volc-design-locale=zh;_qimei_h38=94cee221b20e31b701a412450300000ce19c18;finance-hub-sdk-lang=zh;p_c_check=1;volc_platform_clear_user_locale=1;__spti=11_000JnXNrWATPtPrMwlQ3ilQxfn2UtC;__sptiho=0B11_000JnXNrWATPtPrMwlQ3ilQxfn2UtC_bEv/KoxCOM4AcC;_qimei_i_1=66d87f8b9109058ec395ff62598426e3f6bca3f1130a0783b68b2d582593206c616364c03980b1dddeaaa7c5;_qimei_i_3=57ca79d3970c52d9c497aa625d8027e5a6bcf0f71a5b04d4e0872b502092276d32633f973989e28184b1;_qimei_uuid42=19c180a1723100cab20e31b701a4124555c551b916;_tea_utm_cache_520918={%22utm_source%22:%22coopensrc%22%2C%22utm_medium%22:%22github%22%2C%22utm_campaign%22:%22doubao%22%2C%22utm_term%22:%22project%22%2C%22utm_content%22:%22aidrawio%22};csrfToken=3491b1a53d1625d7135f17ecb6c83301;digest=eyJhbGciOiJSUzI1NiIsImtpZCI6ImE5YzBkZmFjYmZiNDExZjA4OWMwMDAxNjNlMDcwOGJkIn0.eyJhdWQiOlsiY29uc29sZS52b2xjZW5naW5lLmNvbSJdLCJleHAiOjE3NzExNzY5MjksImlhdCI6MTc3MTAwNDEyOSwiaXNzIjoiaHR0cHM6Ly9zaWduaW4udm9sY2VuZ2luZS5jb20iLCJqdGkiOiJhOGU5OTM1Mi0wZjQ1LTQ0YzEtOGE4NS1kNjM4NzJiNGM1MWMiLCJtc2ciOiJINHNJQUFBQUFBQUMvK0tTNDJMeFM4eE5GZUl5TWpTd05EY3hOakl4bDdoOWNPOFpOb1ZISUZMSW40dmRNVGs1dnpTdlJLRC9ZTU03ZGlseEV3c2p3MmVkM2MvbTdIbytaY1d6anUzS3BWRjVKU0hGU21CenROaVM4M056OC9POGNDa0RCQUFBLy8vWVBXOFRjUUFBQUE9PSIsIm5hbWUiOiI0ODIx5omL5py655So5oi3I3VabnRUcyIsInN1YiI6IjIxMDk3NDMyNDciLCJ0b3BpYyI6InNpZ25pbl9jcmVkZW50aWFsIiwidHJuIjoidHJuOmlhbTo6MjEwOTc0MzI0Nzpyb290IiwidmVyc2lvbiI6InYxIiwiemlwIjoiZ3ppcCJ9.qwGgvtbf6DdKmtcrLLF8sAJmgyARXbn3J4sKbZXRUZWfXKMmN8hHPwXZfG41UKancOG9yxymjgFtl6NS0BAj52WxrNH4e-xC_Uelivs5Ti564sXOWBXyHRlt4zUUSuNYY_aR0AxDsZaftKP4g2ry-vLkOvAuyCFqGT8nrKSxu09fkGL-HzCYuL9U7yK7zco6Keno19c2Wlmll_ueFEkpoMBGl4i8Y4Uti6v93FfSx2KY683HCCUD78lbCFgLSmqGmJ3GLgEuxNAi2m7lex6mVCbHN40Hcn9N8dHaSmVz1EgzDIgNtAkkq5fxNwN5Iz_N0gkLfFRceMgqZbWh5h5SsA;gfkadpd=3569,42874|520918,36088;i18next=zh;isIntranet=0;login_scene=11;monitor_session_id=1896580763093473554;monitor_utm=%257B%2522utm_campaign%2522%253A%2522doubao%2522%252C%2522utm_content%2522%253A%2522aidrawio%2522%252C%2522utm_medium%2522%253A%2522github%2522%252C%2522utm_source%2522%253A%2522coopensrc%2522%252C%2522utm_term%2522%253A%2522project%2522%257D;s_v_web_id=verify_mjjfj194_6wx9uxHT_RbvK_42dT_BQQF_Am4VHcR3e6qJ;top_region=;user_locale=zh;vcloudWebId=0d8e34f9-2a27-4f3b-a86a-10cb562dbf67;VOLCFE_im_uuid=1770641165069598896"""

    api_key = """ve_doc_history=82379%2C6269%2C6256%2C85128%2C86081%2C6348%2C85621%2C6260;_qimei_fingerprint=dd38b822c43601e30b795b0bb06bc28b;hasUserBehavior=1;monitor_huoshan_web_id=7467761534115284489;referrer_title=;AccountID=2119178640;user_locale=zh;signin_i18next=zh;monitor_session_id_flag=1;monitor_traceid_base_cookie=1438;volcengineLoginMethod=pwd;_tea_utm_cache_3569={%22utm_source%22:%22coopensrc%22%2C%22utm_medium%22:%22github%22%2C%22utm_campaign%22:%22doubao%22%2C%22utm_term%22:%22project%22%2C%22utm_content%22:%22aidrawio%22};volcfe-uuid=0701f6f2-a611-4599-a2fc-57cb015ff828;userInfo=eyJhbGciOiJSUzI1NiIsImtpZCI6ImE5YzBkZmFjYmZiNDExZjA4OWMwMDAxNjNlMDcwOGJkIn0.eyJhY2NfaSI6MjExOTE3ODY0MCwiYXVkIjpbImNvbnNvbGUudm9sY2VuZ2luZS5jb20iXSwiZXhwIjoxNzczNzE5OTMwLCJpIjoiYTM2NWVmMzgwYTIyMTFmMTljZDEzNDM2YWMxMjAwY2YiLCJpZF9uIjoiNjExNOaJi-acuueUqOaItyNLS3ZyY3QiLCJtc2ciOm51bGwsInBpZCI6ImY3NmFjNWJhLTNhY2EtNDNjMy04NjNlLTZjYjU1OGRlMTc0NiIsInNzX24iOiI2MTE05omL5py655So5oi3I0tLdnJjdCIsInQiOiJBY2NvdW50IiwidG9waWMiOiJzaWduaW5fdXNlcl9pbmZvIiwidmVyc2lvbiI6InYxIiwiemlwIjoiIn0.lB10e3xw0GomkyYxkdvjk9avGg0lpV1zFP2rHiNeSQaieG4h6UQbc0coEYIH68c0VOEG997IKqsjaUfGTxo45t3zm3Ht2FfgpPKPCyItrxgP4RNmczbizKJkoos6v4YBUXOgVkjJFRnFcIGXGn8B6k9qw8rmutOfHXDOYGrYQpSn3bVtKOA0tZIHFgJ8LRWi0TfI3wq-v5nwkpgygt2k6hmHO9kWRRp-3lj5vm9Tb0vAY2oCPj0B5gTQ4-6_rTn88tR_N3CDZxbJzIP-Ifdph_MLy-Fl1qTNSZlaEtvi0xeIP7d4W5wY9m7zU-t9Ytq2ORyR9HkszXNtH6uEhyG_9g;__tea_cache_tokens_3569={%22web_id%22:%227467761534115284489%22%2C%22user_unique_id%22:%227467761534115284489%22%2C%22timestamp%22:1771131957865%2C%22_type_%22:%22default%22};volc-design-locale=zh;_qimei_h38=94cee221b20e31b701a412450300000ce19c18;finance-hub-sdk-lang=zh;verify_mjjfj194_6wx9uxHT_RbvK_42dT_BQQF_Am4VHcR3e6qJ=1;p_c_check=1;volc_platform_clear_user_locale=1;__spti=11_000JnXNrWATPtPrMwlQ3ilQxfn2UtC;__sptiho=0B11_000JnXNrWATPtPrMwlQ3ilQxfn2UtC_bEv/KoxCOM4AcC;_qimei_i_1=5ae14e8b9109058ec395ff62598426e3f6bca3f1130a0783b68b2d582593206c616364c03980b1dddeb1a086;_qimei_i_3=57ca79d3970c52d9c497aa625d8027e5a6bcf0f71a5b04d4e0872b502092276d32633f973989e28184b1;_qimei_uuid42=19c180a1723100cab20e31b701a4124555c551b916;_tea_utm_cache_520918={%22utm_source%22:%22coopensrc%22%2C%22utm_medium%22:%22github%22%2C%22utm_campaign%22:%22doubao%22%2C%22utm_term%22:%22project%22%2C%22utm_content%22:%22aidrawio%22};csrfToken=09ebbbf8543acc10e9d0ee26b10ccd3f;digest=eyJhbGciOiJSUzI1NiIsImtpZCI6ImE5YzBkZmFjYmZiNDExZjA4OWMwMDAxNjNlMDcwOGJkIn0.eyJhdWQiOlsiY29uc29sZS52b2xjZW5naW5lLmNvbSJdLCJleHAiOjE3NzEzMDA3MzAsImlhdCI6MTc3MTEyNzkzMCwiaXNzIjoiaHR0cHM6Ly9zaWduaW4udm9sY2VuZ2luZS5jb20iLCJqdGkiOiJmNzZhYzViYS0zYWNhLTQzYzMtODYzZS02Y2I1NThkZTE3NDYiLCJtc2ciOiJINHNJQUFBQUFBQUMvK0tTNDJMeFM4eE5GZUl5TWpTME5EUzNNRE14a1BqYWNmUU1tOEp2RUNua3o4WHVtSnljWDVwWElqQmg4NEZQN0ZMaVpvYUdKczg2dTUvTjJmVjh5b3BuSGR1VnZiM0xpcEpMbE1EbWFMRWw1K2ZtNXVkNTRWSUdDQUFBLy8vN0p1MFVjUUFBQUE9PSIsIm5hbWUiOiI2MTE05omL5py655So5oi3I0tLdnJjdCIsInN1YiI6IjIxMTkxNzg2NDAiLCJ0b3BpYyI6InNpZ25pbl9jcmVkZW50aWFsIiwidHJuIjoidHJuOmlhbTo6MjExOTE3ODY0MDpyb290IiwidmVyc2lvbiI6InYxIiwiemlwIjoiZ3ppcCJ9.Z8e2jIe4nxWmKsAv0poWymn-Ih1ozdNYnfE6pAcQrhJZD50JGC68mjcPaEBwD4GyizR_TM_C8-B0NI2agxhiKHZ-Skb-b8v9Cs2LoVgtXOXGI-fk-ShSzoHQSZRhNSLaInVoo5XsxpKNWXTwGI919i3dlwSCVk2IrCFxSsj6VZHGLGyuudjrS7KWHiWYdIhJ8fF3dMN7KPD9M1woGcW7fVogvSvWwx8e8Whxzcy_Oiec__mOz4pmyzw5Un3CRiOQc6jurdCrqj_T1Iyp8xXdjUvLS2xIqYOHC7zFi24aTVUwiXTtjEitBQDAY0DjTFpBANNzBTVyOU-fS929pCgVuA;gfkadpd=3569,42874|520918,36088;i18next=zh;isIntranet=0;login_scene=11;monitor_session_id=4541778874643941547;monitor_utm=%257B%2522utm_campaign%2522%253A%2522doubao%2522%252C%2522utm_content%2522%253A%2522aidrawio%2522%252C%2522utm_medium%2522%253A%2522github%2522%252C%2522utm_source%2522%253A%2522coopensrc%2522%252C%2522utm_term%2522%253A%2522project%2522%257D;s_v_web_id=verify_mjjfj194_6wx9uxHT_RbvK_42dT_BQQF_Am4VHcR3e6qJ;top_region=;user_locale=zh;vcloudWebId=0d8e34f9-2a27-4f3b-a86a-10cb562dbf67;VOLCFE_im_uuid=1770641165069598896"""

    api_key = """volc_platform_clear_user_locale=1; p_c_check=1; vcloudWebId=11c7ef64-f16e-4289-a696-1fdcf3fc468e; user_locale=zh; monitor_huoshan_web_id=8691040921984375872; monitor_session_id_flag=1; volc-design-locale=zh; isIntranet=0; VOLCFE_im_uuid=1771005499155462938; login_scene=11; volcengineLoginMethod=pwd; i18next=zh; s_v_web_id=verify_mll6ykev_CGHduuU2_f3X8_4fEs_8O4E_8xc0LEWpy3id; finance-hub-sdk-lang=zh; gfkadpd=3569,42874|520918,36088; monitor_traceid_base_cookie=2; verify_mll6ykev_CGHduuU2_f3X8_4fEs_8O4E_8xc0LEWpy3id=1; digest=eyJhbGciOiJSUzI1NiIsImtpZCI6ImE5YzBkZmFjYmZiNDExZjA4OWMwMDAxNjNlMDcwOGJkIn0.eyJhdWQiOlsiY29uc29sZS52b2xjZW5naW5lLmNvbSJdLCJleHAiOjE3NzEyNjM0MjYsImlhdCI6MTc3MTA5MDYyNiwiaXNzIjoiaHR0cHM6Ly9zaWduaW4udm9sY2VuZ2luZS5jb20iLCJqdGkiOiJhY2VkMGM0ZS1jMTQwLTQ0Y2EtOWQxYi0wZDIwN2VkNDU5M2UiLCJtc2ciOiJINHNJQUFBQUFBQUMvK0tTNDJMeFM4eE5GZUl5TWpTME5EUTNNekV5bFZqLzlOQVpOb1ZESUZMSW40dmRNVGs1dnpTdlJPRGx3Z09mMktYRXpVMHR6WjUxZGorYnMrdjVsQlhQT3JZcjUxVlVoUGtYS29ITjBXSkx6cy9OemMvendxVU1FQUFBLy8vM3Y0MDJjUUFBQUE9PSIsIm5hbWUiOiI3NTk25omL5py655So5oi3I254eFZPcSIsInN1YiI6IjIxMTkxNzY0MjUiLCJ0b3BpYyI6InNpZ25pbl9jcmVkZW50aWFsIiwidHJuIjoidHJuOmlhbTo6MjExOTE3NjQyNTpyb290IiwidmVyc2lvbiI6InYxIiwiemlwIjoiZ3ppcCJ9.S1BuXwVp53CVknYjR5CDg2Fi-uUtbAAlA2raKK1TBkWVY8ti83xEI69Tm-2PC7TqKRp3DuKyL8PLNH1mXpCdsncyyrn8HLMgaqar72m4vYenvXfkerZJPRmJ5oa6ZsYQ8dWvUfzvYiDvwgFHeLukAfIM9bWu3Jd4mpg8F9hWzHKkvCOgGBkze__24fUJce8xnyljRC916eY7pMe-QR5C9jIWBV-qH9tXvW698lYjqv3DTFPwUXLojwdXkyZS9D05fsbXLyvWr60lYG_20oX_2EVk1i5Hgsm4QTSU3brawVfCYsS6FYHvod7umYU9MVvXnhVrVK57hPzlCOL3gN564w; digest=eyJhbGciOiJSUzI1NiIsImtpZCI6ImE5YzBkZmFjYmZiNDExZjA4OWMwMDAxNjNlMDcwOGJkIn0.eyJhdWQiOlsiY29uc29sZS52b2xjZW5naW5lLmNvbSJdLCJleHAiOjE3NzEyNjM0MjYsImlhdCI6MTc3MTA5MDYyNiwiaXNzIjoiaHR0cHM6Ly9zaWduaW4udm9sY2VuZ2luZS5jb20iLCJqdGkiOiJhY2VkMGM0ZS1jMTQwLTQ0Y2EtOWQxYi0wZDIwN2VkNDU5M2UiLCJtc2ciOiJINHNJQUFBQUFBQUMvK0tTNDJMeFM4eE5GZUl5TWpTME5EUTNNekV5bFZqLzlOQVpOb1ZESUZMSW40dmRNVGs1dnpTdlJPRGx3Z09mMktYRXpVMHR6WjUxZGorYnMrdjVsQlhQT3JZcjUxVlVoUGtYS29ITjBXSkx6cy9OemMvendxVU1FQUFBLy8vM3Y0MDJjUUFBQUE9PSIsIm5hbWUiOiI3NTk25omL5py655So5oi3I254eFZPcSIsInN1YiI6IjIxMTkxNzY0MjUiLCJ0b3BpYyI6InNpZ25pbl9jcmVkZW50aWFsIiwidHJuIjoidHJuOmlhbTo6MjExOTE3NjQyNTpyb290IiwidmVyc2lvbiI6InYxIiwiemlwIjoiZ3ppcCJ9.S1BuXwVp53CVknYjR5CDg2Fi-uUtbAAlA2raKK1TBkWVY8ti83xEI69Tm-2PC7TqKRp3DuKyL8PLNH1mXpCdsncyyrn8HLMgaqar72m4vYenvXfkerZJPRmJ5oa6ZsYQ8dWvUfzvYiDvwgFHeLukAfIM9bWu3Jd4mpg8F9hWzHKkvCOgGBkze__24fUJce8xnyljRC916eY7pMe-QR5C9jIWBV-qH9tXvW698lYjqv3DTFPwUXLojwdXkyZS9D05fsbXLyvWr60lYG_20oX_2EVk1i5Hgsm4QTSU3brawVfCYsS6FYHvod7umYU9MVvXnhVrVK57hPzlCOL3gN564w; AccountID=2119176425; AccountID=2119176425; userInfo=eyJhbGciOiJSUzI1NiIsImtpZCI6ImE5YzBkZmFjYmZiNDExZjA4OWMwMDAxNjNlMDcwOGJkIn0.eyJhY2NfaSI6MjExOTE3NjQyNSwiYXVkIjpbImNvbnNvbGUudm9sY2VuZ2luZS5jb20iXSwiZXhwIjoxNzczNjgyNjI2LCJpIjoiYzdmYjM3ZmUwOWNiMTFmMTkzNTAzNDM2YWMxMjAwYTgiLCJpZF9uIjoiNzU5NuaJi-acuueUqOaItyNueHhWT3EiLCJtc2ciOm51bGwsInBpZCI6ImFjZWQwYzRlLWMxNDAtNDRjYS05ZDFiLTBkMjA3ZWQ0NTkzZSIsInNzX24iOiI3NTk25omL5py655So5oi3I254eFZPcSIsInQiOiJBY2NvdW50IiwidG9waWMiOiJzaWduaW5fdXNlcl9pbmZvIiwidmVyc2lvbiI6InYxIiwiemlwIjoiIn0.YlVVx-SxvltrEhjupyi5Ij3bNl3MWNYOn7hjbI0bm1eKgpYFLraMhDFWD2bgMsH1eEObHaV2tGB-SyEHL0zOy4MRjShlw3fXkix846KLjqOy5VHTJf_o7AnOOZXEsV-wZR1F48NXSabcd5uPr1M94W2-FfGCixARde0cWo3cxW5tL-C7g4sFKE04lL6R2p6GPjVAqfgCnJcJFG9axIFP4Y4-9F70svB0pGD4p7lkjxWW-r7WCmGlFRezBHLBhql7CVnOYmjfUr_nDBDU6G8JxVL8SLRHN5d8vhoClwq8FJrzb8qaoxbyhaTqEZ2osHVT4rOBlPYFGF638SDZvg5PSw; csrfToken=f48ebe0bdcaa711c41af50f14ddeac66; csrfToken=f48ebe0bdcaa711c41af50f14ddeac66; user_locale=zh; monitor_session_id=5508498656706438250; __tea_cache_tokens_3569={%22web_id%22:%227606410636642240036%22%2C%22user_unique_id%22:%227606410636642240036%22%2C%22timestamp%22:1771132529352%2C%22_type_%22:%22default%22}"""
    api_key = """monitor_huoshan_web_id=5580802690475581165; user_locale=zh; i18next=zh; volcfe-uuid=3638eba7-a4ed-40f3-976e-aade7b4913cf; hasUserBehavior=1; iaas_global_region=cn-beijing; connect.sid=s%3A46e3c0e7-20a2-4155-94fe-b3bce9edb860.nGJw45VefU8pAZ0%2BCE2eTFCLztzlVbmTQifs0O3e6Ck; vcloudWebId=404de0e8-1e9d-4786-ba76-187feb018352; monitor_session_id_flag=1; volc-design-locale=zh; signin_i18next=zh; finance-hub-sdk-lang=zh; top_region=; p_c_check=1; s_v_web_id=verify_mjqg5k9s_WbrSrTd8_T1XG_46c8_9Bu4_3MbAyFhknxHb; __spti=11_000JnIKZEO2PtPrMwlQ3ilQxfn2UtC; __sptiho=4D11_000JnIKZEO2PtPrMwlQ3ilQxfn2UtC_bEv/KoxCOM4AcC; __spti=11_000JnIKZEO2PtPrMwlQ3ilQxfn2UtC; __sptiho=4D11_000JnIKZEO2PtPrMwlQ3ilQxfn2UtC_bEv/KoxCOM4AcC; volc_platform_clear_user_locale=1; ve_doc_history=82379%2C6269; VOLCFE_im_uuid=1771059509799536691; login_scene=11; volcengineLoginMethod=pwd; gfkadpd=3569,42874|520918,36088; monitor_session_id=7826853238708166961; isIntranet=0; referrer_title=Seedance%202.0%20&%20Seedream%205.0%20%E5%85%8D%E8%B4%B9%E4%BD%93%E9%AA%8C%20-%20%E7%81%AB%E5%B1%B1%E5%BC%95%E6%93%8E%20AI%20%E4%BD%93%E9%AA%8C%E4%B8%AD%E5%BF%83; monitor_traceid_base_cookie=28; digest=eyJhbGciOiJSUzI1NiIsImtpZCI6ImE5YzBkZmFjYmZiNDExZjA4OWMwMDAxNjNlMDcwOGJkIn0.eyJhdWQiOlsiY29uc29sZS52b2xjZW5naW5lLmNvbSJdLCJleHAiOjE3NzEzMjUxMTMsImlhdCI6MTc3MTE1MjMxMywiaXNzIjoiaHR0cHM6Ly9zaWduaW4udm9sY2VuZ2luZS5jb20iLCJqdGkiOiJhODM1ZjJlZS01YTk2LTQyNDUtYWU2Yy03ZmNkNmIwZTBiNzQiLCJtc2ciOiJINHNJQUFBQUFBQUMvK0tTNDJMeFM4eE5GZUl5TWpRd05iRTBOckUwbE5oeS9OZ1pOb1ZkSUZMSW40dmRNVGs1dnpTdlJPQnovOS9YN0ZMaWxtWkdaczg2dTUvTjJmVjh5b3BuSGR1Vk0xeENnbDBybE1EbWFMRWw1K2ZtNXVkNTRWSUdDQUFBLy8vcnpPM3djUUFBQUE9PSIsIm5hbWUiOiI5NjI25omL5py655So5oi3I2hEVFNFeCIsInN1YiI6IjIxMDU0OTM0OTEiLCJ0b3BpYyI6InNpZ25pbl9jcmVkZW50aWFsIiwidHJuIjoidHJuOmlhbTo6MjEwNTQ5MzQ5MTpyb290IiwidmVyc2lvbiI6InYxIiwiemlwIjoiZ3ppcCJ9.DD439j5uhR5kOD0Yz12A0W6K8UljLoGFNRcjStL0bXav4Ml7TjY6fz-k1tsdKB0eGzH5HUL0s9nzS1vv02am1BN1XgweA1pgK8gdeV1uoVXAz9sfccBdhWTKFPES1Pmev4nNp4YpcHIIF50p84sVe65-d9GoBINYlzDr45hqBEwm4jJ1b2ncpJUuMPnXnYN6q4ZYrXx2ErJVTvYlFLOekNtaEssRSv1fMiy8TEYtVp-Ta0_DKuhN7wPa2hhM-EbuYLPUuj3eBZea5VjyQ6Ii0xnjt0VuCMeES82ZFT8kfI_jfDdQNoojD0aII1hpKnYfixxBhmAtRpglA2qYen5Rdg; digest=eyJhbGciOiJSUzI1NiIsImtpZCI6ImE5YzBkZmFjYmZiNDExZjA4OWMwMDAxNjNlMDcwOGJkIn0.eyJhdWQiOlsiY29uc29sZS52b2xjZW5naW5lLmNvbSJdLCJleHAiOjE3NzEzMjUxMTMsImlhdCI6MTc3MTE1MjMxMywiaXNzIjoiaHR0cHM6Ly9zaWduaW4udm9sY2VuZ2luZS5jb20iLCJqdGkiOiJhODM1ZjJlZS01YTk2LTQyNDUtYWU2Yy03ZmNkNmIwZTBiNzQiLCJtc2ciOiJINHNJQUFBQUFBQUMvK0tTNDJMeFM4eE5GZUl5TWpRd05iRTBOckUwbE5oeS9OZ1pOb1ZkSUZMSW40dmRNVGs1dnpTdlJPQnovOS9YN0ZMaWxtWkdaczg2dTUvTjJmVjh5b3BuSGR1Vk0xeENnbDBybE1EbWFMRWw1K2ZtNXVkNTRWSUdDQUFBLy8vcnpPM3djUUFBQUE9PSIsIm5hbWUiOiI5NjI25omL5py655So5oi3I2hEVFNFeCIsInN1YiI6IjIxMDU0OTM0OTEiLCJ0b3BpYyI6InNpZ25pbl9jcmVkZW50aWFsIiwidHJuIjoidHJuOmlhbTo6MjEwNTQ5MzQ5MTpyb290IiwidmVyc2lvbiI6InYxIiwiemlwIjoiZ3ppcCJ9.DD439j5uhR5kOD0Yz12A0W6K8UljLoGFNRcjStL0bXav4Ml7TjY6fz-k1tsdKB0eGzH5HUL0s9nzS1vv02am1BN1XgweA1pgK8gdeV1uoVXAz9sfccBdhWTKFPES1Pmev4nNp4YpcHIIF50p84sVe65-d9GoBINYlzDr45hqBEwm4jJ1b2ncpJUuMPnXnYN6q4ZYrXx2ErJVTvYlFLOekNtaEssRSv1fMiy8TEYtVp-Ta0_DKuhN7wPa2hhM-EbuYLPUuj3eBZea5VjyQ6Ii0xnjt0VuCMeES82ZFT8kfI_jfDdQNoojD0aII1hpKnYfixxBhmAtRpglA2qYen5Rdg; AccountID=2105493491; AccountID=2105493491; userInfo=eyJhbGciOiJSUzI1NiIsImtpZCI6ImE5ZDM1YTQ4YmZiNDExZjA4OWMwMDAxNjNlMDcwOGJkIn0.eyJhY2NfaSI6MjEwNTQ5MzQ5MSwiYXVkIjpbImNvbnNvbGUudm9sY2VuZ2luZS5jb20iXSwiZXhwIjoxNzczNzQ0MzEzLCJpIjoiNjhjNjZlNjYwYTViMTFmMTg2NTIzNDM2YWMxMjAwOTciLCJpZF9uIjoiOTYyNuaJi-acuueUqOaItyNoRFRTRXgiLCJtc2ciOm51bGwsInBpZCI6ImE4MzVmMmVlLTVhOTYtNDI0NS1hZTZjLTdmY2Q2YjBlMGI3NCIsInNzX24iOiI5NjI25omL5py655So5oi3I2hEVFNFeCIsInQiOiJBY2NvdW50IiwidG9waWMiOiJzaWduaW5fdXNlcl9pbmZvIiwidmVyc2lvbiI6InYxIiwiemlwIjoiIn0.S615RupKSuNbmZCRYqgjkb7lgkaUwWO_8QwBZRt9jxBWPUZgFS3tNUTU8hUB7KDfKa0ThN_lsPF48gPxrraah5kUMXAGEuy_5ZfHGb4WpUc44x2viroq-LFFayUX_UpH7AVTEqE8uwyFrECTbxf40USt0m4LvaM8pUaQiOcalhD4fYgi8dDyYW89OUdnlTx7zBrGMmIqr9kmirMmW95HpPeMQS41kqIJAttR_a76HEMJ4Qhqk6vkvADnH24MDQEjr2bc0-emuhq0Dqm1uYhpC_O3AOCp57ynnL-8xAM-9Y0p5T3Gw8X3qJ-ULVkY7NSPlDL8CJPcr_59rFmLgY1q_A; csrfToken=3ae514fef8bca9bbf57567607ad4d189; csrfToken=3ae514fef8bca9bbf57567607ad4d189; user_locale=zh; __tea_cache_tokens_3569={%22web_id%22:%227584046438867830326%22%2C%22user_unique_id%22:%227584046438867830326%22%2C%22timestamp%22:1771154552721%2C%22_type_%22:%22default%22}"""

    api_key = "ve_doc_history=6737%2C82379%2C6269%2C6256%2C85128%2C86081%2C6348%2C85621%2C6260;_qimei_fingerprint=806c1f7b65af4e75c90d884b4816e760;hasUserBehavior=1;monitor_huoshan_web_id=7467761534115284489;referrer_title=%E5%8A%A0%E9%80%9F%E5%99%A8%E8%B4%B9--%E5%85%A8%E7%90%83%E5%8A%A0%E9%80%9F-%E7%81%AB%E5%B1%B1%E5%BC%95%E6%93%8E;AccountID=2119209864;user_locale=zh;signin_i18next=zh;monitor_session_id_flag=1;monitor_traceid_base_cookie=1465;volcengineLoginMethod=pwd;_tea_utm_cache_3569={%22utm_source%22:%22coopensrc%22%2C%22utm_medium%22:%22github%22%2C%22utm_campaign%22:%22doubao%22%2C%22utm_term%22:%22project%22%2C%22utm_content%22:%22aidrawio%22};volcfe-uuid=0701f6f2-a611-4599-a2fc-57cb015ff828;userInfo=eyJhbGciOiJSUzI1NiIsImtpZCI6ImE5ZDM1YTQ4YmZiNDExZjA4OWMwMDAxNjNlMDcwOGJkIn0.eyJhY2NfaSI6MjExOTIwOTg2NCwiYXVkIjpbImNvbnNvbGUudm9sY2VuZ2luZS5jb20iXSwiZXhwIjoxNzc0MTU5NTE3LCJpIjoiMjE5ODZkMmMwZTIyMTFmMWE2Y2UzNDM2YWMxMjAwYTYiLCJpZF9uIjoiOSNwVDQ1dkYiLCJtc2ciOm51bGwsInBpZCI6Ijk1YzA1ZGJiLWFiNDItNGEzOC05ZGI5LWViZjBiOTc2YTk3NyIsInNzX24iOiI5I3BUNDV2RiIsInQiOiJBY2NvdW50IiwidG9waWMiOiJzaWduaW5fdXNlcl9pbmZvIiwidmVyc2lvbiI6InYxIiwiemlwIjoiIn0.A9_jA3otkIw-leG3V621Iy0uVT8uZ5n-zwYMd0Qda3DTAzpWFYnrS5cR2WcBMx_ELBbewdNdMwwgOC46Few9KKGakBs-uqgNA-hx0F9eibnlbvB2DxNjT2jWwTucH7sABsBiAARPwol-oTBjqDjFogjD5aN-AMu5uF4grxfuDCegEo0YlgNI2RLMILacIt9ALJgIi95LksFx2FcFSReeA72gfqQhLLO9VdVyAGj_un8KjYgc19DadphanLfZkBiPNBGDoTS1WOUWyi67imSJAZ1uN1XIJzI95K7BwONmp12SmlYhInwfIMbFOh9fcXWgaLfphqZjH4MKfHry9ByG1A;__tea_cache_tokens_3569={%22web_id%22:%227467761534115284489%22%2C%22user_unique_id%22:%227467761534115284489%22%2C%22timestamp%22:1771582578470%2C%22_type_%22:%22default%22};volc-design-locale=zh;_qimei_h38=94cee221b20e31b701a412450300000ce19c18;finance-hub-sdk-lang=zh;p_c_check=1;volc_platform_clear_user_locale=1;__spti=11_000JnXNrWATPtPrMwlQ3ilQxfn2UtC;__sptiho=0B11_000JnXNrWATPtPrMwlQ3ilQxfn2UtC_bEv/KoxCOM4AcC;_qimei_i_1=2de24d8b9109058ec395ff62598426e3f6bca3f1130a0783b68b2d582593206c616364c03980b1ddde8ee3f7;_qimei_i_3=57ca79d3970c52d9c497aa625d8027e5a6bcf0f71a5b04d4e0872b502092276d32633f973989e28184b1;_qimei_uuid42=19c180a1723100cab20e31b701a4124555c551b916;_tea_utm_cache_520918={%22utm_source%22:%22coopensrc%22%2C%22utm_medium%22:%22github%22%2C%22utm_campaign%22:%22doubao%22%2C%22utm_term%22:%22project%22%2C%22utm_content%22:%22aidrawio%22};csrfToken=5b1d164416317526dd4419ac3915a217;digest=eyJhbGciOiJSUzI1NiIsImtpZCI6ImE5ZDM1YTQ4YmZiNDExZjA4OWMwMDAxNjNlMDcwOGJkIn0.eyJhdWQiOlsiY29uc29sZS52b2xjZW5naW5lLmNvbSJdLCJleHAiOjE3NzE3NDAzMTcsImlhdCI6MTc3MTU2NzUxNywiaXNzIjoiaHR0cHM6Ly9zaWduaW4udm9sY2VuZ2luZS5jb20iLCJqdGkiOiI5NWMwNWRiYi1hYjQyLTRhMzgtOWRiOS1lYmYwYjk3NmE5NzciLCJtc2ciOiJINHNJQUFBQUFBQUMvK0tTNFdMeFM4eE5GZUt3VkM0SU1URXRjNU9ZL3ZuK0dUYUZlU0JTeUpDTDNURTVPYjgwcjBTZ1kvbWhUK3hTY0dWS1lHMWFiTW41dWJuNWVWNXdjVUFBQUFELy96QXhuczlSQUFBQSIsIm5hbWUiOiI5I3BUNDV2RiIsInN1YiI6IjIxMTkyMDk4NjQiLCJ0b3BpYyI6InNpZ25pbl9jcmVkZW50aWFsIiwidHJuIjoidHJuOmlhbTo6MjExOTIwOTg2NDpyb290IiwidmVyc2lvbiI6InYxIiwiemlwIjoiZ3ppcCJ9.OOvCLyhuxySzAhB3ibcI9D11qL9FoIVGTAsP6D4TdCPBniseUKszsbA-Y8j96JbeQdeBq4bcTa6evcVYvjh5AXj-SHDa2QjUbBvtdCfWCUz1GW6FK_n2J3XynKs-CK0bheqSEqnh2TP4eF7sBGIaUZmEeqYm5QDE4BPgbRxwUv0fRqwSa__Se332vSR123rFNKKfKXAAdFOThZx4TtXEuBB1i_F-b0MdDP7g_Ww_twB5b-RCG4lLyEZ98_z3kKfFAqcN5A_ZrKTF686fWG5IG_T-ur2diVpluISM8tUtctU-EQtgeopEujBIjaWcUntNCIokYBmxweq3FoxRptoC1w;gfkadpd=3569,42874|520918,36088;i18next=zh;isIntranet=0;login_scene=11;monitor_session_id=2576916771251209228;monitor_utm=%257B%2522utm_campaign%2522%253A%2522doubao%2522%252C%2522utm_content%2522%253A%2522aidrawio%2522%252C%2522utm_medium%2522%253A%2522github%2522%252C%2522utm_source%2522%253A%2522coopensrc%2522%252C%2522utm_term%2522%253A%2522project%2522%257D;s_v_web_id=verify_mjjfj194_6wx9uxHT_RbvK_42dT_BQQF_Am4VHcR3e6qJ;top_region=;user_locale=zh;vcloudWebId=0d8e34f9-2a27-4f3b-a86a-10cb562dbf67;VOLCFE_im_uuid=1771247302981950646"

    api_key = "ve_doc_history=82379%2C6737%2C6269%2C6256%2C85128%2C86081%2C6348%2C85621%2C6260;_qimei_fingerprint=3c9496c87e8b87997f776282bebdd3a6;hasUserBehavior=1;monitor_huoshan_web_id=7467761534115284489;referrer_title=%E5%A5%97%E9%A4%90%E6%A6%82%E8%A7%88--%E7%81%AB%E5%B1%B1%E6%96%B9%E8%88%9F%E5%A4%A7%E6%A8%A1%E5%9E%8B%E6%9C%8D%E5%8A%A1%E5%B9%B3%E5%8F%B0-%E7%81%AB%E5%B1%B1%E5%BC%95%E6%93%8E;AccountID=2119860253;user_locale=zh;signin_i18next=zh;monitor_session_id_flag=1;monitor_traceid_base_cookie=1515;volcengineLoginMethod=pwd;_tea_utm_cache_3569={%22utm_source%22:%22coopensrc%22%2C%22utm_medium%22:%22github%22%2C%22utm_campaign%22:%22doubao%22%2C%22utm_term%22:%22project%22%2C%22utm_content%22:%22aidrawio%22};volcfe-uuid=0701f6f2-a611-4599-a2fc-57cb015ff828;userInfo=eyJhbGciOiJSUzI1NiIsImtpZCI6ImE5YzBkZmFjYmZiNDExZjA4OWMwMDAxNjNlMDcwOGJkIn0.eyJhY2NfaSI6MjExOTg2MDI1MywiYXVkIjpbImNvbnNvbGUudm9sY2VuZ2luZS5jb20iXSwiZXhwIjoxNzc0NTAwMjI1LCJpIjoiNjcxZDBkNTAxMTNiMTFmMTgwNjIzNDM2YWMxMjAwNWEiLCJpZF9uIjoiNUhsIzl1OCNGN3MiLCJtc2ciOm51bGwsInBpZCI6ImI5MzhiYmNkLTJlZTEtNDMwNi05YWVlLTU2M2U4N2ZjMGRhNiIsInNzX24iOiI1SGwjOXU4I0Y3cyIsInQiOiJBY2NvdW50IiwidG9waWMiOiJzaWduaW5fdXNlcl9pbmZvIiwidmVyc2lvbiI6InYxIiwiemlwIjoiIn0.a6vcEqjjLowvb0IcmkrNwwtGvHkUN3PDZN7hbGSriKkAHxPquL5JKlfOcPk1T7p4tDhleljI6voQ3OWytFDKxuan0umCB-ln_BS6XT6sXMpc5TWOkJiZ3gMBBWAoiej-PgthTbFKjNNlMeZyvuLbfOeqaAsDV4NcSQndpBBXf3H3kFLMuv1z3tBBtPAOiUHgEnwHMJGbQiK0lylD9pMT4uD2-sGdxVh8YDqoKbZIuwLDYUIDLJe2v4q8M-a-7hdyBrBwdT3mg6l5Bk1FvjLdVq42a0X5iePgvsS0pTZw6Ef79Z1yOTLipSCHBkgbRtj-UJr35scJGK4C7yIG1GEuGw;__tea_cache_tokens_3569={%22web_id%22:%227467761534115284489%22%2C%22user_unique_id%22:%227467761534115284489%22%2C%22timestamp%22:1771934312342%2C%22_type_%22:%22default%22};volc-design-locale=zh;_qimei_h38=94cee221b20e31b701a412450300000ce19c18;finance-hub-sdk-lang=zh;p_c_check=1;volc_platform_clear_user_locale=1;__spti=11_000JnXNrWATPtPrMwlQ3ilQxfn2UtC;__sptiho=0B11_000JnXNrWATPtPrMwlQ3ilQxfn2UtC_bEv/KoxCOM4AcC;_qimei_i_1=64bb2b8b9109058ec395ff62598426e3f6bca3f1130a0783b68b2d582593206c616364c03980b1ddde91a7e1;_qimei_i_3=57ca79d3970c52d9c497aa625d8027e5a6bcf0f71a5b04d4e0872b502092276d32633f973989e28184b1;_qimei_uuid42=19c180a1723100cab20e31b701a4124555c551b916;_tea_utm_cache_520918={%22utm_source%22:%22coopensrc%22%2C%22utm_medium%22:%22github%22%2C%22utm_campaign%22:%22doubao%22%2C%22utm_term%22:%22project%22%2C%22utm_content%22:%22aidrawio%22};csrfToken=80e88dd73a98177c2e5260ce80e8b71c;digest=eyJhbGciOiJSUzI1NiIsImtpZCI6ImE5YzBkZmFjYmZiNDExZjA4OWMwMDAxNjNlMDcwOGJkIn0.eyJhdWQiOlsiY29uc29sZS52b2xjZW5naW5lLmNvbSJdLCJleHAiOjE3NzIwODEwMjUsImlhdCI6MTc3MTkwODIyNSwiaXNzIjoiaHR0cHM6Ly9zaWduaW4udm9sY2VuZ2luZS5jb20iLCJqdGkiOiJiOTM4YmJjZC0yZWUxLTQzMDYtOWFlZS01NjNlODdmYzBkYTYiLCJtc2ciOiJINHNJQUFBQUFBQUMvK0tTNTJMeFM4eE5GZUkyOWNoUnRpeTFVSFl6TDViNGVlUExHVGFGeHB0ZnpyQUptWE94T3lZbjU1Zm1sUWpNYlhqMWlWMEtXYVVTV0xNV1czSitibTUrbmhleUZDQUFBUC8vcTI5SUdsb0FBQUE9IiwibmFtZSI6IjVIbCM5dTgjRjdzIiwic3ViIjoiMjExOTg2MDI1MyIsInRvcGljIjoic2lnbmluX2NyZWRlbnRpYWwiLCJ0cm4iOiJ0cm46aWFtOjoyMTE5ODYwMjUzOnJvb3QiLCJ2ZXJzaW9uIjoidjEiLCJ6aXAiOiJnemlwIn0.WXBqI7QBDR3mde4nnTZj3TOy2LwCGymhCyRPYb3MlxLfTF8NFKAeOpNuJR2T-KtsEg1i469FozQGoUrXdIN5KVOetDeEWdvgHLTH8jU1mXxV4jA94XDKbQHWdg28JtJvyrVqIlomeIW9_fyBAEpOiqoSxxVEKI7tYXnkoxKvx3CEy71MmxjhoeY_hv9srg3DMQKjCbB2hIAXqzJaYH--Rc568GH8So6koiwkCsjDDYpOY3nhv1qmIqTw1-ZcEp-8KjJm-yUCtWF63LseLUZFXsO82tGECDyuibZaVT0Fy8IfeJLa8OQ1zB4TXvysGMCr0xwbAeeDpufHcCR7f6CiYg;gfkadpd=3569,42874|520918,36088;i18next=zh;login_scene=11;monitor_session_id=9444348919583365258;monitor_utm=%257B%2522utm_campaign%2522%253A%2522doubao%2522%252C%2522utm_content%2522%253A%2522aidrawio%2522%252C%2522utm_medium%2522%253A%2522github%2522%252C%2522utm_source%2522%253A%2522coopensrc%2522%252C%2522utm_term%2522%253A%2522project%2522%257D;s_v_web_id=verify_mlxcna5b_OPnHmJyI_isi9_4Wph_AE1g_IryXIJgAqHFs;top_region=;vcloudWebId=0d8e34f9-2a27-4f3b-a86a-10cb562dbf67;VOLCFE_im_uuid=1771893239908012284"
    request = SoraVideoRequest(
        # prompt="【图片 1】【图片 2】融合起",
        prompt="孙悟空",

        # seconds=4,
        # resolution="480p",
        # size="16x9",

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

    data = {
        "model": "doubao-seedance-2-0-260128",
        "prompt": "图2人物替换图1人物\n固定镜头下，金发女孩保持视角不动，1.52秒周期眨眼，上眼睑下垂15°，下眼睑0.5HZ微颤；2000+发丝随颈部后方1.2m/s点状风源飘动，发梢幅度8-12cm。8K超写实面部建模，柔肤滤镜强度40%，虹膜动态高光追踪。原比例",
        "seconds": "4",
        "size": "16x9",
        "input_reference": [
            "https://static.mindvideo.ai/mindvideo/images/user-1816015/1771135545106.jpg",
            "https://static.mindvideo.ai/mindvideo/images/user-1816015/1771135553777.jpg"
        ],
        "duration": 4,
        "ratio": "16:9",
        "aspect_ratio": "16:9",
        "resolution": "480p"
    }
    request = SoraVideoRequest(**data)

    task_ids = []
    arun(Tasks(api_key).create(request))
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
    # task_id = "sora-2::cgt-20260212224451-6nrdn"
    # task_id = "request:oZbBDx8JYBwhGfw7rmm5US"
    # arun(Tasks(api_key).get(task_id))
    # arun(Tasks(api_key).get_for_volc(task_id))

# {"model":"doubao-seedance-2-0-260128","stream":false,"top_p":0.7,"temperature":0.7,"n":1,"content":[{"type":"text","text":"刘亦菲穿着肉色丝袜在床上唱歌"}],"generate_audio":true,"ratio":"16:9","duration":15,"watermark":false}

# docker logs -f --tail 100 "apis-videos" | grep "未指定首帧或尾帧图片"
#
# docker logs -f --tail 100"520bdb0c2c5f70b51545ae9300cbb53e1d39e8b1a6547cb5d05f78fffd78ed5c" | grep "未指定首帧或尾帧图片"
# docker logs --tail 100 <container_id> | grep "failed"
