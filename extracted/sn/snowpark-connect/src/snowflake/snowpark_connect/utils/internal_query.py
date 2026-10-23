#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#
"""Helpers for running SCOS-internal SQL without emitting telemetry/traces."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from snowflake.snowpark_connect.utils.scos_query_tag import scos_internal_query_tag

if TYPE_CHECKING:
    from snowflake.snowpark import DataFrame


def collect_without_telemetry(df: DataFrame, *, block: bool = True) -> Any:
    """Execute ``df`` like ``collect()``/``collect_nowait()`` but without an
    OpenTelemetry span or Snowpark usage telemetry, and tagged as SCOS-internal.

    SCOS issues a handful of setup queries around (and before) real user
    requests: session configuration, resource warmup, session registration and
    CLD detection. When routed through the public ``collect()`` action these
    surface as generic ``collect`` spans in the trace UI and drown out the
    operations the user actually cares about. Executing them via the
    telemetry-free internal API keeps them out of the trace while still running
    identical SQL.

    These queries do still appear in Snowflake query history, so they also get
    the ``SCOS_INTERNAL_QUERY`` tag here — every caller of this helper is by
    definition issuing SCOS plumbing SQL, which is exactly what that tag marks.
    Without it they inherit the in-flight user statement's client stack frame
    and query history attributes them to a user file/line.

    This mirrors ``snowflake.snowpark.Session._get_remote_query_tag``, which
    uses the same private DataFrame API to keep internal bookkeeping queries
    out of telemetry.

    Args:
        df: The DataFrame whose plan should be executed.
        block: When ``False`` returns immediately with an ``AsyncJob`` (the
            ``collect_nowait()`` equivalent).
    """
    with scos_internal_query_tag():
        return df._internal_collect_with_tag_no_telemetry(block=block)
