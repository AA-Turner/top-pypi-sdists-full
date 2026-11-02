"""build one headless invocation (never the prompt): model/effort flags, tool allowlists, the argv size limit execve enforces."""

from __future__ import annotations
import re
from pathlib import Path
from probe.cli.imports.folder.agents.agents import Agent

#: Claude's tool allowlist. `Write`/`Edit` are here because the agent may write
#: a JSONL file for `probe-backfill-plan apply`; the deny rule above is what
#: keeps that file out of the imported folder. Bash is scoped to
#: `probe-backfill-plan`, the agents' one command (`plan_tool_launcher`: it
#: touches only the agent's own work dir). No `probe`: code uploads every file
#: and creates every project, and an agent that could run `probe artifact add`
#: uploaded files a second time (2026-10-26, 1,583 duplicates). An unscoped Bash
#: would route around the deny rule with one `echo >`.
AGENT_TOOLS = "Bash(probe-backfill-plan:*),Read,Glob,Grep,Task,Write,Edit"

#: A read-and-write-only allowlist, PER AGENT, for a lane that hands its agent
#: a rendered file and takes one written file back. The claims draft it was
#: sized for is gone (the record pass has its own, `backfill_record.RECORD_TOOLS`);
#: the pi entry is what `agent_argv` falls back to for `--tools`, so the table
#: stays although no lane launches pi today. Per agent because the tool names
#: are not a shared vocabulary: Claude Code spells them `Read,Write` and pi
#: `read,write`, and a lowercase name in Claude's `--allowedTools` is not an
#: error, it is an allowlist that matches nothing. Codex is None because it
#: has no allowlist flag at all (its confinement is the OS sandbox), not
#: because it is unrestricted. No Bash at all: the 84-denial flail of
#: 2026-08-29 was a model reaching for python3/jq over raw JSONL.
DIGEST_TOOLS: dict[Agent, str | None] = {
    Agent.CLAUDE: "Read,Write",
    Agent.CODEX: None,
    Agent.PI: "read,write",
}

#: The reasoning efforts each agent accepts, and the ONLY values an effort can
#: reach an argv as (`agent_argv`): Codex's own API error lists its set
#: ("Supported values are: 'none', 'minimal', ...", codex-cli 0.164.0) and
#: `claude --help` lists Claude's (2.1.296). pi takes none. The server refuses
#: anything else (`app.core.config.IMPORT_AGENT_EFFORTS`, the same lists).
EFFORTS: dict[Agent, tuple[str, ...]] = {
    Agent.CODEX: ("none", "minimal", "low", "medium", "high", "xhigh", "max"),
    Agent.CLAUDE: ("low", "medium", "high", "xhigh", "max"),
}

#: Codex's effort goes in through `-c key=value`, whose value Codex parses as
#: TOML: a string built from input could carry a second key. So the argument is
#: looked up here, never formatted from the setting -- an effort not in this
#: table never reaches the argv at all.
CODEX_EFFORT_CONFIG: dict[str, str] = {
    effort: f'model_reasoning_effort="{effort}"' for effort in EFFORTS[Agent.CODEX]
}

#: A model name an argv may carry: one element (no shell is involved), and
#: never a leading dash an agent's option parser could read as a flag. Model
#: names look like `sonnet`, `gpt-6-astra`, `openai/gpt-6`. The server checks
#: the same pattern.
MODEL_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:/-]{0,79}")

CODEX_ARGS = (
    "-s",
    "workspace-write",
    "--skip-git-repo-check",
)


#: The largest a SINGLE argv element may be, in BYTES.
#:
#: Not `getconf ARG_MAX` (2MB here), which is the total and is the number
#: everyone checks. Linux caps each individual element at `MAX_ARG_STRLEN` =
#: 32 pages, and exceeding it is `E2BIG` from `execve` -- surfaced by this
#: module as "argument list too long" with no hint about which element.
#:
#: This is why the prompt is NOT in the argv. It used to be (`-p <prompt>`),
#: sized against the model's CONTEXT window: `SINGLE_SHOT_TOKEN_BUDGET` of 90k
#: tokens is 288,000 chars, 2.2x over this ceiling, and `CHUNK_TOKEN_BUDGET`
#: at 176,000 chars was over it too -- so the chunked route, which exists to
#: fix "too big for one prompt", crashed identically. Measured: any folder
#: past ~154 sampled evidence files. Those two budgets are context budgets
#: again now, and nothing but this constant guards the transport.
MAX_ARG_STRLEN = 131_071


class ArgvTooLargeError(ValueError):
    """An argv element would be rejected by `execve`.

    Raised rather than asserted: `assert` vanishes under `python -O`, and a
    guard that silently disappears in one deployment mode is worse than none.
    """


