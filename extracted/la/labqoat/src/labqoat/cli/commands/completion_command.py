"""Generate and install Bash or Zsh completion."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING

import click

from labqoat.cli.group_help import GroupHelp
from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.output.json_writer import JsonWriter
from labqoat.cli.strict_command import StrictCommand

if TYPE_CHECKING:
    from click.shell_completion import ShellComplete


class CompletionCommand:
    """Own the completion group and managed shell-file installation."""

    name = "completion"
    managed_start = "# >>> labqoat completion >>>"
    managed_end = "# <<< labqoat completion <<<"

    @staticmethod
    def show(shell: str | None) -> None:
        """Render a completion script without changing files."""
        selected = CompletionCommand.selected_shell(shell)
        root = click.get_current_context().find_root().command
        complete = CompletionCommand.build_complete(selected, root, root.name or "lab")
        if ContextAccessor.current().output_mode == "human":
            click.echo(complete.source(), nl=False)
        else:
            JsonWriter().write(complete.source())

    @staticmethod
    def install(shell: str | None) -> None:
        """Install a completion script and managed shell-source block."""
        selected = CompletionCommand.selected_shell(shell)
        root = click.get_current_context().find_root().command
        complete = CompletionCommand.build_complete(selected, root, root.name or "lab")
        target, startup = CompletionCommand.install_files(selected, complete.source())
        if ContextAccessor.current().output_mode == "human":
            click.echo(f"Installed {selected} completion at {target}.")
            click.echo(f"Start a new shell or run: source {startup}")
        else:
            JsonWriter().write({"shell": selected, "path": str(target), "startup": str(startup)})

    @staticmethod
    def build_complete(shell: str, root: click.Command, name: str) -> ShellComplete:
        """Select the completion implementation for a supported shell."""
        import click.shell_completion as completion

        mapping = {"bash": completion.BashComplete, "zsh": completion.ZshComplete}
        factory = mapping.get(shell)
        if factory is None:
            raise click.UsageError(f"Unsupported shell: {shell}. Choose bash or zsh.")
        return factory(root, {}, name, "_LAB_COMPLETE")

    @staticmethod
    def selected_shell(explicit: str | None) -> str:
        """Resolve an explicit shell or detect Bash/Zsh from the environment."""
        selected = explicit or Path(os.environ.get("SHELL", "")).name
        if selected not in {"bash", "zsh"}:
            raise click.UsageError("Unable to detect Bash or Zsh; pass --shell explicitly.")
        return selected

    @staticmethod
    def install_files(shell: str, script: str) -> tuple[Path, Path]:
        """Write completion and an idempotent startup-file source block."""
        home = Path.home()
        data = Path(os.environ.get("XDG_DATA_HOME", home / ".local" / "share"))
        target = data / "labqoat" / "completions" / f"lab.{shell}"
        startup = home / (".bashrc" if shell == "bash" else ".zshrc")
        CompletionCommand.atomic_write(target, script)
        existing = startup.read_text(encoding="utf-8") if startup.exists() else ""
        CompletionCommand.atomic_write(startup, CompletionCommand.managed_content(existing, target))
        return target, startup

    @staticmethod
    def managed_content(existing: str, target: Path) -> str:
        """Insert or replace the single managed completion block."""
        block = f'{CompletionCommand.managed_start}\nsource "{target}"\n{CompletionCommand.managed_end}'
        start = existing.find(CompletionCommand.managed_start)
        end = existing.find(CompletionCommand.managed_end)
        if start >= 0 and end >= start:
            suffix = end + len(CompletionCommand.managed_end)
            updated = f"{existing[:start]}{block}{existing[suffix:]}"
        else:
            separator = "" if not existing or existing.endswith("\n") else "\n"
            updated = f"{existing}{separator}{block}\n"
        return updated if updated.endswith("\n") else f"{updated}\n"

    @staticmethod
    def atomic_write(path: Path, content: str) -> None:
        """Atomically replace a text file while retaining its mode."""
        path.parent.mkdir(parents=True, exist_ok=True)
        descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
        temporary = Path(temporary_name)
        try:
            with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
                stream.write(content)
            if path.exists():
                temporary.chmod(path.stat().st_mode)
            temporary.replace(path)
        finally:
            temporary.unlink(missing_ok=True)

    @staticmethod
    def shell_option() -> click.Option:
        """Create the optional Bash/Zsh selector."""
        return click.Option(["--shell"], type=click.Choice(["bash", "zsh"]))

    @classmethod
    def as_click_command(cls) -> click.Group:
        """Build the help-first completion group."""
        group = click.Group(
            cls.name,
            callback=GroupHelp.show,
            help="Generate or install shell completion.",
            invoke_without_command=True,
        )
        group.add_command(StrictCommand("show", callback=cls.show, params=[cls.shell_option()]))
        group.add_command(StrictCommand("install", callback=cls.install, params=[cls.shell_option()]))
        return group
