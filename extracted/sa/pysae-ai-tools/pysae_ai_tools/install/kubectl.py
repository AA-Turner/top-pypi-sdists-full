"""Install or update kubectl from dl.k8s.io.

After the binary install succeeds, the ``pysae-dev`` and ``pysae-prod``
contexts are configured via ``aws eks update-kubeconfig`` against the Pysae
EKS clusters (``dev`` / ``prod`` in ``eu-west-3``). The ``pysae-`` prefix
avoids collisions with unrelated contexts named ``dev`` / ``prod`` in the
user's kubeconfig. Configuration needs the ``aws`` CLI on PATH and valid AWS
credentials; a missing prerequisite is reported but never fails the install.
The user's previously-selected current-context is preserved.
"""

import os
import subprocess
from typing import Any

import httpx
import typer

from .common import binary, kubeconfig, platform
from .common.base import BinaryTool, InstallReport, ToolState

EKS_REGION = "eu-west-3"

# (context alias written to kubeconfig, EKS cluster name). The ``pysae-``
# prefix keeps these from clashing with bare ``dev`` / ``prod`` contexts that
# may already live in the user's kubeconfig for other clusters.
EKS_CONTEXTS: tuple[tuple[str, str], ...] = (
    ("pysae-dev", "dev"),
    ("pysae-prod", "prod"),
)


