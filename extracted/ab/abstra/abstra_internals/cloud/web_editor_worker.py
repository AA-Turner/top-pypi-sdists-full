import os

from abstra_internals.controllers.execution.consumer import ConsumerController
from abstra_internals.controllers.main import MainController
from abstra_internals.environment import (
    DEFAULT_PORT,
    RABBITMQ_CONNECTION_URI,
    WORKER_LOG_TO_QUEUE,
)
from abstra_internals.logger import AbstraLogger
from abstra_internals.repositories.consumer import (
    WebEditorConsumer,
    WebEditorControlConsumer,
)
from abstra_internals.repositories.factory import build_web_editor_repositories
from abstra_internals.settings import SettingsController
from abstra_internals.signals import SignalHandlers
from abstra_internals.utils.packages import get_local_package_version


def run():
    SignalHandlers.init()
    AbstraLogger.init("cloud")
    AbstraLogger.warning(
        f"[web-editor-worker] Running abstra version {get_local_package_version()}"
    )
    if WORKER_LOG_TO_QUEUE:
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

    repositories = build_web_editor_repositories(RABBITMQ_CONNECTION_URI)
    controller = MainController(repositories=repositories)

    with WebEditorConsumer(RABBITMQ_CONNECTION_URI) as consumer:
        with WebEditorControlConsumer(RABBITMQ_CONNECTION_URI) as control_consumer:
            SignalHandlers.register_sigterm_callback(consumer.stop_iter)
            SignalHandlers.register_sigterm_callback(control_consumer.stop_iter)
            ConsumerController(controller, consumer, control_consumer).start_loop()


if __name__ == "__main__":
    run()
