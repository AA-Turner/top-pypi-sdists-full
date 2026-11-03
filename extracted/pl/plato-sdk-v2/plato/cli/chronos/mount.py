"""Mount Chronos workspaces locally via a background helper.

Flow:
1. `plato chronos mount` spawns a detached daemon and returns a short alias.
2. The daemon resolves the workspace, provisions a lightweight VM, mounts lazy FUSE,
   exposes it locally, and records state in `~/plato-workspaces/.plato-mounts/state.json`.
3. `plato chronos unmount <alias>` signals the daemon to tear down the local mount,
   tunnel, and VM.
"""

from __future__ import annotations

import asyncio
import contextlib
import json
import logging
import os
import platform
import secrets
import shlex
import signal
import subprocess
import sys
import tempfile
import time
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import TypeAlias

from rich.console import Console

from plato.chronos.sdk import AsyncChronos
from plato.cli.chronos.dev.ssh import SSHKeyPair, build_ssh_command_string, wait_for_ssh_reachable
from plato.cli.chronos.settings import get_settings
from plato.v2.utils.gateway_tunnel import GatewayTunnel
from plato.worlds.dvc_models import DVCManifest, S3Config

logger = logging.getLogger(__name__)
console = Console()
settings = get_settings()

WORLD_BASE_IMAGE = "383806609161.dkr.ecr.us-west-1.amazonaws.com/vm/rootfs/plato-world-base:1.1.11"
KERNEL_NFS_PORT = 2049


MountRecord: TypeAlias = dict[str, object]
MountEvent: TypeAlias = dict[str, object]


def _utcnow_iso() -> str:
    return datetime.now(UTC).isoformat()


def _mounts_root() -> Path:
    return Path.home() / "plato-workspaces"


def _mount_state_dir() -> Path:
    return _mounts_root() / ".plato-mounts"


def _mount_state_index_path() -> Path:
    return _mount_state_dir() / "state.json"


def _mount_log_path(alias: str) -> Path:
    return _mount_state_dir() / f"{alias}.log"


def _ensure_mount_state_dir() -> Path:
    state_dir = _mount_state_dir()
    state_dir.mkdir(parents=True, exist_ok=True)
    return state_dir


def _require_root_on_macos_for_background_mounts() -> None:
    """Fail fast on macOS unless the whole CLI is running as root.

    The detached helper cannot reuse tty-scoped sudo credentials, so a plain
    `sudo -v` in the caller's shell is not enough. Requiring `sudo plato ...`
    is the only reliable behavior for the current background lifecycle.
    """
    if platform.system() != "Darwin":
        return
    if os.geteuid() == 0:
        return
    raise RuntimeError(
        "macOS workspace mounts currently require running the full command with sudo. Run: sudo plato chronos mount ..."
    )


def _ensure_sudo_ready() -> None:
    """Warm sudo credentials before handing work to the detached helper.

    The background daemon cannot prompt on the user's terminal, so any local
    mount/unmount step that relies on sudo must have a live sudo timestamp
    already available.
    """
    ready = subprocess.run(
        ["sudo", "-n", "true"],
        capture_output=True,
        text=True,
        timeout=5,
    )
    if ready.returncode == 0:
        return

    result = subprocess.run(
        ["sudo", "-v"],
        text=True,
        timeout=60,
    )
    if result.returncode != 0:
        raise RuntimeError("sudo authentication is required for local mount operations")


def _read_mount_index() -> dict[str, MountRecord]:
    index_path = _mount_state_index_path()
    if not index_path.exists():
        return {}
    data = json.loads(index_path.read_text())
    return {alias: record for alias, record in data.items()}


def _write_mount_index(records: dict[str, MountRecord]) -> None:
    _ensure_mount_state_dir()
    index_path = _mount_state_index_path()
    temp_path = index_path.with_suffix(".tmp")
    temp_path.write_text(json.dumps(records, indent=2, sort_keys=True))
    temp_path.replace(index_path)


def _record_str(record: MountRecord, key: str) -> str:
    value = record.get(key)
    if not isinstance(value, str):
        raise RuntimeError(f"Mount record field '{key}' is missing or invalid")
    return value


