"""Tests for _documents_dir_from_known_folder."""

import ctypes
from pathlib import Path

from agentic_devtools.cli.setup.shell_profile import _documents_dir_from_known_folder


class _FakeModule:
    """Minimal stand-in for ``ctypes.windll.shell32`` / ``ctypes.windll.ole32``."""

    def __init__(self, func):
        self._func = func

    def __getattr__(self, name):
        return self._func


class _FakeWindll:
    """Minimal stand-in for ``ctypes.windll``."""

    def __init__(self, shgetknownfolderpath):
        self.shell32 = _FakeModule(shgetknownfolderpath)
        self.freed = []
        self.ole32 = _FakeModule(self.freed.append)


class TestDocumentsDirFromKnownFolder:
    """Tests for _documents_dir_from_known_folder."""

    def test_returns_none_when_windll_unavailable(self, monkeypatch):
        """Returns None on platforms without ``ctypes.windll`` (non-Windows)."""
        monkeypatch.delattr(ctypes, "windll", raising=False)
        assert _documents_dir_from_known_folder() is None

    def test_returns_documents_path_from_api(self, monkeypatch):
        """Returns the path reported by SHGetKnownFolderPath."""
        expected = r"C:\Users\u\OneDrive - Org\Dokumente"

        def shgetknownfolderpath(folder_id, flags, token, buffer_ref):
            buffer_ref._obj.value = expected
            return 0

        fake = _FakeWindll(shgetknownfolderpath)
        monkeypatch.setattr(ctypes, "windll", fake, raising=False)

        assert _documents_dir_from_known_folder() == Path(expected)
        assert len(fake.freed) == 1

    def test_returns_none_on_api_failure(self, monkeypatch):
        """Returns None when SHGetKnownFolderPath reports a failure HRESULT."""
        fake = _FakeWindll(lambda *args: 1)
        monkeypatch.setattr(ctypes, "windll", fake, raising=False)

        assert _documents_dir_from_known_folder() is None
        assert len(fake.freed) == 1

    def test_returns_none_when_buffer_empty(self, monkeypatch):
        """Returns None when the API succeeds but writes no path."""
        fake = _FakeWindll(lambda *args: 0)
        monkeypatch.setattr(ctypes, "windll", fake, raising=False)

        assert _documents_dir_from_known_folder() is None
        assert len(fake.freed) == 1

    def test_returns_none_when_api_raises(self, monkeypatch):
        """Returns None when the API call raises."""

        def boom(*args):
            raise OSError("boom")

        monkeypatch.setattr(ctypes, "windll", _FakeWindll(boom), raising=False)
        assert _documents_dir_from_known_folder() is None
