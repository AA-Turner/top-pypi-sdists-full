import logging
import os

from flask import Flask

from workflow_server.api.auth_middleware import AuthMiddleware
from workflow_server.api.healthz_view import bp as healthz_bp
from workflow_server.api.status_view import bp as status_bp
from workflow_server.api.workflow_view import bp as workflow_bp
from workflow_server.config import is_development
from workflow_server.logging_config import GCPJsonFormatter
from workflow_server.utils.sentry import init_sentry
from workflow_server.utils.utils import get_version

# Disabled until we actually use the logs to provide us better debugging
# enable_log_proxy()

logger = logging.getLogger(__name__)

if is_development():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
else:
    handler = logging.StreamHandler()
    handler.setFormatter(GCPJsonFormatter())
    logging.root.addHandler(handler)
    logging.root.setLevel(logging.INFO)


def create_app() -> Flask:
    SENTRY_DSN = os.getenv("SENTRY_DSN")
    if SENTRY_DSN:
        init_sentry(sentry_log_level=logging.INFO, dsn=SENTRY_DSN)

    FLASK_ENV = os.getenv("FLASK_ENV", "local")

    logger.info(f"Creating App using config: config.{FLASK_ENV}")

    version_info = get_version()
    logger.info(
        f"Running with SDK version: {version_info['sdk_version']}, Server version: {version_info['server_version']}"
    )

    app = Flask(__name__)
    app.wsgi_app = AuthMiddleware(app.wsgi_app)  # type: ignore

    # Register blueprints
    app.register_blueprint(healthz_bp, url_prefix="/healthz")
    app.register_blueprint(status_bp, url_prefix="/status")
    app.register_blueprint(workflow_bp, url_prefix="/workflow")

    logger.info(is_development())

    return app


app = create_app()
