"""Sandbox host answers as values, or as the typed failure the protocol assigns to each status."""

import json
from collections.abc import Callable
from typing import ClassVar, TypeVar

from labqoat.json_document import JsonDocument
from labqoat.sandbox.sandbox_capacity_error import SandboxCapacityError
from labqoat.sandbox.sandbox_error import SandboxError
from labqoat.sandbox.sandbox_exists_error import SandboxExistsError
from labqoat.sandbox.sandbox_file_not_found_error import SandboxFileNotFoundError
from labqoat.sandbox.sandbox_image_not_allowed_error import SandboxImageNotAllowedError
from labqoat.sandbox.sandbox_invalid_request_error import SandboxInvalidRequestError
from labqoat.sandbox.sandbox_not_found_error import SandboxNotFoundError
from labqoat.sandbox.sandbox_timeout_error import SandboxTimeoutError
from labqoat.sandbox.sandbox_too_large_error import SandboxTooLargeError
from labqoat.sandbox.sandbox_unavailable_error import SandboxUnavailableError
from labqoat.sandbox.sandbox_write_error import SandboxWriteError

ValueT = TypeVar("ValueT")


class SandboxResponse:
    """Keep the meaning of every status in one place for the synchronous and asynchronous paths."""

    FAILURES: ClassVar[dict[int, type[SandboxError]]] = {
        403: SandboxImageNotAllowedError,
        404: SandboxNotFoundError,
        408: SandboxTimeoutError,
        409: SandboxExistsError,
        413: SandboxTooLargeError,
        422: SandboxInvalidRequestError,
        429: SandboxCapacityError,
    }
    REFINED: ClassVar[dict[tuple[int, str | None], type[SandboxError]]] = {
        (404, "file_not_found"): SandboxFileNotFoundError,
        (422, "write_failed"): SandboxWriteError,
    }

    @staticmethod
    def failure(status: int, content: bytes) -> SandboxError:
        """Choose the failure by status; every server error and unlisted status means unavailable infrastructure."""
        code, detail = SandboxResponse._problem(content)
        kind = SandboxResponse.REFINED.get((status, code)) or SandboxResponse.FAILURES.get(
            status, SandboxUnavailableError
        )
        reason = f" ({code})" if code else ""
        explanation = f": {detail}" if detail else ""
        return kind(f"Sandbox host returned HTTP {status}{reason}{explanation}", status, code, detail)

    @staticmethod
    def decoded(content: bytes, factory: Callable[[JsonDocument], ValueT]) -> ValueT:
        """Build a value from a JSON object; a body outside the protocol is an infrastructure failure."""
        try:
            return factory(JsonDocument.expect_dict(json.loads(content)))
        except (KeyError, TypeError, ValueError) as error:
            raise SandboxUnavailableError("Sandbox host returned a malformed response") from error

    @staticmethod
    def _problem(content: bytes) -> tuple[str | None, str | None]:
        """Read the protocol's error code and optional detail, tolerating any other body."""
        try:
            document = json.loads(content)
        except ValueError:
            return None, None
        if not isinstance(document, dict):
            return None, None
        code, detail = document.get("error"), document.get("detail")
        return (code if isinstance(code, str) else None), (detail if isinstance(detail, str) else None)
