import json
import os
import re
import signal
import threading
import time
import traceback
from multiprocessing import Queue
from typing import Dict, List, Optional, Tuple
from uuid import uuid4

from dotenv import load_dotenv

from abstra_internals.agents import lifecycle
from abstra_internals.consts.filepaths import SMARTCHAT_SNIPPETS_DIR_PATH
from abstra_internals.controllers.execution.connection_protocol import (
    ConnectionProtocol,
)
from abstra_internals.controllers.execution.execution import ExecutionController
from abstra_internals.controllers.execution.execution_client import (
    ClientAbandoned,
    ExecutionClient,
    HeadlessClient,
)
from abstra_internals.controllers.execution.execution_client_form import FormClient
from abstra_internals.controllers.execution.execution_client_hook import HookClient
from abstra_internals.controllers.execution.execution_client_page import PageClient
from abstra_internals.controllers.execution.execution_conn import (
    set_broadcast_publisher,
    set_execution_conn,
)
from abstra_internals.controllers.execution.executor_types import (
    ExecuteRequest,
    ExecutorResponse,
    RunSnippetRequest,
    ShutdownRequest,
    WarmupRequest,
)
from abstra_internals.controllers.main import MainController
from abstra_internals.entities.execution import ClientContext
from abstra_internals.entities.execution_context import (
    FormContext,
    HookContext,
    PageContext,
)
from abstra_internals.environment import (
    EDITOR_MODE,
    IS_DEVELOPMENT,
    IS_PRODUCTION,
    NATS_CREDS,
    NATS_URL,
    WORKER_LOG_TO_QUEUE,
    web_editor_uses_db,
)
from abstra_internals.logger import AbstraLogger
from abstra_internals.repositories.factory import (
    Repositories,
    build_editor_repositories,
    build_prod_repositories,
    build_web_editor_repositories,
)
from abstra_internals.settings import Settings
from abstra_internals.stdio_patcher import StdioPatcher
from abstra_internals.utils.nats_connection import (
    NATSConnection,
    NATSPersistentConnection,
)
from abstra_internals.utils.rabbitmq_connection import RabbitMQConnection
from abstra_internals.utils.stdio_broadcast import StdioBroadcastPublisher

# ---------------------------------------------------------------------------
# Initialize logging once at module-load time so the forkserver pays this
# cost during preload (shared across all forked children) instead of each
# executor subprocess paying it individually inside handle_warmup.
#
# Sentry SDK registers os.register_at_fork callbacks that reinitialize the
# background transport thread in child processes after fork, so event
# reporting works correctly in every executor child.
# ---------------------------------------------------------------------------
if IS_PRODUCTION:
    AbstraLogger.init("cloud")
else:
    AbstraLogger.init("local")

_SESSION_QUEUE_RE = re.compile(
    r"^session_(s2w|w2s)_([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})$"
)


def _validate_session_queues(
    send_queue: str, recv_queue: str, execution_id: str
) -> None:
    for name in (send_queue, recv_queue):
        m = _SESSION_QUEUE_RE.match(name)
        if not m:
            raise ValueError(f"Invalid session queue name: {name}")
        if m.group(2) != execution_id:
            raise ValueError(
                f"Queue executionId mismatch: {m.group(2)} != {execution_id}"
            )
    # Validate directions: send_queue must be s2w (server-to-worker) and
    # recv_queue must be w2s (worker-to-server) from cloud-api's perspective.
    # The worker inverts these in handle_execute.
    send_m = _SESSION_QUEUE_RE.match(send_queue)
    recv_m = _SESSION_QUEUE_RE.match(recv_queue)
    if send_m and recv_m:
        if send_m.group(1) == recv_m.group(1):
            raise ValueError(
                f"Queue direction mismatch: both queues have direction '{send_m.group(1)}'"
            )


