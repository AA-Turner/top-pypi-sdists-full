"""Ordered Docker context rules with recursive globs and parent-directory matching."""

import fnmatch
from pathlib import PurePosixPath


class ContextIgnore:
    """Match relative context paths using Dockerfile-specific or root ignore declarations."""

    def __init__(self, text: str) -> None:
        """Compile ordered include/exclude rules without reading the filesystem."""
        self._rules: list[tuple[bool, tuple[str, ...]]] = []
        for line in text.lstrip("\ufeff").splitlines():
            if not line.strip() or line.startswith("#"):
                continue
            pattern = line.strip()
            include = pattern.startswith("!")
            pattern = pattern.removeprefix("!").strip().strip("/")
            if pattern and pattern != ".":
                self._rules.append((include, PurePosixPath(pattern).parts))

    def includes(self, path: PurePosixPath) -> bool:
        """Apply the last matching rule to a path or any of its containing directories."""
        included = True
        names = [path.parts, *(parent.parts for parent in path.parents if parent != PurePosixPath("."))]
        for include, pattern in self._rules:
            if any(self._matches(pattern, name) for name in names):
                included = include
        return included

    @classmethod
    def _matches(cls, pattern: tuple[str, ...], path: tuple[str, ...]) -> bool:
        """Match ordinary wildcards within segments and recursive wildcards across whole directories."""
        if not pattern:
            return not path
        if pattern[0] == "**":
            return cls._matches(pattern[1:], path) or bool(path and cls._matches(pattern, path[1:]))
        return bool(path and fnmatch.fnmatchcase(path[0], pattern[0]) and cls._matches(pattern[1:], path[1:]))
