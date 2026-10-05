"""Generated shape skills: template, hash stamp, regeneration rule (chat-shape-picks B1-B2).

Forcing: each case is built so the wrong rule would flip the outcome (an edited body that
a naive 'always regenerate' would overwrite; a legacy body the template cannot reproduce).
"""

from __future__ import annotations

from types import SimpleNamespace
from uuid import uuid4

from matrx_ai.tools.implementations.kind_skill_generation import (
    body_hash,
    decide_refresh,
    generated_metadata,
    generic_description,
    render_skill_body,
    skill_description,
)

EXAMPLE = {"title": "Q3 revenue"}


def make_kd(description: str | None = None) -> SimpleNamespace:
    return SimpleNamespace(
        id=uuid4(),
        kind="revenue_card",
        label="Revenue Card",
        emitted_json_schema={"properties": {"title": {"type": "string"}}, "required": ["title"]},
        metadata={"description": description} if description else {},
    )


def skill_from(kd, *, body=None, guidance=None, stamp=True, description=None, extra_meta=None):
    body = body if body is not None else render_skill_body(kd, EXAMPLE, guidance)
    meta = generated_metadata(
        kd, body, extra_guidance=guidance, body_override=False,
        description=description or generic_description(kd.kind),
    )
    if not stamp:
        for k in ("generated_sha256", "template_inputs", "generated_description"):
            meta.pop(k, None)
    meta.update(extra_meta or {})
    return SimpleNamespace(
        id=uuid4(), body=body, metadata=meta,
        description=description or generic_description(kd.kind),
    )


def test_description_comes_from_the_shape_with_generic_fallback():
    assert skill_description(make_kd("One line.")) == "One line."
    assert skill_description(make_kd()) == generic_description("revenue_card")


def test_metadata_carries_kind_id_hash_and_inputs():
    kd = make_kd()
    meta = generated_metadata(kd, "BODY", extra_guidance="g", body_override=False, description="d")
    assert meta["kind_definition_id"] == str(kd.id)
    assert meta["created_via"] == "kind_create_skill"
    assert meta["generated_sha256"] == body_hash("BODY")
    assert meta["template_inputs"] == {"extra_guidance": "g", "body_override": False}


def test_body_override_is_never_stamped_with_a_hash():
    meta = generated_metadata(make_kd(), "X", extra_guidance=None, body_override=True, description="d")
    assert "generated_sha256" not in meta


def test_untouched_skill_gets_the_shape_description():
    kd = make_kd("Compact revenue headline.")
    d = decide_refresh(skill_from(kd), kd, EXAMPLE)
    assert d.action == "regenerate"
    assert d.description == "Compact revenue headline."


def test_edited_body_is_never_touched():
    kd = make_kd("Compact revenue headline.")
    s = skill_from(kd)
    s.body += "\nHand note"
    assert decide_refresh(s, kd, EXAMPLE).action == "skip_edited"


def test_no_created_via_is_hand_written():
    kd = make_kd("x")
    s = skill_from(kd)
    s.metadata.pop("created_via")
    assert decide_refresh(s, kd, EXAMPLE).action == "skip_hand_written"


def test_body_override_skill_is_hand_written():
    kd = make_kd("x")
    s = skill_from(kd)
    s.metadata["template_inputs"]["body_override"] = True
    assert decide_refresh(s, kd, EXAMPLE).action == "skip_hand_written"


def test_extra_guidance_carried_forward_on_regeneration():
    kd = make_kd("x")
    s = skill_from(kd, guidance="Always cite the quarter.")
    kd.label = "Revenue Headline"  # template input changed -> body differs
    d = decide_refresh(s, kd, EXAMPLE)
    assert d.action == "regenerate"
    assert "Always cite the quarter." in d.body
    assert d.metadata["template_inputs"]["extra_guidance"] == "Always cite the quarter."


def test_legacy_unstamped_reproducible_body_is_stamped_only():
    kd = make_kd()  # no description: nothing to change but the stamp
    s = skill_from(kd, guidance="Cite quarter.", stamp=False)
    d = decide_refresh(s, kd, EXAMPLE)
    assert d.action == "stamp"
    assert d.metadata["generated_sha256"] == body_hash(s.body)
    assert d.metadata["template_inputs"]["extra_guidance"] == "Cite quarter."


def test_legacy_unreproducible_body_counts_as_hand_written():
    kd = make_kd("x")
    s = skill_from(kd, body="# custom body written by hand", stamp=False)
    assert decide_refresh(s, kd, EXAMPLE).action == "skip_hand_written"


def test_up_to_date_does_nothing():
    kd = make_kd("Headline.")
    s = skill_from(kd, description="Headline.")
    assert decide_refresh(s, kd, EXAMPLE).action == "up_to_date"


def test_human_edited_description_survives_regeneration():
    kd = make_kd("Generated headline.")
    s = skill_from(kd)
    s.description = "A person wrote this."
    kd.label = "Renamed"  # body must regenerate for the description rule to matter
    d = decide_refresh(s, kd, EXAMPLE)
    assert d.action == "regenerate"
    assert d.description == "A person wrote this."
