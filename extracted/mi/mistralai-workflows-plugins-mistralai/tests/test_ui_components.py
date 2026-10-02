from pydantic import TypeAdapter

from mistralai.workflows.plugins.mistralai.conversational_ui_components import (
    LLM_UI_VERSION,
    Alert,
    Badge,
    Card,
    Chart,
    Column,
    Markdown,
    Row,
)


def _dump(obj):
    """Serialize a Pydantic model via the same path used in task.py."""
    return TypeAdapter(object).dump_python(obj, mode="json")


# --- LLM_UI_VERSION ---


def test_llm_ui_version_is_set():
    assert isinstance(LLM_UI_VERSION, str)
    assert len(LLM_UI_VERSION) > 0


# --- Serialization: optional fields ---


def test_none_optional_fields_omitted():
    a = Alert()
    assert _dump(a) == {"name": "Alert", "props": {}}


def test_card_no_children_omitted():
    c = Card(title="X")
    result = _dump(c)
    assert "children" not in result["props"]


# --- Serialization: children variants ---


def test_children_as_str():
    card = Card(title="Hello", children="some text")
    result = _dump(card)
    assert result["props"]["children"] == "some text"


def test_nested_tree():
    tree = Column(
        gap="md",
        children=[
            Card(
                title="Summary",
                children=[Markdown(content="**Score:** 0.82")],
            ),
            Row(
                gap="sm",
                children=[Badge(variant="success"), Badge(variant="error")],
            ),
        ],
    )
    result = _dump(tree)
    assert result["name"] == "Column"
    assert result["props"]["gap"] == "md"
    children = result["props"]["children"]
    assert len(children) == 2

    card = children[0]
    assert card["name"] == "Card"
    assert card["props"]["title"] == "Summary"
    assert card["props"]["children"][0] == {
        "name": "Markdown",
        "props": {"content": "**Score:** 0.82"},
    }

    row = children[1]
    assert row["name"] == "Row"
    assert len(row["props"]["children"]) == 2


# --- Serialization: list[dict] fields ---


def test_list_of_dicts_serialized_as_plain_dicts():
    chart = Chart(
        variant="bar",
        data=[{"x": "Jan", "y": 10}, {"x": "Feb", "y": 20}],
        xAxis="x",
        yAxis="y",
    )
    result = _dump(chart)
    assert result["name"] == "Chart"
    assert result["props"]["data"] == [
        {"x": "Jan", "y": 10},
        {"x": "Feb", "y": 20},
    ]
