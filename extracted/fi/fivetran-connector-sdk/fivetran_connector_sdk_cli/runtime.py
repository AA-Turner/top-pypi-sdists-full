"""Where the front end sends what a connector emits. `core_adapter` installs a sink before it calls the connector."""
import threading

from fivetran_connector_sdk_core import Sink


# A connector may call operations from several threads. A file's chunks and the row that describes it must stay
# together, and one checkpoint is in flight at a time; other threads keep emitting meanwhile.
producer_lock = threading.Lock()
checkpoint_lock = threading.Lock()

_sink = None


def install(sink):
    global _sink
    _sink = sink


def current() -> Sink:
    if _sink is None:
        raise RuntimeError("no runner is installed: operations can only be called while the runner executes the connector")
    return _sink
