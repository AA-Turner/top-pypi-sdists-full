"""Tailnet join and leave for Chronos VMs, through a CommandRunner (local shell or SSH).

The join steps are in docs/worlds/agent.md, section 8.
"""

from __future__ import annotations

import asyncio
import base64
import logging
import os
import shlex
from collections.abc import Callable
from enum import StrEnum
from typing import Protocol

import httpx
from pydantic import BaseModel, ConfigDict, Field, field_validator

from plato.runtimes.base import RuntimeInfo
from plato.utils.subprocess import _close_subprocess, _ssh_user_for_host, build_ssh_command
from plato.worlds.config import TailscaleConfig

logger = logging.getLogger(__name__)

# An OAuth client secret is accepted by ``tailscale up --auth-key`` with these
# URL-style parameters; a plain auth key carries its own attributes instead.
# This is the fallback for a plan that still carries the secret (a direct join_tailnet
# caller). The normal path mints a one-off key on the world VM first (mint_auth_key).
OAUTH_CLIENT_SECRET_PREFIX = "tskey-client-"
OAUTH_KEY_PARAMS = "ephemeral=true&preauthorized=true"

# Minting a one-off auth key from the OAuth client secret: exchange the secret for a
# short-lived access token, then create one single-use ephemeral preauthorized key.
# https://tailscale.com/api : POST /oauth/token (client_credentials) then POST /keys.
TAILSCALE_API_BASE = "https://api.tailscale.com/api/v2"
OAUTH_TOKEN_PATH = "/oauth/token"
CREATE_KEY_PATH = "/tailnet/-/keys"

TUN_DEVICE = "/dev/net/tun"
TAILSCALED_SOCKET = "/var/run/tailscale/tailscaled.sock"
TAILSCALED_LOG = "/var/log/plato-tailscaled.log"
HOSTS_PATH = "/etc/hosts"
ENVIRONMENT_PATH = "/etc/environment"
BACKEND_RUNNING = "Running"

# ``tailscale up`` reads the auth key from the ``file:`` path: here, the command's stdin.
AUTH_KEY_FROM_STDIN = "file:/dev/stdin"
# Redaction removes each token with this prefix, also a truncated one.
TAILSCALE_KEY_PREFIX = "tskey-"
REDACTED = "<redacted>"

MANAGED_BLOCK_BEGIN = "# BEGIN plato-tailscale (managed, do not edit)"
MANAGED_BLOCK_END = "# END plato-tailscale"

HOSTNAME_MAX_LEN = 63
SESSION_ID_CHARS = 8
NO_SESSION_ID = "local"

# Extra seconds on top of a command's own timeout before the runner gives up.
_RUNNER_TIMEOUT_MARGIN_S = 10
# ssh exits 255 when it cannot reach the VM or the connection drops, so the remote
# command gave no result.
SSH_TRANSPORT_EXIT = 255

PROXY_ENV_VARS = ("ALL_PROXY", "all_proxy", "NO_PROXY", "no_proxy")


class TailscaleError(RuntimeError):
    """A VM could not join or leave the tailnet."""


class TailscaleMintError(TailscaleError):
    """The world VM could not mint a one-off auth key from the OAuth client secret."""


class TailscaleUnavailableError(TailscaleError):
    """The VM has no ``tailscale``/``tailscaled`` binary, and the runtime install did not give one."""


class TailscaleInstallError(TailscaleUnavailableError):
    """The runtime install of the pinned Tailscale build failed (download, SHA-256 check or install)."""


class TailscaleKernelModeRequiredError(TailscaleError):
    """The VM has no /dev/net/tun (userspace mode only), and ``require_kernel_mode`` is set."""


class TailscaleNetworkMode(StrEnum):
    """How tailscaled reaches the tailnet on this VM."""

    KERNEL = "kernel"
    """A TUN device: every process reaches tailnet IPs directly."""
    USERSPACE = "userspace"
    """No /dev/net/tun: tailnet traffic goes through the local SOCKS5/HTTP proxy."""


class TailscaleArch(StrEnum):
    """CPU architecture names that pkgs.tailscale.com uses in its tarball names."""

    AMD64 = "amd64"
    ARM64 = "arm64"


class TailscaleBuild(BaseModel):
    """One pinned static Tailscale build: the tarball and its published SHA-256."""

    model_config = ConfigDict(frozen=True)

    version: str
    arch: TailscaleArch
    sha256: str = Field(pattern=r"^[0-9a-f]{64}$")

    @property
    def name(self) -> str:
        """Tarball name without ``.tgz``, also the top directory inside the tarball."""
        return f"tailscale_{self.version}_{self.arch}"

    @property
    def url(self) -> str:
        return f"https://pkgs.tailscale.com/stable/{self.name}.tgz"


# Each SHA-256 is the value that pkgs.tailscale.com publishes at ``<tarball url>.sha256``.
TAILSCALE_VERSION = "1.104.1"
TAILSCALE_BUILDS: dict[TailscaleArch, TailscaleBuild] = {
    TailscaleArch.AMD64: TailscaleBuild(
        version=TAILSCALE_VERSION,
        arch=TailscaleArch.AMD64,
        sha256="108d1d96ecf410d305571e173516f27038f870919a9b89c914a167c6d33a4528",
    ),
    TailscaleArch.ARM64: TailscaleBuild(
        version=TAILSCALE_VERSION,
        arch=TailscaleArch.ARM64,
        sha256="f60294374967f3dfd8cf57bbbd474d6cfce32d123e3a8ddeab82a87940daa806",
    ),
}


