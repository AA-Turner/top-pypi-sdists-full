"""Folder recovery through real scoped coverage, manifests and SDK receipts.

Only model output and the remote service are substituted. File walks, hashing,
approval persistence, unit journals, immutable staging and drain are real.
"""

from __future__ import annotations

from contextlib import nullcontext
import hashlib
import json
import os
from pathlib import Path
import uuid

import pytest

from probe.cli import backfill as bf
from probe.cli import backfill_github as gh
from probe.cli import backfill_import as imp
from probe.cli import backfill_plan as plans
from probe.cli import backfill_reconstruction as reconstruction
from probe.cli import backfill_run as runner
from probe.cli import telemetry, tui
from probe.cli.backfill_coverage import Coverage, Scope
from probe.cli.backfill_ledger import Ledger
from probe.sdk import journal as jm
from probe.sdk.client import Client
from probe.sdk.config import Settings


class Remote:
    def __init__(self):
        self.records = {}
        self.calls = []

    def upload_fingerprinted(self, anchor, anchor_id, name, path, *, digest, size, **kwargs):
        data = Path(path).read_bytes()
        assert hashlib.sha256(data).hexdigest() == digest and len(data) == size
        self.calls.append((anchor_id, name, data, kwargs))
        return self.records.setdefault(
            (anchor, anchor_id, name, digest),
            {
                "id": str(uuid.uuid4()),
                "name": name,
                "status": "complete",
                "uri": f"r2://test/{digest}",
                "content_hash": digest,
                "size_bytes": size,
                "is_reference": False,
            },
        )


