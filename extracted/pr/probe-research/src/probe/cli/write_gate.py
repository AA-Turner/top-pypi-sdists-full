"""The `probe` CLI's own write gate: who may write to Probe from this session.

WHY IT LIVES IN THE CLI AND NOT IN A HARNESS HOOK. The agent's only write path
is this CLI -- the MCP is read-only, and SDK writes belong to the running
script -- and the CLI already knows which conversation it runs in on every
harness (`agent_session.session_id_from_env`: Claude Code, Codex and pi all
export their session id into the agent's own shell). A check here therefore
holds everywhere, including on pi, which has no pre-tool hook. The
plugin's guard hook keeps doing what only a hook can (refusing MCP reads under
`off`, the switch-flip claims, the after-the-fact notices); both read the same
command list and the same refusals from `session_marker`.

    argv after `probe`
      |
      +- no session id in env, or no state stored for it -----> allowed
      +- inside a run (PROBE_RUN_ID set), run data or a read --> allowed (the run's own data;
      |                                                          `artifact add` only onto that run)
      +- `--help` ---------------------------------------------> allowed
      +- `companion feedback` without --directed -------------> refused (DENY_REASON_DIRECTED)
      +- not a write (and not a read under `off`) -------------> allowed
      +- state read-only (writes) / off (writes AND reads) ---> refused; `exec` runs its
      |                                                          command UNRECORDED instead
      +- state full, or daemon with no live lease (degraded) --> allowed
      +- state daemon, live lease
           +- --directed ---------------------------------------> allowed; the daemon sees it
           +- launch / run data (DAEMON_AGENT_WRITES) ----------> allowed
           +- anything else ------------------------------------> refused (DENY_REASON_DAEMON)

ONLY A SESSION WITH A STORED STATE IS GATED. Claude Code, Codex (with trusted
hooks) and pi seed the state at session start (`probe session initialize`); a
shell that merely carries an id-shaped variable -- a person's own terminal, or
a harness that seeds nothing -- has none and is left alone, as is any shell
with no session id at all. The guard hook, which runs only inside an agent's
tool calls, still falls back to the folder and machine default.

A RUN'S OWN DATA IS NOT GATED. `probe exec` and the SDK export `PROBE_RUN_ID`
to the job; a `probe log`, `span add` or `trial add` in its script is the run
recording itself, which the switch has never governed (the SDK in the same
script is not gated either). So is a `probe artifact add` filed on THAT run --
its RUN argument is the `PROBE_RUN_ID` value (`session_marker.DAEMON_RUN_WRITES`):
the same file `log_artifact` would attach. Anything else -- a note, a rule, an
artifact filed on the project or on another run -- is gated there as everywhere.
"""

from __future__ import annotations

import os
from collections.abc import Mapping, Sequence

from ..sdk import agent_session, session_marker

#: Exit code for a refused write: distinct from usage (2) and failure (1) so a
#: script can tell "Probe said no" from "Probe broke".
EXIT_REFUSED = 3

#: Set by `probe exec` and the SDK in the job they launch.
RUN_ID_ENV = "PROBE_RUN_ID"

DENY_REASON_DIRECTED = (
    "`{matched}` corrects the Probe daemon on the researcher's behalf, so it was refused before "
    "it ran: from an agent session it runs only with `--directed`, when the researcher asked "
    "for it."
)

#: `probe session parent` from an agent session without `--directed`.
DENY_REASON_PARENT = (
    "`{matched}` records the researcher's answer about a `.probe.config`, so it was refused "
    "before it ran: it runs only with `--directed`, after they answered."
)

#: `artifact add` flags that file the artifact somewhere other than the run, so
#: inside a run it is no longer the run's own data. A `--from-manifest` row can
#: name its own anchor, so a manifest never counts as run-anchored.
NON_RUN_ANCHOR_FLAGS = frozenset(
    {"--project", "--experiment", "--workspace", "--shared", "--from-manifest"}
)

