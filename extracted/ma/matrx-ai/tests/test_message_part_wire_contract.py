from __future__ import annotations

import pytest
from pydantic import TypeAdapter, ValidationError

from matrx_ai.db.message_parts import UserInputPart, validate_message_content

ENTITY_PARTS = [
    ("input_agent", "agent_ids"),
    ("input_project", "project_ids"),
    ("input_agent_app", "agent_app_ids"),
    ("input_transcript", "transcript_ids"),
    ("input_transcript_session", "transcript_session_ids"),
    ("input_workbook", "workbook_ids"),
    ("input_document", "document_ids"),
]


@pytest.mark.parametrize(("part_type", "id_field"), ENTITY_PARTS)
def test_entity_input_parts_validate_at_the_persistence_boundary(
    part_type: str,
    id_field: str,
) -> None:
    stored = validate_message_content(
        [
            {
                "type": part_type,
                id_field: ["resource-id"],
                "convert_to_text": False,
                "optional_context": True,
                "keep_fresh": True,
                "editable": True,
                "template": "compact",
            }
        ]
    )[0]

    assert stored["type"] == part_type
    assert stored[id_field] == ["resource-id"]
    assert stored["convert_to_text"] is False
    assert stored["optional_context"] is True
    assert stored["keep_fresh"] is True
    assert stored["editable"] is True
    assert stored["template"] == "compact"


@pytest.mark.parametrize(("part_type", "id_field"), ENTITY_PARTS)
@pytest.mark.parametrize("payload", [None, [], [""]])
def test_entity_id_arrays_are_required_non_empty_and_contain_non_empty_ids(
    part_type: str,
    id_field: str,
    payload: list[str] | None,
) -> None:
    part = {"type": part_type}
    if payload is not None:
        part[id_field] = payload

    with pytest.raises(ValidationError):
        TypeAdapter(UserInputPart).validate_python(part)

    with pytest.raises(ValueError):
        validate_message_content([part])


def test_outbound_user_input_is_validated_but_remains_a_plain_dict() -> None:
    adapter = TypeAdapter(UserInputPart)
    result = adapter.validate_python(
        {
            "type": "input_webpage",
            "urls": [
                {
                    "url": "https://example.com",
                    "title": "Example",
                    "textContent": "Submitted snapshot",
                    "charCount": 18,
                }
            ],
        }
    )

    assert type(result) is dict
    assert result["urls"][0]["textContent"] == "Submitted snapshot"


def test_outbound_user_input_normalizes_legacy_media_without_rejecting_inline_bytes() -> None:
    result = TypeAdapter(UserInputPart).validate_python(
        {"type": "image", "base64_data": "aW1hZ2U=", "mime_type": "image/png"}
    )

    assert result == {
        "type": "media",
        "kind": "image",
        "base64_data": "aW1hZ2U=",
        "mime_type": "image/png",
    }


@pytest.mark.parametrize("part", [{}, {"type": "not_real"}, {"type": "media"}])
def test_outbound_user_input_rejects_missing_unknown_or_malformed_discriminators(
    part: dict[str, object],
) -> None:
    with pytest.raises(ValidationError):
        TypeAdapter(UserInputPart).validate_python(part)


def test_reference_mode_resource_object_requires_an_id() -> None:
    with pytest.raises(ValidationError):
        TypeAdapter(UserInputPart).validate_python({"type": "input_notes", "note_ids": [{}]})

    snapshot = TypeAdapter(UserInputPart).validate_python(
        {
            "type": "input_notes",
            "note_ids": [{"mode": "snapshot", "content": "Frozen note"}],
        }
    )
    assert snapshot["note_ids"][0]["mode"] == "snapshot"


def test_snapshot_resource_requires_real_inline_content() -> None:
    adapter = TypeAdapter(UserInputPart)
    with pytest.raises(ValidationError):
        adapter.validate_python(
            {"type": "input_notes", "note_ids": [{"mode": "snapshot"}]}
        )


@pytest.mark.parametrize("part_type,id_field", [("input_workbook", "workbook_ids"), ("input_document", "document_ids")])
def test_opaque_resources_reject_snapshot_refs(part_type: str, id_field: str) -> None:
    with pytest.raises(ValidationError):
        TypeAdapter(UserInputPart).validate_python(
            {
                "type": part_type,
                id_field: [{"mode": "snapshot", "content": "cannot hydrate a live tool"}],
            }
        )


