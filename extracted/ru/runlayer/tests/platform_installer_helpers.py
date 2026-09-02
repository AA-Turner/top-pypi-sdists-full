"""Shared fakes for native installer tests."""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path
import subprocess

from runlayer_cli.updater import Artifact


class RecordingRunner:
    def __init__(
        self, *responses: subprocess.CompletedProcess[str] | BaseException
    ) -> None:
        self.responses = list(responses)
        self.calls: list[tuple[list[str], dict[str, object]]] = []

    def __call__(self, argv: list[str], **kwargs: object):
        self.calls.append((argv, kwargs))
        response = self.responses.pop(0)
        if isinstance(response, BaseException):
            raise response
        return response


def result(
    *, returncode: int = 0, stdout: str = "", stderr: str = ""
) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess([], returncode, stdout=stdout, stderr=stderr)


def artifact(platform: str, format_: str, filename: str) -> Artifact:
    arch = {
        "macos": "arm64",
        "windows": "x64",
        "linux": "x86_64",
    }[platform]
    return Artifact(
        platform=platform,
        arch=arch,
        filename=filename,
        sha256=sha256(b"installer").hexdigest(),
        size_bytes=1,
        format=format_,
    )


def artifact_path(tmp_path: Path, value: Artifact) -> Path:
    path = tmp_path / value.filename
    path.write_bytes(b"installer")
    return path


def assert_argv_without_shell(runner: RecordingRunner) -> None:
    for argv, kwargs in runner.calls:
        assert isinstance(argv, list)
        assert kwargs["check"] is False
        assert kwargs["capture_output"] is True
        assert kwargs["text"] is True
        assert kwargs["shell"] is False
