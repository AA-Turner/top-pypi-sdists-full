"""Install fnm — Fast Node Manager (Schniz/fnm).

Strategy:

- Windows: ``winget install Schniz.fnm``.
- macOS: ``brew install fnm``.
- Linux (and macOS without brew): the official ``curl|bash`` installer with
  ``--skip-shell`` — we own the dotfile wiring ourselves to stay idempotent.

After install, the tool wires ``eval "$(fnm env --use-on-cd)"`` (or the
PowerShell equivalent) into the user's shell profile(s) so ``node`` resolves
to the fnm-managed version in subsequent sessions.

This tool is OPTIONAL but ``default_selected=True`` — users whose Node is
already installed via another channel (apt, brew, manual installer) can
deselect it and rely on the existing ``node``.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import typer

from ..common import winpath
from .common import binary, github, platform
from .common.base import BinaryTool, InstallReport, ToolState
from .common.download import download_and_install_binary

FNM_INSTALL_URL = "https://fnm.vercel.app/install"
FNM_REPO = "Schniz/fnm"

FNM_INIT_BASH = 'eval "$(fnm env --use-on-cd --shell bash)"'
FNM_INIT_ZSH = 'eval "$(fnm env --use-on-cd --shell zsh)"'
FNM_INIT_PS = "fnm env --use-on-cd | Out-String | Invoke-Expression"

# Sentinel marker so subsequent runs detect a prior wiring even if the user
# reformats the surrounding block.
FNM_MARKER = "# pysae-ai-tools: fnm (Node.js)"

# Dirs that are naturally on a user's interactive shell PATH on Linux/macOS.
# Used to decide whether ``fnm`` is callable from a fresh shell without us
# having to symlink it into ``~/.local/bin``.
_STANDARD_PATH_DIRS: frozenset[Path] = frozenset(
    {
        Path("/usr/local/bin"),
        Path("/usr/bin"),
        Path("/opt/homebrew/bin"),
        Path("/home/linuxbrew/.linuxbrew/bin"),
        Path.home() / ".local" / "bin",
    }
)


def find_fnm() -> str:
    """Locate the fnm binary, including common install dirs not yet on PATH.

    fnm's default install paths (``~/.local/share/fnm`` on Unix, the WinGet
    Links shim on Windows) may not be on the current process's PATH right
    after a fresh install — this helper covers them.
    """
    direct = shutil.which("fnm")
    if direct:
        return direct
    candidates: list[Path] = [
        Path.home() / ".local" / "share" / "fnm" / "fnm",
        Path.home() / ".fnm" / "fnm",
    ]
    if sys.platform == "win32":
        local_app_env = os.environ.get("LOCALAPPDATA")
        if local_app_env:
            local_app = Path(local_app_env)
        else:
            # LOCALAPPDATA unset: prefer %USERPROFILE% over Path.home(), which
            # can diverge from the real profile dir on non-standard setups.
            user_profile = os.environ.get("USERPROFILE")
            base = Path(user_profile) if user_profile else Path.home()
            local_app = base / "AppData" / "Local"
        candidates.extend(
            [
                local_app / "Microsoft" / "WinGet" / "Links" / "fnm.exe",
                local_app / "fnm" / "fnm.exe",
            ]
        )
    for c in candidates:
        if c.exists():
            return str(c)
    return ""


def _fnm_default_alias_dir() -> Path | None:
    """Path of fnm's ``default`` alias — where node/npm/npx land after
    ``fnm default <version>``.
    """
    home = Path.home()
    if sys.platform == "win32":
        appdata = Path(os.environ.get("APPDATA", str(home / "AppData" / "Roaming")))
        return appdata / "fnm" / "aliases" / "default"
    return home / ".local" / "share" / "fnm" / "aliases" / "default" / "bin"


def augment_path() -> None:
    """Make fnm + fnm-managed Node visible in the current Python process.

    fnm puts the default-aliased node under ``$FNM_DIR/aliases/default/bin``
    on Unix, and ``%APPDATA%\\fnm\\aliases\\default`` on Windows. Without
    prepending those, sibling install steps (e.g. node.py running
    ``fnm install --lts``) wouldn't see the binary in this session.
    """
    extras: list[Path] = []

    fnm = find_fnm()
    if fnm:
        extras.append(Path(fnm).parent)

    alias = _fnm_default_alias_dir()
    if alias is not None:
        extras.append(alias)

    current = os.environ.get("PATH", "")
    parts: list[str] = []
    seen: set[str] = set()
    for p in extras:
        if not p.exists():
            continue
        s = str(p)
        if s in seen:
            continue
        seen.add(s)
        parts.append(s)
    if current:
        parts.append(current)
    os.environ["PATH"] = os.pathsep.join(parts)


def alias_dir_in_user_path() -> bool:
    """Windows-only: True when the fnm default-alias dir is on the user-
    scope registry PATH (so cmd.exe sessions see node natively).
    """
    if sys.platform != "win32":
        return True
    alias = _fnm_default_alias_dir()
    if alias is None:
        return True
    target = str(alias).rstrip("\\/").lower()
    try:
        import winreg

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as key:
            try:
                raw, _ = winreg.QueryValueEx(key, "Path")
            except FileNotFoundError:
                return False
    except (ImportError, OSError):
        return False
    if not isinstance(raw, str) or not raw:
        return False
    expanded = os.path.expandvars(raw)
    for part in expanded.split(os.pathsep):
        cleaned = part.strip().strip('"').rstrip("\\/").lower()
        if cleaned == target:
            return True
    return False


def _on_user_path(plat: platform.Platform) -> bool:
    """True when ``fnm`` is reachable from a fresh interactive shell.

    On Windows, winget drops a shim under its ``Links`` dir which is on
    PATH out of the box — nothing to verify.

    On Linux/macOS, we check the filesystem directly rather than ``PATH``
    of the current Python process, because ``augment_path`` may already
    have prepended fnm's install dir for our own use — that wouldn't
    reflect what the user's bash/zsh sees.
    """
    if plat.is_windows:
        return True
    return any((d / "fnm").exists() for d in _STANDARD_PATH_DIRS)


def ensure_on_user_path(fnm_path: str, plat: platform.Platform) -> Path | None:
    """Symlink ``fnm`` into ``~/.local/bin`` when its install dir isn't
    already on the user's shell PATH. Idempotent; returns the symlink
    path when one was created (or refreshed), None otherwise.

    Why: the curl installer puts the binary in ``~/.local/share/fnm/fnm``
    which isn't on PATH. Without a symlink, the dotfile-wired
    ``eval "$(fnm env ...)"`` errors out on every shell start because
    ``fnm`` itself can't be found.

    ``~/.local/bin`` is XDG-standard and on PATH by default on Ubuntu/
    Fedora/macOS (path_helper). Skipped on Windows.
    """
    if _on_user_path(plat):
        return None
    target = Path.home() / ".local" / "bin" / "fnm"
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.is_symlink():
            if Path(os.readlink(target)) == Path(fnm_path):
                return None
            target.unlink()
        elif target.exists():
            # Real file already there — don't clobber.
            return None
        target.symlink_to(fnm_path)
    except OSError:
        return None
    return target


def _wire_dotfile(path: Path, line: str) -> bool:
    """Append the fnm init block to ``path`` when missing. Creates the file
    if absent. Returns True when the file was modified."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        existing = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
    except OSError:
        return False
    if FNM_MARKER in existing or "fnm env" in existing:
        return False
    block = f"\n{FNM_MARKER}\n{line}\n"
    try:
        new_content = existing.rstrip() + "\n" + block if existing else block.lstrip("\n")
        path.write_text(new_content, encoding="utf-8")
    except OSError:
        return False
    return True


