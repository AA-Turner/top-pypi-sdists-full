"""A useful first glance is small; explicit detail reads remain lossless."""

from __future__ import annotations

from copy import deepcopy
from types import SimpleNamespace
from uuid import uuid4

import pytest

from probe.mcp.contract import EntityType, View
from probe.mcp.service import ResearchReadService, _NOTES_CARD_EXCERPT, _VIEWS, _notes_excerpt
from probe.mcp.source import ResearchOSSource
from probe.sdk import errors


class EntitySource:
    def __init__(self, kind, entity):
        self.kind = kind
        self.entity = entity
        self.reads = []
        self.client = SimpleNamespace(list_sub_notes=lambda *_: {"sub_notes": []})

    def get(self, ref):
        self.reads.append(ref)
        return self.kind, deepcopy(self.entity)

    def identity(self):
        return {"customer_id": "synthetic"}

    def capabilities(self):
        return {}


# Every kind whose compact card has the lossless RECORD read behind it. A
# sub-note is the one card-only kind (VIEW_MATRIX): its card IS the whole
# document, which tests/test_mcp_read_gaps.py pins.
_KINDS = sorted({kind for kind, view in _VIEWS if view == View.RECORD})


@pytest.mark.parametrize("kind", _KINDS)
def test_each_kind_has_a_compact_glance_and_exact_record_without_extra_reads(kind):
    entity = {
        "id": "one",
        "name": "Held-out evaluation",
        "kind": "inference",
        "status": "completed",
        "description": "Compare the held-out split.",
        "question": "Does rank 16 preserve accuracy?",
        "tags": ["lora", "eval"],
        "counts": {"metrics": 12},
        "run_count": 4,
        "active_run_count": 0,
        "summary": {"accuracy": 0.945, "analysis_tokens": 0},
        "notes": "Caveat: this is the held-out split.\n" + "unused history\n" * 2000,
        "config": {"model": "synthetic-model", "payload": "配置" * 10000},
        "metadata": {"long_trace": "trace" * 10000},
        "document": "# Full protocol\n" * 2000,
        "spec": {"rank": [8, 16, 32]},
    }
    source = EntitySource(kind, entity)
    service = ResearchReadService(source)
    card = service.get_entity(f"{kind}:one")

    assert source.reads == [f"{kind}:one"]
    assert card["data"]["entity"]["name"] == "Held-out evaluation"
    assert card["data"]["entity"]["summary"]["accuracy"] == 0.945
    assert View.RECORD in card["data"]["available_views"]
    assert not {"notes", "config", "metadata", "document"} & card["data"]["entity"].keys()
    assert len(str(card)) < 4500
    assert "completeness" not in card
    assert "next_cursor" not in card
    if kind in {
        EntityType.PROJECT, EntityType.EXPERIMENT, EntityType.RUN,
        EntityType.GROUP, EntityType.ARTIFACT,
    }:
        assert card["data"]["notes"]["text"].startswith("Caveat: this is the held-out split.")
        assert card["data"]["notes"]["truncated"] is True

    record = service.get_entity(f"{kind}:one", view=View.RECORD, token_budget=1000000)
    assert record["data"]["record"] == entity
    assert source.entity == entity
    assert source.reads == [f"{kind}:one"] * 2


@pytest.mark.parametrize("text", [None, "", "Short caveat.", "x" * _NOTES_CARD_EXCERPT])
def test_notes_excerpt_distinguishes_absence_and_complete_short_notes(text):
    excerpt = _notes_excerpt(text)
    if not text:
        assert excerpt is None
    else:
        assert excerpt == {"text": text, "truncated": False}


@pytest.mark.parametrize("kind", [EntityType.PROJECT, EntityType.EXPERIMENT, EntityType.RUN, EntityType.GROUP])
def test_existing_note_carriers_keep_their_supported_detail_door(kind):
    source = EntitySource(kind, {"id": "one", "notes": "caveat\n" * 500})
    service = ResearchReadService(source)
    data = service.get_entity(f"{kind}:one")["data"]
    assert data["notes"]["truncated"] is True
    assert data["notes"]["read_all"] == 'view="notes"'
    assert View.NOTES in data["available_views"]


