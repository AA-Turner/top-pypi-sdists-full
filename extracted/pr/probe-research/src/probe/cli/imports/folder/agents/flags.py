"""probe an agent binary before launching it: the flags its --help advertises, its version, whether it is too old or degraded."""

from __future__ import annotations
import re
import subprocess
from functools import lru_cache
from probe.cli.imports.folder.agents.agents import AGENT_COPY, Agent, which_agent


#: NOT `--bare`, which removes more and is the obvious-looking answer: it takes
#: auth down with it. "Anthropic auth is strictly ANTHROPIC_API_KEY or
#: apiKeyHelper (OAuth and keychain are never read)", so on a normal
#: subscription install every agent exits 1 with "Not logged in". Verified.
#: What a Claude invocation loads before it reads a single file. Measured on
#: this machine, 2026-08-06, as cache_creation + cache_read on a trivial prompt:
#:
#:     baseline (allowlist only)                47,198
#:     + --strict-mcp-config                    33,050
#:     + --disable-slash-commands               35,631
#:     + both                                   21,483   <- what we send
#:
#: A backfill launches one of these per unit and again per retry, so halving
#: the floor is the difference between fitting a unit's evidence in context and
#: compacting in the middle of describing it.
CONTEXT_FLAGS = ("--strict-mcp-config", "--disable-slash-commands")


#: Flags whose ABSENCE stops the run, per agent. These are not preferences:
#: `--add-dir` + `--settings` ARE the Claude half of CONFINEMENT, and
#: `--output-format`/`--verbose`/`--allowedTools` are how the run is driven and
#: read at all. Running without any of them is either unconfined or blind.
REQUIRED_FLAGS: dict[Agent, tuple[str, ...]] = {
    Agent.CLAUDE: (
        "--output-format",
        "--verbose",
        "--allowedTools",
        "--add-dir",
        "--settings",
        "--session-id",
        "--resume",
    ),
    Agent.CODEX: ("--json", "--skip-git-repo-check"),
    # pi's `--tools` IS its confinement -- there is no permission file and no OS
    # sandbox behind it -- and `--no-session` is what stops a digest run minting
    # a pi session our own live tap then captures. `--mode` picks plain text over
    # pi's interactive stream. `--print` is how pi's help spells `-p`.
    Agent.PI: ("--print", "--tools", "--no-session", "--mode"),
}

#: Flags DROPPED, with a note, when the binary predates them. Each costs
#: something real -- context headroom, MCP isolation -- but none of them is
#: load-bearing for correctness or confinement, and refusing to import a
#: researcher's folder over a compaction hint is the wrong trade.
#:
#: NOT A LIST OF EVERY DROPPABLE FLAG: `--model` and `--effort` are dropped the
#: same way (`_settings_argv`) but are not here, because an import sends them
#: only when its settings name a model or an effort
#: (`import_agent_settings`). Listed here, they would tell everyone whose
#: import sends neither that it runs degraded over flags it does not use.
#: `degraded_note` names them only when this import's settings would send them
#: (`wanted`).
OPTIONAL_FLAGS: dict[Agent, tuple[str, ...]] = {
    Agent.CLAUDE: ("--autocompact", *CONTEXT_FLAGS),
    Agent.CODEX: (),
    # Extensions/skills/context files each load our own tap or the user's
    # configuration into a run whose entire job is reading one rendered file.
    # Worth dropping on an older pi rather than refusing the run. Kept
    # despite the caveat above only because they are still the honest answer to
    # `unsupported_flags`; pi never runs the import lane and no lane launches
    # it today, so nothing reports them to anyone.
    Agent.PI: ("--no-extensions", "--no-skills", "--no-context-files", "--model"),
}

