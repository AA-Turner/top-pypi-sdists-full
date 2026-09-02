"""Process + listening-socket enumeration (scan PHASE 12, Source A + Source B).

Two independent enumeration sources, unioned by pid:

* **Source A -- process table**: macOS/BSD ``ps``, Linux ``/proc/<pid>/*``,
  Windows ``Get-CimInstance Win32_Process``.
* **Source B -- listening sockets -> owning pid**: macOS ``lsof``, Linux
  ``/proc/net/tcp{,6}`` joined to ``/proc/<pid>/fd`` by socket inode, Windows
  ``netstat -ano``.

Port listening is a first-class source, not just a correlation signal: it is the
only way to see a config-less HTTP/SSE MCP server or agent gateway that no config
file (or client parent) reveals.

Everything here is best-effort and must never raise into the scan: each backend
is wrapped so a missing tool, a permission error, or malformed output yields an
empty result rather than aborting the scan. Every subprocess is bounded by a
timeout. The parsers are pure functions (text/data -> records) so they are unit
tested without a live subprocess.

Standard-library only (``subprocess`` to OS tools, ``os``/``pathlib`` for
``/proc``) so this stays inside the frozen ``aiwatch`` bundle -- no ``psutil``.
"""

from __future__ import annotations

import json
import os
import platform
import subprocess
import time
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from pathlib import Path

import structlog

from runlayer_cli.scan.device import DiscoveredWSLDistro
from runlayer_cli.scan.processes.models import BindScope, ProcessCandidate
from runlayer_cli.scan.wsl_exec import WSL_PS_ARGS, run_wsl_command
from runlayer_cli.scan.wsl_limits import MAX_WSL_DISTROS

logger = structlog.get_logger(__name__)

# Bound every OS-tool subprocess. Enumeration is a best-effort side channel; a
# hung tool must never stall the scan.
SUBPROCESS_TIMEOUT_S = 5
WSL_PROCESS_SCAN_TIME_BUDGET_S = 30.0

# Defensive caps: a pathological host (thousands of processes) must not produce
# an unbounded candidate set or per-process port list.
MAX_CANDIDATES = 4000
MAX_PORTS_PER_PROCESS = 32

_LOOPBACK_HOSTS = frozenset({"127.0.0.1", "::1", "localhost"})
_ALL_INTERFACES_HOSTS = frozenset({"*", "0.0.0.0", "::", ""})


@dataclass(frozen=True)
class ListenerSocket:
    """One listening TCP socket resolved to its owning pid."""

    pid: int
    port: int
    bind_scope: BindScope


# ---------------------------------------------------------------------------
# Bind-scope helpers
# ---------------------------------------------------------------------------
def bind_scope_from_host(host: str) -> BindScope:
    """Classify a textual bind host as loopback vs all-interfaces.

    A specific non-loopback address is treated as ``all_interfaces`` for scope
    purposes (it is reachable off-loopback); only 127.x / ::1 / localhost are
    loopback.
    """
    h = host.strip().strip("[]").lower()
    if h in _LOOPBACK_HOSTS or h.startswith("127."):
        return "loopback"
    if h in _ALL_INTERFACES_HOSTS:
        return "all_interfaces"
    return "all_interfaces"


def bind_scope_from_hex_ip(ip_hex: str) -> BindScope:
    """Classify a ``/proc/net/tcp`` hex-encoded local address.

    IPv4 addresses are 8 hex chars stored little-endian; IPv6 addresses are 32
    hex chars stored as four little-endian 32-bit words. Loopback is 127.x /
    ``::1``; the all-zero address is all-interfaces; anything else is treated as
    all-interfaces.
    """
    try:
        raw = bytes.fromhex(ip_hex)
    except ValueError:
        return "all_interfaces"
    if len(raw) == 4:
        octets = raw[::-1]
        if octets[0] == 127:
            return "loopback"
        return "all_interfaces"
    if len(raw) == 16:
        words = [raw[i : i + 4][::-1] for i in range(0, 16, 4)]
        addr = b"".join(words)
        if addr == b"\x00" * 15 + b"\x01":
            return "loopback"
        return "all_interfaces"
    return "all_interfaces"


def _merge_bind_scope(current: BindScope, incoming: BindScope) -> BindScope:
    """Combine two scopes, widening toward the more exposed one."""
    order = {"none": 0, "loopback": 1, "all_interfaces": 2}
    return current if order[current] >= order[incoming] else incoming


