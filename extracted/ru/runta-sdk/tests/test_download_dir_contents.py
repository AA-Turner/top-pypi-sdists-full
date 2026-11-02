"""Directory merge behavior, archive safety, seekable fallback and cleanup."""

import asyncio
import io
import json
import base64
from contextlib import contextmanager, asynccontextmanager
import os
import subprocess
import tarfile
import threading
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import pytest

from runta import ApiError, AsyncFileManager, FileManager
from runta._internal import streaming_transfer as transfer
from runta._internal.async_file_io import _AsyncFileIO


@pytest.fixture(
    autouse=True,
    params=(
        ["native", "compat"]
        if callable(getattr(tarfile.TarFile, "makelink_with_filter", None))
        else ["compat"]
    ),
)
def link_fallback_capability(request, monkeypatch):
    """Exercise fallback selection on patched hosts as well as real old Python."""
    if request.param == "compat":
        monkeypatch.setattr(
            tarfile.TarFile, "makelink_with_filter", None, raising=False
        )
    return request.param


def make_archive(path, entries=()):
    """Entries are (name, data/type, linkname), rooted at the remote tar's '.'."""
    with tarfile.open(path, "w") as archive:
        root = tarfile.TarInfo(".")
        root.type = tarfile.DIRTYPE
        root.mode = 0o700
        archive.addfile(root)
        for name, value, link in entries:
            member = tarfile.TarInfo(name)
            member.mode = 0o755
            if value not in (
                tarfile.DIRTYPE,
                tarfile.SYMTYPE,
                tarfile.LNKTYPE,
                tarfile.FIFOTYPE,
                tarfile.CHRTYPE,
                tarfile.BLKTYPE,
            ):
                member.size = len(value)
                archive.addfile(member, io.BytesIO(value))
            else:
                member.type = value
                member.linkname = link
                archive.addfile(member)


def extract(tmp_path, entries, filter=None):
    path = tmp_path / "payload.tar"
    make_archive(path, entries)
    dst = tmp_path / "target"
    transfer._extract_dir_contents(path, dst, filter)
    return dst


@pytest.mark.parametrize("asynchronous", [False, True])
@pytest.mark.parametrize("empty", [False, True])
@pytest.mark.asyncio
async def test_transfer_merges_and_cleans(tmp_path, monkeypatch, asynchronous, empty):
    target = tmp_path / "target"
    target.mkdir(mode=0o755)
    before = target.stat().st_mode
    (target / "keep").write_text("keep")
    (target / "replace").write_text("old")
    paths = []

    def download(*args, **kwargs):
        assert kwargs["directory_contents"] is True
        path = args[4]
        paths.append(path)
        make_archive(
            path,
            []
            if empty
            else [
                ("./replace", b"new", ""),
                ("./nested/data", b"\x00\xff", ""),
            ],
        )
        assert list(path.parent.iterdir()) == [path]

    async def async_download(*args, **kwargs):
        await kwargs["_file_io"].run(lambda: download(*args, **kwargs))

    monkeypatch.setattr(transfer, "_sync_download_archive", download)
    monkeypatch.setattr(transfer, "_async_download_archive", async_download)
    fn = (
        transfer.async_download_dir_contents
        if asynchronous
        else transfer.download_dir_contents
    )
    result = fn("http://test", "token", "runtime", "/source", target, timeout=1)
    if asynchronous:
        await result
    assert (target / "keep").read_text() == "keep"
    assert (target / "replace").read_text() == ("old" if empty else "new")
    assert target.stat().st_mode == before
    if not empty:
        assert (target / "nested/data").read_bytes() == b"\x00\xff"
    assert not (target / "source").exists()
    assert all(not path.parent.exists() for path in paths)


@pytest.mark.parametrize("filter", [None, tarfile.data_filter])
def test_permissions_and_links(tmp_path, filter):
    target = extract(
        tmp_path,
        [
            ("./data", b"payload", ""),
            ("./nested", tarfile.DIRTYPE, ""),
            ("./nested/sym", tarfile.SYMTYPE, "../data"),
            ("./hard", tarfile.LNKTYPE, "./data"),
        ],
        filter,
    )
    assert (target / "nested/sym").is_symlink()
    assert (target / "nested/sym").read_bytes() == b"payload"
    assert os.path.samefile(target / "hard", target / "data")
    if os.name != "nt":
        assert (target / "data").stat().st_mode & 0o777 == 0o755


def test_link_fallback_uses_seekable_index_and_skips_dangling(tmp_path, monkeypatch):
    def unavailable(*args, **kwargs):
        raise OSError("links prohibited")

    monkeypatch.setattr(os, "symlink", unavailable)
    monkeypatch.setattr(os, "link", unavailable)
    target = extract(
        tmp_path,
        [
            ("./dangling", tarfile.SYMTYPE, "missing"),
            ("./forward", tarfile.SYMTYPE, "nested/data"),
            ("./nested/data", b"payload", ""),
            ("./hard", tarfile.LNKTYPE, "./nested/data"),
            ("./last", b"last", ""),
        ],
    )
    assert not os.path.lexists(target / "dangling")
    assert (target / "forward").read_bytes() == b"payload"
    assert (target / "hard").read_bytes() == b"payload"
    assert not (target / "forward").is_symlink()
    assert (target / "last").read_bytes() == b"last"


