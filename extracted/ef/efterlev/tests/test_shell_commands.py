"""Tests for `efterlev.shell.commands` — registry, parsing, dispatch."""

from __future__ import annotations

from pathlib import Path

from rich.console import Console

from efterlev.shell.commands import (
    COMMANDS,
    ShellContext,
    find_command,
    parse_input,
)


def test_every_command_has_unique_name() -> None:
    names = [c.name for c in COMMANDS]
    assert len(names) == len(set(names))


def test_every_command_has_unique_aliases_disjoint_from_names() -> None:
    """No alias collides with any other command's canonical name or alias."""
    seen: set[str] = set()
    for c in COMMANDS:
        for name in (c.name, *c.aliases):
            assert name not in seen, f"duplicate slash token: {name}"
            seen.add(name)


def test_find_command_canonical() -> None:
    assert find_command("/scan") is not None
    assert find_command("/scan").name == "/scan"  # type: ignore[union-attr]


def test_find_command_alias() -> None:
    s = find_command("/s")
    assert s is not None
    assert s.name == "/scan"


def test_find_command_unknown() -> None:
    assert find_command("/nonexistent") is None
    assert find_command("scan") is None  # no leading slash


def test_parse_input_blank() -> None:
    assert parse_input("") is None
    assert parse_input("   ") is None


def test_parse_input_simple() -> None:
    result = parse_input("/scan")
    assert result == ("/scan", [])


def test_parse_input_with_args() -> None:
    result = parse_input("/import-security-hub findings.json")
    assert result == ("/import-security-hub", ["findings.json"])


def test_parse_input_with_quoted_arg() -> None:
    """shlex handles quoted args so /cd "path with spaces" works."""
    result = parse_input('/cd "path with spaces"')
    assert result == ("/cd", ["path with spaces"])


def test_parse_input_non_slash() -> None:
    """Non-slash input still parses; caller is responsible for the hint."""
    result = parse_input("scan")
    assert result == ("scan", [])


def test_help_lists_all_commands(tmp_path: Path, capsys) -> None:
    """`/help` with no args should output a line per registered command."""
    console = Console(force_terminal=False, width=120)
    ctx = ShellContext(root=tmp_path, console=console)
    cmd = find_command("/help")
    assert cmd is not None
    cmd.handler(ctx, [])
    out = capsys.readouterr().out
    for c in COMMANDS:
        assert c.name in out


def test_help_with_unknown_command_errors(tmp_path: Path, capsys) -> None:
    console = Console(force_terminal=False, width=120)
    ctx = ShellContext(root=tmp_path, console=console)
    cmd = find_command("/help")
    assert cmd is not None
    cmd.handler(ctx, ["/nonexistent"])
    out = capsys.readouterr().out
    assert "unknown command" in out


def test_status_command_does_not_change_state(tmp_path: Path, capsys) -> None:
    console = Console(force_terminal=False, width=120)
    ctx = ShellContext(root=tmp_path, console=console)
    cmd = find_command("/status")
    assert cmd is not None
    changed = cmd.handler(ctx, [])
    assert changed is False


def test_plan_and_catalog_are_registered_in_plan_phase() -> None:
    for name, alias in (("/plan", "/pl"), ("/catalog", "/cat")):
        cmd = find_command(name)
        assert cmd is not None
        assert cmd.phase == "plan"
        assert find_command(alias) is cmd


def test_plan_handler_dispatches_without_target(tmp_path: Path, monkeypatch) -> None:
    """Stage 0 commands are workspace-free — they must NOT pass --target, and
    they're read-only (no state change)."""
    import efterlev.shell.commands as commands_mod

    captured: list[list[str]] = []
    monkeypatch.setattr(
        commands_mod, "_dispatch_efterlev", lambda ctx, cmd: captured.append(cmd) or 0
    )
    console = Console(force_terminal=False, width=120)
    ctx = ShellContext(root=tmp_path, console=console)
    cmd = find_command("/plan")
    assert cmd is not None
    changed = cmd.handler(ctx, ["--architecture", "serverless"])
    assert changed is False
    assert captured == [["plan", "--architecture", "serverless"]]
    assert "--target" not in captured[0]


def test_catalog_handler_dispatches_without_target(tmp_path: Path, monkeypatch) -> None:
    import efterlev.shell.commands as commands_mod

    captured: list[list[str]] = []
    monkeypatch.setattr(
        commands_mod, "_dispatch_efterlev", lambda ctx, cmd: captured.append(cmd) or 0
    )
    console = Console(force_terminal=False, width=120)
    ctx = ShellContext(root=tmp_path, console=console)
    cmd = find_command("/catalog")
    assert cmd is not None
    changed = cmd.handler(ctx, ["--theme", "AFR"])
    assert changed is False
    assert captured == [["catalog", "--theme", "AFR"]]
    assert "--target" not in captured[0]


def test_cd_handler_changes_root(tmp_path: Path) -> None:
    target = tmp_path / "sub"
    target.mkdir()
    console = Console(force_terminal=False)
    ctx = ShellContext(root=tmp_path, console=console)
    cmd = find_command("/cd")
    assert cmd is not None
    changed = cmd.handler(ctx, [str(target)])
    assert changed is True
    assert ctx.root == target.resolve()


def test_cd_handler_rejects_nonexistent(tmp_path: Path, capsys) -> None:
    console = Console(force_terminal=False, width=120)
    ctx = ShellContext(root=tmp_path, console=console)
    cmd = find_command("/cd")
    assert cmd is not None
    changed = cmd.handler(ctx, [str(tmp_path / "does-not-exist")])
    assert changed is False
    assert "not a directory" in capsys.readouterr().out


