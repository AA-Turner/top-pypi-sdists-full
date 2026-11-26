import asyncio
import os
import sys
import threading
from contextlib import asynccontextmanager

import structlog
from langchain_core.runnables.config import RunnableConfig, var_child_runnable_config
from langgraph.constants import CONF
from starlette.applications import Starlette

from langgraph_api import config, embedded_core
from langgraph_api.config import BG_JOB_SHUTDOWN_GRACE_PERIOD_SECS
from langgraph_api.feature_flags import INMEM_USES_CORE
from langgraph_api.runtime import queue
from langgraph_license.validation import (
    check_license_periodically,
    get_license_status,
)
from langgraph_runtime import checkpoint, database

logger = structlog.stdlib.get_logger(__name__)
# Tracks the most recent uncaught startup failure so callers can report it.
_LAST_LIFESPAN_ERROR: BaseException | None = None


def get_last_error() -> BaseException | None:
    return _LAST_LIFESPAN_ERROR


@asynccontextmanager
async def lifespan(
    app: Starlette | None = None,
    *,
    cancel_event: asyncio.Event | None = None,
    with_cron_scheduler: bool = True,
    taskset: set[asyncio.Task] | None = None,
):
    async with (
        _embedded_core(),
        _lifespan(
            app,
            cancel_event=cancel_event,
            with_cron_scheduler=with_cron_scheduler,
            taskset=taskset,
        ),
    ):
        yield


@asynccontextmanager
async def _embedded_core():
    """Run Go core as a child process for the in-memory runtime.

    LSD_GRPC_SERVER_ADDRESS is ignored: the in-memory runtime only talks to its
    own SQLite core, never to an external one.
    """
    if not INMEM_USES_CORE:
        yield
        return
    if os.environ.get("LSD_GRPC_SERVER_ADDRESS"):
        logger.warning(
            "Ignoring LSD_GRPC_SERVER_ADDRESS: the in-memory runtime runs its own core"
        )
    if address := os.environ.get(embedded_core.ADDRESS_ENV):
        config.LSD_GRPC_SERVER_ADDRESS = address
        yield
        return

    persist = os.getenv("LANGGRAPH_DISABLE_FILE_PERSISTENCE", "false").lower() != "true"
    core = embedded_core.start(embedded_core.SQLITE_PATH if persist else None)
    config.LSD_GRPC_SERVER_ADDRESS = await asyncio.to_thread(core.__enter__)
    try:
        yield
    finally:
        await asyncio.to_thread(core.__exit__, None, None, None)