class ExecutorState:
    def __init__(self, verbose: bool = True) -> None:
        self.controller: Optional[MainController] = None
        self.repositories: Optional[Repositories] = None
        self.warmup_complete: bool = False
        self.executions_completed: int = 0
        self.verbose = verbose
        self.nats_persistent: Optional[NATSPersistentConnection] = None
        self.env_file_signature: Optional[Tuple[float, int]] = None

    def is_warmed_up(self) -> bool:
        return self.warmup_complete and self.controller is not None


def _reload_project_env_vars(state: ExecutorState) -> None:
    # Web-editor UI and worker run in separate pods sharing the project via EFS;
    # reload the .env when it changes so user code sees the latest values. Gated
    # to dev so a project .env can never override pod-injected vars in prod. The
    # (mtime, size) signature avoids a full EFS read on every execution.
    if not (IS_DEVELOPMENT and EDITOR_MODE == "web"):
        return
    env_path = Settings.root_path / ".env"
    try:
        stat = env_path.stat()
    except FileNotFoundError:
        state.env_file_signature = None
        return
    signature = (stat.st_mtime, stat.st_size)
    if signature == state.env_file_signature:
        return
    load_dotenv(env_path, override=True)
    state.env_file_signature = signature


def make_client_from_context(
    ctx: ClientContext, connection: ConnectionProtocol
) -> ExecutionClient:
    if isinstance(ctx, FormContext):
        return FormClient(
            context=ctx,
            conn=connection,
            production_mode=IS_PRODUCTION,
        )
    elif isinstance(ctx, HookContext):
        return HookClient(
            context=ctx,
            conn=connection,
            production_mode=IS_PRODUCTION,
        )
    elif isinstance(ctx, PageContext):
        return PageClient(
            context=ctx,
            conn=connection,
            production_mode=IS_PRODUCTION,
        )
    else:
        return HeadlessClient(
            context=ctx, conn=connection, production_mode=IS_PRODUCTION
        )


def handle_warmup(
    state: ExecutorState,
    response_queue: Queue,
    root_path: str,
    server_port: int,
    parent_executions_queue: Optional[Queue] = None,
) -> None:
    try:
        warmup_start = time.time()

        Settings.set_root_path(root_path)
        Settings.set_server_port(server_port, force=True)

        if IS_PRODUCTION:
            state.repositories = build_prod_repositories()
        elif IS_DEVELOPMENT and EDITOR_MODE == "web":
            from abstra_internals.environment import RABBITMQ_CONNECTION_URI

            if RABBITMQ_CONNECTION_URI is None:
                raise Exception("RABBITMQ_CONNECTION_URI required in web editor mode")
            if web_editor_uses_db():
                # An executor is serial: ~2 conns (final-flush + log-flush daemon).
                # Explicit here, not just inherited from the forkserver parent.
                from abstra_internals.services.db.connection import configure_pool

                configure_pool(max_size=2)
            state.repositories = build_web_editor_repositories(RABBITMQ_CONNECTION_URI)
        else:
            state.repositories = build_editor_repositories(parent_executions_queue)

        state.controller = MainController(state.repositories)

        if NATS_URL and NATS_CREDS:
            try:
                state.nats_persistent = NATSPersistentConnection(
                    nats_url=NATS_URL,
                    nats_creds=NATS_CREDS,
                )
            except Exception as e:
                AbstraLogger.error(
                    f"[Executor] NATS warmup failed (will retry on first execution): {e}"
                )

        state.warmup_complete = True

        warmup_time = time.time() - warmup_start

        if state.verbose:
            AbstraLogger.warning(
                f"[Executor] Warmup completed in {warmup_time:.3f}s (pid={os.getpid()})"
            )

        response_queue.put(ExecutorResponse(success=True, execution_time=warmup_time))

    except Exception as e:
        AbstraLogger.error(f"[Executor] Warmup failed: {e}")
        AbstraLogger.capture_exception(e)
        response_queue.put(ExecutorResponse(success=False, error=str(e)))