@pytest.mark.parametrize("body", ["Do not reuse: scorer used the stale split.", "Caveat: stale split.\n" * 500])
def test_artifact_card_keeps_authored_notes_with_a_valid_record_detail_door(body):
    source = EntitySource(EntityType.ARTIFACT, {"id": "one", "name": "scorer.py", "notes": body})
    service = ResearchReadService(source)
    data = service.get_entity("artifact:one")["data"]
    assert data["notes"]["text"] == body[:_NOTES_CARD_EXCERPT]
    assert data["notes"]["truncated"] is (len(body) > _NOTES_CARD_EXCERPT)
    assert View.NOTES not in data["available_views"]
    if len(body) > _NOTES_CARD_EXCERPT:
        assert data["notes"]["read_all"] == 'view="record", view_options={"field":"notes"}'
    else:
        assert "read_all" not in data["notes"]
    assert source.reads == ["artifact:one"]
    full = service.get_entity("artifact:one", view=View.RECORD, filters={"field": "notes"})
    assert full["data"]["record"] == body
    assert "notes" not in full["data"]["entity"]


def test_nonshared_artifact_actual_id_resolution_preserves_its_limitation(client, app):
    artifact_id = str(uuid4())
    app.artifacts["owning-run"] = [{"id": artifact_id, "name": "private-scorer.py", "notes": "private caveat"}]
    service = ResearchReadService(ResearchOSSource(client))
    start = len(app.requests)

    card = service.get_entity(f"artifact:{artifact_id}")

    entity = card["data"]["entity"]
    assert entity["id"] == artifact_id and entity["shared"] is False
    assert "exists but is not shared" in entity["resolution_note"]
    assert "only its id and version chain are readable" in entity["resolution_note"]
    assert len(entity["resolution_note"]) <= 480
    assert entity["read_versions"] == 'view="versions"'
    assert "name" not in entity and "notes" not in card["data"]
    # The ordinary envelope may also initialize the cached /v1/me identity.
    assert [r.url.path for r in app.requests[start:] if r.url.path != "/v1/me"] == [
        "/v1/shared/files", f"/v1/artifacts/{artifact_id}/versions",
    ]
    # The suggested read is real even when there are no versions yet. It must
    # not imply that RECORD can resolve the unavailable name/metadata/notes.
    versions = service.get_entity(f"artifact:{artifact_id}", view=View.VERSIONS)
    assert versions["data"]["versions"] == []
    record = service.get_entity(f"artifact:{artifact_id}", view=View.RECORD)
    assert record["data"]["record"]["shared"] is False
    assert "name" not in record["data"]["record"]


class IntentSource(EntitySource):
    def __init__(self, kind, entity, intent):
        super().__init__(kind, entity)
        self._intent = intent
        self.intent_reads = []

    def intent(self, kind, entity_id):
        self.intent_reads.append((kind, entity_id))
        return self._intent


_INTENT = {
    "entity_type": "run", "entity_id": "one", "ask": "now try lr 3e-4 with the same warmup",
    "ask_truncated": False, "match": "exact", "context": None, "session_goal": "fix the spike",
    "queued": False, "asked_at": "2026-09-30T14:20:00+00:00", "asked_by": "u-1",
    "asked_by_name": "Researcher A", "session": "claude_code/s-1", "step_id": 5,
    "provisional": False,
}


@pytest.mark.parametrize("kind", [EntityType.RUN, EntityType.EXPERIMENT, EntityType.PROJECT])
def test_cards_carry_the_researchers_ask(kind):
    source = IntentSource(kind, {"id": "one", "name": "lr-3e-4"}, dict(_INTENT))
    card = ResearchReadService(source).get_entity(f"{kind}:one")["data"]
    assert card["intent"]["ask"] == "now try lr 3e-4 with the same warmup"
    assert card["intent"]["match"] == "exact"
    assert card["intent"]["asked_by_name"] == "Researcher A"
    # Internal ids and nulls do not ride the card.
    assert "asked_by" not in card["intent"] and "context" not in card["intent"]
    assert source.intent_reads == [(kind, "one")]


def test_only_the_card_reads_intent_and_other_kinds_never_do():
    source = IntentSource(EntityType.RUN, {"id": "one"}, dict(_INTENT))
    ResearchReadService(source).get_entity("run:one", view=View.RECORD, token_budget=100000)
    assert source.intent_reads == []
    artifact = IntentSource(EntityType.ARTIFACT, {"id": "a"}, dict(_INTENT))
    card = ResearchReadService(artifact).get_entity("artifact:a")["data"]
    assert "intent" not in card and artifact.intent_reads == []


@pytest.mark.parametrize("found", [None, {}, {"ask": ""}, "junk"])
def test_no_known_ask_leaves_the_card_without_intent(found):
    card = ResearchReadService(IntentSource(EntityType.RUN, {"id": "one"}, found)).get_entity(
        "run:one"
    )["data"]
    assert "intent" not in card


