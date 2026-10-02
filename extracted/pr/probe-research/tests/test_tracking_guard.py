"""The warn-never-gate observer on probe writes in an untracked session.

Two properties carry the design:

  1. It NEVER denies. The only output it can produce is additionalContext --
     one line restating the contract -- and it exits 0 on every path. The
     deterministic layer detects; the model resolves.
  2. Ambiguity leans SILENT. A false negative costs one unwarned write; a
     false positive on `probe run show` teaches the model the layer cries
     wolf, which is how warning layers die. Every doubtful parse, every
     missing field, every read verb stays quiet.
"""

from __future__ import annotations

import importlib.util
import io
import json
import sys
from pathlib import Path

import pytest

PLUGIN = Path(__file__).resolve().parents[1] / "plugins" / "probe-research"

SESSION_ID = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"


def _load_guard():
    """Load tracking_guard.py the way hooks.json does (hooks dir on sys.path,
    so the sibling `import _session_marker` resolves)."""
    path = PLUGIN / "hooks" / "tracking_guard.py"
    spec = importlib.util.spec_from_file_location("_tracking_guard_under_test", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    hooks_dir = str(path.parent)
    added = hooks_dir not in sys.path
    if added:
        sys.path.insert(0, hooks_dir)
    try:
        spec.loader.exec_module(module)
    finally:
        if added:
            sys.path.remove(hooks_dir)
    return module


@pytest.fixture
def guard(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    # The toggle resolves "current" through the machine default when no
    # explicit signal exists; isolate the config so the developer's real
    # ~/.config/probe/config.json cannot decide a test.
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.delenv("PROBE_CONFIG_PATH", raising=False)
    # Outranks the config file in `default_tracking()`, and every bare-toggle
    # test here depends on the resolved default posture. Researchers export it
    # on this box; test_tracking_autoflip and test_session_marker already
    # scrub it, and without it 13 tests in this file fail.
    monkeypatch.delenv("PROBE_SESSION_TRACKING", raising=False)
    return _load_guard()


def _run_main(guard, monkeypatch, capsys, payload) -> str:
    """Run the hook and return its stdout, MINUS a bare flip announcement.

    The announcement is new: a cycling switch has no readout, so the hook that
    moves the state now says where it landed (`FLIP_NOTICE`). Every flip test
    below predates it and asserts `== ""` to mean "this did not deny and did not
    warn" -- which is still exactly what they are testing, and still true.

    So a stdout whose ONLY content is a recognised flip notice is stripped here,
    and nothing else ever is: a deny, a warn, or an additionalContext this file
    does not recognise all survive intact and still fail those assertions. The
    announcement has its own coverage in
    `test_probe_three_states.py`; this is not a hole, it is the seam
    between two things one assertion used to cover at once.
    """
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(payload)))
    guard.main()
    out = capsys.readouterr().out
    return "" if _is_flip_notice(guard, out) else out


def _is_flip_notice(guard, out: str) -> bool:
    """Is this stdout exactly one flip announcement and nothing else?"""
    if not out.strip():
        return False
    try:
        payload = json.loads(out)
    except ValueError:
        return False
    hso = payload.get("hookSpecificOutput")
    if not isinstance(hso, dict) or set(payload) != {"hookSpecificOutput"}:
        return False
    if set(hso) != {"hookEventName", "additionalContext"}:
        return False
    return hso["additionalContext"] in set(guard.FLIP_NOTICE.values())


def _run_main_raw(guard, monkeypatch, capsys, payload) -> str:
    """`_run_main` without the announcement strip, for tests that want it."""
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(payload)))
    guard.main()
    return capsys.readouterr().out


def _payload(command: str, tool: str = "Bash", session: str = SESSION_ID) -> dict:
    return {
        "hook_event_name": "PostToolUse",
        "tool_name": tool,
        "session_id": session,
        "tool_input": {"command": command},
    }


def _folder_default(folder: Path, value: str = "off") -> None:
    cfg = folder / ".probe"
    cfg.mkdir(parents=True, exist_ok=True)
    (cfg / "config.json").write_text(
        json.dumps({"defaults": {"session_tracking": value}}), encoding="utf-8"
    )


def _pre_payload(command: str, tool: str = "Bash", session: str = SESSION_ID) -> dict:
    payload = _payload(command, tool, session)
    payload["hook_event_name"] = "PreToolUse"
    return payload


# ---------------------------------------------------------------------------
# The deny: PreToolUse refuses the write instead of narrating it afterwards.
# ---------------------------------------------------------------------------


def test_an_off_session_is_denied_before_the_write_runs(guard, monkeypatch, capsys):
    """The gap the warn layer could not close: by the time PostToolUse spoke,
    the project existed."""
    assert guard._session_marker.set_tracking(SESSION_ID, False)

    out = _run_main(guard, monkeypatch, capsys, _pre_payload("probe project create x"))

    hso = json.loads(out)["hookSpecificOutput"]
    assert hso["hookEventName"] == "PreToolUse"
    assert hso["permissionDecision"] == "deny"
    assert "probe project create" in hso["permissionDecisionReason"]
    assert "/probe on" in hso["permissionDecisionReason"]


def test_a_default_off_machine_is_denied_too(guard, monkeypatch, capsys, tmp_path):
    """Off is off whatever its origin -- the default is the researcher choosing
    what a new session starts at."""
    cfg = tmp_path / "config" / "probe"
    cfg.mkdir(parents=True, exist_ok=True)
    (cfg / "config.json").write_text(
        json.dumps({"version": 2, "defaults": {"session_tracking": "off"}}),
        encoding="utf-8",
    )
    assert guard._session_marker.tracking_signal(SESSION_ID) is None

    out = _run_main(guard, monkeypatch, capsys, _pre_payload("probe run create demo"))

    assert json.loads(out)["hookSpecificOutput"]["permissionDecision"] == "deny"


def test_an_absent_signal_uses_the_hook_payload_folder_default(
    guard, monkeypatch, capsys, tmp_path
):
    repo = tmp_path / "research"
    cwd = repo / "src"
    cwd.mkdir(parents=True)
    _folder_default(repo)
    payload = _pre_payload("probe run create demo")
    payload["cwd"] = str(cwd)

    out = _run_main(guard, monkeypatch, capsys, payload)

    assert json.loads(out)["hookSpecificOutput"]["permissionDecision"] == "deny"


def test_an_explicit_signal_wins_without_resolving_the_payload_folder(
    guard, monkeypatch, capsys, tmp_path
):
    repo = tmp_path / "research"
    repo.mkdir()
    _folder_default(repo)
    assert guard._session_marker.set_tracking(SESSION_ID, True)
    payload = _pre_payload("probe run create demo")
    payload["cwd"] = str(repo)

    assert _run_main(guard, monkeypatch, capsys, payload) == ""


def test_bare_toggle_flips_from_the_payload_folder_default(
    guard, monkeypatch, capsys, tmp_path
):
    repo = tmp_path / "research"
    repo.mkdir()
    _folder_default(repo)
    payload = {
        "hook_event_name": "UserPromptSubmit",
        "session_id": SESSION_ID,
        "cwd": str(repo),
        "prompt": "/track-work",
    }

    assert _run_main(guard, monkeypatch, capsys, payload) == ""
    # The folder said `off` in the two-valued vocabulary, which meant
    # read-only, so the press advances from there rather than from `full` --
    # and from `read-only` the only place the bare switch goes is back to on.
    assert _state(guard) == "full"


