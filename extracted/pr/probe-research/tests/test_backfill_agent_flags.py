"""The agent binary is a dependency, and its option set is the contract.

`probe` hands the agent CLI a fixed argv. An agent CLI parses options strictly:
one it does not recognise is a non-zero exit before it reads a single file.

Anthrogen, 2026-08-12. `--autocompact` landed in #194 six days earlier; their
Claude Code predated it; all 33 classify slices died identically with
`error: unknown option '--autocompact'`, and the import reported only "the
classification did not produce a usable plan". Nothing was imported, after a
wait long enough to be its own bug.

Two properties matter here, and they pull in opposite directions:

  * a flag the binary cannot parse must never be passed
  * a probe that FAILS must never be the reason a flag is dropped

The second is the one that is easy to get wrong. A timeout on a loaded machine
silently stripping the confinement flags would turn a slow laptop into an
unconfined import, which is worse than the bug being fixed.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from probe.cli import backfill as bf

FULL_HELP = """Usage: claude [options] [command] [prompt]
  -p, --print                  Print response and exit
  --output-format <format>     Output format
  --verbose                    Override verbose mode
  --allowedTools <tools...>    Comma separated list
  --add-dir <directories...>   Additional directories
  --settings <file-or-json>    Path to a settings JSON
  --session-id <uuid>          Use a specific session ID
  -r, --resume [sessionId]     Resume a conversation
  --autocompact <auto|tokens>  Auto-compact window size
  --strict-mcp-config          Only use MCP servers from --mcp-config
  --disable-slash-commands     Disable slash commands
"""

#: The same help minus the three flags that landed most recently -- i.e. the
#: binary Anthrogen actually had.
OLD_HELP = "\n".join(
    ln
    for ln in FULL_HELP.splitlines()
    if not any(
        f in ln for f in ("--autocompact", "--strict-mcp-config", "--disable-slash-commands")
    )
)


def _clear_probe_caches():
    """`cache_clear` only exists while the real lru_cache is in place.

    A test that monkeypatches one of these swaps in a plain function, and
    teardown then dies on the missing attribute -- taking the real assertion
    failure with it and reporting an unrelated AttributeError instead.
    """
    for name in ("_supported_flags_cached", "_agent_version_cached"):
        clear = getattr(getattr(bf, name), "cache_clear", None)
        if clear is not None:
            clear()


@pytest.fixture(autouse=True)
def _no_cache():
    """One `--help` per binary per PROCESS is the point; per test it is a trap."""
    _clear_probe_caches()
    yield
    _clear_probe_caches()


def _binary(tmp_path: Path, help_text: str, *, version="2.1.231 (Claude Code)", help_rc=0) -> str:
    """A stand-in agent binary that answers --help and --version and nothing else."""
    path = tmp_path / "claude"
    path.write_text(
        "#!/bin/sh\n"
        f'if [ "$1" = "--help" ]; then cat <<\'H\'\n{help_text}\nH\n  exit {help_rc}; fi\n'
        f'if [ "$1" = "--version" ]; then echo "{version}"; exit 0; fi\n'
        "echo \"error: unknown option '$1'\" >&2; exit 1\n"
    )
    path.chmod(0o755)
    return str(path)


# -- the probe ---------------------------------------------------------------


def test_a_current_binary_is_missing_nothing(tmp_path):
    binary = _binary(tmp_path, FULL_HELP)
    assert bf.unsupported_flags(bf.Agent.CLAUDE, binary) == ([], [])
    assert bf.too_old(bf.Agent.CLAUDE, binary) is None


def test_the_binary_anthrogen_had_is_missing_exactly_the_new_flags(tmp_path):
    binary = _binary(tmp_path, OLD_HELP, version="2.0.9 (Claude Code)")
    required, optional = bf.unsupported_flags(bf.Agent.CLAUDE, binary)
    assert required == []
    assert optional == ["--autocompact", "--strict-mcp-config", "--disable-slash-commands"]


def test_that_binary_is_not_refused_it_is_degraded(tmp_path):
    """None of the three is load-bearing for correctness or confinement.

    Refusing to import a researcher's folder over a compaction hint is the
    wrong trade -- the import runs, and says what it is running without.
    """
    binary = _binary(tmp_path, OLD_HELP)
    assert bf.too_old(bf.Agent.CLAUDE, binary) is None


def test_a_binary_missing_confinement_IS_refused(tmp_path):
    """`--add-dir` + `--settings` ARE the Claude half of CONFINEMENT. Running
    without them is running unconfined over somebody's research folder, which
    this module refuses to do elsewhere too."""
    help_text = "\n".join(ln for ln in FULL_HELP.splitlines() if "--settings" not in ln)
    binary = _binary(tmp_path, help_text)
    message = bf.too_old(bf.Agent.CLAUDE, binary)
    assert message is not None
    assert "--settings" in message
    assert "Upgrade" in message
    assert "nothing was read" in message


# -- the probe failing must never strip a flag -------------------------------


def test_a_help_that_exits_nonzero_leaves_the_argv_alone(tmp_path):
    binary = _binary(tmp_path, FULL_HELP, help_rc=3)
    assert bf.supported_flags(binary) is None
    assert bf.unsupported_flags(bf.Agent.CLAUDE, binary) == ([], [])


def test_a_help_that_times_out_leaves_the_argv_alone(tmp_path, monkeypatch):
    def hang(*a, **k):
        raise subprocess.TimeoutExpired(cmd="claude --help", timeout=1)

    monkeypatch.setattr(bf.subprocess, "run", hang)
    assert bf.supported_flags("/nope/claude") is None


def test_a_missing_binary_leaves_the_argv_alone(tmp_path):
    assert bf.supported_flags(str(tmp_path / "not-here")) is None


def test_help_text_we_cannot_parse_is_unknown_not_empty(tmp_path):
    """An empty parse means we did not understand the output, NOT that the
    binary has no options. Treating it as "supports nothing" strips every
    flag -- including the confinement pair."""
    binary = _binary(tmp_path, "some banner with no options at all")
    assert bf.supported_flags(binary) is None
    assert bf.unsupported_flags(bf.Agent.CLAUDE, binary) == ([], [])


def test_unknown_support_still_passes_every_flag(tmp_path):
    """The composed guarantee: probe failure == today's behaviour, exactly."""
    assert bf._has(None, "--autocompact") is True
    assert bf._has(frozenset({"--autocompact"}), "--autocompact") is True
    assert bf._has(frozenset(), "--autocompact") is False


