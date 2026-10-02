"""Git-derived scope, authorized context and reviewed attachment boundaries."""

from __future__ import annotations

import subprocess
from types import SimpleNamespace

import pytest

from probe.cli import backfill_github as gh
from probe.cli.backfill import git_context


def git(root, *args):
    result = subprocess.run(
        ["git", "-C", str(root), *args], check=True, capture_output=True, text=True
    )
    return result.stdout.strip()


def repo(root, remote="git@github.com:acme/train.git"):
    root.mkdir(exist_ok=True)
    git(root, "init", "-q", "-b", "topic")
    (root / "train.py").write_text("print(1)")
    git(root, "add", ".")
    git(
        root,
        "-c",
        "user.name=Test",
        "-c",
        "user.email=test@example.invalid",
        "commit",
        "-qm",
        "initial",
    )
    git(root, "remote", "add", "origin", remote)
    return root


class Client:
    def __init__(self):
        self.transport = self
        self.calls = []
        self.sources = {}
        self.writes = []
        self.page = {
            "repo": "acme/train",
            "state": "ok",
            "access": "installation",
            "installation_id": 99,
            "head_sha": "a" * 40,
            "bounds_verified": True,
            "items": [{"sha": "a" * 40, "subject": "initial"}],
            "cursor": None,
        }

    def get(self, path, params=None):
        self.calls.append((path, params))
        if path.endswith("/branches"):
            return {"branches": [{"name": "topic", "sha": "a" * 40}]}
        if path.endswith("/commits"):
            return dict(self.page)
        if "/commits/" in path:
            return {"commit": {"sha": path.rsplit("/", 1)[-1], "files": []}}
        raise AssertionError(path)

    def list_project_code_sources(self, project):
        return self.sources.get(project, [])

    def list_project_commits(self, project, **params):
        self.calls.append((f"project:{project}", params))
        return {**self.page, "source": self.sources[project][0]}

    def get_project_commit(self, project, sha, **kw):
        return {"sha": sha}

    def attach_project_code_source(self, project, **kw):
        self.writes.append((project, kw))
        row = {"id": "source", "status": "active", **kw}
        self.sources.setdefault(project, []).append(row)
        return row


def source(**kw):
    return {
        "id": "s",
        "repo": "acme/train",
        "ref": "topic",
        "path_prefix": "",
        "status": "active",
        **kw,
    }


def test_non_origin_upstream_is_selected_and_actual_head_subdirectory_retained(tmp_path):
    root = repo(tmp_path / "r", "git@github.com:fork/train.git")
    git(root, "remote", "add", "upstream", "https://github.com/acme/train.git")
    git(root, "update-ref", "refs/remotes/upstream/stable", "HEAD")
    git(root, "branch", "--set-upstream-to=upstream/stable", "topic")
    sub = root / "training"
    sub.mkdir()
    context = git_context(sub)
    assert (context.repo, context.remote_name, context.upstream) == (
        "acme/train",
        "upstream",
        "upstream/stable",
    )
    assert context.path_prefix == "training/"
    assert context.head == git(root, "rev-parse", "HEAD")
    client = Client()
    gh.collect_evidence(client, sub)
    params = next(params for path, params in client.calls if path.endswith("/commits"))
    assert params["ref"] == "stable" and params["path"] == "training/"
    assert not client.writes


def test_ambiguous_fork_is_not_guessed(tmp_path):
    root = repo(tmp_path / "r")
    git(root, "remote", "add", "upstream", "git@github.com:other/train.git")
    client = Client()
    bundle = gh.collect_evidence(client, root)
    assert not client.calls and not bundle.evidence
    assert "ambiguous_remotes" in bundle.prompt_text


def test_detached_head_uses_actual_sha_and_is_not_auto_attached(tmp_path):
    root = repo(tmp_path / "r")
    git(root, "checkout", "--detach", "HEAD")
    client = Client()
    bundle = gh.collect_evidence(client, root)
    assert bundle.evidence[0].ref == git(root, "rev-parse", "HEAD")
    assert gh.attach_reviewed_sources(client, "p", bundle)[0]["reason"] == "branch_required"
    assert not client.writes


