#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : embedding
# @Time         : 2023/12/12 10:39
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from openai.types import EmbeddingCreateParams


class EmbeddingRequest(BaseModel):
    model: str = "SentenceTransformer"
    input: Union[str, List[str]] = Field(description="The input to embed.")  # max_length=1000

    user: Optional[str] = Field(default=None)
    encoding_format: Literal["float", "base64"] = 'float'

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "model": "text-embedding-ada-002",
                    "input": "免费GPT就在这 https://api.chatllm.vip",
                }
            ]
        }
    }
