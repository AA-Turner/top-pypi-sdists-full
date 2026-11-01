"""a failed run: tell a gateway failure from a refused key or a rejected history, and what the worker does next."""

from __future__ import annotations
from probe.daemon.worker.bite import bite as bite_mod
from probe.daemon.host import lease
from probe.daemon.agent import tools
from probe.daemon.worker import alerts
from probe.sdk.session_marker import WIZARD_HINT
from probe.daemon.store.logbook import CARRY_ON
from probe.daemon.store.device import LANE_WRITE
#: The model's gateway failing this many bites in a row (no HTTP answer, a timeout,
#: a 5xx) releases the lease (`gateway`): the agent records until a model round
#: answers again.
GATEWAY_FAILURES_BEFORE_RELEASE = 2
#: Bites in a row whose model thought until its token limit and answered nothing
#: (`agent.answered_nothing`) release the lease with the gateway's reason: the agent
#: records until a round answers again. Each such bite also waits longer before the
#: next (30 s doubling, BACKOFF_CAP_S at most), so a model that never answers costs
#: about two calls an hour, not one every few minutes forever (strand-ai 2026-10-12).
NO_ANSWERS_BEFORE_RELEASE = 3
STATE_DAEMON = lease.STATE_DAEMON


class FailuresMixin:
    """Part of Worker: its methods run with `self` the Worker; compose() folds them into Worker."""

    def _failed(self, bite_id: int, built: bite_mod.Bite, exc: Exception, usage=None,
                deps: tools.Deps | None = None, *, resumed: int | None = None) -> bool:
        """`resumed`: the conversation whose saved history this run continued. A
        failure that history can cause (`_history_rejected`, or a model that
        answered nothing: `agent.answered_nothing`) ends it, so the retry starts
        fresh from disk instead of sending the same history forever."""
        from pydantic_ai.exceptions import ModelHTTPError, UsageLimitExceeded

        from probe.daemon import agent as agent_mod

        text = f"{type(exc).__name__}: {exc}"[:2000]
        log.warning("bite %s failed: %s", bite_id, text)
        # What the model spent before it failed or was cut short counts in the bites
        # row (the device counter took each round as it came, `_record_round`).
        in_tok, out_tok, cached = _tokens(usage)
        spent = {"input_tokens": in_tok, "output_tokens": out_tok, "cached_tokens": cached}
        if self.replay is None and install_replaced():
            # Not a bug: the run read its own files after the CLI was reinstalled. No
            # ping, no failure; its events stay queued and the next poll leaves.
            self.store.close_bite(bite_id, outcome="stopped: reinstalled", error=text, **spent)
            return False
        if isinstance(exc, UsageLimitExceeded) and not _key_refused(deps):
            return self._cut_short(bite_id, built, text, spent)
        if agent_mod.answered_nothing(exc) and not _key_refused(deps):
            # The same request thinks to the limit again: never retried as it was, nor
            # backed off and deferred forever. The history it continued may be what
            # sets it off, so the retry is fresh from disk and smaller; each one in a
            # row waits longer, and NO_ANSWERS_BEFORE_RELEASE of them hand recording to
            # the agent until a round answers.
            if resumed is not None:
                self.store.end_conversation(resumed, f"{agent_mod.ANSWERED_NOTHING}: {text[:300]}")
            self.gateway_failures = 0  # the gateway answered: a 200, cut off at the limit
            self.no_answers += 1
            self.next_attempt_at = self.clock() + min(BACKOFF_CAP_S, 30 * (2 ** (self.no_answers - 1)))
            if self.no_answers >= NO_ANSWERS_BEFORE_RELEASE and self.released_reason is None:
                log.warning("the model answered nothing %s bites in a row: releasing the lease", self.no_answers)
                self._release(lease.REASON_GATEWAY)
                _device_error(f"session {self.session.session_id}: the daemon's model answered nothing "
                              f"{self.no_answers} bites in a row ({agent_mod.ANSWERED_NOTHING}); the agent records "
                              "until it answers again")
            return self._cut_short(bite_id, built, text, spent, cause=CutShort.NO_ANSWER, exc=exc)
        if _refusal_code(exc) == PROMPT_TOO_LARGE and not _key_refused(deps):
            # The route refused the prompt as over its ceiling (daemon cost round 4,
            # A): never sent, never billed. A continued conversation ends and the
            # bite runs again at once, fresh from disk (far under it) -- not a
            # failure, no ping. A fresh one over it is cut short like any other.
            if resumed is not None:
                with self.store.tx():
                    self._end_resumed(resumed, f"over the model route's ceiling: {text[:300]}")
                    self.store.close_bite(bite_id, outcome="over the ceiling: fresh", error=text, **spent)
                self.next_attempt_at = 0.0
                self.last_run_at = float("-inf")  # the fresh retry does not wait for the writer's gap
                return False
            return self._cut_short(bite_id, built, text, spent, cause=CutShort.TOO_LARGE, exc=exc)
        status = getattr(exc, "status_code", None) if isinstance(exc, ModelHTTPError) else None
        self.store.close_bite(bite_id, outcome="failed", error=text, **spent)
        if self._quota_inline(exc, STATE_DAEMON):
            return False
        if resumed is not None and _history_rejected(exc):
            log.warning("conversation %s: the model refused its saved history (%s): the next bite starts fresh "
                        "from disk", resumed, text[:200])
            with self.store.tx():
                self._end_resumed(resumed, f"the model refused its saved history: {text[:300]}")
        if _key_refused(deps):
            return self._refused_key("a `probe` command", probe=True)
        if status in (401, 403):
            reason = _REFUSAL_REASONS.get(_refusal_code(exc) or "") if status == 403 else None
            return self._refused_key(f"the model ({status})", reason=reason)
        if status in (402,) or "budget" in text:
            self._release(lease.REASON_BUDGET)
        else:
            alerts.report_bite_failure(exc, session_id=self.session.session_id, lane=LANE_WRITE)
        if _gateway_failure(exc):
            from probe.foundation.tls import network_down as offline

            self.gateway_failures += 1
            no_network = offline.no_network(exc)
            # Released while it had no network, and now it fails WITH one (back
            # behind a proxy, or our gateway down): said again, as not offline.
            again = self.released_reason == lease.REASON_GATEWAY and self.released_offline and not no_network
            if self.gateway_failures >= GATEWAY_FAILURES_BEFORE_RELEASE and (self.released_reason is None or again):
                # The model is unreachable: the agent records until a round answers again.
                log.warning("the model's gateway failed %s bites in a row: releasing the lease", self.gateway_failures)
                self._release(lease.REASON_GATEWAY, offline=no_network)
                _device_error(f"session {self.session.session_id}: the daemon's model failed "
                              f"{self.gateway_failures} times in a row ({text[:200]}); the agent records until it "
                              "answers again")
                # It answered, with an error: ours, not their network (a 504 is the model's timeout).
                if status is not None and status >= 500 and status not in alerts.USER_SIDE_STATUSES:
                    alerts.report(alerts.Kind.GATEWAY_DOWN, session_id=self.session.session_id, lane=LANE_WRITE,
                                  exc=exc, count=self.gateway_failures)
        else:
            self.gateway_failures = 0
        self.failures += 1
        wait = min(BACKOFF_CAP_S, 30 * (2 ** (self.failures - 1)))
        self.next_attempt_at = self.clock() + wait
        if self.failures >= FAILURES_BEFORE_BACK_OF_QUEUE:
            self._defer(built)
        return False

    def _end_resumed(self, conversation: int, why: str) -> None:
        """Inside a transaction: end a conversation that cannot go on (the model
        route refused its history or its size; its fingerprint or saved history no
        longer serves). A run of it that paused (CARRY_ON) had its events
        covered at the pause and never finished: its events go back on the queue
        for the fresh start (`Store.requeue_paused`, the newest paused run only),
        in the same transaction, so a crash cannot strand them (R2c; review 10-13).
        The loop detector and a model that answered nothing end conversations
        their own way: a skip, said in a notice."""
        self.store.end_conversation(conversation, why)
        if self.store.fact(CARRY_ON):
            self.store.requeue_paused()
            self.store.set_fact(CARRY_ON, None)

    def _refused_key(self, by: str, *, probe: bool = False, reason: str | None = None) -> bool:
        """The daemon's key was refused (by the model gateway or, `probe`, by Probe
        on a `probe` command): release the lease (`unauthorized`) and wait
        UNAUTHORIZED_RETRY_S. Not a failure that moves events to the back: the
        range stays queued for when the key works.

        `reason`: the server said why, and it is not the key (`_REFUSAL_REASONS`),
        so the message says that instead of sending anyone to approve a new key
        that would be refused the same way."""
        if probe:
            self.probe_refused_key = True
        self._release(lease.REASON_UNAUTHORIZED)
        if reason is not None:
            _device_error(f"{by} refused the Probe daemon: {reason}. A new key will not change that; "
                          "the agent records in the meantime")
        else:
            _device_error(f"the daemon's key was refused by {by}: Enter on Who records in the Probe wizard "
                          f"approves a new one ({WIZARD_HINT})")
        self.next_attempt_at = self.clock() + UNAUTHORIZED_RETRY_S
        return False

    async def _probe_accepts_key(self) -> bool:
        """After Probe refused the key: does it take it now (`GET /v1/me` answers
        200)? Only then may a model round take the lease back. Any failure --
        refused again, unreachable -- keeps the release."""
        from probe.daemon.session import probe_api

        try:
            await probe_api.whoami(probe_env(self.session.session_id))
        except Exception as exc:  # noqa: BLE001
            log.info("Probe still refuses the daemon's key (%s): the lease stays released", type(exc).__name__)
            return False
        log.info("Probe accepts the daemon's key again")
        self.probe_refused_key = False
        return True


