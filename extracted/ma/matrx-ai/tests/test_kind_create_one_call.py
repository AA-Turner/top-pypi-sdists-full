"""kind_create is ONE call: every kind in the shape, innermost first, comes back
under the name the caller must use — reused, new, or (only with a stated
reason) a variant — and junk names and near-duplicates of named kinds are refused (Arman, 2026-10-31). Fake registry; the live lifecycle is covered
by ``tests_trials/run_kind_tools_e2e.py``."""

from __future__ import annotations

import contextlib
from types import SimpleNamespace
from typing import Any
from uuid import uuid4

import pytest

from matrx_ai.tools.implementations.kind_shared import (
    ensure_root_marker,
    infer_schema_from_sample,
    inject_kind_markers_into_schema,
    kind_name_problem,
    schema_fingerprint,
    suggested_kind_name,
)
from matrx_ai.tools.models import ToolContext

CALLER_ORG = str(uuid4())
CALLER_USER = str(uuid4())


@pytest.fixture(autouse=True)
def _writes_run_in_a_person_session(monkeypatch: pytest.MonkeyPatch) -> None:
    import matrx_orm

    from matrx_ai import _ext

    @contextlib.asynccontextmanager
    async def _session(_ctx=None):
        yield

    @contextlib.asynccontextmanager
    async def _lane(*_a, **_k):
        yield

    monkeypatch.setitem(_ext._registry, "acting_as_caller", _session)
    monkeypatch.setattr(matrx_orm, "admin_lane", _lane, raising=False)


def make_ctx() -> ToolContext:
    return ToolContext(call_id=str(uuid4()), tool_name="kind_create")


class _Query:
    def __init__(self, rows: list[Any]):
        self._rows = rows

    def limit(self, _n: int) -> _Query:
        return self

    async def all(self) -> list[Any]:
        return list(self._rows)


class FakeRegistry:
    """The four kind tables, in memory. ``existing`` rows are other people's
    kinds already on the platform; ``created`` records every write."""

    def __init__(self) -> None:
        self.rows: list[Any] = []
        self.created: dict[str, list[dict[str, Any]]] = {
            "kind_definition": [],
            "kind_example": [],
            "kind_component": [],
            "kind_edge": [],
        }
        self.soft_deleted: list[str] = []
        self.fail_edges = False

    def existing(
        self,
        slug: str,
        sample: dict[str, Any],
        *,
        family: str = "user_authored",
        json_schema: dict[str, Any] | None = None,
    ) -> Any:
        marked = ensure_root_marker(sample, slug)
        wire = json_schema or infer_schema_from_sample(marked)
        row = SimpleNamespace(
            id=uuid4(),
            kind=slug,
            label=slug,
            version=1,
            emitted_json_schema=inject_kind_markers_into_schema(wire, marked, slug),
            emitted_fingerprint=schema_fingerprint(wire),
            is_active=True,
            deleted_at=None,
            is_contract_artifact=False,
            metadata={"family": family},
            organization_id=str(uuid4()),
            published_to_web=True,
            shown_to=None,
            created_at="2026-01-01",
        )
        self.rows.append(row)
        return row

    def models(self) -> dict[str, Any]:
        reg = self

        class KindDefinition:
            _database = object()

            @classmethod
            def filter(cls, **kw: Any) -> _Query:
                def match(row: Any) -> bool:
                    return all(getattr(row, k, None) == v for k, v in kw.items())

                return _Query([r for r in reg.rows if match(r)])

            @classmethod
            async def create_item(cls, **payload: Any) -> Any:
                reg.created["kind_definition"].append(payload)
                row = SimpleNamespace(
                    id=uuid4(),
                    version=1,
                    deleted_at=None,
                    is_contract_artifact=False,
                    created_at="2026-10-31",
                    **payload,
                )
                reg.rows.append(row)
                return row

            @classmethod
            async def update_where(cls, where: dict[str, Any], **values: Any) -> Any:
                for row in reg.rows:
                    if str(row.id) == where["id"]:
                        for k, v in values.items():
                            setattr(row, k, v)
                        reg.soft_deleted.append(str(row.id))
                        return SimpleNamespace(rows_affected=1)
                return SimpleNamespace(rows_affected=0)

        examples: dict[str, Any] = {}

        class KindExample:
            @classmethod
            async def create_item(cls, **payload: Any) -> Any:
                reg.created["kind_example"].append(payload)
                row = SimpleNamespace(id=uuid4(), validation_status="passed", **payload)
                examples[str(row.id)] = row
                return row

            @classmethod
            async def get_or_none(cls, **kw: Any) -> Any:
                return examples.get(str(kw.get("id")))

        class KindComponent:
            @classmethod
            async def create_item(cls, **payload: Any) -> Any:
                reg.created["kind_component"].append(payload)
                return SimpleNamespace(id=uuid4(), **payload)

        class KindEdge:
            @classmethod
            async def create_item(cls, **payload: Any) -> Any:
                if reg.fail_edges:
                    raise RuntimeError("edge write failed (planted)")
                reg.created["kind_edge"].append(payload)
                return SimpleNamespace(id=uuid4(), **payload)

        return {
            "KindDefinition": KindDefinition,
            "KindExample": KindExample,
            "KindComponent": KindComponent,
            "KindEdge": KindEdge,
        }


