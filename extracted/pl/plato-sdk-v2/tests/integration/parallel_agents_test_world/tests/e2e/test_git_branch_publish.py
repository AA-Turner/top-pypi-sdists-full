"""E2E tests for branch-based git transport workflows on a real Chronos VM."""

from __future__ import annotations

import asyncio
import shutil
import tempfile
from pathlib import Path

from git import Git, Repo
from git.exc import GitCommandError

from plato.git_ops import GitOpRequest, run_remote_git_checked
from plato.transports import GitCheckout, GitSyncBack, GitTransport
from plato.worlds import AgentConfig


def _branch_agent_config(
    world,
    *,
    shared_mode: str,
    shared_path: str,
    duration_seconds: int = 1,
) -> AgentConfig:
    base = world.config.agent
    return AgentConfig(
        package=base.package,
        image=base.image,
        runtime=base.runtime,
        config={
            **base.config,
            "mode": "git_io",
            "workspace_dir": world.workspace("code").mount_path,
            "duration_seconds": duration_seconds,
            "file_count": 1,
            "file_size_kb": 1,
            "git_shared_mode": shared_mode,
            "git_shared_path": shared_path,
            "git_commit_before_exit": True,
        },
    )


async def test_git_feature_branch_checkout_and_publish(world) -> None:
    code_ws = world.workspace("code")
    transport = _git_transport(code_ws)
    await _reset_workspace(
        world,
        files={
            "shared.txt": "base\n",
            "feature-branch.txt": "seed\n",
        },
    )
    main_before = await _rev_parse(transport, "main")

    feature_ws = code_ws.for_git_agent(
        checkout=GitCheckout(ref="origin/main", branch_name="feature/test-checkout"),
        sync_back=GitSyncBack.push_branch("pr/test-checkout"),
    )
    observed: dict[str, str] = {}
    runner = world.agent(
        _branch_agent_config(
            world,
            shared_mode="append",
            shared_path="feature-branch.txt",
        ),
        display_name="branch-checkout",
        workspaces=[feature_ws],
    )
    runner.on_post_run(_capture_branch_state(world, observed, mount_path=feature_ws.mount_path))

    await runner.run("Write branch checkout test output")

    assert observed["branch"] == "feature/test-checkout"
    pr_ref = "refs/heads/pr/test-checkout"
    pr_head = await _rev_parse(transport, pr_ref)
    assert pr_head == observed["head"]
    assert await _rev_parse(transport, "main") == main_before
    assert (code_ws.path / "feature-branch.txt").read_text() == "seed\n"
    branch_shared = await _show_ref_file(transport, pr_ref, "feature-branch.txt")
    assert branch_shared.startswith("seed\n")
    assert "line from agent" in branch_shared


async def test_multiple_git_agents_publish_distinct_pr_branches(world) -> None:
    code_ws = world.workspace("code")
    transport = _git_transport(code_ws)
    await _reset_workspace(
        world,
        files={
            "shared.txt": "base\n",
            "branches/alpha.txt": "alpha-seed\n",
            "branches/beta.txt": "beta-seed\n",
        },
    )
    main_before = await _rev_parse(transport, "main")

    observed_alpha: dict[str, str] = {}
    observed_beta: dict[str, str] = {}

    alpha_ws = code_ws.for_git_agent(
        checkout=GitCheckout(ref="origin/main", branch_name="feature/alpha"),
        sync_back=GitSyncBack.push_branch("pr/alpha"),
    )
    beta_ws = code_ws.for_git_agent(
        checkout=GitCheckout(ref="origin/main", branch_name="feature/beta"),
        sync_back=GitSyncBack.push_branch("pr/beta"),
    )

    alpha_runner = world.agent(
        _branch_agent_config(
            world,
            shared_mode="append",
            shared_path="branches/alpha.txt",
        ),
        display_name="branch-alpha",
        workspaces=[alpha_ws],
    )
    alpha_runner.on_post_run(_capture_branch_state(world, observed_alpha, mount_path=alpha_ws.mount_path))

    beta_runner = world.agent(
        _branch_agent_config(
            world,
            shared_mode="append",
            shared_path="branches/beta.txt",
        ),
        display_name="branch-beta",
        workspaces=[beta_ws],
    )
    beta_runner.on_post_run(_capture_branch_state(world, observed_beta, mount_path=beta_ws.mount_path))

    await asyncio.gather(
        alpha_runner.run("Publish branch alpha"),
        beta_runner.run("Publish branch beta"),
    )

    alpha_ref = "refs/heads/pr/alpha"
    beta_ref = "refs/heads/pr/beta"
    assert observed_alpha["branch"] == "feature/alpha"
    assert observed_beta["branch"] == "feature/beta"
    assert await _rev_parse(transport, alpha_ref) == observed_alpha["head"]
    assert await _rev_parse(transport, beta_ref) == observed_beta["head"]
    assert await _rev_parse(transport, "main") == main_before
    assert alpha_ref != beta_ref
    assert await _show_ref_file(transport, alpha_ref, "branches/alpha.txt") != "alpha-seed\n"
    assert await _show_ref_file(transport, beta_ref, "branches/beta.txt") != "beta-seed\n"


