"""The C compiler `torch.compile` needs at run time, which slim Debian bases do not ship."""

import re
from collections.abc import Iterable
from pathlib import Path
from typing import ClassVar

from labqoat.compute.images.apt_step import AptStep
from labqoat.compute.images.operation import Operation


class Compiler:
    """Inductor builds kernels with a C compiler while a run trains, so an image with torch needs one."""

    PACKAGES: ClassVar[tuple[str, ...]] = ("build-essential=12.9",)
    USERS: ClassVar[frozenset[str]] = frozenset({"torch"})

    @classmethod
    def required(cls, names: Iterable[str]) -> bool:
        """Whether any installed distribution compiles kernels at run time."""
        return any(name.lower().replace("_", "-") in cls.USERS for name in names)

    @staticmethod
    def name(requirement: str) -> str:
        """The distribution name of a `name[extra]==version` requirement."""
        return re.split(r"[\[=<>~!; ]", requirement.strip(), maxsplit=1)[0]

    @classmethod
    def listed(cls, requirements: Path) -> tuple[str, ...]:
        """Distribution names in a requirements file; an unreadable file names none."""
        if not requirements.is_file():
            return ()
        lines = requirements.read_text(encoding="utf-8").splitlines()
        return tuple(cls.name(line) for line in lines if line.strip() and not line.lstrip().startswith(("#", "-")))

    @staticmethod
    def locked(project: Path) -> tuple[str, ...]:
        """Distribution names in a uv project's lock; a project without one names none."""
        lock = project / "uv.lock"
        if not lock.is_file():
            return ()
        return tuple(re.findall(r'^name = "([^"]+)"$', lock.read_text(encoding="utf-8"), flags=re.MULTILINE))

    @classmethod
    def present(cls, operations: Iterable[Operation]) -> bool:
        """Whether the recipe already installs the compiler."""
        return any(
            isinstance(step, AptStep) and any(package.startswith("build-essential=") for package in step.packages)
            for step in operations
        )
