"""The @kind SDK — one decorator, the whole ceremony; publication as a plan.

Pins the effort-inversion contract (plan §4.3): decorating pins the
discriminator, catalogs the model, validates the canonical example at import,
derives nested edges from the schema — and publication NEVER silently
overwrites a live registration (drift is reported for the compatibility gate).
"""

from __future__ import annotations

import pytest

from matrx_graph.content_ir.model import KindModel
from matrx_graph.content_ir.sdk import (
    clear_kind_catalog,
    kind,
    kind_catalog,
    nested_kind_slugs,
    publication_plan,
)


@pytest.fixture(autouse=True)
def _isolated_catalog():
    clear_kind_catalog()
    yield
    clear_kind_catalog()


def _declare_rating():
    @kind("rating", disposition="record", family="primitive", example={"value": 4.5, "count": 120})
    class Rating(KindModel):
        value: float
        count: int | None = None

    return Rating


def test_decorator_pins_the_discriminator_and_catalogs() -> None:
    Rating = _declare_rating()
    assert Rating.kind_slug == "rating"
    assert Rating(value=4.5).model_dump()["__kind"] == "rating"
    registration = kind_catalog()["rating"]
    assert registration.family == "primitive"
    assert registration.category == "data"


def test_label_defaults_from_the_class_name() -> None:
    @kind("web_result", disposition="record")
    class WebResult(KindModel):
        url: str

    @kind("ai_answer", disposition="record")
    class AIAnswer(KindModel):
        text: str

    assert kind_catalog()["web_result"].label == "Web Result"
    assert kind_catalog()["ai_answer"].label == "AI Answer"


def test_broken_example_fails_at_import_in_the_authors_face() -> None:
    with pytest.raises(Exception):

        @kind(
            "bad_example",
            disposition="record",
            example={"value": "not-a-float-at-all", "bogus": 1},
        )
        class Bad(KindModel):
            value: float


def test_two_models_cannot_claim_one_slug() -> None:
    _declare_rating()
    with pytest.raises(ValueError, match="already declared"):

        @kind("rating", disposition="record")
        class Impostor(KindModel):
            stars: int


def test_one_class_cannot_carry_two_kinds() -> None:
    with pytest.raises(ValueError, match="contradicts"):

        @kind("second_name", disposition="record")
        class Conflicted(KindModel, kind="first_name"):
            value: int


def test_category_is_layer_model_only() -> None:
    with pytest.raises(ValueError, match="'data' or 'runtime'"):
        kind("x", disposition="record", category="fancy")


def test_nested_edges_come_from_the_schema() -> None:
    Rating = _declare_rating()

    @kind("web_result", disposition="record", family="search")
    class WebResult(KindModel):
        url: str
        rating: Rating | None = None

    @kind("search_results", disposition="record", family="search")
    class SearchResults(KindModel):
        query: str
        web: list[WebResult] = []

    assert nested_kind_slugs(WebResult) == ("rating",)
    # Transitively visible in the schema; dedup holds.
    assert set(nested_kind_slugs(SearchResults)) == {"web_result", "rating"}


def test_publication_plan_create_match_drift() -> None:
    Rating = _declare_rating()

    @kind("web_result", disposition="record", family="search")
    class WebResult(KindModel):
        url: str
        title: str
        rating: Rating | None = None

    live = {
        # rating is live and identical (modulo cosmetic keys)
        "rating": Rating.model_json_schema(),
        # web_result is live but the LIVE schema lacks `title`
    }
    live_web = WebResult.model_json_schema()
    import copy

    drifted = copy.deepcopy(live_web)
    for candidate in [drifted] + list((drifted.get("$defs") or {}).values()):
        if isinstance(candidate, dict) and "title" in (candidate.get("properties") or {}):
            del candidate["properties"]["title"]
    live["web_result"] = drifted

    plan = {p.slug: p for p in publication_plan(kind_catalog(), live.get)}
    # search_results not in catalog here; rating matches; web_result drifts.
    assert plan["rating"].action == "match"
    assert plan["web_result"].action == "drift"
    assert "title" in (plan["web_result"].drift_summary or "")
    # An unregistered kind is a create, carrying its edges for kind_edge rows.
    clear_kind_catalog()
    RatingAgain = _declare_rating()
    plan2 = publication_plan(kind_catalog(), lambda slug: None)
    assert plan2[0].action == "create"


def test_cosmetic_docstring_changes_are_not_drift() -> None:
    Rating = _declare_rating()
    live = Rating.model_json_schema()
    live = {**live, "description": "Some older prose that changed."}
    plan = publication_plan({"rating": kind_catalog()["rating"]}, {"rating": live}.get)
    assert plan[0].action == "match"


# ---------------------------------------------------------------------------
# The compatibility gate (distillation pass, 2026-08-20)
# ---------------------------------------------------------------------------


def _schema(properties: dict, required: list[str]) -> dict:
    return {"type": "object", "properties": properties, "required": required}