def check_argv(argv: list[str]) -> list[str]:
    """Fail loudly, and BEFORE the exec, on an argv element `execve` will reject.

    A tripwire, not a routine check. Nothing in the argv is user content any
    more -- the prompt goes to stdin and what remains is flags, a binary path,
    a folder path and a small settings JSON. That is the point: if this ever
    fires again, something put content back in the argv, and the message says
    which element rather than leaving `[Errno 7]` to be re-diagnosed.

    BYTES, not characters. `len(str)` counts code points and this ceiling is
    bytes, so a folder path or a sample carrying non-ASCII passes a character
    check and still fails the exec. The same units bug has shipped twice in
    this repo (`team_note_file.py`, hooks `additionalContextLimit`).
    """
    for i, element in enumerate(argv):
        size = len(element.encode("utf-8", "replace"))
        if size >= MAX_ARG_STRLEN:
            raise ArgvTooLargeError(
                f"argv[{i}] is {size:,} bytes, over the {MAX_ARG_STRLEN:,}-byte "
                f"per-element limit execve enforces (starts: {element[:60]!r}). "
                "Anything this large belongs on stdin or in a file the agent reads."
            )
    return argv


def _settings_argv(
    agent: Agent, supported: frozenset[str] | None, model: str | None, effort: str | None
) -> list[str]:
    """The model and effort flags one launch carries. Nothing when neither is set.

    Each half is dropped on its own, never the launch: a model that is not a
    `MODEL_NAME`, an effort not on the agent's `EFFORTS`, or a flag this binary
    does not advertise (`supported_flags`; unknown counts as yes, see `_has`).
    Codex's effort is a `CODEX_EFFORT_CONFIG` lookup, never a formatted string.
    pi takes a model and no effort.
    """
    model = model if model and MODEL_NAME.fullmatch(model) else None
    args: list[str] = []
    if agent is Agent.CODEX:
        if model and _has(supported, "--model"):
            args += ["-m", model]
        config = CODEX_EFFORT_CONFIG.get(effort or "")
        if config and _has(supported, "--config"):
            args += ["-c", config]
        return args
    if model and _has(supported, "--model"):
        args += ["--model", model]
    if agent is Agent.CLAUDE and effort in EFFORTS[Agent.CLAUDE] and _has(supported, "--effort"):
        args += ["--effort", effort]
    return args


