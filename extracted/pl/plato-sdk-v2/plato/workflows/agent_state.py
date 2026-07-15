"""Pull/push an agent harness's resumable session state over rsync+ssh.

The workflow world's orchestrator runs an agent harness on a pooled agent VM.
To make its *conversation* durable across session crashes (not just the
journaled work), the world periodically pulls the harness's session state into
the tracked ``agent_state`` workspace (it rides the existing DVC checkpoint
cadence) and pushes it back onto the fresh VM on relaunch, so the resumed
harness can pick up the newest session (``claude --continue`` for claude-code,
``codex-exec resume --last`` for codex). WHICH directories hold that state is
harness-specific — see :data:`HARNESS_STATE_SPECS`. A harness without a spec
gets conversation durability explicitly disabled, never mis-pathed pulls
(the TurboTax gpt-5.6 run resumed amnesiac because codex state was silently
not captured by the then-claude-only paths).

Pull-based snapshots on purpose: NEVER NFS-mount ``~/.claude`` on the agent VM
— long-lived append handles on FUSE-backed paths corrupt (see
``plato/workflows/journal.py`` module docstring history).

State layout inside ``state_dir``::

    claude-projects/<cwd-key>/   <- {home}/.claude/projects/<cwd-key>/
    claude-todos/                <- {home}/.claude/todos/
    cwd/                         <- {cwd}/ (scratch files; data/, node_modules,
                                    .git, *.log excluded)
    manifest.json                <- {version, cwd, home, cwd_key, pulled_at_label}

``<cwd-key>`` is the Claude Code project-directory key: the cwd path with
``/`` replaced by ``-`` (cwd ``/workflow-results`` -> ``-workflow-results``).
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

logger = logging.getLogger(__name__)

__all__ = [
    "ORCHESTRATOR_STATE_VERSION",
    "CLAUDE_HOME_DEFAULT",
    "HARNESS_STATE_SPECS",
    "HarnessStateSpec",
    "AgentStateSync",
]

ORCHESTRATOR_STATE_VERSION = 2

#: Default ``$HOME`` of the claude CLI process on Chronos agent VMs.
#:
#: Verified evidence (re-verify before changing):
#:
#: - ``plato/agents/vm_setup.py::execute_agent`` launches ``plato-agent-runner``
#:   over SSH with ``user="root"``; ``run_ssh_streaming`` only sudo-wraps for
#:   non-root users, so the harness runs in a plain root SSH session
#:   (``HOME=/root`` from root's passwd entry — nothing in the sourced
#:   ``/tmp/.plato_agent_env`` file or ``VM_PATH_EXPORT`` overrides HOME).
#: - ``agents/claude-code/src/claude_code/__init__.py`` starts the ``claude``
#:   CLI with ``env = os.environ.copy(); env["IS_SANDBOX"] = "1"`` and no HOME
#:   override — ``IS_SANDBOX=1`` is what lets ``--dangerously-skip-permissions``
#:   run as root. All harness state paths use ``Path.home()`` (credentials at
#:   ``~/.claude/.credentials.json``, transcripts at ``~/.claude/projects``),
#:   which resolves to ``/root`` in that process.
#: - The ``superman`` user and ``ENV HOME=/home/superman`` in
#:   ``agents/agent-base.Dockerfile`` apply only to container-mode entrypoints
#:   (``USER superman``); Chronos VM agents run over SSH as root and never
#:   re-exec as superman (the Dockerfile's node-symlink comment: "for root with
#:   no shell prefix required — the agent subprocess and SSH").
CLAUDE_HOME_DEFAULT = "/root"

#: Scratch-dir pull excludes: the mounted results data, dependency/VCS trees,
#: and log spew have their own durability (or none worth paying for).
_CWD_PULL_EXCLUDES: tuple[str, ...] = ("data/", "node_modules", ".git", "*.log")

_PULL_TIMEOUT_S = 120.0
_PUSH_TIMEOUT_S = 300.0
_PUSH_MAX_RETRIES = 3
_PUSH_RETRY_DELAY_S = 5.0


def _cwd_key(cwd: str) -> str:
    """Claude Code project-dir key for ``cwd`` (``/`` -> ``-``)."""
    return cwd.replace("/", "-")


@dataclass(frozen=True)
class StatePath:
    """One remote-dir <-> ``state_dir``-subdir mapping (templated).

    ``remote`` and ``local`` are templates over ``{home}``, ``{cwd}``,
    ``{cwd_key}``. ``exact_restore`` pushes with ``--delete`` so the VM dir
    ends up exactly equal to the checkpoint: both harnesses resume "the newest
    session in the dir" (claude ``--continue``, ``codex-exec resume --last``),
    so any stale rollout/transcript left on the VM (e.g. a pool reset that
    failed to wipe) could win over the restored one. The cwd scratch push must
    stay non-deleting — it targets the live results mount and the snapshot
    excludes ``data/`` and friends.
    """

    remote: str
    local: str
    excludes: tuple[str, ...] = ()
    exact_restore: bool = True


@dataclass(frozen=True)
class HarnessStateSpec:
    """Where a harness keeps its resumable conversation state on the VM.

    ``marker_glob`` (relative to ``state_dir``) decides
    :meth:`AgentStateSync.has_state` — match one file and the harness's resume
    flag has a session to pick up.
    """

    name: str
    paths: tuple[StatePath, ...]
    marker_glob: str


_CWD_STATE_PATH = StatePath(remote="{cwd}", local="cwd", excludes=_CWD_PULL_EXCLUDES, exact_restore=False)

_CLAUDE_STATE_SPEC = HarnessStateSpec(
    name="claude-code",
    paths=(
        StatePath(remote="{home}/.claude/projects/{cwd_key}", local="claude-projects/{cwd_key}"),
        StatePath(remote="{home}/.claude/todos", local="claude-todos"),
        _CWD_STATE_PATH,
    ),
    marker_glob="claude-projects/**/*.jsonl",
)

HARNESS_STATE_SPECS: dict[str, HarnessStateSpec] = {
    "claude-code": _CLAUDE_STATE_SPEC,
    # test-agent is the zero-cost e2e stand-in for a claude-code orchestrator:
    # the state-capture e2e's payload fabricates claude-layout session files on
    # its VM, so it aliases the claude spec — keeping the cheap e2e exercising
    # the exact pull/manifest/push pipeline production claude runs use.
    "test-agent": _CLAUDE_STATE_SPEC,
    # Codex keeps session rollouts under ~/.codex/sessions/YYYY/MM/DD/*.jsonl;
    # `codex-exec resume --last` resumes the newest one. ONLY the sessions dir
    # is captured — ~/.codex/auth.json is a credential and must never land in
    # a workspace checkpoint (the harness rewrites it from config each launch).
    # Locally verified 2026-07-14 (codex-cli 0.144.4): a sessions-only restore
    # into a clean CODEX_HOME resumes with full recall via `resume --last`.
    "codex": HarnessStateSpec(
        name="codex",
        paths=(
            StatePath(remote="{home}/.codex/sessions", local="codex-sessions"),
            _CWD_STATE_PATH,
        ),
        marker_glob="codex-sessions/**/*.jsonl",
    ),
}


class AgentStateSync:
    """Pull/push an agent harness's resumable session state over rsync+ssh."""

    def __init__(self, *, state_dir: Path, ssh_key_path: Path, harness: str = "claude-code") -> None:
        spec = HARNESS_STATE_SPECS.get(harness)
        if spec is None:
            raise ValueError(
                f"No agent-state spec for harness {harness!r} "
                f"(known: {sorted(HARNESS_STATE_SPECS)}) — conversation durability "
                "must be explicitly disabled for unknown harnesses, not mis-pathed"
            )
        self._spec = spec
        self._state_dir = Path(state_dir)
        self._ssh_key_path = Path(ssh_key_path)

    def _resolved_paths(self, *, cwd: str, home: str) -> list[tuple[str, Path, StatePath]]:
        subs = {"home": home, "cwd": cwd, "cwd_key": _cwd_key(cwd)}
        return [(p.remote.format(**subs), self._state_dir / p.local.format(**subs), p) for p in self._spec.paths]

    @property
    def state_dir(self) -> Path:
        return self._state_dir

    def _ssh_command(self) -> str:
        # Same invocation style as plato/transports/rsync.py, plus a connect
        # timeout so a periodic pull against a dying VM cannot wedge the loop
        # on TCP handshake.
        return (
            f"ssh -i {self._ssh_key_path} -o StrictHostKeyChecking=no "
            f"-o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o ConnectTimeout=15"
        )

    async def pull(self, hostname: str, *, cwd: str, home: str) -> bool:
        """Snapshot the VM's harness session state into ``state_dir``.

        Returns True if anything changed. Best-effort: any ssh/rsync failure
        logs a warning and returns False — the world's pull loop must never
        die because an agent VM is mid-teardown or unreachable.
        """
        pulls = self._resolved_paths(cwd=cwd, home=home)
        changed = False
        failed = False
        for remote_path, local_path, spec_path in pulls:
            try:
                changed |= await self._pull_one(hostname, remote_path, local_path, spec_path.excludes)
            except Exception:
                failed = True
                logger.warning(
                    "agent-state pull failed for %s:%s",
                    hostname,
                    remote_path,
                    exc_info=True,
                )
        if failed:
            return False

        try:
            manifest_path = self._state_dir / "manifest.json"
            if changed or not manifest_path.exists():
                self._write_manifest(manifest_path, cwd=cwd, home=home, cwd_key=_cwd_key(cwd))
        except Exception:
            logger.warning("agent-state manifest write failed", exc_info=True)
            return False
        return changed

    async def _pull_one(
        self,
        hostname: str,
        remote_path: str,
        local_path: Path,
        excludes: tuple[str, ...],
    ) -> bool:
        """Rsync one remote dir down; return True iff rsync itemized any change."""
        local_path.mkdir(parents=True, exist_ok=True)
        cmd = ["rsync", "-az", "--delete", "--itemize-changes"]
        for pattern in excludes:
            cmd.append(f"--exclude={pattern}")
        cmd.extend(["-e", self._ssh_command(), f"root@{hostname}:{remote_path}/", f"{local_path}/"])

        returncode, stdout, stderr = await self._run_rsync(cmd, timeout=_PULL_TIMEOUT_S)
        if returncode == 23 and "No such file or directory" in stderr:
            # The remote dir does not exist yet (e.g. claude has not written
            # its first transcript). Normal early in a run — not a failure.
            logger.debug("agent-state pull: %s:%s does not exist yet", hostname, remote_path)
            return False
        # 24 = source files vanished mid-transfer — expected against a live
        # session; whatever did transfer is itemized below.
        if returncode not in (0, 24):
            raise RuntimeError(f"rsync pull from {hostname}:{remote_path} failed (exit {returncode}): {stderr}")
        return any(line.strip() for line in stdout.splitlines())

    async def push(self, hostname: str, *, cwd: str, home: str) -> None:
        """Restore ``state_dir`` onto the VM (inverse of :meth:`pull`).

        Creates remote parent dirs. Raises on failure — a broken restore must
        fail the orchestrator launch loudly rather than silently start a
        fresh conversation.

        Deliberately no ``--delete``: the cwd push targets the live results
        mount, and the snapshot excludes ``data/`` and friends — a deleting
        restore would wipe them from the mount.
        """
        for remote_path, local_path, spec_path in self._resolved_paths(cwd=cwd, home=home):
            if not local_path.is_dir():
                logger.debug("agent-state push: no local %s captured, skipping", local_path)
                continue
            await self._push_one(hostname, local_path, remote_path, delete=spec_path.exact_restore)

    async def _push_one(self, hostname: str, local_path: Path, remote_path: str, *, delete: bool) -> None:
        cmd = ["rsync", "-az"]
        if delete:
            # Exact restore: the VM dir must equal the checkpoint — resume
            # picks "the newest session in the dir", so a stale file left on
            # the VM could win over the restored conversation.
            cmd.append("--delete")
        cmd += [
            "--rsync-path",
            f"mkdir -p {remote_path} && rsync",
            "-e",
            self._ssh_command(),
            f"{local_path}/",
            f"root@{hostname}:{remote_path}/",
        ]
        last_error = ""
        for attempt in range(1, _PUSH_MAX_RETRIES + 1):
            returncode, _, stderr = await self._run_rsync(cmd, timeout=_PUSH_TIMEOUT_S)
            if returncode == 0:
                return
            last_error = stderr
            if attempt < _PUSH_MAX_RETRIES:
                logger.warning(
                    "agent-state push to %s:%s failed (attempt %d/%d), retrying in %.0fs: %s",
                    hostname,
                    remote_path,
                    attempt,
                    _PUSH_MAX_RETRIES,
                    _PUSH_RETRY_DELAY_S,
                    last_error.strip(),
                )
                await asyncio.sleep(_PUSH_RETRY_DELAY_S)
        raise RuntimeError(
            f"agent-state push to {hostname}:{remote_path} failed after {_PUSH_MAX_RETRIES} attempts: {last_error}"
        )

    def has_state(self) -> bool:
        """True iff the harness's marker glob matches a captured session file."""
        if not self._state_dir.is_dir():
            return False
        return any(self._state_dir.glob(self._spec.marker_glob))

    async def _run_rsync(self, cmd: list[str], *, timeout: float) -> tuple[int, str, str]:
        """Run one rsync subprocess (transports/rsync.py invocation style) with a hard timeout."""
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        try:
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
        except TimeoutError:
            try:
                proc.kill()
            except ProcessLookupError:
                pass  # exited between timeout and kill
            await proc.wait()
            raise RuntimeError(f"rsync timed out after {timeout:.0f}s: {' '.join(cmd[:4])} ...")
        return proc.returncode or 0, stdout.decode(errors="replace"), stderr.decode(errors="replace")

    def _write_manifest(self, manifest_path: Path, *, cwd: str, home: str, cwd_key: str) -> None:
        """Atomically write ``manifest.json`` (tmp + ``os.replace``)."""
        manifest = {
            "version": ORCHESTRATOR_STATE_VERSION,
            "harness": self._spec.name,
            "cwd": cwd,
            "home": home,
            "cwd_key": cwd_key,
            "pulled_at_label": datetime.now(UTC).isoformat(),
        }
        self._state_dir.mkdir(parents=True, exist_ok=True)
        tmp_path = manifest_path.with_suffix(".json.tmp")
        tmp_path.write_text(json.dumps(manifest, indent=2) + "\n")
        os.replace(tmp_path, manifest_path)
