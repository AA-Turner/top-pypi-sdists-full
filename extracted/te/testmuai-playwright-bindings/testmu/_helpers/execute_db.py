"""execute_db helper — runs a SQL query via the automind /db-query endpoint.

Auth-gated: requires LT_USERNAME + LT_ACCESS_KEY to be set (automind is an
LT-hosted service). Works in both local and cloud run targets as long as
creds are present. Raises RuntimeError when creds are missing.

Env vars consumed (when not passed explicitly):
    LT_USERNAME         — LambdaTest username (used to build auth header)
    LT_ACCESS_KEY       — LambdaTest access key
    AUTOMIND_URL        — Base URL of the automind service
    LT_PROXY_TUNNEL_ID  — Tunnel ID for network connectivity

Raises:
    RuntimeError: When LT creds are missing, on non-200 response, or on network failure.

Returns:
    Query result dict on success.
"""
import asyncio
import base64
import binascii
import json
import logging
import os

_log = logging.getLogger("testmu")


def _do_query(query, db_id, db_name, timeout, tunnel_id, auth_header, automind_url):
    """Synchronous inner function executed via asyncio.to_thread."""
    import requests as _requests

    url = f"{automind_url}/db-query"
    _timeout = timeout
    if isinstance(_timeout, str):
        try:
            _timeout = int(_timeout)
        except (ValueError, TypeError):
            _timeout = 10000

    payload = {
        "payload": {
            "id": db_id,
            "timeout": _timeout,
            "db_name": db_name,
            "tunnel_id": tunnel_id,
        },
        "query": query,
    }
    headers = {
        "content-type": "application/json",
        "Authorization": f"Basic {auth_header}",
    }
    resp = _requests.post(url, json=payload, headers=headers)
    if resp.status_code != 200:
        raise RuntimeError(f"DB query failed: {resp.text}")
    result = resp.json()
    if isinstance(result, str):
        result = json.loads(result)
    if "error" in result:
        raise RuntimeError(f"DB query error: {result['error']}")
    return result


async def execute_db(
    query,
    db_id="",
    db_name="",
    timeout=10000,
    tunnel_id="",
    auth_header="",
    automind_url="",
):
    """Execute a database query via the automind /db-query endpoint.

    Auth-gated: raises RuntimeError when LT_USERNAME/LT_ACCESS_KEY are not set.

    Args:
        query: Base64-encoded SQL query string.
        db_id: Database connection identifier.
        db_name: Database name.
        timeout: Query timeout in milliseconds (default 10000).
        tunnel_id: Tunnel ID for network connectivity.
        auth_header: Base64-encoded "username:access_key" string.
        automind_url: Automind service base URL.

    Returns:
        Query result dict on success.

    Raises:
        RuntimeError: When LT creds are missing, on non-200 response,
            or on network/query failure.
    """
    from testmu import _config

    if not _config.lt_auth:
        raise RuntimeError("DB query requires LT_USERNAME and LT_ACCESS_KEY")

    # Fall back to environment variables
    if not automind_url:
        automind_url = os.environ.get("AUTOMIND_URL", "https://kaneai-api.lambdatest.com")
    if not auth_header:
        username = os.environ.get("LT_USERNAME", "")
        access_key = os.environ.get("LT_ACCESS_KEY", "")
        if username and access_key:
            auth_header = base64.b64encode(f"{username}:{access_key}".encode()).decode()
    if not tunnel_id:
        tunnel_id = os.environ.get("LT_PROXY_TUNNEL_ID", "")

    # Resolve {{...}} / ${...} variable templates in the query.
    # The query arrives base64-encoded: decode → resolve → re-encode.
    # If the value is not valid base64 / not valid UTF-8, forward it unchanged.
    try:
        from testmu._vars import var as _var
        decoded_query = base64.b64decode(query, validate=True).decode("utf-8")
        resolved_query = _var(decoded_query)
        if not isinstance(resolved_query, str):
            resolved_query = str(resolved_query)
        query = base64.b64encode(resolved_query.encode("utf-8")).decode("utf-8")
    except (binascii.Error, UnicodeDecodeError):
        pass  # not valid base64 or UTF-8 — leave query unchanged

    _log.info("    [execute_db] db_id=%r db_name=%r", db_id, db_name)
    try:
        result = await asyncio.to_thread(
            _do_query, query, db_id, db_name, timeout, tunnel_id, auth_header, automind_url
        )
    except RuntimeError:
        raise
    except Exception as e:
        raise RuntimeError(f"execute_db failed: {e}") from e

    # Outcome log — row count if result is list-shaped, else type
    try:
        if isinstance(result, list):
            _log.info("    [execute_db] result=%d rows", len(result))
        elif isinstance(result, dict) and "rows" in result:
            _log.info("    [execute_db] result=%d rows", len(result["rows"]))
        else:
            _log.info("    [execute_db] result=%s", type(result).__name__)
    except Exception:
        _log.info("    [execute_db] completed")
    return result
