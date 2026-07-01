"""Shared HTTP session factory for AI API calls.

All smart helpers (vision, assertion, wait, network) call LT-hosted
endpoints that require Basic auth via LT_USERNAME + LT_ACCESS_KEY.

Also threads session tracking headers (x-session-id, x-source) so the
LT backend can distinguish local runs from HyperExecute runs. Forge
sets TESTMUAI_SOURCE=hyperexecute in all cloud YAML paths; locally we
default to "local".
"""
import base64
import os

import aiohttp


def create_session(**kwargs) -> aiohttp.ClientSession:
    """Create an aiohttp session with LT Basic auth + tracking headers."""
    headers = kwargs.pop("headers", {})

    username = os.getenv("LT_USERNAME", "")
    access_key = os.getenv("LT_ACCESS_KEY", "")
    if username and access_key:
        auth = base64.b64encode(f"{username}:{access_key}".encode()).decode()
        headers["Authorization"] = f"Basic {auth}"

    session_id = os.getenv("TESTMUAI_SESSION_ID", "")
    if session_id:
        headers["x-session-id"] = session_id

    headers["x-source"] = os.getenv("TESTMUAI_SOURCE", "local")

    return aiohttp.ClientSession(headers=headers, **kwargs)
