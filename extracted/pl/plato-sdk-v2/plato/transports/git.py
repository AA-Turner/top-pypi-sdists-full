"""Git-based workspace transport implementation."""

from __future__ import annotations

import asyncio
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
    ensure_remote_git_server,
    run_remote_git_checked,
    run_remote_git_op,
    trust_git_directory,
)
from plato.markers import WorkspaceMarker
from plato.transports.base import Transport
from plato.utils.subprocess import run_local, run_ssh

if TYPE_CHECKING:
    from plato.v2.async_.environment import Environment
    from plato.worlds.config import GitTransportConfig, MergeAgentConfig

logger = logging.getLogger(__name__)
_PLATO_ACTOR = Actor("Plato", "plato@plato.dev")
_AGENT_ACTOR = Actor("Plato Agent", "agent@plato.dev")


@dataclass(frozen=True, slots=True)
class GitCheckout:
    """Checkout configuration for an agent git workspace."""

    ref: str | None
    branch_name: str | None = None


@dataclass(frozen=True, slots=True)
class GitSyncBack:
    """Sync-back policy for an agent git workspace."""

    target_ref: str | None = None
    exact_ref: bool = False

    @classmethod
    def merge_to_main(cls) -> GitSyncBack:
        return cls()

    @classmethod
    def publish_ref(cls, ref: str, *, exact: bool = False) -> GitSyncBack:
        return cls(target_ref=ref, exact_ref=exact)

    @classmethod
    def push_branch(cls, branch_name: str) -> GitSyncBack:
        return cls(target_ref=f"refs/heads/{branch_name}", exact_ref=True)


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
        publish_ref_prefix: str | None = None,
    ) -> None:
        self.path = path
        self.world_vm_ip = world_vm_ip
        self.ssh_key_path = ssh_key_path
        self.mount_path = mount_path
        self._bare_repo_path = f"{path}/.git-bare"
        self._raise_on_conflict = raise_on_conflict
        self._publish_ref_prefix = publish_ref_prefix
        self._publish_ref_exact = False
        self._published_ref: GitPublishedRef | None = None
        self._checkout_base_ref: str | None = None
        self._checkout_branch_name: str | None = None
        if git_config is None:
            from plato.worlds.config import GitTransportConfig as _GitTransportConfig

            git_config = _GitTransportConfig()
        self._git_config = git_config
        self._merge_resolver: Callable[[str, Path, str, list[str]], Awaitable[None]] | None = None
        self._sync_lock = asyncio.Lock() if self._git_config.serialize_sync else None
        self.configure_workspace(name=None, repo_root=None, tracked=False)
        self.configure_audit_scope(audit_run_id=None, audit_key=None)

    @property
    def bare_repo_path(self) -> str:
        return self._bare_repo_path

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
    def publish_ref_prefix(self) -> str | None:
        return self._publish_ref_prefix

    @property
    def published_ref(self) -> GitPublishedRef | None:
        return self._published_ref

    @property
    def checkout_base_ref(self) -> str | None:
        return self._checkout_base_ref

    def set_raise_on_conflict(self, enabled: bool) -> None:
        self._raise_on_conflict = enabled

    def set_publish_ref_prefix(self, prefix: str | None, *, exact: bool = False) -> None:
        self._publish_ref_prefix = prefix
        self._publish_ref_exact = exact
        self._published_ref = None

    def set_checkout_base_ref(self, ref: str | None, *, branch_name: str | None = None) -> None:
        self._checkout_base_ref = ref
        self._checkout_branch_name = branch_name

    def set_merge_resolver(
        self,
        resolver: Callable[[str, Path, str, list[str]], Awaitable[None]],
    ) -> None:
        self._merge_resolver = resolver

    def for_agent(
        self,
        *,
        path: str | None = None,
        mount_path: str | None = None,
        checkout: GitCheckout | None = None,
        sync_back: GitSyncBack | None = None,
        raise_on_conflict: bool | None = None,
    ) -> GitTransport:
        """Return a cloned transport configured for one agent run."""
        resolved_path = path or self.path
        transport = self.with_path(resolved_path)
        if mount_path is not None:
            transport.mount_path = mount_path
        elif resolved_path == self.path and self.mount_path is not None:
            transport.mount_path = self.mount_path
        if checkout is not None:
            transport._checkout_base_ref = checkout.ref
            transport._checkout_branch_name = checkout.branch_name
        if sync_back is not None:
            transport._publish_ref_prefix = sync_back.target_ref
            transport._publish_ref_exact = sync_back.exact_ref
            transport._published_ref = None
        if raise_on_conflict is not None:
            transport._raise_on_conflict = raise_on_conflict
        return transport

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

    async def _init_bare_repo(self, workspace_path: str, bare_path: str) -> None:
        await self._ensure_git_installed_local()
        workspace_dir = Path(workspace_path)
        bare_dir = Path(bare_path)
        trust_git_directory(workspace_dir)
        trust_git_directory(bare_dir)
        shutil.rmtree(bare_dir, ignore_errors=True)
        bare_dir.parent.mkdir(parents=True, exist_ok=True)
        bare_repo = Repo.init(bare_dir, bare=True, initial_branch="main")
        with bare_repo.config_writer() as config:
            config.set_value("transfer", "unpackLimit", "99999")
        gitignore_lines = list(WorkspaceMarker.DEFAULT_DVCIGNORE) + [".git-bare"]
        gitignore_content = "\n".join(gitignore_lines) + "\n"
        (workspace_dir / ".gitignore").write_text(gitignore_content)
        shutil.rmtree(workspace_dir / ".git", ignore_errors=True)
        repo = Repo.init(workspace_dir, initial_branch="main")
        repo.git.add(A=True)
        repo.index.commit("Initial workspace state", author=_PLATO_ACTOR, committer=_PLATO_ACTOR)
        origin = repo.create_remote("origin", bare_path)
        origin.push(refspec="main:main")
        shutil.rmtree(workspace_dir / ".git", ignore_errors=True)
        lock_name = bare_path.replace("/", "_")
        hook_content = (
            "#!/usr/bin/env python3\n"
            "import fcntl\n"
            "from pathlib import Path\n\n"
            "from plato.git_ops.repo import checkout_main_from_bare\n\n"
            f'lock_path = Path("/tmp/git-transport-{lock_name}.lock")\n'
            'with lock_path.open("w") as lock_file:\n'
            "    fcntl.flock(lock_file, fcntl.LOCK_EX)\n"
            f"    checkout_main_from_bare(bare_repo_path={bare_path!r}, worktree_path={workspace_path!r})\n"
        )
        self._write_hook(bare_dir / "hooks" / "post-receive", hook_content)
        logger.info("Git bare repo initialized at %s (workspace: %s)", bare_path, workspace_path)

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
        await self._init_bare_repo(self.path, self._bare_repo_path)

    async def update_bare_repo(self, message: str = "Update workspace") -> None:
        await self._ensure_git_installed_local()
        workspace_dir = Path(self.path)
        bare_dir = Path(self._bare_repo_path)
        trust_git_directory(workspace_dir)
        trust_git_directory(bare_dir)
        shutil.rmtree(workspace_dir / ".git", ignore_errors=True)
        repo = Repo.init(workspace_dir, initial_branch="main")
        repo.git.add(A=True)
        repo.index.commit(message, author=_PLATO_ACTOR, committer=_PLATO_ACTOR)
        origin = repo.create_remote("origin", self._bare_repo_path)
        origin.push(refspec="main:main", force=True)
        shutil.rmtree(workspace_dir / ".git", ignore_errors=True)

    async def setup_agent(self, agent_env: Environment, hostname: str) -> None:
        del agent_env
        t0 = _time.monotonic()
        logger.info("GitTransport.setup_agent: installing git on %s", hostname)
        await run_ssh(
            self.ssh_key_path,
            hostname,
            "which git > /dev/null 2>&1 || (apt-get update -qq && apt-get install -y -qq git)",
            timeout=180,
        )
        logger.info("GitTransport.setup_agent: git installed on %s (%.1fs)", hostname, _time.monotonic() - t0)

        t1 = _time.monotonic()
        logger.info("GitTransport.setup_agent: copying SSH key to %s", hostname)
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
        logger.info("GitTransport.setup_agent: SSH key configured on %s (%.1fs)", hostname, _time.monotonic() - t1)
        await ensure_remote_git_server(self.ssh_key_path, hostname, timeout=15)
        logger.info("GitTransport.setup_agent: git server ready on %s", hostname)

        remote = self.agent_mount_path
        t2 = _time.monotonic()
        logger.info("GitTransport.setup_agent: cloning %s -> %s on %s", self._bare_repo_path, remote, hostname)
        await self._run_remote_git_checked(
            hostname,
            request=GitOpRequest.clone_setup(
                remote,
                bare_repo_path=self._bare_repo_path,
                checkout_ref=self._checkout_base_ref,
                branch_name=self._checkout_branch_name or "plato-task",
            ),
            timeout=120,
            error_context="Failed to clone git repo on agent VM",
        )

        logger.info(
            "GitTransport.setup_agent: done on %s (clone=%.1fs, total=%.1fs): %s -> %s",
            hostname,
            _time.monotonic() - t2,
            _time.monotonic() - t0,
            self._bare_repo_path,
            remote,
        )

    async def sync_back(self, agent_env: Environment, hostname: str) -> None:
        logger.info(
            "GitTransport.sync_back hostname=%s publish_ref_prefix=%s transport_id=%s",
            hostname,
            self._publish_ref_prefix,
            id(self),
        )
        if self._publish_ref_prefix:
            await self._publish_sync_back_impl(agent_env, hostname)
            return
        if self._sync_lock:
            async with self._sync_lock:
                await self._sync_back_impl(agent_env, hostname)
        else:
            await self._sync_back_impl(agent_env, hostname)

    async def _sync_back_impl(self, agent_env: Environment, hostname: str) -> None:
        self._published_ref = None
        cfg = self._git_config
        remote = self.agent_mount_path

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
            push_result = await self._run_remote_git(
                hostname,
                request=GitOpRequest.push(remote, "HEAD:main", force=False),
                timeout=60,
            )
            if push_result.ok:
                logger.info("Git push succeeded from agent %s (attempt %d)", hostname, attempt)
                return

            logger.warning(
                "Git push failed from agent %s (attempt %d/%d): %s",
                hostname,
                attempt,
                merge_cfg.max_retries,
                (push_result.stderr or push_result.stdout or "").strip(),
            )

            push_stderr = push_result.stderr or push_result.stdout or ""
            if self._raise_on_conflict and self._is_push_conflict(push_stderr):
                await self._run_remote_git_checked(
                    hostname,
                    request=GitOpRequest.fetch_origin(remote),
                    timeout=30,
                    error_context=f"Failed to fetch origin on agent {hostname}",
                )
                commit_sha = await self._head_commit_sha(remote, hostname)
                conflict_ref = await self._publish_conflict_ref(remote, hostname, commit_sha)
                raise GitPushConflict(commit_sha=commit_sha, conflict_ref=conflict_ref)

            if attempt == merge_cfg.max_retries:
                break

            resolved = await self._resolve_and_retry(agent_env, hostname, remote, merge_cfg)
            if resolved:
                logger.info("Git conflict resolved for agent %s without another retry push", hostname)
                return

        raise RuntimeError(f"Git push failed from agent {hostname} after {merge_cfg.max_retries} attempts")

    async def _publish_sync_back_impl(self, agent_env: Environment, hostname: str) -> None:
        del agent_env
        self._published_ref = None
        cfg = self._git_config
        remote = self.agent_mount_path

        if cfg.commit_on_sync:
            await self._auto_commit_changes(remote, hostname, cfg.auto_commit_message)

        head_sha = await self._git_rev_parse(remote, hostname, "HEAD")
        compare_ref = self._checkout_base_ref or "origin/main"
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

        if not self._publish_ref_prefix:
            raise RuntimeError("publish_ref_prefix must be set for publish-only sync mode")

        published_ref = (
            self._publish_ref_prefix if self._publish_ref_exact else f"{self._publish_ref_prefix}/{head_sha}"
        )
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

    async def _resolve_and_retry(
        self,
        agent_env: Environment,
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

        result = await self._run_remote_git(
            hostname,
            request=GitOpRequest.merge_origin_main(workspace_path),
            timeout=60,
        )
        if result.ok:
            return False

        await self._resolve_merge_conflicts(agent_env, hostname, workspace_path, merge_cfg)
        return False

    async def _resolve_merge_conflicts(
        self,
        agent_env: Environment,
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
            logger.warning("No merge resolver configured, resolving conflicts with 'accept theirs'")
            await self._accept_theirs(hostname, workspace_path, "Auto-resolved conflicts (accept theirs)")
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
        bare_path = f"{path}/.git-bare"
        await self._init_bare_repo(path, bare_path)

    async def refresh_exports(self) -> None:
        """No-op for git transport."""

    async def collect_audit_log(
        self,
        hostname: str,
        audit_key: str | None = None,
    ) -> str | None:
        try:
            key = audit_key or self.audit_key or "plato_workspace"
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
            self._publish_ref_prefix,
        )
        transport._merge_resolver = self._merge_resolver
        transport._sync_lock = self._sync_lock
        transport._published_ref = None
        transport._checkout_base_ref = self._checkout_base_ref
        transport._checkout_branch_name = self._checkout_branch_name
        transport.configure_workspace(
            name=self.workspace_name,
            repo_root=self.workspace_repo_root,
            tracked=self.workspace_tracked,
        )
        transport.configure_audit_scope(
            audit_run_id=self.audit_run_id,
            audit_key=self.audit_key,
        )
        return transport
