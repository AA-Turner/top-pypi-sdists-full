"""The shared write path for files the user owns: `through_symlink` picks the
file, `write_text_atomic(keep_mode=True)` replaces it.

Every Probe writer of a user's agent files (CLAUDE.md / AGENTS.md, pi's and
Claude Code's settings.json, Codex's config.toml during repair) goes through
these two, so their edge cases are pinned here once, on every OS the matrix
runs, rather than copied into each caller's tests.
"""

from __future__ import annotations

import os
import stat
from pathlib import Path

import pytest

from probe.sdk.durable import through_symlink, write_text_atomic

_POSIX_ONLY = pytest.mark.skipif(os.name == "nt", reason="POSIX modes and symlinks")


def _real(path: Path) -> Path:
    return Path(os.path.realpath(path))


@_POSIX_ONLY
def test_a_link_resolves_to_its_target_and_a_plain_file_to_itself(tmp_path: Path) -> None:
    plain = tmp_path / "plain.json"
    plain.write_text("{}")
    assert through_symlink(plain) == plain

    repo = tmp_path / "dotfiles"
    repo.mkdir()
    (repo / "s.json").write_text("{}")
    relative = tmp_path / "relative.json"
    relative.symlink_to(Path("dotfiles") / "s.json")  # relative, as stow makes them
    assert through_symlink(relative) == _real(repo / "s.json")

    dangling = tmp_path / "dangling.json"
    dangling.symlink_to(repo / "missing.json")
    assert through_symlink(dangling) == _real(repo / "missing.json")


@_POSIX_ONLY
def test_a_link_loop_gives_back_a_path_and_never_raises(tmp_path: Path) -> None:
    loop = tmp_path / "loop.json"
    loop.symlink_to(loop)
    assert through_symlink(loop) == _real(loop)


@_POSIX_ONLY
@pytest.mark.skipif(not hasattr(os, "geteuid") or os.geteuid() == 0, reason="root writes anywhere")
def test_a_target_folder_that_takes_no_new_file_gives_back_the_link(tmp_path: Path) -> None:
    """The temp file goes beside the target; a read-only folder (the Nix store)
    cannot take it, so the caller replaces the link as Probe always did."""
    store = tmp_path / "store"
    store.mkdir()
    (store / "s.json").write_text("{}")
    store.chmod(0o555)
    link = tmp_path / "s.json"
    link.symlink_to(store / "s.json")
    try:
        assert through_symlink(link) == link
    finally:
        store.chmod(0o755)


@_POSIX_ONLY
@pytest.mark.parametrize("existing", [0o600, 0o664, 0o640])
def test_keep_mode_gives_the_new_file_the_old_ones_mode(tmp_path: Path, existing: int) -> None:
    """Not the umask's: a 0600 file is not left 0644, a 0664 one keeps its group."""
    path = tmp_path / "settings.json"
    path.write_text("old")
    path.chmod(existing)

    write_text_atomic(path, "new", mode=0o600, keep_mode=True)

    assert path.read_text() == "new"
    assert stat.S_IMODE(path.stat().st_mode) == existing


@_POSIX_ONLY
def test_keep_mode_on_a_new_file_uses_mode(tmp_path: Path) -> None:
    path = tmp_path / "settings.json"
    write_text_atomic(path, "new", mode=0o600, keep_mode=True)
    assert stat.S_IMODE(path.stat().st_mode) == 0o600


@_POSIX_ONLY
def test_the_temp_file_never_follows_a_link_planted_beside_the_target(tmp_path: Path) -> None:
    """The temp name is unique and created exclusively, so a link left in the
    folder under any fixed name is never written through."""
    unrelated = tmp_path / "unrelated.txt"
    unrelated.write_text("keep me")
    for name in ("settings.json.probe.tmp", ".settings.json.tmp", "settings.json.tmp"):
        (tmp_path / name).symlink_to(unrelated)

    write_text_atomic(tmp_path / "settings.json", "new", keep_mode=True)

    assert unrelated.read_text() == "keep me"
    assert (tmp_path / "settings.json").read_text() == "new"


@_POSIX_ONLY
@pytest.mark.parametrize(("existing", "expected"), [(0o4755, 0o755), (0o2775, 0o775), (0o444, 0o444)])
def test_keep_mode_drops_special_bits_and_keeps_the_rest_exactly(
    tmp_path: Path, existing: int, expected: int
) -> None:
    """Setuid/setgid/sticky are never copied onto a file Probe wrote; every
    other bit is, read-only included (the old callers copied it exactly)."""
    path = tmp_path / "CLAUDE.md"
    path.write_text("old")
    path.chmod(existing)

    write_text_atomic(path, "new", keep_mode=True)

    assert stat.S_IMODE(path.stat().st_mode) == expected


@_POSIX_ONLY
def test_a_filesystem_that_refuses_chmod_still_gets_the_write(tmp_path: Path, monkeypatch) -> None:
    """vfat, some FUSE and SMB mounts refuse chmod. Keeping the mode is best
    effort; refusing the write over it would wedge the integration repair."""
    from probe.sdk import durable

    def refuse(*_args, **_kwargs):
        raise PermissionError("operation not permitted")

    path = tmp_path / "settings.json"
    path.write_text("old")
    path.chmod(0o640)
    monkeypatch.setattr(durable.os, "fchmod", refuse)
    monkeypatch.setattr(durable.os, "chmod", refuse)

    write_text_atomic(path, "new", keep_mode=True)

    assert path.read_text() == "new"


@_POSIX_ONLY
def test_the_temp_is_never_readable_more_widely_than_the_old_file(tmp_path: Path, monkeypatch) -> None:
    """The temp holds the new bytes before the replace; created at the umask
    it would be world-readable for that moment even when the file is 0600."""
    from probe.sdk import durable

    opened: list[int] = []
    real_open = durable.os.open

    def record(path, flags, mode=0o777, *args, **kwargs):
        opened.append(mode)
        return real_open(path, flags, mode, *args, **kwargs)

    path = tmp_path / "settings.json"
    path.write_text("old")
    path.chmod(0o600)
    monkeypatch.setattr(durable.os, "open", record)

    write_text_atomic(path, "new", keep_mode=True)

    assert opened and opened[0] == 0o600


@_POSIX_ONLY
def test_keep_mode_refuses_a_link_loop_instead_of_replacing_it(tmp_path: Path) -> None:
    """A path that exists but cannot be stat'ed is not "no file yet": writing
    would silently replace the user's (broken) link."""
    loop = tmp_path / "settings.json"
    loop.symlink_to(loop)

    with pytest.raises(OSError):
        write_text_atomic(loop, "new", keep_mode=True)

    assert loop.is_symlink()


@_POSIX_ONLY
def test_replacing_a_link_itself_does_not_copy_its_targets_mode(tmp_path: Path) -> None:
    """When the link itself is replaced (its target's folder takes no new file),
    the target's mode belongs to the target: a 0444 Nix-store file must not
    turn the user's new settings file read-only."""
    target = tmp_path / "target.json"
    target.write_text("{}")
    target.chmod(0o444)
    link = tmp_path / "settings.json"
    link.symlink_to(target)

    write_text_atomic(link, "new", mode=0o600, keep_mode=True)

    assert not link.is_symlink()
    assert stat.S_IMODE(link.stat().st_mode) == 0o600
    assert target.read_text() == "{}"
