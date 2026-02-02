#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : audio
# @Time         : 2025/12/11 17:17
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.schemas.openai_types import TTSRequest
from openai import OpenAI

"""
input: str,
model: Union[str, SpeechModel],
voice: Union[
    str, Literal["alloy", "ash", "ballad", "coral", "echo", "sage", "shimmer", "verse", "marin", "cedar"]
],
instructions: str | Omit = omit,
response_format: Literal["mp3", "opus", "aac", "flac", "wav", "pcm"] | Omit = omit,
speed: float | Omit = omit,
stream_format: Literal["sse", "audio"] | Omit = omit,
# Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
# The extra values given here take precedence over values defined on the client or passed to this method.
extra_headers: Headers | None = None,
extra_query: Query | None = None,
extra_body: Body | None = None,
timeout: float | httpx.Timeout | None | NotGiven = not_given,

{
    "model": "test",
    "input": "你好你好你好你好你好你好你好你好你好你好你好你好你好",
    "voice": "",
    "response_format": "url",
    "chunking_strategy": null,
    "include": null,
    "known_speaker_names": null,
    "known_speaker_references": null,
    "language": "",
    "prompt": "",
    "stream": false,
    "temperature": null,
    "timestamp_granularities": null
}


    
{
    "id": "test",
    "status": "SUBMITTED",
    "headers": {
        "host": "openai-dev.chatfire.cn",
        "x-real-ip": "172.17.0.3",
        "x-forwarded-for": "172.17.0.3",
        "remote-host": "172.17.0.3",
        "connection": "close",
        "content-length": "330",
        "content-type": "application/json",
        "accept": "*/*",
        "authorization": "Bearer https://openai-dev.chatfire.cn/v0",
        "accept-encoding": "gzip",
        "user-agent": "Go-http-client/2.0"
    },
    "url": "http://openai-dev.chatfire.cn/v0/v1/audio/speech",
    "method": "POST",
    "path": "v1/audio/speech",
    "payload": {
        "model": "test",
        "input": "你好你好你好你好你好你好你好你好你好你好你好你好你好",
        "voice": "",
        "response_format": "url",
        "chunking_strategy": null,
        "include": null,
        "known_speaker_names": null,
        "known_speaker_references": null,
        "language": "",
        "prompt": "",
        "stream": false,
        "temperature": null,
        "timestamp_granularities": null
    },
    "form": {},
    "params": {},
    "x-headers": null,
    "model": "test",
    "input": "你好你好你好你好你好你好你好你好你好你好你好你好你好",
    "voice": "",
    "response_format": "url",
    "chunking_strategy": null,
    "include": null,
    "known_speaker_names": null,
    "known_speaker_references": null,
    "language": "",
    "prompt": "",
    "stream": false,
    "temperature": null,
    "timestamp_granularities": null
}
"""
