"""Privilege boundary for packaged binary self-update."""

from collections.abc import Mapping
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile


PRIVILEGED_CA_BUNDLE_ENV = "RUNLAYER_SELF_UPDATE_CA_BUNDLE"
PRIVILEGED_CA_DIR_ENV = "RUNLAYER_SELF_UPDATE_CA_DIR"
PRIVILEGED_HOST_ENV = "RUNLAYER_SELF_UPDATE_HOST"
PRIVILEGED_ORG_KEY_ENV = "RUNLAYER_SELF_UPDATE_ORG_KEY"
_INSTALL_LAYOUTS = {
    ("macos", "ai-watch"): (
        Path("/usr/local/bin/aiwatch"),
        Path("/usr/local/lib/runlayer/aiwatch"),
        Path("/usr/local"),
    ),
    ("macos", "cli"): (
        Path("/usr/local/bin/runlayer"),
        Path("/usr/local/lib/runlayer/runlayer"),
        Path("/usr/local"),
    ),
    ("macos", "desktop"): (
        Path("/usr/local/bin/runlayer"),
        Path("/usr/local/lib/runlayer/runlayer"),
        Path("/usr/local"),
    ),
    ("linux", "ai-watch"): (
        Path("/usr/bin/aiwatch"),
        Path("/usr/lib/runlayer/aiwatch"),
        Path("/usr"),
    ),
    ("linux", "cli"): (
        Path("/usr/bin/runlayer"),
        Path("/usr/lib/runlayer"),
        Path("/usr"),
    ),
}
_PRIVILEGED_TEMP_ROOT = Path("/var/tmp")
_TEMP_ENV_NAMES = ("TMPDIR", "TMP", "TEMP")


def _requires_root(argv: list[str]) -> bool:
    if not argv:
        return False
    executable = argv[0]
    return (
        executable == "/usr/sbin/installer"
        or (executable == "/usr/bin/dpkg" and "--install" in argv)
        or (executable == "/usr/bin/rpm" and "-U" in argv)
    )


def elevating_runner(
    argv: list[str],
    *,
    check: bool,
    capture_output: bool,
    text: bool,
    shell: bool,
    env: Mapping[str, str] | None,
) -> subprocess.CompletedProcess[str]:
    """Run installer tooling after enforcing whole-process elevation."""
    getuid = getattr(os, "geteuid", None)
    if callable(getuid) and getuid() != 0 and _requires_root(argv):
        raise RuntimeError(
            "Native installer mutation requires the privileged self-update continuation"
        )
    return subprocess.run(
        argv,
        check=check,
        capture_output=capture_output,
        text=text,
        shell=shell,
        env=env,
    )


def _validate_secure_node(
    path: Path, *, required_uid: int, follow_symlinks: bool = True
) -> os.stat_result:
    try:
        metadata = path.stat() if follow_symlinks else path.lstat()
    except OSError as exc:
        raise RuntimeError(f"Installed update path is unavailable: {path}") from exc
    if metadata.st_uid != required_uid:
        raise RuntimeError(f"Installed update path is not root-owned: {path}")
    if not stat.S_ISLNK(metadata.st_mode) and metadata.st_mode & 0o022:
        raise RuntimeError(f"Installed update path is group/other-writable: {path}")
    if os.access(path, os.W_OK):
        raise RuntimeError(f"Installed update path is writable by the caller: {path}")
    return metadata


def _validate_secure_chain(start: Path, stop: Path, *, required_uid: int) -> None:
    if start != stop and stop not in start.parents:
        raise RuntimeError(f"Installed update path escapes its trusted root: {start}")
    current = start
    while True:
        metadata = _validate_secure_node(
            current,
            required_uid=required_uid,
            follow_symlinks=False,
        )
        if stat.S_ISLNK(metadata.st_mode):
            raise RuntimeError(
                f"Installed update path contains a symbolic link: {current}"
            )
        if current == stop:
            break
        current = current.parent


