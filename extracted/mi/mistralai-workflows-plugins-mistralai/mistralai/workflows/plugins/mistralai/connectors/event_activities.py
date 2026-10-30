"""Marker activities for connector-auth front-end discoverability.

These activities record return values as Temporal local-activity markers
(for la-console) **and** publish CustomTask events through the Abraxas
event stream (for le-chat and other SSE consumers).
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel

from mistralai.workflows.core._events.event_activities import emitter_activity, publish_emitter_event
from mistralai.workflows.core._events.event_utils import create_emitter_event_fields
from mistralai.workflows.protocol.v1.events import (
    CustomTaskCompleted,
    CustomTaskCompletedAttributes,
    CustomTaskFailed,
    CustomTaskFailedAttributes,
    CustomTaskStarted,
    CustomTaskStartedAttributes,
    Failure,
    JSONPayload,
)

CONNECTOR_AUTH_TASK_TYPE = "connector_auth"


class ConnectorAuthMarkerResult(BaseModel):
    task_id: str
    connector_name: str
    connector_id: str
    credentials_name: str | None = None
    auth_url: str | None = None
    error: str | None = None


def _connector_payload(
    connector_name: str,
    connector_id: str,
    credentials_name: str | None = None,
    *,
    status: str = "waiting_for_auth",
    **extra: Any,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "connector_name": connector_name,
        "connector_id": connector_id,
        "status": status,
    }
    if credentials_name is not None:
        payload["credentials_name"] = credentials_name
    payload.update(extra)
    return payload


@emitter_activity(name="__emit_connector_auth_started")
async def _emit_connector_auth_started(
    task_id: str,
    connector_name: str,
    connector_id: str,
    auth_url: str,
    credentials_name: str | None = None,
) -> ConnectorAuthMarkerResult:
    await publish_emitter_event(
        lambda: CustomTaskStarted(
            **create_emitter_event_fields("payload"),
            attributes=CustomTaskStartedAttributes(
                custom_task_id=task_id,
                custom_task_type=CONNECTOR_AUTH_TASK_TYPE,
                payload=JSONPayload(
                    value=_connector_payload(
                        connector_name,
                        connector_id,
                        credentials_name=credentials_name,
                        auth_url=auth_url,
                    )
                ),
            ),
        )
    )
    return ConnectorAuthMarkerResult(
        task_id=task_id,
        connector_name=connector_name,
        connector_id=connector_id,
        credentials_name=credentials_name,
        auth_url=auth_url,
    )


@emitter_activity(name="__emit_connector_auth_completed")
async def _emit_connector_auth_completed(
    task_id: str,
    connector_name: str,
    connector_id: str,
    credentials_name: str | None = None,
) -> ConnectorAuthMarkerResult:
    await publish_emitter_event(
        lambda: CustomTaskCompleted(
            **create_emitter_event_fields("payload"),
            attributes=CustomTaskCompletedAttributes(
                custom_task_id=task_id,
                custom_task_type=CONNECTOR_AUTH_TASK_TYPE,
                payload=JSONPayload(
                    value=_connector_payload(
                        connector_name,
                        connector_id,
                        credentials_name=credentials_name,
                        status="connected",
                    )
                ),
            ),
        )
    )
    return ConnectorAuthMarkerResult(
        task_id=task_id,
        connector_name=connector_name,
        connector_id=connector_id,
        credentials_name=credentials_name,
    )


@emitter_activity(name="__emit_connector_auth_failed")
async def _emit_connector_auth_failed(
    task_id: str,
    connector_name: str,
    connector_id: str,
    error: str,
    credentials_name: str | None = None,
) -> ConnectorAuthMarkerResult:
    await publish_emitter_event(
        lambda: CustomTaskFailed(
            **create_emitter_event_fields("payload"),
            attributes=CustomTaskFailedAttributes(
                custom_task_id=task_id,
                custom_task_type=CONNECTOR_AUTH_TASK_TYPE,
                failure=Failure(message=f"[{connector_id}:{connector_name}] {error}"),
            ),
        )
    )
    return ConnectorAuthMarkerResult(
        task_id=task_id,
        connector_name=connector_name,
        connector_id=connector_id,
        credentials_name=credentials_name,
        error=error,
    )