def test_compatibility_allows_added_optional_field():
    """The distillation upgrade shape: new OPTIONAL fields, old payloads fine."""
    from matrx_graph.content_ir.sdk import compatibility_verdict

    live = _schema({"text": {"type": "string"}}, ["text"])
    model = _schema(
        {
            "text": {"type": "string"},
            "iso": {"anyOf": [{"type": "string"}, {"type": "null"}]},
        },
        ["text"],
    )
    verdict = compatibility_verdict(model, live)
    assert verdict.compatible
    assert verdict.breaking == ()
    assert any("iso" in note for note in verdict.additive)


def test_compatibility_refuses_added_required_field():
    from matrx_graph.content_ir.sdk import compatibility_verdict

    live = _schema({"text": {"type": "string"}}, ["text"])
    model = _schema({"text": {"type": "string"}, "iso": {"type": "string"}}, ["text", "iso"])
    verdict = compatibility_verdict(model, live)
    assert not verdict.compatible
    assert any("REQUIRED" in note for note in verdict.breaking)


def test_compatibility_refuses_removed_field_and_type_change():
    from matrx_graph.content_ir.sdk import compatibility_verdict

    live = _schema({"text": {"type": "string"}, "n": {"type": "integer"}}, ["text"])

    removed = compatibility_verdict(_schema({"text": {"type": "string"}}, ["text"]), live)
    assert not removed.compatible
    assert any("removes field 'n'" in note for note in removed.breaking)

    retyped = compatibility_verdict(
        _schema({"text": {"type": "string"}, "n": {"type": "string"}}, ["text"]), live
    )
    assert not retyped.compatible
    assert any("type/constraints" in note for note in retyped.breaking)


def test_compatibility_refuses_tightening_an_existing_field():
    """An optional field going required breaks readers of old payloads."""
    from matrx_graph.content_ir.sdk import compatibility_verdict

    live = _schema({"text": {"type": "string"}, "iso": {"type": "string"}}, ["text"])
    model = _schema({"text": {"type": "string"}, "iso": {"type": "string"}}, ["text", "iso"])
    verdict = compatibility_verdict(model, live)
    assert not verdict.compatible
    assert any("makes existing field 'iso' REQUIRED" in note for note in verdict.breaking)


def test_compatibility_allows_a_field_widening_to_a_superset_model():
    """``$ref`` swapped for a subclass that only ADDS optional fields.

    The distillation shape: a kind declared ``usage: AiUsage`` while its node
    emitted ``TranscriptionUsage`` (AiUsage + an optional billing figure), so
    the extra field was invisible to the registry. Comparing ``$ref`` NAMES
    calls that a type change; comparing what they point at does not.
    """
    from matrx_graph.content_ir.sdk import compatibility_verdict

    live = {
        "type": "object",
        "properties": {"usage": {"$ref": "#/$defs/AiUsage"}},
        "required": ["usage"],
        "$defs": {
            "AiUsage": {
                "type": "object",
                "properties": {"cost_usd": {"type": "number"}},
                "required": [],
            }
        },
    }
    model = {
        "type": "object",
        "properties": {"usage": {"$ref": "#/$defs/TranscriptionUsage"}},
        "required": ["usage"],
        "$defs": {
            "TranscriptionUsage": {
                "type": "object",
                "properties": {
                    "cost_usd": {"type": "number"},
                    "duration_seconds": {"anyOf": [{"type": "number"}, {"type": "null"}]},
                },
                "required": [],
            }
        },
    }
    verdict = compatibility_verdict(model, live)
    assert verdict.compatible, verdict.breaking
    assert any("widens field 'usage'" in note for note in verdict.additive)


def test_compatibility_refuses_a_field_narrowing_to_a_subset_model():
    """The reverse direction is a real break — old payloads carry the field."""
    from matrx_graph.content_ir.sdk import compatibility_verdict

    rich = {
        "type": "object",
        "properties": {"usage": {"$ref": "#/$defs/Rich"}},
        "required": [],
        "$defs": {
            "Rich": {
                "type": "object",
                "properties": {"a": {"type": "number"}, "b": {"type": "number"}},
                "required": [],
            }
        },
    }
    thin = {
        "type": "object",
        "properties": {"usage": {"$ref": "#/$defs/Thin"}},
        "required": [],
        "$defs": {
            "Thin": {"type": "object", "properties": {"a": {"type": "number"}}, "required": []}
        },
    }
    verdict = compatibility_verdict(thin, rich)
    assert not verdict.compatible
    assert any("type/constraints of field 'usage'" in note for note in verdict.breaking)


def test_compatibility_refuses_a_nested_field_becoming_required():
    from matrx_graph.content_ir.sdk import compatibility_verdict

    live = {
        "type": "object",
        "properties": {"usage": {"$ref": "#/$defs/U"}},
        "required": [],
        "$defs": {"U": {"type": "object", "properties": {"a": {"type": "number"}}, "required": []}},
    }
    model = {
        "type": "object",
        "properties": {"usage": {"$ref": "#/$defs/U"}},
        "required": [],
        "$defs": {
            "U": {"type": "object", "properties": {"a": {"type": "number"}}, "required": ["a"]}
        },
    }
    verdict = compatibility_verdict(model, live)
    assert not verdict.compatible