def test_exit_handler_sets_should_exit(tmp_path: Path) -> None:
    console = Console(force_terminal=False)
    ctx = ShellContext(root=tmp_path, console=console)
    cmd = find_command("/exit")
    assert cmd is not None
    cmd.handler(ctx, [])
    assert ctx.should_exit is True


def test_quit_alias_maps_to_exit() -> None:
    assert find_command("/quit") is find_command("/exit")
    assert find_command(":q") is find_command("/exit")


def test_question_mark_alias_maps_to_help() -> None:
    assert find_command("?") is find_command("/help")


# v0.1.145 / #350: phase grouping + /map + /open


def test_every_command_has_a_known_phase() -> None:
    """Each command's `phase` must be one of the registered PHASES so the
    /help grouped output doesn't silently drop commands."""
    from efterlev.shell.commands import PHASES

    valid = {p for p, _ in PHASES}
    for c in COMMANDS:
        assert c.phase in valid, f"{c.name} has unknown phase {c.phase!r}"


def test_help_renders_phase_headers(tmp_path: Path, capsys) -> None:
    """`/help` should print the phase labels so the natural pipeline
    order is visible (not just an alphabetical dump)."""
    from efterlev.shell.commands import PHASES

    console = Console(force_terminal=False, width=120)
    ctx = ShellContext(root=tmp_path, console=console)
    cmd = find_command("/help")
    assert cmd is not None
    cmd.handler(ctx, [])
    out = capsys.readouterr().out
    for _, label in PHASES:
        # Match a leading word from each label so test isn't brittle to
        # punctuation tweaks.
        first_word = label.split()[0]
        assert first_word in out


def test_help_shows_state_markers(tmp_path: Path, capsys) -> None:
    """When uninitialized, the marker for /init should be → (next) and
    every downstream pipeline command should be ○ (pending)."""
    console = Console(force_terminal=False, width=120)
    ctx = ShellContext(root=tmp_path, console=console)
    cmd = find_command("/help")
    assert cmd is not None
    cmd.handler(ctx, [])
    out = capsys.readouterr().out
    # At least one marker symbol must appear.
    assert "→" in out or "○" in out
    # The legend explains the markers.
    assert "✓ done" in out
    assert "→ next" in out
    assert "○ pending" in out


def test_map_command_exists_and_prints_pipeline(tmp_path: Path, capsys) -> None:
    console = Console(force_terminal=False, width=120)
    ctx = ShellContext(root=tmp_path, console=console)
    cmd = find_command("/map")
    assert cmd is not None
    cmd.handler(ctx, [])
    out = capsys.readouterr().out
    # The map must list every pipeline command in order.
    for name in ("/init", "/scan", "/agent", "/report", "/readiness", "/package"):
        assert name in out
    # Subcommand annotation for /agent.
    assert "gap" in out and "document" in out and "remediate" in out


def test_open_no_args_shows_target_list(tmp_path: Path, capsys) -> None:
    console = Console(force_terminal=False, width=120)
    ctx = ShellContext(root=tmp_path, console=console)
    cmd = find_command("/open")
    assert cmd is not None
    cmd.handler(ctx, [])
    out = capsys.readouterr().out
    for target in ("reports", "gap", "docs", "poam", "oscal", "package", "workspace"):
        assert target in out


def test_open_unknown_target_errors(tmp_path: Path, capsys) -> None:
    console = Console(force_terminal=False, width=120)
    ctx = ShellContext(root=tmp_path, console=console)
    cmd = find_command("/open")
    assert cmd is not None
    cmd.handler(ctx, ["bogus-target"])
    out = capsys.readouterr().out
    assert "unknown" in out.lower()
    assert "valid:" in out.lower()


def test_open_target_with_missing_directory_errors(tmp_path: Path, capsys) -> None:
    """No `.efterlev/reports` yet → /open reports should error helpfully,
    not crash. Empty workspace is the common case for first-time users."""
    console = Console(force_terminal=False, width=120)
    ctx = ShellContext(root=tmp_path, console=console)
    cmd = find_command("/open")
    assert cmd is not None
    cmd.handler(ctx, ["reports"])
    out = capsys.readouterr().out
    # The error mentions "nothing to open"; rich may wrap "does not exist"
    # across lines depending on terminal width / path length, so match the
    # stable prefix instead.
    assert "nothing to open" in out
    assert "/scan" in out and "/report" in out  # hint mentions the unblock commands


def test_pipeline_state_marks_done_for_initialized_workspace(tmp_path: Path) -> None:
    """Sanity-check the per-command state computation: a workspace with
    a `.efterlev/` directory should mark /init as ✓ done."""
    from efterlev.shell.commands import _pipeline_state_for_commands
    from efterlev.shell.state import WorkspaceSnapshot

    (tmp_path / ".efterlev").mkdir()
    snap = WorkspaceSnapshot(
        root=tmp_path,
        initialized=True,
        baseline="fedramp-20x-moderate",
        evidence_count=0,
        claim_count=0,
        last_scan_at=None,
        cost_by_model={},
    )
    state = _pipeline_state_for_commands(snap, next_name="/scan")
    assert state["/init"] == "✓"
    assert state["/scan"] == "→"
    assert state["/agent"] == "○"
    assert state["/report"] == "○"
