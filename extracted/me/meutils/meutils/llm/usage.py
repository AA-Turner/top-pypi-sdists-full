#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : usage
# @Time         : 2025/10/12 13:20
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.schemas.openai_types import CompletionUsage, ChatCompletion

d = {"id": "cgt-20251012131916-zdg8q", "model": "doubao-seedance-1-0-lite-t2v-250428", "status": "succeeded",
     "content": {
         "video_url": "https://ark-content-generation-cn-beijing.tos-cn-beijing.volces.com/doubao-seedance-1-0-lite-t2v/02176024635702100000000000000000000ffffac15ae33f8ddbe.mp4?X-Tos-Algorithm=TOS4-HMAC-SHA256&X-Tos-Credential=AKLTYWJkZTExNjA1ZDUyNDc3YzhjNTM5OGIyNjBhNDcyOTQ%2F20251012%2Fcn-beijing%2Ftos%2Frequest&X-Tos-Date=20251012T051950Z&X-Tos-Expires=86400&X-Tos-Signature=604ba900d31722e95c8b129a95d71ef2b0c9717c719d549a26c904aa19cca6be&X-Tos-SignedHeaders=host"},
     "usage": {"completion_tokens": 103818, "total_tokens": 103818}, "created_at": 1760246356, "updated_at": 1760246390,
     "seed": 8961, "resolution": "720p", "duration": 5, "ratio": "16:9", "framespersecond": 24}



CompletionUsage(**d['usage'])
