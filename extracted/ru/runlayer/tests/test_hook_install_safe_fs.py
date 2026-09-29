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


def _lstat_uid_override(monkeypatch, path: Path, uid: int) -> None:
    """Make ``os.lstat(path)`` report *uid* as owner (tests run unprivileged)."""
    real_lstat = os.lstat

    def fake(target, *args, **kwargs):
        st = real_lstat(target, *args, **kwargs)
        if isinstance(target, (str, os.PathLike)) and Path(target) == path:
            values = list(st)
            values[4] = uid
            return os.stat_result(values)
        return st

    monkeypatch.setattr(os, "lstat", fake)


def _other_uid(home: Path) -> int:
    return home.stat().st_uid + 1


def _record_fchown_inodes(monkeypatch) -> list[int]:
    records: list[int] = []
    real_fchown = os.fchown

    def spy(fd: int, uid: int, gid: int) -> None:
        records.append(os.fstat(fd).st_ino)
        real_fchown(fd, uid, gid)

    monkeypatch.setattr(os, "fchown", spy)
    return records


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
        """An ancestor link is neither followed nor replaced: the walk aborts
        and the user's link (however hostile) is left exactly as it was."""
        home = tmp_path / "home"
        home.mkdir()
        outside_dir = tmp_path / "outside_dir"
        outside_dir.mkdir()
        (home / ".claude").symlink_to(outside_dir, target_is_directory=True)
        target = home / ".claude" / "settings.json"

        with pytest.raises(OSError) as excinfo:
            safe_fs.safe_write_text(home, target, "safe")

        assert excinfo.value.errno == errno.ELOOP
        assert not (outside_dir / "settings.json").exists()
        assert (home / ".claude").is_symlink()

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


