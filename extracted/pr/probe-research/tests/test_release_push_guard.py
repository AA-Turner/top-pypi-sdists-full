"""Execute the real release push shell against isolated local Git remotes.

The artifact is built before a push retry can rebase the release commit. Every
tracked byte under agent/ must still match that original source, including files
outside the wheel, while unrelated backend/dashboard merges remain admissible.
"""

from __future__ import annotations

import os
from pathlib import Path
import subprocess

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github/workflows/release.yml"
TAG = "cli-v0.2.0"


def release_steps() -> tuple[str, str, list[dict]]:
    steps = yaml.safe_load(WORKFLOW.read_text())["jobs"]["build"]["steps"]
    pin = next(s for s in steps if s.get("name") == "Pin the release source before testing and building")
    push = next(s for s in steps if s.get("name") == "Push the release commit + tag(s) (workflow_dispatch)")
    return pin["run"], push["run"], steps


@pytest.fixture
def release_repo(tmp_path, monkeypatch):
    # Never mutate repository/global identity, including in these local fixtures.
    for key, value in {
        "GIT_AUTHOR_NAME": "Release fixture", "GIT_COMMITTER_NAME": "Release fixture",
        "GIT_AUTHOR_EMAIL": "fixture@example.invalid", "GIT_COMMITTER_EMAIL": "fixture@example.invalid",
        "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_SYSTEM": os.devnull,
        "GIT_CONFIG_NOSYSTEM": "1", "GIT_TERMINAL_PROMPT": "0",
    }.items():
        monkeypatch.setenv(key, value)

    def git(cwd, *args, check=True):
        return subprocess.run(["git", "-C", str(cwd), *args], check=check,
                              capture_output=True, text=True, timeout=15)

    def write(cwd, path, text):
        target = cwd / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)

    remote = tmp_path / "remote.git"
    subprocess.run(["git", "init", "--bare", "-q", str(remote)], check=True,
                   capture_output=True, timeout=15)
    writer = tmp_path / "writer"
    writer.mkdir()
    git(writer, "init", "--initial-branch=main", "-q")
    git(writer, "remote", "add", "origin", str(remote))
    for path in ("agent/src/probe/example.py", "agent/schema/openapi.json",
                 "agent/plugins/probe-research/skill.md", "agent/CHANGELOG.md",
                 "dashboard/example.ts", "app/example.py"):
        write(writer, path, "original\n")
    write(writer, "agent/pyproject.toml", 'version = "0.1.0"\n')
    git(writer, "add", ".")
    git(writer, "commit", "-qm", "fixture baseline")
    git(writer, "push", "-q", "origin", "HEAD:main")
    checkout = tmp_path / "release"
    subprocess.run(["git", "clone", "-q", "--branch", "main", str(remote), str(checkout)],
                   check=True, capture_output=True, timeout=15)
    write(checkout, "agent/pyproject.toml", 'version = "0.2.0"\n')
    git(checkout, "add", "agent/pyproject.toml")
    git(checkout, "commit", "-qm", "fixture release bump")
    tested = git(checkout, "rev-parse", "HEAD").stdout.strip()
    git(checkout, "tag", "-a", TAG, "-m", TAG)
    env_file = tmp_path / "github-env"
    subprocess.run(["bash", "-e", "-o", "pipefail", "-c", release_steps()[0]],
                   cwd=checkout, env={**os.environ, "GITHUB_ENV": str(env_file)},
                   check=True, capture_output=True, timeout=15)
    pinned = dict(line.split("=", 1) for line in env_file.read_text().splitlines())
    assert pinned == {"RELEASE_BUILD_COMMIT": tested}
    # A stand-in for already-built dist bytes, outside either checkout.
    artifact = tmp_path / "built-source"
    artifact.write_bytes((checkout / "agent/src/probe/example.py").read_bytes())

    def advance(path, change="edit"):
        if change == "delete":
            (writer / path).unlink()
        elif change == "mode":
            (writer / path).chmod(0o755)
        else:
            write(writer, path, "concurrent change\n")
        git(writer, "add", "-A")
        git(writer, "commit", "-qm", "fixture concurrent main")
        git(writer, "push", "-q", "origin", "HEAD:main")
        return git(remote, "rev-parse", "refs/heads/main").stdout.strip()

    def push(*, with_pin=True):
        # BOT_PUSH_URL is the prbe-release-bot app-token URL in CI; here it is
        # the same bare remote, so main and the tags land in one place.
        env = {**os.environ, "RELEASE_TAGS": TAG, "BOT_PUSH_URL": str(remote)}
        env.pop("RELEASE_BUILD_COMMIT", None)
        if with_pin:
            env.update(pinned)
        return subprocess.run(["bash", "-e", "-o", "pipefail", "-c", release_steps()[1]],
                              cwd=checkout, env=env, capture_output=True, text=True, timeout=30)

    return git, remote, checkout, tested, artifact, advance, push


