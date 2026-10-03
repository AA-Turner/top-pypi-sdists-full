"""A field shared by several actions reaches the model with EVERY action's meaning.

Flattening ``$variants`` merged root + first variant, so the first action's text for a shared
field was all the model read (google_workspace: ``file_id`` = "the Google Sheet's file id" on
every action). Guard for ``_with_action_descriptions``.
"""

from matrx_ai.tools.models import ToolDefinition


def _tool(root_file_id: dict) -> ToolDefinition:
    return ToolDefinition(
        name="ws",
        description="Workspace.",
        parameters={
            "action": {"type": "string", "enum": ["read_sheet", "read_doc"], "required": True},
            "file_id": root_file_id,
            "$variants": {
                "read_sheet": {"type": "object", "properties": {
                    "action": {"const": "read_sheet"},
                    "file_id": {"type": "string", "description": "The Google Sheet's file id."}},
                    "required": ["file_id"]},
                "read_doc": {"type": "object", "properties": {
                    "action": {"const": "read_doc"},
                    "file_id": {"type": "string", "description": "The Google Doc's file id."}},
                    "required": ["file_id"]},
            },
        },
    )


def test_differing_action_texts_are_all_rendered() -> None:
    desc = _tool({"type": "string"}).to_anthropic_format()["input_schema"]["properties"]["file_id"]["description"]
    assert "Sheet" in desc and "Doc" in desc
    assert "read_sheet:" in desc and "read_doc:" in desc


def test_deliberate_root_union_text_wins() -> None:
    root = {"type": "string", "description": "read_sheet, read_doc: the file id."}
    desc = _tool(root).to_anthropic_format()["input_schema"]["properties"]["file_id"]["description"]
    assert desc == "read_sheet, read_doc: the file id."


def test_stale_root_copy_of_first_variant_does_not_hide_the_others() -> None:
    root = {"type": "string", "description": "The Google Sheet's file id."}
    desc = _tool(root).to_anthropic_format()["input_schema"]["properties"]["file_id"]["description"]
    assert "Doc" in desc
