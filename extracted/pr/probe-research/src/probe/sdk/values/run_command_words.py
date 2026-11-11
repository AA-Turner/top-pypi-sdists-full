"""The words of a run command's `?with=writer` read: the writer's state, the list parts, and the writer's roles (twins:
probe_contracts `CommandWriter`, `CommandListPart` and the `writer_role` Literal of `CommandList`; a test holds them
equal). Light on purpose: the CLI starts without the SDK client."""

from __future__ import annotations

from ...foundation.compat.compat import StrEnum


class CommandWriter(StrEnum):
    """`writer` in a `?with=writer` page (twin: probe_contracts `CommandWriter`; a test holds them equal)."""

    LIVE = "live"
    NONE = "none"
    UNREPORTED = "unreported"


class CommandListPart(StrEnum):
    """What `list_run_commands(parts=...)` may add (twin: probe_contracts `CommandListPart`)."""

    WRITER = "writer"


class WriterRole(StrEnum):
    """`writer_role` in a `?with=writer` page (twin: the `writer_role` Literal of probe_contracts `CommandList`)."""

    OWNER = "owner"
    RANK = "rank"
    LAUNCHER = "launcher"
    OBSERVER = "observer"


#: The roles of the script itself; a `launcher` (`probe exec`) or an `observer` beat says it is not.
SCRIPT_WRITER_ROLES = (WriterRole.OWNER, WriterRole.RANK)
