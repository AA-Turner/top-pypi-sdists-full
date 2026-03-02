"""Upload Session Documents"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status


def _build_request_args(
    session_id: str,
    job_id: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v2/sessions/{session_id}/jobs/{job_id}/documents/upload"

    headers: dict[str, str] = {}
    if authorization is not None:
        headers["authorization"] = authorization
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "POST",
        "url": url,
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    session_id: str,
    job_id: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> Any:
    """Receive documents from interface and upload to S3.

    Called by interface when it stops recording or when agents upload documents.

    Supports two upload modes:

    1. Single file upload with explicit type/label:
        - file: <file>
        - document_type: "log"
        - label: "Shell Logs" (optional)

    2. Multi-file upload (field name = document type):
        - screen_recording: <file>
        - ui_events: <file>
        - label_screen_recording: "Screen Recording" (optional)
        - label_ui_events: "UI Events" (optional)

    Flow:
    1. Parse multipart form upload
    2. Upload each document to S3 using field name or document_type as type
    3. Store S3 URIs and labels in session_documents table
    4. Return success response"""

    request_args = _build_request_args(
        session_id=session_id,
        job_id=job_id,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return response.json()


async def asyncio(
    client: httpx.AsyncClient,
    session_id: str,
    job_id: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> Any:
    """Receive documents from interface and upload to S3.

    Called by interface when it stops recording or when agents upload documents.

    Supports two upload modes:

    1. Single file upload with explicit type/label:
        - file: <file>
        - document_type: "log"
        - label: "Shell Logs" (optional)

    2. Multi-file upload (field name = document type):
        - screen_recording: <file>
        - ui_events: <file>
        - label_screen_recording: "Screen Recording" (optional)
        - label_ui_events: "UI Events" (optional)

    Flow:
    1. Parse multipart form upload
    2. Upload each document to S3 using field name or document_type as type
    3. Store S3 URIs and labels in session_documents table
    4. Return success response"""

    request_args = _build_request_args(
        session_id=session_id,
        job_id=job_id,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return response.json()
