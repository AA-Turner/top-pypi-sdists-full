from types import SimpleNamespace

import pytest

from matrx_seo.artifact_writers import (
    apply_page_keyword_analysis,
    apply_page_keyword_map,
    apply_site_topic_valuations,
    apply_topic_assignments,
)


@pytest.mark.asyncio
@pytest.mark.parametrize("keyword_id", ["", "foreign-keyword-id"])
async def test_topic_assignments_reject_ids_outside_the_offered_batch(keyword_id: str) -> None:
    with pytest.raises(ValueError, match="outside its offered batch"):
        await apply_topic_assignments(
            {
                "assigner_version": "topic-v1",
                "assignments": [
                    {
                        "keyword_id": keyword_id,
                        "primary_topic": "recycling",
                    }
                ],
            },
            allowed_keyword_ids={"offered-keyword-id"},
        )


@pytest.mark.asyncio
async def test_first_site_topic_valuation_carries_tenant_identity(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from matrx_seo.artifact_writers import m

    async def topics(**_filters: object):
        # A taxonomy node: its worth stays on seo.site_topic_value only, so this
        # unit test never reaches the canonical offering writer (proven live).
        return [SimpleNamespace(id="topic-1", slug="recycling", node_type="authority")]

    async def missing(**_filters: object):
        return None

    created: list[dict[str, object]] = []

    async def create(**fields: object):
        created.append(fields)
        return SimpleNamespace(**fields)

    monkeypatch.setattr(m.Topic, "filter_items", staticmethod(topics))
    monkeypatch.setattr(m.SiteTopicValue, "get_or_none", staticmethod(missing))
    monkeypatch.setattr(m.SiteTopicValue, "create", staticmethod(create))

    summary = await apply_site_topic_valuations(
        {
            "valuer_version": "sitevalue-v1",
            "valuations": [
                {
                    "topic_slug": "recycling",
                    "service_match": "core_service",  # old key + value vocabulary
                    "weight": 0.9,
                }
            ],
        },
        site_id="site-1",
        organization_id="org-1",
        created_by="user-1",
    )

    assert summary["valuations_written"] == 1
    assert created and created[0].get("offering_match") == "core_offering"
    assert created[0]["organization_id"] == "org-1"
    assert created[0]["site_id"] == "site-1"
    assert created[0]["created_by"] == "user-1"


@pytest.mark.asyncio
async def test_site_topic_valuation_normalizes_stale_enum_on_update(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from matrx_seo.artifact_writers import m

    async def topics(**_filters: object):
        # A taxonomy node: its worth stays on seo.site_topic_value only, so this
        # unit test never reaches the canonical offering writer (proven live).
        return [SimpleNamespace(id="topic-1", slug="recycling", node_type="authority")]

    updated: list[dict[str, object]] = []

    async def update(**fields: object):
        updated.append(fields)

    async def existing(**_filters: object):
        return SimpleNamespace(update=update)

    monkeypatch.setattr(m.Topic, "filter_items", staticmethod(topics))
    monkeypatch.setattr(m.SiteTopicValue, "get_or_none", staticmethod(existing))

    summary = await apply_site_topic_valuations(
        {
            "valuer_version": "sitevalue-v1",
            "valuations": [
                {
                    "topic_slug": "recycling",
                    "offering_match": "adjacent_service",
                    "weight": 0.9,
                }
            ],
        },
        site_id="site-1",
        organization_id="org-1",
        created_by="user-1",
    )

    assert summary["valuations_written"] == 1
    assert updated and updated[0]["offering_match"] == "adjacent_offering"


@pytest.mark.asyncio
async def test_page_keyword_analysis_writes_site_value_and_links_page(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import matrx_seo.orm_identity as orm_identity
    from matrx_seo.artifact_writers import m

    keyword_ids = {"lip filler newport beach": "kw-primary", "lip filler cost": "kw-support"}

    async def upsert_keywords(items):
        return [(keyword_ids[phrase], True) for phrase, _lang in items]

    linked: list[tuple[str, str, str]] = []

    async def link_keyword_to_page(keyword_id, page_id, **_kwargs):
        linked.append((keyword_id, page_id, _kwargs.get("role")))

    async def missing(**_filters):
        return None

    created: list[dict[str, object]] = []

    async def create(**fields):
        created.append(fields)
        return SimpleNamespace(**fields)

    monkeypatch.setattr(orm_identity, "upsert_keywords", upsert_keywords)
    monkeypatch.setattr(orm_identity, "link_keyword_to_page", link_keyword_to_page)
    monkeypatch.setattr(m.SiteKeywordValue, "get_or_none", staticmethod(missing))
    monkeypatch.setattr(m.SiteKeywordValue, "create", staticmethod(create))

    summary = await apply_page_keyword_analysis(
        {
            "analyzer_version": "pageanalyze-v1",
            "page_url": "https://example.com/lip-fillers",
            "inferred_primary_keyword": {
                "phrase": "lip filler newport beach",
                "evidence": "H1",
                "confidence": 88,
            },
            "supported_keywords": [
                {"phrase": "lip filler cost", "evidence": "H2", "confidence": 90}
            ],
            "discovered_keywords": [],
            "declared_vs_actual": {"status": "aligned"},
            "content_role": "money_page",
            "funnel_position": "vendor_evaluation",
            "gaps": [],
            "cannibalization_risk": [],
        },
        site_id="site-1",
        page_id="page-1",
        organization_id="org-1",
        created_by="user-1",
    )

    assert summary["primary_keyword_id"] == "kw-primary"
    assert summary["supporting_keyword_ids"] == ["kw-support"]
    assert len(created) == 2
    assert all(row["content_role"] == "money_page" for row in created)
    assert all(row["workflow_status"] == "targeted" for row in created)
    assert {kid for kid, _pid, _role in linked} == {"kw-primary", "kw-support"}


@pytest.mark.asyncio
async def test_page_keyword_analysis_requires_analyzer_version() -> None:
    with pytest.raises(ValueError, match="analyzer_version"):
        await apply_page_keyword_analysis(
            {"inferred_primary_keyword": {"phrase": "x"}},
            site_id="site-1",
            page_id="page-1",
            organization_id="org-1",
            created_by="user-1",
        )


@pytest.mark.asyncio
async def test_page_keyword_map_assigns_existing_page_and_suppresses(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import matrx_seo.artifact_writers as writers
    import matrx_seo.orm_identity as orm_identity
    from matrx_seo.artifact_writers import m

    async def upsert_keyword(phrase, _language="en"):
        return {"lip filler newport beach": "kw-primary", "cheap lip filler": "kw-skip"}[
            phrase
        ], True

    linked: list[tuple[str, str, str]] = []

    async def link_keyword_to_page(keyword_id, page_id, **_kwargs):
        linked.append((keyword_id, page_id, _kwargs.get("role")))

    async def missing(**_filters):
        return None

    created: list[dict[str, object]] = []

    async def create(**fields):
        created.append(fields)
        return SimpleNamespace(**fields)

    page_row = SimpleNamespace(id="page-1")

    async def get_page(**_filters):
        return page_row

    monkeypatch.setattr(orm_identity, "upsert_keyword", upsert_keyword)
    monkeypatch.setattr(orm_identity, "link_keyword_to_page", link_keyword_to_page)
    monkeypatch.setattr(writers.WebPage, "get_or_none", staticmethod(get_page))
    monkeypatch.setattr(m.SiteKeywordValue, "get_or_none", staticmethod(missing))
    monkeypatch.setattr(m.SiteKeywordValue, "create", staticmethod(create))

    summary = await apply_page_keyword_map(
        {
            "mapper_version": "pagemap-v1",
            "topic_slug": "lip-fillers",
            "page_plans": [
                {
                    "page": {"existing_url": "https://example.com/lip-fillers"},
                    "primary_keyword": "lip filler newport beach",
                    "supporting_keywords": [],
                    "content_role": "money_page",
                    "confidence": 85,
                }
            ],
            "skipped": [{"phrase": "cheap lip filler", "reason": "off_brand"}],
        },
        site_id="site-1",
        organization_id="org-1",
        created_by="user-1",
    )

    assert summary["pages_mapped"] == 1
    assert summary["keywords_assigned"] == 1
    assert summary["keywords_suppressed"] == 1
    assert summary["unresolved_pages"] == []
    assert linked == [("kw-primary", "page-1", "primary")]
    assert any(row["workflow_status"] == "targeted" for row in created)
    assert any(row["workflow_status"] == "suppressed" for row in created)


@pytest.mark.asyncio
async def test_page_keyword_map_records_unresolved_pages(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import matrx_seo.artifact_writers as writers
    import matrx_seo.orm_identity as orm_identity
    from matrx_seo.artifact_writers import m

    async def upsert_keyword(phrase, _language="en"):
        return "kw-1", True

    async def missing_page(**_filters):
        return None

    async def missing_value(**_filters):
        return None

    created: list[dict[str, object]] = []

    async def create(**fields):
        created.append(fields)
        return SimpleNamespace(**fields)

    monkeypatch.setattr(orm_identity, "upsert_keyword", upsert_keyword)
    monkeypatch.setattr(writers.WebPage, "get_or_none", staticmethod(missing_page))
    monkeypatch.setattr(m.SiteKeywordValue, "get_or_none", staticmethod(missing_value))
    monkeypatch.setattr(m.SiteKeywordValue, "create", staticmethod(create))

    summary = await apply_page_keyword_map(
        {
            "mapper_version": "pagemap-v1",
            "topic_slug": "lip-fillers",
            "page_plans": [
                {
                    "page": {"existing_url": "https://example.com/gone"},
                    "primary_keyword": "lip filler cost",
                    "content_role": "money_page",
                }
            ],
        },
        site_id="site-1",
        organization_id="org-1",
        created_by="user-1",
    )

    assert summary["unresolved_pages"] == ["https://example.com/gone"]
    # unresolved page still values the keyword (workflow_status stays candidate)
    assert created[0]["workflow_status"] == "candidate"


# ── KI-039: universal facts are tenant-neutral ──────────────────────────────


def _guard_vocabulary():
    from matrx_seo.facet_registry import FacetDimension, FacetValue, FacetVocabulary

    def val(dim: str, v: str) -> FacetValue:
        return FacetValue(
            value=v, label=v, description=None, category_id=f"{dim}:{v}", position=0, abstain=False
        )

    platform = FacetDimension(
        slug="intent_class",
        label="Intent",
        description=None,
        scope="platform",
        cardinality="single",
        site_id=None,
        category_id="dim-intent",
        values=(val("intent_class", "informational"), val("intent_class", "transactional")),
    )
    site = FacetDimension(
        slug="site:severity",
        label="Severity",
        description=None,
        scope="site",
        cardinality="single",
        site_id="site-1",
        category_id="dim-severity",
        values=(val("site:severity", "hot"), val("site:severity", "cold")),
    )
    return FacetVocabulary(
        dimensions=(platform, site),
        skipped=(),
        platform_revision="20260824000000",
        site_id="site-1",
    )


def test_emitted_facets_universal_false_drops_platform_answers() -> None:
    """KI-039: a context-carrying run's platform-dimension answers are discarded."""
    from matrx_seo.artifact_writers import _emitted_facets

    result = {
        "keyword_id": "kw-1",
        "intent_class": "transactional",
        "site_facets": {"site:severity": "hot"},
    }
    vocab = _guard_vocabulary()
    assert _emitted_facets(result, vocab, universal=True) == {
        "intent_class": "transactional",
        "site:severity": "hot",
    }
    assert _emitted_facets(result, vocab, universal=False) == {"site:severity": "hot"}


@pytest.mark.asyncio
async def test_apply_classifications_site_tier_never_touches_the_shared_row(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """KI-039: universal=False writes site-tier facts only — no mirror columns,
    no classifier_version stamp — and says so in its summary."""
    import matrx_seo.artifact_writers as writers

    update_calls: list[dict[str, object]] = []

    class FakeKeyword:
        id = "0b6f1c9e-3a2d-4c1e-9f7a-5d2b8e4a1c01"
        organization_id = "org-sys"
        phrase = "crt tv disposal"

        async def update(self, **fields: object) -> None:
            update_calls.append(fields)

    async def load(_kid: str):
        return FakeKeyword()

    facet_calls: list[dict[str, object]] = []

    async def fake_write(**kwargs: object) -> int:
        facet_calls.append(kwargs)
        return len(kwargs.get("emitted") or {})  # type: ignore[arg-type]

    monkeypatch.setattr(writers.m.Keyword, "load_by_id_or_none", staticmethod(load))
    monkeypatch.setattr(writers, "_write_keyword_facets", fake_write)

    batch = {
        "classifier_version": "kwclass-v2.20260824000000",
        "results": [
            {
                "keyword_id": "0b6f1c9e-3a2d-4c1e-9f7a-5d2b8e4a1c01",
                "intent_class": "transactional",
                "site_facets": {"site:severity": "hot"},
                "overall_confidence": 88,
            }
        ],
    }
    summary = await writers.apply_keyword_classifications(
        batch, vocabulary=_guard_vocabulary(), universal=False
    )

    assert update_calls == []  # the shared row was never written
    assert summary["site_tier_only"] is True
    assert summary["updated"] == 1
    assert len(facet_calls) == 1
    assert facet_calls[0]["universal"] is False
    assert facet_calls[0]["emitted"] == {"site:severity": "hot"}


def test_site_facets_channel_rejects_platform_slugs() -> None:
    """Adversarial fix: a platform slug smuggled through site_facets fails the
    item loudly instead of overwriting a shared universal fact."""
    from matrx_seo.artifact_writers import _emitted_facets
    from matrx_seo.facet_registry import FacetVocabularyError

    result = {
        "keyword_id": "0b6f1c9e-3a2d-4c1e-9f7a-5d2b8e4a1c01",
        "site_facets": {"intent_class": "transactional"},
    }
    for universal in (True, False):
        with pytest.raises(FacetVocabularyError, match="site channel"):
            _emitted_facets(result, _guard_vocabulary(), universal=universal)


@pytest.mark.asyncio
async def test_smuggled_platform_slug_rejects_item_not_batch(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The channel violation lands in rejected_unknown_value; the batch survives."""
    import matrx_seo.artifact_writers as writers

    class FakeKeyword:
        id = "0b6f1c9e-3a2d-4c1e-9f7a-5d2b8e4a1c01"
        organization_id = "org-sys"
        phrase = "crt tv disposal"

        async def update(self, **fields: object) -> None:
            raise AssertionError("shared row must not be written for a rejected item")

    async def load(_kid: str):
        return FakeKeyword()

    monkeypatch.setattr(writers.m.Keyword, "load_by_id_or_none", staticmethod(load))

    batch = {
        "classifier_version": "kwclass-v2.20260824000000",
        "results": [{"keyword_id": "0b6f1c9e-3a2d-4c1e-9f7a-5d2b8e4a1c01", "site_facets": {"intent_class": "transactional"}}],
    }
    summary = await writers.apply_keyword_classifications(
        batch, vocabulary=_guard_vocabulary(), universal=False
    )
    assert summary["updated"] == 0
    assert len(summary["rejected_unknown_value"]) == 1
    assert "site channel" in summary["rejected_unknown_value"][0]


@pytest.mark.asyncio
async def test_unavailable_offering_is_proposed_never_placed_or_made_available(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """D2 (brand-offerings cutover): the assigner places on an offering the site
    offers, and PROPOSES one it does not offer — it never writes a placement on
    it and never calls anything that adopts or makes an offering available."""
    import matrx_seo.artifact_writers as writers

    calls: list[tuple[str, tuple[object, ...]]] = []

    async def fake_call_function(_db: str, schema: str, name: str, *args: object, **_kw: object):
        calls.append((f"{schema}.{name}", args))
        if name == "fn_site_available_offering_for_template":
            return "offering-sold" if args[1] == "topic-sold" else None
        if name == "write_site_keyword_offering":
            return [{"written": len(args[2].value), "removed": 0, "human_protected": 0}]
        if name == "propose_site_offering_from_template":
            return [{"assist_id": "a-1", "status": "created", "keyword_count": 2}]
        if name == "set_site_keyword_map_home":
            return [
                {
                    "homed": 0,
                    "created": len(args[1].value),
                    "moved": 0,
                    "kept": 0,
                    "kept_human": 0,
                    "no_map": 0,
                    "no_offering": 0,
                }
            ]
        raise AssertionError(f"unexpected database call {schema}.{name}")

    async def org(_site_id: str) -> str:
        return "org-1"

    async def kinds(topic_ids: set[str]) -> dict[str, str]:
        return {topic_id: "service" for topic_id in topic_ids}

    monkeypatch.setattr(writers, "call_function", fake_call_function)
    monkeypatch.setattr(writers, "_site_organization_id", org)
    monkeypatch.setattr(writers, "_topic_node_types", kinds)

    placement = {"assigner_version": "topic-v9", "confirmed": True}
    counts = await writers._write_canonical_placements(
        "site-1",
        [
            {
                "keyword_id": "kw-1",
                "topic_id": "topic-sold",
                "confidence": 80,
                "placement": placement,
            },
            {
                "keyword_id": "kw-2",
                "topic_id": "topic-new",
                "confidence": 80,
                "placement": placement,
            },
            {
                "keyword_id": "kw-3",
                "topic_id": "topic-new",
                "confidence": 60,
                "placement": placement,
            },
        ],
    )

    names = [name for name, _ in calls]
    assert "seo.fn_site_offering_for_topic" not in names
    writes = [args for name, args in calls if name == "seo.write_site_keyword_offering"]
    assert len(writes) == 1 and writes[0][3] == "offering-sold"
    assert writes[0][2].value == ["kw-1"]
    proposals = [args for name, args in calls if name == "seo.propose_site_offering_from_template"]
    assert len(proposals) == 1
    assert proposals[0][1] == "topic-new" and proposals[0][2].value == ["kw-2", "kw-3"]
    assert counts["offering_proposals"] == 1
    assert counts["keywords_awaiting_offering"] == 2
    assert counts["canonical_written"] == 1

    # THE THIRD WRITE (migration 23): the topical map's home topic is set for
    # exactly the keywords that were PLACED. A keyword whose offering was only
    # proposed has no primary offering yet, so it must not be sent — otherwise
    # the map would be asked to home a keyword nothing placed.
    homes = [args for name, args in calls if name == "seo.set_site_keyword_map_home"]
    assert len(homes) == 1
    assert homes[0][0] == "site-1"
    assert homes[0][1].value == ["kw-1"]
    assert counts["map_home_created"] == 1


@pytest.mark.asyncio
async def test_a_topic_with_no_offering_template_skips_that_topic_never_the_batch(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """2026-09-21 → 09-30, All Green Recycling: the assigner had lazily grown a
    service topic with no ``web.offering_template`` row, the proposal writer
    raised ``offering_template_not_found`` for it, and that ONE topic failed the
    whole batch every night — so the site placement of the offered keywords, the
    map homes, and every later pass of the platform's largest site never ran.
    One unresolvable topic is skipped WITH its reason; everything else lands."""
    import matrx_seo.artifact_writers as writers

    calls: list[tuple[str, tuple[object, ...]]] = []

    class NoDataFoundError(Exception):
        pass

    async def fake_call_function(_db: str, schema: str, name: str, *args: object, **_kw: object):
        calls.append((f"{schema}.{name}", args))
        if name == "fn_site_available_offering_for_template":
            return "offering-sold" if args[1] == "topic-sold" else None
        if name == "write_site_keyword_offering":
            return [{"written": len(args[2].value), "removed": 0, "human_protected": 0}]
        if name == "propose_site_offering_from_template":
            if args[1] == "topic-orphan":
                raise NoDataFoundError(
                    "offering_template_not_found: topic-orphan is not an active offering template"
                )
            return [{"assist_id": "a-1", "status": "created", "keyword_count": 1}]
        if name == "set_site_keyword_map_home":
            return [
                {
                    "homed": 0,
                    "created": len(args[1].value),
                    "moved": 0,
                    "kept": 0,
                    "kept_human": 0,
                    "no_map": 0,
                    "no_offering": 0,
                }
            ]
        raise AssertionError(f"unexpected database call {schema}.{name}")

    async def org(_site_id: str) -> str:
        return "org-1"

    async def kinds(topic_ids: set[str]) -> dict[str, str]:
        return {topic_id: "service" for topic_id in topic_ids}

    monkeypatch.setattr(writers, "call_function", fake_call_function)
    monkeypatch.setattr(writers, "_site_organization_id", org)
    monkeypatch.setattr(writers, "_topic_node_types", kinds)

    placement = {"assigner_version": "topic-v9", "confirmed": True}
    counts = await writers._write_canonical_placements(
        "site-1",
        [
            {"keyword_id": "kw-1", "topic_id": "topic-orphan", "confidence": 90, "placement": placement},
            {"keyword_id": "kw-2", "topic_id": "topic-orphan", "confidence": 90, "placement": placement},
            {"keyword_id": "kw-3", "topic_id": "topic-new", "confidence": 90, "placement": placement},
            {"keyword_id": "kw-4", "topic_id": "topic-sold", "confidence": 90, "placement": placement},
        ],
    )

    assert counts["canonical_written"] == 1
    assert counts["offering_proposals"] == 1
    assert counts["keywords_awaiting_offering"] == 1
    assert counts["offering_proposals_skipped"] == 1
    assert counts["keywords_unproposable"] == 2
    [skip] = counts["offering_proposal_skips"]
    assert skip["topic_id"] == "topic-orphan" and skip["keyword_count"] == 2
    assert skip["reason"].startswith("offering_template_not_found: ")
    # The map home still runs after the skipped topic.
    homes = [args for name, args in calls if name == "seo.set_site_keyword_map_home"]
    assert len(homes) == 1 and homes[0][1].value == ["kw-4"]


@pytest.mark.asyncio
async def test_a_mangled_or_foreign_keyword_id_never_reaches_the_database(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Live 2026-09-15…18: the model echoed a UUID back with a dropped
    character, the lookup raised ParameterError (invalid input syntax for type
    uuid) and the whole batch — and the nightly — died. A non-UUID, or a UUID
    this batch never sent, is reported missing and never looked up; the rest of
    the batch lands."""
    import matrx_seo.artifact_writers as writers

    sent = "9493a48e-dde8-4da8-ad03-719f807993cc"
    looked_up: list[str] = []
    updated: list[str] = []

    class FakeKeyword:
        def __init__(self, kid: str) -> None:
            self.id = kid
            self.organization_id = "org-sys"
            self.phrase = "crt tv disposal"

        async def update(self, **_fields: object) -> None:
            updated.append(self.id)

    async def load(kid: str):
        looked_up.append(kid)
        return FakeKeyword(kid)

    async def fake_write(**_kwargs: object) -> int:
        return 0

    monkeypatch.setattr(writers.m.Keyword, "load_by_id_or_none", staticmethod(load))
    monkeypatch.setattr(writers, "_write_keyword_facets", fake_write)

    batch = {
        "classifier_version": "kwclass-v2.20260824000000",
        "results": [
            {"keyword_id": "9493a48e-de8-4da8-ad03-719f807993cc", "overall_confidence": 80},
            {"keyword_id": "3f9c52e5-\u6574\u6cbb4d94-b82a-1d3134a0ffe8", "overall_confidence": 80},
            {"keyword_id": "11111111-2222-4333-8444-555555555555", "overall_confidence": 80},
            {"keyword_id": sent.upper(), "overall_confidence": 80},
        ],
    }
    summary = await writers.apply_keyword_classifications(
        batch, vocabulary=_guard_vocabulary(), allowed_keyword_ids={sent}
    )

    assert looked_up == [sent]
    assert updated == [sent]
    assert summary["updated"] == 1
    assert len(summary["missing_keyword_ids"]) == 3