def docker_build_args() -> list[str]:
    """The ``--build-arg`` flags that give agents/agent-base.Dockerfile its Tailscale pins.

    TAILSCALE_BUILDS is the one source of truth. agents/tailscale-build-args.sh prints
    these flags for each docker build of the agent base image.
    """
    args = {"TAILSCALE_VERSION": TAILSCALE_VERSION}
    for arch, build in sorted(TAILSCALE_BUILDS.items()):
        if build.version != TAILSCALE_VERSION:
            raise ValueError(f"Tailscale build {build.name} does not use version {TAILSCALE_VERSION}")
        args[f"TAILSCALE_SHA256_{arch.upper()}"] = build.sha256
    return [flag for key, value in args.items() for flag in ("--build-arg", f"{key}={value}")]


UNAME_ARCHES: dict[str, TailscaleArch] = {
    "x86_64": TailscaleArch.AMD64,
    "amd64": TailscaleArch.AMD64,
    "aarch64": TailscaleArch.ARM64,
    "arm64": TailscaleArch.ARM64,
}
SYSTEM_BIN_DIR = "/usr/local/bin"
# A shell word, not a path: the install script expands ``$HOME``.
PRIVATE_BIN_DIR = '"$HOME"/.cache/plato-tailscale/bin'
INSTALL_EXIT_NO_DOWNLOADER = 3
INSTALL_EXIT_DOWNLOAD = 4
INSTALL_EXIT_SHA_MISMATCH = 5
INSTALL_EXIT_EXTRACT = 6
INSTALL_EXIT_VERSION = 7


class TailscaleInstall(BaseModel):
    """Where the join finds the binaries on one VM."""

    bin_dir: str | None = None
    """Directory of the runtime-installed binaries, or None when they were already on PATH."""
    build: TailscaleBuild | None = None
    """The pinned build that the join installed or reused, or None when the image had the binaries."""


class CommandResult(BaseModel):
    """Result of one shell command on a VM."""

    exit_code: int
    stdout: str = ""
    stderr: str = ""
    runner_failed: bool = False
    """True when the command gave no result from the VM: the runner timed out or raised,
    or ssh could not reach the VM. The exit code then says nothing about the VM."""

    @property
    def ok(self) -> bool:
        return self.exit_code == 0


class CommandRunner(Protocol):
    """Runs a shell command on one VM (the world VM or an agent VM)."""

    @property
    def label(self) -> str:
        """Short name of the VM for logs."""
        ...

    async def run(self, command: str, *, timeout_s: int, stdin: str | None = None) -> CommandResult:
        """Run ``command`` with bash and return its result. Never raises on a non-zero exit.

        ``stdin`` goes to the command's standard input. Secrets travel this way, never in ``command``.
        A result that did not come from the VM (for example an ssh exit 255) has ``runner_failed`` set.
        """
        ...


