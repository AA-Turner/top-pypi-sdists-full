#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : replicate_types
# @Time         : 2024/11/15 18:32
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

FEISHU_URL = "https://xchatllm.feishu.cn/sheets/GYCHsvI4qhnDPNtI4VPcdw2knEd?sheet=QHbR7a"


class ReplicateRequest(BaseModel):
    ref: str = "black-forest-labs/flux-schnell"
    input: Optional[Dict[str, Any]] = None  # {"prompt": "A majestic lion", "num_outputs": 2}



class ReplicateResponse(BaseModel):
    model: str = "🔥"

    id: str = Field(default_factory=shortuuid.random)
    status: str = "starting"  # succeeded

    input: Optional[Any] = None  # 兼容任意结构体
    output: Optional[Any] = None

    logs: str = ""
    error: Optional[str] = None
    metrics: Optional[Any] = None

    created_at: str = Field(default_factory=lambda: datetime.datetime.today().isoformat())  # "2024-11-19T03:11:22.795Z"
    started_at: Optional[str] = None
    completed_at: Optional[str] = None

    """
    {
    "get": "https://api.replicate.com/v1/predictions/pab8srw8jhrm20cj1e7s0d8kf4",
    "cancel": "https://api.replicate.com/v1/predictions/pab8srw8jhrm20cj1e7s0d8kf4/cancel"
    }
    """
    urls: Optional[Dict[str, str]] = None

    data_removed: bool = False  # 移除任务
    version: str = ""

    # token
    system_fingerprint: Optional[str] = None

    def __init__(self, /, **data: Any):
        super().__init__(**data)

    class Config:
        # 允许额外字段，增加灵活性
        extra = 'allow'




if __name__ == '__main__':
    from meutils.db.redis_db import redis_client

    r = ReplicateRequest(
        input=ReplicateSDKRequest(
            ref="stability-ai/stable-diffusion:db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf",
            input={"prompt": "A majestic lion", "num_outputs": 2}
        )
    )

    # print(r.model_dump_json(indent=4))

    # print(ReplicateResponse())

    url = "https://oss.ffire.cc/files/kling_watermark.png"

    response = ReplicateResponse(output=[url])
    print(response.model_dump_json(indent=4))

    # redis_client.set(response.id, response.model_dump_json(indent=4), ex=3600)

    # redis_client.set(response.id, response, ex=3600)

    data = {
        "status": "starting",
        "urls": {
            "get": "https://api.chatfire.cn/v1/predictions/d42c7e90a577bdec0a68797e77a8e0d8"
        },
        "id": "d42c7e90a577bdec0a68797e77a8e0d8",
        "model": "black-forest-labs/flux-1.1-pro",
        "error": None,
        "output": None,
        "data_removed": False,
        "created_at": "2024-11-19T03:11:22.795Z",
        "version": "dp-a956b5a516d14ae1a2b108b3a81e8306",
        "input": {
            "num_inference_steps": 28,
            "num_outputs": 1,
            "prompt": "a cat",
            "prompt_strength": 0.8,
            "aspect_ratio": "1:1",
            "megapixels": "1",
            "output_quality": 80,
            "go_fast": True,
            "guidance": 3
        },
        "logs": ""
    }

    print(ReplicateResponse(**data))
