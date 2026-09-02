"""Tests for triage_manifest."""

from agentic_devtools.cli.azure_devops.pr_review_triage import triage_manifest

_CONFIG = {
    "enabled": True,
    "defaultDepth": "deep",
    "deepGlobs": ["**/auth/**", "**/*.sql"],
    "lightGlobs": ["**/*.md", "**/*.lock"],
    "minDiffLinesForDeep": 20,
    "maxDeepModelCalls": 30,
    "maxDeepTotalChangedLines": 2000,
    "maxReviewMinutes": 60,
}


def _row(key, path, *, mode="diff", changed=5):
    return {"fileKey": key, "normalizedPath": path, "reviewMode": mode, "changedLines": changed}


class TestTriageManifest:
    def test_classifies_and_summarizes(self):
        manifest = {
            "files": [
                _row("a", "/src/auth/login.py"),
                _row("b", "/docs/readme.md"),
            ]
        }
        triage_manifest(manifest, _CONFIG)
        assert manifest["files"][0]["reviewDepth"] == "deep"
        assert manifest["files"][0]["reviewDepthReasons"] == ["force-deep:glob"]
        assert manifest["files"][1]["reviewDepth"] == "light"
        assert manifest["triage"]["enabled"] is True
        assert manifest["triage"]["deepCount"] == 1
        assert manifest["triage"]["lightCount"] == 1
        assert manifest["triage"]["caps"]["maxDeepModelCalls"] == 30

    def test_disabled_marks_all_default_depth(self):
        manifest = {"files": [_row("a", "/src/a.py")]}
        config = {**_CONFIG, "enabled": False, "defaultDepth": "deep"}
        triage_manifest(manifest, config)
        assert manifest["files"][0]["reviewDepth"] == "deep"
        assert manifest["files"][0]["reviewDepthReasons"] == ["triage-disabled"]
        assert manifest["triage"]["enabled"] is False
        assert manifest["triage"]["deepCount"] == 1
        assert manifest["triage"]["demotions"] == []

    def test_demotion_recorded(self):
        files = [_row(f"f{i}", f"/src/x{i}.py", changed=25) for i in range(5)]
        manifest = {"files": files}
        config = {**_CONFIG, "maxDeepModelCalls": 6}
        triage_manifest(manifest, config)
        assert len(manifest["triage"]["demotions"]) == 3
        deep = [f for f in files if f["reviewDepth"] == "deep"]
        assert len(deep) == 2