@pytest.mark.parametrize(
    "entry",
    [
        ("../escape", b"bad", ""),
        ("/absolute", b"bad", ""),
        ("other/file", b"bad", ""),
        ("./../escape", b"bad", ""),
        ("./C:stream", b"bad", ""),
        ("./dir\\escape", b"bad", ""),
        ("./link", tarfile.SYMTYPE, "../../escape"),
        ("./link", tarfile.SYMTYPE, "/absolute"),
        ("./link", tarfile.LNKTYPE, "other/file"),
        ("./link", tarfile.LNKTYPE, "./../escape"),
    ],
)
def test_rejects_malicious_members(tmp_path, entry):
    with pytest.raises(tarfile.FilterError):
        extract(tmp_path, [entry])
    assert not (tmp_path / "escape").exists()


@pytest.mark.parametrize("link", [False, True])
def test_rejects_existing_escape_link(tmp_path, link):
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "data").write_text("original")
    target = tmp_path / "target"
    target.mkdir()
    (target / "escape").symlink_to(outside, target_is_directory=True)
    entry = (
        ("./alias", tarfile.SYMTYPE, "escape/data")
        if link
        else ("./escape/data", b"bad", "")
    )
    with pytest.raises(tarfile.FilterError):
        extract(tmp_path, [entry])
    assert (outside / "data").read_text() == "original"


@pytest.mark.parametrize(
    "field,value",
    [
        ("name", "../escape"),
        ("name", "/escape"),
        ("name", "C:escape"),
        ("linkname", "../../escape"),
    ],
)
def test_callback_cannot_bypass_safety(tmp_path, field, value):
    def callback(member, destination):
        setattr(member, field, value)
        return member

    with pytest.raises(tarfile.FilterError):
        extract(tmp_path, [("./link", tarfile.SYMTYPE, "data")], callback)


@pytest.mark.parametrize("kind", [tarfile.FIFOTYPE, tarfile.CHRTYPE, tarfile.BLKTYPE])
def test_special_files_can_be_skipped(tmp_path, kind):
    entries = [("./special", kind, ""), ("./data", b"ok", "")]
    with pytest.raises(tarfile.SpecialFileError):
        extract(tmp_path, entries)
    seen = []

    def callback(member, destination):
        seen.append(member.name)
        return None if member.isdev() else tarfile.data_filter(member, destination)

    target = extract(tmp_path, entries, callback)
    assert seen == ["special", "data"]
    assert not (target / "special").exists()
    assert (target / "data").read_bytes() == b"ok"


@pytest.mark.parametrize("directory", [False, True])
def test_type_conflicts_preserve_destination(tmp_path, directory):
    target = tmp_path / "target"
    target.mkdir()
    existing = target / "conflict"
    if directory:
        existing.mkdir()
        (existing / "keep").write_text("keep")
    else:
        existing.write_text("keep")
    with pytest.raises(FileExistsError):
        extract(
            tmp_path, [("./conflict", b"bad" if directory else tarfile.DIRTYPE, "")]
        )
    assert (existing / "keep" if directory else existing).read_text() == "keep"


@pytest.mark.parametrize("stage", ["network", "extract"])
@pytest.mark.parametrize("asynchronous", [False, True])
@pytest.mark.asyncio
async def test_failures_cleanup(tmp_path, monkeypatch, stage, asynchronous):
    paths = []

    def download(*args, **kwargs):
        paths.append(args[4])
        make_archive(args[4], [("./data", b"ok", "")])
        if stage == "network":
            raise ConnectionError("failed")

    def fail(*args):
        raise OSError("failed")

    async def async_download(*args, **kwargs):
        await kwargs["_file_io"].run(lambda: download(*args, **kwargs))

    monkeypatch.setattr(transfer, "_sync_download_archive", download)
    monkeypatch.setattr(transfer, "_async_download_archive", async_download)
    monkeypatch.setattr(transfer, "_extract_dir_contents", fail)
    fn = (
        transfer.async_download_dir_contents
        if asynchronous
        else transfer.download_dir_contents
    )
    with pytest.raises(OSError, match="failed"):
        result = fn(
            "http://test",
            "token",
            "runtime",
            "/src",
            tmp_path / "target",
            timeout=1,
            attempts=1,
        )
        if asynchronous:
            await result
    assert paths and all(not p.parent.exists() for p in paths)


