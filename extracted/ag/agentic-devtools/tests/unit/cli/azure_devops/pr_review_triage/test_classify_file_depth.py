"""Tests for classify_file_depth."""

from agentic_devtools.cli.azure_devops.pr_review_triage import classify_file_depth

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


def _row(path, *, mode="diff", changed=5, **extra):
    base = {"normalizedPath": path, "reviewMode": mode, "changedLines": changed}
    base.update(extra)
    return base


class TestClassifyFileDepth:
    def test_trivial_mode_is_light(self):
        depth, reasons = classify_file_depth(_row("/src/a.py", mode="deleted"), _CONFIG)
        assert depth == "light"
        assert reasons == ["force-light:deleted"]

    def test_light_glob(self):
        depth, reasons = classify_file_depth(_row("/docs/readme.md"), _CONFIG)
        assert depth == "light"
        assert reasons == ["force-light:glob"]

    def test_deep_glob(self):
        depth, reasons = classify_file_depth(_row("/src/auth/login.py"), _CONFIG)
        assert depth == "deep"
        assert reasons == ["force-deep:glob"]

    def test_prior_needs_work(self):
        depth, reasons = classify_file_depth(_row("/src/a.py", priorStatus="needs-work"), _CONFIG)
        assert depth == "deep"
        assert reasons == ["force-deep:prior-needs-work"]

    def test_existing_threads(self):
        depth, reasons = classify_file_depth(_row("/src/a.py", existingThreadCount=3), _CONFIG)
        assert depth == "deep"
        assert reasons == ["force-deep:existing-threads"]

    def test_large_diff(self):
        depth, reasons = classify_file_depth(_row("/src/a.py", changed=25), _CONFIG)
        assert depth == "deep"
        assert reasons == ["force-deep:large-diff"]

    def test_default_deep(self):
        depth, reasons = classify_file_depth(_row("/src/a.py", changed=5), _CONFIG)
        assert depth == "deep"
        assert reasons == ["default:deep"]

    def test_default_light(self):
        config = {**_CONFIG, "defaultDepth": "light"}
        depth, reasons = classify_file_depth(_row("/src/a.py", changed=5), config)
        assert depth == "light"
        assert reasons == ["default:light"]
