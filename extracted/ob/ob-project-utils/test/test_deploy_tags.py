# Unit tests for the deployment-tag plumbing in deploy/deploy_obproject.py.
#
# Run:
#   python -m pytest test/test_deploy_tags.py -v
# or:
#   python test/test_deploy_tags.py
#
# These tests are pure-Python (no network, no git push, no cluster). They
# monkeypatch os.environ and the cached CI handler globals to exercise each
# CI provider independently.

import os
import sys
import subprocess
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import deploy.deploy_obproject as deploy_mod
from deploy.deploy_obproject import (
    compute_auto_tags,
    _deploy_tags_enabled,
    GitHubEnvironment,
    AzureDevOpsEnvironment,
    GitLabEnvironment,
    CircleCIEnvironment,
)


# Every test must clear cached CI detection so monkeypatched env vars are
# re-evaluated. The module caches the result in two module-level globals.
def _reset_ci_cache():
    deploy_mod._CI_ENV = None
    deploy_mod._CI_HANDLER = None


# A predictable SHA used in place of `git rev-parse HEAD` in tests where we
# don't want to depend on the real git state of the test checkout.
FAKE_LOCAL_SHA = "0000000000000000000000000000000000000000"


def _patched_env(env):
    """Replace os.environ entirely with the given dict for the test scope."""
    return patch.dict(os.environ, env, clear=True)


# ---------------------------------------------------------------------------
# get_commits() per provider
# ---------------------------------------------------------------------------

def test_github_push_event_uses_github_sha_as_source():
    env = {"GITHUB_ACTIONS": "true", "GITHUB_SHA": "deadbeef", "GITHUB_EVENT_NAME": "push"}
    with _patched_env(env):
        commits = GitHubEnvironment.get_commits()
    assert commits == {"source": "deadbeef", "merge": None}


def test_github_pr_event_distinguishes_source_and_merge():
    env = {
        "GITHUB_ACTIONS": "true",
        "GITHUB_SHA": "mergesha",
        "GITHUB_EVENT_NAME": "pull_request",
    }
    with _patched_env(env), patch.object(deploy_mod, "_git_head_sha", return_value="sourcesha"):
        commits = GitHubEnvironment.get_commits()
    assert commits == {"source": "sourcesha", "merge": "mergesha"}


def test_github_pr_event_collapses_when_head_and_merge_match():
    # If the workflow didn't checkout the PR head sha, git HEAD == GITHUB_SHA.
    # We must not emit a redundant merge-commit-hash tag in this case.
    env = {
        "GITHUB_ACTIONS": "true",
        "GITHUB_SHA": "samesha",
        "GITHUB_EVENT_NAME": "pull_request",
    }
    with _patched_env(env), patch.object(deploy_mod, "_git_head_sha", return_value="samesha"):
        commits = GitHubEnvironment.get_commits()
    assert commits == {"source": "samesha", "merge": None}


def test_azure_pr_distinguishes_source_and_merge():
    env = {
        "SYSTEM_COLLECTIONURI": "https://dev.azure.com/foo/",
        "BUILD_SOURCEVERSION": "mergesha",
        "SYSTEM_PULLREQUEST_SOURCECOMMITID": "sourcesha",
    }
    with _patched_env(env):
        commits = AzureDevOpsEnvironment.get_commits()
    assert commits == {"source": "sourcesha", "merge": "mergesha"}


def test_azure_push_uses_build_sourceversion():
    env = {
        "SYSTEM_COLLECTIONURI": "https://dev.azure.com/foo/",
        "BUILD_SOURCEVERSION": "pushsha",
    }
    with _patched_env(env):
        commits = AzureDevOpsEnvironment.get_commits()
    assert commits == {"source": "pushsha", "merge": None}


def test_gitlab_merged_results_distinguishes_source_and_merge():
    env = {
        "GITLAB_CI": "true",
        "CI_COMMIT_SHA": "mergesha",
        "CI_MERGE_REQUEST_SOURCE_BRANCH_SHA": "sourcesha",
    }
    with _patched_env(env):
        commits = GitLabEnvironment.get_commits()
    assert commits == {"source": "sourcesha", "merge": "mergesha"}


def test_gitlab_regular_pipeline_uses_commit_sha():
    env = {"GITLAB_CI": "true", "CI_COMMIT_SHA": "pushsha"}
    with _patched_env(env):
        commits = GitLabEnvironment.get_commits()
    assert commits == {"source": "pushsha", "merge": None}


def test_circleci_uses_circle_sha1_no_merge_concept():
    env = {"CIRCLECI": "true", "CIRCLE_SHA1": "circlesha"}
    with _patched_env(env):
        commits = CircleCIEnvironment.get_commits()
    assert commits == {"source": "circlesha", "merge": None}


# ---------------------------------------------------------------------------
# get_run_id() per provider
# ---------------------------------------------------------------------------

def test_run_ids_per_provider():
    cases = [
        (GitHubEnvironment, {"GITHUB_ACTIONS": "true", "GITHUB_RUN_ID": "1001"}, "1001"),
        (
            AzureDevOpsEnvironment,
            {"SYSTEM_COLLECTIONURI": "https://x/", "BUILD_BUILDID": "2002"},
            "2002",
        ),
        (GitLabEnvironment, {"GITLAB_CI": "true", "CI_PIPELINE_ID": "3003"}, "3003"),
        (CircleCIEnvironment, {"CIRCLECI": "true", "CIRCLE_BUILD_NUM": "4004"}, "4004"),
    ]
    for cls, env, expected in cases:
        with _patched_env(env):
            assert cls.get_run_id() == expected, f"{cls.__name__} run id"