def test_a_tracking_session_is_never_denied(guard, monkeypatch, capsys):
    assert guard._session_marker.set_tracking(SESSION_ID, True)
    assert _run_main(guard, monkeypatch, capsys, _pre_payload("probe project create x")) == ""


def test_reads_are_never_denied(guard, monkeypatch, capsys):
    assert guard._session_marker.set_tracking(SESSION_ID, False)
    assert _run_main(guard, monkeypatch, capsys, _pre_payload("probe project list")) == ""


def test_cleanup_is_never_denied_or_warned(guard, monkeypatch, capsys):
    """"Record nothing" is not "prevent cleanup". Deleting an untracked
    session's leftovers is the FIRST thing a researcher does about them, and a
    gate that blocked it would make the mess permanent."""
    assert guard._session_marker.set_tracking(SESSION_ID, False)
    command = "probe project delete dashboard-agent-ui-blocks --yes"

    assert _run_main(guard, monkeypatch, capsys, _pre_payload(command)) == ""
    assert _run_main(guard, monkeypatch, capsys, _payload(command)) == ""
    assert guard.probe_write(command) is None


# ---------------------------------------------------------------------------
# The parse: what counts as a write.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("command", "matched"),
    [
        ("probe run create --project x demo", "probe run create"),
        ("probe artifact add ckpt.pt --run r1", "probe artifact add"),
        ("probe log r1 loss=0.3", "probe log"),
        ("probe snapshot r1", "probe snapshot"),
        ("probe exec r1 -- python train.py", "probe exec"),
        ("probe notes append p1 'switched optimizer'", "probe notes append"),
        ("cd ~/work && probe experiment create sweep", "probe experiment create"),
        ("PROBE_TOKEN=t probe project create demo", "probe project create"),
        ("/Users/x/.local/bin/probe notes edit --team", "probe notes edit"),
        ("git pull; probe import wandb ./runs", "probe import"),
        # A subgroup's own verb decides, and so does a flag that turns a read
        # into a write.
        ("probe project code attach p1 org/repo", "probe project code attach"),
        ("probe project contributors p1 --add u1", "probe project contributors"),
        ("probe project contributors p1 --remove=u1", "probe project contributors"),
        ("probe wandb import-local ./runs --project p1", "probe wandb import-local"),
        # A redirection is never a separator that hides the words after it,
        # and a leading one is skipped with its file.
        ("probe project contributors p1 &>/dev/null --add u1", "probe project contributors"),
        (">/dev/null probe project create demo", "probe project create"),
        ("&>/dev/null probe project create demo", "probe project create"),
        # A QUOTED `>` looks like an operator once shlex strips the quotes; it
        # must not swallow the `;` or the `<(` after it.
        ("echo '>'; probe project create demo", "probe project create"),
        ("probe project contributors p1 --fields '>' --add u1", "probe project contributors"),
        ("cat < <(probe project create demo)", "probe project create"),
        ("cat > >(probe project create demo)", "probe project create"),
        # A redirection's file is not a help flag, and a comment's apostrophe
        # does not open a quote that swallows the command before it.
        ("probe project create x &> --help", "probe project create"),
        ("probe project create x &>/dev/null # don't print output", "probe project create"),
        ("probe project create x # don't print output", "probe project create"),
        # Bash joins a backslash-newline inside a word, and a glob can name `--add`.
        ("probe project contributors p1 --a\\\ndd u1", "probe project contributors"),
        ("probe project contributors p1 --a[d]d u1", "probe project contributors"),
        # A word the shell has not expanded yet could be `--add`.
        ("OP=--add; probe project contributors p1 $OP u1", "probe project contributors"),
        ("probe project contributors p1 $'--add' u1", "probe project contributors"),
        ("probe project contributors p1 --{add,fields} u1", "probe project contributors"),
        # An empty command word must not crash the parse before the next write.
        ("probe ''; probe project create demo", "probe project create"),
    ],
)
def test_writes_are_detected(guard, command, matched):
    assert guard.probe_write(command) == matched


@pytest.mark.parametrize(
    "command",
    ["probe project code &>/dev/null attach p1 org/repo", "probe project code >&/tmp/x attach p1 org/repo"],
)
def test_a_redirection_between_command_words_fails_closed(guard, command):
    """Bash runs `project code attach`; the hook cannot tell a quoted `>` from
    a real one, so it refuses rather than guess the verb."""
    assert guard.probe_write(command) is not None


@pytest.mark.parametrize(
    "command",
    [
        # Reads inside write groups.
        "probe run show r1",
        "probe run list --project x",
        "probe artifact download ckpt.pt",
        "probe project get demo",
        # Reads one level deeper, or reads unless a flag says otherwise.
        "probe project code list p1",
        "probe project contributors p1",
        # Help, even with its output redirected (refused as `probe run 2>&1`
        # by plugins up to 0.94.0).
        "probe run --help 2>&1 | grep -o x",
        # Local-only W&B commands: they never talk to Probe.
        "probe wandb discover ./runs",
        "probe wandb key status",
        "probe wandb key set --key k",
        "probe project code list p1 &>/dev/null",
        # A literal IPv6 host is not shell expansion.
        "probe --base-url 'http://[::1]:8000' project contributors p1",
        "probe --base-url=http://[::1]:8000 project contributors p1",
        # A `#` inside a word is text, not a comment.
        "probe run list --fields a#b",
        # The switch itself: warning on the un-mute would be self-defeating.
        "probe session track",
        "probe session untrack",
        "probe session status",
        # Read/meta surfaces.
        "probe metrics grouped r1 --key loss",
        "probe get r1",
        "probe doctor",
        "probe update",
        "probe statusline install",
        "probe flush",
        "probe --help",
        # Not probe at all, or not enough of it.
        "git status",
        "reprobe run create x",
        "probe",
        "probe run",
        # Unparseable: unbalanced quote leans silent.
        'probe run create "unterminated',
    ],
)
def test_non_writes_stay_silent(guard, command):
    assert guard.probe_write(command) is None


#: A probe command MENTIONED inside quotes or a heredoc is text, not a command.
#: The old parse split the raw string on `|` and `;` before tokenizing, so a
#: quoted regex or a commit message became a segment that began with `probe`.
MENTIONS = [
    # A quoted regex whose `|` split the old parse (refused 09-23).
    "grep -E 'x|probe run start|y' notes.md",
    "python3 -c \"import re; print(re.sub(r'a|b', 'probe run start', s))\" && ls",
    # A Python heredoc naming the commands.
    "python3 - <<'EOF'\nimport re\nPAT = re.compile(r'probe (run start|exec)')\n"
    "print('a | probe exec -- y')\nEOF",
    # A commit heredoc about the gate (refused 09-17).
    "git commit -m \"$(cat <<'EOF'\nfix(guard): a quoted | no longer starts\n"
    "probe exec; probe notes create x\nEOF\n)\"",
    # `<<-` strips leading tabs from the terminator.
    "cat <<-EOF\n\tprobe notes create x\n\tEOF",
    # A here-string is a quoted word, not a heredoc.
    "cat <<< 'probe notes create x'",
]


