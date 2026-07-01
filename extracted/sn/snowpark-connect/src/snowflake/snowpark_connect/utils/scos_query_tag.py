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


def build_scos_query_tag_json(
    session: snowpark.Session | None,
    frame: dict[str, Any] | None = None,
) -> str:
    payload: dict[str, Any] = {"tag": get_effective_base_tag(session)}
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

    return _fit_query_tag_json(payload)


def _fit_query_tag_json(payload: dict[str, Any]) -> str:
    trimmed = dict(payload)

    encoded = json.dumps(trimmed, separators=(",", ":"))
    if len(encoded) <= SNOWFLAKE_QUERY_TAG_MAX_LENGTH:
        return encoded

    if "fn" in trimmed:
        trimmed.pop("fn")
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

    encoded = json.dumps({"tag": DEFAULT_SCOS_QUERY_TAG}, separators=(",", ":"))
    return encoded[:SNOWFLAKE_QUERY_TAG_MAX_LENGTH]


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