def _parse_host_port(value: str) -> tuple[int, BindScope] | None:
    """Parse a ``host:port`` (or ``[::1]:port``) into ``(port, scope)``.

    Returns ``None`` when there is no numeric port (e.g. ``*:*``) or the value
    is an established-connection name (``a->b``), which listeners never are.
    """
    if "->" in value:
        return None
    host, sep, port_str = value.rpartition(":")
    if not sep or not port_str.isdigit():
        return None
    return int(port_str), bind_scope_from_host(host)


# ---------------------------------------------------------------------------
# Source A parsers -- process table
# ---------------------------------------------------------------------------
def parse_ps_table(text: str) -> list[ProcessCandidate]:
    """Parse ``ps -axww -o pid=,ppid=,user:32=,lstart=,args=`` output.

    ``lstart`` is a fixed five-token timestamp (``Wed Jul 15 09:27:01 2026``), so
    the leading eight whitespace tokens are ``pid ppid user <5-token lstart>``
    and everything after is the command line -- split with ``maxsplit=8`` so the
    args keep their internal spacing as one string, then tokenized.
    """
    candidates: list[ProcessCandidate] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        fields = line.split(None, 8)
        if len(fields) < 8:
            continue
        try:
            pid = int(fields[0])
            ppid = int(fields[1])
        except ValueError:
            continue
        user = fields[2]
        started_at = " ".join(fields[3:8])
        args_str = fields[8] if len(fields) >= 9 else ""
        argv = args_str.split()
        exe = argv[0] if argv else None
        candidates.append(
            ProcessCandidate(
                pid=pid,
                ppid=ppid,
                exe=exe,
                argv=argv,
                user=user,
                started_at=started_at or None,
                discovery_source="proc_table",
            )
        )
    return candidates


def parse_linux_proc_status(text: str) -> tuple[int | None, str | None]:
    """Extract ``(ppid, uid)`` from ``/proc/<pid>/status`` text.

    ``uid`` is the effective uid (second field of the ``Uid:`` line), returned
    as a string for parity with the other backends.
    """
    ppid: int | None = None
    uid: str | None = None
    for line in text.splitlines():
        if line.startswith("PPid:"):
            value = line.split(":", 1)[1].strip()
            if value.isdigit():
                ppid = int(value)
        elif line.startswith("Uid:"):
            parts = line.split()
            if len(parts) >= 3:
                uid = parts[2]
    return ppid, uid


def _decode_proc_cmdline(raw: bytes) -> list[str]:
    """Split a NUL-delimited ``/proc/<pid>/cmdline`` into an argv list."""
    return [tok.decode("utf-8", "replace") for tok in raw.split(b"\x00") if tok]


def _read_linux_pid(pid_dir: Path, pid: int) -> ProcessCandidate | None:
    """Read one ``/proc/<pid>`` entry into a candidate (best-effort)."""
    try:
        cmdline = (pid_dir / "cmdline").read_bytes()
    except OSError:
        return None
    argv = _decode_proc_cmdline(cmdline)
    ppid: int | None = None
    user: str | None = None
    try:
        ppid, user = parse_linux_proc_status((pid_dir / "status").read_text())
    except OSError:
        pass
    exe: str | None = None
    try:
        exe = os.readlink(pid_dir / "exe")
    except OSError:
        exe = argv[0] if argv else None
    cwd: str | None = None
    try:
        cwd = os.readlink(pid_dir / "cwd")
    except OSError:
        cwd = None
    if not argv and exe:
        argv = [exe]
    return ProcessCandidate(
        pid=pid,
        ppid=ppid,
        exe=exe,
        argv=argv,
        user=user,
        cwd=cwd,
        discovery_source="proc_table",
    )


def _enumerate_linux_proc() -> list[ProcessCandidate]:
    candidates: list[ProcessCandidate] = []
    proc = Path("/proc")
    try:
        entries = list(proc.iterdir())
    except OSError:
        return candidates
    for entry in entries:
        if not entry.name.isdigit():
            continue
        try:
            candidate = _read_linux_pid(entry, int(entry.name))
        except OSError:
            continue
        if candidate is not None:
            candidates.append(candidate)
        if len(candidates) >= MAX_CANDIDATES:
            break
    return candidates


