"""Env service: /etc/hosts entries and /etc/environment managed block.

The managed block is delimited by marker comments so writes are idempotent
upserts, not appends — unlike the SSH ``echo >> /etc/environment`` it replaces,
which accumulated a fresh line on every warm-pool reuse. The pool reset removes
this block by marker instead of truncating the whole file (which used to wipe
image-baked entries too).
"""

from __future__ import annotations

from pathlib import Path

from aiohttp import web

from plato.agents.daemon.http_util import parse_body
from plato.agents.daemon.idempotency import ResultCache, with_idempotency
from plato.agents.daemon.state import DaemonContext
from plato.rpc.models.env import EnvSetupRequest, EnvSetupResponse, HostsEntry
from plato.rpc.protocol import API_PREFIX, CAP_ENV_SETUP

_BEGIN = "# BEGIN plato-agent managed block"
_END = "# END plato-agent managed block"

_ETC_ENVIRONMENT = Path("/etc/environment")
_ETC_HOSTS = Path("/etc/hosts")


def render_managed_block(env_vars: dict[str, str]) -> str:
    lines = [_BEGIN]
    lines.extend(f"{k}={v}" for k, v in env_vars.items())
    lines.append(_END)
    return "\n".join(lines) + "\n"


def upsert_managed_block(existing: str, env_vars: dict[str, str]) -> str:
    """Replace (or append) the managed block in ``existing``."""
    block = render_managed_block(env_vars)
    begin = existing.find(_BEGIN)
    if begin == -1:
        prefix = existing if existing.endswith("\n") or not existing else existing + "\n"
        return prefix + block
    end = existing.find(_END, begin)
    if end == -1:  # malformed — replace from begin to EOF
        return existing[:begin] + block
    end += len(_END)
    trailing = existing[end:].lstrip("\n")
    return existing[:begin] + block + (trailing if trailing else "")


def strip_managed_block(existing: str) -> str:
    """Remove the managed block entirely (used by pool reset)."""
    begin = existing.find(_BEGIN)
    if begin == -1:
        return existing
    end = existing.find(_END, begin)
    if end == -1:
        return existing[:begin]
    end += len(_END)
    return existing[:begin] + existing[end:].lstrip("\n")


def scrub_env_for_reset(existing: str) -> str:
    """Reset-time scrub of /etc/environment: managed block plus any bare
    ``PLATO_API_KEY=`` line.

    The bare-line case exists because ``rpc_or_ssh`` gates per capability: env
    setup may have gone over SSH (``echo "PLATO_API_KEY=..." >>``, no markers)
    on a VM whose reset goes over RPC. A scrub that only understands its own
    path's write format would let the key survive into the next pooled task.
    """
    remaining = strip_managed_block(existing)
    kept = [ln for ln in remaining.splitlines() if not ln.strip().startswith("PLATO_API_KEY=")]
    out = "\n".join(kept)
    return out + "\n" if out else ""


def upsert_hosts(existing: str, entries: list[HostsEntry]) -> str:
    """Replace each hostname's mapping, then append the fresh one — mirrors the
    SSH ``sed -i '/host/d' && echo >>`` idempotency.

    Replacement is TOKEN-level, not line-level: hosts lines carry multiple
    names (``127.0.0.1 localhost myvm``), and deleting the whole line would
    take the co-resident names down with it — breaking ``sudo``/``getfqdn``
    for the VM's own hostname. Only the matching name is removed; the line
    survives if other names remain, and dies only when the target was its sole
    name (the ``runtime.plato.internal`` case, matching the SSH ``sed``).

    Only a SAME-FAMILY mapping is replaced: an IPv4 ``localhost`` entry must
    not touch the stock ``::1 localhost ip6-localhost`` line.
    """
    out: list[str] = []
    for line in existing.splitlines():
        parts = line.split()
        if len(parts) < 2 or line.lstrip().startswith("#"):
            out.append(line)
            continue
        ip, names = parts[0], parts[1:]
        kept_names = [n for n in names if not any(e.hostname == n and (":" in ip) == (":" in e.ip) for e in entries)]
        if kept_names == names:
            out.append(line)  # untouched lines keep their original formatting
        elif kept_names:
            out.append(f"{ip} {' '.join(kept_names)}")
        # else: the target was the line's only name — drop the line
    out.extend(f"{e.ip} {e.hostname}" for e in entries)
    return "\n".join(out) + "\n"


def _write(path: Path, content: str) -> None:
    path.write_text(content)


def _read(path: Path) -> str:
    # ONLY a missing file reads as empty. Any other OSError must propagate
    # (→ typed INTERNAL error): swallowing it here would make the subsequent
    # full-file _write silently replace /etc/hosts with just the new entries.
    try:
        return path.read_text()
    except FileNotFoundError:
        return ""


def _setup_handler(env_path: Path, hosts_path: Path, cache: ResultCache):
    async def setup(request: web.Request) -> web.Response:
        req = await parse_body(request, EnvSetupRequest)

        async def produce() -> EnvSetupResponse:
            if req.env_vars:
                _write(env_path, upsert_managed_block(_read(env_path), req.env_vars))
            if req.hosts:
                _write(hosts_path, upsert_hosts(_read(hosts_path), req.hosts))
            return EnvSetupResponse(hosts_written=len(req.hosts), env_vars_written=len(req.env_vars))

        return await with_idempotency(request, cache, produce)

    return setup


def register(
    app: web.Application,
    ctx: DaemonContext,
    *,
    env_path: Path = _ETC_ENVIRONMENT,
    hosts_path: Path = _ETC_HOSTS,
) -> None:
    app.router.add_post(f"{API_PREFIX}/env/setup", _setup_handler(env_path, hosts_path, ResultCache()))
    ctx.capabilities.append(CAP_ENV_SETUP)