@pytest.mark.parametrize("command", MENTIONS)
def test_a_mentioned_probe_command_is_not_a_write(guard, command):
    assert guard.probe_write(command) is None


@pytest.mark.parametrize("command", MENTIONS)
def test_a_mentioned_probe_command_is_not_refused(guard, monkeypatch, capsys, command):
    assert guard._session_marker.set_tracking(SESSION_ID, False)
    assert _run_main(guard, monkeypatch, capsys, _pre_payload(command)) == ""


@pytest.mark.parametrize(
    ("command", "matched"),
    [
        ("echo x | probe notes create p --title t", "probe notes create"),
        ("probe notes create p --title 'a | b; c'", "probe notes create"),
        ("cd ~/work\nprobe notes push n.md", "probe notes push"),
        ("probe notes push n.md \\\n  --note Findings", "probe notes push"),
        ("(cd ~/work && probe notes push n.md)", "probe notes push"),
        ("cat <<'EOF' > n.md\nsome text\nEOF\nprobe notes push n.md", "probe notes push"),
        # An unclosed quote AFTER a complete command leaves that command readable.
        ("probe notes push n.md; echo 'unterminated", "probe notes push"),
    ],
)
def test_real_writes_outside_quotes_are_still_found(guard, command, matched):
    assert guard.probe_write(command) == matched


@pytest.mark.parametrize(
    ("command", "matched"),
    [
        # A `<<` the shell reads as a shift, not a heredoc: dropping the lines
        # after it would hide the real write on the next line.
        ("x=$((1<<2))\nprobe notes push n.md", "probe notes push"),
        ("x=$(( y << z ))\nprobe notes push n.md", "probe notes push"),
        ("(( y = x << z ))\nprobe notes push n.md", "probe notes push"),
        # A `<<` inside quoted code is text.
        ("python -c 'print(1<<2)'\nprobe notes push n.md", "probe notes push"),
        ('python -c "print(1<<x)"\nprobe notes push n.md', "probe notes push"),
        # `<<\EOF` is a heredoc too: its body is dropped, what follows is read.
        ("cat <<\\EOF\nprobe notes create x\nEOF\nprobe log r1 loss=1", "probe log"),
        ("cat <<\\EOF\nprobe notes create x\nEOF", None),
        # Two heredocs on one line close in order.
        ("cat <<A <<B\nprobe notes create 1\nA\nprobe notes create 2\nB\nprobe log r1 x=1", "probe log"),
        # A commit body with its own quotes stays inside its heredoc.
        (
            "git commit -m \"$(cat <<'EOF'\nsay \" and ' | probe notes create\nEOF\n)\" "
            "&& probe notes push n.md",
            "probe notes push",
        ),
    ],
)
def test_only_a_heredoc_the_shell_reads_drops_lines(guard, command, matched):
    assert guard.probe_write(command) == matched


def test_a_piped_write_is_still_refused(guard, monkeypatch, capsys):
    assert guard._session_marker.set_tracking(SESSION_ID, False)
    out = _run_main(
        guard, monkeypatch, capsys, _pre_payload("echo x | probe notes create p --title t")
    )
    assert "`probe notes create` was refused before it ran" in out


# ---------------------------------------------------------------------------
# The gate order: marker first, then parse.
# ---------------------------------------------------------------------------


def test_warns_only_when_marker_set(guard, monkeypatch, capsys):
    """The same write is silent while tracking is on and warned once it is
    off -- the marker, not the command, is what arms the layer."""
    command = "probe run create --project x demo"

    assert _run_main(guard, monkeypatch, capsys, _payload(command)) == ""

    assert guard._session_marker.set_tracking(SESSION_ID, False)
    out = _run_main(guard, monkeypatch, capsys, _payload(command))
    body = json.loads(out)
    hso = body["hookSpecificOutput"]
    assert hso["hookEventName"] == "PostToolUse"
    assert "probe run create" in hso["additionalContext"]
    assert "/probe on" in hso["additionalContext"]
    assert list(body) == ["hookSpecificOutput"]  # no decision/block key, ever


def test_warns_on_a_default_off_machine_with_no_marker(guard, monkeypatch, capsys, tmp_path):
    """The silence this closes. A machine whose default is `off` had no marker
    to match, so the layer stayed quiet on exactly the box where every write is
    a violation -- the case that filled the dashboard while the status line
    read `untracked`."""
    cfg = tmp_path / "config" / "probe"
    cfg.mkdir(parents=True, exist_ok=True)
    (cfg / "config.json").write_text(
        json.dumps({"version": 2, "defaults": {"session_tracking": "off"}}),
        encoding="utf-8",
    )
    assert guard._session_marker.tracking_signal(SESSION_ID) is None

    out = _run_main(guard, monkeypatch, capsys, _payload("probe project create x"))

    assert "probe project create" in json.loads(out)["hookSpecificOutput"]["additionalContext"]


@pytest.mark.parametrize(
    "command",
    ["probe run list --help", "probe project contributors --help", "probe project code list --help"],
)
def test_help_for_a_read_is_not_refused_when_off(guard, monkeypatch, capsys, command):
    """Asking what a read does reads nothing; the CLI's own gate already agrees."""
    marker = guard._session_marker
    assert marker.set_session_state(SESSION_ID, marker.STATE_OFF)
    assert _run_main(guard, monkeypatch, capsys, _pre_payload(command)) == ""
    assert "probe run list" in _run_main(guard, monkeypatch, capsys, _pre_payload("probe run list"))
    # After `--`, `--help` is an argument (a project named `--help`): still a read.
    denied = _run_main(guard, monkeypatch, capsys, _pre_payload("probe project contributors -- --help"))
    assert "probe project contributors" in denied


@pytest.mark.parametrize(
    "command", ["probe wandb discover ./runs", "probe wandb key status", "probe wandb key set --key k"]
)
def test_local_wandb_commands_are_not_reads_either(guard, command):
    assert guard.probe_read(command) is None


def test_reads_stay_silent_even_when_off(guard, monkeypatch, capsys):
    assert guard._session_marker.set_tracking(SESSION_ID, False)
    assert _run_main(guard, monkeypatch, capsys, _payload("probe run show r1")) == ""


def test_other_tools_and_broken_payloads_stay_silent(guard, monkeypatch, capsys):
    assert guard._session_marker.set_tracking(SESSION_ID, False)
    cases = [
        _payload("probe run create x", tool="Skill"),
        _payload("probe run create x", session=""),
        _payload("probe run create x", session="../../etc/passwd"),
        {"tool_name": "Bash", "session_id": SESSION_ID},  # no tool_input
        {"tool_name": "Bash", "session_id": SESSION_ID, "tool_input": {"command": 7}},
    ]
    for payload in cases:
        assert _run_main(guard, monkeypatch, capsys, payload) == ""
    monkeypatch.setattr(sys, "stdin", io.StringIO("not json"))
    guard.main()
    assert capsys.readouterr().out == ""


# ---------------------------------------------------------------------------
# The flip: skill activation writes the signal, deterministically.
# ---------------------------------------------------------------------------


def _skill_payload(args: str, *, skill: str = "probe-research:toggle-research-tracking") -> dict:
    return {
        "hook_event_name": "PostToolUse",
        "tool_name": "Skill",
        "session_id": SESSION_ID,
        "tool_input": {"skill": skill, "args": args},
    }