def test_nested_repository_scope_belongs_only_to_deepest_reviewed_files(tmp_path):
    root = repo(tmp_path / "r")
    repo(root / "nested", "git@github.com:acme/other.git")
    contexts, issues = gh.discover_repositories(
        root, [SimpleNamespace(path="train.py"), SimpleNamespace(path="nested/train.py")]
    )
    assert not issues and len(contexts) == 2
    bundle = gh.GitEvidenceBundle([gh._from_local(c, root) for c in contexts])
    assert [e.repo for e in bundle.for_paths(["nested/train.py"], folder=root).evidence] == [
        "acme/other"
    ]
    assert [e.repo for e in bundle.for_paths(["train.py"], folder=root).evidence] == ["acme/train"]


def test_project_free_reads_supply_context_then_only_reviewed_attach_writes(tmp_path):
    root = repo(tmp_path / "r")
    client = Client()
    bundle = gh.collect_evidence(client, root)
    assert bundle.evidence[0].access == "installation"
    assert "initial" in bundle.prompt_text
    assert not client.writes
    result = gh.attach_reviewed_sources(client, "p", bundle)
    assert result[0]["state"] == "attached" and client.writes[0][1]["via"] == "wizard"
    result = gh.attach_reviewed_sources(client, "p", bundle)
    assert result[0]["state"] == "reused" and len(client.writes) == 1


def test_zip_reuses_existing_source_and_preserves_its_bounds(tmp_path):
    client = Client()
    client.sources["p"] = [source(start_at="2026-01-01T00:00:00Z")]
    bundle = gh.collect_evidence(client, tmp_path, project_ids=["p"])
    assert bundle.evidence[0].source_id == "s"
    assert bundle.evidence[0].start_at == "2026-01-01T00:00:00Z"
    assert any(path == "project:p" for path, _ in client.calls)
    assert not any(path.endswith("/commits") for path, _ in client.calls)
    assert not client.writes


@pytest.mark.parametrize("status", ["revoked", "suggested"])
def test_project_source_policy_never_falls_back_to_repo_route(tmp_path, status):
    root = repo(tmp_path / "r")
    client = Client()
    client.sources["p"] = [source(status=status)]
    bundle = gh.collect_evidence(client, root, project_ids=["p"])
    assert not client.calls and not bundle.evidence and not client.writes
    assert status in bundle.prompt_text


def test_conflicting_existing_source_needs_review_and_does_not_patch(tmp_path):
    root = repo(tmp_path / "r")
    client = Client()
    client.sources["p"] = [source(ref="other")]
    bundle = gh.collect_evidence(client, root, project_ids=["p"])
    assert not client.calls and "local_source_conflict" in bundle.prompt_text


@pytest.mark.parametrize("access", ["public", "installation"])
def test_actual_access_path_not_connection_state_controls_evidence(tmp_path, access):
    root = repo(tmp_path / "r")
    client = Client()
    client.page["access"] = access
    bundle = gh.collect_evidence(client, root)
    assert bundle.evidence[0].access == access
    assert not any("repositories?q" in path for path, _ in client.calls)


def test_repeated_cursor_and_duplicate_sha_are_bounded(tmp_path):
    root = repo(tmp_path / "r")
    client = Client()
    client.page["cursor"] = "repeat"
    bundle = gh.collect_evidence(client, root)
    item = bundle.evidence[0]
    assert len(item.items) == 1 and item.reason == "repeated_cursor" and item.truncated
    assert len([p for p, _ in client.calls if p.endswith("/commits")]) == 2


def test_unavailable_or_unverified_history_never_becomes_chronology(tmp_path):
    root = repo(tmp_path / "r")
    client = Client()
    client.page.update(state="unavailable", bounds_verified=False, reason="bound_unresolved")
    item = gh.collect_evidence(client, root).evidence[0]
    assert not item.items and not item.details and item.reason == "bound_unresolved"