def _close_leaked_agent_tools(execution_id: Optional[str] = None) -> None:
    leaked = lifecycle.close_leaked_tools()
    if leaked:
        suffix = f" after execution {execution_id}" if execution_id else ""
        AbstraLogger.warning(
            f"[Executor] Closed {leaked} leaked agent tool(s){suffix}. "
            "Close BrowserTools (or use it as a context manager) when done."
        )


def handle_execute(
    state: ExecutorState,
    request: ExecuteRequest,
    response_queue: Queue,
    root_path: str,
    server_port: int,
) -> None:
    execution_start = time.time()

    if not state.is_warmed_up():
        error_msg = "Executor not warmed up"
        AbstraLogger.error(f"[Executor] {error_msg}")
        response_queue.put(
            ExecutorResponse(
                success=False,
                execution_id=request.execution_id,
                error=error_msg,
            )
        )
        return

    rabbitmq_connection_to_close = None
    nats_connection_to_close = None
    actual_connection = None
    try:
        Settings.set_root_path(root_path)
        Settings.set_server_port(server_port, force=True)
        _reload_project_env_vars(state)

        thread = threading.current_thread()
        thread.name = f"Executor[{request.worker_id}]"

        actual_connection = request.connection

        # Use NATS for non-form executions. Forms use RabbitMQ session queues (WebSocket path).
        is_form = request.stage.type_name == "form"
        if (
            NATS_URL
            and NATS_CREDS
            and request.rabbitmq_params is not None
            and not is_form
        ):
            execution_id = request.rabbitmq_params.execution_id
            if state.nats_persistent is None or not state.nats_persistent.is_alive:
                state.nats_persistent = NATSPersistentConnection(
                    nats_url=NATS_URL,
                    nats_creds=NATS_CREDS,
                )

            nats_connection_to_close = NATSConnection(
                nats_url=NATS_URL,
                nats_creds=NATS_CREDS,
                send_subject=f"{execution_id}.w2s",
                recv_subject=f"{execution_id}.s2w",
                execution_id=execution_id,
                persistent=state.nats_persistent,
            )
            actual_connection = nats_connection_to_close

        # RabbitMQ fallback
        elif request.rabbitmq_params is not None:
            params = request.rabbitmq_params
            # Session queues: cloud-api's send = worker's recv, and vice versa
            if params.recv_queue and params.send_queue:
                _validate_session_queues(
                    params.send_queue, params.recv_queue, params.execution_id
                )
                if params.queue_expire_ms is not None:
                    if params.queue_expire_ms < 60_000:
                        AbstraLogger.warning(
                            f"[Executor] queue_expire_ms unusually low ({params.queue_expire_ms}ms), "
                            f"keeping cloud-api value to avoid PRECONDITION_FAILED"
                        )
                worker_send_queue = params.recv_queue
                worker_recv_queue = params.send_queue
                is_session = True
            elif params.recv_queue or params.send_queue:
                AbstraLogger.error(
                    f"[Executor] Received partial session fields "
                    f"(send_queue={params.send_queue}, recv_queue={params.recv_queue}). "
                    f"Falling back to legacy mode. This is likely a bug in cloud-api."
                )
                worker_send_queue = f"worker_to_server_{params.execution_id}"
                worker_recv_queue = f"server_to_worker_{params.execution_id}"
                is_session = False
            else:
                worker_send_queue = f"worker_to_server_{params.execution_id}"
                worker_recv_queue = f"server_to_worker_{params.execution_id}"
                is_session = False
            rabbitmq_connection_to_close = RabbitMQConnection(
                connection_uri=params.connection_uri,
                send_queue=worker_send_queue,
                recv_queue=worker_recv_queue,
                execution_id=params.execution_id,
                is_session=is_session,
                queue_expire_ms=params.queue_expire_ms,
            )
            actual_connection = rabbitmq_connection_to_close

        if (
            WORKER_LOG_TO_QUEUE
            and not web_editor_uses_db()
            and actual_connection is not None
        ):
            set_execution_conn(actual_connection)

            if request.rabbitmq_params is not None:
                broadcast_publisher = StdioBroadcastPublisher.get_or_create(
                    request.rabbitmq_params.connection_uri
                )
                set_broadcast_publisher(broadcast_publisher)

        if actual_connection is None:
            raise Exception("No connection available")

        if state.controller is None:
            raise Exception("Controller not initialized")

        StdioPatcher.apply(state.controller)

        execution_controller = ExecutionController(
            repositories=state.controller.repositories,
            stage=request.stage,
            client=make_client_from_context(request.request, actual_connection),
            context=request.request,
            user_jwt=request.user_jwt,
        )

        def sigterm_handler(_signum, _frame):
            del _signum, _frame
            raise ClientAbandoned()

        signal.signal(signal.SIGTERM, sigterm_handler)

        execution_controller.run(
            execution_id=request.execution_id, worker_id=request.worker_id
        )

        total_time = time.time() - execution_start
        state.executions_completed += 1

        AbstraLogger.lifecycle(
            f"[RUN {request.execution_id}] User code finished",
            {
                "executionId": request.execution_id,
                "jobId": request.stage.id,
                "status": "finished",
                "durationMs": int(total_time * 1000),
                "stage": "runtime.user_code.finished",
            },
        )

        response_queue.put(
            ExecutorResponse(
                success=True,
                execution_id=request.execution_id,
                execution_time=total_time,
            )
        )

    except Exception as e:
        total_time = time.time() - execution_start
        AbstraLogger.error(
            f"[RUN {request.execution_id}] User code failed",
            {
                "executionId": request.execution_id,
                "jobId": request.stage.id,
                "status": "failed",
                "durationMs": int(total_time * 1000),
                "errorType": type(e).__name__,
                "errorMessage": str(e),
                "stage": "runtime.user_code.failed",
            },
        )
        AbstraLogger.capture_exception(e)
        traceback.print_exc()

        response_queue.put(
            ExecutorResponse(
                success=False,
                execution_id=request.execution_id,
                error=str(e),
            )
        )
    finally:
        # 1. Flush remaining buffered logs and clear the buffer
        set_execution_conn(None)

        # 2. Send execution:ended signal so the server knows to close the queue
        if (
            WORKER_LOG_TO_QUEUE
            and not web_editor_uses_db()
            and actual_connection is not None
        ):
            ended_msg = {
                "type": "execution:ended",
                "execution_id": request.execution_id,
            }
            try:
                actual_connection.send(json.dumps(ended_msg))
            except Exception as e:
                AbstraLogger.error(
                    f"[Executor] Error sending execution:ended via queue: {e}"
                )

        # 3. Clear broadcast publisher
        set_broadcast_publisher(None)

        # 3.5. Close agent tools (browsers etc.) leaked by user code. Warm
        #      executors are reused across executions: a leaked playwright
        #      driver keeps an asyncio loop marked as running on this thread
        #      and stacks Chromium/driver processes on every reuse. Runs after
        #      the log flush and execution:ended — playwright's close has no
        #      client-side timeout, so a wedged Chromium must not be able to
        #      hold the delivery lifecycle hostage.
        _close_leaked_agent_tools(request.execution_id)

        # 4. Close the connection (NATS, RabbitMQ, or multiprocessing)
        if nats_connection_to_close is not None:
            try:
                nats_connection_to_close.close()
            except Exception as e:
                AbstraLogger.error(f"[Executor] Error closing NATS connection: {e}")
        elif rabbitmq_connection_to_close is not None:
            try:
                rabbitmq_connection_to_close.close()
            except Exception as e:
                AbstraLogger.error(f"[Executor] Error closing RabbitMQ connection: {e}")
        elif actual_connection is not None:
            try:
                actual_connection.close()
            except Exception:
                pass


