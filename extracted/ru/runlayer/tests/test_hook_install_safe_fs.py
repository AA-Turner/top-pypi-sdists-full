"""Unit tests for ``runlayer_cli.hook_install.safe_fs`` (TOCTOU-safe fs ops).

These primitives back the ENG-3217 fix: root-run MDM writes into the console
user's home must never follow a symlink the (non-admin) user planted there.
"""

from __future__ import annotations

import errno
import os
from pathlib import Path

import pytest

from runlayer_cli.hook_install import safe_fs


class TestSafeWriteText:
    def test_creates_missing_parent_dirs(self, tmp_path: Path):
        home = tmp_path / "home"
        home.mkdir()
        target = home / ".claude" / "hooks" / "settings.json"

        safe_fs.safe_write_text(home, target, "hello")

        assert target.read_text() == "hello"

    def test_truncates_existing_regular_file(self, tmp_path: Path):
        home = tmp_path / "home"
        (home / ".claude").mkdir(parents=True)
        target = home / ".claude" / "settings.json"
        target.write_text("old-and-longer-content")

        safe_fs.safe_write_text(home, target, "new")

        assert target.read_text() == "new"

    def test_truncates_existing_regular_file_to_empty(self, tmp_path: Path):
        home = tmp_path / "home"
        home.mkdir()
        target = home / "settings.json"
        target.write_text("old content")

        safe_fs.safe_write_bytes(home, target, b"")

        assert target.read_bytes() == b""

    def test_replaces_symlink_without_following(self, tmp_path: Path):
        home = tmp_path / "home"
        (home / ".claude").mkdir(parents=True)
        outside = tmp_path / "outside.txt"
        outside.write_text("DO NOT CLOBBER")
        target = home / ".claude" / "settings.json"
        target.symlink_to(outside)

        safe_fs.safe_write_text(home, target, "safe")

        assert outside.read_text() == "DO NOT CLOBBER"
        assert not target.is_symlink()
        assert target.read_text() == "safe"

    def test_refuses_symlinked_parent(self, tmp_path: Path):
        home = tmp_path / "home"
        home.mkdir()
        outside_dir = tmp_path / "outside_dir"
        outside_dir.mkdir()
        (home / ".claude").symlink_to(outside_dir, target_is_directory=True)
        target = home / ".claude" / "settings.json"

        # Symlinked intermediate component: the link is replaced by a real dir
        # (self-heal) rather than followed, so nothing lands in outside_dir.
        safe_fs.safe_write_text(home, target, "safe")

        assert not (outside_dir / "settings.json").exists()
        assert target.read_text() == "safe"
        assert not (home / ".claude").is_symlink()

    def test_rejects_path_outside_home(self, tmp_path: Path):
        home = tmp_path / "home"
        home.mkdir()
        outside = tmp_path / "elsewhere.txt"

        with pytest.raises(ValueError):
            safe_fs.safe_write_text(home, outside, "x")

    def test_applies_mode(self, tmp_path: Path):
        home = tmp_path / "home"
        home.mkdir()
        target = home / ".claude" / "hook.sh"

        safe_fs.safe_write_text(home, target, "#!/bin/sh\n", mode=0o755)

        assert target.stat().st_mode & 0o777 == 0o755

    def test_raises_when_write_returns_zero(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        home = tmp_path / "home"
        home.mkdir()
        target = home / "settings.json"
        write_calls = 0

        def write(fd: int, data: bytes | memoryview) -> int:
            nonlocal write_calls
            write_calls += 1
            if write_calls == 1:
                return 0
            raise AssertionError("write retried after returning zero bytes")

        monkeypatch.setattr(safe_fs.os, "write", write)

        with pytest.raises(OSError, match="write returned zero bytes"):
            safe_fs.safe_write_bytes(home, target, b"new")

    @pytest.mark.skipif(os.name != "posix", reason="requires fchmod")
    def test_preserves_existing_data_when_fchmod_fails(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        home = tmp_path / "home"
        home.mkdir()
        target = home / "settings.json"
        target.write_text("existing config")

        def fail_fchmod(fd: int, mode: int) -> None:
            raise OSError("chmod failed")

        monkeypatch.setattr(safe_fs.os, "fchmod", fail_fchmod)

        with pytest.raises(OSError, match="chmod failed"):
            safe_fs.safe_write_text(home, target, "replacement", mode=0o600)

        assert target.read_text() == "existing config"


class TestMaybeSafeWriteBytes:
    @pytest.mark.skipif(os.name != "posix", reason="requires fchmod")
    def test_plain_write_preserves_existing_data_when_fchmod_fails(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        target = tmp_path / "settings.json"
        target.write_bytes(b"existing config")

        def fail_fchmod(fd: int, mode: int) -> None:
            raise OSError("chmod failed")

        monkeypatch.setattr(safe_fs.os, "fchmod", fail_fchmod)

        with pytest.raises(OSError, match="chmod failed"):
            safe_fs.maybe_safe_write_bytes(
                target, b"replacement", home=None, mode=0o600
            )

        assert target.read_bytes() == b"existing config"

    def test_plain_write_preserves_existing_data_when_windows_chmod_fails(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        target = tmp_path / "settings.json"
        target.write_bytes(b"existing config")
        monkeypatch.setattr(safe_fs.platform, "system", lambda: "Windows")

        def fail_chmod(path: Path, mode: int) -> None:
            raise OSError("chmod failed")

        monkeypatch.setattr(safe_fs.os, "chmod", fail_chmod)

        with pytest.raises(OSError, match="chmod failed"):
            safe_fs.maybe_safe_write_bytes(
                target, b"replacement", home=None, mode=0o600
            )

        assert target.read_bytes() == b"existing config"

    def test_plain_write_applies_mode_before_writing_data(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        target = tmp_path / "settings.json"
        modes_during_write: list[int] = []
        real_write = os.write

        def write(fd: int, data: bytes | memoryview) -> int:
            modes_during_write.append(os.fstat(fd).st_mode & 0o777)
            return real_write(fd, data)

        monkeypatch.setattr(safe_fs.os, "write", write)

        safe_fs.maybe_safe_write_bytes(
            target, b'secret = "token"\n', home=None, mode=0o600
        )

        assert modes_during_write
        assert set(modes_during_write) == {0o600}

    def test_plain_write_truncates_and_applies_requested_mode(
        self, tmp_path: Path
    ) -> None:
        target = tmp_path / "settings.json"
        target.write_bytes(b"old-and-longer")

        safe_fs.maybe_safe_write_bytes(target, b"new", home=None, mode=0o640)

        assert target.read_bytes() == b"new"
        assert target.stat().st_mode & 0o777 == 0o640


class TestWindowsReparseSafeWrite:
    """MDM-scope Windows writes must not follow symlinks (TOCTOU-safe).

    On Windows, ``console_home_anchor`` returns ``None``, forcing MDM writes
    through the ``home=None`` branch of ``maybe_safe_write_bytes``. Before the
    fix, ``os.open`` followed symlinks, and the preflight
    ``is_unsafe_windows_mdm_path`` was not atomic with the open — a TOCTOU race.
    Now ``_windows_open_no_reparse`` uses ``CreateFileW`` with
    ``FILE_FLAG_OPEN_REPARSE_POINT`` for an atomic open + reparse-point check.
    """

    def test_mdm_write_uses_reparse_safe_open(self, tmp_path, monkeypatch):
        """MDM-scope writes delegate to _windows_open_no_reparse, not os.open."""
        target = tmp_path / "settings.json"
        reparse_calls = []
        os_open_calls = []
        real_open = safe_fs.os.open

        def tracking_reparse(path, mode):
            reparse_calls.append(str(path))
            return real_open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, mode)

        def tracking_os_open(path, flags, *args, **kwargs):
            os_open_calls.append(str(path))
            return real_open(path, flags, *args, **kwargs)

        monkeypatch.setattr(safe_fs.platform, "system", lambda: "Windows")
        monkeypatch.setattr(safe_fs, "_windows_open_no_reparse", tracking_reparse)
        monkeypatch.setattr(safe_fs.os, "open", tracking_os_open)

        safe_fs.maybe_safe_write_bytes(
            target, b'{"hooks": {}}', home=None, mode=0o644, replace_symlink=False
        )

        assert len(reparse_calls) == 1
        assert reparse_calls[0] == str(target)
        assert not os_open_calls
        assert target.read_bytes() == b'{"hooks": {}}'

    def test_mdm_write_raises_eloop_on_reparse_point(self, tmp_path, monkeypatch):
        """When _windows_open_no_reparse raises ELOOP, the write is refused."""
        target = tmp_path / "settings.json"
        privileged = tmp_path / "privileged"
        privileged.write_bytes(b"must remain unchanged")

        def raise_eloop(path, mode):
            raise OSError(
                errno.ELOOP, "refusing to write through reparse point", str(path)
            )

        monkeypatch.setattr(safe_fs.platform, "system", lambda: "Windows")
        monkeypatch.setattr(safe_fs, "_windows_open_no_reparse", raise_eloop)

        with pytest.raises(OSError) as exc_info:
            safe_fs.maybe_safe_write_bytes(
                target,
                b'{"hooks": {}}',
                home=None,
                mode=0o644,
                replace_symlink=False,
            )

        assert exc_info.value.errno == errno.ELOOP
        assert not target.exists()
        assert privileged.read_bytes() == b"must remain unchanged"

    def test_mdm_write_preserves_existing_data_on_eloop(self, tmp_path, monkeypatch):
        """ELOOP raised before truncation — existing file data is preserved."""
        target = tmp_path / "settings.json"
        target.write_bytes(b'{"existing": true}')
        original = target.read_bytes()
        truncate_calls = []
        real_ftruncate = safe_fs.os.ftruncate

        def tracking_ftruncate(fd, length):
            truncate_calls.append(fd)
            return real_ftruncate(fd, length)

        def raise_eloop(path, mode):
            raise OSError(errno.ELOOP, "symlink", str(path))

        monkeypatch.setattr(safe_fs.platform, "system", lambda: "Windows")
        monkeypatch.setattr(safe_fs, "_windows_open_no_reparse", raise_eloop)
        monkeypatch.setattr(safe_fs.os, "ftruncate", tracking_ftruncate)

        with pytest.raises(OSError):
            safe_fs.maybe_safe_write_bytes(
                target,
                b'{"new": false}',
                home=None,
                mode=0o644,
                replace_symlink=False,
            )

        assert not truncate_calls
        assert target.read_bytes() == original

    def test_mdm_write_succeeds_when_no_reparse_point(self, tmp_path, monkeypatch):
        """A successful reparse-safe open writes data correctly."""
        target = tmp_path / "config.yaml"
        real_open = safe_fs.os.open

        def safe_open(path, mode):
            return real_open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, mode)

        monkeypatch.setattr(safe_fs.platform, "system", lambda: "Windows")
        monkeypatch.setattr(safe_fs, "_windows_open_no_reparse", safe_open)

        safe_fs.maybe_safe_write_bytes(
            target, b"hooks: {}", home=None, mode=0o644, replace_symlink=False
        )

        assert target.read_bytes() == b"hooks: {}"

    def test_windows_handle_is_switched_to_binary_mode(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """The CRT fd must not translate payload LF bytes to CRLF."""
        target = tmp_path / "settings.json"
        backing_fd = os.open(target, os.O_WRONLY | os.O_CREAT)
        setmode_calls: list[tuple[int, int]] = []

        class FakeMsvcrt:
            @staticmethod
            def open_osfhandle(handle: int, flags: int) -> int:
                assert handle == 123
                assert flags == 0
                return backing_fd

            @staticmethod
            def setmode(fd: int, flags: int) -> None:
                setmode_calls.append((fd, flags))

        class FakeCreateFile:
            restype = None
            argtypes = None

            def __call__(self, *_args) -> int:
                return 123

        class FakeKernel32:
            def __init__(self) -> None:
                self.CreateFileW = FakeCreateFile()

            @staticmethod
            def CloseHandle(_handle: int) -> None:
                raise AssertionError("valid handle was closed as invalid")

        monkeypatch.setattr(safe_fs, "msvcrt", FakeMsvcrt, raising=False)
        monkeypatch.setattr(
            safe_fs.ctypes,
            "WinDLL",
            lambda *_args, **_kwargs: FakeKernel32(),
            raising=False,
        )

        returned_fd: int | None = None
        try:
            returned_fd = safe_fs._windows_open_no_reparse(target, 0o644)

            assert returned_fd == backing_fd
            assert setmode_calls == [(backing_fd, safe_fs._O_BINARY)]
        finally:
            for fd in {backing_fd, returned_fd} - {None}:
                os.close(fd)

    def test_home_none_write_always_uses_reparse_safe_open(self, tmp_path, monkeypatch):
        """All home=None writes on Windows use _windows_open_no_reparse,
        regardless of replace_symlink, because every MDM caller on Windows
        receives home=None (console_home_anchor returns None on Windows) and
        may reach a user-controlled path (ENG-6087 / CWE-59/61)."""
        target = tmp_path / "settings.json"
        reparse_calls = []
        real_open = safe_fs.os.open

        def tracking_reparse(path, mode):
            reparse_calls.append(str(path))
            return real_open(path, os.O_WRONLY | os.O_CREAT, mode)

        monkeypatch.setattr(safe_fs.platform, "system", lambda: "Windows")
        monkeypatch.setattr(safe_fs, "_windows_open_no_reparse", tracking_reparse)
        monkeypatch.setattr(safe_fs.os, "chmod", lambda p, m: None)

        safe_fs.maybe_safe_write_bytes(
            target, b"data", home=None, mode=0o644, replace_symlink=True
        )

        assert len(reparse_calls) == 1
        assert reparse_calls[0] == str(target)
        assert target.read_bytes() == b"data"

    def test_mdm_write_propagates_non_eloop_errors(self, tmp_path, monkeypatch):
        """Non-ELOOP errors from _windows_open_no_reparse propagate."""
        target = tmp_path / "settings.json"

        def raise_eacces(path, mode):
            raise OSError(errno.EACCES, "permission denied", str(path))

        monkeypatch.setattr(safe_fs.platform, "system", lambda: "Windows")
        monkeypatch.setattr(safe_fs, "_windows_open_no_reparse", raise_eacces)

        with pytest.raises(OSError) as exc_info:
            safe_fs.maybe_safe_write_bytes(
                target, b"data", home=None, mode=0o644, replace_symlink=False
            )

        assert exc_info.value.errno == errno.EACCES

    def test_toctou_simulation_preflight_passes_write_caught(
        self, tmp_path, monkeypatch
    ):
        """Simulate the TOCTOU: preflight passes, but _windows_open_no_reparse
        catches a symlink planted in the race window."""
        target = tmp_path / "settings.json"
        privileged = tmp_path / "privileged.txt"
        privileged.write_text("root-only content")

        # Step 1: preflight passes because the path is not yet a symlink.
        assert not safe_fs.is_unsafe_windows_mdm_path(
            target, mdm=True, path_check=safe_fs.path_has_link_or_reparse_point
        )

        # Step 2: attacker creates a symlink in the race window.
        target.symlink_to(privileged)

        # Step 3: the reparse-safe open detects the symlink and refuses.
        def detect_reparse(path, mode):
            raise OSError(
                errno.ELOOP, "refusing to write through reparse point", str(path)
            )

        monkeypatch.setattr(safe_fs.platform, "system", lambda: "Windows")
        monkeypatch.setattr(safe_fs, "_windows_open_no_reparse", detect_reparse)

        with pytest.raises(OSError) as exc_info:
            safe_fs.maybe_safe_write_bytes(
                target,
                b'{"hooks": {}}',
                home=None,
                mode=0o644,
                replace_symlink=False,
            )

        assert exc_info.value.errno == errno.ELOOP
        assert privileged.read_text() == "root-only content"
        # The symlink itself was not replaced with data.
        assert target.is_symlink()


class TestSafeReadText:
    def test_reads_regular_file(self, tmp_path: Path):
        home = tmp_path / "home"
        (home / ".claude").mkdir(parents=True)
        target = home / ".claude" / "settings.json"
        target.write_text("data")

        assert safe_fs.safe_read_text(home, target) == "data"

    def test_missing_returns_none(self, tmp_path: Path):
        home = tmp_path / "home"
        home.mkdir()

        assert safe_fs.safe_read_text(home, home / ".claude" / "x.json") is None

    def test_symlink_returns_none_without_following(self, tmp_path: Path):
        home = tmp_path / "home"
        (home / ".claude").mkdir(parents=True)
        outside = tmp_path / "secret.txt"
        outside.write_text("root-only-secret")
        link = home / ".claude" / "settings.json"
        link.symlink_to(outside)

        # Must NOT leak the symlink target's contents back to the caller.
        assert safe_fs.safe_read_text(home, link) is None

    def test_path_outside_home_returns_none(self, tmp_path: Path):
        home = tmp_path / "home"
        home.mkdir()

        assert safe_fs.safe_read_text(home, tmp_path / "x.txt") is None


class TestWalkParentsFdLeak:
    """``_walk_parents`` must not leak fds when an iteration raises mid-walk."""

    def test_closes_opened_fds_when_component_raises(self, tmp_path, monkeypatch):
        home = tmp_path / "home"
        # 3 intermediate dirs, so _walk_parents opens fds for "a" and "b"
        # before failing on "c".
        (home / "a" / "b" / "c").mkdir(parents=True)
        home_fd = safe_fs._open_home_dir(home)

        opened: list[int] = []
        closed: list[int] = []
        real_open = safe_fs._open_dir_component
        real_close = os.close

        def tracking_open(
            parent_fd: int,
            name: str,
            *,
            create: bool,
            replace_symlink: bool = True,
        ) -> int:
            if name == "c":
                raise OSError("boom mid-walk")
            fd = real_open(
                parent_fd,
                name,
                create=create,
                replace_symlink=replace_symlink,
            )
            opened.append(fd)
            return fd

        def tracking_close(fd: int) -> None:
            closed.append(fd)
            real_close(fd)

        monkeypatch.setattr(safe_fs, "_open_dir_component", tracking_open)
        monkeypatch.setattr(os, "close", tracking_close)

        try:
            with pytest.raises(OSError):
                safe_fs._walk_parents(
                    home_fd, ("a", "b", "c", "settings.json"), create=False
                )
            assert opened, "expected fds to be opened before the raise"
            assert set(opened) <= set(closed), "fds opened mid-walk were leaked"
        finally:
            monkeypatch.undo()
            os.close(home_fd)


class TestSafeChownWithinHome:
    def _spy(self, monkeypatch) -> list[int]:
        inodes: list[int] = []
        real = os.fchown

        def spy(fd: int, uid: int, gid: int) -> None:
            try:
                inodes.append(os.fstat(fd).st_ino)
            except OSError:
                pass
            return real(fd, uid, gid)

        monkeypatch.setattr(os, "fchown", spy)
        return inodes

    def test_chowns_file_and_ancestors_not_home(self, tmp_path, monkeypatch):
        home = tmp_path / "home"
        claude = home / ".claude"
        claude.mkdir(parents=True)
        target = claude / "settings.json"
        target.write_text("{}")
        inodes = self._spy(monkeypatch)
        my_uid, my_gid = os.getuid(), os.getgid()

        safe_fs.safe_chown_within_home(home, target, my_uid, my_gid)

        assert target.stat().st_ino in inodes
        assert claude.stat().st_ino in inodes
        assert home.stat().st_ino not in inodes

    def test_refuses_symlinked_target(self, tmp_path, monkeypatch):
        home = tmp_path / "home"
        claude = home / ".claude"
        claude.mkdir(parents=True)
        outside = tmp_path / "secret"
        outside.write_text("x")
        outside_ino = outside.stat().st_ino
        link = claude / "settings.json"
        link.symlink_to(outside)
        inodes = self._spy(monkeypatch)

        with pytest.raises(OSError):
            safe_fs.safe_chown_within_home(home, link, os.getuid(), os.getgid())

        assert outside_ino not in inodes