# What every job that tests or packages the release must check out. The gate is
# sharded across runners (2026-09-12), so "the tested tree" is no longer whatever
# one job happened to have in its workspace -- it is one SHA, named once.
STAGED_SHA = "${{ needs.stage.outputs.test_sha }}"


def jobs() -> dict:
    return yaml.safe_load(WORKFLOW.read_text())["jobs"]


def checkout_ref(job: dict) -> str | None:
    step = next(s for s in job["steps"] if str(s.get("uses", "")).startswith("actions/checkout"))
    return (step.get("with") or {}).get("ref")


def test_release_source_is_pinned_before_the_test_and_build_gate():
    _, _, steps = release_steps()
    pin = next(i for i, s in enumerate(steps) if s.get("name") == "Pin the release source before testing and building")
    assert pin < next(i for i, s in enumerate(steps) if "python -m build" in s.get("run", ""))
    # Pin also applies to plugin-only dispatches; it is never repinned by retry.
    assert "if" not in steps[pin]
    # The gate moved out of this job entirely; the test below is what now keeps
    # the tested tree and the built tree the same tree.
    assert not [s for s in steps if "pytest" in str(s.get("run", ""))]


def test_every_job_that_tests_or_packages_uses_the_one_staged_commit():
    """A shard testing `main` while `build` packages the bump tests nothing.

    Sharding the gate put the tests on runners that cannot see the release
    commit, so it is parked on a throwaway branch and named by SHA. If any of
    these jobs drifts back to a branch ref -- `main`, or the staging branch by
    name, which is force-pushable -- the release is no longer gated on the bytes
    it publishes.
    """
    spec = jobs()
    testing = {
        name for name, job in spec.items()
        if any("pytest" in str(s.get("run", "")) for s in job.get("steps", []))
    }
    assert testing == {"gate"}, testing
    for name in sorted(testing | {"build"}):
        assert checkout_ref(spec[name]) == STAGED_SHA, f"{name} checks out {checkout_ref(spec[name])!r}"
    assert spec["stage"]["outputs"]["test_sha"] == "${{ steps.park.outputs.sha }}"


def test_main_is_written_by_exactly_one_step_and_staging_is_disposable():
    """Parking the commit early must not become a second door onto main."""
    spec = jobs()
    pushes = {
        (name, s.get("name") or str(s.get("run", ""))[:40])
        for name, job in spec.items()
        for s in job.get("steps", [])
        if "HEAD:main" in str(s.get("run", ""))
    }
    assert pushes == {("build", "Push the release commit + tag(s) (workflow_dispatch)")}, pushes

    park = next(s for s in spec["stage"]["steps"] if s.get("id") == "park")
    assert 'branch="release-staging/${{ github.run_id }}"' in park["run"]
    assert 'git push --force origin "HEAD:refs/heads/$branch"' in park["run"]
    # ...and it is deleted however the run ends, or every release leaks a branch.
    delete = next(s for s in spec["cleanup"]["steps"] if "push origin --delete" in str(s.get("run", "")))
    assert delete and spec["cleanup"]["if"].startswith("${{ always()")


