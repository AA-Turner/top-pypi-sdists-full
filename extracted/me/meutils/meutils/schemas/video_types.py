#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : video_types
# @Time         : 2024/9/13 10:15
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import json

from meutils.pipe import *
from meutils.math_utils import size2aspect_ratio
from meutils.schemas.utils import to_status

from openai.types.video import Video as _Video


class VideoCreateError(BaseModel):
    code: str = "400"

    message: Optional[str] = None

    def __init__(self, /, **data: Any):
        super().__init__(**data)


class Video(_Video):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    """Unique identifier for the video job."""

    created_at: int = Field(default_factory=lambda: int(time.time()))
    """Unix timestamp (seconds) for when the job was created."""

    model: Optional[Union[str, Literal["sora-2", "sora-2-pro"]]] = ""
    """The video generation model that produced the job."""

    object: Literal["image", "video"] = "video"
    """The object type, which is always `video`."""

    progress: int = 0
    """Approximate completion percentage for the generation task."""

    seconds: Optional[Union[str, Literal["4", "8", "12"]]] = None
    """Duration of the generated clip in seconds."""

    size: Optional[Union[str, Literal["720x1280", "1280x720", "1024x1792", "1792x1024"]]] = None
    """The resolution of the generated video."""

    status: Union[Literal["queued", "in_progress", "completed", "failed"], str, dict] = "queued"
    """Current lifecycle status of the video job."""

    video_url: Optional[str] = None  # todo 是否支持多张

    error: Optional[Union[dict, str]] = None

    # "error": {
    #     "code": "generation_failed",
    #     "message": "This content may violate our content policies."
    # },

    # 自定义
    metadata: Optional[Union[dict, str]] = None
    polling_url: Optional[str] = None
    usage: Optional[dict] = None

    # class Config:
    #     extra = "allow"

    def __init__(self, /, **data: Any):  # todo status映射
        super().__init__(**data)

        self.status = to_status(self.status) or "queued"

        if isinstance(self.error, (tuple, list)):
            self.error = self.error[0]

        if isinstance(self.error, dict):
            self.error["code"] = str(self.error.get("code", "400"))
            self.error["message"] = self.error.get("message", str(self.error))
        else:
            self.error = self.error and {"code": "1", "message": str(self.error)}

        # if self.metadata and not self.video_url: # todo 解析 结果
        #     self.video_url = self.metadata.get("video_url")


class VideoRequest(BaseModel):
    model: Union[str, Literal["cogvideox-flash", "cogvideox"]] = "cogvideox-flash"

    prompt: str = "比得兔开小汽车，游走在马路上，脸上的表情充满开心喜悦。"
    negative_prompt: Optional[str] = None

    """
    提供基于其生成内容的图像。如果传入此参数，系统将以该图像为基础进行操作。支持通过URL或Base64编码传入图片。
    图片要求如下：图片支持.png、jpeg、.jpg 格式、图片大小：不超过5M。image_url和prompt二选一或者同时传入。
    """
    image_url: Optional[str] = None
    tail_image_url: Optional[str] = None

    """
    输出模式，默认为 "quality"。 "quality"：质量优先，生成质量高。 "speed"：速度优先，生成时间更快，质量相对降低。 
    cogvideox-flash模型不支持选择输出模式。
    """
    quality: Literal["quality", "speed"] = "speed"

    """是否生成 AI 音效。默认值: False（不生成音效）。"""
    with_audio: bool = True

    cfg_scale: Optional[float] = None

    """
    默认值: 若不指定，默认生成视频的短边为 1080，长边根据原图片比例缩放。最高支持 4K 分辨率。
    分辨率选项：720x480、1024x1024、1280x960、960x1280、1920x1080、1080x1920、2048x1080、3840x2160
    """
    aspect_ratio: Union[str, Literal["1:1", "21:9", "16:9", "9:16", "4:3", "3:4"]] = "16:9"

    size: Literal[
        '720x480',
        '1024x1024',
        '1280x960',
        '960x1280',
        '1920x1080',
        '1080x1920',
        '2048x1080',
        '3840x2160'] = "1024x1024"

    duration: Literal[5, 10] = 5

    fps: Literal[30, 60] = 30