def _collect_execution_logs(
    state: ExecutorState, execution_id: str
) -> List[Dict[str, str]]:
    """Fetch logs from the execution logs repository after snippet execution."""
    if state.controller is None:
        return []
    try:
        log_entries = state.controller.execution_logs_repository.get(execution_id)
        return [
            {"type": entry.event, "text": entry.payload.get("text", "")}
            for entry in log_entries
        ]
    except Exception:
        return []


def handle_run_snippet(
    state: ExecutorState,
    request: RunSnippetRequest,
    response_queue: Queue,
    root_path: str,
    server_port: int,
) -> None:
    execution_start = time.time()

    if not state.is_warmed_up():
        error_msg = "Executor not warmed up"
        AbstraLogger.error(f"[Executor] {error_msg}")
        response_queue.put(ExecutorResponse(success=False, error=error_msg))
        return

    Settings.set_root_path(root_path)
    Settings.set_server_port(server_port, force=True)
    _reload_project_env_vars(state)

    snippet_dir = Settings.root_path / SMARTCHAT_SNIPPETS_DIR_PATH
    snippet_dir.mkdir(parents=True, exist_ok=True)
    snippet_file = snippet_dir / f"{uuid4()}.py"

    try:
        snippet_file.write_text(request.code, encoding="utf-8")

        if state.controller is None:
            raise Exception("Controller not initialized")

        StdioPatcher.apply(state.controller)

        result = ExecutionController.run_snippet(
            file_path=snippet_file,
            worker_id=request.worker_id,
            repositories=state.controller.repositories,
        )

        execution_id = result.get("execution_id")
        logs = _collect_execution_logs(state, execution_id) if execution_id else []

        total_time = time.time() - execution_start
        state.executions_completed += 1

        response_queue.put(
            ExecutorResponse(
                success=result["ok"],
                error=result.get("error"),
                execution_time=total_time,
                logs=logs,
            )
        )

    except Exception as e:
        AbstraLogger.error(f"[Executor] Snippet execution failed: {e}")
        AbstraLogger.capture_exception(e)
        response_queue.put(ExecutorResponse(success=False, error=str(e)))
    finally:
        _close_leaked_agent_tools()
        if snippet_file.exists():
            snippet_file.unlink()


