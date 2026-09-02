"""Shared primitives for OS-native package installation."""

from __future__ import annotations

from collections.abc import Collection, Mapping
import ntpath
from pathlib import Path
import subprocess
from typing import Protocol

from runlayer_cli.updater import Artifact


_INSTALLER_PATH = "/usr/sbin:/usr/bin:/sbin:/bin"
_MAX_FAILURE_OUTPUT_CHARS = 4096


class CommandRunner(Protocol):
    def __call__(
        self,
        argv: list[str],
        *,
        check: bool,
        capture_output: bool,
        text: bool,
        shell: bool,
        env: Mapping[str, str] | None,
    ) -> subprocess.CompletedProcess[str]: ...


def default_command_runner(
    argv: list[str],
    *,
    check: bool,
    capture_output: bool,
    text: bool,
    shell: bool,
    env: Mapping[str, str] | None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv,
        check=check,
        capture_output=capture_output,
        text=text,
        shell=shell,
        env=env,
    )


class UnsupportedInstallerError(ValueError):
    """Artifact or host does not match a supported native installer slot."""


class InstallerVerificationError(RuntimeError):
    """The operating system did not verify the expected vendor identity."""


class InstallerExecutionError(RuntimeError):
    """The native installer could not be queried or executed safely."""


def posix_installer_environment(**overrides: str) -> dict[str, str]:
    """Build a minimal, deterministic environment for privileged installers."""
    env = {
        "LANG": "C",
        "LC_ALL": "C",
        "PATH": _INSTALLER_PATH,
    }
    env.update(overrides)
    return env


def windows_installer_environment(
    system_directory: str, **overrides: str
) -> dict[str, str]:
    """Build a minimal environment rooted in the OS-resolved System32 path."""
    windows_directory = ntpath.dirname(system_directory)
    powershell_directory = ntpath.join(
        system_directory,
        "WindowsPowerShell",
        "v1.0",
    )
    env = {
        "ComSpec": ntpath.join(system_directory, "cmd.exe"),
        "PATH": ";".join((system_directory, powershell_directory)),
        "PSModulePath": ntpath.join(powershell_directory, "Modules"),
        "SystemRoot": windows_directory,
        "TEMP": ntpath.join(windows_directory, "Temp"),
        "TMP": ntpath.join(windows_directory, "Temp"),
        "WINDIR": windows_directory,
    }
    env.update(overrides)
    return env


def combined_output(result: subprocess.CompletedProcess[str]) -> str:
    return "\n".join(part for part in (result.stdout, result.stderr) if part)


def _bounded_failure_output(result: subprocess.CompletedProcess[str]) -> str:
    output = combined_output(result).strip()
    if len(output) > _MAX_FAILURE_OUTPUT_CHARS:
        output = f"[output truncated]\n{output[-_MAX_FAILURE_OUTPUT_CHARS:]}"
    return output


def run_checked(
    runner: CommandRunner,
    argv: list[str],
    *,
    verification: bool,
    allowed_returncodes: Collection[int] = (0,),
    env: Mapping[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    try:
        result = runner(
            argv,
            check=False,
            capture_output=True,
            text=True,
            shell=False,
            env=env,
        )
    except OSError as exc:
        error_type = (
            InstallerVerificationError if verification else InstallerExecutionError
        )
        purpose = "verification" if verification else "installation"
        raise error_type(
            f"Native installer {purpose} command failed: {argv[0]}"
        ) from exc
    if result.returncode not in allowed_returncodes:
        error_type = (
            InstallerVerificationError if verification else InstallerExecutionError
        )
        purpose = "verification" if verification else "installation"
        output = _bounded_failure_output(result)
        output_suffix = f"\n{output}" if output else ""
        raise error_type(
            f"Native installer {purpose} command failed with exit code "
            f"{result.returncode}: {argv[0]}{output_suffix}"
        )
    return result


def validate_artifact(
    artifact_path: Path,
    artifact: Artifact,
    *,
    platform: str,
    formats: Collection[str],
) -> Path:
    if artifact.platform != platform or artifact.format not in formats:
        supported = ", ".join(sorted(formats))
        raise UnsupportedInstallerError(
            f"Expected {platform} installer format ({supported}); got "
            f"{artifact.platform}/{artifact.format}"
        )
    if artifact_path.name.casefold() != artifact.filename.casefold():
        raise UnsupportedInstallerError(
            "Installer path does not match artifact filename"
        )
    expected_suffix = f".{artifact.format}".casefold()
    if not artifact_path.name.casefold().endswith(expected_suffix):
        raise UnsupportedInstallerError(
            f"Artifact filename extension does not match format {artifact.format!r}"
        )
    try:
        resolved = artifact_path.resolve(strict=True)
    except OSError as exc:
        raise InstallerExecutionError("Installer artifact does not exist") from exc
    if not resolved.is_file():
        raise InstallerExecutionError("Installer artifact is not a regular file")
    return resolved