def test_bare_invocation_toggles_to_the_opposite(guard, monkeypatch, capsys):
    """The whole point, twice over: the flip must not depend on the model then
    running a CLI command, and a bare invocation IS the switch moving.

    An undecided session reads as `full` (the shipped default posture), and the
    lap is TWO presses -- `off` is not on the bare cycle. Asserting on the STATE
    rather than on `_signal` still matters: `read-only` and `off` both spell
    "off" there, so a press that wrongly landed on `off` would look identical."""
    assert guard._session_marker.session_state(SESSION_ID) is None
    for expected in ("read-only", "full"):
        assert _run_main(guard, monkeypatch, capsys, _skill_payload("")) == ""
        assert _state(guard) == expected
    assert _signal(guard) == "on"  # back where it started, for the old readers too


def test_explicit_directions_set_rather_than_flip(guard, monkeypatch, capsys):
    """`off` on an already-off session stays off -- explicit words are
    idempotent setters, not flips, or repeating an instruction would undo it."""
    assert _run_main(guard, monkeypatch, capsys, _skill_payload("off")) == ""
    assert guard._session_marker.tracking_signal(SESSION_ID) == "off"
    assert _run_main(guard, monkeypatch, capsys, _skill_payload("off")) == ""
    assert guard._session_marker.tracking_signal(SESSION_ID) == "off"
    assert _run_main(guard, monkeypatch, capsys, _skill_payload("on")) == ""
    assert guard._session_marker.tracking_signal(SESSION_ID) == "on"


def test_slash_command_form_flips_too(guard, monkeypatch, capsys):
    payload = {
        "hook_event_name": "PostToolUse",
        "tool_name": "SlashCommand",
        "session_id": SESSION_ID,
        "tool_input": {"command": "/toggle-research-tracking off"},
    }
    assert _run_main(guard, monkeypatch, capsys, payload) == ""
    assert guard._session_marker.tracking_signal(SESSION_ID) == "off"


def test_old_slug_still_flips(guard, monkeypatch, capsys):
    """A transcript mid-upgrade can invoke the pre-rename name against this
    newer hook file; the flip must not depend on which spelling fired."""
    payload = _skill_payload("off", skill="probe-research:research-tracking")
    assert _run_main(guard, monkeypatch, capsys, payload) == ""
    assert guard._session_marker.tracking_signal(SESSION_ID) == "off"


@pytest.mark.parametrize("args", ["status", "what is going on?"])
def test_status_and_prose_flip_nothing(guard, monkeypatch, capsys, args):
    """`status` is a question and unrecognised prose is ambiguity; a hook that
    guessed a direction there would flip the switch on a sentence."""
    assert _run_main(guard, monkeypatch, capsys, _skill_payload(args)) == ""
    assert guard._session_marker.tracking_signal(SESSION_ID) is None


@pytest.mark.parametrize(("word", "expected"), [("stop", "off"), ("resume", "on")])
def test_direction_synonyms_mirror_the_skill(guard, monkeypatch, capsys, word, expected):
    assert _run_main(guard, monkeypatch, capsys, _skill_payload(word)) == ""
    assert guard._session_marker.tracking_signal(SESSION_ID) == expected


def test_other_skills_never_flip(guard, monkeypatch, capsys):
    payload = _skill_payload("off", skill="probe-research:start-research-work")
    assert _run_main(guard, monkeypatch, capsys, payload) == ""
    assert guard._session_marker.tracking_signal(SESSION_ID) is None


def test_invalid_session_never_flips(guard, monkeypatch, capsys):
    payload = _skill_payload("off")
    payload["session_id"] = "../../etc/passwd"
    assert _run_main(guard, monkeypatch, capsys, payload) == ""


# ---------------------------------------------------------------------------
# The typed path: a slash command the researcher types produces NO tool use,
# so UserPromptSubmit is the only deterministic surface it has.
# ---------------------------------------------------------------------------


def _prompt_payload(prompt: str) -> dict:
    return {
        "hook_event_name": "UserPromptSubmit",
        "session_id": SESSION_ID,
        "prompt": prompt,
    }


def test_typed_bare_command_toggles(guard, monkeypatch, capsys):
    """The raw shape: the researcher typed the command and nothing else."""
    payload = _prompt_payload("/probe-research:toggle-research-tracking")
    for expected in ("read-only", "full", "read-only"):
        assert _run_main(guard, monkeypatch, capsys, payload) == ""
        assert _state(guard) == expected


@pytest.mark.parametrize(
    ("prompt", "expected"),
    [
        ("/probe-research:toggle-research-tracking off", "off"),
        ("/toggle-research-tracking on", "on"),
        ("/probe-research:research-tracking off", "off"),  # pre-rename slug
    ],
)
def test_typed_explicit_directions_set(guard, monkeypatch, capsys, prompt, expected):
    assert _run_main(guard, monkeypatch, capsys, _prompt_payload(prompt)) == ""
    assert guard._session_marker.tracking_signal(SESSION_ID) == expected


def test_expanded_command_message_flips(guard, monkeypatch, capsys):
    """The expanded shape: <command-name> with the argument in <command-args>
    or a trailing ARGUMENTS: line, around a body that is the skill text
    itself -- which says "off" and "on" in every paragraph, so direction must
    come from the argument carriers only, never the body."""
    tagged = (
        "<command-message>probe-research:toggle-research-tracking</command-message>\n"
        "<command-name>/probe-research:toggle-research-tracking</command-name>\n"
        "<command-args>off</command-args>\n"
        "# Research tracking\nTurning it ON means `probe session track`.\n"
    )
    assert _run_main(guard, monkeypatch, capsys, _prompt_payload(tagged)) == ""
    assert guard._session_marker.tracking_signal(SESSION_ID) == "off"

    arguments_line = (
        "<command-name>/probe-research:toggle-research-tracking</command-name>\n"
        "Body prose saying on and off everywhere.\n\nARGUMENTS: on\n"
    )
    assert _run_main(guard, monkeypatch, capsys, _prompt_payload(arguments_line)) == ""
    assert guard._session_marker.tracking_signal(SESSION_ID) == "on"

    bare = (
        "<command-name>/probe-research:toggle-research-tracking</command-name>\n"
        "Body prose saying on and off everywhere, with no argument carrier.\n"
    )
    assert _run_main(guard, monkeypatch, capsys, _prompt_payload(bare)) == ""
    assert guard._session_marker.tracking_signal(SESSION_ID) == "off"  # toggled


@pytest.mark.parametrize(
    "prompt",
    [
        # A mention is not an invocation.
        "should I run /toggle-research-tracking here?",
        # A question must not flip the switch.
        "/probe-research:toggle-research-tracking status",
        "/toggle-research-tracking what is going on?",
        # Some other command, expanded and raw, in both harnesses' spellings.
        "<command-name>/probe-research:start-research-work</command-name>\nbody",
        "<skill>\n<name>probe-research:start-research-work</name>\n</skill>\nbody",
        "$probe-research:start-research-work",
        "/probe-research:start-research-work",
        # Ordinary prompts.
        "fix the flaky test in tests/test_runs.py",
        "",
    ],
)
def test_prompts_that_are_not_an_invocation_flip_nothing(
    guard, monkeypatch, capsys, prompt
):
    assert _run_main(guard, monkeypatch, capsys, _prompt_payload(prompt)) == ""
    assert guard._session_marker.tracking_signal(SESSION_ID) is None