#: WHICH help to ask, per agent, because the flags do not live in the same
#: place. Claude takes its options on the root command; Codex takes ours on the
#: `exec` SUBCOMMAND -- `codex --help` does not mention `--json` or
#: `--skip-git-repo-check` at all. Probing the root for Codex reports every
#: install, current ones included, as missing both: `too_old` then refuses
#: every Codex import with an upgrade instruction that cannot help, and on a
#: Codex-only machine backfill stops working entirely.
HELP_ARGV: dict[Agent, tuple[str, ...]] = {
    Agent.CLAUDE: ("--help",),
    Agent.CODEX: ("exec", "--help"),
    # pi takes everything on the root command; there is no subcommand.
    Agent.PI: ("--help",),
}

#: `--help` should answer instantly. A binary that cannot is a binary we are
#: about to hand a folder to for an hour, so a short bound is generous.
HELP_TIMEOUT_S = 20

#: An option DEFINITION line: indented, optionally a short form first, then the
#: long form. Anchored on purpose -- a bare scan of the help text also matches
#: flags named inside OTHER options' descriptions, and `claude --help` has
#: three of those today (`--allowed-tools`, `--background`,
#: `--disallowed-tools`). Reading a cross-reference as support is the guard
#: failing open on precisely the crash it exists to prevent.
_OPTION_LINE = re.compile(r"^\s{2,}(?:-[A-Za-z]\w*,\s*)?(--[A-Za-z][\w-]*)", re.M)


def _has(supported: frozenset[str] | None, flag: str) -> bool:
    """Whether `flag` may be passed. UNKNOWN counts as yes.

    The probe failing must never be the thing that removes a flag: that would
    turn a slow machine into a silently degraded import, which is the failure
    class this whole guard exists to close.
    """
    return supported is None or flag in supported


def supported_flags(binary: str, agent: Agent = Agent.CLAUDE) -> frozenset[str] | None:
    """Long options `binary --help` advertises, or None if it would not say.

    THE PROBE, AND WHY IT IS A PROBE. The CLI hands the agent binary a fixed
    argv, and an agent CLI parses options strictly: one it does not recognise
    is a non-zero exit before it reads a single file. Anthrogen hit this on
    2026-08-12 -- `--autocompact` had landed in #194 six days earlier, their
    Claude Code predated it, and all 33 classify slices died identically with
    `error: unknown option '--autocompact'`. The import reported "the
    classification did not produce a usable plan" and nothing else.

    ASKING THE BINARY, not comparing versions. A floor means knowing which
    release added each flag, writing it down, and remembering to raise it every
    time a flag is added -- and the failure of forgetting is silent and total.
    `--help` is the same question asked of the thing that will actually answer
    it, and it stays correct for flags nobody has written yet.

    ASKING THE RIGHT HELP. The flags are not all on the root command -- see
    `HELP_ARGV`. Getting this wrong does not fail open: the wrong subcommand
    answers rc 0 with a real option list, so every flag we care about reads as
    missing and the guard refuses a binary that was fine.

    None on ANY doubt -- non-zero exit, timeout, unreadable output. See `_has`:
    unknown means "pass the flag", so a broken probe leaves behaviour exactly
    as it was rather than quietly stripping the argv.
    """
    return _supported_flags_cached(binary, HELP_ARGV[agent])