@pytest.mark.asyncio
@pytest.mark.parametrize("selection", [None, ["data"]])
@pytest.mark.parametrize("stage", ["download", "extract", "cleanup"])
async def test_repeated_cancel_drains_before_cleanup(
    tmp_path, monkeypatch, stage, selection
):
    entered = threading.Event()
    release = threading.Event()
    paths = []
    threads = []
    real_extract = transfer._extract_dir_contents
    real_cleanup = transfer.tempfile.TemporaryDirectory.cleanup

    def block():
        threads.append(threading.current_thread().name)
        entered.set()
        assert release.wait(5)
        assert paths[0].exists()

    async def download(*args, **kwargs):
        paths.append(args[4])
        await kwargs["_file_io"].run(make_archive, args[4], [("./data", b"ok", "")])
        if stage == "download":
            await kwargs["_file_io"].run(block)

    def unpack(*args):
        if stage == "extract":
            block()
        real_extract(*args)

    def cleanup(workspace):
        if stage == "cleanup":
            block()
        real_cleanup(workspace)

    monkeypatch.setattr(transfer, "_async_download_archive", download)
    monkeypatch.setattr(transfer, "_extract_dir_contents", unpack)
    monkeypatch.setattr(transfer.tempfile.TemporaryDirectory, "cleanup", cleanup)
    pool = _AsyncFileIO(1, asyncio.get_running_loop)
    task = asyncio.create_task(
        transfer.async_download_dir_contents(
            "http://test",
            "token",
            "runtime",
            "/source",
            tmp_path / "target",
            timeout=1,
            paths=selection,
            _file_io=pool,
        )
    )
    try:

        async def wait_entered():
            while not entered.is_set():
                await asyncio.sleep(0)

        await asyncio.wait_for(wait_entered(), 5)
        task.cancel()
        await asyncio.sleep(0)
        task.cancel()
        await asyncio.sleep(0)
        assert not task.done()
        assert paths[0].exists()
    finally:
        release.set()
        with pytest.raises(asyncio.CancelledError):
            await task
        pool.close()
    assert not paths[0].parent.exists()
    assert all(name.startswith("runta-file-io") for name in threads)


@pytest.mark.parametrize("asynchronous", [False, True])
@pytest.mark.asyncio
@pytest.mark.parametrize("selection", [None, ["agent.log"]])
async def test_public_facade(asynchronous, tmp_path, selection):
    download = AsyncMock() if asynchronous else Mock()
    runtime = SimpleNamespace(
        id="runtime",
        _client=SimpleNamespace(_http=SimpleNamespace(download_dir_contents=download)),
    )
    manager = object.__new__(AsyncFileManager if asynchronous else FileManager)
    manager._init(runtime)

    def callback(member, destination):
        return member

    result = manager.download_dir_contents(
        "/src", str(tmp_path), paths=selection, filter=callback
    )
    if asynchronous:
        await result
    download.assert_called_once_with(
        "runtime", "/src", tmp_path, paths=selection, filter=callback
    )


@pytest.mark.skipif(
    os.name == "nt", reason="runtime shell command is POSIX; host shell fixture"
)
@pytest.mark.parametrize("symlink", [False, True])
def test_remote_command_resolves_top_directory_and_quotes(tmp_path, symlink):
    source = tmp_path / "source ' $(touch injected)\n"
    source.mkdir()
    (source / "data").write_text("payload")
    (source / "internal").symlink_to("data")
    entry = tmp_path / "link"
    entry.symlink_to(source, target_is_directory=True)
    archive = tmp_path / "payload.tar"
    command, args = transfer._download_archive_command(
        str(entry if symlink else source), True
    )
    with archive.open("wb") as out:
        subprocess.run([command, *args], stdout=out, check=True, cwd=tmp_path)
    target = tmp_path / "target"
    transfer._extract_dir_contents(archive, target)
    assert (target / "internal").is_symlink()
    assert (target / "data").read_text() == "payload"
    assert not (tmp_path / "injected").exists()


def test_missing_security_support_fails_closed(tmp_path, monkeypatch):
    monkeypatch.delattr(tarfile, "data_filter")
    with pytest.raises(RuntimeError, match="tarfile.data_filter"):
        extract(tmp_path, [("./data", b"payload", "")])
    assert not (tmp_path / "target").exists()


def test_missing_source_directory_rejected(tmp_path):
    archive = tmp_path / "payload.tar"
    with tarfile.open(archive, "w") as tar:
        tar.addfile(tarfile.TarInfo("file"))
    with pytest.raises(ApiError, match="source directory"):
        transfer._extract_dir_contents(archive, tmp_path / "target")


def test_large_archive_does_not_create_staging_or_second_archive(tmp_path, monkeypatch):
    archive = tmp_path / "payload.tar"
    make_archive(archive, [(f"./nested/file-{i}", b"x" * 8192, "") for i in range(512)])
    real_extractall = tarfile.TarFile.extractall

    def check(archive_file, target, **kwargs):
        assert {p.name for p in tmp_path.iterdir()} == {"payload.tar", "target"}
        assert archive_file.fileobj.seekable()
        return real_extractall(archive_file, target, **kwargs)

    monkeypatch.setattr(tarfile.TarFile, "extractall", check)
    transfer._extract_dir_contents(archive, tmp_path / "target")
    assert len(list((tmp_path / "target/nested").iterdir())) == 512
    assert {p.name for p in tmp_path.iterdir()} == {"payload.tar", "target"}