def _tokenize_windows_cmdline(cmdline: str) -> list[str]:
    """Split a Windows command line into argv, honoring double-quoted spans.

    A minimal tokenizer: whitespace separates tokens except inside double
    quotes. Sufficient for correlation/redaction (we do not need exact CRT
    argv semantics); the raw string is never retained.
    """
    tokens: list[str] = []
    current: list[str] = []
    in_quotes = False
    for ch in cmdline:
        if ch == '"':
            in_quotes = not in_quotes
        elif ch.isspace() and not in_quotes:
            if current:
                tokens.append("".join(current))
                current = []
        else:
            current.append(ch)
    if current:
        tokens.append("".join(current))
    return tokens


def parse_windows_cim(text: str) -> list[ProcessCandidate]:
    """Parse ``Get-CimInstance Win32_Process | ConvertTo-Json`` output.

    PowerShell emits a JSON object for a single process and a JSON array for
    many, so both shapes are accepted. Owner (user) is intentionally not
    resolved here -- ``GetOwner()`` is a per-process WMI call that is too costly
    for a poll and is deferred; ``user`` stays ``None`` on Windows for v1.
    """
    try:
        data = json.loads(text)
    except (ValueError, TypeError):
        return []
    if isinstance(data, dict):
        data = [data]
    if not isinstance(data, list):
        return []
    candidates: list[ProcessCandidate] = []
    for item in data:
        if not isinstance(item, dict):
            continue
        pid = item.get("ProcessId")
        if not isinstance(pid, int):
            continue
        ppid_raw = item.get("ParentProcessId")
        ppid = ppid_raw if isinstance(ppid_raw, int) else None
        name = item.get("Name") if isinstance(item.get("Name"), str) else None
        cmdline = item.get("CommandLine")
        if isinstance(cmdline, str) and cmdline.strip():
            argv = _tokenize_windows_cmdline(cmdline)
        elif name:
            argv = [name]
        else:
            argv = []
        exe = argv[0] if argv else name
        candidates.append(
            ProcessCandidate(
                pid=pid,
                ppid=ppid,
                exe=exe,
                argv=argv,
                discovery_source="proc_table",
            )
        )
        if len(candidates) >= MAX_CANDIDATES:
            break
    return candidates


# ---------------------------------------------------------------------------
# Source B parsers -- listening sockets
# ---------------------------------------------------------------------------
def parse_lsof(text: str) -> list[ListenerSocket]:
    """Parse ``lsof -nP -iTCP -sTCP:LISTEN -Fpn`` field output.

    ``-F`` emits one field per line: ``p<pid>`` starts a process set, and each
    following ``n<name>`` is a socket name (``127.0.0.1:3000`` / ``*:8080`` /
    ``[::1]:5000``) belonging to that pid.
    """
    listeners: list[ListenerSocket] = []
    pid: int | None = None
    for line in text.splitlines():
        if not line:
            continue
        tag, value = line[0], line[1:]
        if tag == "p":
            pid = int(value) if value.isdigit() else None
        elif tag == "n" and pid is not None:
            parsed = _parse_host_port(value)
            if parsed is not None:
                port, scope = parsed
                listeners.append(ListenerSocket(pid=pid, port=port, bind_scope=scope))
    return listeners


def parse_proc_net_tcp(text: str) -> list[tuple[int, int, BindScope]]:
    """Parse ``/proc/net/tcp{,6}`` LISTEN rows into ``(inode, port, scope)``.

    Column layout (whitespace-separated, first line is a header): index 1 is the
    local ``HEXIP:HEXPORT`` address, index 3 is the connection state (``0A`` is
    LISTEN), and index 9 is the socket inode used to join to ``/proc/<pid>/fd``.
    """
    rows: list[tuple[int, int, BindScope]] = []
    for line in text.splitlines()[1:]:
        parts = line.split()
        if len(parts) < 10:
            continue
        if parts[3] != "0A":
            continue
        local = parts[1]
        if ":" not in local:
            continue
        ip_hex, _, port_hex = local.rpartition(":")
        try:
            port = int(port_hex, 16)
            inode = int(parts[9])
        except ValueError:
            continue
        rows.append((inode, port, bind_scope_from_hex_ip(ip_hex)))
    return rows


