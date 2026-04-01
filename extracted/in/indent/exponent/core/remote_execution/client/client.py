from __future__ import annotations

import asyncio
import json
import logging
import platform
import socket
import time
import uuid
from collections.abc import AsyncGenerator, Callable, Coroutine, Generator
from contextlib import asynccontextmanager
from typing import Any, cast

import msgspec
import websockets.exceptions
from httpx import (
    AsyncClient,
    codes as http_status,
)
from websockets.asyncio import client as asyncio_websockets_client
from websockets.asyncio.client import ClientConnection, connect

from exponent.commands.utils import ConnectionTracker
from exponent.core.config import get_indent_home, is_editable_install
from exponent.core.file_layout import ensure_chat_directories
from exponent.core.remote_execution import files, system_context
from exponent.core.remote_execution.background_tracker import (
    BackgroundProcessTracker,
    TrackedProcess,
)
from exponent.core.remote_execution.blit_terminal_server import (
    BlitTerminalServer,
    get_blit_socket_path,
)
from exponent.core.remote_execution.cli_rpc_types import (
    BackgroundProcessCompletedNotification,
    BashToolInput,
    BatchToolExecutionRequest,
    BatchToolExecutionResponse,
    CliRpcRequest,
    CliRpcResponse,
    DownloadFromUrlRequest,
    ErrorResponse,
    ErrorToolResult,
    GenerateUploadUrlRequest,
    GenerateUploadUrlResponse,
    GetAllFilesRequest,
    GetAllFilesResponse,
    HttpRequest,
    ListTerminalsRequest,
    ListTerminalsResponse,
    StartBlitTerminalRequest,
    StartBlitTerminalResponse,
    StartTerminalRequest,
    StartTerminalResponse,
    StopTerminalRequest,
    StopTerminalResponse,
    SwitchCLIChatRequest,
    SwitchCLIChatResponse,
    TerminalInputRequest,
    TerminalInputResponse,
    TerminalResizeRequest,
    TerminalResizeResponse,
    TerminateRequest,
    TerminateResponse,
    ToolExecutionRequest,
    ToolExecutionResponse,
    ToolResultType,
)
from exponent.core.remote_execution.client.types import (
    REMOTE_EXECUTION_CLIENT_EXIT_INFO,
    SwitchCLIChat,
    WSDisconnected,
    cli_uuid,
)
from exponent.core.remote_execution.code_execution import (
    execute_code_streaming,
)
from exponent.core.remote_execution.file_download import download_file_from_url
from exponent.core.remote_execution.files import file_walk
from exponent.core.remote_execution.http_fetch import fetch_http_content
from exponent.core.remote_execution.session import (
    RemoteExecutionClientSession,
    get_session,
    send_exception_log,
)
from exponent.core.remote_execution.terminal_controller import TerminalControllerServer
from exponent.core.remote_execution.terminal_session import TerminalSessionManager
from exponent.core.remote_execution.terminal_types import TerminalMessage
from exponent.core.remote_execution.tool_execution import (
    BackgroundBashResult,
    execute_bash_tool,
    execute_tool,
    truncate_result,
)
from exponent.core.remote_execution.types import (
    ChatSource,
    CLIConnectedState,
    CreateChatResponse,
    HeartbeatInfo,
    RunWorkflowRequest,
    WorkflowInput,
    WorkflowTriggerRequest,
    WorkflowTriggerResponse,
)
from exponent.core.remote_execution.utils import (
    deserialize_api_response,
)
from exponent.utils.version import get_installed_version

logger = logging.getLogger(__name__)


