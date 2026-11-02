"""Tests for render_pr_context (budget degradation chain)."""

from agentic_devtools.cli.azure_devops.pr_review_manifest import (
    _partition_rows,
    _render_context,
    render_pr_context,
)


def _row(key, path, *, risk=False, depth=None, hint="edits file.py"):
    return {
        "fileKey": key,
        "normalizedPath": path,
        "changeType": "edit",
        "addedLines": 3,
        "removedLines": 1,
        "reviewMode": "diff",
        "riskFlag": risk,
        "reviewDepth": depth,
        "purposeHint": hint,
        "promptFile": f"{key}.md",
    }


def _mixed_manifest():
    rows = [_row("risk-0", "/src/auth.py", risk=True)]
    rows += [_row(f"low-{i}", f"/src/f{i}.py") for i in range(8)]
    return {
        "meta": {"prTitle": "Mixed", "jiraKey": "J-1", "prSummary": "summary", "focusAreas": "FA"},
        "pullRequestId": 1,
        "files": rows,
        "clusters": [{"id": "cluster-1", "reasons": ["test"], "paths": ["/src/auth.py", "/src/f0.py"]}],
    }


def _all_risk_manifest():
    rows = [_row("deep-0", "/src/a.py", risk=True, depth="deep", hint="short")]
    rows += [
        _row(f"deep-{i}", f"/src/m{i}.py", risk=True, depth="deep", hint="a very long purpose hint " * 3)
        for i in range(1, 6)
    ]
    return {"meta": {}, "pullRequestId": 2, "files": rows, "clusters": []}


class TestRenderPrContext:
    def test_passthrough(self):
        manifest = _mixed_manifest()
        full = _render_context(
            manifest["meta"], 1, manifest["files"], 0, manifest["clusters"], hint_chars=None, links_only=False
        )
        text, info = render_pr_context(manifest, len(full))
        assert info["stage"] == "passthrough"
        assert info["finalChars"] == info["fullChars"] == len(full)
        assert text == full

    def test_collapse_light(self):
        manifest = _mixed_manifest()
        full = _render_context(
            manifest["meta"], 1, manifest["files"], 0, manifest["clusters"], hint_chars=None, links_only=False
        )
        _text, info = render_pr_context(manifest, len(full) - 1)
        assert info["stage"] == "collapse-light"
        assert info["degradations"] == ["collapse-light"]
        assert info["finalChars"] <= len(full) - 1

    def test_shorten_hints(self):
        manifest = _all_risk_manifest()
        full = _render_context(
            manifest["meta"], 2, manifest["files"], 0, manifest["clusters"], hint_chars=None, links_only=False
        )
        _text, info = render_pr_context(manifest, len(full) - 1)
        assert info["stage"] == "shorten-hints"
        assert info["degradations"] == ["collapse-light", "shorten-hints"]

    def test_links_only(self):
        manifest = _all_risk_manifest()
        kept, collapsed = _partition_rows(manifest["files"])
        shortened = _render_context(
            manifest["meta"], 2, kept, collapsed, manifest["clusters"], hint_chars=24, links_only=False
        )
        _text, info = render_pr_context(manifest, len(shortened) - 1)
        assert info["stage"] == "links-only"
        assert info["degradations"][-1] == "links-only"

    def test_truncated(self):
        manifest = _all_risk_manifest()
        kept, collapsed = _partition_rows(manifest["files"])
        links = _render_context(
            manifest["meta"], 2, kept, collapsed, manifest["clusters"], hint_chars=0, links_only=True
        )
        text, info = render_pr_context(manifest, len(links) - 1)
        assert info["stage"] == "truncated"
        assert info["degradations"][-1] == "truncated"
        assert len(text) <= len(links) - 1

    def test_empty_meta_and_no_clusters(self):
        manifest = {"meta": {}, "pullRequestId": 5, "files": [_row("k", "/a.py")], "clusters": []}
        text, info = render_pr_context(manifest, 10_000)
        assert info["stage"] == "passthrough"
        assert "# PR Review Context — PR 5" in text
        assert "## Clusters" not in text

    def test_partition_rows_branches(self):
        risk = _row("r", "/a.py", risk=True)
        deep = _row("d", "/b.py", risk=False, depth="deep")
        light = _row("l", "/c.py", risk=False, depth=None)
        kept, collapsed = _partition_rows([risk, deep, light])
        assert kept == [risk, deep]
        assert collapsed == 1

    def test_partition_rows_all_collapsible_keeps_first(self):
        rows = [_row("l1", "/a.py"), _row("l2", "/b.py"), _row("l3", "/c.py")]
        kept, collapsed = _partition_rows(rows)
        assert len(kept) == 1
        assert kept[0] is rows[0]
        assert collapsed == 2

    def test_collapse_light_on_all_collapsible_manifest(self):
        rows = [_row(f"l{i}", f"/src/f{i}.py") for i in range(12)]
        manifest = {"meta": {}, "pullRequestId": 7, "files": rows, "clusters": []}
        full = _render_context(manifest["meta"], 7, rows, 0, [], hint_chars=None, links_only=False)
        _text, info = render_pr_context(manifest, len(full) - 1)
        assert info["stage"] == "collapse-light"
