import asyncio
import asyncio.events
import asyncio.exceptions
import concurrent.futures
import functools
import time
from collections.abc import Callable, Coroutine
from contextlib import ExitStack, suppress
from datetime import UTC, datetime
from typing import Any, cast

import structlog

from langgraph_api import config
from langgraph_api import store as api_store
from langgraph_api.drain import (
    SERVER_SHUTDOWN_DRAIN_REASON,
    RunControlRegistry,
)
from langgraph_api.grpc.client import close_shared_client
from langgraph_api.grpc.ops import Runs, Threads
from langgraph_api.metrics_otlp import (
    COUNTER_FAILED_TO_FETCH_RUNS,
    COUNTER_RUN_ABANDONED_BY_SHUTDOWN,
    LATENCY_RUN_QUEUE_WAIT_TIME_1ST_ATTEMPT,
    LATENCY_RUN_QUEUE_WAIT_TIME_RETRY_ATTEMPT,
    get_otlp_metrics_reporter,
)
from langgraph_api.utils import future as lg_future
from langgraph_runtime.database import stop_pool

logger = structlog.stdlib.get_logger(__name__)

WORKERS: set[lg_future.AnyFuture] = set()
# Drain controls of in-flight checkpointed runs, drained at shutdown.
RUN_CONTROLS = RunControlRegistry()
WEBHOOKS: set[concurrent.futures.Future] = set()
SHUTDOWN_GRACE_PERIOD_SECS = 5


def get_num_workers():
    return len(WORKERS)


class BgLoopRunner(asyncio.Runner):  # type: ignore[subclass-of-final-class]
    """
    A runner that runs a loop in a separate thread. It's very important to
    use run the loop always in the same thread, as some objects may be created
    which are bound to the loop's thread.
    """

    executor: concurrent.futures.ThreadPoolExecutor

    def __init__(self, idx: int):
        super().__init__()
        self.idx = idx

    def __enter__(self):
        self.executor = concurrent.futures.ThreadPoolExecutor(
            1, thread_name_prefix=f"bg-loop-{self.idx}"
        )
        self.executor.submit(self.get_loop).result()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        loop = self.get_loop()
        # cancel all remaining tasks
        for task in asyncio.all_tasks(loop):
            task.cancel("Stopping background loop")
        # close postgres connection pool
        try:
            if not loop.is_running():
                self.executor.submit(self.run, stop_pool()).result(
                    SHUTDOWN_GRACE_PERIOD_SECS / 2
                )
            else:
                asyncio.run_coroutine_threadsafe(stop_pool(), loop).result(
                    SHUTDOWN_GRACE_PERIOD_SECS / 2
                )
        except TimeoutError:
            pass
        try:
            if not loop.is_running():
                self.executor.submit(self.run, api_store.exit_store()).result(
                    SHUTDOWN_GRACE_PERIOD_SECS / 2
                )
            else:
                asyncio.run_coroutine_threadsafe(api_store.exit_store(), loop).result(
                    SHUTDOWN_GRACE_PERIOD_SECS / 2
                )
        except TimeoutError:
            pass
        try:
            if not loop.is_running():
                self.executor.submit(self.run, close_shared_client()).result(
                    SHUTDOWN_GRACE_PERIOD_SECS / 2
                )
            else:
                asyncio.run_coroutine_threadsafe(close_shared_client(), loop).result(
                    SHUTDOWN_GRACE_PERIOD_SECS / 2
                )
        except TimeoutError:
            pass
        self.executor.shutdown(wait=False)

    def submit(
        self,
        coro: Coroutine,
        *,
        name: str | None = None,
        callback: Callable[[lg_future.AnyFuture], None] | None = None,
    ):
        fut = self.executor.submit(
            self.run,
            coro,
            name=name,
        )
        WORKERS.add(fut)
        if callback:
            fut.add_done_callback(callback)
        return fut

    def run(
        self,
        coro: Coroutine,
        *,
        name: str | None = None,
    ):
        """Run a coroutine inside the embedded event loop.
        Modified from asyncio.Runner.run
        - Removed main thread check (we only use it on bg threads)
        - Added callback and name arguments
        - Added WORKERS set to track tasks
        """

        if asyncio.events._get_running_loop() is not None:
            # fail fast with short traceback
            raise RuntimeError(
                "Runner.run() cannot be called from a running event loop"
            )

        self._lazy_init()

        task = self._loop.create_task(coro, name=name)

        try:
            return self._loop.run_until_complete(task)
        except asyncio.exceptions.CancelledError:
            raise  # CancelledError


