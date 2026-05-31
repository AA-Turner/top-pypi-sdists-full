import os
import ssl
import subprocess
import sys
import threading
from typing import NamedTuple, Optional

import certifi
from dotenv import load_dotenv
from werkzeug.serving import make_server

from abstra_internals.cloud_api import connect_tunnel
from abstra_internals.controllers.codebase_events import CodebaseEventController
from abstra_internals.controllers.execution.consumer import ConsumerController
from abstra_internals.controllers.linter_events import LinterEventController
from abstra_internals.controllers.main import MainController
from abstra_internals.environment import (
    EDITOR_MODE,
    HOST,
    RABBITMQ_CONNECTION_URI,
    WORKER_LOG_TO_QUEUE,
    web_editor_uses_db,
)
from abstra_internals.interface.cli.messages import serve_message
from abstra_internals.logger import AbstraLogger
from abstra_internals.logs_watcher import LogsWatcher, on_logs_update
from abstra_internals.repositories.consumer import EditorConsumer
from abstra_internals.repositories.factory import (
    build_editor_repositories,
    build_web_editor_repositories,
    get_mp_context_repository,
)
from abstra_internals.repositories.producer import (
    LocalProducerRepository,
)
from abstra_internals.server.apps import get_local_app
from abstra_internals.services.file_watcher import FileWatcher
from abstra_internals.services.notifiers import (
    AbstraJsonChangeNotifier,
    RequirementsChangeNotifier,
)
from abstra_internals.services.web_editor_heartbeat import WebEditorHeartbeat
from abstra_internals.settings import Settings
from abstra_internals.signals import SignalHandlers
from abstra_internals.stdio_patcher import StdioPatcher
from abstra_internals.tasks_watcher import TasksWatcher
from abstra_internals.utils.browser import background_open_editor
from abstra_internals.utils.multiprocessing import safe_multiprocessing_queue
from abstra_internals.utils.stdio_broadcast import start_stdio_broadcast_consumer
from abstra_internals.version import check_latest_version


def start_consumer(controller: MainController, debug_mode: bool = False):
    if isinstance(controller.producer_repository, LocalProducerRepository):
        consumer = EditorConsumer(controller.producer_repository.queue)
        consumer_controller = ConsumerController(
            controller, consumer, debug_mode=debug_mode
        )

        th = threading.Thread(
            daemon=True,
            name="start_consumer::EditorConsumer",
            target=consumer_controller.start_loop,
        )

        th.start()
        return consumer, th, consumer_controller

    raise ValueError("Invalid producer repository")


def shutdown_editor_components(
    *,
    server,
    watchers,
    editor_consumer,
    consumer_controller,
    stdio_broadcast_stop_event,
    poller_stop_event=None,
    poller_thread=None,
    execution_logs=None,
    thread_factory=threading.Thread,
):
    """Stop every long-lived resource started by editor() and unblock
    serve_forever() by scheduling server.shutdown() on a background thread.

    Exposed at module level so it can be unit-tested without bootstrapping
    the full editor() function.
    """
    AbstraLogger.warning("[Editor] Graceful shutdown initiated")

    if poller_stop_event is not None:
        # DB path. Order matters: stop + join the poller (so it isn't mid-query),
        # then close the logs repo (drains + stops its flush thread + unregisters
        # its atexit so it can't resurrect the pool), and only THEN close the pool
        # so nothing is left holding a checked-out connection.
        poller_stop_event.set()
        if poller_thread is not None:
            try:
                poller_thread.join(timeout=2.0)
            except Exception as e:
                AbstraLogger.error(f"[Editor] Error joining poller thread: {e}")
        if execution_logs is not None:
            try:
                execution_logs.close()
            except Exception as e:
                AbstraLogger.error(f"[Editor] Error closing logs repository: {e}")
        try:
            from abstra_internals.services.db.connection import close_pool

            close_pool()
        except Exception as e:
            AbstraLogger.error(f"[Editor] Error closing DB pool: {e}")

    if editor_consumer is not None:
        try:
            editor_consumer.stop_iter()
        except Exception as e:
            AbstraLogger.error(f"[Editor] Error stopping editor consumer: {e}")
    if consumer_controller is not None:
        try:
            consumer_controller.shutdown()
        except Exception as e:
            AbstraLogger.error(f"[Editor] Error shutting down consumer controller: {e}")

    if stdio_broadcast_stop_event is not None:
        stdio_broadcast_stop_event.set()

    for component in watchers:
        if component is None:
            continue
        try:
            component.stop()
        except Exception as e:
            AbstraLogger.error(
                f"[Editor] Error stopping {component.__class__.__name__}: {e}"
            )

    # server.shutdown() blocks until serve_forever() returns, so run it
    # from a dedicated thread — the signal handler runs on the main thread
    # (same thread that is blocked in serve_forever).
    thread_factory(
        target=server.shutdown,
        name="WerkzeugShutdown",
        daemon=True,
    ).start()