def wire_shell_init(plat: platform.Platform) -> list[str]:
    """Append fnm init to user shell profile(s). Idempotent.

    Linux/macOS: ``~/.bashrc``, ``~/.bash_profile``, ``~/.zshrc``.
    Windows: PowerShell Core + Windows PowerShell profiles.

    Returns the list of files modified during this run.
    """
    home = Path.home()
    targets: list[tuple[Path, str]]
    if plat.is_windows:
        documents = home / "Documents"
        targets = [
            (documents / "PowerShell" / "profile.ps1", FNM_INIT_PS),
            (documents / "WindowsPowerShell" / "profile.ps1", FNM_INIT_PS),
        ]
    else:
        targets = [
            (home / ".bashrc", FNM_INIT_BASH),
            (home / ".bash_profile", FNM_INIT_BASH),
            (home / ".zshrc", FNM_INIT_ZSH),
        ]

    modified: list[str] = []
    for path, line in targets:
        if _wire_dotfile(path, line):
            modified.append(str(path))
    return modified


def shell_init_wired(plat: platform.Platform) -> bool:
    """Return True when at least one shell profile has fnm init wired."""
    home = Path.home()
    candidates: list[Path]
    if plat.is_windows:
        candidates = [
            home / "Documents" / "PowerShell" / "profile.ps1",
            home / "Documents" / "WindowsPowerShell" / "profile.ps1",
        ]
    else:
        candidates = [home / ".bashrc", home / ".bash_profile", home / ".zshrc"]
    for path in candidates:
        try:
            if path.exists() and "fnm env" in path.read_text(encoding="utf-8", errors="replace"):
                return True
        except OSError:
            continue
    return False