@pytest.fixture
def registry(monkeypatch: pytest.MonkeyPatch) -> FakeRegistry:
    from matrx_ai.tools.implementations import kind_authoring, kind_create_plan, kind_shared

    reg = FakeRegistry()
    models = reg.models()
    monkeypatch.setattr(kind_authoring, "get_db_model", lambda key: models[key])
    monkeypatch.setattr(kind_shared, "get_db_model", lambda key: models[key])
    monkeypatch.setattr(kind_authoring, "ctx_user_id", lambda _ctx: CALLER_USER)
    monkeypatch.setattr(kind_authoring, "ctx_org_id", lambda _ctx: CALLER_ORG)

    async def _viewer(_row: Any, _ctx: Any, _level: str) -> bool:
        return True

    monkeypatch.setattr(kind_create_plan, "can_access_kind", _viewer)
    return reg


async def create(**args: Any) -> Any:
    from matrx_ai.tools.implementations.kind_authoring import kind_create

    return await kind_create({"label": "Thing", "disposition": "record", **args}, make_ctx())


def card(**extra: Any) -> dict[str, Any]:
    return {"front": "Q", "back": "A", "hint": "think", **extra}


# ---------------------------------------------------------------------------
# Junk names
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "slug",
    [
        "",
        "unknown",
        "none",
        "null",
        "n_a",
        "na",
        "tbd",
        "data_2",
        "my_object",
        "unknown_kind",
        "tbd_v1",
        "placeholder",
        "undefined",
        "kind",
        "value_v2",
        "x",
        "test_data",
        "generic_item",
        "new_kind",
        "untitled_3",
    ],
)
def test_junk_kind_names_are_refused(slug: str) -> None:
    assert kind_name_problem(slug) is not None


@pytest.mark.parametrize(
    "slug", ["invoice_summary", "test_card", "brand_profile_people", "wine_tasting", "q3_report"]
)
def test_real_kind_names_pass(slug: str) -> None:
    assert kind_name_problem(slug) is None


def test_a_junk_nested_name_is_offered_a_real_one() -> None:
    assert suggested_kind_name("brand_profile", "people") == "brand_profile_people"
    assert suggested_kind_name("data", "item") is None


@pytest.mark.asyncio
@pytest.mark.parametrize("name", ["", "  ", "Unknown", "NONE", "N/A", "data 2", "unknown-kind"])
async def test_kind_create_refuses_a_junk_root_name_and_writes_nothing(
    registry: FakeRegistry, name: str
) -> None:
    result = await create(name=name, sample_data={"title": "Deck"})
    assert result.success is False
    assert "Nothing was saved" in result.error.message
    assert "not a usable kind name" in result.error.message
    assert all(not rows for rows in registry.created.values())