def test_compatibility_allows_an_unchanged_ref_to_a_non_object_definition():
    """An enum ``$ref`` that did not change is not a type change.

    Found 2026-08-20: ``agent_assignment_batch_result`` could not be evolved at
    all because its nested ``AssignmentSessionStatus`` enum resolved to a
    ``"type": "string"`` definition, and the superset rule only accepted
    OBJECT targets — so a byte-identical enum was reported as
    *changes the type/constraints of field 'session'*. Every kind carrying a
    nested enum was permanently un-evolvable.
    """
    from matrx_graph.content_ir.sdk import compatibility_verdict

    status_def = {"type": "string", "enum": ["pending", "completed", "failed"]}
    live = {
        "type": "object",
        "properties": {"status": {"$ref": "#/$defs/Status"}, "note": {"type": "string"}},
        "required": ["status"],
        "$defs": {"Status": status_def},
    }
    model = {
        "type": "object",
        "properties": {
            "status": {"$ref": "#/$defs/Status"},
            "note": {"type": "string"},
            "attempts": {"type": "integer", "default": 0},
        },
        "required": ["status"],
        "$defs": {"Status": dict(status_def)},
    }
    verdict = compatibility_verdict(model, live)
    assert verdict.compatible, verdict.breaking
    assert any("adds optional field 'attempts'" in note for note in verdict.additive)


def test_compatibility_still_refuses_a_changed_enum_ref():
    """A shrunk enum is a real break — old payloads may carry the dropped value."""
    from matrx_graph.content_ir.sdk import compatibility_verdict

    live = {
        "type": "object",
        "properties": {"status": {"$ref": "#/$defs/Status"}},
        "required": ["status"],
        "$defs": {"Status": {"type": "string", "enum": ["pending", "completed", "failed"]}},
    }
    model = {
        "type": "object",
        "properties": {"status": {"$ref": "#/$defs/Status"}},
        "required": ["status"],
        "$defs": {"Status": {"type": "string", "enum": ["pending", "completed"]}},
    }
    verdict = compatibility_verdict(model, live)
    assert not verdict.compatible
    assert any("field 'status'" in note for note in verdict.breaking)


def test_compatibility_allows_marker_normalization_and_unordered_union_widening():
    """The registry's marker sweep and a widened authored union are not breaks.

    This is the minimal ``agent_definition`` shape: old rows have only text
    blocks, while the new model keeps text and admits a second typed part.  The
    stored schema also has trigger-injected optional markers and reordered enum
    values.  Each old payload remains valid under the new schema.
    """
    from matrx_graph.content_ir.sdk import compatibility_verdict

    live = {
        "type": "object",
        "properties": {"content": {"items": {"$ref": "#/$defs/Text"}, "type": "array"}},
        "$defs": {
            "Text": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "__kind": {"type": "string"},
                    "text": {"type": "string"},
                    "role": {"type": "string", "enum": ["user", "system"]},
                },
                "required": ["text", "role"],
            }
        },
    }
    model = {
        "type": "object",
        "properties": {
            "content": {
                "items": {
                    "anyOf": [
                        {"$ref": "#/$defs/Text"},
                        {"$ref": "#/$defs/TypedPart"},
                    ]
                },
                "type": "array",
            }
        },
        "$defs": {
            "Text": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "text": {"type": "string"},
                    "role": {"type": "string", "enum": ["system", "user", "assistant"]},
                },
                "required": ["text", "role"],
            },
            "TypedPart": {
                "type": "object",
                "additionalProperties": False,
                "properties": {"value": {"type": "number"}},
                "required": ["value"],
            },
        },
    }

    verdict = compatibility_verdict(model, live)
    assert verdict.compatible, verdict.breaking


def test_compatibility_still_refuses_a_union_or_enum_narrowing():
    """Subset tests must not become a permissive marker/reorder exception."""
    from matrx_graph.content_ir.sdk import compatibility_verdict

    live = {
        "type": "object",
        "properties": {
            "value": {
                "anyOf": [
                    {"type": "string", "enum": ["old", "kept"]},
                    {"type": "integer"},
                ]
            }
        },
    }
    narrowed_enum = {
        "type": "object",
        "properties": {
            "value": {
                "anyOf": [
                    {"type": "string", "enum": ["kept"]},
                    {"type": "integer"},
                ]
            }
        },
    }
    dropped_branch = {
        "type": "object",
        "properties": {"value": {"anyOf": [{"type": "string", "enum": ["old", "kept"]}]}},
    }

    assert not compatibility_verdict(narrowed_enum, live).compatible
    assert not compatibility_verdict(dropped_branch, live).compatible