# -- the argv ----------------------------------------------------------------


def test_the_argv_drops_only_what_the_binary_cannot_parse(tmp_path):
    binary = _binary(tmp_path, OLD_HELP)
    argv = bf.agent_argv(bf.Agent.CLAUDE, binary, tmp_path, workdir=tmp_path / "w")
    assert "--autocompact" not in argv
    assert "--strict-mcp-config" not in argv
    assert "--disable-slash-commands" not in argv
    # Everything load-bearing survives.
    assert "--add-dir" in argv and "--settings" in argv
    assert "--output-format" in argv and "--allowedTools" in argv


def test_the_argv_keeps_everything_on_a_current_binary(tmp_path):
    binary = _binary(tmp_path, FULL_HELP)
    argv = bf.agent_argv(bf.Agent.CLAUDE, binary, tmp_path, workdir=tmp_path / "w")
    assert argv[argv.index("--autocompact") + 1] == "auto"
    assert "--strict-mcp-config" in argv and "--disable-slash-commands" in argv


def test_a_dropped_flag_is_said_out_loud(tmp_path, monkeypatch):
    binary = _binary(tmp_path, OLD_HELP)
    monkeypatch.setattr(bf, "which_agent", lambda a: binary)
    note = bf.degraded_note(bf.Agent.CLAUDE)
    assert note is not None
    assert "--autocompact" in note
    assert "isolation" in note


def test_nothing_is_said_when_nothing_was_dropped(tmp_path, monkeypatch):
    """A note on every import is a note nobody reads."""
    binary = _binary(tmp_path, FULL_HELP)
    monkeypatch.setattr(bf, "which_agent", lambda a: binary)
    assert bf.degraded_note(bf.Agent.CLAUDE) is None


# -- the gate ----------------------------------------------------------------


