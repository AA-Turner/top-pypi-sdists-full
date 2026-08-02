"""Base classes for the install tool framework.

All installable tools inherit from ``BaseTool``. Two concrete subclasses
handle the two families:

- ``BinaryTool`` — CLI binaries installed on the system (glab, aws, kubectl, …)
- ``McpTool`` — MCP server configs upserted into each present assistant's store
  (``~/.claude.json`` for Claude, ``~/.codex/config.toml`` for Codex)

Each tool module exposes a single ``tool`` instance; the orchestrator
(:mod:`pysae_ai_tools.install.all`) drives everything through the typed
:class:`BaseTool` contract — no duck-typing.
"""

import subprocess
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Literal

import typer

from . import binary, platform, syspkg

# ---------------------------------------------------------------------------
# Shared dataclasses
# ---------------------------------------------------------------------------

Status = Literal["installed", "needs-update", "needs-reconfigure", "auth-required", "missing"]


@dataclass
class ToolState:
    """Typed state of a tool, as reported by :meth:`BaseTool.get_state`.

    The four boolean-ish flags are the whole contract; :meth:`classify`
    turns them into a single :data:`Status` and is the only classifier in
    the codebase. ``extra`` carries display-only detail (versions, per-target
    breakdowns, identity lines) and never drives classification.
    """

    needs_install: bool = True
    needs_update: bool = False
    needs_reconfigure: bool = False
    auth_ok: bool | None = None
    extra: dict[str, Any] = field(default_factory=dict)

    def classify(self) -> Status:
        """Reduce the flags to a single status, most-blocking first.

        ``missing`` (not installed) → ``needs-update`` (version drift) →
        ``needs-reconfigure`` (a config/secret step must re-run) →
        ``auth-required`` (installed & current but not authenticated) →
        ``installed``. ``auth_ok is None`` means the tool has no auth
        concept and never yields ``auth-required``.
        """
        if self.needs_install:
            return "missing"
        if self.needs_update:
            return "needs-update"
        if self.needs_reconfigure:
            return "needs-reconfigure"
        if self.auth_ok is False:
            return "auth-required"
        return "installed"

    @property
    def installed(self) -> bool:
        """True once the tool is present, regardless of updates, pending
        reconfiguration or auth state."""
        return not self.needs_install

    @property
    def needs_work(self) -> bool:
        """True when an install/update/reconfigure step is pending. An auth
        failure alone is not "work": the tool still resolves, so the
        orchestrator leaves it up-to-date."""
        return self.needs_install or self.needs_update or self.needs_reconfigure

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {
            "needs_install": self.needs_install,
            "needs_update": self.needs_update,
            "needs_reconfigure": self.needs_reconfigure,
        }
        out.update(self.extra)
        if self.auth_ok is not None:
            out["auth_ok"] = self.auth_ok
        return out


@dataclass
class InstallReport:
    """Universal install report."""

    action: str = "install"
    version: str = ""
    path: str = ""
    method: str = ""
    error: str = ""
    extra: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, object]:
        out: dict[str, object] = {"action": self.action}
        for f in ("version", "path", "method", "error"):
            v = getattr(self, f)
            if v:
                out[f] = v
        if self.extra:
            out.update(self.extra)
        return out


@dataclass
class EnvVar:
    """Environment variable definition for a tool."""

    name: str
    help: str = ""


@dataclass
class Context:
    """A named context/profile that can be checked."""

    name: str
    ok: bool = False
    error: str = ""


# ---------------------------------------------------------------------------
# Base class
# ---------------------------------------------------------------------------