class FnmTool(BinaryTool):
    name = "fnm"
    binary_name = "fnm"
    cli_help = "Install fnm (Fast Node Manager) and wire its shell init"
    winget_package = "Schniz.fnm"
    brew_package = "fnm"

    def fetch_latest_version(self) -> str:
        try:
            tag = github.latest_release(FNM_REPO)
        except Exception:  # noqa: BLE001
            return ""
        return tag.lstrip("v")

    def get_state(self) -> ToolState:
        # Surface fnm even if its install dir isn't on the current PATH yet.
        augment_path()
        state = super().get_state()
        plat = platform.detect()

        located = find_fnm()
        installed = bool(located)
        if installed and not state.extra.get("binary", {}).get("installed"):
            # ``binary.status`` missed it because PATH didn't cover the install
            # dir — patch the payload so the tool reports as installed.
            state.extra["binary"] = {
                "name": self.binary_name,
                "installed": True,
                "path": located,
                "version": binary.get_version(located, version_arg=self.version_arg) or "",
            }
            state.needs_install = False

        wired = shell_init_wired(plat) if installed else False
        state.extra["shell_init_wired"] = wired
        if installed and not wired:
            # Binary in place but the user's shell still won't pick up node-by-fnm.
            state.needs_update = True

        on_path = _on_user_path(plat) if installed else False
        state.extra["on_user_path"] = on_path
        if installed and not on_path:
            # ``fnm`` exists but its dir isn't on the shell PATH — the dotfile
            # eval will fail on every session start until we symlink it.
            state.needs_update = True

        # Windows: also flag for re-run when the default-alias dir isn't
        # on the user-scope registry PATH yet — without it, cmd.exe (which
        # never sources our PowerShell init) can't find ``node``.
        if plat.is_windows:
            user_path_ok = alias_dir_in_user_path() if installed else False
            state.extra["alias_dir_in_user_path"] = user_path_ok
            if installed and not user_path_ok:
                state.needs_update = True
        return state

    def install_linux(self, plat: platform.Platform) -> InstallReport:
        return self._curl_install()

    def install_macos(self, plat: platform.Platform) -> InstallReport:
        # brew_package is set, so install_binary tries brew first and only
        # falls into install_macos when brew is unavailable.
        return self._curl_install()

    def install_windows(self, plat: platform.Platform) -> InstallReport:
        # winget_package is set; this hook fires only when winget is absent
        # (e.g. some CI runners). Fall back to the official GitHub release zip:
        # fnm-windows.zip ships fnm.exe at its root.
        try:
            tag = github.latest_release(FNM_REPO)
        except Exception as exc:  # noqa: BLE001
            return InstallReport(error=f"could not fetch fnm release: {exc}")
        url = f"https://github.com/{FNM_REPO}/releases/download/{tag}/fnm-windows.zip"
        try:
            target = download_and_install_binary(url, self.binary_name, archive_member="fnm.exe")
        except Exception as exc:  # noqa: BLE001
            return InstallReport(error=f"fnm download/install failed: {exc}")
        return InstallReport(method="github release zip", path=str(target))

    def _curl_install(self) -> InstallReport:
        try:
            proc = subprocess.run(
                ["bash", "-c", f"curl -fsSL {FNM_INSTALL_URL} | bash -s -- --skip-shell"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
                timeout=180,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            return InstallReport(error=f"fnm installer failed: {exc}")
        if proc.returncode != 0:
            return InstallReport(error=(proc.stderr or proc.stdout).strip()[:500])
        return InstallReport(method="curl|bash")

    def do_install(self) -> InstallReport:
        # Try the package-manager / curl path first.
        report = self.install_binary()
        if report.error:
            return report

        augment_path()
        located = find_fnm()
        if not located:
            return InstallReport(error="fnm not found after install — check $PATH and re-run")

        plat = platform.detect()
        wired = wire_shell_init(plat)
        symlink = ensure_on_user_path(located, plat)

        version = binary.get_version(located, version_arg=self.version_arg)
        report.version = version or report.version
        report.path = located
        report.extra.setdefault("shell_init", wired or "already wired")
        if symlink is not None:
            report.extra["symlink"] = str(symlink)

        # On Windows, persist the default-alias dir into the user PATH so
        # cmd.exe (which has no profile init equivalent) finds ``node``
        # natively. The shell init wiring above only covers PowerShell.
        if plat.is_windows:
            alias = _fnm_default_alias_dir()
            if alias is not None and winpath.ensure_in_user_path(str(alias)):
                report.extra["user_path_added"] = str(alias)
                # Reflect the registry change in the running process so
                # ``node.py`` (which runs right after fnm here) can see
                # node without waiting for a new shell.
                winpath.refresh_process_path_from_registry(force=True)
        return report

    def extract_identity(self, state: dict[str, Any]) -> list[tuple[str, str | None]]:
        wired = bool(state.get("shell_init_wired"))
        icon = "✓" if wired else "✗"
        color = typer.colors.GREEN if wired else typer.colors.YELLOW
        return [(f"{icon} shell init", color)]

    def format_install(self, report: InstallReport) -> None:
        if report.error:
            typer.echo(f"FAILED: {report.error}", err=True)
            return
        line = "fnm installed"
        if report.version:
            line += f" ({report.version})"
        if report.method:
            line += f" via {report.method}"
        typer.echo(line)
        wired = report.extra.get("shell_init")
        if wired:
            label = ", ".join(wired) if isinstance(wired, list) and wired else (wired if wired else "no change")
            typer.echo(f"  shell init: {label}")
        symlink = report.extra.get("symlink")
        if symlink:
            typer.echo(f"  symlink: {symlink} (so 'fnm' resolves in fresh shells)")
        added = report.extra.get("user_path_added")
        if added:
            typer.echo(f"  user PATH: added {added} (open a new shell to pick it up)")


tool = FnmTool()
