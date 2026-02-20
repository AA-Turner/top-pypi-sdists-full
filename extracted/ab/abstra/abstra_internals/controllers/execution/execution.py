import gc
import os
import traceback
from pathlib import Path
from typing import Literal, Optional, Tuple, cast

from abstra_internals.controllers.execution.execution_client import ExecutionClient
from abstra_internals.controllers.execution.execution_client_form import ClientAbandoned
from abstra_internals.controllers.sdk.sdk_context import SDKContext
from abstra_internals.entities.execution import Execution
from abstra_internals.entities.execution_context import ClientContext
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
    ) -> None:
        self.repositories = repositories
        self.stage = stage
        self.client = client
        self.context = context

    def run(self, execution_id: str, worker_id: str):
        execution = Execution.create(
            id=execution_id,
            context=self.context,
            stage_id=self.stage.id,
            worker_id=worker_id,
        )

        with SDKContext(execution, self.client, self.repositories):
            status = DEFAULT_STATUS
            try:
                self.repositories.execution.create(execution)
                short_stage_id = self.stage.id.split("-")[0]
                print(
                    f"[ABSTRA] {now_str()} - Execution started for stage {short_stage_id}"
                )

                self.client.handle_start(execution.id)

                from abstra_internals.repositories.project.project import AgentStage

                if isinstance(self.stage, AgentStage):
                    status, exception = self._execute_agent()
                else:
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
                    execution.set_status(status)
                    self.repositories.execution.update(execution)
                except Exception as e_final:
                    AbstraLogger.capture_exception(e_final)

        return {"execution": execution.model_dump()}

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

    def _execute_agent(self) -> ExecutionResult:
        """Execute an agent stage via the Lua REPL executor."""
        browser_session = None
        try:
            from abstra_internals.controllers.sdk.sdk_context import SDKContextStore
            from abstra_internals.entities.agents.action_intelligence import (
                ActionIntelligence,
            )
            from abstra_internals.entities.agents.action_tracker import ActionTracker
            from abstra_internals.entities.agents.exploration_strategy import (
                BFSExplorationStrategy,
            )
            from abstra_internals.entities.agents.lua.executor import LuaExecutor
            from abstra_internals.entities.agents.lua.prompt_builder import (
                LuaPromptBuilder,
            )
            from abstra_internals.entities.agents.lua.runtime import LupaRuntime
            from abstra_internals.entities.agents.lua.tool_adapter import LuaToolAdapter
            from abstra_internals.entities.agents.memory_manager import (
                MemoryManager,
                MemoryReducer,
            )
            from abstra_internals.entities.agents.secret_manager import SecretManager
            from abstra_internals.entities.agents.template import JinjaTemplateRenderer
            from abstra_internals.entities.agents.tools.browser_session import (
                BrowserSession,
            )
            from abstra_internals.entities.agents.tools.factory import (
                build_tool_handlers,
            )
            from abstra_internals.repositories.project.project import AgentStage

            stage = cast(AgentStage, self.stage)
            sdk_context = SDKContextStore.get_by_thread()

            # Reload stage from project file to ensure permissions and
            # transitions are fresh (they may be lost during serialization
            # through multiprocessing Queue).
            project = self.repositories.project.load(include_disabled_stages=False)
            fresh_stage = project.get_stage(stage.id)
            if isinstance(fresh_stage, AgentStage):
                stage = fresh_stage

            # 1. Get trigger task data
            trigger_task = sdk_context.task_sdk.get_trigger_task()

            # 2. Render the .md template with task context
            renderer = JinjaTemplateRenderer()
            prompt = renderer.render_from_file(
                str(stage.file_path),
                {
                    "os": os,
                    "trigger_task": {
                        "type": trigger_task.type,
                        "payload": trigger_task.payload,
                        **(
                            trigger_task.payload
                            if isinstance(trigger_task.payload, dict)
                            else {}
                        ),
                    },
                },
            )
            # 3. Build tools from permissions + workflow transitions
            target_task_schemas = {}
            for transition in stage.workflow_transitions:
                target_stage = project.get_stage(transition.target_id)
                if target_stage is not None:
                    schema = getattr(target_stage, "task_schema", None)
                    if schema:
                        target_task_schemas[transition.target_id] = schema

            import tempfile
            from pathlib import Path

            working_dir = Path(tempfile.mkdtemp(prefix="agent_work_"))
            browser_session = BrowserSession(download_dir=str(working_dir))

            # Create intelligence modules
            memory_manager = MemoryManager()
            memory_reducer = MemoryReducer()
            secret_manager = SecretManager()
            action_tracker = ActionTracker()
            action_intelligence = ActionIntelligence()
            exploration_strategy = BFSExplorationStrategy()

            tool_handlers = build_tool_handlers(
                stage=stage,
                tables_repo=self.repositories.tables,
                connectors_repo=self.repositories.connectors,
                task_sdk=sdk_context.task_sdk,
                working_dir=working_dir,
                target_task_schemas=target_task_schemas,
                browser_session=browser_session,
                memory_manager=memory_manager,
            )

            # 4. Execute with Lua REPL
            runtime = LupaRuntime(working_dir=working_dir)
            executor = LuaExecutor(
                ai_sdk=sdk_context.ai_sdk,
                tool_handlers=tool_handlers,
                runtime=runtime,
                tool_adapter=LuaToolAdapter(log_fn=runtime.log_output),
                prompt_builder=LuaPromptBuilder(),
                max_steps=stage.max_steps,
                screenshot_fn=browser_session.take_screenshot
                if browser_session
                else None,
                secret_manager=secret_manager,
                memory_manager=memory_manager,
                memory_reducer=memory_reducer,
                action_tracker=action_tracker,
                action_intelligence=action_intelligence,
                exploration_strategy=exploration_strategy,
                browser_session=browser_session,
            )
            result = executor.execute(
                prompt, stage.permissions, base_dir=stage.file_path.parent
            )

            if result.success:
                return "finished", None
            else:
                return "failed", Exception(result.error or "Agent execution failed")

        except ClientAbandoned:
            return "abandoned", None
        except Exception as e:
            traceback.print_exc()
            return "failed", e
        finally:
            if browser_session is not None:
                browser_session.close()