def test_main_is_pushed_as_the_release_bot_and_tags_are_not():
    """main is protected (PR required) and the prbe-release-bot app is the
    ruleset's bypass actor; GITHUB_TOKEN's own app cannot be one in an org repo.
    Tags must stay on GITHUB_TOKEN: its pushes fire no workflows, so a cli-v*
    tag pushed here can never re-trigger this workflow's recovery path."""
    _, run, steps = release_steps()
    names = [s.get("name") for s in steps]
    mint = steps[names.index("Mint the prbe-release-bot token (workflow_dispatch)")]
    push = steps[names.index("Push the release commit + tag(s) (workflow_dispatch)")]
    assert mint["uses"].startswith("actions/create-github-app-token@")
    assert mint["with"] == {
        "app-id": "${{ secrets.RELEASE_BOT_APP_ID }}",
        "private-key": "${{ secrets.RELEASE_BOT_PRIVATE_KEY }}",
        "permission-contents": "write",
    }
    assert names.index(mint["name"]) < names.index(push["name"])
    assert push["env"]["BOT_PUSH_URL"] == (
        "https://x-access-token:${{ steps.bot.outputs.token }}@github.com/${{ github.repository }}.git"
    )
    assert 'push "$BOT_PUSH_URL" HEAD:main' in run
    assert "git push origin HEAD:main" not in run
    assert 'git push origin "$t"' in run


def test_the_release_commit_fires_no_push_workflows():
    """An app-token push fires push workflows (a GITHUB_TOKEN push does not).
    The release already ran its gate and calls mirror/release-notes itself."""
    stage = jobs()["stage"]["steps"]
    commit = next(s["run"] for s in stage if 'git commit -m "$MSG"' in str(s.get("run", "")))
    assert 'git commit -m "$MSG" -m "[skip ci]' in commit


def test_the_readme_agent_never_shares_a_runner_with_the_bot_token():
    """readme.yml's agent reads commit/PR text anyone can write. The token that
    may push past main's PR rule must never be on the runner the agent ran on: a
    hijacked agent could push itself, plant a git hook, or swap `git` for a
    later step. So the agent job is read-only with no persisted credential and
    never sees the bot's secrets; the token is minted only in a job with no
    agent in it, which publishes onto the commit the draft was written against."""
    spec = yaml.safe_load((ROOT / ".github/workflows/readme.yml").read_text())
    assert spec["permissions"] == {"contents": "read"}
    agent_markers = ("readme-updater", "claude-code-action")
    agent_jobs = []
    for name, job in spec["jobs"].items():
        steps = job.get("steps", [])
        uses = [str(s.get("uses", "")) for s in steps]
        has_agent = any(m in u for u in uses for m in agent_markers)
        mints = any(u.startswith("actions/create-github-app-token@") for u in uses)
        assert not (has_agent and mints), f"{name} runs the agent AND mints the bot token"
        if not has_agent:
            continue
        agent_jobs.append(name)
        assert "RELEASE_BOT" not in yaml.safe_dump(job), f"{name} can see the bot's secrets"
        assert (job.get("permissions") or {}).get("contents") == "read", name
        checkout = next(s for s in steps if str(s.get("uses", "")).startswith("actions/checkout"))
        assert checkout["with"].get("persist-credentials") is False, name
        assert checkout["with"].get("ref") == "main", f"{name} must draft from main"
        agent = next(s for s in steps if "readme-updater" in str(s.get("uses", "")))
        assert agent["with"].get("commit") == "false", name
    assert agent_jobs == ["draft"], agent_jobs
    publish = spec["jobs"]["publish"]
    checkout = next(s for s in publish["steps"] if str(s.get("uses", "")).startswith("actions/checkout"))
    assert checkout["with"]["ref"] == "${{ needs.draft.outputs.base_sha }}"
    mint = next(s for s in publish["steps"] if str(s.get("uses", "")).startswith("actions/create-github-app-token@"))
    assert mint["with"]["permission-contents"] == "write"


