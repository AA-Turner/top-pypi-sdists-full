"""Bound and validate duplex JSON frames independently of sockets and event loops."""

import json
from collections.abc import Mapping
from typing import ClassVar

from labqoat.json_document import JsonDocument, JsonValue
from labqoat.worker.rejection_advice import RejectionAdvice
from labqoat.worker.worker_api_error import WorkerApiError


class SessionFrames:
    """Preserve exact JSON values and keep protocol failures free of authored payloads."""

    maximum: ClassVar[int] = 16_777_216

    @staticmethod
    def encode(document: Mapping[str, JsonValue]) -> str:
        """Reject non-JSON values and oversized outgoing frames before transport."""
        text = json.dumps(document, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
        if len(text.encode()) > SessionFrames.maximum:
            raise WorkerApiError("Worker session frame exceeds its limit", 413)
        return text

    @staticmethod
    def decode(text: str | bytes) -> JsonDocument:
        """Require one bounded object without reflecting malformed response contents."""
        if len(text.encode() if isinstance(text, str) else text) > SessionFrames.maximum:
            raise WorkerApiError("Worker session response exceeds its limit", 502)
        try:
            return JsonDocument.expect_dict(json.loads(text))
        except (ValueError, TypeError) as error:
            raise WorkerApiError("Worker session response is invalid", 502) from error

    @staticmethod
    def result(frame: JsonDocument) -> JsonDocument:
        """Interpret a durable receipt without exposing server exception details."""
        if "error" in frame:
            status = JsonDocument.expect_scalar(frame.get("status", 409), int)
            error = WorkerApiError.coded("Worker session command was rejected", status, frame["error"])
            raise WorkerApiError(f"{error}{RejectionAdvice.explain(error.code)}", status, error.code)
        return JsonDocument.expect_dict(frame["data"])
