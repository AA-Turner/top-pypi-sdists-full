"""
"""
import threading
from typing import Any
from typing import Callable


reload_server_ports: set[int] = set()


def start_reload_server(
    prerun: Callable[[], Any],
    postrun: Callable[[], bool],
    stop_event: threading.Event,
    port: int = 7887,
):
    from .server import ReloadServer

    reload_server = ReloadServer(
        prerun=prerun,
        postrun=postrun,
        stop_event=stop_event,
    )

    reload_server_ports.add(port)
    try:
        reload_server.run(port=port)
    finally:
        reload_server_ports.remove(port)