class SoraVideoRequest(BaseModel):
    model: Union[str, Literal["sora-2", "sora-2-pro"]] = "sora-2"
    prompt: str = "比得兔开小汽车，游走在马路上，脸上的表情充满开心喜悦。"
    seconds: Optional[Union[float, str, Literal["4", "8", "12"]]] = None
    size: Optional[Union[str, Literal["720x1280", "1280x720", "1024x1792", "1792x1024"]]] = None
    input_reference: Optional[Union[str, bytes, list]] = None  # image url/base64/bytes

    # 兼容
    negative_prompt: Optional[str] = None
    duration: Optional[int] = None

    ratio: Optional[str] = None
    aspect_ratio: Optional[str] = None

    resolution: Optional[str] = None

    metadata: Optional[Union[dict, str]] = None

    first_frame_image: Optional[str] = None
    last_frame_image: Optional[str] = None

    #
    image: Optional[str] = None
    audio: Optional[str] = None
    video: Optional[str] = None

    # 声音
    generate_audio: Optional[bool] = None
    keep_audio: Optional[bool] = None
    enhance_prompt: Optional[bool] = None

    # 万相
    template: Optional[str] = None  # 视频特效模板
    shot_type: Optional[str] = None  # single multi

    # style
    style: Optional[str] = None
    action_control: Optional[bool] = None
    character_orientation: Optional[str] = None

    # 回调
    callback_url: Optional[str] = None

    def __init__(self, /, **data: Any):
        super().__init__(**data)
        if isinstance(self.metadata, str):
            self.metadata = json.loads(self.metadata)

        self.duration = self.duration or self.seconds and int(self.seconds)

        if self.input_reference and not isinstance(self.input_reference, list):
            self.input_reference = [self.input_reference]

        if self.size:
            self.size = self.size.replace(':', 'x').replace('*', 'x')
            self.ratio = self.aspect_ratio = size2aspect_ratio(self.size)

        if (not self.resolution
                and '_' in self.model
                # and self.model.lower().endswith(
                #     ('p', 'auto', 'k', '720', '1080', '3840', 'high', 'standard', 'pro', 'std')
                # )
        ):
            self.model, self.resolution = self.model.rsplit('_', maxsplit=1)

    class Config:
        extra = "allow"


class FalVideoRequest(BaseModel):
    model: Union[str, Literal["latentsync", "sync-lipsync",]] = 'latentsync'
    video_url: Optional[str] = None
    audio_url: Optional[str] = None
    image_url: Optional[str] = None

    sync_mode: Union[str, Literal["cut_off", "loop", "bounce"]] = "cut_off"


class FalKlingVideoRequest(BaseModel):
    model: Union[
        str, Literal["fal-ai/kling-video/v1/standard/text-to-video",]] = 'fal-ai/kling-video/v1/standard/text-to-video'

    prompt: Optional[str] = None
    duration: Optional[float] = 5.0
    video_url: Optional[str] = None
    audio_url: Optional[str] = None
    image_url: Optional[str] = None

    sync_mode: Union[str, Literal["cut_off", "loop", "bounce"]] = "cut_off"


class LipsyncVideoRequest(BaseModel):
    model: Union[str, Literal[
        "latentsync", "sync-lipsync",
        "lip_sync_avatar_std", "lip_sync_avatar_lively"
    ]
    ] = 'latentsync'

    video_url: Optional[str] = None
    audio_url: Optional[str] = None
    image_url: Optional[str] = None

    sync_mode: Union[str, Literal["cut_off", "loop", "bounce"]] = "cut_off"


if __name__ == '__main__':
    # print(LipsyncVideoRequest())

    # print(Video(x=1))

    v = SoraVideoRequest(
        # model="doubao-seedance-1-0-pro-fast-251015_1080p",
        # model="doubao-seedance-1-0-pro-fast-251015_4k",
        model="doubao-seedance-1-0-pro-fast-251015_3840",

        input_reference=["https://example.com/image.jpg"] * 10,

        size="1x1",
        xx=11111111
    )

    print(len(v.model_dump_json()))
    print(v.model_dump_json(indent=4, exclude_none=True))

    # data = {
    #     'id': 'cgt-20250613160030-2dvd7',
    #     'model': 'doubao-seedance-1-0-pro-250528',
    #     'status': 'succeeded',
    #     'content': {
    #         'video_url': 'https://ark-content-generation-cn-beijing.tos-cn-beijing.volces.com/doubao-seedance-1-0-pro/02174980163157800000000000000000000ffffac182c17b26890.mp4?X-Tos-Algorithm=TOS4-HMAC-SHA256&X-Tos-Credential=AKLTYjg3ZjNlOGM0YzQyNGE1MmI2MDFiOTM3Y2IwMTY3OTE%2F20250613%2Fcn-beijing%2Ftos%2Frequest&X-Tos-Date=20250613T080120Z&X-Tos-Expires=86400&X-Tos-Signature=5e0928f738f49b93f54923549de4c65940c5007d5e86cb5ebadc756cca3aa03e&X-Tos-SignedHeaders=host'},
    #     'usage': {'completion_tokens': 246840, 'total_tokens': 246840},
    #     'created_at': 1749801631,
    #     'updated_at': 1749801680,
    #     "x": 11111111,
    #     "xx": [1, 2],
    # }
    #
    # _ = Video(
    #     **data
    # )
    #
    # _ = Video(status={
    #     "id": "",
    #     "status": "unknown",
    #     "error": {
    #         "name": "Error",
    #         "message": "invalid params, task_id cannot by empty"
    #     }
    # })
    #
    # print(_)