def _record_int(record: MountRecord, key: str) -> int | None:
    value = record.get(key)
    if value is None:
        return None
    if not isinstance(value, int):
        raise RuntimeError(f"Mount record field '{key}' is missing or invalid")
    return value


def _record_events(record: MountRecord) -> list[MountEvent]:
    value = record.get("events")
    if isinstance(value, list):
        events: list[MountEvent] = []
        for event in value:
            if isinstance(event, dict):
                events.append({str(key): item for key, item in event.items()})
        return events
    return []


def _put_mount_record(record: MountRecord) -> None:
    records = _read_mount_index()
    records[_record_str(record, "alias")] = record
    _write_mount_index(records)


def _append_mount_event(
    alias: str,
    *,
    kind: str,
    message: str,
    duration_s: float | None = None,
) -> MountEvent:
    records = _read_mount_index()
    record = records[alias]
    events = _record_events(record)
    event: MountEvent = {
        "kind": kind,
        "message": message,
        "timestamp": _utcnow_iso(),
    }
    if duration_s is not None:
        event["duration_s"] = round(duration_s, 1)
    events.append(event)
    record["events"] = events
    record["updated_at"] = _utcnow_iso()
    records[alias] = record
    _write_mount_index(records)
    return event


def _update_mount_record(alias: str, **changes: str | int | None) -> MountRecord:
    records = _read_mount_index()
    record = records[alias]
    for key, value in changes.items():
        if value is None:
            record.pop(key, None)
        else:
            record[key] = value
    record["updated_at"] = _utcnow_iso()
    records[alias] = record
    _write_mount_index(records)
    return record


def _remove_mount_record(alias: str) -> None:
    records = _read_mount_index()
    records.pop(alias, None)
    _write_mount_index(records)


def _read_mount_record(alias: str) -> MountRecord | None:
    return _read_mount_index().get(alias)


def _find_mount_record(identifier: str) -> MountRecord | None:
    records = _read_mount_index()
    record = records.get(identifier)
    if record is not None:
        return record

    for candidate in records.values():
        if candidate["mount_path"] == identifier:
            return candidate
    return None


def _allocate_mount_alias() -> str:
    existing = set(_read_mount_index())
    while True:
        alias = secrets.token_hex(3)
        if alias not in existing:
            return alias


def _default_mount_path(session_id: str, repo_name: str) -> str:
    safe_repo = repo_name.replace("/", "-")
    return str(_mounts_root() / f"{session_id[:12]}-{safe_repo}")


def _spawn_mount_daemon(
    alias: str,
    session_id: str,
    *,
    repo_name: str | None,
    step_name: str | None,
    mount_path: str | None,
    api_key: str,
    cpus: int,
    memory: int,
    disk: int,
    log_path: Path,
) -> subprocess.Popen[str]:
    daemon_cmd = [
        sys.executable,
        "-m",
        "plato.cli.chronos.mount_daemon",
        "--alias",
        alias,
        "--session-id",
        session_id,
        "--cpus",
        str(cpus),
        "--memory",
        str(memory),
        "--disk",
        str(disk),
    ]
    if repo_name is not None:
        daemon_cmd.extend(["--repo-name", repo_name])
    if step_name is not None:
        daemon_cmd.extend(["--step-name", step_name])
    if mount_path is not None:
        daemon_cmd.extend(["--mount-path", mount_path])

    env = dict(os.environ)
    env["PLATO_MOUNT_API_KEY"] = api_key

    log_handle = log_path.open("w")
    try:
        process = subprocess.Popen(
            daemon_cmd,
            stdin=subprocess.DEVNULL,
            stdout=log_handle,
            stderr=subprocess.STDOUT,
            text=True,
            env=env,
            start_new_session=True,
        )
        log_handle.close()
        return process
    except Exception:
        log_handle.close()
        raise