class BaseTool(ABC):
    """Abstract base for all installable tools."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Tool name as used in the CLI (e.g. 'glab', 'aws', 'mongo-mcp')."""

    @property
    def cli_help(self) -> str:
        return f"Install/check {self.name}"

    @property
    def env_vars(self) -> list[EnvVar]:
        """Env vars required for installation. Override in subclass."""
        return []

    @property
    def system_deps(self) -> list[syspkg.SystemDep]:
        """OS-level shared libraries this tool needs at run time (e.g. libfuse2
        for an AppImage). The install framework ensures them before
        :meth:`do_install`, decoupled from the tool's own installer. Override in
        subclasses; return only what applies to the current OS."""
        return []

    @property
    def env_required(self) -> tuple[str, ...]:
        return tuple(v.name for v in self.env_vars)

    @property
    def env_help(self) -> dict[str, str]:
        return {v.name: v.help for v in self.env_vars if v.help}

    # --- State ---

    @abstractmethod
    def get_state(self) -> ToolState:
        """Return current state of this tool."""

    # --- Install ---

    @abstractmethod
    def do_install(self) -> InstallReport:
        """Install or update the binary only. Configuration is a separate
        concern carried by :meth:`do_configure`; the orchestrator runs them
        in order. Returns a report."""

    # --- Configure (without installing) ---

    def do_configure(self) -> InstallReport:
        """Apply configuration only — auth, MCP registration, contexts, … —
        never installing or updating the binary.

        Disjoint from :meth:`do_install`: a normal ``tools install`` runs
        ``do_install`` then ``do_configure``; ``tools install --configure-only``
        runs ``do_configure`` alone. The default is a no-op
        (``method="nothing to configure"``): plain binaries have nothing to
        configure. Tools with auth tokens, kube contexts or an MCP upsert
        override this to carry that work.
        """
        return InstallReport(action="configure", method="nothing to configure")

    # --- Uninstall ---

    def do_uninstall(self, *, dry_run: bool = False) -> InstallReport:
        """Tear down what this tool installed or configured.

        Default no-op: plain binaries are removed by the user's package
        manager, not here. Tools that write into shared config (assistant
        settings, MCP stores, shell rc files) override this to strip only
        what they own. ``dry_run`` reports what *would* be removed without
        touching anything.
        """
        return InstallReport(action="uninstall", method="nothing to uninstall", extra={"removed": []})

    # --- Contract metadata (replaces the getattr/*_BIN/SERVER_NAME probing) ---

    def binary_names(self) -> tuple[str, ...]:
        """Binary names this tool puts on PATH, for the lightweight presence
        check. Empty for tools with no binary (MCP servers, plugins, …)."""
        return ()

    def mcp_server_names(self) -> tuple[str, ...]:
        """MCP server name(s) this tool registers in each assistant store.
        Empty for tools that register none."""
        return ()

    def secret_ids(self) -> tuple[str, ...]:
        """AWS Secrets Manager ids to warm before resolving this tool's env
        vars. Empty by default."""
        return ()

    # --- Identity for status display ---

    def extract_identity(self, state: dict[str, Any]) -> list[tuple[str, str | None]]:
        """Return identity/context lines for the status display."""
        return []

    # --- Human-readable output ---

    def format_check(self, state: ToolState) -> None:
        """Print human-readable check output. Override for custom formatting."""
        d = state.to_dict()
        bin_info = d.get("binary", {})
        if isinstance(bin_info, dict) and bin_info.get("installed"):
            version = bin_info.get("version", "n/a")
            latest = d.get("latest", "")
            update = f" (latest {latest})" if latest and latest != version else ""
            typer.echo(f"{self.name}: {version}{update}")
        else:
            typer.echo(f"{self.name}: NOT installed")

    def format_install(self, report: InstallReport) -> None:
        """Print human-readable install output."""
        if report.error:
            typer.echo(f"FAILED: {report.error}", err=True)
        else:
            parts = [f"installed {self.name}"]
            if report.version:
                parts[0] += f" {report.version}"
            if report.method:
                parts.append(f"via {report.method}")
            if report.path:
                parts.append(f"at {report.path}")
            typer.echo(" ".join(parts))


# ---------------------------------------------------------------------------
# BinaryTool
# ---------------------------------------------------------------------------


