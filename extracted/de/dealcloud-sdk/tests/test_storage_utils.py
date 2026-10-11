"""Unit tests for dealcloud_sdk.storage.utils."""

from pathlib import Path

from dealcloud_sdk.storage.utils import (
    FsspecStreamingStorage,
    LocalStorage,
    StorageBackend,
    StreamingStorageBackend,
)


class TestLocalStorage:
    def test_write_creates_file_and_returns_absolute_path(self, tmp_path):
        store = LocalStorage(tmp_path)
        out = store.write("dir/a.txt", b"payload", "text/plain")
        assert Path(out).is_file()
        assert Path(out).read_bytes() == b"payload"
        assert str(Path(out).resolve()) == out

    def test_exists(self, tmp_path):
        store = LocalStorage(tmp_path)
        assert store.exists("missing.bin") is False
        store.write("present.bin", b"\x00", "application/octet-stream")
        assert store.exists("present.bin") is True

    def test_open_write_streaming(self, tmp_path):
        store = LocalStorage(tmp_path)
        with store.open_write("stream/out.dat", content_type="application/octet-stream") as buf:
            buf.write(b"chunk")
        assert store.exists("stream/out.dat")
        assert (Path(tmp_path) / "stream" / "out.dat").read_bytes() == b"chunk"

    def test_full_path_joins_root(self, tmp_path):
        store = LocalStorage(tmp_path)
        rel = "exports/backup.zip"
        expected = str(Path(tmp_path).resolve() / rel)
        assert store.full_path(rel) == expected

    def test_isinstance_storage_backend(self, tmp_path):
        store = LocalStorage(tmp_path)
        assert isinstance(store, StorageBackend)

    def test_isinstance_streaming_storage_backend(self, tmp_path):
        store = LocalStorage(tmp_path)
        assert isinstance(store, StreamingStorageBackend)


class TestFsspecStreamingStorage:
    def test_init_strips_trailing_slash_from_base_uri(self, tmp_path):
        root = tmp_path / "bucket"
        root.mkdir()
        uri = root.as_uri() + "///"
        store = FsspecStreamingStorage(uri)
        assert store._base == root.as_uri().rstrip("/")

    def test_full_path_joins_relative_key(self, tmp_path):
        root = tmp_path / "data"
        root.mkdir()
        base = root.as_uri()
        store = FsspecStreamingStorage(base)
        assert store.full_path("a/b.bin") == f"{base}/a/b.bin"

    def test_full_path_strips_leading_slash_on_key(self, tmp_path):
        root = tmp_path / "data"
        root.mkdir()
        base = root.as_uri()
        store = FsspecStreamingStorage(base)
        assert store.full_path("/x/y.txt") == f"{base}/x/y.txt"

    def test_open_write_creates_nested_file(self, tmp_path):
        root = tmp_path / "out"
        root.mkdir()
        store = FsspecStreamingStorage(root.as_uri())
        with store.open_write("nested/dir/file.bin", content_type="application/octet-stream") as f:
            f.write(b"\x00\x01\x02")
        written = root / "nested" / "dir" / "file.bin"
        assert written.is_file()
        assert written.read_bytes() == b"\x00\x01\x02"

    def test_isinstance_streaming_storage_backend(self, tmp_path):
        root = tmp_path / "s"
        root.mkdir()
        store = FsspecStreamingStorage(root.as_uri())
        assert isinstance(store, StreamingStorageBackend)

    def test_open_write_passes_storage_options(self, tmp_path, monkeypatch):
        """Optional kwargs are forwarded to fsspec.open (verified via capture)."""
        root = tmp_path / "opts"
        root.mkdir()
        calls = []

        real_open = __import__("fsspec").open

        def capture_open(path, mode, **kwargs):
            calls.append((path, mode, kwargs))
            return real_open(path, mode, **kwargs)

        monkeypatch.setattr("dealcloud_sdk.storage.utils.fsspec.open", capture_open)
        store = FsspecStreamingStorage(root.as_uri(), auto_mkdir=True)
        with store.open_write("k.txt", content_type="text/plain") as f:
            f.write(b"z")
        assert len(calls) == 1
        assert calls[0][1] == "wb"
        assert calls[0][2].get("auto_mkdir") is True
