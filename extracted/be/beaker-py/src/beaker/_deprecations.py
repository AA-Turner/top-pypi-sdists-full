import warnings

from . import beaker_pb2 as _pb2

_original_system_details_getattribute = _pb2.SystemDetails.__getattribute__


def _system_details_getattribute(self, name):
    if name == "preemptible":
        warnings.warn(
            "SystemDetails.preemptible is deprecated and always returns False. "
            "Use min_runtime and auto_resume instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return False
    return _original_system_details_getattribute(self, name)


_pb2.SystemDetails.__getattribute__ = _system_details_getattribute  # type: ignore[method-assign]