def executor_main(
    work_queue: Queue,
    response_queue: Queue,
    root_path: str,
    server_port: int,
    parent_executions_queue: Optional[Queue] = None,
    verbose: bool = True,
) -> None:
    state = ExecutorState(verbose=verbose)

    try:
        while True:
            command_data = work_queue.get()

            if isinstance(command_data, WarmupRequest):
                handle_warmup(
                    state,
                    response_queue,
                    root_path,
                    server_port,
                    parent_executions_queue,
                )

            elif isinstance(command_data, ExecuteRequest):
                handle_execute(
                    state,
                    command_data,
                    response_queue,
                    root_path,
                    server_port,
                )

            elif isinstance(command_data, RunSnippetRequest):
                handle_run_snippet(
                    state,
                    command_data,
                    response_queue,
                    root_path,
                    server_port,
                )

            elif isinstance(command_data, ShutdownRequest):
                AbstraLogger.warning("[Executor] Received shutdown command")
                break

            else:
                AbstraLogger.error(
                    f"[Executor] Unknown command type: {type(command_data)}"
                )

    except KeyboardInterrupt:
        if state.verbose:
            AbstraLogger.warning("[Executor] Interrupted by keyboard")
    except ClientAbandoned:
        AbstraLogger.debug("[Executor] Client abandoned during executor recycling")
    except Exception as e:
        AbstraLogger.error(f"[Executor] Fatal error in executor loop: {e}")
        AbstraLogger.capture_exception(e)
    finally:
        if state.verbose:
            AbstraLogger.warning(
                f"[Executor] Shutting down (executions_completed={state.executions_completed})"
            )
