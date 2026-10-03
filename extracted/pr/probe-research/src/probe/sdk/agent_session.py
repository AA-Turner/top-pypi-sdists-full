"""Coding-agent session attribution for outbound Probe Research requests.

Every request carries the id of the coding-agent session driving it, when
there is one, so the backend can record which conversation produced a run and
search can walk from a session to the work that came out of it.

Same contract shape as :mod:`probe.client_headers`: validated, bounded, and
fail-open. Malformed input produces NO header rather than a bad one, and the
backend treats what does arrive as untrusted — it is recorded against the run
and never consulted for authorization. A spoofed id yields a dead link, never
access to someone else's transcript.

ONLY agents whose transcripts are actually captured are reported. Claude Code
ships with capture support. Codex is reported only when its tap has a local
credential, which is the durable evidence that this device completed pairing;
merely running under Codex must not create a transcript link that can never
resolve. pi ships with capture support like Claude Code. Cursor remains
detectable but uncaptured.
"""

from __future__ import annotations

import os
import re
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from . import homedir

#: Request headers naming the coding agent and its session.
AGENT_HEADER = "X-Probe-Agent"
AGENT_SESSION_HEADER = "X-Probe-Agent-Session"
#: The hosted MCP's opt-in, sent beside the two above: with it set to "1" and
#: the caller's session known, `search_knowledge` and `browse` leave out every
#: project, experiment and run THAT session created (the backend's
#: `exclude_origin_session`). The Probe daemon's reader sends it, because the
#: session it reads beside is being recorded as it goes, and its own fresh
#: records are never the team's prior work. Absent -> nothing changes.
HIDE_SESSION_WORK_HEADER = "X-Probe-Hide-Session-Work"

# Session ids are uuids today. The bound and charset are the real guard: this
# value is interpolated into an HTTP header, so anything with whitespace,
# control characters or header delimiters is rejected outright rather than
# escaped. Deliberately looser than a strict uuid match so a future agent that
# uses a different id shape still works without a client release.
_MAX_SESSION_LENGTH = 200
# \A/\Z, not ^/$: `$` also matches just before a trailing newline, and this
# exact string composes the cross-repo graph canonical_id, where a stray
# newline yields a node that silently never merges with the transcript side.
_SESSION_RE = re.compile(r"\A[A-Za-z0-9._:-]{8,200}\Z")

# Leading semver out of a version string that may carry a suffix. Claude Code
# reports "2.1.219 (Claude Code)", NOT a bare semver, so a strict parse finds
# nothing and every client looks too old.
_LEADING_SEMVER_RE = re.compile(r"^\s*(\d+)\.(\d+)\.(\d+)")


@dataclass(frozen=True)
class AgentSpec:
    """One coding agent and how to read its session out of the environment."""

    label: str
    """Matches the engine connector's agent label, so both sides compose the
    same graph canonical_id (``agent_session:{label}:{session_id}``)."""

    detect_env: tuple[str, ...]
    """Any one of these being set means we are running under this agent."""

    session_env: str | None
    """Where the session id lives, or None if the agent does not expose one."""

    captured: bool
    """Whether transcripts for this agent actually reach Research OS."""

    version_env: str | None = None
    min_version: tuple[int, int, int] | None = None
    """Below this version the agent does not export its session id at all."""

    display: str = ""


