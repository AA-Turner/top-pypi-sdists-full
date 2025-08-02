import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from project.core.settings import get_cached_settings
from project.core.util import setup_logging
from project.sqladmin_.add_admin_in_app import add_sqladmin_in_app
from project.sqladmin_.event import get_sqladmin_startup_events, get_sqladmin_shutdown_events

_logger = logging.getLogger(__name__)


def create_sqladmin_app(*, prefix: str = "/sqladmin") -> FastAPI:
    setup_logging()

    _logger.info("start")

    sqladmin_app = FastAPI(
        title=get_cached_settings().project_name,
        description=get_cached_settings().project_name,
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
        on_startup=get_sqladmin_startup_events(),
        on_shutdown=get_sqladmin_shutdown_events(),
        contact={
            "name": "ARPAKIT Company",
            "url": "https://arpakit.com/",
            "email": "support@arpakit.com",
        },
    )

    sqladmin_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    add_sqladmin_in_app(
        app=sqladmin_app,
        base_url=prefix
    )

    _logger.info("finish")

    return sqladmin_app
