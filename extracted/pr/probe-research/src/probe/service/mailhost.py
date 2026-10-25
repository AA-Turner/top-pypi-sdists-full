"""The reads mailbox and the approvals board, kept by the Probe service (plan Q2).

The service owns delivery: a daemon worker posts its messages, run alerts and
held questions here, and the hooks claim messages and answer held questions
here. The files stay the store, and every step is the one a caller without a
service takes itself, run on this module's one daemon thread with the same
functions on the same files (`probe.daemon.mailbox.rooted`: the session's own
state folder):

    mailbox.post   {sid, state_dir, deadline, message | question}
                   -> mailbox.publish_here / Board.save      -> {posted, kind}
                   (and `mailbox.changed` / `approvals.changed` at once)
    mailbox.claim  {sid, state_dir, deadline, names, by, token}
                   -> mailbox.claim, each name in order      -> {claimed, gone, late}
    mailbox.answer {state_dir, deadline, id, choice, channel, key}
                   -> Board.key_matches, Board.answer         -> {answered, sid, late}
                   (refused without the request's answer key; `channel` is
                   still required, as `protocol.need_mailbox_answer` checks it
                   for every service version, and never recorded)

THE DEADLINE. A caller that heard nothing (a service that stalled, or died
mid-request) does the step itself, but only once the request's deadline and a
moment past it are gone; this side never starts a step past the deadline, and
answers `late` only for a step it took back before it started (one that had
started is waited for, and its own answer sent). So the service and its
caller never both write a message, and a claim the service made for a caller
that lost the answer is found by its token in the claim log
(`reads_hook.claim_all`): nothing is lost or delivered twice across a restart,
a stall or a fallback. One step stuck (a hung network home) costs no one a
wait: a request behind it is refused at once (`busy`), and its caller works on
the files itself. The step itself is atomic on disk
(`os.replace`, `os.rename`), so an older worker or hook, pi's reader, or a
machine with no service, working on the files beside the service, stays right.

WHO MAY ANSWER (#3355). `mailbox.answer` writes a yes the daemon acts on, so
it takes one only with the held question's answer key (`approvals.Board.
mint_key`: `<state>/approvals/keys/<id>`, which the answer hook reads beside
the request). Any process of this user can reach the socket; a caller that
cannot read the approvals folder -- the agent's own shell, which the guard
keeps out of it -- cannot send the key, and is refused (`REFUSED`, nothing
written). A request filed before keys has none, so every answer to it is
refused here and the answer hook writes the answer file itself, exactly as
an older hook does on any refusal. Where the answer came from (`channel`)
is the service's to say, never the caller's: the one answer path that sends
the key is the answer hook's, after the question tool (`ANSWER_CHANNEL`).
A new question posted here gets its key written beside it (`Board.create`)
when its daemon did not write one, and the key is never sent back.

`probe.daemon.mailbox` and `approvals` are imported on the thread (stdlib
only, off the start path).
"""

from __future__ import annotations

import asyncio
import time
from collections.abc import Callable
from pathlib import Path

from .mailwatch import DaemonLane
from .protocol import MAILBOX_ID

#: What a handler waits past the deadline before it takes the step back.
GRACE_S = 0.25
#: The `channel` every answer recorded here carries: the one path that holds
#: the request's key and answers through this method is the answer hook, with
#: the person's pick from the harness's question tool. What the caller says is
#: never taken (#3355).
ANSWER_CHANNEL = "question-tool"
#: A step that has run this long is stuck (a hung network home, a FIFO): every
#: new request is refused at once (`busy`, nothing queued), and its caller does
#: the step on the files itself.
STUCK_S = 1.0
#: A step that had begun when its wait ran out is waited for this long more,
#: then given up on (its caller has long acted by then).
FINISH_S = 30.0


def _settled(future: asyncio.Future) -> None:
    if not future.cancelled():
        future.exception()


