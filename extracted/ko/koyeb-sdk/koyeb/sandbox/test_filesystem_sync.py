"""Pins filesystem.sync() against a miniature executor.

The fake executor backs the streamed /files routes with a real directory
tree, using the sync engine's own walk/build/extract — so push and pull
are exercised end to end (real tar bytes, real extraction, real diff)
with zero network, the way test_filesystem.py pins the legacy seam.
"""

import hashlib
import os
import tempfile
import unittest
from contextlib import asynccontextmanager, contextmanager
from unittest.mock import patch

from koyeb.sandbox.errors import SandboxRequestError
from koyeb.sandbox.filesystem import (
    AsyncSandboxFilesystem,
    SandboxFileNotFoundError,
    SandboxFilesystem,
    SandboxFilesystemError,
)
from koyeb.sandbox.sync import (
    SYNC_BATCH_BYTES,
    build_archive,
    extract_archive,
    walk_local,
)


def _write(path, content=b"x"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(content)


def _body_bytes(content):
    """Bytes from any body shape the client sends: bytes, file, iterator."""
    if isinstance(content, (bytes, bytearray)):
        return bytes(content)
    if hasattr(content, "read"):
        return content.read()
    return b"".join(content)


def _touch_new(path, content=b"new", offset_seconds=5):
    """Write a file with an mtime that differs by whole seconds."""
    _write(path, content)
    st = os.stat(path)
    os.utime(path, ns=(st.st_mtime_ns + offset_seconds * 1_000_000_000,) * 2)


class _FakeExecutorTree:
    """The streamed /files routes over a real directory (executor v0.0.24+).

    Relative remote paths resolve under root — the fake's workdir — the
    way the executor's cwd resolves them. Archive puts are recorded as raw
    bytes so tests can open the exact tars that left the client.
    """

    def __init__(self, root):
        self.root = root
        self.calls = []
        self.archives = []
        self._sessions = {}
        self._next_session = 0
        os.makedirs(root, exist_ok=True)

    def _resolve(self, path):
        if os.path.isabs(path):
            return path
        return os.path.join(self.root, *path.split("/"))

    # ---- streamed routes ----
    def has_files_routes(self):
        return True

    def files_list(self, path, recursive=False):
        self.calls.append(("files_list", path, recursive))
        target = self._resolve(path)
        if not os.path.isdir(target):
            raise SandboxRequestError(
                404, body='{"error": "no such file or directory"}'
            )
        return iter(walk_local(target))

    def files_archive_put(self, path, content):
        data = _body_bytes(content)
        self.calls.append(("files_archive_put", path, len(data)))
        self.archives.append((path, data))
        target = self._resolve(path)
        os.makedirs(target, exist_ok=True)
        fd, spool = tempfile.mkstemp(suffix=".tgz")
        os.close(fd)
        try:
            with open(spool, "wb") as f:
                f.write(data)
            extract_archive(spool, target)
        finally:
            os.unlink(spool)
        return {"files": 1, "bytes": len(data)}

    def files_archive_get(self, path, exclude=()):
        self.calls.append(("files_archive_get", path, tuple(exclude)))
        target = self._resolve(path)
        fd, spool = tempfile.mkstemp(suffix=".tgz")
        os.close(fd)
        try:
            build_archive(target, walk_local(target, exclude=exclude), spool)
            with open(spool, "rb") as f:
                while True:
                    chunk = f.read(65536)
                    if not chunk:
                        break
                    yield chunk
        finally:
            os.unlink(spool)

    def files_stat(self, path, hash=None):
        self.calls.append(("files_stat", path, hash))
        target = self._resolve(path)
        st = os.stat(target)  # follows symlinks, like the executor
        import stat as stat_module

        if stat_module.S_ISDIR(st.st_mode):
            type_ = "dir"
        elif stat_module.S_ISLNK(os.lstat(target).st_mode):
            type_ = "symlink"
        else:
            type_ = "file"
        from koyeb.sandbox.sync import format_mtime

        entry = {
            "type": type_,
            "size": st.st_size,
            "mode": f"{stat_module.S_IMODE(st.st_mode):04o}",
            "mtime": format_mtime(st.st_mtime_ns),
        }
        if hash == "sha256":
            digest = hashlib.sha256()
            with open(target, "rb") as f:
                for chunk in iter(lambda: f.read(1 << 20), b""):
                    digest.update(chunk)
            entry["sha256"] = digest.hexdigest()
        return entry

    def files_read(self, path, chunk_size=65536, timeout=None):
        self.calls.append(("files_read", path))
        with open(self._resolve(path), "rb") as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                yield chunk

    def files_put(
        self, path, content, mode=None, parents=False, sha256=None, timeout=None
    ):
        data = _body_bytes(content)
        self.calls.append(("files_put", path, len(data)))
        target = self._resolve(path)
        if parents:
            os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "wb") as f:
            f.write(data)
        return {"size": len(data), "sha256": hashlib.sha256(data).hexdigest()}

    # ---- multipart sessions (the executor's offset-addressed shape) ----
    def files_upload_open(self, path, size, mode=None, sha256=None, timeout=None):
        self.calls.append(("files_upload_open", path, size))
        upload_id = f"u-{self._next_session}"
        self._next_session += 1
        self._sessions[upload_id] = {
            "path": self._resolve(path),
            "size": size,
            "mode": mode,
            "sha256": sha256,
            "spool": bytearray(size),
            "ranges": [],
        }
        return {"upload_id": upload_id, "max_part_size": 100 * 1024 * 1024}

    def files_upload_part(self, upload_id, offset, content, sha256=None, timeout=None):
        self.calls.append(("files_upload_part", upload_id, offset))
        session = self._sessions[upload_id]
        data = _body_bytes(content)
        if sha256 is not None and hashlib.sha256(data).hexdigest() != sha256:
            raise SandboxRequestError(400, body='{"error": "sha256 mismatch"}')
        session["spool"][offset : offset + len(data)] = data
        session["ranges"].append([offset, offset + len(data)])
        return None

    def files_upload_status(self, upload_id, timeout=None):
        session = self._sessions[upload_id]
        return {"size": session["size"], "ranges": list(session["ranges"])}

    def files_upload_complete(self, upload_id, timeout=None):
        self.calls.append(("files_upload_complete", upload_id))
        session = self._sessions.pop(upload_id)
        missing = self._missing_ranges(session)
        if missing:
            raise SandboxRequestError(
                409,
                body='{"error": "missing ranges", "ranges": ' + repr(missing) + "}",
            )
        data = bytes(session["spool"])
        target = session["path"]
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "wb") as f:
            f.write(data)
        if session["mode"]:
            os.chmod(target, int(session["mode"], 8))
        return {"size": len(data), "sha256": hashlib.sha256(data).hexdigest()}

    def files_upload_abort(self, upload_id, timeout=None):
        self._sessions.pop(upload_id, None)
        return None

    @staticmethod
    def _missing_ranges(session):
        """Spans of [0, size) no part covered, half-open."""
        covered = sorted(session["ranges"])
        missing = []
        cursor = 0
        for start, end in covered:
            if start > cursor:
                missing.append([cursor, start])
            cursor = max(cursor, end)
        if cursor < session["size"]:
            missing.append([cursor, session["size"]])
        return missing

    # ---- legacy routes (deletes have no new-route surface) ----
    def delete_file(self, path):
        self.calls.append(("delete_file", path))
        target = self._resolve(path)
        if not os.path.lexists(target):
            raise SandboxRequestError(
                404, body='{"error": "no such file or directory"}'
            )
        os.remove(target)
        return {}

    def delete_dir(self, path):
        self.calls.append(("delete_dir", path))
        target = self._resolve(path)
        if not os.path.isdir(target):
            raise SandboxRequestError(
                404, body='{"error": "no such file or directory"}'
            )
        import shutil

        shutil.rmtree(target)
        return {}


