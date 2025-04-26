#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : dify_types
# @Time         : 2024/8/30 10:49
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

BASE_URL = "https://flow.chatfire.cn/v1"


class ChatCompletionResponse(BaseModel):
    pass


class ChatCompletionChunkResponse(BaseModel):
    event: str = "message"
    id: Optional[str] = None
    task_id: Optional[str] = None
    message_id: Optional[str] = None
    conversation_id: Optional[str] = None
    answer: str = ""
    created_at: int = Field(default_factory=lambda: int(time.time()))

    # position: int
    # thought: str
    # observation: str
    # tool: str
    # tool_input: dict
    # message_files: List[str]


if __name__ == '__main__':
    chunk = """data: {"event": "message", "task_id": "900bbd43-dc0b-4383-a372-aa6e6c414227", "id": "663c5084-a254-4040-8ad3-51f2a3c1a77c", "answer": "Hi", "created_at": 1705398420}\n\n"""
    _ = ChatCompletionChunkResponse.model_validate_json(chunk.strip('data:'))
    print(_)
