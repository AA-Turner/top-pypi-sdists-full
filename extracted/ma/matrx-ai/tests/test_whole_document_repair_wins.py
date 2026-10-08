"""A whole JSON document with one typo is the answer, never a fragment carved out of it.

Real failure (describe box, 2026-10-08): the agent returned an 8,363-character minified
``describe_template_result`` with ONE stray ``]`` after the template object. With no schema,
the brace-walker's first inner array won, so the mandate saw no ``template``/``notes`` and the
person got "its answer is missing template, notes".
"""

from matrx_ai.agents.response_parser import extract_json

BROKEN = (
    '{"__kind":"describe_template_result","template":{"id":"creator-post-tracker",'
    '"tables":[{"token":"brand","fields":[{"key":"brand_name"}]},{"token":"post","fields":[{"key":"title"}]}],'
    '"views":[{"name":"Post pipeline","table":"post","kind":"kanban","groupBy":"stage"}]}],'
    '"notes":["Every post starts as a TikTok."],"reuses":[]}'
)


def test_whole_document_with_a_stray_bracket_is_recovered_whole():
    value = extract_json(BROKEN)
    assert isinstance(value, dict)
    assert value["__kind"] == "describe_template_result"
    assert value["template"]["id"] == "creator-post-tracker"
    assert value["notes"] == ["Every post starts as a TikTok."]
    assert value["reuses"] == []


def test_valid_document_is_unchanged():
    ok = BROKEN.replace('"stage"}]}],', '"stage"}]},', 1)
    value = extract_json(ok)
    assert value["template"]["views"][0]["kind"] == "kanban"


def test_json_inside_prose_still_returns_the_embedded_block():
    value = extract_json('Here you go: {"a": [1, 2]} hope that helps')
    assert value == {"a": [1, 2]}


def test_garbage_is_not_invented():
    assert extract_json("{{{{ unbalanced") is None
