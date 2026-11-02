"""Shell profile detection and environment variable persistence utilities.

Provides functions to detect the user's shell type and profile file, and to
persist environment variables (``export`` lines) to shell profile files in an
idempotent, error-tolerant way.

Supported shells: bash (``~/.bashrc``), zsh (``~/.zshrc``), PowerShell
(``$PROFILE``).  Unknown shells cause persistence to be skipped gracefully.
"""

import os
import re
import shutil
import sys
from pathlib import Path

from ..subprocess_utils import run_safe

#: PowerShell interpreters to probe, most-preferred first (Core, then 5.1).
_POWERSHELL_EXECUTABLES = ("pwsh", "powershell")

#: ``$PROFILE`` members to query, most-specific first.
_POWERSHELL_PROFILE_EXPRESSIONS = (
    "$PROFILE.CurrentUserCurrentHost",
    "$PROFILE.CurrentUserAllHosts",
)

#: Prefix that forces UTF-8 stdout before evaluating a profile expression.
_POWERSHELL_UTF8_COMMAND_PREFIX = (
    "$utf8NoBom = New-Object System.Text.UTF8Encoding $false; "
    "[Console]::OutputEncoding = $utf8NoBom; "
    "$OutputEncoding = $utf8NoBom; "
)

#: Sub-directories of Documents that hold a PowerShell profile, newest first.
_POWERSHELL_PROFILE_DIRS = ("PowerShell", "WindowsPowerShell")

#: File name of the current-user/current-host PowerShell profile.
_POWERSHELL_PROFILE_FILENAME = "Microsoft.PowerShell_profile.ps1"


def _escape_for_double_quotes_posix(value: str) -> str:
    """Escape a value for safe inclusion inside POSIX double-quotes.

    Escapes ``\\``, ``"``, ``$``, and backtick — the characters that are
    special inside double-quoted strings in bash/zsh.
    """
    # Backslash must be escaped first to avoid double-escaping later replacements.
    value = value.replace("\\", "\\\\")
    value = value.replace('"', '\\"')
    value = value.replace("$", "\\$")
    value = value.replace("`", "\\`")
    return value


def _escape_for_double_quotes_powershell(value: str) -> str:
    """Escape a value for safe inclusion inside PowerShell double-quotes.

    In PowerShell double-quoted strings, backtick is the escape char and
    ``"`` must be doubled or backtick-escaped.  ``$`` triggers variable
    expansion and must be backtick-escaped.
    """
    value = value.replace("`", "``")
    value = value.replace('"', '`"')
    value = value.replace("$", "`$")
    return value


def detect_shell_type() -> str:
    """Detect the current shell type.

    Returns:
        One of ``"bash"``, ``"zsh"``, ``"powershell"``, or ``"unknown"``.
    """
    # On Windows, check for Git Bash / MSYS2 environment before defaulting
    # to PowerShell.  Git Bash sets $SHELL and/or MSYSTEM.
    if sys.platform == "win32":
        shell = os.environ.get("SHELL", "")
        if shell.endswith("bash"):
            return "bash"
        if shell.endswith("zsh"):
            return "zsh"
        if os.environ.get("MSYSTEM"):
            return "bash"
        return "powershell"

    shell = os.environ.get("SHELL", "")
    if shell.endswith("bash"):
        return "bash"
    if shell.endswith("zsh"):
        return "zsh"
    return "unknown"


def _run_powershell_expression(executable: str, expression: str) -> Path | None:
    """Evaluate a PowerShell *expression* and return its output as a path.

    Args:
        executable: PowerShell interpreter to invoke (``pwsh`` or ``powershell``).
        expression: PowerShell expression whose output is a single path.

    Returns:
        The resolved path, or ``None`` if the interpreter could not be run,
        exited non-zero, or produced no output.
    """
    try:
        command = f"{_POWERSHELL_UTF8_COMMAND_PREFIX}{expression}"
        result = run_safe(
            [executable, "-NoProfile", "-NonInteractive", "-Command", command],
            capture_output=True,
            text=True,
            timeout=30,
            shell=False,
        )
    except Exception:  # noqa: BLE001 — any launch failure means "not usable"
        return None

    if result.returncode != 0:
        return None

    value = (result.stdout or "").strip()
    if not value:
        return None
    return Path(value)


def _query_powershell_profile_path() -> Path | None:
    """Ask PowerShell itself where the current user's profile lives.

    PowerShell resolves ``$PROFILE`` through the Windows known-folder API, so
    the returned path honours OneDrive *Known Folder Move* redirection and
    localized Documents folder names (e.g. German ``Dokumente``).

    Returns:
        The profile path reported by the first PowerShell interpreter that
        answers, or ``None`` if no interpreter is available or answers.
    """
    for executable in _POWERSHELL_EXECUTABLES:
        if shutil.which(executable) is None:
            continue
        for expression in _POWERSHELL_PROFILE_EXPRESSIONS:
            candidate = _run_powershell_expression(executable, expression)
            if candidate is not None:
                return candidate
    return None