class Harness:
    def __init__(self, root, monkeypatch):
        self.folder = root / "folder"
        self.folder.mkdir()
        (self.folder / "a.py").write_text("value = 1\n")
        self.remote = Remote()
        self.projects = {}
        self.created = []
        self.classified = []
        self.manifested = []
        self.calls = []
        self.events = []
        self.attachments = []
        self.git = gh.GitEvidenceBundle()
        self.placement = lambda path: "project"
        self.failed_model = False
        self.model_success = True
        self.after_units = lambda: None
        self.lost_create_ack = False
        self.root = root
        self.monkeypatch = monkeypatch
        self.client = self.new_client()
        monkeypatch.setattr(runner, "classify", self.classify)
        monkeypatch.setattr(bf, "launch_agent", self.launch)
        real_run_units = runner.run_units

        def units(*args, **kwargs):
            result = real_run_units(*args, **kwargs)
            self.after_units()
            return result

        monkeypatch.setattr(runner, "run_units", units)
        monkeypatch.setattr(gh, "collect_evidence", self.collect)
        monkeypatch.setattr(gh, "attach_reviewed_sources", self.attach)
        monkeypatch.setattr(
            reconstruction, "complete_reconstruction", lambda *a, **kw: ["Draft retained locally."]
        )
        monkeypatch.setattr(tui, "page", lambda *a, **kw: "")
        monkeypatch.setattr(tui, "review", lambda title, lines, choices: choices[0][1])
        monkeypatch.setattr(tui, "interactive", lambda: False)

    def new_client(self, *, tenant="tenant", workspace="workspace", backend="https://test.invalid"):
        client = Client(
            settings=Settings(base_url=backend, token="test-token", workspace=workspace),
            spool_dir=self.root / "outbox",
            async_writes=False,
            auto_drain=False,
            attribution="backfill",
        )
        self.monkeypatch.setattr(client, "me", lambda: {"customer_id": tenant, "user_id": "user"})
        self.monkeypatch.setattr(
            client,
            "get_workspace",
            lambda ident: {
                "id": ident,
                "customer_id": tenant,
                "kind": "personal",
                "owner_user_id": "user",
            },
        )
        self.monkeypatch.setattr(
            client,
            "list_projects",
            lambda **kw: [
                row
                for row in self.projects.values()
                if row["customer_id"] == tenant and row["workspace_id"] == workspace
            ],
        )
        self.monkeypatch.setattr(client, "get_project", lambda ident: self.projects[ident])
        self.monkeypatch.setattr(
            client,
            "resolve_project",
            lambda slug, **kw: next(
                (
                    row
                    for row in self.projects.values()
                    if row["slug"] == slug and row["customer_id"] == tenant
                ),
                None,
            ),
        )

        def create(slug, name, **kw):
            project = {
                "id": str(uuid.uuid4()),
                "slug": slug,
                "name": name,
                "customer_id": tenant,
                "workspace_id": kw["workspace_id"],
            }
            self.projects[project["id"]] = project
            self.created.append(project)
            if self.lost_create_ack:
                self.lost_create_ack = False
                raise TimeoutError("created before response was lost")
            return project

        self.monkeypatch.setattr(client, "create_project", create)
        return client

    def classify(self, folder, evidence, **kwargs):
        assert self.calls[-1] == "git"
        assert (kwargs["work_dir"] / "github-context.txt").read_text() == self.git.prompt_text
        paths = sorted(str(Path(file.path).relative_to(folder)) for file in evidence.files)
        self.classified.append(paths)
        self.calls.append("classify")
        assigned = [plans.Assignment(path, self.placement(path)) for path in paths]
        slugs = sorted({entry.project for entry in assigned})
        return plans.Plan([plans.ProjectSpec(slug) for slug in slugs], assigned), "", None

    def launch(self, folder, prompt, **kwargs):
        if self.failed_model:
            return False, "model failed before writing a manifest"
        destination = next(
            line.split("Write JSONL to:", 1)[1].strip()
            for line in prompt.splitlines()
            if line.strip().startswith("Write JSONL to:")
        )
        paths = (
            prompt.split("are yours (relative to the folder):\n\n", 1)[1]
            .split("\n\nRead them", 1)[0]
            .splitlines()
        )
        rows = []
        for path in paths:
            if path.strip():
                value = (folder / path.strip()).read_text()
                self.manifested.append((path.strip(), value))
                rows.append({"path": path.strip(), "notes": value.strip()})
        Path(destination).write_text("".join(json.dumps(row) + "\n" for row in rows))
        return self.model_success, ""

    def collect(self, *args, **kwargs):
        self.calls.append("git")
        return self.git

    def attach(self, client, project_id, bundle):
        if bundle.evidence:
            self.attachments.append((project_id, [entry.repo for entry in bundle.evidence]))
        return [{"repo": item.repo, "state": "reused"} for item in bundle.evidence]

    def emit(self, event, **kwargs):
        self.events.append((event, kwargs))

    def run(self, **kwargs):
        return imp.execute(
            client_factory=lambda: nullcontext(self.client),
            folder=self.folder,
            agent=bf.Agent.CLAUDE,
            interactive=kwargs.pop("interactive", False),
            yes=kwargs.pop("yes", True),
            concurrency=1,
            telemetry=self,
            **kwargs,
        )

    def coverage(self, project=None):
        return Coverage.for_folder(self.folder, Scope.resolve(self.client, project))

    def report(self, project=None):
        with self.coverage(project).writer() as coverage:
            return coverage.report()

    def drain(self):
        return jm.drain(jm.Journal(self.root / "outbox"), client_factory=lambda _: self.remote)

    @property
    def outcome(self):
        return [
            data["outcome"]
            for event, data in self.events
            if event == telemetry.EVENT_BACKFILL_SUMMARY
        ][-1]


def make_harness(tmp_path, monkeypatch):
    monkeypatch.setenv("PROBE_BACKFILL_STATE_DIR", str(tmp_path / "state"))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "config.json"))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "xdg-state"))
    monkeypatch.setattr(jm, "MIN_FREE_BYTES", 0)
    return Harness(tmp_path, monkeypatch)


@pytest.fixture
def scoped_harness(tmp_path, monkeypatch):
    return make_harness(tmp_path, monkeypatch)