# ---------------------------------------------------------------------------
# One invocation, one flip -- however many shapes the harness sends it in.
#
# Every test above fires a single shape, which is exactly how the switch
# shipped broken: each path flipped correctly on its own, and the harnesses
# send TWO of them per invocation.
# ---------------------------------------------------------------------------

_EXPANDED = (
    "<command-name>/probe-research:toggle-research-tracking</command-name>\n"
    "Body prose saying on and off everywhere.\n"
)

_CODEX_BLOCK = (
    "<skill>\n"
    "<name>probe-research:toggle-research-tracking</name>\n"
    "<path>/home/r/.codex/plugins/probe-research/skills/toggle-research-tracking</path>\n"
    "</skill>\n"
    "Body prose saying on and off everywhere.\n"
)


def _signal(guard):
    return guard._session_marker.tracking_signal(SESSION_ID)


def _state(guard, session: str = SESSION_ID):
    """The THREE-valued state, which is what the cycle actually moves.

    `_signal` above reads the two-valued compat file, where `read-only` and
    `off` are both spelled "off". That is correct for the old readers it exists
    for and useless for asserting a cycle: two of the three steps look the same
    through it. Tests that care WHICH non-recording state the switch landed in
    read this instead.
    """
    return guard._session_marker.session_state(session)


def test_a_typed_command_and_its_tool_call_flip_once(guard, monkeypatch, capsys):
    """Claude Code delivers one invocation twice -- the expanded command
    message at UserPromptSubmit, then the model's Skill call at PostToolUse.
    Flipping on each sighting lands back where it started: the researcher
    types the command, the state does not move, and `probe session status`
    honestly reports the switch did nothing."""
    assert _run_main(guard, monkeypatch, capsys, _prompt_payload(_EXPANDED)) == ""
    assert _signal(guard) == "off"
    assert _run_main(guard, monkeypatch, capsys, _skill_payload("")) == ""
    assert _signal(guard) == "off"  # converged on the same target, not flipped back


def test_the_codex_typed_spelling_flips(guard, monkeypatch, capsys):
    """Codex types `$slug` where Claude Code types `/slug`, and runs this same
    hooks.json. The slash-only parser wrote NOTHING for it -- so on Codex the
    switch had no deterministic path at all, and the state only ever showed
    whatever SessionStart had seeded."""
    payload = _prompt_payload("$probe-research:toggle-research-tracking")
    assert _run_main(guard, monkeypatch, capsys, payload) == ""
    assert _signal(guard) == "off"


def test_the_codex_expansion_converges_on_the_typed_line(guard, monkeypatch, capsys):
    """Codex sends the raw `$` line and then its own <skill><name> expansion
    of it -- two UserPromptSubmit events for one invocation."""
    raw = _prompt_payload("$probe-research:toggle-research-tracking")
    assert _run_main(guard, monkeypatch, capsys, raw) == ""
    assert _signal(guard) == "off"
    assert _run_main(guard, monkeypatch, capsys, _prompt_payload(_CODEX_BLOCK)) == ""
    assert _signal(guard) == "off"


def test_all_three_shapes_of_one_invocation_flip_once(guard, monkeypatch, capsys):
    """No harness is known to send all three, but the claim must not depend on
    which two arrive -- a third sighting is still the same invocation."""
    for payload in (
        _prompt_payload("/probe-research:toggle-research-tracking"),
        _prompt_payload(_EXPANDED),
        _skill_payload(""),
    ):
        assert _run_main(guard, monkeypatch, capsys, payload) == ""
        assert _signal(guard) == "off"


def test_the_next_invocation_still_flips(guard, monkeypatch, capsys):
    """The switch has to keep working. Convergence is scoped to ONE
    invocation: the researcher invoking it again -- which arrives as a shape
    already seen -- flips, however soon it comes."""
    assert _run_main(guard, monkeypatch, capsys, _prompt_payload(_EXPANDED)) == ""
    assert _run_main(guard, monkeypatch, capsys, _skill_payload("")) == ""
    assert _state(guard) == "read-only"  # one invocation, one step

    assert _run_main(guard, monkeypatch, capsys, _prompt_payload(_EXPANDED)) == ""
    assert _state(guard) == "full"  # ADVANCED a step; it did not converge
    assert _run_main(guard, monkeypatch, capsys, _skill_payload("")) == ""
    assert _state(guard) == "full"


def test_two_tool_sightings_are_two_invocations(guard, monkeypatch, capsys):
    """Two Skill calls with no prompt between them are two invocations: the
    model can only reach the skill by invoking it, and it does not invoke
    twice for one request. A repeat of a shape already seen always flips.

    The case this does NOT cover, deliberately: a model-initiated bare Skill
    call arriving within the window AFTER a typed invocation converges instead
    of flipping. Shapes cannot tell that apart from the typed invocation's own
    tool sighting, which is the trade the claim makes — and the rarer of the
    two, against a switch that never worked at all.
    """
    assert _run_main(guard, monkeypatch, capsys, _skill_payload("")) == ""
    assert _state(guard) == "read-only"
    assert _run_main(guard, monkeypatch, capsys, _skill_payload("")) == ""
    assert _state(guard) == "full"  # advanced again, not stuck on the claim


def _frozen_clock(guard, monkeypatch, start=1_700_000_000.0):
    """A clock the test moves, so the TTL is tested against its real value."""
    now = {"t": start}
    monkeypatch.setattr(guard.time, "time", lambda: now["t"])
    return now


@pytest.mark.parametrize(
    ("offset", "expected"),
    [
        (1.0, "read-only"),  # the same invocation, seconds apart: converge
        (299.0, "read-only"),  # still inside the window
        (301.0, "full"),  # past it: a sighting this old is not that invocation
    ],
)
def test_the_claim_window_is_the_real_constant(
    guard, monkeypatch, capsys, offset, expected
):
    """Freezing the CLOCK rather than the constant. Monkeypatching the TTL to
    -1.0 proved only that the comparison is not inverted: it expired every
    claim regardless of the constant's value or units, and a TTL of 3e9 (never
    expires) left the whole file green."""
    assert guard.FLIP_CLAIM_TTL_SECONDS == 300.0
    now = _frozen_clock(guard, monkeypatch)
    assert _run_main(guard, monkeypatch, capsys, _prompt_payload(_EXPANDED)) == ""
    assert _signal(guard) == "off"
    now["t"] += offset
    assert _run_main(guard, monkeypatch, capsys, _skill_payload("")) == ""
    assert _state(guard) == expected


def test_converging_does_not_renew_the_window(guard, monkeypatch, capsys):
    """A converging sighting rewrites the claim, and stamping a fresh time
    there would let a chain of sightings hold the window open forever — the
    bound would describe the last sighting instead of the invocation."""
    now = _frozen_clock(guard, monkeypatch)
    assert _run_main(guard, monkeypatch, capsys, _prompt_payload(_EXPANDED)) == ""
    now["t"] += 200.0
    assert _run_main(guard, monkeypatch, capsys, _skill_payload("")) == ""  # converges
    now["t"] += 200.0  # 400s from the CLAIM, 200s from the last sighting
    raw = _prompt_payload("/probe-research:toggle-research-tracking")
    assert _run_main(guard, monkeypatch, capsys, raw) == ""
    assert _state(guard) == "full", "the window must run from the claim, not the echo"