@pytest.mark.asyncio
@pytest.mark.parametrize("marker", ["none", "unknown_kind", "item"])
async def test_kind_create_refuses_a_junk_nested_marker_with_a_suggestion(
    registry: FakeRegistry, marker: str
) -> None:
    result = await create(
        name="study_deck",
        sample_data={"title": "Deck", "cards": [{"__kind": marker, **card()}]},
    )
    assert result.success is False
    assert "study_deck.cards[]" in result.error.message
    assert "'study_deck_cards'" in result.error.message
    assert all(not rows for rows in registry.created.values())


@pytest.mark.asyncio
@pytest.mark.parametrize("marker", ["", "   ", None])
async def test_kind_create_refuses_a_blank_marker(registry: FakeRegistry, marker: Any) -> None:
    result = await create(
        name="study_deck",
        sample_data={"title": "Deck", "cards": [{"__kind": marker, **card()}]},
    )
    assert result.success is False
    assert "'__kind' is empty" in result.error.message
    assert all(not rows for rows in registry.created.values())


@pytest.mark.asyncio
async def test_every_problem_comes_back_in_one_refusal(registry: FakeRegistry) -> None:
    result = await create(
        name="study_deck",
        sample_data={
            "title": "Deck",
            "cards": [{"__kind": "none", **card()}],
            "author": {"__kind": "unknown", "name": "Ada", "bio": "b", "site": "s"},
        },
    )
    assert result.success is False
    assert "these 2 problems" in result.error.message
    assert (
        "study_deck.cards[]" in result.error.message and "study_deck.author" in result.error.message
    )


# ---------------------------------------------------------------------------
# Reuse — inner kinds first, and their names change the outer shape
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_an_inner_kind_with_an_existing_shape_is_reused_under_its_name(
    registry: FakeRegistry,
) -> None:
    flash = registry.existing("flash_card", card())
    result = await create(
        name="study_deck",
        sample_data={"title": "Deck", "cards": [{"__kind": "card_item", **card()}]},
        child_dispositions={"card_item": "record"},
    )
    assert result.success, result.error
    out = result.output
    assert out.kind == "study_deck" and out.status == "created"
    by_path = {n.path: n for n in out.names}
    assert by_path["study_deck.cards[]"].kind == "flash_card"
    assert by_path["study_deck.cards[]"].status == "reused"
    assert [d["kind"] for d in registry.created["kind_definition"]] == ["study_deck"]
    stored = registry.created["kind_definition"][0]["sample_data"]
    assert stored["cards"][0]["__kind"] == "flash_card"
    assert registry.created["kind_edge"][0]["child_definition_id"] == str(flash.id)


@pytest.mark.asyncio
async def test_an_outer_shape_built_from_existing_parts_is_reused_whole(
    registry: FakeRegistry,
) -> None:
    registry.existing("flash_card", card())
    deck = registry.existing(
        "deck",
        {"title": "T", "subject": "S", "cards": [{"__kind": "flash_card", **card()}]},
    )
    result = await create(
        name="study_deck",
        sample_data={
            "title": "Deck",
            "subject": "Bio",
            "cards": [{"__kind": "card_item", **card()}],
        },
    )
    assert result.success, result.error
    assert result.output.kind == "deck"
    assert result.output.status == "reused"
    assert result.output.kind_definition_id == str(deck.id)
    assert all(not rows for rows in registry.created.values())


@pytest.mark.asyncio
async def test_the_requested_name_is_reused_when_the_example_fits_it(
    registry: FakeRegistry,
) -> None:
    timeline = registry.existing(
        "timeline",
        {"title": "T", "events": ["e"], "owner": "o"},
    )
    result = await create(name="timeline", sample_data={"title": "Q3", "events": ["kickoff"]})
    assert result.success, result.error
    assert result.output.kind == "timeline" and result.output.status == "reused"
    assert result.output.kind_definition_id == str(timeline.id)
    assert all(not rows for rows in registry.created.values())


