"""Durable file URLs replace the retired signed-URL wire contract."""

from __future__ import annotations

from typing import Any

import pytest

import matrx_files
from matrx_files.asset_builder import build_asset_from_master
from matrx_files.asset_envelope import AssetVariant, FileRef
from matrx_files.cloud_sync.sync_engine import SyncEngine

MASTER_ID = "11111111-1111-4111-8111-111111111111"
VARIANT_ID = "22222222-2222-4222-8222-222222222222"
OWNER_ID = "33333333-3333-4333-8333-333333333333"
PUBLIC_BASE = "https://files.example.test"


def _record(file_id: str, path: str) -> dict[str, Any]:
    return {
        "id": file_id,
        "owner_id": OWNER_ID,
        "file_path": path,
        "file_name": path.rsplit("/", 1)[-1],
        "storage_uri": f"s3://bucket/{path}",
        "canonical_storage_uri": f"s3://bucket/{path}",
        "mime_type": "image/png",
        "size_bytes": 509,
        "published_to_web": False,
        "shown_to": "only_me",
        "metadata": {},
    }


@pytest.fixture(autouse=True)
def _durable_url_base() -> None:
    matrx_files.configure(files_public_base_url=PUBLIC_BASE)


@pytest.mark.asyncio
async def test_private_file_builds_only_durable_file_id_urls() -> None:
    engine = object.__new__(SyncEngine)
    urls = await engine.build_urls_for_record_async(_record(MASTER_ID, "u/pics/rotated.png"))
    assert urls == {
        "url": f"{PUBLIC_BASE}/files/{MASTER_ID}/download?inline=1",
        "cdn_url": None,
        "download_url": f"{PUBLIC_BASE}/files/{MASTER_ID}/download",
    }
    assert "signed_url" not in urls
    assert "signed_url_expires_at" not in urls


@pytest.mark.asyncio
async def test_soft_deleted_file_has_no_urls() -> None:
    engine = object.__new__(SyncEngine)
    urls = await engine.build_urls_for_record_async(
        {**_record(MASTER_ID, "u/x.png"), "deleted_at": "2026-01-01"}
    )
    assert urls == {"url": None, "cdn_url": None, "download_url": None}


class _FakeDB:
    def __init__(self, variants: list[dict[str, Any]]) -> None:
        self._variants = variants

    async def list_variants_by_master_async(self, master_file_id: str) -> list[dict]:
        assert master_file_id == MASTER_ID
        return self._variants


class _FakeSyncEngine:
    build_urls_for_record = SyncEngine.build_urls_for_record
    build_urls_for_record_async = SyncEngine.build_urls_for_record_async

    def __init__(self, variants: list[dict[str, Any]]) -> None:
        self.db = _FakeDB(variants)


class _FakeFileManager:
    def __init__(self, variants: list[dict[str, Any]]) -> None:
        self.sync_engine = _FakeSyncEngine(variants)


@pytest.mark.asyncio
async def test_asset_envelope_variants_carry_durable_urls_only() -> None:
    variant_row = {
        **_record(VARIANT_ID, "u/pics/v/thumbnail_url.png"),
        "metadata": {"derived_from": MASTER_ID, "variant_key": "thumbnail_url"},
    }
    asset = await build_asset_from_master(
        _FakeFileManager([variant_row]), _record(MASTER_ID, "u/pics/rotated.png")
    )
    assert set(asset.variants) == {"original", "thumbnail_url"}
    for variant in asset.variants.values():
        assert variant.url == f"{PUBLIC_BASE}/files/{variant.file_id}/download?inline=1"
        assert variant.download_url == f"{PUBLIC_BASE}/files/{variant.file_id}/download"
        assert "signed_url" not in type(variant).model_fields
        assert "signed_url_expires_at" not in type(variant).model_fields


@pytest.mark.asyncio
async def test_heic_asset_uses_existing_browser_safe_derivative_as_primary() -> None:
    variant_row = {
        **_record(VARIANT_ID, f"u/pics/v/{MASTER_ID}/gemini3_high.jpg"),
        "mime_type": "image/jpeg",
        "size_bytes": 4096,
        "metadata": {
            "derived_from": MASTER_ID,
            "variant_key": "gemini3_high",
            "variant_family": "vision",
        },
    }
    master = {
        **_record(MASTER_ID, "u/pics/Product.HEIC"),
        "mime_type": "image/heic",
    }

    asset = await build_asset_from_master(_FakeFileManager([variant_row]), master)

    assert set(asset.variants) == {"original", "gemini3_high"}
    assert asset.primary_key == "gemini3_high"
    assert asset.primary_url == asset.variants["gemini3_high"].url


@pytest.mark.parametrize("model_cls", [AssetVariant, FileRef])
def test_historical_signed_fields_are_ignored(model_cls: type) -> None:
    fields: dict[str, Any] = {
        "file_id": MASTER_ID,
        "signed_url": "https://bucket.example/object?X-Amz-Signature=old",
        "signed_url_expires_at": 1755703600000,
    }
    if model_cls is AssetVariant:
        fields |= {"key": "original", "file_path": "u/pics/rotated.png"}
    dumped = model_cls(**fields).model_dump()
    assert "signed_url" not in dumped
    assert "signed_url_expires_at" not in dumped


def test_durable_inline_url_uses_configured_public_base() -> None:
    from matrx_files.cloud_sync import render_urls

    assert render_urls.files_public_base_url() == PUBLIC_BASE
    assert render_urls.durable_inline_url("abc") == f"{PUBLIC_BASE}/files/abc/download?inline=1"
    assert render_urls.durable_download_url("abc") == f"{PUBLIC_BASE}/files/abc/download"


def test_file_ref_carries_exactly_the_durable_contract_fields() -> None:
    assert set(FileRef.model_fields) == {
        "file_id",
        "published_to_web",
        "shown_to",
        "visibility",
        "file_name",
        "mime_type",
        "size_bytes",
        "url",
        "cdn_url",
        "download_url",
        "thumbnail_url",
    }


@pytest.mark.parametrize("model_cls", [AssetVariant, FileRef])
def test_permanent_cdn_url_remains_supported(model_cls: type) -> None:
    fields: dict[str, Any] = {
        "file_id": MASTER_ID,
        "cdn_url": "https://cdn.matrx/x.png",
    }
    if model_cls is AssetVariant:
        fields |= {"key": "original", "file_path": "u/pics/rotated.png"}
    assert model_cls(**fields).cdn_url == "https://cdn.matrx/x.png"