def test_a_corrupt_claim_never_costs_the_flip(guard, monkeypatch, capsys):
    """Same lean as the rest of the file: an unreadable claim resolves toward
    doing what the researcher asked, which is flipping."""
    assert _run_main(guard, monkeypatch, capsys, _prompt_payload(_EXPANDED)) == ""
    guard._claim_path(SESSION_ID).write_text("{not json", encoding="utf-8")
    assert _run_main(guard, monkeypatch, capsys, _skill_payload("")) == ""
    assert _state(guard) == "full"


def test_explicit_directions_ignore_the_claim(guard, monkeypatch, capsys):
    """`off` is an absolute setter on every path, so it needs no claim and
    must not consume one: seeing the same instruction twice sets the same
    state, and the bare toggle after it still flips from where that left it."""
    typed_off = _prompt_payload("/probe-research:toggle-research-tracking off")
    assert _run_main(guard, monkeypatch, capsys, typed_off) == ""
    assert _run_main(guard, monkeypatch, capsys, _skill_payload("off")) == ""
    # A LEGACY slug, so `off` is read-only -- the state it has always set.
    assert _state(guard) == "read-only"
    assert _run_main(guard, monkeypatch, capsys, _prompt_payload(_EXPANDED)) == ""
    assert _state(guard) == "full"


def test_an_invalid_session_writes_no_claim_either(guard, monkeypatch, capsys, tmp_path):
    """The signal write validates the session id; the claim is a filename in
    the same directory and must validate it too. It did not, and a bare toggle
    with a traversal id wrote its claim OUTSIDE the sessions directory --
    a guarded write that grew an unguarded sibling."""
    payload = _skill_payload("")  # bare: the path that reaches the claim
    payload["session_id"] = "../../../escaped"
    assert _run_main(guard, monkeypatch, capsys, payload) == ""
    state = tmp_path / "state"
    strays = [p for p in state.rglob("*escaped*")] + [p for p in tmp_path.glob("*escaped*")]
    assert strays == [], f"wrote outside the sessions dir: {strays}"


def test_an_explicit_direction_clears_the_claim(guard, monkeypatch, capsys):
    """bare -> explicit -> bare. The explicit setter needs no claim, but
    leaving the previous one behind outlives the invocation that wrote it: the
    third sighting arrives in a shape that claim never saw and converges on a
    target nobody asked for. Reproduced end-to-end before the fix — the
    shipped bug, back through the door the claim just closed."""
    assert _run_main(guard, monkeypatch, capsys, _prompt_payload(_EXPANDED)) == ""
    assert _state(guard) == "read-only"  # claim{read-only, [expanded]}
    assert _run_main(guard, monkeypatch, capsys, _skill_payload("off")) == ""
    assert _state(guard) == "read-only"  # explicit: absolute, and clears the claim
    assert _run_main(guard, monkeypatch, capsys, _skill_payload("")) == ""
    assert _state(guard) == "full", "a new bare press must advance, not converge"


def test_a_degenerate_claim_never_costs_the_flip(guard, monkeypatch, capsys):
    """Shapes a damaged claim file can take that would each swallow a flip:
    an empty `seen` (every shape reads unseen), a non-finite `at` (never
    expires), and `at: true` (bool is an int)."""
    for broken in (
        {"target": "off", "at": 1_700_000_000.0, "seen": []},
        {"target": "off", "at": float("nan"), "seen": ["expanded"]},
        {"target": "off", "at": True, "seen": ["expanded"]},
    ):
        guard._session_marker.set_tracking(SESSION_ID, False)  # -> read-only
        guard._claim_path(SESSION_ID).write_text(json.dumps(broken), encoding="utf-8")
        assert _run_main(guard, monkeypatch, capsys, _skill_payload("")) == ""
        # A honoured claim would land on its `off` target -- which the bare
        # switch can no longer reach at all, so this tells the two apart twice.
        assert _state(guard) == "full", f"swallowed the flip on {broken}"


def test_a_claim_is_per_session(guard, monkeypatch, capsys):
    """One researcher's invocation must not converge another session's.

    The other session starts explicitly at read-only so the two outcomes
    differ: advancing lands it back on `full`, converging on this session's
    claim would leave it READ-ONLY. With both sessions starting undecided the assertion could
    not tell them apart — it passed with the claim keyed on nothing at all.
    """
    other = "ffffffff-1111-2222-3333-444444444444"
    guard._session_marker.set_tracking(other, False)  # -> read-only
    assert _run_main(guard, monkeypatch, capsys, _prompt_payload(_EXPANDED)) == ""
    assert _state(guard) == "read-only"
    payload = _skill_payload("")
    payload["session_id"] = other
    assert _run_main(guard, monkeypatch, capsys, payload) == ""
    # advanced from ITS OWN state, not converged onto this session's claim
    assert _state(guard, other) == "full"
    assert _state(guard) == "read-only"


# ---------------------------------------------------------------------------
# Wiring.
# ---------------------------------------------------------------------------


def test_hooks_json_runs_the_guard_on_post_tool_use(guard):
    """The guard cannot fire unregistered, and no test of the module would
    notice -- the same argument the version hook's wiring test makes."""
    wiring = json.loads((PLUGIN / "hooks" / "hooks.json").read_text())
    post = wiring["hooks"]["PostToolUse"]
    rendered = json.dumps(post)
    assert "tracking_guard.py" in rendered
    matchers = [entry.get("matcher", "") for entry in post]
    assert any("Bash" in m for m in matchers)


def test_hooks_json_runs_the_guard_on_user_prompt_submit(guard):
    """The typed path produces no tool use, so PostToolUse registration alone
    would leave the most common invocation with no deterministic flip."""
    wiring = json.loads((PLUGIN / "hooks" / "hooks.json").read_text())
    prompt_hooks = wiring["hooks"]["UserPromptSubmit"]
    assert "tracking_guard.py" in json.dumps(prompt_hooks)


# ---------------------------------------------------------------------------
# track-work: the switch merged into the manual, and the semantics that keeps
# that merge safe. Bare invocation splits by SURFACE, not by slug: typed by
# the researcher it is a toggle like any other switch, while a bare TOOL call
# is an agent reading its own guidance -- mid-task, unprompted, exactly when
# tracking should stay untouched -- and writes nothing. The legacy toggle
# slugs flip bare on both surfaces (tested above): a resumed transcript must
# keep meaning what it meant.
# ---------------------------------------------------------------------------

_TRACK_WORK_EXPANDED = (
    "<command-name>/probe-research:track-work</command-name>\n"
    "Body prose saying on and off everywhere.\n"
)

_TRACK_WORK_CODEX_BLOCK = (
    "<skill>\n"
    "<name>probe-research:track-work</name>\n"
    "<path>/home/r/.codex/plugins/probe-research/skills/track-work</path>\n"
    "</skill>\n"
    "Body prose saying on and off everywhere.\n"
)


