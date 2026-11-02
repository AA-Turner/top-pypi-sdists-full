"""Tests for derive_clusters."""

from agentic_devtools.cli.azure_devops.pr_review_filekey import build_file_key
from agentic_devtools.cli.azure_devops.pr_review_manifest import derive_clusters


def _entry(path: str, lines: list[str] | None = None, *, normalized: str | None = None) -> dict:
    norm = normalized if normalized is not None else path
    return {
        "fileKey": build_file_key(path),
        "path": path,
        "normalizedPath": norm,
        "addedTextLines": lines or [],
    }


class TestDeriveClusters:
    def test_empty_input(self):
        assert derive_clusters([]) == []

    def test_source_then_test_uses_elif_branch(self):
        clusters = derive_clusters([_entry("/src/state.py"), _entry("/tests/test_state.py")])
        assert len(clusters) == 1
        assert clusters[0]["reasons"] == ["test"]
        assert clusters[0]["id"] == "cluster-1"
        assert len(clusters[0]["members"]) == 2

    def test_test_then_source_uses_first_branch(self):
        clusters = derive_clusters([_entry("/tests/test_state.py"), _entry("/src/state.py")])
        assert len(clusters) == 1
        assert clusters[0]["reasons"] == ["test"]

    def test_marker_based_test_stems(self):
        for source, test in (
            ("/a.ts", "/a.test.ts"),
            ("/b.ts", "/b.spec.ts"),
            ("/c.py", "/c_test.py"),
            ("/d.js", "/d-test.js"),
            ("/e.ts", "/e.steps.ts"),
        ):
            clusters = derive_clusters([_entry(source), _entry(test)])
            assert len(clusters) == 1, f"{source} <-> {test}"
            assert clusters[0]["reasons"] == ["test"]

    def test_schema_left_pairs_same_folder(self):
        clusters = derive_clusters([_entry("/db/schema.sql"), _entry("/db/model.py")])
        assert len(clusters) == 1
        assert clusters[0]["reasons"] == ["schema"]

    def test_schema_right_pairs_same_folder(self):
        clusters = derive_clusters([_entry("/db/model.py"), _entry("/db/0001.sql")])
        assert len(clusters) == 1
        assert clusters[0]["reasons"] == ["schema"]

    def test_immigration_name_does_not_trigger_schema_cluster(self):
        clusters = derive_clusters([_entry("/src/immigration_policy.py"), _entry("/src/handlers.py")])
        assert clusters == []

    def test_import_edge_from_import(self):
        clusters = derive_clusters([_entry("/pkg/a.py", ["from b import x"]), _entry("/pkg/b.py")])
        assert len(clusters) == 1
        assert clusters[0]["reasons"] == ["import"]

    def test_import_edge_plain_import_and_js(self):
        clusters = derive_clusters(
            [
                _entry("/pkg/a.py", ["import b"]),
                _entry("/pkg/b.py"),
                _entry("/web/c.ts", ["import x from './d'"]),
                _entry("/web/d.ts"),
            ]
        )
        reasons = {tuple(c["paths"]): c["reasons"] for c in clusters}
        assert reasons[("/pkg/a.py", "/pkg/b.py")] == ["import"]
        assert reasons[("/web/c.ts", "/web/d.ts")] == ["import"]

    def test_import_edge_right_imports_left_uses_elif(self):
        clusters = derive_clusters([_entry("/pkg/b.py"), _entry("/pkg/a.py", ["from b import x"])])
        assert len(clusters) == 1
        assert clusters[0]["reasons"] == ["import"]

    def test_duplicate_file_key_self_edge_guarded(self):
        same = _entry("/pkg/a.py", ["from a import x"])
        clusters = derive_clusters([same, dict(same)])
        # Same key on both sides → self-edge guarded → no real cluster emitted.
        assert clusters == []

    def test_triangle_covers_union_skip_and_find_chain(self):
        clusters = derive_clusters(
            [
                _entry("/p/a.py", ["from b import x", "from c import y"]),
                _entry("/p/b.py", ["from c import z"]),
                _entry("/p/c.py"),
            ]
        )
        assert len(clusters) == 1
        assert clusters[0]["reasons"] == ["import"]
        assert len(clusters[0]["members"]) == 3

    def test_singleton_not_emitted(self):
        assert derive_clusters([_entry("/x/lonely.py")]) == []

    def test_empty_normalized_path_yields_no_tokens(self):
        entries = [
            _entry("/src/a.py", ["from b import x"]),
            {"fileKey": "empty-0000", "path": "", "normalizedPath": "", "addedTextLines": []},
        ]
        assert derive_clusters(entries) == []

    def test_relative_dot_import_target_filtered(self):
        # `from '.'` yields a "." leaf which must be filtered out (no edge).
        clusters = derive_clusters(
            [
                _entry("/web/a.ts", ["export x from '.'"]),
                _entry("/web/b.ts"),
            ]
        )
        assert clusters == []

    def test_relative_python_import_yields_no_tokens(self):
        # `from . import b` → module ".", empty split parts → no import tokens → no edge.
        clusters = derive_clusters(
            [
                _entry("/pkg/a.py", ["from . import b"]),
                _entry("/pkg/b.py"),
            ]
        )
        assert clusters == []

    def test_multiple_reasons_aggregated(self):
        # Source + its test + an importer of the source share one cluster.
        clusters = derive_clusters(
            [
                _entry("/pkg/state.py"),
                _entry("/tests/test_state.py"),
                _entry("/pkg/user.py", ["from state import load"]),
            ]
        )
        assert len(clusters) == 1
        assert clusters[0]["reasons"] == ["import", "test"]
        assert len(clusters[0]["members"]) == 3

    def test_js_import_from_word_boundary_no_false_positive(self):
        # A JS identifier that contains 'from' as a substring (e.g. 'datafrom')
        # must not generate a false import token, even when followed by a quoted
        # string ('utils').  The \bfrom\b word boundary in _JS_IMPORT_RE prevents
        # the match because 'a' immediately precedes 'f' in 'datafrom'.
        clusters = derive_clusters(
            [
                _entry("/web/a.ts", ["const x = datafrom('utils')"]),
                _entry("/web/utils.ts"),
            ]
        )
        assert clusters == []