@lru_cache(maxsize=8)
def _supported_flags_cached(binary: str, help_argv: tuple[str, ...]) -> frozenset[str] | None:
    """One help call per (binary, subcommand) per process. See `supported_flags`."""
    try:
        done = subprocess.run(
            [binary, *help_argv],
            capture_output=True,
            text=True,
            timeout=HELP_TIMEOUT_S,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if done.returncode != 0:
        return None
    found = set(_OPTION_LINE.findall(done.stdout or ""))
    # An empty parse is a help text we did not understand, not a binary with no
    # options. Treating it as "supports nothing" would strip every flag.
    return frozenset(found) or None


def unsupported_flags(agent: Agent, binary: str) -> tuple[list[str], list[str]]:
    """``(required_missing, optional_missing)`` for this binary."""
    supported = supported_flags(binary, agent)
    if supported is None:
        return [], []
    return (
        [f for f in REQUIRED_FLAGS[agent] if f not in supported],
        [f for f in OPTIONAL_FLAGS[agent] if f not in supported],
    )


def too_old(agent: Agent, binary: str) -> str | None:
    """Why this binary cannot run an import, or None if it can.

    Checked ONCE, before the folder is walked. Per-invocation would be correct
    and useless: the walk is minutes on the drives this feature is for, and
    finding out afterwards -- 33 times, once per slice -- is what actually
    happened.
    """
    missing, _ = unsupported_flags(agent, binary)
    if not missing:
        return None
    return (
        f"{_describe(agent, binary)} is too old for the import: it does not "
        f"accept {', '.join(missing)}. Upgrade {AGENT_COPY[agent][0]} and "
        "re-run — nothing was read."
    )


def _describe(agent: Agent, binary: str) -> str:
    """`This Claude Code (1.0.4)`, or without the version when it would not say.

    NAMING THE VERSION. "Upgrade Claude Code" is advice the reader cannot check
    against anything: they do not know what they have, and neither did we --
    `doctor` recorded a boolean until 0.79.0. With the number in the sentence
    they can compare it to the release notes, and a bug report carries the one
    fact that would otherwise take a round trip to establish.

    Omitted rather than guessed when the probe could not read it: `This Claude
    Code (unknown)` reads like a broken install on top of an old one.
    """
    name = AGENT_COPY[agent][0]
    version = _agent_version_cached(binary)
    return f"This {name} ({version})" if version else f"This {name}"


def degraded_note(agent: Agent, wanted: tuple[str, ...] = ()) -> str | None:
    """What this binary is too old to be given, or None if nothing.

    Said out loud rather than dropped quietly. Each of these costs something a
    reader would want to know about: without `--autocompact` a long
    classification has less context headroom, and without the isolation flags
    the agent runs with whatever MCP servers and slash commands the user has
    configured, inside an import that is supposed to see only the folder.

    `wanted` are the settings flags THIS import would send (`--model`,
    `--effort`; `import_agent_settings.AgentSettings.flags`): named when the
    binary would drop them, never when the import does not use them.
    """
    binary = which_agent(agent)
    if binary is None:
        return None
    _, optional = unsupported_flags(agent, binary)
    supported = supported_flags(binary, agent)
    optional += [flag for flag in wanted if not _has(supported, flag) and flag not in optional]
    if not optional:
        return None
    return (
        f"{_describe(agent, binary)} does not accept {', '.join(optional)}, so "
        "the import runs without them. It will work; upgrade "
        f"{AGENT_COPY[agent][0]} for the isolation and context headroom they buy."
    )


def agent_version(agent: Agent) -> str | None:
    """The agent binary's own version string, or None.

    Recorded so the NEXT flag break is visible. `doctor` knew only whether the
    binary existed -- a boolean -- so a fleet-wide failure caused entirely by
    old Claude Code installs produced no signal at all, and the one report that
    surfaced it was a screenshot in a meeting.
    """
    from .....shared.harness.harnesses.claude_code import binary as claude_cli

    binary = which_agent(agent)
    if binary is None or claude_cli.already_hung(binary):
        return None
    return _agent_version_cached(binary)


@lru_cache(maxsize=8)
def _agent_version_cached(binary: str) -> str | None:
    from .....shared.harness.harnesses.claude_code import binary as claude_cli

    # `probe status --refresh` bounds every agent-CLI call (`claude_cli.bounded`).
    timeout = claude_cli.call_timeout(HELP_TIMEOUT_S)
    if timeout <= 0:
        return None
    try:
        done = claude_cli.capture([binary, "--version"], timeout=timeout)
    except subprocess.TimeoutExpired:
        claude_cli.timed_out(binary)
        return None
    except (OSError, subprocess.SubprocessError):
        return None
    if done.returncode != 0:
        return None
    first = (done.stdout or "").strip().splitlines()
    if not first:
        return None
    # "2.1.231 (Claude Code)" / "codex-cli 0.24.0" -- the number is the part
    # worth comparing, and the rest is branding that changes on its own.
    match = re.search(r"\d+\.\d+\.\d+", first[0])
    return match.group(0) if match else first[0][:32] or None