def test_agent_ci_runs_release_guards_for_workflow_only_changes():
    """A release.yml edit must still re-run the guards that assert about it.

    Narrowed from (push, pull_request) to push alone on 2026-09-21, when
    agent-ci lost its pull_request trigger -- the gates run once, on main, so
    `push` is now the only path this guard can travel. The assertion that
    matters is unchanged: whichever events this workflow DOES listen to must
    all cover release.yml, or a workflow-only change skips its own guards.
    """
    workflow = yaml.load(
        (ROOT / ".github/workflows/agent-ci.yml").read_text(), Loader=yaml.BaseLoader
    )
    triggers = {e for e in ("push", "pull_request") if e in workflow["on"]}
    assert triggers, "agent-ci must keep at least one path-filtered trigger"
    for event in triggers:
        assert ".github/workflows/release.yml" in workflow["on"][event]["paths"]


@pytest.mark.parametrize("path,change", [
    ("agent/src/probe/example.py", "edit"),
    ("agent/schema/openapi.json", "edit"),
    ("agent/plugins/probe-research/skill.md", "edit"),
    ("agent/CHANGELOG.md", "edit"),
    ("agent/new-file.txt", "add"),
    ("agent/src/probe/example.py", "delete"),
    ("agent/src/probe/example.py", "mode"),
])
def test_rebased_client_drift_refuses_before_remote_release_or_local_retag(release_repo, path, change):
    git, remote, checkout, tested, artifact, advance, push = release_repo
    concurrent = advance(path, change)
    result = push()
    assert result.returncode != 0
    assert "agent/ changed after the release test/build" in result.stdout
    assert git(remote, "rev-parse", "refs/heads/main").stdout.strip() == concurrent
    assert git(remote, "rev-parse", "--verify", "refs/tags/" + TAG, check=False).returncode != 0
    assert git(checkout, "rev-parse", TAG + "^{commit}").stdout.strip() == tested
    # The real rebase succeeded; refusal is the byte fence, not a merge conflict.
    assert git(checkout, "merge-base", "--is-ancestor", concurrent, "HEAD").returncode == 0
    assert artifact.read_bytes() == b"original\n"


@pytest.mark.parametrize("path", [None, "dashboard/example.ts", "app/example.py"])
def test_identical_client_source_allows_direct_push_or_unrelated_rebase(release_repo, path):
    git, remote, checkout, tested, artifact, advance, push = release_repo
    concurrent = advance(path) if path else None
    result = push()
    assert result.returncode == 0, result.stdout + result.stderr
    published = git(remote, "rev-parse", "refs/heads/main").stdout.strip()
    assert git(remote, "rev-parse", TAG + "^{commit}").stdout.strip() == published
    assert git(checkout, "rev-parse", "HEAD").stdout.strip() == published
    assert git(checkout, "diff", "--quiet", tested, published, "--", "agent/").returncode == 0
    if concurrent:
        assert git(checkout, "merge-base", "--is-ancestor", concurrent, published).returncode == 0
    assert (checkout / "agent/src/probe/example.py").read_bytes() == artifact.read_bytes()


def test_missing_original_source_pin_fails_before_any_push(release_repo):
    git, remote, _, _, _, _, push = release_repo
    before = git(remote, "rev-parse", "refs/heads/main").stdout.strip()
    result = push(with_pin=False)
    assert result.returncode != 0 and "missing tested release source" in result.stderr
    assert git(remote, "rev-parse", "refs/heads/main").stdout.strip() == before
    assert git(remote, "rev-parse", "--verify", "refs/tags/" + TAG, check=False).returncode != 0