@pytest.mark.asyncio
async def test_a_small_shape_is_not_merged_into_a_different_name(registry: FakeRegistry) -> None:
    registry.existing(
        "web_link",
        {"name": "n", "url": "u"},
        json_schema={
            "type": "object",
            "description": "A link",
            "properties": {"name": {"type": "string"}, "url": {"type": "string"}},
            "additionalProperties": False,
        },
    )
    result = await create(name="author_ref", sample_data={"name": "Ada", "url": "https://x"})
    assert result.success, result.error
    assert result.output.kind == "author_ref" and result.output.status == "created"


@pytest.mark.asyncio
async def test_a_byte_identical_small_shape_is_reused(registry: FakeRegistry) -> None:
    link = registry.existing("web_link", {"name": "n", "url": "u"})
    result = await create(name="author_ref", sample_data={"name": "Ada", "url": "https://x"})
    assert result.success, result.error
    assert result.output.kind == "web_link" and result.output.status == "reused"
    assert result.output.kind_definition_id == str(link.id)


# ---------------------------------------------------------------------------
# Near-duplicates — a named kind is reused or evolved, never twinned (2026-11-02)
#
# Live, 2026-11-01: 55 kinds like brand_claim_decisions_2 / _3 and
# brand_claim_decisions_brand_claim were minted beside the kinds their mandates
# bind, because a slightly different schema under a taken name was silently
# renamed. A taken name is now refused with the field difference and the doors
# (match it, or kind_update_schema); only new_kind_reasons mints a variant.
# ---------------------------------------------------------------------------


def _decisions_row(registry: FakeRegistry) -> Any:
    row = registry.existing(
        "brand_claim_decisions",
        {"room": "self_description", "order": ["c1"], "not_found": ["x"], "added": ["c2"]},
        family="brand",
    )
    return row


@pytest.mark.asyncio
async def test_a_near_duplicate_of_a_named_kind_is_refused_not_numbered(
    registry: FakeRegistry,
) -> None:
    _decisions_row(registry)
    result = await create(
        name="brand_claim_decisions",
        sample_data={
            "room": "self_description",
            "order": ["c1"],
            "not_found": ["x"],
            "added": ["c2"],
            "decision_notes": "grouped by topic",
        },
    )
    assert result.success is False
    message = result.error.message
    assert "Nothing was saved" in message
    assert "'brand_claim_decisions' already exists with a different shape" in message
    assert "yours adds decision_notes" in message
    assert "kind_update_schema(kind='brand_claim_decisions'" in message
    assert "published from code" in message
    assert "new_kind_reasons" in message
    assert registry.created["kind_definition"] == []
    assert not [r for r in registry.rows if r.kind.startswith("brand_claim_decisions_")]


@pytest.mark.asyncio
async def test_a_near_duplicate_nested_kind_is_refused_not_qualified_by_its_container(
    registry: FakeRegistry,
) -> None:
    registry.existing("person", {"name": "n", "email": "e", "phone": "p"})
    result = await create(
        name="brand_profile",
        sample_data={
            "brand": "Acme",
            "people": [{"__kind": "person", "full_name": "Ada", "role": "CEO", "linkedin": "l"}],
        },
        child_dispositions={"person": "record"},
    )
    assert result.success is False
    message = result.error.message
    assert "brand_profile.people[]: 'person' already exists with a different shape" in message
    assert "yours lacks email, name, phone" in message
    assert all(not rows for rows in registry.created.values())


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("name", "sample", "base"),
    [
        ("brand_profile_2", {"brand": "Acme", "tagline": "t", "hq": "h"}, "brand_profile"),
        (
            "brand_claim_decisions_3",
            {"room": "r", "order": ["c1"], "not_found": [], "added": [], "notes": "n"},
            "brand_claim_decisions",
        ),
    ],
)
async def test_asking_for_a_numbered_copy_by_name_is_refused(
    registry: FakeRegistry, name: str, sample: dict[str, Any], base: str
) -> None:
    registry.existing("brand_profile", {"brand": "b", "founded": 1990, "country": "c"})
    _decisions_row(registry)
    result = await create(name=name, sample_data=sample)
    assert result.success is False
    assert f"copy of the existing kind '{base}'" in result.error.message
    assert registry.created["kind_definition"] == []


