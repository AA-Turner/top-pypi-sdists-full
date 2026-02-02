#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : tripo3d_types
# @Time         : 2024/10/28 15:19
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

BASE_URL = "https://api.tripo3d.ai"
FEISHU_URL = "https://xchatllm.feishu.cn/sheets/GYCHsvI4qhnDPNtI4VPcdw2knEd?sheet=KU4zY6"


class ImageRequest(BaseModel):
    model_version: Optional[str] = "v2.0-20240919"

    prompt: str

    render_sequence: Optional[bool] = True
    client_id: Optional[str] = "web"

    isPrivate: bool = False
    type: str = "text_to_model"
    name: str = ""

    def __init__(self, /, **data: Any):
        super().__init__(**data)
        self.name = self.name or self.prompt


class TaskResponse(BaseModel):
    """
    {
        "code": 0,
        "data": {
            "task_ids": [
                "e327f716-6300-44ac-baf1-bdd57dd774a9",
                "3320b387-e049-4645-bce3-64636b454a3e",
                "c95fb37a-b766-4e3e-8b97-badf145d7a51",
                "41df5dd5-19c2-4df4-9f4f-71d0cf63d83e"
            ]
        }
    }
    """
    code: Optional[int] = None
    data: Optional[dict] = None
    task_ids: Optional[list] = None
    system_fingerprint: Optional[str] = None

    def __init__(self, /, **data: Any):
        super().__init__(**data)

        if self.data:
            self.task_ids = self.data.get('task_ids', [])