def _wait_for_mount_ready(
    alias: str,
    *,
    timeout_s: float = 90.0,
    on_event: Callable[[MountEvent], None] | None = None,
) -> MountRecord:
    deadline = time.monotonic() + timeout_s
    seen_events = 0
    while time.monotonic() < deadline:
        record = _read_mount_record(alias)
        if record is None:
            time.sleep(0.2)
            continue
        events = _record_events(record)
        if on_event is not None:
            for event in events[seen_events:]:
                on_event(event)
        seen_events = len(events)
        if record["status"] == "mounted":
            return record
        if record["status"] == "failed":
            error = record.get("error", "mount daemon failed")
            log_path = record.get("log_path", "")
            _remove_mount_record(alias)
            raise RuntimeError(f"{error}. See log: {log_path}")
        time.sleep(0.2)
    record = _read_mount_record(alias)
    if record is not None and record["status"] == "failed":
        error = record.get("error", "mount daemon failed")
        log_path = record.get("log_path", "")
        _remove_mount_record(alias)
        raise RuntimeError(f"{error}. See log: {log_path}")
    raise RuntimeError(f"Timed out waiting for mount {alias} to become ready")


def _process_exists(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def _cleanup_stale_mount(record: MountRecord) -> None:
    mount_dir = Path(_record_str(record, "mount_path"))
    with contextlib.suppress(Exception):
        _unmount_local_nfs(mount_dir, is_mac=platform.system() == "Darwin")
    with contextlib.suppress(OSError):
        mount_dir.rmdir()
    _remove_mount_record(_record_str(record, "alias"))


async def _resolve_workspace(
    session_id: str,
    repo_name: str | None,
    step_name: str | None,
    api_key: str,
) -> tuple[str, dict, dict, dict[str, str]]:
    """Resolve workspace ref to repo info, S3 creds, and raw DVC files.

    Returns (repo_name, ref, repo_info, creds).
    """
    chronos_url = settings.chronos_url
    async with AsyncChronos(base_url=chronos_url, api_key=api_key) as chronos:
        refs = await chronos.get_workspace_refs(session_id, repo_name=repo_name)
        if not refs:
            available = await chronos.get_workspace_refs(session_id)
            repos = sorted({r.get("repo_name", "") for r in available}) if available else []
            if repos:
                raise ValueError(f"No refs for repo '{repo_name}'. Available: {', '.join(repos)}")
            raise ValueError(f"No workspace refs found for session {session_id}")

        repo_name_resolved, ref, dvc_files = chronos._resolve_pull_context(refs, repo_name, step_name)
        repo_info = await chronos.resolve_workspace_repo(repo_name_resolved)
        creds = await chronos.get_workspace_credentials(repo_info["repo_id"])

    if not dvc_files:
        raise ValueError(f"Ref '{ref['step_name']}' has no DVC files")

    return repo_name_resolved, ref, repo_info, creds


async def _setup_fuse_on_vm(
    env,
    ssh_key: SSHKeyPair,
    repo_info: dict,
    creds: dict[str, str],
    dvc_files: dict[str, str],
    workspace_path: str = "/mnt/workspace",
) -> int:
    """Prepare the manifest locally, then start plato-fuse directly on the VM."""
    cache_dir = "/tmp/plato-lazy-cache"
    config_path = f"{cache_dir}/config.json"
    workspace_path_quoted = shlex.quote(workspace_path)
    cache_dir_quoted = shlex.quote(cache_dir)
    config_path_quoted = shlex.quote(config_path)

    s3_creds = {k: v for k, v in creds.items() if k.startswith("AWS_")}
    dvc_content = next(iter(dvc_files.values()))
    s3_config = S3Config(
        bucket=repo_info["s3_bucket"],
        prefix=repo_info["s3_prefix"],
        credentials=s3_creds,
    )

    manifest = await DVCManifest.from_dvc_file(
        dvc_content,
        s3_config,
    )
    file_count = len(manifest.entries_list)

    config_json = json.dumps(
        {
            "manifest": manifest.to_dict(),
            "s3_config": s3_config.to_dict(),
            "mountpoint": workspace_path,
            "cache_dir": cache_dir,
        }
    )

    result = await env.execute(
        " && ".join(
            [
                f"mkdir -p {workspace_path_quoted} {cache_dir_quoted}/overlay {cache_dir_quoted}/cache",
                f"rm -f {cache_dir_quoted}/live-meta.json {cache_dir_quoted}/live-dir-renames.json {config_path_quoted}",
            ]
        ),
        timeout=10,
    )
    if result.exit_code != 0:
        raise RuntimeError(f"Failed to create directories: {result.stderr}")

    await asyncio.to_thread(
        _upload_remote_file_via_rsync,
        env.job_id,
        ssh_key.private_key_path,
        cache_dir,
        config_path,
        config_json,
    )

    result = await env.execute(
        'if [ -n "${PLATO_FUSE_BINARY:-}" ] && [ -x "${PLATO_FUSE_BINARY}" ]; then '
        'printf "%s\\n" "${PLATO_FUSE_BINARY}"; '
        "else command -v plato-fuse; fi",
        timeout=10,
    )
    if result.exit_code != 0:
        raise RuntimeError(f"Failed to resolve plato-fuse on VM: {result.stderr}")
    rust_binary = (result.stdout or "").strip().splitlines()
    if not rust_binary:
        raise RuntimeError("plato-fuse binary not found on VM")
    resolved_binary = rust_binary[-1].strip()

    launch = await env.execute(
        f"nohup {shlex.quote(resolved_binary)} {config_path_quoted} >/tmp/plato-fuse.log 2>&1 </dev/null &",
        timeout=10,
    )
    if launch.exit_code != 0:
        raise RuntimeError(f"Failed to launch plato-fuse: {launch.stderr}")

    verify = await env.execute(
        f"for i in $(seq 1 300); do mountpoint -q {workspace_path_quoted} && exit 0; sleep 0.1; done; exit 1",
        timeout=40,
    )
    if verify.exit_code != 0:
        log_result = await env.execute("cat /tmp/plato-fuse.log 2>/dev/null || true", timeout=5)
        log_output = (log_result.stdout or "").strip() if log_result.exit_code == 0 else "unavailable"
        raise RuntimeError(f"FUSE mount not present at {workspace_path}. Logs: {log_output}")

    return file_count


def _upload_remote_file_via_rsync(
    job_id: str,
    private_key_path: Path,
    remote_dir: str,
    remote_path: str,
    contents: str,
) -> None:
    remote_dir_quoted = shlex.quote(remote_dir)
    ssh_cmd = build_ssh_command_string(job_id, private_key_path)
    host = f"root@{job_id}.plato"

    with tempfile.TemporaryDirectory(prefix="plato-mount-config-") as temp_dir:
        local_path = Path(temp_dir) / Path(remote_path).name
        local_path.write_text(contents)
        result = subprocess.run(
            [
                "rsync",
                "-az",
                "--rsync-path",
                f"mkdir -p {remote_dir_quoted} && rsync",
                "-e",
                ssh_cmd,
                str(local_path),
                f"{host}:{remote_path}",
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )
    if result.returncode != 0:
        error = (result.stderr or result.stdout or "").strip()
        raise RuntimeError(f"Failed to upload FUSE config: {error}")


async def _setup_kernel_nfs_on_vm(env, workspace_path: str = "/mnt/workspace") -> None:
    """Start Linux kernel nfsd on the VM for the FUSE-mounted workspace."""
    setup_cmd = (
        "which exportfs > /dev/null 2>&1 || "
        "(apt-get update -qq && apt-get install -y -qq nfs-kernel-server nfs-common rpcbind) && "
        f"printf '%s\\n' '{workspace_path} *(rw,sync,fsid=0,no_subtree_check,no_root_squash,insecure)' > /etc/exports && "
        "modprobe nfsd 2>/dev/null || true && "
        "mkdir -p /proc/fs/nfsd && "
        "mountpoint -q /proc/fs/nfsd || mount -t nfsd nfsd /proc/fs/nfsd && "
        "systemctl start rpcbind || true && "
        "exportfs -ra && "
        "systemctl start nfs-kernel-server || true && "
        "rpc.nfsd 8 2>/dev/null || true"
    )
    result = await env.execute(setup_cmd, timeout=120)
    if result.exit_code != 0:
        raise RuntimeError(f"Failed to start kernel NFS server: {result.stderr}")

    verify = await env.execute("rpcinfo -p 127.0.0.1 | grep -q '100003.*2049'", timeout=10)
    if verify.exit_code != 0:
        raise RuntimeError("Kernel NFS server did not register on port 2049")


def _mount_local_nfs(mount_dir: Path, local_port: int, is_mac: bool, *, vers: int | None = None) -> None:
    """Mount the tunneled NFS export locally."""
    if is_mac:
        nfs_opts = f"port={local_port},tcp,resvport,intr,retrycnt=0"
        if vers is not None:
            nfs_opts = f"vers={vers}," + nfs_opts
        mount_cmd = ["mount_nfs", "-o", nfs_opts, "127.0.0.1:/", str(mount_dir)]
    else:
        if vers == 4:
            nfs_opts = f"vers=4,port={local_port},tcp"
        else:
            nfs_opts = f"port={local_port},mountport={local_port},tcp"
            if vers is not None:
                nfs_opts = f"vers={vers}," + nfs_opts
        mount_cmd = ["mount", "-t", "nfs", "-o", nfs_opts, "127.0.0.1:/", str(mount_dir)]

    attempts = 5 if is_mac else 1
    last_error = ""
    for attempt in range(attempts):
        try:
            result = subprocess.run(
                ["sudo", "-n"] + mount_cmd,
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode == 0:
                return
            last_error = (result.stderr or "").strip()
            if (
                is_mac
                and ("Connection refused" in last_error or "Operation timed out" in last_error)
                and attempt < attempts - 1
            ):
                time.sleep(0.5)
                continue
            raise RuntimeError(f"NFS mount failed: {last_error}")
        except subprocess.TimeoutExpired:
            if is_mac and attempt < attempts - 1:
                time.sleep(0.5)
                continue
            raise RuntimeError(
                "NFS mount timed out after 30s. The tunnel may not be passing NFS traffic correctly."
            ) from None

    raise RuntimeError(f"NFS mount failed: {last_error}")


async def _mount_local_nfs_async(mount_dir: Path, local_port: int, is_mac: bool, *, vers: int | None = None) -> None:
    await asyncio.to_thread(_mount_local_nfs, mount_dir, local_port, is_mac, vers=vers)


def _unmount_local_nfs(mount_dir: Path, is_mac: bool) -> None:
    """Run the blocking local NFS unmount."""
    if is_mac:
        attempts = [
            ["sudo", "-n", "umount", str(mount_dir)],
            ["sudo", "-n", "umount", "-f", str(mount_dir)],
            ["diskutil", "unmount", "force", str(mount_dir)],
        ]
    else:
        attempts = [["sudo", "-n", "umount", str(mount_dir)]]

    last_error = ""
    for cmd in attempts:
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=15,
            )
            if result.returncode == 0:
                return
            last_error = ((result.stderr or "") or (result.stdout or "")).strip()
        except subprocess.TimeoutExpired:
            last_error = f"{cmd[0]} timed out"

    raise RuntimeError(last_error or f"Failed to unmount {mount_dir}")


async def _unmount_local_nfs_async(mount_dir: Path, is_mac: bool) -> None:
    await asyncio.to_thread(_unmount_local_nfs, mount_dir, is_mac)


def start_mount_daemon(
    session_id: str,
    *,
    repo_name: str | None = None,
    step_name: str | None = None,
    mount_path: str | None = None,
    api_key: str | None = None,
    cpus: int = 1,
    memory: int = 2048,
    disk: int = 10240,
    on_event: Callable[[MountEvent], None] | None = None,
) -> MountRecord:
    """Start a background workspace mount daemon and wait for readiness."""
    resolved_api_key = api_key or os.environ.get("PLATO_API_KEY")
    if not resolved_api_key:
        raise ValueError("PLATO_API_KEY required")

    _require_root_on_macos_for_background_mounts()
    _ensure_sudo_ready()
    _ensure_mount_state_dir()
    alias = _allocate_mount_alias()
    now = _utcnow_iso()
    log_path = _mount_log_path(alias)
    record: MountRecord = {
        "alias": alias,
        "status": "starting",
        "session_id": session_id,
        "repo_name": repo_name,
        "step_name": step_name,
        "mount_path": mount_path or "",
        "log_path": str(log_path),
        "created_at": now,
        "updated_at": now,
    }
    _put_mount_record(record)

    process = _spawn_mount_daemon(
        alias,
        session_id,
        repo_name=repo_name,
        step_name=step_name,
        mount_path=mount_path,
        api_key=resolved_api_key,
        cpus=cpus,
        memory=memory,
        disk=disk,
        log_path=log_path,
    )
    _update_mount_record(alias, pid=process.pid)
    return _wait_for_mount_ready(alias, on_event=on_event)


def unmount_workspace(identifier: str, *, timeout_s: float = 45.0) -> None:
    """Stop a background mount by alias or mount path."""
    record = _find_mount_record(identifier)
    if record is None:
        raise ValueError(f"No active mount found for '{identifier}'")

    _require_root_on_macos_for_background_mounts()
    _ensure_sudo_ready()
    alias = _record_str(record, "alias")
    pid = _record_int(record, "pid")
    if pid is not None and _process_exists(pid):
        with contextlib.suppress(ProcessLookupError):
            os.kill(pid, signal.SIGTERM)

    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        current = _read_mount_record(alias)
        if current is None:
            return
        if current["status"] == "failed":
            if pid is None or not _process_exists(pid):
                _cleanup_stale_mount(current)
                return
        if pid is not None and not _process_exists(pid):
            _cleanup_stale_mount(current)
            return
        time.sleep(0.2)

    current = _read_mount_record(alias)
    if current is not None and (pid is None or not _process_exists(pid)):
        _cleanup_stale_mount(current)
        return
    raise RuntimeError(f"Timed out waiting for mount {alias} to stop")


async def run_mount_daemon(
    alias: str,
    session_id: str,
    *,
    repo_name: str | None = None,
    step_name: str | None = None,
    mount_path: str | None = None,
    api_key: str | None = None,
    cpus: int = 1,
    memory: int = 2048,
    disk: int = 10240,
) -> None:
    """Run the long-lived mount helper process."""
    resolved_api_key = api_key or os.environ.get("PLATO_MOUNT_API_KEY") or os.environ.get("PLATO_API_KEY")
    if not resolved_api_key:
        raise ValueError("PLATO_API_KEY required")

    record = _read_mount_record(alias)
    if record is None:
        raise RuntimeError(f"Mount state for alias {alias} not found")

    _update_mount_record(alias, pid=os.getpid())

    from plato.v2 import AsyncPlato, Env
    from plato.v2.types import SimConfigCompute

    plato_client = AsyncPlato(api_key=resolved_api_key)
    session = None
    tunnel: GatewayTunnel | None = None
    ssh_key: SSHKeyPair | None = None
    mount_dir: Path | None = None
    transport = ""
    mounted = False
    is_mac = platform.system() == "Darwin"
    workspace_path = "/mnt/workspace"

    stop_event = asyncio.Event()
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        with contextlib.suppress(NotImplementedError):
            loop.add_signal_handler(sig, stop_event.set)

    try:
        started_at = time.monotonic()
        _append_mount_event(alias, kind="start", message="Resolving workspace")
        repo_name_resolved, ref, repo_info, creds = await _resolve_workspace(
            session_id, repo_name, step_name, resolved_api_key
        )
        step = ref.get("step_name", "")
        dvc_files = ref.get("dvc_files", {})
        _append_mount_event(
            alias,
            kind="done",
            message=f"Resolved [bold]{repo_name_resolved}[/bold] @ {step}",
            duration_s=time.monotonic() - started_at,
        )

        resolved_mount_path = mount_path or _default_mount_path(session_id, repo_name_resolved)
        mount_dir = Path(resolved_mount_path)
        mount_dir.mkdir(parents=True, exist_ok=True)
        _update_mount_record(
            alias,
            repo_name=repo_name_resolved,
            step_name=step,
            mount_path=str(mount_dir),
        )

        started_at = time.monotonic()
        _append_mount_event(alias, kind="start", message="Creating VM")
        session = await plato_client.sessions.create(
            envs=[
                Env.resource(
                    "workspace-mount",
                    SimConfigCompute(cpus=cpus, memory=memory, disk=disk),
                    docker_image_url=WORLD_BASE_IMAGE,
                    upload_rootfs=False,
                    rootfs_storage_backend="snapshot-store",
                )
            ],
        )
        await session.start_heartbeat()
        env = session.envs[0]
        _update_mount_record(alias, vm_job_id=env.job_id)
        _append_mount_event(
            alias,
            kind="done",
            message=f"VM [bold]{env.job_id}[/bold] created",
            duration_s=time.monotonic() - started_at,
        )

        started_at = time.monotonic()
        _append_mount_event(alias, kind="start", message="Waiting for SSH")
        ssh_key = SSHKeyPair.generate()
        await session.add_ssh_key(ssh_key.public_key)
        reachable = await wait_for_ssh_reachable(env.job_id, ssh_key.private_key_path)
        if not reachable:
            raise RuntimeError("SSH gateway not reachable")
        _append_mount_event(alias, kind="done", message="SSH connected", duration_s=time.monotonic() - started_at)

        started_at = time.monotonic()
        _append_mount_event(alias, kind="start", message="Setting up lazy FUSE mount")
        file_count = await _setup_fuse_on_vm(
            env,
            ssh_key,
            repo_info,
            creds,
            dvc_files,
            workspace_path,
        )
        _append_mount_event(
            alias,
            kind="done",
            message=f"FUSE mounted ({file_count} files available lazily)",
            duration_s=time.monotonic() - started_at,
        )

        started_at = time.monotonic()
        _append_mount_event(alias, kind="start", message="Starting kernel NFS server")
        await _setup_kernel_nfs_on_vm(env, workspace_path)
        _append_mount_event(
            alias,
            kind="done",
            message="Kernel NFS server running",
            duration_s=time.monotonic() - started_at,
        )

        started_at = time.monotonic()
        _append_mount_event(alias, kind="start", message="Opening gateway tunnel")
        tunnel = GatewayTunnel(job_id=env.job_id, remote_port=KERNEL_NFS_PORT, local_port=0)
        await tunnel.start()
        _append_mount_event(
            alias,
            kind="done",
            message=f"Gateway tunnel open (nfs4=:{tunnel.local_port})",
            duration_s=time.monotonic() - started_at,
        )

        started_at = time.monotonic()
        _append_mount_event(alias, kind="start", message=f"Mounting NFS at [bold]{mount_dir}[/bold]")
        await _mount_local_nfs_async(mount_dir, tunnel.local_port, is_mac=is_mac, vers=4)
        transport = "nfs"
        _append_mount_event(
            alias,
            kind="done",
            message=f"NFS mounted at [bold]{mount_dir}[/bold]",
            duration_s=time.monotonic() - started_at,
        )

        mounted = True
        _update_mount_record(
            alias,
            status="mounted",
            transport=transport,
            file_count=file_count,
            error=None,
        )
        await stop_event.wait()
    except Exception as exc:
        logger.exception("Mount daemon failed for %s", alias)
        _update_mount_record(alias, status="failed", error=str(exc))
        raise
    finally:
        cleanup_error: str | None = None

        if mounted and mount_dir is not None:
            _update_mount_record(alias, status="stopping")
            try:
                await _unmount_local_nfs_async(mount_dir, is_mac=is_mac)
            except Exception as exc:
                cleanup_error = f"Failed to unmount {mount_dir}: {exc}"
            with contextlib.suppress(OSError):
                mount_dir.rmdir()

        if tunnel is not None:
            with contextlib.suppress(Exception):
                await tunnel.stop()

        if session is not None:
            with contextlib.suppress(Exception):
                await session.close()

        with contextlib.suppress(Exception):
            await plato_client.close()

        if cleanup_error is not None:
            _update_mount_record(alias, status="failed", error=cleanup_error)
            return

        current = _read_mount_record(alias)
        if current is not None and current.get("status") != "failed":
            with contextlib.suppress(Exception):
                _remove_mount_record(alias)
