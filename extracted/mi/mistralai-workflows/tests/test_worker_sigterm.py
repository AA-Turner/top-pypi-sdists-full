import asyncio
import multiprocessing
import multiprocessing.synchronize
import os
import signal
import sys
import time
import uuid
from contextlib import ExitStack, asynccontextmanager
from datetime import timedelta
from typing import AsyncIterator, Callable, Iterator
from unittest.mock import AsyncMock, Mock, patch

import pytest
from temporalio import activity, workflow
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import UnsandboxedWorkflowRunner, Worker

from mistralai.workflows.core.config.config import AppConfig, WorkerConfig
from mistralai.workflows.core.utils.health_server import HealthServer
from mistralai.workflows.core.worker import (
    _create_temporal_workers,
    _on_sigterm,
    _sigterm_requests_stop,
    _stop_workers_when_requested,
    run_worker,
)
from mistralai.workflows.protocol.v1.workflow import WorkflowSpecsRegisterResponse

# Windows delivers no SIGTERM to Python: os.kill(pid, SIGTERM) terminates the process there.
pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="SIGTERM is not a signal on Windows")


@pytest.fixture
async def workers(temporal_env: WorkflowEnvironment) -> AsyncIterator[list[Worker]]:
    # Other test modules leave activities with clashing names in the process-wide registry.
    with (
        patch("mistralai.workflows.core.worker.get_all_temporal_activities", return_value=[]),
        ExitStack() as registrations,
    ):
        created, _ = _create_temporal_workers(
            temporal_client=temporal_env.client,
            workflows=[],
            config=AppConfig(worker=WorkerConfig(local_retry_backoff_coefficient=0)),
            task_queue=f"sigterm-{uuid.uuid4()}",
            workflow_config_registrations=registrations,
        )
        yield created


@pytest.fixture
def default_sigterm() -> Iterator[None]:
    # Test plugins such as ddtrace's install their own SIGTERM handler; a bare worker process has none.
    previous = signal.signal(signal.SIGTERM, signal.SIG_DFL)
    yield
    signal.signal(signal.SIGTERM, previous)


@pytest.mark.usefixtures("default_sigterm")
class TestStopOnSigterm:
    async def test_sigterm_stops_workers_and_health_server(self, workers: list[Worker]) -> None:
        health_server = HealthServer("127.0.0.1", 0)
        # os.kill below would end pytest if the worker did not take SIGTERM.
        assert signal.getsignal(signal.SIGTERM) is signal.SIG_DFL
        run = asyncio.gather(health_server.run(), *[worker.run() for worker in workers])
        try:
            with _sigterm_requests_stop(enabled=True) as stop_requested:
                async with _stop_workers_when_requested(stop_requested, workers, health_server):
                    assert signal.getsignal(signal.SIGTERM) is not signal.SIG_DFL
                    os.kill(os.getpid(), signal.SIGTERM)
                    await asyncio.sleep(0.1)
                    # A second SIGTERM before run_worker returns must not end the process or the drain.
                    os.kill(os.getpid(), signal.SIGTERM)
                    await asyncio.wait_for(asyncio.shield(run), timeout=10)
        finally:
            # Like run_worker's cleanup, stop everything a second time.
            await asyncio.gather(*[worker.shutdown() for worker in workers])
            await asyncio.wait_for(asyncio.get_running_loop().run_in_executor(None, health_server.shutdown), timeout=5)
            await run

        assert all(worker.is_shutdown for worker in workers)
        assert signal.getsignal(signal.SIGTERM) is signal.SIG_DFL

    async def test_caller_keeps_its_sigterm_handler(self, workers: list[Worker]) -> None:
        loop = asyncio.get_running_loop()
        received = asyncio.Queue[None]()

        def caller_handler() -> None:
            received.put_nowait(None)
            for worker in workers:
                loop.create_task(worker.shutdown())

        loop.add_signal_handler(signal.SIGTERM, caller_handler)
        try:
            with _sigterm_requests_stop(enabled=True) as stop_requested:
                async with _stop_workers_when_requested(stop_requested, workers, None):
                    run = asyncio.gather(*[worker.run() for worker in workers])
                    os.kill(os.getpid(), signal.SIGTERM)
                    await asyncio.wait_for(run, timeout=10)
            await asyncio.wait_for(received.get(), timeout=5)

            assert signal.getsignal(signal.SIGTERM) is not signal.SIG_DFL
            os.kill(os.getpid(), signal.SIGTERM)
            await asyncio.wait_for(received.get(), timeout=5)
        finally:
            loop.remove_signal_handler(signal.SIGTERM)


def _signal_ready_then_sleep(ready: multiprocessing.synchronize.Event) -> None:
    ready.set()
    time.sleep(60)