def ensure_certificates():
    try:
        cafile = certifi.where()
        if not os.path.isfile(cafile):
            raise FileNotFoundError(f"Certifi CA file not found at {cafile}")
        ssl.create_default_context(cafile=cafile)
    except Exception:
        print(
            "SSL certificate validation failed. Attempting to restore certificates..."
        )
        try:
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "--force-reinstall",
                    "certifi",
                ],
                check=True,
            )
            import certifi as certifi_reinstalled

            cafile_re = certifi_reinstalled.where()
            if os.path.isfile(cafile_re):
                print(f"Certificates restored at: {cafile_re}")
            else:
                print(
                    f"Certifi CA file still missing at: {cafile_re}. Please check your Python environment."
                )
        except Exception as update_e:
            print(f"Failed to restore certificates: {update_e}")


class EditorStorageHandles(NamedTuple):
    heartbeat: Optional[WebEditorHeartbeat]
    logs_watcher: Optional[object]
    tasks_watcher: Optional[object]
    stdio_broadcast_stop_event: Optional[threading.Event]
    poller_stop_event: Optional[threading.Event]
    poller_thread: Optional[threading.Thread] = None


def _wire_editor_storage(
    main_controller: MainController,
    *,
    is_web_editor: bool,
    use_rabbitmq_workers: bool,
) -> EditorStorageHandles:
    """Wire the editor's storage-side moving parts and return their handles.

    The single switch is ``WEB_EDITOR_DATABASE_URI`` (invariant §6). On the DB
    path we run migrations (owner-canonical, D11), the age-based cleanup, and the
    poller — and do NOT start the heartbeat, the RabbitMQ stdio broadcast
    consumer, the LogsWatcher, or the TasksWatcher (gating §3/§18). On the legacy
    path behavior is unchanged.
    """
    from abstra_internals.environment import web_editor_uses_db

    db_set = web_editor_uses_db()
    if db_set and not use_rabbitmq_workers:
        # The factory would fall back to file-based local mode, silently
        # persisting to EFS while the DB sits idle — the spec's worst case (§20).
        # Fail fast (symmetric with web_editor_worker, which raises on missing
        # RabbitMQ) so the misconfiguration surfaces as a loud boot failure
        # instead of corrupting storage. cloud-api always injects both together.
        raise RuntimeError(
            "ABSTRA_WEB_EDITOR_DATABASE_URI is set but RABBITMQ_CONNECTION_URI is "
            "missing; the web-editor requires both. Refusing to start in a "
            "silent file-mode fallback."
        )

    db_mode = db_set and use_rabbitmq_workers

    if db_mode:
        from abstra_internals.services.db.cleanup import delete_old_records
        from abstra_internals.services.db.connection import configure_pool
        from abstra_internals.services.db.migrations import apply_migrations
        from abstra_internals.services.db.poller import start_poller

        # The editor serves a threaded Flask server + the poller concurrently, so
        # it needs a touch more headroom than the serial worker/executors.
        configure_pool(max_size=3)
        apply_migrations()
        try:
            # Retention cleanup is best-effort maintenance, not a serving
            # prerequisite — a failure here must never abort the editor boot.
            delete_old_records()
        except Exception as e:
            AbstraLogger.capture_exception(e)
        poller_stop_event, poller_thread = start_poller()
        return EditorStorageHandles(
            heartbeat=None,
            logs_watcher=None,
            tasks_watcher=None,
            stdio_broadcast_stop_event=None,
            poller_stop_event=poller_stop_event,
            poller_thread=poller_thread,
        )

    # Legacy (file-based) path — unchanged behavior.
    heartbeat: Optional[WebEditorHeartbeat] = None
    if is_web_editor:
        heartbeat = WebEditorHeartbeat()
        if heartbeat.is_stale():
            AbstraLogger.info(
                "[Editor] Heartbeat older than staleness threshold, "
                "cleaning shared storage"
            )
            main_controller.reset_repositories()
        else:
            AbstraLogger.info(
                "[Editor] Heartbeat is fresh, skipping reset_repositories "
                "to preserve shared storage"
            )
        heartbeat.start()
    else:
        main_controller.reset_repositories()

    stdio_broadcast_stop_event = None
    logs_watcher = None
    if WORKER_LOG_TO_QUEUE and not web_editor_uses_db() and use_rabbitmq_workers:
        assert RABBITMQ_CONNECTION_URI is not None
        broadcast_result = start_stdio_broadcast_consumer(RABBITMQ_CONNECTION_URI)
        if isinstance(broadcast_result, tuple) and len(broadcast_result) >= 2:
            stdio_broadcast_stop_event = broadcast_result[1]
    else:
        logs_watcher = LogsWatcher([on_logs_update])
        logs_watcher.start()

    tasks_watcher = TasksWatcher()
    tasks_watcher.start()

    return EditorStorageHandles(
        heartbeat=heartbeat,
        logs_watcher=logs_watcher,
        tasks_watcher=tasks_watcher,
        stdio_broadcast_stop_event=stdio_broadcast_stop_event,
        poller_stop_event=None,
    )