def test_fresh_queue_resume_requires_real_durable_receipt(scoped_harness):
    h = scoped_harness
    lines = h.run()
    assert h.classified == [["a.py"]] and h.manifested == [("a.py", "value = 1\n")]
    assert h.report()["queued"] == ["a.py"]
    assert h.outcome == telemetry.BackfillOutcome.PARTIAL
    assert any("Backfill is partial" in line for line in lines)
    queue = h.client._delivery_journal()
    assert len(queue.pending()) == 1 and len(list(queue.blobs_dir.iterdir())) == 1
    assert h.drain().delivered == 1
    lines = h.run()
    assert h.report()["delivered"] == ["a.py"] and not queue.pending()
    assert len(h.classified) == len(h.manifested) == len(h.created) == 1
    assert h.outcome == telemetry.BackfillOutcome.SUCCESS
    assert any("Every observed file has a receipt" in line for line in lines)


def test_optional_wandb_outage_cannot_block_real_file_delivery(scoped_harness, monkeypatch):
    h = scoped_harness
    monkeypatch.setattr(
        tui, "review",
        lambda title, lines, choices: "wandb" if title == "Add W&B history" else "import",
    )

    def unavailable():
        raise ConnectionError("provider unavailable")

    monkeypatch.setattr(h.client, "list_mirror_connections", unavailable)
    lines = h.run(interactive=True, yes=False)
    assert any("W&B history pending" in line for line in lines)
    assert h.report()["queued"] == ["a.py"]
    assert h.drain().delivered == 1
    lines = h.run(interactive=True, yes=False)
    assert h.report()["delivered"] == ["a.py"]
    assert h.outcome == telemetry.BackfillOutcome.SUCCESS
    assert any("Every observed file has a receipt" in line for line in lines)
    assert any("W&B history pending" in line for line in lines)
    assert len(h.remote.records) == len(h.classified) == 1


def test_new_file_added_during_resume_stays_unreviewed_until_next_delta(scoped_harness):
    h = scoped_harness
    h.run()
    h.drain()
    h.after_units = lambda: (h.folder / "b.py").write_text("new = True\n")
    lines = h.run()
    assert h.report()["new"] == ["b.py"]
    assert h.outcome == telemetry.BackfillOutcome.PARTIAL
    assert not any("Every observed file" in line for line in lines)
    h.after_units = lambda: None
    h.run()
    assert h.classified == [["a.py"], ["b.py"]]
    assert h.drain().delivered == 1


def test_same_stat_rewrite_requires_review_and_does_not_reuse_old_manifest(scoped_harness):
    h = scoped_harness
    h.run()
    h.drain()
    source = h.folder / "a.py"
    before = source.stat()
    source.write_text("value = 2\n")
    os.utime(source, ns=(before.st_atime_ns, before.st_mtime_ns))
    h.run()
    assert h.report()["changed"] == ["a.py"] and len(h.classified) == 1
    assert h.outcome == telemetry.BackfillOutcome.PARTIAL
    h.run(import_changed=True)
    assert h.classified == [["a.py"], ["a.py"]]
    assert h.manifested == [("a.py", "value = 1\n"), ("a.py", "value = 2\n")]
    assert h.drain().delivered == 1
    assert [call[2] for call in h.remote.calls] == [b"value = 1\n", b"value = 2\n"]
    assert h.remote.calls[-1][3]["notes"] == "value = 2"


@pytest.mark.parametrize("selection", [False, True])
def test_changed_file_review_requires_explicit_opt_in(scoped_harness, monkeypatch, selection):
    h = scoped_harness
    h.run()
    h.drain()
    (h.folder / "a.py").write_text("value = 2\n")
    reviews = []

    def review(title, lines, choices):
        if title == "Add W&B history":
            return "skip"
        reviews.append(title)
        if title == "Review changed files":
            assert choices == [
                ("Leave changed files pending", False),
                ("Review changed files for import", True),
            ]
            assert "a.py" in lines
            return selection
        assert title == "Review the import plan"
        return "import"

    monkeypatch.setattr(tui, "review", review)
    h.run(interactive=True, yes=False)

    assert reviews == ["Review changed files", *(["Review the import plan"] if selection else [])]
    assert len(h.classified) == (2 if selection else 1)
    if selection:
        assert h.report()["queued"] == ["a.py"]
        assert h.manifested[-1] == ("a.py", "value = 2\n")
    else:
        assert h.report()["changed"] == ["a.py"]
        assert not h.client._delivery_journal().pending()


