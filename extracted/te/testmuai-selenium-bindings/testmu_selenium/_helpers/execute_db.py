"""execute_db helper — runs a SQL query via the automind /db-query endpoint.

Sync version for the V3 Selenium runtime. Caller passes a pre-built Basic
auth header (base64 of "username:access_key"); this helper raises
RuntimeError when no auth_header is supplied. The LT_PROXY_TUNNEL_ID env-var
fallback is applied when tunnel_id is blank; a blank automind_url is resolved
from the binding config _config.get("automind_url") (set by configure();
initialized at import from AUTEUR_AUTOMIND > AUTOMIND_URL > prod).

Raises:
    RuntimeError: When auth_header is missing, on non-200 response, or on
        network failure.

Returns:
    Query result dict on success.
"""
import base64
import json
import logging
import os

_log = logging.getLogger("testmu_selenium")


def execute_db(
    query,
    db_id="",
    db_name="",
    timeout=10000,
    tunnel_id="",
    auth_header="",
    automind_url="",
):
    """Execute a database query via the automind /db-query endpoint.

    Args:
        query: Base64-encoded SQL query string.
        db_id: Database connection identifier.
        db_name: Database name.
        timeout: Query timeout in milliseconds (default 10000).
        tunnel_id: Tunnel ID for network connectivity. Falls back to
            LT_PROXY_TUNNEL_ID env var when blank.
        auth_header: Base64-encoded "username:access_key" string. When blank,
            it is built from the LT_USERNAME/LT_ACCESS_KEY env vars (the code
            generator emits an empty value because credentials must not be baked
            into exported tests). Raises RuntimeError only when it is blank and
            those creds are also absent.
        automind_url: Automind service base URL. When blank, resolved from the
            binding config _config.get("automind_url") (set by configure();
            initialized at import from AUTEUR_AUTOMIND > AUTOMIND_URL > prod).

    Returns:
        Query result dict on success.

    Raises:
        RuntimeError: When no auth_header can be resolved, on non-200 response,
            or on network/query failure.
    """
    import requests as _requests

    # Fall back to environment variables for non-secret args. Resolve the URL from
    # the binding config (set by configure(); initialized at import from env).
    if not automind_url:
        from testmu_selenium import _config
        automind_url = _config.get("automind_url")
    if not tunnel_id:
        tunnel_id = os.environ.get("LT_PROXY_TUNNEL_ID", "")

    # Auth header: built by the caller, or derived from LT creds in the
    # environment (parity with the V2 db_query implementation and the Playwright binding).
    if not auth_header:
        username = os.environ.get("LT_USERNAME", "")
        access_key = os.environ.get("LT_ACCESS_KEY", "")
        if username and access_key:
            auth_header = base64.b64encode(f"{username}:{access_key}".encode()).decode()

    # Auth gate — no caller-supplied header and no LT creds means no way to auth.
    if not auth_header:
        raise RuntimeError("execute_db: auth_header is required")

    _log.info("    [execute_db] db_id=%r db_name=%r", db_id, db_name)

    # Resolve variable templates ({{name}} / ${name}) embedded in the query.
    # The query arrives as a base64-encoded string; mirror the V2 source:
    # decode → resolve → re-encode before building the payload.
    try:
        _decoded = base64.b64decode(query).decode("utf-8")
    except Exception:
        _decoded = None
    if _decoded is not None:
        from testmu_selenium._vars import var as _var
        _resolved = _var(_decoded)
        if not isinstance(_resolved, str):
            _resolved = str(_resolved)
        query = base64.b64encode(_resolved.encode("utf-8")).decode("utf-8")

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

    try:
        resp = _requests.post(url, json=payload, headers=headers)
    except RuntimeError:
        raise
    except Exception as e:
        raise RuntimeError(f"execute_db failed: {e}") from e

    if resp.status_code != 200:
        raise RuntimeError(f"DB query failed: status={resp.status_code} body={resp.text}")

    result = resp.json()
    if isinstance(result, str):
        result = json.loads(result)
    if isinstance(result, dict) and "error" in result:
        raise RuntimeError(f"DB query error: {result['error']}")

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
