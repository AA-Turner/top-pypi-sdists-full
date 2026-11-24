"""A SNAPSHOT'S PICTURE REFERENCE NAMES THE EXACT BYTES IT STANDS FOR (CGU-10 AND-V IMG17, finding N3).

The snapshot now references a stored picture as ``{file_id, vision_class}`` (9c5b2d93346). Since AND-IMG17 #1 a
replaced master renders a NEW variant (``{key}.v{N}.{ext}``) and keeps the old one, so ``file_id + class`` names a
different picture after the master is replaced: a replay renders the new bytes, and the reference carries no
version (nor, unlike the blob-store branch's ``file_sha256``, the decoded bytes' hash) to find the old ones. The
reference must name what was sent: the master version it was rendered from.

Enabled with the fix (AND-IMG18): the resolver records metadata.master_version, the media pass carries it, the reference names it.
"""

from __future__ import annotations

import base64


from matrx_ai.providers.snapshot_redactors import known_media_blobs


def test_the_reference_carries_the_master_version() -> None:
    data = base64.b64encode(b"\xff\xd8\xff" + b"x" * 1000).decode()
    tree = {"content": [{"type": "image", "base64_data": data, "file_id": "f1", "vision_class": "anthropic_sonnet_default",
                         "metadata": {"master_version": 3}}]}
    (ref,) = known_media_blobs(tree).values()
    assert ref.get("master_version") in (3, "3"), ref


def test_the_marker_names_the_version_and_the_resolver_records_it() -> None:
    from matrx_files.cloud_sync._media_resolution import _carry_master_version
    from matrx_files.cloud_sync.media_ref import MediaRef

    ref = MediaRef(file_id="f1", metadata={"file_name": "x.jpg"})
    _carry_master_version(ref, 3)
    assert ref.metadata == {"file_name": "x.jpg", "master_version": 3}

    from matrx_ai.providers.unified_client import _carry_proxy_master_version
    from matrx_ai.config.media_config import ImageContent

    item = ImageContent(file_id="f1", mime_type="image/jpeg")
    _carry_proxy_master_version(item, ref)
    assert item.metadata.get("master_version") == 3
