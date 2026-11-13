"""
"""

import threading
from typing import Any
from typing import Callable
from uuid import uuid4


reload_server_ports: set[int] = set()


def start_reload_server(
    prerun: Callable[[], Any],
    postrun: Callable[[], bool],
    stop_event: threading.Event,
    port: int = 7887,
):
    from ..zero.context import GlobalContext
    from .server import ReloadServer

    reload_server = ReloadServer(
        prerun=prerun,
        postrun=postrun,
        stop_event=stop_event,
    )

    server_port_uuid = uuid4()
    GlobalContext.server_ports[server_port_uuid] = port
    try:
        reload_server.run(port=port)
    finally:
        del GlobalContext.server_ports[server_port_uuid]
