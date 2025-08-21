import uvicorn

from project.api.before_start_api import before_start_api
from project.core.settings import get_cached_settings
from project.core.setup_logging import setup_logging


def start_api():
    setup_logging()
    before_start_api()
    uvicorn.run(
        "project.api.asgi:app",
        port=get_cached_settings().api_port,
        host=get_cached_settings().api_host,
        workers=get_cached_settings().api_workers,
        reload=get_cached_settings().api_reload
    )


if __name__ == '__main__':
    start_api()
