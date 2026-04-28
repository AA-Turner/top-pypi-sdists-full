import os
import ssl
import subprocess
import sys
import threading

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
    thread_factory=threading.Thread,
):
    """Stop every long-lived resource started by editor() and unblock
    serve_forever() by scheduling server.shutdown() on a background thread.

    Exposed at module level so it can be unit-tested without bootstrapping
    the full editor() function.
    """
    AbstraLogger.warning("[Editor] Graceful shutdown initiated")

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
    if WORKER_LOG_TO_QUEUE:
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
    main_controller.reset_repositories()
    StdioPatcher.apply(main_controller)

    codebase_event_controller = CodebaseEventController(repositories)
    watcher = FileWatcher(
        [
            codebase_event_controller.reload_env,
            codebase_event_controller.reload_modules,
            codebase_event_controller.lint_files,
            codebase_event_controller.broadcast_changes,
        ]
    )
    watcher.start()

    # Run all linters once on startup in a background thread
    def _initial_lint():
        checks = repositories.linter.update_checks()
        LinterEventController.broadcast(checks)

    threading.Thread(target=_initial_lint, daemon=True, name="InitialLintCheck").start()

    logs_watcher = None
    stdio_broadcast_stop_event = None
    if WORKER_LOG_TO_QUEUE and use_rabbitmq_workers:
        assert RABBITMQ_CONNECTION_URI is not None
        broadcast_result = start_stdio_broadcast_consumer(RABBITMQ_CONNECTION_URI)
        if isinstance(broadcast_result, tuple) and len(broadcast_result) >= 2:
            stdio_broadcast_stop_event = broadcast_result[1]
    else:
        logs_watcher = LogsWatcher([on_logs_update])
        logs_watcher.start()

    tasks_watcher = TasksWatcher()
    tasks_watcher.start()

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
            watchers=(watcher, logs_watcher, tasks_watcher),
            editor_consumer=editor_consumer,
            consumer_controller=consumer_controller,
            stdio_broadcast_stop_event=stdio_broadcast_stop_event,
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