def test_compatibility_does_not_confuse_json_boolean_and_number_enum_values():
    """Python says ``True == 1``; JSON Schema validates distinct value types."""
    from matrx_graph.content_ir.sdk import compatibility_verdict

    live = _schema({"flag": {"type": "boolean", "enum": [True]}}, [])
    model = _schema({"flag": {"type": "boolean", "enum": [1]}}, [])

    assert not compatibility_verdict(model, live).compatible


def test_compatibility_refuses_closing_an_open_object_behind_a_ref():
    """Ref resolution must retain old extra keys, not only named properties."""
    from matrx_graph.content_ir.sdk import compatibility_verdict

    live = {
        "type": "object",
        "properties": {"payload": {"$ref": "#/$defs/OpenPayload"}},
        "$defs": {
            "OpenPayload": {
                "type": "object",
                "properties": {"known": {"type": "string"}},
                "additionalProperties": True,
            }
        },
    }
    model = {
        "type": "object",
        "properties": {"payload": {"$ref": "#/$defs/ClosedPayload"}},
        "$defs": {
            "ClosedPayload": {
                "type": "object",
                "properties": {"known": {"type": "string"}},
                "additionalProperties": False,
            }
        },
    }

    assert not compatibility_verdict(model, live).compatible


def test_compatibility_keeps_json_types_distinct_behind_refs_and_map_values():
    """Reference equality must not reintroduce Python's ``True == 1`` bug."""
    from matrx_graph.content_ir.sdk import compatibility_verdict

    live_enum = {
        "type": "object",
        "properties": {"value": {"$ref": "#/$defs/Flag"}},
        "$defs": {"Flag": {"type": "boolean", "enum": [True]}},
    }
    model_enum = {
        "type": "object",
        "properties": {"value": {"$ref": "#/$defs/Flag"}},
        "$defs": {"Flag": {"type": "boolean", "enum": [1]}},
    }
    live_map = {
        "type": "object",
        "properties": {"value": {"$ref": "#/$defs/OpenMap"}},
        "$defs": {
            "OpenMap": {
                "type": "object",
                "additionalProperties": {"type": "boolean", "enum": [True]},
            }
        },
    }
    model_map = {
        "type": "object",
        "properties": {"value": {"$ref": "#/$defs/OpenMap"}},
        "$defs": {
            "OpenMap": {
                "type": "object",
                "additionalProperties": {"type": "boolean", "enum": [1]},
            }
        },
    }

    assert not compatibility_verdict(model_enum, live_enum).compatible
    assert not compatibility_verdict(model_map, live_map).compatible


# ---------------------------------------------------------------------------
# The gate resolves $refs INSIDE containers, not just at the top of a field
# ---------------------------------------------------------------------------


def _container_schema(defs_name: str, *, extra_prop: bool = False) -> dict:
    """``{variants: dict[str, <defs_name>]}`` with that definition inlined."""
    target: dict = {
        "type": "object",
        "properties": {"key": {"type": "string"}},
        "required": ["key"],
    }
    if extra_prop:
        # An ADDED OPTIONAL field — the superset case a distillation makes.
        target["properties"]["__kind"] = {"type": "string", "default": "x"}
    return {
        "type": "object",
        "properties": {
            "variants": {
                "type": "object",
                "additionalProperties": {"$ref": f"#/$defs/{defs_name}"},
            }
        },
        "$defs": {defs_name: target},
    }


def test_renaming_a_container_element_definition_is_not_a_breaking_change():
    """``dict[str, AssetVariant]`` → ``dict[str, AssetVariantKind]``.

    Found 2026-08-21 while minting ``asset_variant``: the gate resolved a
    ``$ref`` sitting directly on a field but compared a ref nested under
    ``additionalProperties`` by NAME, so pointing a dict-valued field at an
    identically-shaped definition was refused as a type change.
    """
    from matrx_graph.content_ir.sdk import compatibility_verdict

    verdict = compatibility_verdict(
        _container_schema("AssetVariantKind"), _container_schema("AssetVariant")
    )
    assert verdict.compatible, verdict.breaking


def test_container_element_gaining_an_optional_field_is_a_widening():
    from matrx_graph.content_ir.sdk import compatibility_verdict

    verdict = compatibility_verdict(
        _container_schema("AssetVariantKind", extra_prop=True),
        _container_schema("AssetVariant"),
    )
    assert verdict.compatible, verdict.breaking
    assert any("variants" in note for note in verdict.additive), verdict.additive


def test_container_element_gaining_a_REQUIRED_field_is_still_refused():
    """The resolution must not become a blanket pass — tightening still breaks."""
    from matrx_graph.content_ir.sdk import compatibility_verdict

    tightened = _container_schema("AssetVariantKind")
    tightened["$defs"]["AssetVariantKind"]["properties"]["file_id"] = {"type": "string"}
    tightened["$defs"]["AssetVariantKind"]["required"] = ["key", "file_id"]
    verdict = compatibility_verdict(tightened, _container_schema("AssetVariant"))
    assert not verdict.compatible
    assert any("variants" in note for note in verdict.breaking), verdict.breaking