class TestResolveWithinHome:
    """Links whose resolved chain stays under home resolve; escapes return None."""

    def test_regular_file_resolves_to_itself(self, tmp_path: Path):
        home = tmp_path / "home"
        (home / ".claude").mkdir(parents=True)
        target = home / ".claude" / "settings.json"
        target.write_text("{}")

        assert safe_fs.resolve_within_home(home, target) == target

    def test_missing_regular_path_resolves_to_itself(self, tmp_path: Path):
        home = tmp_path / "home"
        home.mkdir()
        target = home / ".claude" / "settings.json"

        assert safe_fs.resolve_within_home(home, target) == target

    def test_absolute_file_link_in_home(self, tmp_path: Path):
        home = tmp_path / "home"
        (home / ".claude").mkdir(parents=True)
        (home / "dotfiles").mkdir()
        real = home / "dotfiles" / "settings.json"
        real.write_text("{}")
        link = home / ".claude" / "settings.json"
        link.symlink_to(real)

        assert safe_fs.resolve_within_home(home, link) == real

    def test_relative_file_link_in_home(self, tmp_path: Path):
        home = tmp_path / "home"
        (home / ".claude").mkdir(parents=True)
        (home / "dotfiles").mkdir()
        real = home / "dotfiles" / "settings.json"
        real.write_text("{}")
        link = home / ".claude" / "settings.json"
        link.symlink_to(Path("..") / "dotfiles" / "settings.json")

        assert safe_fs.resolve_within_home(home, link) == real

    def test_directory_link_ancestor_in_home(self, tmp_path: Path):
        home = tmp_path / "home"
        real_dir = home / "dotfiles" / "claude"
        real_dir.mkdir(parents=True)
        (home / ".claude").symlink_to(real_dir, target_is_directory=True)

        resolved = safe_fs.resolve_within_home(home, home / ".claude" / "settings.json")

        assert resolved == real_dir / "settings.json"

    def test_dangling_link_in_home_resolves_to_target(self, tmp_path: Path):
        home = tmp_path / "home"
        (home / ".claude").mkdir(parents=True)
        link = home / ".claude" / "settings.json"
        link.symlink_to(home / "dotfiles" / "settings.json")

        resolved = safe_fs.resolve_within_home(home, link)

        assert resolved == home / "dotfiles" / "settings.json"

    def test_escaping_link_returns_none(self, tmp_path: Path):
        home = tmp_path / "home"
        (home / ".claude").mkdir(parents=True)
        outside = tmp_path / "secret"
        outside.write_text("x")
        link = home / ".claude" / "settings.json"
        link.symlink_to(outside)

        assert safe_fs.resolve_within_home(home, link) is None

    def test_dotdot_link_escaping_home_returns_none(self, tmp_path: Path):
        home = tmp_path / "home"
        (home / ".claude").mkdir(parents=True)
        (tmp_path / "secret").write_text("x")
        link = home / ".claude" / "settings.json"
        link.symlink_to(Path("..") / ".." / "secret")

        assert safe_fs.resolve_within_home(home, link) is None

    def test_link_to_home_itself_returns_none(self, tmp_path: Path):
        home = tmp_path / "home"
        (home / ".claude").mkdir(parents=True)
        link = home / ".claude" / "settings.json"
        link.symlink_to(home)

        assert safe_fs.resolve_within_home(home, link) is None

    def test_symlink_loop_returns_none(self, tmp_path: Path):
        home = tmp_path / "home"
        (home / ".claude").mkdir(parents=True)
        a = home / ".claude" / "a"
        b = home / ".claude" / "b"
        a.symlink_to(b)
        b.symlink_to(a)

        assert safe_fs.resolve_within_home(home, a) is None

    def test_path_outside_home_returns_none(self, tmp_path: Path):
        home = tmp_path / "home"
        home.mkdir()

        assert safe_fs.resolve_within_home(home, tmp_path / "x.txt") is None

    def test_hop_through_outside_directory_returns_none(self, tmp_path: Path):
        """Every hop must stay in-home, even one that lands back inside: root
        must never walk a user-chosen path outside the home (automount hang,
        existence oracle on root-only directories)."""
        home = tmp_path / "home"
        real_dir = home / "dotfiles" / "claude"
        real_dir.mkdir(parents=True)
        (real_dir / "settings.json").write_text("{}")
        outside_hop = tmp_path / "hop"
        outside_hop.symlink_to(real_dir, target_is_directory=True)
        (home / ".claude").symlink_to(outside_hop, target_is_directory=True)

        assert (
            safe_fs.resolve_within_home(home, home / ".claude" / "settings.json")
            is None
        )

    def test_relative_dotdot_hop_inside_home_resolves(self, tmp_path: Path):
        home = tmp_path / "home"
        real_dir = home / "dotfiles" / "claude"
        real_dir.mkdir(parents=True)
        (home / "cfg").mkdir()
        (home / "cfg" / ".claude").symlink_to(
            Path("..") / "dotfiles" / "claude", target_is_directory=True
        )

        resolved = safe_fs.resolve_within_home(
            home, home / "cfg" / ".claude" / "settings.json"
        )

        assert resolved == real_dir / "settings.json"

    def test_resolution_never_calls_realpath_on_the_chain(
        self, tmp_path: Path, monkeypatch
    ):
        home = tmp_path / "home"
        real_dir = home / "dotfiles" / "claude"
        real_dir.mkdir(parents=True)
        (home / ".claude").symlink_to(real_dir, target_is_directory=True)

        def boom(*_args, **_kwargs):
            raise AssertionError("realpath walked a user-chosen chain")

        monkeypatch.setattr(safe_fs.os.path, "realpath", boom)

        resolved = safe_fs.resolve_within_home(home, home / ".claude" / "settings.json")

        assert resolved == real_dir / "settings.json"

    def test_long_hop_chain_returns_none(self, tmp_path: Path):
        home = tmp_path / "home"
        home.mkdir()
        real = home / "real.json"
        real.write_text("{}")
        previous = real
        for index in range(safe_fs._MAX_LINK_HOPS + 1):
            link = home / f"hop{index}.json"
            link.symlink_to(previous)
            previous = link

        assert safe_fs.resolve_within_home(home, previous) is None

    def test_hop_chain_within_bound_resolves(self, tmp_path: Path):
        home = tmp_path / "home"
        home.mkdir()
        real = home / "real.json"
        real.write_text("{}")
        previous = real
        for index in range(safe_fs._MAX_LINK_HOPS):
            link = home / f"hop{index}.json"
            link.symlink_to(previous)
            previous = link

        assert safe_fs.resolve_within_home(home, previous) == real

    def test_link_to_target_owned_by_another_uid_returns_none(
        self, tmp_path: Path, monkeypatch
    ):
        """In-home is not enough: the user must already own what root would write."""
        home = tmp_path / "home"
        (home / ".claude").mkdir(parents=True)
        (home / "dotfiles").mkdir()
        real = home / "dotfiles" / "settings.json"
        real.write_text("{}")
        link = home / ".claude" / "settings.json"
        link.symlink_to(real)
        _lstat_uid_override(monkeypatch, real, _other_uid(home))

        assert safe_fs.resolve_within_home(home, link) is None

    def test_link_through_directory_owned_by_another_uid_returns_none(
        self, tmp_path: Path, monkeypatch
    ):
        home = tmp_path / "home"
        real_dir = home / "managed" / "claude"
        real_dir.mkdir(parents=True)
        (real_dir / "settings.json").write_text("{}")
        (home / ".claude").symlink_to(real_dir, target_is_directory=True)
        _lstat_uid_override(monkeypatch, home / "managed", _other_uid(home))

        assert (
            safe_fs.resolve_within_home(home, home / ".claude" / "settings.json")
            is None
        )

    def test_plain_path_owned_by_another_uid_resolves_to_itself(
        self, tmp_path: Path, monkeypatch
    ):
        """No link followed means no new trust decision: the old walk applies."""
        home = tmp_path / "home"
        (home / ".claude").mkdir(parents=True)
        target = home / ".claude" / "settings.json"
        target.write_text("{}")
        _lstat_uid_override(monkeypatch, target, _other_uid(home))

        assert safe_fs.resolve_within_home(home, target) == target