def editor(headless: bool, verbose: bool = False, debug_mode: bool = False):
    ensure_certificates()

    load_dotenv(Settings.root_path / ".env")

    serve_message()
    check_latest_version()
    AbstraLogger.init("local" if EDITOR_MODE == "local" else "cloud")

    _pythonuserbase = os.environ.get("PYTHONUSERBASE")
    if _pythonuserbase and os.path.isfile(
        os.path.join(_pythonuserbase, ".keep-abstra")
    ):
        AbstraLogger.warning(
            "[Editor] .keep-abstra marker detected — abstra package cleanup was skipped"
        )

    # Determine if we should use RabbitMQ based on EDITOR_MODE and RABBITMQ_CONNECTION_URI
    # Web editor with workers: EDITOR_MODE=web + RABBITMQ_CONNECTION_URI set
    # Web editor without workers: EDITOR_MODE=web + no RABBITMQ_CONNECTION_URI (legacy mode)
    # Local editor: EDITOR_MODE=local
    is_web_editor = EDITOR_MODE == "web"
    use_rabbitmq_workers = is_web_editor and RABBITMQ_CONNECTION_URI is not None

    AbstraLogger.info(
        f"[Editor] Configuration: EDITOR_MODE={EDITOR_MODE}, RABBITMQ_CONNECTION_URI={'SET' if RABBITMQ_CONNECTION_URI else 'NOT SET'}"
    )
    if WORKER_LOG_TO_QUEUE and not web_editor_uses_db():
        AbstraLogger.warning(
            "[Editor] ABSTRA_WORKER_LOG_TO_QUEUE=true, will receive execution logs from workers via RabbitMQ"
        )

    if use_rabbitmq_workers:
        AbstraLogger.info(
            "[Editor] Running in web editor mode with RabbitMQ workers (isolated execution)"
        )
        assert RABBITMQ_CONNECTION_URI is not None
        repositories = build_web_editor_repositories(RABBITMQ_CONNECTION_URI)
    else:
        if is_web_editor:
            AbstraLogger.info(
                "[Editor] Running in web editor mode without workers (legacy mode)"
            )
        else:
            AbstraLogger.info("[Editor] Running in local editor mode")
        mp_context = get_mp_context_repository()
        local_queue = safe_multiprocessing_queue(mp_context.get_context())
        repositories = build_editor_repositories(local_queue)

    main_controller = MainController(repositories)

    storage = _wire_editor_storage(
        main_controller,
        is_web_editor=is_web_editor,
        use_rabbitmq_workers=use_rabbitmq_workers,
    )
    heartbeat = storage.heartbeat

    StdioPatcher.apply(main_controller)

    codebase_event_controller = CodebaseEventController(repositories)
    CodebaseEventController.configure(
        repositories, controller_driven=use_rabbitmq_workers
    )

    watcher: Optional[FileWatcher] = None
    if not use_rabbitmq_workers:
        watcher = FileWatcher(
            [
                codebase_event_controller.reload_env,
                codebase_event_controller.reload_modules,
                codebase_event_controller.lint_files,
                codebase_event_controller.broadcast_changes,
            ]
        )
        watcher.start()

    RequirementsChangeNotifier.register(
        CodebaseEventController.notify_requirements_changed
    )
    AbstraJsonChangeNotifier.register(CodebaseEventController.notify_project_saved)

    # Run all linters once on startup in a background thread
    def _initial_lint():
        checks = repositories.linter.update_checks()
        LinterEventController.broadcast(checks)

    threading.Thread(target=_initial_lint, daemon=True, name="InitialLintCheck").start()

    logs_watcher = storage.logs_watcher
    tasks_watcher = storage.tasks_watcher
    stdio_broadcast_stop_event = storage.stdio_broadcast_stop_event

    editor_consumer = None
    consumer_controller = None
    if not is_web_editor:
        editor_consumer, _, consumer_controller = start_consumer(
            main_controller, debug_mode=debug_mode
        )

    app = get_local_app(main_controller)
    server = make_server(host=HOST, port=Settings.server_port, threaded=True, app=app)

    shutdown_started = threading.Event()

    def _graceful_shutdown():
        if shutdown_started.is_set():
            return
        shutdown_started.set()
        shutdown_editor_components(
            server=server,
            watchers=(watcher, logs_watcher, tasks_watcher, heartbeat),
            editor_consumer=editor_consumer,
            consumer_controller=consumer_controller,
            stdio_broadcast_stop_event=stdio_broadcast_stop_event,
            poller_stop_event=storage.poller_stop_event,
            poller_thread=storage.poller_thread,
            execution_logs=main_controller.repositories.execution_logs,
        )

    SignalHandlers.register_sigterm_callback(_graceful_shutdown)
    SignalHandlers.init()

    if not headless:
        background_open_editor()

    connect_tunnel(verbose=verbose)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        _graceful_shutdown()
    finally:
        try:
            server.server_close()
        except Exception:
            pass
        AbstraLogger.warning("[Editor] Server stopped")
