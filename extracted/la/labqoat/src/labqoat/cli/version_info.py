"""Installed release identity and live source-checkout provenance."""

from __future__ import annotations

import os
import shutil
import subprocess
import tomllib
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from labqoat import __version__
from labqoat.json_document import JsonDocument


class VersionInfo:
    """Describe the executing package without consulting the caller's project."""

    @classmethod
    def label(cls) -> str:
        """Return a release number or a local version with revision and source path."""
        source = cls.source_project()
        if source is None:
            return cls.installed_version()
        root, release = source
        return f"{release}+local.{cls.revision(root)} ({root})"

    @staticmethod
    def source_project() -> tuple[Path, str] | None:
        """Recognize this package's source layout, including editable installs."""
        module = Path(__file__).resolve()
        root = module.parents[3]
        if module != root / "src" / "labqoat" / "cli" / "version_info.py":
            return None
        try:
            document = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
            project = JsonDocument.expect_dict(document.get("project"))
            if project.get("name") != "labqoat":
                return None
            return root, JsonDocument.expect_scalar(project["version"], str)
        except (OSError, ValueError, TypeError, KeyError):
            return None

    @staticmethod
    def installed_version() -> str:
        """Use distribution metadata, falling back when metadata is unavailable."""
        try:
            return version("labqoat")
        except PackageNotFoundError:
            return __version__

    @classmethod
    def revision(cls, root: Path) -> str:
        """Read the checkout's short commit and mark tracked package changes."""
        commit = cls.git_output(root, ("rev-parse", "--short=12", "HEAD"))
        if not commit:
            return "unknown"
        changes = cls.git_output(root, ("status", "--porcelain", "--untracked-files=no", "--", str(root)))
        suffix = ".dirty" if changes else ""
        return f"g{commit}{suffix}"

    @staticmethod
    def git_output(root: Path, arguments: tuple[str, ...]) -> str | None:
        """Run bounded, read-only Git commands against the executing checkout."""
        executable = shutil.which("git")
        if executable is None:
            return None
        environment = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
        try:
            result = subprocess.run(
                [executable, "-C", str(root), *arguments],
                env=environment,
                capture_output=True,
                text=True,
                check=True,
                timeout=1,
            )
            return result.stdout.strip()
        except (OSError, subprocess.SubprocessError):
            return None