@pytest.mark.asyncio
async def test_asking_for_a_container_qualified_copy_by_name_is_refused(
    registry: FakeRegistry,
) -> None:
    registry.existing("brand_claim", {"claim": "c", "quote": "q", "topic": "t"})
    result = await create(
        name="brand_claim_decisions",
        sample_data={
            "room": "self_description",
            "added": [{"__kind": "brand_claim_decisions_brand_claim", "claim": "c", "id": "c1"}],
        },
        child_dispositions={"brand_claim_decisions_brand_claim": "record"},
    )
    assert result.success is False
    assert "copy of the existing kind 'brand_claim'" in result.error.message
    assert registry.created["kind_definition"] == []


@pytest.mark.asyncio
async def test_a_stated_reason_mints_the_variant_and_the_row_keeps_it(
    registry: FakeRegistry,
) -> None:
    registry.existing("brand_profile", {"brand": "b", "founded": 1990, "country": "c"})
    registry.existing("person", {"name": "n", "email": "e", "phone": "p"})
    why_root = "a press-kit profile, not the onboarding brand profile"
    why_child = "a press contact, not a CRM person"
    result = await create(
        name="brand_profile",
        sample_data={
            "brand": "Acme",
            "tagline": "t",
            "people": [{"__kind": "person", "full_name": "Ada", "role": "CEO", "linkedin": "l"}],
        },
        child_dispositions={"person": "record"},
        new_kind_reasons={"brand_profile": why_root, "person": why_child},
    )
    assert result.success, result.error
    assert result.output.kind == "brand_profile_2" and result.output.status == "renamed"
    child = {n.path: n for n in result.output.names}["brand_profile.people[]"]
    assert child.kind == "brand_profile_person" and child.status == "renamed"
    assert why_child in child.note
    rows = {d["kind"]: d for d in registry.created["kind_definition"]}
    assert rows["brand_profile_2"]["metadata"]["variant_of"] == "brand_profile"
    assert rows["brand_profile_2"]["metadata"]["new_kind_reason"] == why_root
    assert rows["brand_profile_person"]["metadata"]["variant_of"] == "person"
    assert rows["brand_profile_person"]["metadata"]["new_kind_reason"] == why_child


@pytest.mark.asyncio
async def test_a_free_new_name_needs_no_reason(registry: FakeRegistry) -> None:
    registry.existing("brand_profile", {"brand": "b", "founded": 1990, "country": "c"})
    result = await create(
        name="press_kit_profile", sample_data={"brand": "Acme", "tagline": "t", "hq": "h"}
    )
    assert result.success, result.error
    assert result.output.kind == "press_kit_profile" and result.output.status == "created"
    assert "variant_of" not in registry.created["kind_definition"][0]["metadata"]


def test_the_arg_contract_accepts_new_kind_reasons() -> None:
    from matrx_ai.tools._generated_declarations import KindCreateArgs

    KindCreateArgs.model_validate(
        {"name": "x_report", "label": "X", "disposition": "record", "new_kind_reasons": {"a": "b"}}
    )


@pytest.mark.asyncio
async def test_one_nested_kind_used_twice_is_created_once(registry: FakeRegistry) -> None:
    result = await create(
        name="match_card",
        sample_data={
            "home": {"__kind": "team_line", "team": "A", "score": 1, "coach": "c"},
            "away": {"__kind": "team_line", "team": "B", "score": 2, "coach": "d"},
        },
        child_dispositions={"team_line": "record"},
    )
    assert result.success, result.error
    assert [d["kind"] for d in registry.created["kind_definition"]].count("team_line") == 1
    assert len(registry.created["kind_edge"]) == 2


# ---------------------------------------------------------------------------
# dry_run and the no-half-shape guarantee
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_dry_run_returns_every_name_and_writes_nothing(registry: FakeRegistry) -> None:
    registry.existing("flash_card", card())
    result = await create(
        name="study_deck",
        sample_data={"title": "Deck", "cards": [{"__kind": "card_item", **card()}]},
        dry_run=True,
    )
    assert result.success, result.error
    assert result.output.dry_run is True
    assert {n.path: n.kind for n in result.output.names} == {
        "study_deck": "study_deck",
        "study_deck.cards[]": "flash_card",
    }
    assert all(not rows for rows in registry.created.values())


