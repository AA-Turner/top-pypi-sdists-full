"""The `probe` CLI's own write gate: who may write to Probe from this session.

WHY IT LIVES IN THE CLI AND NOT IN A HARNESS HOOK. The agent's only write path
is this CLI -- the MCP is read-only, and SDK writes belong to the running
script -- and the CLI already knows which conversation it runs in on every
harness (`agent_session.session_id_from_env`: Claude Code, Codex, pi and Cursor
all export their session id into the agent's own shell). A check here therefore
holds everywhere, including on pi and Cursor, which have no pre-tool hook. The
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
