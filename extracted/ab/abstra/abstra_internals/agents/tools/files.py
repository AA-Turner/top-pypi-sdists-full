from collections.abc import Iterable
from os import PathLike
from typing import List, Literal, Set, Union, get_args

from .base import AgentTools

FileAction = Literal[
    "read",
    "read_text",
    "read_bytes",
    "write",
    "write_text",
    "write_bytes",
    "delete",
    "move",
    "list",
    "append",
]


def to_actions(a: Union[FileAction, Iterable[FileAction]]) -> Set[FileAction]:
    if isinstance(a, str):
        return set(*[a])
    return set(a)


def to_globs(g: Union[str, PathLike, Iterable[Union[str, PathLike]]]) -> Set[str]:
    if isinstance(g, Iterable):
        return set(map(str, g))
    return set(map(str, [g]))


def path_in_glob(glob_exp: str, path: PathLike) -> bool:
    from glob import glob

    return path in glob(glob_exp)


class FilesTools(AgentTools):
    """
    Toolkit that gives an agent access to the project filesystem. The agent gets one tool per allowed action (`read_text`, `write_text`, `list`, `delete`, etc.), restricted to paths matching the configured glob patterns.
    """

    actions: Set[FileAction]
    globs: Set[str]

    def __init__(
        self,
        actions: Union[FileAction, Iterable[FileAction]] = get_args(FileAction),
        globs: Union[str, PathLike, Iterable[PathLike]] = "*",
    ):
        """
        Build a FilesTools toolkit, optionally scoped to specific actions and path globs.

        Args:
            actions (Union): Allowed file operations. One of `"read"`, `"read_text"`, `"read_bytes"`, `"write"`, `"write_text"`, `"write_bytes"`, `"delete"`, `"move"`, `"list"`, `"append"`, or a list of them. Shorthand `"read"` enables both `read_text` and `read_bytes`; `"write"` enables both write variants. Defaults to all actions.
            globs (Union): Glob pattern(s) restricting which paths the agent can touch (e.g. `"data/*"` or `["*.csv", "reports/**"]`). Defaults to `"*"` (all paths).
        """
        self.actions = to_actions(actions)
        self.globs = to_globs(globs)

    def read_text(self, path: PathLike, encoding="utf-8") -> str:
        if "read" not in self.actions and "read_text" not in self.actions:
            raise PermissionError("Read action is not allowed.")

        for glob_exp in self.globs:
            if path_in_glob(glob_exp, path):
                break
        else:
            raise ValueError(f"Path '{path}' is not allowed.")

        with open(path, "r", encoding=encoding) as f:
            return f.read()

    def read_bytes(self, path: PathLike) -> bytes:
        if "read" not in self.actions and "read_bytes" not in self.actions:
            raise PermissionError("Read action is not allowed.")

        for glob_exp in self.globs:
            if path_in_glob(glob_exp, path):
                break
        else:
            raise ValueError(f"Path '{path}' is not allowed.")

        with open(path, "rb") as f:
            return f.read()

    def write_text(self, path: PathLike, data: str, encoding="utf-8") -> None:
        if "write" not in self.actions and "write_text" not in self.actions:
            raise PermissionError("Write action is not allowed.")

        for glob_exp in self.globs:
            if path_in_glob(glob_exp, path):
                break
        else:
            raise ValueError(f"Path '{path}' is not allowed.")

        with open(path, "w", encoding=encoding) as f:
            f.write(data)

    def write_bytes(self, path: PathLike, data: bytes) -> None:
        if "write" not in self.actions and "write_bytes" not in self.actions:
            raise PermissionError("Write action is not allowed.")

        for glob_exp in self.globs:
            if path_in_glob(glob_exp, path):
                break
        else:
            raise ValueError(f"Path '{path}' is not allowed.")

        with open(path, "wb") as f:
            f.write(data)

    def delete(self, path: PathLike) -> None:
        import os

        if "delete" not in self.actions:
            raise PermissionError("Delete action is not allowed.")

        for glob_exp in self.globs:
            if path_in_glob(glob_exp, path):
                break
        else:
            raise ValueError(f"Path '{path}' is not allowed.")

        os.remove(path)

    def move(self, src: PathLike, dst: PathLike) -> None:
        import shutil

        if "move" not in self.actions:
            raise PermissionError("Move action is not allowed.")

        for glob_exp in self.globs:
            if path_in_glob(glob_exp, src) and path_in_glob(glob_exp, dst):
                break
        else:
            raise ValueError(f"Source '{src}' or destination '{dst}' is not allowed.")

        shutil.move(src, dst)

    def list(self, path: PathLike) -> list[str]:
        import os

        if "list" not in self.actions:
            raise PermissionError("List action is not allowed.")

        for glob_exp in self.globs:
            if path_in_glob(glob_exp, path):
                break
        else:
            raise ValueError(f"Path '{path}' is not allowed.")

        return os.listdir(path)

    def append(self, path: PathLike, data: str, encoding="utf-8") -> None:
        if "append" not in self.actions:
            raise PermissionError("Append action is not allowed.")

        for glob_exp in self.globs:
            if path_in_glob(glob_exp, path):
                break
        else:
            raise ValueError(f"Path '{path}' is not allowed.")

        with open(path, "a", encoding=encoding) as f:
            f.write(data)

    def __tools__(self) -> List[str]:
        return [
            self.read_text.__name__,
            self.read_bytes.__name__,
            self.write_text.__name__,
            self.write_bytes.__name__,
            self.delete.__name__,
            self.move.__name__,
            self.list.__name__,
            self.append.__name__,
        ]