@pytest.mark.asyncio
async def test_a_failed_write_soft_deletes_what_this_call_created(registry: FakeRegistry) -> None:
    """A planted failure after the first kind is written: nothing is left live."""
    registry.fail_edges = True
    result = await create(
        name="study_deck",
        sample_data={"title": "Deck", "cards": [{"__kind": "flash_card", **card()}]},
        child_dispositions={"flash_card": "record"},
    )
    assert result.success is False
    created_ids = {str(r.id) for r in registry.rows if r.kind in ("flash_card", "study_deck")}
    assert created_ids, "the planted failure must come after a write to prove the undo"
    assert created_ids <= set(registry.soft_deleted)
    assert all(r.deleted_at is not None for r in registry.rows if str(r.id) in created_ids)


# ---------------------------------------------------------------------------
# Review round 1 (2026-10-31): a green plan never fails at write time
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_two_new_positions_with_one_shape_become_one_kind(registry: FakeRegistry) -> None:
    """The database refuses two names for one byte-identical shape; the plan agrees."""
    result = await create(
        name="site_map",
        sample_data={
            "home": {"__kind": "homepage", "title": "t", "url": "u", "body": "b"},
            "docs": {"__kind": "docs_page", "title": "t", "url": "u", "body": "b"},
        },
        child_dispositions={"homepage": "record", "docs_page": "record"},
    )
    assert result.success, result.error
    made = [d["kind"] for d in registry.created["kind_definition"]]
    assert sorted(made) == ["homepage", "site_map"]
    root = next(d for d in registry.created["kind_definition"] if d["kind"] == "site_map")
    assert root["sample_data"]["docs"]["__kind"] == "homepage"


@pytest.mark.asyncio
async def test_same_fields_with_different_nested_kinds_is_a_plan_time_problem(
    registry: FakeRegistry,
) -> None:
    """press_line has byline's exact wire fields but nests a different kind: the database
    would refuse it (fingerprints ignore nested names), so the plan refuses it first."""
    registry.existing(
        "byline",
        {"headline": "h", "owner": {"__kind": "person_ref", "name": "n", "url": "u", "bio": "b"}},
    )
    result = await create(
        name="press_line",
        sample_data={
            "headline": "h",
            "owner": {"__kind": "company_ref", "name": "Acme", "url": "u", "bio": "b"},
        },
        child_dispositions={"company_ref": "record"},
    )
    assert result.success is False
    assert "has exactly the fields of the existing kind 'byline'" in result.error.message
    assert all(not rows for rows in registry.created.values())


@pytest.mark.asyncio
async def test_an_identical_shape_you_cannot_see_is_named_in_the_plan_without_leaking(
    registry: FakeRegistry, monkeypatch: pytest.MonkeyPatch
) -> None:
    from matrx_ai.tools.implementations import kind_create_plan

    hidden = registry.existing("secret_ledger", {"amount": 1, "memo": "m"})

    async def _no_view(row: Any, _ctx: Any, _level: str) -> bool:
        return row is not hidden

    monkeypatch.setattr(kind_create_plan, "can_access_kind", _no_view)
    result = await create(name="expense_line", sample_data={"amount": 5, "memo": "taxi"})
    assert result.success is False
    assert "a kind you cannot see already has exactly these fields" in result.error.message
    assert "secret_ledger" not in result.error.message
    assert all(not rows for rows in registry.created.values())


@pytest.mark.asyncio
async def test_an_explicit_schema_is_never_reused_into_a_looser_kind(
    registry: FakeRegistry,
) -> None:
    registry.existing("post_state", {"title": "t", "status": "s", "author": "a"})
    strict_schema = {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "status": {"type": "string", "enum": ["draft", "published"]},
            "author": {"type": "string"},
        },
        "required": ["title", "status"],
        "additionalProperties": False,
    }
    result = await create(
        name="article_state",
        json_schema=strict_schema,
        canonical_example={"title": "T", "status": "draft", "author": "Ada"},
    )
    assert result.success, result.error
    assert result.output.kind == "article_state" and result.output.status == "created"