def test_run_id_missing_returns_none():
    with _patched_env({"GITHUB_ACTIONS": "true"}):
        assert GitHubEnvironment.get_run_id() is None


# ---------------------------------------------------------------------------
# compute_auto_tags() end-to-end across detection + handler
# ---------------------------------------------------------------------------

def test_compute_auto_tags_github_pr():
    env = {
        "GITHUB_ACTIONS": "true",
        "GITHUB_SHA": "mergesha",
        "GITHUB_EVENT_NAME": "pull_request",
        "GITHUB_RUN_ID": "42",
    }
    _reset_ci_cache()
    with _patched_env(env), patch.object(deploy_mod, "_git_head_sha", return_value="sourcesha"):
        tags = compute_auto_tags()
    assert tags == [
        "commit-hash:sourcesha",
        "merge-commit-hash:mergesha",
        "obproject-deploy-gh-action-run:42",
    ]


def test_compute_auto_tags_azure_push():
    env = {
        "SYSTEM_COLLECTIONURI": "https://dev.azure.com/foo/",
        "BUILD_SOURCEVERSION": "pushsha",
        "BUILD_BUILDID": "777",
    }
    _reset_ci_cache()
    with _patched_env(env):
        tags = compute_auto_tags()
    assert tags == ["commit-hash:pushsha", "obproject-deploy-azure-pipeline-run:777"]


def test_compute_auto_tags_gitlab_mr():
    env = {
        "GITLAB_CI": "true",
        "CI_COMMIT_SHA": "mergesha",
        "CI_MERGE_REQUEST_SOURCE_BRANCH_SHA": "sourcesha",
        "CI_PIPELINE_ID": "99",
    }
    _reset_ci_cache()
    with _patched_env(env):
        tags = compute_auto_tags()
    assert tags == [
        "commit-hash:sourcesha",
        "merge-commit-hash:mergesha",
        "obproject-deploy-gitlab-pipeline-run:99",
    ]


def test_compute_auto_tags_circleci():
    env = {"CIRCLECI": "true", "CIRCLE_SHA1": "circlesha", "CIRCLE_BUILD_NUM": "5"}
    _reset_ci_cache()
    with _patched_env(env):
        tags = compute_auto_tags()
    assert tags == ["commit-hash:circlesha", "obproject-deploy-circleci-run:5"]


def test_compute_auto_tags_local_no_ci():
    _reset_ci_cache()
    with _patched_env({}), patch.object(deploy_mod, "_git_head_sha", return_value=FAKE_LOCAL_SHA):
        tags = compute_auto_tags()
    assert tags == [f"commit-hash:{FAKE_LOCAL_SHA}"]


def test_compute_auto_tags_git_failure_returns_empty_in_local():
    _reset_ci_cache()
    with _patched_env({}), patch.object(deploy_mod, "_git_head_sha", return_value=None):
        tags = compute_auto_tags()
    assert tags == []


def test_git_head_sha_swallows_subprocess_errors():
    # Real subprocess call: simulate a failure (file not found, non-git cwd, etc.).
    def boom(*args, **kwargs):
        raise subprocess.CalledProcessError(1, args)

    with patch("deploy.deploy_obproject.subprocess.run", side_effect=boom):
        assert deploy_mod._git_head_sha() is None


# ---------------------------------------------------------------------------
# _deploy_tags_enabled() config parsing
# ---------------------------------------------------------------------------

def test_deploy_tags_enabled_default_true_when_no_config():
    assert _deploy_tags_enabled({}) is True
    assert _deploy_tags_enabled({"deploy": {}}) is True
    assert _deploy_tags_enabled({"deploy": {"tags": {}}}) is True


def test_deploy_tags_enabled_false_when_explicit():
    conf = {"deploy": {"tags": {"auto": False}}}
    assert _deploy_tags_enabled(conf) is False


def test_deploy_tags_enabled_true_when_explicit():
    conf = {"deploy": {"tags": {"auto": True}}}
    assert _deploy_tags_enabled(conf) is True


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    tests = [
        test_github_push_event_uses_github_sha_as_source,
        test_github_pr_event_distinguishes_source_and_merge,
        test_github_pr_event_collapses_when_head_and_merge_match,
        test_azure_pr_distinguishes_source_and_merge,
        test_azure_push_uses_build_sourceversion,
        test_gitlab_merged_results_distinguishes_source_and_merge,
        test_gitlab_regular_pipeline_uses_commit_sha,
        test_circleci_uses_circle_sha1_no_merge_concept,
        test_run_ids_per_provider,
        test_run_id_missing_returns_none,
        test_compute_auto_tags_github_pr,
        test_compute_auto_tags_azure_push,
        test_compute_auto_tags_gitlab_mr,
        test_compute_auto_tags_circleci,
        test_compute_auto_tags_local_no_ci,
        test_compute_auto_tags_git_failure_returns_empty_in_local,
        test_git_head_sha_swallows_subprocess_errors,
        test_deploy_tags_enabled_default_true_when_no_config,
        test_deploy_tags_enabled_false_when_explicit,
        test_deploy_tags_enabled_true_when_explicit,
    ]
    for t in tests:
        t()
        print(f"PASS: {t.__name__}")
    print(f"\nAll {len(tests)} tests passed.")
