#
# Copyright 2026 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from __future__ import annotations

import os
from typing import TYPE_CHECKING, Dict, Optional

if TYPE_CHECKING:
    from opentelemetry.sdk.resources import Resource


def create_dr_resource(
    entity_type: str,
    entity_id: str,
    *,
    service_priority: str = "p1",
    extra_attrs: Optional[Dict[str, str]] = None,
) -> "Resource":
    """Build an OpenTelemetry Resource with DataRobot-standard attributes.

    Args:
        entity_type: DataRobot entity type (e.g. ``"experiment_container"``).
        entity_id: DataRobot entity ID.
        service_priority: Value for ``datarobot.service.priority``. Defaults to ``"p1"``.
        extra_attrs: Additional or override attributes merged last, taking precedence
            over all computed values.

    Returns:
        An ``opentelemetry.sdk.resources.Resource`` ready to pass to a
        ``TracerProvider`` / ``MeterProvider`` / ``LoggerProvider``.

    Raises:
        ImportError: If ``opentelemetry-sdk`` is not installed. Install the
            ``datarobot[otel]`` extra to add it.

    Note:
        ``service.name`` is only set when ``OTEL_SERVICE_NAME`` is absent from the
        environment — ``Resource.create()`` merges env vars at lower precedence than
        explicit attrs, so setting it here would shadow any platform-provided value.
    """
    try:
        from opentelemetry.sdk.resources import Resource
    except ImportError as exc:
        raise ImportError(
            "opentelemetry-sdk is required to use create_dr_resource. Install it with: pip install 'datarobot[otel]'"
        ) from exc

    attrs: Dict[str, str] = {"datarobot.service.priority": service_priority}

    if not os.environ.get("OTEL_SERVICE_NAME"):
        attrs["service.name"] = f"{entity_type}-{entity_id}"

    if entity_id:
        attrs["datarobot.application.id"] = entity_id

    if os.environ.get("KUBERNETES_SERVICE_HOST"):
        pod_name = os.environ.get("HOSTNAME")
        if pod_name:
            attrs["k8s.pod.name"] = pod_name

    version = os.environ.get("APP_VERSION") or os.environ.get("SERVICE_VERSION")
    if version:
        attrs["service.version"] = version

    if extra_attrs:
        attrs.update(extra_attrs)

    return Resource.create(attrs)
