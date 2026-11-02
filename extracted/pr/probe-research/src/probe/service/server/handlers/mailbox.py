"""mailbox.post/claim/answer: write, take or answer a session's messages within the caller's deadline."""

from __future__ import annotations
from ...mail.mail import MailHost
from ...mail.watch import default_state
from ....foundation.service_api.vocabularies import (
    MailboxPart,
    Topic)
from ....foundation.service_api.wire import (
    ErrorCode,
    RpcError,
    invalid_params)
from ....foundation.service_api.params import (
    need_mailbox_answer,
    need_mailbox_claim,
    need_mailbox_post)
from probe.service.server.connections.connections import Connection
#: `mailbox.answer`'s `key` (a held question's answer key, 64 hex characters:
#: `probe.shared.mailbox.approvals.KEY_HEX_CHARS`) is at most this long; checked in full
#: on the mailbox thread (`Board.key_matches`).
MAX_ANSWER_KEY = 128


class MailboxHandlersMixin:
    """Part of Service: its methods run with `self` the Service; compose() folds them into Service."""

    # -- the mailbox (plan Q2) -----------------------------------------------

    async def _mailbox_post(self, conn: Connection, params: dict) -> dict:
        """`mailbox.post`: a message or a held question written for its session
        (`mailhost.MailHost.post`), and its watchers told at once. Never for a
        caller in a sandbox, which writes the file itself; and only from the
        session's own daemon worker (#3361, `_refuse_foreign_mail`)."""
        request = need_mailbox_post(params)
        await self._refuse_sandboxed(conn)
        await self._refuse_foreign_mail(conn, request["sid"], claim=False)
        request["state"] = request["state_dir"] or default_state()
        answer = self._mailbox_answered(await self.mailhost.run(MailHost.post, request))
        if "error" in answer:
            raise invalid_params(answer["error"])
        if answer.get("posted"):
            if answer.get("kind") == "question":
                self._emit(Topic.APPROVALS_CHANGED, {"sid": request["sid"], "ids": [answer["posted"]]})
            else:
                self._emit(Topic.MAILBOX_CHANGED, {"sid": request["sid"], "parts": [MailboxPart.MESSAGES]})
        return answer

    async def _mailbox_claim(self, conn: Connection, params: dict) -> dict:
        """`mailbox.claim`: the named messages taken once for the caller to show
        (`mailhost.MailHost.claim`). Never for a caller in a sandbox, and only
        from inside the session's own agent or a hook host (#3361,
        `_refuse_foreign_mail`)."""
        request = need_mailbox_claim(params)
        await self._refuse_sandboxed(conn)
        await self._refuse_foreign_mail(conn, request["sid"], claim=True)
        request["state"] = request["state_dir"] or default_state()
        answer = self._mailbox_answered(await self.mailhost.run(MailHost.claim, request))
        if answer.get("claimed"):
            self._emit(Topic.MAILBOX_CHANGED, {"sid": request["sid"],
                                               "parts": [MailboxPart.CLAIMED, MailboxPart.MESSAGES]})
        answer.setdefault("claimed", [])
        answer.setdefault("gone", [])
        return answer

    async def _mailbox_answer(self, conn: Connection, params: dict) -> dict:
        """`mailbox.answer`: the researcher's pick for a held question
        (`mailhost.MailHost.answer`). Never for a caller in a sandbox, and
        never without the question's answer key (`key`, which the answer hook
        reads beside the request; #3355): any process of this user reaches
        this socket, and a yes recorded here is one the daemon acts on. A
        refusal writes nothing, and its caller (an answer hook, of any
        version) writes the answer file itself, which only a caller with the
        approvals folder can. The caller's `channel` is checked (an older
        service requires it) and never recorded: the service names it."""
        request = need_mailbox_answer(params)
        key = params.get("key")
        if key is not None and not (isinstance(key, str) and len(key) <= MAX_ANSWER_KEY):
            raise invalid_params(f"key must be a string of at most {MAX_ANSWER_KEY} characters")
        request["key"] = key
        await self._refuse_sandboxed(conn)
        request["state"] = request["state_dir"] or default_state()
        answer = self._mailbox_answered(await self.mailhost.run(MailHost.answer, request))
        if "refused" in answer:
            raise RpcError(ErrorCode.REFUSED, f"refused: {answer['refused']}")
        if answer.get("answered") and answer.get("sid"):
            self._emit(Topic.APPROVALS_CHANGED, {"sid": answer["sid"], "ids": [request["id"]]})
        return answer

    @staticmethod
    def _mailbox_answered(answer: dict | None) -> dict:
        """A step's answer, or `busy` when none came (a stuck step before it,
        or this one): its caller then works on the files itself."""
        if answer is None:
            raise RpcError(ErrorCode.BUSY, "busy: the mailbox is stuck on a file; work on the files directly")
        return answer
