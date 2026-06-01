"""Load RF command codes from Flipper ``.sub`` files."""

from __future__ import annotations

import asyncio
from pathlib import Path

from .commands import RadioFrequencyCommand
from .parser import parse_sub_content

_DEFAULT_BASE_DIR = Path(__file__).parent / "codes"


class CodeCollection:
    """A device's RF command codes on disk.

    Holds a resolved device directory. ``.sub`` files are not read until
    :meth:`load_command` is called.
    """

    def __init__(self, codes_dir: Path) -> None:
        """Store the resolved device directory."""
        self._codes_dir = codes_dir
        self._cache: dict[str, RadioFrequencyCommand] = {}

    def load_command(self, name: str) -> RadioFrequencyCommand:
        """Read and parse the ``.sub`` file for ``name``. Does I/O.

        Raises :class:`KeyError` if no command with that name exists.
        Cached per instance: subsequent calls with the same ``name`` return
        the previously-parsed command without re-reading the file.
        """
        if (cached := self._cache.get(name)) is not None:
            return cached
        sub_file = self._codes_dir / f"{name.lower()}.sub"
        if not sub_file.is_file():
            raise KeyError(f"No command {name!r} in {self._codes_dir}")
        cmd = parse_sub_content(sub_file.read_text())
        self._cache[name] = cmd
        return cmd

    async def async_load_command(self, name: str) -> RadioFrequencyCommand:
        """Async variant of :meth:`load_command`.

        Returns the cached command synchronously when available; otherwise
        reads and parses the ``.sub`` file in the default executor.
        """
        if (cached := self._cache.get(name)) is not None:
            return cached
        return await asyncio.get_running_loop().run_in_executor(
            None, self.load_command, name
        )

    def __repr__(self) -> str:
        """Return a concise representation."""
        return f"CodeCollection({self._codes_dir})"


def get_codes(name: str, base_dir: Path | str | None = None) -> CodeCollection:
    """Return a :class:`CodeCollection` for a named device.

    Resolves ``name`` as an identifier under ``base_dir`` (default: bundled
    codes directory) and verifies the directory exists and stays within
    ``base_dir``. No ``.sub`` files are read.
    """
    root = (Path(base_dir) if base_dir is not None else _DEFAULT_BASE_DIR).resolve()
    codes_dir = (root / name).resolve()
    if not codes_dir.is_relative_to(root):
        raise ValueError(f"{name!r} resolves outside of {root}")
    if not codes_dir.is_dir():
        raise FileNotFoundError(f"No codes directory at {codes_dir}")
    return CodeCollection(codes_dir)