#: `artifact add` options that take NO value. Every other `--option` there takes
#: one, so its value is skipped when looking for the RUN argument. A new bare
#: flag missing from this list makes the next word read as its value: the RUN is
#: then not found and the write is gated as usual, never let through.
ARTIFACT_ADD_BARE_FLAGS = frozenset(
    {"--reference", "--hash", "--allow-missing", "--shared", "--sync", "--async", "--help"}
)

#: The prefix a CLI ref may carry (`id:<uuid>`); `PROBE_RUN_ID` never has it.
_ID_PREFIX = "id:"

#: What `probe exec` prints when the switch keeps the run from being recorded.
EXEC_UNRECORDED = (
    "Probe is {state} for this conversation, so `probe exec` opens no run; running the "
    "command directly."
)

#: What `probe exec` prints when a `.probe.config` excludes where it runs.
EXEC_EXCLUDED = (
    "`{path}` is excluded by `{source}`, so `probe exec` opens no run; running the command "
    "directly."
)


#: Writes a `.probe.config` `hash` path does NOT refuse (C9): the command records
#: only the file's identity. `exec` hashes what its command reads and writes
#: (and its `--input`/`--output` files); `dataset add` records a REFERENCE --
#: with `--upload` (`HASH_LEVEL_REFUSED_FLAGS`) it would send the bytes and is
#: refused as for `off`. A `hash` working directory refuses no write: the run
#: it opens records identities only.
HASH_LEVEL_WRITES = frozenset({"exec", "dataset add"})
#: Flags that make a `HASH_LEVEL_WRITES` command send a file's bytes.
HASH_LEVEL_REFUSED_FLAGS = frozenset({"--upload"})


def _hash_level_allowed(args: Sequence[str], words: Sequence[str]) -> bool:
    """Does this write record only identities of a `hash` path it names?"""
    own = list(args[: list(args).index("--")]) if "--" in args else list(args)
    if words[:1] == ["exec"]:
        return True
    if " ".join(words[:2]) in HASH_LEVEL_WRITES:
        return not any(a.split("=", 1)[0] in HASH_LEVEL_REFUSED_FLAGS for a in own)
    return False


def split_directed(args: Sequence[str]) -> tuple[list[str], bool]:
    """Remove every `--directed` before a standalone `--`; report whether one was there.

    The flag may appear anywhere after `probe` (`probe notes push ... --directed`
    is what the skill teaches), and the subcommand parsers do not know it, so it
    is taken out before they run. Everything after `--` belongs to the command
    `probe exec` launches and is left alone.
    """
    out: list[str] = []
    directed = False
    passthrough = False
    for arg in args:
        if not passthrough and arg == "--":
            passthrough = True
        elif not passthrough and arg == session_marker.DIRECTED_FLAG:
            directed = True
            continue
        out.append(arg)
    return out, directed


def _command_words(args: Sequence[str]) -> list[str]:
    """Everything before the first `--`: where a `--help` means help."""
    words: list[str] = []
    for arg in args:
        if arg == "--":
            break
        words.append(arg)
    return words


def _run_argument(args: Sequence[str]) -> str | None:
    """The first positional after the two command words (`artifact add RUN ...`).

    Root options before the command, and option values after it, are skipped;
    anything this cannot place reads as "no RUN", which keeps the write gated.
    """
    words = 0
    skip = False
    for token in _command_words(args):
        if skip:
            skip = False
            continue
        if token.startswith("-"):
            if words == 0:
                skip = token in session_marker.ROOT_VALUE_OPTIONS
            elif words == 2:
                skip = "=" not in token and token not in ARTIFACT_ADD_BARE_FLAGS
            continue
        if words < 2:
            words += 1
            continue
        return token
    return None


