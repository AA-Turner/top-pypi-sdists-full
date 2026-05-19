import os
from importlib.metadata import PackageNotFoundError

from abstra_internals.cloud.tracing import init_tracing

# Must run before pika/requests are imported/used so instrumentation can patch them.
# Every `from abstra_internals…` import below carries `# noqa: E402` because of this —
# ruff flags them as "module-level import not at top of file" otherwise.
init_tracing(service_name="abstra-worker")

from abstra_internals.controllers.execution.consumer import (  # noqa: E402
    ConsumerController,
)
from abstra_internals.controllers.main import MainController  # noqa: E402
from abstra_internals.environment import (  # noqa: E402
    DEFAULT_PORT,
    RABBITMQ_CONNECTION_URI,
)
from abstra_internals.logger import AbstraLogger  # noqa: E402
from abstra_internals.repositories.consumer import (  # noqa: E402
    ProductionControlConsumer,
    RabbitConsumer,
)
from abstra_internals.repositories.factory import build_prod_repositories  # noqa: E402
from abstra_internals.settings import SettingsController  # noqa: E402
from abstra_internals.signals import SignalHandlers  # noqa: E402
from abstra_internals.utils.packages import get_local_package_version  # noqa: E402


def run():
    SignalHandlers.init()
    AbstraLogger.init("cloud")
    try:
        abstra_version = str(get_local_package_version())
    except PackageNotFoundError:
        abstra_version = "0.0.0"
    AbstraLogger.warning(f"[abstra-worker] Running abstra version {abstra_version}")
    SettingsController.set_root_path(os.getenv("ABSTRA_PROJECT_PATH", "."))
    SettingsController.set_server_port(DEFAULT_PORT)

    if not RABBITMQ_CONNECTION_URI:
        raise Exception("RABBITMQ_CONNECTION_URI not found")

    controller = MainController(repositories=build_prod_repositories())

    with RabbitConsumer(RABBITMQ_CONNECTION_URI) as consumer:
        with ProductionControlConsumer(RABBITMQ_CONNECTION_URI) as control_consumer:
            SignalHandlers.register_sigterm_callback(consumer.stop_iter)
            SignalHandlers.register_sigterm_callback(control_consumer.stop_iter)
            ConsumerController(controller, consumer, control_consumer).start_loop()


if __name__ == "__main__":
    run()
