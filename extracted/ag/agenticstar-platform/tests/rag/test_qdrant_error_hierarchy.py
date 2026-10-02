"""Refs #1938: QdrantConfigError の VectorStoreError 階層取込と init 失敗ラップを検証。

qdrant_client 未インストール環境では skip する。
"""

import pytest

pytest.importorskip("qdrant_client")

from agenticstar_platform.rag.base import (  # noqa: E402
    VectorStoreError,
    VectorStoreConfigError,
    VectorStoreConnectionError,
)
from agenticstar_platform.rag.qdrant_manager import (  # noqa: E402
    QdrantConfigError,
    QdrantManager,
)


class TestQdrantConfigErrorHierarchy:
    """修正1: QdrantConfigError を VectorStoreError 階層に取り込む。"""

    def test_is_subclass_of_vectorstore_config_error(self):
        assert issubclass(QdrantConfigError, VectorStoreConfigError)

    def test_is_subclass_of_vectorstore_error(self):
        assert issubclass(QdrantConfigError, VectorStoreError)

    def test_instance_isinstance_of_hierarchy(self):
        err = QdrantConfigError("boom")
        assert isinstance(err, VectorStoreConfigError)
        assert isinstance(err, VectorStoreError)

    def test_catchable_as_vectorstore_config_error(self):
        with pytest.raises(VectorStoreConfigError):
            raise QdrantConfigError("mismatch")

    def test_catchable_as_vectorstore_error(self):
        with pytest.raises(VectorStoreError):
            raise QdrantConfigError("mismatch")

    def test_backward_compat_catchable_by_own_type(self):
        # 既存の except QdrantConfigError は引き続き機能する（下位互換）
        with pytest.raises(QdrantConfigError):
            raise QdrantConfigError("mismatch")


class TestInitializeFailureWrapping:
    """修正2: initialize() の init 失敗を VectorStoreConnectionError にラップ。"""

    def _manager_with_failing_client(self, exc: Exception) -> QdrantManager:
        # __init__ は実 QdrantClient を生成するため __new__ で回避し、
        # initialize() が参照する最小限の属性だけを差し込む。
        mgr = QdrantManager.__new__(QdrantManager)
        mgr._initialized = False
        mgr.collection_name = "dummy"

        class _FailingClient:
            def get_collections(self):
                raise exc

        mgr.client = _FailingClient()
        return mgr

    async def test_init_failure_wrapped_in_connection_error(self):
        mgr = self._manager_with_failing_client(RuntimeError("connection refused"))
        with pytest.raises(VectorStoreConnectionError):
            await mgr.initialize()

    async def test_init_failure_preserves_cause(self):
        original = RuntimeError("connection refused")
        mgr = self._manager_with_failing_client(original)
        try:
            await mgr.initialize()
        except VectorStoreConnectionError as ce:
            assert ce.__cause__ is original
            assert "connection refused" in str(ce.__cause__)
        else:
            pytest.fail("VectorStoreConnectionError が送出されなかった")

    async def test_wrapped_error_is_also_vectorstore_error(self):
        mgr = self._manager_with_failing_client(RuntimeError("x"))
        with pytest.raises(VectorStoreError):
            await mgr.initialize()

    async def test_already_typed_vectorstore_error_is_not_rewrapped(self):
        # config 系（VectorStoreConfigError）が init 中に発生した場合、
        # Connection へ二重ラップせず型を保ったまま伝播する
        original = VectorStoreConfigError("bad payload index schema")
        mgr = self._manager_with_failing_client(original)
        with pytest.raises(VectorStoreConfigError) as exc_info:
            await mgr.initialize()
        assert exc_info.value is original
        assert not isinstance(exc_info.value, VectorStoreConnectionError)


class TestInitializeIdempotency:
    """initialize() が collection 既存時にも payload index を ensure すること。

    以前は collection が既存だと index 作成を丸ごとスキップしていたため、
    index 作成が途中失敗→再初期化すると index 未作成のまま初期化完了扱いになった。
    """

    class _RecordingClient:
        def __init__(self, existing_collections):
            self._existing = existing_collections
            self.created_indices = []

        def get_collections(self):
            class _Col:
                def __init__(self, name):
                    self.name = name

            class _Resp:
                pass

            resp = _Resp()
            resp.collections = [_Col(n) for n in self._existing]
            return resp

        def create_payload_index(self, collection_name, field_name, field_schema):
            self.created_indices.append(field_name)

    def _manager_with_existing_collection(self):
        from types import SimpleNamespace

        mgr = QdrantManager.__new__(QdrantManager)
        mgr._initialized = False
        mgr.collection_name = "existing_col"
        mgr.config = SimpleNamespace(
            payload_indexes=[
                SimpleNamespace(field_name="content_type", field_schema="keyword"),
                SimpleNamespace(field_name="created_at", field_schema="integer"),
            ]
        )
        mgr.client = self._RecordingClient(existing_collections=["existing_col"])
        return mgr

    async def test_payload_indices_created_even_when_collection_exists(self):
        mgr = self._manager_with_existing_collection()
        await mgr.initialize()
        assert mgr._initialized is True
        # collection 既存でも全 payload index が ensure される
        assert mgr.client.created_indices == ["content_type", "created_at"]