async def _exec(argv: list[str], *, timeout_s: int, stdin: str | None) -> CommandResult:
    """Run ``argv`` with ``stdin`` piped in. A timeout raises without the command text."""
    proc = await asyncio.create_subprocess_exec(
        *argv,
        stdin=asyncio.subprocess.PIPE if stdin is not None else asyncio.subprocess.DEVNULL,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    try:
        stdout, stderr = await asyncio.wait_for(
            proc.communicate(stdin.encode() if stdin is not None else None), timeout=timeout_s
        )
    except BaseException as exc:
        # A timeout or a cancelled task must not leave the child ('tailscale up', ssh) running.
        try:
            proc.kill()
        except ProcessLookupError:
            pass  # The process exited between the timeout and the kill.
        await proc.wait()
        _close_subprocess(proc)
        if isinstance(exc, TimeoutError):
            raise TailscaleError(f"command timed out after {timeout_s}s") from None
        raise
    _close_subprocess(proc)
    return CommandResult(
        exit_code=proc.returncode or 0,
        stdout=stdout.decode("utf-8", errors="replace"),
        stderr=stderr.decode("utf-8", errors="replace"),
    )


class LocalCommandRunner:
    """Runs commands on this VM (the world VM). Uses ``sudo -n`` when not root."""

    label = "world"

    async def run(self, command: str, *, timeout_s: int, stdin: str | None = None) -> CommandResult:
        argv = ["bash", "-c", command]
        if os.geteuid() != 0:
            argv = ["sudo", "-n", *argv]
        return await _exec(argv, timeout_s=timeout_s, stdin=stdin)


class SshCommandRunner:
    """Runs commands on an agent VM over SSH, with the VM's runtime info."""

    _SSH_EXTRA_OPTS: list[tuple[str, str]] = [("ServerAliveInterval", "30"), ("ServerAliveCountMax", "3")]

    def __init__(self, info: RuntimeInfo) -> None:
        if info.ssh_key_path is None:
            raise TailscaleError(f"Agent VM {info.runtime_id} has no SSH key, so it cannot join the tailnet")
        self._info = info
        self.label = info.runtime_id

    async def run(self, command: str, *, timeout_s: int, stdin: str | None = None) -> CommandResult:
        """Run ``command`` over SSH. ``stdin`` goes through the SSH channel, not the argv.

        Not :func:`plato.utils.subprocess.run_ssh`: that one cannot pipe stdin and logs the output.
        """
        assert self._info.ssh_key_path is not None
        if self._info.ssh_user != "root":
            command = f"sudo -u {shlex.quote(self._info.ssh_user)} -- bash -c {shlex.quote(command)}"
        argv = build_ssh_command(
            self._info.ssh_key_path,
            self._info.hostname,
            extra_opts=self._SSH_EXTRA_OPTS,
            ssh_user=_ssh_user_for_host(self._info.hostname),
        )
        argv.append(command)
        result = await _exec(argv, timeout_s=timeout_s, stdin=stdin)
        if result.exit_code == SSH_TRANSPORT_EXIT:
            return result.model_copy(update={"runner_failed": True})
        return result


class TailscalePeerStatus(BaseModel):
    """One node in ``tailscale status --json`` (the ``Self`` entry or a ``Peer`` value)."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    host_name: str = Field(default="", alias="HostName")
    dns_name: str = Field(default="", alias="DNSName")
    tailscale_ips: list[str] = Field(default_factory=list, alias="TailscaleIPs")
    online: bool = Field(default=False, alias="Online")

    @field_validator("tailscale_ips", mode="before")
    @classmethod
    def _null_ips_are_empty(cls, value: object) -> object:
        # A logged-out daemon (NeedsLogin, for example a warm-pool VM after 'tailscale logout')
        # prints "TailscaleIPs": null for Self. That is valid status, not a broken answer.
        return [] if value is None else value


class TailscaleStatus(BaseModel):
    """The parts of ``tailscale status --json`` that the join uses."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    backend_state: str = Field(default="", alias="BackendState")
    self_node: TailscalePeerStatus | None = Field(default=None, alias="Self")
    peers: dict[str, TailscalePeerStatus] | None = Field(default=None, alias="Peer")

    @property
    def running(self) -> bool:
        return self.backend_state == BACKEND_RUNNING

    def peer_list(self) -> list[TailscalePeerStatus]:
        return list((self.peers or {}).values())


class HostsEntry(BaseModel):
    """One line of the managed /etc/hosts block."""

    ip: str
    names: list[str]

    def render(self) -> str:
        return f"{self.ip}\t{' '.join(self.names)}"


class TailscaleJoinPlan(BaseModel):
    """Everything one VM needs to join: built from :class:`TailscaleConfig` plus its role."""

    hostname: str
    auth_key: str = Field(repr=False)
    tags: list[str]
    accept_dns: bool
    join_timeout_s: int
    daemon_start_timeout_s: int
    command_timeout_s: int
    leave_timeout_s: int
    install_timeout_s: int
    proxy_port: int
    write_hosts: bool
    export_proxy_env: bool
    no_proxy: list[str]
    require_kernel_mode: bool = False


class TailscaleNode(BaseModel):
    """A VM that joined the tailnet. :func:`leave_tailnet` takes it back out."""

    vm: str
    hostname: str
    mode: TailscaleNetworkMode
    peer_count: int = 0
    proxy_env: dict[str, str] = Field(default_factory=dict)
    """Environment that reaches the tailnet (userspace mode only, else empty)."""
    created_by_session: bool = True
    """True when this session logged the node in. :func:`leave_tailnet` logs out only such a node."""
    bin_dir: str | None = None
    """Directory of the runtime-installed binaries, put first on PATH for each command. None: image binaries."""


def _clean_hostname_label(text: str) -> str:
    chars = [c if (c.isascii() and c.isalnum()) or c == "-" else "-" for c in text.lower()]
    return "".join(chars).strip("-")


def node_hostname(prefix: str, session_id: str, role: str) -> str:
    """``<prefix>-<session8>-<role>``, as a valid DNS label of 63 chars or fewer."""
    session8 = _clean_hostname_label(session_id)[:SESSION_ID_CHARS] or NO_SESSION_ID
    name = "-".join(part for part in (_clean_hostname_label(prefix), session8, _clean_hostname_label(role)) if part)
    return name[:HOSTNAME_MAX_LEN].rstrip("-")


def build_auth_key(secret: str) -> str:
    """Return the ``--auth-key`` value. An OAuth client secret gets the ephemeral parameters.

    Fallback for a plan that still carries the OAuth client secret. The normal path mints a
    one-off key with :func:`mint_auth_key` first, so the plan here holds a plain ``tskey-auth-``
    key and this returns it unchanged.
    """
    secret = secret.strip()
    if secret.startswith(OAUTH_CLIENT_SECRET_PREFIX) and "?" not in secret:
        return f"{secret}?{OAUTH_KEY_PARAMS}"
    return secret


def is_oauth_client_secret(auth_key: str) -> bool:
    return auth_key.strip().startswith(OAUTH_CLIENT_SECRET_PREFIX)


def _json_body(response: httpx.Response, field: str) -> str:
    """Pull ``field`` from a JSON response. Raises without ever putting the body in the error.

    Both the token response and the key response hold secrets, so a parse or missing-field
    error names only the field, never the body text.
    """
    try:
        value = response.json().get(field)
    except ValueError:
        raise TailscaleMintError(f"Tailscale API response was not JSON (no {field})") from None
    if not isinstance(value, str) or not value:
        raise TailscaleMintError(f"Tailscale API response had no {field}")
    return value


async def mint_auth_key(
    oauth_secret: str,
    *,
    tags: list[str],
    expiry_s: int,
    timeout_s: int,
    client: httpx.AsyncClient | None = None,
) -> str:
    """Mint one single-use ephemeral preauthorized auth key from the OAuth client secret.

    Runs on the world VM, which holds the secret. The returned ``tskey-auth-...`` key is the
    only thing that goes to a joining VM's ``tailscale up``; the OAuth secret never leaves here.
    Raises :class:`TailscaleMintError`; its text never carries the secret, the token or the key.
    """
    if not tags:
        raise TailscaleMintError("an OAuth client secret needs at least one tag to mint an auth key")
    owns_client = client is None
    client = client or httpx.AsyncClient()
    try:
        try:
            token_resp = await client.post(
                f"{TAILSCALE_API_BASE}{OAUTH_TOKEN_PATH}",
                data={"client_secret": oauth_secret},
                timeout=timeout_s,
            )
        except httpx.HTTPError as exc:
            raise TailscaleMintError(f"Tailscale OAuth token request failed ({type(exc).__name__})") from None
        if token_resp.status_code != 200:
            raise TailscaleMintError(f"Tailscale OAuth token request failed (HTTP {token_resp.status_code})")
        token = _json_body(token_resp, "access_token")

        body = {
            "capabilities": {
                "devices": {
                    "create": {
                        "reusable": False,
                        "ephemeral": True,
                        "preauthorized": True,
                        "tags": list(tags),
                    }
                }
            },
            "expirySeconds": expiry_s,
        }
        try:
            key_resp = await client.post(
                f"{TAILSCALE_API_BASE}{CREATE_KEY_PATH}",
                headers={"Authorization": f"Bearer {token}"},
                json=body,
                timeout=timeout_s,
            )
        except httpx.HTTPError as exc:
            raise TailscaleMintError(f"Tailscale auth-key mint failed ({type(exc).__name__})") from None
        if key_resp.status_code not in (200, 201):
            raise TailscaleMintError(f"Tailscale auth-key mint failed (HTTP {key_resp.status_code})")
        return _json_body(key_resp, "key")
    finally:
        if owns_client:
            await client.aclose()


async def resolve_auth_key(
    ts: TailscaleConfig,
    *,
    client: httpx.AsyncClient | None = None,
    log: logging.Logger = logger,
) -> str:
    """The auth key for one VM's join. Mints a one-off key from an OAuth client secret.

    A plain auth key is returned as given. Raises :class:`TailscaleError` on an empty key or a
    failed mint. Call this on the world VM (where the secret lives) and pass the result to
    :func:`build_join_plan`, so an agent VM only ever receives the minted key.
    """
    secret = (ts.auth_key or "").strip()
    if not secret:
        raise TailscaleError("tailscale.auth_key is empty")
    if not is_oauth_client_secret(secret):
        return secret
    log.info("Minting a one-off Tailscale auth key (tags %s, expiry %ds)", ",".join(ts.tags), ts.mint_key_expiry_s)
    return await mint_auth_key(
        secret,
        tags=list(ts.tags),
        expiry_s=ts.mint_key_expiry_s,
        timeout_s=ts.mint_timeout_s,
        client=client,
    )


def build_join_plan(
    ts: TailscaleConfig, *, session_id: str, role: str, auth_key: str | None = None
) -> TailscaleJoinPlan:
    """Resolve the config for one VM. Raises :class:`TailscaleError` without an auth key.

    ``auth_key`` overrides ``ts.auth_key`` with the key this VM should use: the normal path
    passes the one-off key from :func:`resolve_auth_key` so the plan never holds the OAuth secret.
    """
    key = auth_key if auth_key is not None else ts.auth_key
    if not key:
        raise TailscaleError("tailscale.auth_key is empty")
    return TailscaleJoinPlan(
        hostname=node_hostname(ts.hostname_prefix, session_id, role),
        auth_key=key,
        tags=list(ts.tags),
        accept_dns=ts.accept_dns,
        join_timeout_s=ts.join_timeout_s,
        daemon_start_timeout_s=ts.daemon_start_timeout_s,
        command_timeout_s=ts.command_timeout_s,
        leave_timeout_s=ts.leave_timeout_s,
        install_timeout_s=ts.install_timeout_s,
        proxy_port=ts.proxy_port,
        write_hosts=ts.write_hosts,
        export_proxy_env=ts.export_proxy_env,
        no_proxy=list(ts.no_proxy),
        require_kernel_mode=ts.require_kernel_mode,
    )


def build_up_flags(plan: TailscaleJoinPlan) -> list[str]:
    flags = [f"--hostname={plan.hostname}"]
    if plan.tags:
        flags.append(f"--advertise-tags={','.join(plan.tags)}")
    flags += [f"--accept-dns={'true' if plan.accept_dns else 'false'}", f"--timeout={plan.join_timeout_s}s"]
    return flags


def build_up_command(plan: TailscaleJoinPlan) -> str:
    """The ``tailscale up`` command. It holds no secret: send :func:`build_up_stdin` to its stdin."""
    flags = " ".join(shlex.quote(flag) for flag in build_up_flags(plan))
    return f"tailscale up --auth-key={AUTH_KEY_FROM_STDIN} {flags}"


def build_up_stdin(plan: TailscaleJoinPlan) -> str:
    """The stdin for :func:`build_up_command`: the auth key (``tailscale up`` trims the newline)."""
    return build_auth_key(plan.auth_key) + "\n"


def build_daemon_command(mode: TailscaleNetworkMode, *, proxy_port: int) -> str:
    """Start ``tailscaled`` in the background with in-memory state (an ephemeral node)."""
    argv = ["tailscaled", "--state=mem:", f"--socket={TAILSCALED_SOCKET}"]
    if mode is TailscaleNetworkMode.USERSPACE:
        proxy = f"localhost:{proxy_port}"
        argv += ["--tun=userspace-networking", f"--socks5-server={proxy}", f"--outbound-http-proxy-listen={proxy}"]
    daemon = " ".join(shlex.quote(arg) for arg in argv)
    return f"mkdir -p {shlex.quote(os.path.dirname(TAILSCALED_SOCKET))} && nohup {daemon} > {TAILSCALED_LOG} 2>&1 &"


def build_wait_for_socket_command(timeout_s: int) -> str:
    sock = shlex.quote(TAILSCALED_SOCKET)
    return f"for _ in $(seq 1 {timeout_s}); do test -S {sock} && exit 0; sleep 1; done; exit 1"


def proxy_env_for(plan: TailscaleJoinPlan) -> dict[str, str]:
    """Proxy environment for userspace mode: ``http://``, because httpx needs an extra package for ``socks5://``."""
    proxy_url = f"http://localhost:{plan.proxy_port}"
    no_proxy = ",".join(plan.no_proxy)
    return {"ALL_PROXY": proxy_url, "all_proxy": proxy_url, "NO_PROXY": no_proxy, "no_proxy": no_proxy}


def peer_hosts_entries(status: TailscaleStatus) -> list[HostsEntry]:
    """One /etc/hosts entry per peer with an IPv4 address: the MagicDNS short name, then the OS hostname."""
    entries: list[HostsEntry] = []
    for peer in status.peer_list():
        ipv4 = next((ip for ip in peer.tailscale_ips if "." in ip), None)
        if ipv4 is None:
            continue
        names: list[str] = []
        short_name = peer.dns_name.rstrip(".").split(".")[0]
        if short_name:
            names.append(short_name)
        if peer.host_name and peer.host_name not in names:
            names.append(peer.host_name)
        if names:
            entries.append(HostsEntry(ip=ipv4, names=names))
    return entries


def strip_managed_block(text: str) -> str:
    """Remove every managed block (BEGIN..END lines included) from ``text``."""
    if MANAGED_BLOCK_BEGIN not in text:
        return text
    kept: list[str] = []
    inside = False
    for line in text.splitlines():
        if line.strip() == MANAGED_BLOCK_BEGIN:
            inside = True
            continue
        if inside:
            if line.strip() == MANAGED_BLOCK_END:
                inside = False
            continue
        kept.append(line)
    return "\n".join(kept) + ("\n" if kept else "")


def replace_managed_block(text: str, lines: list[str]) -> str:
    """Return ``text`` with ONE managed block that holds ``lines``. No ``lines`` removes the block."""
    base = strip_managed_block(text)
    if not lines:
        return base
    if base and not base.endswith("\n"):
        base += "\n"
    block = "\n".join([MANAGED_BLOCK_BEGIN, *lines, MANAGED_BLOCK_END]) + "\n"
    return base + block


def render_hosts_file(existing: str, entries: list[HostsEntry]) -> str:
    return replace_managed_block(existing, [entry.render() for entry in entries])


def render_environment_file(existing: str, env: dict[str, str]) -> str:
    return replace_managed_block(existing, [f'{key}="{value}"' for key, value in env.items()])


def build_write_file_command(path: str, content: str) -> str:
    """Overwrite ``path`` in place (works on a bind-mounted /etc/hosts) without shell quoting issues."""
    encoded = base64.b64encode(content.encode()).decode()
    return f"printf %s {encoded} | base64 -d > {shlex.quote(path)}"


WHICH_COMMAND = "command -v tailscale >/dev/null && command -v tailscaled >/dev/null"


def build_install_command(
    build: TailscaleBuild,
    *,
    download_timeout_s: int,
    system_dir: str = SYSTEM_BIN_DIR,
    private_dir: str = PRIVATE_BIN_DIR,
) -> str:
    """One bash script that installs ``build`` and prints the install dir as its last stdout line.

    The SHA-256 check runs before the extract. Root or ``sudo -n``: ``system_dir``, else
    ``private_dir`` (mode 700). No systemd unit is installed or started.
    """
    q = shlex.quote
    system = q(system_dir)
    t = int(download_timeout_s)
    download_failed = f'{{ echo "download of $url failed" >&2; exit {INSTALL_EXIT_DOWNLOAD}; }}'
    lines = [
        "set -eu",
        f"version={q(build.version)}; name={q(build.name)}; url={q(build.url)}; sha={q(build.sha256)}",
        f'if [ "$(id -u)" = 0 ]; then as_root=""; owner="-o root -g root"; dir={system}',
        f'elif sudo -n true 2>/dev/null; then as_root="sudo -n"; owner="-o root -g root"; dir={system}',
        f'else as_root=""; owner=""; dir={private_dir}; fi',
        'if [ -x "$dir/tailscale" ] && [ -x "$dir/tailscaled" ] '
        '&& [ "$("$dir/tailscale" version 2>/dev/null | head -n 1)" = "$version" ]; then echo "$dir"; exit 0; fi',
        'tmp="$(mktemp -d)"',
        """trap 'rm -rf "$tmp"' EXIT""",
        'tgz="$tmp/$name.tgz"',
        "if command -v curl >/dev/null 2>&1; then",
        f'  curl -fsSL --proto =https --tlsv1.2 --retry 3 --max-time {t} -o "$tgz" "$url" || {download_failed}',
        "elif command -v wget >/dev/null 2>&1; then",
        f'  wget -q --https-only --timeout={t} -O "$tgz" "$url" || {download_failed}',
        f'else echo "no curl or wget to download $url" >&2; exit {INSTALL_EXIT_NO_DOWNLOADER}; fi',
        'if command -v sha256sum >/dev/null 2>&1; then got="$(sha256sum "$tgz" | cut -d " " -f 1)"',
        'elif command -v shasum >/dev/null 2>&1; then got="$(shasum -a 256 "$tgz" | cut -d " " -f 1)"',
        'else got=""; fi',
        'if [ "$got" != "$sha" ]; then',
        '  echo "SHA-256 mismatch for $url: expected $sha, got ${got:-nothing (no sha256 tool)}" >&2',
        f"  exit {INSTALL_EXIT_SHA_MISMATCH}",
        "fi",
        'tar -xzf "$tgz" -C "$tmp" "$name/tailscale" "$name/tailscaled" '
        f'|| {{ echo "extract of $name.tgz failed" >&2; exit {INSTALL_EXIT_EXTRACT}; }}',
        f'if [ "$dir" = {system} ]; then [ -d "$dir" ] || $as_root install -d -m 755 "$dir"',
        'else mkdir -p "$dir"; chmod 700 "$dir"; fi',
        '$as_root install -m 755 $owner "$tmp/$name/tailscale" "$dir/tailscale"',
        '$as_root install -m 755 $owner "$tmp/$name/tailscaled" "$dir/tailscaled"',
        'if [ "$("$dir/tailscale" version 2>/dev/null | head -n 1)" != "$version" ]; then',
        f'  echo "installed tailscale in $dir does not report version $version" >&2; exit {INSTALL_EXIT_VERSION}',
        "fi",
        'echo "$dir"',
    ]
    return "\n".join(lines)


def bin_dir_prefix(bin_dir: str) -> str:
    return f'export PATH={shlex.quote(bin_dir)}:"$PATH"; '


class _BinDirRunner:
    """A :class:`CommandRunner` that runs each command with the runtime-installed binaries first on PATH."""

    def __init__(self, inner: CommandRunner, bin_dir: str) -> None:
        self._inner = inner
        self._prefix = bin_dir_prefix(bin_dir)
        self.label = inner.label

    async def run(self, command: str, *, timeout_s: int, stdin: str | None = None) -> CommandResult:
        return await self._inner.run(self._prefix + command, timeout_s=timeout_s, stdin=stdin)


def _with_bin_dir(runner: CommandRunner, bin_dir: str | None) -> CommandRunner:
    return _BinDirRunner(runner, bin_dir) if bin_dir else runner


async def ensure_tailscale_binaries(
    runner: CommandRunner,
    *,
    command_timeout_s: int,
    install_timeout_s: int,
    log: logging.Logger = logger,
) -> TailscaleInstall:
    """Install the pinned build when the image has no binaries.

    Raises :class:`TailscaleUnavailableError` (no pinned build) or :class:`TailscaleInstallError`.
    """
    which = await _run(runner, WHICH_COMMAND, command_timeout_s)
    if which.ok:
        log.info("Tailscale binaries are already on PATH on %s, skipping the install", runner.label)
        return TailscaleInstall()

    uname = await _run(runner, "uname -m", command_timeout_s)
    machine = uname.stdout.strip() if uname.ok else ""
    arch = UNAME_ARCHES.get(machine)
    build = TAILSCALE_BUILDS.get(arch) if arch is not None else None
    if build is None:
        detail = repr(machine) if machine else f"unknown ({uname.stderr.strip() or 'uname -m failed'})"
        raise TailscaleUnavailableError(
            f"VM {runner.label} has no tailscale/tailscaled binary, and its architecture {detail} "
            f"has no pinned Tailscale build (pinned: {', '.join(sorted(TAILSCALE_BUILDS))})"
        )

    log.info("Installing Tailscale %s (%s) on %s from %s", build.version, build.arch, runner.label, build.url)
    result = await _run(runner, build_install_command(build, download_timeout_s=install_timeout_s), install_timeout_s)
    out_lines = result.stdout.strip().splitlines()
    bin_dir = out_lines[-1].strip() if out_lines else ""
    if not result.ok or not bin_dir.startswith("/"):
        detail = result.stderr.strip() or result.stdout.strip() or "no output"
        raise TailscaleInstallError(
            f"Install of Tailscale {build.version} ({build.arch}) failed on {runner.label} "
            f"(exit {result.exit_code}): {detail}"
        )
    log.info("Tailscale %s is in %s on %s", build.version, bin_dir, runner.label)
    return TailscaleInstall(bin_dir=bin_dir, build=build)


def _is_token_end(char: str) -> bool:
    return char.isspace() or char in "'\"`"


def _redact_key_tokens(text: str) -> str:
    """Replace each ``tskey-...`` token (up to the next space or quote) with ``<redacted>``."""
    parts: list[str] = []
    start = 0
    while (found := text.find(TAILSCALE_KEY_PREFIX, start)) != -1:
        end = found
        while end < len(text) and not _is_token_end(text[end]):
            end += 1
        parts += [text[start:found], REDACTED]
        start = end
    parts.append(text[start:])
    return "".join(parts)


def _redact(text: str, secret: str) -> str:
    """Remove ``secret`` and every Tailscale key token, also a truncated one, from ``text``."""
    if secret:
        text = text.replace(secret, REDACTED)
    return _redact_key_tokens(text)


async def _run(
    runner: CommandRunner, command: str, timeout_s: int, *, secret: str = "", stdin: str | None = None
) -> CommandResult:
    """Run one command; a runner error becomes a failed result, with the secret redacted.

    With ``secret`` set, a runner error gives a generic message, without the exception text.
    """
    try:
        result = await runner.run(command, timeout_s=timeout_s + _RUNNER_TIMEOUT_MARGIN_S, stdin=stdin)
    except Exception as exc:
        if secret:
            stderr = f"command failed or timed out ({type(exc).__name__})"
        else:
            stderr = _redact(str(exc), secret)
        return CommandResult(exit_code=-1, stderr=stderr, runner_failed=True)
    if secret:
        result = result.model_copy(
            update={"stdout": _redact(result.stdout, secret), "stderr": _redact(result.stderr, secret)}
        )
    return result


STATUS_COMMAND = "tailscale status --json"
# A process check, because a tailscaled killed with -9 leaves its socket behind and a new
# daemon starts fine over it. Without pgrep, the socket test.
# A system tailscaled uses the same socket path, so the check covers it too.
SOCKET_TEST_COMMAND = (
    "if command -v pgrep >/dev/null 2>&1; then pgrep -x tailscaled >/dev/null; "
    f"else test -S {shlex.quote(TAILSCALED_SOCKET)}; fi"
)
TUN_TEST_COMMAND = f"test -c {shlex.quote(TUN_DEVICE)}"


def _detail(result: CommandResult) -> str:
    return result.stderr.strip() or result.stdout.strip() or "no output"


def _raise_if_runner_failed(runner: CommandRunner, command: str, result: CommandResult) -> None:
    if result.runner_failed:
        raise TailscaleError(f"'{command}' did not run on {runner.label}: {_detail(result)}")


async def _run_test(runner: CommandRunner, command: str, timeout_s: int) -> bool:
    """Run a shell ``test`` command: exit 0 is True, exit 1 is False.

    Any other result raises :class:`TailscaleError`: it says nothing, and a wrong False changes the join.
    """
    result = await _run(runner, command, timeout_s)
    _raise_if_runner_failed(runner, command, result)
    if result.exit_code not in (0, 1):
        raise TailscaleError(f"'{command}' on {runner.label} gave exit {result.exit_code}: {_detail(result)}")
    return result.ok


async def read_status(runner: CommandRunner, timeout_s: int) -> TailscaleStatus | None:
    """``tailscale status --json``, or None when no tailscaled runs.

    Raises :class:`TailscaleError` for any other unclear answer, because the join starts a
    daemon after None, and a second daemon must not start over one that does not answer.
    """
    result = await _run(runner, STATUS_COMMAND, timeout_s)
    _raise_if_runner_failed(runner, STATUS_COMMAND, result)
    if not result.stdout.strip():
        if not await _run_test(runner, SOCKET_TEST_COMMAND, timeout_s):
            return None
        raise TailscaleError(
            f"'{STATUS_COMMAND}' failed on {runner.label} (exit {result.exit_code}) "
            f"while a tailscaled runs: {_detail(result)}"
        )
    try:
        return TailscaleStatus.model_validate_json(result.stdout)
    except ValueError:
        # No output text in the error: keep the message short and free of node data.
        raise TailscaleError(
            f"'tailscale status --json' on {runner.label} gave {len(result.stdout)} bytes that are not status JSON"
        ) from None


async def _detect_mode(runner: CommandRunner, timeout_s: int) -> TailscaleNetworkMode:
    has_tun = await _run_test(runner, TUN_TEST_COMMAND, timeout_s)
    return TailscaleNetworkMode.KERNEL if has_tun else TailscaleNetworkMode.USERSPACE


async def _rewrite_file(runner: CommandRunner, path: str, transform: Callable[[str], str], timeout_s: int) -> bool:
    """Read ``path``, apply ``transform`` and write it back when it changed.

    A missing file reads as empty. A failed read gives False and no write, so a partial read never overwrites the file.
    """
    quoted = shlex.quote(path)
    read = await _run(runner, f"cat {quoted} 2>/dev/null || test ! -e {quoted}", timeout_s)
    if not read.ok:
        return False
    content = transform(read.stdout)
    if content == read.stdout:
        return True
    write = await _run(runner, build_write_file_command(path, content), timeout_s)
    return write.ok


async def join_tailnet(
    runner: CommandRunner,
    plan: TailscaleJoinPlan,
    *,
    persist_proxy_env: bool,
    log: logging.Logger = logger,
) -> TailscaleNode:
    """Join the VM behind ``runner`` to the tailnet. Raises :class:`TailscaleError` on failure.

    ``persist_proxy_env``: in userspace mode, write the proxy into /etc/environment (agent VMs).
    """
    timeout = plan.command_timeout_s
    # With require_kernel_mode the mode check runs first, so a VM without the device downloads nothing.
    mode = await _detect_mode(runner, timeout) if plan.require_kernel_mode else None
    if mode is TailscaleNetworkMode.USERSPACE:
        raise TailscaleKernelModeRequiredError(
            f"{runner.label} has no {TUN_DEVICE}, so Tailscale can join only in userspace mode, "
            "and tailscale.require_kernel_mode is true: a process that does not use the local "
            "userspace proxy (for example yt-dlp or curl with its own --proxy) cannot reach tailnet peers"
        )
    install = await ensure_tailscale_binaries(
        runner, command_timeout_s=timeout, install_timeout_s=plan.install_timeout_s, log=log
    )
    runner = _with_bin_dir(runner, install.bin_dir)

    if mode is None:
        mode = await _detect_mode(runner, timeout)
    status = await read_status(runner, timeout)
    created_by_session = True
    if status is not None and status.running:
        self_name = status.self_node.host_name if status.self_node else ""
        # Same hostname: an earlier join of this session (a warm-pool VM whose logout
        # failed). Another hostname: a node that was there before, never logged out here.
        created_by_session = self_name == plan.hostname
        log.info("Tailscale on %s already joined as %s, skipping 'tailscale up'", runner.label, self_name or "unknown")
    elif status is None:
        log.info("Starting tailscaled on %s (%s networking)", runner.label, mode)
        start = await _run(runner, build_daemon_command(mode, proxy_port=plan.proxy_port), timeout)
        if not start.ok:
            raise TailscaleError(f"tailscaled did not start on {runner.label}: {start.stderr.strip()}")
        ready = await _run(
            runner, build_wait_for_socket_command(plan.daemon_start_timeout_s), plan.daemon_start_timeout_s
        )
        if not ready.ok:
            raise TailscaleError(
                f"tailscaled on {runner.label} opened no socket in {plan.daemon_start_timeout_s}s "
                f"(see {TAILSCALED_LOG})"
            )

    try:
        if status is None or not status.running:
            log.info("Joining tailnet from %s as %s", runner.label, plan.hostname)
            up = await _run(
                runner, build_up_command(plan), plan.join_timeout_s, secret=plan.auth_key, stdin=build_up_stdin(plan)
            )
            if not up.ok:
                detail = up.stderr.strip() or up.stdout.strip()
                raise TailscaleError(f"'tailscale up' failed on {runner.label} (exit {up.exit_code}): {detail}")
        node = await _finish_join(runner, plan, mode, status, persist_proxy_env, created_by_session, log)
        return node.model_copy(update={"bin_dir": install.bin_dir})
    except BaseException:
        # A timed-out 'tailscale up' can still have logged the node in. A cancel logs out
        # too: the world records the node only after this returns, so its cleanup cannot
        # find a half-joined node.
        if created_by_session:
            await _logout_after_failed_join(runner, plan, log)
        # _finish_join can fail after it wrote the hosts block: a run that goes on without
        # the tailnet must not keep peer names it cannot reach.
        await _strip_after_failed_join(runner, plan, log)
        raise


async def _logout_after_failed_join(runner: CommandRunner, plan: TailscaleJoinPlan, log: logging.Logger) -> None:
    logout = await _run(runner, "tailscale logout", plan.leave_timeout_s)
    log.warning("Join failed on %s; 'tailscale logout' exit %d", runner.label, logout.exit_code)


async def _strip_block(runner: CommandRunner, path: str, timeout_s: int, log: logging.Logger) -> bool:
    """Remove the managed block from ``path``. Best effort: a failure logs the file, it does not raise."""
    try:
        if await _rewrite_file(runner, path, strip_managed_block, timeout_s):
            return True
        reason = "the read or write failed"
    except Exception as exc:  # noqa: BLE001 - the caller's own result or error is the one that goes up
        reason = str(exc)
    log.warning("Could not remove the tailnet block from %s on %s: %s", path, runner.label, reason)
    return False


async def _strip_after_failed_join(runner: CommandRunner, plan: TailscaleJoinPlan, log: logging.Logger) -> None:
    for path in (HOSTS_PATH, ENVIRONMENT_PATH):
        await _strip_block(runner, path, plan.leave_timeout_s, log)


async def _finish_join(
    runner: CommandRunner,
    plan: TailscaleJoinPlan,
    mode: TailscaleNetworkMode,
    status: TailscaleStatus | None,
    persist_proxy_env: bool,
    created_by_session: bool,
    log: logging.Logger,
) -> TailscaleNode:
    """The join steps after the node is logged in: status check, /etc/hosts, proxy environment."""
    timeout = plan.command_timeout_s
    if status is None or not status.running:
        status = await read_status(runner, timeout)
        if status is None or not status.running:
            state = status.backend_state if status else "no status"
            raise TailscaleError(f"Tailscale on {runner.label} is not running after 'tailscale up' ({state})")
    hostname = plan.hostname if created_by_session else (status.self_node.host_name if status.self_node else "")

    peers = status.peer_list()
    log.info("Tailscale on %s connected as %s, %d peer(s) visible", runner.label, hostname, len(peers))

    if plan.write_hosts:
        entries = peer_hosts_entries(status)
        if not await _rewrite_file(runner, HOSTS_PATH, lambda text: render_hosts_file(text, entries), timeout):
            # No peer name resolves without it; tailscale.required decides whether the run stops.
            raise TailscaleError(f"Could not write the tailnet peers into {HOSTS_PATH} on {runner.label}")

    proxy_env: dict[str, str] = {}
    if mode is TailscaleNetworkMode.USERSPACE and plan.export_proxy_env:
        proxy_env = proxy_env_for(plan)
        env = proxy_env
        if persist_proxy_env and not await _rewrite_file(
            runner, ENVIRONMENT_PATH, lambda text: render_environment_file(text, env), timeout
        ):
            # The agent's only route to tailnet peers; tailscale.required decides if the run stops.
            raise TailscaleError(f"Could not write the tailnet proxy into {ENVIRONMENT_PATH} on {runner.label}")

    return TailscaleNode(
        vm=runner.label,
        hostname=hostname,
        mode=mode,
        peer_count=len(peers),
        proxy_env=proxy_env,
        created_by_session=created_by_session,
    )


async def leave_tailnet(
    runner: CommandRunner,
    node: TailscaleNode,
    *,
    timeout_s: int,
    log: logging.Logger = logger,
) -> bool:
    """Log the node out and remove the managed blocks. Best effort: never raises.

    A node that this session did not create keeps its login. Returns True when the node
    is off the tailnet or was not ours to log out.
    """
    try:
        runner = _with_bin_dir(runner, node.bin_dir)
        logged_out = True
        if node.created_by_session:
            logout = await _run(runner, "tailscale logout", timeout_s)
            logged_out = logout.ok
            if not logout.ok:
                log.warning("'tailscale logout' failed on %s: %s", node.vm, logout.stderr.strip())
        else:
            log.info("Tailscale node %s was there before the join; not logging it out", node.hostname)
        await _strip_block(runner, HOSTS_PATH, timeout_s, log)
        if node.proxy_env:
            await _strip_block(runner, ENVIRONMENT_PATH, timeout_s, log)
        if logged_out and node.created_by_session:
            log.info("Tailscale node %s left the tailnet", node.hostname)
        return logged_out
    except Exception as exc:
        log.warning("Tailscale leave failed on %s: %s", node.vm, exc)
        return False
