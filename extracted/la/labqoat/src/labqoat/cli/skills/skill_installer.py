"""Install bundled skills without silently replacing workspace content."""

from __future__ import annotations

import os
import tempfile
from collections.abc import Mapping
from pathlib import Path
from typing import ClassVar

import click

from labqoat.json_document import JsonDocument


class SkillInstaller:
    """Preflight workspace destinations and atomically write skill entrypoints."""

    directories: ClassVar[dict[str, str]] = {"codex": ".agents", "claude": ".claude"}

    def __init__(self, workspace: Path, agent: str, force: bool = False) -> None:
        """Select the workspace-local skill directory and replacement policy."""
        self.workspace = workspace.resolve()
        self.agent = agent
        self.target = self.workspace / self.directories[agent] / "skills"
        self.force = force

    def install(self, contents: Mapping[str, str], references: Mapping[str, str] | None = None) -> JsonDocument:
        """Validate every destination before changing any skill file; references sit beside their entrypoint."""
        documents = {f"{name}/SKILL.md": content for name, content in contents.items()} | dict(references or {})
        self._preflight(documents)
        changed = {
            relative.split("/", 1)[0] for relative, content in documents.items() if self._place(relative, content)
        }
        return JsonDocument(
            {
                "workspace": str(self.workspace),
                "agent": self.agent,
                "path": str(self.target),
                "installed": JsonDocument.expect_value([name for name in contents if name in changed]),
                "unchanged": JsonDocument.expect_value([name for name in contents if name not in changed]),
            }
        )

    def _place(self, relative: str, content: str) -> bool:
        """Write one file unless it already holds exactly this content."""
        path = self.target / relative
        if path.exists() and path.read_bytes() == content.encode("utf-8"):
            return False
        self._write(path, content)
        return True

    def _preflight(self, documents: Mapping[str, str]) -> None:
        """Reject conflicts, redirected paths, and non-directory parents."""
        self._directory(self.workspace)
        self._directory(self.target.parent)
        self._directory(self.target)
        for relative, content in documents.items():
            path = self.target / relative
            for parent in reversed(path.relative_to(self.target).parents[:-1]):
                self._directory(self.target / parent)
            if path.is_symlink() or (path.exists() and not path.is_file()):
                raise click.ClickException(f"Skill destination must be a regular file: {path}")
            if path.exists() and not self.force and path.read_bytes() != content.encode("utf-8"):
                raise click.ClickException(
                    f"Skill already exists with different content: {path}. Use --force to replace."
                )

    @staticmethod
    def _directory(path: Path) -> None:
        """Keep skill writes within real workspace directories."""
        if path.is_symlink() or (path.exists() and not path.is_dir()):
            raise click.ClickException(f"Skill destination must be a directory without symlinks: {path}")

    @staticmethod
    def _write(path: Path, content: str) -> None:
        """Atomically replace one skill, cleaning up incomplete temporary files."""
        path.parent.mkdir(parents=True, exist_ok=True)
        descriptor, name = tempfile.mkstemp(prefix=".SKILL.", dir=path.parent)
        temporary = Path(name)
        try:
            with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
                stream.write(content)
            temporary.replace(path)
        finally:
            temporary.unlink(missing_ok=True)
