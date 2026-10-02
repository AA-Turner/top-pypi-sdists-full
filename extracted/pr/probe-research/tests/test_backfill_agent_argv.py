"""How a backfill agent is actually launched.

Two things are load-bearing and neither is obvious from reading the argv:
the context flags (measured, and NOT --bare, which breaks auth), and the
mutual exclusion between minting a session and resuming one.
"""

from __future__ import annotations

import inspect
from pathlib import Path

import pytest

from probe.cli import backfill


def _claude(**kw):
    return backfill.agent_argv(backfill.Agent.CLAUDE, "/bin/claude", Path("/tmp/x"), **kw)


def test_the_event_stream_is_still_requested():
    argv = _claude()
    assert "--output-format" in argv and "stream-json" in argv
    assert "--verbose" in argv, "stream-json emits only the result without it"


def test_the_tool_allowlist_is_sent():
    argv = _claude()
    assert argv[argv.index("--allowedTools") + 1] == backfill.AGENT_TOOLS


def test_a_workdir_makes_the_folder_readable_and_unwritable():
    """Both halves, or the confinement is not a confinement.

    `--add-dir` ALONE makes the folder writable, which is the opposite of what
    it is here for; the deny rule alone leaves it unreadable. They only mean
    "read this, write elsewhere" together, so both are asserted together."""
    argv = _claude(workdir=Path("/state/work"))
    assert argv[argv.index("--add-dir") + 1] == "/tmp/x"
    settings = argv[argv.index("--settings") + 1]
    assert "Edit(/tmp/x/**)" in settings


def test_no_workdir_means_no_confinement_flags():
    """The non-import callers run IN the folder and are not confined by this."""
    argv = _claude()
    assert "--add-dir" not in argv and "--settings" not in argv


def test_codex_writes_to_the_workdir_not_the_imported_folder():
    """`-C` is what Codex scopes its WRITABLE workspace to.

    Pointed at the imported folder -- which is what shipped -- the customer's
    research directory was the one writable thing on disk. Reads are
    unrestricted in workspace-write mode, so pointing it at the scratch dir
    leaves the folder readable and unwritable in one move. Verified against the
    real binary on 2026-08-06: read outside succeeded, write outside blocked."""
    argv = backfill.agent_argv(
        backfill.Agent.CODEX,
        "/bin/codex",
        Path("/drive/research"),
        workdir=Path("/state/work"),
    )
    assert argv[argv.index("-C") + 1] == "/state/work"
    assert "/drive/research" not in argv
    assert "workspace-write" in argv


def test_autocompact_is_on_so_a_long_unit_survives_its_own_context():
    argv = _claude()
    assert argv[argv.index("--autocompact") + 1] == "auto"


def test_the_measured_context_flags_are_sent():
    argv = _claude()
    for flag in backfill.CONTEXT_FLAGS:
        assert flag in argv


def test_bare_is_never_sent_because_it_breaks_auth():
    """--bare removes more context but never reads OAuth or the keychain, so a
    normal subscription install exits 1 with 'Not logged in'. Verified."""
    assert "--bare" not in _claude()
    assert "--bare" not in backfill.CONTEXT_FLAGS


def test_a_session_id_is_minted_when_one_is_asked_for():
    argv = _claude(session_id="sess-1")
    assert argv[argv.index("--session-id") + 1] == "sess-1"
    assert "--resume" not in argv


def test_resume_adopts_a_session_instead_of_minting_one():
    argv = _claude(session_id="sess-1", resume="sess-0")
    assert argv[argv.index("--resume") + 1] == "sess-0"
    assert "--session-id" not in argv, "a session cannot be both new and pre-existing"


def test_neither_flag_appears_when_neither_is_asked_for():
    argv = _claude()
    assert "--session-id" not in argv and "--resume" not in argv


def test_codex_is_unchanged_and_ignores_resume():
    """Codex has no --resume equivalent, so its units restart clean rather than
    being handed something that merely looks similar."""
    argv = backfill.agent_argv(
        backfill.Agent.CODEX, "/bin/codex", Path("/tmp/x"), resume="sess-0"
    )
    assert argv[:3] == ["/bin/codex", "exec", "--json"]
    assert "--resume" not in argv and "--session-id" not in argv
    assert "-C" in argv and "/tmp/x" in argv