@pytest.mark.parametrize("asynchronous", [False, True])
@pytest.mark.asyncio
async def test_network_retry_finishes_before_merge(tmp_path, monkeypatch, asynchronous):
    calls = []
    real_extract = transfer._extract_dir_contents

    def download(*args, **kwargs):
        calls.append(args[4])
        if len(calls) == 1:
            args[4].write_bytes(b"incomplete archive")
            raise transfer._TransferInterrupted("retry")
        make_archive(args[4], [("./data", b"complete", "")])

    async def async_download(*args, **kwargs):
        await kwargs["_file_io"].run(lambda: download(*args, **kwargs))

    def check_extract(*args):
        assert len(calls) == 2
        assert not args[1].exists()
        real_extract(*args)

    monkeypatch.setattr(transfer, "_sync_download_archive", download)
    monkeypatch.setattr(transfer, "_async_download_archive", async_download)
    monkeypatch.setattr(transfer, "_extract_dir_contents", check_extract)
    monkeypatch.setattr(
        "runta._internal.retry._full_jitter_delay", lambda *args, **kwargs: 0
    )
    fn = (
        transfer.async_download_dir_contents
        if asynchronous
        else transfer.download_dir_contents
    )
    result = fn(
        "http://test",
        "token",
        "runtime",
        "/src",
        tmp_path / "target",
        timeout=1,
        attempts=2,
    )
    if asynchronous:
        await result
    assert (tmp_path / "target/data").read_bytes() == b"complete"
    assert calls[0] == calls[1]
    assert not calls[0].exists()


def test_filtered_link_fallback_cannot_copy_excluded_referent(tmp_path, monkeypatch):
    def unavailable(*args, **kwargs):
        raise OSError("links prohibited")

    def callback(member, destination):
        return None if member.name == "secret" else member

    monkeypatch.setattr(os, "symlink", unavailable)
    target = extract(
        tmp_path,
        [
            ("./alias", tarfile.SYMTYPE, "secret"),
            ("./secret", b"secret", ""),
            ("./last", b"ok", ""),
        ],
        callback,
    )
    assert not (target / "alias").exists()
    assert not (target / "secret").exists()
    assert (target / "last").read_bytes() == b"ok"


@pytest.mark.parametrize(
    "alias", ["symlink", "hardlink", "dangling", "external_hardlink"]
)
@pytest.mark.parametrize(
    "member_kind", ["file", "hardlink_fallback", "symlink_fallback"]
)
def test_overwrite_replaces_existing_alias_without_changing_referent(
    tmp_path, monkeypatch, alias, member_kind
):
    target = tmp_path / "target"
    target.mkdir()
    keep = tmp_path / "outside" if alias == "external_hardlink" else target / "keep"
    keep.write_bytes(b"original")
    replace = target / "replace"
    if alias in {"hardlink", "external_hardlink"}:
        os.link(keep, replace)
    else:
        replace.symlink_to("missing" if alias == "dangling" else "keep")

    entries = [("./data", b"new", "")]
    if member_kind == "file":
        entries.append(("./replace", b"new", ""))
    else:

        def unavailable(*args, **kwargs):
            raise OSError("links prohibited")

        monkeypatch.setattr(os, "link", unavailable)
        monkeypatch.setattr(os, "symlink", unavailable)
        if member_kind == "hardlink_fallback":
            entries.append(("./replace", tarfile.LNKTYPE, "./data"))
        else:
            entries.append(("./replace", tarfile.SYMTYPE, "data"))

    extract(tmp_path, entries)
    assert replace.read_bytes() == b"new"
    assert not replace.is_symlink()
    assert keep.read_bytes() == b"original"
    assert not os.path.samefile(keep, replace)
    assert not (target / "missing").exists()
    assert (target / "data").read_bytes() == b"new"


def test_skipped_member_preserves_existing_alias(tmp_path):
    target = tmp_path / "target"
    target.mkdir()
    (target / "keep").write_bytes(b"original")
    (target / "replace").symlink_to("keep")

    def skip(member, destination):
        return None

    extract(tmp_path, [("./replace", b"new", "")], skip)
    assert (target / "replace").is_symlink()
    assert (target / "keep").read_bytes() == b"original"


@pytest.mark.parametrize("rename_referent", [False, True])
def test_link_fallback_filters_referent_at_actual_destination(
    tmp_path, monkeypatch, rename_referent
):
    outside = tmp_path / "safe"
    outside.write_text("outside")
    real_symlink = os.symlink

    def fail_alias(link, destination, *args, **kwargs):
        if os.path.normpath(link) == os.path.normpath("deep/ref"):
            raise OSError("force alias to copy its referent")
        return real_symlink(link, destination, *args, **kwargs)

    def callback(member, destination):
        if rename_referent and member.name == "deep/ref":
            return member.replace(name="deep/renamed")
        return member

    monkeypatch.setattr(os, "symlink", fail_alias)
    with pytest.raises(tarfile.FilterError):
        extract(
            tmp_path,
            [
                ("./safe", b"inside", ""),
                ("./deep/ref", tarfile.SYMTYPE, "../safe"),
                ("./alias", tarfile.SYMTYPE, "deep/ref"),
            ],
            callback,
        )
    assert outside.read_text() == "outside"
    assert not os.path.lexists(tmp_path / "target/alias")