def test_an_unusable_agent_is_refused_before_the_folder_is_walked(tmp_path, monkeypatch):
    """The whole point of the timing. Per-invocation is correct and useless:
    the walk is minutes on these drives, and Anthrogen found out afterwards --
    33 times, once per slice."""
    help_text = "\n".join(ln for ln in FULL_HELP.splitlines() if "--add-dir" not in ln)
    binary = _binary(tmp_path, help_text)
    monkeypatch.setattr(bf, "which_agent", lambda a: binary)

    chosen, error = bf.resolve_agent(bf.Agent.CLAUDE, interactive=False)
    assert chosen is None
    assert error is not None and "--add-dir" in error


def test_a_usable_agent_still_resolves(tmp_path, monkeypatch):
    binary = _binary(tmp_path, FULL_HELP)
    monkeypatch.setattr(bf, "which_agent", lambda a: binary)
    chosen, error = bf.resolve_agent(bf.Agent.CLAUDE, interactive=False)
    assert chosen is bf.Agent.CLAUDE and error is None


def test_an_unusable_agent_is_not_offered_as_a_choice(tmp_path, monkeypatch):
    """And the refusal says WHY. "No coding agent found" would send someone to
    install what is already sitting on their PATH."""
    help_text = "\n".join(ln for ln in FULL_HELP.splitlines() if "--add-dir" not in ln)
    binary = _binary(tmp_path, help_text)
    monkeypatch.setattr(bf, "which_agent", lambda a: binary)
    monkeypatch.setattr(bf, "available_agents", lambda: [bf.Agent.CLAUDE])

    chosen, error = bf.resolve_agent(None, interactive=False)
    assert chosen is None
    assert error is not None
    assert "too old" in error and "not on PATH" not in error


# -- the version, so the next one is visible ---------------------------------


def test_the_agent_version_is_recorded_not_just_a_boolean(tmp_path, monkeypatch):
    binary = _binary(tmp_path, FULL_HELP, version="2.1.231 (Claude Code)")
    monkeypatch.setattr(bf, "which_agent", lambda a: binary)
    assert bf.agent_version(bf.Agent.CLAUDE) == "2.1.231"


def test_a_version_with_no_number_still_returns_something(tmp_path, monkeypatch):
    binary = _binary(tmp_path, FULL_HELP, version="nightly-build")
    monkeypatch.setattr(bf, "which_agent", lambda a: binary)
    assert bf.agent_version(bf.Agent.CLAUDE) == "nightly-build"


def test_an_absent_binary_has_no_version(monkeypatch):
    monkeypatch.setattr(bf, "which_agent", lambda a: None)
    assert bf.agent_version(bf.Agent.CLAUDE) is None


def test_the_probe_runs_once_per_binary_not_once_per_unit(tmp_path, monkeypatch):
    """An import launches one agent per unit. A `--help` per launch would add a
    subprocess to every one of them."""
    binary = _binary(tmp_path, FULL_HELP)
    calls = []
    real = bf.subprocess.run

    def counted(argv, *a, **k):
        calls.append(argv)
        return real(argv, *a, **k)

    monkeypatch.setattr(bf.subprocess, "run", counted)
    for _ in range(5):
        bf.supported_flags(binary)
    assert len([c for c in calls if c[-1] == "--help"]) == 1


# -- the doctor wiring -------------------------------------------------------


def test_doctor_maps_its_own_agent_spelling_to_the_enum(tmp_path, monkeypatch):
    """`agent_source()` says "claude_code"; `Agent` says "claude".

    Passing the first straight to `Agent(...)` raises, the fail-soft `except`
    swallows it, and the field reads None on every machine forever -- a probe
    that reports nothing while looking like it works. Caught by running
    `doctor` for real, not by any unit test of `agent_version`.
    """
    from probe.cli import doctor

    binary = _binary(tmp_path, FULL_HELP, version="2.1.231 (Claude Code)")
    monkeypatch.setattr(bf, "which_agent", lambda a: binary)

    assert doctor._agent_version("claude_code") == "2.1.231"
    assert doctor._agent_version("codex") == "2.1.231"  # same stub binary