@pytest.mark.parametrize("selection", [None, tui.BACK])
def test_cancelling_changed_file_review_keeps_the_delta_pending(
    scoped_harness, monkeypatch, selection
):
    h = scoped_harness
    h.run()
    h.drain()
    (h.folder / "a.py").write_text("value = 2\n")
    monkeypatch.setattr(tui, "review", lambda *a, **kw: selection)

    with pytest.raises(KeyboardInterrupt):
        h.run(interactive=True, yes=False)

    assert h.report()["changed"] == ["a.py"]
    assert len(h.classified) == len(h.manifested) == 1
    assert not h.client._delivery_journal().pending()
    assert h.outcome == telemetry.BackfillOutcome.ABORTED


@pytest.mark.parametrize("changed", ["tenant", "workspace", "backend", "project"])
def test_other_scope_cannot_reuse_delivered_coverage_or_source_id(scoped_harness, changed):
    h = scoped_harness
    h.run()
    h.drain()
    h.run()
    previous = h.coverage()
    options = {}
    if changed == "project":
        options["project"] = "project"
    else:
        h.client = h.new_client(
            **{changed: "other" if changed != "backend" else "https://other.invalid"}
        )
        if changed == "workspace":
            h.placement = lambda _: "other-project"
    h.run(**options, source_id=previous.source_id)
    assert h.outcome == telemetry.BackfillOutcome.PARTIAL
    assert len(h.classified) == 1
    h.run(**options)
    assert h.coverage(options.get("project")).directory != previous.directory
    assert h.report(options.get("project"))["queued"] == ["a.py"]
    assert len(h.classified) == 2


def test_project_create_lost_ack_resumes_saved_review_without_model(scoped_harness):
    h = scoped_harness
    h.lost_create_ack = True
    h.run()
    assert len(h.classified) == len(h.created) == 1 and not h.manifested
    with h.coverage().writer() as coverage:
        assert coverage.meta("approved_request")["hashes"]["a.py"]
    h.run()
    assert len(h.classified) == len(h.created) == len(h.manifested) == 1
    assert h.report()["queued"] == ["a.py"]


def test_git_context_precedes_classification_and_attaches_only_reviewed_subset(scoped_harness):
    h = scoped_harness
    (h.folder / "nested").mkdir()
    (h.folder / "nested/b.py").write_text("nested = True\n")
    h.placement = lambda path: "nested-project" if path.startswith("nested/") else "project"
    h.git = gh.GitEvidenceBundle(
        [
            gh.GitEvidence("org/outer", "main", local_folder=str(h.folder), state="ok"),
            gh.GitEvidence("org/nested", "main", local_folder=str(h.folder / "nested"), state="ok"),
        ]
    )
    h.run()
    by_slug = {h.projects[project_id]["slug"]: repos for project_id, repos in h.attachments}
    assert by_slug == {"project": ["org/outer"], "nested-project": ["org/nested"]}
    assert h.calls[:2] == ["git", "classify"]


def test_failed_model_cannot_be_reported_as_delivered(scoped_harness):
    h = scoped_harness
    h.failed_model = True
    lines = h.run()
    assert h.report()["unresolved"] == ["a.py"]
    assert not h.client._delivery_journal().pending() and not h.remote.calls
    assert h.outcome == telemetry.BackfillOutcome.PARTIAL
    assert not any("Every observed file" in line for line in lines)
    h.failed_model = False
    h.run()
    assert len(h.classified) == 1 and len(h.manifested) == 1


def test_code_attachment_outage_does_not_abort_durable_file_delivery(scoped_harness, monkeypatch):
    h = scoped_harness
    h.git = gh.GitEvidenceBundle(
        [gh.GitEvidence("org/repo", "main", local_folder=str(h.folder), state="ok")]
    )

    def outage(*args, **kwargs):
        raise TimeoutError()

    monkeypatch.setattr(gh, "attach_reviewed_sources", outage)
    lines = h.run()
    assert h.report()["queued"] == ["a.py"] and len(h.manifested) == 1
    assert any("attachment pending" in line and "file delivery continues" in line for line in lines)
    assert h.drain().delivered == 1


