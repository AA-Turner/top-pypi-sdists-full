"""The emitted contract schema — the artifact this migration exists to produce.

D2 makes a pure-TypeScript sister package the goal; D8 puts the contract's home
in matrx-utils; `model_json_schema()` is the mechanism joining them.
`UnifiedConfig` being a dataclass is exactly why the most important type in the
system has had no cross-language definition. This is that gap closing, and these
tests are what stop the document from quietly lying.
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "scripts"))

import emit_contract_schema as emit  # noqa: E402


def test_the_committed_schema_matches_the_live_models():
    """Same posture as aidream's generate_types.py --check: a committed snapshot
    that drifts from its source is worse than no snapshot."""
    assert emit.main.__module__  # imported
    doc, _ = emit.build()
    expected = json.dumps(doc, indent=2, sort_keys=False) + "\n"
    assert emit.OUT.exists(), "contract.schema.json has never been generated"
    assert emit.OUT.read_text() == expected, (
        "contract.schema.json is stale — regenerate with "
        "python scripts/emit_contract_schema.py"
    )


def test_it_describes_every_twin_including_registry_exported_ones():
    """The gap the first version had: walking `__all__` alone emitted 20 of 27,
    because the fourteen structured inputs reach the surface through
    STRUCTURED_INPUT_MODEL_MAP rather than as individual names. Half a family
    was silently undescribed."""
    doc, _ = emit.build()
    defs = doc["$defs"]

    for name in ("UnifiedConfigModel", "UnifiedMessageModel", "UnifiedResponseModel",
                 "TokenUsageModel", "TextContentModel", "ImageContentModel"):
        assert name in defs, name

    structured = [n for n in defs if n.endswith("InputContentModel")]
    assert len(structured) == 16, f"expected 16 structured inputs, found {len(structured)}"


def test_the_document_is_self_contained():
    """Every $ref resolves inside the document. A dangling ref makes it
    unusable by a generator, which is the only reason it exists."""
    doc, _ = emit.build()
    text = json.dumps(doc)
    refs = set(re.findall(r'"\$ref":\s*"#/\$defs/([^"]+)"', text))
    missing = refs - set(doc["$defs"])
    assert not missing, f"dangling $refs: {sorted(missing)}"


def test_unconstrained_fields_are_declared_not_hidden():
    """A schema that hides its own soft spots is worse than one that names them.
    Ten fields emit no usable constraint — the staged `Any`s and the four
    media-generation inputs that have never been populated."""
    doc, loose = emit.build()
    assert doc["x-unconstrained-fields"] == loose
    assert "UnifiedConfigModel.messages" in loose
    assert "UnifiedConfigModel.system_instruction" in loose
    assert "ToolResultContentModel.content" in loose


def test_an_anyOf_hiding_an_Any_still_counts_as_unconstrained():
    """The subtle detection gap, pinned. `Any | list[Any]` emits a union whose
    first branch accepts anything, so the union constrains nothing — and the
    naive check (`does it have an anyOf?`) called that constrained. It hid the
    two most important staged fields in the contract."""
    assert emit._is_unconstrained({}) is True
    assert emit._is_unconstrained({"type": "string"}) is False
    assert emit._is_unconstrained({"anyOf": [{}, {"type": "array"}]}) is True
    assert emit._is_unconstrained({"anyOf": [{"type": "string"}, {"type": "null"}]}) is False


def test_the_schema_is_valid_json_and_declares_its_dialect():
    doc = json.loads(emit.OUT.read_text())
    assert doc["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert doc["title"] == "Matrx engine contract"


def test_the_schema_does_not_depend_on_what_was_imported_first():
    """A ``Literal`` compares by its SET of values and ``typing`` caches
    ``Optional[...]`` by that key (an LRU of 128), so a library that declared the
    same values in another order shortly before hands ITS object to our twin. The
    OpenAI SDK's ``Optional[Literal["transparent", "opaque", "auto"]]``
    (``openai.types.responses.tool``) did exactly that to
    ``UnifiedConfigModel.background`` and turned nightly level1 red whenever the
    full suite's collection order put the SDK there first (2026-11-01).

    The collision is staged deterministically — clear the typing caches, declare
    the SDK's union first, let the twin's own declaration take the cache hit and
    rebuild the twin with it — and the document must still be the committed bytes.
    The twin is restored afterwards so no other test sees the staged state."""
    import typing
    from typing import Literal

    from matrx_ai.config.models.unified import UnifiedConfigModel as twin

    field = twin.model_fields["background"]
    original = field.annotation
    try:
        for clear in typing._cleanups:
            clear()
        # The collision lives in ``Optional``'s cache specifically (the spelling both the
        # SDK and the twin use); ``X | None`` does not share it, so it cannot stage this.
        optional = typing.Optional
        sdk = optional[Literal["transparent", "opaque", "auto"]]  # the SDK's order, declared first
        ours = optional[Literal["auto", "opaque", "transparent"]]  # what the twin declares
        assert ours is sdk, "the typing cache no longer collides — the staging is void"
        field.annotation = ours
        twin.model_rebuild(force=True)
        staged = twin.model_json_schema()["properties"]["background"]["anyOf"][0]["enum"]
        assert staged == ["transparent", "opaque", "auto"], f"collision not staged: {staged}"

        doc, _ = emit.build()
        text = json.dumps(doc, indent=2, sort_keys=False) + "\n"
        assert emit.OUT.read_text() == text, (
            "contract.schema.json changes when another library declared the same Literal first"
        )
    finally:
        field.annotation = original
        twin.model_rebuild(force=True)
