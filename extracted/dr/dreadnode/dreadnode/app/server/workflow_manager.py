"""Runtime-owned execution for authored workflows.

The platform persists and scopes runs; this manager is the Release 1 host that
polls for pending runs assigned to this runtime and executes their step bodies
beside the installed capability code.
"""

import asyncio
import contextlib
import typing as t
import uuid
from datetime import UTC, datetime

from dreadnode_workflow_core import Fact
from loguru import logger

from dreadnode.app.api.client import ConflictError
from dreadnode.app.client.runtime_client import RuntimeClient
from dreadnode.workflows import PlatformFactSink, WorkflowHost
from dreadnode.workflows.loader import load_workflow_for_definition

ApiContext = tuple[t.Any, str, str, str]


class WorkflowLifecycleManager:
    """Poll and execute runs assigned to one hosted runtime."""

    def __init__(
        self,
        *,
        runtime_id: str,
        resolve_api_context: t.Callable[[], ApiContext | None],
        resolve_runtime_connection: t.Callable[[], tuple[str | None, str | None]],
        poll_interval: float = 2.0,
        max_concurrent_runs: int = 4,
    ) -> None:
        self.runtime_id = runtime_id
        self._resolve_api_context = resolve_api_context
        self._resolve_runtime_connection = resolve_runtime_connection
        self._poll_interval = poll_interval
        self._max_concurrent_runs = max_concurrent_runs
        self._poll_task: asyncio.Task[None] | None = None
        self._run_tasks: dict[str, asyncio.Task[None]] = {}

    async def start(self) -> None:
        if self._poll_task is not None:
            return
        self._poll_task = asyncio.create_task(
            self._poll_loop(),
            name=f"workflow-poll-{self.runtime_id}",
        )
        logger.info("Workflow runtime host started | runtime_id={}", self.runtime_id)

    async def stop(self) -> None:
        tasks = [task for task in (self._poll_task, *self._run_tasks.values()) if task]
        self._poll_task = None
        self._run_tasks.clear()
        for task in tasks:
            task.cancel()
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def poll_once(self) -> None:
        """Poll once. Public for deterministic lifecycle tests."""
        context = self._resolve_api_context()
        if context is None:
            return
        api, org, workspace, _user_id = context
        available = self._max_concurrent_runs - len(self._run_tasks)
        if available <= 0:
            return
        rows = await asyncio.to_thread(
            api.list_workflow_runs,
            org,
            workspace,
            runtime_id=self.runtime_id,
            status="pending",
            limit=100,
        )
        for row in rows[:available]:
            run_id = str(row["id"])
            if run_id in self._run_tasks:
                continue
            execution_id = str(uuid.uuid4())
            try:
                await asyncio.to_thread(
                    api.claim_workflow_run,
                    org,
                    workspace,
                    run_id,
                    execution_id=execution_id,
                    runtime_id=self.runtime_id,
                )
            except ConflictError:
                continue
            except Exception:
                logger.exception(
                    "Workflow runtime claim failed | runtime_id={} run_id={}",
                    self.runtime_id,
                    run_id,
                )
                continue
            task = asyncio.create_task(
                self._execute_run(api, org, workspace, row, execution_id),
                name=f"workflow-run-{run_id}",
            )
            self._run_tasks[run_id] = task
            task.add_done_callback(
                lambda completed, owned_run_id=run_id: self._run_finished(owned_run_id, completed)
            )

    async def _poll_loop(self) -> None:
        while True:
            try:
                await self.poll_once()
            except asyncio.CancelledError:
                raise
            except Exception:
                logger.exception("Workflow runtime poll failed | runtime_id={}", self.runtime_id)
            await asyncio.sleep(self._poll_interval)

    def _run_finished(self, run_id: str, task: asyncio.Task[None]) -> None:
        self._run_tasks.pop(run_id, None)
        if task.cancelled():
            return
        error = task.exception()
        if error is not None:
            logger.error(
                "Workflow runtime task failed | runtime_id={} run_id={} error={}",
                self.runtime_id,
                run_id,
                error,
            )

    async def _execute_run(
        self,
        api: t.Any,
        org: str,
        workspace: str,
        summary: dict[str, t.Any],
        execution_id: str,
    ) -> None:
        run_id = str(summary["id"])
        sink = PlatformFactSink(api, org, workspace, run_id, execution_id)
        client: RuntimeClient | None = None
        try:
            detail, definition = await asyncio.gather(
                asyncio.to_thread(api.get_workflow_run, org, workspace, run_id),
                asyncio.to_thread(
                    api.get_workflow_definition,
                    org,
                    workspace,
                    str(summary["definition_id"]),
                ),
            )
            if str(detail.get("runtime_id") or "") != self.runtime_id:
                return

            workflow, topology = await asyncio.to_thread(load_workflow_for_definition, definition)
            runtime_url, runtime_token = self._resolve_runtime_connection()
            client = RuntimeClient(runtime_url, auth_token=runtime_token)
            host = WorkflowHost(
                workflow,
                topology,
                client=client,
                sink=sink,
                capability=definition.get("capability_name"),
                run_id=run_id,
                session_group_id=detail.get("session_group_id"),
            )
            await host.run(detail.get("input_json") or {})
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            logger.exception(
                "Workflow execution failed before completion | runtime_id={} run_id={}",
                self.runtime_id,
                run_id,
            )
            await self._record_failure(api, org, workspace, run_id, sink, exc)
        finally:
            if client is not None:
                await client.close()

    async def _record_failure(
        self,
        api: t.Any,
        org: str,
        workspace: str,
        run_id: str,
        sink: PlatformFactSink,
        error: Exception,
    ) -> None:
        with contextlib.suppress(Exception):
            detail = await asyncio.to_thread(api.get_workflow_run, org, workspace, run_id)
            if detail.get("status") in {"completed", "failed", "cancelled", "lost"}:
                return
            await sink.emit(
                [
                    Fact(
                        seq=int(detail.get("last_fact_seq") or 0) + 1,
                        kind="run_failed",
                        payload={"error": str(error)},
                        occurred_at=datetime.now(UTC),
                    )
                ]
            )
