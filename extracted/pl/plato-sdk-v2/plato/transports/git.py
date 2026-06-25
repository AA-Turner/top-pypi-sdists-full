"""Git-based workspace transport implementation."""

from __future__ import annotations

import asyncio
import hashlib
import logging
import shlex
import shutil
import time as _time
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from git import Actor, Repo

from plato.git_ops import (
    GitOpRequest,
    checkout_main_from_bare,
    ensure_remote_git_server,
    run_remote_git_checked,
    run_remote_git_op,
    trust_git_directory,
)
from plato.markers import WorkspaceMarker
from plato.transports.base import Transport, build_auditctl_commands
from plato.utils.subprocess import run_local, run_ssh

if TYPE_CHECKING:
    from plato.agents.mounts import AgentWorkspaceMount
    from plato.v2.async_.environment import Environment
    from plato.worlds.config import GitTransportConfig, MergeAgentConfig

logger = logging.getLogger(__name__)
_PLATO_ACTOR = Actor("Plato", "plato@plato.dev")
_AGENT_ACTOR = Actor("Plato Agent", "agent@plato.dev")


class GitPushConflict(RuntimeError):
    """Raised when a git push loses a race and the caller should resolve it centrally."""

    def __init__(self, *, commit_sha: str, conflict_ref: str) -> None:
        super().__init__(f"Git push conflict for commit {commit_sha}")
        self.commit_sha = commit_sha
        self.conflict_ref = conflict_ref


@dataclass(slots=True)
class GitPublishedRef:
    """Published hidden ref produced by a git transport sync."""

    commit_sha: str
    ref: str


