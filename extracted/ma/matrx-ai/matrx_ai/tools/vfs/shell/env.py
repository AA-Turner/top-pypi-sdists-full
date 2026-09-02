from __future__ import annotations

import os


class ShellEnv:
    __slots__ = (
        "cwd",
        "oldpwd",
        "vars",
        "exported",
        "last_exit",
        "pid",
        "last_bg_pid",
        "positional",
        "shell_opts",
        "script_name",
    )

    def __init__(
        self,
        *,
        cwd: str = "/home/user",
        env: dict[str, str] | None = None,
        positional: list[str] | None = None,
        script_name: str = "matrx-shell",
    ) -> None:
        defaults = {
            "PATH": "/usr/bin:/bin",
            "HOME": "/home/user",
            "PWD": cwd,
            "USER": "user",
            "LOGNAME": "user",
            "SHELL": "/bin/bash",
            "TERM": "dumb",
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
            "IFS": " \t\n",
            "OLDPWD": cwd,
        }
        if env:
            defaults.update(env)

        self.cwd: str = cwd
        self.oldpwd: str = defaults.get("OLDPWD", cwd)
        self.vars: dict[str, str] = defaults
        self.exported: set[str] = set(defaults.keys())
        self.last_exit: int = 0
        self.pid: int = 1234
        self.last_bg_pid: int = 0
        self.positional: list[str] = list(positional) if positional else []
        self.shell_opts: dict[str, bool] = {
            "errexit": False,
            "pipefail": False,
            "xtrace": False,
            "nullglob": False,
            "globstar": True,
            "nounset": False,
            "noglob": False,
        }
        self.script_name: str = script_name

    def get(self, name: str, default: str = "") -> str:
        return self.vars.get(name, default)

    def is_set(self, name: str) -> bool:
        return name in self.vars

    def set(self, name: str, value: str, export: bool = False) -> None:
        self.vars[name] = value
        if export:
            self.exported.add(name)
        if name == "PWD":
            self.cwd = value
        elif name == "OLDPWD":
            self.oldpwd = value

    def unset(self, name: str) -> None:
        self.vars.pop(name, None)
        self.exported.discard(name)

    def export(self, name: str) -> None:
        self.exported.add(name)

    def cd(self, path: str) -> None:
        # Caller is responsible for normalization (paths.normalize) — we just
        # update bookkeeping.
        prev = self.cwd
        self.cwd = path
        self.oldpwd = prev
        self.vars["PWD"] = path
        self.vars["OLDPWD"] = prev

    def child_env(self) -> dict[str, str]:
        return {k: v for k, v in self.vars.items() if k in self.exported}

    def copy(self) -> ShellEnv:
        new = ShellEnv.__new__(ShellEnv)
        new.cwd = self.cwd
        new.oldpwd = self.oldpwd
        new.vars = dict(self.vars)
        new.exported = set(self.exported)
        new.last_exit = self.last_exit
        new.pid = self.pid
        new.last_bg_pid = self.last_bg_pid
        new.positional = list(self.positional)
        new.shell_opts = dict(self.shell_opts)
        new.script_name = self.script_name
        return new

    @property
    def ifs(self) -> str:
        return self.vars.get("IFS", " \t\n")


def env_from_os() -> dict[str, str]:
    return {k: v for k, v in os.environ.items() if not k.startswith("_")}