def test_context_budget_caps_large_provider_text(tmp_path):
    root = repo(tmp_path / "r")
    client = Client()
    client.page["items"][0]["subject"] = "界" * gh.MAX_CONTEXT_BYTES
    bundle = gh.collect_evidence(client, root)
    assert len(bundle.prompt_text.encode()) <= gh.MAX_CONTEXT_BYTES
    assert bundle.evidence[0].truncated and not bundle.evidence[0].items


def test_attach_lost_ack_reconciles_without_second_write(tmp_path):
    root = repo(tmp_path / "r")
    client = Client()
    bundle = gh.collect_evidence(client, root)
    original = client.attach_project_code_source

    def lost_ack(project, **kw):
        original(project, **kw)
        raise TimeoutError()

    client.attach_project_code_source = lost_ack
    assert gh.attach_reviewed_sources(client, "p", bundle)[0]["state"] == "reused"
    assert len(client.writes) == 1


def test_ambiguous_saved_start_bounds_block_project_free_fallback(tmp_path):
    root = repo(tmp_path / "r")
    client = Client()
    client.sources["p"] = [
        source(id="first", start_sha="1" * 40),
        source(id="second", start_sha="2" * 40),
    ]
    bundle = gh.collect_evidence(client, root, project_ids=["p"])
    assert not client.calls and not bundle.evidence
    assert "source_selection_required" in bundle.prompt_text
    bundle = gh.collect_evidence(client, root, project_ids=["p"], source_ids={"p": "second"})
    assert bundle.evidence[0].start_sha == "2" * 40
    assert any(
        path == "project:p" and params["source_id"] == "second" for path, params in client.calls
    )
    assert not any(path.endswith("/commits") for path, _ in client.calls)


def test_unique_exact_local_source_match_preserves_saved_bound(tmp_path):
    root = repo(tmp_path / "r")
    client = Client()
    client.sources["p"] = [
        source(id="first", start_sha="1" * 40),
        source(id="second", ref="other", start_sha="2" * 40),
    ]
    bundle = gh.collect_evidence(client, root, project_ids=["p"])
    assert bundle.evidence[0].source_id == "first"
    assert bundle.evidence[0].start_sha == "1" * 40
    assert not any(path.endswith("/commits") for path, _ in client.calls)


def test_invalid_explicit_source_id_cannot_fall_back_to_unbounded_repo(tmp_path):
    root = repo(tmp_path / "r")
    client = Client()
    client.sources["p"] = [source(start_sha="1" * 40)]
    bundle = gh.collect_evidence(client, root, project_ids=["p"], source_ids={"p": "absent"})
    assert not bundle.evidence and not client.calls


def test_source_listing_outage_stays_pending_without_attachment_write(tmp_path):
    root = repo(tmp_path / "r")
    client = Client()
    bundle = gh.collect_evidence(client, root)

    def unavailable(project):
        raise TimeoutError()

    client.list_project_code_sources = unavailable
    assert gh.attach_reviewed_sources(client, "p", bundle) == [
        {"repo": "acme/train", "state": "unavailable", "reason": "TimeoutError"}
    ]
    assert not client.writes


def test_attachment_and_reconciliation_outage_recovers_existing_source(tmp_path):
    root = repo(tmp_path / "r")
    client = Client()
    bundle = gh.collect_evidence(client, root)
    original_attach = client.attach_project_code_source
    original_list = client.list_project_code_sources

    def lost_ack(project, **kwargs):
        original_attach(project, **kwargs)
        raise TimeoutError()

    def unavailable_after_write(project):
        if client.writes:
            raise TimeoutError()
        return original_list(project)

    client.attach_project_code_source = lost_ack
    client.list_project_code_sources = unavailable_after_write
    assert gh.attach_reviewed_sources(client, "p", bundle)[0]["state"] == "unavailable"
    client.list_project_code_sources = original_list
    assert gh.attach_reviewed_sources(client, "p", bundle)[0]["state"] == "reused"
    assert len(client.writes) == 1
