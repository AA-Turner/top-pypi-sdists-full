import uvicorn

from project.core.settings import get_cached_settings
from project.core.util import setup_logging


def __command():
    setup_logging()
    uvicorn.run(
        "project.sqladmin_.asgi:app",
        port=get_cached_settings().sqladmin_port,
        host="localhost",
        workers=1,
        reload=False
    )


if __name__ == '__main__':
    __command()
