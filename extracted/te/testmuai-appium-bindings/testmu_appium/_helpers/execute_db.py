"""execute_db() — run a SQL query via the shared automind /db-query endpoint.

The base URL comes from the ``automind_url`` config slot, which defaults to
``_config._resolve_automind_url()`` (``AUTEUR_AUTOMIND`` > ``AUTOMIND_URL`` >
the prod default) and can be overridden through ``configure()``.

Endpoint path (``/db-query``), payload shape (``{"payload": {"id", "timeout",
"db_name", "tunnel_id"}, "query": ...}``), QUERY ENCODING and AUTH HEADER are
kept identical to the selenium/playwright siblings' ``execute_db`` so automind
sees one contract across bindings:

- ``query`` is base64-encoded SQL on the wire, both in and out. The helper
  decodes it, resolves ``{{var}}``/``${var}`` tokens in the SQL text, and
  re-encodes before building the payload — the same decode→resolve→re-encode
  the siblings do, and the shape automind's decoder expects. Plaintext SQL on
  the wire does not decode there.
- Auth is ``Authorization: Basic <base64 of "user:key">``, built explicitly
  rather than delegated to httpx's auth tuple, so an explicitly supplied
  ``auth_header`` lands in the same header with the same ``Basic `` prefix
  instead of being written raw.
"""
import base64
import binascii
import logging
import os

from testmu_appium import _config
from testmu_appium._helpers._http import request_with_retry
from testmu_appium._vars import set_var, var

_log = logging.getLogger("testmu_appium")


def _resolve_automind_url() -> str:
    """The configured automind host, else the env-driven default. Read live (not
    cached) so a host runtime publishing env after import is still honoured."""
    return _config.resolved("automind_url", _config._resolve_automind_url)


def _resolve_text(value: str) -> str:
    resolved = var(value)
    return resolved if isinstance(resolved, str) else str(resolved)


def _resolve_encoded_query(query: str) -> str:
    """Decode base64 SQL, resolve its variable tokens, re-encode.

    A query that does not decode is passed through untouched: the caller handed
    over something this helper cannot interpret, and mangling it into base64
    would corrupt a payload automind might otherwise have understood.
    """
    try:
        decoded = base64.b64decode(query, validate=True).decode("utf-8")
    except (binascii.Error, UnicodeDecodeError, ValueError):
        return query
    return base64.b64encode(_resolve_text(decoded).encode("utf-8")).decode("utf-8")


def _lt_credentials() -> str:
    """base64("user:key") from the LT environment, or "" when either is absent."""
    username = os.getenv("LT_USERNAME", "")
    accesskey = os.getenv("LT_ACCESS_KEY", "")
    if not (username and accesskey):
        return ""
    return base64.b64encode(f"{username}:{accesskey}".encode()).decode()


def execute_db(
    *,
    query: str,
    db_id: str = "",
    db_name: str = "",
    timeout: int | None = None,
    tunnel_id: str = "",
    auth_header: str = "",
    automind_url: str = "",
    output_variable: str = "",
    description: str = "",
) -> dict:
    """Run a SQL query against the automind ``/db-query`` endpoint.

    Args:
        query: Base64-encoded SQL text. The decoded SQL may carry
            ``{{var}}``/``${var}`` tokens; it is decoded, resolved and re-encoded
            before the request.
        db_id: Recorded connection id.
        db_name: Recorded database name.
        timeout: Query timeout in ms; defaults to 10000.
        tunnel_id: LT tunnel id; falls back to the LT_PROXY_TUNNEL_ID env var.
        auth_header: The base64 of ``"<username>:<access_key>"`` — the credential
            only, NOT a full header value: it is sent as
            ``Authorization: Basic <auth_header>``. When empty it is built from
            LT_USERNAME/LT_ACCESS_KEY (the code generator emits an empty value,
            because credentials must not be baked into an exported test).
        automind_url: Overrides the resolved automind host for this call.
        output_variable: When non-empty, the result dict is written via
            ``set_var(output_variable, result)``.
        description: Step description (logging only).

    Returns:
        The parsed query-result dict on success.

    Raises:
        RuntimeError: No auth_header and LT_USERNAME/LT_ACCESS_KEY are not set,
            the endpoint responded non-200, or the response body carries an
            "error" key.
    """
    credential = auth_header or _lt_credentials()
    if not credential:
        raise RuntimeError(
            "execute_db requires LT_USERNAME and LT_ACCESS_KEY (automind is an LT-hosted "
            "service), or an explicit auth_header"
        )

    host = automind_url or _resolve_automind_url()
    url = f"{host}/db-query"

    payload = {
        "payload": {
            "id": _resolve_text(db_id) if db_id else "",
            "timeout": 10000 if timeout is None else int(timeout),
            "db_name": _resolve_text(db_name) if db_name else "",
            "tunnel_id": tunnel_id or os.getenv("LT_PROXY_TUNNEL_ID", ""),
        },
        "query": _resolve_encoded_query(query),
    }
    _log.info(
        "[execute_db] db_id=%r db_name=%r",
        payload["payload"]["id"], payload["payload"]["db_name"],
    )

    response = request_with_retry(
        "POST", url,
        headers={
            "content-type": "application/json",
            "Authorization": f"Basic {credential}",
        },
        json_data=payload,
    )
    if response.status_code != 200:
        raise RuntimeError(
            f"execute_db: /db-query returned {response.status_code}: {response.text[:500]}"
        )

    result = response.json()
    if isinstance(result, dict) and "error" in result:
        raise RuntimeError(f"execute_db: query error: {result['error']}")

    _log.info("[execute_db] result=%s", type(result).__name__)
    if output_variable:
        set_var(output_variable, result)
    return result
