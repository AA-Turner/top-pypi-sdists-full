"""IntegrationsResource (client.integrations, typed reads) and IntegrationsMixin, Client's methods:
GitHub sources and commits, W&B, run and experiment code (twin: app/integrations)."""

from __future__ import annotations
from ....generated.models import (
    CodeSourceOut,
    CommitCard,
    CommitsPage,
    ExperimentCodeOut,
    MirrorConnectionOut,
    PullsPage,
    ReleasesPage,
    RunCodeCompareOut,
    RunCodeOut,
    ScopeOptionOut,
)
from ..resource import Resource


class IntegrationsMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client."""

    def list_project_code_sources(self, project_id: str) -> list[dict]:
        """The project's attached repositories (repo/branch/directory rows)."""
        return self.transport.get(f"/v1/projects/{project_id}/code-sources")

    def attach_project_code_source(
        self,
        project_id: str,
        *,
        repo: str,
        ref: str | None = None,
        path_prefix: str = "",
        start_sha: str | None = None,
        start_at: str | None = None,
        add_readme_embed: bool = False,
        via: str = "cli",
        reason: str | None = None,
    ) -> dict:
        """Attach a GitHub repository (and branch) to a project.

        Grants no access an installation (or public visibility) has not already
        granted; the backend resolves the repo through the covering
        installation's token or unauthenticated for public repos. ``via`` is
        attribution ('cli' from scripts, 'agent' from an agent acting alone —
        which then REQUIRES ``reason``, rendered next to the attribution)."""
        body = {
            key: value
            for key, value in {
                "repo": repo,
                "ref": ref,
                "path_prefix": path_prefix,
                "start_sha": start_sha,
                "start_at": start_at,
                "add_readme_embed": add_readme_embed,
                "via": via,
                "reason": reason,
            }.items()
            if value not in (None, "", False)
        }
        body["repo"] = repo
        return self.transport.post(f"/v1/projects/{project_id}/code-sources", body)

    def detach_project_code_source(self, project_id: str, source_id: str) -> None:
        self.transport.delete(f"/v1/projects/{project_id}/code-sources/{source_id}")

    def confirm_project_code_source(self, project_id: str, source_id: str) -> dict:
        """suggested -> active (the one-click yes to a snapshot's suggestion)."""
        return self.transport.post(
            f"/v1/projects/{project_id}/code-sources/{source_id}/confirm", {}
        )

    def patch_project_code_source(
        self,
        project_id: str,
        source_id: str,
        *,
        ref: str | None = None,
        path_prefix: str | None = None,
        start_sha: str | None = None,
        start_at: str | None = None,
    ) -> dict:
        """Edit a source's branch/directory/start bound (the backend re-resolves)."""
        body = {
            key: value
            for key, value in {
                "ref": ref,
                "path_prefix": path_prefix,
                "start_sha": start_sha,
                "start_at": start_at,
            }.items()
            if value is not None
        }
        return self.transport.patch(f"/v1/projects/{project_id}/code-sources/{source_id}", body)

    def sync_project_code_source(self, project_id: str, source_id: str) -> dict:
        """Re-check the branch tip now (heals a `missing` source when it is back)."""
        return self.transport.post(f"/v1/projects/{project_id}/code-sources/{source_id}/sync", {})

    def mark_project_commit(
        self, project_id: str, sha: str, *, excluded: bool, source_id: str | None = None
    ) -> None:
        """Exclude a commit from the timeline (or bring it back). A display
        verdict, never history editing — include_excluded still lists it."""
        body: dict[str, object] = {"excluded": excluded}
        if source_id:
            body["source_id"] = source_id
        self.transport.post(f"/v1/projects/{project_id}/commits/{sha}/mark", body)

    # --- W&B account selection and project-owned history --------------------

    def create_wandb_account(self, *, api_key: str) -> dict:
        """Connect W&B credentials without creating a workspace or source binding.

        Uses the W&B-specific account contract; credentials never enter the
        durable write queue, including when the server is unavailable.
        """
        # Account credentials are intentional authentication input, not captured
        # research data: bypass its redactor as well as its fail-open journal.
        return self.transport.post(
            "/v1/integrations/wandb/accounts", {"credentials": {"api_key": api_key}}
        )

    def reconnect_wandb_account(self, connection_id: str, *, api_key: str) -> dict:
        """Replace credentials on the same account, retaining its source identity."""
        return self.transport.post(
            f"/v1/integrations/wandb/accounts/{connection_id}/reconnect",
            {"credentials": {"api_key": api_key}},
        )

    def rename_wandb_account(self, connection_id: str, *, name: str) -> dict:
        """Rename a saved account.

        Allowed on a DISCONNECTED one too -- that is the row whose name is
        doing the most work, its key being gone.
        """
        return self.transport.patch(
            f"/v1/integrations/wandb/accounts/{connection_id}", {"name": name}
        )

    def disconnect_wandb_account(self, connection_id: str) -> None:
        """Disconnect a W&B account: revoke its credential and PERMANENTLY delete
        every run its sources imported, with any work attached to those runs.

        The destination projects and experiments, runs created in Probe, and
        the account row (revoked, reconnectable) stay; W&B itself is untouched.
        To stop importing but keep the runs, pause the sources instead
        (`patch_project_wandb_source(..., sync_enabled=False)`)."""
        self.transport.delete(f"/v1/integrations/wandb/accounts/{connection_id}")

    def list_mirror_connections(self) -> list[dict]:
        """Connected accounts; credentials are managed in Integrations."""
        return self.transport.get("/v1/integrations/mirror/connections")

    def list_mirror_scope_options(self, connection_id: str) -> list[dict]:
        return self.transport.get(
            f"/v1/integrations/mirror/connections/{connection_id}/scope-options"
        )

    def list_project_wandb_sources(self, project_id: str) -> list[dict]:
        return self.transport.get(f"/v1/projects/{project_id}/wandb-sources")

    def attach_project_wandb_source(
        self, project_id: str, *, connection_id: str, external_id: str
    ) -> dict:
        """Reuse the canonical source attachment; new attachments start paused.

        Strict writes never enter the generic outbox. Callers retaining an
        admission intent must receive either the actual receipt or an error.
        """
        return self.send(
            "POST",
            f"/v1/projects/{project_id}/wandb-sources",
            {"connection_id": connection_id, "external_id": external_id},
            strict=True,
        )

    def claim_wandb_run(
        self,
        external_id: str,
        *,
        project_id: str,
        name: str | None = None,
        config: dict | None = None,
        tags: list[str] | None = None,
        metadata: dict | None = None,
        notes: str | None = None,
        started_at: str | None = None,
        experiment_id: str | None = None,
        parent_external_id: str | None = None,
    ) -> dict:
        """The one Probe run a W&B import copies `external_id` (`wandb:entity/project/run_id`) into:
        `{outcome, run, representation, reads_from_wandb}`. Idempotent: the run that id names, an
        earlier CLI import's (adopted), a read-through mirror run (upgraded once a team admin pressed
        Copy into Probe on its attachment, else 409), or a new run in `project_id`. `name`, `config`,
        `tags`, `metadata`, `notes`, `started_at` (W&B's start), `experiment_id` (where it is filed) and
        `parent_external_id` (the W&B run it was forked from) only start a new run."""
        from ... import agent_session

        body: dict = {"external_id": external_id, "project_id": project_id}
        for field, value in (("name", name), ("config", config), ("tags", tags), ("metadata", metadata),
                             ("notes", notes), ("started_at", started_at), ("experiment_id", experiment_id),
                             ("parent_external_id", parent_external_id)):
            if value is not None:
                body[field] = value
        if isinstance(name, agent_session.ComposedName):  # W&B's made-up name: Probe may title the run
            body["authored_by"] = "agent"
        return self.send("POST", "/v1/integrations/wandb/runs/claim", body, strict=True)

    def mark_wandb_copied(self, run_id: str) -> dict:
        """A copy's parity check passed: its reads move from W&B to Probe (`copying` -> `copied`).
        Idempotent; `{representation, reads_from_wandb}`."""
        return self.send("POST", f"/v1/integrations/wandb/runs/{run_id}/copied", {}, strict=True)

    def patch_project_wandb_source(
        self, project_id: str, attachment_id: str, *, sync_enabled: bool, expected_revision: int
    ) -> dict:
        return self.send(
            "PATCH",
            f"/v1/projects/{project_id}/wandb-sources/{attachment_id}",
            {"sync_enabled": sync_enabled, "expected_revision": expected_revision},
            strict=True,
        )

    def detach_project_wandb_source(self, project_id: str, attachment_id: str) -> None:
        """Detach one source: revoke it and PERMANENTLY delete the runs it
        imported, with any work attached to them. Runs created in Probe and
        the destination stay. Pausing (`patch_project_wandb_source(...,
        sync_enabled=False)`) keeps them."""
        self.send(
            "DELETE", f"/v1/projects/{project_id}/wandb-sources/{attachment_id}", strict=True
        )

    # An experiment's W&B sources live on the experiment API (server X21b):
    # `/v1/projects/{P}/experiments/{E}/wandb-sources[...]`, never the leaf
    # door `/v1/projects/{E}/wandb-sources` R6 removes. `project_id` (the
    # project the experiment is filed in) saves the one `GET /v1/scopes/{E}`
    # that places it otherwise. Their history imports are launched and read at
    # the PROJECT's address (`*_project_wandb_backfill` with the project's id):
    # a job's target is the project, so both addresses answer the same job.

    def list_experiment_wandb_sources(
        self, experiment_id: str, *, project_id: str | None = None
    ) -> list[dict]:
        return self._on_experiment(
            lambda p, e: self.transport.get(
                f"/v1/projects/{p}/experiments/{e}/wandb-sources"
            ),
            experiment_id,
            project_id,
        )

    def attach_experiment_wandb_source(
        self,
        experiment_id: str,
        *,
        connection_id: str,
        external_id: str,
        project_id: str | None = None,
    ) -> dict:
        """Reuse the canonical source attachment; new attachments start paused.

        Strict writes never enter the generic outbox. Callers retaining an
        admission intent must receive either the actual receipt or an error.
        """
        return self._on_experiment(
            lambda p, e: self.send(
                "POST",
                f"/v1/projects/{p}/experiments/{e}/wandb-sources",
                {"connection_id": connection_id, "external_id": external_id},
                strict=True,
            ),
            experiment_id,
            project_id,
        )

    def patch_experiment_wandb_source(
        self,
        experiment_id: str,
        attachment_id: str,
        *,
        sync_enabled: bool,
        expected_revision: int,
        project_id: str | None = None,
    ) -> dict:
        return self._on_experiment(
            lambda p, e: self.send(
                "PATCH",
                f"/v1/projects/{p}/experiments/{e}/wandb-sources/{attachment_id}",
                {"sync_enabled": sync_enabled, "expected_revision": expected_revision},
                strict=True,
            ),
            experiment_id,
            project_id,
        )

    def detach_experiment_wandb_source(
        self, experiment_id: str, attachment_id: str, *, project_id: str | None = None
    ) -> None:
        """`detach_project_wandb_source` for an experiment's source: the runs it
        imported are PERMANENTLY deleted; pausing keeps them."""
        self._on_experiment(
            lambda p, e: self.send(
                "DELETE",
                f"/v1/projects/{p}/experiments/{e}/wandb-sources/{attachment_id}",
                strict=True,
            ),
            experiment_id,
            project_id,
        )

    def launch_project_wandb_backfill(
        self, project_id: str, attachment_id: str, *, idempotency_key: str
    ) -> dict:
        return self.send(
            "POST",
            f"/v1/projects/{project_id}/wandb-sources/{attachment_id}/backfills",
            {"idempotency_key": idempotency_key},
            strict=True,
        )

    def list_project_wandb_backfills(
        self, project_id: str, attachment_id: str, *, cursor: str | None = None, limit: int = 25
    ) -> dict:
        return self.transport.get(
            f"/v1/projects/{project_id}/wandb-sources/{attachment_id}/backfills",
            params={"limit": limit, **({"cursor": cursor} if cursor else {})},
        )

    def get_project_wandb_backfill(self, project_id: str, attachment_id: str, job_id: str) -> dict:
        return self.transport.get(
            f"/v1/projects/{project_id}/wandb-sources/{attachment_id}/backfills/{job_id}"
        )

    def cancel_project_wandb_backfill(
        self, project_id: str, attachment_id: str, job_id: str
    ) -> dict:
        return self.send(
            "POST",
            f"/v1/projects/{project_id}/wandb-sources/{attachment_id}/backfills/{job_id}/cancel",
            {},
            strict=True,
        )

    def retry_project_wandb_backfill(
        self, project_id: str, attachment_id: str, job_id: str, *, idempotency_key: str
    ) -> dict:
        return self.send(
            "POST",
            f"/v1/projects/{project_id}/wandb-sources/{attachment_id}/backfills/{job_id}/retry",
            {"idempotency_key": idempotency_key},
            strict=True,
        )

    def list_project_pulls(self, project_id: str, **filters: object) -> dict:
        """One page of pull requests targeting the attached branch (proxied)."""
        params = {key: value for key, value in filters.items() if value is not None}
        return self.transport.get(f"/v1/projects/{project_id}/pulls", params=params)

    def list_project_releases(self, project_id: str, **filters: object) -> dict:
        """The repository's releases (proxied; headers only)."""
        params = {key: value for key, value in filters.items() if value is not None}
        return self.transport.get(f"/v1/projects/{project_id}/releases", params=params)

    def list_project_commits(self, project_id: str, **filters: object) -> dict:
        """One page of the proxied commit timeline: ``{state, source, items,
        cursor}``. ``state`` is honest — 'stale' is real data with degraded
        freshness, 'unavailable' means GitHub could not answer, never an empty
        history."""
        params = {key: value for key, value in filters.items() if value is not None}
        return self.transport.get(f"/v1/projects/{project_id}/commits", params=params)

    def get_project_commit(self, project_id: str, sha: str, source_id: str | None = None) -> dict:
        """One commit in full (message body, files, stats, linked runs)."""
        params = {"source_id": source_id} if source_id else None
        return self.transport.get(f"/v1/projects/{project_id}/commits/{sha}", params=params)

    def get_run_code(self, run_id: str) -> dict:
        """The run panel's answer: the commit the run's snapshot was BASED ON
        (nearest pushed ancestor — provenance, never the exact tree)."""
        return self.transport.get(f"/v1/runs/{run_id}/code")

    def compare_run_code(self, run_id: str, to: str) -> dict:
        """What changed in code between two runs (integrations-v2 phase 6).

        ``base`` in the answer is the OLDER run whichever way this call named
        them (``swapped`` says when they were reordered); ``commits`` reads
        oldest-first from STORED link rows only — mismatched repos come back
        as a named ``state``, never an error."""
        return self.transport.get(f"/v1/runs/{run_id}/code/compare", params={"to": to})

    def get_experiment_code(self, experiment_id: str, *, project_id: str | None = None) -> dict:
        """What changed in the repo between an experiment's runs: the
        project's sources (inherited — there is no experiment-level attach),
        each run's stored ``owner/repo@sha``, and the per-repo commit window.
        Stored rows only; the backend never asks GitHub on this read."""
        return self._on_experiment(
            lambda p, e: self.transport.get(f"/v1/projects/{p}/experiments/{e}/code"),
            experiment_id,
            project_id,
        )


