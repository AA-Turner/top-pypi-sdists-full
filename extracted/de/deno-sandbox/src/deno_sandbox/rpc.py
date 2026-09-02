from __future__ import annotations

import asyncio
import base64
import json
from typing import Any, Dict, Literal, Mapping, Optional, TypedDict, cast
from typing_extensions import NotRequired
from websockets import ConnectionClosed

from .errors import (
    HTTPStatusError,
    ProcessAlreadyExited,
    RpcValidationError,
    UnknownRpcMethod,
    ZodErrorRaw,
)
from .transport import WebSocketTransport
from .utils import (
    convert_to_camel_case,
    convert_to_snake_case,
    to_snake_case,
)


class RpcRequest(TypedDict):
    id: int
    method: str
    params: dict[str, Any]
    jsonrpc: str


class RpcResult(TypedDict):
    ok: NotRequired[Any]
    error: NotRequired[Any]


class RpcResponse(TypedDict):
    id: int
    jsonrpc: str
    result: NotRequired[RpcResult | None]
    error: NotRequired[dict[str, Any] | None]


class AsyncRpcClient:
    def __init__(self, transport: WebSocketTransport):
        self._transport = transport
        self._id = 0
        self._pending_requests: Dict[int, asyncio.Future[Any]] = {}
        self._listen_task: asyncio.Task[Any] | None = None
        self._pending_processes: Dict[int, asyncio.StreamReader] = {}
        self.__loop: asyncio.AbstractEventLoop | None = None
        self._signal_id = 0
        self._stream_id = 0
        self._debug = transport._debug

    @property
    def _loop(self) -> asyncio.AbstractEventLoop:
        if self.__loop is None:
            self.__loop = asyncio.get_running_loop()
        return self.__loop

    async def close(self):
        await self._transport.close()

    async def send_notification(self, method: str, params: dict[str, Any]) -> None:
        """Send a notification (no response expected)."""
        payload = {"method": method, "params": params, "jsonrpc": "2.0"}
        await self._transport.send(json.dumps(payload))

    def next_stream_id(self) -> int:
        """Get next stream ID."""
        self._stream_id += 1
        return self._stream_id

    async def call(self, method: str, params: Mapping[str, Any]) -> Any:
        if self._listen_task is None or self._listen_task.done():
            self._listen_task = self._loop.create_task(self._listener())

        req_id = self._id + 1
        self._id = req_id

        camel_params = convert_to_camel_case(params)
        payload = RpcRequest(
            method=method, params=camel_params, id=req_id, jsonrpc="2.0"
        )

        future = self._loop.create_future()
        self._pending_requests[req_id] = future

        await self._transport.send(json.dumps(payload))

        raw_response = await future
        response = cast(RpcResponse, raw_response)

        maybeError = response.get("error")
        if maybeError is not None:
            if maybeError.get("message") == "Method not found":
                raise UnknownRpcMethod("RPC method not found")

            if maybeError.get("data") is not None:
                data = maybeError["data"]
                if data.get("constructor_name") == "ZodError":
                    # For some reason ZodError data is serialized as
                    # json inside json ¯\_(ツ)_/¯
                    zod_errors: list[ZodErrorRaw] = []
                    for e in json.loads(data["message"]):
                        value = cast(ZodErrorRaw, e)

                        value["path"] = [to_snake_case(p) for p in value["path"]]
                        zod_errors.append(value)

                    raise RpcValidationError(zod_errors)

            raise Exception(maybeError)

        maybeResult = response.get("result")
        if maybeResult is not None:
            err = maybeResult.get("error")
            if err is not None:
                if (
                    "constructor_name" in err
                    and err.get("constructor_name") == "TypeError"
                    and "code" in err
                    and err.get("code") == "ENOENT"
                ):
                    raise ProcessAlreadyExited("Process has already exited")

                raise Exception(f"Application Error: {err}")

        return maybeResult["ok"] if maybeResult else None

    async def _listener(self) -> None:
        try:
            async for raw in self._transport:
                data = json.loads(raw)
                req_id = data.get("id")

                if req_id is not None and req_id in self._pending_requests:
                    future = self._pending_requests.pop(req_id)
                    if not future.done():
                        converted_data = convert_to_snake_case(data)
                        future.set_result(converted_data)

                elif "method" in data:
                    method = data["method"]
                    params = data.get("params", {})

                    if method == "$sandbox.stream.enqueue":
                        stream_id = params.get("streamId")
                        chunk = base64.b64decode(params.get("data", ""))
                        stream = self._pending_processes.get(stream_id)
                        if stream:
                            stream.feed_data(chunk)
                    elif method == "$sandbox.stream.end":
                        stream_id = params.get("streamId")
                        stream = self._pending_processes.get(stream_id)
                        if stream:
                            stream.feed_eof()
                            del self._pending_processes[stream_id]

        except ConnectionClosed:
            # Cancel all pending requests when connection closes
            for future in self._pending_requests.values():
                if not future.done():
                    future.cancel()
            self._pending_requests.clear()
        except Exception as e:
            for future in self._pending_requests.values():
                if not future.done():
                    future.set_exception(e)

    async def fetch(
        self,
        url: str,
        method: Optional[str] = "GET",
        headers: Optional[dict[str, str]] = None,
        redirect: Optional[Literal["follow", "manual"]] = None,
        pid: Optional[int] = None,
    ) -> AsyncFetchResponse:
        self._signal_id += 1
        signal_id = self._signal_id

        params: FetchParams = {
            "url": url,
            "method": method or "GET",
            "headers": list(headers.items()) if headers else [],
            "redirect": redirect or "follow",
            "abortId": signal_id,
        }

        if pid is not None:
            params["pid"] = pid

        response_data = await self.call("fetch", params)
        response = cast(FetchResponseData, response_data)

        fetch_response = AsyncFetchResponse(self, response)
        return fetch_response


