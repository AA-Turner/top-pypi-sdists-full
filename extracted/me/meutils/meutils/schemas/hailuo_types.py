#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : hailuo_types
# @Time         : 2024/10/21 20:16
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

BASE_URL = "https://hailuoai.com"
BASE_URL_ABROAD = "https://hailuoai.video"

FEISHU_URL = "https://xchatllm.feishu.cn/sheets/GYCHsvI4qhnDPNtI4VPcdw2knEd?sheet=eDzlrj"
FEISHU_URL_ABROAD = "https://xchatllm.feishu.cn/sheets/GYCHsvI4qhnDPNtI4VPcdw2knEd?sheet=8rB8xi"

FEISHU_URL_OSS = "https://xchatllm.feishu.cn/sheets/MekfsfVuohfUf1tsWV0cCvTmn3c?sheet=Kcg6QC"

#     """生成中是1 成功是2 失败是5 内容审核7 排队中11"""
# "status": 12,
# "message": "Optimizing prompt in progress...",
status_mapper = {
    11: "Queueing",
    12: "Processing",  # "Optimizing prompt in progress..." # 大于10应该都算正常

    1: "Processing",
    2: "Success",
    5: "Failed",
    7: "Failed",
}


class VideoRequest(BaseModel):
    """https://platform.minimaxi.com/document/video_generation?key=66d1439376e52fcee2853049
    23000 文生视频
    "T2V-01": "23000"
    "I2V-01": "23001"
    "I2V-01-live"： "23011"

    "T2V-01": "23000",
    "I2V-01": "23001",
    "I2V-01-live": "23011",
    "S2V-01": "23021"

    {"desc":"飞起来","useOriginPrompt":false,"fileList":[{"id":"320650134834716679","name":"s.jpg","type":"jpg"}],"modelID":"23001"} # 老模型
    {"desc":"飞起来","useOriginPrompt":false,"fileList":[{"id":"320650134834716679","name":"s.jpg","type":"jpg"}],"modelID":"23011"} # 新模型

    {"desc":"跳动","useOriginPrompt":true,"fileList":[{"id":"304987062153912323","name":"3a71b0bb-3cab-4e69-b1f0-592976d0897b_00001_.png","type":"png"}]}
    """
    model: Union[str, Literal["video-01", "T2V-01", "I2V-01", "I2V-01-live", "S2V-01"]] = "video-01"

    """生成视频的描述。(注：需少于2000字)"""
    prompt: Optional[str] = None

    """默认取值为True，模型会自动优化传入的prompt，以提升生成质量。如果需要更精确的控制，可以将此参数设置为False，模型将更加严格地遵循指令。此时建议提供更精细的prompt，以获得最佳效果。"""
    prompt_optimizer: bool = True

    """模型将以此参数中传入的图片为首帧画面来生成视频。支持传入图片的url或base64编码。传入此参数时支持将prompt设置为空字符串或不传入prompt，模型将自主决定画面如何演变。
    传入图片需要满足以下条件：格式为JPG/JPEG/PNG；长宽比大于2:5、小于5:2；短边像素大于300px；体积不大于20MB。"""
    first_frame_image: Optional[str] = None

    """本参数仅当model选择为S2V-01时可用。模型将依据此参数中上传的主体来生成视频。目前仅支持单主体参考（数组长度为 1）。"""
    # subject_reference: list = [{"type": "character", "image": ""}]

    callback_url: Optional[str] = None

    "n"
    n: int = 1

    def __init__(self, /, **data: Any):
        super().__init__(**data)


