"""Shared HTTP session factory for AI API calls.

All smart helpers (vision, assertion, wait, network) call LT-hosted
endpoints that require Basic auth via LT_USERNAME + LT_ACCESS_KEY.

Also threads session tracking headers (x-session-id, x-source, x-test-id)
so the LT backend can distinguish local runs from HyperExecute runs. Forge
sets TESTMUAI_SOURCE=hyperexecute in all cloud YAML paths; locally we
default to "local".
"""
import base64
import logging
import os

import aiohttp

from testmu import _configure
from testmu._step import get_instruction_id

_log = logging.getLogger("testmu")


async def _log_api_call_id(session, ctx, params):
    """One run-log line per AI call that names its api_call_id, the key to
    look the call up server-side, and the controller request_id(s) that name
    its captured data."""
    call_id = params.response.headers.get("x-api-call-id")
    if call_id:
        request_ids = params.response.headers.get("x-controller-request-id")
        _log.info("%s %s -> %s api_call_id=%s%s",
                  params.method, params.url.path, params.response.status, call_id,
                  f" request_id={request_ids}" if request_ids else "")


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

    run_id = os.getenv("TESTMUAI_RUN_ID", "") or os.getenv("TEST_RUN_ID", "")
    if run_id:
        headers["x-run-id"] = run_id

    commit_id = os.getenv("TESTMUAI_COMMIT_ID", "") or os.getenv("COMMIT_ID", "")
    if commit_id:
        headers["x-commit-id"] = commit_id

    trace = aiohttp.TraceConfig()
    trace.on_request_end.append(_log_api_call_id)
    kwargs["trace_configs"] = [*kwargs.get("trace_configs", []), trace]

    return aiohttp.ClientSession(headers=headers, **kwargs)