class GitTransport(Transport):
    """Transport via git clone/push over SSH."""

    def __init__(
        self,
        path: str,
        world_vm_ip: str,
        ssh_key_path: Path,
        mount_path: str | None = None,
        git_config: GitTransportConfig | None = None,
        raise_on_conflict: bool = False,
    ) -> None:
        self.path = path
        self.world_vm_ip = world_vm_ip
        self.ssh_key_path = ssh_key_path
        self.mount_path = mount_path
        # Active object store lives on local VM disk, OFF the FUSE workspace
        # mount. Persistence is a packed snapshot at ``_mirror_repo_path``
        # (inside the FUSE mount, so the normal workspace checkpoint ships it
        # to S3). See ``_init_bare_repo`` / ``snapshot_to_mirror``.
        self._bare_repo_path = self._local_bare_path(path)
        self._mirror_repo_path = f"{path}/.git-bare"
        self._raise_on_conflict = raise_on_conflict
        self._published_ref: GitPublishedRef | None = None
        if git_config is None:
            from plato.worlds.config import GitTransportConfig as _GitTransportConfig

            git_config = _GitTransportConfig()
        self._git_config = git_config
        self._merge_resolver: Callable[[str, Path, str, list[str]], Awaitable[None]] | None = None
        self._sync_lock = asyncio.Lock() if self._git_config.serialize_sync else None

    @staticmethod
    def _local_bare_path(workspace_path: str) -> str:
        """Local-disk path for the active bare, keyed by the workspace path.

        Deterministic in ``workspace_path`` so the same workspace resolves to
        the same local bare across sessions on a given VM (the path is stable;
        the contents are rehydrated from the persisted mirror on resume).
        """
        digest = hashlib.sha1(workspace_path.encode("utf-8")).hexdigest()[:16]
        return f"/tmp/plato-git/{digest}/.git-bare"

    @property
    def bare_repo_path(self) -> str:
        """Active bare on local VM disk — what agents clone/push and what
        checkout/publish operate against."""
        return self._bare_repo_path

    @property
    def mirror_repo_path(self) -> str:
        """Persisted packed snapshot of the bare, inside the FUSE workspace
        mount (shipped to S3 by the workspace checkpoint)."""
        return self._mirror_repo_path

    @property
    def repo_path(self) -> str:
        """Path to the working tree (repo/) inside the workspace."""
        return f"{self.path}/repo"

    @property
    def merge_config(self) -> GitTransportConfig:
        return self._git_config

    @property
    def sync_lock(self) -> asyncio.Lock | None:
        return self._sync_lock

    @property
    def raise_on_conflict(self) -> bool:
        return self._raise_on_conflict

    @property
    def published_ref(self) -> GitPublishedRef | None:
        return self._published_ref

    def set_raise_on_conflict(self, enabled: bool) -> None:
        self._raise_on_conflict = enabled

    def set_merge_resolver(
        self,
        resolver: Callable[[str, Path, str, list[str]], Awaitable[None]],
    ) -> None:
        self._merge_resolver = resolver

    @staticmethod
    async def _ensure_git_installed_local() -> None:
        await run_local(
            "which git > /dev/null 2>&1 || (apt-get update -qq && apt-get install -y -qq git)",
            timeout=120,
        )

    @staticmethod
    def _write_hook(path: Path, content: str) -> None:
        path.write_text(content)
        path.chmod(0o755)

    async def _run_remote_git(
        self,
        hostname: str,
        *,
        request: GitOpRequest,
        timeout: int,
    ):
        return await run_remote_git_op(
            self.ssh_key_path,
            hostname,
            request,
            timeout=timeout,
        )

    async def _run_remote_git_checked(
        self,
        hostname: str,
        *,
        request: GitOpRequest,
        timeout: int,
        error_context: str,
    ):
        return await run_remote_git_checked(
            self.ssh_key_path,
            hostname,
            request,
            timeout=timeout,
            error_context=error_context,
        )

    async def _setup_workspace_path(self, path: str) -> None:
        quoted = shlex.quote(path)
        exit_code, _, stderr = await run_local(f"mkdir -p {quoted}", timeout=10)
        if exit_code != 0:
            raise RuntimeError(f"Failed to create workspace path {path}: {stderr}")

    async def _hydrate_local_bare_from_mirror(self, bare_dir: Path, mirror_dir: Path) -> None:
        """Reconstruct the local-disk bare from the persisted mirror, if needed.

        On resume, only the mirror (``{workspace}/.git-bare``) is restored —
        it rides back in on the workspace checkpoint. The active bare lives on
        local VM disk and is empty on a fresh VM, so copy the mirror's packed
        objects/refs over. No-op when the local bare already exists (same VM
        session) or when there is no mirror to hydrate from (fresh workspace).
        """
        if (bare_dir / "HEAD").exists():
            return
        if not (mirror_dir / "HEAD").exists():
            return
        logger.info("Hydrating active bare %s from restored mirror %s", bare_dir, mirror_dir)

        def _copy() -> None:
            shutil.rmtree(bare_dir, ignore_errors=True)
            bare_dir.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(mirror_dir, bare_dir)

        await asyncio.to_thread(_copy)
        trust_git_directory(bare_dir)

    async def ensure_local_bare(self) -> None:
        """Public entrypoint to hydrate the local bare from the persisted mirror.

        Called on the resume path before the working tree is re-checked-out
        (the checkout reads from the local bare, which must exist first).
        Idempotent.
        """
        await self._hydrate_local_bare_from_mirror(Path(self._bare_repo_path), Path(self._mirror_repo_path))

    async def snapshot_to_mirror(self) -> None:
        """Write a packed snapshot of the active bare to the FUSE mirror.

        Run at checkpoint time so the persisted mirror at ``mirror_repo_path``
        is a handful of pack files — fast manifest commit, cheap S3 delta,
        browsable ``repo/`` working tree — instead of the 40k+ loose objects
        the old in-FUSE bare accumulated. The mirror is then shipped to S3 by
        the normal workspace checkpoint.

        The active bare is left **untouched**: a consumer may deliberately keep
        it loose (e.g. webclone's transport patch unpacks objects on checkout),
        and the snapshot must not fight that. The pack is built on a local-disk
        staging copy and the finished result is copied into the mirror — we
        never run ``repack`` against the FUSE mirror itself, which would
        reintroduce the non-atomic multi-file pack write the off-FUSE move was
        meant to avoid. A plain ``copytree`` (vs rsync) is used because
        ``refs/heads/main`` is a 41-byte file whose content changes but size
        does not, so rsync's size+mtime quick-check can skip it and leave the
        mirror's ``main`` stale when two snapshots land in the same 1s window.
        """
        bare_dir = Path(self._bare_repo_path)
        mirror_dir = Path(self._mirror_repo_path)
        if not (bare_dir / "HEAD").exists():
            return

        def _build_and_swap() -> None:
            staging = Path(f"{bare_dir}.snapshot")
            if staging.exists():
                shutil.rmtree(staging)
            # copytree (not a bare clone) preserves ALL refs, including hidden
            # refs/plato/* published refs that a clone would drop.
            shutil.copytree(bare_dir, staging)
            trust_git_directory(staging)
            Repo(staging).git.repack("-a", "-d", "-q")
            mirror_dir.parent.mkdir(parents=True, exist_ok=True)
            if mirror_dir.exists():
                shutil.rmtree(mirror_dir)
            shutil.copytree(staging, mirror_dir)
            shutil.rmtree(staging, ignore_errors=True)

        await asyncio.to_thread(_build_and_swap)

    def _write_post_receive_hook(self, bare_dir: Path, repo_dir: Path) -> None:
        """(Re)write the post-receive hook that refreshes repo/ on push.

        Rewritten on every init so a bare hydrated from a mirror picks up the
        current VM's paths rather than whatever was baked in at creation time.
        """
        lock_name = str(bare_dir).replace("/", "_")
        hook_content = (
            "#!/bin/sh\n"
            f'LOCK="/tmp/git-transport-{lock_name}.lock"\n'
            f'REPO="{repo_dir}"\n'
            f'BARE="{bare_dir}"\n'
            "(\n"
            "  flock 9\n"
            '  git config --global --add safe.directory "$REPO" 2>/dev/null\n'
            '  git config --global --add safe.directory "$BARE" 2>/dev/null\n'
            '  git -C "$REPO" fetch origin main 2>&1\n'
            '  git -C "$REPO" reset --hard origin/main 2>&1\n'
            '  git -C "$REPO" clean -fd 2>&1\n'
            ') 9>"$LOCK"\n'
        )
        self._write_hook(bare_dir / "hooks" / "post-receive", hook_content)

    async def _init_bare_repo(self, workspace_path: str) -> None:
        await self._ensure_git_installed_local()
        workspace_dir = Path(workspace_path)
        repo_dir = workspace_dir / "repo"
        mirror_dir = Path(f"{workspace_path}/.git-bare")
        bare_dir = Path(self._local_bare_path(workspace_path))

        # The active bare lives on local VM disk (off the FUSE workspace mount):
        # keeps git's object store and every agent push's index-pack write off
        # FUSE, where multi-file rename/fsync is non-atomic and per-object
        # latency is brutal at 40k+ objects. On resume, rebuild it from the
        # restored packed mirror.
        bare_dir.parent.mkdir(parents=True, exist_ok=True)
        await self._hydrate_local_bare_from_mirror(bare_dir, mirror_dir)
        trust_git_directory(bare_dir)

        # If the active bare already exists (same VM session, or just hydrated
        # from a restored mirror), keep it and refresh the working tree.
        if (bare_dir / "HEAD").exists():
            logger.info("Active bare repo present at %s, skipping re-init", bare_dir)
            if repo_dir.exists():
                trust_git_directory(repo_dir)
                checkout_main_from_bare(bare_repo_path=str(bare_dir), worktree_path=str(repo_dir))
            self._write_post_receive_hook(bare_dir, repo_dir)
            await self.snapshot_to_mirror()
            return

        shutil.rmtree(bare_dir, ignore_errors=True)
        bare_dir.parent.mkdir(parents=True, exist_ok=True)
        bare_dir.mkdir(parents=True, exist_ok=True)
        Repo.init(bare_dir, bare=True, initial_branch="main")

        # Seed bare repo with initial commit from repo/ if it has content,
        # otherwise create an empty initial commit.
        if repo_dir.exists() and any(repo_dir.iterdir()):
            trust_git_directory(repo_dir)
            shutil.rmtree(repo_dir / ".git", ignore_errors=True)
            seed = Repo.init(repo_dir, initial_branch="main")
            gitignore_lines = list(WorkspaceMarker.DEFAULT_DVCIGNORE)
            (repo_dir / ".gitignore").write_text("\n".join(gitignore_lines) + "\n")
            seed.git.add(A=True)
            seed.index.commit("Initial workspace state", author=_PLATO_ACTOR, committer=_PLATO_ACTOR)
            seed.create_remote("origin", str(bare_dir)).push(refspec="main:main")
            shutil.rmtree(repo_dir / ".git")
        else:
            # Empty seed so bare has a main branch
            import tempfile

            with tempfile.TemporaryDirectory() as tmp:
                seed = Repo.init(tmp, initial_branch="main")
                (Path(tmp) / ".gitignore").write_text("\n".join(WorkspaceMarker.DEFAULT_DVCIGNORE) + "\n")
                seed.git.add(A=True)
                seed.index.commit("Initial workspace state", author=_PLATO_ACTOR, committer=_PLATO_ACTOR)
                seed.create_remote("origin", str(bare_dir)).push(refspec="main:main")

        # Clone bare → repo/ as a proper git working tree
        shutil.rmtree(repo_dir, ignore_errors=True)
        trust_git_directory(bare_dir)
        Repo.clone_from(str(bare_dir), str(repo_dir))

        # Post-receive hook: update repo/ working tree from bare on push
        self._write_post_receive_hook(bare_dir, repo_dir)
        # Seed the persisted mirror so a resume before the first checkpoint
        # still has something to hydrate from.
        await self.snapshot_to_mirror()
        logger.debug("Git bare repo initialized at %s (mirror: %s, repo: %s)", bare_dir, mirror_dir, repo_dir)

    async def _copy_ssh_key_to_agent(self, hostname: str) -> str:
        agent_key_path = "/root/.ssh/world_key"
        await run_ssh(
            self.ssh_key_path,
            hostname,
            "mkdir -p /root/.ssh && chmod 700 /root/.ssh",
            timeout=10,
        )
        ssh_cmd = (
            f"ssh -i {self.ssh_key_path} -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR"
        )
        proc = await asyncio.create_subprocess_exec(
            "rsync",
            "-e",
            ssh_cmd,
            str(self.ssh_key_path),
            f"root@{hostname}:{agent_key_path}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        _, rsync_err = await proc.communicate()
        if proc.returncode != 0:
            raise RuntimeError(f"Failed to copy SSH key to agent VM: {rsync_err.decode()}")
        await run_ssh(self.ssh_key_path, hostname, f"chmod 600 {agent_key_path}", timeout=10)
        return agent_key_path

    async def _head_commit_sha(self, workspace_path: str, hostname: str) -> str:
        return await self._git_rev_parse(workspace_path, hostname, "HEAD")

    async def _git_rev_parse(self, workspace_path: str, hostname: str, ref: str) -> str:
        result = await self._run_remote_git_checked(
            hostname,
            request=GitOpRequest.rev_parse(workspace_path, ref),
            timeout=10,
            error_context=f"Failed to resolve git ref {ref} on agent {hostname}",
        )
        return result.stdout

    async def _git_status_short(self, workspace_path: str, hostname: str, timeout: int = 10) -> str:
        result = await self._run_remote_git_checked(
            hostname,
            request=GitOpRequest.status_short(workspace_path),
            timeout=timeout,
            error_context=f"Failed to read git status on agent {hostname}",
        )
        return result.stdout

    async def _auto_commit_changes(self, workspace_path: str, hostname: str, commit_message: str) -> None:
        result = await self._run_remote_git(
            hostname,
            request=GitOpRequest.auto_commit(workspace_path, commit_message),
            timeout=60,
        )
        logger.info(
            "GitTransport auto-commit hostname=%s ok=%s stdout=%s stderr=%s",
            hostname,
            result.ok,
            result.stdout,
            result.stderr,
        )
        if not result.ok:
            status = await self._git_status_short(workspace_path, hostname, timeout=10)
            raise RuntimeError(
                f"Auto-commit failed on agent {hostname}: "
                f"{result.stderr or result.stdout or 'unknown error'} (status={status})"
            )

    async def _publish_conflict_ref(self, workspace_path: str, hostname: str, commit_sha: str) -> str:
        conflict_ref = f"refs/plato/conflicts/{commit_sha}"
        await self._push_head_to_ref(workspace_path, hostname, conflict_ref)
        return conflict_ref

    async def _push_head_to_ref(self, workspace_path: str, hostname: str, ref: str) -> None:
        await self._run_remote_git_checked(
            hostname,
            request=GitOpRequest.push(workspace_path, f"HEAD:{ref}", force=True),
            timeout=60,
            error_context=f"Failed to push ref {ref} from agent {hostname}",
        )

    @staticmethod
    def _is_push_conflict(stderr: str) -> bool:
        lowered = stderr.lower()
        return "non-fast-forward" in lowered or "[rejected]" in lowered or "fetch first" in lowered

    async def initialize(self) -> None:
        await self._setup_workspace_path(self.path)
        await self._init_bare_repo(self.path)

    async def update_bare_repo(self, message: str = "Update workspace") -> None:
        """Commit any changes in repo/ and push to the bare repo."""
        await self._ensure_git_installed_local()
        repo_dir = Path(self.repo_path)
        trust_git_directory(repo_dir)
        repo = Repo(repo_dir)
        repo.git.add(A=True)
        if repo.is_dirty(index=True):
            repo.index.commit(message, author=_PLATO_ACTOR, committer=_PLATO_ACTOR)
            repo.remote("origin").push(refspec="main:main", force=True)

    async def setup_agent(
        self,
        agent_env: Environment | None,
        hostname: str,
        mount: AgentWorkspaceMount,
    ) -> None:
        del agent_env
        t0 = _time.monotonic()
        logger.info("GitTransport.setup_agent: installing git on %s", hostname)
        await run_ssh(
            self.ssh_key_path,
            hostname,
            "which git > /dev/null 2>&1 || (apt-get update -qq && apt-get install -y -qq git)",
            timeout=180,
        )
        logger.debug("GitTransport.setup_agent: git installed on %s (%.1fs)", hostname, _time.monotonic() - t0)

        t1 = _time.monotonic()
        agent_key_path = await self._copy_ssh_key_to_agent(hostname)
        ssh_config = (
            "Host world-git\n"
            f"    HostName {self.world_vm_ip}\n"
            "    User root\n"
            f"    IdentityFile {agent_key_path}\n"
            "    StrictHostKeyChecking no\n"
            "    UserKnownHostsFile /dev/null\n"
            "    LogLevel ERROR\n"
        )
        await run_ssh(
            self.ssh_key_path,
            hostname,
            f"cat > /root/.ssh/config << 'SSHCFG'\n{ssh_config}SSHCFG",
            timeout=10,
        )
        logger.debug("GitTransport.setup_agent: SSH key configured on %s (%.1fs)", hostname, _time.monotonic() - t1)
        await ensure_remote_git_server(self.ssh_key_path, hostname, timeout=15)

        remote = mount.agent_path
        checkout_ref = mount.git_checkout.ref if mount.git_checkout is not None else None
        branch_name = mount.git_checkout.branch_name if mount.git_checkout is not None else None
        t2 = _time.monotonic()
        logger.debug("GitTransport.setup_agent: cloning %s -> %s on %s", self._bare_repo_path, remote, hostname)
        await self._run_remote_git_checked(
            hostname,
            request=GitOpRequest.clone_setup(
                remote,
                bare_repo_path=self._bare_repo_path,
                checkout_ref=checkout_ref,
                branch_name=branch_name or "plato-task",
            ),
            timeout=120,
            error_context="Failed to clone git repo on agent VM",
        )

        audit_key = mount.audit_key
        tracked = mount.tracked
        if tracked and audit_key:
            audit_cmd = " && ".join(build_auditctl_commands(remote, audit_key))
            exit_code, _, stderr = await run_ssh(self.ssh_key_path, hostname, audit_cmd, timeout=30)
            if exit_code != 0:
                raise RuntimeError(
                    f"Failed to enable filesystem audit on agent VM for {remote} (key={audit_key}): {stderr}"
                )
            logger.info("Filesystem audit enabled on agent VM for %s (key=%s)", remote, audit_key)

        logger.info(
            "GitTransport.setup_agent: done on %s (clone=%.1fs, total=%.1fs): %s -> %s",
            hostname,
            _time.monotonic() - t2,
            _time.monotonic() - t0,
            self._bare_repo_path,
            remote,
        )

    async def sync_back(
        self,
        agent_env: Environment | None,
        hostname: str,
        mount: AgentWorkspaceMount,
    ) -> None:
        sync_mode, sync_target, sync_exact = self._sync_policy(mount)
        remote = mount.agent_path
        raise_on_conflict = mount.git_raise_on_conflict

        if sync_mode != "merge_to_main":
            compare_ref = mount.git_checkout.ref if mount.git_checkout and mount.git_checkout.ref else "origin/main"
            # Serialize publish_ref/push_branch pushes too: concurrent
            # receive-pack invocations against the same bare repo race the
            # packfile index even when each push targets a unique hidden
            # ref, producing "packfile claims to have N objects while index
            # indicates M" corruption.
            if self._sync_lock:
                async with self._sync_lock:
                    await self._publish_sync_back_impl(
                        agent_env,
                        hostname,
                        remote,
                        sync_mode,
                        sync_target,
                        sync_exact,
                        compare_ref,
                    )
            else:
                await self._publish_sync_back_impl(
                    agent_env,
                    hostname,
                    remote,
                    sync_mode,
                    sync_target,
                    sync_exact,
                    compare_ref,
                )
            return
        if self._sync_lock:
            async with self._sync_lock:
                await self._sync_back_impl(agent_env, hostname, remote, raise_on_conflict)
        else:
            await self._sync_back_impl(agent_env, hostname, remote, raise_on_conflict)

    async def _sync_back_impl(
        self,
        agent_env: Environment | None,
        hostname: str,
        remote: str,
        raise_on_conflict: bool,
    ) -> None:
        self._published_ref = None
        cfg = self._git_config

        if cfg.commit_on_sync:
            await self._auto_commit_changes(remote, hostname, cfg.auto_commit_message)

        compare = await self._run_remote_git_checked(
            hostname,
            request=GitOpRequest.head_diff(remote, "origin/main"),
            timeout=10,
            error_context=f"Failed to compare HEAD against origin/main on agent {hostname}",
        )
        if bool(compare.noop):
            logger.debug("No changes to push from agent %s", hostname)
            return

        merge_cfg = cfg.merge_agent
        for attempt in range(1, merge_cfg.max_retries + 1):
            # Fetch and merge origin/main before every push attempt
            await self._run_remote_git_checked(
                hostname,
                request=GitOpRequest.fetch_origin(remote),
                timeout=30,
                error_context=f"Failed to fetch origin on agent {hostname}",
            )
            merge_result = await self._run_remote_git(
                hostname,
                request=GitOpRequest.merge_origin_main(remote),
                timeout=60,
            )
            if not merge_result.ok:
                logger.info(
                    "sync_back: agent %s pre-push merge had conflicts (attempt %d), resolving",
                    hostname,
                    attempt,
                )
                await self._resolve_merge_conflicts(agent_env, hostname, remote, merge_cfg)

            push_result = await self._run_remote_git(
                hostname,
                request=GitOpRequest.push(remote, "HEAD:main", force=False),
                timeout=60,
            )
            if push_result.ok:
                logger.info("Git push succeeded from agent %s (attempt %d)", hostname, attempt)
                await self._refresh_local_workspace_from_main()
                return

            logger.warning(
                "Git push failed from agent %s (attempt %d/%d): %s",
                hostname,
                attempt,
                merge_cfg.max_retries,
                (push_result.stderr or push_result.stdout or "").strip(),
            )

            push_stderr = push_result.stderr or push_result.stdout or ""
            if raise_on_conflict and self._is_push_conflict(push_stderr):
                commit_sha = await self._head_commit_sha(remote, hostname)
                conflict_ref = await self._publish_conflict_ref(remote, hostname, commit_sha)
                raise GitPushConflict(commit_sha=commit_sha, conflict_ref=conflict_ref)

            if attempt == merge_cfg.max_retries:
                break

        raise RuntimeError(f"Git push failed from agent {hostname} after {merge_cfg.max_retries} attempts")

    async def _publish_sync_back_impl(
        self,
        agent_env: Environment | None,
        hostname: str,
        remote: str,
        sync_mode: str,
        sync_target: str | None,
        sync_exact: bool,
        compare_ref: str,
    ) -> None:
        del agent_env
        self._published_ref = None
        cfg = self._git_config

        if cfg.commit_on_sync:
            await self._auto_commit_changes(remote, hostname, cfg.auto_commit_message)

        head_sha = await self._git_rev_parse(remote, hostname, "HEAD")
        publish_state = await self._run_remote_git_checked(
            hostname,
            request=GitOpRequest.publish_state(remote, compare_ref),
            timeout=10,
            error_context=f"Failed to inspect publish state on agent {hostname}",
        )
        compare_sha = publish_state.compare_sha or ""
        status = publish_state.git_status or ""
        ahead_behind = publish_state.ahead_behind or ""
        logger.info(
            "GitTransport publish state hostname=%s head=%s compare_ref=%s compare_sha=%s status=%s ahead_behind=%s",
            hostname,
            head_sha,
            compare_ref,
            compare_sha,
            status or "<clean>",
            ahead_behind,
        )

        if head_sha == compare_sha:
            if status:
                raise RuntimeError(
                    f"Agent {hostname} has uncommitted changes after sync but HEAD still matches {compare_ref}: {status}"
                )
            logger.info("No committed changes to publish from agent %s", hostname)
            return

        if sync_mode == "push_branch":
            if not sync_target:
                raise RuntimeError("push_branch sync policy requires a branch target")
            published_ref = f"refs/heads/{sync_target}"
        else:
            if not sync_target:
                raise RuntimeError("publish_ref sync policy requires a target ref")
            published_ref = sync_target if sync_exact else f"{sync_target}/{head_sha}"
        logger.info("Publishing agent %s commit %s to hidden ref %s", hostname, head_sha, published_ref)

        retries = max(1, cfg.merge_agent.max_retries)
        for attempt in range(1, retries + 1):
            try:
                await self._push_head_to_ref(remote, hostname, published_ref)
                self._published_ref = GitPublishedRef(commit_sha=head_sha, ref=published_ref)
                logger.info("Published agent %s commit %s to %s", hostname, head_sha, published_ref)
                return
            except RuntimeError:
                if attempt == retries:
                    raise
                logger.warning(
                    "Publishing hidden ref failed from agent %s (attempt %d/%d)",
                    hostname,
                    attempt,
                    retries,
                    exc_info=True,
                )

    async def _refresh_local_workspace_from_main(self) -> None:
        await asyncio.to_thread(
            checkout_main_from_bare,
            bare_repo_path=self._bare_repo_path,
            worktree_path=self.repo_path,
        )

    async def _resolve_and_retry(
        self,
        agent_env: Environment | None,
        hostname: str,
        workspace_path: str,
        merge_cfg: MergeAgentConfig,
    ) -> bool:
        if merge_cfg.strategy == "theirs":
            result = await self._run_remote_git(
                hostname,
                request=GitOpRequest.rebase_ours(workspace_path),
                timeout=60,
            )
            if not result.ok:
                logger.warning(
                    "Rebase failed, accepting theirs: %s",
                    (result.stderr or result.stdout or "").strip(),
                )
                await self._run_remote_git_checked(
                    hostname,
                    request=GitOpRequest.abort_rebase_reset_main(workspace_path),
                    timeout=30,
                    error_context=f"Failed to reset to origin/main on agent {hostname}",
                )
            return False

        if merge_cfg.strategy == "ours":
            result = await self._run_remote_git(
                hostname,
                request=GitOpRequest.force_push_main(workspace_path),
                timeout=60,
            )
            if not result.ok:
                raise RuntimeError(
                    f"Failed to force-push local changes for agent {hostname}: "
                    f"{result.stderr or result.stdout or 'unknown error'}"
                )
            return True

        logger.info(
            "sync_back: agent %s merging origin/main (strategy=%s)",
            hostname,
            merge_cfg.strategy,
        )
        result = await self._run_remote_git(
            hostname,
            request=GitOpRequest.merge_origin_main(workspace_path),
            timeout=60,
        )
        if result.ok:
            logger.info("sync_back: agent %s merge origin/main succeeded cleanly", hostname)
            return False

        logger.warning(
            "sync_back: agent %s merge origin/main had conflicts: %s",
            hostname,
            (result.stderr or result.stdout or "").strip()[:300],
        )
        await self._resolve_merge_conflicts(agent_env, hostname, workspace_path, merge_cfg)
        return False

    async def _resolve_merge_conflicts(
        self,
        agent_env: Environment | None,
        hostname: str,
        workspace_path: str,
        merge_cfg: MergeAgentConfig,
    ) -> None:
        del agent_env, merge_cfg
        result = await self._run_remote_git_checked(
            hostname,
            request=GitOpRequest.unmerged_files(workspace_path),
            timeout=10,
            error_context=f"Failed to inspect merge conflicts on agent {hostname}",
        )
        conflicted_files = [str(path) for path in (result.files or [])]
        logger.info("Merge conflicts in %d files: %s", len(conflicted_files), conflicted_files)

        if not self._merge_resolver:
            logger.warning(
                "No merge resolver configured, resolving conflicts with 'accept theirs' for files: %s",
                conflicted_files,
            )
            await self._accept_theirs(hostname, workspace_path, "Auto-resolved conflicts (accept theirs)")
            post_head = await self._head_commit_sha(workspace_path, hostname)
            post_status = await self._git_status_short(workspace_path, hostname)
            logger.info(
                "sync_back: agent %s after accept_theirs: HEAD=%s status=%s",
                hostname,
                post_head[:12] if post_head else "?",
                post_status.strip()[:200] or "(clean)",
            )
            return

        logger.info("Invoking merge resolver for %d conflicts", len(conflicted_files))
        try:
            await self._merge_resolver(hostname, self.ssh_key_path, workspace_path, conflicted_files)
        except Exception:
            logger.warning("Merge resolver failed, falling back to accept-theirs", exc_info=True)
            await self._accept_theirs(hostname, workspace_path, "Auto-resolved conflicts (agent failed, accept theirs)")
            return

        remaining_result = await self._run_remote_git_checked(
            hostname,
            request=GitOpRequest.unmerged_files(workspace_path),
            timeout=10,
            error_context=f"Failed to inspect remaining merge conflicts on agent {hostname}",
        )
        remaining = [str(path) for path in (remaining_result.files or [])]
        if remaining:
            logger.warning(
                "Merge resolver left unresolved conflicts: %s — falling back to accept-theirs",
                remaining,
            )
            await self._accept_theirs(hostname, workspace_path, "Resolved merge conflicts (with fallback)")

    async def _accept_theirs(self, hostname: str, workspace_path: str, message: str) -> None:
        await self._run_remote_git_checked(
            hostname,
            request=GitOpRequest.accept_theirs(workspace_path, message),
            timeout=30,
            error_context=f"Failed to accept theirs on agent {hostname}",
        )

    async def add_export(self, path: str, fsid: int) -> None:
        del fsid
        await self._setup_workspace_path(path)
        await self._init_bare_repo(path)

    async def refresh_exports(self) -> None:
        """No-op for git transport."""

    async def collect_audit_log(
        self,
        hostname: str,
        audit_key: str | None = None,
    ) -> str | None:
        try:
            key = audit_key or "plato_workspace"
            exit_code, stdout, _ = await run_ssh(
                self.ssh_key_path,
                hostname,
                f"ausearch -if /var/log/audit/audit.log --format raw -k {shlex.quote(key)} 2>/dev/null || true",
                timeout=30,
            )
            if exit_code != 0 or not stdout.strip():
                return None
            return stdout
        except Exception:
            logger.warning("Failed to collect audit log from agent VM", exc_info=True)
            return None

    async def prepare(self) -> None:
        await self._setup_workspace_path(self.path)

    def with_path(self, path: str) -> GitTransport:
        sub_mount = None
        if self.mount_path and path.startswith(self.path + "/"):
            sub_mount = self.mount_path + path[len(self.path) :]
        transport = GitTransport(
            path,
            self.world_vm_ip,
            self.ssh_key_path,
            sub_mount,
            self._git_config,
            self._raise_on_conflict,
        )
        transport._merge_resolver = self._merge_resolver
        transport._sync_lock = self._sync_lock
        transport._published_ref = None
        return transport

    def _sync_policy(self, mount: AgentWorkspaceMount) -> tuple[str, str | None, bool]:
        if mount.git_sync is None:
            return "merge_to_main", None, False
        return mount.git_sync.mode, mount.git_sync.target, mount.git_sync.exact