def test_doctor_shows_the_version_beside_the_tick(tmp_path):
    from probe.cli import doctor
    from probe.cli.capabilities import Capabilities

    caps = Capabilities(agent_source="claude_code", claude_available=True, agent_version="2.1.231")
    assert "ok (2.1.231)" in doctor.render(caps)


def test_doctor_says_nothing_extra_when_the_version_is_unknown(tmp_path):
    from probe.cli import doctor
    from probe.cli.capabilities import Capabilities

    caps = Capabilities(agent_source="claude_code", claude_available=True)
    line = next(ln for ln in doctor.render(caps).splitlines() if "Claude Code CLI" in ln)
    assert line.strip().endswith("ok")


# -- the flags are not all on the root command -------------------------------


def _codex(tmp_path: Path) -> str:
    """A stand-in Codex: our flags live on `exec`, not the root command.

    This is the real shape. `codex --help` lists --sandbox, --config, --cd and
    friends; `--json` and `--skip-git-repo-check` appear only under
    `codex exec --help`.
    """
    path = tmp_path / "codex"
    path.write_text(
        "#!/bin/sh\n"
        'if [ "$1" = "exec" ] && [ "$2" = "--help" ]; then\n'
        "  printf '%s\\n' 'Usage: codex exec [OPTIONS]' '  --json  Emit JSONL'"
        " '  --skip-git-repo-check  Allow outside a repo' '  -C, --cd <DIR>  Working dir'\n"
        "  exit 0; fi\n"
        'if [ "$1" = "--help" ]; then\n'
        "  printf '%s\\n' 'Usage: codex [OPTIONS]' '  --sandbox <MODE>  Sandbox policy'"
        " '  --config <K=V>  Override' '  --cd <DIR>  Working dir'\n"
        "  exit 0; fi\n"
        'if [ "$1" = "--version" ]; then echo "codex-cli 0.24.0"; exit 0; fi\n'
        "echo \"error: unexpected argument '$1'\" >&2; exit 1\n"
    )
    path.chmod(0o755)
    return str(path)


def test_codex_is_probed_on_exec_not_on_the_root_command(tmp_path):
    """THE BUG THIS PINS: probing `codex --help` finds neither of our flags,
    because they belong to the `exec` subcommand.

    That does not fail open -- the root command answers rc 0 with a real
    option list, so the parse succeeds and every flag we need reads as
    missing. `too_old` then refuses EVERY Codex install, current ones
    included, with an upgrade instruction that cannot possibly help.
    """
    binary = _codex(tmp_path)
    root = bf._supported_flags_cached(binary, ("--help",))
    assert root is not None and "--json" not in root, "fixture must mirror real codex"

    required, optional = bf.unsupported_flags(bf.Agent.CODEX, binary)
    assert required == [], "a current Codex must not be called too old"
    assert optional == []
    assert bf.too_old(bf.Agent.CODEX, binary) is None


def test_a_codex_only_machine_can_still_run_a_backfill(tmp_path, monkeypatch):
    """The consequence of getting the subcommand wrong: `usable` is empty and
    backfill stops working on every Codex-only box."""
    binary = _codex(tmp_path)
    monkeypatch.setattr(bf, "which_agent", lambda a: binary if a is bf.Agent.CODEX else None)
    monkeypatch.setattr(bf, "available_agents", lambda: [bf.Agent.CODEX])

    chosen, error = bf.resolve_agent(None, interactive=False)
    assert error is None
    assert chosen is bf.Agent.CODEX


def test_both_agents_installed_still_reaches_the_picker(tmp_path, monkeypatch):
    """A false 'too old' on one agent collapses `usable` to length 1, and the
    `len(usable) == 1` short-circuit then skips `choose_agent` entirely -- the
    picker silently vanishes and the user is handed an agent they never chose."""
    claude = _binary(tmp_path, FULL_HELP)
    codex_dir = tmp_path / "cx"
    codex_dir.mkdir()
    codex = _codex(codex_dir)
    monkeypatch.setattr(bf, "which_agent", lambda a: claude if a is bf.Agent.CLAUDE else codex)
    monkeypatch.setattr(bf, "available_agents", lambda: [bf.Agent.CLAUDE, bf.Agent.CODEX])
    asked = []
    monkeypatch.setattr(bf, "choose_agent", lambda avail: asked.append(avail) or avail[0])
    from probe.cli import tui

    monkeypatch.setattr(tui, "clear", lambda: None)

    bf.resolve_agent(None, interactive=True)
    assert asked == [[bf.Agent.CLAUDE, bf.Agent.CODEX]], "the picker must still offer both"