def parse_netstat(text: str) -> list[ListenerSocket]:
    """Parse Windows ``netstat -ano`` LISTENING TCP rows.

    Row shape: ``TCP  <local>  <foreign>  LISTENING  <pid>``. UDP has no state
    column and is skipped; only TCP LISTENING rows with a numeric pid are kept.
    """
    listeners: list[ListenerSocket] = []
    for line in text.splitlines():
        parts = line.split()
        if len(parts) < 5:
            continue
        if parts[0].upper() != "TCP":
            continue
        if parts[3].upper() != "LISTENING":
            continue
        pid_str = parts[4]
        if not pid_str.isdigit():
            continue
        parsed = _parse_host_port(parts[1])
        if parsed is None:
            continue
        port, scope = parsed
        listeners.append(ListenerSocket(pid=int(pid_str), port=port, bind_scope=scope))
    return listeners


def _build_inode_pid_index() -> dict[int, int]:
    """Map socket inode -> owning pid by scanning ``/proc/<pid>/fd`` symlinks.

    Each fd is a symlink; socket fds point at ``socket:[<inode>]``. Best-effort:
    pids/fds that vanish or deny access mid-scan are skipped.
    """
    index: dict[int, int] = {}
    proc = Path("/proc")
    try:
        entries = list(proc.iterdir())
    except OSError:
        return index
    for entry in entries:
        if not entry.name.isdigit():
            continue
        pid = int(entry.name)
        fd_dir = entry / "fd"
        try:
            fds = list(fd_dir.iterdir())
        except OSError:
            continue
        for fd in fds:
            try:
                target = os.readlink(fd)
            except OSError:
                continue
            if target.startswith("socket:["):
                try:
                    inode = int(target[len("socket:[") : -1])
                except ValueError:
                    continue
                index.setdefault(inode, pid)
    return index