def test_a_source_without_the_intent_read_still_serves_a_card():
    card = ResearchReadService(EntitySource(EntityType.RUN, {"id": "one"})).get_entity("run:one")
    assert "intent" not in card["data"]


def test_the_intent_read_swallows_transport_errors():
    calls = []

    def boom(path, **_):
        calls.append(path)
        raise errors.NotFoundError("no intent recorded")

    source = ResearchOSSource.__new__(ResearchOSSource)
    source.client = SimpleNamespace(transport=SimpleNamespace(get=boom))
    assert source.intent("run", "one") is None
    assert calls == ["/v1/intent/run/one"]


class PageSource(EntitySource):
    """A source whose Overview page read answers `page` (or raises it)."""

    def __init__(self, kind, entity, page):
        super().__init__(kind, entity)
        self._page = page
        self.page_reads = []

    def project_overview(self, project_id):
        self.page_reads.append(("project", project_id))
        if isinstance(self._page, Exception):
            raise self._page
        return self._page

    def experiment_overview(self, experiment_id, *, project_id=None):
        self.page_reads.append(("experiment", experiment_id))
        if isinstance(self._page, Exception):
            raise self._page
        return self._page


_PAGE = {"anchor_type": "project", "anchor_id": "one", "content": "fresh", "html": "<p>x</p>",
         "blurb": "Warmup 500 removed the 7B spike; lr 3e-4 is next.", "version": 3,
         "saved_page_readable": True}


@pytest.mark.parametrize("kind", [EntityType.PROJECT, EntityType.EXPERIMENT])
def test_project_and_experiment_cards_carry_the_pages_blurb(kind):
    source = PageSource(kind, {"id": "one", "name": "warmup"}, dict(_PAGE))
    card = ResearchReadService(source).get_entity(f"{kind}:one")["data"]
    assert card["blurb"] == "Warmup 500 removed the 7B spike; lr 3e-4 is next."
    assert source.page_reads == [(str(kind), "one")]


def test_a_withheld_page_gives_the_card_no_blurb():
    """The page is written over the project's whole family; a caller refused it
    (a project in that family hidden from them) gets no blurb on the card either."""
    withheld = {**_PAGE, "content": "absent", "saved_page_readable": False}
    card = ResearchReadService(PageSource(EntityType.PROJECT, {"id": "one"}, withheld)).get_entity(
        "project:one"
    )["data"]
    assert "blurb" not in card


@pytest.mark.parametrize("page", [errors.NotFoundError("no page"), RuntimeError("boom"), {"blurb": ""}, {}])
def test_no_blurb_or_a_failed_page_read_leaves_the_card_as_it_was(page):
    card = ResearchReadService(PageSource(EntityType.PROJECT, {"id": "one"}, page)).get_entity(
        "project:one"
    )["data"]
    assert "blurb" not in card and card["entity_type"] == EntityType.PROJECT


def test_only_project_and_experiment_cards_read_the_page():
    source = PageSource(EntityType.RUN, {"id": "one"}, dict(_PAGE))
    card = ResearchReadService(source).get_entity("run:one")["data"]
    assert "blurb" not in card and source.page_reads == []
    record = PageSource(EntityType.PROJECT, {"id": "one"}, dict(_PAGE))
    ResearchReadService(record).get_entity("project:one", view=View.RECORD, token_budget=100000)
    assert record.page_reads == []


def test_artifact_resolution_note_is_bounded_without_losing_the_versions_door():
    source = EntitySource(EntityType.ARTIFACT, {
        "id": "one", "shared": False, "resolution_note": "Metadata unavailable. " * 1000,
    })
    card = ResearchReadService(source).get_entity("artifact:one")["data"]["entity"]
    assert card["shared"] is False and card["resolution_note_truncated"] is True
    assert len(card["resolution_note"]) == 480
    assert card["read_versions"] == 'view="versions"'


@pytest.mark.parametrize(
    "field, expected",
    [
        ("config.rank", 16),
        ("$.config.rank", 16),
        (["config", "loss.final"], 0.0),
        (["config", "flags", 0], False),
        (["config", "flags", 1], None),
        ("notes", "完整文档\n" * 1000),
    ],
)
def test_record_can_select_exact_nested_data_without_reading_other_fields(field, expected):
    source = EntitySource(
        EntityType.RUN,
        {
            "id": "one",
            "notes": "完整文档\n" * 1000,
            "config": {"rank": 16, "loss.final": 0.0, "flags": [False, None]},
            "metadata": {"irrelevant": "x" * 100000},
        },
    )
    result = ResearchReadService(source).get_entity(
        "run:one", view=View.RECORD, filters={"field": field}, token_budget=1000000
    )
    assert result["data"]["record"] == expected
    assert "metadata" not in str(result)
    assert source.reads == ["run:one"]