def _runs_own_file(args: Sequence[str], matched: str, run_id: str) -> bool:
    """Is this a `DAEMON_RUN_WRITES` command filed on THE run the job belongs to?

    Inside run r1, `probe artifact add r1 f.png` is r1 attaching its own file;
    `probe artifact add r2 f.png` is a write about another run, and it is gated.
    """
    if matched[len("probe ") :] not in session_marker.DAEMON_RUN_WRITES:
        return False
    if any(arg.split("=", 1)[0] in NON_RUN_ANCHOR_FLAGS for arg in _command_words(args)):
        return False
    run = _run_argument(args)
    if run is None:
        return False
    return run.removeprefix(_ID_PREFIX) == run_id.strip().removeprefix(_ID_PREFIX)


def refusal(
    args: Sequence[str],
    *,
    directed: bool,
    env: Mapping[str, str] | None = None,
) -> str | None:
    """The refusal message for this invocation, or None when it may run."""
    values = os.environ if env is None else env
    session_id = agent_session.session_id_from_env(env)
    if not session_id:
        return None
    words = session_marker.command_words(list(args))
    if words[:2] == ["session", "parent"] and len(words) > 2 and not directed:
        if session_marker.HELP_FLAG not in _command_words(args):
            return DENY_REASON_PARENT.format(matched="probe session parent " + words[2])
    state = session_marker.session_state(session_id)
    if state is None:
        return None
    if session_marker.HELP_FLAG in _command_words(args):
        return None  # asking what a command does is never a write
    kind, matched = session_marker.classify_probe_args(list(args))
    if kind is None:
        return None
    if values.get(RUN_ID_ENV) and (
        kind == "read"
        or session_marker.daemon_allows_agent(matched)
        or _runs_own_file(args, matched, values[RUN_ID_ENV])
    ):
        return None
    if matched[len("probe "):] in session_marker.DIRECTED_ONLY and not directed:
        return DENY_REASON_DIRECTED.format(matched=matched)
    if state == session_marker.STATE_OFF:
        return session_marker.DENY_REASON_OFF.format(matched=matched)
    if kind != "write":
        return None
    if state == session_marker.STATE_READ_ONLY:
        return session_marker.DENY_REASON.format(matched=matched)
    if state != session_marker.STATE_DAEMON:
        return None
    if directed or session_marker.daemon_allows_agent(matched):
        return None
    if session_marker.agent_writes_freely(session_id, state):
        return None  # degraded: fall back to the agent, never to silence
    return session_marker.DENY_REASON_DAEMON.format(matched=matched)


def exec_child(args: Sequence[str]) -> list[str] | None:
    """For a refused `probe exec ... -- CMD`, the CMD to run unrecorded, else None.

    Refusing `exec` outright would stop the training job itself -- inside a
    script, a Makefile or a sweep driver as much as at the agent's prompt -- and
    the switch only ever meant "record nothing", never "run nothing".
    """
    if session_marker.command_words(list(args))[:1] != ["exec"] or "--" not in args:
        return None
    child = list(args[list(args).index("--") + 1 :])
    return child or None


def _path_like(token: str, cwd: str, *, missing_ok: bool = False) -> str | None:
    """`token` as a path on disk worth checking, else None: one naming a folder
    (`a/b`, `./x`) or an existing file. A bare word that happens to be a folder
    name (`--name data`) is not a path."""
    value = token.split("=", 1)[1] if token.startswith("-") and "=" in token else token
    local = session_marker.probe_config().local_path_of(value)
    if local is not None:
        return local
    if not value or value.startswith("-") or "://" in value:
        return None
    full = os.path.join(cwd, os.path.expanduser(value))
    try:
        # Unmistakably a path (`/x`, `./x`, `../x`, `~/x`), or a path argument
        # (`artifact add RUN PATH`): counts whether or not it exists yet (an
        # `--allow-missing` reference). Otherwise only what exists: `--name
        # eval/data` or `meta-llama/Llama-3-8B` is not a path.
        if value.startswith(("/", "./", "../", "~")) or (missing_ok and os.sep in value):
            return full
        if os.sep in value:
            # Existing, or about to be written into an existing folder
            # (`--out out/run1`); `meta-llama/Llama-3-8B` is neither.
            return full if os.path.lexists(full) or os.path.isdir(os.path.dirname(full)) else None
        return full if os.path.isfile(full) else None
    except (OSError, ValueError):
        return None


