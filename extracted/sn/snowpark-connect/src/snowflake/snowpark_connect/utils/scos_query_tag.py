#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#
"""Statement-level JSON QUERY_TAG enrichment from client stack traces.

Injection is wired at two Snowpark entry points:

- ``cursor.execute`` (via describe-cache wrapper): ``session.sql(...).collect()``,
  DDL/catalog SQL, and describe queries.
- ``ServerConnection.execute`` (via ``instrument_session_for_scos_query_tag``):
  compiled-plan terminal actions such as ``collect()``, ``to_arrow``, and async
  paths that bypass ``cursor.execute``.

On the sync plan path Snowpark may call both; ``inject_query_tag_kwargs`` skips
re-injection when ``QUERY_TAG`` is already present in ``_statement_params``.
"""
from __future__ import annotations

import json
import os
from typing import Any

from snowflake import snowpark
from snowflake.snowpark._internal.server_connection import ServerConnection
from snowflake.snowpark._internal.utils import QUERY_TAG_STRING
from snowflake.snowpark.exceptions import SnowparkClientException
from snowflake.snowpark.session import _get_active_session
from snowflake.snowpark_connect.server_common import _client_telemetry_context

DEFAULT_SCOS_QUERY_TAG = "SNOWPARK_CONNECT_QUERY"
SNOWFLAKE_QUERY_TAG_MAX_LENGTH = 2000


def _is_add_debug_info_to_query_tag_enabled() -> bool:
    from snowflake.snowpark_connect.config import is_add_debug_info_to_query_tag_enabled

    return is_add_debug_info_to_query_tag_enabled()


def store_client_stack_trace(client_stack_info: list[dict[str, Any]] | None) -> None:
    _client_telemetry_context.stack_trace = client_stack_info


def clear_client_stack_trace() -> None:
    _client_telemetry_context.stack_trace = None


def get_client_stack_trace() -> list[dict[str, Any]] | None:
    return getattr(_client_telemetry_context, "stack_trace", None)


def get_effective_base_tag(session: snowpark.Session | None) -> str:
    if session is None:
        return DEFAULT_SCOS_QUERY_TAG
    return session.query_tag or DEFAULT_SCOS_QUERY_TAG


def _get_session_for_query_tag() -> snowpark.Session | None:
    """Return the active Snowpark session without CLD re-entrancy.

    ``get_or_create_snowpark_session()`` must not be used from execute hooks:
    it calls ``_ensure_cld_context_for_session``, which can issue SQL while
    another statement is already in flight on the same connection (deadlock
    during server startup and internal queries).
    """
    try:
        return _get_active_session()
    except SnowparkClientException as ex:
        if ex.error_code == "1403":
            return None
        raise


def get_top_client_stack_frame() -> dict[str, Any] | None:
    stack = get_client_stack_trace()
    if not stack:
        return None
    return stack[0]


def _parse_tag_object(base: str | None) -> dict[str, Any] | None:
    """Return *base* as a dict when it is a JSON object, else ``None``.

    The session-level base tag may itself be a JSON object (e.g. the unified-
    workload ``{"uw_workload":..,"uw_iteration":..}`` context set on the session
    by the ``snowpark.connect.test.uw_context`` config). When it is, its keys are
    merged into the per-statement tag rather than nested under ``"tag"`` as an
    opaque string, so ``uw_*`` attribution survives alongside the caller frame.
    """
    if not base:
        return None
    try:
        parsed = json.loads(base)
    except (TypeError, ValueError):
        return None
    return parsed if isinstance(parsed, dict) else None


def _add_rpc_context(payload: dict[str, Any]) -> None:
    """Fold server-intrinsic RPC facts into the tag (best-effort).

    ``rpc`` is the Spark Connect request type (``ExecutePlan`` vs ``AnalyzePlan``)
    and ``op`` is the terminal operation verb (``collect``, ``aggregate``, ...) of
    the RPC under which this query ran. Both are cached per-request on the
    telemetry thread-local by the server RPC handler. They identify the ENCLOSING
    RPC, not real-work-vs-metadata on their own: a single ExecutePlan can emit
    several Snowflake queries (the action plus nested describe/metadata queries),
    and they all inherit the same ``rpc``/``op``. Server facts are authoritative
    for the statement, so they overwrite any value already on the payload.
    """
    try:
        from snowflake.snowpark_connect.server_common import (
            get_rpc_type,
            get_terminal_op,
        )
    except Exception:  # pragma: no cover - defensive import guard
        return
    rpc = get_rpc_type()
    if rpc:
        payload["rpc"] = str(rpc)
    op = get_terminal_op()
    if op:
        payload["op"] = str(op)