class KubectlTool(BinaryTool):
    name = "kubectl"
    binary_name = "kubectl"
    version_arg = "version --client=true"
    cli_help = "Install/update kubectl and configure EKS contexts (pysae-dev/pysae-prod)"
    winget_package = "Kubernetes.kubectl"
    brew_package = "kubectl"

    def fetch_latest_version(self) -> str:
        r = httpx.get("https://dl.k8s.io/release/stable.txt", timeout=5.0, follow_redirects=True)
        r.raise_for_status()
        return r.text.strip()

    def _install_from_dlk8s(self, plat: platform.Platform) -> InstallReport:
        try:
            version = self.fetch_latest_version()
        except Exception as exc:  # noqa: BLE001
            return InstallReport(error=f"could not fetch stable version: {exc}")

        ver = version if version.startswith("v") else f"v{version}"
        arch = "amd64" if plat.arch.value == "x86_64" else plat.arch.value
        suffix = ".exe" if plat.is_windows else ""
        url = f"https://dl.k8s.io/release/{ver}/bin/{plat.os.value}/{arch}/kubectl{suffix}"

        from .common.download import download_and_install_binary

        try:
            path = download_and_install_binary(url, self.binary_name)
        except Exception as exc:  # noqa: BLE001
            return InstallReport(error=f"download/install failed: {exc}")
        installed_v = binary.get_version(self.binary_name, version_arg=self.version_arg)
        return InstallReport(version=installed_v or version.lstrip("v"), path=str(path))

    def install_linux(self, plat: platform.Platform) -> InstallReport:
        return self._install_from_dlk8s(plat)

    def install_macos(self, plat: platform.Platform) -> InstallReport:
        return self._install_from_dlk8s(plat)

    def install_windows(self, plat: platform.Platform) -> InstallReport:
        return self._install_from_dlk8s(plat)

    # ------------------------------------------------------------------
    # EKS context configuration (post-install)
    # ------------------------------------------------------------------

    def _kubectl(self, *args: str, timeout: int = 10) -> subprocess.CompletedProcess[str] | None:
        try:
            return subprocess.run(
                [self.binary_name, *args],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
                timeout=timeout,
            )
        except (OSError, subprocess.TimeoutExpired):
            return None

    def _existing_contexts(self) -> set[str]:
        r = self._kubectl("config", "get-contexts", "-o", "name", timeout=5)
        if r is None or r.returncode != 0:
            return set()
        return {line.strip() for line in r.stdout.splitlines() if line.strip()}

    def _current_context(self) -> str:
        r = self._kubectl("config", "current-context", timeout=5)
        return r.stdout.strip() if r is not None and r.returncode == 0 else ""

    def _configure_contexts(self) -> dict[str, str]:
        """Upsert each Pysae EKS context via ``aws eks update-kubeconfig``.

        Needs the ``aws`` CLI and valid credentials. The user's current
        context is restored afterwards, since ``update-kubeconfig`` flips
        it to the alias it just wrote.
        """
        results: dict[str, str] = {}
        if not binary.which("aws"):
            return {alias: "skipped — aws CLI not installed" for alias, _ in EKS_CONTEXTS}

        region = os.environ.get("AWS_DEFAULT_REGION") or EKS_REGION
        saved_current = self._current_context()

        for alias, cluster in EKS_CONTEXTS:
            try:
                r = subprocess.run(
                    ["aws", "eks", "update-kubeconfig", "--name", cluster, "--region", region, "--alias", alias],
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    check=False,
                    timeout=30,
                )
            except (OSError, subprocess.TimeoutExpired) as exc:
                results[alias] = f"failed — {exc}"
                continue
            if r.returncode != 0:
                err = (r.stderr or r.stdout or "").strip().splitlines()
                results[alias] = f"failed — {err[-1] if err else 'update-kubeconfig failed'}"
            else:
                results[alias] = "ok"

        # ``update-kubeconfig`` sets current-context to the last alias it wrote.
        # Restore the user's choice, or default to pysae-dev on a fresh config.
        target = saved_current or EKS_CONTEXTS[0][0]
        if target in self._existing_contexts():
            self._kubectl("config", "use-context", target, timeout=5)

        # Refresh the per-context kubeconfig files the Kubernetes MCP servers
        # rely on (they follow the current-context, not K8S_CONTEXT).
        for alias, _cluster in EKS_CONTEXTS:
            if results.get(alias) == "ok":
                kubeconfig.write_dedicated_kubeconfig(alias)

        return results

    def do_install(self) -> InstallReport:
        # When the only reason we're re-run is missing contexts
        # (``needs_reconfigure_contexts``), skip re-downloading the binary.
        binary_current = False
        installed_version = ""
        if binary.which(self.binary_name):
            installed_version = binary.get_version(self.binary_name, version_arg=self.version_arg) or ""
            try:
                latest = self.fetch_latest_version().lstrip("v")
            except Exception:  # noqa: BLE001
                latest = ""
            if installed_version and (not latest or not binary.needs_update(installed_version, latest)):
                binary_current = True

        if binary_current:
            return InstallReport(version=installed_version, method="already up-to-date")
        return super().do_install()

    def do_configure(self) -> InstallReport:
        report = InstallReport(action="configure")
        contexts = self._configure_contexts()
        if contexts:
            report.extra["contexts"] = contexts
        else:
            report.method = "nothing to configure"
        return report

    # ------------------------------------------------------------------
    # State / display
    # ------------------------------------------------------------------

    def get_state(self) -> ToolState:
        state = super().get_state()
        existing = set() if state.needs_install else self._existing_contexts()
        contexts: dict[str, dict[str, Any]] = {}
        any_missing = False
        for alias, _cluster in EKS_CONTEXTS:
            if state.needs_install:
                contexts[alias] = {"ok": False, "error": "binary not installed"}
                continue
            present = alias in existing
            contexts[alias] = {"ok": present, "error": "" if present else "context not configured"}
            if not present:
                any_missing = True
        state.extra["contexts"] = contexts
        if not state.needs_install:
            # A missing EKS context makes ``tools install`` re-run the EKS
            # configuration step.
            state.extra["auth_ok"] = not any_missing
            if any_missing:
                state.extra["auth_message"] = "one or more Pysae EKS contexts are not configured"
                state.extra["needs_reconfigure_contexts"] = True
                state.needs_reconfigure = True
        return state

    def extract_identity(self, state: dict[str, Any]) -> list[tuple[str, str | None]]:
        lines: list[tuple[str, str | None]] = []
        contexts = state.get("contexts", {})
        for name, data in contexts.items():
            if not isinstance(data, dict):
                continue
            ok = bool(data.get("ok"))
            err = str(data.get("error", "")).strip()
            icon = "✓" if ok else "✗"
            suffix = f" — {err}" if err and not ok else ""
            lines.append((f"{icon} {name}{suffix}", typer.colors.GREEN if ok else typer.colors.RED))
        return lines


tool = KubectlTool()
