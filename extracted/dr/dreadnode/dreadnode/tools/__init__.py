import importlib
import typing as t

if t.TYPE_CHECKING:
    from dreadnode.agents.tools import Tool, Toolset
    from dreadnode.tools.apply_patch import apply_patch
    from dreadnode.tools.dreadnode_cli import dreadnode_cli
    from dreadnode.tools.editing import delete_lines, edit_file, insert_lines, multiedit
    from dreadnode.tools.execute import bash, python
    from dreadnode.tools.fetch import fetch
    from dreadnode.tools.glob import glob
    from dreadnode.tools.grep import grep
    from dreadnode.tools.interaction import UserCancelled, ask_user, confirm
    from dreadnode.tools.ls import ls
    from dreadnode.tools.memory import Memory
    from dreadnode.tools.project_memory import ProjectMemory
    from dreadnode.tools.read import read
    from dreadnode.tools.report import report
    from dreadnode.tools.think import think
    from dreadnode.tools.todo import todo
    from dreadnode.tools.web_extract import web_extract
    from dreadnode.tools.web_search import web_search
    from dreadnode.tools.write import write

# Lazy attribute access via __getattr__ — submodules are loaded on demand
# to avoid circular imports. Each public name maps to a submodule that
# defines an attribute of the same name.

__all__ = [
    "Memory",
    "ProjectMemory",
    "UserCancelled",
    "apply_patch",
    "ask_user",
    "bash",
    "confirm",
    "delete_lines",
    "dreadnode_cli",
    "edit_file",
    "fetch",
    "glob",
    "grep",
    "insert_lines",
    "ls",
    "multiedit",
    "python",
    "read",
    "report",
    "think",
    "todo",
    "web_extract",
    "web_search",
    "write",
]

# Names whose submodule has a different filename than the public attribute.
_SUBMODULE_OVERRIDES: dict[str, str] = {
    "Memory": "memory",
    "ProjectMemory": "project_memory",
    "delete_lines": "editing",
    "edit_file": "editing",
    "insert_lines": "editing",
    "multiedit": "editing",
    "bash": "execute",
    "python": "execute",
    "ask_user": "interaction",
    "confirm": "interaction",
    "UserCancelled": "interaction",
}


def __getattr__(name: str) -> t.Any:
    if name in __all__:
        submodule_name = _SUBMODULE_OVERRIDES.get(name, name)
        module = importlib.import_module(f".{submodule_name}", __name__)
        attr = getattr(module, name)
        globals()[name] = attr
        return attr

    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


def default_tools(
    *,
    additional_toolsets: list["Toolset"] | None = None,
) -> dict[str, "Tool | Toolset"]:
    """All standard tools, keyed by function name.

    Imports are deferred to avoid circular dependencies.
    """
    from dreadnode.tools.apply_patch import apply_patch
    from dreadnode.tools.editing import delete_lines, edit_file, insert_lines, multiedit
    from dreadnode.tools.execute import bash, python
    from dreadnode.tools.fetch import fetch
    from dreadnode.tools.glob import glob
    from dreadnode.tools.grep import grep
    from dreadnode.tools.interaction import ask_user, confirm
    from dreadnode.tools.ls import ls
    from dreadnode.tools.memory import Memory
    from dreadnode.tools.read import read
    from dreadnode.tools.report import report
    from dreadnode.tools.think import think
    from dreadnode.tools.todo import todo
    from dreadnode.tools.web_extract import web_extract
    from dreadnode.tools.web_search import web_search
    from dreadnode.tools.write import write

    tools: list[Tool | Toolset] = [
        read,
        write,
        glob,
        grep,
        ls,
        edit_file,
        multiedit,
        delete_lines,
        insert_lines,
        apply_patch,
        bash,
        python,
        fetch,
        web_extract,
        web_search,
        report,
        think,
        todo,
        ask_user,
        confirm,
        Memory(),
    ]
    if additional_toolsets:
        tools.extend(additional_toolsets)
    return {tool.name: tool for tool in tools}