@asynccontextmanager
async def _lifespan(
    app: Starlette | None,
    *,
    cancel_event: asyncio.Event | None,
    with_cron_scheduler: bool,
    taskset: set[asyncio.Task] | None,
):
    # Import at point of use to avoid circular dependencies
    from langgraph_api import (  # noqa: PLC0415
        __version__,
        config,
        cron_scheduler,
        feature_flags,
        graph,
        http,
        metadata,
        priority_settings,
        web_identity,
    )
    from langgraph_api import (  # noqa: PLC0415
        _checkpointer as api_checkpointer,
    )
    from langgraph_api import asyncio as langgraph_asyncio  # noqa: PLC0415
    from langgraph_api import (  # noqa: PLC0415
        store as api_store,
    )
    from langgraph_api.js import ui  # noqa: PLC0415

    global _LAST_LIFESPAN_ERROR
    _LAST_LIFESPAN_ERROR = None

    await logger.ainfo(
        f"Starting LangGraph runtime with langgraph-api={__version__}",
        version=__version__,
    )

    try:
        current_loop = asyncio.get_running_loop()
        langgraph_asyncio.set_event_loop(current_loop)
    except RuntimeError:
        await logger.aerror("Failed to set loop")

    # Before the store, checkpointer and graphs, any of which may build cloud clients.
    web_identity_refreshes = await web_identity.start()

    # Need access to redis client in get_license_status
    await database.start_pool()
    await api_checkpointer.start_checkpointer()
    await checkpoint.start_checkpoint_ingestion_loop()

    if not await get_license_status():
        raise ValueError(
            "License verification failed. Please ensure proper configuration:\n"
            "- For local development, set a valid LANGSMITH_API_KEY for an account with LangGraph Cloud access "
            "in the environment defined in your langgraph.json file.\n"
            "- For production, configure the LANGGRAPH_CLOUD_LICENSE_KEY environment variable "
            "with your LangGraph Cloud license key.\n"
            "Review your configuration settings and try again. If issues persist, "
            "contact support for assistance."
        )

    # needs to be initialized after get_license_status to get CUSTOMER_ID and CUSTOMER_NAME
    if config.LANGGRAPH_LOGS_ENABLED:
        from langgraph_api import self_hosted_logs  # noqa: PLC0415

        self_hosted_logs.initialize_self_hosted_logs()

    await http.start_http_client()
    await ui.start_ui_bundler()

    # Start Python gRPC server if custom encryption or checkpointer is configured
    # This exposes Python implementations to the Go server
    grpc_waits = []
    if config.PYTHON_GRPC_SERVER_ENABLED:
        from langgraph_api.grpc.server import (  # noqa: PLC0415
            run_python_grpc_server,
            wait_until_python_grpc_ready,
        )

        langgraph_asyncio.create_task(
            run_python_grpc_server(port=config.PYTHON_GRPC_SERVER_PORT)
        )
        grpc_waits.append(wait_until_python_grpc_ready())

    # Connect to shared gRPC client--this warms the pool of
    # connections and verifies initial connectivity. Wait for the server to be
    # ready with retries since the gRPC server may start concurrently.
    # On postgres backend, we always use gRPC for assistants.
    from langgraph_api.grpc.client import wait_until_grpc_ready  # noqa: PLC0415

    grpc_waits.append(wait_until_grpc_ready())
    await asyncio.gather(*grpc_waits)

    # needs to be initialized after get_license_status to get CUSTOMER_ID and CUSTOMER_NAME
    if config.LANGGRAPH_METRICS_ENABLED:
        from langgraph_api import self_hosted_metrics  # noqa: PLC0415

        self_hosted_metrics.initialize_self_hosted_metrics()
    # OTLP metrics are always exported (Prometheus via /metrics; Datadog when a
    # DD API key is set). The reporter no-ops if OTel deps are unavailable.
    from langgraph_api.metrics_otlp import (  # noqa: PLC0415
        COUNTER_SERVER_STARTED,
        get_otlp_metrics_reporter,
    )

    reporter = get_otlp_metrics_reporter()
    reporter.initialize()
    reporter.inc_counter(COUNTER_SERVER_STARTED)

    async def _log_graph_load_failure(err: graph.GraphLoadError) -> None:
        cause = err.__cause__ or err.cause
        log_fields = err.log_fields()
        log_fields["action"] = "fix_user_graph"
        await logger.aerror(
            f"Graph '{err.spec.id}' failed to load: {err.cause_message}",
            **log_fields,
        )
        await logger.adebug(
            "Full graph load failure traceback (internal)",
            **{k: v for k, v in log_fields.items() if k != "user_traceback"},
            exc_info=cause,
        )

    try:
        async with langgraph_asyncio.SimpleTaskGroup(
            cancel=True, cancel_event=cancel_event, taskgroup_name="Lifespan"
        ) as tg:
            tg.create_task(metadata.metadata_loop())
            # The collector runs in EVERY process (both the API server and the
            # dedicated queue worker share this lifespan).
            from langgraph_api.metrics_collector import (  # noqa: PLC0415
                collector_loop,
            )

            tg.create_task(collector_loop())
            tg.create_task(check_license_periodically())
            await api_store.collect_store_from_env()
            store_instance = await api_store.get_store()
            if api_store.CUSTOM_STORE:
                await logger.ainfo("Using custom store.")
            else:
                await logger.ainfo("Using default store backend.")

            if feature_flags.USE_RUNTIME_CONTEXT_API:
                from langgraph._internal._constants import (  # noqa: PLC0415
                    CONFIG_KEY_RUNTIME,
                )
                from langgraph.runtime import Runtime  # noqa: PLC0415

                langgraph_config: RunnableConfig = {
                    CONF: {CONFIG_KEY_RUNTIME: Runtime(store=store_instance)}
                }
            else:
                from langgraph.constants import CONFIG_KEY_STORE  # noqa: PLC0415

                langgraph_config = {CONF: {CONFIG_KEY_STORE: store_instance}}

            var_child_runnable_config.set(langgraph_config)

            # Keep after the setter above so users can access the store from within the factory function
            graph.patch_packages_distributions()
            try:
                await graph.collect_graphs_from_env(True)
            except graph.GraphLoadError as exc:
                _LAST_LIFESPAN_ERROR = exc
                await _log_graph_load_failure(exc)
                raise
            # Loaded now so a bad path fails startup, not every run create.
            if (
                priority_settings.get_priority_callback() is not None
                and feature_flags.IS_INMEM_BACKEND
            ):
                await logger.awarning(
                    "The in-memory runtime stores each thread's priority settings"
                    " but starts runs in the order they were created"
                )
            if (
                config.N_JOBS_PER_WORKER > 0
                and config.DISPATCH_MODE != config.DispatchMode.MULTI_PROCESS
            ):
                tg.create_task(queue_with_signal())
            elif config.DISPATCH_MODE == config.DispatchMode.MULTI_PROCESS:
                await logger.ainfo(
                    "DISPATCH_MODE=multi-process; Go worker manager handles run dispatch"
                )
            else:
                await logger.ainfo("N_JOBS_PER_WORKER is 0. Skipping queue.")

            if with_cron_scheduler:
                tg.create_task(cron_scheduler.cron_scheduler())
            yield
    except graph.GraphLoadError as exc:
        _LAST_LIFESPAN_ERROR = exc
        raise
    except asyncio.CancelledError:
        pass
    except Exception as exc:
        _LAST_LIFESPAN_ERROR = exc
        logger.exception("Lifespan failed", exc_info=True)
    finally:
        for refresh in web_identity_refreshes:
            refresh.cancel()
        if web_identity_refreshes:
            await asyncio.wait(web_identity_refreshes)
        from langgraph_api.metrics_otlp import (  # noqa: PLC0415
            COUNTER_SERVER_REQUESTED_TO_STOP,
            get_otlp_metrics_reporter,
        )

        # Shutdown has been requested; teardown is starting.
        otlp_reporter = get_otlp_metrics_reporter()
        otlp_reporter.inc_counter(COUNTER_SERVER_REQUESTED_TO_STOP)

        await api_checkpointer.exit_checkpointer()
        await api_store.exit_store()
        await ui.stop_ui_bundler()
        if config.LANGGRAPH_METRICS_ENABLED:
            from langgraph_api import self_hosted_metrics  # noqa: PLC0415

            self_hosted_metrics.shutdown_self_hosted_metrics()

        await graph.stop_remote_graphs()
        await http.stop_http_client()
        await http.stop_webhook_http_client()

        # Close shared gRPC client (always used for assistants on postgres backend)
        from langgraph_api.grpc.client import close_shared_client  # noqa: PLC0415

        await close_shared_client()

        await checkpoint.stop_checkpoint_ingestion_loop()
        await database.stop_pool()

        # Stop Python gRPC server if it was started
        if config.PYTHON_GRPC_SERVER_ENABLED:
            from langgraph_api.grpc.server import (  # noqa: PLC0415
                stop_python_grpc_server,
            )

            await stop_python_grpc_server()

        if config.LANGGRAPH_LOGS_ENABLED:
            from langgraph_api import self_hosted_logs  # noqa: PLC0415

            self_hosted_logs.shutdown_self_hosted_logs()

        if otlp_reporter is not None:
            from langgraph_api.metrics_otlp import (  # noqa: PLC0415
                COUNTER_SERVER_STOPPED,
            )

            # Teardown completed successfully. Emit before shutting down the
            # reporter so the final OTLP export includes this counter.
            otlp_reporter.inc_counter(COUNTER_SERVER_STOPPED)
            otlp_reporter.shutdown()


