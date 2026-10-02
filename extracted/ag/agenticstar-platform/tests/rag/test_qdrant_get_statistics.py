"""Refs #2008: qdrant-client >=1.16.0 で CollectionInfo.vectors_count が削除されたことへの互換対応を検証。

qdrant_client 未インストール環境では skip する。
"""

from enum import Enum

import pytest

pytest.importorskip("qdrant_client")

from agenticstar_platform.rag.qdrant_manager import QdrantManager  # noqa: E402


class _Status(Enum):
    green = "green"


class _CollectionInfoWithVectorsCount:
    """qdrant-client <1.16.0 相当。vectors_count を持つ。"""

    def __init__(self, points_count: int, vectors_count: int):
        self.points_count = points_count
        self.vectors_count = vectors_count
        self.status = _Status.green


class _CollectionInfoWithoutVectorsCount:
    """qdrant-client >=1.16.0 相当。vectors_count 属性を持たない。"""

    def __init__(self, points_count: int):
        self.points_count = points_count
        self.status = _Status.green


class _FakeClient:
    def __init__(self, collection_info, scroll_points):
        self._collection_info = collection_info
        self._scroll_points = scroll_points

    def get_collection(self, collection_name):
        return self._collection_info

    def scroll(self, *, collection_name, limit, with_payload, with_vectors):
        return (self._scroll_points, None)


class _Point:
    def __init__(self, content_type):
        self.payload = {"content_type": content_type}


def _make_manager(collection_info, scroll_points=None):
    """__init__ をバイパスして最小属性のみ差し込む(実 QdrantClient を作らないため)。"""
    mgr = QdrantManager.__new__(QdrantManager)
    mgr._initialized = True
    mgr.collection_name = "dummy_collection"
    mgr.client = _FakeClient(collection_info, scroll_points or [])
    return mgr


class TestGetStatisticsVectorsCountCompat:
    """CollectionInfo.vectors_count の有無で挙動が変わらないこと。"""

    async def test_success_when_vectors_count_present(self):
        # qdrant-client <1.16.0 相当
        info = _CollectionInfoWithVectorsCount(points_count=42, vectors_count=40)
        mgr = _make_manager(info, scroll_points=[_Point("text"), _Point("text"), _Point("image")])

        result = await mgr.get_statistics()

        assert result["success"] is True
        data = result["data"]
        assert data["total_objects"] == 42
        # vectors_count は本来値をそのまま返す
        assert data["vectors_count"] == 40
        assert data["content_type_breakdown"] == {"text": 2, "image": 1}
        assert data["collection_name"] == "dummy_collection"
        assert data["status"] == "green"

    async def test_success_when_vectors_count_missing(self):
        # qdrant-client >=1.16.0 相当。以前は AttributeError で失敗していたケース
        info = _CollectionInfoWithoutVectorsCount(points_count=42)
        mgr = _make_manager(info, scroll_points=[_Point("text")])

        result = await mgr.get_statistics()

        assert result["success"] is True
        data = result["data"]
        assert data["total_objects"] == 42
        # vectors_count が無い場合は points_count にフォールバック
        assert data["vectors_count"] == 42
        assert data["content_type_breakdown"] == {"text": 1}
        assert data["status"] == "green"

    async def test_no_longer_raises_attribute_error_on_1_16_plus(self):
        # Regression guard: この修正前は QDRANT_STATS_ERROR (AttributeError) を返していた
        info = _CollectionInfoWithoutVectorsCount(points_count=0)
        mgr = _make_manager(info, scroll_points=[])

        result = await mgr.get_statistics()

        assert result["success"] is True
        assert "error" not in result or result.get("error") is None
