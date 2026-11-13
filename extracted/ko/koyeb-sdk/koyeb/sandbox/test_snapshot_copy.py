"""Pins DeclarativeSnapshot's copy onto the new routes.

``copy`` moves a local file or directory into the builder sandbox:
directories travel as one archive push (binary-safe, modes/mtimes/symlinks
kept) on executors v0.0.24+, single files through the streamed
upload_file — with the legacy per-file walk preserved for old executors.
"""

import os
import tempfile
import types
import unittest
from unittest.mock import patch

from koyeb.sandbox import Sandbox
from koyeb.sandbox.errors import SandboxError
from koyeb.sandbox.snapshot import DeclarativeSnapshot


class _FakeFS:
    def __init__(self, new_routes):
        self.new_routes = new_routes
        self.calls = []

    def _get_client(self):
        return self

    def has_files_routes(self):
        return self.new_routes

    def sync(self, local, remote, **kwargs):
        self.calls.append(("sync", local, remote))
        return {"uploaded": 0, "deleted": 0, "skipped": 0, "bytes": 0}

    def upload_file(self, local, remote, **kwargs):
        self.calls.append(("upload_file", local, remote))

    def mkdir(self, path):
        self.calls.append(("mkdir", path))

    def write_file(self, path, content, encoding="utf-8"):
        self.calls.append(("write_file", path, content, encoding))


class _FakeBuilderSandbox:
    def __init__(self, fs):
        self.filesystem = fs


class SnapshotCopyTestCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.base = self._tmp.name
        self.addCleanup(self._tmp.cleanup)
        self.snap = DeclarativeSnapshot(name="t", image="img", api_token="token")

    def _fs(self, new_routes):
        fs = _FakeFS(new_routes)
        self.snap._builder_sandbox = _FakeBuilderSandbox(fs)
        return fs

    def _tree(self):
        # Text-only contents: the legacy arm reads files as text, exactly
        # as it always did — the binary-safety of the new arms is
        # upload_file/sync's own tested property.
        root = os.path.join(self.base, "src")
        os.makedirs(os.path.join(root, "sub"))
        with open(os.path.join(root, "a.txt"), "wb") as f:
            f.write(b"hello")
        with open(os.path.join(root, "sub", "b.txt"), "wb") as f:
            f.write(b"world")
        return root


class TestCopyDirectory(SnapshotCopyTestCase):
    def test_new_routes_pushes_one_archive(self):
        src = self._tree()
        fs = self._fs(new_routes=True)

        self.snap._copy(src, "dst")

        self.assertEqual(
            [c[0] for c in fs.calls],
            ["sync"],
        )
        self.assertEqual(fs.calls[0][1:], (src, "dst"))

    def test_legacy_walks_per_file(self):
        src = self._tree()
        fs = self._fs(new_routes=False)

        self.snap._copy(src, "dst")

        methods = [c[0] for c in fs.calls]
        self.assertNotIn("sync", methods)
        self.assertIn("mkdir", methods)
        self.assertEqual(methods.count("write_file"), 2)
        written = {c[1]: c[2] for c in fs.calls if c[0] == "write_file"}
        self.assertEqual(written["dst/a.txt"], "hello")

    def test_legacy_walk_reads_text_like_before(self):
        # The legacy arm keeps its historical shape: directories created,
        # files read as text. Unchanged behavior for old executors.
        src = self._tree()
        fs = self._fs(new_routes=False)

        self.snap._copy(src, "dst")

        made = [c[1] for c in fs.calls if c[0] == "mkdir"]
        # The root itself was never an explicit mkdir: make_dir's MkdirAll
        # semantics create it as a parent — unchanged legacy behavior.
        self.assertEqual(made, ["dst/sub"])


class TestCopySingleFile(SnapshotCopyTestCase):
    def test_uploads_streamed_binary_safe(self):
        src = os.path.join(self.base, "one.bin")
        with open(src, "wb") as f:
            f.write(b"\x00\x01")
        fs = self._fs(new_routes=True)

        self.snap._copy(src, "dst/one.bin")

        self.assertEqual(
            fs.calls,
            [("upload_file", src, "dst/one.bin")],
        )

    def test_build_applies_the_whole_recipe(self):
        # build() must reach every recipe arm — workdir, files, the copy
        # seam, commands — on the live builder, not just in isolation.
        source = self._tree()
        fs = _FakeFS(True)
        stub = types.SimpleNamespace(filesystem=fs, calls=[])

        def _snapshot(**kw):
            stub.calls.append(("snapshot", kw["name"]))
            return types.SimpleNamespace(operations=None)

        def _exec(command, timeout=None):
            stub.calls.append(("exec", command))
            return types.SimpleNamespace(success=True)

        stub.snapshot = _snapshot
        stub.exec = _exec
        stub.delete = lambda: stub.calls.append(("delete",))
        snap = DeclarativeSnapshot(
            name="t", image="img", workdir="/w", api_token="token"
        )
        snap.file("/w/req.txt", "text").copy(source, "dst").run("echo hi")

        with patch.object(Sandbox, "create", return_value=stub):
            built = snap.build("snap")

        self.assertEqual(
            fs.calls,
            [
                ("mkdir", "/w"),
                ("write_file", "/w/req.txt", "text", "utf-8"),
                ("sync", source, "dst"),
            ],
        )
        self.assertEqual(
            built.operations,
            [
                "set_workdir: /w",
                "create_file: /w/req.txt",
                f"copy: {source} -> dst",
                "run: echo hi",
            ],
        )
        self.assertEqual(
            stub.calls,
            [("exec", "echo hi"), ("snapshot", "snap"), ("delete",)],
        )

    def test_build_failed_command_raises(self):
        fs = _FakeFS(True)
        stub = types.SimpleNamespace(filesystem=fs, calls=[])

        def _exec(command, timeout=None):
            return types.SimpleNamespace(success=False, stdout="out", stderr="boom")

        stub.exec = _exec
        stub.snapshot = lambda **kw: types.SimpleNamespace(operations=None)
        stub.delete = lambda: None
        snap = DeclarativeSnapshot(name="t", image="img", api_token="token")
        snap.run("false")

        with patch.object(Sandbox, "create", return_value=stub):
            with self.assertRaises(SandboxError) as cm:
                snap.build("snap")

        self.assertIn("Command failed: false", str(cm.exception))

    def test_single_file_uploads_on_legacy_too(self):
        # upload_file carries its own legacy fallback; no probe needed.
        src = os.path.join(self.base, "one.txt")
        with open(src, "w") as f:
            f.write("text")
        fs = self._fs(new_routes=False)

        self.snap._copy(src, "dst/one.txt")

        self.assertEqual(
            fs.calls,
            [("upload_file", src, "dst/one.txt")],
        )


if __name__ == "__main__":
    unittest.main()