class RemoteExecutionClient:
    def __init__(
        self,
        session: RemoteExecutionClientSession,
        file_cache: files.FileCache | None = None,
    ):
        self.current_session = session
        self.file_cache = file_cache or files.FileCache(session.working_directory)

        self._halt_states: dict[str, bool] = {}
        self._halt_lock = asyncio.Lock()

        self._last_request_time: float | None = None

        self._pending_upload_requests: dict[str, asyncio.Future[GenerateUploadUrlResponse]] = {}
        self._upload_request_lock = asyncio.Lock()
        self._websocket: ClientConnection | None = None

        self._background_tracker = BackgroundProcessTracker(on_complete=self._on_background_process_complete)
        self._terminal_controller: TerminalControllerServer | None = None
        self._blit_terminal_server: BlitTerminalServer | None = None

        self._executed_idempotency_keys: set[str] = set()

    @property
    def working_directory(self) -> str:
        return self.current_session.working_directory

    @property
    def chat_uuid(self) -> str:
        if self.current_session.chat_uuid is None:
            raise RuntimeError("chat_uuid not set on session")
        return self.current_session.chat_uuid

    @property
    def api_client(self) -> AsyncClient:
        return self.current_session.api_client

    @property
    def ws_client(self) -> AsyncClient:
        return self.current_session.ws_client

    async def add_code_execution_to_halt_states(self, correlation_id: str) -> None:
        async with self._halt_lock:
            self._halt_states[correlation_id] = False

    async def halt_all_code_executions(self) -> None:
        logger.info(f"Halting all code executions: {self._halt_states}")
        async with self._halt_lock:
            self._halt_states = {correlation_id: True for correlation_id in self._halt_states.keys()}

    async def clear_halt_state(self, correlation_id: str) -> None:
        async with self._halt_lock:
            self._halt_states.pop(correlation_id, None)

    def get_halt_check(self, correlation_id: str) -> Callable[[], bool]:
        def should_halt() -> bool:
            return self._halt_states.get(correlation_id, False)

        return should_halt

    async def _on_background_process_complete(
        self,
        tracked: TrackedProcess,
        exit_code: int,
        output: str,
        truncated: bool,
        duration_ms: int,
    ) -> None:
        if self._terminal_controller is not None:
            await self._terminal_controller.handle_bg_process_completed(str(tracked.pid), exit_code)
        notification = BackgroundProcessCompletedNotification(
            pid=tracked.pid,
            command=tracked.command,
            exit_code=exit_code,
            output=output,
            output_file=tracked.output_file,
            correlation_id=tracked.correlation_id,
            truncated=truncated,
            duration_ms=duration_ms,
        )
        await self._send_background_notification(notification)

    async def _send_background_notification(self, notification: BackgroundProcessCompletedNotification) -> None:
        if self._websocket is None:
            logger.warning(
                "Cannot send background process notification: no websocket connection",
                extra={"pid": notification.pid},
            )
            return

        try:
            msg = json.dumps(
                {
                    "type": "background_process_completed",
                    "data": msgspec.to_builtins(notification),
                }
            )
            await self._websocket.send(msg)
            logger.info(
                "Sent background process completion notification",
                extra={
                    "pid": notification.pid,
                    "exit_code": notification.exit_code,
                    "correlation_id": notification.correlation_id,
                },
            )
        except Exception as e:
            logger.exception(
                "Error sending background process notification",
                extra={"pid": notification.pid, "error": str(e)},
            )

    async def _timeout_monitor(self, timeout_seconds: int | None) -> WSDisconnected | None:
        try:
            while True:
                await asyncio.sleep(1)
                if (
                    timeout_seconds is not None
                    and self._last_request_time is not None
                    and time.time() - self._last_request_time > timeout_seconds
                ):
                    logger.info(f"No requests received for {timeout_seconds} seconds. Shutting down...")
                    return WSDisconnected(error_message=f"Timeout after {timeout_seconds} seconds of inactivity")
        except asyncio.CancelledError:
            return None

    async def _handle_websocket_message(  # noqa: PLR0911
        self,
        msg: str,
        websocket: ClientConnection,
        requests: asyncio.Queue[CliRpcRequest],
        terminal_session_manager: TerminalSessionManager,
    ) -> REMOTE_EXECUTION_CLIENT_EXIT_INFO | None:
        self._last_request_time = time.time()

        msg_data = json.loads(msg)
        if msg_data["type"] == "result":
            data = json.dumps(msg_data["data"])
            try:
                response = msgspec.json.decode(data, type=CliRpcResponse)
                if isinstance(response.response, GenerateUploadUrlResponse):
                    async with self._upload_request_lock:
                        if response.request_id in self._pending_upload_requests:
                            future = self._pending_upload_requests.pop(response.request_id)
                            future.set_result(response.response)
            except Exception as e:
                logger.error(f"Error handling upload URL response: {e}")
            return None
        elif msg_data["type"] != "request":
            return None

        data = json.dumps(msg_data["data"])
        try:
            request = msgspec.json.decode(data, type=CliRpcRequest)
        except (msgspec.DecodeError, msgspec.ValidationError) as e:
            request = msgspec.json.decode(data)
            if isinstance(request, dict) and "request_id" in request:
                request_id = request["request_id"]
                if (request.get("request", {}).get("type", {}) == "tool_execution") and (
                    "tool_input" in request["request"] and "tool_name" in request["request"]["tool_input"]
                ):
                    tool_name = request["request"]["tool_input"]["tool_name"]
                    logger.error(
                        f"Error tool {tool_name} received in a request."
                        "Please ensure you are running the latest version of Indent. If this issue persists, please contact support."
                    )
                    await websocket.send(
                        json.dumps(
                            {
                                "type": "result",
                                "data": msgspec.to_builtins(
                                    CliRpcResponse(
                                        request_id=request_id,
                                        response=ErrorResponse(
                                            error_message=f"Unknown tool: {tool_name}. If you are running an older version of Indent, please upgrade to the latest version to ensure compatibility."
                                        ),
                                    )
                                ),
                            }
                        )
                    )
                else:
                    logger.error(
                        "Error decoding cli rpc request. Please ensure you are running the latest version of Indent."
                    )
                    await websocket.send(
                        json.dumps(
                            {
                                "type": "result",
                                "data": msgspec.to_builtins(
                                    CliRpcResponse(
                                        request_id=request_id,
                                        response=ErrorResponse(
                                            error_message=f"Unknown cli rpc request type: {request}",
                                        ),
                                    )
                                ),
                            }
                        )
                    )

                return None
            else:
                raise e

        if isinstance(request.request, TerminateRequest):
            await self.halt_all_code_executions()
            await websocket.send(
                json.dumps(
                    {
                        "type": "result",
                        "data": msgspec.to_builtins(
                            CliRpcResponse(
                                request_id=request.request_id,
                                response=TerminateResponse(),
                            )
                        ),
                    }
                )
            )
            return None
        elif isinstance(request.request, SwitchCLIChatRequest):
            await websocket.send(
                json.dumps(
                    {
                        "type": "result",
                        "data": msgspec.to_builtins(
                            CliRpcResponse(
                                request_id=request.request_id,
                                response=SwitchCLIChatResponse(),
                            )
                        ),
                    }
                )
            )
            return SwitchCLIChat(new_chat_uuid=request.request.new_chat_uuid)
        elif isinstance(request.request, StartBlitTerminalRequest):
            response: StartBlitTerminalResponse
            if self._blit_terminal_server is None:
                response = StartBlitTerminalResponse(
                    success=False,
                    error_message="Blit terminal server is not available",
                )
            else:
                try:
                    pty_id = await self._blit_terminal_server.start_tagged_terminal(
                        rows=request.request.rows,
                        cols=request.request.cols,
                        tag=request.request.tag,
                        command=request.request.command,
                    )
                    response = StartBlitTerminalResponse(success=True, pty_id=pty_id)
                except Exception as e:
                    response = StartBlitTerminalResponse(
                        success=False,
                        error_message=str(e),
                    )
            await websocket.send(
                json.dumps(
                    {
                        "type": "result",
                        "data": msgspec.to_builtins(
                            CliRpcResponse(
                                request_id=request.request_id,
                                response=response,
                            )
                        ),
                    }
                )
            )
            return None
        elif isinstance(request.request, StartTerminalRequest):
            session_id = await terminal_session_manager.start_session(
                websocket=websocket,
                session_id=request.request.session_id,
                command=request.request.command,
                cols=request.request.cols,
                rows=request.request.rows,
                env=request.request.env,
                name=request.request.name,
            )
            await websocket.send(
                json.dumps(
                    {
                        "type": "result",
                        "data": msgspec.to_builtins(
                            CliRpcResponse(
                                request_id=request.request_id,
                                response=StartTerminalResponse(
                                    session_id=session_id,
                                    success=True,
                                    name=request.request.name,
                                ),
                            )
                        ),
                    }
                )
            )
            return None
        elif isinstance(request.request, TerminalInputRequest):
            success = await terminal_session_manager.send_input(
                session_id=request.request.session_id,
                data=request.request.data,
            )
            await websocket.send(
                json.dumps(
                    {
                        "type": "result",
                        "data": msgspec.to_builtins(
                            CliRpcResponse(
                                request_id=request.request_id,
                                response=TerminalInputResponse(
                                    session_id=request.request.session_id,
                                    success=success,
                                ),
                            )
                        ),
                    }
                )
            )
            return None
        elif isinstance(request.request, TerminalResizeRequest):
            success = await terminal_session_manager.resize_terminal(
                session_id=request.request.session_id,
                rows=request.request.rows,
                cols=request.request.cols,
            )
            await websocket.send(
                json.dumps(
                    {
                        "type": "result",
                        "data": msgspec.to_builtins(
                            CliRpcResponse(
                                request_id=request.request_id,
                                response=TerminalResizeResponse(
                                    session_id=request.request.session_id,
                                    success=success,
                                ),
                            )
                        ),
                    }
                )
            )
            return None
        elif isinstance(request.request, StopTerminalRequest):
            success = await terminal_session_manager.stop_session(session_id=request.request.session_id)
            await websocket.send(
                json.dumps(
                    {
                        "type": "result",
                        "data": msgspec.to_builtins(
                            CliRpcResponse(
                                request_id=request.request_id,
                                response=StopTerminalResponse(
                                    session_id=request.request.session_id,
                                    success=success,
                                ),
                            )
                        ),
                    }
                )
            )
            return None
        elif isinstance(request.request, ListTerminalsRequest):
            terminals = await terminal_session_manager.list_sessions()
            await websocket.send(
                json.dumps(
                    {
                        "type": "result",
                        "data": msgspec.to_builtins(
                            CliRpcResponse(
                                request_id=request.request_id,
                                response=ListTerminalsResponse(terminals=terminals),
                            )
                        ),
                    }
                )
            )
            return None
        else:
            if isinstance(request.request, ToolExecutionRequest) and isinstance(
                request.request.tool_input, BashToolInput
            ):
                await self.add_code_execution_to_halt_states(request.request_id)
            elif isinstance(request.request, BatchToolExecutionRequest):
                if any(isinstance(tool_input, BashToolInput) for tool_input in request.request.tool_inputs):
                    await self.add_code_execution_to_halt_states(request.request_id)

            await requests.put(request)
            return None

    async def _setup_tasks(
        self,
        beats: asyncio.Queue[HeartbeatInfo],
        requests: asyncio.Queue[CliRpcRequest],
        results: asyncio.Queue[CliRpcResponse],
    ) -> list[asyncio.Task[None]]:
        async def beat() -> None:
            while True:
                info = await self.get_heartbeat_info()
                await beats.put(info)
                await asyncio.sleep(3)

        requests_lock = asyncio.Lock()
        results_lock = asyncio.Lock()

        async def executor() -> None:
            while True:
                async with requests_lock:
                    request = await requests.get()

                key = request.idempotency_key
                if key is not None and key in self._executed_idempotency_keys:
                    logger.warning(
                        f"Duplicate idempotency key={key} reached CLI, skipping request_id={request.request_id}"
                    )
                    continue
                if key is not None:
                    self._executed_idempotency_keys.add(key)

                try:
                    from exponent.core.remote_execution.cli_rpc_types import (
                        StreamingCodeExecutionRequest,
                    )

                    if isinstance(request.request, StreamingCodeExecutionRequest):
                        async for streaming_response in self.handle_streaming_request(request.request):
                            async with results_lock:
                                await results.put(
                                    CliRpcResponse(
                                        request_id=request.request_id,
                                        response=streaming_response,
                                    )
                                )
                    else:
                        logger.info(f"Handling request {request}")
                        response = await self.handle_request(request)
                        async with results_lock:
                            logger.info(f"Putting response {response}")
                            await results.put(response)
                except Exception as e:
                    logger.info(f"Error handling request {request}:\n\n{e}")
                    try:
                        await send_exception_log(e, session=self.current_session)
                    except Exception:
                        pass
                    async with results_lock:
                        from exponent.core.remote_execution.cli_rpc_types import (
                            StreamingCodeExecutionRequest,
                            StreamingErrorResponse,
                        )

                        if isinstance(request.request, StreamingCodeExecutionRequest):
                            await results.put(
                                CliRpcResponse(
                                    request_id=request.request_id,
                                    response=StreamingErrorResponse(
                                        correlation_id=request.request.correlation_id,
                                        error_message=str(e),
                                    ),
                                )
                            )
                        else:
                            await results.put(
                                CliRpcResponse(
                                    request_id=request.request_id,
                                    response=ErrorResponse(
                                        error_message=str(e),
                                    ),
                                )
                            )

        beat_task = asyncio.create_task(beat())
        executor_tasks = [asyncio.create_task(executor()) for _ in range(10)]

        return [beat_task, *executor_tasks]

    async def _process_websocket_messages(
        self,
        websocket: ClientConnection,
        beats: asyncio.Queue[HeartbeatInfo],
        requests: asyncio.Queue[CliRpcRequest],
        results: asyncio.Queue[CliRpcResponse],
        terminal_output_queue: asyncio.Queue[TerminalMessage],
        terminal_session_manager: TerminalSessionManager,
        terminal_controller: TerminalControllerServer | None = None,
    ) -> REMOTE_EXECUTION_CLIENT_EXIT_INFO:
        pending: set[asyncio.Task[object]] = set()
        try:
            recv = asyncio.create_task(websocket.recv())
            get_beat = asyncio.create_task(beats.get())
            get_result = asyncio.create_task(results.get())
            get_terminal_output = asyncio.create_task(terminal_output_queue.get())
            pending = {recv, get_beat, get_result, get_terminal_output}

            while True:
                done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)

                if recv in done:
                    msg = str(recv.result())
                    exit_info = await self._handle_websocket_message(msg, websocket, requests, terminal_session_manager)
                    if exit_info is not None:
                        return exit_info

                    recv = asyncio.create_task(websocket.recv())
                    pending.add(recv)

                if get_beat in done:
                    info = get_beat.result()
                    data = json.loads(info.model_dump_json())
                    msg = json.dumps({"type": "heartbeat", "data": data})
                    await websocket.send(msg)

                    get_beat = asyncio.create_task(beats.get())
                    pending.add(get_beat)

                if get_result in done:
                    response = get_result.result()
                    data = msgspec.to_builtins(response)
                    msg = json.dumps({"type": "result", "data": data})
                    await websocket.send(msg)

                    get_result = asyncio.create_task(results.get())
                    pending.add(get_result)

                if get_terminal_output in done:
                    terminal_message = get_terminal_output.result()

                    if terminal_controller is not None:
                        await terminal_controller.handle_terminal_message(terminal_message)
                    else:
                        data = msgspec.to_builtins(terminal_message)
                        msg = json.dumps({"type": "terminal_message", "data": data})
                        await websocket.send(msg)

                    get_terminal_output = asyncio.create_task(terminal_output_queue.get())
                    pending.add(get_terminal_output)
        finally:
            for task in pending:
                task.cancel()

            await asyncio.gather(*pending, return_exceptions=True)

    async def _handle_websocket_connection(
        self,
        websocket: ClientConnection,
        connection_tracker: ConnectionTracker | None,
        beats: asyncio.Queue[HeartbeatInfo],
        requests: asyncio.Queue[CliRpcRequest],
        results: asyncio.Queue[CliRpcResponse],
        terminal_output_queue: asyncio.Queue[TerminalMessage],
        terminal_session_manager: TerminalSessionManager,
        terminal_controller: TerminalControllerServer | None = None,
    ) -> REMOTE_EXECUTION_CLIENT_EXIT_INFO | None:
        if connection_tracker is not None:
            await connection_tracker.set_connected(True)

        self._websocket = websocket

        try:
            return await self._process_websocket_messages(
                websocket,
                beats,
                requests,
                results,
                terminal_output_queue,
                terminal_session_manager,
                terminal_controller,
            )
        except asyncio.CancelledError:
            raise
        except websockets.exceptions.ConnectionClosed as e:
            if e.rcvd is not None:
                if e.rcvd.code == 1000:
                    return WSDisconnected()
                elif e.rcvd.code == 1008:
                    error_message = "Error connecting to websocket" if e.rcvd.reason is None else e.rcvd.reason
                    return WSDisconnected(error_message=error_message)
            logger.debug("Websocket connection closed by remote.")
            return None
        except TimeoutError:
            return None
        finally:
            if connection_tracker is not None:
                await connection_tracker.set_connected(False)

    @staticmethod
    def _set_tcp_sockopt_if_available(sock: socket.socket, option_name: str, value: int) -> None:
        option = cast(int | None, getattr(socket, option_name, None))
        if option is None:
            logger.debug("Skipping unsupported TCP socket option: %s", option_name)
            return

        sock.setsockopt(socket.IPPROTO_TCP, option, value)

    @staticmethod
    def _configure_tcp_keepalive(websocket: ClientConnection) -> None:
        # Detect dead TCP connections quickly after E2B sandbox pause/resume by setting
        # aggressive keepalive probes (idle sockets) and TCP_USER_TIMEOUT (all states).
        # See: https://blog.cloudflare.com/when-tcp-sockets-refuse-to-die/
        if platform.system() != "Linux":
            return

        try:
            sock = cast(socket.socket | None, websocket.transport.get_extra_info("socket"))
            if sock is None:
                return

            sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            RemoteExecutionClient._set_tcp_sockopt_if_available(sock, "TCP_KEEPIDLE", 5)
            RemoteExecutionClient._set_tcp_sockopt_if_available(sock, "TCP_KEEPINTVL", 3)
            RemoteExecutionClient._set_tcp_sockopt_if_available(sock, "TCP_KEEPCNT", 3)
            RemoteExecutionClient._set_tcp_sockopt_if_available(sock, "TCP_USER_TIMEOUT", 14_000)
        except OSError:
            logger.debug("Failed to set TCP keepalive options", exc_info=True)

    async def _connect_blit_terminal_server(
        self,
    ) -> BlitTerminalServer | None:
        socket_path = get_blit_socket_path()
        try:
            return await BlitTerminalServer.connect_existing(socket_path)
        except Exception:
            logger.debug("No existing blit socket at %s, spawning server", socket_path)

        blit_terminal_server = BlitTerminalServer(socket_path)
        try:
            await blit_terminal_server.start()
        except Exception:
            logger.warning(
                "Failed to start blit terminal server, falling back to legacy terminal controller",
                extra={"socket_path": socket_path},
                exc_info=True,
            )
            await blit_terminal_server.stop()
            return None

        return blit_terminal_server

    async def run_connection(
        self,
        chat_uuid: str,
        connection_tracker: ConnectionTracker | None = None,
        timeout_seconds: int | None = None,
        terminal_controller_socket_path: str | None = None,
    ) -> REMOTE_EXECUTION_CLIENT_EXIT_INFO:
        self.current_session.set_chat_uuid(chat_uuid)
        ensure_chat_directories(chat_uuid)

        self._last_request_time = time.time()

        beats: asyncio.Queue[HeartbeatInfo] = asyncio.Queue()
        requests: asyncio.Queue[CliRpcRequest] = asyncio.Queue()
        results: asyncio.Queue[CliRpcResponse] = asyncio.Queue()
        terminal_output_queue: asyncio.Queue[TerminalMessage] = asyncio.Queue()

        terminal_session_manager = TerminalSessionManager(terminal_output_queue)

        terminal_controller: TerminalControllerServer | None = None
        blit_terminal_server: BlitTerminalServer | None = None
        self._blit_terminal_server = None
        if terminal_controller_socket_path:

            async def _on_input(session_id: str, data: str) -> None:
                await terminal_session_manager.send_input(session_id, data)

            async def _on_resize(session_id: str, cols: int, rows: int) -> None:
                await terminal_session_manager.resize_terminal(session_id, rows=rows, cols=cols)

            async def _on_start_terminal(session_id: str, cols: int, rows: int) -> None:
                await terminal_session_manager.start_session(
                    websocket=None, session_id=session_id, cols=cols, rows=rows
                )

            terminal_controller = TerminalControllerServer(
                terminal_controller_socket_path,
                on_input=_on_input,
                on_resize=_on_resize,
                on_start_terminal=_on_start_terminal,
            )
            await terminal_controller.start()
            blit_terminal_server = await self._connect_blit_terminal_server()
            self._blit_terminal_server = blit_terminal_server
        self._terminal_controller = terminal_controller

        executors = await self._setup_tasks(beats, requests, results)

        try:
            async for websocket in self.ws_connect(f"/api/ws/chat/{chat_uuid}"):
                self._configure_tcp_keepalive(websocket)
                done, pending = await asyncio.wait(
                    [
                        asyncio.create_task(
                            self._handle_websocket_connection(
                                websocket,
                                connection_tracker,
                                beats,
                                requests,
                                results,
                                terminal_output_queue,
                                terminal_session_manager,
                                terminal_controller,
                            )
                        ),
                        asyncio.create_task(self._timeout_monitor(timeout_seconds)),
                    ],
                    return_when=asyncio.FIRST_COMPLETED,
                )

                for task in pending:
                    task.cancel()

                for task in done:
                    result = await task
                    if result is not None:
                        return result

            return WSDisconnected(error_message="Could not establish websocket connection")
        finally:
            self._blit_terminal_server = None
            if blit_terminal_server is not None:
                await blit_terminal_server.stop()

            if terminal_controller is not None:
                await terminal_controller.stop()

            await terminal_session_manager.stop_all_sessions()

            await self._background_tracker.stop_all()

            for task in executors:
                task.cancel()
            await asyncio.gather(*executors, return_exceptions=True)

    async def create_chat(self, chat_source: ChatSource) -> CreateChatResponse:
        response = await self.api_client.post(
            "/api/remote_execution/create_chat",
            params={"chat_source": chat_source.value},
        )
        return await deserialize_api_response(response, CreateChatResponse)

    async def run_workflow(self, chat_uuid: str, workflow_id: str) -> dict[str, Any]:
        response = await self.api_client.post(
            "/api/remote_execution/run_workflow",
            json=RunWorkflowRequest(
                chat_uuid=chat_uuid,
                workflow_id=workflow_id,
            ).model_dump(),
            timeout=60,
        )
        if response.status_code != http_status.OK:
            raise Exception(
                f"Failed to run workflow with status code {response.status_code} and response {response.text}"
            )
        return cast(dict[str, Any], response.json())

    async def trigger_workflow(self, workflow_name: str, workflow_input: WorkflowInput) -> WorkflowTriggerResponse:
        response = await self.api_client.post(
            "/api/remote_execution/trigger_workflow",
            json=WorkflowTriggerRequest(
                workflow_name=workflow_name,
                workflow_input=workflow_input,
            ).model_dump(),
        )
        return await deserialize_api_response(response, WorkflowTriggerResponse)

    async def get_heartbeat_info(self) -> HeartbeatInfo:
        return HeartbeatInfo(
            system_info=await system_context.get_system_info(self.working_directory),
            exponent_version=get_installed_version(),
            editable_installation=is_editable_install(),
            cli_uuid=str(cli_uuid),
            config_dir=get_indent_home(),
        )

    async def send_heartbeat(self, chat_uuid: str) -> CLIConnectedState:
        logger.info(f"Sending heartbeat for chat_uuid {chat_uuid}")
        heartbeat_info = await self.get_heartbeat_info()
        response = await self.api_client.post(
            f"/api/remote_execution/{chat_uuid}/heartbeat",
            content=heartbeat_info.model_dump_json(),
            timeout=60,
        )
        if response.status_code != http_status.OK:
            raise Exception(f"Heartbeat failed with status code {response.status_code} and response {response.text}")
        connected_state = await deserialize_api_response(response, CLIConnectedState)
        logger.info(f"Heartbeat response: {connected_state}")
        return connected_state

    async def request_upload_url(self, s3_key: str, content_type: str) -> GenerateUploadUrlResponse:
        if self._websocket is None:
            raise RuntimeError("No active websocket connection")

        request_id = str(uuid.uuid4())
        request = CliRpcRequest(
            request_id=request_id,
            request=GenerateUploadUrlRequest(s3_key=s3_key, content_type=content_type),
        )

        future: asyncio.Future[GenerateUploadUrlResponse] = asyncio.Future()
        async with self._upload_request_lock:
            self._pending_upload_requests[request_id] = future

        try:
            await self._websocket.send(json.dumps({"type": "request", "data": msgspec.to_builtins(request)}))

            response = await asyncio.wait_for(future, timeout=30)
            return response
        except TimeoutError:
            async with self._upload_request_lock:
                self._pending_upload_requests.pop(request_id, None)
            raise RuntimeError("Timeout waiting for upload URL response")
        except Exception as e:
            async with self._upload_request_lock:
                self._pending_upload_requests.pop(request_id, None)
            raise e

    async def handle_request(self, request: CliRpcRequest) -> CliRpcResponse:
        self._last_request_time = time.time()

        response: CliRpcResponse | None = None
        try:
            if isinstance(request.request, ToolExecutionRequest):
                if isinstance(request.request.tool_input, BashToolInput):
                    bash_result = await execute_bash_tool(
                        request.request.tool_input,
                        self.working_directory,
                        should_halt=self.get_halt_check(request.request_id),
                        chat_uuid=self.chat_uuid,
                    )
                    if isinstance(bash_result, BackgroundBashResult):
                        self._background_tracker.track(
                            process=bash_result.process,
                            output_file=bash_result.result.output_file or "",
                            command=request.request.tool_input.command,
                            correlation_id=request.request_id,
                        )
                        if self._terminal_controller is not None and bash_result.process.pid is not None:
                            await self._terminal_controller.handle_bg_process_started(
                                str(bash_result.process.pid),
                                request.request.tool_input.command,
                                bash_result.result.output_file or "",
                            )
                        raw_result = bash_result.result
                    else:
                        raw_result = bash_result
                else:
                    raw_result = await execute_tool(request.request.tool_input, self.working_directory, self)
                tool_result = (
                    raw_result if request.request.tool_input.skip_result_truncation() else truncate_result(raw_result)
                )
                response = CliRpcResponse(
                    request_id=request.request_id,
                    response=ToolExecutionResponse(
                        tool_result=tool_result,
                    ),
                )
            elif isinstance(request.request, GetAllFilesRequest):
                files_list = await file_walk(self.working_directory)
                response = CliRpcResponse(
                    request_id=request.request_id,
                    response=GetAllFilesResponse(files=files_list),
                )
            elif isinstance(request.request, BatchToolExecutionRequest):
                coros: list[Coroutine[Any, Any, ToolResultType | BackgroundBashResult]] = []
                tool_inputs = request.request.tool_inputs
                for tool_input in tool_inputs:
                    if isinstance(tool_input, BashToolInput):
                        coros.append(
                            execute_bash_tool(
                                tool_input,
                                self.working_directory,
                                should_halt=self.get_halt_check(request.request_id),
                                chat_uuid=self.chat_uuid,
                            )
                        )
                    else:
                        coros.append(execute_tool(tool_input, self.working_directory, self))

                results_list = await asyncio.gather(*coros, return_exceptions=True)

                processed_results: list[ToolResultType] = []
                for i, result in enumerate(results_list):
                    if isinstance(result, BaseException):
                        processed_results.append(ErrorToolResult(error_message=str(result)))
                    elif isinstance(result, BackgroundBashResult):
                        tool_input = tool_inputs[i]
                        assert isinstance(tool_input, BashToolInput)
                        self._background_tracker.track(
                            process=result.process,
                            output_file=result.result.output_file or "",
                            command=tool_input.command,
                            correlation_id=f"{request.request_id}_{i}",
                        )
                        if self._terminal_controller is not None and result.process.pid is not None:
                            await self._terminal_controller.handle_bg_process_started(
                                str(result.process.pid),
                                tool_input.command,
                                result.result.output_file or "",
                            )
                        processed_results.append(truncate_result(result.result))
                    else:
                        tool_input = tool_inputs[i]
                        processed_results.append(
                            result if tool_input.skip_result_truncation() else truncate_result(result)
                        )

                response = CliRpcResponse(
                    request_id=request.request_id,
                    response=BatchToolExecutionResponse(
                        tool_results=processed_results,
                    ),
                )
            elif isinstance(request.request, HttpRequest):
                http_response = await fetch_http_content(request.request)
                response = CliRpcResponse(
                    request_id=request.request_id,
                    response=http_response,
                )
            elif isinstance(request.request, DownloadFromUrlRequest):
                download_response = await download_file_from_url(request.request)
                response = CliRpcResponse(
                    request_id=request.request_id,
                    response=download_response,
                )
            elif isinstance(request.request, TerminateRequest):
                raise ValueError("TerminateRequest should not be handled by handle_request")

            elif isinstance(request.request, SwitchCLIChatRequest):
                raise ValueError("SwitchCLIChatRequest should not be handled by handle_request")
            elif isinstance(request.request, StartTerminalRequest):
                raise ValueError("StartTerminalRequest should not be handled by handle_request")
            elif isinstance(request.request, TerminalInputRequest):
                raise ValueError("TerminalInputRequest should not be handled by handle_request")
            elif isinstance(request.request, TerminalResizeRequest):
                raise ValueError("TerminalResizeRequest should not be handled by handle_request")
            elif isinstance(request.request, StopTerminalRequest):
                raise ValueError("StopTerminalRequest should not be handled by handle_request")
            elif isinstance(request.request, ListTerminalsRequest):
                raise ValueError("ListTerminalsRequest should not be handled by handle_request")
            else:
                raise ValueError(f"Unhandled request type: {type(request)}")

        except Exception as e:
            logger.error(f"Error handling request {request}:\n\n{e}")
            raise e
        finally:
            if isinstance(request.request, ToolExecutionRequest) and isinstance(
                request.request.tool_input, BashToolInput
            ):
                await self.clear_halt_state(request.request_id)
            elif isinstance(request.request, BatchToolExecutionRequest):
                if any(isinstance(tool_input, BashToolInput) for tool_input in request.request.tool_inputs):
                    await self.clear_halt_state(request.request_id)

        return response

    async def handle_streaming_request(
        self,
        request: Any,
    ) -> AsyncGenerator[Any, None]:
        from exponent.core.remote_execution.cli_rpc_types import (
            StreamingCodeExecutionRequest,
        )

        if not isinstance(request, StreamingCodeExecutionRequest):
            assert False, f"{type(request)} should be sent to handle_streaming_request"
        async for output in execute_code_streaming(
            request,
            working_directory=self.working_directory,
            should_halt=self.get_halt_check(request.correlation_id),
            chat_uuid=self.chat_uuid,
        ):
            yield output

    def ws_connect(self, path: str) -> connect:
        base_url = str(self.ws_client.base_url).replace("http://", "ws://").replace("https://", "wss://")

        url = f"{base_url}{path}"
        headers = {"api-key": self.api_client.headers["api-key"]}

        def custom_backoff() -> Generator[float, None, None]:
            yield 0.1

            delay = 0.5
            while True:
                if delay < 2.0:
                    yield delay
                    delay *= 1.5
                else:
                    yield 2.0

        asyncio_websockets_client.backoff = custom_backoff  # ty: ignore[invalid-assignment]

        conn = connect(url, additional_headers=headers, open_timeout=10, ping_timeout=10)

        return conn

    @staticmethod
    @asynccontextmanager
    async def session(
        api_key: str,
        base_url: str,
        base_ws_url: str,
        working_directory: str,
        file_cache: files.FileCache | None = None,
    ) -> AsyncGenerator[RemoteExecutionClient, None]:
        async with get_session(working_directory, base_url, base_ws_url, api_key) as session:
            yield RemoteExecutionClient(session, file_cache)
