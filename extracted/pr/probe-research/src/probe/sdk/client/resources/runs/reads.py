"""RunReadsMixin, Client's methods: read, update, fork and delete one run: trials, sandbox base
state, bundle and reproduce (twins: app/runs, app/runs/trials)."""

from __future__ import annotations
from .....models import TrialPatch
from .... import agent_session

from .... import errors
from ....delivery.transport.transport import Page


# Late import to avoid a cycle at module load (Run needs Client, Client returns Run).
from ....run.run import Run  # noqa: E402
from probe.sdk.routes import WriteOp, path_for

#: Runs one `get_run_failures` call may name (the server's cap).
MAX_FAILURE_IDS = 20


class RunReadsMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client."""

    # -- fork (0185) ---------------------------------------------------------
    def fork_run(
        self,
        source: str,
        *,
        step: int | None = None,
        name: str | None = None,
        **run_kw,
    ) -> Run:
        """Open a NEW run that continues ``source`` from ``step``, leaving the
        source untouched and unmarked — the keep-both alternative to
        ``Rewind``.

        W&B's fork shape: the new run carries ``parent_relation="fork"`` plus
        ``fork_of``/``fork_step`` foreign keys and logs from the checkpoint
        step onward under its own identity, so both curves survive. Works from
        any source status — a fork reads the source's row and writes nothing
        to it (unlike ``supersede``, which is a from-scratch RETRY and tags a
        dead incumbent ``superseded``).
        """
        src = self.get_run(source)
        fork_name = name or f"{src.get('name') or str(src['id'])[:8]}-fork"
        if not name and run_kw.get("authored_by") is None and not run_kw.get("description"):
            # THE SDK composed this NAME, so say so -- but only when the caller
            # has not declared anything. `--authored-by human` on a fork with no
            # `--name` is the normal shape of "the researcher dictated the
            # description", and overwriting it here made the flag silently
            # inert on the exact path it is most used on. A description riding
            # along is someone's words: `composed` would hand it to generation.
            run_kw["authored_by"] = agent_session.AUTHORSHIP_COMPOSED
        kw = dict(run_kw, parent_run_id=src["id"], parent_relation="fork")
        experiment_id = src.get("experiment_id")
        if experiment_id:
            run = self.create_run(
                experiment_id, fork_name, project_id=src.get("project_id"), **kw
            )
        elif src.get("project_id"):
            run = self.create_project_run(src["project_id"], fork_name, **kw)
        elif "project_id" in src:
            # Unfiled (an older CLI made it): no home to inherit.
            raise errors.build_unfiled_parent_error(source)
        else:
            raise errors.ValidationError(
                f"run {source} reports neither an experiment nor a project — this "
                "research-os backend predates project-direct runs (0054)."
            )
        links: dict = {"fork_of": src["id"]}
        if step is not None:
            links["fork_step"] = step
        # link() is the sanctioned foreign-keys surface; per-key new-wins.
        run.link(**links)
        return run

    # -- runs (read) --------------------------------------------------------
    def get_run(self, run_id: str) -> dict:
        return self.transport.get(f"/v1/runs/{run_id}")

    def get_run_failures(self, run_ids: list[str]) -> list[dict]:
        """Why each failed or crashed run failed (`GET /v1/runs/failures`, at most
        `MAX_FAILURE_IDS`): its cause, exception, exit code and last log lines. A run that did not
        fail is left out. A server from before the route raises `NotFoundError`."""
        if len(run_ids) > MAX_FAILURE_IDS:
            raise ValueError(f"at most {MAX_FAILURE_IDS} runs per call, got {len(run_ids)}")
        data = self.transport.get("/v1/runs/failures", params={"ids": ",".join(run_ids)})
        return list((data or {}).get("failures") or [])

    # -- trials (read) ------------------------------------------------------
    def list_run_trials(
        self,
        run_ref: str,
        *,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> Page:
        """One cursor-aware page of authored Trials belonging to a Run."""
        params = {
            key: value
            for key, value in {"cursor": cursor, "limit": limit}.items()
            if value is not None
        }
        return self.transport.get_page(f"/v1/runs/{run_ref}/trials", params=params or None)

    def get_trial(self, trial_id: str) -> dict:
        """Read one rollout-backed Trial by its rollout span id."""
        return self.transport.get(f"/v1/trials/{trial_id}")

    # -- trials (write) -----------------------------------------------------
    def update_trial(
        self,
        trial_id: str,
        *,
        name: str | None = None,
        description: str | None = None,
    ) -> dict:
        """Field-replace PATCH on the AUTHORED half of a Trial.

        Only what a person writes: title and description. Lifecycle, result and
        timing stay the producer's, and a span retry keeps rewriting them --
        which is exactly why the two halves are separate rows and why this cannot
        reach the other one.

        Notes are NOT here because a Trial HAS none -- the one research entity
        without a notes document. A rollout ran once and is immutable, so
        `description` is the whole of its prose; there is no `--trial` flag on
        `probe notes push` either.
        """
        model = TrialPatch(name=name, description=description)
        body = model.model_dump(mode="json", exclude_none=True)
        if not body:
            raise ValueError("update_trial needs at least one of name/description")
        return self.transport.patch(f"/v1/trials/{trial_id}", body)

    def claim_sandbox_base_state(self, run_id: str, ref: str, owner_key: str) -> dict:
        """Atomically elect one begin-state capturer for a run-local ref.

        This is intentionally synchronous: a queued claim cannot tell the
        caller whether to archive the environment it is about to execute.
        """
        return self.transport.post(
            f"/v1/runs/{run_id}/sandbox-state/base-state/claim",
            {"ref": ref, "owner_key": owner_key},
        )

    def update_run(
        self,
        run_id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        notes: str | None = None,
        status: str | None = None,
        authored_by: str | None = None,
        expected_name: str | None = None,
    ) -> dict:
        """PATCH /v1/runs/{id} — amend a run's authored fields.

        ``expected_name`` makes a ``name`` write a compare-and-set: the name read before it, so a rename
        meanwhile refuses the write (409) instead of being overwritten. It marks the script's own name
        being applied to the run its launcher opened (a ``probe exec`` join), so the name goes out like a
        create-time one: undeclared and kept, unless Probe composed it (``agent_session.ComposedName``).

        ``status`` CORRECTS the run's recorded status and sends nothing else: no
        ``ended_at``, no ``started_at``, no ``write_epoch``, so the run's start,
        end and duration stay exactly as recorded. Closing a run you are running
        is ``Run.finish`` (``probe run end``), which stamps the end time.

        0220: a run carries no authored document -- see ``update_project`` and
        ``update_experiment``, whose ``document`` is the Overview page's marked
        block. Read immediately before editing and preserve useful
        sections; ``""`` clears it. A line containing only
        ``[README](https://github.com/owner/repo)`` embeds that README and derives
        the run's read-only ``repo`` field.

        ``notes`` (server 0096) is the door that matters most for that field: a
        run's caveat is nearly always learned after the run finished. It is NOT a
        second description — a description says what the run is, notes says what a
        later reader should distrust about it, and writing the caveat into
        ``description`` means destroying the description to keep it.

        Omitting a field leaves it alone; passing ``""`` for ``notes`` clears it."""
        body = {
            key: value
            for key, value in {
                "name": name,
                "description": description,
                "notes": notes,
                "status": status,
            }.items()
            if value is not None
        }
        if not body:
            raise ValueError("update_run needs at least one of name/description/notes/status")
        # AFTER the emptiness check, deliberately. `authored_by` declares who
        # wrote the OTHER fields; on its own it declares authorship of nothing,
        # and letting it satisfy "at least one field to set" would turn a
        # no-op call into a PATCH.
        if expected_name is not None and name is not None:
            body["expected_name"] = expected_name
        if expected_name is not None and set(body) == {"name", "expected_name"}:
            # The script's own name alone, like a create-time name; a description or note beside it is not.
            # `composed`: a placeholder lands only on a placeholder; a name an agent or person chose is kept (409).
            if authored_by is None and isinstance(name, agent_session.ComposedName):
                authored_by = agent_session.AUTHORSHIP_COMPOSED
            _put_authorship(body, authored_by, is_new_run_name=True)
        else:
            _put_authorship(body, authored_by)
        row = self.transport.patch(path_for(WriteOp.RUN_PATCH, run_id), body)
        self._warn_if_notes_dropped(notes, row, "runs")
        return row

    def run_bundle(self, run_id: str, *, source_read_contract: str | None = None) -> dict:
        """GET /v1/runs/{id}/bundle. A SOURCE-BACKED run (a W&B mirror, say)
        answers 422 `unsupported_source_query` unless the caller names the
        coverage read contract: its metric catalog carries the provider's
        coverage receipts, which an older client would render as exact. Pass
        ``source_read_contract=SOURCE_READ_CONTRACT`` where the caller reads
        those receipts (or ignores the catalog); the default sends nothing."""
        params = (
            {"source_read_contract": source_read_contract} if source_read_contract else None
        )
        return self.transport.get(f"/v1/runs/{run_id}/bundle", params=params)

    def run_reproduce(self, run_id: str) -> dict:
        """GET /v1/runs/{id}/reproduce — the server-assembled reproduction record:
        execution record, launch context, restore command, code snapshot,
        inputs-decision (content inlined when small), notes, lockfiles, lineage
        edges, per-span env refs, and a completeness verdict. This is a thin
        passthrough on purpose — the backend is the one place that reads every
        piece together (research-os app/read_models/reproduce.py). A run captured
        before capture-core answers 200 with a degraded body, never a 404."""
        return self.transport.get(f"/v1/runs/{run_id}/reproduce")

    def experiment_reproduce(
        self, experiment_id: str, *, version: int | None = None, project_id: str | None = None
    ) -> dict:
        """GET /v1/projects/{P}/experiments/{E}/reproduce — per-run reproduction summaries (a
        map, not N full assemblies; each summary carries a `reproduce_url` for
        drill-down). `version` pins against a minted experiment_versions manifest;
        omitted reads live rows."""
        params = {"version": version} if version is not None else None
        return self._on_experiment(
            lambda p, e: self.transport.get(
                f"/v1/projects/{p}/experiments/{e}/reproduce", params=params
            ),
            experiment_id,
            project_id,
        )

    def run_lineage(self, run_id: str) -> dict:
        return self.transport.get(f"/v1/runs/{run_id}/lineage")

    # -- lifecycle (delete = move to the trash) -----------------------------
    def delete_run(self, run_id: str, *, dry_run: bool = False) -> dict | None:
        """Move a run, with its telemetry, to the server's TRASH. Frees its
        natural key.

        Spans, metrics, artifacts and lineage go with it. Probe support can
        restore it for 21 days (the returned receipt says until when); after
        that it is deleted for good. A server without the `trash` feature
        deletes PERMANENTLY and returns None. 404 if the run does not exist.
        ``dry_run=True`` changes nothing and answers what would go."""
        if not dry_run:
            return self.transport.delete(f"/v1/runs/{run_id}")
        self._require_dry_run_delete()
        resp = self.transport.request(
            "DELETE", f"/v1/runs/{run_id}", params={"dry_run": "true"}, idempotent=True
        )
        return resp.json() if resp.content else None
from probe.sdk.client.authorship import _put_authorship  # noqa: E402 -- pieces need each other; the front door loads this one first
