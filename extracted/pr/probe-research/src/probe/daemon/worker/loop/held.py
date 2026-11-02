"""answers to held questions: run what the researcher said yes to, void or refuse the rest."""

from __future__ import annotations
from pathlib import Path
from probe.daemon.worker.bite import bite as bite_mod
from probe.daemon.host import lease
from probe.daemon.agent import tools
from probe.shared.mailbox import approvals as appr
from probe.daemon.session import scope
from probe.shared.harness.events import (
    Event,
    Kind)
from probe.daemon.store.store import Store
#: Acting on an answered question failed (Probe unreachable...): again after this, doubling.
SETTLE_RETRY_S = 30.0
#: A held action the researcher said yes to, marked BEFORE it runs: whatever
#: happens after (an error, a crash, a cancel), it is never run a second time.
HELD_RUNNING = "yes: running"
#: What a yes still marked HELD_RUNNING when a worker starts came to: the worker
#: that marked it stopped before it could say (a crash, a kill). Never run again.
HELD_INTERRUPTED = "yes: interrupted (the daemon stopped mid-way; it may not have run)"


class HeldAnswersMixin:
    """Part of Worker: its methods run with `self` the Worker; compose() folds them into Worker."""

    # -- answers to held questions ---------------------------------------------
    def _interrupted_yeses(self) -> None:
        """At start: a yes of this session still marked HELD_RUNNING was being run
        by a worker that stopped before it could say how it went (one worker per
        session: that one is gone). It may or may not have run: reported, never
        run again."""
        for request in self.board.all(session_id=self.session.session_id, state=appr.APPROVED):
            if request.outcome != HELD_RUNNING:
                continue
            self.board.resolve(request, state=appr.APPROVED, outcome=HELD_INTERRUPTED)
            self._notice(f"the researcher said yes to question {request.id}, but the daemon stopped while running it - "
                         "it may not have run, or run in part. The daemon won't run it again by itself.")

    async def settle_answers(self) -> None:
        for request in self.board.all(session_id=self.session.session_id, state=appr.WAITING):
            if request.policy == appr.FEEDBACK:
                continue  # no held action: `probe feedback flush` sends a yes (`probe.shared.feedback.feedback`)
            retry = self.settle_retry.get(request.id)
            if retry is not None and self.clock() < retry[1]:
                continue
            try:
                await self._settle(request)
            except Exception as exc:  # noqa: BLE001 -- e.g. Probe unreachable: the answer waits for a later pass
                # Only failures BEFORE the held action started reach here: from the moment
                # it is marked HELD_RUNNING, `_settle` reports its own outcome.
                n = (retry[0] if retry else 0) + 1
                self.settle_retry[request.id] = (n, self.clock() + min(BACKOFF_CAP_S, SETTLE_RETRY_S * 2 ** (n - 1)))
                log.warning("question %s: acting on it failed (%s in a row): %s: %s", request.id, n,
                            type(exc).__name__, exc)
                if n == 1:
                    self._notice(f"question {request.id}: acting on it failed ({type(exc).__name__}) - it stays open "
                                 "and the daemon tries again. Nothing ran.")
            else:
                self.settle_retry.pop(request.id, None)

    async def _settle(self, req: appr.Request) -> None:
        if req.expires_at and self.clock() > req.expires_at:
            self.board.resolve(req, state=appr.EXPIRED, outcome="expired: nobody answered")
            self._notice(f"question {req.id} expired unanswered - nothing was done")
            return
        if self.replay is None and lease.may_write(self.session.session_id) is not None:
            return  # an answer waits on disk until this process may act for the session again
        answer = self.board.take_answer(req.id)
        if answer is None:
            return
        if answer.get("answer") != appr.YES:
            self.board.resolve(req, state=appr.DENIED, outcome=f"no ({answer.get('choice')!r})",
                               channel=answer.get("channel"))
            self._notice(f"the researcher said no to question {req.id}")
            return
        # A yes: the held action must still be the one they were asked about (C1),
        # then re-read the facts; the same fingerprint runs the held action exactly as held.
        if not appr.verify_held(req):
            self.board.resolve(req, state=appr.VOID, outcome="void: the held action changed on disk",
                               channel=answer.get("channel"))
            self._notice(f"question {req.id} was answered yes, but its held action no longer matches what the "
                         "researcher was asked - nothing was done")
            return
        if req.policy == "delete.others_data" and req.held.get("kind") == "probe":
            from probe.shared.command_rules import command_rules as precheck

            deps = self.deps(None)
            fresh = await tools.deletion_facts(deps, precheck.parse(req.held["argv"]))
            if fresh is not None and appr.POLICIES[req.policy].fingerprint(fresh) != req.fingerprint:
                self.board.resolve(req, state=appr.VOID, outcome="void: what it would delete changed",
                                   channel=answer.get("channel"))
                self._notice(f"question {req.id} was answered yes, but what it would delete changed since - "
                             "nothing was done.")
                return
        deps = self.deps(None)
        # A fresh lease for the run: one about to lapse would stop it seconds in.
        self._renew()
        refusal = tools.held_refusal(deps, req)
        if refusal is not None:  # lost the lease between the check above and now (G7)
            self.board.resolve(req, state=appr.VOID, outcome=f"void: {refusal}", channel=answer.get("channel"))
            # Only why it did not run: a lost lease's own text is a tool reply, not a notice.
            reason = deps.stopped or refusal.removeprefix("not run: ")
            self._notice(f"question {req.id} was answered yes but not run: {reason}")
            return
        # Marked BEFORE it runs: it leaves the waiting list, so an error, a crash or a
        # cancel from here on never runs it a second time.
        self.board.resolve(req, state=appr.APPROVED, outcome=HELD_RUNNING, channel=answer.get("channel"))
        try:
            output, stopped = await self._run_held(req, deps)
        except Exception as exc:  # noqa: BLE001 -- it may have run in part: reported, never retried
            log.warning("question %s: running the held action failed: %s: %s", req.id, type(exc).__name__, exc)
            self._held_outcome(req, f"yes: failed while running ({type(exc).__name__}); not run again",
                               f"the researcher said yes to question {req.id}, but running it failed "
                               f"({type(exc).__name__}: {str(exc)[:300]}). It may have run in part. The daemon won't "
                               "run it again by itself.")
            return
        if _key_refused(deps):
            self._held_outcome(req, "yes: Probe refused the daemon's key",
                               f"the researcher said yes to question {req.id}, but Probe refused the daemon's key, "
                               f"so it didn't run:\n{output[:3000]}", refused=True)
            return
        if stopped is not None:
            self._held_outcome(req, f"yes: stopped ({stopped[:200]})",
                               f"the researcher said yes to question {req.id}, but it was stopped while it ran "
                               f"({stopped[:300]}). It may have run in part. The daemon won't run it again by "
                               f"itself.\n{output[:3000]}")
            return
        self._held_outcome(req, "yes: ran", f"the researcher said yes to question {req.id}; it ran:\n{output[:3000]}")

    def _held_outcome(self, req: appr.Request, outcome: str, notice: str, *, refused: bool = False) -> None:
        """What a yes marked HELD_RUNNING came to, and the model's notice of it. It
        ran (or may have): a failure to report that is logged -- never the "Nothing
        ran" notice `settle_answers` gives a failure BEFORE the run."""
        try:
            if refused:
                self._refused_key("a `probe` command the researcher approved", probe=True)
            self.board.resolve(req, state=appr.APPROVED, outcome=outcome)
            self._notice(notice)
        except Exception as exc:  # noqa: BLE001
            log.warning("question %s: its outcome (%s) could not be recorded: %s: %s", req.id, outcome[:80],
                        type(exc).__name__, exc)

    async def _run_held(self, req: appr.Request, deps: tools.Deps) -> tuple[str, str | None]:
        """Runs a held action: `(what it printed, why it was stopped or None)`.
        Callers check `tools.held_refusal` first."""
        held = req.held
        if held.get("kind") == "shell":
            from probe.daemon import shell as sh

            # Watched like any tool's command (G-8): a switch that moves, or a lease
            # lost, while it runs stops its process group.
            result = await sh.run(held["command"], cwd=Path(held.get("cwd") or self.session.cwd),
                                  watch=tools.lease_watch(deps))
            status = f"stopped: {result.stopped}" if result.stopped else "ran"
            self.store.log_write(bite=None, op_id=held["op_id"], argv=tools.shell_argv(held["command"]), head="shell",
                                 status=status, reason=f"yes to {req.id}", output=result.output,
                                 exit_code=result.exit_code, request=req.id)
            why = result.stopped or ("it did not finish in time" if result.exit_code is None else None)
            return f"{status if result.stopped else f'exit {result.exit_code}'}\n{result.output}", why
        # In the session's folder: a yes to a block from after a `cd` is refused
        # before it is held (`tools.override`).
        code, output, stderr = await tools._run_probe(deps, held["argv"], held["op_id"])
        self.store.log_write(bite=None, op_id=held["op_id"], argv=["probe", *held["argv"]], head="approved",
                             status=tools.write_status(code, stderr), reason=f"yes to {req.id}", output=output,
                             exit_code=code, request=req.id)
        if tools.write_status(code, stderr) == "ran":
            scope.forget_argv(deps, held["argv"])  # a deleted project leaves the status line
        return f"exit {code}\n{output}", (deps.stopped or "it did not finish in time") if code is None else None

    def _notice(self, text: str) -> None:
        with self.store.tx():
            self.store.add([_notice_event(self.store, text)])


def _notice_event(store: Store, text: str) -> Event:
    """A notice for the model's next bite (a META event on the `daemon` stream)."""
    return Event(kind=Kind.META, stream=bite_mod.NOTICE_STREAM, offset=store.next_offset(), text=text)
from probe.daemon.worker.loop.failures import _key_refused  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.worker.loop.reading import log  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.worker.loop.run_end import BACKOFF_CAP_S  # noqa: E402 -- pieces need each other; the front door loads this one first