class TestMaybeSafeInHomeLinks:
    """Opted-in dispatch follows in-home links; default and escaping links refuse."""

    def test_read_follows_in_home_link(self, tmp_path: Path):
        home = tmp_path / "home"
        (home / ".claude").mkdir(parents=True)
        (home / "dotfiles").mkdir()
        real = home / "dotfiles" / "settings.json"
        real.write_text("linked")
        link = home / ".claude" / "settings.json"
        link.symlink_to(real)

        assert (
            safe_fs.maybe_safe_read_text(link, home=home, follow_in_home_links=True)
            == "linked"
        )
        read = safe_fs.maybe_safe_read_file(link, home=home, follow_in_home_links=True)
        assert read is not None and read["data"] == b"linked"

    def test_read_ignores_in_home_link_without_opt_in(self, tmp_path: Path):
        home = tmp_path / "home"
        (home / ".claude").mkdir(parents=True)
        (home / "dotfiles").mkdir()
        real = home / "dotfiles" / "settings.json"
        real.write_text("linked")
        link = home / ".claude" / "settings.json"
        link.symlink_to(real)

        assert safe_fs.maybe_safe_read_text(link, home=home) is None
        assert safe_fs.maybe_safe_read_file(link, home=home) is None

    def test_read_does_not_follow_escaping_link(self, tmp_path: Path):
        home = tmp_path / "home"
        (home / ".claude").mkdir(parents=True)
        outside = tmp_path / "secret"
        outside.write_text("root-only-secret")
        link = home / ".claude" / "settings.json"
        link.symlink_to(outside)

        assert (
            safe_fs.maybe_safe_read_text(link, home=home, follow_in_home_links=True)
            is None
        )
        assert (
            safe_fs.maybe_safe_read_file(link, home=home, follow_in_home_links=True)
            is None
        )

    def test_write_follows_in_home_link(self, tmp_path: Path):
        home = tmp_path / "home"
        (home / ".claude").mkdir(parents=True)
        (home / "dotfiles").mkdir()
        real = home / "dotfiles" / "settings.json"
        real.write_text("old")
        link = home / ".claude" / "settings.json"
        link.symlink_to(real)

        safe_fs.maybe_safe_write_text(
            link, "new", home=home, replace_symlink=False, follow_in_home_links=True
        )

        assert link.is_symlink()
        assert real.read_text() == "new"

    def test_write_refuses_in_home_link_without_opt_in(self, tmp_path: Path):
        home = tmp_path / "home"
        (home / ".claude").mkdir(parents=True)
        (home / "dotfiles").mkdir()
        real = home / "dotfiles" / "settings.json"
        real.write_text("keep")
        link = home / ".claude" / "settings.json"
        link.symlink_to(real)

        with pytest.raises(OSError) as excinfo:
            safe_fs.maybe_safe_write_text(link, "new", home=home, replace_symlink=False)

        assert excinfo.value.errno == errno.ELOOP
        assert real.read_text() == "keep"

    def test_write_refuses_escaping_link(self, tmp_path: Path):
        home = tmp_path / "home"
        (home / ".claude").mkdir(parents=True)
        outside = tmp_path / "secret"
        outside.write_text("keep")
        link = home / ".claude" / "settings.json"
        link.symlink_to(outside)

        with pytest.raises(OSError) as excinfo:
            safe_fs.maybe_safe_write_text(
                link, "new", home=home, replace_symlink=False, follow_in_home_links=True
            )

        assert excinfo.value.errno == errno.ELOOP
        assert link.is_symlink()
        assert outside.read_text() == "keep"

    def test_unlink_removes_link_not_target(self, tmp_path: Path):
        home = tmp_path / "home"
        (home / ".claude").mkdir(parents=True)
        (home / "dotfiles").mkdir()
        real = home / "dotfiles" / "settings.json"
        real.write_text("keep")
        link = home / ".claude" / "settings.json"
        link.symlink_to(real)

        assert safe_fs.maybe_safe_unlink(link, home=home)

        assert not link.is_symlink()
        assert real.read_text() == "keep"

    def test_unlink_follows_in_home_directory_link(self, tmp_path: Path):
        """A file behind ``~/.claude -> ~/dotfiles/claude`` is reachable without
        any opt-in: ancestor links in-home are the user's layout, not a target."""
        home = tmp_path / "home"
        real_dir = home / "dotfiles" / "claude"
        real_dir.mkdir(parents=True)
        (home / ".claude").symlink_to(real_dir, target_is_directory=True)
        backup = real_dir / "settings.backup_20260901_120000_000000.json"
        backup.write_text("{}")

        assert safe_fs.maybe_safe_unlink(home / ".claude" / backup.name, home=home)
        assert not backup.exists()
        assert (home / ".claude").is_symlink()

    def test_unlink_refuses_escaping_directory_link(self, tmp_path: Path):
        home = tmp_path / "home"
        outside = tmp_path / "outside"
        outside.mkdir()
        home.mkdir()
        (home / ".claude").symlink_to(outside, target_is_directory=True)
        victim = outside / "settings.backup_20260901_120000_000000.json"
        victim.write_text("{}")

        assert not safe_fs.maybe_safe_unlink(home / ".claude" / victim.name, home=home)
        assert victim.exists()