@pytest.mark.usefixtures("default_sigterm")
class TestRunWorkerSigtermOwnership:
    @pytest.mark.parametrize("detach", [False, True])
    async def test_only_attached_worker_takes_sigterm(self, detach: bool) -> None:
        cfg = AppConfig(worker=WorkerConfig(deployment_name="test"))
        installed = []

        async def record_handler(*_args: object, **_kwargs: object) -> None:
            installed.append(signal.getsignal(signal.SIGTERM) is not signal.SIG_DFL)

        with patch("mistralai.workflows.core.worker._run_worker", side_effect=record_handler) as worker:
            task = await run_worker([], detach=detach, enable_config_discovery=False, config=cfg)
            if task is not None:
                await task

        assert (worker.call_args.kwargs.get("stop_requested") is not None) is not detach
        assert installed == [not detach]

    @pytest.mark.skipif("fork" not in multiprocessing.get_all_start_methods(), reason="needs fork")
    async def test_forked_child_dies_on_sigterm(self) -> None:
        # A child forked while the worker owns SIGTERM, e.g. by multiprocessing, must not inherit the handler, or
        # Pool.terminate() hangs.
        context = multiprocessing.get_context("fork")
        ready = context.Event()
        with _sigterm_requests_stop(enabled=True):
            child = context.Process(target=_signal_ready_then_sleep, args=(ready,))
            child.start()
        try:
            assert ready.wait(timeout=5)
            child.terminate()
            child.join(timeout=5)
            assert child.exitcode == -signal.SIGTERM
        finally:
            child.kill()
            child.join()

    @pytest.mark.parametrize("lands_before", ["install_returns", "restore"])
    async def test_sigterm_next_to_install_or_restore_still_requests_stop(self, lands_before: str) -> None:
        set_signal = signal.signal

        def set_signal_with_sigterm_landing(signum: int, handler: object) -> object:
            # A SIGTERM lands right after the worker's handler is installed, or right before it is removed.
            if lands_before == "restore" and handler is signal.SIG_DFL:
                _on_sigterm(signum, None)
            previous = set_signal(signum, handler)  # type: ignore[arg-type]
            if lands_before == "install_returns" and handler is _on_sigterm:
                _on_sigterm(signum, None)
            return previous

        with patch.object(signal, "signal", set_signal_with_sigterm_landing):
            with _sigterm_requests_stop(enabled=True) as stop_requested:
                pass
        await asyncio.sleep(0)

        assert stop_requested is not None
        assert stop_requested.is_set()

    async def test_fallback_keeps_no_context_from_the_refused_handler(self) -> None:
        # An embedded interpreter can refuse signal handlers. The worker's own errors must not chain to that refusal.
        with patch.object(signal, "signal", side_effect=ValueError), pytest.raises(RuntimeError) as raised:
            with _sigterm_requests_stop(enabled=True):
                raise RuntimeError("worker failed")

        assert raised.value.__context__ is None


@workflow.defn(name="sigterm-test-workflow")
class BlockingWorkflow:
    @workflow.run
    async def run(self) -> None:
        await workflow.execute_activity("sigterm-test-activity", start_to_close_timeout=timedelta(minutes=1))


# Runs until the worker shuts down, then until the test releases it.
class BlockingActivity:
    def __init__(self) -> None:
        self.started = asyncio.Event()
        self.draining = asyncio.Event()
        self.release = asyncio.Event()

    @activity.defn(name="sigterm-test-activity")
    async def run(self) -> None:
        self.started.set()
        await activity.wait_for_worker_shutdown()
        self.draining.set()
        await self.release.wait()


async def _send_sigterm_once_polling(runs: list[asyncio.Task[asyncio.Task | None]], workers: list[Worker]) -> None:
    async def until_polling() -> None:
        while not all(worker.is_running for worker in workers):
            for run in runs:
                if run.done():
                    run.result()
            await asyncio.sleep(0.01)

    await asyncio.wait_for(until_polling(), timeout=10)
    # os.kill below would end pytest if the worker did not take SIGTERM.
    assert signal.getsignal(signal.SIGTERM) is not signal.SIG_DFL
    os.kill(os.getpid(), signal.SIGTERM)


@asynccontextmanager
async def _run_worker_against(
    temporal_env: WorkflowEnvironment,
    workers: list[Worker],
    config: AppConfig,
    *,
    on_register: Callable[[], None] = lambda: None,
) -> AsyncIterator[list[asyncio.Task[asyncio.Task | None]]]:
    # Runs one attached run_worker per Temporal worker; only the Workflows API calls are faked.
    async def wait_forever(*_args: object, **_kwargs: object) -> None:
        await asyncio.Event().wait()

    def register(*_args: object, **_kwargs: object) -> WorkflowSpecsRegisterResponse:
        on_register()
        return WorkflowSpecsRegisterResponse(has_conflicts=False)

    with (
        patch("mistralai.workflows.core.worker.create_temporal_client", AsyncMock(return_value=temporal_env.client)),
        patch(
            "mistralai.workflows.core.worker._create_temporal_workers",
            Mock(side_effect=[([worker], []) for worker in workers]),
        ),
        patch("mistralai.workflows.core.worker._register_workflow_specs", AsyncMock(side_effect=register)),
        patch("mistralai.workflows.core.worker.build_worker_registrations", Mock(return_value={})),
        patch("mistralai.workflows.core.worker._worker_heartbeat", wait_forever),
        patch("mistralai.workflows.core.worker.refresh_temporal_credentials", wait_forever),
    ):
        runs = [
            asyncio.create_task(run_worker([], enable_config_discovery=False, config=config.model_copy(deep=True)))
            for _ in workers
        ]
        try:
            yield runs
        finally:
            # A failed test must not leave the worker polling into the next fixtures.
            for run in runs:
                run.cancel()
            await asyncio.wait(runs, timeout=10)