def test_container_keywords_themselves_must_still_match():
    """Only the ELEMENT type may resolve; the container's own keywords cannot drift."""
    from matrx_graph.content_ir.sdk import compatibility_verdict

    retyped = _container_schema("AssetVariantKind")
    retyped["properties"]["variants"]["type"] = "array"
    verdict = compatibility_verdict(retyped, _container_schema("AssetVariant"))
    assert not verdict.compatible


def test_ref_with_sibling_keywords_is_not_spurious_drift():
    from matrx_graph.content_ir.sdk import compatibility_verdict

    """A ``$ref`` beside ordinary keywords must keep them through resolution.

    JSON Schema 2020-12 allows siblings next to ``$ref`` and pydantic uses that
    for every defaulted ``JsonValue`` field. The gate used to return the bare
    ``$defs`` target and throw the siblings away, so a model field that says
    ``{"$ref": "#/$defs/JsonValue", "default": null}`` compared as ``{}``
    against a live field published by an older dump that inlined the same empty
    definition as ``{"default": null}`` — identical in meaning, refused as
    "changes the type/constraints of field 'first'"
    (``regex_extract_result``, 2026-08-23).
    """
    live = {
        "type": "object",
        "title": "RegexExtractOutput",
        "properties": {
            "count": {"type": "integer", "default": 0},
            "first": {"title": "First", "default": None, "description": "the first match"},
        },
        "additionalProperties": False,
    }
    model = {
        "type": "object",
        "title": "RegexExtractOutput",
        "$defs": {"JsonValue": {}},
        "properties": {
            "count": {"type": "integer", "default": 0},
            "first": {
                "$ref": "#/$defs/JsonValue",
                "default": None,
                "description": "the first match",
            },
        },
        "additionalProperties": False,
    }
    verdict = compatibility_verdict(model, live)
    assert verdict.compatible, verdict.breaking

    # …and the siblings still COUNT: tightening one through the ref is caught.
    tightened = {
        **model,
        "properties": {
            **model["properties"],
            "first": {"$ref": "#/$defs/JsonValue", "default": "now-required-ish", "const": "x"},
        },
    }
    assert not compatibility_verdict(tightened, live).compatible


def test_a_default_alone_is_not_a_type_or_constraint_change():
    """``default`` is a pure ANNOTATION (JSON Schema 2020-12 §9.2).

    It does not participate in validation, so it cannot make an old payload
    stop validating in either direction. A live field with no ``default`` and
    a model field carrying one — same type, same const — is the SAME contract.
    """
    from matrx_graph.content_ir.sdk import compatibility_verdict

    live = _schema({"mode": {"type": "string", "const": "fast"}}, ["mode"])
    model = _schema(
        {"mode": {"type": "string", "const": "fast", "default": "fast", "title": "Mode"}},
        ["mode"],
    )
    verdict = compatibility_verdict(model, live)
    assert verdict.compatible, verdict.breaking
    assert verdict.breaking == ()


def test_kind_marker_default_no_longer_forces_a_breaking_publish():
    """The exact ``scraped_page`` case, reproduced live 2026-08-23.

    Every ``@kind`` model emits ``__kind`` WITH a ``default``; live rows the
    ``__kind`` schema-law campaign patched by hand carry the same const with
    NO ``default``. The gate reported "changes the type/constraints of field
    '__kind'" and forced the distillation through ``--breaking`` — dishonest,
    and it hides any real break behind a flag the author already had to pass.
    """
    from matrx_graph.content_ir.sdk import compatibility_verdict

    live = _schema(
        {
            "__kind": {
                "type": "string",
                "const": "scraped_page",
                "description": "Content-IR kind marker.",
            },
            "url": {"type": "string"},
        },
        ["__kind", "url"],
    )
    model = _schema(
        {
            "__kind": {
                "type": "string",
                "const": "scraped_page",
                "title": "Kind",
                "default": "scraped_page",
                "description": "Content-IR kind marker.",
            },
            "url": {"type": "string"},
        },
        ["__kind", "url"],
    )
    verdict = compatibility_verdict(model, live)
    assert verdict.compatible, verdict.breaking
    assert not any("__kind" in note for note in verdict.breaking)


def test_optional_deep_kind_marker_on_an_untyped_dict_is_not_breaking():
    """The file_write_result ``stat`` regression from the live marker sweep."""
    from matrx_graph.content_ir.sdk import compatibility_verdict

    model = _schema(
        {"stat": {"anyOf": [{"type": "object"}, {"type": "null"}]}}, []
    )
    live = _schema(
        {
            "stat": {
                "anyOf": [
                    {
                        "type": "object",
                        "properties": {"__kind": {"type": "string"}},
                        "additionalProperties": True,
                    },
                    {"type": "null"},
                ]
            }
        },
        [],
    )

    verdict = compatibility_verdict(model, live)
    assert verdict.compatible, verdict.breaking