class BinaryTool(BaseTool, ABC):
    """Tool installed as a system binary.

    Subclasses declare per-OS install strategies in two layers:

    1. **Native package managers** — set :attr:`winget_package` and/or
       :attr:`brew_package` (and later ``apt_package``) to the package id and
       the framework will run the corresponding manager when available on the
       current OS. A failure from a configured manager is surfaced as-is and
       does **not** fall back to the OS hook.
    2. **Per-OS hooks** — override :meth:`install_linux`, :meth:`install_macos`,
       and :meth:`install_windows`. They are called when no native manager is
       configured for that OS, or when the manager is unavailable.

    Most subclasses only need to set the package ids; ``ArchiveBinaryTool``
    provides default OS hooks driven by :meth:`archive_info`.
    """

    # --- Native package manager ids (None = not packaged for that manager) ---
    winget_package: str | None = None
    brew_package: str | None = None
    brew_cask: bool = False  # True for GUI casks (e.g. docker desktop)

    @property
    @abstractmethod
    def binary_name(self) -> str:
        """Name of the binary on PATH (e.g. 'glab', 'aws', 'kubectl')."""

    def binary_names(self) -> tuple[str, ...]:
        return (self.binary_name,)

    @property
    def version_arg(self) -> str:
        return "--version"

    @property
    def version_timeout(self) -> int:
        """Timeout in seconds for version detection. Override for slow tools."""
        return 5

    @abstractmethod
    def fetch_latest_version(self) -> str:
        """Fetch the latest available version string."""

    # --- Per-OS install hooks (override what applies to your tool) ---

    def install_linux(self, plat: platform.Platform) -> InstallReport:
        return InstallReport(error=f"{self.name}: install on Linux not implemented")

    def install_macos(self, plat: platform.Platform) -> InstallReport:
        return InstallReport(error=f"{self.name}: install on macOS not implemented")

    def install_windows(self, plat: platform.Platform) -> InstallReport:
        return InstallReport(error=f"{self.name}: install on Windows not implemented")

    # --- Dispatcher: native manager first, then per-OS hook ---

    def install_binary(self) -> InstallReport:
        try:
            plat = platform.detect()
        except ValueError as exc:
            return InstallReport(error=str(exc))

        from . import brew as _brew
        from . import winget as _winget

        if plat.is_windows and self.winget_package:
            r = _winget.install(
                self.winget_package,
                binary_name=self.binary_name,
                version_arg=self.version_arg,
                version_timeout=self.version_timeout,
            )
            if r is not None:
                return r
        if plat.is_macos and self.brew_package:
            r = _brew.install(self.brew_package, cask=self.brew_cask)
            if r is not None:
                return r

        if plat.is_linux:
            return self.install_linux(plat)
        if plat.is_macos:
            return self.install_macos(plat)
        if plat.is_windows:
            return self.install_windows(plat)
        return InstallReport(error=f"unsupported OS: {plat.os}")

    # --- Optional overrides ---

    def check_auth(self) -> dict[str, Any] | None:
        """Return auth info dict (e.g. {'auth_ok': True, 'auth_message': '...'}) or None."""
        return None

    def check_contexts(self) -> dict[str, Any] | None:
        """Return contexts/profiles dict or None."""
        return None

    # --- Concrete implementations ---

    def get_state(self) -> ToolState:
        bin_status = binary.status(self.binary_name, version_arg=self.version_arg, timeout=self.version_timeout)
        try:
            latest = self.fetch_latest_version().lstrip("v")
        except Exception:  # noqa: BLE001
            latest = ""

        extra: dict[str, Any] = {
            "binary": bin_status.to_dict(),
            "latest": latest,
        }

        auth_ok: bool | None = None
        auth = self.check_auth()
        if auth is not None:
            extra.update(auth)
            val = auth.get("auth_ok")
            if isinstance(val, bool):
                auth_ok = val

        contexts = self.check_contexts()
        if contexts is not None:
            extra.update(contexts)

        return ToolState(
            needs_install=not bin_status.installed,
            needs_update=bin_status.installed and bool(latest) and binary.needs_update(bin_status.version, latest),
            auth_ok=auth_ok,
            extra=extra,
        )

    def do_install(self) -> InstallReport:
        pre = binary.get_version(self.binary_name, version_arg=self.version_arg, timeout=self.version_timeout)
        report = self.install_binary()
        if report.error:
            return report
        post = binary.get_version(self.binary_name, version_arg=self.version_arg, timeout=self.version_timeout)
        # Catch silent no-op installs: the underlying command exited 0 but the
        # binary's version did not move. Without this, the user sees "installed"
        # on every run while nothing actually changes.
        #
        # Skip the check when the package manager itself has reported that
        # nothing was upgradable (e.g. winget's "no available upgrade") —
        # that's a legitimate up-to-date result, not a silent failure, even
        # if GitHub's latest tag is ahead because the catalog hasn't caught
        # up yet (winget's repo trails new releases by hours/days).
        method = (report.method or "").lower()
        already_up_to_date = "already up-to-date" in method or "already installed" in method
        if not already_up_to_date and pre and post and pre == post:
            try:
                latest = self.fetch_latest_version().lstrip("v")
            except Exception:  # noqa: BLE001
                latest = ""
            if latest and binary.needs_update(post, latest):
                return InstallReport(
                    error=f"installer exited 0 but version did not change ({post}); expected update to {latest}",
                )
        return report

    def format_check(self, state: ToolState) -> None:
        d = state.to_dict()
        bin_info = d.get("binary", {})
        if isinstance(bin_info, dict) and bin_info.get("installed"):
            version = bin_info.get("version", "n/a")
            latest = d.get("latest", "")
            update = f" (latest {latest})" if latest and latest != version else ""
            typer.echo(f"{self.name}: {version}{update}")

            # Auth
            if "auth_ok" in d:
                typer.echo(f"  auth: {'OK' if d['auth_ok'] else 'FAILED'}")

            # Contexts
            for line_text, _ in self.extract_identity(d):
                typer.echo(f"  {line_text}")
        else:
            typer.echo(f"{self.name}: NOT installed")


