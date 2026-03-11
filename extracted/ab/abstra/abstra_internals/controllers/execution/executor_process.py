import json
import os
import signal
import threading
import time
import traceback
from dataclasses import dataclass
from enum import Enum
from multiprocessing import Queue
from multiprocessing.connection import Connection
from typing import Optional

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
from abstra_internals.controllers.execution.execution_conn import (
    set_broadcast_publisher,
    set_execution_conn,
)
from abstra_internals.controllers.main import MainController
from abstra_internals.entities.execution import ClientContext
from abstra_internals.entities.execution_context import FormContext, HookContext
from abstra_internals.environment import (
    EDITOR_MODE,
    IS_DEVELOPMENT,
    IS_PRODUCTION,
    WORKER_LOG_TO_QUEUE,
)
from abstra_internals.logger import AbstraLogger
from abstra_internals.repositories.factory import (
    Repositories,
    build_editor_repositories,
    build_prod_repositories,
    build_web_editor_repositories,
)
from abstra_internals.repositories.project.project import StageWithFile
from abstra_internals.settings import Settings
from abstra_internals.stdio_patcher import StdioPatcher
from abstra_internals.utils.rabbitmq_connection import RabbitMQConnection
from abstra_internals.utils.stdio_broadcast import StdioBroadcastPublisher


class ExecutorCommand(str, Enum):
    WARMUP = "warmup"
    EXECUTE = "execute"
    SHUTDOWN = "shutdown"


@dataclass
class WarmupRequest:
    command: ExecutorCommand = ExecutorCommand.WARMUP


@dataclass
class ExecuteRequest:
    command: ExecutorCommand
    worker_id: str
    execution_id: str
    stage: StageWithFile
    request: ClientContext
    connection: Optional[Connection]
    rabbitmq_params: Optional["RabbitMQParams"]
    user_jwt: Optional[str] = None


@dataclass
class ShutdownRequest:
    command: ExecutorCommand = ExecutorCommand.SHUTDOWN


@dataclass
class RabbitMQParams:
    connection_uri: str
    execution_id: str


@dataclass
class ExecutorResponse:
    success: bool
    execution_id: Optional[str] = None
    error: Optional[str] = None
    execution_time: Optional[float] = None


class ExecutorState:
    def __init__(self, verbose: bool = True) -> None:
        self.controller: Optional[MainController] = None
        self.repositories: Optional[Repositories] = None
        self.warmup_complete: bool = False
        self.executions_completed: int = 0
        self.verbose = verbose

    def is_warmed_up(self) -> bool:
        return self.warmup_complete and self.controller is not None


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
            AbstraLogger.init("cloud")
        else:
            AbstraLogger.init("local")

        if IS_PRODUCTION:
            state.repositories = build_prod_repositories()
        elif IS_DEVELOPMENT and EDITOR_MODE == "web":
            from abstra_internals.environment import RABBITMQ_CONNECTION_URI

            if RABBITMQ_CONNECTION_URI is None:
                raise Exception("RABBITMQ_CONNECTION_URI required in web editor mode")
            state.repositories = build_web_editor_repositories(RABBITMQ_CONNECTION_URI)
        else:
            state.repositories = build_editor_repositories(parent_executions_queue)

        state.controller = MainController(state.repositories)

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
    actual_connection = None
    try:
        Settings.set_root_path(root_path)
        Settings.set_server_port(server_port, force=True)

        thread = threading.current_thread()
        thread.name = f"Executor[{request.worker_id}]"

        actual_connection = request.connection
        if request.rabbitmq_params is not None:
            rabbitmq_connection_to_close = RabbitMQConnection(
                connection_uri=request.rabbitmq_params.connection_uri,
                send_queue=f"worker_to_server_{request.rabbitmq_params.execution_id}",
                recv_queue=f"server_to_worker_{request.rabbitmq_params.execution_id}",
                execution_id=request.rabbitmq_params.execution_id,
            )
            actual_connection = rabbitmq_connection_to_close

        if WORKER_LOG_TO_QUEUE and rabbitmq_connection_to_close is not None:
            set_execution_conn(rabbitmq_connection_to_close)

            if request.rabbitmq_params is not None:
                broadcast_publisher = StdioBroadcastPublisher.get_or_create(
                    request.rabbitmq_params.connection_uri
                )
                set_broadcast_publisher(broadcast_publisher)

            AbstraLogger.warning(
                f"[Worker] ABSTRA_WORKER_LOG_TO_QUEUE=true, will send execution logs via RabbitMQ "
                f"(execution_id={rabbitmq_connection_to_close.execution_id})"
            )

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

        def sigterm_handler(signum, frame):
            raise ClientAbandoned()

        signal.signal(signal.SIGTERM, sigterm_handler)

        AbstraLogger.info(
            f"[Executor] Starting execution (execution_id={request.execution_id})"
        )
        execution_controller.run(
            execution_id=request.execution_id, worker_id=request.worker_id
        )

        total_time = time.time() - execution_start
        state.executions_completed += 1

        AbstraLogger.info(
            f"[Executor] Execution completed successfully "
            f"(execution_id={request.execution_id}, time={total_time:.3f}s)"
        )

        response_queue.put(
            ExecutorResponse(
                success=True,
                execution_id=request.execution_id,
                execution_time=total_time,
            )
        )

    except Exception as e:
        AbstraLogger.error(
            f"[Executor] Execution failed (execution_id={request.execution_id}): {e}"
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
        if WORKER_LOG_TO_QUEUE and rabbitmq_connection_to_close is not None:
            ended_msg = {
                "type": "execution:ended",
                "execution_id": request.execution_id,
            }
            try:
                rabbitmq_connection_to_close.send(json.dumps(ended_msg))
            except Exception as e:
                AbstraLogger.error(
                    f"[Executor] Error sending execution:ended via queue: {e}"
                )

        # 3. Clear broadcast publisher
        set_broadcast_publisher(None)

        # 4. Close the connection (RabbitMQ or multiprocessing)
        if rabbitmq_connection_to_close is not None:
            try:
                rabbitmq_connection_to_close.close()
            except Exception as e:
                AbstraLogger.error(f"[Executor] Error closing RabbitMQ connection: {e}")
        elif actual_connection is not None:
            try:
                actual_connection.close()
            except Exception:
                pass


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