def test_later_link_cannot_turn_an_accepted_link_into_an_escape(tmp_path):
    target = extract(
        tmp_path,
        [
            ("./alias", tarfile.SYMTYPE, "directory/../outside"),
            ("./directory", tarfile.SYMTYPE, "."),
        ],
    )
    assert (target / "alias").is_symlink()
    assert (target / "alias").resolve() == target / "outside"


def test_callback_cannot_enable_special_files_with_missing_mode(tmp_path):
    def callback(member, destination):
        member.mode = None
        return member

    with pytest.raises(tarfile.SpecialFileError):
        extract(tmp_path, [("./fifo", tarfile.FIFOTYPE, "")], callback)
    assert not (tmp_path / "target/fifo").exists()


def test_compat_rejects_cyclic_link_copy(tmp_path, monkeypatch):
    monkeypatch.setattr(tarfile.TarFile, "makelink_with_filter", None, raising=False)

    def unavailable(*args, **kwargs):
        raise OSError("links prohibited")

    monkeypatch.setattr(os, "symlink", unavailable)
    with pytest.raises(tarfile.FilterError, match="cyclic"):
        extract(
            tmp_path,
            [
                ("./a", tarfile.SYMTYPE, "b"),
                ("./b", tarfile.SYMTYPE, "a"),
            ],
        )
    assert not (tmp_path / "target/a").exists()
    assert not (tmp_path / "target/b").exists()


@pytest.mark.parametrize("alias", ["file", "symlink", "hardlink", "dangling"])
def test_unsupported_dangling_link_preserves_existing_destination(
    tmp_path, monkeypatch, alias
):
    target = tmp_path / "target"
    target.mkdir()
    keep = target / "keep"
    keep.write_bytes(b"keep")
    report = target / "report"
    if alias == "file":
        report.write_bytes(b"original")
    elif alias == "hardlink":
        os.link(keep, report)
    else:
        report.symlink_to("old-missing" if alias == "dangling" else "keep")
    original_stat = report.lstat()

    def unavailable(*args, **kwargs):
        raise OSError("links prohibited")

    monkeypatch.setattr(os, "symlink", unavailable)
    extract(
        tmp_path,
        [
            ("./report", tarfile.SYMTYPE, "new-missing"),
            ("./last", b"last", ""),
        ],
    )
    assert os.path.lexists(report)
    assert report.lstat().st_mode == original_stat.st_mode
    assert keep.read_bytes() == b"keep"
    if alias == "file":
        assert report.read_bytes() == b"original"
    elif alias == "hardlink":
        assert os.path.samefile(keep, report)
    else:
        assert os.readlink(report) == ("old-missing" if alias == "dangling" else "keep")
    assert (target / "last").read_bytes() == b"last"
    assert not list(target.glob(".runta-link-*"))


def test_filtered_fallback_preserves_existing_destination_metadata(
    tmp_path, monkeypatch
):
    target = tmp_path / "target"
    target.mkdir()
    report = target / "report"
    report.write_bytes(b"original")
    report.chmod(0o600)
    before = report.stat()

    def unavailable(*args, **kwargs):
        raise OSError("links prohibited")

    def skip_referent(member, destination):
        return None if member.name == "data" else member

    monkeypatch.setattr(os, "link", unavailable)
    extract(
        tmp_path,
        [
            ("./data", b"new", ""),
            ("./report", tarfile.LNKTYPE, "./data"),
            ("./last", b"last", ""),
        ],
        skip_referent,
    )
    assert report.read_bytes() == b"original"
    assert report.stat().st_mode == before.st_mode
    assert report.stat().st_mtime_ns == before.st_mtime_ns
    assert (target / "last").read_bytes() == b"last"
    assert not list(target.glob(".runta-link-*"))


@pytest.mark.parametrize("fault", ["filter", "copy"])
def test_link_fallback_failure_restores_existing_destination(
    tmp_path, monkeypatch, fault
):
    target = tmp_path / "target"
    target.mkdir()
    report = target / "report"
    report.write_bytes(b"original")

    def unavailable(*args, **kwargs):
        raise OSError("links prohibited")

    def callback(member, destination):
        if fault == "filter" and member.name == "data":
            raise ValueError("injected failure")
        return member

    def failed_copy(*args, **kwargs):
        raise OSError("injected failure")

    monkeypatch.setattr(os, "symlink", unavailable)
    if fault == "copy":
        monkeypatch.setattr(transfer._DirectoryMergeTarFile, "makefile", failed_copy)
    with pytest.raises(
        ValueError if fault == "filter" else OSError, match="injected failure"
    ):
        extract(
            tmp_path,
            [
                ("./report", tarfile.SYMTYPE, "data"),
                ("./data", b"new", ""),
            ],
            callback,
        )
    assert report.read_bytes() == b"original"
    assert not list(target.glob(".runta-link-*"))


