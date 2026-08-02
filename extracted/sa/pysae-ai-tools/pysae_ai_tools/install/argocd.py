"""Install or update the ArgoCD CLI.

Source of truth for the version is the Pysae dev server (/api/version).
Download is attempted from the Pysae dev mirror first, then GitHub releases.

After the binary install succeeds, dev and prod contexts are authenticated
non-interactively by writing the ``argocd`` auth tokens directly to the CLI
config file (resolved cross-platform, see ``_argocd_config_path``). Tokens
come from ``ARGOCD_AUTH_TOKEN_DEV`` /
``ARGOCD_AUTH_TOKEN_PROD``, resolved through :mod:`pysae_ai_tools.env.resolve`
(env → AWS Secrets Manager via ``iam/<username>/<env>/argocd`` → MCP config).
Existing contexts in the config file are preserved — only the ``dev`` and
``prod`` entries are upserted — except stale SSO contexts pointing at a
``pysae.com`` server (e.g. the ``argocd login``-created
``argocd.dev.pysae.com`` / ``argocd.prod.pysae.com``), which are pruned so
they stop shadowing the managed token contexts. Missing tokens are reported
but never fail the install.
"""

import json
import os
import subprocess
from pathlib import Path
from typing import Any

import httpx
import typer
import yaml

from .common import binary, platform
from .common.base import BinaryTool, InstallReport, ToolState

ARGOCD_SERVERS: dict[str, str] = {
    "dev": "argocd.dev.pysae.com",
    "prod": "argocd.prod.pysae.com",
}
DEV_SERVER = ARGOCD_SERVERS["dev"]
GH_RELEASES = "https://github.com/argoproj/argo-cd/releases/download"


def _is_pysae_server(server: str) -> bool:
    host = server.split("/")[-1].split(":")[0]
    return host == "pysae.com" or host.endswith(".pysae.com")


def _argocd_config_path() -> Path:
    """Resolve the argocd CLI config file path, matching the CLI on every OS.

    The argocd CLI resolves its config directory as ``$ARGOCD_CONFIG_DIR`` if
    set, else ``<home>/.config/argocd`` — where ``<home>`` is Go's
    ``os.UserHomeDir`` (``%USERPROFILE%`` on Windows, *not* ``%APPDATA%``).
    Note: argocd hardcodes ``.config`` and does **not** honor
    ``XDG_CONFIG_HOME``, so we deliberately don't either — mirroring the CLI
    guarantees we write the tokens exactly where it later reads them.
    """
    env_dir = os.environ.get("ARGOCD_CONFIG_DIR")
    if env_dir:
        return Path(env_dir) / "config"
    return Path.home() / ".config" / "argocd" / "config"


