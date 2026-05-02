import logging
import os
from typing import Any, Optional

from gunicorn import glogging
import gunicorn.app.base

from workflow_server.config import ENABLE_PROCESS_WRAPPER, PORT, is_development
from workflow_server.server import app
from workflow_server.utils.exit_handler import gunicorn_exit_handler, init_signal_handlers
from workflow_server.utils.oom_killer import start_oom_killer_worker


class StandaloneApplication(gunicorn.app.base.BaseApplication):
    def __init__(self, app_param: gunicorn.app.base.BaseApplication, options: Optional[dict] = None) -> None:
        self.options = options or {}
        self.application = app_param
        super().__init__()

    def load_config(self) -> None:
        config = {key: value for key, value in self.options.items() if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self) -> None:
        return self.application


class CustomGunicornLogger(glogging.Logger):
    def setup(self, cfg: dict) -> None:
        super().setup(cfg)

        logger = logging.getLogger("gunicorn.access")
        logger.addFilter(HealthCheckFilter())
        logger.addFilter(SignalFilter())
        logger.addFilter(StatusIsAvailableFilter())


class HealthCheckFilter(logging.Filter):
    def filter(self, record: Any) -> bool:
        return "Handling signal: winch" not in record.getMessage()


class SignalFilter(logging.Filter):
    def filter(self, record: Any) -> bool:
        return "SIGTERM" not in record.getMessage()


class StatusIsAvailableFilter(logging.Filter):
    def filter(self, record: Any) -> bool:
        return "/status/is_available" not in record.getMessage()


def start() -> None:
    if not is_development():
        start_oom_killer_worker()
    init_signal_handlers()

    max_workflow_runtime_seconds = int(os.getenv("GUNICORN_TIMEOUT", os.getenv("MAX_WORKFLOW_RUNTIME_SECONDS", 1800)))

    # gevent didn't play nice with pebble and processes so just gthread here
    options = {
        "bind": f"0.0.0.0:{PORT}",
        "workers": int(os.getenv("GUNICORN_WORKERS", 2)),
        "threads": int(os.getenv("GUNICORN_THREADS", 9 if ENABLE_PROCESS_WRAPPER else 6)),
        # Aggressively try to avoid memory leaks when using non process mode
        "max_requests": int(os.getenv("GUNICORN_MAX_REQUESTS", 120 if ENABLE_PROCESS_WRAPPER else 20)),
        "max_requests_jitter": int(os.getenv("GUNICORN_MAX_REQUESTS_JITTER", 30 if ENABLE_PROCESS_WRAPPER else 10)),
        "worker_class": "gthread",
        "timeout": max_workflow_runtime_seconds,
        "logger_class": CustomGunicornLogger,
        "accesslog": "-",
        "on_exit": gunicorn_exit_handler,
        "graceful_timeout": max_workflow_runtime_seconds,
    }
    StandaloneApplication(app, options).run()
