"""Install or update codex-flow via npm.

``codex-flow`` (github.com/Dmatut7/codex-flow, npm ``codex-flow``) is the community
mirror of Claude Code's ``Workflow`` tool for Codex: it turns a ``*.workflow.ts``
script exposing ``ctx.agent()`` / ``ctx.parallel()`` / ``ctx.pipeline()`` /
``ctx.phase()`` into parallel, resumable, schema-validated Codex sub-agents. It is
the runtime the Codex port of ``/code-autopilot-batch`` runs its parallel phase on.

**Optional, local/dev only** — like every assistant-side tool, it is never required
in CI (the CI stays on Claude). It is a **community package**, so treating it as a
managed tool is a deliberate supply-chain decision; it is opt-in and off by default.

Installed through npm exactly like the Codex CLI (idempotent — re-running upgrades to
the latest), so no public version manifest is consulted. fnm-managed Node is surfaced
via :func:`fnm.augment_path` before shelling out, otherwise ``npm`` would not resolve
in a non-interactive run. After a successful install, ``codex-flow install-codex`` is
run best-effort when the Codex CLI is present, to register codex-flow with Codex.
"""

import shutil
import subprocess

from . import fnm as fnm_module
from .common import binary, platform
from .common.base import BinaryTool, InstallReport

_NPM_INSTALL = "npm install -g codex-flow"


class CodexFlowTool(BinaryTool):
    name = "codex-flow"
    binary_name = "codex-flow"
    cli_help = "Install/update codex-flow (Workflow mirror for Codex)"

    def fetch_latest_version(self) -> str:
        # No public version manifest consulted — npm is the source of truth.
        return ""

    def install_linux(self, plat: platform.Platform) -> InstallReport:
        return self._npm_install()

    def install_macos(self, plat: platform.Platform) -> InstallReport:
        return self._npm_install()

    def install_windows(self, plat: platform.Platform) -> InstallReport:
        return self._npm_install()

    def _npm_install(self) -> InstallReport:
        # fnm-managed Node lives under $FNM_DIR/aliases/default/bin, off the session
        # PATH until `fnm env` is sourced — surface it so `npm` resolves here.
        fnm_module.augment_path()
        try:
            # shell=True so Windows resolves ``npm`` to ``npm.cmd`` on PATH.
            r = subprocess.run(
                _NPM_INSTALL,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
                timeout=300,
                shell=True,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            return InstallReport(error=f"installer failed: {exc}")
        if r.returncode != 0:
            return InstallReport(error=(r.stderr or r.stdout).strip()[:500])
        self._register_with_codex()
        return InstallReport(
            version=binary.get_version(self.binary_name, "--version"),
            path=shutil.which(self.binary_name) or "",
            method="npm",
        )

    def _register_with_codex(self) -> None:
        """Wire codex-flow into Codex (``codex-flow install-codex``), best-effort.

        Only when the Codex CLI is present — the registration is meaningless without
        it — and never fatal: a failure here does not fail the npm install.
        """
        if shutil.which("codex") is None or shutil.which(self.binary_name) is None:
            return
        try:
            subprocess.run(
                [self.binary_name, "install-codex"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
                timeout=120,
            )
        except (OSError, subprocess.TimeoutExpired):
            pass


tool = CodexFlowTool()
