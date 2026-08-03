"""
Events module for handling background tasks and event streaming in the xpander.ai platform.

This module provides functionality for managing Server Sent Events (SSE) and executing tasks
based on events within the xpander.ai platform. It supports asynchronous execution and retry logic.
"""

from __future__ import annotations

import asyncio
import json
import json as py_json
import os
import signal
import sys
from os import getenv
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Awaitable, Callable, Optional, Set, Union, List

import httpx
from httpx_sse import aconnect_sse
from loguru import logger
from pydantic import BaseModel

from xpander_sdk.utils.answer_guards import PROMISE_CONTINUATION_NUDGE, is_promise_only_answer

from xpander_sdk.core.module_base import ModuleBase
from xpander_sdk.exceptions.module_exception import ModuleException
from xpander_sdk.models.configuration import Configuration
from xpander_sdk.models.shared import OutputFormat
from xpander_sdk.modules.agents.models.agent import SourceNodeType
from xpander_sdk.modules.tasks.tasks_module import Tasks

from .utils.git_init import configure_git_credentials
from .utils.generic import backoff_delay, get_events_base, get_events_headers
from .models.deployments import DeployedAsset
from .models.events import (
    EventType,
    WorkerEnvironmentConflict,
    WorkerFinishedEvent,
    WorkerHeartbeat,
    WorkerCapacityUpdateEvent,
)
from ..tasks.sub_modules.task import Task
from ..tasks.models.task import AgentExecutionStatus, LocalTaskTest

_MAX_RETRIES = 5  # total attempts (1 initial + 4 retries)

# Plan enforcement: max retries when plan tasks remain incomplete after arun()
MAX_PLAN_RETRIES: int = 5


async def _run_end_finalize(task) -> None:
    """Mark evidence-backed plan items when a mid-run finalize exited in plain text."""
    try:
        from xpander_sdk.core.context_optimizer.finalize_mode import (
            finalize_task_from_run_end,
        )

        await finalize_task_from_run_end(task)
    except Exception as exc:
        logger.warning(f"[finalize-mode] run-end finalize failed: {exc}")


ExecutionRequestHandler = Union[
    Callable[[Task], Task],
    Callable[[Task], Awaitable[Task]],
]

BootHandler = Union[
    Callable[[], None],
    Callable[[], Awaitable[None]],
]

ShutdownHandler = Union[
    Callable[[], None],
    Callable[[], Awaitable[None]],
]


