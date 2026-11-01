"""RetryLineageMixin, Client's methods: auto-retry lineage: link a relaunch to the run it retries
when it is the same launch (twins: app/runs, app/lineage)."""

from __future__ import annotations
import os
from collections.abc import Mapping
from typing import Any
from ..... import agent_session
from ......foundation.safe_warn import safe_warn as _diagnostics


class RetryLineageMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client."""

    def _maybe_attach_retry_parent(
        self,
        run_kw: dict,
        *,
        experiment_id: str | None = None,
        project_id: str | None = None,
    ) -> None:
        """Attach `retry` parentage when this run is plainly a relaunch.

        WHY THIS EXISTS. The only other automatic producer of lineage is the
        `external_id` collision path, which fires when a caller REUSES an id. That
        is a mistake-shaped trigger, and the two natural ways to launch a retry both
        avoid it: measured fleet-wide, 12 of 34 retry-shaped runs carry no
        `external_id` at all and 16 minted a fresh one per attempt (`…-attempt-1..4`
        -- someone numbering their attempts correctly, and thereby never colliding).
        This path catches those; the two overlap on nothing.

        FIVE CONJUNCTS, each load-bearing (the first four measured):

        * **same agent session** -- scopes the question to runs THIS SDK opened, not
          a colleague's. Session ids are stamped by the server. (They are
          client-SUPPLIED on `X-Probe-Agent-Session`, so this is a scoping device,
          not an authorization one -- see app/runs/agent_session.py.)
        * **immediately preceding** -- the run before this one in the session, not
          "the most recent dead one". Without it a pipeline reads as a retry chain:
          a `dataset-prep` sequence of fail, fail, ok, ok, ok had the last two
          labeled retries of a failure two successes earlier. 4 wrong edges in 9.
        * **config equality, non-empty** -- separates a retry from a SWEEP SIBLING.
          Name matching does not: one failed seed would make every later seed a
          "retry" of it, 48% false positives on the fleet. The seed lives in the
          config, which is why config equality excludes them correctly.
        * **the predecessor has ENDED** -- a concurrent sibling is not a
          predecessor. Parallel subagents of one Claude Code session share ONE
          session id (`agent_session.py`: "no child-session handling"), so under
          fan-out "immediately preceding" is otherwise a race.
        * **the same launch** -- entrypoint, argv (as stored: scrubbed) and cwd
          equal to the predecessor's `metadata.launch.process`, each compared
          only where BOTH sides have it (lineage plan L6). A relaunch runs the
          same command in the same place; config equality alone let a different
          script with the same (or a default) config read as a retry. The new
          run has no launch block yet (the snapshot writes it after the open),
          so its side is computed by the same rules (`launch.process_identity`):
          this process's command, or the one `launch.launching()` names
          (`probe exec`'s child).

        SCOPE is weak since floating runs (daemon v2): every unfiled run has
        scope None, so the scope conjunct no longer separates two lines of work
        opened without a project; config equality and the launch do.

        LIMITS, on the record. Precision was measured retrospectively on SETTLED
        statuses. A predecessor whose process died reads `running` only until
        its death is noticed -- seconds for a sole writer since #2049, the
        reaper's 900s stale window otherwise -- and this fails closed meanwhile.
        A run marked crashed that comes back (its owner's next heartbeat undoes
        the mark) is a new false positive the measurement has to count. Live
        recall and precision are unmeasured. Hence OFF BY DEFAULT.

        FAILS OPEN and is SILENT ON AMBIGUITY: any error opens the run with no
        edge, and lineage is never worth failing a training run over.
        """
        mode = os.environ.get("PROBE_AUTO_RETRY_LINEAGE", "").strip().lower()
        if mode not in ("1", "true", "on", "shadow"):
            return
        if run_kw.get("parent_run_id") is not None:
            return  # the caller declared it; never second-guess a stated claim
        config = run_kw.get("config")
        if not isinstance(config, dict) or not config:
            return  # config equality is the discriminator; without one there is none
        try:
            resolved = agent_session.resolve_agent_session()
            if resolved is None:
                return
            agent, session_id = resolved
            # UNFILTERED, deliberately, and that includes the SCOPE. Any narrowing
            # before `limit=1` answers a different question: `status=failed` gives
            # the most recent DEAD run, and an `experiment_id` filter gives the most
            # recent run IN THIS EXPERIMENT -- neither is "the run immediately before
            # this one". A session that went A(exp1, failed) -> B(exp2, completed) ->
            # C(exp1) would attach C to A under either filter, which is precisely the
            # false positive the immediately-preceding conjunct exists to prevent.
            # So: fetch the session's single most recent run and check scope, status
            # and config locally. `created_at DESC` is the list order, so limit=1 IS
            # the predecessor.
            page = self.list_runs(foreign_key=f"{agent}_session_id:{session_id}", limit=1)
            candidates = page.items or []
            if not candidates:
                return
            previous = candidates[0]
            scope_id = experiment_id if experiment_id is not None else project_id
            scope_key = "experiment_id" if experiment_id is not None else "project_id"
            # A floating run (scope None) matches only a floating predecessor.
            found = previous.get(scope_key)
            if (None if found is None else str(found)) != (None if scope_id is None else str(scope_id)):
                return
            if str(previous.get("status") or "") not in self._RETRY_DEAD_STATUSES:
                return
            if not previous.get("ended_at"):
                return  # still open: a concurrent sibling, not a predecessor
            if previous.get("config") != config:
                return
            if not self._same_launch(previous):
                return
        except Exception:  # noqa: BLE001 -- never fail a run for a lineage guess
            return
        if mode == "shadow":
            # SHADOW MODE. The measured precision is retrospective, so watch what
            # this would have written before letting it write anything.
            _diagnostics.warn(
                f"probe: auto-retry lineage WOULD attach parent_run_id="
                f"{previous.get('id')} (relation=retry) — matched on session + "
                "immediately-preceding + config equality + launch. Set "
                "PROBE_AUTO_RETRY_LINEAGE=1 to write it."
            )
            return
        run_kw["parent_run_id"] = str(previous["id"])
        run_kw["parent_relation"] = "retry"
        run_kw["parent_provenance"] = "observed_call"

    @classmethod
    def _same_launch(cls, previous: Mapping[str, Any]) -> bool:
        """Is the run about to open launched like `previous` was? Each of
        `_RETRY_LAUNCH_KEYS` is compared only where both sides have it: a
        predecessor with no launch block (snapshots off, `probe run start`) is
        judged on the other conjuncts alone, as before."""
        from .....run.launch import launch as _launch

        metadata = previous.get("metadata")
        block = metadata.get("launch") if isinstance(metadata, Mapping) else None
        stored = block.get("process") if isinstance(block, Mapping) else None
        if not isinstance(stored, Mapping):
            return True
        mine, _ = _launch.process_identity()
        for key in cls._RETRY_LAUNCH_KEYS:
            theirs = stored.get(key)
            if theirs is None or mine.get(key) is None:
                continue
            if theirs != mine[key]:
                return False
        return True