class _FakeAsyncExecutorTree(_FakeExecutorTree):
    async def has_files_routes(self):
        return _FakeExecutorTree.has_files_routes(self)

    async def files_list(self, path, recursive=False):
        for entry in _FakeExecutorTree.files_list(self, path, recursive):
            yield entry

    async def files_archive_put(self, path, content):
        return _FakeExecutorTree.files_archive_put(self, path, content)

    async def files_archive_get(self, path, exclude=()):
        for chunk in _FakeExecutorTree.files_archive_get(self, path, exclude):
            yield chunk

    async def files_stat(self, path, hash=None):
        return _FakeExecutorTree.files_stat(self, path, hash=hash)

    async def files_read(self, path, chunk_size=65536, timeout=None):
        for chunk in _FakeExecutorTree.files_read(self, path, chunk_size):
            yield chunk

    async def files_put(
        self, path, content, mode=None, parents=False, sha256=None, timeout=None
    ):
        return _FakeExecutorTree.files_put(
            self, path, content, mode=mode, parents=parents, sha256=sha256
        )

    async def delete_file(self, path):
        return _FakeExecutorTree.delete_file(self, path)

    async def delete_dir(self, path):
        return _FakeExecutorTree.delete_dir(self, path)

    async def files_upload_open(self, path, size, mode=None, sha256=None, timeout=None):
        return _FakeExecutorTree.files_upload_open(
            self, path, size, mode=mode, sha256=sha256
        )

    async def files_upload_part(
        self, upload_id, offset, content, sha256=None, timeout=None
    ):
        return _FakeExecutorTree.files_upload_part(
            self, upload_id, offset, content, sha256=sha256
        )

    async def files_upload_status(self, upload_id, timeout=None):
        return _FakeExecutorTree.files_upload_status(self, upload_id)

    async def files_upload_complete(self, upload_id, timeout=None):
        return _FakeExecutorTree.files_upload_complete(self, upload_id)

    async def files_upload_abort(self, upload_id, timeout=None):
        return _FakeExecutorTree.files_upload_abort(self, upload_id)


class _ScriptedExecutorTree(_FakeExecutorTree):
    """An executor whose listing and archive are given verbatim: a pull
    must stay inside its destination whatever the sandbox sends."""

    def __init__(self, root, listing, members):
        super().__init__(root)
        self.listing = listing
        self.members = members

    def files_list(self, path, recursive=False):
        self.calls.append(("files_list", path, recursive))
        return iter(self.listing)

    def files_archive_get(self, path, exclude=()):
        import io
        import tarfile

        self.calls.append(("files_archive_get", path, tuple(exclude)))
        out = io.BytesIO()
        with tarfile.open(fileobj=out, mode="w:gz") as tar:
            for name, linkname, payload in self.members:
                info = tarfile.TarInfo(name)
                if linkname is not None:
                    info.type = tarfile.SYMTYPE
                    info.linkname = linkname
                    tar.addfile(info)
                else:
                    info.size = len(payload)
                    tar.addfile(info, io.BytesIO(payload))
        yield out.getvalue()

    def files_stat(self, path, hash=None):
        return {
            "type": "file",
            "size": 2,
            "mode": "0644",
            "mtime": "2026-10-27T10:00:00Z",
        }

    def files_read(self, path, chunk_size=65536, timeout=None):
        self.calls.append(("files_read", path))
        yield b"hi"


def _listed(path, type_, size=0):
    return {
        "path": path,
        "type": type_,
        "size": size,
        "mode": "0644",
        "mtime": "2026-10-27T10:00:00Z",
    }


class _FakeLegacyExecutor:
    """An executor without the streamed /files routes."""

    def has_files_routes(self):
        return False


class _FakeAsyncLegacyExecutor:
    """The legacy executor, async shape."""

    async def has_files_routes(self):
        return False


@contextmanager
def _fs(client):
    fs = SandboxFilesystem(sandbox=None)
    with patch.object(SandboxFilesystem, "_get_client", return_value=client):
        yield fs


def _local_tree(base, name="src"):
    """A small source tree: file, subdir file, symlink, empty dir.

    File mtimes are pinned: whole-second diffing must not depend on when
    the test happens to run.
    """
    root = os.path.join(base, name)
    _write(os.path.join(root, "a.txt"), b"hello")
    os.chmod(os.path.join(root, "a.txt"), 0o755)
    os.utime(os.path.join(root, "a.txt"), ns=(1774590000_000000000,) * 2)
    _write(os.path.join(root, "sub", "b.bin"), b"\x00\xff")
    os.utime(os.path.join(root, "sub", "b.bin"), ns=(1774590000_000000000,) * 2)
    os.symlink("a.txt", os.path.join(root, "link"))
    os.makedirs(os.path.join(root, "empty"))
    return root


class SyncTestCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.base = self._tmp.name
        self.addCleanup(self._tmp.cleanup)
        self.remote_root = os.path.join(self.base, "workdir")
        self.fake = _FakeExecutorTree(self.remote_root)

    def _calls(self, method):
        return [c for c in self.fake.calls if c[0] == method]

    def _archive_members(self, index=0):
        import io
        import tarfile

        _, data = self.fake.archives[index]
        with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tar:
            return sorted(m.name for m in tar)


