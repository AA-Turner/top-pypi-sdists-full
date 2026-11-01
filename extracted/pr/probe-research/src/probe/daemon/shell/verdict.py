"""agent/src/probe/daemon/shell/shell.py."""

from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class Step:
    """One pipeline of a compound command that has `probe` commands in it
    (`Verdict.steps`). The caller runs the steps in order itself, never bash."""

    before: str  # "" for the first; else "&&", "||" or ";" (a newline is ";")
    text: str  # the pipeline as written (what a shell step runs, and what is shown)
    #: A pipeline that starts with `probe ...`: its argv, for the probe tool's checks.
    probe_argv: list[str] | None = None
    #: The rest of that pipeline (`probe run list | jq .items` -> "jq .items"),
    #: fed the probe command's stdout; None when it is not piped on.
    filter: str | None = None
    #: The probe command's stderr: "keep" (shown after the filter's output),
    #: "merge" (`2>&1`: into the filter too) or "drop" (`2>/dev/null`).
    stderr: str = "keep"
    #: A lone `cd FOLDER`: the folder (`~` expanded), which the caller moves into.
    cd: str | None = None


@dataclass(frozen=True)
class Verdict:
    safe: bool  # may run at once
    reason: str  # "" when safe; else one plain sentence why it needs the researcher's yes
    # Set when the WHOLE command is a single `probe ...` call (the argv after the
    # word `probe`); `safe` is then False with reason "probe command", and the
    # caller routes it to its own pre-check.
    probe_argv: list[str] | None = None
    # The text a quoted heredoc feeds that probe command (`probe draft edit PATH
    # <<'EOF'`, `_probe_heredoc`): the caller hands it to the command as stdin.
    probe_stdin: str | None = None
    # Set when the command is several commands and some are `probe ...` calls:
    # the caller runs them one by one (`Step`), each probe command through its
    # own pre-check and each other part as a command of its own.
    steps: list[Step] | None = None
    # Set when the command is the one allowed write, `cat > FILE <<'TAG'`: the
    # resolved FILE and the body it writes, so the caller can scan the body and
    # hold a write to the team note (the verdict alone says only "safe").
    note_target: str | None = None
    note_body: str | None = None
    note_append: bool = False  # `>>`: the body is added to the end of FILE
    # True: refused outright (`_Never`) -- not a question, not even in bypass mode.
    refused: bool = False
    # True: one flag away from safe (`_Fix`) -- not a question; the daemon adds it.
    fixable: bool = False
    # True on a question (neither safe nor refused): a word of the command, or a
    # path-shaped piece of one, names a credential-shaped file (`_secret`), or the
    # command can't be read word by word (`_Checker.names_credential`). Such a
    # question is the researcher's alone: never put to Jev (`tools._jev_approval`).
    credential: bool = False
    # True on a question about a read Jev can't judge (`_Checker.names_private`): a
    # path inside a hidden file or folder, or a whole tree's contents. Also never
    # put to Jev: its `no_secrets` scores these like any harmless read.
    private: bool = False


@dataclass
class ShellResult:
    exit_code: int | None  # None when the time limit killed it
    output: str  # stdout and stderr together, capped
    truncated: bool
    timed_out: bool
    #: Why `run` stopped it early (its `watch` said so), or None.
    stopped: str | None = None
    #: False: stopped before the launch, so nothing ran (`_run_shell_write` logs it not run).
    started: bool = True