class Events(ModuleBase):
    """
    Events module for managing SSE connections and task execution.

    This class manages Server Sent Events (SSE) for real-time task execution requests
    and integrates with agents deployed on xpander.ai. It handles event streaming,
    retry logic, and background task management. The worker is directly attached
    to the agent without a parent worker hierarchy.

    Attributes:
        worker (Optional[DeployedAsset]): Represents the deployed asset/agent worker.
        test_task (Optional[LocalTaskTest]): Task to be tested within the local environment.
        configuration (Configuration): SDK configuration with credentials and endpoints.

    Example:
        >>> events = Events()
        >>> events.register(on_task=handle_task)
    """

    worker: Optional[DeployedAsset] = None
    test_task: Optional[LocalTaskTest] = None
    _heartbeat_task: Optional[asyncio.Task] = None

    # Class-level registries for boot and shutdown handlers
    _boot_handlers: List[BootHandler] = []
    _shutdown_handlers: List[ShutdownHandler] = []

    def __init__(
        self,
        configuration: Optional[Configuration] = None,
        max_sync_workers: Optional[int] = 6,
        max_retries: Optional[int] = _MAX_RETRIES,
    ):
        """
        Initialize the Events module with configuration and worker settings.

        Configures event streaming parameters and validates essential environment setup.

        Args:
            configuration (Optional[Configuration]): SDK configuration with credentials and endpoints. Defaults to environment configuration.
            max_sync_workers (Optional[int]): Maximum number of synchronous worker threads. Defaults to 6.
            max_retries (Optional[int]): Maximum retry attempts for network calls. Defaults to 5.

        Raises:
            ModuleException: When required environment variables are missing or configuration is incorrect.
        """
        super().__init__(configuration)
        configure_git_credentials()

        self.is_xpander_cloud = getenv("IS_XPANDER_CLOUD", "false") == "true"
        self.agent_id = self.configuration.agent_id or getenv("XPANDER_AGENT_ID", None)

        if not self.agent_id:
            raise ModuleException(
                400, "XPANDER_AGENT_ID is missing from your environment variables."
            )
        if not self.configuration.organization_id:
            raise ModuleException(
                400,
                "XPANDER_ORGANIZATION_ID is missing from your environment variables.",
            )
        if not self.configuration.api_key:
            raise ModuleException(
                400, "XPANDER_API_KEY is missing from your environment variables."
            )

        self.max_retries = max_retries
        self.max_sync_workers = max_sync_workers

        # Internal resources
        self._pool: ThreadPoolExecutor = ThreadPoolExecutor(
            max_workers=max_sync_workers,
            thread_name_prefix="xpander-handler",
        )
        self._bg: Set[asyncio.Task] = set()
        self._execution_semaphore: Optional[asyncio.Semaphore] = None

        from xpander_sdk import __version__

        logger.info(f"xpander-sdk v{__version__}")
        logger.debug(
            f"Events initialised (base_url={self.configuration.base_url}, "
            f"org_id={self.configuration.organization_id}, retries={self.max_retries})"
        )

    # lifecycle
    async def start(
        self,
        on_execution_request: ExecutionRequestHandler,
    ) -> None:
        """
        Start the event listener and register handlers for task execution events.

        This method sets up signal handling for graceful shutdown, registers the
        agent worker directly, and begins listening to task execution requests over SSE.
        Use the @on_task decorator instead of calling this method directly.

        Args:
            on_execution_request (ExecutionRequestHandler): Callback handler
                for processing task execution requests. Can be synchronous or asynchronous.
        """
        # Execute boot handlers first, before any event listeners are set up
        await self._execute_boot_handlers()

        # Initialize semaphore for capacity tracking
        self._execution_semaphore = asyncio.Semaphore(self.max_sync_workers)

        loop = asyncio.get_running_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(
                sig, lambda s=sig: asyncio.create_task(self.stop(s))
            )

        # Register agent worker directly
        self.track(
            asyncio.create_task(
                self.register_agent_worker(self.agent_id, on_execution_request)
            )
        )

        logger.info("Listener started; waiting for events…")
        await asyncio.gather(*self._bg)

    async def stop(self, sig: signal.Signals | None = None) -> None:
        """
        Stop the event listener and cleanup background tasks.

        Args:
            sig (signal.Signals | None): Signal that triggered the stop request.

        Example:
            >>> await events.stop()
        """
        if sig:
            logger.info(f"Received {sig.name} – shutting down…")

        for t in self._bg:
            t.cancel()
        if self._bg:
            await asyncio.gather(*self._bg, return_exceptions=True)

        self._pool.shutdown(wait=False, cancel_futures=True)
        self._bg.clear()

        # Execute shutdown handlers after stopping event listeners but before final cleanup
        await self._execute_shutdown_handlers()

        logger.info("Listener stopped.")

    async def __aenter__(self) -> "Events":
        return self

    async def __aexit__(self, *_exc) -> bool:  # noqa: D401
        await self.stop()
        return False

    # ---------------------- HTTP helpers with retry ---------------------- #

    async def _request_with_retries(
        self,
        method: str,
        url: str,
        *,
        headers: dict[str, str],
        json: Any | None = None,
        timeout: float | None = 10.0,
    ) -> httpx.Response:
        """
        Perform an HTTP request with automatic retries on failure.

        Args:
            method (str): HTTP method to use for the request (e.g., 'POST', 'GET').
            url (str): The URL to which the request is sent.
            headers (dict[str, str]): HTTP headers to include in the request.
            json (Any | None, optional): JSON payload to send with the request.
            timeout (float | None, optional): Timeout for the request.

        Returns:
            httpx.Response: The response object received from the request.

        Raises:
            Exception: If the request fails after the maximum retry attempts.
        """
        last_exc: Exception | None = None
        for attempt in range(1, self.max_retries + 1):
            try:
                async with httpx.AsyncClient(timeout=timeout) as client:
                    response = await client.request(
                        method,
                        url,
                        headers=headers,
                        json=json,
                        follow_redirects=True,
                    )
                return response
            except Exception as exc:  # noqa: BLE001 broad (includes timeouts)
                last_exc = exc
                if attempt < self.max_retries:
                    delay = backoff_delay(attempt)
                    await asyncio.sleep(delay)
                else:
                    logger.error(
                        f"{method} {url} failed after {self.max_retries} attempts - exiting. ({exc})"
                    )
                    sys.exit(1)
        assert last_exc is not None
        raise last_exc  # for static checkers

    async def _notify_capacity_status(self, worker_id: str, is_busy: bool) -> None:
        """
        Notify the backend of the worker's capacity status.

        Args:
            worker_id (str): The unique identifier of the worker.
            is_busy (bool): Whether the worker is at max capacity.
        """
        url = f"{get_events_base(configuration=self.configuration)}/{worker_id}?type=worker&agent_id={self.agent_id}"
        await self._request_with_retries(
            "POST",
            url,
            headers=get_events_headers(configuration=self.configuration),
            json=WorkerCapacityUpdateEvent(data={"is_busy": is_busy}).model_dump_safe(),
        )

    async def _release_worker(self, worker_id: str) -> None:
        """
        Release the worker resource after task execution completion.

        Args:
            worker_id (str): The unique identifier of the worker to release.
        """
        url = f"{get_events_base(configuration=self.configuration)}/{worker_id}?type=worker&agent_id={self.agent_id}"
        await self._request_with_retries(
            "POST",
            url,
            headers=get_events_headers(configuration=self.configuration),
            json=WorkerFinishedEvent(data={}).model_dump_safe(),
        )

    async def _make_heartbeat(self, worker_id: str) -> None:
        """
        Send a heartbeat signal to maintain the worker's active status.

        Args:
            worker_id (str): The unique identifier of the worker to update.
        """
        url = f"{get_events_base(configuration=self.configuration)}/{worker_id}?type=worker&agent_id={self.agent_id}"
        await self._request_with_retries(
            "POST",
            url,
            headers=get_events_headers(configuration=self.configuration),
            json=WorkerHeartbeat().model_dump_safe(),
        )

    # ----------------------- SSE helpers with retry ---------------------- #

    async def _sse_events_with_retries(self, url: str):
        """Yield Server-Sent Events with reconnect/back‑off logic using httpx‑sse."""
        attempt = 1
        while True:
            try:
                async with httpx.AsyncClient(
                    timeout=None, follow_redirects=True
                ) as client:
                    if not url.endswith("/"):
                        url += "/"
                    async with aconnect_sse(
                        client,
                        "GET",
                        url,
                        headers=get_events_headers(configuration=self.configuration),
                        follow_redirects=True,
                    ) as event_source:
                        async for sse in event_source.aiter_sse():
                            yield sse

                # Server closed the stream gracefully – reconnect
                attempt = 1
                await asyncio.sleep(backoff_delay(1))

            except asyncio.CancelledError:
                logger.info("SSE connection cancelled – shutting down.")
                return

            except Exception as exc:  # noqa: BLE001 broad
                if attempt >= self.max_retries:
                    logger.error(
                        f"SSE connection to {url} failed after {self.max_retries} attempts – exiting. ({exc})"
                    )
                    sys.exit(1)
                await asyncio.sleep(backoff_delay(attempt))
                attempt += 1

    async def _handle_task_with_semaphore(
        self,
        agent_worker: DeployedAsset,
        task: Task,
        on_execution_request: ExecutionRequestHandler,
    ) -> None:
        """
        Wrapper that releases semaphore after task execution.
        Semaphore is already acquired before calling this method.
        """
        try:
            await self.handle_task_execution_request(
                agent_worker, task, on_execution_request
            )
        finally:
            # Release execution slot
            self._execution_semaphore.release()

            # Check if we now have available capacity and notify backend
            if self._execution_semaphore._value > 0:
                try:
                    await self._notify_capacity_status(agent_worker.id, is_busy=False)
                except Exception as e:
                    logger.warning(f"Failed to notify available status: {e}")

    async def handle_task_execution_request(
        self,
        agent_worker: DeployedAsset,
        task: Task,
        on_execution_request: ExecutionRequestHandler,
        retry_count: int = 0,
    ) -> None:
        """
        Handle an incoming task execution request.

        After execution completes, checks plan status. If tasks remain
        incomplete, retries with a continuation prompt (up to MAX_PLAN_RETRIES).
        On retry #2, injects focused context about remaining tasks.

        Args:
            agent_worker (DeployedAsset): The deployed asset (agent) to handle the task.
            task (Task): The task object containing execution details.
            on_execution_request (ExecutionRequestHandler): The handler function to process the task.
            retry_count (int): Current retry attempt count. Defaults to 0.
        """
        error = None
        try:
            logger.info(f"Handling task {task.id}")
            await task.aset_status(status=AgentExecutionStatus.Executing)
            if asyncio.iscoroutinefunction(on_execution_request):
                task = await on_execution_request(task)
            else:
                task = await asyncio.get_running_loop().run_in_executor(
                    self._pool,
                    on_execution_request,
                    task,
                )

            # Before the plan check: a mid-run finalize exits in plain text, so its
            # evidence-backed items must be marked or this retries for work already done.
            await _run_end_finalize(task)

            # Check if plan is complete, retry if not
            plan_following_status = await task.aget_plan_following_status()
            if not plan_following_status.can_finish:
                if retry_count >= MAX_PLAN_RETRIES:
                    logger.warning(
                        f"Failed to complete plan after {retry_count + 1} attempts "
                        f"(max: {MAX_PLAN_RETRIES}). Remaining incomplete tasks."
                    )
                    return

                # Pre-retry: build retry-focus guidance for the L2 compaction LLM.
                from xpander_sdk.core.context_optimizer import (
                    build_pre_retry_focus_instructions,
                )
                from xpander_sdk.core.context_optimizer.action_ledger import (
                    get_attached_ledger,
                )
                from xpander_sdk.core.context_optimizer.completion_evidence import (
                    detect_completion_evidence,
                )
                from xpander_sdk.core.context_optimizer.constants import (
                    FINALIZE_MODE_ENABLED,
                    LEDGER_ENABLED,
                )
                from xpander_sdk.core.context_optimizer.finalize_mode import (
                    enter_finalize_mode,
                )

                # Robust-L2 evidence-skip: if the durable action ledger
                # already shows write+verify pairs covering the small
                # number of remaining plan items, skip pre_retry and
                # transition straight to Finalize-Only Mode. This is the
                # Mode-2 fix — "agent did the real work but forgot to
                # toggle the last plan item, then got force-restarted".
                # When evidence is detected we engage Finalize-Only Mode
                # AND fall through to the drain + recurse path below. The
                # recursion runs another ``arun()`` with finalize state
                # active on the task — the agno tool gate then forces
                # ``xpfinalize_task``, which writes ``task.result`` and
                # marks plan items. Returning early here would mean no
                # further ``arun()``: the surrounding ``finally`` block
                # would mark the task ``Completed`` with stale state and
                # ``xpfinalize_task`` would never run.
                evidence_skip = False
                if FINALIZE_MODE_ENABLED and LEDGER_ENABLED:
                    ledger = get_attached_ledger(task)
                    deep_planning = getattr(task, "deep_planning", None)
                    evidence = detect_completion_evidence(ledger, deep_planning)
                    uncompleted = list(plan_following_status.uncompleted_tasks or [])
                    if evidence.has_evidence and len(uncompleted) <= 2:
                        optimizer = getattr(task, "_xp_context_optimizer", None)
                        if optimizer is not None:
                            enter_finalize_mode(
                                optimizer,
                                reason="evidence",
                                evidence=evidence,
                            )
                            logger.info(
                                f"[events] pre_retry skipped — completion evidence "
                                f"detected ({evidence.rationale}); "
                                "finalize-only mode engaged for next arun"
                            )
                            evidence_skip = True

                retry_focus_for_compaction = build_pre_retry_focus_instructions(
                    plan_following_status.uncompleted_tasks, retry_count
                )

                # Pre-retry: force L2 compaction to preserve working state.
                # Skipped on evidence-based finalize — the existing
                # session is already authoritative; another LLM summarize
                # would just burn tokens.
                try:
                    if evidence_skip:
                        compact_result = None
                    else:
                        compact_result = await task.acompact_session_for_retry(
                            custom_instructions=retry_focus_for_compaction,
                        )
                    if compact_result and compact_result.compacted:
                        logger.info(
                            f"Pre-retry compaction complete "
                            f"(tokens: {compact_result.total_tokens:,})"
                        )
                        # Aggregate compaction tokens into task metrics so the
                        # cost of summarization is billed back to the run.
                        # Two bugs were silently dropping tokens here:
                        #   (a) ``if task.tokens:`` skipped aggregation when
                        #       ``task.tokens`` was None (fresh task, first
                        #       compaction before agno populated metrics);
                        #   (b) ``Tokens.total_tokens`` is a Pydantic
                        #       ``@computed_field`` derived from
                        #       prompt+completion — assigning to it raises
                        #       ``AttributeError`` and the compact tokens
                        #       were silently lost.
                        from xpander_sdk.models.shared import Tokens

                        if task.tokens is None:
                            task.tokens = Tokens()
                        task.tokens.prompt_tokens = (
                            task.tokens.prompt_tokens or 0
                        ) + compact_result.input_tokens
                        task.tokens.completion_tokens = (
                            task.tokens.completion_tokens or 0
                        ) + compact_result.output_tokens
                        # ``total_tokens`` is computed; do NOT assign.
                except Exception as compact_exc:
                    logger.warning(f"Pre-retry compaction failed: {compact_exc}")

                # On retry #2: inject focused context about remaining tasks
                if retry_count == 1 and plan_following_status.uncompleted_tasks:
                    focus = ", ".join(
                        t.title for t in plan_following_status.uncompleted_tasks
                    )
                    task.additional_context = (
                        (task.additional_context or "")
                        + f"\n\n<retry_focus>Focus on completing: {focus}. "
                        f"Previous work context is above in <compacted_context>.\n</retry_focus>"
                    )

                # Drain THIS attempt's L1 workspace cache before recursing.
                # The next attempt's ``_configure_context_optimizer`` will
                # overwrite ``task._xp_context_optimizer`` with a fresh
                # instance, so once we recurse we lose the handle to the
                # current optimizer's pending writes. Drain here to avoid
                # leaving an orphaned optimizer with un-flushed writes.
                attempt_optimizer = getattr(task, "_xp_context_optimizer", None)
                if attempt_optimizer is not None:
                    try:
                        await attempt_optimizer.aclose()
                    except Exception as close_exc:
                        logger.warning(
                            f"context-optimizer close failed (pre-retry): {close_exc}"
                        )
                    # Clear the attribute so the outer attempt's finally
                    # block doesn't try to close it again (and so the next
                    # attempt's _configure_context_optimizer sees a clean
                    # slate when it reattaches).
                    try:
                        delattr(task, "_xp_context_optimizer")
                    except AttributeError:
                        pass

                logger.info(
                    f"Plan not complete, retrying "
                    f"(attempt {retry_count + 2}/{MAX_PLAN_RETRIES + 1})"
                )
                await self.handle_task_execution_request(
                    agent_worker,
                    task,
                    on_execution_request,
                    retry_count=retry_count + 1,
                )
                return

            # A promise with zero tool calls is a failed run dressed as progress -
            # nudge ONCE. The nudge's presence in additional_context is the
            # once-only marker (it survives a rebuilt Task object, an attribute
            # flag would not); the retry bound backstops a lost marker.
            if (
                plan_following_status.can_finish
                and retry_count < MAX_PLAN_RETRIES
                and PROMISE_CONTINUATION_NUDGE not in (task.additional_context or "")
                and is_promise_only_answer(
                    str(task.result or ""), len(getattr(task, "used_tools", None) or [])
                )
            ):
                task.additional_context = (
                    (task.additional_context or "") + "\n\n" + PROMISE_CONTINUATION_NUDGE
                )
                logger.warning(
                    f"[promise-guard] task {task.id} ended on a promise with no "
                    "tool calls; auto-continuing once"
                )
                # Drain this attempt's optimizer before recursing (same contract
                # as the plan retry above: the next attempt overwrites the handle).
                nudge_optimizer = getattr(task, "_xp_context_optimizer", None)
                if nudge_optimizer is not None:
                    try:
                        await nudge_optimizer.aclose()
                    except Exception as close_exc:
                        logger.warning(
                            f"context-optimizer close failed (pre-nudge): {close_exc}"
                        )
                    try:
                        delattr(task, "_xp_context_optimizer")
                    except AttributeError:
                        pass
                await self.handle_task_execution_request(
                    agent_worker,
                    task,
                    on_execution_request,
                    retry_count=retry_count + 1,
                )
                return

        except Exception as e:
            logger.exception(f"Execution handler failed - {str(e)}")
            error = str(e)
        finally:
            # Drain the L1 workspace write cache so any encrypted blobs the
            # agent's last turn queued actually land on the sandbox before
            # the task is marked complete. Attached to the task by
            # ``_configure_context_optimizer`` in agno.py. The retry path
            # above drains and detaches before recursing, so this only
            # closes the optimizer for the FINAL attempt (or the only
            # attempt when no retry happens).
            optimizer = getattr(task, "_xp_context_optimizer", None)
            if optimizer is not None:
                try:
                    await optimizer.aclose()
                except Exception as close_exc:
                    logger.warning(f"context-optimizer close failed: {close_exc}")

            # Safety net for the paths that return before the pre-plan call; idempotent.
            await _run_end_finalize(task)

            task_used_tokens = task.tokens
            task_used_tools = task.used_tools

            if error:
                task.result = error
                task.status = AgentExecutionStatus.Error
            elif (
                task.status == AgentExecutionStatus.Executing
            ):  # let the handler set the status, if not set - mark as completed
                task.status = AgentExecutionStatus.Completed
                # a tool-equipped run that never called one and barely answered is the
                # zero-tool-call failure shape (provider dropped/rejected the tool block)
                try:
                    result_len = len(str(task.result or "").strip())
                    had_tools = bool(getattr(task, "_xp_tools_attached", False))
                    if had_tools and not task_used_tools and result_len < 200:
                        logger.warning(
                            f"[zero-tool-run] task {task.id} completed with 0 tool calls "
                            f"and a {result_len}-char answer - suspect the provider never "
                            f"received/honored the tool block (model={getattr(task, 'llm_model_name', None)})"
                        )
                except Exception:
                    pass

            # in case of structured output, return as stringified json
            try:
                if task.output_format == OutputFormat.Json:
                    if isinstance(task.result, BaseModel):
                        task.result = task.result.model_dump_json()
                    if isinstance(task.result, dict) or isinstance(task.result, list):
                        task.result = py_json.dumps(task.result)
            except Exception:
                pass

            await task.asave()
            task.tokens = task_used_tokens
            task.used_tools = task_used_tools

            if task.tokens:
                await task.areport_metrics()

            logger.info(f"Finished handling task {task.id}")

            # local test task, finish? kill the worker
            if self.test_task:
                logger.info("Local task handled, exiting")

                # Print the task result for CLI
                if task.result:
                    logger.info("\n" + "=" * 50)
                    logger.info("TASK RESULT:")
                    logger.info("=" * 50)
                    if isinstance(task.result, (dict, list)):
                        import json

                        logger.info(json.dumps(task.result, indent=2))
                    else:
                        logger.info(task.result)
                    logger.info("=" * 50 + "\n")
                else:
                    logger.info("\n" + "=" * 50)
                    logger.info("TASK COMPLETED (No result set)")
                    logger.info("=" * 50 + "\n")

                # Use os._exit to avoid exception traceback from asyncio
                os._exit(0)

    async def register_agent_worker(
        self,
        agent_id: str,
        on_execution_request: ExecutionRequestHandler,
    ) -> None:
        """
        Register a worker agent and start listening for task events.

        Args:
            agent_id (str): The unique identifier of the agent to register.
            on_execution_request (ExecutionRequestHandler): The callback function to process task execution requests.
        """
        environment = "xpander" if self.is_xpander_cloud else "local"

        url = f"{get_events_base(configuration=self.configuration)}/{agent_id}?environment={environment}"

        async for event in self._sse_events_with_retries(url):
            if event.event == EventType.EnvironmentConflict:
                conflict = WorkerEnvironmentConflict(**json.loads(event.data))
                logger.error(f"Conflict! - {conflict.error}")
                return
            if event.event == EventType.WorkerRegistration:
                self.worker = agent_worker = DeployedAsset(**json.loads(event.data))
                logger.info(f"Worker registered – id={agent_worker.id}")

                # convenience URLs
                agent_meta = agent_worker.metadata or {}
                if agent_meta:
                    is_stg = "stg." in get_events_base(
                        configuration=self.configuration
                    ) or "localhost" in get_events_base(
                        configuration=self.configuration
                    )
                    chat_url = (
                        f"https://{agent_meta.get('unique_name', agent_id)}.agents"
                    )
                    chat_url += ".stg" if is_stg else ""
                    chat_url += ".xpander.ai"

                    builder_url = (
                        "https://"
                        + ("stg." if is_stg else "")
                        + f"app.xpander.ai/agents/{agent_id}"
                    )
                    logger.info(
                        f"Agent '{agent_meta.get('name', agent_id)}' chat: {chat_url} | builder: {builder_url}"
                    )

                if self.test_task:
                    logger.info(f"Invoking agent {self.test_task.model_dump_json()}")
                    created_task = await Tasks(
                        configuration=self.configuration
                    ).acreate(
                        agent_id=self.agent_id,
                        prompt=self.test_task.input.text,
                        file_urls=self.test_task.input.files,
                        user_details=self.test_task.input.user,
                        agent_version=self.test_task.agent_version,
                        worker_id=self.worker.id,
                        output_format=self.test_task.output_format,
                        output_schema=self.test_task.output_schema,
                        run_locally=True,
                        source=SourceNodeType.SDK.value,
                    )
                    self.track(
                        asyncio.create_task(
                            self.handle_task_execution_request(
                                agent_worker, created_task, on_execution_request
                            )
                        )
                    )

                # Cancel previous heartbeat task if it exists and start a new one
                if self._heartbeat_task and not self._heartbeat_task.done():
                    logger.debug(
                        f"Canceling previous heartbeat task for worker {agent_worker.id}"
                    )
                    self._heartbeat_task.cancel()
                self._heartbeat_task = asyncio.create_task(
                    self.heartbeat_loop(agent_worker.id)
                )
                self.track(self._heartbeat_task)

            elif event.event == EventType.AgentExecution:
                task = Task(**json.loads(event.data), configuration=self.configuration)

                # Acquire execution slot immediately (blocks here if at max capacity)
                await self._execution_semaphore.acquire()

                # Check if we're now at max capacity and notify backend
                if self._execution_semaphore._value == 0:
                    try:
                        await self._notify_capacity_status(
                            agent_worker.id, is_busy=True
                        )
                    except Exception as e:
                        logger.warning(f"Failed to notify busy status: {e}")

                self.track(
                    asyncio.create_task(
                        self._handle_task_with_semaphore(
                            agent_worker, task, on_execution_request
                        )
                    )
                )

    # --------------------------------------------------------------------- #
    # Misc helpers                                                          #
    # --------------------------------------------------------------------- #

    def track(self, task: asyncio.Task) -> None:
        """
        Add a task to the background task set for auto-removal on completion.

        Args:
            task (asyncio.Task): The asynchronous task to track.
        """
        self._bg.add(task)
        task.add_done_callback(self._bg.discard)

    async def heartbeat_loop(self, worker_id: str) -> None:
        """
        Continuously send heartbeat signals to maintain worker's active status.

        Args:
            worker_id (str): The unique identifier of the worker.
        """
        while True:
            try:
                await self._make_heartbeat(worker_id)
            except Exception:
                # _request_with_retries handles fatal exit
                pass
            await asyncio.sleep(2)

    def register(
        self,
        on_task: ExecutionRequestHandler,
        test_task: Optional[LocalTaskTest] = None,
    ) -> None:
        """
        Register the event listener with optional test task in synchronous or asynchronous environments.

        Args:
            on_task (ExecutionRequestHandler): Callback handler for task execution.
            test_task (Optional[LocalTaskTest]): Optional local test task for diagnostics and testing.

        Example:
            >>> def handle_task(task):
            ...     # process task execution

            >>> events = Events()
            >>> events.register(on_task=handle_task)
        """
        try:
            self.test_task = test_task
            loop = asyncio.get_running_loop()
            if loop.is_running():
                loop.create_task(self.start(on_task))
            else:
                asyncio.run(self.start(on_task))
        except RuntimeError:
            # No running loop, safe to run
            asyncio.run(self.start(on_task))

    # --------------------------------------------------------------------- #
    # Boot and Shutdown Handler Management                                  #
    # --------------------------------------------------------------------- #

    @classmethod
    def register_boot_handler(cls, handler: BootHandler) -> None:
        """
        Register a boot handler to be executed before event listeners are set up.

        Args:
            handler (BootHandler): The boot handler function to register.
        """
        cls._boot_handlers.append(handler)
        logger.debug(
            f"Boot handler registered: {handler.__name__ if hasattr(handler, '__name__') else 'anonymous'}"
        )

    @classmethod
    def register_shutdown_handler(cls, handler: ShutdownHandler) -> None:
        """
        Register a shutdown handler to be executed during application shutdown.

        Args:
            handler (ShutdownHandler): The shutdown handler function to register.
        """
        cls._shutdown_handlers.append(handler)
        logger.debug(
            f"Shutdown handler registered: {handler.__name__ if hasattr(handler, '__name__') else 'anonymous'}"
        )

    @classmethod
    async def _execute_boot_handlers(cls) -> None:
        """
        Execute all registered boot handlers.

        Raises:
            Exception: If any boot handler fails, the application will not start.
        """
        if not cls._boot_handlers:
            return

        logger.info(f"Executing {len(cls._boot_handlers)} boot handler(s)...")

        for handler in cls._boot_handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler()
                else:
                    handler()
                logger.debug(
                    f"Boot handler executed successfully: {handler.__name__ if hasattr(handler, '__name__') else 'anonymous'}"
                )
            except Exception as e:
                logger.error(
                    f"Boot handler failed: {handler.__name__ if hasattr(handler, '__name__') else 'anonymous'} - {e}"
                )
                raise

        logger.info("All boot handlers executed successfully")

    @classmethod
    async def _execute_shutdown_handlers(cls) -> None:
        """
        Execute all registered shutdown handlers.

        Note: Exceptions in shutdown handlers are logged but do not prevent shutdown.
        """
        if not cls._shutdown_handlers:
            return

        logger.info(f"Executing {len(cls._shutdown_handlers)} shutdown handler(s)...")

        for handler in cls._shutdown_handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler()
                else:
                    handler()
                logger.debug(
                    f"Shutdown handler executed successfully: {handler.__name__ if hasattr(handler, '__name__') else 'anonymous'}"
                )
            except Exception as e:
                logger.error(
                    f"Shutdown handler failed: {handler.__name__ if hasattr(handler, '__name__') else 'anonymous'} - {e}"
                )
                # Continue with other shutdown handlers even if one fails

        logger.info("All shutdown handlers executed")