def agent_argv(
    agent: Agent,
    binary: str,
    folder: Path,
    *,
    workdir: Path | None = None,
    tools: str | None = None,
    model: str | None = None,
    session_id: str | None = None,
    resume: str | None = None,
    effort: str | None = None,
) -> list[str]:
    """The headless invocation for one agent. THE PROMPT IS NOT IN IT.

    All three read the prompt from stdin: `claude -p` and `pi -p` with no
    prompt argument, and `codex exec` with no positional. See `MAX_ARG_STRLEN`
    for why, and `run_one` for how the prompt is fed.

    Codex must be given NEITHER a positional NOR `-`, only piped stdin: its
    own docs say a prompt supplied alongside piped stdin makes the stdin
    arrive as a separate `<stdin>` block rather than as the instructions.

    The two IMPORTER agents are asked for a JSONL EVENT STREAM, and that is not
    a preference. A bare `claude -p` prints nothing at all until the whole run
    finishes, so a backfill over a real folder sat silent for minutes and read
    as hung -- which is exactly what it looked like. The event stream is the
    only way to know the agent is alive, and the only way to count what it has
    done so far. pi is asked for plain `--mode text` instead: it runs one
    bounded digest with `progress=False`, so there is nothing to fold and
    nobody watching a counter.

    `workdir` is the agent's SCRATCH directory -- the one place it may write.
    The importer's agents are pointed at it as their working root and given
    `folder` as something to read, by the two different mechanisms CONFINEMENT
    describes. Claude takes cwd from the process, so its half is `--add-dir`
    plus the deny rule; Codex resolves its writable workspace from `-C` rather
    than from cwd, so pointing that there is the whole of its half.

    Without a `workdir` both fall back to running IN `folder`, which is what the
    non-import callers (and the tests that predate the scratch dir) expect.

    `session_id` names the session so the ledger can record it; `resume` picks
    one back up. A unit killed mid-turn leaves a transcript whose last message
    asks for a tool result that never arrived, and that DOES replay cleanly --
    verified 2026-08-06 against a SIGKILL, exit 0 with context intact, and a
    SIGTERM is safer still because Claude Code writes the missing tool_result
    before dying. The journal still decides WHICH units rerun; resume only
    decides whether a rerun keeps what it had already read.

    Codex has no equivalent, so its units restart clean. That is why `resume` is
    ignored for it rather than approximated with something that looks similar.

    `tools` is the digest lane's allowlist (`DIGEST_TOOLS[agent]`, keyed because
    the tool names are spelled differently per agent); Codex has no allowlist
    flag. `model` and `effort` come from the import's settings
    (`import_agent_settings`) and go through `_settings_argv`: Codex `-m <model>`
    and `-c model_reasoning_effort="<effort>"`, Claude `--model` and `--effort`.
    Absent, each means "exactly what the importer has always sent": no flag at
    all, which is not the same as passing a default we picked -- the agent runs
    as the researcher configured it.
    """
    supported = supported_flags(binary, agent)
    if agent is Agent.PI:
        argv = [
            binary,
            "-p",  # no prompt argument: it arrives on stdin, like the other two
            "--mode",
            "text",
            # pi has no permission file and no OS sandbox, so whatever value
            # lands here IS the confinement -- see CONFINEMENT. The fallback is
            # the digest entry rather than a literal, so the safe default is
            # written down in exactly one place.
            "--tools",
            tools or DIGEST_TOOLS[Agent.PI],
            # A digest run must not mint a session our own live tap then
            # captures -- a recursive capture whose input is the last digest.
            "--no-session",
        ]
        argv += [
            f
            for f in ("--no-extensions", "--no-skills", "--no-context-files")
            if _has(supported, f)
        ]
        argv += _settings_argv(agent, supported, model, effort)
        return check_argv(argv)
    if agent is Agent.CLAUDE:
        argv = [
            binary,
            "-p",  # no prompt argument: it arrives on stdin
            "--output-format",
            "stream-json",
            "--verbose",  # required: stream-json emits only the result without it
            "--allowedTools",
            tools or AGENT_TOOLS,
        ]
        # OPTIONAL flags are filtered against the binary in front of us. An
        # older Claude Code exits on the first option it does not recognise,
        # before reading a single file -- see `supported_flags`.
        if _has(supported, "--autocompact"):
            argv += ["--autocompact", "auto"]
        argv += [f for f in CONTEXT_FLAGS if _has(supported, f)]
        argv += _settings_argv(agent, supported, model, effort)
        # RESOLVED, not compared as written: the question is whether these are
        # the same directory on disk, and a scratch path reached through a
        # symlink (macOS `/var` -> `/private/var`, a `..` in a caller's path)
        # is the same dir spelled differently. Getting that wrong writes a deny
        # rule over the agent's own output file.
        if workdir is not None and Path(folder).resolve() != Path(workdir).resolve():
            # Read the folder, write only the scratch dir. Both halves, or
            # neither: --add-dir alone makes the folder WRITABLE, which is the
            # opposite of what it is here for.
            #
            # SAME DIR IS THE EXCEPTION, not an oversight. When the folder IS
            # the workdir the only visible tree is the scratch dir the agent was
            # given to write in, so a deny rule on it would block the output
            # file this run exists to produce -- and there is no second tree
            # left to protect. That is the digest lane: it hands the agent a
            # rendered view inside its own scratch dir and nothing else.
            argv += [
                "--add-dir",
                str(folder),
                "--settings",
                readonly_settings(folder),
            ]
        else:
            # No second tree to protect, but still no hooks (`readonly_settings`).
            argv += ["--settings", readonly_settings(None)]
        if resume:
            argv += ["--resume", resume]
        elif session_id:
            # Mutually exclusive: --session-id MINTS one, --resume ADOPTS one,
            # and passing both asks for a session that must be simultaneously
            # new and pre-existing.
            argv += ["--session-id", session_id]
        return check_argv(argv)
    return check_argv(
        [
            binary,
            "exec",
            "--json",
            *CODEX_ARGS,
            *_settings_argv(agent, supported, model, effort),
            "-C",
            str(workdir if workdir is not None else folder),
            # No hooks: Probe's own automation is not the researcher's session
            # (`readonly_settings`). Only when this Codex names a `hooks`
            # feature: `--disable` with a name it does not know is a hard
            # "Unknown feature flag" exit (0.80.0), and a Codex without the
            # feature has no hooks to disable.
            *(["--disable", "hooks"] if "hooks" in (codex_features(binary) or ()) else []),
            # No positional prompt and no `-`: stdin alone is the instructions.
        ]
    )
from probe.cli.imports.folder.agents.flags import CONTEXT_FLAGS, _has, supported_flags  # noqa: E402 -- an import cycle: bound once this module's names exist
from probe.shared.harness.harnesses.claude_code.headless import readonly_settings  # noqa: E402 -- an import cycle: bound once this module's names exist
from probe.shared.harness.harnesses.codex.headless import codex_features  # noqa: E402 -- an import cycle: bound once this module's names exist
