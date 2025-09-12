import logging
import os

import starlette.types
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from project.api.event import get_startup_api_events, get_shutdown_api_events
from project.api.exception_handler import add_exception_handler_to_api_app
from project.api.middleware.add_api_middlewares import add_api_middlewares
from project.api.openapi_ui import add_local_openapi_ui_to_api_app
from project.api.router.main_router import main_api_router
from project.core.const import ProjectPaths
from project.core.settings import get_cached_settings
from project.core.setup_logging import setup_logging

_logger = logging.getLogger(__name__)


def create_api_app(*, prefix: str = "/api") -> FastAPI:
    setup_logging()

    _logger.info("start")

    api_app = FastAPI(
        title=get_cached_settings().project_name,
        description=get_cached_settings().project_title,
        version=get_cached_settings().api_version,
        docs_url=None,
        redoc_url=None,
        openapi_url=get_cached_settings().api_openapi_url,
        on_startup=get_startup_api_events(),
        on_shutdown=get_shutdown_api_events(),
        contact={
            "name": "ARPAKIT Company",
            "url": "https://arpakit.com/",
            "email": "support@arpakit.com",
        },
    )

    add_api_middlewares(app=api_app)

    add_local_openapi_ui_to_api_app(
        app=api_app,
        docs_url=get_cached_settings().api_docs_url,
        redoc_url=get_cached_settings().api_redoc_url
    )

    add_exception_handler_to_api_app(app=api_app)

    api_app.include_router(
        prefix=prefix,
        router=main_api_router
    )

    class _CustomStaticFiles(StaticFiles):
        async def get_response(self, path: str, scope: starlette.types.Scope):
            if os.path.isfile(os.path.join(self.directory, path)):
                headers = {"Content-Disposition": f"attachment; filename={os.path.basename(path)}"}
                response = await super().get_response(path, scope)
                response.headers.update(headers)
                return response
            return await super().get_response(path, scope)

    if get_cached_settings().media_dirpath is not None:
        if not os.path.exists(get_cached_settings().media_dirpath):
            os.makedirs(get_cached_settings().media_dirpath, exist_ok=True)
        api_app.mount("/media", _CustomStaticFiles(directory=get_cached_settings().media_dirpath), name="media")

    if not os.path.exists(ProjectPaths.static_dirpath):
        os.makedirs(ProjectPaths.static_dirpath, exist_ok=True)
    api_app.mount("/static", _CustomStaticFiles(directory=ProjectPaths.static_dirpath), name="static")

    if get_cached_settings().api_enable_sqladmin:
        from project.sqladmin_.add_admin_in_app import add_sqladmin_in_app
        add_sqladmin_in_app(
            base_url=get_cached_settings().sqladmin_prefix, app=api_app, favicon_url="/static/openapi-favicon.png"
        )

    _logger.info("finish")

    return api_app
