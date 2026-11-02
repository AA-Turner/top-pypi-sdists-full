from dataclasses import FrozenInstanceError

import pytest

from agentic_devtools.ai_providers.promotion import PromotionManifest


def test_promotion_manifest_is_frozen() -> None:
    manifest = PromotionManifest(
        round_id=1,
        meta_path="meta-canonical.json",
        body_path="body-canonical.md",
        meta_sha256="a" * 64,
        body_sha256="b" * 64,
        status="accepted",
        verification_timestamp="2026-08-20T00:00:00Z",
    )

    assert manifest.round_id == 1

    with pytest.raises(FrozenInstanceError):
        manifest.status = "rejected"  # type: ignore[misc]
