from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, patch

import pytest

from anteroom.services.version_check import (
    DEFAULT_UPDATE_CHECK_MESSAGE,
    VersionCheckStatus,
    check_for_update,
    format_update_message,
)


class _FakeProc:
    def __init__(self, *, stdout: bytes = b"", returncode: int | None = 0) -> None:
        self._stdout = stdout
        self.returncode = returncode
        self.killed = False
        self.waited = False

    async def communicate(self) -> tuple[bytes, bytes]:
        return self._stdout, b""

    def kill(self) -> None:
        self.killed = True

    async def wait(self) -> None:
        self.waited = True


@pytest.mark.asyncio
async def test_default_pip_output_returns_update_available() -> None:
    proc = _FakeProc(stdout=b"anteroom (2.0.0)\n", returncode=0)

    with patch("anteroom.services.version_check.asyncio.create_subprocess_exec", new=AsyncMock(return_value=proc)):
        result = await check_for_update("1.0.0")

    assert result.status is VersionCheckStatus.UPDATE_AVAILABLE
    assert result.latest == "2.0.0"


@pytest.mark.asyncio
async def test_custom_command_returns_current() -> None:
    proc = _FakeProc(stdout=b"1.0.0\n", returncode=0)

    with patch("anteroom.services.version_check.asyncio.create_subprocess_shell", new=AsyncMock(return_value=proc)):
        result = await check_for_update("1.0.0", command="internal-version")

    assert result.status is VersionCheckStatus.CURRENT
    assert result.latest == "1.0.0"


@pytest.mark.asyncio
async def test_custom_command_returns_not_newer_for_lower_version() -> None:
    proc = _FakeProc(stdout=b"0.9.0\n", returncode=0)

    with patch("anteroom.services.version_check.asyncio.create_subprocess_shell", new=AsyncMock(return_value=proc)):
        result = await check_for_update("1.0.0", command="internal-version")

    assert result.status is VersionCheckStatus.NOT_NEWER
    assert result.latest == "0.9.0"


@pytest.mark.asyncio
async def test_custom_command_nonzero_is_unavailable() -> None:
    proc = _FakeProc(stdout=b"", returncode=1)

    with patch("anteroom.services.version_check.asyncio.create_subprocess_shell", new=AsyncMock(return_value=proc)):
        result = await check_for_update("1.0.0", command="false")

    assert result.status is VersionCheckStatus.UNAVAILABLE
    assert result.reason == "checker exited non-zero"


@pytest.mark.asyncio
async def test_invalid_version_is_unavailable_not_current() -> None:
    proc = _FakeProc(stdout=b"not-a-version\n", returncode=0)

    with patch("anteroom.services.version_check.asyncio.create_subprocess_shell", new=AsyncMock(return_value=proc)):
        result = await check_for_update("1.0.0", command="bad-version")

    assert result.status is VersionCheckStatus.UNAVAILABLE
    assert result.latest == "not-a-version"


@pytest.mark.asyncio
async def test_unparseable_default_output_is_unavailable() -> None:
    proc = _FakeProc(stdout=b"unexpected output\n", returncode=0)

    with patch("anteroom.services.version_check.asyncio.create_subprocess_exec", new=AsyncMock(return_value=proc)):
        result = await check_for_update("1.0.0")

    assert result.status is VersionCheckStatus.UNAVAILABLE
    assert result.reason == "checker returned no version"


@pytest.mark.asyncio
async def test_timeout_kills_process_and_returns_unavailable() -> None:
    proc = _FakeProc(returncode=None)

    async def _slow() -> tuple[bytes, bytes]:
        await asyncio.sleep(1)
        return b"", b""

    proc.communicate = _slow  # type: ignore[method-assign]

    with patch("anteroom.services.version_check.asyncio.create_subprocess_shell", new=AsyncMock(return_value=proc)):
        result = await check_for_update("1.0.0", command="slow", timeout=0.01)

    assert result.status is VersionCheckStatus.UNAVAILABLE
    assert proc.killed is True
    assert proc.waited is True


def test_format_update_message_default_and_custom() -> None:
    assert format_update_message(DEFAULT_UPDATE_CHECK_MESSAGE, "1.0.0", "2.0.0") == (
        "Update available: 1.0.0 -> 2.0.0 -- pip install --upgrade anteroom"
    )
    assert format_update_message("Install {latest}; current {current}", "1.0.0", "2.0.0") == (
        "Install 2.0.0; current 1.0.0"
    )


def test_format_update_message_empty_suppresses_output() -> None:
    assert format_update_message("", "1.0.0", "2.0.0") == ""


def test_format_update_message_malformed_falls_back() -> None:
    assert format_update_message("Install {bogus}", "1.0.0", "2.0.0") == (
        "Update available: 1.0.0 -> 2.0.0 -- pip install --upgrade anteroom"
    )
