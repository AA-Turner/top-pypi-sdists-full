"""Run lineage: the doors, the refusal, and the auto-capture gate.

Written because the fleet audit found the field populated on 24 of 506 runs and
NOTHING pinning any of it: `run(parent_run_id=…)` worked only through `**run_kw`
and no test proved it reached the wire, so the passthrough could have broken
silently at any refactor.
"""

from __future__ import annotations

import pytest

from probe import errors
from probe.sdk import agent_session
from probe.sdk.client import Client
from tests.conftest import open_run


class TestTheDoorsCarryLineage:
    def test_explicit_kwargs_reach_the_wire(self, client):
        """The passthrough `run()` relies on, pinned.

        `_run_impl` splats run_kw into `create_run`, so this worked before it was
        ever a named parameter -- and nothing asserted it. Asserted on the STORED
        row, not on the kwargs, because a kwarg that never leaves the client is
        exactly the failure this guards.
        """
        parent = open_run(client, experiment="e1", name="parent", heartbeat=False)
        child = open_run(
            client,
            experiment="e1",
            name="child",
            parent_run_id=parent.id,
            parent_relation="retry",
            heartbeat=False,
        )
        row = client.get_run(child.id)
        assert row["parent_run_id"] == parent.id
        assert row["parent_relation"] == "retry"

    def test_child_of_a_project_direct_run_does_not_post_to_experiment_none(self, client):
        """`Run.experiment_id` stringified unconditionally, so `child()` on a
        project-direct run POSTed to `/v1/experiments/None/runs` -- 122 of 506
        fleet runs are project-direct, i.e. the W&B-shaped half of the platform."""
        project = client.create_project("proj-direct", kind="general")
        parent = client.create_project_run(project["id"], "parent", heartbeat=False)
        assert parent.experiment_id is None  # not the string "None"
        child = parent.child("attempt-2", relation="retry", heartbeat=False)
        row = client.get_run(child.id)
        assert row["parent_run_id"] == parent.id
        assert row["parent_relation"] == "retry"
        assert row["project_id"] == project["id"]

    def test_a_child_needs_no_name(self, client):
        """`child()` took `name` positionally and required it, so every retry
        was hand-named and frozen out of server titling. Omitted, no name is
        sent and the server mints one, like any other run."""
        parent = open_run(client, experiment="e1", name="parent", heartbeat=False)
        child = parent.child(relation="retry", heartbeat=False)
        row = client.get_run(child.id)
        assert row["parent_run_id"] == parent.id
        assert row["parent_relation"] == "retry"
        assert row["name_customized"] is False
        assert row["name"] == row["slug"]


class TestTheRelationIsNeverGuessed:
    def test_a_parent_with_no_relation_is_refused(self):
        """`_run_create_body` read `parent_relation or "fork"`, which turned the
        server's 422 into a silent success carrying a word nobody chose."""
        with pytest.raises(errors.ValidationError, match="fork, resume, retry or branch"):
            Client._run_create_body(
                "a-run",
                description=None,
                notes=None,
                source="api",
                external_id=None,
                parent_run_id="11111111-1111-1111-1111-111111111111",
                parent_relation=None,
                group_id=None,
                config=None,
                tags=None,
                metadata=None,
                labeled_point_budget=None,
            )

    def test_the_refusal_names_the_edge_door_for_a_consuming_run(self):
        """The miles case: an eval of a checkpoint is not fork|resume|retry|branch,
        and the error has to say where it DOES go or the caller picks one anyway."""
        with pytest.raises(errors.ValidationError, match="probe edge add"):
            Client._run_create_body(
                "a-run",
                description=None,
                notes=None,
                source="api",
                external_id=None,
                parent_run_id="11111111-1111-1111-1111-111111111111",
                parent_relation=None,
                group_id=None,
                config=None,
                tags=None,
                metadata=None,
                labeled_point_budget=None,
            )


