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


class HealthCheckFilter(logging.Filter):
    def filter(self, record: Any) -> bool:
        return "GET /healthz" not in record.getMessage()


def start() -> None:
    if not is_development():
        start_oom_killer_worker()
    init_signal_handlers()

    # gevent didn't play nice with pebble and processes so just gthread here
    options = {
        "bind": f"0.0.0.0:{PORT}",
        "workers": int(os.getenv("GUNICORN_WORKERS", 2)),
        "threads": int(os.getenv("GUNICORN_THREADS", 9 if ENABLE_PROCESS_WRAPPER else 6)),
        # Try to avoid memory leaks when using non process mode
        "max_requests": 0 if ENABLE_PROCESS_WRAPPER else 20,
        "worker_class": "gthread",
        "timeout": int(os.getenv("GUNICORN_TIMEOUT", 1800)),
        "logger_class": CustomGunicornLogger,
        "accesslog": "-",
        "on_exit": gunicorn_exit_handler,
        "graceful_timeout": int(os.getenv("GUNICORN_TIMEOUT", 1800)),
    }
    StandaloneApplication(app, options).run()