async def shutdown_queue(
    loop: asyncio.AbstractEventLoop,
    timeout: float,
    futs: list[asyncio.Future] | None = None,
):
    # run all pending workers and webhooks in a timeout
    if not futs:
        futs = []

    # when BG_JOB_ISOLATED_LOOPS is enabled, WORKERS will contain concurrent.futures.Future objects instead of asyncio.Future objects
    # in order to correctly asyncio.gather this future, we call chain_future to convert this into an asyncio.Future
    if config.BG_JOB_ISOLATED_LOOPS:
        futs.extend(
            [
                cast(
                    "asyncio.Future",
                    lg_future.chain_future(f, loop.create_future()),
                )
                for f in WORKERS
            ],
        )
    else:
        futs.extend([cast("asyncio.Future", f) for f in WORKERS])

    futs.extend(
        [
            cast("asyncio.Future", lg_future.chain_future(w, loop.create_future()))
            for w in WEBHOOKS
        ]
    )

    await asyncio.wait_for(
        asyncio.gather(
            *futs,
            return_exceptions=True,
        ),
        timeout,
    )


async def queue():
    # Avoid impact of cyclic imports
    from langgraph_api import graph, webhook, worker  # noqa: PLC0415
    from langgraph_api.asyncio import AsyncQueue  # noqa: PLC0415
    from langgraph_api.schema import Run  # noqa: PLC0415
    from langgraph_api.worker_runtime import DRAIN_POLICY  # noqa: PLC0415

    concurrency = config.N_JOBS_PER_WORKER
    reporter = get_otlp_metrics_reporter()
    loop = asyncio.get_running_loop()
    # when not using isolated event loops the queue is used to limit concurrency
    # where every task checks out a token before running, and returns it when done
    runners = AsyncQueue[BgLoopRunner](concurrency)
    with ExitStack() as stack:
        if config.BG_JOB_ISOLATED_LOOPS:
            await logger.ainfo("Starting queue with isolated loops")
            executor = stack.enter_context(concurrent.futures.ThreadPoolExecutor())
            RUNNERS = {
                stack.enter_context(BgLoopRunner(idx)) for idx in range(concurrency)
            }
            for r in RUNNERS:
                runners.put_nowait(r)
                r.get_loop().set_default_executor(executor)
        else:
            await logger.ainfo("Starting queue with shared loop")
            # when not using isolated event loops the queue items are used as
            # tokens to limit concurrency, so we just create empty objects
            for _ in range(concurrency):
                runners.put_nowait(cast("BgLoopRunner", object()))
        expired_runners = []

        async def get_graph_id(run: Run) -> str | None:
            try:
                return run["kwargs"]["config"]["configurable"]["graph_id"]
            except Exception as exc1:
                await logger.aexception(
                    "Failed to get graph id from run",
                    run_id=run["run_id"],
                    exc_info=exc1,
                )
                try:
                    await Threads.set_joint_status(
                        None,
                        run["thread_id"],
                        run["run_id"],
                        "error",
                        "",
                        exception=RuntimeError("run is missing graph_id"),
                    )
                except Exception as exc2:
                    await logger.aexception(
                        "Failed to set joint status to error",
                        run_id=run["run_id"],
                        exc_info=exc2,
                    )
                return None

        def release_runner(runner: BgLoopRunner):
            try:
                if config.BG_JOB_ISOLATED_LOOPS:
                    loop.call_soon_threadsafe(runners.put_nowait, runner)
                else:
                    # We don't use isolated loops, so we can just put the runner back in the queue
                    runners.put_nowait(runner)
            except Exception as exc:
                expired_runners.append(runner)
                logger.exception("Background worker cleanup failed", exc_info=exc)

        def cleanup(
            task: lg_future.AnyFuture,
            runner: BgLoopRunner,
            run_id: Any,
            control: Any | None,
        ):
            WORKERS.discard(task)
            RUN_CONTROLS.release(run_id, control)
            release_runner(runner)

            try:
                if task.cancelled():
                    return
                if exc := task.exception():
                    if not isinstance(exc, asyncio.CancelledError):
                        logger.exception(
                            f"Background worker failed for task {task}",
                            exc_info=exc,
                        )
                    return
                result: worker.WorkerResult | None = task.result()
                if result and result["webhook"]:
                    hook_fut = asyncio.run_coroutine_threadsafe(
                        webhook.call_webhook(result), loop
                    )
                    WEBHOOKS.add(hook_fut)
                    hook_fut.add_done_callback(WEBHOOKS.remove)
            except Exception as exc:
                logger.exception("Background worker cleanup failed", exc_info=exc)

        await logger.ainfo(f"Starting {concurrency} background workers")

        try:
            while True:
                if expired_runners:
                    # Should never happen.
                    await logger.awarning(
                        "Background worker expired, adding to queue",
                        num=len(expired_runners),
                    )
                    for runner in expired_runners:
                        await runners.put(runner)
                    expired_runners.clear()
                await runners.wait()
                runner: BgLoopRunner | None = None
                try:
                    # try to get a run, handle it
                    run: Run | None = None
                    async for run, attempt, drains, encryption_context in Runs.next(
                        wait=True, limit=runners.qsize()
                    ):
                        wait_ms = int(
                            (datetime.now(UTC) - run["created_at"]).total_seconds()
                            * 1000
                        )
                        await logger.ainfo(
                            "Dequeued run for background worker",
                            run_id=str(run["run_id"]),
                            thread_id=str(run["thread_id"]),
                            attempt=attempt,
                            run_queue_wait_ms=wait_ms,
                        )
                        # Labelled by level only on a deployment with a priority
                        # callback, so one without keeps its series as they were.
                        wait_attributes = (
                            {"priority": str(run["priority"])}
                            if config.PRIORITY_CALLBACK_CONFIGURED
                            else None
                        )
                        if attempt == 1:
                            reporter.record_latency(
                                LATENCY_RUN_QUEUE_WAIT_TIME_1ST_ATTEMPT,
                                float(wait_ms) / 1000.0,
                                wait_attributes,
                            )
                        else:
                            reporter.record_latency(
                                LATENCY_RUN_QUEUE_WAIT_TIME_RETRY_ATTEMPT,
                                float(wait_ms) / 1000.0,
                                wait_attributes,
                            )
                        # we know a runner exists, so get it
                        runner = runners.get_nowait()

                        graph_id = await get_graph_id(run)
                        if graph_id is None:
                            release_runner(runner)
                            runner = None
                            continue

                        # Every run gets a control when drained-run handling
                        # is on, so drains requested by graph code stop only
                        # at a top-level step boundary.
                        control = DRAIN_POLICY.new_control()
                        # This queue drains its runs when the server shuts
                        # down, except temporary runs, which have no
                        # checkpoint to resume from, and JS graphs (which
                        # aren't drained yet). Those keep the grace-period
                        # wait.
                        if (
                            control is not None
                            and not run["kwargs"].get("temporary", False)
                            and not graph.is_js_graph(graph_id)
                        ):
                            RUN_CONTROLS.add(run["run_id"], control)
                        on_done = functools.partial(
                            cleanup,
                            runner=runner,
                            run_id=run["run_id"],
                            control=control,
                        )
                        try:
                            if not config.BG_JOB_ISOLATED_LOOPS or (
                                graph_id and graph.is_js_graph(graph_id)
                            ):
                                task = asyncio.create_task(
                                    worker.worker(
                                        run,
                                        attempt,
                                        loop,
                                        encryption_context=encryption_context,
                                        drains=drains,
                                        control=control,
                                    ),
                                    name=f"run-{run['run_id']}-attempt-{attempt}",
                                )
                                task.add_done_callback(on_done)
                                runner = None
                                WORKERS.add(task)
                            else:
                                runner.submit(
                                    worker.worker(
                                        run,
                                        attempt,
                                        loop,
                                        encryption_context=encryption_context,
                                        drains=drains,
                                        control=control,
                                    ),
                                    name=f"run-{run['run_id']}-attempt-{attempt}",
                                    callback=on_done,
                                )
                                runner = None
                        except Exception:
                            # The run never started, so nothing will release it.
                            RUN_CONTROLS.release(run["run_id"], control)
                            raise
                except Exception as exc:
                    # keep trying to run the scheduler indefinitely
                    reporter.inc_counter(COUNTER_FAILED_TO_FETCH_RUNS)
                    logger.exception("Background worker scheduler failed", exc_info=exc)

                    # Release the runner back to the queue
                    if runner is not None:
                        release_runner(runner)

        except asyncio.CancelledError as e:
            # If k8s signals a sigterm, the queue task gets cancelled.
            # wait up to BG_JOB_SHUTDOWN_GRACE_PERIOD_SECS for workers to finish
            log_kwargs = {}
            if e.args:
                log_kwargs["reason"] = " ".join(map(str, e.args))
            await logger.awarning(
                "Queue task cancelled. Shutting down workers. "
                f"Will terminate after {config.BG_JOB_SHUTDOWN_GRACE_PERIOD_SECS}s",
                **log_kwargs,
            )
            reporter.inc_counter(COUNTER_RUN_ABANDONED_BY_SHUTDOWN, value=len(WORKERS))
            # The claim loop is already cancelled, so a drained run can only be
            # picked up by another pod. Ask in-flight runs to stop at their
            # next superstep boundary; a run still in a node when the grace
            # period ends is cancelled, its current step redone elsewhere.
            # Nothing is registered with drained-run handling off.
            if drained := RUN_CONTROLS.drain_all(SERVER_SHUTDOWN_DRAIN_REASON):
                await logger.ainfo(
                    "Requested cooperative drain of registered in-flight runs",
                    num=drained,
                )
            start = time.perf_counter()
            await shutdown_queue(loop, config.BG_JOB_SHUTDOWN_GRACE_PERIOD_SECS)
            elapsed = time.perf_counter() - start
            await logger.ainfo("Workers finished.")
        finally:
            remaining_shutdown_time = 0
            with suppress(UnboundLocalError):
                remaining_shutdown_time = (
                    config.BG_JOB_SHUTDOWN_GRACE_PERIOD_SECS - elapsed
                )

            # we may have additional webhook tasks created after runs finish in the previous except block, so we repeat shutdown
            await shutdown_queue(
                loop,
                max(
                    remaining_shutdown_time,
                    SHUTDOWN_GRACE_PERIOD_SECS,
                ),
            )
            await logger.ainfo("Successfully shutdown queue")