def validate_installation_layout(
    *,
    entrypoint: Path,
    bundle_root: Path,
    installation_root: Path,
    running_executable: Path,
    required_uid: int,
    ancestor_stop: Path,
) -> Path:
    """Return a stable packaged executable safe to authorize through sudo."""
    _validate_secure_chain(installation_root, ancestor_stop, required_uid=required_uid)
    _validate_secure_chain(
        entrypoint.parent, installation_root, required_uid=required_uid
    )
    _validate_secure_chain(
        bundle_root.parent, installation_root, required_uid=required_uid
    )
    _validate_secure_node(entrypoint, required_uid=required_uid, follow_symlinks=False)
    bundle_metadata = _validate_secure_node(
        bundle_root,
        required_uid=required_uid,
        follow_symlinks=False,
    )
    if stat.S_ISLNK(bundle_metadata.st_mode):
        raise RuntimeError("Installed package bundle must not be a symbolic link")
    try:
        resolved_entrypoint = entrypoint.resolve(strict=True)
        resolved_bundle = bundle_root.resolve(strict=True)
        resolved_running = running_executable.resolve(strict=True)
    except OSError as exc:
        raise RuntimeError("Installed update executable cannot be resolved") from exc
    if resolved_entrypoint != resolved_running:
        raise RuntimeError(
            "Self-update requires the fixed package-installed executable"
        )
    if not resolved_entrypoint.is_relative_to(resolved_bundle):
        raise RuntimeError("Installed update executable escapes its package bundle")
    if not resolved_bundle.is_dir() or not resolved_entrypoint.is_file():
        raise RuntimeError("Installed update bundle layout is invalid")

    _validate_secure_chain(
        resolved_entrypoint,
        resolved_bundle,
        required_uid=required_uid,
    )

    for path in (resolved_bundle, *resolved_bundle.rglob("*")):
        metadata = _validate_secure_node(
            path,
            required_uid=required_uid,
            follow_symlinks=False,
        )
        if stat.S_ISLNK(metadata.st_mode):
            try:
                resolved_link = path.resolve(strict=True)
            except OSError as exc:
                raise RuntimeError(
                    f"Installed bundle has a broken link: {path}"
                ) from exc
            if not resolved_link.is_relative_to(resolved_bundle):
                raise RuntimeError(
                    f"Installed bundle link escapes its package bundle: {path}"
                )
            _validate_secure_chain(
                resolved_link,
                resolved_bundle,
                required_uid=required_uid,
            )
    return resolved_entrypoint


def _trusted_installed_executable(*, package: str, platform: str) -> Path:
    layout = _INSTALL_LAYOUTS.get((platform, package))
    if layout is None:
        raise RuntimeError(f"No packaged update layout for {platform}/{package}")
    entrypoint, bundle_root, installation_root = layout
    return validate_installation_layout(
        entrypoint=entrypoint,
        bundle_root=bundle_root,
        installation_root=installation_root,
        running_executable=Path(sys.executable),
        required_uid=0,
        ancestor_stop=Path("/"),
    )


def configure_privileged_temp_root() -> None:
    try:
        metadata = _PRIVILEGED_TEMP_ROOT.stat()
    except OSError as exc:
        raise RuntimeError("Privileged update temp root is unavailable") from exc
    if (
        metadata.st_uid != 0
        or not stat.S_ISDIR(metadata.st_mode)
        or not metadata.st_mode & stat.S_ISVTX
    ):
        raise RuntimeError("Privileged update temp root is not root-owned and sticky")
    for name in _TEMP_ENV_NAMES:
        os.environ.pop(name, None)
    tempfile.tempdir = str(_PRIVILEGED_TEMP_ROOT)


def run_privileged_update(
    *,
    package: str,
    platform: str,
    host: str,
    org_api_key: str,
    ca_bundle: str | None = None,
    ca_bundle_dir: str | None = None,
) -> None:
    """Validate a non-root packaged binary, then re-exec the update as root."""
    getuid = getattr(os, "geteuid", None)
    if not callable(getuid) or getuid() == 0:
        raise RuntimeError("Privilege handoff requires a non-root POSIX caller")
    executable = _trusted_installed_executable(package=package, platform=platform)
    env = {
        PRIVILEGED_HOST_ENV: host,
        PRIVILEGED_ORG_KEY_ENV: org_api_key,
    }
    preserved = [
        PRIVILEGED_HOST_ENV,
        PRIVILEGED_ORG_KEY_ENV,
    ]
    if ca_bundle:
        env[PRIVILEGED_CA_BUNDLE_ENV] = ca_bundle
        preserved.append(PRIVILEGED_CA_BUNDLE_ENV)
    if ca_bundle_dir:
        env[PRIVILEGED_CA_DIR_ENV] = ca_bundle_dir
        preserved.append(PRIVILEGED_CA_DIR_ENV)
    result = subprocess.run(
        [
            "/usr/bin/sudo",
            f"--preserve-env={','.join(preserved)}",
            "--",
            str(executable),
            "__self-update-root",
            package,
        ],
        check=False,
        shell=False,
        env=env,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"Privileged update process failed with exit code {result.returncode}"
        )