@pytest.mark.parametrize("flag", ["--strict-mcp-config", "--disable-slash-commands"])
def test_the_context_flags_are_the_measured_pair(flag):
    assert flag in backfill.CONTEXT_FLAGS


# -- the prompt is NOT in the argv -------------------------------------------
#
# What follows is the crash the stdin change exists to prevent. Linux caps ONE
# argv element at MAX_ARG_STRLEN bytes; the prompt used to be one, sized
# against the model's context window instead, so every folder past ~154 sampled
# evidence files died with "[Errno 7] Argument list too long" -- on the chunked
# route too, which exists to fix "too big for one prompt".


def test_the_prompt_is_not_an_argv_element_for_claude():
    """`-p` is present and takes no value: the prompt arrives on stdin."""
    argv = _claude()
    assert "-p" in argv
    assert argv[argv.index("-p") + 1] == "--output-format", (
        "-p must be followed by the next FLAG, not a prompt -- a prompt here is "
        "the E2BIG crash"
    )


def test_codex_gets_neither_a_positional_prompt_nor_a_dash():
    """Codex reads stdin only when no prompt is supplied alongside it.

    Its own docs: a prompt given WITH piped stdin makes the stdin arrive as a
    separate `<stdin>` block rather than as the instructions. `-` would be a
    second way to say the same thing and is equally unnecessary."""
    argv = backfill.agent_argv(backfill.Agent.CODEX, "/bin/codex", Path("/tmp/x"))
    assert argv[-1] == "/tmp/x", "the -C value is last; nothing follows it"
    assert "-" not in argv


def test_no_argv_element_can_approach_the_exec_ceiling():
    """A 300KB prompt is ordinary for a real research folder. Before stdin it
    was argv[2], and `execve` refused it."""
    argv = _claude(workdir=Path("/state/work"))
    assert max(len(a.encode("utf-8")) for a in argv) < backfill.MAX_ARG_STRLEN


# -- the guard ---------------------------------------------------------------


def test_the_guard_counts_bytes_not_characters():
    """The units bug this repo has already shipped twice.

    A string of MAX_ARG_STRLEN-1 MULTIBYTE characters passes a `len()` check
    and is still rejected by the kernel, because the ceiling is bytes."""
    multibyte = "é" * (backfill.MAX_ARG_STRLEN - 1)
    assert len(multibyte) < backfill.MAX_ARG_STRLEN, "passes a character check"
    with pytest.raises(backfill.ArgvTooLargeError) as caught:
        backfill.check_argv(["/bin/claude", multibyte])
    assert "argv[1]" in str(caught.value), "says WHICH element, not just that one is big"


def test_the_guard_is_a_raise_not_an_assert():
    """`assert` is stripped by `python -O`, so a guard built on one is absent
    in exactly the deployment that skipped the checks."""
    source = inspect.getsource(backfill.check_argv)
    assert "assert " not in source
    assert "raise" in source


def test_the_guard_passes_a_normal_argv_through_unchanged():
    argv = ["/bin/claude", "-p", "--verbose"]
    assert backfill.check_argv(argv) is argv


def test_an_ordinary_folder_path_does_not_trip_the_guard():
    """A deep path plus its settings JSON is nowhere near the ceiling. The
    guard must not fire on real input, or whoever hits it will disable it.

    The scratch dir is DISTINCT from the folder, and has to be: a workdir equal
    to the folder skips the confinement pair entirely (see the same-dir rule in
    `agent_argv`), which is the one shape of this call that carries no settings
    JSON at all -- exactly what this test is here to size."""
    deep = Path("/" + "/".join(f"level{i}" for i in range(40)))
    argv = backfill.agent_argv(backfill.Agent.CLAUDE, "/bin/claude", deep, workdir=deep / "scratch")
    assert "--settings" in argv