# ---------------------------------------------------------------------------
# McpTool
# ---------------------------------------------------------------------------


# Binary the shim entry invokes: ``pysae-ai-tools mcp run <server>`` resolves the
# server's secrets at launch (env → AWS Secrets Manager → CLI) and execs the real
# MCP server. No secret is ever written to disk.
SHIM_BINARY = "pysae-ai-tools"


def _same_command(stored: dict[str, Any], shim: dict[str, Any]) -> bool:
    """True when two stdio entries invoke the same command line.

    Compared on ``command`` + ``args`` only: stores normalize differently (Codex
    drops ``type``; a store may omit an empty ``env``), so a key-by-key equality
    would report spurious drift."""
    return stored.get("command") == shim.get("command") and list(stored.get("args", [])) == list(shim.get("args", []))


class McpTool(BaseTool, ABC):
    """Tool for an MCP server declared through the resolver shim.

    The server is never written to disk with its secrets baked in. Instead:

    - assistants that load MCP from the Pysae plugin (Claude) get the server
      declared in the plugin's ``.mcp.json`` (handled by the plugin deploy),
      and any legacy baked entry is removed from their store (migration);
    - assistants without a plugin-MCP mechanism (Codex) get the **secret-free
      shim triplet** upserted into their store.

    In both cases the on-disk entry runs ``pysae-ai-tools mcp run <server>``,
    which calls :meth:`build_config` at launch to resolve secrets and exec the
    real server. :meth:`build_config` therefore stays the single source of the
    resolved command line; it is invoked by the shim, not at configure time.
    """

    @property
    @abstractmethod
    def server_name(self) -> str:
        """MCP server name in the assistant stores / plugin manifest."""

    def mcp_server_names(self) -> tuple[str, ...]:
        return (self.server_name,)

    @abstractmethod
    def build_config(self) -> dict[str, Any]:
        """Resolve the server's stdio config (``command``/``args``/``env`` with
        secrets baked). Called by the shim at launch — never persisted."""

    def shim_config(self) -> dict[str, Any]:
        """The secret-free stdio entry written to a store / plugin manifest.

        Defers all resolution to ``pysae-ai-tools mcp run <server>`` at launch.
        Identical for every server; the ``server_name`` is the only variable."""
        return {"type": "stdio", "command": SHIM_BINARY, "args": ["mcp", "run", self.server_name]}

    def prepare(self) -> None:
        """Idempotent side effects the real server needs before it starts (e.g.
        writing a dedicated kubeconfig, creating a browser-profile dir).

        Run by the shim just before exec. No-op by default; overridden by the
        servers that need it (Kubernetes, Chrome)."""

    def _store_targets(self) -> list[Any]:
        """Active assistants that carry the shim entry in their own store (i.e.
        not the plugin-MCP ones). Claude is excluded — its servers live in the
        plugin manifest."""
        from .assistants import active_assistants

        return [a for a in active_assistants() if not a.uses_plugin_mcp()]

    def get_state(self) -> ToolState:
        # Presence is tracked only in stores we still write to. Native plugin MCP
        # servers are owned and reported by their plugin deployment tool.
        shim = self.shim_config()
        targets = {a.name: a.mcp.get(self.server_name) for a in self._store_targets()}
        need_install = bool(targets) and any(cfg is None for cfg in targets.values())
        need_update = any(cfg is not None and not _same_command(cfg, shim) for cfg in targets.values())
        return ToolState(
            needs_install=need_install,
            needs_update=need_update,
            extra={"name": self.server_name, "targets": {name: cfg is not None for name, cfg in targets.items()}},
        )

    def do_install(self) -> InstallReport:
        # An MCP server has no binary to install — declaring it (plugin manifest
        # for Claude, shim entry for Codex) is pure configuration.
        return InstallReport(action="install", method="nothing to install")

    def do_configure(self) -> InstallReport:
        from .assistants import active_assistants

        assistants = active_assistants()
        if not assistants:
            return InstallReport(
                action="configure",
                method="no assistant CLI present",
                extra={"name": self.server_name, "changed": False, "targets": {}},
            )

        shim = self.shim_config()
        # Each assistant independently: a failure on one config must not abort the
        # others. Plugin-MCP assistants only get any legacy baked entry stripped;
        # other assistants carry the secret-free shim triplet in their own store.
        changed: dict[str, bool] = {}
        errors: dict[str, str] = {}
        for assistant in assistants:
            try:
                if assistant.uses_plugin_mcp():
                    changed[assistant.name] = assistant.mcp.remove(self.server_name)
                else:
                    changed[assistant.name] = assistant.mcp.upsert(self.server_name, shim)
            except Exception as exc:  # noqa: BLE001
                errors[assistant.name] = str(exc)

        if errors:
            detail = "; ".join(f"{name}: {msg}" for name, msg in errors.items())
            return InstallReport(
                error=f"{self.server_name}: {detail}",
                extra={"name": self.server_name, "changed": any(changed.values()), "targets": changed},
            )
        return InstallReport(
            action="configure",
            extra={"name": self.server_name, "changed": any(changed.values()), "targets": changed},
        )

    def format_check(self, state: ToolState) -> None:
        targets = state.to_dict().get("targets") or {}
        if not targets:
            typer.echo(f"{self.server_name}: declared by the plugin (no store target)")
        elif all(targets.values()):
            typer.echo(f"{self.server_name}: configured")
        else:
            missing = ", ".join(name for name, ok in targets.items() if not ok)
            typer.echo(f"{self.server_name}: NOT configured (missing on {missing})")

    def format_install(self, report: InstallReport) -> None:
        if report.error:
            typer.echo(f"FAILED: {report.error}", err=True)
            return
        targets = report.extra.get("targets") or {}
        if not targets:
            typer.echo(f"{self.server_name}: declared by the plugin (nothing to write)")
        elif report.extra.get("changed"):
            typer.echo(f"{self.server_name}: updated")
        else:
            typer.echo(f"{self.server_name}: already configured (no changes)")


