"""The media nodes declare the platform Shapes their outputs actually are.

A node whose only kind is the auto-derived `action_io_*` contract slug is
invisible to the Shape system — no renderer, no reuse, and the runtime UI
shows a JSON blob. These five declare curated kinds seeded from their OWN
output models (matrx-frontend `migrations/content_ir_seed_media_io_kinds.sql`).

This pins the declaration so a rename or a silent drop is caught here rather
than as a missing renderer in the UI. It does NOT prove the live registry
still holds the slug — that is the DB's half, verified at seed time.
"""

from __future__ import annotations

import pytest
from matrx_graph.executor.registry import default_registry

# node type -> (declared kind, the model the kind's schema was derived from)
EXPECTED = {
    "ai.generate_image": ("generated_image_set", "GenerateImageOutput"),
    "ai.generate_video": ("generated_video_set", "GenerateVideoOutput"),
    "ai.edit_video": ("generated_video_set", "GenerateVideoOutput"),
    "ai.extend_video": ("generated_video_set", "GenerateVideoOutput"),
    "ai.text_to_speech": ("generated_audio", "TextToSpeechOutput"),
}


@pytest.fixture(scope="module", autouse=True)
def _register_media_nodes():
    import matrx_ai.graph_nodes.image_action  # noqa: F401
    import matrx_ai.graph_nodes.tts_action  # noqa: F401
    import matrx_ai.graph_nodes.video_action  # noqa: F401


@pytest.mark.parametrize(("node_type", "expected"), sorted(EXPECTED.items()))
def test_media_node_declares_its_curated_kind(node_type: str, expected: tuple[str, str]):
    kind, model_name = expected
    spec = default_registry().get(node_type).spec
    assert spec.output_kind == kind, (
        f"{node_type} must declare '{kind}'. An auto-derived action_io_* slug means "
        "the Shape system cannot render it."
    )
    assert spec.output_schema.__name__ == model_name, (
        f"{node_type}'s output model changed to {spec.output_schema.__name__}; the '{kind}' "
        "kind schema was derived from it and must be re-seeded in the same change."
    )


# The media-durability law: internally we pass the ``file_id``; a URL is a
# handoff, never an identity. Each media output model must therefore carry the
# durable handle for the artifact it describes. `path` is the JSON-schema path
# to the property that must exist on that model.
FILE_ID_CARRIERS = {
    "ai.generate_image": ("$defs", "GeneratedImage"),
    "ai.generate_video": ("$defs", "GeneratedVideo"),
    "ai.edit_video": ("$defs", "GeneratedVideo"),
    "ai.extend_video": ("$defs", "GeneratedVideo"),
    # TTS returns ONE audio artifact — the id lives on the output root, not in
    # a per-item sub-model.
    "ai.text_to_speech": (),
}


@pytest.mark.parametrize(("node_type", "defs_path"), sorted(FILE_ID_CARRIERS.items()))
def test_media_output_carries_the_durable_file_id(node_type: str, defs_path: tuple[str, ...]):
    """A node output is PERSISTED — replayed on resume, read by later nodes,
    rendered days later. A signed URL is dead by then and there is nothing to
    re-mint from, so the cld_files id must be on the shape itself."""
    schema = default_registry().get(node_type).spec.output_schema.model_json_schema()
    node = schema
    for key in defs_path:
        node = node[key]
    props = node["properties"]
    assert "file_id" in props, (
        f"{node_type}'s output shape must carry file_id — the durable handle. "
        "Emitting only a URL leaves a consumer that outlives the signature with "
        "nothing to re-mint from (common-docs/systems/media/media-durability/FEATURE.md)."
    )
    assert props["file_id"]["description"], "file_id must document that it is the durable handle."


def test_the_three_video_nodes_share_one_kind():
    """generate / edit / extend return the same shape — one kind, never three."""
    registry = default_registry()
    kinds = {
        registry.get(t).spec.output_kind
        for t in ("ai.generate_video", "ai.edit_video", "ai.extend_video")
    }
    assert kinds == {"generated_video_set"}