class TestAutoRetryCaptureGate:
    """The four conjuncts. Each one was measured, and dropping any of them writes
    a wrong edge -- which is worse than no edge, because a stored relation reads
    later as something someone determined."""

    @pytest.fixture(autouse=True)
    def _in_an_agent_session(self, monkeypatch):
        """The gate is a NO-OP outside a coding agent, by design: it scopes on the
        session so it only ever reasons about runs this SDK opened. 19 of the 31
        retry-shaped runs in the fleet carry no session at all (machine launchers),
        and those are deliberately out of reach."""
        monkeypatch.setattr(
            agent_session, "resolve_agent_session", lambda *a, **k: ("claude_code", "sess-1")
        )

    def _client_with_previous(self, client, monkeypatch, **previous):
        row = {
            "id": "99999999-9999-4999-8999-999999999999",
            # The scope is checked CLIENT-side now. Filtering the query by
            # experiment_id would have answered "most recent run in this
            # experiment", not "the run before this one" -- so a session that went
            # A(exp1, failed) -> B(exp2, ok) -> C(exp1) would attach C to A.
            "experiment_id": "exp-1",
            "project_id": None,
            "status": "failed",
            "ended_at": "2026-08-29T00:00:00Z",
            "config": {"lr": 3e-4},
            **previous,
        }
        monkeypatch.setattr(
            client, "list_runs", lambda **kw: type("P", (), {"items": [row]})()
        )
        return row

    def _attach(self, client, config=None):
        run_kw: dict = {"config": config if config is not None else {"lr": 3e-4}}
        client._maybe_attach_retry_parent(run_kw, experiment_id="exp-1")
        return run_kw

    def test_off_by_default(self, client, monkeypatch):
        """Precision was measured retrospectively on SETTLED statuses; the reaper
        takes up to 900s to write crashed/untracked, so live behaviour is not the
        replay. It stays off until someone has watched it."""
        monkeypatch.delenv("PROBE_AUTO_RETRY_LINEAGE", raising=False)
        self._client_with_previous(client, monkeypatch)
        assert "parent_run_id" not in self._attach(client)

    def test_attaches_when_every_conjunct_holds(self, client, monkeypatch):
        monkeypatch.setenv("PROBE_AUTO_RETRY_LINEAGE", "1")
        row = self._client_with_previous(client, monkeypatch)
        run_kw = self._attach(client)
        assert run_kw["parent_run_id"] == row["id"]
        assert run_kw["parent_relation"] == "retry"

    def test_a_live_predecessor_is_a_sibling_not_a_parent(self, client, monkeypatch):
        """Parallel subagents of one Claude Code session share ONE session id
        (`agent_session.py`: no child-session handling), so without the ended_at
        gate a concurrent sweep member reads as the run before this one."""
        monkeypatch.setenv("PROBE_AUTO_RETRY_LINEAGE", "1")
        self._client_with_previous(client, monkeypatch, ended_at=None)
        assert "parent_run_id" not in self._attach(client)

    def test_a_completed_predecessor_is_not_a_retry(self, client, monkeypatch):
        """The immediately-preceding conjunct. A dead-FILTERED query cannot answer
        this: a session that went A(failed) -> B(completed) -> C would hand back A
        and pass. Measured on the fleet, dropping this made 4 of 9 edges wrong --
        a `dataset-prep` run labeled a retry of a failure two successes earlier."""
        monkeypatch.setenv("PROBE_AUTO_RETRY_LINEAGE", "1")
        self._client_with_previous(client, monkeypatch, status="completed")
        assert "parent_run_id" not in self._attach(client)

    def test_untracked_counts_as_dead(self, client, monkeypatch):
        """The reaper's verdict for a run that never heartbeated -- the DESIGNED
        terminal state for agent-driven CLI runs, i.e. this feature's population.
        48 runs carry it fleet-wide, and the first draft of the gate omitted it."""
        monkeypatch.setenv("PROBE_AUTO_RETRY_LINEAGE", "1")
        row = self._client_with_previous(client, monkeypatch, status="untracked")
        assert self._attach(client)["parent_run_id"] == row["id"]

    def test_a_different_config_is_a_sweep_sibling(self, client, monkeypatch):
        """Config equality is what separates a retry from a seed sweep -- the seed
        lives in the config. Name matching does not: one failed seed would make
        every later seed a 'retry' of it, 48% false positives fleet-wide."""
        monkeypatch.setenv("PROBE_AUTO_RETRY_LINEAGE", "1")
        self._client_with_previous(client, monkeypatch, config={"lr": 3e-4, "seed": 7})
        assert "parent_run_id" not in self._attach(client)

    def test_an_empty_config_has_no_discriminator(self, client, monkeypatch):
        monkeypatch.setenv("PROBE_AUTO_RETRY_LINEAGE", "1")
        self._client_with_previous(client, monkeypatch, config={})
        assert "parent_run_id" not in self._attach(client, config={})

    def test_a_declared_parent_is_never_second_guessed(self, client, monkeypatch):
        monkeypatch.setenv("PROBE_AUTO_RETRY_LINEAGE", "1")
        self._client_with_previous(client, monkeypatch)
        run_kw = {"config": {"lr": 3e-4}, "parent_run_id": "declared", "parent_relation": "fork"}
        client._maybe_attach_retry_parent(run_kw, experiment_id="exp-1")
        assert run_kw["parent_run_id"] == "declared"

    def test_shadow_mode_writes_nothing(self, client, monkeypatch):
        monkeypatch.setenv("PROBE_AUTO_RETRY_LINEAGE", "shadow")
        self._client_with_previous(client, monkeypatch)
        assert "parent_run_id" not in self._attach(client)

    def test_a_lookup_failure_opens_the_run_anyway(self, client, monkeypatch):
        """Fails open. Lineage is never worth failing a training run over."""
        monkeypatch.setenv("PROBE_AUTO_RETRY_LINEAGE", "1")

        def boom(**kw):
            raise RuntimeError("backend down")

        monkeypatch.setattr(client, "list_runs", boom)
        assert "parent_run_id" not in self._attach(client)

    def test_a_predecessor_in_another_scope_is_not_the_predecessor(
        self, client, monkeypatch
    ):
        """The scope check runs CLIENT-side on purpose.

        Narrowing the QUERY by experiment_id answers "most recent run in this
        experiment", which is not "the run immediately before this one" -- a session
        that went A(exp1, failed) -> B(exp2, completed) -> C(exp1) would hand back A
        and attach C to it, the exact false positive the conjunct exists to prevent.
        So the query is unfiltered, `limit=1` gives the true predecessor, and a
        predecessor belonging to a different scope disqualifies rather than being
        skipped over.
        """
        monkeypatch.setenv("PROBE_AUTO_RETRY_LINEAGE", "1")
        self._client_with_previous(client, monkeypatch, experiment_id="some-other-exp")
        assert "parent_run_id" not in self._attach(client)