# ---------------------------------------------------------------------------
# Convenience: download-and-install binary tool
# ---------------------------------------------------------------------------


class ArchiveBinaryTool(BinaryTool, ABC):
    """Binary tool installed from a downloaded archive.

    The default per-OS hooks all delegate to :meth:`_install_from_archive`, so
    a subclass only needs to provide :meth:`archive_info`. Override an
    individual hook (or set ``winget_package`` / ``brew_package``) to deviate
    on a specific OS.
    """

    @abstractmethod
    def archive_info(self, version: str, plat: platform.Platform) -> tuple[str, str | None]:
        """Return (download_url, archive_member_path_or_None) for the given version and platform."""

    def _install_from_archive(self, plat: platform.Platform) -> InstallReport:
        try:
            version = self.fetch_latest_version()
        except Exception as exc:  # noqa: BLE001
            return InstallReport(error=f"could not fetch latest version: {exc}")

        url, member = self.archive_info(version.lstrip("v"), plat)

        from .download import download_and_install_binary

        try:
            path = download_and_install_binary(url, self.binary_name, archive_member=member)
        except Exception as exc:  # noqa: BLE001
            return InstallReport(error=f"download/install failed: {exc}")

        installed_v = binary.get_version(self.binary_name, version_arg=self.version_arg)
        return InstallReport(version=installed_v or version.lstrip("v"), path=str(path))

    def install_linux(self, plat: platform.Platform) -> InstallReport:
        return self._install_from_archive(plat)

    def install_macos(self, plat: platform.Platform) -> InstallReport:
        return self._install_from_archive(plat)

    def install_windows(self, plat: platform.Platform) -> InstallReport:
        return self._install_from_archive(plat)


# ---------------------------------------------------------------------------
# UvTool — installed via `uv tool install`
# ---------------------------------------------------------------------------


class UvTool(BinaryTool, ABC):
    """Binary tool installed via ``uv tool install``."""

    @property
    @abstractmethod
    def pip_package(self) -> str:
        """PyPI package name (e.g. 'prefect')."""

    def install_binary(self) -> InstallReport:
        r = subprocess.run(
            ["uv", "tool", "install", "--force", "--reinstall", self.pip_package],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if r.returncode != 0:
            return InstallReport(error=f"uv tool failed: {r.stderr.strip() or r.stdout.strip()}")
        installed_v = binary.get_version(self.binary_name, version_arg=self.version_arg)
        return InstallReport(version=installed_v, method="uv tool")