class TestAncestorLinks:
    """In-home ancestor links are followed for every op; none is ever replaced."""

    def test_plain_write_follows_linked_parent(self, tmp_path: Path):
        """Runlayer-owned files under a linked user dir (Goose ``plugin.json``
        under ``~/.agents -> ~/dotfiles/agents``) land in the real dir."""
        home = tmp_path / "home"
        real_dir = home / "dotfiles" / "agents"
        real_dir.mkdir(parents=True)
        (home / ".agents").symlink_to(real_dir, target_is_directory=True)
        path = home / ".agents" / "plugins" / "runlayer-hooks" / "plugin.json"

        safe_fs.maybe_safe_write_text(path, "{}", home=home)

        assert (home / ".agents").is_symlink()
        assert (
            real_dir / "plugins" / "runlayer-hooks" / "plugin.json"
        ).read_text() == "{}"

    def test_plain_write_still_replaces_final_link(self, tmp_path: Path):
        home = tmp_path / "home"
        real_dir = home / "dotfiles" / "agents"
        real_dir.mkdir(parents=True)
        (home / ".agents").symlink_to(real_dir, target_is_directory=True)
        elsewhere = home / "elsewhere.json"
        elsewhere.write_text("keep")
        final_link = real_dir / "plugin.json"
        final_link.symlink_to(elsewhere)

        safe_fs.maybe_safe_write_text(home / ".agents" / "plugin.json", "{}", home=home)

        assert not final_link.is_symlink()
        assert final_link.read_text() == "{}"
        assert elsewhere.read_text() == "keep"

    def test_plain_write_refuses_final_link_when_asked(self, tmp_path: Path):
        home = tmp_path / "home"
        real_dir = home / "dotfiles" / "agents"
        real_dir.mkdir(parents=True)
        (home / ".agents").symlink_to(real_dir, target_is_directory=True)
        elsewhere = home / "elsewhere.json"
        elsewhere.write_text("keep")
        (real_dir / "plugin.json").symlink_to(elsewhere)

        with pytest.raises(OSError) as excinfo:
            safe_fs.maybe_safe_write_text(
                home / ".agents" / "plugin.json", "{}", home=home, replace_symlink=False
            )

        assert excinfo.value.errno == errno.ELOOP
        assert elsewhere.read_text() == "keep"

    def test_plain_read_follows_linked_parent(self, tmp_path: Path):
        home = tmp_path / "home"
        real_dir = home / "dotfiles" / "agents"
        real_dir.mkdir(parents=True)
        (real_dir / "plugin.json").write_text("manifest")
        (home / ".agents").symlink_to(real_dir, target_is_directory=True)

        assert (
            safe_fs.maybe_safe_read_text(home / ".agents" / "plugin.json", home=home)
            == "manifest"
        )

    def test_escaping_parent_link_is_refused_not_replaced(self, tmp_path: Path):
        home = tmp_path / "home"
        home.mkdir()
        outside = tmp_path / "outside"
        outside.mkdir()
        (home / ".agents").symlink_to(outside, target_is_directory=True)

        with pytest.raises(OSError) as excinfo:
            safe_fs.maybe_safe_write_text(
                home / ".agents" / "plugin.json", "{}", home=home
            )

        assert excinfo.value.errno == errno.ELOOP
        assert (home / ".agents").is_symlink()
        assert not (outside / "plugin.json").exists()

    def test_foreign_owned_parent_link_target_is_refused(
        self, tmp_path: Path, monkeypatch
    ):
        home = tmp_path / "home"
        real_dir = home / "managed" / "agents"
        real_dir.mkdir(parents=True)
        (home / ".agents").symlink_to(real_dir, target_is_directory=True)
        _lstat_uid_override(monkeypatch, home / "managed", _other_uid(home))

        with pytest.raises(OSError) as excinfo:
            safe_fs.maybe_safe_write_text(
                home / ".agents" / "plugin.json", "{}", home=home
            )

        assert excinfo.value.errno == errno.ELOOP
        assert not (real_dir / "plugin.json").exists()

    def test_created_components_under_linked_parent_are_handed_over(
        self, tmp_path: Path, monkeypatch
    ):
        home = tmp_path / "home"
        real_dir = home / "dotfiles" / "agents"
        real_dir.mkdir(parents=True)
        (home / ".agents").symlink_to(real_dir, target_is_directory=True)
        path = home / ".agents" / "plugins" / "plugin.json"
        _fstat_created_as_root(monkeypatch, home)
        records = _record_fchown_inodes(monkeypatch)

        safe_fs.maybe_safe_write_text(path, "{}", home=home)

        assert set(records) == {
            (real_dir / "plugins").stat().st_ino,
            (real_dir / "plugins" / "plugin.json").stat().st_ino,
        }

    def test_linked_parent_to_regular_file_is_refused(self, tmp_path: Path):
        """A parent link whose target is a *file* must not be mkdir'd over."""
        home = tmp_path / "home"
        (home / "dotfiles").mkdir(parents=True)
        notes = home / "dotfiles" / "notes.txt"
        notes.write_text("keep")
        (home / ".claude").symlink_to(notes)

        with pytest.raises(OSError) as excinfo:
            safe_fs.maybe_safe_write_text(
                home / ".claude" / "settings.json", "{}", home=home
            )

        assert excinfo.value.errno == errno.ELOOP
        assert (home / ".claude").is_symlink()
        assert notes.read_text() == "keep"
        assert list(home.rglob("settings.json")) == []

    def test_links_under_runlayer_tree_are_never_followed(self, tmp_path: Path):
        """``~/.runlayer`` is Runlayer's own tree: a link anywhere in it is
        refused, even one the ownership gate would otherwise pass."""
        home = tmp_path / "home"
        real_dir = home / "dotfiles" / "runlayer"
        (real_dir / "aiwatch").mkdir(parents=True)
        (real_dir / "aiwatch" / "cred").write_text("secret\n")
        (home / ".runlayer").symlink_to(real_dir, target_is_directory=True)
        path = home / ".runlayer" / "aiwatch" / "cred"

        with pytest.raises(OSError) as excinfo:
            safe_fs.maybe_safe_write_text(
                path, "new\n", home=home, replace_symlink=False
            )

        assert excinfo.value.errno == errno.ELOOP
        assert safe_fs.maybe_safe_read_text(path, home=home) is None
        assert not safe_fs.maybe_safe_unlink(path, home=home)
        assert (real_dir / "aiwatch" / "cred").read_text() == "secret\n"
        assert (home / ".runlayer").is_symlink()