class TestSyncPush(SyncTestCase):
    def test_push_new_tree(self):
        local = _local_tree(self.base)

        with _fs(self.fake) as fs:
            result = fs.sync(local, "dst")

        target = os.path.join(self.remote_root, "dst")
        with open(os.path.join(target, "a.txt"), "rb") as f:
            self.assertEqual(f.read(), b"hello")
        self.assertEqual(
            oct(os.stat(os.path.join(target, "a.txt")).st_mode & 0o7777), oct(0o755)
        )
        with open(os.path.join(target, "sub", "b.bin"), "rb") as f:
            self.assertEqual(f.read(), b"\x00\xff")
        self.assertTrue(os.path.islink(os.path.join(target, "link")))
        self.assertTrue(os.path.isdir(os.path.join(target, "empty")))
        self.assertEqual(
            self._archive_members(),
            ["a.txt", "empty", "link", "sub", "sub/b.bin"],
        )
        self.assertEqual(
            result,
            {"uploaded": 5, "deleted": 0, "skipped": 0, "bytes": 5 + 2},
        )

    def test_push_noop_sends_nothing(self):
        local = _local_tree(self.base)
        with _fs(self.fake) as fs:
            fs.sync(local, "dst")
            self.fake.calls.clear()
            self.fake.archives.clear()
            result = fs.sync(local, "dst")

        self.assertEqual(self.fake.archives, [])
        self.assertEqual(
            result,
            {"uploaded": 0, "deleted": 0, "skipped": 5, "bytes": 0},
        )
        self.assertEqual(len(self._calls("files_list")), 1)

    def test_push_noop_with_checksum_stats_only(self):
        local = _local_tree(self.base)
        with _fs(self.fake) as fs:
            fs.sync(local, "dst")
        self.fake.calls.clear()
        self.fake.archives.clear()

        with _fs(self.fake) as fs:
            result = fs.sync(local, "dst", checksum=True)

        self.assertEqual(result["uploaded"], 0)
        self.assertEqual(self.fake.archives, [])
        # The docstring's honest no-op: checksum asks one sha256 stat
        # per size-and-mtime-equal file, nothing else.
        self.assertEqual(len(self._calls("files_stat")), 2)
        self.assertEqual(self._calls("files_archive_put"), [])

    def test_push_changed_file_only(self):
        local = _local_tree(self.base)
        with _fs(self.fake) as fs:
            fs.sync(local, "dst")
            self.fake.calls.clear()
            self.fake.archives.clear()
            _touch_new(os.path.join(local, "sub", "b.bin"), b"\x00\xee")
            result = fs.sync(local, "dst")

        self.assertEqual(self._archive_members(), ["sub/b.bin"])
        self.assertEqual(result["uploaded"], 1)
        self.assertEqual(result["skipped"], 4)
        self.assertEqual(result["bytes"], 2)

    def test_push_delete(self):
        local = _local_tree(self.base)
        with _fs(self.fake) as fs:
            fs.sync(local, "dst")
        _write(os.path.join(self.remote_root, "dst", "extra.txt"))
        self.fake.calls.clear()

        with _fs(self.fake) as fs:
            keep = fs.sync(local, "dst")
        self.assertTrue(
            os.path.exists(os.path.join(self.remote_root, "dst", "extra.txt"))
        )
        with _fs(self.fake) as fs:
            gone = fs.sync(local, "dst", delete=True)
        self.assertFalse(
            os.path.exists(os.path.join(self.remote_root, "dst", "extra.txt"))
        )
        self.assertEqual(keep["skipped"], 6)
        self.assertEqual(gone["deleted"], 1)
        self.assertEqual([c[1] for c in self._calls("delete_file")], ["dst/extra.txt"])

    def test_push_delete_prunes_descendants(self):
        local = _local_tree(self.base)
        with _fs(self.fake) as fs:
            fs.sync(local, "dst")
        _write(os.path.join(self.remote_root, "dst", "gone", "child.txt"))
        self.fake.calls.clear()

        with _fs(self.fake) as fs:
            result = fs.sync(local, "dst", delete=True)

        self.assertFalse(os.path.exists(os.path.join(self.remote_root, "dst", "gone")))
        self.assertEqual([c[1] for c in self._calls("delete_dir")], ["dst/gone"])
        self.assertEqual([c[1] for c in self._calls("delete_file")], [])
        self.assertEqual(result["deleted"], 1)

    def test_push_delete_spares_excluded_remote(self):
        local = _local_tree(self.base)
        _write(os.path.join(self.remote_root, "dst", "skip.log"), b"keep me")
        self.fake.calls.clear()

        with _fs(self.fake) as fs:
            result = fs.sync(local, "dst", exclude=("*.log",), delete=True)

        self.assertTrue(
            os.path.exists(os.path.join(self.remote_root, "dst", "skip.log"))
        )
        self.assertEqual(self._calls("delete_file"), [])
        self.assertEqual(result["deleted"], 0)

    def test_push_type_flip_replaces_remote_dir(self):
        local = _local_tree(self.base)
        _write(os.path.join(local, "flip"), b"now a file")
        _write(os.path.join(self.remote_root, "dst", "flip", "child.txt"))
        self.fake.calls.clear()

        with _fs(self.fake) as fs:
            result = fs.sync(local, "dst", delete=True)

        remote_flip = os.path.join(self.remote_root, "dst", "flip")
        self.assertTrue(os.path.isfile(remote_flip))
        with open(remote_flip, "rb") as f:
            self.assertEqual(f.read(), b"now a file")
        self.assertEqual(result["deleted"], 1)

    def test_push_delete_spares_excluded_remote_dirs_whole(self):
        # The walker prunes an excluded directory whole; the remote
        # plan must spare its descendants too.
        local = _local_tree(self.base)
        _write(os.path.join(self.remote_root, "dst", "backup", "nested", "keep.txt"))
        self.fake.calls.clear()

        with _fs(self.fake) as fs:
            result = fs.sync(local, "dst", exclude=("backup",), delete=True)

        self.assertTrue(
            os.path.exists(
                os.path.join(self.remote_root, "dst", "backup", "nested", "keep.txt")
            )
        )
        self.assertEqual(self._calls("delete_file"), [])
        self.assertEqual(result["deleted"], 0)

    def test_push_oversized_file_routes_through_upload_file(self):
        local = _local_tree(self.base)
        big = os.path.join(local, "big.bin")
        with open(big, "wb") as f:
            f.truncate(SYNC_BATCH_BYTES + 1)

        with _fs(self.fake) as fs:
            result = fs.sync(local, "dst")

        # The rest of the tree still rides one archive batch.
        self.assertEqual(len(self.fake.archives), 1)
        self.assertNotIn("big.bin", self._archive_members())
        # The big file went through the multipart session flow in
        # upload_file, not a single PUT.
        self.assertEqual(
            [c[:2] for c in self._calls("files_upload_open")],
            [("files_upload_open", "dst/big.bin")],
        )
        self.assertEqual(self._calls("files_put"), [])
        self.assertEqual(
            os.path.getsize(os.path.join(self.remote_root, "dst", "big.bin")),
            SYNC_BATCH_BYTES + 1,
        )
        self.assertEqual(result["uploaded"], 6)
        self.assertEqual(result["bytes"], 5 + 2 + SYNC_BATCH_BYTES + 1)

    def test_dry_run_computes_without_transfers(self):
        local = _local_tree(self.base)

        with _fs(self.fake) as fs:
            result = fs.sync(local, "dst", dry_run=True)

        self.assertEqual(self.fake.archives, [])
        self.assertEqual(self._calls("files_archive_put"), [])
        self.assertEqual(self._calls("files_put"), [])
        self.assertEqual(
            result,
            {"uploaded": 5, "deleted": 0, "skipped": 0, "bytes": 5 + 2},
        )

    def test_remote_none_uses_relative_basename(self):
        local = _local_tree(self.base)

        with _fs(self.fake) as fs:
            fs.sync(local)

        self.assertEqual(self._calls("files_list")[0][1], "src")
        self.assertTrue(os.path.exists(os.path.join(self.remote_root, "src", "a.txt")))

    def test_checksum_detects_same_size_same_mtime_change(self):
        local = _local_tree(self.base)
        with _fs(self.fake) as fs:
            fs.sync(local, "dst")
        # Same size, same mtime, different bytes: only sha256 can see it.
        target = os.path.join(self.remote_root, "dst", "a.txt")
        st = os.stat(target)
        with open(target, "wb") as f:
            f.write(b"HELLO")  # same length as "hello"
        os.utime(target, ns=(st.st_mtime_ns,) * 2)
        self.fake.calls.clear()

        with _fs(self.fake) as fs:
            without = fs.sync(local, "dst")
            with_sum = fs.sync(local, "dst", checksum=True)

        self.assertEqual(without["uploaded"], 0)
        self.assertEqual(with_sum["uploaded"], 1)
        # Both file entries passed the size+mtime test, so both hashed.
        self.assertEqual(len(self._calls("files_stat")), 2)

    def test_push_checksum_stat_failure_wraps(self):
        local = _local_tree(self.base)
        with _fs(self.fake) as fs:
            fs.sync(local, "dst")
        target = os.path.join(self.remote_root, "dst", "a.txt")
        with open(target, "wb") as f:
            f.write(b"HELLO")
        st = os.stat(target)
        os.utime(target, ns=(st.st_mtime_ns,) * 2)

        def boom(path, hash=None):
            raise SandboxRequestError(500, body='{"error": "boom"}')

        self.fake.files_stat = boom
        with _fs(self.fake) as fs:
            with self.assertRaises(SandboxFilesystemError) as cm:
                fs.sync(local, "dst", checksum=True)

        self.assertIn("boom", str(cm.exception))

    def test_push_onto_missing_remote_root(self):
        local = _local_tree(self.base)

        with _fs(self.fake) as fs:
            result = fs.sync(local, "brand-new")

        self.assertEqual(result["uploaded"], 5)
        self.assertTrue(
            os.path.exists(os.path.join(self.remote_root, "brand-new", "a.txt"))
        )

    def test_legacy_executor_raises(self):
        local = _local_tree(self.base)
        with _fs(_FakeLegacyExecutor()) as fs:
            with self.assertRaises(SandboxFilesystemError) as cm:
                fs.sync(local, "dst")

        self.assertIn("v0.0.24", str(cm.exception))

    def test_push_from_missing_local_raises(self):
        # rsync refuses a missing source; silently treating it as an
        # empty tree would delete the whole remote side.
        with _fs(self.fake) as fs:
            with self.assertRaises(SandboxFilesystemError):
                fs.sync(os.path.join(self.base, "nope"), "dst")

    def test_bad_direction_raises(self):
        local = _local_tree(self.base)
        with _fs(self.fake) as fs:
            with self.assertRaises(ValueError):
                fs.sync(local, "dst", direction="sideways")

    def test_push_error_wraps_into_taxonomy(self):
        local = _local_tree(self.base)
        self.fake.calls.clear()

        def boom(path, recursive=False):
            raise SandboxRequestError(500, body='{"error": "boom"}')

        self.fake.files_list = boom
        with _fs(self.fake) as fs:
            with self.assertRaises(SandboxFilesystemError) as cm:
                fs.sync(local, "dst")

        self.assertIn("sync", str(cm.exception))


