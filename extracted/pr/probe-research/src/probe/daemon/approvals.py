"""One shared way to ask the researcher (daemon v2, D22 / S14).

A daemon action that needs a person's yes is HELD. The daemon writes the exact
question (facts first, read from Probe or from plain code; its own reason
labelled and capped), the coding agent is asked to put it to the researcher word
for word through its question tool, and the researcher's pick comes back through
a hook the agent cannot answer for. Where the harness has no question tool, the
researcher answers in their own terminal (`probe approvals`).

Every question is a POLICY registered here: when it applies, the facts it shows,
how it renders, what binds the answer (a fingerprint of the facts). Channels,
CLI, hooks and logbook never change when a policy is added.

    delete.others_data     a delete whose target or anything under it was made by
                           another researcher (R13)
    delete.permanent       a delete Probe cannot undo (no trash behind it: an
                           artifact, a note, a paper, a view, an edge...), whoever
                           made what it deletes
    shell.unsafe_command   a daemon shell command not on the safe list (D15); a
                           script it runs is shown too, and bound by its hash
    check.override         a command a pre-check blocked, which the daemon thinks
                           is a false alarm (D14)
    team_note.edit         a change to the team note, which is rendered into every
                           teammate's agent instructions: shown as a diff

BYPASS MODE (Richard, 2026-09-26: "Bypass means bypass"): when the session runs
with the harness's approvals off, nothing is asked -- secrets included -- and the
logbook says "auto-approved: bypass mode". When the mode cannot be read, the
daemon asks.

The files: `<state>/probe/approvals/requests/<id>.json` (written by the daemon,
read by the hooks and `probe approvals`), `<state>/probe/approvals/answers/<id>.json`
(written by the answer hook, `probe approvals` or `probe deny`, read by the
daemon). Plain JSON on purpose: the hooks are stdlib Python 3.9. A request
file is created exclusively (its id is never reused while it exists), and
resolved or expired requests are deleted with their answers after
`KEEP_RESOLVED_S`; the daemon's own logbook keeps the record. A bypass-mode
auto-approval writes no file at all: nothing reads one.

WHAT A YES RUNS. The question shows the action; the request binds it. `action`
is a digest of the held action itself (the raw command or argv, and its
folder), so `verify_held` refuses a request whose held action was edited on
disk after the question was asked. The daemon checks it before it runs a yes.

NOTHING IS CUT. A question shows the whole command or change, never a part of
it: a yes runs all of it. A command longer than `COMMAND_CHARS` is refused
before it is asked (the daemon splits it), and so is a command whose script is
longer than `SCRIPT_CHARS` (the question shows the script's text); a team-note change
too long for the question tool is asked in the terminal only (`terminal_only`:
the hook refuses the question tool for it, and `probe approvals` prints it whole).
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import secrets as _random
import shlex
import tempfile
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable

WAITING = "waiting"
APPROVED = "approved"
DENIED = "denied"
EXPIRED = "expired"
VOID = "void"
AUTO = "auto-approved: bypass mode"

REASON_CHARS = 200
#: The longest command a question shows. The daemon asks about nothing longer:
#: a question never cuts what a yes runs.
COMMAND_CHARS = 300
#: The most script text a shell question shows (the scripts a held command runs,
#: all together). The daemon asks about nothing longer.
SCRIPT_CHARS = 1500
DEFAULT_EXPIRY_S = 7 * 86400
#: Resolved and expired requests (and their answers) are deleted this long after.
#: Longer than any expiry, so a recent NO is still found (`find_same`).
KEEP_RESOLVED_S = 14 * 86400
#: Ids are random hex: 8 characters is 4 billion, and a file is created only if
#: its id is free, so a collision costs one more draw, never a reused id.
ID_HEX_CHARS = 8
ID_ATTEMPTS = 32
YES = "yes"
NO = "no"


def approvals_dir() -> Path:
    base = os.environ.get("XDG_STATE_HOME") or str(Path.home() / ".local" / "state")
    return Path(base) / "probe" / "approvals"


@dataclass
class Question:
    header: str  # "Probe 7f3a09c1"
    question: str
    yes_label: str
    no_label: str
    #: Too long for the harness's question tool: answered only in a terminal
    #: (`probe approvals`, which prints it whole); the hook refuses the tool for it.
    terminal_only: bool = False

    def options(self) -> list[str]:
        return [self.yes_label, self.no_label]


@dataclass
class Request:
    id: str
    policy: str
    session_id: str
    question: Question
    facts: dict
    fingerprint: str
    held: dict  # what runs on a yes: {"kind": "probe"|"shell", "argv"|"command", "op_id", "cwd"}
    state: str = WAITING
    asked_at: float = 0.0
    answered_at: float | None = None
    channel: str | None = None
    expires_at: float = 0.0
    outcome: str | None = None
    action: str = ""  # digest of `held` without its op id (`verify_held`)

    def to_json(self) -> dict:
        data = asdict(self)
        data["question"]["options"] = self.question.options()
        return data

    @classmethod
    def from_json(cls, data: dict) -> "Request":
        q = dict(data["question"])
        q.pop("options", None)
        return cls(**{**data, "question": Question(**q)})


@dataclass
class Policy:
    """`applies` decides from the held action and its facts; `facts` reads them
    (plain code, Probe reads); `render` writes the question; `fingerprint` is what
    a later yes must still match."""

    name: str
    render: Callable[[dict, str], Question]
    fingerprint: Callable[[dict], str]
    expires_after: float = DEFAULT_EXPIRY_S


def _digest(*parts: object) -> str:
    return hashlib.sha256(json.dumps(parts, sort_keys=True, default=str).encode()).hexdigest()[:32]


def short_id() -> str:
    """A fresh random id for a request or a pre-check block."""
    return _random.token_hex(ID_HEX_CHARS // 2)


def action_digest(held: dict) -> str:
    """What a yes would run, as one digest. The op id is left out: it is minted
    per proposal, and the same action proposed twice is the same question."""
    return _digest({k: v for k, v in (held or {}).items() if k != "op_id"})


def verify_held(req: "Request") -> bool:
    """Does the request's held action still match what the researcher was asked?

    Recomputes the action digest from `req.held` and the policy fingerprint from
    `req.facts`, re-renders the question from the facts (the words shown must be
    the words the facts make), and binds the facts to the held action: a shell
    command is the one shown, in the folder shown; an override's argv renders to
    the command shown; a delete is a delete; a team-note change is a heredoc or
    `notes sync` (its document is re-read by `tools.held_refusal`, and a delete's
    facts by the worker). False on any mismatch, or when the request predates the
    digest: the caller then refuses to run it. Call this, and `lease.may_write`,
    right before running a yes.

    This binds the parts of the request to each other and to the question. It
    is NOT a signature: the request is a file of the same user, and a process of
    that user could rewrite all of it consistently before the question is shown."""
    pol = POLICIES.get(req.policy)
    if pol is None or not req.action:
        return False
    try:
        shown = pol.render(req.facts, req.question.header)
    except (KeyError, TypeError, ValueError):
        return False
    return (hmac.compare_digest(action_digest(req.held), req.action)
            and hmac.compare_digest(pol.fingerprint(req.facts), req.fingerprint)
            and req.question.header == f"Probe {req.id}" and shown == req.question
            and _bound(req.policy, req.facts or {}, req.held or {}))


def override_command(argv: list[str]) -> str:
    """The command an override question shows: each argument scrubbed on its own,
    so a redaction can hide a flagged value, never swallow the arguments after it."""
    return "probe " + shlex.join(_clean(str(arg)) for arg in argv)


def _bound(policy: str, facts: dict, held: dict) -> bool:
    """The facts a question was rendered from describe the held action."""
    argv = held.get("argv")
    if policy == "shell.unsafe_command":
        return (held.get("kind") == "shell" and facts.get("command") == held.get("command")
                and facts.get("cwd") == held.get("cwd"))
    if policy == "check.override":
        return (held.get("kind") == "probe" and isinstance(argv, list)
                and facts.get("command") == override_command(argv))
    if policy == "delete.permanent":
        from probe.daemon import precheck

        if held.get("kind") != "probe" or not isinstance(argv, list) or facts.get("command") != override_command(argv):
            return False
        try:
            parsed = precheck.parse([str(a) for a in argv])
        except precheck.ParseError:
            return False
        what = precheck.PERMANENT_DELETES.get(parsed.path)
        return what is not None and facts.get("what") == what
    if policy in ("delete.others_data", "team_note.edit") and held.get("kind") == "probe":
        from probe.daemon import precheck

        try:
            parsed = precheck.parse([str(a) for a in argv]) if isinstance(argv, list) else None
        except precheck.ParseError:
            return False
        if parsed is None:
            return False
        if policy == "delete.others_data":
            return parsed.path in precheck.CASCADE_DELETES
        return parsed.path == "notes sync" and not parsed.params.get("pull_only")
    return policy == "team_note.edit" and held.get("kind") == "shell" and isinstance(held.get("command"), str)


def _command(command: str) -> tuple[str, bool]:
    """The whole command, and whether it is too long for the question tool."""
    command = _clean(command)
    return command, len(command) > COMMAND_CHARS


def _reason(text: str | None) -> str:
    text = " ".join(_clean(text or "").split())
    return text[:REASON_CHARS - 1] + "…" if len(text) > REASON_CHARS else text


# ---------------------------------------------------------------------------
# The policies.
# ---------------------------------------------------------------------------


def _render_delete(facts: dict, header: str) -> Question:
    what = facts.get("what") or "this"
    name = facts.get("name") or facts.get("id")
    others = facts.get("others") or {}
    theirs = ", ".join(f"{n} of {who}'s {kind}" for (who, kind), n in _pairs(others)) or "data made by another researcher"
    reason = _reason(facts.get("reason"))
    restore = facts.get("restorable_until")
    text = f'Delete the {what} "{name}"? It holds {theirs}, which would go to the trash with it'
    text += f" (Probe can restore it until {restore})." if restore else "."
    if reason:
        text += f" The Probe daemon's reason: {reason}"
    return Question(header=header, question=text, yes_label="Delete it", no_label="Keep it")


def _pairs(others: dict) -> list[tuple[tuple[str, str], int]]:
    out = []
    for key, count in sorted(others.items()):
        who, _, kind = key.partition("|")
        out.append(((who, kind or "items"), int(count)))
    return out


def _clean(text: str) -> str:
    """The question lands in the chat, which is itself uploaded: no credential in it."""
    from probe.tap_core import secrets

    return secrets.redact(text or "")[0]


def _render_shell(facts: dict, header: str) -> Question:
    reason = _reason(facts.get("reason"))
    command, long = _command(facts["command"])
    text = f"The Probe daemon wants to run `{command}` in {facts['cwd']}."
    if facts.get("why_asking"):
        text += f" It isn't on the safe list: {facts['why_asking']}."
    if reason:
        text += f" The daemon's reason: {reason}"
    for script in facts.get("scripts") or []:
        if script.get("sha256"):
            text += (f"\nIt runs {script['path']} (sha256 {script['sha256'][:12]}), which reads:\n"
                     f"{_clean(script.get('text') or '')}")
    return Question(header=header, question=text + " Run it?", yes_label="Run it", no_label="Don't run it",
                    terminal_only=long)


def _render_permanent_delete(facts: dict, header: str) -> Question:
    reason = _reason(facts.get("reason"))
    command, long = _command(facts["command"])
    undo = facts.get("undo") or "cannot be undone"
    text = (f"The Probe daemon wants to delete {facts['what']}: `{command}`. This {undo}: Probe keeps no "
            "trash copy of it.")
    if reason:
        text += f" The daemon's reason: {reason}"
    return Question(header=header, question=text + " Delete it?", yes_label="Delete it", no_label="Keep it",
                    terminal_only=long)


def _scripts_key(facts: dict) -> list:
    """What binds a shell question to the scripts it showed (none: nothing added)."""
    scripts = facts.get("scripts") or []
    return [[(s.get("path"), s.get("sha256")) for s in scripts]] if scripts else []


def _render_override(facts: dict, header: str) -> Question:
    reason = _reason(facts.get("reason"))
    command, long = _command(facts["command"])
    text = f"A check blocked the Probe daemon's command `{command}`: {facts['blocked_because']}."
    if facts.get("masked"):
        text += f" Flagged: {facts['masked']}."
    if reason:
        text += f" The daemon says it's a false alarm: {reason}"
    return Question(header=header, question=text + " Run it anyway?", yes_label="Run it anyway",
                    no_label="Keep it blocked", terminal_only=long)


#: The longest team-note change the question tool shows; a longer one is asked in
#: the terminal only (`probe approvals` prints the whole diff).
TEAM_NOTE_DIFF_CHARS = 1500


def _render_team_note(facts: dict, header: str) -> Question:
    reason = _reason(facts.get("reason"))
    diff = _clean(facts.get("diff") or "")
    long = len(diff) > TEAM_NOTE_DIFF_CHARS
    text = ("The Probe daemon wants to change the team note, which is rendered into every teammate's agent "
            f"instructions ({facts.get('what') or 'an edit'}). ")
    if long:
        text += (f"The change is {len(diff.splitlines())} lines, too long to show here: answer in a terminal with "
                 "`probe approvals`, which prints all of it.\n")
    else:
        text += f"The change:\n{diff or '(no visible change)'}\n"
    if reason:
        text += f"The daemon's reason: {reason}\n"
    return Question(header=header, question=text + "Publish it?", yes_label="Publish it", no_label="Don't publish",
                    terminal_only=long)


POLICIES: dict[str, Policy] = {
    "delete.others_data": Policy(
        "delete.others_data", _render_delete,
        lambda f: _digest(f.get("id"), sorted((f.get("others") or {}).items()), f.get("updated_at"), f.get("count"))),
    "delete.permanent": Policy(
        "delete.permanent", _render_permanent_delete, lambda f: _digest(f.get("command"), f.get("what"))),
    "shell.unsafe_command": Policy(
        "shell.unsafe_command", _render_shell,
        lambda f: _digest(f.get("command"), f.get("cwd"), *_scripts_key(f))),
    "check.override": Policy(
        "check.override", _render_override, lambda f: _digest(f.get("command"), f.get("flagged"))),
    "team_note.edit": Policy(
        "team_note.edit", _render_team_note, lambda f: _digest(f.get("path"), f.get("text_sha"))),
}


def mask(secret: str) -> str:
    """The first 4 and last 2 characters (the question lands in the uploaded chat)."""
    secret = secret.strip()
    if len(secret) <= 8:
        return "…" * 3
    return f"{secret[:4]}…{secret[-2:]}"


# ---------------------------------------------------------------------------
# The board: requests on disk, shared by the daemon, the hooks and the CLI.
# ---------------------------------------------------------------------------


class Board:
    def __init__(self, root: Path | None = None, *, clock=time.time) -> None:
        self.root = root or approvals_dir()
        self.clock = clock
        (self.root / "requests").mkdir(parents=True, exist_ok=True)
        (self.root / "answers").mkdir(parents=True, exist_ok=True)

    def _path(self, kind: str, rid: str) -> Path:
        return self.root / kind / f"{rid}.json"

    def _write(self, path: Path, data: dict) -> None:
        """Atomic, through a temporary file of its own (two writers never share one)."""
        fd, tmp = tempfile.mkstemp(prefix=f".{path.stem}.", suffix=".tmp", dir=str(path.parent))
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(json.dumps(data, indent=1))
            os.replace(tmp, path)
        except BaseException:
            try:
                os.unlink(tmp)
            except OSError:
                pass
            raise

    def new_id(self) -> str:
        """A free request id, reserved by creating its file exclusively."""
        for _ in range(ID_ATTEMPTS):
            rid = short_id()
            try:
                fd = os.open(self._path("requests", rid), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            except FileExistsError:
                continue
            os.close(fd)
            return rid
        raise RuntimeError(f"no free approval id after {ID_ATTEMPTS} tries in {self.root / 'requests'}")

    def find_same(self, session_id: str, policy: str, fingerprint: str, action: str | None = None) -> Request | None:
        """The same action proposed again returns the same request (not a second question),
        and so does one the researcher said NO to recently (the caller says so, instead
        of asking again every bite)."""
        now = self.clock()
        for req in self.all(session_id=session_id):
            if req.policy != policy or req.fingerprint != fingerprint:
                continue
            if action is not None and req.action != action:
                continue
            if req.state == WAITING:
                return req
            if req.state == DENIED and now - (req.answered_at or req.asked_at) < POLICIES[policy].expires_after:
                return req
        return None

    def hold(self, *, policy: str, session_id: str, facts: dict, held: dict, bypass: bool,
             mode_known: bool = True) -> Request:
        """Ask (or find the same question already asked). The request comes back
        WAITING, APPROVED (bypass mode: nothing is asked and nothing is written to
        disk), or DENIED (the researcher already said no to exactly this)."""
        pol = POLICIES[policy]
        fingerprint = pol.fingerprint(facts)
        action = action_digest(held)
        now = self.clock()
        if bypass and mode_known:
            rid = short_id()
            return Request(id=rid, policy=policy, session_id=session_id, question=pol.render(facts, f"Probe {rid}"),
                           facts=facts, fingerprint=fingerprint, held=held, asked_at=now,
                           expires_at=now + pol.expires_after, state=APPROVED, answered_at=now, channel="bypass",
                           outcome=AUTO, action=action)
        self.prune()
        existing = self.find_same(session_id, policy, fingerprint, action)
        if existing is not None:
            return existing
        rid = self.new_id()
        req = Request(id=rid, policy=policy, session_id=session_id, question=pol.render(facts, f"Probe {rid}"),
                      facts=facts, fingerprint=fingerprint, held=held, asked_at=now,
                      expires_at=now + pol.expires_after, action=action)
        self._write(self._path("requests", rid), req.to_json())
        return req

    def prune(self) -> int:
        """Delete resolved and expired requests, with their answers, `KEEP_RESOLVED_S`
        after they settled, and answers whose request is gone. Returns how many."""
        cutoff = self.clock() - KEEP_RESOLVED_S
        removed = 0
        for path in list((self.root / "requests").glob("*.json")):
            req = self.get(path.stem)
            if req is None:
                try:  # an unreadable leftover (or a reservation a crash left empty)
                    if path.stat().st_mtime < cutoff:
                        path.unlink()
                        removed += 1
                except OSError:
                    pass
                continue
            settled = req.answered_at if req.state != WAITING else req.expires_at
            if settled and settled < cutoff:
                for stale in (path, self._path("answers", req.id)):
                    try:
                        stale.unlink()
                        removed += 1
                    except OSError:
                        pass
        for path in list((self.root / "answers").glob("*.json")):
            try:
                if not self._path("requests", path.stem).exists() and path.stat().st_mtime < cutoff:
                    path.unlink()
                    removed += 1
            except OSError:
                pass
        return removed

    def get(self, rid: str) -> Request | None:
        try:
            return Request.from_json(json.loads(self._path("requests", rid).read_text(encoding="utf-8")))
        except (OSError, ValueError, TypeError, KeyError):
            return None

    def save(self, req: Request) -> None:
        self._write(self._path("requests", req.id), req.to_json())

    def all(self, *, session_id: str | None = None, state: str | None = None) -> list[Request]:
        out = []
        for path in sorted((self.root / "requests").glob("*.json")):
            req = self.get(path.stem)
            if req is None or (session_id and req.session_id != session_id) or (state and req.state != state):
                continue
            out.append(req)
        return sorted(out, key=lambda r: r.asked_at)

    def waiting(self) -> list[Request]:
        now = self.clock()
        out = []
        for req in self.all(state=WAITING):
            if req.expires_at and now > req.expires_at:
                req.state, req.outcome = EXPIRED, "expired: nobody answered"
                self.save(req)
                continue
            out.append(req)
        return out

    def answer(self, rid: str, choice: str, *, channel: str) -> bool:
        """Record an answer (from the answer hook, `probe approvals` or `probe deny`).
        Only the exact yes label is a yes; anything else is a no. A request past its
        expiry takes no answer."""
        req = self.get(rid)
        if req is None or req.state != WAITING or (req.expires_at and self.clock() > req.expires_at):
            return False
        verdict = YES if choice == req.question.yes_label else NO
        self._write(self._path("answers", rid), {"id": rid, "answer": verdict, "choice": choice,
                                                  "channel": channel, "at": self.clock()})
        return True

    def take_answer(self, rid: str) -> dict | None:
        """The answer to a request, or None. An answer stamped outside the request's
        life (before it was asked, or after it expired) is ignored: a late yes
        never runs a stale action."""
        path = self._path("answers", rid)
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return None
        if not isinstance(data, dict):
            return None
        req = self.get(rid)
        if req is not None:
            try:
                at = float(data.get("at"))
            except (TypeError, ValueError):
                return None
            if at < req.asked_at or (req.expires_at and at > req.expires_at):
                return None
        return data

    def resolve(self, req: Request, *, state: str, outcome: str, channel: str | None = None) -> None:
        req.state, req.outcome, req.answered_at = state, outcome, self.clock()
        if channel:
            req.channel = channel
        self.save(req)