@pytest.mark.usefixtures("default_sigterm")
@pytest.mark.timeout(60)
class TestRunWorkerOnSigterm:
    @pytest.fixture
    def task_queue(self) -> str:
        return f"sigterm-{uuid.uuid4()}"

    @pytest.fixture
    def blocking_activity(self) -> Iterator[BlockingActivity]:
        blocking = BlockingActivity()
        yield blocking
        blocking.release.set()

    @pytest.fixture
    def worker(self, temporal_env: WorkflowEnvironment, task_queue: str, blocking_activity: BlockingActivity) -> Worker:
        return Worker(
            temporal_env.client,
            task_queue=task_queue,
            workflows=[BlockingWorkflow],
            activities=[blocking_activity.run],
            workflow_runner=UnsandboxedWorkflowRunner(),
            graceful_shutdown_timeout=timedelta(seconds=5),
        )

    @pytest.fixture
    def config(self) -> AppConfig:
        return AppConfig(worker=WorkerConfig(deployment_name="sigterm-test"))

    async def test_sigterm_stops_the_worker_and_returns(
        self, temporal_env: WorkflowEnvironment, worker: Worker, config: AppConfig
    ) -> None:
        async with _run_worker_against(temporal_env, [worker], config) as runs:
            await _send_sigterm_once_polling(runs, [worker])

            assert await asyncio.wait_for(runs[0], timeout=10) is None

        assert worker.is_shutdown
        assert signal.getsignal(signal.SIGTERM) is signal.SIG_DFL

    async def test_one_sigterm_stops_every_run_worker_in_the_process(
        self, temporal_env: WorkflowEnvironment, worker: Worker, config: AppConfig
    ) -> None:
        other_worker = Worker(
            temporal_env.client,
            task_queue=f"sigterm-{uuid.uuid4()}",
            workflows=[BlockingWorkflow],
            workflow_runner=UnsandboxedWorkflowRunner(),
        )
        workers = [worker, other_worker]
        async with _run_worker_against(temporal_env, workers, config) as runs:
            await _send_sigterm_once_polling(runs, workers)

            assert await asyncio.wait_for(asyncio.gather(*runs), timeout=10) == [None, None]

        assert all(w.is_shutdown for w in workers)
        assert signal.getsignal(signal.SIGTERM) is signal.SIG_DFL

    async def test_sigterm_during_startup_skips_polling(
        self, temporal_env: WorkflowEnvironment, worker: Worker, config: AppConfig
    ) -> None:
        def sigterm_during_registration() -> None:
            # os.kill below would end pytest if the worker did not take SIGTERM yet.
            assert signal.getsignal(signal.SIGTERM) is not signal.SIG_DFL
            os.kill(os.getpid(), signal.SIGTERM)

        async with _run_worker_against(temporal_env, [worker], config, on_register=sigterm_during_registration) as runs:
            assert await asyncio.wait_for(runs[0], timeout=10) is None

        assert not worker.is_running
        assert not worker.is_shutdown
        assert signal.getsignal(signal.SIGTERM) is signal.SIG_DFL

    async def test_caller_handler_installed_while_running_survives_the_worker(
        self, temporal_env: WorkflowEnvironment, worker: Worker, config: AppConfig
    ) -> None:
        def caller_handler(_signum: int, _frame: object) -> None:
            pass

        async with _run_worker_against(temporal_env, [worker], config) as runs:
            while not worker.is_running:
                await asyncio.sleep(0.01)
            signal.signal(signal.SIGTERM, caller_handler)
            await worker.shutdown()

            assert await asyncio.wait_for(runs[0], timeout=10) is None

        assert signal.getsignal(signal.SIGTERM) is caller_handler

    async def test_cancel_during_the_drain_does_not_hang(
        self,
        temporal_env: WorkflowEnvironment,
        worker: Worker,
        config: AppConfig,
        task_queue: str,
        blocking_activity: BlockingActivity,
    ) -> None:
        async with _run_worker_against(temporal_env, [worker], config) as runs:
            run = runs[0]
            await temporal_env.client.start_workflow(BlockingWorkflow.run, id=str(uuid.uuid4()), task_queue=task_queue)
            await asyncio.wait_for(blocking_activity.started.wait(), timeout=10)
            await _send_sigterm_once_polling(runs, [worker])
            await asyncio.wait_for(blocking_activity.draining.wait(), timeout=10)

            # Like Ctrl+C, or a failed task cancelling its TaskGroup, while activities drain.
            run.cancel()
            # asyncio.wait, unlike wait_for, does not cancel the task again on timeout.
            await asyncio.wait({run}, timeout=10)

            assert run.cancelled()
        assert signal.getsignal(signal.SIGTERM) is signal.SIG_DFL
