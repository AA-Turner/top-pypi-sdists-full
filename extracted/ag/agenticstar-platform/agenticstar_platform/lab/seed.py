"""lab の schema / bucket / collection / synthetic 文書の投入（冪等、molt#1610）。

run_lab の phase [3/5] から呼ばれる。単体でも
`python -m agenticstar_platform.lab.seed` で実行可能。
credential は lab_config の非本番固定値のみを使う。
"""

from __future__ import annotations

import asyncio
import uuid

from . import lab_config
from .offline_embedding import OfflineEmbeddingGenerator


class SeedVersionMismatch(RuntimeError):
    """適用済み seed と lab_config の version が食い違っている（reset が必要）。"""


def _ensure(result: dict, step: str) -> dict:
    """execute_query 系の失敗 result（success=False）を例外へ昇格する。"""
    if not result.get("success"):
        raise RuntimeError(f"seed step failed ({step}): {result.get('error')}")
    return result


async def apply() -> dict:
    """schema / bucket / collection / 文書 / version meta を冪等に適用する。

    version meta の書き込みは **最後**（bucket / Qdrant まで成功した後）に行う。
    途中失敗した部分適用状態で doctor が all-green を報告しないようにするため。

    Returns:
        {"documents": int, "bucket": str, "collection": str}

    Raises:
        SeedVersionMismatch: 適用済み version が一致しない場合（自動 migrate はしない）
    """
    from agenticstar_platform.db import DataAccess, PostgreSQLManager
    from agenticstar_platform.rag import QdrantManager
    from agenticstar_platform.storage import S3StorageClient

    expected = {
        "seed_version": lab_config.SEED_VERSION,
        "embedding_version": lab_config.EMBEDDING_VERSION,
    }

    # --- PostgreSQL: schema + version 検査 ---
    manager = PostgreSQLManager(lab_config.postgres_config())
    da = DataAccess(manager)
    await da.initialize()
    try:
        _ensure(await da.execute_query(
            f"""
            CREATE TABLE IF NOT EXISTS {lab_config.META_TABLE} (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
            """
        ), "create lab_meta")
        _ensure(await da.execute_query(
            f"""
            CREATE TABLE IF NOT EXISTS {lab_config.RESULTS_TABLE} (
                id BIGSERIAL PRIMARY KEY,
                execution_id TEXT NOT NULL,
                query TEXT NOT NULL,
                retrieved_document_id TEXT NOT NULL,
                artifact_object TEXT NOT NULL,
                outcome TEXT NOT NULL,
                created_at TIMESTAMPTZ NOT NULL DEFAULT now()
            )
            """
        ), "create lab_results")

        applied = _ensure(await da.execute_query(
            f"SELECT key, value FROM {lab_config.META_TABLE}"
        ), "read lab_meta")
        meta = {r["key"]: r["value"] for r in (applied.get("data") or [])}
        if meta and any(meta.get(k) != v for k, v in expected.items()):
            raise SeedVersionMismatch(
                f"applied={meta} expected={expected}. "
                "python -m agenticstar_platform.lab --reset で破棄してから再実行してください。"
            )

        # --- S3 互換 storage: bucket ---
        storage = S3StorageClient(lab_config.s3_config())
        try:
            if not await storage.ensure_bucket_exists():
                raise RuntimeError(
                    f"bucket '{lab_config.S3_BUCKET}' を作成/確認できませんでした"
                )
        finally:
            await storage.close()

        # --- Qdrant: collection + synthetic 文書（upsert は冪等） ---
        embedding = OfflineEmbeddingGenerator(
            dimensions=lab_config.EMBEDDING_DIMENSIONS,
            version=lab_config.EMBEDDING_VERSION,
        )
        # Qdrant の point ID は UUID/整数のみ有効なので、文書 id から決定論的 UUID を
        # 生成する（冪等な upsert を保つ）。人間可読の id は payload.document_id に、
        # 本文は payload.content に持つ（batch_upsert は metadata のみ payload に載せる）
        async with QdrantManager(lab_config.qdrant_config(), embedding) as qdrant:
            result = await qdrant.batch_upsert(
                [
                    {
                        "id": str(uuid.uuid5(uuid.NAMESPACE_URL, f"agenticstar-lab:{doc['id']}")),
                        "content": doc["content"],
                        "metadata": {
                            "title": doc["title"],
                            "content": doc["content"],
                            "content_type": "lab_document",
                            "document_id": doc["id"],
                        },
                    }
                    for doc in lab_config.SYNTHETIC_DOCUMENTS
                ]
            )
            if not result.get("success"):
                raise RuntimeError(f"Qdrant batch_upsert failed: {result.get('error')}")

        # --- version meta（全 step 成功後に書く） ---
        for key, value in expected.items():
            _ensure(await da.execute_query(
                f"INSERT INTO {lab_config.META_TABLE} (key, value) VALUES ($1, $2) "
                "ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value",
                (key, value),
            ), f"write meta {key}")
    finally:
        await da.close()

    return {
        "documents": len(lab_config.SYNTHETIC_DOCUMENTS),
        "bucket": lab_config.S3_BUCKET,
        "collection": lab_config.QDRANT_COLLECTION,
    }


if __name__ == "__main__":
    summary = asyncio.run(apply())
    print(f"seed applied: {summary}")
