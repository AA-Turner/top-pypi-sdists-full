"""Local setup of one project directory through uv and git."""

import re
from collections.abc import Sequence
from pathlib import Path
from typing import ClassVar

from labqoat.cli.compute.enrollment.command_result import CommandResult
from labqoat.cli.compute.enrollment.process_runner import ProcessRunner
from labqoat.cli.init.project_template import ProjectTemplate
from labqoat.cli.project_checks import ProjectChecks
from labqoat.json_document import JsonDocument


class ProjectScaffold:
    """Create only what a directory is missing; never overwrite a file or touch a repository it did not create."""

    tracked: ClassVar[tuple[str, ...]] = (
        "pyproject.toml",
        "uv.lock",
        ".agents/skills",
        ".claude/skills",
        ".claude/settings.json",
        ".codex/hooks.json",
        ".opencode/plugins",
        "AGENTS.md",
        "CLAUDE.md",
    )
    baseline: ClassVar[str] = "baseline-1"

    def __init__(self, directory: Path, name: str, runner: ProcessRunner) -> None:
        """Name the directory, its project and the process boundary."""
        self.directory = directory
        self.name = name
        self.runner = runner

    def python_project(self) -> JsonDocument:
        """Let uv write the project file when there is none."""
        if (self.directory / "pyproject.toml").exists():
            return self.step("pyproject", "kept", "pyproject.toml already exists")
        command = ["uv", "init", "--bare", "--no-workspace", "--name", self.name, "--directory", str(self.directory)]
        result = self.run(command)
        if not result.ok:
            return self.step("pyproject", "failed", f"uv init: {result.diagnostic()}")
        return self.step("pyproject", "done", "created by uv init")

    def sdk(self, version: str) -> JsonDocument:
        """Make `import labqoat` work in the project's own environment, so local tests run without PYTHONPATH."""
        pyproject = self.directory / "pyproject.toml"
        text = pyproject.read_text(encoding="utf-8") if pyproject.exists() else ""
        if re.search(r"""["']labqoat(?=[\s<>=!~\[;,"'])""", text):
            return self.step("sdk", "kept", "pyproject.toml already depends on labqoat")
        requirement = f"labqoat=={version}"
        result = self.run(["uv", "add", "--dev", "--directory", str(self.directory), requirement])
        if not result.ok:
            detail = f"uv add: {result.diagnostic()}; run `uv add --dev {requirement}` when online"
            return self.step("sdk", "skipped", detail)
        return self.step("sdk", "done", f"{requirement} in the dev group: `uv run pytest` can import labqoat")

    def checks(self) -> JsonDocument:
        """Add the strict format, lint and type settings and pin ruff and ty, unless the project has its own."""
        pyproject = self.directory / "pyproject.toml"
        text = pyproject.read_text(encoding="utf-8") if pyproject.exists() else ""
        if any(table in text for table in ("[tool.ruff", "[tool.ty", "[tool.labqoat.checks]")):
            return self.step("checks", "kept", "pyproject.toml already configures ruff or ty; not changed")
        pyproject.write_text(text.rstrip("\n") + "\n" + ProjectTemplate.text("checks.toml"), encoding="utf-8")
        tools = [f"ruff=={ProjectChecks.ruff}", f"ty=={ProjectChecks.ty}"]
        result = self.run(["uv", "add", "--dev", "--directory", str(self.directory), *tools])
        if not result.ok:
            return self.step("checks", "failed", f"uv add: {result.diagnostic()}; run `uv add --dev {' '.join(tools)}`")
        return self.step("checks", "done", "strict ruff and ty settings; `lab run` and pre-commit enforce them")

    def sources(self) -> JsonDocument:
        """Write each starter file that does not exist yet."""
        written = [path for path, content in ProjectTemplate.documents(self.name).items() if self.place(path, content)]
        if not written:
            return self.step("files", "kept", "every starter file already exists")
        return self.step("files", "done", ", ".join(written))

    def place(self, relative: str, content: str) -> bool:
        """Write one file unless something is already there."""
        path = self.directory / relative
        if path.exists():
            return False
        path.write_text(content, encoding="utf-8")
        return True

    def repository(self) -> JsonDocument:
        """Outside any repository: commit the project's own files, tag the baseline, then install the checks."""
        if self.git("rev-parse", "--is-inside-work-tree").ok:
            return self.step("git", "kept", "already inside a repository; nothing committed, no hook installed")
        present = [path for path in (*ProjectTemplate.documents(self.name), *self.tracked) if self.exists(path)]
        commands: tuple[tuple[str, ...], ...] = (
            ("init",),
            ("add", "--", *present),
            ("commit", "--message", "Start the project"),
            ("tag", self.baseline),
        )
        for command in commands:
            result = self.git(*command)
            if not result.ok:
                return self.step("git", "failed", f"git {command[0]}: {result.diagnostic()}")
        located = self.git("rev-parse", "--git-path", "hooks/pre-commit")
        if not located.ok:
            return self.step("git", "failed", f"git rev-parse: {located.diagnostic()}")
        hook = self.directory / located.output
        hook.parent.mkdir(parents=True, exist_ok=True)
        hook.write_text(ProjectTemplate.hook(), encoding="utf-8")
        hook.chmod(0o755)
        return self.step("git", "done", f"first commit tagged {self.baseline}; pre-commit runs the checks")

    def exists(self, relative: str) -> bool:
        """Whether a path this setup owns is present."""
        return (self.directory / relative).exists()

    def git(self, *arguments: str) -> CommandResult:
        """Run git in the project directory."""
        return self.run(["git", "-C", str(self.directory), *arguments])

    def run(self, command: Sequence[str]) -> CommandResult:
        """Run one tool; a tool that is not installed is a failed step, not a crash."""
        try:
            return self.runner.run(command)
        except OSError as error:
            return CommandResult(127, stderr=f"{command[0]} could not be started: {error}".encode())

    @staticmethod
    def step(name: str, status: str, detail: str) -> JsonDocument:
        """One line of the setup report."""
        return JsonDocument({"name": name, "status": status, "detail": detail})
