import json
import os
import time
from concurrent.futures import ThreadPoolExecutor
from multiprocessing.process import BaseProcess
from threading import Thread
from typing import Dict, Optional, Union, cast
from uuid import uuid4

from abstra_internals.cloud.metrics_reporter import (
    MetricsReporter,
    create_metrics_reporter,
)
from abstra_internals.controllers.execution.debug_monitor import DebugMonitor
from abstra_internals.controllers.execution.executor_config import ExecutorConfig
from abstra_internals.controllers.execution.executor_pool import (
    ExecutorDiedError,
    ExecutorPool,
    ExecutorPoolNotReadyError,
)
from abstra_internals.controllers.execution.executor_types import RabbitMQParams
from abstra_internals.controllers.main import MainController
from abstra_internals.environment import (
    ABSTRA_EXECUTOR_POOL_SIZE,
    EDITOR_MODE,
    IS_PRODUCTION,
    RABBITMQ_CONNECTION_URI,
)
from abstra_internals.logger import AbstraLogger
from abstra_internals.repositories.consumer import (
    Consumer,
    ControlQueueMessage,
    QueueMessage,
)
from abstra_internals.repositories.models import (
    RunSnippetMessage,
    RunSnippetSandboxedMessage,
    StopAllExecutionsMessage,
    StopExecutionMessage,
)
from abstra_internals.repositories.producer import (
    LocalProducerRepository,
)
from abstra_internals.repositories.project.project import StageWithFile
from abstra_internals.settings import Settings
from abstra_internals.utils.rabbitmq_connection import RabbitMQConnection


class StageNotFound(Exception):
    pass


class NonCleanExit(Exception):
    pass