def test_optional_deep_marker_exception_reads_pydantic_s_REAL_open_object():
    """🚨 THE 2026-09-13 HOLE — the test above hand-typed a schema pydantic never emits.

    ``test_optional_deep_kind_marker_on_an_untyped_dict_is_not_breaking`` writes
    the model branch as ``{"type": "object"}``. A real ``stat: dict | None``
    field emits ``{"type": "object", "additionalProperties": true}`` — the same
    open object, one extra key — and the recognizer's exact-match
    (``model != {"type": "object"}``) refused it. So ``file_write_result`` was
    reported INCOMPATIBLE for a change nobody made, the publisher refused it,
    and the full census went red on 2026-09-13 with no way to publish out of it.

    This test builds the model schema from a REAL model, so it can never again
    pass against a spelling pydantic does not produce.
    """
    from matrx_graph.content_ir.sdk import compatibility_verdict

    class FileWriteLike(KindModel):
        path: str = ""
        stat: dict | None = None

    model = FileWriteLike.model_json_schema()
    assert model["properties"]["stat"]["anyOf"][0] == {
        "type": "object",
        "additionalProperties": True,
    }, "pydantic changed how it spells an open dict — re-read the recognizer"

    live = {
        **model,
        "properties": {
            **model["properties"],
            "stat": {
                "anyOf": [
                    {
                        "type": "object",
                        "properties": {
                            "__kind": {
                                "type": "string",
                                "description": "The registered kind this payload is an instance of, when it is one.",
                            }
                        },
                        "additionalProperties": True,
                    },
                    {"type": "null"},
                ],
                "title": "Stat",
                "default": None,
            },
        },
    }

    verdict = compatibility_verdict(model, live)
    assert verdict.compatible, verdict.breaking


def test_open_object_recognizer_still_refuses_a_narrowed_map_value():
    """Falsifiability: ``additionalProperties`` carrying a SCHEMA is not open.

    The fix above treats ``additionalProperties: true`` as "no constraint". A
    schema there IS a constraint, and an old payload whose stat values are not
    strings must still stop the gate.
    """
    from matrx_graph.content_ir.sdk import compatibility_verdict

    model = _schema(
        {"stat": {"type": "object", "additionalProperties": {"type": "string"}}}, []
    )
    live = _schema(
        {
            "stat": {
                "type": "object",
                "properties": {"__kind": {"type": "string"}},
                "additionalProperties": True,
            }
        },
        [],
    )
    assert not compatibility_verdict(model, live).compatible


def test_true_open_schemas_match_empty_jsonvalue_refs_in_maps_and_items():
    """``additionalProperties: true`` and ``JsonValue: {}`` accept the same values."""
    from matrx_graph.content_ir.sdk import compatibility_verdict

    empty_ref = {"$ref": "#/$defs/JsonValue"}
    defs = {"JsonValue": {}}
    for container in ("additionalProperties", "items"):
        if container == "additionalProperties":
            model_value = {"type": "object", container: True}
            live_value = {"type": "object", container: empty_ref}
        else:
            model_value = {"type": "array", container: True}
            live_value = {"type": "array", container: empty_ref}
        for new_value, old_value in ((model_value, live_value), (live_value, model_value)):
            model = _schema({"value": new_value}, [])
            live = _schema({"value": old_value}, [])
            model["$defs"] = defs
            live["$defs"] = defs
            verdict = compatibility_verdict(model, live)
            assert verdict.compatible, verdict.breaking

    referenced_models = (
        ({"type": "object", "additionalProperties": True}, {"type": "object", "additionalProperties": empty_ref}),
        ({"type": "object", "additionalProperties": empty_ref}, {"type": "object", "additionalProperties": True}),
    )
    for model_target, live_target in referenced_models:
        model = _schema({"value": {"$ref": "#/$defs/Container"}}, [])
        live = _schema({"value": {"$ref": "#/$defs/Container"}}, [])
        model["$defs"] = {"Container": model_target, "JsonValue": {}}
        live["$defs"] = {"Container": live_target, "JsonValue": {}}
        verdict = compatibility_verdict(model, live)
        assert verdict.compatible, verdict.breaking

    # The two normalizations must compose when the empty value ref sits inside
    # an object reached through a separate schema reference.
    combined = (
        (
            {"type": "object", "properties": {}, "additionalProperties": empty_ref},
            {"type": "object", "additionalProperties": True},
        ),
        (
            {"type": "object", "additionalProperties": True},
            {"type": "object", "properties": {}, "additionalProperties": empty_ref},
        ),
    )
    for model_target, live_target in combined:
        model = _schema({"value": {"$ref": "#/$defs/Container"}}, [])
        live = _schema({"value": {"$ref": "#/$defs/Container"}}, [])
        model["$defs"] = {"Container": model_target, "JsonValue": {}}
        live["$defs"] = {"Container": live_target, "JsonValue": {}}
        verdict = compatibility_verdict(model, live)
        assert verdict.compatible, verdict.breaking