class IntegrationsResource(Resource):
    """`client.integrations`: typed code, commit and mirror reads. W&B reads stay dicts: their
    models refuse unknown fields, so a newer server's field would raise."""

    __slots__ = ()

    def list_code_sources(self, project_id: str) -> list[CodeSourceOut]:
        """`Client.list_project_code_sources` as `CodeSourceOut`s."""
        return self._to_models(CodeSourceOut, self._client.list_project_code_sources(project_id))

    def list_mirror_connections(self) -> list[MirrorConnectionOut]:
        """`Client.list_mirror_connections` as `MirrorConnectionOut`s."""
        return self._to_models(MirrorConnectionOut, self._client.list_mirror_connections())

    def list_mirror_scope_options(self, connection_id: str) -> list[ScopeOptionOut]:
        """`Client.list_mirror_scope_options` as `ScopeOptionOut`s."""
        return self._to_models(
            ScopeOptionOut,
            self._client.list_mirror_scope_options(connection_id),
        )

    def list_pulls(self, project_id: str, **filters: object) -> PullsPage:
        """`Client.list_project_pulls` as a `PullsPage`."""
        return self._to_model(PullsPage, self._client.list_project_pulls(project_id, **filters))

    def list_releases(self, project_id: str, **filters: object) -> ReleasesPage:
        """`Client.list_project_releases` as a `ReleasesPage`."""
        return self._to_model(
            ReleasesPage,
            self._client.list_project_releases(project_id, **filters),
        )

    def list_commits(self, project_id: str, **filters: object) -> CommitsPage:
        """`Client.list_project_commits` as a `CommitsPage`."""
        return self._to_model(CommitsPage, self._client.list_project_commits(project_id, **filters))

    def get_commit(self, project_id: str, sha: str, source_id: str | None = None) -> CommitCard:
        """`Client.get_project_commit` as a `CommitCard`."""
        return self._to_model(
            CommitCard,
            self._client.get_project_commit(project_id, sha, source_id),
        )

    def get_run_code(self, run_id: str) -> RunCodeOut:
        """`Client.get_run_code` as a `RunCodeOut`."""
        return self._to_model(RunCodeOut, self._client.get_run_code(run_id))

    def compare_run_code(self, run_id: str, to: str) -> RunCodeCompareOut:
        """`Client.compare_run_code` as a `RunCodeCompareOut`."""
        return self._to_model(RunCodeCompareOut, self._client.compare_run_code(run_id, to))

    def get_experiment_code(
        self, experiment_id: str, *, project_id: str | None = None,
    ) -> ExperimentCodeOut:
        """`Client.get_experiment_code` as an `ExperimentCodeOut`."""
        return self._to_model(
            ExperimentCodeOut,
            self._client.get_experiment_code(experiment_id, project_id=project_id),
        )
