#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : task_types
# @Time         : 2024/5/31 15:47
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
from enum import Enum

from meutils.pipe import *

# "NOT_START", "SUBMITTED", "QUEUED", "IN_PROGRESS", "FAILURE", "SUCCESS", "UNKNOWN"

STATUSES = {
    "not_start": "NOT_START",

    "submitted": "SUBMITTED",

    "starting": "QUEUED",
    "queued": "QUEUED",
    "STARTED": "QUEUED",
    "started": "QUEUED",
    "pending": "QUEUED",
    "PENDING": "QUEUED",
    "Queueing": "QUEUED",

    "processing": "IN_PROGRESS",
    "in_progress": "IN_PROGRESS",
    "received": "IN_PROGRESS",
    "inprogress": "IN_PROGRESS",

    "succeed": "SUCCESS",
    "success": "SUCCESS",
    "succeeded": "SUCCESS",

    "fail": "FAILURE",
    "failed": "FAILURE",
    "canceled": "FAILURE",
    "FAILURE": "FAILURE",
    "failure": "FAILURE",

    "unknown": "UNKNOWN",

}


class TaskResponse(BaseModel):
    """异步任务 通用响应体"""
    task_id: Optional[str] = None

    code: Optional[int] = 0
    message: Optional[str] = None
    status: Optional[str] = "submitted"
    data: Optional[Any] = None

    # 系统水印：可以存token
    system_fingerprint: Optional[str] = None

    model: Optional[str] = None

    # created_at: int = Field(default_factory=lambda: int(time.time()))
    created_at: Union[str, int] = Field(default_factory=lambda: datetime.datetime.today().isoformat())

    def __init__(self, /, **data: Any):
        super().__init__(**data)
        self.status = STATUSES.get((self.status or '').lower(), "UNKNOWN")

    class Config:
        # 允许额外字段，增加灵活性
        extra = 'allow'


class TaskType(str, Enum):
    # 存储
    oss = "oss"

    # 百度助手
    pcedit = "pcedit"

    # 图 音频 视频

    kling = "kling"
    kling_vip = "kling@vip"
    # api
    kling_image = "kling-image"
    kling_video = "kling-video"

    vidu = "vidu"
    vidu_vip = "vidu@vip"

    suno = "suno"
    haimian = "haimian"
    lyrics = "lyrics"

    runwayml = "runwayml"
    fish = 'fish'
    cogvideox = "cogvideox"
    cogvideox_vip = "cogvideox@vip"

    faceswap = "faceswap"

    # 文档智能
    file_extract = "file-extract"
    moonshot_fileparser = "moonshot-fileparser"
    textin_fileparser = "textin-fileparser"
    qwen = "qwen"

    watermark_remove = "watermark-remove"

    # 语音克隆 tts  Voice clone
    tts = "tts"
    voice_clone = "voice-clone"

    # OCR
    ocr_pro = "ocr-pro"

    # todo
    assistants = "assistants"
    fine_tune = "fine-tune"


Purpose = TaskType


class Task(BaseModel):
    id: Optional[Union[str, int]] = Field(default_factory=lambda: shortuuid.random())
    status: Optional[Union[str, int]] = "success"  # pending, running, success, failed

    status_code: Optional[int] = None

    data: Optional[Any] = None
    metadata: Optional[Any] = None
    # metadata: Optional[Dict[str, str]] = None

    system_fingerprint: Optional[str] = None  # api-key token cookie 加密

    created_at: int = Field(default_factory=lambda: int(time.time()))
    description: Optional[str] = None


class FileTask(BaseModel):
    id: Union[str, int] = Field(default_factory=lambda: shortuuid.random())
    status: Optional[str] = None  # pending, running, success, failed
    status_code: Optional[int] = None

    data: Optional[Any] = None
    metadata: Optional[Any] = None

    system_fingerprint: Optional[str] = None  # api-key token cookie 加密

    created_at: int = Field(default_factory=lambda: int(time.time()))

    url: Optional[str] = None


# pass

if __name__ == '__main__':
    # print(TaskType("kling").name)
    #
    # print(TaskType("kling") == 'kling')

    # print(Task(id=1, status='failed', system_fingerprint='xxx').model_dump(exclude={"system_fingerprint"}))

    # print("kling" == TaskType.kling)
    # print("kling" == Purpose.kling)

    # print(Purpose('kling').value)
    # print(Purpose.vidu.startswith('vidu'))

    # print('vidu' in Purpose.vidu)

    # print('kling_vip' in {TaskType.kling, TaskType.kling_vip})

    # print('kling_vip'.startswith(TaskType.kling))

    # print(Purpose.__members__)
    # print(list(Purpose))
    #
    # print(Purpose.oss in Purpose.__members__)

    # , ** {"a": 1, "system_fingerprint": 1}
    response = TaskResponse(system_fingerprint="121")

    # print(response.model_dump())
    #
    # response.__dict__.update({"a": 1, "system_fingerprint": 1})
    #
    # print(response.model_dump())

    response.user_id = 1

    print(response)