#: Characters around a path inside a shell string (`<in`, `>out`, `$(cat x)`, `'x'`).
_SHELL_EDGES = "\"'`()$<>|;&{}"


def _pieces(token: str) -> list[str]:
    """`token`, and when it is a shell string (`sh -c "head -n 3 data/a.jsonl"`)
    each word inside it, stripped of quotes and redirection marks."""
    out = [token]
    if any(c.isspace() for c in token):
        import shlex

        try:
            words = shlex.split(token, posix=True)
        except ValueError:
            words = token.split()
        for word in words:
            for part in word.replace(">", " ").replace("<", " ").split():
                part = part.strip(_SHELL_EDGES)
                if part:
                    out.append(part)
    return out


def names_excluded(argv: Sequence[str], cwd: str, env: Mapping[str, str] | None = None) -> bool:
    """Does a command name -- as an argument, or as a word inside a shell
    string -- a path a `.probe.config` sets to anything but `on`? `probe exec`
    then keeps no console log (review of #2791): the step may print the
    file's records, and a `hash`, `read` or `off` path's text must never
    leave the machine. Best effort over what the command line shows; a path
    the command builds itself is beyond it. Never raises."""
    try:
        session_id = agent_session.session_id_from_env(env)
        for token in argv:
            for piece in _pieces(str(token)):
                full = _path_like(piece, cwd)
                if full is not None and session_marker.excluded(full, session_id).excluded:
                    return True
    except Exception:  # noqa: BLE001 - fails closed: keep no log
        return True
    return False


def excluded_refusal(args: Sequence[str], env: Mapping[str, str] | None = None) -> tuple[str, list[str] | None] | None:
    """`(message, child)` when a `.probe.config` keeps this command from recording.

    For any write, in any shell (a person's own terminal included: "never record"
    means never): refused when the working directory is excluded or a path it
    names is. `probe exec` instead runs its command unrecorded (`child`), as the
    switch does. Reads are never refused. Never raises."""
    try:
        if session_marker.HELP_FLAG in _command_words(args):
            return None
        words = session_marker.command_words(list(args))
        is_exec = words[:1] == ["exec"]
        kind, matched = session_marker.classify_probe_args(list(args))
        if kind != "write" and not is_exec:
            return None
        session_id = agent_session.session_id_from_env(env)
        cwd = os.getcwd()
        hit = None
        hash_ok = _hash_level_allowed(args, words)
        verdict = session_marker.excluded(cwd, session_id, as_cwd=True)
        if verdict.excluded and not getattr(verdict, "identity_only", False):
            hit = (cwd, verdict)
        else:
            missing_ok = words[:2] == ["artifact", "add"]
            option_value = False  # the token is the value of the option before it
            for token in args:
                if token == "--":
                    option_value = False
                    continue
                positional = not token.startswith("-") and not option_value
                option_value = token.startswith("-") and "=" not in token and token not in ARTIFACT_ADD_BARE_FLAGS
                full = _path_like(token, cwd, missing_ok=missing_ok and positional)
                if full is None:
                    continue
                verdict = session_marker.excluded(full, session_id)
                if verdict.excluded and not (hash_ok and getattr(verdict, "identity_only", False)):
                    hit = (full, verdict)
                    break
        if hit is None:
            return None
        pc = session_marker.probe_config()
        path, verdict = hit
        source = session_marker.verdict_source(verdict)
        if is_exec:
            return EXEC_EXCLUDED.format(path=pc.shown(path), source=source), exec_child(args)
        return (
            session_marker.EXCLUDED_DENY.format(path=pc.shown(path), source=source, matched=matched),
            None,
        )
    except Exception:  # noqa: BLE001 - a check never breaks the CLI
        return None

