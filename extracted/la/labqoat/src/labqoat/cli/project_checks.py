"""The format, lint and type checks a strict project passes before any of its code runs on Labqoat."""

import tomllib
from pathlib import Path
from typing import ClassVar

from labqoat.cli.compute.enrollment.process_runner import ProcessRunner
from labqoat.cli.output.cli_failure import CliFailure


class ProjectChecks:
    """Run the project's own pinned ruff and ty; a failure keeps the launch from being submitted."""

    ruff = "0.17.2"
    ty = "0.0.91"
    commands: ClassVar[tuple[tuple[str, ...], ...]] = (
        ("ruff", "format", "--check", "."),
        ("ruff", "check", "--output-format", "concise", "."),
        ("ty", "check", "--output-format", "concise"),
    )
    shown = 40

    @staticmethod
    def root(source: Path) -> Path | None:
        """The nearest directory at or above ``source`` holding a pyproject.toml."""
        for directory in (source.resolve().parent, *source.resolve().parents):
            if (directory / "pyproject.toml").is_file():
                return directory
        return None

    @staticmethod
    def strict(root: Path) -> bool:
        """Whether the project asked for checks with ``[tool.labqoat.checks] strict = true``."""
        try:
            document = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
        except (OSError, tomllib.TOMLDecodeError):
            return False
        checks = document.get("tool", {}).get("labqoat", {}).get("checks", {})
        return isinstance(checks, dict) and checks.get("strict") is True

    @classmethod
    def enforce(cls, source: Path, runner: ProcessRunner) -> None:
        """Run every check for the project that owns ``source``, and refuse the launch if any fails."""
        root = cls.root(source)
        if root is None or not cls.strict(root):
            return
        failed: list[str] = []
        for command in cls.commands:
            result = runner.run(["uv", "run", "--quiet", "--frozen", "--directory", str(root), *command])
            if not result.ok:
                text = (result.stdout + result.stderr).decode(errors="replace").strip()
                failed.append(f"$ {' '.join(command)}\n{text}")
        if failed:
            raise CliFailure(cls.report(failed), 1)

    @classmethod
    def report(cls, failed: list[str]) -> str:
        """The first findings and how to fix them, bounded so a broken tree does not flood the reader."""
        lines = "\n\n".join(failed).splitlines()
        hidden = len(lines) - cls.shown
        shown = "\n".join(lines[: cls.shown]) + (f"\n... {hidden} more lines" if hidden > 0 else "")
        return (
            f"{shown}\n\nNothing was submitted: this project's checks failed ([tool.labqoat.checks] in "
            "pyproject.toml). `uv run ruff format . && uv run ruff check --fix .` fixes most findings; fix the "
            f"rest in the code. Missing tools: `uv add --dev ruff=={cls.ruff} ty=={cls.ty}`."
        )