def test_track_work_bare_tool_call_never_flips(guard, monkeypatch, capsys):
    """THE MERGE'S LOAD-BEARING RULE, and the half the typed toggle must not
    cost. track-work is the how-to manual, and an agent loads a manual bare
    dozens of times a session; if a bare TOOL call flipped, an agent
    consulting its own guidance would silently switch tracking off -- the
    exact silent stop this hook exists to prevent."""
    for payload in (
        _skill_payload("", skill="probe-research:track-work"),
        _skill_payload("", skill="track-work"),
    ):
        assert _run_main(guard, monkeypatch, capsys, payload) == ""
        assert _signal(guard) is None, payload


@pytest.mark.parametrize(
    "prompt",
    [
        # The raw line the researcher types -- Claude's `/` and Codex's `$`.
        # The model has no way to send this shape on either harness.
        "/probe-research:track-work",
        "/track-work",
        "$probe-research:track-work",
        # Claude Code's expansion, which only the harness builds and only from
        # a command a person typed (this plugin ships no commands/track-work.md
        # for the model to invoke into one).
        _TRACK_WORK_EXPANDED,
    ],
)
def test_track_work_typed_bare_toggles(guard, monkeypatch, capsys, prompt):
    """Typed bare IS the toggle. The researcher reaching for the switch by its
    own name must not have to remember a direction word -- and every spelling
    that is PROOF OF A PERSON has to honour it, or the switch works on Claude
    and not Codex (or before expansion and not after).
    Default posture here is `full`, so the presses walk the cycle."""
    assert _run_main(guard, monkeypatch, capsys, _prompt_payload(prompt)) == ""
    assert _state(guard) == "read-only"
    assert _run_main(guard, monkeypatch, capsys, _prompt_payload(prompt)) == ""
    assert _state(guard) == "full"


def test_a_bare_codex_skill_block_alone_never_flips_track_work(
    guard, monkeypatch, capsys
):
    """THE HARNESS ASYMMETRY, and the one that nearly shipped a silent stop.
    Codex delivers a skill ACTIVATION as this block -- and the model activates
    skills too, unprompted, to read their guidance. Nothing in the payload
    tells the two apart, so the block alone is not proof of a person and must
    not flip the slug that IS the manual.

    Claude Code's <command-name> expansion is not the same claim: the harness
    builds it only from a command a person typed."""
    for _ in range(3):
        assert _run_main(
            guard, monkeypatch, capsys, _prompt_payload(_TRACK_WORK_CODEX_BLOCK)
        ) == ""
        assert _signal(guard) is None


def test_a_codex_researcher_still_gets_the_bare_flip(guard, monkeypatch, capsys):
    """...and the carve-out costs them nothing. A typed `$track-work` reaches
    the hook as the raw line AND the block; the raw line is the sighting the
    flip rides, and the block converges on it. One flip, not zero and not two."""
    assert _run_main(
        guard, monkeypatch, capsys, _prompt_payload("$probe-research:track-work")
    ) == ""
    assert _signal(guard) == "off"
    assert _run_main(
        guard, monkeypatch, capsys, _prompt_payload(_TRACK_WORK_CODEX_BLOCK)
    ) == ""
    assert _signal(guard) == "off"


def test_the_codex_block_keeps_its_bare_flip_on_the_legacy_slugs(
    guard, monkeypatch, capsys
):
    """The carve-out is scoped to the slug that is also a manual. A legacy
    toggle slug has no guidance to read, so its activation block flips as it
    always has -- a resumed transcript must keep meaning what it meant."""
    assert _run_main(guard, monkeypatch, capsys, _prompt_payload(_CODEX_BLOCK)) == ""
    assert _signal(guard) == "off"


def test_one_typed_bare_invocation_flips_exactly_once_across_all_shapes(
    guard, monkeypatch, capsys
):
    """THE DOUBLE-FLIP BUG, on the path this change opened. One typed
    `/track-work` can reach the hook three times -- the raw line, the
    harness's expansion of it, and the model's Skill call for it -- and a
    switch that flipped on each sighting landed exactly where it started,
    which reads as a switch that does nothing.

    The claim converges the second typed sighting on the target the first
    resolved, and the tool sighting is inert on this slug, so the whole
    delivery is ONE flip however many shapes the harness sends."""
    for payload in (
        _prompt_payload("/track-work"),
        _prompt_payload(_TRACK_WORK_EXPANDED),
        _skill_payload("", skill="probe-research:track-work"),
    ):
        assert _run_main(guard, monkeypatch, capsys, payload) == ""
        assert _signal(guard) == "off", payload


def test_the_next_typed_bare_track_work_still_flips(guard, monkeypatch, capsys):
    """...and convergence stays scoped to ONE invocation. A researcher who
    types the command again gets the flip, however soon it comes -- a repeat
    of a shape already seen is a new invocation, not a second sighting."""
    for expected in ("read-only", "full", "read-only", "full"):
        assert _run_main(guard, monkeypatch, capsys, _prompt_payload("/track-work")) == ""
        assert _state(guard) == expected


def test_two_different_switch_slugs_are_two_invocations(guard, monkeypatch, capsys):
    """ONE INVOCATION is (slug, shape) -- not shape alone. A typed bare
    `/track-work` then a bare legacy toggle inside the claim window are two
    invocations however their shapes line up, and the second must FLIP. Before
    the claim recorded its slug the second converged on the first one's target
    and silently did nothing, which is the symptom the claim exists to fix."""
    assert _run_main(guard, monkeypatch, capsys, _prompt_payload("/track-work")) == ""
    assert _state(guard) == "read-only"
    assert _run_main(guard, monkeypatch, capsys, _skill_payload("")) == ""
    assert _state(guard) == "full"  # a DIFFERENT slug: a second invocation


def test_a_claim_without_a_slug_still_converges(guard, monkeypatch, capsys):
    """The upgrade path. A claim written by a plugin version that did not
    record the slug can only be read the old way -- converge -- because
    treating "absent" as "a different slug" would flip twice for one
    invocation that straddles the upgrade."""
    assert _run_main(guard, monkeypatch, capsys, _prompt_payload("/track-work")) == ""
    assert _signal(guard) == "off"
    path = guard._claim_path(SESSION_ID)
    claim = json.loads(path.read_text())
    del claim["slug"]
    path.write_text(json.dumps(claim))
    assert _run_main(
        guard, monkeypatch, capsys, _skill_payload("", skill="probe-research:track-work")
    ) == ""
    assert _signal(guard) == "off"


def test_track_work_typed_bare_flips_from_the_current_state(guard, monkeypatch, capsys):
    """The cycle is relative: after an explicit `off`, bare must ADVANCE. The
    explicit setter also has to clear its claim, or this bare sighting would
    converge on `off` and the switch would silently do nothing."""
    # `off` typed at a LEGACY slug is read-only -- what it has always meant.
    assert _run_main(guard, monkeypatch, capsys, _prompt_payload("/track-work off")) == ""
    assert _state(guard) == "read-only"
    assert _run_main(guard, monkeypatch, capsys, _prompt_payload("/track-work")) == ""
    assert _state(guard) == "full"


