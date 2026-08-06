"""Download archives, extract them, and install binaries to the system."""

import os
import shutil
import sys
import tarfile
import tempfile
import zipfile
from pathlib import Path

import httpx

from .privileged import run_privileged


def default_install_prefix() -> Path:
    """Per-OS default install prefix.

    - Linux/macOS: /usr/local/bin (requires sudo)
    - Windows: %USERPROFILE%\\.local\\bin (matches install.cmd's BINDIR;
      already added to user PATH by the bootstrap installer, so installed
      binaries are immediately runnable from any shell).
    """
    if sys.platform == "win32":
        return Path.home() / ".local" / "bin"
    return Path("/usr/local/bin")


def ensure_on_path(directory: Path) -> bool:
    """Return True when `directory` is in $PATH (or %PATH% on Windows)."""
    parts = os.environ.get("PATH", "").split(os.pathsep)
    return any(Path(p) == directory for p in parts if p)


def _augment_process_path(directory: Path) -> None:
    """Prepend ``directory`` to the current process's ``PATH`` if missing.

    Lets sibling tools (e.g. argocd's auth flow calling ``argocd context``)
    find a freshly installed binary without forcing the user to restart
    their shell. Only affects the current Python process and its children.
    """
    if ensure_on_path(directory):
        return
    current = os.environ.get("PATH", "")
    os.environ["PATH"] = f"{directory}{os.pathsep}{current}" if current else str(directory)


def download(url: str, dest: Path, timeout: float = 120.0) -> None:
    """Stream-download a URL to a local path."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    with httpx.stream("GET", url, timeout=timeout, follow_redirects=True) as response:
        response.raise_for_status()
        with dest.open("wb") as fh:
            for chunk in response.iter_bytes(chunk_size=64 * 1024):
                fh.write(chunk)


def _extract_zip_preserving_mode(archive: Path, dest: Path) -> None:
    """Extract a zip, restoring Unix file permissions from ``external_attr``.

    ``zipfile.extractall`` ignores the Unix permission bits stored in the zip
    entry's ``external_attr`` (upper 16 bits), so executables lose their ``+x``.
    The AWS CLI v2 installer, for example, ships ``aws/dist/aws`` with mode
    0755 — without this, the bundled installer fails silently and reports
    "Found same AWS CLI version. Skipping install."
    """
    with zipfile.ZipFile(archive) as zf:
        for info in zf.infolist():
            extracted = zf.extract(info, dest)
            if sys.platform == "win32" or info.is_dir():
                continue
            mode = (info.external_attr >> 16) & 0xFFFF
            if mode:
                os.chmod(extracted, mode)


def extract(archive: Path, dest: Path) -> None:
    """Extract a .tar.gz, .tgz, .tar, or .zip archive to a destination directory."""
    dest.mkdir(parents=True, exist_ok=True)
    name = archive.name.lower()
    if name.endswith((".tar.gz", ".tgz")):
        with tarfile.open(archive, "r:gz") as tar:
            tar.extractall(dest, filter="data")
    elif name.endswith(".tar"):
        with tarfile.open(archive, "r:") as tar:
            tar.extractall(dest, filter="data")
    elif name.endswith(".zip"):
        _extract_zip_preserving_mode(archive, dest)
    else:
        raise ValueError(f"Unsupported archive format: {archive.name}")


def _is_user_writable(path: Path) -> bool:
    """True when we can write to ``path`` without sudo.

    A path under the user's home is always assumed writable; otherwise we
    walk up to the nearest existing ancestor and probe it with ``os.access``
    (so a not-yet-created dir whose parent is writable counts as writable).
    """
    try:
        home = Path.home()
        if path == home or home in path.parents:
            return True
    except (OSError, RuntimeError):
        pass
    probe = path
    while not probe.exists():
        if probe.parent == probe:
            return False
        probe = probe.parent
    return os.access(probe, os.W_OK)


def _copy_executable(source: Path, target: Path, mode: int) -> Path:
    """Copy ``source`` to ``target`` (creating parents) and set its mode."""
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    target.chmod(mode)
    _augment_process_path(target.parent)
    return target


def install_binary(source: Path, name: str, prefix: str | Path | None = None, mode: int = 0o755) -> Path:
    """Install a single binary to a system prefix.

    On Windows, copies the binary to the per-user install dir (no admin
    required) and ensures the `.exe` suffix. On Linux/macOS, copies directly
    when the prefix is user-writable, otherwise tries `sudo install`, and as a
    last resort falls back to the per-user ``~/.local/bin`` — so a locked-down
    host without sudo still gets a working install instead of a hard failure.
    """
    prefix_path = Path(prefix) if prefix is not None else default_install_prefix()

    target_name = name
    if sys.platform == "win32" and not name.lower().endswith(".exe"):
        target_name = f"{name}.exe"

    target = prefix_path / target_name

    if sys.platform == "win32":
        return _copy_executable(source, target, mode)

    # User-writable prefix (e.g. ~/.local/bin passed explicitly): no sudo needed.
    if _is_user_writable(prefix_path):
        return _copy_executable(source, target, mode)

    # System prefix (e.g. /usr/local/bin): privileged install. Goes through
    # run_privileged so a sudo password prompt is announced and visible instead
    # of being swallowed by a captured stream.
    result = run_privileged(
        ["install", "-m", oct(mode)[2:], str(source), str(target)],
        what=f"Installing {target_name} into {prefix_path}",
        timeout=120,
    )
    if result.ok:
        return target

    # Last resort: the per-user ~/.local/bin never needs sudo. Keeps the
    # install non-interactive on hosts where sudo is missing or refused.
    fallback = Path.home() / ".local" / "bin"
    return _copy_executable(source, fallback / target_name, mode)


def download_and_install_binary(
    url: str,
    binary_name: str,
    *,
    archive_member: str | None = None,
    prefix: str | Path | None = None,
) -> Path:
    """End-to-end: download an archive, extract it, install the named binary.

    Args:
        url: Download URL of the archive (or raw binary).
        binary_name: Name of the binary to install (e.g. 'glab').
        archive_member: Path inside the archive to the binary
            (e.g. 'bin/glab'). Required for archives, ignored for raw binaries.
        prefix: System install prefix.
    """
    with tempfile.TemporaryDirectory(prefix="pysae-install-") as tmp:
        tmp_path = Path(tmp)
        archive = tmp_path / Path(url).name
        download(url, archive)

        # Detect raw binary vs archive
        is_archive = archive.suffix.lower() in {".gz", ".tgz", ".tar", ".zip"} or archive.name.endswith(".tar.gz")

        if not is_archive:
            return install_binary(archive, binary_name, prefix=prefix)

        if archive_member is None:
            raise ValueError("archive_member is required for archive downloads")

        extract_dir = tmp_path / "extracted"
        extract(archive, extract_dir)
        source = extract_dir / archive_member
        if not source.exists():
            # Search recursively as a fallback
            candidates = list(extract_dir.rglob(Path(archive_member).name))
            if not candidates:
                raise FileNotFoundError(f"Binary {binary_name!r} not found in archive (looked for {archive_member!r})")
            source = candidates[0]
        return install_binary(source, binary_name, prefix=prefix)