class TestSyncPull(SyncTestCase):
    def test_pull_matching_tree_is_noop(self):
        source = _local_tree(self.base, "src")
        with _fs(self.fake) as fs:
            fs.sync(source, "dst")
        self.fake.calls.clear()

        matching = _local_tree(self.base, "matching-dest")
        with _fs(self.fake) as fs:
            result = fs.sync(matching, "dst", direction="pull")

        self.assertEqual(result["downloaded"], 0)
        self.assertEqual(self._calls("files_archive_get"), [])
        self.assertEqual(result["skipped"], 5)

    def test_pull_into_empty_tree(self):
        source = _local_tree(self.base)
        with _fs(self.fake) as fs:
            fs.sync(source, "dst")
        self.fake.calls.clear()

        dest = os.path.join(self.base, "empty-dest")
        os.makedirs(dest)
        with _fs(self.fake) as fs:
            result = fs.sync(dest, "dst", direction="pull")

        with open(os.path.join(dest, "a.txt"), "rb") as f:
            self.assertEqual(f.read(), b"hello")
        self.assertEqual(
            oct(os.stat(os.path.join(dest, "a.txt")).st_mode & 0o7777), oct(0o755)
        )
        self.assertTrue(os.path.islink(os.path.join(dest, "link")))
        self.assertTrue(os.path.isdir(os.path.join(dest, "empty")))
        self.assertEqual(
            result,
            {"downloaded": 5, "deleted": 0, "skipped": 0, "bytes": 7},
        )
        self.assertEqual(len(self._calls("files_archive_get")), 1)

    def test_pull_noop_sends_nothing(self):
        source = _local_tree(self.base)
        with _fs(self.fake) as fs:
            fs.sync(source, "dst")
        dest = os.path.join(self.base, "dest")
        with _fs(self.fake) as fs:
            fs.sync(dest, "dst", direction="pull")
            self.fake.calls.clear()
            result = fs.sync(dest, "dst", direction="pull")

        self.assertEqual(self._calls("files_archive_get"), [])
        self.assertEqual(result["downloaded"], 0)
        self.assertEqual(result["skipped"], 5)

    def test_pull_delete_removes_local_extras(self):
        source = _local_tree(self.base)
        with _fs(self.fake) as fs:
            fs.sync(source, "dst")
        dest = os.path.join(self.base, "dest")
        with _fs(self.fake) as fs:
            fs.sync(dest, "dst", direction="pull")
        _write(os.path.join(dest, "stale.txt"))
        self.fake.calls.clear()

        with _fs(self.fake) as fs:
            result = fs.sync(dest, "dst", direction="pull", delete=True)

        self.assertFalse(os.path.exists(os.path.join(dest, "stale.txt")))
        self.assertEqual(result["deleted"], 1)

    def test_pull_delete_prunes_descendants(self):
        source = _local_tree(self.base)
        with _fs(self.fake) as fs:
            fs.sync(source, "dst")
        dest = os.path.join(self.base, "dest")
        with _fs(self.fake) as fs:
            fs.sync(dest, "dst", direction="pull")
        _write(os.path.join(dest, "gonedir", "child.txt"))
        self.fake.calls.clear()

        with _fs(self.fake) as fs:
            result = fs.sync(dest, "dst", direction="pull", delete=True)

        self.assertFalse(os.path.exists(os.path.join(dest, "gonedir")))
        self.assertEqual(result["deleted"], 1)

    def test_pull_excludes_remote_entries_from_plan(self):
        source = _local_tree(self.base)
        with _fs(self.fake) as fs:
            fs.sync(source, "dst")
        _write(os.path.join(self.remote_root, "dst", "skip.log"), b"not wanted")
        self.fake.calls.clear()

        dest = os.path.join(self.base, "dest")
        os.makedirs(dest)
        with _fs(self.fake) as fs:
            result = fs.sync(dest, "dst", direction="pull", exclude=("*.log",))

        self.assertFalse(os.path.exists(os.path.join(dest, "skip.log")))
        self.assertTrue(os.path.exists(os.path.join(dest, "a.txt")))
        self.assertEqual(result["downloaded"], 5)
        self.assertEqual(
            self._calls("files_archive_get"),
            [("files_archive_get", "dst", ("*.log",))],
        )

    def test_pull_colliding_dir_prune_refuses_loudly(self):
        # An oversized name also prunes same-named directories whole
        # from the archive — their planned contents would be lost.
        source = _local_tree(self.base)
        with _fs(self.fake) as fs:
            fs.sync(source, "dst")
        _write(
            os.path.join(self.remote_root, "dst", "x", "backup", "small.txt"),
            b"first",
        )
        dest = os.path.join(self.base, "dest")
        with _fs(self.fake) as fs:
            fs.sync(dest, "dst", direction="pull")

        big = os.path.join(self.remote_root, "dst", "backup")
        with open(big, "wb") as f:
            f.truncate(SYNC_BATCH_BYTES + 1)
        _write(
            os.path.join(self.remote_root, "dst", "x", "backup", "small.txt"),
            b"changed",
        )
        self.fake.calls.clear()

        with _fs(self.fake) as fs:
            with self.assertRaises(SandboxFilesystemError) as cm:
                fs.sync(dest, "dst", direction="pull")

        self.assertIn("x/backup/small.txt", str(cm.exception))

    def test_pull_type_flip_replaces_local_dir(self):
        source = _local_tree(self.base)
        with _fs(self.fake) as fs:
            fs.sync(source, "dst")
        _write(os.path.join(self.remote_root, "dst", "flip"), b"remote file")
        dest = os.path.join(self.base, "dest")
        _write(os.path.join(dest, "flip", "child.txt"))
        self.fake.calls.clear()

        with _fs(self.fake) as fs:
            result = fs.sync(dest, "dst", direction="pull", delete=True)

        local_flip = os.path.join(dest, "flip")
        self.assertTrue(os.path.isfile(local_flip))
        with open(local_flip, "rb") as f:
            self.assertEqual(f.read(), b"remote file")
        self.assertEqual(result["deleted"], 1)

    def test_pull_excludes_descendants_of_excluded_dirs(self):
        # The archive walker prunes an excluded directory whole; the
        # plan must agree or members silently vanish.
        source = _local_tree(self.base)
        with _fs(self.fake) as fs:
            fs.sync(source, "dst")
        _write(
            os.path.join(self.remote_root, "dst", "x", "backup", "small.txt"),
            b"deep",
        )
        dest = os.path.join(self.base, "dest")
        with _fs(self.fake) as fs:
            fs.sync(dest, "dst", direction="pull")
        self.fake.calls.clear()

        with _fs(self.fake) as fs:
            result = fs.sync(dest, "dst", direction="pull", exclude=("backup",))

        self.assertEqual(result["downloaded"], 0)
        self.assertEqual(self._calls("files_archive_get"), [])
        with open(os.path.join(dest, "x", "backup", "small.txt"), "rb") as f:
            self.assertEqual(f.read(), b"deep")

    def test_pull_colliding_suffix_member_refuses_loudly(self):
        # An oversized name also drops same-suffixed planned members
        # from the archive — refuse loudly instead of losing them.
        source = _local_tree(self.base)
        with _fs(self.fake) as fs:
            fs.sync(source, "dst")
        big = os.path.join(self.remote_root, "dst", "big.bin")
        with open(big, "wb") as f:
            f.truncate(SYNC_BATCH_BYTES + 1)
        _write(os.path.join(self.remote_root, "dst", "backup", "big.bin"), b"new")
        dest = os.path.join(self.base, "dest")
        os.makedirs(dest)

        with _fs(self.fake) as fs:
            with self.assertRaises(SandboxFilesystemError) as cm:
                fs.sync(dest, "dst", direction="pull")

        self.assertIn("backup/big.bin", str(cm.exception))

    def test_pull_excluded_oversized_is_not_downloaded(self):
        source = _local_tree(self.base)
        with _fs(self.fake) as fs:
            fs.sync(source, "dst")
        big = os.path.join(self.remote_root, "dst", "big.bin")
        with open(big, "wb") as f:
            f.truncate(SYNC_BATCH_BYTES + 1)
        self.fake.calls.clear()

        dest = os.path.join(self.base, "dest")
        os.makedirs(dest)
        with _fs(self.fake) as fs:
            result = fs.sync(dest, "dst", direction="pull", exclude=("big.bin",))

        self.assertFalse(os.path.exists(os.path.join(dest, "big.bin")))
        self.assertEqual(self._calls("files_read"), [])
        self.assertEqual(result["downloaded"], 5)

    def test_pull_oversized_routes_through_download_file(self):
        source = _local_tree(self.base)
        with _fs(self.fake) as fs:
            fs.sync(source, "dst")
        big = os.path.join(self.remote_root, "dst", "big.bin")
        with open(big, "wb") as f:
            f.truncate(SYNC_BATCH_BYTES + 1)
        st = os.stat(big)
        os.utime(big, ns=(st.st_mtime_ns + 5_000_000_000,) * 2)
        self.fake.calls.clear()

        dest = os.path.join(self.base, "dest")
        os.makedirs(dest)
        with _fs(self.fake) as fs:
            result = fs.sync(dest, "dst", direction="pull")

        self.assertEqual(
            os.path.getsize(os.path.join(dest, "big.bin")), SYNC_BATCH_BYTES + 1
        )
        # big.bin rode download_file; the pull archive excluded it so its
        # bytes did not travel twice.
        self.assertEqual(result["downloaded"], 6)
        self.assertEqual(self._calls("files_read"), [("files_read", "dst/big.bin")])
        self.assertIn("big.bin", self._calls("files_archive_get")[0][2])

    def test_dry_run_pull_touches_nothing(self):
        source = _local_tree(self.base)
        with _fs(self.fake) as fs:
            fs.sync(source, "dst")
        self.fake.calls.clear()

        dest = os.path.join(self.base, "empty-dest")
        os.makedirs(dest)
        with _fs(self.fake) as fs:
            result = fs.sync(dest, "dst", direction="pull", dry_run=True)

        self.assertEqual(self._calls("files_archive_get"), [])
        self.assertEqual(os.listdir(dest), [])
        self.assertEqual(
            result,
            {"downloaded": 5, "deleted": 0, "skipped": 0, "bytes": 7},
        )

    def test_pull_missing_remote_raises(self):
        local = _local_tree(self.base)
        with _fs(self.fake) as fs:
            with self.assertRaises(SandboxFileNotFoundError):
                fs.sync(local, "missing", direction="pull")

    def _outside(self):
        outside = os.path.join(self.base, "outside")
        _write(os.path.join(outside, "child.txt"), b"keep")
        return outside

    def test_pull_refuses_listing_path_outside_dest(self):
        outside = self._outside()
        fake = _ScriptedExecutorTree(
            self.remote_root,
            [_listed("../outside/evil.txt", "file", 2)],
            [("../outside/evil.txt", None, b"hi")],
        )
        dest = os.path.join(self.base, "dest")

        with _fs(fake) as fs:
            with self.assertRaises(SandboxFilesystemError):
                fs.sync(dest, "dst", direction="pull")

        self.assertEqual(os.listdir(outside), ["child.txt"])
        self.assertEqual([c for c in fake.calls if c[0] == "files_archive_get"], [])

    def test_pull_refuses_member_through_symlink(self):
        outside = self._outside()
        fake = _ScriptedExecutorTree(
            self.remote_root,
            [_listed("a", "symlink"), _listed("a/evil.txt", "file", 2)],
            [("a", outside, None), ("a/evil.txt", None, b"hi")],
        )
        dest = os.path.join(self.base, "dest")

        with _fs(fake) as fs:
            with self.assertRaises(SandboxFilesystemError):
                fs.sync(dest, "dst", direction="pull")

        self.assertEqual(os.listdir(outside), ["child.txt"])

    def test_pull_refuses_oversized_download_through_symlink(self):
        outside = self._outside()
        fake = _ScriptedExecutorTree(
            self.remote_root,
            [
                _listed("a", "symlink"),
                _listed("a/big.bin", "file", SYNC_BATCH_BYTES + 1),
            ],
            [("a", outside, None)],
        )
        dest = os.path.join(self.base, "dest")

        with _fs(fake) as fs:
            with self.assertRaises(SandboxFilesystemError):
                fs.sync(dest, "dst", direction="pull")

        self.assertEqual(os.listdir(outside), ["child.txt"])
        self.assertEqual([c for c in fake.calls if c[0] == "files_read"], [])

    def test_pull_oversized_part_symlink_not_followed(self):
        # The archive lands before the oversized downloads: a symlink at
        # <name>.part must not carry the download's bytes elsewhere.
        victim = os.path.join(self._outside(), "child.txt")
        remote = os.path.join(self.remote_root, "dst")
        big = os.path.join(remote, "big.bin")
        _write(big, b"")
        with open(big, "wb") as f:
            f.truncate(SYNC_BATCH_BYTES + 1)
        os.symlink(victim, os.path.join(remote, "big.bin.part"))
        dest = os.path.join(self.base, "dest")

        with _fs(self.fake) as fs:
            with self.assertRaises(SandboxFilesystemError):
                fs.sync(dest, "dst", direction="pull")

        with open(victim, "rb") as f:
            self.assertEqual(f.read(), b"keep")

    def test_pull_type_flip_to_symlink_deletes_nothing_through_it(self):
        outside = self._outside()
        os.makedirs(os.path.join(self.remote_root, "dst"))
        os.symlink(outside, os.path.join(self.remote_root, "dst", "flip"))
        dest = os.path.join(self.base, "dest")
        _write(os.path.join(dest, "flip", "child.txt"))

        with _fs(self.fake) as fs:
            result = fs.sync(dest, "dst", direction="pull", delete=True)

        self.assertTrue(os.path.islink(os.path.join(dest, "flip")))
        self.assertEqual(os.listdir(outside), ["child.txt"])
        self.assertEqual(result["deleted"], 1)


