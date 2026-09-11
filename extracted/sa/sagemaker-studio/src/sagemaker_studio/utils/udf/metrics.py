"""Metrics for UDF routing decisions.

Emitted through the SDK's existing session-metric channel so UDF routing shows
up in the same place as session creation. Every function here swallows its own
errors: telemetry must never be able to break a UDF.
"""

from __future__ import annotations

import logging
from typing import Optional

from sagemaker_studio.utils.loggerutils import log_session_metric

logger = logging.getLogger("SparkConnect")


def record_route_decision(
    *,
    capability: str,
    worker_python: str,
    client_python: str,
    spark_version: str,
    source: str,
    routed: bool,
    session_id: Optional[str] = None,
) -> None:
    """One metric per UDF whose route was decided.

    ``routed`` distinguishes the sidecar path from the untouched local build, and
    ``source`` records HOW the worker version was detected -- which is what tells
    us whether the static fallback map is still being relied on in the fleet.
    """
    try:
        log_session_metric(
            metric_name="UDFRouteDecision",
            session_id=session_id,
            duration_ms=0,
            additional_properties={
                "Capability": capability,
                "WorkerPython": worker_python,
                "ClientPython": client_python,
                "SparkVersion": spark_version,
                "DetectionSource": source,
                "Routed": "true" if routed else "false",
            },
        )
    except Exception as e:
        logger.debug("could not emit UDFRouteDecision: %s", e)


def record_sidecar_failure(
    *,
    capability: str,
    worker_python: str,
    spark_version: str,
    error_class: str,
    session_id: Optional[str] = None,
) -> None:
    """One metric per UDF build that failed in or on the way to the sidecar."""
    try:
        log_session_metric(
            metric_name="UDFSidecarFailure",
            session_id=session_id,
            duration_ms=0,
            additional_properties={
                "Capability": capability,
                "WorkerPython": worker_python,
                "SparkVersion": spark_version,
                "ErrorClass": error_class,
            },
        )
    except Exception as e:
        logger.debug("could not emit UDFSidecarFailure: %s", e)