# -- prose is not support ----------------------------------------------------


def test_a_flag_named_only_in_another_options_description_is_not_support(tmp_path):
    """`claude --help` cross-references flags inside other options' prose --
    three of them today. Reading a mention as support passes a flag the binary
    rejects, which is the guard reproducing the exact crash it exists to stop.
    """
    help_text = (
        "Usage: claude [options]\n"
        "  --output-format <f>   Output format\n"
        "  --verbose             Verbose\n"
        "  --allowedTools <t>    Tools\n"
        "  --add-dir <d>         Dirs\n"
        "  --settings <s>        Settings\n"
        "  --session-id <u>      Session\n"
        "  -r, --resume [s]      Resume\n"
        "  --bare                Strips --autocompact, --strict-mcp-config and\n"
        "                        --disable-slash-commands from the run\n"
    )
    binary = _binary(tmp_path, help_text)
    supported = bf.supported_flags(binary)
    assert "--bare" in supported, "a real definition line is support"
    assert "--autocompact" not in supported, "a mention in prose is not"

    argv = bf.agent_argv(bf.Agent.CLAUDE, binary, tmp_path, workdir=tmp_path / "w")
    assert "--autocompact" not in argv


def test_a_short_form_before_the_long_form_still_parses(tmp_path):
    binary = _binary(tmp_path, FULL_HELP)
    assert "--resume" in bf.supported_flags(binary), "`-r, --resume` must be seen"


# -- the message names the version it found ----------------------------------


def test_the_refusal_names_the_version_it_found(tmp_path):
    """ "Upgrade Claude Code" is advice the reader cannot check against anything.

    They do not know what they have -- and until 0.79.0 neither did we, because
    `doctor` recorded a boolean. With the number in the sentence they can
    compare it to the release notes, and a bug report carries the one fact that
    would otherwise cost a round trip.
    """
    help_text = "\n".join(ln for ln in FULL_HELP.splitlines() if "--settings" not in ln)
    binary = _binary(tmp_path, help_text, version="1.0.4 (Claude Code)")
    message = bf.too_old(bf.Agent.CLAUDE, binary)
    assert "This Claude Code (1.0.4) is too old" in message


def test_the_degraded_note_names_it_too(tmp_path, monkeypatch):
    binary = _binary(tmp_path, OLD_HELP, version="2.0.9 (Claude Code)")
    monkeypatch.setattr(bf, "which_agent", lambda a: binary)
    note = bf.degraded_note(bf.Agent.CLAUDE)
    assert note.startswith("This Claude Code (2.0.9) does not accept")


def test_an_unreadable_version_is_omitted_not_guessed(tmp_path, monkeypatch):
    """`This Claude Code (unknown)` reads like a broken install on top of an
    old one, which is a second problem the reader does not have."""
    help_text = "\n".join(ln for ln in FULL_HELP.splitlines() if "--settings" not in ln)
    binary = _binary(tmp_path, help_text)
    monkeypatch.setattr(bf, "_agent_version_cached", lambda b: None)
    message = bf.too_old(bf.Agent.CLAUDE, binary)
    assert message.startswith("This Claude Code is too old")
    assert "(" not in message.split(":")[0], "no empty or placeholder parens"


def test_the_refusal_still_says_which_agent_to_upgrade(tmp_path):
    """The version goes in the subject; the instruction still needs the NAME,
    or "Upgrade  and re-run" is what ships."""
    help_text = "\n".join(ln for ln in FULL_HELP.splitlines() if "--settings" not in ln)
    binary = _binary(tmp_path, help_text, version="1.0.4 (Claude Code)")
    assert "Upgrade Claude Code and re-run" in bf.too_old(bf.Agent.CLAUDE, binary)