@pytest.mark.asyncio
async def test_a_failure_after_the_insert_removes_that_kind_too(
    registry: FakeRegistry, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The example trigger disagreeing (row already inserted) must not leave the slug held."""
    models = registry.models()
    from matrx_ai.tools.implementations import kind_authoring

    class FailingExample(models["KindExample"]):  # type: ignore[misc, valid-type]
        @classmethod
        async def get_or_none(cls, **kw: Any) -> Any:
            return SimpleNamespace(id=kw.get("id"), validation_status="failed")

    patched = {**models, "KindExample": FailingExample}
    monkeypatch.setattr(kind_authoring, "get_db_model", lambda key: patched[key])
    result = await create(
        name="study_deck", sample_data={"title": "Deck", "topic": "x", "level": 1}
    )
    assert result.success is False
    held = [r for r in registry.rows if r.kind == "study_deck"]
    assert held and all(r.deleted_at is not None for r in held)


@pytest.mark.asyncio
async def test_a_dry_run_needs_no_label(registry: FakeRegistry) -> None:
    from matrx_ai.tools.implementations.kind_authoring import kind_create

    result = await kind_create(
        {
            "name": "study_deck",
            "label": "",
            "disposition": "record",
            "dry_run": True,
            "sample_data": {"title": "Deck"},
        },
        make_ctx(),
    )
    assert result.success, result.error
    assert result.output.dry_run is True


@pytest.mark.asyncio
async def test_an_example_alone_is_enough(registry: FakeRegistry) -> None:
    """canonical_example with no json_schema and no sample_data is the shape (2026-11-01 live run)."""
    result = await create(
        name="study_deck",
        canonical_example={"title": "Deck", "cards": [{"__kind": "flash_card", **card()}]},
        child_dispositions={"flash_card": "record"},
    )
    assert result.success, result.error
    assert {d["kind"] for d in registry.created["kind_definition"]} == {"study_deck", "flash_card"}


# ---------------------------------------------------------------------------
# field_rules: what an example cannot show
# ---------------------------------------------------------------------------


def _programme() -> dict[str, Any]:
    return {
        "title": "Summit",
        "starts_on": "2026-05-01",
        "sessions": [
            {
                "__kind": "conference_session",
                "title": "Opening",
                "track": "keynote",
                "tags": ["ai"],
            },
        ],
    }


def _schema_of(registry: FakeRegistry, slug: str) -> dict[str, Any]:
    row = next(r for r in registry.created["kind_definition"] if r["kind"] == slug)
    return row["emitted_json_schema"]


@pytest.mark.asyncio
async def test_field_rules_keep_allowed_values_and_formats_at_every_level(
    registry: FakeRegistry,
) -> None:
    result = await create(
        name="conference_programme",
        sample_data=_programme(),
        child_dispositions={"conference_session": "record"},
        field_rules={
            "conference_programme": {"starts_on": {"format": "date", "description": "First day."}},
            "conference_session": {
                "track": {"enum": ["keynote", "workshop"]},
                "tags": {"enum": ["ai", "data"]},
            },
        },
    )
    assert result.success is True, result.error
    root = _schema_of(registry, "conference_programme")["properties"]
    assert root["starts_on"]["format"] == "date"
    assert root["starts_on"]["description"] == "First day."
    session = _schema_of(registry, "conference_session")["properties"]
    assert session["track"]["enum"] == ["keynote", "workshop"]
    assert session["tags"]["items"]["enum"] == ["ai", "data"]


@pytest.mark.asyncio
async def test_field_rules_problems_are_all_reported_and_nothing_is_saved(
    registry: FakeRegistry,
) -> None:
    result = await create(
        name="conference_programme",
        sample_data=_programme(),
        child_dispositions={"conference_session": "record"},
        field_rules={
            "conference_programme": {"venue": {"enum": ["a"]}},
            "conference_session": {"track": {"enum": ["workshop"]}},
            "conference_sponsor": {"tier": {"enum": ["gold"]}},
        },
    )
    assert result.success is False
    message = result.error.message
    assert "venue" in message
    assert "breaks field_rules" in message
    assert "conference_sponsor" in message
    assert registry.created["kind_definition"] == []


@pytest.mark.asyncio
async def test_stated_rules_are_never_reused_into_a_looser_kind(registry: FakeRegistry) -> None:
    registry.existing(
        "conference_session", {"title": "Opening", "track": "keynote", "tags": ["ai"]}
    )
    args = {
        "name": "conference_programme",
        "sample_data": _programme(),
        "child_dispositions": {"conference_session": "record"},
        "field_rules": {"conference_session": {"track": {"enum": ["keynote", "workshop"]}}},
    }
    refused = await create(**args)
    assert refused.success is False
    assert "'conference_session' already exists with a different shape" in refused.error.message
    assert registry.created["kind_definition"] == []

    result = await create(
        **args, new_kind_reasons={"conference_session": "tracks are a closed list here"}
    )
    assert result.success is True, result.error
    created = [r["kind"] for r in registry.created["kind_definition"]]
    assert "conference_session" not in created
    assert "conference_programme_conference_session" in created


# ---------------------------------------------------------------------------
# A reused child must be readable by the PARENT's audience, not only the caller
# ---------------------------------------------------------------------------

SYSTEM_ORG_FOR_TEST = "39c38960-0000-4000-8000-000000000000"
OTHER_ORG_FOR_TEST = "5dc930e9-0000-4000-8000-000000000000"


def _caller_in(monkeypatch: pytest.MonkeyPatch, org: str) -> None:
    from matrx_ai.tools.implementations import kind_authoring, kind_shared

    monkeypatch.setattr(kind_authoring, "ctx_org_id", lambda _ctx: org)
    monkeypatch.setattr(kind_shared, "ctx_org_id", lambda _ctx: org)
    monkeypatch.setattr(kind_shared, "system_organization_id", lambda: SYSTEM_ORG_FOR_TEST)
    monkeypatch.setattr(kind_authoring, "system_organization_id", lambda: SYSTEM_ORG_FOR_TEST, raising=False)


@pytest.mark.asyncio
async def test_a_child_private_to_another_org_is_never_reused_under_a_system_org_parent(
    registry: FakeRegistry, monkeypatch: pytest.MonkeyPatch
) -> None:
    """kind_edge 221e5eed (app_log a9c125af): a parent written into the System org reused a
    child private to another org, so every catalog reader met an edge to a child it cannot see."""
    _caller_in(monkeypatch, SYSTEM_ORG_FOR_TEST)
    private = registry.existing("flash_card", card())
    private.organization_id = OTHER_ORG_FOR_TEST
    private.published_to_web = False

    result = await create(
        name="study_deck",
        sample_data={"title": "Deck", "cards": [{"__kind": "card_item", **card()}]},
        child_dispositions={"card_item": "record"},
    )

    edges = registry.created["kind_edge"]
    assert all(e["child_definition_id"] != str(private.id) for e in edges), (
        "a System-org parent's edge points at a child only another organization can read"
    )
    # The identical shape cannot be minted twice (the database's shape-uniqueness guard), so
    # the plan refuses by naming the real reason, before any write.
    assert not result.success
    assert "belongs to another organization and is not published" in result.error.message
    assert registry.created["kind_definition"] == []


@pytest.mark.asyncio
async def test_a_private_child_in_the_parents_own_org_is_still_reused(
    registry: FakeRegistry, monkeypatch: pytest.MonkeyPatch
) -> None:
    _caller_in(monkeypatch, OTHER_ORG_FOR_TEST)
    own = registry.existing("flash_card", card())
    own.organization_id = OTHER_ORG_FOR_TEST
    own.published_to_web = False

    result = await create(
        name="study_deck",
        sample_data={"title": "Deck", "cards": [{"__kind": "card_item", **card()}]},
        child_dispositions={"card_item": "record"},
    )

    assert result.success, result.error
    assert registry.created["kind_edge"][0]["child_definition_id"] == str(own.id)