class MailHost:
    def __init__(self, *, log: Callable[[str], None]) -> None:
        self._log = log
        self._lane = DaemonLane("mailhost")

    def stuck(self) -> bool:
        return self._lane.running_for() > STUCK_S

    async def run(self, step: Callable[[dict], dict], request: dict) -> dict | None:
        """`step(request)` on the thread, and its answer. None when a step
        before it is stuck: nothing was queued. `{"late": True}` only when the
        step never started (it was taken back from the queue at the deadline):
        a step that started is waited for and its own answer returned (it
        starts nothing past the deadline), so `late` always means "nothing was
        done", and a caller acting on it never races the step."""
        if self.stuck():
            return None
        try:
            work = self._lane.submit(step, request)
        except RuntimeError:
            return None
        future = asyncio.wrap_future(work)
        wait = max(0.0, request["deadline_mono"] - time.monotonic()) + GRACE_S
        done, _ = await asyncio.wait({future}, timeout=wait)
        if done:
            return future.result()
        if work.cancel():
            return {"late": True}
        done, _ = await asyncio.wait({future}, timeout=FINISH_S)
        if done:
            return future.result()
        future.add_done_callback(_settled)
        self._log(f"mailbox: {step.__name__} for {request.get('sid') or request.get('id')} is stuck")
        return None

    def close(self) -> None:
        self._lane.close()

    # -- the thread ------------------------------------------------------------

    @staticmethod
    def post(request: dict) -> dict:
        """A message, or a held question, written as its caller would write it."""
        from probe.daemon import mailbox

        if time.monotonic() > request["deadline_mono"]:
            return {"posted": None, "late": True}
        sid, state = request["sid"], request["state"]
        if request["message"] is not None:
            msg = mailbox.Message.from_dict(request["message"])
            if msg is None or msg.session != sid or not MAILBOX_ID.fullmatch(msg.id):
                return {"error": "message is not a message of this session"}
            try:
                with mailbox.rooted(state, deadline=request["deadline_mono"]):
                    path = mailbox.publish_here(msg)
            except mailbox.Late:
                return {"posted": None, "late": True}
            return {"posted": path.name, "kind": "message", "late": False}
        from probe.daemon import approvals

        try:
            question = approvals.Request.from_json(request["question"])
        except (KeyError, TypeError, ValueError):
            return {"error": "question is not a held question"}
        if question.session_id != sid or question.state != approvals.WAITING or not MAILBOX_ID.fullmatch(
            str(question.id)
        ):
            return {"error": "question is not a waiting question of this session"}
        board = approvals.Board(Path(state) / "approvals")
        if board.get(question.id) is not None:
            # Written already (its caller wrote it, and may have moved it past
            # waiting since): never written over.
            return {"posted": question.id, "kind": "question", "late": False}
        try:
            with mailbox.rooted(state, deadline=request["deadline_mono"]):
                board.create(question)  # its answer key first, unless its daemon wrote one
        except mailbox.Late:
            return {"posted": None, "late": True}
        return {"posted": question.id, "kind": "question", "late": False}

    @staticmethod
    def claim(request: dict) -> dict:
        """Each named message taken once (`mailbox.claim`: one rename to
        `claimed/<stem>.<token>.json`, then a line in the claim log), in order,
        until the deadline. Its caller renames each to the plain name (its
        receipt) before it shows it. `gone`: taken by someone else, or not a
        message."""
        from dataclasses import asdict

        from probe.daemon import mailbox

        claimed: list = []
        gone: list = []
        with mailbox.rooted(request["state"]):
            folder = mailbox.messages_dir(request["sid"])
            for name in request["names"]:
                if time.monotonic() > request["deadline_mono"]:
                    return {"claimed": claimed, "gone": gone, "late": True}
                msg = mailbox.claim(request["sid"], folder / name, by=request["by"], token=request["token"])
                if msg is None:
                    gone.append(name)
                else:
                    claimed.append({"name": name, "message": asdict(msg)})
        return {"claimed": claimed, "gone": gone, "late": False}

    @staticmethod
    def answer(request: dict) -> dict:
        """The researcher's pick for a held question (`Board.answer`): False when
        it is no longer there, no longer waiting, or has expired; `{"refused":
        ...}`, with nothing written, when the caller did not send the
        question's answer key (`Board.key_matches`). The channel recorded is
        ANSWER_CHANNEL, whatever the caller said."""
        from probe.daemon import approvals

        if time.monotonic() > request["deadline_mono"]:
            return {"answered": None, "late": True}
        from probe.daemon import mailbox

        board = approvals.Board(Path(request["state"]) / "approvals")
        held = board.get(request["id"])
        if held is None:
            return {"answered": False, "sid": None, "late": False}
        if not board.key_matches(request["id"], request.get("key")):
            return {"refused": "the answer did not carry the held question's answer key"}
        try:
            with mailbox.rooted(request["state"], deadline=request["deadline_mono"]):
                answered = board.answer(request["id"], request["choice"], channel=ANSWER_CHANNEL)
        except mailbox.Late:
            return {"answered": None, "late": True}
        return {"answered": answered, "sid": held.session_id, "late": False}


__all__ = ["ANSWER_CHANNEL", "GRACE_S", "MailHost"]
