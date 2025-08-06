import logging
from typing import Any, Optional

from datetime import datetime, timezone
from google.protobuf import json_format, field_mask_pb2, struct_pb2

import va.protos.orby.va.public.execution_messages_pb2 as execution_messages
import va.protos.orby.va.public.execution_service_pb2_grpc as execution_service_grpc
from va.protos.orby.va.public.execution_messages_pb2 import ExecutionStatus
from va.store.execution.execution_client import get_execution_client
from va.utils.auth import get_credential

import os

logger = logging.getLogger(__name__)


def _get_org_and_user_ids() -> tuple[Optional[str], Optional[str]]:
    """Return the active (org_id, user_id) tuple.

    * *org_id* is taken from the credential loaded via :func:`va.utils.auth.get_credential`
      as a fallback, the ``ORBY_ORG_ID`` environment variable.
    * *user_id* is extracted from the ``sub`` claim of the access-token.
      If the token is missing or malformed the function returns ``None``.
    """

    # TODO: update this method once we have a way to get the org_id and user_id from the execution service
    credential = None
    try:
        credential = get_credential()
    except Exception as e:
        logger.error(f"Failed to get credential from file: {e}")

    org_id: Optional[str] = credential.org_id if credential else None
    org_id = org_id or os.getenv("ORBY_ORG_ID")
    user_id = os.getenv("ORBY_USER_ID")

    return org_id, user_id


def update_execution_status(
    execution_id: str, status: ExecutionStatus.ValueType
) -> None:
    """
    Update the status of an execution.

    Args:
        execution_id: The id of the execution to be updated.
        status: The desired status (value from :class:`~va.protos.orby.va.public.execution_messages_pb2.ExecutionStatus`).
        org_id: Optional organization identifier to include as gRPC metadata.
    """
    try:
        execution_client = get_execution_client()
        execution_stub = execution_service_grpc.ExecutionServiceStub(
            execution_client._grpc_channel
        )

        org_id, user_id = _get_org_and_user_ids()

        metadata: list[tuple[str, str]] = []
        if org_id:
            metadata.append(("orby-org-id", org_id))
        if user_id:
            metadata.append(("orby-user-id", user_id))

        # Prepare field mask to update only the status field.
        mask = field_mask_pb2.FieldMask(paths=["status"])
        request = execution_messages.UpdateExecutionRequest(
            execution_id=execution_id, status=status, field_mask=mask
        )
        execution_client.call_grpc_channel(
            execution_stub.UpdateExecution, request, metadata=metadata
        )
        logger.info(f"Updated execution {execution_id} to status {status}")
    except Exception as e:
        logger.error(f"Failed to update execution {execution_id}: {e}")
        raise


def append_execution_log(
    execution_id: str,
    description: str,
    metadata: Optional[dict[str, Any]] = None,
    step_id: Optional[int] = None,
    screenshot: Optional[str] = None,
):
    """
    Append a log to an execution.

    Args:
        execution_id: The id of the execution to append the log to.
        description: The description of the log.
        metadata: Optional JSON-serialisable extra payload attached to the log entry.
            A UTC ISO-8601 timestamp will be added automatically if the caller
            does not supply one under the "timestamp" key.

    Returns:
        The id of the new log entry (if call succeeds) or None if call fails.
    """
    try:
        execution_client = get_execution_client()
        execution_stub = execution_service_grpc.ExecutionServiceStub(
            execution_client._grpc_channel
        )

        org_id, user_id = _get_org_and_user_ids()

        log = execution_messages.ExecutionLog(
            org_id=org_id or "",
            execution_id=execution_id,
            description=description,
        )
        if step_id is not None:
            log.step_id = step_id

        if screenshot is not None:
            log.screenshot = screenshot

        if metadata is None:
            metadata = {}

        metadata.setdefault("timestamp", datetime.now(timezone.utc).isoformat())

        # Convert the dict into a protobuf Struct and attach it to the log.
        log.metadata.CopyFrom(json_format.ParseDict(metadata, struct_pb2.Struct()))

        # gRPC metadata (headers)
        grpc_metadata: list[tuple[str, str]] = []
        if org_id:
            grpc_metadata.append(("orby-org-id", org_id))
        if user_id:
            grpc_metadata.append(("orby-user-id", user_id))

        request = execution_messages.AppendExecutionLogRequest(log=log)
        response = execution_client.call_grpc_channel(
            execution_stub.AppendExecutionLog, request, metadata=grpc_metadata
        )
        logger.info(f"Appended log to execution {execution_id}")
        return response.id
    except Exception as e:
        logger.error(f"Failed to append execution log: {e}")
        return None


def request_review(execution_id: str, instruction: str = ""):
    execution_client = get_execution_client()
    execution_stub = execution_service_grpc.ExecutionServiceStub(
        execution_client._grpc_channel
    )
    request = execution_messages.RequestReviewRequest(
        execution_id=execution_id, user_message=instruction
    )
    response = execution_client.call_grpc_channel(execution_stub.RequestReview, request)
    return response.review_id


def get_review_status(review_id: str):
    try:
        execution_client = get_execution_client()
        execution_stub = execution_service_grpc.ExecutionServiceStub(
            execution_client._grpc_channel
        )
        request = execution_messages.GetReviewStatusRequest(review_id=review_id)
        response = execution_client.call_grpc_channel(
            execution_stub.GetReviewStatus, request
        )
        return response.status
    except Exception as e:
        logger.error(f"Failed to fetch review status: {e}")
        return None