def test_real_comparison_item_input_list_schema_matches_legacy_open_inputs():
    """Reproduce the live ComparisonItemInputList shape from the 2026-10-23 drift."""
    from copy import deepcopy

    from pydantic import BaseModel, ConfigDict, Field, JsonValue

    from matrx_graph.content_ir.sdk import compatibility_verdict

    class ComparisonInput(BaseModel):
        model_config = ConfigDict(extra="forbid")
        label: str | None = None
        url: str | None = None
        inputs: dict[str, JsonValue] | None = None
        website: str | None = None
        logo_url: str | None = None

    class ComparisonItemInputListLike(KindModel):
        items: list[ComparisonInput] = Field(default_factory=list)

    model = ComparisonItemInputListLike.model_json_schema()
    live = deepcopy(model)
    item = next(
        name
        for name, schema in model["$defs"].items()
        if schema.get("properties", {}).get("inputs") is not None
    )
    model_inputs = model["$defs"][item]["properties"]["inputs"]["anyOf"][0]
    assert model_inputs == {"type": "object", "additionalProperties": {"$ref": "#/$defs/JsonValue"}}
    live["$defs"][item]["properties"]["inputs"]["anyOf"][0] = {
        "type": "object",
        "properties": {
            "__kind": {
                "type": "string",
                "description": "The registered kind this payload is an instance of, when it is one.",
            }
        },
        "additionalProperties": True,
    }

    verdict = compatibility_verdict(model, live)
    assert verdict.compatible, verdict.breaking


def test_empty_properties_normalization_keeps_other_object_constraints():
    from matrx_graph.content_ir.sdk import compatibility_verdict

    model = _schema({"value": {"type": "object", "properties": {}}}, [])
    live = _schema({"value": {"type": "object"}}, [])
    assert compatibility_verdict(model, live).compatible
    assert compatibility_verdict(live, model).compatible

    constrained = _schema({"value": {"type": "object", "minProperties": 1}}, [])
    assert not compatibility_verdict(model, constrained).compatible
    assert not compatibility_verdict(constrained, model).compatible


def test_open_schema_normalization_does_not_hide_real_narrowing_or_ref_constraints():
    from matrx_graph.content_ir.sdk import compatibility_verdict

    empty_ref = {"$ref": "#/$defs/JsonValue"}
    open_model = _schema({"value": {"type": "object", "additionalProperties": empty_ref}}, [])
    open_model["$defs"] = {"JsonValue": {}}
    legacy = _schema({"value": {"type": "object", "additionalProperties": True}}, [])
    assert compatibility_verdict(open_model, legacy).compatible

    dropped_property = _schema({"value": {"type": "object", "properties": {}, "additionalProperties": empty_ref}}, [])
    dropped_property["$defs"] = {"JsonValue": {}}
    old_property = _schema({"value": {"type": "object", "properties": {"old": {"type": "string"}}, "additionalProperties": True}}, [])
    assert not compatibility_verdict(dropped_property, old_property).compatible

    closed = _schema({"value": {"type": "object", "additionalProperties": False}}, [])
    assert not compatibility_verdict(closed, legacy).compatible

    constrained = _schema(
        {"value": {"type": "object", "additionalProperties": {"$ref": "#/$defs/StringValue"}}}, []
    )
    constrained["$defs"] = {"StringValue": {"type": "string"}}
    assert not compatibility_verdict(constrained, legacy).compatible

    sibling_constraint = _schema(
        {"value": {"type": "object", "additionalProperties": {"$ref": "#/$defs/JsonValue", "enum": ["only"]}}}, []
    )
    sibling_constraint["$defs"] = {"JsonValue": {}}
    assert not compatibility_verdict(sibling_constraint, legacy).compatible

    unknown_ref = _schema(
        {"value": {"type": "object", "additionalProperties": {"$ref": "#/$defs/Missing"}}}, []
    )
    unknown_ref["$defs"] = {}
    assert not compatibility_verdict(unknown_ref, legacy).compatible

    cyclic = _schema({"value": {"type": "object", "additionalProperties": {"$ref": "#/$defs/Cycle"}}}, [])
    cyclic["$defs"] = {"Cycle": {"$ref": "#/$defs/Cycle"}}
    assert not compatibility_verdict(cyclic, legacy).compatible

    dropped_enum = _schema(
        {"value": {"type": "object", "additionalProperties": {"type": "string", "enum": ["kept"]}}}, []
    )
    legacy_enum = _schema(
        {"value": {"type": "object", "additionalProperties": {"type": "string", "enum": ["old", "kept"]}}}, []
    )
    assert not compatibility_verdict(dropped_enum, legacy_enum).compatible


def test_optional_deep_marker_exception_does_not_hide_real_object_constraints():
    from matrx_graph.content_ir.sdk import compatibility_verdict

    model = _schema({"stat": {"type": "object"}}, [])
    live = _schema(
        {
            "stat": {
                "type": "object",
                "properties": {
                    "__kind": {"type": "string"},
                    "required_by_old_rows": {"type": "string"},
                },
                "required": ["required_by_old_rows"],
                "additionalProperties": True,
            }
        },
        [],
    )
    assert not compatibility_verdict(model, live).compatible