class TestAsyncSyncPush(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.base = self._tmp.name
        self.addCleanup(self._tmp.cleanup)
        self.remote_root = os.path.join(self.base, "workdir")
        self.fake = _FakeAsyncExecutorTree(self.remote_root)

    async def test_push_new_tree_and_noop(self):
        local = _local_tree(self.base)
        async with _async_ctx(self.fake) as fs:
            result = await fs.sync(local, "dst")
            self.fake.calls.clear()
            again = await fs.sync(local, "dst")

        self.assertEqual(result["uploaded"], 5)
        self.assertEqual(again["uploaded"], 0)
        self.assertTrue(os.path.exists(os.path.join(self.remote_root, "dst", "a.txt")))

    async def test_pull_into_empty_tree(self):
        source = _local_tree(self.base)
        async with _async_ctx(self.fake) as fs:
            await fs.sync(source, "dst")
        self.fake.calls.clear()

        dest = os.path.join(self.base, "empty-dest")
        os.makedirs(dest)
        async with _async_ctx(self.fake) as fs:
            result = await fs.sync(dest, "dst", direction="pull")

        self.assertEqual(result["downloaded"], 5)
        with open(os.path.join(dest, "a.txt"), "rb") as f:
            self.assertEqual(f.read(), b"hello")

    async def test_dry_run_computes_without_transfers(self):
        local = _local_tree(self.base)
        async with _async_ctx(self.fake) as fs:
            result = await fs.sync(local, "dst", dry_run=True)

        self.assertEqual(
            [c for c in self.fake.calls if c[0] == "files_archive_put"], []
        )
        self.assertEqual(result["uploaded"], 5)

    async def test_push_delete(self):
        local = _local_tree(self.base)
        async with _async_ctx(self.fake) as fs:
            await fs.sync(local, "dst")
        _write(os.path.join(self.remote_root, "dst", "extra.txt"))
        self.fake.calls.clear()

        async with _async_ctx(self.fake) as fs:
            result = await fs.sync(local, "dst", delete=True)

        self.assertFalse(
            os.path.exists(os.path.join(self.remote_root, "dst", "extra.txt"))
        )
        self.assertEqual(result["deleted"], 1)

    async def test_push_delete_spares_excluded_remote(self):
        local = _local_tree(self.base)
        _write(os.path.join(self.remote_root, "dst", "skip.log"), b"keep me")
        self.fake.calls.clear()

        async with _async_ctx(self.fake) as fs:
            result = await fs.sync(local, "dst", exclude=("*.log",), delete=True)

        self.assertTrue(
            os.path.exists(os.path.join(self.remote_root, "dst", "skip.log"))
        )
        self.assertEqual(result["deleted"], 0)

    async def test_push_delete_spares_excluded_remote_dirs_whole(self):
        local = _local_tree(self.base)
        _write(os.path.join(self.remote_root, "dst", "backup", "nested", "keep.txt"))
        self.fake.calls.clear()

        async with _async_ctx(self.fake) as fs:
            result = await fs.sync(local, "dst", exclude=("backup",), delete=True)

        self.assertTrue(
            os.path.exists(
                os.path.join(self.remote_root, "dst", "backup", "nested", "keep.txt")
            )
        )
        self.assertEqual(result["deleted"], 0)

    async def test_push_type_flip_replaces_remote_dir(self):
        local = _local_tree(self.base)
        _write(os.path.join(local, "flip"), b"now a file")
        _write(os.path.join(self.remote_root, "dst", "flip", "child.txt"))
        self.fake.calls.clear()

        async with _async_ctx(self.fake) as fs:
            result = await fs.sync(local, "dst", delete=True)

        remote_flip = os.path.join(self.remote_root, "dst", "flip")
        self.assertTrue(os.path.isfile(remote_flip))
        with open(remote_flip, "rb") as f:
            self.assertEqual(f.read(), b"now a file")
        self.assertEqual(result["deleted"], 1)

    async def test_pull_type_flip_replaces_local_dir(self):
        source = _local_tree(self.base)
        async with _async_ctx(self.fake) as fs:
            await fs.sync(source, "dst")
        _write(os.path.join(self.remote_root, "dst", "flip"), b"remote file")
        dest = os.path.join(self.base, "dest")
        _write(os.path.join(dest, "flip", "child.txt"))
        self.fake.calls.clear()

        async with _async_ctx(self.fake) as fs:
            result = await fs.sync(dest, "dst", direction="pull", delete=True)

        local_flip = os.path.join(dest, "flip")
        self.assertTrue(os.path.isfile(local_flip))
        with open(local_flip, "rb") as f:
            self.assertEqual(f.read(), b"remote file")
        self.assertEqual(result["deleted"], 1)

    async def test_pull_excludes_remote_entries_from_plan(self):
        source = _local_tree(self.base)
        async with _async_ctx(self.fake) as fs:
            await fs.sync(source, "dst")
        _write(os.path.join(self.remote_root, "dst", "skip.log"), b"not wanted")
        self.fake.calls.clear()

        dest = os.path.join(self.base, "dest")
        os.makedirs(dest)
        async with _async_ctx(self.fake) as fs:
            result = await fs.sync(dest, "dst", direction="pull", exclude=("*.log",))

        self.assertFalse(os.path.exists(os.path.join(dest, "skip.log")))
        self.assertTrue(os.path.exists(os.path.join(dest, "a.txt")))
        self.assertEqual(result["downloaded"], 5)
        get_calls = [c for c in self.fake.calls if c[0] == "files_archive_get"]
        self.assertEqual(get_calls, [("files_archive_get", "dst", ("*.log",))])

    async def test_pull_colliding_dir_prune_refuses_loudly(self):
        source = _local_tree(self.base)
        async with _async_ctx(self.fake) as fs:
            await fs.sync(source, "dst")
        _write(
            os.path.join(self.remote_root, "dst", "x", "backup", "small.txt"),
            b"first",
        )
        dest = os.path.join(self.base, "dest")
        async with _async_ctx(self.fake) as fs:
            await fs.sync(dest, "dst", direction="pull")

        big = os.path.join(self.remote_root, "dst", "backup")
        with open(big, "wb") as f:
            f.truncate(SYNC_BATCH_BYTES + 1)
        _write(
            os.path.join(self.remote_root, "dst", "x", "backup", "small.txt"),
            b"changed",
        )
        self.fake.calls.clear()

        async with _async_ctx(self.fake) as fs:
            with self.assertRaises(SandboxFilesystemError) as cm:
                await fs.sync(dest, "dst", direction="pull")

        self.assertIn("x/backup/small.txt", str(cm.exception))

    async def test_pull_excludes_descendants_of_excluded_dirs(self):
        source = _local_tree(self.base)
        async with _async_ctx(self.fake) as fs:
            await fs.sync(source, "dst")
        _write(
            os.path.join(self.remote_root, "dst", "x", "backup", "small.txt"),
            b"deep",
        )
        dest = os.path.join(self.base, "dest")
        async with _async_ctx(self.fake) as fs:
            await fs.sync(dest, "dst", direction="pull")
        self.fake.calls.clear()

        async with _async_ctx(self.fake) as fs:
            result = await fs.sync(dest, "dst", direction="pull", exclude=("backup",))

        self.assertEqual(result["downloaded"], 0)
        get_calls = [c for c in self.fake.calls if c[0] == "files_archive_get"]
        self.assertEqual(get_calls, [])
        with open(os.path.join(dest, "x", "backup", "small.txt"), "rb") as f:
            self.assertEqual(f.read(), b"deep")

    async def test_pull_colliding_suffix_member_refuses_loudly(self):
        source = _local_tree(self.base)
        async with _async_ctx(self.fake) as fs:
            await fs.sync(source, "dst")
        big = os.path.join(self.remote_root, "dst", "big.bin")
        with open(big, "wb") as f:
            f.truncate(SYNC_BATCH_BYTES + 1)
        _write(os.path.join(self.remote_root, "dst", "backup", "big.bin"), b"new")
        dest = os.path.join(self.base, "dest")
        os.makedirs(dest)

        async with _async_ctx(self.fake) as fs:
            with self.assertRaises(SandboxFilesystemError) as cm:
                await fs.sync(dest, "dst", direction="pull")

        self.assertIn("backup/big.bin", str(cm.exception))

    async def test_pull_excluded_oversized_is_not_downloaded(self):
        source = _local_tree(self.base)
        async with _async_ctx(self.fake) as fs:
            await fs.sync(source, "dst")
        big = os.path.join(self.remote_root, "dst", "big.bin")
        with open(big, "wb") as f:
            f.truncate(SYNC_BATCH_BYTES + 1)
        self.fake.calls.clear()

        dest = os.path.join(self.base, "dest")
        os.makedirs(dest)
        async with _async_ctx(self.fake) as fs:
            result = await fs.sync(dest, "dst", direction="pull", exclude=("big.bin",))

        self.assertFalse(os.path.exists(os.path.join(dest, "big.bin")))
        read_calls = [c for c in self.fake.calls if c[0] == "files_read"]
        self.assertEqual(read_calls, [])
        self.assertEqual(result["downloaded"], 5)

    async def test_pull_oversized_routes_through_download_file(self):
        source = _local_tree(self.base)
        async with _async_ctx(self.fake) as fs:
            await fs.sync(source, "dst")
        big = os.path.join(self.remote_root, "dst", "big.bin")
        with open(big, "wb") as f:
            f.truncate(SYNC_BATCH_BYTES + 1)
        st = os.stat(big)
        os.utime(big, ns=(st.st_mtime_ns + 5_000_000_000,) * 2)
        self.fake.calls.clear()

        dest = os.path.join(self.base, "dest")
        os.makedirs(dest)
        async with _async_ctx(self.fake) as fs:
            result = await fs.sync(dest, "dst", direction="pull")

        self.assertEqual(
            os.path.getsize(os.path.join(dest, "big.bin")), SYNC_BATCH_BYTES + 1
        )
        self.assertEqual(result["downloaded"], 6)
        read_calls = [c for c in self.fake.calls if c[0] == "files_read"]
        self.assertEqual(read_calls, [("files_read", "dst/big.bin")])
        get_calls = [c for c in self.fake.calls if c[0] == "files_archive_get"]
        self.assertIn("big.bin", get_calls[0][2])

    async def test_push_from_missing_local_raises(self):
        # rsync refuses a missing source; silently treating it as an
        # empty tree would delete the whole remote side.
        async with _async_ctx(self.fake) as fs:
            with self.assertRaises(SandboxFilesystemError):
                await fs.sync(os.path.join(self.base, "nope"), "dst")

    async def test_legacy_executor_raises(self):
        local = _local_tree(self.base)
        async with _async_ctx(_FakeAsyncLegacyExecutor()) as fs:
            with self.assertRaises(SandboxFilesystemError) as cm:
                await fs.sync(local, "dst")

        self.assertIn("v0.0.24", str(cm.exception))

    async def test_bad_direction_raises(self):
        local = _local_tree(self.base)
        async with _async_ctx(self.fake) as fs:
            with self.assertRaises(ValueError):
                await fs.sync(local, "dst", direction="sideways")

    async def test_push_error_wraps_into_taxonomy(self):
        local = _local_tree(self.base)

        def boom(path, recursive=False):
            raise SandboxRequestError(500, body='{"error": "boom"}')

        self.fake.files_list = boom
        async with _async_ctx(self.fake) as fs:
            with self.assertRaises(SandboxFilesystemError) as cm:
                await fs.sync(local, "dst")

        self.assertIn("boom", str(cm.exception))

    async def test_pull_missing_remote_raises(self):
        dest = os.path.join(self.base, "dest")
        os.makedirs(dest)
        async with _async_ctx(self.fake) as fs:
            with self.assertRaises(SandboxFileNotFoundError):
                await fs.sync(dest, "missing", direction="pull")

    async def test_push_oversized_file_routes_through_upload_file(self):
        local = _local_tree(self.base)
        big = os.path.join(local, "big.bin")
        with open(big, "wb") as f:
            f.truncate(SYNC_BATCH_BYTES + 1)

        async with _async_ctx(self.fake) as fs:
            result = await fs.sync(local, "dst")

        self.assertEqual(len(self.fake.archives), 1)
        open_calls = [c for c in self.fake.calls if c[0] == "files_upload_open"]
        self.assertEqual(
            [c[:2] for c in open_calls], [("files_upload_open", "dst/big.bin")]
        )
        self.assertEqual(
            os.path.getsize(os.path.join(self.remote_root, "dst", "big.bin")),
            SYNC_BATCH_BYTES + 1,
        )
        self.assertEqual(result["uploaded"], 6)

    async def test_push_checksum_stat_failure_wraps(self):
        local = _local_tree(self.base)
        async with _async_ctx(self.fake) as fs:
            await fs.sync(local, "dst")
        target = os.path.join(self.remote_root, "dst", "a.txt")
        with open(target, "wb") as f:
            f.write(b"HELLO")
        st = os.stat(target)
        os.utime(target, ns=(st.st_mtime_ns,) * 2)

        def boom(path, hash=None):
            raise SandboxRequestError(500, body='{"error": "boom"}')

        self.fake.files_stat = boom
        async with _async_ctx(self.fake) as fs:
            with self.assertRaises(SandboxFilesystemError) as cm:
                await fs.sync(local, "dst", checksum=True)

        self.assertIn("boom", str(cm.exception))

    async def test_push_noop_with_checksum_stats_only(self):
        local = _local_tree(self.base)
        async with _async_ctx(self.fake) as fs:
            await fs.sync(local, "dst")
        self.fake.calls.clear()
        self.fake.archives.clear()

        async with _async_ctx(self.fake) as fs:
            result = await fs.sync(local, "dst", checksum=True)

        self.assertEqual(result["uploaded"], 0)
        self.assertEqual(self.fake.archives, [])
        stat_calls = [c for c in self.fake.calls if c[0] == "files_stat"]
        self.assertEqual(len(stat_calls), 2)
        put_calls = [c for c in self.fake.calls if c[0] == "files_archive_put"]
        self.assertEqual(put_calls, [])

    async def test_checksum_detects_content_change(self):
        local = _local_tree(self.base)
        async with _async_ctx(self.fake) as fs:
            await fs.sync(local, "dst")
        target = os.path.join(self.remote_root, "dst", "a.txt")
        st = os.stat(target)
        with open(target, "wb") as f:
            f.write(b"HELLO")  # same length as "hello"
        os.utime(target, ns=(st.st_mtime_ns,) * 2)
        self.fake.calls.clear()

        async with _async_ctx(self.fake) as fs:
            without = await fs.sync(local, "dst")
            with_sum = await fs.sync(local, "dst", checksum=True)

        self.assertEqual(without["uploaded"], 0)
        self.assertEqual(with_sum["uploaded"], 1)
        # Both file entries passed the size+mtime test, so both hashed.
        self.assertEqual(len([c for c in self.fake.calls if c[0] == "files_stat"]), 2)

    async def test_pull_oversized_part_symlink_not_followed(self):
        victim = os.path.join(self.base, "outside", "child.txt")
        _write(victim, b"keep")
        remote = os.path.join(self.remote_root, "dst")
        big = os.path.join(remote, "big.bin")
        _write(big, b"")
        with open(big, "wb") as f:
            f.truncate(SYNC_BATCH_BYTES + 1)
        os.symlink(victim, os.path.join(remote, "big.bin.part"))
        dest = os.path.join(self.base, "dest")

        async with _async_ctx(self.fake) as fs:
            with self.assertRaises(SandboxFilesystemError):
                await fs.sync(dest, "dst", direction="pull")

        with open(victim, "rb") as f:
            self.assertEqual(f.read(), b"keep")

    async def test_pull_type_flip_to_symlink_deletes_nothing_through_it(self):
        outside = os.path.join(self.base, "outside")
        _write(os.path.join(outside, "child.txt"), b"keep")
        os.makedirs(os.path.join(self.remote_root, "dst"))
        os.symlink(outside, os.path.join(self.remote_root, "dst", "flip"))
        dest = os.path.join(self.base, "dest")
        _write(os.path.join(dest, "flip", "child.txt"))

        async with _async_ctx(self.fake) as fs:
            result = await fs.sync(dest, "dst", direction="pull", delete=True)

        self.assertTrue(os.path.islink(os.path.join(dest, "flip")))
        self.assertEqual(os.listdir(outside), ["child.txt"])
        self.assertEqual(result["deleted"], 1)

    async def test_pull_delete_removes_local_extras(self):
        source = _local_tree(self.base)
        async with _async_ctx(self.fake) as fs:
            await fs.sync(source, "dst")
        dest = os.path.join(self.base, "dest")
        async with _async_ctx(self.fake) as fs:
            await fs.sync(dest, "dst", direction="pull")
        _write(os.path.join(dest, "stale.txt"))
        _write(os.path.join(dest, "gonedir", "child.txt"))
        self.fake.calls.clear()

        async with _async_ctx(self.fake) as fs:
            result = await fs.sync(dest, "dst", direction="pull", delete=True)

        self.assertFalse(os.path.exists(os.path.join(dest, "stale.txt")))
        self.assertFalse(os.path.exists(os.path.join(dest, "gonedir")))
        # A directory counts as one deletion; its descendants ride it.
        self.assertEqual(result["deleted"], 2)


@asynccontextmanager
async def _async_ctx(client):
    fs = AsyncSandboxFilesystem(sandbox=None)
    with patch.object(AsyncSandboxFilesystem, "_get_async_client", return_value=client):
        yield fs


class TestJoinHelpers(unittest.TestCase):
    def test_remote_join(self):
        from koyeb.sandbox.sync import remote_join

        self.assertEqual(remote_join("dst", "a/b.txt"), "dst/a/b.txt")
        self.assertEqual(remote_join("/abs", "x"), "/abs/x")

    def test_join_local(self):
        from koyeb.sandbox.sync import join_local

        self.assertEqual(
            join_local("/base", "a/b.txt"), os.path.join("/base", "a", "b.txt")
        )

    def test_join_local_refuses_paths_outside_root(self):
        from koyeb.sandbox.sync import join_local

        with tempfile.TemporaryDirectory() as root:
            os.symlink(tempfile.gettempdir(), os.path.join(root, "link"))
            for rel in ("../x", "/etc/x", "a/../../x", "link/x"):
                with self.subTest(rel=rel), self.assertRaises(ValueError):
                    join_local(root, rel)


if __name__ == "__main__":
    unittest.main()
