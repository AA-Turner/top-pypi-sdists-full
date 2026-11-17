from typing import TYPE_CHECKING, Any

from chalk_remote_call._version import __version__
from chalk_remote_call.server import serve

if TYPE_CHECKING:
    from chalk_remote_call._native import ServingHandle

__all__ = ["ServingHandle", "__version__", "serve"]


def __getattr__(name: str) -> Any:
    if name == "ServingHandle":
        from chalk_remote_call._native import ServingHandle

        return ServingHandle
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