class ConsumerController:
    def __init__(
        self,
        main_controller: MainController,
        consumer: Consumer,
        control_consumer: Optional[Consumer] = None,
        debug_mode: bool = False,
    ):
        self.main_controller = main_controller
        self.consumer = consumer
        self.control_consumer = control_consumer
        self.worker_id = str(uuid4())
        self.concurrency = ABSTRA_EXECUTOR_POOL_SIZE
        self.executor: Optional[ThreadPoolExecutor] = None
        self.metrics_reporter: Optional["MetricsReporter"] = None
        self.debug_monitor: Optional["DebugMonitor"] = None
        self.debug_mode = debug_mode

        self.active_processes: Dict[int, BaseProcess] = {}

        config = ExecutorConfig.from_environment()
        config.validate()

        local_queue = None
        if isinstance(main_controller.repositories.producer, LocalProducerRepository):
            local_queue = main_controller.repositories.producer.queue

        verbose = debug_mode or IS_PRODUCTION is True or EDITOR_MODE == "web"

        self.executor_pool = ExecutorPool(
            config=config,
            mp_context=main_controller.repositories.mp_context.get_context(),
            root_path=str(Settings.root_path),
            server_port=Settings.server_port,
            worker_id=self.worker_id,
            parent_executions_queue=local_queue,
            verbose=verbose,
        )

        try:
            self.metrics_reporter = create_metrics_reporter(self.executor_pool)
        except ImportError:
            pass

        if debug_mode:
            self.debug_monitor = DebugMonitor(self.executor_pool)

    def _control_loop(self):
        if not self.control_consumer:
            return

        AbstraLogger.info("[ConsumerController] Starting control loop")
        for msg in self.control_consumer.iter():
            try:
                if isinstance(msg, ControlQueueMessage):
                    control_msg = msg.message
                    if isinstance(control_msg, StopExecutionMessage):
                        if control_msg.payload.execution_id:
                            AbstraLogger.info(
                                f"[ConsumerController] Received stop request for execution {control_msg.payload.execution_id}"
                            )
                            self.executor_pool.kill_execution(
                                control_msg.payload.execution_id
                            )
                    elif isinstance(control_msg, StopAllExecutionsMessage):
                        with self.executor_pool.lock:
                            active_ids = list[str](
                                self.executor_pool.execution_to_executor.keys()
                            )
                        AbstraLogger.info(
                            f"[ConsumerController] Received stop_all request, killing {len(active_ids)} active execution(s)"
                        )
                        for execution_id in active_ids:
                            self.executor_pool.force_kill_execution(execution_id)
                    elif control_msg.type == "ping":
                        AbstraLogger.debug(
                            "[ConsumerController] Received ping message for worker warmup"
                        )
                    elif control_msg.type == "restart":
                        AbstraLogger.warning(
                            "[ConsumerController] Received restart request, restarting worker"
                        )
                        self.control_consumer.threadsafe_ack(msg)
                        os._exit(0)

                    self.control_consumer.threadsafe_ack(msg)
                else:
                    AbstraLogger.warning(
                        f"[ConsumerController] Received unknown message type in control loop: {type(msg)}"
                    )
                    self.control_consumer.threadsafe_ack(msg)
            except Exception as e:
                AbstraLogger.error(f"[ConsumerController] Error in control loop: {e}")
                self.control_consumer.threadsafe_nack(msg)

    def start_loop(self):
        if self.executor_pool:
            self.executor_pool.start()

        if self.metrics_reporter:
            self.metrics_reporter.start()

        if self.debug_monitor:
            self.debug_monitor.start()

        if self.control_consumer:
            self.control_thread = Thread(target=self._control_loop, daemon=True)
            self.control_thread.start()

        elapsed_time = 0
        while not self.executor_pool.can_start_loop():
            time.sleep(1)
            elapsed_time += 1
            if elapsed_time % 60 == 0:
                AbstraLogger.warning(
                    "[ConsumerController] Waiting for executor pool to be ready..."
                    f"Elapsed time: {elapsed_time} seconds"
                )

            if elapsed_time >= 300:
                AbstraLogger.error(
                    "[ConsumerController] Executor pool not ready after 5 minutes. "
                    "Shutting down pool and exiting with error."
                )
                self.executor_pool.shutdown()
                raise ExecutorPoolNotReadyError(
                    "Executor pool not ready after 5 minutes"
                )

        try:
            self.executor = ThreadPoolExecutor(
                max_workers=self.concurrency,
                thread_name_prefix="ExecutionConsumer",
            )

            for msg in self.consumer.iter():
                if self.executor._shutdown:
                    break

                if isinstance(msg, ControlQueueMessage):
                    self.executor.submit(self._handle_control_message, msg=msg)
                    continue

                self.executor.submit(
                    self.run_subprocess,
                    msg=msg,
                )
        except Exception as e:
            AbstraLogger.error(f"[ConsumerController] Error in main loop: {e}")
            AbstraLogger.capture_exception(e)
        finally:
            if self.debug_monitor:
                self.debug_monitor.stop()
            if self.metrics_reporter:
                self.metrics_reporter.stop()
            if self.executor:
                self.executor.shutdown(wait=True)
                self.executor = None
            if self.executor_pool:
                self.executor_pool.shutdown()

    def shutdown(self):
        if self.executor:
            self.executor.shutdown(wait=True)
            self.executor = None

    def _handle_control_message(self, msg: ControlQueueMessage) -> None:
        try:
            control_msg = msg.message
            if isinstance(control_msg, StopExecutionMessage):
                self.executor_pool.kill_execution(control_msg.payload.execution_id)
            elif isinstance(control_msg, RunSnippetMessage):
                control_msg.connection = msg.connection
                self._handle_run_snippet(control_msg)
            elif isinstance(control_msg, RunSnippetSandboxedMessage):
                control_msg.connection = msg.connection
                self._handle_run_snippet_sandboxed(control_msg)

            self.consumer.threadsafe_ack(msg)
        except Exception as e:
            AbstraLogger.error(
                f"[ConsumerController] Error handling control message: {e}"
            )
            self.consumer.threadsafe_nack(msg)

    def _handle_run_snippet(self, msg: RunSnippetMessage) -> None:
        response = self.executor_pool.run_snippet(
            code=msg.payload.code,
            worker_id=self.worker_id,
            title=msg.payload.title,
        )

        result = {
            "ok": response.success,
            "error": response.error,
            "logs": response.logs or [],
        }
        self._send_snippet_result(msg, result)

    def _handle_run_snippet_sandboxed(self, msg: RunSnippetSandboxedMessage) -> None:
        # Throwaway Landlock process (not an executor-pool process). Still holds
        # one dispatch thread while blocking on the child — bounded by timeout.
        # build_prod_repositories is module-level so it pickles into the child.
        from abstra_internals.controllers.execution.sandboxed_snippet import (
            run_snippet_sandboxed,
        )
        from abstra_internals.repositories.factory import build_prod_repositories

        response = run_snippet_sandboxed(
            code=msg.payload.code,
            title=msg.payload.title,
            worker_id=self.worker_id,
            mp_context=self.main_controller.repositories.mp_context.get_context(),
            repositories_factory=build_prod_repositories,
            timeout_s=int(msg.timeout_ms / 1000) if msg.timeout_ms else None,
        )

        result = {
            "ok": response.success,
            "error": response.error,
            "logs": response.logs or [],
        }
        # Match cloud-api's SessionConnection queue args (session mode +
        # publisher-supplied expiry) or RabbitMQ 406s on redeclare. Send-only.
        self._send_snippet_result(
            msg,
            result,
            is_session=True,
            queue_expire_ms=msg.queue_expire_ms,
            auto_start_consumer=False,
        )

    def _send_snippet_result(
        self,
        msg: Union[RunSnippetMessage, RunSnippetSandboxedMessage],
        result: dict,
        is_session: bool = False,
        queue_expire_ms: Optional[int] = None,
        auto_start_consumer: bool = True,
    ) -> None:
        result_json = json.dumps(result)

        if msg.connection:
            msg.connection.send(result_json)
            msg.connection.close()
        elif RABBITMQ_CONNECTION_URI:
            correlation_id = msg.correlation_id or ""
            with RabbitMQConnection(
                connection_uri=RABBITMQ_CONNECTION_URI,
                send_queue=f"worker_to_server_{correlation_id}",
                recv_queue=f"server_to_worker_{correlation_id}",
                execution_id=correlation_id,
                is_session=is_session,
                queue_expire_ms=queue_expire_ms,
                auto_start_consumer=auto_start_consumer,
            ) as conn:
                conn.send(result_json)

    def run_subprocess(self, msg: QueueMessage) -> None:
        execution_id = msg.preexecution.execution_id
        connection = None
        rabbitmq_params = None
        message_handled = False

        AbstraLogger.lifecycle(
            f"[RUN {execution_id}] PreExecution received",
            {
                "executionId": execution_id,
                "jobId": msg.preexecution.stage_id,
                "sendQueue": msg.preexecution.send_queue,
                "recvQueue": msg.preexecution.recv_queue,
                "stage": "runtime.preexecution.received",
            },
        )

        try:
            if msg.redelivered:
                message_handled = True
                raise Exception("Execution did not complete on a previous delivery")

            stage = self.main_controller.get_stage(msg.preexecution.stage_id)

            if stage is None:
                AbstraLogger.error(
                    f"[ConsumerController] Stage not found: {msg.preexecution.stage_id}."
                    f"Aborting execution. Message [{msg.delivery_tag}] will be acknowledged."
                )
                self.consumer.threadsafe_ack(msg)
                message_handled = True
                return

            if isinstance(
                self.main_controller.repositories.producer, LocalProducerRepository
            ):
                assert msg.connection is not None, "Connection is None in local mode"
                connection = msg.connection
            else:
                assert RABBITMQ_CONNECTION_URI is not None, (
                    "RABBITMQ_CONNECTION_URI is None in production mode"
                )
                rabbitmq_params = RabbitMQParams(
                    connection_uri=RABBITMQ_CONNECTION_URI,
                    execution_id=execution_id,
                    send_queue=msg.preexecution.send_queue,
                    recv_queue=msg.preexecution.recv_queue,
                    queue_expire_ms=msg.preexecution.queue_expire_ms,
                )

            response = self.executor_pool.execute(
                stage=cast(StageWithFile, stage),
                worker_id=self.worker_id,
                execution_id=execution_id,
                request=msg.preexecution.context,
                connection=connection,
                rabbitmq_params=rabbitmq_params,
                user_jwt=msg.preexecution.user_jwt,
            )

            if not response.success:
                raise NonCleanExit(f"Execution failed: {response.error}")

            self.consumer.threadsafe_ack(msg)
            message_handled = True

        except ExecutorDiedError as e:
            AbstraLogger.warning(
                f"[ConsumerController] Executor died during [{msg.delivery_tag}] "
                f"execution_id={execution_id}: {e}; requeuing to mark failed on redelivery"
            )
            try:
                self.consumer.threadsafe_nack(msg, requeue=True)
            except Exception as nack_error:
                AbstraLogger.error(
                    f"[ConsumerController] Failed to nack [{msg.delivery_tag}]: {nack_error}"
                )
            message_handled = True

        except Exception as e:
            AbstraLogger.error(
                f"[ConsumerController] Error processing message [{msg.delivery_tag}]: {e}"
            )
            AbstraLogger.capture_exception(e)

            try:
                self.main_controller.fail_execution(
                    execution_id=execution_id,
                    reason=f"{e}",
                )
            except Exception as db_error:
                AbstraLogger.error(
                    f"[ConsumerController] Failed to update execution status in DB: {db_error}"
                )
                AbstraLogger.capture_exception(db_error)

            self.consumer.threadsafe_ack(msg)
            message_handled = True

        finally:
            if not message_handled:
                AbstraLogger.error(
                    f"[ConsumerController] Message [{msg.delivery_tag}] was not handled properly, nacking"
                )
                try:
                    self.consumer.threadsafe_nack(msg)
                except Exception as nack_error:
                    AbstraLogger.error(
                        f"[ConsumerController] Failed to nack message [{msg.delivery_tag}]: {nack_error}"
                    )
