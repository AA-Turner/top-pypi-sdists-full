#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : response2chat
# @Time         : 2026/1/13 13:34
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 
"""
background: Optional[bool] | Omit = omit,
        conversation: Optional[response_create_params.Conversation] | Omit = omit,
        include: Optional[List[ResponseIncludable]] | Omit = omit,
        input: Union[str, ResponseInputParam] | Omit = omit,
        instructions: Optional[str] | Omit = omit,
        max_output_tokens: Optional[int] | Omit = omit,
        max_tool_calls: Optional[int] | Omit = omit,
        metadata: Optional[Metadata] | Omit = omit,
        model: ResponsesModel | Omit = omit,
        parallel_tool_calls: Optional[bool] | Omit = omit,
        previous_response_id: Optional[str] | Omit = omit,
        prompt: Optional[ResponsePromptParam] | Omit = omit,
        prompt_cache_key: str | Omit = omit,
        prompt_cache_retention: Optional[Literal["in-memory", "24h"]] | Omit = omit,
        reasoning: Optional[Reasoning] | Omit = omit,
        safety_identifier: str | Omit = omit,
        service_tier: Optional[Literal["auto", "default", "flex", "scale", "priority"]] | Omit = omit,
        store: Optional[bool] | Omit = omit,
        stream: Optional[Literal[False]] | Literal[True] | Omit = omit,
        stream_options: Optional[response_create_params.StreamOptions] | Omit = omit,
        temperature: Optional[float] | Omit = omit,
        text: ResponseTextConfigParam | Omit = omit,
        tool_choice: response_create_params.ToolChoice | Omit = omit,
        tools: Iterable[ToolParam] | Omit = omit,
        top_logprobs: Optional[int] | Omit = omit,
        top_p: Optional[float] | Omit = omit,
        truncation: Optional[Literal["auto", "disabled"]] | Omit = omit,

"""
from meutils.pipe import *

from openai import OpenAI

client = OpenAI(
    base_url="https://api.routin.ai/v1",
    api_key="ak-4a2f1c784cbd4b658b1219ef951ce63c"
)

data = {
    "model": "gpt-5.2-codex",
    "input": "hi",
    "instructions": None,
    # "stream": True
}

r = client.responses.create(**data)