class FetchParams(TypedDict):
    method: str
    url: str
    headers: list[tuple[str, str]]
    redirect: str
    pid: NotRequired[int | None]
    abortId: int


class FetchResponseData(TypedDict):
    status: int
    status_text: str
    headers: list[tuple[str, str]]
    body_stream_id: int


class AsyncFetchResponse:
    def __init__(self, rpc: AsyncRpcClient, response: FetchResponseData):
        self._rpc = rpc
        self._response = response

    def raise_for_status(self) -> HTTPStatusError | None:
        if self.is_success:
            return

        message = "{self} resulted in a {error_type} (status code: {self.status_code})"
        status_class = self.status_code // 100
        error_types = {
            1: "Informational response",
            3: "Redirect response",
            4: "Client error",
            5: "Server error",
        }
        error_type = error_types.get(status_class, "Invalid status code")
        message = message.format(self, error_type=error_type)

        return HTTPStatusError(self.status_code, message)

    @property
    def headers(self) -> list[tuple[str, str]]:
        return self._response["headers"]

    @property
    def status_code(self) -> int:
        return self._response["status"]

    @property
    def is_informational(self) -> int:
        return 100 <= self.status_code <= 199

    @property
    def is_success(self) -> int:
        return 200 <= self.status_code <= 299

    @property
    def is_redirect(self) -> int:
        return 300 <= self.status_code <= 399

    @property
    def is_client_error(self) -> int:
        return 400 <= self.status_code <= 499

    @property
    def is_server_error(self) -> int:
        return 500 <= self.status_code <= 599

    @property
    def is_error(self) -> int:
        return 400 <= self.status_code <= 599

    @property
    def has_redirect_location(self) -> bool:
        return (
            self.status_code in (301, 302, 303, 307, 308)
            and "location" in self._response["headers"]
        )

    def __repr__(self) -> str:
        return f"<Response [{self.status_code}]>"


class FetchResponse(AsyncFetchResponse):
    def __init__(self, async_res: AsyncFetchResponse):
        self._async = async_res

    def raise_for_status(self) -> HTTPStatusError | None:
        return self._async.raise_for_status()

    @property
    def headers(self) -> list[tuple[str, str]]:
        return self._async.headers

    @property
    def status_code(self) -> int:
        return self._async.status_code

    @property
    def is_informational(self) -> int:
        return self._async.is_informational

    @property
    def is_success(self) -> int:
        return self._async.is_success

    @property
    def is_redirect(self) -> int:
        return self._async.is_redirect

    @property
    def is_client_error(self) -> int:
        return self._async.is_client_error

    @property
    def is_server_error(self) -> int:
        return self._async.is_server_error

    @property
    def is_error(self) -> int:
        return self._async.is_error

    @property
    def has_redirect_location(self) -> bool:
        return self._async.has_redirect_location

    def __repr__(self) -> str:
        return f"<Response [{self.status_code}]>"