# The table is the harness registry's (probe/harness/harnesses.json): one row
# per coding agent, in DETECTION ORDER (the first whose marker is set wins).
# What the rows encode, and why:
#
# - Claude Code only exports CLAUDE_CODE_SESSION_ID to Bash subprocesses from
#   2.1.132 onward. Below that the variable is simply absent, which is
#   indistinguishable from "not Claude Code" unless we also read the version --
#   hence version_env, so an old client gets a "you need to upgrade" answer
#   instead of silence. There is deliberately no child-session handling:
#   CLAUDE_CODE_CHILD_SESSION is a BOOLEAN FLAG ("1"), not an id, and
#   CLAUDE_CODE_SESSION_ID still holds the real session id when it is set.
# - pi's CLI and RPC entry points always set PI_CODING_AGENT ("true") on every
#   child process and stamp PI_SESSION_ID too. pi ALSO sets the generic
#   AI_AGENT=pi, deliberately NOT used: a variable named for "any AI agent" is
#   exactly the one some other harness will export next, and misdetecting that
#   harness as pi is this table's worst failure.
# - Cursor is detected but never captured.
def _agents() -> tuple[AgentSpec, ...]:
    from probe.harness import get_registry

    return tuple(
        AgentSpec(
            label=h.id,
            detect_env=h.detect_env,
            session_env=h.session_env,
            captured=h.captured,
            version_env=h.version_env,
            min_version=h.min_version,
            display=h.display,
        )
        for h in get_registry().all()
    )


AGENTS: tuple[AgentSpec, ...] = _agents()


def _capture_paired(label: str, env: Mapping[str, str]) -> bool:
    """Whether this harness's tap has a credential, without reading the secret.

    For a harness whose session variable is set in every shell, Probe or not
    (Codex), a session is only worth attributing once capture is paired:
    otherwise the link could never resolve. The tap accepts its environment
    token or its mode-0600 token file; this checks presence only. The plugin
    dir override is also the tap's test/development hook, so this stays
    deterministic without touching a user's real state.
    """
    from probe.harness import get_registry

    capture = get_registry().get(label).capture
    if capture is None:
        return False
    if (env.get(capture.token_env) or "").strip():
        return True
    configured = env.get(capture.plugin_dir_env)
    if configured:
        root = Path(configured)
    else:
        current = homedir.home() / capture.plugin_dir
        legacy = homedir.home() / capture.legacy_plugin_dir if capture.legacy_plugin_dir else None
        root = legacy if legacy is not None and legacy.exists() and not current.exists() else current
    try:
        return bool((root / ".token").read_text(encoding="utf-8").strip())
    except OSError:
        return False


def _attribution_needs_pairing(label: str) -> bool:
    from probe.harness import get_registry

    return get_registry().get(label).attribution_requires_pairing


def _env(env: Mapping[str, str] | None) -> Mapping[str, str]:
    return os.environ if env is None else env


def detect_agent(env: Mapping[str, str] | None = None) -> AgentSpec | None:
    """The coding agent driving this process, or None."""
    e = _env(env)
    for spec in AGENTS:
        if any(e.get(key) for key in spec.detect_env):
            return spec
    return None


def parse_version(raw: object) -> tuple[int, int, int] | None:
    """Leading ``major.minor.patch`` from a version string, tolerating a suffix."""
    if not isinstance(raw, str):
        return None
    match = _LEADING_SEMVER_RE.match(raw)
    if not match:
        return None
    return (int(match.group(1)), int(match.group(2)), int(match.group(3)))


def valid_session_id(raw: object) -> bool:
    """Whether a value is safe and plausible enough to send as a header."""
    return isinstance(raw, str) and len(raw) <= _MAX_SESSION_LENGTH and bool(_SESSION_RE.match(raw))


def resolve_agent_session(
    env: Mapping[str, str] | None = None,
) -> tuple[str, str] | None:
    """``(agent_label, session_id)`` for the current session, or None.

    None whenever we are not under a supported agent, the agent's transcripts
    are not captured, the client is too old to export its session, or the value
    present is not header-safe. Never raises: attribution is telemetry, and a
    run must never fail to be created because of it.
    """
    spec = detect_agent(env)
    if spec is None:
        # No agent on THIS machine: a job a launcher shipped somewhere else
        # (Modal, Ray, Slurm) may still carry the session that launched it.
        return forwarded_agent_session(env)
    if not spec.captured or spec.session_env is None:
        return None
    values = _env(env)
    if _attribution_needs_pairing(spec.label) and not _capture_paired(spec.label, values):
        return None
    session_id = values.get(spec.session_env)
    if not valid_session_id(session_id):
        return None
    assert isinstance(session_id, str)  # narrowed by valid_session_id
    return (spec.label, session_id)