@pytest.mark.parametrize("selection", [False, True, None, tui.BACK])
def test_saved_file_code_sources_require_an_explicit_attachment_choice(
    scoped_harness, monkeypatch, selection
):
    h = scoped_harness
    h.run()
    h.drain()
    # Model a saved import from before Code-source choices were recorded.
    with h.coverage().writer() as coverage:
        coverage.put_meta("reviewed_sources", {})
    h.git = gh.GitEvidenceBundle(
        [gh.GitEvidence("org/repo", "main", local_folder=str(h.folder), state="ok")]
    )
    prompts = []

    def review(title, lines, choices):
        if title == "Add W&B history":
            return "skip"
        prompts.append(title)
        assert title == "Review Code sources"
        assert choices == [
            ("Attach these Code sources", True),
            ("Leave attachment pending", False),
        ]
        assert any("org/repo" in line for line in lines)
        return selection

    monkeypatch.setattr(tui, "review", review)
    if selection is None or selection is tui.BACK:
        with pytest.raises(KeyboardInterrupt):
            h.run(interactive=True, yes=False)
        assert h.outcome == telemetry.BackfillOutcome.ABORTED
    else:
        lines = h.run(interactive=True, yes=False)
        if selection is False:
            assert any("attachment is pending review" in line for line in lines)

    assert prompts == ["Review Code sources"]
    assert len(h.classified) == len(h.manifested) == 1
    assert h.report()["delivered"] == ["a.py"]
    assert len(h.attachments) == (1 if selection is True else 0)
    with h.coverage().writer() as coverage:
        assert bool(coverage.meta("reviewed_sources", {})) is (selection is True)


def test_unbound_old_unit_manifest_is_regenerated_without_reclassification(scoped_harness):
    h = scoped_harness
    h.failed_model = True
    h.run()
    with h.coverage().writer() as coverage:
        coverage.put_meta("approved_units", {})
        ledger = Ledger(coverage.directory / "units.jsonl")
        record = next(iter(ledger.read().units.values()))
        (coverage.directory / "manifests" / f"{record.unit.unit_id}.jsonl").write_text(
            '{"path":"a.py","notes":"obsolete unbound interpretation"}\n'
        )
    h.failed_model = False
    h.run()
    h.drain()
    assert len(h.classified) == 1 and h.remote.calls[-1][3]["notes"] == "value = 1"


def test_staging_pressure_retains_manifest_and_retries_without_another_model(
    scoped_harness, monkeypatch
):
    h = scoped_harness
    with monkeypatch.context() as patch:
        patch.setattr(jm.Journal, "_staging_headroom", lambda *args: "disk full")
        h.run()
    assert h.report()["unresolved"] == ["a.py"]
    assert not h.client._delivery_journal().pending()
    h.run()
    assert len(h.classified) == len(h.manifested) == 1
    assert h.report()["queued"] == ["a.py"] and h.drain().delivered == 1


def test_remote_acceptance_before_receipt_does_not_create_false_completion(
    scoped_harness, monkeypatch
):
    h = scoped_harness
    h.run()

    def lost_local_receipt(conn):
        raise OSError("disk full after remote acceptance")

    with monkeypatch.context() as patch:
        patch.setattr(jm.Journal, "_commit_receipt_index", staticmethod(lost_local_receipt))
        assert h.drain().delivered == 0
    h.run()
    assert h.outcome == telemetry.BackfillOutcome.PARTIAL
    assert len(h.remote.records) == 1 and len(h.classified) == len(h.manifested) == 1
    assert h.drain().delivered == 1
    h.run()
    assert h.report()["delivered"] == ["a.py"] and len(h.remote.records) == 1


def test_failed_agent_exit_stays_partial_even_when_valid_rows_are_delivered(
    scoped_harness, monkeypatch
):
    h = scoped_harness
    h.model_success = False
    monkeypatch.setattr(h.client, "_wake_delivery", h.drain)
    lines = h.run()
    assert h.report()["delivered"] == ["a.py"]
    assert h.outcome == telemetry.BackfillOutcome.PARTIAL
    assert any("Backfill is partial" in line for line in lines)
    assert not any("Every observed file" in line for line in lines)