# ---------------------------------------------------------------------------
# Best-effort OS-tool runners
# ---------------------------------------------------------------------------
def _run(cmd: list[str], *, timeout: int) -> str | None:
    """Run an OS tool, returning stdout or ``None`` on any failure."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0 and not result.stdout:
        return None
    return result.stdout


def _enumerate_ps(timeout: int) -> list[ProcessCandidate]:
    output = _run(
        ["/bin/ps", "-axww", "-o", "pid=,ppid=,user=,lstart=,args="],
        timeout=timeout,
    )
    if output is None:
        output = _run(
            ["ps", "-axww", "-o", "pid=,ppid=,user=,lstart=,args="],
            timeout=timeout,
        )
    if output is None:
        return []
    candidates = parse_ps_table(output)[:MAX_CANDIDATES]
    for candidate in candidates:
        if candidate.exe is None:
            continue
        executable = Path(candidate.exe)
        try:
            if executable.is_absolute() and executable.is_symlink():
                candidate.exe = str(executable.resolve(strict=True))
        except OSError:
            continue
    return candidates


def _enumerate_windows_processes(timeout: int) -> list[ProcessCandidate]:
    output = _run(
        [
            "powershell",
            "-NoProfile",
            "-NonInteractive",
            "-Command",
            "Get-CimInstance Win32_Process | "
            "Select-Object ProcessId,ParentProcessId,Name,CommandLine | "
            "ConvertTo-Json -Compress",
        ],
        timeout=timeout,
    )
    if output is None:
        return []
    return parse_windows_cim(output)


def _listeners_lsof(timeout: int) -> list[ListenerSocket]:
    output = _run(
        ["lsof", "-nP", "-iTCP", "-sTCP:LISTEN", "-Fpn"],
        timeout=timeout,
    )
    if output is None:
        return []
    return parse_lsof(output)


def _listeners_linux() -> list[ListenerSocket]:
    rows: list[tuple[int, int, BindScope]] = []
    for name in ("tcp", "tcp6"):
        try:
            text = Path("/proc/net", name).read_text()
        except OSError:
            continue
        rows.extend(parse_proc_net_tcp(text))
    if not rows:
        return []
    inode_pid = _build_inode_pid_index()
    listeners: list[ListenerSocket] = []
    for inode, port, scope in rows:
        pid = inode_pid.get(inode)
        if pid is not None:
            listeners.append(ListenerSocket(pid=pid, port=port, bind_scope=scope))
    return listeners


def _listeners_netstat(timeout: int) -> list[ListenerSocket]:
    output = _run(["netstat", "-ano", "-p", "TCP"], timeout=timeout)
    if output is None:
        output = _run(["netstat", "-ano"], timeout=timeout)
    if output is None:
        return []
    return parse_netstat(output)


# ---------------------------------------------------------------------------
# Public entry points
# ---------------------------------------------------------------------------
def enumerate_process_table(
    *, timeout: int = SUBPROCESS_TIMEOUT_S
) -> list[ProcessCandidate]:
    """Source A: enumerate the process table for the current platform."""
    system = platform.system()
    try:
        if system == "Linux":
            return _enumerate_linux_proc()
        if system == "Windows":
            return _enumerate_windows_processes(timeout)
        return _enumerate_ps(timeout)
    except Exception as exc:  # never raise into the scan
        logger.debug("process_table_enumeration_failed", error=str(exc))
        return []


def enumerate_wsl_process_tables(
    distros: Iterable[DiscoveredWSLDistro],
    *,
    timeout: int = SUBPROCESS_TIMEOUT_S,
    checkpoint: Callable[[], None] | None = None,
) -> list[ProcessCandidate]:
    """Enumerate process tables of bounded running WSL distros."""
    candidates: list[ProcessCandidate] = []
    deadline = time.monotonic() + WSL_PROCESS_SCAN_TIME_BUDGET_S
    for distro in tuple(distros)[:MAX_WSL_DISTROS]:
        if time.monotonic() >= deadline:
            break
        if not distro.is_running or distro.name.casefold() == "docker-desktop":
            continue
        if checkpoint is not None:
            checkpoint()
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            break
        try:
            result = run_wsl_command(
                distro.name,
                ("ps", *WSL_PS_ARGS),
                timeout=min(timeout, remaining),
            )
        except Exception as exc:
            logger.debug(
                "wsl_process_table_enumeration_failed",
                distro=distro.name,
                error=str(exc),
            )
            continue
        if result is None:
            continue
        distro_candidates = parse_ps_table(result.stdout)
        for candidate in distro_candidates:
            candidate.wsl_distro = distro.name
            candidates.append(candidate)
            if len(candidates) >= MAX_CANDIDATES:
                return candidates
    return candidates


def enumerate_listeners(*, timeout: int = SUBPROCESS_TIMEOUT_S) -> list[ListenerSocket]:
    """Source B: enumerate listening TCP sockets -> owning pid."""
    system = platform.system()
    try:
        if system == "Linux":
            return _listeners_linux()
        if system == "Windows":
            return _listeners_netstat(timeout)
        return _listeners_lsof(timeout)
    except Exception as exc:  # never raise into the scan
        logger.debug("listener_enumeration_failed", error=str(exc))
        return []


def union_by_pid(
    processes: list[ProcessCandidate],
    listeners: list[ListenerSocket],
) -> list[ProcessCandidate]:
    """Union Source A + Source B by pid.

    A listener whose pid is in the process table folds its port + bind scope
    into that candidate. A listener whose pid is *not* in the table (Source B
    saw a process Source A missed -- e.g. a race, or a restricted process that
    still owns a socket) becomes a bare ``listening_port`` candidate so the
    config-less HTTP server is still surfaced.
    """
    by_pid: dict[int, ProcessCandidate] = {}
    for candidate in processes:
        # First writer wins on duplicate pids (shouldn't happen, but be safe).
        by_pid.setdefault(candidate.pid, candidate)

    for listener in listeners:
        candidate = by_pid.get(listener.pid)
        if candidate is None:
            candidate = ProcessCandidate(
                pid=listener.pid,
                discovery_source="listening_port",
            )
            by_pid[listener.pid] = candidate
        if (
            listener.port not in candidate.listening_ports
            and len(candidate.listening_ports) < MAX_PORTS_PER_PROCESS
        ):
            candidate.listening_ports.append(listener.port)
        candidate.bind_scope = _merge_bind_scope(
            candidate.bind_scope, listener.bind_scope
        )

    for candidate in by_pid.values():
        candidate.listening_ports.sort()

    return list(by_pid.values())


def enumerate_candidates(
    *, timeout: int = SUBPROCESS_TIMEOUT_S
) -> list[ProcessCandidate]:
    """Run both sources and return the pid-unioned candidate set (never raises)."""
    processes = enumerate_process_table(timeout=timeout)
    listeners = enumerate_listeners(timeout=timeout)
    return union_by_pid(processes, listeners)
