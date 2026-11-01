"""RunCreateMixin, Client's methods: create a run: its body, idempotent create, floating and
project-direct runs (twin: app/runs)."""

from __future__ import annotations
import uuid
from collections.abc import Callable
from typing import Any
from ....values import values as _coerce

from .... import errors
from ....errors import CapabilityUnavailable
from ....delivery.transport.failures import outcome_unknown
from ....delivery.transport.deadlines import wait_out_retry_after


# Late import to avoid a cycle at module load (Run needs Client, Client returns Run).
from ....run.run import Run  # noqa: E402


class RunCreateMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client."""

    # -- runs (create) ------------------------------------------------------
    @staticmethod
    def _run_create_body(
        name: str | None,
        *,
        description: str | None,
        notes: str | None,
        source: str,
        external_id: str | None,
        parent_run_id: str | None,
        parent_relation: str | None,
        group_id: str | None,
        config: dict | None,
        tags: list[str] | None,
        metadata: dict | None,
        labeled_point_budget: int | None,
        slug: str | None = None,
        heartbeat: bool = True,
        awaiting_attach: bool = False,
        launcher: bool = False,
        authored_by: str | None = None,
        parent_provenance: str | None = None,
    ) -> dict[str, Any]:
        # 0268 (plan 2.5): a fresh key per create, so the SAME body can be sent
        # again when its response is lost and the server hands back the run it
        # already made instead of a second one. Sent always: a server that
        # predates the field ignores it, and the re-send is gated on the
        # feature (`_create_idempotently`), never on the key being present.
        body: dict[str, Any] = {"source": source, "creation_key": uuid.uuid4().hex}
        # Stamped even when `name` is omitted: `authored_by` also governs
        # `description_customized`, and a run created with a description and no
        # name still has an authored field on it.
        _put_authorship(body, authored_by)
        # OMITTED, not null: `name` is optional server-side since 0080, and leaving
        # it out is the only way to say "the server picks it". Sending it -- with
        # any value -- stamps `name_customized` and takes the run out of generated
        # titles permanently. `min_length=1` on the server field also means an
        # explicit null and an empty string are not interchangeable here.
        if name is not None:
            body["name"] = name
        # The run's own slug (server 0.110.0.0), stored in the `slug` column.
        # Omitted = the server mints a petname, which stays the normal case. A
        # TAKEN one is a 409, never a silent substitution.
        if slug is not None:
            body["slug"] = slug
        if description is not None:
            body["description"] = description
        # Separate from `description` on purpose (server 0096): a description says
        # what the run IS, notes is the caveat a later reader needs ("suspect, the
        # dataloader was stale"). With one field the two compete.
        if notes is not None:
            body["notes"] = notes
        if external_id is not None:
            body["external_id"] = external_id
        if parent_run_id is not None:
            # NO DEFAULT. This read `parent_relation or "fork"` and quietly stamped
            # `fork` on every parent whose relation the caller left unset -- turning
            # the server's 422 (`RunCreate._parent_pair`, mirrored by
            # `runs_parent_pair_chk`) into a silent success carrying a word nobody
            # chose. The miles integration hit it exactly: its own comment says none
            # of the four honestly describes "evaluated this run's checkpoint", so it
            # deliberately omitted the relation, and this line supplied `fork` anyway.
            if not parent_relation:
                raise errors.ValidationError(
                    "parent_run_id needs parent_relation — fork, resume, retry or "
                    "branch. They mean different things and a guess is stored as a "
                    "claim. If this run CONSUMED the parent's output rather than "
                    "re-attempting it (an eval of its checkpoint, training on its "
                    "rollouts), that is a lineage edge, not parentage: use "
                    "`probe edge add --relation consumes`."
                )
            body["parent_run_id"] = parent_run_id
            body["parent_relation"] = parent_relation
            if parent_provenance is not None:
                # How the parent is known (server 0255): `observed_call` when
                # the SDK derived it itself; omitted means the caller declared it.
                body["parent_provenance"] = parent_provenance
        if group_id is not None:
            body["group_id"] = group_id
        if config is not None:
            # Plan (c): a Namespace, dataclass, DictConfig or numpy leaf used to
            # reach the server as one repr() string (or a 422). Every create
            # path funnels through here; a dict that is already plain comes
            # back equal.
            body["config"] = _coerce.to_config(config)
        if tags is not None:
            body["tags"] = tags
        if metadata is not None:
            body["metadata"] = metadata
        # Per-run labeled-point budget (server 0061): a run that will log more
        # per-sample points than the server default declares its plan up front.
        if labeled_point_budget is not None:
            body["labeled_point_budget"] = labeled_point_budget
        # 0205. The server DERIVES liveness_mode from signals rather than taking
        # a label, and this is the signal: "this process will beat for the run"
        # gets last_heartbeat_at stamped at insert, so an owned run is never
        # momentarily indistinguishable from an unowned one. Sent only when
        # true, so a pre-0205 server sees the request it always saw.
        if heartbeat:
            body["heartbeat"] = True
        if launcher:
            # A fact about the CALLER, not a mode: "I am wrapping a child".
            body["launcher"] = True
        if awaiting_attach:
            # A hand-off: the row is for a job that has not started. Nothing owns
            # it yet, so it lands 'created' and the sweep is the backstop.
            body["awaiting_attach"] = True
        return body

    def create_run(
        self,
        experiment_id: str,
        name: str | None,
        *,
        description: str | None = None,
        notes: str | None = None,
        source: str = "api",
        external_id: str | None = None,
        parent_run_id: str | None = None,
        parent_relation: str | None = None,
        parent_provenance: str | None = None,
        group_id: str | None = None,
        config: dict | None = None,
        tags: list[str] | None = None,
        metadata: dict | None = None,
        heartbeat: bool = True,
        awaiting_attach: bool = False,
        launcher: bool = False,
        labeled_point_budget: int | None = None,
        slug: str | None = None,
        authored_by: str | None = None,
        project_id: str | None = None,
    ) -> Run:
        """Create an experiment-attached run
        (``POST /v1/projects/{P}/experiments/{E}/runs``; ``project_id`` saves the
        lookup of where the experiment is filed).

        0220: a run carries no authored document. Projects and experiments
        keep theirs as ``document``, which is the Overview page's marked block.
        """
        body = self._run_create_body(
            name,
            slug=slug,
            description=description,
            notes=notes,
            source=source,
            external_id=external_id,
            parent_run_id=parent_run_id,
            parent_relation=parent_relation,
            parent_provenance=parent_provenance,
            group_id=group_id,
            config=config,
            tags=tags,
            metadata=metadata,
            labeled_point_budget=labeled_point_budget,
            heartbeat=heartbeat,
            awaiting_attach=awaiting_attach,
            launcher=launcher,
            authored_by=authored_by,
        )
        session_id, lease = self._lease_for_create(
            body, heartbeat=heartbeat, awaiting_attach=awaiting_attach, launcher=launcher
        )
        def create_in(project: str, experiment: str) -> Any:
            return self._create_idempotently(
                # Literal call site: the tests/test_parity.py AST scan must see the route.
                lambda replay: self.transport.post(
                    f"/v1/projects/{project}/experiments/{experiment}/runs",
                    body,
                    idempotent=replay,
                ),
                path=f"/v1/projects/{project}/experiments/{experiment}/runs",
                body=body,
            )

        # A 404 creates nothing, so a remembered home gone stale is re-asked
        # and the create sent once more (`_on_experiment`).
        data = self._on_experiment(create_in, experiment_id, project_id)
        self._verify_slug_written(slug, data)
        self._warn_if_notes_dropped(notes, data, "runs")
        return self._opened(
            self._wrap_run(
                data,
                heartbeat=heartbeat,
                session_id=session_id,
                lease=lease,
                # The create's own transaction wrote it.
                lease_registered=lease is not None,
                # The create carried the lease: the run is on leases.
                lease_protocol="leases" if lease is not None else None,
            )
        )

    def _create_idempotently(
        self, send: Callable[[bool], Any], *, path: str | None = None, body: dict | None = None
    ) -> Any:
        """Send a run create once, and AGAIN only when that is provably safe.

        ``send(replay)`` posts the create body, which carries its own
        ``creation_key``; ``replay=True`` lets the transport retry it like a
        read. A create whose outcome is unknown (read timeout, dropped
        connection, 502/503/504 -- ``outcome_unknown``) may have committed, so
        re-sending it is safe only on a server that replays a key it has seen
        (``run_creation_key``). There it comes back with the run it already
        made; anywhere else the failure stands, because a second POST would be
        a second run (or, with an ``external_id``, a 409 against itself).

        The feature is read only on that failure, so a healthy create costs no
        extra request; once the answer is cached, the first send already
        retries.

        A 429 on the first send is re-sent on ANY server: rate limiting refuses
        a request before processing it, so nothing can have landed. Every
        re-send first waits the failure's ``Retry-After`` by the transport's
        own rule for that header: inside init's budget, whenever the budget
        still holds it; outside one, up to the inline cap. When it does not
        fit, the failure is raised at once instead (`wait_out_retry_after`).

        Every create leaves ``_last_run_create`` behind for
        ``PROBE_INIT_FALLBACK=offline`` (plan 2.12): the request as sent, and
        whether it LANDED (``landed``: this client got the run back). One that
        did not land is what the fallback records -- the offline queue keeps it
        and replays it verbatim at sync ONLY if the server says its key already
        made a run (`offline.deliver_create`), so whether a lost answer "may have
        landed" is decided by the server, never guessed here. One that landed
        stops the fallback: recording offline would make a second run."""
        record = {"path": path, "body": body, "landed": False} if path and body else None
        self._last_run_create = record

        def attempt(replay: bool) -> Any:
            created = send(replay)
            if record is not None:
                record["landed"] = True
            return created

        known = getattr(self, "_server_features_cache", None)
        replay_known = known is not None and self._CREATION_REPLAY_FEATURE in known
        try:
            return attempt(replay_known)
        except errors.RosError as exc:
            if replay_known:
                raise  # the transport already retried it within its own policy
            rate_limited = exc.status == 429
            if not rate_limited and not outcome_unknown(exc):
                raise
            try:
                supported = self.supports_feature(self._CREATION_REPLAY_FEATURE)
            except errors.RosError:
                supported = False  # cannot tell: only a 429 is still safe to re-send
            if not (supported or rate_limited):
                raise
            if not wait_out_retry_after(exc, minimum=0.5 if rate_limited else 0.0):
                raise
            replay = supported
        return attempt(replay)

    def create_floating_run(
        self,
        name: str | None,
        *,
        description: str | None = None,
        notes: str | None = None,
        source: str = "api",
        external_id: str | None = None,
        parent_run_id: str | None = None,
        parent_relation: str | None = None,
        config: dict | None = None,
        tags: list[str] | None = None,
        metadata: dict | None = None,
        heartbeat: bool = True,
        awaiting_attach: bool = False,
        launcher: bool = False,
        labeled_point_budget: int | None = None,
        slug: str | None = None,
        authored_by: str | None = None,
    ) -> Run:
        """POST /v1/runs — open a FLOATING run: no project, no experiment (daemon v2, D1).

        The run is its own record from its first second (metrics, spans, files,
        parentage), and is filed afterwards -- by the Probe daemon, or a person
        with `probe run move` -- which moves everything it holds with it. Same
        body as a project-direct run, and like one it cannot join a group.
        """
        body = self._run_create_body(
            name,
            slug=slug,
            description=description,
            notes=notes,
            source=source,
            external_id=external_id,
            parent_run_id=parent_run_id,
            parent_relation=parent_relation,
            group_id=None,
            config=config,
            tags=tags,
            metadata=metadata,
            labeled_point_budget=labeled_point_budget,
            heartbeat=heartbeat,
            awaiting_attach=awaiting_attach,
            launcher=launcher,
            authored_by=authored_by,
        )
        session_id, lease = self._lease_for_create(
            body, heartbeat=heartbeat, awaiting_attach=awaiting_attach, launcher=launcher
        )
        try:
            data = self._create_idempotently(
                # Literal call site: the tests/test_parity.py AST scan must see the route.
                lambda replay: self.transport.post("/v1/runs", body, idempotent=replay),
                path="/v1/runs",
                body=body,
            )
        except errors.RosError as exc:
            # A backend that predates floating runs has GET /v1/runs only, so a
            # POST there is FastAPI's 405 (or a route-level "Not Found" behind a
            # proxy; a handler's own 404, like a missing parent run, says more
            # and passes through). Name the way out instead of "Method Not Allowed".
            if exc.status == 405 or (exc.status == 404 and str(exc).strip().lower() == "not found"):
                raise errors.CapabilityUnavailable(
                    "floating_runs",
                    "this research-os backend predates floating runs (POST /v1/runs). "
                    "Upgrade the backend, or open the run in a project: pass "
                    "project= / experiment= (CLI: --project / --experiment, or "
                    "`probe project use`).",
                ) from exc
            raise
        self._verify_slug_written(slug, data)
        self._warn_if_notes_dropped(notes, data, "runs")
        return self._opened(
            self._wrap_run(
                data,
                heartbeat=heartbeat,
                session_id=session_id,
                lease=lease,
                # The create's own transaction wrote it.
                lease_registered=lease is not None,
                # The create carried the lease: the run is on leases.
                lease_protocol="leases" if lease is not None else None,
            )
        )

    @staticmethod
    def _verify_slug_written(slug: str | None, row: dict) -> None:
        """A backend predating run slugs DROPS the field and names the run itself.

        Pydantic ignores an undeclared body field by default, so the create
        succeeds, returns 201, and hands back a random petname -- and the caller
        exits 0 believing it owns a handle it does not. Reading the stored value
        back is the only thing that tells the two apart.
        """
        if slug is None:
            return
        # scanning disabled: from .redaction import default_scrub

        # scanning disabled: expected = default_scrub(slug)
        expected = slug
        written = row.get("slug")
        if written != expected:
            raise CapabilityUnavailable(
                f"this backend ignored the run slug {expected!r} (it stored "
                # scanning disabled: f"{default_scrub(written)!r}); run slugs need research-os >= 0.110.0.0"
                f"{written!r}); run slugs need research-os >= 0.110.0.0"
            )

    def create_project_run(
        self,
        project_id: str,
        name: str | None,
        *,
        description: str | None = None,
        notes: str | None = None,
        source: str = "api",
        external_id: str | None = None,
        parent_run_id: str | None = None,
        parent_relation: str | None = None,
        parent_provenance: str | None = None,
        config: dict | None = None,
        tags: list[str] | None = None,
        metadata: dict | None = None,
        heartbeat: bool = True,
        awaiting_attach: bool = False,
        launcher: bool = False,
        labeled_point_budget: int | None = None,
        slug: str | None = None,
        authored_by: str | None = None,
    ) -> Run:
        """POST /v1/projects/{id}/runs — open a PROJECT-DIRECT run (W&B shape).

        The experiment level is optional grouping; a run opened here attaches
        straight to the project. No ``group_id``: run groups are
        experiment-anchored, so the backend rejects one on a direct run (422).

        0220: a run carries no authored document. Projects and experiments
        keep theirs as ``document``, which is the Overview page's marked block.
        """
        body = self._run_create_body(
            name,
            slug=slug,
            description=description,
            notes=notes,
            source=source,
            external_id=external_id,
            parent_run_id=parent_run_id,
            parent_relation=parent_relation,
            parent_provenance=parent_provenance,
            group_id=None,
            config=config,
            tags=tags,
            metadata=metadata,
            labeled_point_budget=labeled_point_budget,
            heartbeat=heartbeat,
            awaiting_attach=awaiting_attach,
            launcher=launcher,
            authored_by=authored_by,
        )
        session_id, lease = self._lease_for_create(
            body, heartbeat=heartbeat, awaiting_attach=awaiting_attach, launcher=launcher
        )
        try:
            data = self._create_idempotently(
                # Literal call site: the tests/test_parity.py AST scan must see the route.
                lambda replay: self.transport.post(
                    f"/v1/projects/{project_id}/runs", body, idempotent=replay
                ),
                path=f"/v1/projects/{project_id}/runs",
                body=body,
            )
        except errors.NotFoundError as exc:
            # A pre-0054 backend has no such route, and its route-level 404
            # ("Not Found") is indistinguishable from a missing project. The
            # handler's own 404 says "project not found"; anything else means
            # the backend predates the route — say so, and say what to do
            # (the browse/search degraded-backend standard).
            if "project" not in str(exc).lower():
                raise errors.NotFoundError(
                    "this research-os backend predates POST /v1/projects/{id}/runs "
                    "(project-direct runs, 0054). Upgrade the backend, or open "
                    "the run inside an experiment (--experiment / run(experiment=...)).",
                    status=exc.status,
                    detail=exc.detail,
                ) from exc
            raise
        self._verify_slug_written(slug, data)
        self._warn_if_notes_dropped(notes, data, "runs")
        return self._opened(
            self._wrap_run(
                data,
                heartbeat=heartbeat,
                session_id=session_id,
                lease=lease,
                # The create's own transaction wrote it.
                lease_registered=lease is not None,
                # The create carried the lease: the run is on leases.
                lease_protocol="leases" if lease is not None else None,
            )
        )
from probe.sdk.client.authorship import _put_authorship  # noqa: E402 -- pieces need each other; the front door loads this one first