class TestAutoRetryNeedsTheSameLaunch:
    """Lineage plan L6: a relaunch runs the same command in the same place.

    The predecessor's side is its stored `metadata.launch.process`; the new
    run's is computed by the same rules (`launch.process_identity`), because
    its own launch block is written after it opens."""

    PREVIOUS_ID = "99999999-9999-4999-8999-999999999999"

    @pytest.fixture(autouse=True)
    def _armed(self, monkeypatch):
        monkeypatch.setattr(agent_session, "resolve_agent_session", lambda *a, **k: ("claude_code", "sess-1"))
        monkeypatch.setenv("PROBE_AUTO_RETRY_LINEAGE", "1")

    def _previous(self, client, monkeypatch, process):
        row = {"id": self.PREVIOUS_ID, "experiment_id": "exp-1", "project_id": None, "status": "crashed",
               "ended_at": "2026-09-27T00:00:00Z", "config": {"lr": 3e-4},
               "metadata": {"launch": {"schema": "probe.launch/1", "process": process}}}
        monkeypatch.setattr(client, "list_runs", lambda **kw: type("P", (), {"items": [row]})())

    def _attach(self, client, argv, cwd):
        from probe.sdk import launch

        run_kw: dict = {"config": {"lr": 3e-4}}
        with launch.launching(argv, cwd):
            client._maybe_attach_retry_parent(run_kw, experiment_id="exp-1")
        return run_kw.get("parent_run_id")

    def test_the_same_command_in_the_same_folder_is_a_retry(self, client, monkeypatch, tmp_path):
        self._previous(client, monkeypatch, {"entrypoint": "python", "argv": ["python", "train.py"],
                                             "cwd": str(tmp_path)})
        assert self._attach(client, ["python", "train.py"], str(tmp_path)) == self.PREVIOUS_ID

    @pytest.mark.parametrize("argv, where", [
        (["python", "eval.py"], "same"),   # another script, same (default) config
        (["python", "train.py"], "other"),  # the same command in another folder
        (["python3", "train.py"], "same"),  # another interpreter
    ])
    def test_another_command_or_folder_is_not_a_retry(self, client, monkeypatch, tmp_path, argv, where):
        self._previous(client, monkeypatch, {"entrypoint": "python", "argv": ["python", "train.py"],
                                             "cwd": str(tmp_path)})
        cwd = str(tmp_path) if where == "same" else str(tmp_path / "elsewhere")
        assert self._attach(client, argv, cwd) is None

    def test_the_argv_is_compared_as_stored_scrubbed(self, client, monkeypatch, tmp_path):
        """The launch block stores argv with credentials redacted; the new side is
        scrubbed the same way, so a key on the command line does not break a match."""
        from probe.sdk import launch

        secret = ["python", "train.py", "--api-key", "sk-" + "a" * 24]
        stored, scrubbed = launch.scrub_argv(secret)
        assert scrubbed and stored != secret
        self._previous(client, monkeypatch, {"argv": stored, "cwd": str(tmp_path)})
        assert self._attach(client, secret, str(tmp_path)) == self.PREVIOUS_ID

    def test_only_the_fields_both_sides_have_are_compared(self, client, monkeypatch, tmp_path):
        # The stored block holds argv only: the cwd cannot disqualify.
        self._previous(client, monkeypatch, {"argv": ["python", "train.py"]})
        assert self._attach(client, ["python", "train.py"], str(tmp_path / "anywhere")) == self.PREVIOUS_ID
        # No launch block at all (snapshots off, `probe run start`): as before L6.
        self._previous(client, monkeypatch, None)
        assert self._attach(client, ["python", "other.py"], str(tmp_path)) == self.PREVIOUS_ID

    def test_an_entrypoint_file_is_compared_by_its_absolute_path(self, client, monkeypatch, tmp_path):
        script = tmp_path / "train.py"
        script.write_text("print('hi')\n")
        monkeypatch.chdir(tmp_path)
        self._previous(client, monkeypatch, {"entrypoint": str(script), "argv": ["train.py"],
                                             "cwd": str(tmp_path)})
        assert self._attach(client, ["train.py"], None) == self.PREVIOUS_ID
        (tmp_path / "b").mkdir()
        (tmp_path / "b" / "train.py").write_text("print('other')\n")
        monkeypatch.chdir(tmp_path / "b")
        assert self._attach(client, ["train.py"], str(tmp_path)) is None  # b/train.py is another file

    def test_the_identity_rules_are_the_launch_blocks(self, tmp_path):
        """`process_identity` and the stored block must agree field by field, or
        every relaunch would read as a different launch."""
        from probe.sdk import launch

        argv, cwd = ["python", "train.py", "--token=abc"], str(tmp_path)
        identity, _ = launch.process_identity(argv, cwd)
        stored, _ = launch.capture_process(argv, cwd)
        for key in ("entrypoint", "argv", "cwd"):
            assert identity[key] == stored[key], key

    def test_probe_exec_names_its_child_as_the_launch(self, monkeypatch, tmp_path):
        """`probe exec` opens the run in THIS process, whose own argv is
        `probe exec ...`: the detector must compare the child's command."""
        import contextlib
        import importlib

        from probe.sdk import launch

        cli_main = importlib.import_module("probe.cli.main")
        seen: list[dict] = []

        class Opened(Exception):
            pass

        class FakeClient:
            def run(self, **_kw):
                seen.append(launch.process_identity()[0])
                raise Opened

        monkeypatch.setattr(cli_main, "_client", lambda *a, **k: contextlib.nullcontext(FakeClient()))
        monkeypatch.setattr(cli_main, "_ambient_project", lambda *a, **k: None)

        class Ctx:
            args = ["--", "python", "train.py", "--lr", "3e-4"]

        with pytest.raises(Opened):
            cli_main.exec(Ctx(), run=None, cwd=str(tmp_path), project=None, experiment=None, slug=None, name=None,
                          description=None, tag=None, external_id=None, config=None, parent=None, relation=None,
                          intent=None, authored_by=None, launcher=None, detached_launcher=False, outputs=None,
                          no_capture_outputs=False)
        assert seen == [{"argv": ["python", "train.py", "--lr", "3e-4"], "argv_scrubbed": False,
                         "cwd": str(tmp_path), "entrypoint": "python"}]