@pytest.mark.parametrize("field", ["", [], None, True, 3, ["config", -1], ["config", True]])
def test_invalid_field_never_falls_back_to_full_record(field):
    source = EntitySource(EntityType.RUN, {"id": "one", "config": {"rank": 16}})
    with pytest.raises(errors.ValidationError, match="field"):
        ResearchReadService(source).get_entity(
            "run:one", view=View.RECORD, filters={"field": field}
        )


def test_missing_field_is_distinct_from_present_null():
    source = EntitySource(EntityType.RUN, {"id": "one", "config": {"rank": None}})
    with pytest.raises(errors.NotFoundError, match="field"):
        ResearchReadService(source).get_entity(
            "run:one", view=View.RECORD, filters={"field": ["config", "other"]}
        )


def test_large_trial_description_and_group_spec_have_explicit_detail_access():
    trial = EntitySource(
        EntityType.TRIAL, {"id": "one", "description": "Authored diagnosis. " * 100}
    )
    service = ResearchReadService(trial)
    card = service.get_entity("trial:one")["data"]
    assert card["entity"]["description"].startswith("Authored diagnosis.")
    assert card["entity"]["description_truncated"] is True
    assert (
        service.get_entity("trial:one", view=View.RECORD, filters={"field": "description"})["data"][
            "record"
        ]
        == trial.entity["description"]
    )

    group = EntitySource(EntityType.GROUP, {"id": "one", "spec": {"rank": list(range(1000))}})
    service = ResearchReadService(group)
    card = service.get_entity("group:one")["data"]
    assert card["entity"]["spec_truncated"] is True
    assert "spec" not in card["entity"]  # an incomplete sweep must not look executable
    assert (
        service.get_entity("group:one", view=View.RECORD, filters={"field": "spec"})["data"][
            "record"
        ]
        == group.entity["spec"]
    )


def test_session_card_keeps_inventory_and_exact_counts_with_one_source_read():
    source = EntitySource(
        EntityType.SESSION,
        {
            "id": "one",
            "agent": "codex",
            "name": "Evaluation changes",
            "projects": [{"id": "p1", "name": "Fine tuning"}],
            "experiments": [],
            "runs": [
                {"id": str(i), "name": f"Run {i}", "metadata": {"large": "x" * 10000}}
                for i in range(20)
            ],
            "artifacts": None,
        },
    )
    card = ResearchReadService(source).get_entity("session:one")["data"]["entity"]
    assert card["projects"] == [{"id": "p1", "name": "Fine tuning"}]
    assert card["experiments"] == [] and card["artifacts"] is None
    assert card["runs_count"] == 20 and card["runs_truncated"] is True
    assert len(card["runs"]) == 8
    assert "metadata" not in str(card)
    assert source.reads == ["session:one"]


def test_requested_documents_have_one_body_and_keep_existing_version():
    body = "# A useful document\n" * 100
    source = EntitySource(
        EntityType.PROJECT,
        {
            "id": "one",
            "name": "Research",
            "notes": body,
            "notes_version": 7,
            "document": body,
            "metadata": {"large": "x" * 10000},
        },
    )
    service = ResearchReadService(source)
    notes = service.get_entity("project:one", view=View.NOTES, token_budget=100000)
    assert notes["data"]["notes"] == body
    assert notes["data"]["notes_version"] == 7
    assert "notes" not in notes["data"]["entity"]
    summary = service.get_entity("project:one", view=View.SUMMARY, token_budget=100000)
    assert summary["data"]["project_summary"] == {"document": body}
    assert "document" not in summary["data"]["entity"]
    assert "metadata" not in str(notes) + str(summary)


def test_team_note_delivers_briefing_text_immediately():
    body = "# Team briefing\n" * 1000
    source = EntitySource(EntityType.TEAM_NOTE, {"body": body, "version": 4})
    result = ResearchReadService(source).get_entity("team-note", token_budget=100000)
    assert result["data"]["entity"] == {"body": body, "version": 4}
    assert source.reads == ["team-note"]


