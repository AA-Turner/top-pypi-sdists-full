# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Local end-to-end chain (no Ray/Azure): seed -> download -> normalize -> phash.

Exercises the actual stage row-functions in sequence over a local object store, to
prove the benchmark's data path is connected: an object uploaded by `upload-images`
is fetched by `download-images` (reading the reference-table locator columns), the
downloaded bytes normalize and pHash, and — the property the whole benchmark rests on
— two driver rows that reference the SAME image produce the SAME pHash, so the dedupe
stage will detect reused reads as duplicates. The Geneva backfill *plumbing* (which
column each stage adds/reads) is covered by the per-stage tests + the
schema-compatibility checks in test_download_images; this test covers the per-row
transform chain.
"""

from __future__ import annotations

import io
from typing import Any

import pytest

from loadtest.azure_scale_bench import (
    download_images,
    normalize,
    phash,
    upload_images,
)
from loadtest.azure_scale_bench.benchmark_env import BenchConfig
from loadtest.azure_scale_bench.object_writer import LocalFileReader, LocalFileWriter


def _cfg(**overrides: Any) -> BenchConfig:
    base: dict[str, Any] = {
        "seed_run_id": "e2e",
        "accounts": ("acctA",),
        "loose_container": "cont",
        "base_prefix": "pre",
        "prefix_count": 8,
        "image_format": "png",
        "object_count": 32,
    }
    base.update(overrides)
    return BenchConfig(**base)


def _params() -> upload_images._UploadParams:
    cfg = _cfg()
    assert cfg.seed_run_id is not None
    return upload_images._params(cfg, upload_images._seed_run_salt(cfg.seed_run_id))


def _seed_population(writer: LocalFileWriter, params: Any, seed_count: int) -> None:
    """Upload the full seed population to the local object store."""
    for image_id in range(seed_count):
        row = upload_images.upload_one(image_id, lambda _a: writer, params)
        assert row["ok"] is True


def _locator(image_id: int) -> dict[str, Any]:
    """Derive the reference-table locator columns for ``image_id``.

    Matches what ``build-ref-table`` writes per row, so a direct-ref download of these
    columns fetches exactly the object the upload seeded.
    """
    params = _params()
    prefix_id = upload_images.prefix_id_for(image_id, params)
    object_key = upload_images.object_key_for(image_id, prefix_id, params)
    return {
        "url": upload_images.url_for(object_key, params),
        "account": upload_images.account_for(image_id, params),
        "container": params.container,
        "object_key": object_key,
    }


def test_seed_download_normalize_phash_chain(tmp_path: Any) -> None:
    params = _params()
    seed_count = 32
    writer = LocalFileWriter(tmp_path, "cont")
    _seed_population(writer, params, seed_count)

    def _reader(_account: str, container: str) -> LocalFileReader:
        return LocalFileReader(tmp_path, container)

    # Walk several driver rows through the full per-row chain. Multiple driver rows
    # reference the same image_id (reuse_factor 3), exactly like the shuffled ref table.
    seen_phash: dict[int, list[int]] = {}
    for row_index in range(seed_count * 3):
        image_id = row_index % seed_count
        loc = _locator(image_id)
        dl = download_images.download_ref_one(
            row_index,
            image_id,
            loc["url"],
            loc["account"],
            loc["container"],
            loc["object_key"],
            _reader,
        )
        assert dl["ok"] is True
        assert dl["error"] == ""
        assert dl["image_bytes"] is not None

        norm_bytes, norm_err = normalize.normalize_image(dl["image_bytes"], size=32)
        assert norm_err is None
        assert norm_bytes is not None
        with io.BytesIO(norm_bytes) as buf:
            from PIL import Image

            with Image.open(buf) as img:
                assert img.size == (32, 32)

        ph = phash.compute_phash(norm_bytes)
        assert ph is not None
        assert len(ph) == 8

        # The dedupe signal: the same image (reached via different driver rows) must
        # hash identically, so reused reads cluster as duplicates.
        sid = dl["seed_image_id"]
        if sid in seen_phash:
            assert ph == seen_phash[sid], "reused read produced a different pHash"
        else:
            seen_phash[sid] = ph

    # Every seed image was visited (each 3x), so the duplicate assertion above fired.
    assert len(seen_phash) == seed_count


def test_distinct_seeds_generally_differ(tmp_path: Any) -> None:
    # Sanity: different seed images do not all collapse to one pHash (the synthetic
    # images carry real low-frequency structure — gradients, shapes, lines — not
    # white noise), so dedupe is detecting reuse, not arbitrary hash residue.
    params = _params()
    seed_count = 16
    writer = LocalFileWriter(tmp_path, "cont")
    _seed_population(writer, params, seed_count)

    def _reader(_account: str, container: str) -> LocalFileReader:
        return LocalFileReader(tmp_path, container)

    by_seed: dict[int, list[int]] = {}
    for row_index in range(200):
        image_id = row_index % seed_count
        loc = _locator(image_id)
        dl = download_images.download_ref_one(
            row_index,
            image_id,
            loc["url"],
            loc["account"],
            loc["container"],
            loc["object_key"],
            _reader,
        )
        norm_bytes, _ = normalize.normalize_image(dl["image_bytes"], size=32)
        ph = phash.compute_phash(norm_bytes)
        assert ph is not None
        by_seed.setdefault(dl["seed_image_id"], ph)

    distinct_hashes = {tuple(h) for h in by_seed.values()}
    # Not all seeds share one hash — the structured images spread across distinct
    # pHashes (at least a few across 16 seeds).
    assert len(distinct_hashes) >= 3


if __name__ == "__main__":  # pragma: no cover - convenience for manual runs
    raise SystemExit(pytest.main([__file__, "-v"]))
