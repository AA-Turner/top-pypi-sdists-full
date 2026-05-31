import gc
import os
import threading
import traceback
from pathlib import Path
from typing import Literal, Optional, Tuple
from uuid import uuid4

from abstra_internals.controllers.execution.execution_client import ExecutionClient
from abstra_internals.controllers.execution.execution_client_form import ClientAbandoned
from abstra_internals.controllers.sdk.sdk_context import SDKContext
from abstra_internals.entities.execution import Execution
from abstra_internals.entities.execution_context import (
    ClientContext,
    CodeSnippetContext,
)
from abstra_internals.environment import IS_PRODUCTION
from abstra_internals.logger import AbstraLogger
from abstra_internals.modules import import_as_new
from abstra_internals.repositories.factory import Repositories
from abstra_internals.repositories.project.project import StageWithFile
from abstra_internals.settings import Settings
from abstra_internals.usage import send_execution_usage
from abstra_internals.utils.datetime import now_str
from abstra_internals.utils.file import clear_local_modules

DEFAULT_STATUS = "failed"

ExecutionResult = Tuple[Literal["finished", "abandoned", "failed"], Optional[Exception]]


class ExecutionController:
    def __init__(
        self,
        *,
        repositories: Repositories,
        stage: StageWithFile,
        client: ExecutionClient,
        context: ClientContext,
        user_jwt: Optional[str] = None,
    ) -> None:
        self.repositories = repositories
        self.stage = stage
        self.client = client
        self.context = context
        self.user_jwt = user_jwt

    def run(self, execution_id: str, worker_id: str):
        execution = Execution.create(
            id=execution_id,
            context=self.context,
            stage_id=self.stage.id,
            worker_id=worker_id,
        )

        AbstraLogger.lifecycle(
            f"[RUN {execution.id}] User code starting",
            {
                "executionId": execution.id,
                "jobId": self.stage.id,
                "filePath": str(self.stage.file_path),
                "stage": "runtime.user_code.start",
            },
        )

        with SDKContext(execution, self.client, self.repositories, self.user_jwt):
            status = DEFAULT_STATUS
            create_thread = threading.Thread(
                target=self.repositories.execution.create,
                args=(execution,),
                daemon=True,
            )
            try:
                create_thread.start()
                short_stage_id = self.stage.id.split("-")[0]
                print(
                    f"[ABSTRA] {now_str()} - Execution started for stage {short_stage_id}"
                )

                self.client.handle_start(execution.id)

                status, exception = self._execute_code(self.stage.file_path)
                send_execution_usage(self.stage.file_path, status, exception)
                if status == "abandoned":
                    self.client.handle_abandoned()
                elif exception:
                    self.client.handle_failure(exception)
                else:
                    self.client.handle_success()
            except ClientAbandoned:
                status = "abandoned"
                self.client.handle_abandoned()
            except Exception as e:
                status = "failed"
                AbstraLogger.error(f"[ExecutionController] Unexpected error: {e}")
                AbstraLogger.capture_exception(e)
            finally:
                execution.teardown_tests()
                print(f"[ABSTRA] {now_str()} - Execution {status}")
                try:
                    create_thread.join(timeout=10.0)
                    execution.set_status(status)
                    self.repositories.execution.update(execution)
                    # Drain any buffered logs before the (long-lived) executor
                    # moves on / is recycled. No-op on file/HTTP repos; the
                    # Postgres repo overrides it. Inside the existing try →
                    # best-effort, can never escape run().
                    self.repositories.execution_logs.final_flush()
                except Exception as e_final:
                    AbstraLogger.capture_exception(e_final)

        return {"execution": execution.model_dump()}

    @staticmethod
    def run_snippet(
        file_path: Path,
        worker_id: str,
        repositories: Repositories,
    ) -> dict:
        """Simplified execution for code snippets.

        No execution persistence, no client callbacks, no stage.
        Wraps with SDKContext so code can use SDK features (tasks, AI, etc.).
        Returns ok/error plus execution_id so caller can retrieve logs.
        """
        snippet_id = str(uuid4())
        execution_id = f"snippet-{snippet_id}"

        execution = Execution.create(
            id=execution_id,
            context=CodeSnippetContext(),
            stage_id=f"snippet-{snippet_id}",
            worker_id=worker_id,
        )

        with SDKContext(execution, None, repositories):
            try:
                if not IS_PRODUCTION:
                    clear_local_modules(file_path, Settings.root_path)
                import_as_new(file_path.as_posix())
                return {"ok": True, "error": None, "execution_id": execution_id}
            except SystemExit as e:
                if e.code is None or e.code == 0:
                    return {"ok": True, "error": None, "execution_id": execution_id}
                return {
                    "ok": False,
                    "error": f"SystemExit: {e.code}",
                    "execution_id": execution_id,
                }
            except Exception as e:
                return {"ok": False, "error": str(e), "execution_id": execution_id}

    def _execute_without_exit(self, filepath: Path):
        try:
            if not IS_PRODUCTION:
                clear_local_modules(filepath, Settings.root_path)
            import_as_new(filepath.as_posix())
        except SystemExit as e:
            no_errors = e.code is None or e.code == 0
            if no_errors:
                return
            raise Exception(f"SystemExit: {e.code}") from e

    def print_filtered_exception(self, exception: Exception, entrypoint: Path) -> None:
        # normcase is used to make the paths case-insensitive and replace backslashes with slashes on Windows
        normalized_entrypoint = os.path.normcase(str(entrypoint.resolve()))

        entrypoint_frame_index = 0
        legacy_thread_frame_index = 0

        tb = exception.__traceback__
        index = 0
        while tb:
            frame_filename = os.path.normcase(
                str(Path(tb.tb_frame.f_code.co_filename).resolve())
            )
            if frame_filename == normalized_entrypoint:
                entrypoint_frame_index = index
            if tb.tb_frame.f_code.co_name == "use_legacy_threads":
                legacy_thread_frame_index = index
            index += 1
            tb = tb.tb_next

        user_frame_index = max(entrypoint_frame_index, legacy_thread_frame_index)

        # Reset traceback and skip frames before the user frame
        tb = exception.__traceback__
        for _ in range(user_frame_index):
            if tb is not None:
                tb = tb.tb_next

        traceback.print_exception(type(exception), exception, tb)

    def _execute_code(self, filepath: Path) -> ExecutionResult:
        try:
            self._execute_without_exit(filepath)
            return "finished", None
        except ClientAbandoned:
            return "abandoned", None
        except Exception as e:
            self.print_filtered_exception(e, entrypoint=filepath)
            return "failed", e
        finally:
            gc.collect()