def _key_refused(deps: tools.Deps | None) -> bool:
    """Did a `probe` command this run find Probe refusing the daemon's key? Set
    by `tools.run_probe_process` (`Deps.key_refused`); read defensively, so a
    Deps without the field reads as no."""
    return bool(getattr(deps, "key_refused", False))


#: A 403 from the model's route whose cause is the TEAM, not the key, by the
#: server's `CompanionErrorCode` (app/companion/router.py). A new key is refused
#: the same way, so the daemon says the cause. `companion_credential_required`
#: (the saved key is not the daemon's) is the one a new key fixes, so it is not here.
_REFUSAL_REASONS = {
    "companion_disabled": "daemon recording is turned off for this team",
}


#: The model route's code for a prompt over its token ceiling
#: (`app/companion/router.py` `PROMPT_TOO_LARGE`): start the conversation fresh.
PROMPT_TOO_LARGE = "prompt_too_large"


def _refusal_code(exc: BaseException) -> str | None:
    """The server's `code` on a model-route refusal. The OpenAI client hands over
    the envelope's inner `error` object as the body; a raw envelope is read too."""
    body = getattr(exc, "body", None)
    if not isinstance(body, dict):
        return None
    inner = body.get("error") if isinstance(body.get("error"), dict) else body
    code = inner.get("code")
    return str(code) if code else None