#: The agent session a LAUNCHER hands to the job it starts, as
#: ``<agent_label>:<session_id>``, next to ``PROBE_RUN_ID`` (audit E2). A remote
#: job (Modal, Ray, Slurm) has none of the agent's own variables, and forwarding
#: those would not be enough: detection keys on a MARKER (``CLAUDECODE``,
#: ``PI_CODING_AGENT``) that would make the job believe it IS the agent, and
#: Codex also needs a paired tap on the machine. So the session travels under
#: Probe's own name and is read ONLY when no agent is detected here, which keeps
#: every local process byte-identical to before. Same bounds as the header: a
#: malformed value is ignored, never sent.
FORWARDED_SESSION_ENV = "PROBE_AGENT_SESSION"


def forwarded_agent_session(env: Mapping[str, str] | None = None) -> tuple[str, str] | None:
    """``(agent_label, session_id)`` from :data:`FORWARDED_SESSION_ENV`, or None."""
    raw = (_env(env).get(FORWARDED_SESSION_ENV) or "").strip()
    label, sep, session_id = raw.partition(":")
    if not sep:
        return None
    captured = {spec.label for spec in AGENTS if spec.captured and spec.session_env}
    if label not in captured or not valid_session_id(session_id):
        return None
    return (label, session_id)


def forwarding_env(env: Mapping[str, str] | None = None) -> dict[str, str]:
    """What a launcher adds to a job's environment so the job's runs carry this
    session: ``{PROBE_AGENT_SESSION: "<agent>:<id>"}``, or ``{}`` outside one."""
    resolved = resolve_agent_session(env)
    if resolved is None:
        return {}
    return {FORWARDED_SESSION_ENV: f"{resolved[0]}:{resolved[1]}"}


def session_id_from_env(env: Mapping[str, str] | None = None) -> str | None:
    """This conversation's id, for the surfaces that only need to NAME it.

    Deliberately NOT ``resolve_agent_session``, whose extra gates exist for
    transcript attribution: it returns None when ``captured`` is false and when
    the Codex tap is unpaired, because an unattributable session must not be
    stamped on a run. The tracking switch asks a different question -- WHICH
    conversation am I -- and a session nobody captures is still a session whose
    tracking the researcher may turn off. Gating this on capture is what made
    ``probe session status`` unreadable under pi, and it would have refused
    Cursor too.

    The env-var-per-agent knowledge stays in ``AGENTS`` and nowhere else: the
    CLI used to hardcode Claude Code's and Codex's own variables, so pi's
    ``PI_SESSION_ID`` was already in the table above and still resolved to
    nothing.
    """
    resolved = session_agent_from_env(env)
    return resolved[1] if resolved else None


def session_agent_from_env(env: Mapping[str, str] | None = None) -> tuple[str, str] | None:
    """``(agent_label, session_id)`` for this conversation: `session_id_from_env`
    plus WHICH coding agent's variable carried the id (daemon reads: `probe ask`
    and `probe session track` answer by that agent's "Who records" profile).
    Same resolution order, so the two can never name different sessions."""
    values = _env(env)
    # A DEDICATED marker first. `detect_agent` returns the first spec matching
    # any `detect_env`, and Codex's `CODEX_THREAD_ID` is both its marker and its
    # id -- so a stale Codex id exported into a pi shell detects as Codex and
    # wins, purely because Codex sits higher in the table. A variable that is
    # only ever a marker (`PI_CODING_AGENT`, `CODEX_SANDBOX`, `CLAUDECODE`) is
    # strictly better evidence of which agent is running than one that doubles
    # as payload, so it is consulted first. `detect_agent` itself is unchanged:
    # its ordering is load-bearing for attribution elsewhere.
    for candidate in AGENTS:
        if candidate.session_env is None:
            continue
        markers = [key for key in candidate.detect_env if key != candidate.session_env]
        if not markers or not any(values.get(key) for key in markers):
            continue
        session_id = values.get(candidate.session_env)
        if valid_session_id(session_id):
            assert isinstance(session_id, str)
            return (candidate.label, session_id)
    spec = detect_agent(env)
    if spec is not None and spec.session_env is not None:
        session_id = values.get(spec.session_env)
        if valid_session_id(session_id):
            assert isinstance(session_id, str)
            return (spec.label, session_id)
    # Detection FIRST, then any session variable we know of. The fallback runs
    # only when no agent marker matched at all, which is a shell someone set up
    # by hand -- and refusing those would be a regression: the two hardcoded
    # variables this replaced needed no marker, so `CLAUDE_CODE_SESSION_ID=x`
    # alone used to resolve and must keep resolving. Table order decides if a
    # hand-made env somehow carries two, which is deterministic and documented.
    for candidate in AGENTS:
        if candidate.session_env is None:
            continue
        session_id = values.get(candidate.session_env)
        if valid_session_id(session_id):
            assert isinstance(session_id, str)
            return (candidate.label, session_id)
    return None


