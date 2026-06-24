import os
from importlib.metadata import PackageNotFoundError

from abstra_internals.controllers.execution.consumer import ConsumerController
from abstra_internals.controllers.main import MainController
from abstra_internals.environment import (
    DEFAULT_PORT,
    NATS_CREDS,
    NATS_URL,
    RABBITMQ_CONNECTION_URI,
    WORKER_LOG_TO_QUEUE,
    web_editor_uses_db,
)
from abstra_internals.logger import AbstraLogger
from abstra_internals.repositories.consumer import (
    WebEditorConsumer,
    WebEditorControlConsumer,
)
from abstra_internals.repositories.factory import build_web_editor_repositories
from abstra_internals.services.nats_file_events import WorkerFileChangeNotifier
from abstra_internals.settings import SettingsController
from abstra_internals.signals import SignalHandlers
from abstra_internals.utils.packages import get_local_package_version


def run():
    SignalHandlers.init()
    AbstraLogger.init("cloud")
    try:
        abstra_version = str(get_local_package_version())
    except PackageNotFoundError:
        abstra_version = "0.0.0"
    AbstraLogger.warning(f"[web-editor-worker] Running abstra version {abstra_version}")
    if WORKER_LOG_TO_QUEUE and not web_editor_uses_db():
        AbstraLogger.warning(
            "[web-editor-worker] ABSTRA_WORKER_LOG_TO_QUEUE=true, execution logs will be sent via RabbitMQ"
        )

    _pythonuserbase = os.environ.get("PYTHONUSERBASE")
    if _pythonuserbase and os.path.isfile(
        os.path.join(_pythonuserbase, ".keep-abstra")
    ):
        AbstraLogger.warning(
            "[web-editor-worker] .keep-abstra marker detected — abstra package cleanup was skipped"
        )

    SettingsController.set_root_path(".")
    SettingsController.set_server_port(DEFAULT_PORT)

    if not RABBITMQ_CONNECTION_URI:
        raise Exception("ABSTRA_RABBITMQ_CONNECTION_URI not found")

    if web_editor_uses_db():
        # Owner-canonical migration for the worker (decision D11): run once per
        # pod, BEFORE building repositories. The factory never migrates.
        from abstra_internals.services.db.connection import configure_pool
        from abstra_internals.services.db.migrations import apply_migrations

        # Worker main and the executors it forks are largely serial (~2 conns:
        # the synchronous final-flush + the log-flush daemon). Setting it here
        # also covers the forkserver-forked executors, which inherit this value.
        configure_pool(max_size=2)
        apply_migrations()

    repositories = build_web_editor_repositories(RABBITMQ_CONNECTION_URI)
    controller = MainController(repositories=repositories)

    with WebEditorConsumer(RABBITMQ_CONNECTION_URI) as consumer:
        with WebEditorControlConsumer(RABBITMQ_CONNECTION_URI) as control_consumer:
            # SIGTERM callbacks fire in registration order (FIFO). Stop the
            # consumers FIRST so the message loop quiesces, THEN drain the logs
            # repo, THEN close the pool last — otherwise an in-flight handler
            # could check out from a closing pool (and get_pool would silently
            # recreate it, defeating the close-last intent).
            SignalHandlers.register_sigterm_callback(consumer.stop_iter)
            SignalHandlers.register_sigterm_callback(control_consumer.stop_iter)

            # publish this node's own file writes over NATS for the editor pod
            file_change_notifier = None
            if NATS_URL and NATS_CREDS:
                try:
                    file_change_notifier = WorkerFileChangeNotifier(
                        NATS_URL, NATS_CREDS
                    )
                    file_change_notifier.start()
                    SignalHandlers.register_sigterm_callback(file_change_notifier.stop)
                    AbstraLogger.warning(
                        "[web-editor-worker] file-change NATS notifier started"
                    )
                except Exception as e:
                    AbstraLogger.error(
                        f"[web-editor-worker] failed to start file-change notifier: {e}"
                    )

            if web_editor_uses_db():
                from abstra_internals.services.db.connection import close_pool

                SignalHandlers.register_sigterm_callback(
                    repositories.execution_logs.close
                )
                SignalHandlers.register_sigterm_callback(close_pool)
            ConsumerController(controller, consumer, control_consumer).start_loop()


if __name__ == "__main__":
    run()
