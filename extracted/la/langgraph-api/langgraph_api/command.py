import re
from typing import Any, cast

from langgraph.types import Command, Send

from langgraph_api.schema import RunCommand

# langgraph resumes interrupts by id only when every key of the resume map has
# this shape; any other key turns the whole map into one value for whichever
# interrupt is pending.
INTERRUPT_ID_RE = re.compile(r"[0-9a-f]{32}")


def keyed_by_interrupt_id(value: Any) -> bool:
    """Whether langgraph resumes ``value`` per interrupt rather than as one answer."""
    return (
        isinstance(value, dict)
        and bool(value)
        and all(INTERRUPT_ID_RE.fullmatch(key) for key in value)
    )


def map_cmd(cmd: RunCommand) -> Command:
    goto = cmd.get("goto")
    if goto is not None and not isinstance(goto, list):
        goto = [cmd.get("goto")]

    update = cmd.get("update")
    if isinstance(update, tuple | list) and all(
        isinstance(t, tuple | list) and len(t) == 2 and isinstance(t[0], str)
        for t in cast("list", update)
    ):
        update = [tuple(t) for t in cast("list", update)]

    return Command(
        update=update,
        goto=(
            [
                it if isinstance(it, str) else Send(it["node"], it["input"])
                for it in goto
            ]
            if goto
            else None
        ),
        resume=cmd.get("resume"),
    )