@pytest.mark.asyncio
async def test_cancel_drains_link_replacement_before_restoring_and_cleaning(
    tmp_path, monkeypatch
):
    target = tmp_path / "target"
    target.mkdir()
    report = target / "report"
    report.write_bytes(b"original")
    entered = threading.Event()
    release = threading.Event()
    archives = []

    async def download(*args, **kwargs):
        archives.append(args[4])
        await kwargs["_file_io"].run(
            make_archive,
            args[4],
            [
                ("./report", tarfile.SYMTYPE, "missing"),
                ("./data", b"payload", ""),
            ],
        )

    def unavailable(*args, **kwargs):
        entered.set()
        assert release.wait(5)
        raise OSError("links prohibited")

    monkeypatch.setattr(transfer, "_async_download_archive", download)
    monkeypatch.setattr(os, "symlink", unavailable)
    task = asyncio.create_task(
        transfer.async_download_dir_contents(
            "http://test",
            "token",
            "runtime",
            "/src",
            target,
            timeout=1,
        )
    )
    try:

        async def wait_entered():
            while not entered.is_set():
                await asyncio.sleep(0)

        await asyncio.wait_for(wait_entered(), 5)
        task.cancel()
        await asyncio.sleep(0)
        task.cancel()
        await asyncio.sleep(0)
        assert not task.done()
        assert archives[0].exists()
        assert list(target.glob(".runta-link-*"))
    finally:
        release.set()
        with pytest.raises(asyncio.CancelledError):
            await task
    assert report.read_bytes() == b"original"
    assert (target / "data").read_bytes() == b"payload"
    assert not list(target.glob(".runta-link-*"))
    assert not archives[0].parent.exists()


@pytest.mark.parametrize("asynchronous", [False, True])
@pytest.mark.parametrize(
    "selection",
    [
        [],
        ["/abs"],
        ["a/../b"],
        ["a\x00b"],
        ["a\\b"],
        ["C:foo"],
        ["."],
        [""],
        "file",
        [1],
    ],
)
@pytest.mark.asyncio
async def test_selection_validates_before_any_resources(
    tmp_path, monkeypatch, asynchronous, selection
):
    def forbidden(*args, **kwargs):
        pytest.fail("selection must return/fail before acquiring resources")

    monkeypatch.setattr(transfer.tempfile, "TemporaryDirectory", forbidden)
    monkeypatch.setattr(transfer, "_AsyncFileIO", forbidden)
    callback = Mock(side_effect=forbidden)
    fn = (
        transfer.async_download_dir_contents
        if asynchronous
        else transfer.download_dir_contents
    )

    async def call():
        result = fn(
            "http://test",
            "token",
            "runtime",
            "/src",
            tmp_path / "target",
            paths=selection,
            filter=callback,
            timeout=1,
        )
        if asynchronous:
            await result

    if selection == []:
        await call()
    else:
        with pytest.raises((TypeError, ValueError)):
            await call()
    callback.assert_not_called()
    assert not (tmp_path / "target").exists()


@pytest.mark.skipif(os.name == "nt", reason="remote POSIX shell fixture")
@pytest.mark.parametrize("source_link", [False, True])
def test_selection_remote_archive_contains_only_selected_entries(tmp_path, source_link):
    source = tmp_path / "source ' $(touch injected)\n"
    source.mkdir()
    names = [
        "space name",
        "line\nname\n",
        "中文",
        "-flag",
        "$(touch injected)",
        "quote'\"`*?",
        "nested/data",
    ]
    for name in names:
        path = source / name
        path.parent.mkdir(exist_ok=True)
        path.write_text(name)
    (source / "nested/excluded").write_text("SECRET-EXCLUDED-CONTENT")
    (source / "excluded").write_text("SECRET-EXCLUDED-CONTENT")
    (source / "sym").symlink_to("excluded")
    (source / "dangling").symlink_to("missing")
    os.link(source / names[0], source / "hard")
    alias = tmp_path / "source-link"
    alias.symlink_to(source, target_is_directory=True)
    selection = transfer._normalize_download_paths(
        ["./nested//", *names, "hard", "sym", "dangling", names[0]]
    )
    command, args = transfer._download_archive_command(
        str(alias if source_link else source), True, paths=selection
    )
    result = subprocess.run(
        [command, *args],
        input=b"".join(transfer._selection_stdin(selection)),
        capture_output=True,
        cwd=tmp_path,
        env={**os.environ, "TAR_OPTIONS": "--dereference --recursion"},
        check=True,
    )
    with tarfile.open(fileobj=io.BytesIO(result.stdout)) as archive:
        members = archive.getmembers()
        assert {m.name.removeprefix("./") for m in members} == {
            ".",
            "nested",
            *names,
            "hard",
        }
        assert not any(m.issym() for m in members)
        assert archive.getmember("./hard").islnk()
        assert archive.getmember("./hard").linkname == "./space name"
    assert b"SECRET-EXCLUDED-CONTENT" not in result.stdout
    assert not (tmp_path / "injected").exists()
    payload = tmp_path / "payload.tar"
    payload.write_bytes(result.stdout)
    (tmp_path / "target").mkdir()
    (tmp_path / "target/sym").write_text("keep skipped destination")
    transfer._extract_dir_contents(payload, tmp_path / "target", paths=selection)
    assert (tmp_path / "target/sym").read_text() == "keep skipped destination"
    for name in [*names, "hard"]:
        assert (tmp_path / "target" / name).read_text() == (
            names[0] if name == "hard" else name
        )
    assert not (tmp_path / "target/nested/excluded").exists()


