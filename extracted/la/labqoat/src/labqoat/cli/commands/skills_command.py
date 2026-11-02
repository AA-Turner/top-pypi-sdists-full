"""Install end-user agent guidance into a selected workspace."""

from pathlib import Path

import click

from labqoat.cli.agent.agent_hooks import AgentHooks
from labqoat.cli.group_help import GroupHelp
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.cli.skills.skill_bundle import SkillBundle
from labqoat.cli.skills.skill_installer import SkillInstaller
from labqoat.cli.strict_command import StrictCommand
from labqoat.json_document import JsonValue


class SkillsCommand:
    """Expose offline, workspace-local installation through the CLI."""

    @staticmethod
    def install(workspace: Path, agent: str, force: bool) -> None:
        """Install packaged skills and report changed and unchanged entrypoints."""
        result = SkillInstaller(workspace, agent, force).install(SkillBundle.contents(), SkillBundle.references())
        agents = (agent, "opencode") if agent == "codex" else (agent,)
        hooks: list[JsonValue] = [name for each in agents for name in AgentHooks.install(workspace.resolve(), each)]
        result["hooks"] = hooks
        ResultWriter().write_dict(result)

    @staticmethod
    def as_click_command() -> click.Group:
        """Build the skills group with explicit destination and overwrite options."""
        group = click.Group(
            "skills",
            help="Install Labqoat workflow skills for AI agents.",
            callback=GroupHelp.show,
            invoke_without_command=True,
        )
        group.add_command(
            StrictCommand(
                "install",
                callback=SkillsCommand.install,
                help="Install bundled agent skills locally; works offline.",
                params=SkillsCommand.options(),
            )
        )
        return group

    @staticmethod
    def options() -> list[click.Parameter]:
        """Declare portable workspace installation without global configuration changes."""
        return [
            click.Option(
                ["--workspace"],
                type=click.Path(exists=True, file_okay=False, path_type=Path),
                default=".",
                show_default=True,
                help="Workspace directory; defaults to the current directory.",
            ),
            click.Option(
                ["--agent"],
                type=click.Choice(tuple(SkillInstaller.directories)),
                default="codex",
                show_default=True,
                help="codex: .agents/skills (portable agent skills); claude: .claude/skills.",
            ),
            click.Option(
                ["--force"], is_flag=True, help="Replace differing bundled SKILL.md files; preserve other files."
            ),
        ]