class ArgocdTool(BinaryTool):
    name = "argocd"
    binary_name = "argocd"
    version_arg = "version"
    cli_help = "Install/update the ArgoCD CLI and authenticate to dev/prod"
    brew_package = "argocd"
    # Pre-configure: ``do_install`` reads these tokens and writes
    # ~/.config/argocd/config to authenticate the dev/prod contexts. Auto-resolved
    # from AWS Secrets Manager (no prompt needed).
    env_pre_configure = ("ARGOCD_AUTH_TOKEN_DEV", "ARGOCD_AUTH_TOKEN_PROD")
    env_help = {
        "ARGOCD_AUTH_TOKEN_DEV": "AWS Secrets Manager (iam/<user>/dev/argocd argocd-auth-token)",
        "ARGOCD_AUTH_TOKEN_PROD": "AWS Secrets Manager (iam/<user>/prod/argocd argocd-auth-token)",
    }

    def fetch_latest_version(self) -> str:
        r = httpx.get(f"https://{DEV_SERVER}/api/version", timeout=5.0, follow_redirects=True)
        r.raise_for_status()
        version = r.json().get("Version", "")
        return version.split("+")[0] if isinstance(version, str) else ""

    def get_state(self) -> ToolState:
        bin_status = binary.status(self.binary_name, version_arg=self.version_arg)
        # argocd version outputs to stderr; use json client mode
        if bin_status.installed:
            try:
                r = subprocess.run(
                    [self.binary_name, "version", "--client", "-o", "json"],
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    check=False,
                    timeout=5,
                )
                data = json.loads(r.stdout) if r.stdout else {}
                client_v = data.get("client", {}).get("Version", "")
                if isinstance(client_v, str) and client_v:
                    bin_status.version = binary.extract_version(client_v) or client_v.lstrip("v").split("+")[0]
            except (json.JSONDecodeError, OSError, subprocess.TimeoutExpired):
                pass

        try:
            srv = self.fetch_latest_version()
        except Exception:  # noqa: BLE001
            srv = ""

        contexts: dict[str, dict[str, Any]] = {}
        any_unauthenticated = False
        for ctx in ARGOCD_SERVERS:
            if bin_status.installed:
                ok, err = self._context_status(ctx)
                contexts[ctx] = {"ok": ok, "error": err}
                any_unauthenticated = any_unauthenticated or not ok
            else:
                contexts[ctx] = {"ok": False, "error": "binary not installed"}

        extra: dict[str, Any] = {
            "binary": bin_status.to_dict(),
            "latest": srv,
            "server_version": srv,
            "contexts": contexts,
        }
        # A stored token that no longer authenticates (rotated/expired upstream
        # in AWS Secrets Manager, or never written) makes ``tools install``
        # re-run and re-upsert the contexts.
        needs_reconfigure = bin_status.installed and any_unauthenticated
        if needs_reconfigure:
            extra["needs_reconfigure_contexts"] = True

        return ToolState(
            needs_install=not bin_status.installed,
            needs_update=bin_status.installed and bool(srv) and binary.needs_update(bin_status.version, srv),
            needs_reconfigure=needs_reconfigure,
            extra=extra,
        )

    def _context_status(self, context: str) -> tuple[bool, str]:
        try:
            sw = subprocess.run(
                [self.binary_name, "context", context],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
                timeout=5,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            return False, f"argocd not runnable: {exc}"
        if sw.returncode != 0:
            err = sw.stderr.strip().split("\n")[-1] if sw.stderr.strip() else "context not configured"
            return False, err
        try:
            check = subprocess.run(
                [self.binary_name, "account", "get-user-info", "--grpc-web"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
                timeout=10,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            return False, f"argocd not runnable: {exc}"
        if check.returncode != 0:
            raw = check.stderr.strip().split("\n")[-1] if check.stderr.strip() else "auth failed"
            try:
                log = json.loads(raw)
                err = str(log.get("msg", raw))
            except (json.JSONDecodeError, TypeError):
                err = raw
            return False, err
        return True, ""

    def _download_install(self, sources: list[tuple[str, str]], version: str) -> InstallReport:
        from .common.download import download_and_install_binary

        last_error = ""
        for source, url in sources:
            try:
                path = download_and_install_binary(url, self.binary_name)
                installed_v = binary.get_version(self.binary_name, version_arg=self.version_arg)
                return InstallReport(version=installed_v or version, path=str(path), method=source)
            except Exception as exc:  # noqa: BLE001
                last_error = f"{source}: {exc}"
        return InstallReport(error=f"download failed: {last_error}")

    def _release_filename(self, plat: platform.Platform) -> str:
        arch = "amd64" if plat.arch.value == "x86_64" else plat.arch.value
        suffix = ".exe" if plat.is_windows else ""
        return f"argocd-{plat.os.value}-{arch}{suffix}"

    def install_linux(self, plat: platform.Platform) -> InstallReport:
        try:
            version = self.fetch_latest_version()
        except Exception as exc:  # noqa: BLE001
            return InstallReport(error=f"could not fetch server version: {exc}")
        filename = self._release_filename(plat)
        sources: list[tuple[str, str]] = []
        if plat.arch.value == "x86_64":
            sources.append(("pysae-dev", f"https://{DEV_SERVER}/download/{filename}"))
        sources.append(("github", f"{GH_RELEASES}/v{version.lstrip('v')}/{filename}"))
        return self._download_install(sources, version)

    def install_macos(self, plat: platform.Platform) -> InstallReport:
        try:
            version = self.fetch_latest_version()
        except Exception as exc:  # noqa: BLE001
            return InstallReport(error=f"could not fetch server version: {exc}")
        filename = self._release_filename(plat)
        return self._download_install(
            [("github", f"{GH_RELEASES}/v{version.lstrip('v')}/{filename}")],
            version,
        )

    def install_windows(self, plat: platform.Platform) -> InstallReport:
        try:
            version = self.fetch_latest_version()
        except Exception as exc:  # noqa: BLE001
            return InstallReport(error=f"could not fetch server version: {exc}")
        filename = self._release_filename(plat)
        return self._download_install(
            [("github", f"{GH_RELEASES}/v{version.lstrip('v')}/{filename}")],
            version,
        )

    def do_configure(self) -> InstallReport:
        report = InstallReport(action="configure")
        auth = self._authenticate_contexts()
        if auth:
            report.extra["auth"] = auth
        else:
            report.method = "nothing to configure"
        return report

    def _authenticate_contexts(self) -> dict[str, str]:
        """Upsert each ArgoCD context in ``~/.config/argocd/config`` with tokens from ``env.resolve``."""
        from ..env.resolve import preload_secrets, try_auto_resolve

        token_vars = [f"ARGOCD_AUTH_TOKEN_{ctx.upper()}" for ctx in ARGOCD_SERVERS]
        # Warm both context tokens in one parallel batch before resolving them.
        preload_secrets(token_vars)

        results: dict[str, str] = {}
        tokens: dict[str, str] = {}
        for ctx in ARGOCD_SERVERS:
            var = f"ARGOCD_AUTH_TOKEN_{ctx.upper()}"
            token = os.environ.get(var) or try_auto_resolve(var) or ""
            if not token:
                results[ctx] = f"skipped — {var} unavailable"
                continue
            tokens[ctx] = token

        if tokens:
            try:
                self._write_config(tokens)
            except OSError as exc:
                for ctx in tokens:
                    results[ctx] = f"failed — {exc}"
                return results
            for ctx in tokens:
                ok, err = self._context_status(ctx)
                results[ctx] = "ok" if ok else f"failed — {err}"
        return results

    def _write_config(self, tokens: dict[str, str]) -> None:
        """Merge our dev/prod contexts into the argocd CLI config (YAML)."""
        config_path = _argocd_config_path()
        config_path.parent.mkdir(parents=True, exist_ok=True)

        data: dict[str, Any] = {}
        if config_path.exists():
            try:
                loaded = yaml.safe_load(config_path.read_text(encoding="utf-8"))
                if isinstance(loaded, dict):
                    data = loaded
            except yaml.YAMLError:
                pass  # treat as fresh config

        contexts: list[dict[str, Any]] = list(data.get("contexts") or [])
        servers: list[dict[str, Any]] = list(data.get("servers") or [])
        users: list[dict[str, Any]] = list(data.get("users") or [])

        for ctx, token in tokens.items():
            server = ARGOCD_SERVERS[ctx]

            # Upsert context { name, server, user }
            ctx_entry = {"name": ctx, "server": server, "user": ctx}
            contexts = [c for c in contexts if c.get("name") != ctx] + [ctx_entry]

            # Upsert server { server, grpc-web, grpc-web-root-path }
            server_entry = {"grpc-web": True, "grpc-web-root-path": "", "server": server}
            servers = [s for s in servers if s.get("server") != server] + [server_entry]

            # Upsert user { name, auth-token } — drop any stale refresh-token
            user_entry = {"auth-token": token, "name": ctx}
            users = [u for u in users if u.get("name") != ctx] + [user_entry]

        managed = set(ARGOCD_SERVERS)
        stale = [c for c in contexts if c.get("name") not in managed and _is_pysae_server(str(c.get("server") or ""))]
        if stale:
            stale_names = {c.get("name") for c in stale}
            stale_users = {c.get("user") for c in stale}
            contexts = [c for c in contexts if c.get("name") not in stale_names]
            still_referenced = {c.get("user") for c in contexts}
            orphaned_users = stale_users - still_referenced
            users = [u for u in users if u.get("name") not in orphaned_users]
            if data.get("current-context") in stale_names:
                data["current-context"] = ""

        data["contexts"] = contexts
        data["servers"] = servers
        data["users"] = users
        if not data.get("current-context"):
            data["current-context"] = "dev" if "dev" in tokens else next(iter(tokens))

        # Write with restricted permissions — tokens are secrets.
        fd = os.open(config_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            yaml.safe_dump(data, f, sort_keys=False, default_flow_style=False)

    def extract_identity(self, state: dict[str, Any]) -> list[tuple[str, str | None]]:
        lines: list[tuple[str, str | None]] = []
        version = state.get("server_version", "")
        if version:
            lines.append((f"server {version}", typer.colors.BRIGHT_BLACK))
        contexts = state.get("contexts", {})
        for ctx_name, ctx_data in contexts.items():
            if isinstance(ctx_data, dict):
                ctx_ok = ctx_data.get("ok", False)
                ctx_err = ctx_data.get("error", "")
            else:
                ctx_ok = bool(ctx_data)
                ctx_err = ""
            icon = "✓" if ctx_ok else "✗"
            suffix = f" — {ctx_err}" if ctx_err else ""
            lines.append((f"{icon} {ctx_name}{suffix}", typer.colors.GREEN if ctx_ok else typer.colors.RED))
        return lines


tool = ArgocdTool()
