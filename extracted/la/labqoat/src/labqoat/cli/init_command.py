"""Start a project directory with its files, checks, skills and Labqoat project in one step."""

from pathlib import Path

import click

from labqoat._generated.project_attributes import ProjectAttributes
from labqoat.cli.agent.agent_hooks import AgentHooks
from labqoat.cli.compute.enrollment.process_runner import ProcessRunner
from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.init.project_scaffold import ProjectScaffold
from labqoat.cli.output.error_reporter import ErrorReporter
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.cli.skills.skill_bundle import SkillBundle
from labqoat.cli.skills.skill_installer import SkillInstaller
from labqoat.cli.strict_command import StrictCommand
from labqoat.cli.version_info import VersionInfo
from labqoat.errors.api_error import ApiError
from labqoat.json_document import JsonDocument, JsonValue
from labqoat.projects.project_names import ProjectNames
from labqoat.projects.project_pin import ProjectPin


class InitCommand(StrictCommand):
    """Compose uv, git, the bundled skills and project creation; each step reports and none overwrites."""

    def __init__(self) -> None:
        """Take an optional name: a new subdirectory, or the current directory when omitted."""
        super().__init__(
            "init",
            help=(
                "Set up a project here, or in a new directory NAME: a uv project depending on this SDK for local "
                "tests, typed starter files, git with "
                "pre-commit checks, agent skills, and the Labqoat project pinned for the directory. Existing files "
                "are kept."
            ),
            params=[click.Argument(["name"], required=False)],
        )

    def invoke(self, ctx: click.Context) -> object:
        """Run every step even when one fails, then fail the process if any did."""
        directory, name = InitCommand.target(ctx.params["name"])
        scaffold = ProjectScaffold(directory, name, ProcessRunner(timeout_seconds=120.0))
        steps = [scaffold.python_project(), scaffold.sources(), InitCommand.pin(directory, name)]
        steps += [scaffold.sdk(VersionInfo.installed_version()), scaffold.checks()]
        steps += [InitCommand.skills(directory, agent) for agent in SkillInstaller.directories]
        steps += [InitCommand.hooks(directory), scaffold.repository(), InitCommand.remote(name)]
        passed = all(step["status"] != "failed" for step in steps)
        documents: list[JsonValue] = list(steps)
        report: dict[str, JsonValue] = {"directory": str(directory), "project": name, "steps": documents, "ok": passed}
        report["next"] = InitCommand.hints(name)
        ResultWriter().write_dict(report)
        if not passed:
            ctx.exit(1)
        return None

    @staticmethod
    def hints(name: str) -> list[JsonValue]:
        """What to do in the new project, alone and with several agents."""
        return [
            "lab run app.py  # prepare, train and evaluate the starter model",
            "export LABQOAT_AGENT=lead  # label memory writes; each agent uses its own name",
            f"git worktree add ../{name}-AGENT -b AGENT baseline-1  # one copy per agent; skills and checks come along",
            "skill labqoat-research: what to explore, and reference/swarm.md for several agents on one codebase",
        ]

    @staticmethod
    def target(name: str | None) -> tuple[Path, str]:
        """The directory to set up and the project it belongs to, validated before anything is written."""
        directory = Path.cwd() / name if name else Path.cwd()
        source = "the NAME argument" if name else "the current directory's name; pass a NAME"
        try:
            project = ProjectNames.project(directory.name, source)
        except ValueError as error:
            ErrorReporter.report_usage(str(error))
        directory.mkdir(exist_ok=True)
        return directory, project

    @staticmethod
    def pin(directory: Path, name: str) -> JsonDocument:
        """Select the project for every command run from the directory."""
        try:
            ProjectPin.write(directory, name)
        except ValueError as error:
            return ProjectScaffold.step("pin", "failed", str(error))
        return ProjectScaffold.step("pin", "done", f"[tool.labqoat] project = {name}")

    @staticmethod
    def hooks(directory: Path) -> JsonDocument:
        """Make Claude Code, Codex and opencode re-read the rules and check commands through `lab agent`."""
        changed = [name for agent in ("claude", "codex", "opencode") for name in AgentHooks.install(directory, agent)]
        if not changed:
            return ProjectScaffold.step("hooks", "kept", "agent rules and hooks already in place")
        return ProjectScaffold.step("hooks", "done", ", ".join(dict.fromkeys(changed)))

    @staticmethod
    def skills(directory: Path, agent: str) -> JsonDocument:
        """Install the bundled skills for one agent, leaving differing local copies alone."""
        try:
            installed = SkillInstaller(directory, agent).install(SkillBundle.contents(), SkillBundle.references())
        except click.ClickException as error:
            return ProjectScaffold.step(f"skills {agent}", "failed", error.message)
        status = "done" if installed["installed"] else "kept"
        return ProjectScaffold.step(f"skills {agent}", status, str(installed["path"]))

    @staticmethod
    def remote(name: str) -> JsonDocument:
        """Create the project on Labqoat; without a login the local setup still stands."""
        try:
            with ContextAccessor.current().client(project=name) as client:
                client.projects.put(name, ProjectAttributes())
        except (ApiError, click.ClickException) as error:
            later = f"run `lab auth login`, then `lab project init {name}`"
            return ProjectScaffold.step("project", "skipped", f"not created on Labqoat ({error}); {later}")
        return ProjectScaffold.step("project", "done", f"{name} exists on Labqoat")