@pytest.mark.skipif(os.name == "nt", reason="remote POSIX shell fixture")
@pytest.mark.parametrize("failure", ["missing", "directory-link", "tar"])
def test_selection_remote_failure_cleans_manifest(tmp_path, failure):
    source = tmp_path / "source"
    source.mkdir()
    (source / "first").write_text("first")
    (source / "link").symlink_to(source, target_is_directory=True)
    # Instrument mktemp so the script's cleanup can be checked without scanning /tmp.
    tools = tmp_path / "bin"
    tools.mkdir()
    manifest = tmp_path / "manifest"
    (tools / "mktemp").write_text('#!/bin/sh\nprintf "%s\\n" "$TEST_MANIFEST"\n')
    (tools / "mktemp").chmod(0o755)
    if failure == "tar":
        (tools / "tar").write_text("#!/bin/sh\nexit 23\n")
        (tools / "tar").chmod(0o755)
    paths = (
        ("first", "link/first" if failure == "directory-link" else "missing")
        if failure != "tar"
        else ("first",)
    )
    command, args = transfer._download_archive_command(str(source), True, paths=paths)
    result = subprocess.run(
        [command, *args],
        input=b"".join(transfer._selection_stdin(paths)),
        capture_output=True,
        env={
            **os.environ,
            "PATH": str(tools) + os.pathsep + os.environ["PATH"],
            "TEST_MANIFEST": str(manifest),
        },
    )
    assert result.returncode != 0
    assert result.stdout == b""
    assert not manifest.exists()


@pytest.mark.parametrize(
    "entries",
    [
        [("./extra", b"secret", "")],
        [("./chosen", b"one", ""), ("./chosen", b"two", "")],
        [("./chosen", tarfile.SYMTYPE, "other")],
        [("./chosen", tarfile.LNKTYPE, "./other")],
        [("./chosen", tarfile.LNKTYPE, "./missing")],
        [(".", tarfile.DIRTYPE, "")],
    ],
)
def test_selection_archive_scope_is_checked_before_callback_or_merge(tmp_path, entries):
    payload = tmp_path / "payload.tar"
    make_archive(payload, entries)
    target = tmp_path / "target"
    target.mkdir()
    (target / "keep").write_text("keep")
    callback = Mock(return_value=None)
    with pytest.raises(tarfile.FilterError):
        transfer._extract_dir_contents(
            payload, target, callback, paths=("chosen", "other")
        )
    callback.assert_not_called()
    assert list(target.iterdir()) == [target / "keep"]


@pytest.mark.parametrize("asynchronous", [False, True])
@pytest.mark.asyncio
async def test_selection_retry_snapshots_paths_and_cleans(
    tmp_path, monkeypatch, asynchronous
):
    selection = ["./nested//data", "nested/data", "hard"]
    archives = []

    def download(*args, **kwargs):
        assert kwargs["paths"] == ("nested/data", "hard")
        selection[:] = ["changed-after-start"]
        archives.append(args[4])
        if len(archives) == 1:
            args[4].write_bytes(b"incomplete")
            raise transfer._TransferInterrupted("retry")
        make_archive(
            args[4],
            [
                ("./nested/data", b"new", ""),
                ("./hard", tarfile.LNKTYPE, "./nested/data"),
            ],
        )

    async def async_download(*args, **kwargs):
        await kwargs["_file_io"].run(lambda: download(*args, **kwargs))

    monkeypatch.setattr(transfer, "_sync_download_archive", download)
    monkeypatch.setattr(transfer, "_async_download_archive", async_download)
    monkeypatch.setattr(
        "runta._internal.retry._full_jitter_delay", lambda *args, **kwargs: 0
    )
    monkeypatch.setattr(
        os,
        "link",
        lambda *args, **kwargs: (_ for _ in ()).throw(OSError("links unavailable")),
    )
    target = tmp_path / "target"
    target.mkdir()
    (target / "keep").write_text("keep")
    (target / "hard").write_text("old")
    fn = (
        transfer.async_download_dir_contents
        if asynchronous
        else transfer.download_dir_contents
    )
    result = fn(
        "http://test",
        "token",
        "runtime",
        "/src",
        target,
        paths=selection,
        timeout=1,
        attempts=2,
    )
    if asynchronous:
        await result
    assert (target / "hard").read_text() == "new"
    assert (target / "keep").read_text() == "keep"
    assert len(archives) == 2
    assert all(not p.parent.exists() for p in archives)