def _fstat_created_as_root(monkeypatch, home: Path) -> None:
    """Make ``os.fstat`` report ``st_uid=0`` for anything not yet under *home*.

    Tests run unprivileged, so everything the walk creates is really owned by
    the test user; this fakes the root-run picture where every inode that did
    not exist when the helper was called was created by root. ``st_ino`` and
    ``st_mode`` survive so inode-based spies keep working.
    """
    existing = {home.lstat().st_ino} | {p.lstat().st_ino for p in home.rglob("*")}
    real_fstat = os.fstat

    def fake(fd: int):
        st = real_fstat(fd)
        if st.st_ino not in existing:
            values = list(st)
            values[4] = 0
            return os.stat_result(values)
        return st

    monkeypatch.setattr(os, "fstat", fake)


class TestSafeWriteOwner:
    """``owner=`` hands over what the walk created, while the fds are held."""

    def test_owner_hands_over_created_dirs_and_file_only(
        self, tmp_path: Path, monkeypatch
    ):
        home = tmp_path / "home"
        (home / "dotfiles").mkdir(parents=True)
        target = home / "dotfiles" / "vscode" / "settings.json"
        _fstat_created_as_root(monkeypatch, home)
        records = _record_fchown_inodes(monkeypatch)

        safe_fs.safe_write_bytes(home, target, b"{}", owner=(os.getuid(), os.getgid()))

        assert set(records) == {target.parent.stat().st_ino, target.stat().st_ino}

    def test_no_owner_never_chowns(self, tmp_path: Path, monkeypatch):
        home = tmp_path / "home"
        target = home / "dotfiles" / "vscode" / "settings.json"
        _fstat_created_as_root(monkeypatch, home.parent)
        records = _record_fchown_inodes(monkeypatch)

        safe_fs.safe_write_bytes(home, target, b"{}")

        assert records == []

    def test_followed_dangling_link_hands_over_created_chain(
        self, tmp_path: Path, monkeypatch
    ):
        home = tmp_path / "home"
        link = home / ".config" / "Code" / "User" / "settings.json"
        link.parent.mkdir(parents=True)
        target = home / "dotfiles" / "vscode" / "settings.json"
        link.symlink_to(target)
        _fstat_created_as_root(monkeypatch, home)
        records = _record_fchown_inodes(monkeypatch)

        safe_fs.maybe_safe_write_bytes(
            link, b"{}", home=home, follow_in_home_links=True
        )

        assert link.is_symlink()
        assert set(records) == {
            (home / "dotfiles").stat().st_ino,
            target.parent.stat().st_ino,
            target.stat().st_ino,
        }

    def test_plain_path_with_opt_in_does_not_chown(self, tmp_path: Path, monkeypatch):
        """No link followed means nothing to hand over here; the caller's plain
        ``reown_to_console_user`` reclaims Runlayer-created paths."""
        home = tmp_path / "home"
        home.mkdir()
        target = home / ".claude" / "settings.json"
        _fstat_created_as_root(monkeypatch, home)
        records = _record_fchown_inodes(monkeypatch)

        safe_fs.maybe_safe_write_bytes(
            target, b"{}", home=home, follow_in_home_links=True
        )

        assert records == []