def _history_rejected(exc: BaseException) -> bool:
    """A failure a saved history can cause: the model's gateway answered a 4xx
    that is not about the key (401, 403), the budget (402), a timeout (408) or
    the rate (429) -- it refused what was sent --, or the history could not be
    validated or serialized on the way out."""
    from pydantic import ValidationError
    from pydantic_ai.exceptions import ModelHTTPError, UserError
    from pydantic_core import PydanticSerializationError

    if isinstance(exc, ModelHTTPError):
        return 400 <= int(exc.status_code) < 500 and int(exc.status_code) not in (401, 402, 403, 408, 429)
    return isinstance(exc, (UserError, ValidationError, PydanticSerializationError))


def _gateway_failure(exc: BaseException) -> bool:
    """The model's gateway failed rather than answered: no HTTP answer at all (a
    refused or dropped connection, the client's own timeout) or a 5xx."""
    from pydantic_ai.exceptions import ModelAPIError, ModelHTTPError

    if isinstance(exc, ModelHTTPError):
        return int(exc.status_code) >= 500
    if isinstance(exc, ModelAPIError):
        return True  # the OpenAI client's connection / timeout errors, as Pydantic AI maps them
    try:
        import httpx
    except ImportError:  # pragma: no cover
        return isinstance(exc, ConnectionError)
    return isinstance(exc, (ConnectionError, httpx.TransportError))
from probe.daemon.worker.bite.run import FAILURES_BEFORE_BACK_OF_QUEUE, UNAUTHORIZED_RETRY_S  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.worker.env import _tokens, probe_env  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.worker.error_log import _device_error  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.worker.install import install_replaced  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.worker.loop.reading import log  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.worker.loop.run_end import BACKOFF_CAP_S, CutShort  # noqa: E402 -- pieces need each other; the front door loads this one first