def outdated_client(env: Mapping[str, str] | None = None) -> tuple[str, str] | None:
    """``(display_name, minimum_version)`` when the agent is too old to attribute.

    Distinguishes "your Claude Code predates session export" from "you are not
    running a coding agent", so the one-time upgrade nudge only fires at people
    it can actually help. None when there is nothing to say.
    """
    spec = detect_agent(env)
    if spec is None or not spec.captured or spec.min_version is None or spec.version_env is None:
        return None
    # Already attributing: nothing to nudge about.
    if resolve_agent_session(env) is not None:
        return None
    current = parse_version(_env(env).get(spec.version_env))
    if current is None or current >= spec.min_version:
        # Unknown or new-enough version: the session is missing for some other
        # reason, and telling someone to upgrade would be wrong.
        return None
    return (spec.display, ".".join(str(part) for part in spec.min_version))


def agent_session_headers(env: Mapping[str, str] | None = None) -> dict[str, str]:
    """Headers naming the current agent session, or ``{}`` — never a blank header."""
    resolved = resolve_agent_session(env)
    if resolved is None:
        return {}
    agent, session_id = resolved
    return {AGENT_HEADER: agent, AGENT_SESSION_HEADER: session_id}


#: The two values `authored_by` takes on the wire. Spelled as literals rather
#: than imported from `probe._generated.models.Authorship` on purpose: this
#: module is stdlib-only (see the header — a Miles actor spilling metric
#: batches must not drag pydantic in), and the enum is a `StrEnum` whose members
#: serialize to exactly these strings. `agent/tests/test_authorship_default.py`
#: pins the two spellings against the generated enum so they cannot drift.
AUTHORSHIP_AGENT = "agent"
AUTHORSHIP_HUMAN = "human"


def default_authorship(env: Mapping[str, str] | None = None) -> str | None:
    """``"agent"`` when a coding agent is driving this process, else ``None``.

    THE ONE HEURISTIC IN THE AUTHORSHIP PATH, and it answers the only question
    the environment can answer. Whether a PROGRAM is running the command is
    readable from `AGENTS`; who COMPOSED the words is not -- a researcher
    dictating a title to a coding agent and that agent inventing one are
    identical from here. `app/core/authorship.py` states the rule this obeys:
    "the writer says which it is". So the writer (the agent composing the
    command) overrides with `--authored-by`, and this only supplies the default
    when it says nothing.

    NONE, NEVER ``"human"``. A missing `authored_by` means "this caller has not
    been taught to say", and the server then applies its historical inference.
    Returning `"human"` here would be a NEW claim about a person, made by a
    heuristic, which is the exact move that module exists to prevent -- and it
    keeps a person typing in a bare terminal byte-identical on the wire to
    every release before this one.

    `detect_agent` rather than `resolve_agent_session`: the latter's extra gates
    (captured transcripts, a paired Codex tap) exist for ATTRIBUTION, and an
    uncaptured agent -- Cursor -- is still a program composing a name.
    """
    return AUTHORSHIP_AGENT if detect_agent(env) is not None else None