def _documents_dir_from_known_folder() -> Path | None:
    """Resolve the Documents folder via the Windows known-folder API.

    Uses ``SHGetKnownFolderPath(FOLDERID_Documents)``, which — unlike
    ``%USERPROFILE%\\Documents`` — reflects OneDrive redirection and
    localized folder names.

    Returns:
        The Documents directory, or ``None`` when the API is unavailable
        (non-Windows platforms) or the call fails.
    """
    import ctypes
    from ctypes import wintypes

    class _GUID(ctypes.Structure):
        _fields_ = (
            ("Data1", wintypes.DWORD),
            ("Data2", wintypes.WORD),
            ("Data3", wintypes.WORD),
            ("Data4", ctypes.c_ubyte * 8),
        )

    folder_id = _GUID(
        0xFDD39AD0,
        0x238F,
        0x46AF,
        (ctypes.c_ubyte * 8)(0xAD, 0xB4, 0x6C, 0x85, 0x48, 0x03, 0x69, 0xC7),
    )
    buffer = ctypes.c_wchar_p()

    try:
        windll = ctypes.windll  # type: ignore[attr-defined]  # Windows-only
        result = windll.shell32.SHGetKnownFolderPath(ctypes.byref(folder_id), 0, None, ctypes.byref(buffer))
        try:
            if result != 0 or not buffer.value:
                return None
            return Path(buffer.value)
        finally:
            windll.ole32.CoTaskMemFree(buffer)
    except Exception:  # noqa: BLE001 — treat any API failure as "unresolvable"
        return None


def _detect_powershell_profile() -> Path | None:
    """Detect the current user's PowerShell profile path on Windows.

    Resolution order:

    1. Ask PowerShell for ``$PROFILE`` (honours OneDrive Known Folder Move
       and localized Documents folder names).
    2. Probe the known-folder Documents directory for a ``PowerShell`` or
       ``WindowsPowerShell`` sub-directory.
    3. Probe ``%USERPROFILE%\\Documents`` for the same sub-directories.

    Returns:
        The profile path, or ``None`` if none of the strategies succeed.
    """
    profile = _query_powershell_profile_path()
    if profile is not None:
        return profile

    documents_dirs: list[Path] = []
    known_folder = _documents_dir_from_known_folder()
    if known_folder is not None:
        documents_dirs.append(known_folder)
    user_profile = os.environ.get("USERPROFILE", "")
    if user_profile:
        documents_dirs.append(Path(user_profile) / "Documents")

    for documents_dir in documents_dirs:
        for subdir in _POWERSHELL_PROFILE_DIRS:
            candidate = documents_dir / subdir / _POWERSHELL_PROFILE_FILENAME
            if candidate.parent.is_dir():
                return candidate
    return None


def detect_shell_profile() -> Path | None:
    """Detect the path to the user's shell profile file.

    Returns:
        Path to the profile file, or ``None`` if the shell cannot be
        determined or no PowerShell fallback strategy can resolve a profile
        location on Windows.  For PowerShell, a resolved profile path may be
        returned even when the file or its parent directory does not exist
        yet (repairs create them as needed).
    """
    shell_type = detect_shell_type()

    if shell_type == "bash":
        return Path.home() / ".bashrc"
    if shell_type == "zsh":
        return Path.home() / ".zshrc"
    if shell_type == "powershell":
        return _detect_powershell_profile()
    return None


def _path_assignment_contains_entry(line: str, path_entry: str, shell_type: str) -> bool:
    """Return whether a PATH-assignment line contains ``path_entry`` as a component."""
    if "=" not in line:
        return False

    delimiter = ":" if shell_type in ("bash", "zsh") else ";"
    value = line.split("=", 1)[1].strip()

    # Strip trailing inline shell comment that follows the closing quote.
    # Example: export PATH="/home/user/.agdt/bin:$PATH"  # managed
    # Without this, the "# managed" fragment becomes part of the last PATH
    # component, causing an exact-match failure (false negative).
    if value and value[0] in {'"', "'"}:
        quote = value[0]
        close_idx = value.rfind(quote, 1)
        if close_idx > 0:
            value = value[: close_idx + 1]

    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        value = value[1:-1]

    for component in value.split(delimiter):
        stripped = component.strip()
        if len(stripped) >= 2 and stripped[0] == stripped[-1] and stripped[0] in {'"', "'"}:
            stripped = stripped[1:-1]
        if stripped == path_entry:
            return True

    return False


