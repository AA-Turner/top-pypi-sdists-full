import contextlib
from enum import Enum

from .version import version as __version__


print(
    "Hud does not support this platform yet. The SDK has initiated a graceful shutdown. Your application remains unaffected. See the compatibility matrix for details: https://docs.hud.io/docs/hud-sdk-compatibility-matrix-for-python"
)


def init_session(*args, **kwargs):
    pass


def register(*args, **kwargs):
    pass


def init(*args, **kwargs):
    pass


def set_hook(*args, **kwargs):
    pass

def set_failure(*args, **kwargs):
    pass

def set_context(*args, **kwargs):
    pass


def start_flow(*args, **kwargs):
    pass


def end_flow(*args, **kwargs):
    pass


try:
    _AsyncContextDecorator = contextlib.AsyncContextDecorator
except AttributeError:  # Python < 3.10
    from functools import wraps

    class _AsyncContextDecorator:
        def __call__(self, func):
            # The stdlib AsyncContextDecorator enters self._recreate_cm() to give
            # single-use context managers a fresh instance per call. This no-op
            # stand-in is trivially reusable, so we enter self directly and drop
            # the _recreate_cm indirection.
            @wraps(func)
            async def inner(*args, **kwds):
                async with self:
                    return await func(*args, **kwds)

            return inner


class sync_flow(contextlib.ContextDecorator):
    # No-op stand-in usable as a context manager or a decorator.
    def __init__(self, *args, **kwargs):
        pass

    def __enter__(self):
        return None

    def __exit__(self, *exc_info):
        return False


class async_flow(_AsyncContextDecorator):
    # No-op stand-in usable as an async context manager or a decorator.
    def __init__(self, *args, **kwargs):
        pass

    async def __aenter__(self):
        return None

    async def __aexit__(self, *exc_info):
        return False


class FlowType(str, Enum):
    QUEUE = "queue"
    CUSTOM = "custom"


class Framework(str, Enum):
    PIKA = "pika"
    AIO_PIKA = "aio_pika"
    GOOGLE_CLOUD_PUBSUB = "google_cloud_pubsub"
    AZURE_SERVICEBUS = "azure_servicebus"
    AZURE_EVENTHUB = "azure_eventhub"
    SQS = "sqs"
    KAFKA = "kafka"
    # Manual flows
    CUSTOM = "custom"

class RegisterConfig:
    def __init__(self, *args, **kwargs):
        pass


__all__ = [
    "__version__",
    "RegisterConfig",
    "init_session",
    "register",
    "init",
    "set_hook",
    "set_failure",
    "set_context",
    "start_flow",
    "end_flow",
    "sync_flow",
    "async_flow",
    "FlowType",
    "Framework",
]