def test_reproduction_is_preserved_without_duplicating_the_original_entity():
    source = EntitySource(
        EntityType.RUN, {"id": "one", "notes": "private notes" * 1000, "config": {"rank": 16}}
    )
    manifest = {
        "run": {"id": "one", "config": {"rank": 16}},
        "completeness": {"missing": ["execution_record"]},
    }
    source.reproduce = lambda _: deepcopy(manifest)
    result = ResearchReadService(source).get_entity("run:one", view=View.REPRODUCE)
    assert result["data"]["run"] == manifest["run"]
    assert result["data"]["entity"] == {"id": "one"}
    assert result["completeness"]["missing"] == ["execution_record"]


@pytest.mark.parametrize("empty", [{}, ""])
def test_an_empty_summary_is_omitted_like_an_absent_one(empty):
    from probe.mcp.service import _entity_projection

    entity = {"id": str(uuid4()), "name": "n", "slug": "s", "summary_metrics": empty}
    assert "summary" not in _entity_projection(EntityType.PROJECT, entity, card=False, document=True)
    entity["summary_metrics"] = {"accuracy": 0.9}
    shown = _entity_projection(EntityType.PROJECT, entity, card=False, document=True)
    assert shown["summary"] == {"accuracy": 0.9}


def test_a_summary_emptied_by_truncation_is_still_shown_beside_its_flag():
    from probe.mcp.service import _entity_projection

    entity = {"id": str(uuid4()), "name": "n", "slug": "s", "summary_metrics": {"loss": {"min": 1}}}
    shown = _entity_projection(EntityType.PROJECT, entity, card=False, document=True)
    assert shown["summary"] == {} and shown["summary_truncated"] is True


def test_a_summary_of_the_wrong_type_is_flagged_not_shown_as_null():
    from probe.mcp.service import _entity_projection

    entity = {"id": str(uuid4()), "name": "n", "slug": "s", "summary_metrics": ["x"]}
    shown = _entity_projection(EntityType.PROJECT, entity, card=False, document=True)
    assert "summary" not in shown and shown["summary_truncated"] is True


# ---------------------------------------------------------------------------
# Forks (CONTRACT.md, Forks): the card names the source, counts the forks and
# points at what a fork reads -- each only when it says something.
# ---------------------------------------------------------------------------

_SOURCE = {
    "id": "src-1",
    "slug": "warmup-500",
    "name": "Warmup 500",
    "project_id": "proj-1",
    "forked_at": "2026-10-12T05:00:00Z",
}


def _experiment_card(**fork_fields):
    entity = {"id": "one", "name": "lr sweep", "question": "Does lr 3e-4 help?"} | fork_fields
    return ResearchReadService(EntitySource(EntityType.EXPERIMENT, entity)).get_entity(
        "experiment:one"
    )["data"]["entity"]


def test_a_fork_card_names_its_source_and_where_it_inherits():
    card = _experiment_card(forked_from=dict(_SOURCE), fork_count=0, inherits=True)
    assert card["forked_from"] == {
        "id": "src-1",
        "slug": "warmup-500",
        "name": "Warmup 500",
        "forked_at": "2026-10-12T05:00:00Z",
    }
    assert card["read_inherited"].startswith('view="inherited"')
    assert '"runs": true' in card["read_inherited"]
    assert "fork_count" not in card


def test_a_source_card_counts_its_forks_and_is_no_fork_itself():
    card = _experiment_card(forked_from=None, fork_count=2, inherits=False)
    assert card["fork_count"] == 2
    assert "forked_from" not in card
    assert "read_inherited" not in card


def test_a_fork_whose_source_is_in_the_trash_still_points_at_what_it_inherits():
    """`forked_from` is null for a source in the trash; the fork still reads
    through it, so the hint keys on `inherits`."""
    card = _experiment_card(forked_from=None, fork_count=0, inherits=True)
    assert "forked_from" not in card
    assert card["read_inherited"].startswith('view="inherited"')


def test_an_experiment_with_no_fork_either_way_keeps_its_card():
    plain = _experiment_card()
    with_defaults = _experiment_card(forked_from=None, fork_count=0, inherits=False)
    assert with_defaults == plain
    assert not {"forked_from", "fork_count", "read_inherited"} & plain.keys()


def test_a_long_source_name_is_cut_and_says_so():
    long = dict(_SOURCE, name="n" * 1000)
    card = _experiment_card(forked_from=long, inherits=True)
    assert len(card["forked_from"]["name"]) < 1000
    assert card["forked_from"]["name_truncated"] is True


def test_a_run_card_never_carries_fork_facts():
    entity = {"id": "one", "name": "r", "forked_from": dict(_SOURCE), "fork_count": 3}
    card = ResearchReadService(EntitySource(EntityType.RUN, entity)).get_entity("run:one")
    assert not {"forked_from", "fork_count", "read_inherited"} & card["data"]["entity"].keys()
