"""Shared HTTP session factory for AI API calls.

All smart helpers (vision, assertion, wait, network) call LT-hosted
endpoints that require Basic auth via LT_USERNAME + LT_ACCESS_KEY.

Also threads session tracking headers (x-session-id, x-source, x-test-id)
so the LT backend can distinguish local runs from HyperExecute runs. Forge
sets TESTMUAI_SOURCE=hyperexecute in all cloud YAML paths; locally we
default to "local".
"""
import base64
import os

import aiohttp

from testmu import _configure
from testmu._step import get_instruction_id


def create_session(**kwargs) -> aiohttp.ClientSession:
    """Create an aiohttp session with LT Basic auth + tracking headers."""
    headers = kwargs.pop("headers", {})

    # Negotiate only the codecs backed by stdlib zlib. Left to itself, aiohttp
    # advertises `br` whenever a brotli module happens to be importable, and the
    # endpoints below sit behind a CDN that honours it — so decoding a response
    # silently depends on a native package nobody declared. aiohttp >=3.13 drives
    # it via Decompressor.process(data, max_length), a 2-arg form that only
    # exists in Brotli >=1.1.0; a runtime carrying an older Brotli therefore
    # fails EVERY compressed response with "Can not decode content-encoding: br",
    # which aiohttp raises as a bogus 400. zlib ships with CPython and cannot
    # skew this way.
    headers.setdefault("Accept-Encoding", "gzip, deflate")

    username = os.getenv("LT_USERNAME", "")
    access_key = os.getenv("LT_ACCESS_KEY", "")
    if username and access_key:
        auth = base64.b64encode(f"{username}:{access_key}".encode()).decode()
        headers["Authorization"] = f"Basic {auth}"

    session_id = os.getenv("TESTMUAI_SESSION_ID", "")
    if session_id:
        headers["x-session-id"] = session_id

    headers["x-source"] = os.getenv("TESTMUAI_SOURCE", "local")

    test_id = (_configure.get("test_id")
               or os.getenv("TESTMUAI_TEST_ID", "")
               or os.getenv("TEST_ID", ""))
    if test_id:
        headers["x-test-id"] = test_id

    instruction_id = get_instruction_id()
    if instruction_id:
        headers["x-instruction-id"] = instruction_id

    return aiohttp.ClientSession(headers=headers, **kwargs)