@pytest.mark.parametrize("asynchronous", [False, True])
@pytest.mark.asyncio
async def test_selection_stdin_frames_are_chunked_and_closed(
    tmp_path, monkeypatch, asynchronous
):
    payload = tmp_path / "source.tar"
    make_archive(payload, [("./data", b"ok", "")])
    frames = [
        json.dumps(
            {
                "type": "stdout",
                "data_base64": base64.b64encode(payload.read_bytes()).decode(),
            }
        ),
        json.dumps({"type": "exit", "code": 0}),
        None,
    ]
    sent = []

    def send(frame):
        sent.append(json.loads(frame))

    def recv(*args, **kwargs):
        return frames.pop(0)

    @contextmanager
    def sync_socket(*args, **kwargs):
        yield SimpleNamespace(send=send, recv=recv)

    async def async_send(frame):
        send(frame)

    async def async_recv():
        return recv()

    @asynccontextmanager
    async def async_socket(*args, **kwargs):
        yield SimpleNamespace(send=async_send, recv=async_recv)

    monkeypatch.setattr(transfer, "_sync_socket", sync_socket)
    monkeypatch.setattr(transfer, "_async_socket", async_socket)
    monkeypatch.setattr(transfer, "_CHUNK_SIZE", 7)
    paths = ("data", "name\nwith\n", "中文", "-flag")
    fn = (
        transfer.async_download_dir_contents
        if asynchronous
        else transfer.download_dir_contents
    )
    result = fn(
        "http://test",
        "token",
        "runtime",
        "/src",
        tmp_path / "target",
        paths=paths,
        timeout=1,
    )
    if asynchronous:
        await result
    assert [m["type"] for m in sent][0] == "start"
    assert sent[-1]["type"] == "close_stdin"
    chunks = [base64.b64decode(m["data_base64"]) for m in sent if m["type"] == "stdin"]
    assert all(len(chunk) <= 7 for chunk in chunks)
    assert b"".join(chunks) == b"".join(transfer._selection_stdin(paths))
    assert (tmp_path / "target/data").read_bytes() == b"ok"


@pytest.mark.asyncio
async def test_selection_cancel_during_stdin_closes_socket_and_workspace(
    tmp_path, monkeypatch
):
    entered = asyncio.Event()
    closed = asyncio.Event()
    archives = []
    real_workspace = transfer._async_download_workspace

    @asynccontextmanager
    async def workspace(pool):
        async with real_workspace(pool) as path:
            archives.append(path)
            yield path

    async def send(frame):
        if json.loads(frame)["type"] == "stdin":
            entered.set()
            await asyncio.Future()

    @asynccontextmanager
    async def socket(*args, **kwargs):
        try:
            yield SimpleNamespace(send=send)
        finally:
            closed.set()

    monkeypatch.setattr(transfer, "_async_socket", socket)
    monkeypatch.setattr(transfer, "_async_download_workspace", workspace)
    task = asyncio.create_task(
        transfer.async_download_dir_contents(
            "http://test",
            "token",
            "runtime",
            "/src",
            tmp_path / "target",
            paths=["data"],
            timeout=1,
        )
    )
    await asyncio.wait_for(entered.wait(), 5)
    task.cancel()
    await asyncio.sleep(0)
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
    assert closed.is_set()
    assert all(not path.exists() for path in archives)
    assert not (tmp_path / "target").exists()


@pytest.mark.skipif(os.name == "nt", reason="remote POSIX shell fixture")
def test_selection_single_hardlink_does_not_add_unselected_alias(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    (source / "unselected").write_bytes(b"payload")
    os.link(source / "unselected", source / "selected")
    paths = ("selected",)
    command, args = transfer._download_archive_command(str(source), True, paths=paths)
    result = subprocess.run(
        [command, *args],
        input=b"".join(transfer._selection_stdin(paths)),
        capture_output=True,
        check=True,
    )
    with tarfile.open(fileobj=io.BytesIO(result.stdout)) as archive:
        assert archive.getnames() == [".", "./selected"]
        assert archive.getmember("./selected").isreg()
        assert archive.extractfile("./selected").read() == b"payload"


@pytest.mark.skipif(os.name == "nt", reason="remote POSIX shell fixture")
def test_selection_remote_signal_cleans_private_manifest(tmp_path):
    tools = tmp_path / "bin"
    tools.mkdir()
    manifest = tmp_path / "manifest"
    (tools / "mktemp").write_text(
        '#!/bin/sh\n(umask 077; : > "$TEST_MANIFEST")\nprintf "%s\\n" "$TEST_MANIFEST"\n'
    )
    (tools / "mktemp").chmod(0o755)
    command, args = transfer._download_archive_command(
        str(tmp_path), True, paths=("waiting",)
    )
    process = subprocess.Popen(
        [command, *args],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env={
            **os.environ,
            "PATH": str(tools) + os.pathsep + os.environ["PATH"],
            "TEST_MANIFEST": str(manifest),
        },
    )
    try:
        import time

        deadline = time.monotonic() + 5
        # The root header is written only after cleanup traps are installed.
        # mktemp creates the file earlier, which is not a readiness signal.
        while not manifest.exists() or manifest.read_bytes() != b".\0":
            assert time.monotonic() < deadline
            time.sleep(0.01)
        assert manifest.stat().st_mode & 0o077 == 0
        process.terminate()
        process.communicate(timeout=5)
        assert process.returncode != 0
        assert not manifest.exists()
    finally:
        if process.poll() is None:
            process.kill()
            process.communicate(timeout=5)