def build_scos_query_tag_json(
    session: snowpark.Session | None,
    frame: dict[str, Any] | None = None,
) -> str:
    # Merge the effective base tag with the caller frame. Lift ONLY the uw_*
    # attribution keys to top level (that is our unified-workload context); any
    # other base tag -- including a user's structured JSON QUERY_TAG -- is kept
    # verbatim under ``tag`` so it is never silently clobbered. Always emit JSON,
    # never the bare ``SNOWPARK_CONNECT_QUERY`` string. (SNOW-4183579)
    base = get_effective_base_tag(session)
    parsed = _parse_tag_object(base)
    payload: dict[str, Any]
    if parsed is not None:
        uw_keys = {k: v for k, v in parsed.items() if str(k).startswith("uw_")}
        if uw_keys:
            non_uw = {k: v for k, v in parsed.items() if not str(k).startswith("uw_")}
            payload = {**non_uw, **uw_keys}
            payload.setdefault("tag", DEFAULT_SCOS_QUERY_TAG)
        else:
            # Foreign JSON tag with no uw_* context: preserve it verbatim.
            payload = {"tag": base}
    else:
        payload = {"tag": base or DEFAULT_SCOS_QUERY_TAG}

    if frame is None:
        frame = get_top_client_stack_frame()
    if frame:
        file_name = frame.get("file_name")
        line_number = frame.get("line_number")
        method_name = frame.get("method_name")
        if file_name and line_number is not None:
            payload["file"] = os.path.basename(str(file_name))
            payload["line"] = int(line_number)
        if method_name:
            payload["fn"] = str(method_name)

    _add_rpc_context(payload)
    return _fit_query_tag_json(payload)


def _fit_query_tag_json(payload: dict[str, Any]) -> str:
    trimmed = dict(payload)

    encoded = json.dumps(trimmed, separators=(",", ":"))
    if len(encoded) <= SNOWFLAKE_QUERY_TAG_MAX_LENGTH:
        return encoded

    # ``uw_*`` attribution keys are the highest priority (the whole point of the
    # tag) and are preserved through every step below. Drop the RPC facts and the
    # function name first, then truncate the (possibly user-supplied) ``tag``
    # value, then drop the caller frame -- so a non-UW user's debug frame outlives
    # the truncation of a large tag they already have.
    for droppable in ("fn", "op", "rpc"):
        if droppable in trimmed:
            trimmed.pop(droppable)
            encoded = json.dumps(trimmed, separators=(",", ":"))
            if len(encoded) <= SNOWFLAKE_QUERY_TAG_MAX_LENGTH:
                return encoded

    tag = str(trimmed.get("tag", DEFAULT_SCOS_QUERY_TAG))
    if len(tag) > 1:
        over = len(encoded) - SNOWFLAKE_QUERY_TAG_MAX_LENGTH
        trimmed["tag"] = tag[: max(1, len(tag) - over)]
        encoded = json.dumps(trimmed, separators=(",", ":"))
        if len(encoded) <= SNOWFLAKE_QUERY_TAG_MAX_LENGTH:
            return encoded

    # Drop the caller frame as a pair (``file`` without ``line`` is awkward for
    # consumers that render ``file:line``).
    if "line" in trimmed or "file" in trimmed:
        trimmed.pop("line", None)
        trimmed.pop("file", None)
        encoded = json.dumps(trimmed, separators=(",", ":"))
        if len(encoded) <= SNOWFLAKE_QUERY_TAG_MAX_LENGTH:
            return encoded

    # Last resort: keep whatever ``uw_*`` attribution fits plus a tag marker.
    # Re-encode a shrinking dict rather than byte-slicing the JSON string, so the
    # result is always valid JSON (a truncated string would make downstream
    # parsers drop ALL attribution). If the uw_* values themselves overflow the
    # cap, drop them one at a time; ``{"tag": DEFAULT}`` is short and always fits.
    protected = {k: v for k, v in trimmed.items() if k.startswith("uw_")}
    protected["tag"] = DEFAULT_SCOS_QUERY_TAG
    encoded = json.dumps(protected, separators=(",", ":"))
    if len(encoded) <= SNOWFLAKE_QUERY_TAG_MAX_LENGTH:
        return encoded
    for key in [k for k in protected if k != "tag"]:
        protected.pop(key)
        encoded = json.dumps(protected, separators=(",", ":"))
        if len(encoded) <= SNOWFLAKE_QUERY_TAG_MAX_LENGTH:
            return encoded
    return encoded


def enrich_statement_params(
    statement_params: dict[str, str] | None,
    session: snowpark.Session | None,
) -> dict[str, str] | None:
    if not _is_add_debug_info_to_query_tag_enabled():
        return statement_params

    result = dict(statement_params or {})
    result[QUERY_TAG_STRING] = build_scos_query_tag_json(session)
    return result


def inject_query_tag_kwargs(
    kwargs: dict[str, Any],
    session: snowpark.Session | None = None,
) -> dict[str, Any]:
    if not _is_add_debug_info_to_query_tag_enabled():
        return kwargs
    params = kwargs.get("_statement_params")
    if params and QUERY_TAG_STRING in params:
        return kwargs
    if session is None:
        session = _get_session_for_query_tag()
    kwargs["_statement_params"] = enrich_statement_params(params, session)
    return kwargs


def instrument_session_for_scos_query_tag(session: snowpark.Session) -> None:
    if getattr(session, "_scos_query_tag_instrumented", False):
        return

    conn = session._conn
    if not isinstance(conn, ServerConnection):
        return

    if not getattr(conn, "_scos_query_tag_execute_wrapped", False):
        original_execute = conn.execute

        def execute_with_query_tag(self, *args, **kwargs):
            inject_query_tag_kwargs(kwargs, session=session)
            return original_execute(*args, **kwargs)

        conn.execute = execute_with_query_tag.__get__(conn, type(conn))
        conn._scos_query_tag_execute_wrapped = True

    session._scos_query_tag_instrumented = True
