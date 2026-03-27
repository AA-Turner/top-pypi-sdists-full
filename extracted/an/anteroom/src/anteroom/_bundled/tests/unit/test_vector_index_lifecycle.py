"""Tests for VectorIndex and VectorIndexManager lifecycle (#1021)."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from anteroom.services.vector_index import (
    VectorIndex,
    VectorIndexManager,
    _string_key_to_int,
    _validate_embedding,
)

# ---------------------------------------------------------------------------
# Embedding validation
# ---------------------------------------------------------------------------


class TestValidateEmbedding:
    def test_valid_embedding(self) -> None:
        _validate_embedding([0.1, 0.2, 0.3])

    def test_empty_embedding_raises(self) -> None:
        with pytest.raises(ValueError, match="1-"):
            _validate_embedding([])

    def test_oversized_embedding_raises(self) -> None:
        with pytest.raises(ValueError, match="1-"):
            _validate_embedding([0.0] * 5000)

    def test_nan_raises(self) -> None:
        with pytest.raises(ValueError, match="not a finite"):
            _validate_embedding([1.0, float("nan"), 0.5])

    def test_inf_raises(self) -> None:
        with pytest.raises(ValueError, match="not a finite"):
            _validate_embedding([1.0, float("inf")])

    def test_wrong_dimensions_raises(self) -> None:
        with pytest.raises(ValueError, match="expected 3"):
            _validate_embedding([0.1, 0.2], dimensions=3)


# ---------------------------------------------------------------------------
# String key to int mapping
# ---------------------------------------------------------------------------


class TestStringKeyToInt:
    def test_deterministic(self) -> None:
        key = "abc-123-def"
        assert _string_key_to_int(key) == _string_key_to_int(key)

    def test_positive(self) -> None:
        assert _string_key_to_int("test-key") > 0

    def test_different_keys_different_ints(self) -> None:
        a = _string_key_to_int("key-a")
        b = _string_key_to_int("key-b")
        assert a != b


# ---------------------------------------------------------------------------
# VectorIndex (mocking usearch)
# ---------------------------------------------------------------------------


class TestVectorIndex:
    @pytest.fixture
    def mock_usearch(self) -> Any:
        with patch("anteroom.services.vector_index.has_vector_support", return_value=True):
            mock_index_cls = MagicMock()
            mock_index_instance = MagicMock()
            mock_index_instance.ndim = 384
            mock_index_instance.__contains__ = lambda self, k: False
            mock_index_instance.__len__ = lambda self: 0
            mock_index_cls.return_value = mock_index_instance
            mock_index_cls.restore.return_value = None

            with patch("anteroom.services.vector_index.Index", mock_index_cls, create=True):
                # Need to patch in the usearch.index module
                with patch.dict("sys.modules", {"usearch": MagicMock(), "usearch.index": MagicMock()}):
                    with patch("anteroom.services.vector_index.Index", mock_index_cls):
                        yield mock_index_cls, mock_index_instance

    def test_new_index_created_when_no_file(self, tmp_path: Path, mock_usearch: Any) -> None:
        cls, inst = mock_usearch
        idx = VectorIndex(tmp_path / "test.usearch", dimensions=384)
        assert idx.dimensions == 384

    def test_restore_returns_none_creates_new(self, tmp_path: Path, mock_usearch: Any) -> None:
        cls, inst = mock_usearch
        cls.restore.return_value = None
        path = tmp_path / "test.usearch"
        path.write_bytes(b"fake")
        idx = VectorIndex(path, dimensions=384)
        assert idx.dimensions == 384

    def test_restore_wrong_ndim_rebuilds(self, tmp_path: Path, mock_usearch: Any) -> None:
        cls, inst = mock_usearch
        wrong_index = MagicMock()
        wrong_index.ndim = 768
        cls.restore.return_value = wrong_index
        path = tmp_path / "test.usearch"
        path.write_bytes(b"fake")
        idx = VectorIndex(path, dimensions=384)
        assert idx.dimensions == 384

    def test_invalid_dimensions_raises(self, tmp_path: Path) -> None:
        with pytest.raises(ValueError, match="Invalid embedding dimensions"):
            VectorIndex(tmp_path / "test.usearch", dimensions=0)

    def test_invalid_dimensions_too_large(self, tmp_path: Path) -> None:
        with pytest.raises(ValueError, match="Invalid embedding dimensions"):
            VectorIndex(tmp_path / "test.usearch", dimensions=5000)

    def test_register_key(self, tmp_path: Path, mock_usearch: Any) -> None:
        cls, inst = mock_usearch
        idx = VectorIndex(tmp_path / "test.usearch", dimensions=384)
        idx.register_key("my-uuid")
        int_key = _string_key_to_int("my-uuid")
        assert idx._int_to_str[int_key] == "my-uuid"

    def test_rebuild_key_map(self, tmp_path: Path, mock_usearch: Any) -> None:
        cls, inst = mock_usearch
        idx = VectorIndex(tmp_path / "test.usearch", dimensions=384)
        pairs = [("key-1", "conv-1"), ("key-2", "conv-2")]
        idx.rebuild_key_map(pairs)
        assert len(idx._int_to_str) == 2

    def test_save_delegates(self, tmp_path: Path, mock_usearch: Any) -> None:
        cls, inst = mock_usearch
        idx = VectorIndex(tmp_path / "test.usearch", dimensions=384)
        idx.save()
        # The internal _index should have save() called
        idx._index.save.assert_called_once()


# ---------------------------------------------------------------------------
# VectorIndexManager
# ---------------------------------------------------------------------------


class TestVectorIndexManager:
    def test_disabled_when_no_usearch(self, tmp_path: Path) -> None:
        with patch("anteroom.services.vector_index.has_vector_support", return_value=False):
            mgr = VectorIndexManager(tmp_path)
        assert mgr.enabled is False
        assert mgr.messages is None
        assert mgr.source_chunks is None

    def test_save_all_no_op_when_disabled(self, tmp_path: Path) -> None:
        with patch("anteroom.services.vector_index.has_vector_support", return_value=False):
            mgr = VectorIndexManager(tmp_path)
        mgr.save_all()

    def test_rebuild_no_op_when_disabled(self, tmp_path: Path) -> None:
        with patch("anteroom.services.vector_index.has_vector_support", return_value=False):
            mgr = VectorIndexManager(tmp_path)
        mock_db = MagicMock()
        mgr.rebuild_from_db(mock_db)
        mock_db.execute_fetchall.assert_not_called()