def persist_env_var(
    profile_path: Path,
    var_name: str,
    var_value: str,
    shell_type: str,
    *,
    overwrite: bool = False,
) -> bool:
    """Persist an environment variable to a shell profile file.

    Appends an ``export VAR="value"`` (bash/zsh) or ``$env:VAR = "value"``
    (PowerShell) line to the profile.  Idempotent: skips if the variable is
    already set in the file (unless *overwrite* is ``True``).

    This function enforces **append/refresh-only** semantics: it will never
    remove or blank out an existing variable line.  When *overwrite* is
    ``True``, the existing line is replaced with the new value (a refresh);
    it is never deleted.  Callers that want to skip a variable entirely
    (e.g. when npm is disabled) should simply not call this function for
    that variable — the existing line will remain untouched.

    Args:
        profile_path: Path to the shell profile file.
        var_name: Environment variable name.
        var_value: Environment variable value.
        shell_type: One of ``"bash"``, ``"zsh"``, or ``"powershell"``.
        overwrite: Replace existing line if ``True``.

    Returns:
        ``True`` if the line was written (or replaced), ``False`` if skipped
        or on error.
    """
    try:
        # Build the export line with shell-appropriate escaping
        if shell_type in ("bash", "zsh"):
            safe_value = _escape_for_double_quotes_posix(var_value)
            new_line = f'export {var_name}="{safe_value}"'
            # Match common assignment patterns:
            #   export VAR=...  |  export VAR  |  VAR=...
            pattern = re.compile(rf"^(?:export\s+{re.escape(var_name)}(?:\s*=.*)?|{re.escape(var_name)}\s*=)")
        else:  # powershell
            safe_value = _escape_for_double_quotes_powershell(var_value)
            new_line = f'$env:{var_name} = "{safe_value}"'
            pattern = re.compile(rf"^\$env:{re.escape(var_name)}\s*=")

        # Read existing content
        profile_path.parent.mkdir(parents=True, exist_ok=True)
        if profile_path.exists():
            lines = profile_path.read_text(encoding="utf-8", errors="replace").splitlines(keepends=True)
        else:
            lines = []

        # Check for existing line
        existing_idx = None
        for idx, line in enumerate(lines):
            if pattern.match(line.strip()):
                existing_idx = idx
                break

        if existing_idx is not None and not overwrite:
            return False

        if existing_idx is not None and overwrite:
            # Replace in-place
            lines[existing_idx] = new_line + "\n"
        else:
            # Append with a comment marker
            if lines and not lines[-1].endswith("\n"):
                lines.append("\n")
            lines.append("# Added by agdt-setup\n")
            lines.append(new_line + "\n")

        profile_path.write_text("".join(lines), encoding="utf-8")
        return True
    except Exception as exc:  # noqa: BLE001
        print(f"  ⚠ Could not persist {var_name} to {profile_path}: {exc}", file=sys.stderr)
        return False


def persist_path_entry(
    profile_path: Path,
    path_entry: str,
    shell_type: str,
    *,
    overwrite: bool = False,
) -> bool:
    """Persist a PATH entry to a shell profile file.

    Appends an ``export PATH="<entry>:$PATH"`` (bash/zsh) or the equivalent
    PowerShell ``$env:PATH`` prepend to the profile.  Idempotent for a given
    ``path_entry``: if a PATH-assignment line already contains ``path_entry``
    as an exact PATH component, it is left unchanged unless ``overwrite`` is
    ``True``.

    Args:
        profile_path: Path to the shell profile file.
        path_entry: Directory to prepend to PATH.
        shell_type: One of ``"bash"``, ``"zsh"``, or ``"powershell"``.
        overwrite: If ``True`` and a PATH-assignment line already containing
            ``path_entry`` exists, replace that line with the new
            PATH-prepend line instead of leaving it unchanged.  When no such
            line exists, a new line is appended regardless of this flag.

    Returns:
        ``True`` if the line was written (or replaced), ``False`` if skipped
        or on error.
    """
    try:
        # Build new PATH-prepend line with shell-appropriate escaping
        if shell_type in ("bash", "zsh"):
            safe_entry = _escape_for_double_quotes_posix(path_entry)
            new_line = f'export PATH="{safe_entry}:$PATH"'
            # Match lines like: export PATH=... or PATH=...
            path_line_re = re.compile(r"^\s*(?:export\s+)?PATH\s*=")
        else:  # powershell
            safe_entry = _escape_for_double_quotes_powershell(path_entry)
            new_line = f'$env:PATH = "{safe_entry};$env:PATH"'
            path_line_re = re.compile(r"^\s*\$env:PATH\s*=", re.IGNORECASE)

        # Read existing content
        profile_path.parent.mkdir(parents=True, exist_ok=True)
        if profile_path.exists():
            content = profile_path.read_text(encoding="utf-8", errors="replace")
        else:
            content = ""

        # Check only actual PATH assignment lines for the entry
        lines = content.splitlines(keepends=True)
        found_in_path_line = False
        found_line_idx = None
        for idx, line in enumerate(lines):
            if path_line_re.match(line) and _path_assignment_contains_entry(line, path_entry, shell_type):
                found_in_path_line = True
                found_line_idx = idx
                break

        if found_in_path_line and not overwrite:
            return False

        if found_in_path_line and overwrite:
            # Replace the matching PATH line in-place
            lines[found_line_idx] = new_line + "\n"  # type: ignore[index]
            profile_path.write_text("".join(lines), encoding="utf-8")
            return True

        # Append
        if lines and not lines[-1].endswith("\n"):
            lines.append("\n")
        lines.append("# Added by agdt-setup\n")
        lines.append(new_line + "\n")
        profile_path.write_text("".join(lines), encoding="utf-8")
        return True
    except Exception as exc:  # noqa: BLE001
        print(f"  ⚠ Could not persist PATH entry to {profile_path}: {exc}", file=sys.stderr)
        return False