@pytest.mark.parametrize("interactive,yes", [(False, False), (False, True), (True, True)])
def test_recovery_hint_never_auto_adopts_source_identity(interactive, yes, monkeypatch):
    def no_prompt(*args, **kwargs):
        raise AssertionError("automated run must not prompt")

    monkeypatch.setattr(tui, "review", no_prompt)
    source_id, lines = imp._choose_source(
        [{"source_id": "old-id", "paths": ["/old/mount"]}], interactive=interactive, yes=yes
    )
    assert source_id is None
    assert any("old-id: /old/mount" in line for line in lines)
    assert any("--source-id" in line for line in lines)


def test_recovery_choice_accepts_only_an_explicit_listed_id(monkeypatch):
    candidates = [{"source_id": "old-id", "paths": ["/old/mount"]}]
    monkeypatch.setattr(tui, "review", lambda *args, **kwargs: "old-id")
    assert imp._choose_source(candidates, interactive=True, yes=False)[0] == "old-id"
    monkeypatch.setattr(tui, "review", lambda *args, **kwargs: "unrelated-id")
    with pytest.raises(ValueError, match="listed source ID"):
        imp._choose_source(candidates, interactive=True, yes=False)


def test_recovery_menu_defaults_to_a_separate_import(monkeypatch):
    candidates = [
        {"source_id": "first-id", "paths": ["/first/mount"]},
        {"source_id": "second-id", "paths": ["/second/mount"]},
    ]

    def review(title, lines, choices):
        assert title == "Recover an earlier import?"
        assert choices == [
            ("Start a separate import", ""),
            ("Recover first-id", "first-id"),
            ("Recover second-id", "second-id"),
        ]
        return choices[0][1]

    monkeypatch.setattr(tui, "review", review)
    source_id, lines = imp._choose_source(candidates, interactive=True, yes=False)
    assert source_id is None
    assert any("Starting a separate source" in line for line in lines)


@pytest.mark.parametrize("selection", [None, tui.BACK])
def test_cancelling_recovery_never_starts_or_adopts_an_import(monkeypatch, selection):
    monkeypatch.setattr(tui, "review", lambda *a, **kw: selection)
    with pytest.raises(KeyboardInterrupt):
        imp._choose_source(
            [{"source_id": "old-id", "paths": ["/old/mount"]}],
            interactive=True,
            yes=False,
        )


def test_moved_folder_interactive_choice_recovers_receipts_without_reclassification(
    scoped_harness, monkeypatch
):
    h = scoped_harness
    h.run()
    h.drain()
    original = h.coverage()
    old_path = str(h.folder)
    h.folder = h.folder.rename(h.root / "remounted")
    prompts = []

    def choose(title, lines, choices):
        assert title == "Recover an earlier import?"
        assert choices == [
            ("Start a separate import", ""),
            (f"Recover {original.source_id}", original.source_id),
        ]
        prompts.append(lines)
        return original.source_id

    monkeypatch.setattr(tui, "review", choose)
    lines = h.run(interactive=True, yes=False)
    assert len(prompts) == 1 and any(old_path in line for line in prompts[0])
    assert h.coverage().source_id == original.source_id
    assert h.report()["delivered"] == ["a.py"] and len(h.classified) == 1
    assert any("Recovering selected source" in line for line in lines)


def test_moved_folder_headless_hint_requires_explicit_source_id_to_adopt(scoped_harness):
    h = scoped_harness
    h.run()
    h.drain()
    original = h.coverage()
    h.folder = h.folder.rename(h.root / "remounted")
    lines = h.run()
    assert h.coverage().source_id != original.source_id
    assert h.report()["queued"] == ["a.py"] and len(h.classified) == 2
    assert any(original.source_id in line for line in lines)
    h.run(source_id=original.source_id)
    assert h.coverage().source_id == original.source_id
    assert h.report()["delivered"] == ["a.py"] and len(h.classified) == 2