class TestSafeChownAncestors:
    def test_chowns_chain(self, tmp_path: Path, monkeypatch):
        home = tmp_path / "home"
        target = home / "dotfiles" / "claude" / "settings.json"
        target.parent.mkdir(parents=True)
        target.write_text("{}")
        records = _record_fchown_inodes(monkeypatch)

        safe_fs.safe_chown_within_home(home, target, os.getuid(), os.getgid())

        assert set(records) == {
            (home / "dotfiles").stat().st_ino,
            (home / "dotfiles" / "claude").stat().st_ino,
            target.stat().st_ino,
        }


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

        def tracking_open(parent_fd: int, name: str, *, create: bool) -> int:
            if name == "c":
                raise OSError("boom mid-walk")
            fd = real_open(parent_fd, name, create=create)
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


@pytest.mark.skipif(
    os.name != "posix", reason="descriptor-relative helpers are POSIX-only"
)
def test_safe_read_file_max_bytes_bounds_the_read(tmp_path: Path) -> None:
    home = tmp_path / "home"
    target = home / ".runlayer" / "secret"
    target.parent.mkdir(parents=True)
    target.write_bytes(b"0123456789")

    bounded = safe_fs.safe_read_file(home, target, max_bytes=4)
    unbounded = safe_fs.safe_read_file(home, target)

    assert bounded is not None and bounded["data"] == b"01234"
    assert unbounded is not None and unbounded["data"] == b"0123456789"