def test_optional_deep_marker_exception_checks_nullable_union_siblings():
    """A sibling can narrow every union branch, so it must not be skipped."""
    from matrx_graph.content_ir.sdk import compatibility_verdict

    live = _schema(
        {
            "stat": {
                "anyOf": [
                    {
                        "type": "object",
                        "properties": {"__kind": {"type": "string"}},
                        "additionalProperties": True,
                    },
                    {"type": "null"},
                ]
            }
        },
        [],
    )
    model = {
        **live,
        "properties": {
            "stat": {
                **live["properties"]["stat"],
                "additionalProperties": False,
            }
        },
    }
    assert not compatibility_verdict(model, live).compatible


def test_the_kind_marker_gate_can_still_fail_on_a_real_narrowing():
    """Planted failure: the gate must still catch a REAL change to ``__kind``.

    Same field, same annotation-only ``default`` difference — but the const
    VALUE moves (a re-slug: old rows say ``scraped_page`` and would stop
    validating), and separately the TYPE moves. Both must be refused, or the
    fix above would have made this suite unable to fail.
    """
    from matrx_graph.content_ir.sdk import compatibility_verdict

    live = _schema(
        {"__kind": {"type": "string", "const": "scraped_page", "description": "marker"}},
        ["__kind"],
    )

    reslugged = _schema(
        {
            "__kind": {
                "type": "string",
                "const": "scraped_document",
                "default": "scraped_document",
                "description": "marker",
            }
        },
        ["__kind"],
    )
    verdict = compatibility_verdict(reslugged, live)
    assert not verdict.compatible
    assert any("__kind" in note for note in verdict.breaking), verdict

    retyped = _schema(
        {"__kind": {"type": "integer", "const": 7, "default": 7, "description": "marker"}},
        ["__kind"],
    )
    assert not compatibility_verdict(retyped, live).compatible


def test_a_changed_default_is_still_DRIFT_even_though_it_is_compatible():
    """Compatible is not the same as unchanged — the plan must still publish it.

    ``default`` is stripped for the compatibility question ONLY. Drift
    detection keeps it, so a changed default is planned as an update and never
    lands silently.
    """
    from matrx_graph.content_ir.sdk import _structurally_equal

    live = {"type": "object", "properties": {"n": {"type": "integer"}}}
    model = {"type": "object", "properties": {"n": {"type": "integer", "default": 0}}}
    assert not _structurally_equal(model, live)


def test_a_field_literally_NAMED_default_is_still_compared():
    """The annotation strip must never reach a property NAME.

    ``properties`` keys are data. A kind with a real field called ``default``
    losing its type would otherwise be invisible to the gate.
    """
    from matrx_graph.content_ir.sdk import compatibility_verdict

    live = _schema({"default": {"type": "string"}}, ["default"])
    retyped = _schema({"default": {"type": "integer"}}, ["default"])
    assert not compatibility_verdict(retyped, live).compatible
    assert compatibility_verdict(live, live).compatible


# ── Disposition at birth (KINDS-GLUE wave 1) ─────────────────────────────────
# Break each guards: `@kind` accepting a kind that never said what its output is, so the
# kind is published, activated, and every verified emission of it is refused storage.


def test_a_kind_without_a_disposition_is_refused_at_declaration_naming_it() -> None:
    with pytest.raises(ValueError, match=r"'halvorsen_rate_card' does not say what its output is"):

        @kind("halvorsen_rate_card", family="commerce")
        class HalvorsenRateCard(KindModel):
            crew_rate: float

    assert "halvorsen_rate_card" not in kind_catalog()


@pytest.mark.parametrize("bad", ["", "  ", "table", "Record"])
def test_a_disposition_outside_the_closed_set_is_refused(bad: str) -> None:
    with pytest.raises(ValueError, match="halvorsen_rate_card"):

        @kind("halvorsen_rate_card", disposition=bad)
        class HalvorsenRateCard(KindModel):
            crew_rate: float


@pytest.mark.parametrize(
    "disposition", ["record", "envelope", "receipt", "proposal", "prose"]
)
def test_the_declared_disposition_reaches_the_publication_plan(disposition: str) -> None:
    @kind("lindqvist_move_quote", disposition=disposition)
    class LindqvistMoveQuote(KindModel):
        crew_size: int

    assert kind_catalog()["lindqvist_move_quote"].disposition == disposition
    (action,) = publication_plan(kind_catalog(), lambda _slug: None)
    assert action.disposition == disposition


def test_a_registration_built_directly_still_needs_a_disposition() -> None:
    from matrx_graph.content_ir.sdk import KindRegistration

    class Bare(KindModel, kind="bare_quote"):
        amount: float

    with pytest.raises(ValueError, match="'bare_quote' does not say what its output is"):
        KindRegistration(slug="bare_quote", model=Bare, label="Bare", disposition="")
