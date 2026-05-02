# Gunicorn Configuration File
import asyncio
import multiprocessing
import navconfig
from qw.discovery import get_server_discovery

cores = int(multiprocessing.cpu_count() / 2)

APP_HOST = navconfig.config.get("APP_HOST", fallback="0.0.0.0")
APP_PORT = navconfig.config.get("APP_PORT", fallback=5000)
GUNICORN_WORKERS = navconfig.config.getint("GUNICORN_WORKERS", fallback=cores)
GUNICORN_REQUESTS = navconfig.config.getint('GUNICORN_REQUESTS', fallback=100)


def on_starting(server):
    """Run the discovery server in the master process."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def start_discovery():
        transport, discovery_server = await get_server_discovery(loop)
        print(":: Starting Discovery Server in master process ::")

    loop.run_until_complete(start_discovery())


# workers = int(APP_WORKERS)
workers = 1
threads = 1
max_request = GUNICORN_REQUESTS
max_requests_jitter = 10
bind = f"{APP_HOST}:{APP_PORT}"
backlog = 2048
worker_connections = GUNICORN_REQUESTS
timeout = 360
keepalive = 2
worker_class = "aiohttp.worker.GunicornUVLoopWebWorker"
