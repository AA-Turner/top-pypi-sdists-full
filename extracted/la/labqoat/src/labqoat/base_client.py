"""Base HTTP behavior for typed management clients."""

from __future__ import annotations

import gzip
import json
from collections.abc import Callable, Iterator, Mapping
from contextlib import contextmanager
from typing import TYPE_CHECKING, TypeVar
from urllib.parse import quote, urlsplit

from labqoat.errors.api_error import ApiError
from labqoat.errors.authentication_error import AuthenticationError
from labqoat.errors.transport_error import TransportError
from labqoat.json_document import JsonDocument, JsonValue
from labqoat.net.api_retry import ApiRetry
from labqoat.net.http_error import HttpError
from labqoat.net.http_timeout_error import HttpTimeoutError

if TYPE_CHECKING:
    from labqoat._generated.transport import Transport
    from labqoat.net.response import Response

ModelT = TypeVar("ModelT")


class BaseClient:
    """Shared request, pagination, and error handling."""

    COMPRESSED_FROM = 16_384

    def __init__(self, transport: Transport) -> None:
        """Store the shared transport."""
        self._transport = transport

    def send(self, method: str, path: str) -> Response:
        """Send a request and raise typed errors."""
        response = self.request(method, path)
        BaseClient.raise_for_status(path, response)
        return response

    def send_json(
        self,
        method: str,
        path: str,
        payload: JsonValue | Mapping[str, JsonValue],
        *,
        idempotency_key: str | None = None,
    ) -> Response:
        """Send a JSON request and raise typed errors."""
        body = json.dumps(payload).encode()
        encoding = None
        if len(body) >= BaseClient.COMPRESSED_FROM:
            body, encoding = gzip.compress(body, compresslevel=6, mtime=0), "gzip"
        response = self.request(
            method,
            path,
            content=body,
            content_type="application/json",
            idempotency_key=idempotency_key,
            content_encoding=encoding,
        )
        BaseClient.raise_for_status(path, response)
        return response

    def send_content(
        self,
        method: str,
        path: str,
        content: bytes | Iterator[bytes],
        content_type: str,
        content_length: int | None = None,
    ) -> Response:
        """Send byte or streaming content and raise typed errors."""
        response = self.request(method, path, content=content, content_type=content_type, content_length=content_length)
        BaseClient.raise_for_status(path, response)
        return response

    def request(
        self,
        method: str,
        path: str,
        content: bytes | Iterator[bytes] | None = None,
        content_type: str | None = None,
        content_length: int | None = None,
        idempotency_key: str | None = None,
        content_encoding: str | None = None,
    ) -> Response:
        """Normalize every HTTP transport failure and send again after a temporary refusal (``ApiRetry``)."""
        retry = ApiRetry(method, content, idempotency_key)
        while True:
            try:
                response = self._transport.request(
                    method,
                    path,
                    content=content,
                    content_type=content_type,
                    content_length=content_length,
                    idempotency_key=idempotency_key,
                    content_encoding=content_encoding,
                )
            except HttpTimeoutError as error:
                raise TransportError(f"Request to {path} exceeded its deadline.", timed_out=True) from error
            except HttpError as error:
                if retry.lost():
                    continue
                raise TransportError(f"Could not reach the API at {path}.") from error
            if response.status_code < 400 or not retry.refused(
                response.status_code, response.content, response.headers.get("retry-after")
            ):
                return response

    @contextmanager
    def stream_response(
        self,
        method: str,
        path: str,
        content: bytes | Iterator[bytes] | None = None,
        content_type: str | None = None,
        event_stream: bool = False,
    ) -> Iterator[Response]:
        """Open a streaming response with normalized failures."""
        try:
            with self._transport.stream(
                method, path, content=content, content_type=content_type, event_stream=event_stream
            ) as response:
                if not 200 <= response.status_code < 300:
                    response.read()
                BaseClient.raise_for_status(path, response)
                yield response
        except HttpTimeoutError as error:
            raise TransportError(f"Request to {path} exceeded its deadline.", timed_out=True) from error
        except HttpError as error:
            raise TransportError(f"Could not reach the API at {path}.") from error

    def decode(self, response: Response, path: str, factory: Callable[[Mapping[str, JsonValue]], ModelT]) -> ModelT:
        """Decode a JSON object response into a typed model."""
        try:
            data = json.loads(response.text or "{}")
        except ValueError as error:
            raise ApiError(f"invalid JSON from {path}: {error}") from error
        try:
            return factory(data)
        except (KeyError, TypeError, ValueError) as error:
            raise ApiError(f"malformed response from {path}: {error}") from error

    def close(self) -> None:
        """Release the underlying connection."""
        self._transport.close()

    @staticmethod
    def raise_for_status(path: str, response: Response) -> None:
        """Map HTTP failures to safe typed Problem Details errors."""
        if 200 <= response.status_code < 300:
            return
        problem = BaseClient.problem_document(response)
        detail = BaseClient.problem_detail(problem, path)
        request_id = response.headers.get("x-request-id")
        retry_after = response.headers.get("retry-after")
        if response.status_code in (401, 403):
            detail = BaseClient.authentication_detail(problem)
            raise AuthenticationError(
                detail,
                status=response.status_code,
                problem=problem,
                request_id=request_id,
                retry_after=retry_after,
            )
        raise ApiError(
            detail,
            status=response.status_code,
            problem=problem,
            request_id=request_id,
            retry_after=retry_after,
        )

    @staticmethod
    def authentication_detail(problem: JsonDocument | None) -> str:
        """Render an authentication detail without exposing request material."""
        if problem is not None and problem.get("detail"):
            return str(problem["detail"])
        return "Authentication failed."

    @staticmethod
    def problem_document(response: Response) -> JsonDocument | None:
        """Decode a Problem Details object when one is present."""
        try:
            value = response.json()
        except (ValueError, UnicodeDecodeError):
            return None
        return JsonDocument(value) if isinstance(value, dict) else None

    @staticmethod
    def problem_detail(problem: JsonDocument | None, path: str) -> str:
        """Render title, detail, and field errors without losing context."""
        if problem is None:
            return f"Request to {path} failed."
        title = str(problem.get("title") or "API request failed")
        detail = str(problem.get("detail") or f"Request to {path} failed.")
        diagnostics = BaseClient.problem_diagnostics(problem.get("errors"), detail)
        suffix = "".join(f"\n  - {diagnostic}" for diagnostic in diagnostics)
        remediation = problem.get("remediation")
        advice = f"\n  {remediation}" if isinstance(remediation, str) and remediation else ""
        return f"{title}: {detail}{suffix}{advice}"

    @staticmethod
    def problem_diagnostics(raw_errors: object, detail: str) -> list[str]:
        """Render safe Problem Details extensions as readable lines, leaving out any that only repeat `detail`."""
        diagnostics: list[str] = []
        if isinstance(raw_errors, list):
            for raw in raw_errors:
                if isinstance(raw, dict) and raw.get("detail") and raw["detail"] != detail:
                    name = str(raw.get("field") or "request")
                    code = str(raw.get("code") or "invalid")
                    diagnostics.append(f"{name} [{code}]: {raw['detail']}")
        return diagnostics

    @staticmethod
    def encode_ref(value: str) -> str:
        """Encode a selector for a query string."""
        return quote(value, safe="")

    @staticmethod
    def check_origin(base_url: str, link: str) -> str:
        """Allow only same-origin navigation links."""
        base = urlsplit(base_url)
        target = urlsplit(link)
        if (target.scheme or base.scheme) != base.scheme:
            raise ApiError("cross-origin link refused")
        if target.netloc and target.netloc != base.netloc:
            raise ApiError("cross-origin link refused")
        path = target.path
        if target.query:
            path = f"{path}?{target.query}"
        return path

    @staticmethod
    def iter_paged(
        fetch: Callable[[str | None], tuple[list[ModelT], str | None]],
    ) -> Iterator[ModelT]:
        """Yield items across pages with loop protection."""
        seen: set[str] = set()
        cursor: str | None = None
        while True:
            items, nxt = fetch(cursor)
            yield from items
            if nxt is None:
                return
            if nxt in seen:
                raise ApiError("repeated pagination cursor")
            seen.add(nxt)
            cursor = nxt
