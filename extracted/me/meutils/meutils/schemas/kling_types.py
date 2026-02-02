#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : kling_types
# @Time         : 2024/9/24 10:15
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.notice.feishu import send_message as _send_message

send_message = partial(
    _send_message,
    title=__name__,
    url="https://open.feishu.cn/open-apis/bot/v2/hook/ad8c3010-7706-4ba0-b945-645c492e535b"
)

STATUSES = {
    5: "submitted",
    10: "processing",
    99: "succeed",
    50: "failed",

    6: "The uploaded image size should be greater than 300PX",
    7: 'NSFW：输入的提示词包含敏感词',
    8: "NSFW：上传图片包含敏感信息",  # 上传图片包含敏感信息

    400: "非法请求",
    500: "内部系统繁忙",

    "submitted": "SUBMITTED",
    "processing": "IN_PROGRESS",
    "succeed": "SUCCESS",
    "failed": "FAILURE",

}

API_BASE_URL = "https://api.klingai.com"
API_FEISHU_URL = "https://xchatllm.feishu.cn/sheets/GYCHsvI4qhnDPNtI4VPcdw2knEd?sheet=LGVKwN"


class TryOnRequest(BaseModel):
    model_name: str = "kolors-virtual-try-on-v1"
    """
    ● 支持传入图片Base64编码或图片URL（确保可访问）
    ● 图片格式支持.jpg / .jpeg / .png
    ● 图片文件大小不能超过10MB，图片分辨率不小于300*300px
    """
    human_image: str = "https://oss.ffire.cc/files/try-on.png"
    cloth_image: str = "https://oss.ffire.cc/files/x.png"

    callback_url: Optional[str] = None

    class Config:
        frozen = True


class Config(BaseModel):
    """包含六个字段，用于指定摄像机的运动或变化"""
    """水平运镜，可选，取值范围：[-10, 10]"""
    horizontal: Optional[int] = 0
    """水平摇镜，可选，取值范围：[-10, 10]"""
    pan: Optional[int] = 0
    """旋转运镜，可选，取值范围：[-10, 10]"""
    roll: Optional[int] = 0
    """垂直摇镜，可选，取值范围：[-10, 10]"""
    tilt: Optional[int] = 0
    """垂直运镜，可选，取值范围：[-10, 10]"""
    vertical: Optional[int] = 0
    """变焦，可选，取值范围：[-10, 10]"""
    zoom: Optional[int] = 0


class CameraControl(BaseModel):
    """控制摄像机运动的协议，可选，未指定则智能匹配"""
    """包含六个字段，用于指定摄像机的运动或变化"""
    config: Config = Config()
    type: str = "simple"  # empty


class VideoRequest(BaseModel):
    model: Optional[str] = "kling-v1"

    """生成视频的模式，可选，枚举值：std（高性能）或 pro（高表现）"""
    mode: Optional[str] = "std"

    """正向文本提示，必须，不能超过500个字符"""
    prompt: str

    """生成视频的画面纵横比，可选，枚举值：16:9, 9:16, 1:1"""
    aspect_ratio: Optional[str] = "1:1"

    """控制摄像机运动的协议，可选，未指定则智能匹配"""
    camera_control: CameraControl = CameraControl()

    """生成视频的自由度，可选，值越大，相关性越强，取值范围：[0,1]"""
    cfg_scale: Optional[float] = None

    """生成视频时长，单位秒，可选，枚举值：5，10"""
    duration: Optional[int] = 5

    """负向文本提示，可选，不能超过200个字符"""
    negative_prompt: Optional[str] = None

    # 图生视频多出来的参数
    """参考图像，必须，支持Base64编码或图片URL，支持.jpg / .jpeg / .png格式，大小不能超过10MB，分辨率不小于300*300px"""
    image: Optional[str] = None

    """参考图像 - 尾帧控制，可选，支持Base64编码或图片URL，支持.jpg / .jpeg / .png格式，大小不能超过10MB，分辨率不小于300*300px"""
    image_tail: Optional[str] = None

    """生成视频数量，可选，取值范围：[1,4]"""
    n: int = 1


class ImageRequest(BaseModel):
    model: Optional[str] = None

    """正向文本提示，必须，不能超过500个字符"""
    prompt: str
    """生成图片的纵横比，可选，枚举值：16:9, 9:16, 1:1, 4:3, 3:4, 3:2, 2:3"""
    aspect_ratio: Optional[str] = None

    """生成图片数量，可选，取值范围：[1,9]"""
    n: int = 1

    """参考图片，可选，支持Base64编码或图片URL，支持.jpg / .jpeg / .png格式，大小不能超过10MB，图片分辨率不小于300*300px。
    Base64仅提供编码部分，data:image/png;base64,后面的部分。
    """
    image: Optional[str] = None

    """生成过程中对用户上传图片的参考强度，可选，取值范围：[0,1]"""
    image_fidelity: Optional[float] = None

    """负向文本提示，可选，不能超过200个字符"""
    negative_prompt: Optional[str] = None

    """本次任务结果回调通知地址，可选"""
    callback_url: Optional[str] = None


# {
#     "code": 0,
#     "message": "string",
#     "request_id": "string",
#     "data": {
#         "task_id": "string",
#         "task_status": "string",
#         "created_at": 0,
#         "updated_at": 0
#     }
# }

class TaskResult(BaseModel):
    """视频ID，系统生成"""
    id: str

    """视频URL"""
    url: str

    """视频时长，单位ms"""
    duration: int


class Task(BaseModel):
    """任务ID，系统生成"""
    task_id: str

    """任务状态，枚举值：submitted（已提交）、processing（处理中）、succeed（成功）、failed（失败）"""
    task_status: str = "processing"

    """任务状态信息，具体定义状态信息"""
    task_status_msg: Optional[str] = None

    """任务创建时间，Unix时间戳、单位ms"""
    created_at: int = Field(default_factory=lambda: int(time.time() * 1000))

    """任务更新时间，Unix时间戳、单位ms"""
    updated_at: int = Field(default_factory=lambda: int(time.time() * 1000))

    """任务最终结果"""
    task_result: Optional[dict] = None


class TaskResponse(BaseModel):
    code: int = 0
    message: str = ""
    request_id: str = ""

    data: Optional[Task] = None

    # 系统水印
    system_fingerprint: Optional[str] = None


# {
#     "code": 0,
#     "message": "string",
#     "request_id": "string",
#     "data": {
#         "task_id": "string",
#         "task_status": "string",
#         "created_at": 0,
#         "updated_at": 0
#     }
# }


# {
#     "code": 0,
#     "message": "string",
#     "request_id": "string",
#     "data": {
#         "task_id": "string",
#         "task_status": "string",
#         "task_status_msg": "string",
#         "created_at": 1722769557708,
#         "updated_at": 1722769557708,
#         "task_result": {
#             "videos": [
#                 {
#                     "id": "string",
#                     "url": "string",
#                     "duration": "string"
#                 }
#             ]
#         }
#     }
# }


if __name__ == '__main__':
    print(TaskResponse(data=Task(task_id='xx')).model_dump(exclude_none=True))