async def queue_with_signal():
    try:
        await queue.queue()
    except asyncio.CancelledError:
        pass
    except TimeoutError as e:
        await logger.aerror(
            f"The queue surpassed the grace period while shutting down. Some runs may still be running and will be canceled and retried on a healthy instance. The grace period is currently set to {BG_JOB_SHUTDOWN_GRACE_PERIOD_SECS} seconds. If that is too low, adjust the BG_JOB_SHUTDOWN_GRACE_PERIOD_SECS environment variable to an appropriate value. Signaling shutdown",
            exc_info=e,
            BG_JOB_SHUTDOWN_GRACE_PERIOD_SECS=BG_JOB_SHUTDOWN_GRACE_PERIOD_SECS,
        )
        _exit_after_flush()
    except Exception as exc:
        await logger.aexception("Queue failed. Signaling shutdown", exc_info=exc)
        _exit_after_flush()


def _exit_after_flush(timeout: float = 5.0) -> None:
    """Trigger Python's normal shutdown sequence, then hard-exit if needed.

    sys.exit(1) raises SystemExit which lets asyncio clean up, runs atexit
    handlers (ddtrace and LangSmith background flush threads), and joins
    non-daemon threads — including stuck BgLoopRunner workers when
    BG_JOB_ISOLATED_LOOPS is enabled.

    The daemon timer ensures os._exit fires after `timeout` seconds if any
    thread blocks exit (e.g. a BgLoopRunner worker stuck on an in-flight
    request). If the process exits cleanly before the timer fires, the daemon
    timer is discarded harmlessly.
    """

    def _hard_exit() -> None:
        # Use stderr directly and flush explicitly — structlog is async and
        # os._exit() bypasses all Python I/O buffering, so we must flush
        # before calling it.
        sys.stderr.write(
            "Queue shutdown timer expired: threads did not exit within "
            f"{timeout}s grace period. Force-exiting via os._exit.\n"
        )
        sys.stderr.flush()
        os._exit(1)

    t = threading.Timer(timeout, _hard_exit)
    t.daemon = True
    t.start()
    sys.exit(1)


lifespan.get_last_error = get_last_error