async def test_pr_branches_require_explicit_merge_resolution(world) -> None:
    code_ws = world.workspace("code")
    transport = _git_transport(code_ws)
    await _reset_workspace(
        world,
        files={
            "shared.txt": "base\n",
        },
    )

    branch_a_ws = code_ws.for_git_agent(
        checkout=GitCheckout(ref="origin/main", branch_name="feature/conflict-a"),
        sync_back=GitSyncBack.push_branch("pr/conflict-a"),
    )
    branch_b_ws = code_ws.for_git_agent(
        checkout=GitCheckout(ref="origin/main", branch_name="feature/conflict-b"),
        sync_back=GitSyncBack.push_branch("pr/conflict-b"),
    )

    await asyncio.gather(
        world.agent(
            _branch_agent_config(
                world,
                shared_mode="replace",
                shared_path="shared.txt",
            ),
            display_name="conflict-a",
            workspaces=[branch_a_ws],
        ).run("Create branch conflict A"),
        world.agent(
            _branch_agent_config(
                world,
                shared_mode="replace",
                shared_path="shared.txt",
            ),
            display_name="conflict-b",
            workspaces=[branch_b_ws],
        ).run("Create branch conflict B"),
    )

    branch_a_content = await _show_ref_file(transport, "refs/heads/pr/conflict-a", "shared.txt")
    branch_b_content = await _show_ref_file(transport, "refs/heads/pr/conflict-b", "shared.txt")

    conflicted = await _merge_branch_into_main(transport, "pr/conflict-a")
    assert conflicted is False

    conflicted = await _merge_branch_into_main(
        transport,
        "pr/conflict-b",
        resolved_files={
            "shared.txt": _merge_unique_lines(branch_a_content, branch_b_content),
        },
    )
    assert conflicted is True

    main_content = await _show_ref_file(transport, "main", "shared.txt")
    assert main_content == _merge_unique_lines(branch_a_content, branch_b_content)


async def _reset_workspace(world, *, files: dict[str, str]) -> None:
    code_ws = world.workspace("code")
    code_path = Path(code_ws.path)

    for path in code_path.glob("git-agent-*"):
        if path.is_dir():
            shutil.rmtree(path)

    for relpath, content in files.items():
        target = code_path / relpath
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)

    transport = _git_transport(code_ws)
    await transport.update_bare_repo("Reset git branch publish e2e workspace")


def _git_transport(workspace) -> GitTransport:
    transport = workspace.transport
    assert isinstance(transport, GitTransport)
    return transport


def _trust_git_directory(path: Path) -> None:
    Git().config("--global", "--add", "safe.directory", str(path.resolve()))


def _capture_branch_state(world, observed: dict[str, str], *, mount_path: str):
    async def _hook(prepared) -> None:
        ssh_key_path = world._ssh_key_path
        assert ssh_key_path is not None
        payload = await run_remote_git_checked(
            ssh_key_path,
            prepared.hostname,
            GitOpRequest.current_head_info(mount_path),
            timeout=30,
            error_context=f"Failed to capture git branch state on {prepared.hostname}",
        )
        observed["branch"] = payload.branch or ""
        observed["head"] = payload.head or ""

    return _hook


async def _rev_parse(transport: GitTransport, ref: str) -> str:
    _trust_git_directory(Path(transport.bare_repo_path))
    repo = Repo(transport.bare_repo_path)
    return repo.commit(ref).hexsha


async def _show_ref_file(transport: GitTransport, ref: str, relpath: str) -> str:
    _trust_git_directory(Path(transport.bare_repo_path))
    repo = Repo(transport.bare_repo_path)
    blob = repo.commit(ref).tree / relpath
    return blob.data_stream.read().decode()


async def _merge_branch_into_main(
    transport: GitTransport,
    branch_name: str,
    *,
    resolved_files: dict[str, str] | None = None,
) -> bool:
    with tempfile.TemporaryDirectory(prefix="git-branch-merge-") as tmpdir:
        clone_dir = Path(tmpdir)
        repo = Repo.clone_from(transport.bare_repo_path, clone_dir)
        _trust_git_directory(clone_dir)
        with repo.config_writer() as config:
            config.set_value("user", "email", "plato@plato.dev")
            config.set_value("user", "name", "Plato")

        try:
            repo.git.merge(f"origin/{branch_name}", m=f"Merge {branch_name}")
            merge_conflicted = False
        except GitCommandError:
            merge_conflicted = True
            assert resolved_files is not None
            for relpath, content in resolved_files.items():
                target = clone_dir / relpath
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content)
            repo.git.add(A=True)
            repo.index.commit(f"Resolve {branch_name} merge")

        repo.remote("origin").push(refspec="HEAD:main")
        return merge_conflicted


def _merge_unique_lines(*contents: str) -> str:
    ordered_lines: list[str] = []
    seen: set[str] = set()
    for content in contents:
        for line in content.splitlines():
            if line not in seen:
                ordered_lines.append(line)
                seen.add(line)
    return "\n".join(ordered_lines) + "\n"