EMPTY_PAYLOAD_PARTS = [
    ("input_webpage", "urls"),
    ("input_notes", "note_ids"),
    ("input_task", "task_ids"),
    ("input_table", "bookmarks"),
    ("input_list", "bookmarks"),
    ("input_data", "refs"),
]


@pytest.mark.parametrize(("part_type", "payload_field"), EMPTY_PAYLOAD_PARTS)
@pytest.mark.parametrize("payload", [None, []])
def test_resolvable_structured_payloads_are_required_and_non_empty(
    part_type: str,
    payload_field: str,
    payload: list[object] | None,
) -> None:
    part: dict[str, object] = {"type": part_type}
    if payload is not None:
        part[payload_field] = payload
    with pytest.raises(ValidationError):
        TypeAdapter(UserInputPart).validate_python(part)
    with pytest.raises(ValueError):
        validate_message_content([part])


@pytest.mark.parametrize(
    "ref",
    [
        {"ref_type": "db_record", "table": "notes", "id": "note-id"},
        {"ref_type": "db_query", "table": "tasks", "filter": {"status": "open"}},
        {
            "ref_type": "db_field",
            "table": "projects",
            "id": "project-id",
            "field_name": "name",
        },
    ],
)
def test_exact_data_ref_variants_validate(ref: dict[str, object]) -> None:
    result = TypeAdapter(UserInputPart).validate_python({"type": "input_data", "refs": [ref]})
    assert result["refs"][0]["ref_type"] == ref["ref_type"]


@pytest.mark.parametrize(
    "ref",
    [
        {"ref_type": "unknown", "table": "notes"},
        {"ref_type": "db_record", "table": "notes"},
        {"ref_type": "db_field", "table": "notes", "id": "note-id"},
        {"ref_type": "db_query", "table": "not_registered"},
        {"ref_type": "db_query", "table": "tasks", "surprise": True},
    ],
)
def test_malformed_data_refs_fail_at_ingress(ref: dict[str, object]) -> None:
    with pytest.raises(ValidationError):
        TypeAdapter(UserInputPart).validate_python({"type": "input_data", "refs": [ref]})


def test_outbound_json_schema_requires_discriminators() -> None:
    schema = TypeAdapter(UserInputPart).json_schema()
    definitions = schema["$defs"]

    assert "type" in definitions["WebpageInputPart"]["required"]
    assert {"type", "kind"}.issubset(definitions["UserImageMediaPart"]["required"])


@pytest.mark.parametrize(
    "part",
    [
        {"type": "media", "kind": "youtube", "url": ""},
        {
            "type": "input_webpage",
            "urls": [{"url": "", "textContent": "snapshot"}],
        },
        {
            "type": "input_webpage",
            "urls": [{"url": "https://example.com", "textContent": "x", "charCount": -1}],
        },
    ],
)
def test_web_sources_require_a_real_url_and_non_negative_character_count(
    part: dict[str, object],
) -> None:
    with pytest.raises(ValidationError):
        TypeAdapter(UserInputPart).validate_python(part)
    with pytest.raises(ValueError):
        validate_message_content([part])


@pytest.mark.parametrize(
    "bookmark",
    [
        {"type": "full_table", "table_id": ""},
        {"type": "table_schema", "table_id": ""},
        {"type": "table_column", "table_id": "", "column_name": "name"},
        {"type": "table_column", "table_id": "table", "column_name": ""},
        {"type": "table_row", "table_id": "table", "row_id": ""},
        {"type": "table_cell", "table_id": "table", "row_id": "", "column_name": "name"},
        {"type": "table_cell", "table_id": "table", "row_id": "row", "column_name": ""},
    ],
)
def test_table_bookmark_identity_fields_are_non_empty(bookmark: dict[str, str]) -> None:
    with pytest.raises(ValidationError):
        TypeAdapter(UserInputPart).validate_python(
            {"type": "input_table", "bookmarks": [bookmark]}
        )


@pytest.mark.parametrize(
    "bookmark",
    [
        {"type": "full_list", "list_id": ""},
        {"type": "list_group", "list_id": "", "group_name": "group"},
        {"type": "list_group", "list_id": "list", "group_name": ""},
        {"type": "list_item", "list_id": "", "item_id": "item"},
        {"type": "list_item", "list_id": "list", "item_id": ""},
    ],
)
def test_list_bookmark_identity_fields_are_non_empty(bookmark: dict[str, str]) -> None:
    with pytest.raises(ValidationError):
        TypeAdapter(UserInputPart).validate_python(
            {"type": "input_list", "bookmarks": [bookmark]}
        )