class BaseResponse(BaseModel):
    """
    状态码及其分别含义如下：
    0，请求成功
    1002，触发限流，请稍后再试 1000061 1500009
    1004，账号鉴权失败，请检查 API-Key 是否填写正确
    1008，账号余额不足
    1013，传入参数异常，请检查入参是否按要求填写
    1026，视频描述涉及敏感内容
    1027，生成视频涉及敏感内容

    1500002 Please try again with a different prompt

    status string任务状态，包括以下状态
    Preparing-准备中
    Queueing-队列中
    Processing-生成中
    Success-成功
    Fail-失败
    """
    status_code: int = Field(default=0, alias="code")

    """生成视频任务的状态消息，success 为成功。"""
    status_msg: str = Field(default="success", alias="message")


class Video(BaseModel):
    id: Optional[str] = None
    canAppeal: Optional[bool] = None
    canRetry: Optional[bool] = None
    coverURL: Optional[str] = None
    desc: Optional[str] = None
    message: Optional[str] = None
    originFiles: Optional[List[Any]] = None
    percent: Optional[int] = None
    status: Optional[int] = None
    """生成中是1 成功是2 失败是5 内容审核7 排队中11"""
    videoURL: Optional[str] = None
    downloadURL: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None


class VideoResponse(BaseModel):
    """
        {
        "task_id": "106916112212032",
        "base_resp": {
            "status_code": 0,
            "status_msg": "success"
        }
    }
    {
        "task_id": "176843862716480",
        "status": "Success",
        "file_id": "176844028768320",
        "base_resp": {
            "status_code": 0,
            "status_msg": "success"
        }
    }
    """
    task_id: str
    base_resp: BaseResponse  # response.statusInfo

    """
    SUBMITTED-已提交
    Preparing-准备中
    Queueing-队列中
    Processing-生成中
    Success-成功
    Failed-失败
    """
    status: str = "SUBMITTED"
    file_id: Optional[str] = None  # 通过file_id 可以获取视频地址download_url

    videos: Optional[List[Video]] = None  # response.data.videos

    system_fingerprint: Optional[str] = None

    def __init__(self, /, **data: Any):
        super().__init__(**data)
        if self.file_id is None and self.videos:
            self.file_id = self.videos[0].downloadURL

        if self.videos:
            self.status = status_mapper.get(self.videos[0].status, "Failed")


#
# "data": {
#         "videos": [
#             {
#                 "id": "304988292041920515",
#                 "desc": "跳动",
#                 "coverURL": "",
#                 "videoURL": "",
#                 "status": 1,   # 5 生成失败
#                 "percent": 0,
#                 "message": "正在生成，退出后AI会继续生成",
#                 "canRetry": false,
#                 "width": 0,
#                 "height": 0,
#                 "originFiles": [
#                     {
#                         "id": "304987062153912323",
#                         "url": "https://cdn.hailuoai.com/prod/2024-10-22-12/user/multi_chat_file/b9e76359-07ca-4ef4-9f6d-80d8ab416c9f.png",
#                         "type": "png"
#                     }
#                 ],
#                 "canAppeal": false
#             }
#         ],
#         "processing": true,
#         "cycleTime": 10,
#         "hasMore": false
#     }

"""
refer_voice
请输入您的参考音色ID
refer_instrumental
请输入您的参考伴奏ID
lyrics
##在无垠的星空下\n\n梦开始飞翔\n月光洒在心上\n\n温柔的想象\n在这片宁静中\n\n我们自由歌唱##
model
music-01
audio_setting
{"sample_rate":44100,"bitrate":256000,"format":"mp3"}

"""


class MusicRequet(BaseModel):
    model: str = "music-01"

    lyrics: str

    refer_voice: Optional[str] = None
    refer_instrumental: Optional[str] = None
    audio_setting: dict = {
        "sample_rate": 44100,
        "bitrate": 256000,
        "format": "mp3"
    }


"""
{
   "data":{
      "audio":"hex编码的音频数据",
      "status":2
   },
   "trace_id":"02cb3e6a7f8ada5886fdc11e09452353",
   "base_resp":{
      "status_code":0,
      "status_msg":"success"
   }
}
"""


class MusicResponse(BaseModel):
    trace_id: str
    base_resp: BaseResponse