def test_track_work_typed_bare_then_its_tool_call_does_not_flip_back(
    guard, monkeypatch, capsys
):
    """The interleaving that makes the surface split load-bearing. One typed
    `/track-work` reaches the hook as the prompt AND as the model's bare Skill
    call; the tool sighting is inert, so the invocation flips exactly once."""
    assert _run_main(guard, monkeypatch, capsys, _prompt_payload("/track-work")) == ""
    assert _signal(guard) == "off"
    assert _run_main(
        guard, monkeypatch, capsys, _skill_payload("", skill="probe-research:track-work")
    ) == ""
    assert _signal(guard) == "off"


def test_track_work_explicit_words_flip_and_are_idempotent(guard, monkeypatch, capsys):
    """`off`/`on` are absolute setters on track-work exactly as on the legacy
    slugs -- repeating an instruction must not undo it."""
    assert _run_main(
        guard, monkeypatch, capsys, _skill_payload("off", skill="probe-research:track-work")
    ) == ""
    assert _signal(guard) == "off"
    assert _run_main(
        guard, monkeypatch, capsys, _skill_payload("off", skill="probe-research:track-work")
    ) == ""
    assert _signal(guard) == "off"
    assert _run_main(
        guard, monkeypatch, capsys, _skill_payload("on", skill="probe-research:track-work")
    ) == ""
    assert _signal(guard) == "on"


def test_track_work_typed_directions_flip_in_both_harness_spellings(guard, monkeypatch, capsys):
    """The typed path may produce no tool use, so UserPromptSubmit must read
    the direction from both the Claude `/` and Codex `$` spellings."""
    assert _run_main(guard, monkeypatch, capsys, _prompt_payload("/track-work off")) == ""
    assert _signal(guard) == "off"
    assert _run_main(
        guard, monkeypatch, capsys, _prompt_payload("$probe-research:track-work on")
    ) == ""
    assert _signal(guard) == "on"


def test_track_work_expanded_arguments_line_carries_the_direction(guard, monkeypatch, capsys):
    payload = _prompt_payload(_TRACK_WORK_EXPANDED + "ARGUMENTS: off\n")
    assert _run_main(guard, monkeypatch, capsys, payload) == ""
    assert _signal(guard) == "off"


def test_track_work_questions_and_status_never_flip(guard, monkeypatch, capsys):
    for prompt in (
        "should I run /track-work here?",
        "/probe-research:track-work status",
        "/track-work what is going on?",
    ):
        assert _run_main(guard, monkeypatch, capsys, _prompt_payload(prompt)) == ""
        assert _signal(guard) is None, prompt


def test_track_work_direction_and_its_tool_call_converge(guard, monkeypatch, capsys):
    """One `/track-work off` invocation arrives as the expanded prompt AND the
    model's Skill call; the second sighting must converge, not re-set."""
    payload = _prompt_payload(_TRACK_WORK_EXPANDED + "ARGUMENTS: off\n")
    assert _run_main(guard, monkeypatch, capsys, payload) == ""
    assert _signal(guard) == "off"
    assert _run_main(
        guard, monkeypatch, capsys, _skill_payload("off", skill="probe-research:track-work")
    ) == ""
    assert _signal(guard) == "off"


def test_a_bare_manual_read_between_direction_and_tool_call_stays_inert(
    guard, monkeypatch, capsys
):
    """The dangerous interleaving: researcher types `/track-work off`, the
    model then loads the skill bare to read how to comply. The bare read must
    neither flip back nor claim the invocation's convergence slot."""
    assert _run_main(guard, monkeypatch, capsys, _prompt_payload("/track-work off")) == ""
    assert _signal(guard) == "off"
    assert _run_main(
        guard, monkeypatch, capsys, _skill_payload("", skill="probe-research:track-work")
    ) == ""
    assert _signal(guard) == "off"


def test_track_work_toggle_word_rides_the_same_permission_as_bare(
    guard, monkeypatch, capsys
):
    """`toggle` is bare, spelled out -- the same request -- so it is granted on
    the same surfaces. Typed it flips; as a bare-equivalent TOOL argument it
    stays inert, which is what keeps "toggle" from being reachable by ambient
    args text on the slug an agent invokes unprompted."""
    for args in ("toggle", "flip"):
        assert _run_main(
            guard, monkeypatch, capsys, _skill_payload(args, skill="probe-research:track-work")
        ) == ""
        assert _signal(guard) is None, args
    # ...while the legacy slug keeps it on the tool surface too, unchanged.
    assert _run_main(guard, monkeypatch, capsys, _skill_payload("toggle")) == ""
    assert _signal(guard) == "off"


@pytest.mark.parametrize("word", ["toggle", "flip"])
def test_track_work_typed_toggle_word_flips(guard, monkeypatch, capsys, word):
    """The typed half of the same permission: a researcher who spells the
    relative flip out gets the flip, exactly as bare does."""
    assert _run_main(
        guard, monkeypatch, capsys, _prompt_payload("/track-work " + word)
    ) == ""
    assert _signal(guard) == "off"


def test_pasted_expansion_shaped_text_never_flips(guard, monkeypatch, capsys):
    """The mid-paste attack, both slugs. A prompt that merely CONTAINS an
    expansion-shaped block -- an issue body, documentation of this hook, a
    transcript -- is not an invocation: real harness expansions LEAD with the
    command/skill block. Matching a tag anywhere let pasted text flip tracking
    with no invocation, and a pasted ARGUMENTS line defeated bare-never-flips."""
    for prompt in (
        "Here is the bug report I got:\n\n" + _TRACK_WORK_EXPANDED + "ARGUMENTS: off\n",
        "Quoting the hook docs:\n" + _EXPANDED,
        "context first\n" + _TRACK_WORK_CODEX_BLOCK,
        "see this example:\n<command-name>/probe-research:toggle-research-tracking</command-name>\n",
    ):
        assert _run_main(guard, monkeypatch, capsys, _prompt_payload(prompt)) == ""
        assert _signal(guard) is None, prompt[:40]


def test_a_leading_expansion_with_a_quoted_tag_reads_the_leading_one(
    guard, monkeypatch, capsys
):
    """A real expansion whose BODY quotes another tag (skill docs quote these
    blocks) must resolve to the leading invocation, not the quoted example."""
    prompt = (
        _TRACK_WORK_EXPANDED
        + "The docs quote: <command-name>/probe-research:toggle-research-tracking"
        + "</command-name> as the legacy spelling.\n"
    )
    assert _run_main(guard, monkeypatch, capsys, _prompt_payload(prompt)) == ""
    # The LEADING invocation is a typed bare track-work, so it toggles; the
    # quoted legacy tag in the body must not be what decided that.
    assert _signal(guard) == "off"


def test_track_work_slash_command_shapes(guard, monkeypatch, capsys):
    """The SlashCommand tool shape with INLINE args, per slug class -- the
    parts[1] parse combined with the per-slug bare computation."""
    bare = {
        "hook_event_name": "PostToolUse",
        "tool_name": "SlashCommand",
        "session_id": SESSION_ID,
        "tool_input": {"command": "/track-work"},
    }
    assert _run_main(guard, monkeypatch, capsys, bare) == ""
    assert _signal(guard) is None
    directed = {
        "hook_event_name": "PostToolUse",
        "tool_name": "SlashCommand",
        "session_id": SESSION_ID,
        "tool_input": {"command": "/track-work off"},
    }
    assert _run_main(guard, monkeypatch, capsys, directed) == ""
    assert _signal(guard) == "off"
