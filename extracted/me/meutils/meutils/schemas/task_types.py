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
from meutils.str_utils.json_utils import json_path

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


class FluxTaskResponse(BaseModel):
    id: Union[str, int] = Field(default_factory=lambda: shortuuid.random())

    """Task not found, Pending, Request Moderated, Content Moderated, Ready, Error"""
    status: Optional[Literal["Pending", "Ready", "Error", "Content Moderated"]] = None  # Ready, Error, success, failed

    result: Optional[dict] = None

    details: Optional[dict] = None  # Error才显示, 当做 metadata
    progress: Optional[int] = None

    def __init__(self, /, **data: Any):
        super().__init__(**data)

        self.details = self.details or self.result or {}

        if self.status is None and self.result:
            if status := (
                    self.result.get("status")
                    or self.result.get("task_status")
                    or self.result.get("state")
                    or self.result.get("task_state")
                    or self.result.get("detail")  # fal
                    or json_path(self.result, expr="$..status")

            ):
                if isinstance(status, list):
                    status = status[0]

                if isinstance(status, dict): # fal
                    self.status = "Error"

                status = str(status).lower()
                logger.debug(status)

                if status.startswith(("pro", "inpro", "pending", "task_status_queu", "sub", "start", "run", "inqueue")):
                    self.status = "Pending"

                if status.startswith(("succ", "ok", "compl", "task_status_succ")):
                    self.status = "Ready"

                if status.startswith(("fail", "error", "cancel", "task_status_fail")):
                    self.status = "Error"

                if any(i in status for i in ("moder",)):
                    self.status = "Content Moderated"

                if any(i in status for i in ("feature_not_supported",)):
                    self.status = "Error"

        # fal 会误判其他渠道 todo 增强
        if (
                self.status is None
                and "queue.fal.run" not in str(self.result)
                and "fal.media" in str(self.result)  # fal 任务一般是有结果的 https://v3.fal.media/files
        ):
            self.status = "Ready"

            # bug
            # {'detail': [{'input': 4.0,
            #              'loc': ['body', 'upscale_factor'],
            #              'msg': 'The output video resolution exceeds 4K limits '
            #                     '(3840x2160).',
            #              'type': 'feature_not_supported',
            #              'url': 'https://docs.fal.ai/errors#feature_not_supported'}]}

            # {
            #   "detail": [
            #     {
            #       "loc": [
            #         "body",
            #         "audio_url"
            #       ],
            #       "msg": "Audio duration is too short. Minimum is 10 seconds, provided is 7.2 seconds.",
            #       "type": "audio_duration_too_short",
            #       "url": "https://docs.fal.ai/errors#audio_duration_too_short",
            #       "ctx": {
            #         "min_duration": 10,
            #         "provided_duration": 7.2
            #       },
            #       "input": "https://s3.ffire.cc/files/jay_prompt.wav"
            #     }
            #   ]
            # }
            # Voice3f6ccdc71752639560
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

    data = {
        "task": {
            "eta": 0,
            "reason": "",
            "status": "TASK_STATUS_QUEUED",
            "task_id": "d7197eed-54b4-40dd-a265-a736435abbf9",
            "task_type": "MINIMAX_HAILUO_02_10S_768P",
            "progress_percent": 0
        },
        "extra": {},
        "audios": [],
        "images": [],
        "videos": []
    }

    print(FluxTaskResponse(result=data))
