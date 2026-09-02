"""FlowTask Events.

Event System for Flowtask.
"""
from .abstract import AbstractEvent
from .publish import PublishEvent
from .log import LogEvent
from .logerr import LogError
from .dummy import Dummy
from .webhook import WebHook
from .file import FileDelete, FileCopy

# Heavy event classes that pull in notify, jira, pandas, etc.
# are lazy-loaded to avoid importing those packages at startup.
_LAZY_IMPORTS = {
    "NotifyEvent": (".notify_event", "NotifyEvent"),
    "TeamsMessage": (".teams", "TeamsMessage"),
    "SendFile": (".sendfile", "SendFile"),
    "Alert": (".alerts", "Alert"),
    "Notify": (".notify", "Notify"),
    "RunTask": (".task", "RunTask"),
    "Jira": (".jira", "Jira"),
}


def __getattr__(name: str):
    if name in _LAZY_IMPORTS:
        module_path, attr_name = _LAZY_IMPORTS[name]
        import importlib
        module = importlib.import_module(module_path, package=__name__)
        value = getattr(module, attr_name)
        globals()[name] = value
        return value
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
