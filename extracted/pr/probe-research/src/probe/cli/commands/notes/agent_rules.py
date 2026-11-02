"""probe agent-rules refresh: rewrite the managed instruction block when it is stale."""

from __future__ import annotations
import sys

import typer

rules_app = typer.Typer(
    no_args_is_help=True, help="the managed Probe block in your agent's memory file"
)


@rules_app.command("refresh")
def agent_rules_refresh() -> None:
    """Rewrite the managed block when it is older than this CLI, or when its
    research-plan-review paragraph still has the retired opt-out (then
    `from_version` equals `to_version`).

    THE MIGRATION CHANNEL for a file no release can reach. The block lives in the
    researcher's own CLAUDE.md or AGENTS.md, so a release that changes what the
    block should say cannot change what it does say -- every machine keeps
    instructing its agent with whatever was installed the day the wizard last
    ran.

    THE AUTOMATIC CHANNEL IS `notes sync`, not this command and not a hook. This
    docstring used to claim the session-start hook called this; it never did, in
    any shipped plugin, so bumping POINTER_VERSION corrected nothing and the
    block only ever moved when somebody ran this by hand. Wiring a hook would
    have repeated the fault it was fixing -- hooks ship in the PLUGIN, so the fix
    would reach a machine only after a plugin release AND a session restart. The
    team-note sync is CLI-side, already fires on every Stop, and already holds
    each instruction file's lock, so `refresh_pointer` rides it and lands with
    the CLI. This command stays as the explicit, inspectable path.

    THREE THINGS IT WILL NOT DO. It will not install a block into a file that
    never had one: that is the wizard's moment, with the researcher's consent,
    and a hook that adds instructions to somebody's memory file uninvited is a
    different act from keeping an existing one current. It will not touch a file
    whose markers are damaged, because the only safe response to "I cannot tell
    which bytes are mine" is to leave all of them alone. And it holds a lock
    while it works, because the block rewrite is a whole-file read-modify-write
    and several agent sessions can share one home directory.
    """
    from ....foundation.durable.durable import file_lock
    from ...wizard.apply import agent_rules
    from ....shared.notes.team_note.render import instruction_lock_path

    path = agent_rules.memory_path()
    try:
        # THE SAME LOCK the note sync takes, keyed on the file. This used to
        # take a single global `agent-rules.lock` while the note sync took a
        # per-file one -- two writers of one file serialising against different
        # locks, which is no lock at all for a whole-file read-modify-write.
        with file_lock(instruction_lock_path(path)):
            installed = agent_rules.installed_version(path)
            state = agent_rules.refresh_pointer(path)
            if state != agent_rules.POINTER_REFRESHED:
                _print_json({"path": str(path), "state": state, "changed": False})
                return
            changed = True
    except agent_rules.DamagedBlock as exc:
        print(f"left {path} alone: {exc}", file=sys.stderr)
        _print_json({"path": str(path), "state": "damaged", "changed": False})
        raise typer.Exit(2) from None
    except (OSError, UnicodeDecodeError) as exc:
        print(f"could not update {path}: {exc}", file=sys.stderr)
        _print_json({"path": str(path), "state": "unwritable", "changed": False})
        raise typer.Exit(1) from None
    _print_json(
        {
            "path": str(path),
            "state": "refreshed",
            "changed": changed,
            "from_version": installed,
            "to_version": agent_rules.POINTER_VERSION,
        }
    )
from probe.cli.commands.json_print import _print_json  # noqa: E402 -- pieces need each other; the front door loads this one first
