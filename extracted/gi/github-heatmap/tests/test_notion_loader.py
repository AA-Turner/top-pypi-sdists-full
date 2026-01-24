import requests

from github_heatmap.loader import notion_loader
from github_heatmap.loader.notion_loader import NotionLoader


def build_loader():
    return NotionLoader(
        2024,
        2024,
        "notion",
        notion_token="token",
        database_id="db",
        date_prop_name="Date",
        value_prop_name="Value",
        tooltip_prop_name="Tooltip",
    )


def test_notion_loader_make_track_dict_with_tooltips():
    loader = build_loader()

    loader.get_api_data = lambda: [
        {
            "properties": {
                "Date": {"date": {"start": "2024-01-01"}},
                "Value": {"type": "number", "number": 5},
                "Tooltip": {
                    "type": "rich_text",
                    "rich_text": [{"plain_text": "Study"}],
                },
            }
        },
        {
            "properties": {
                "Date": {"date": {"start": "2024-01-01"}},
                "Value": {"type": "number", "number": 2},
                "Tooltip": {
                    "type": "multi_select",
                    "multi_select": [{"name": "Read"}, {"name": "Write"}],
                },
            }
        },
    ]

    loader.make_track_dict()

    assert loader.number_by_date_dict["2024-01-01"] == 7
    assert (
        loader.tooltip_by_date_dict["2024-01-01"]
        == "Study\nRead, Write"
    )


def test_notion_loader_extract_property_text_variants():
    rich_text = {
        "type": "rich_text",
        "rich_text": [{"plain_text": "Hello"}, {"plain_text": " World"}],
    }
    assert NotionLoader._extract_property_text(rich_text) == "Hello World"

    select = {
        "type": "select",
        "select": {"name": "Done"},
    }
    assert NotionLoader._extract_property_text(select) == "Done"

    multi_select = {
        "type": "multi_select",
        "multi_select": [{"name": "Tag1"}, {"name": "Tag2"}],
    }
    assert NotionLoader._extract_property_text(multi_select) == "Tag1, Tag2"

    formula_number = {
        "type": "formula",
        "formula": {"type": "number", "number": 42},
    }
    assert NotionLoader._extract_property_text(formula_number) == "42"

    rollup_array = {
        "type": "rollup",
        "rollup": {
            "type": "array",
            "array": [
                {
                    "type": "rich_text",
                    "rich_text": [{"plain_text": "Note"}],
                },
                {
                    "type": "people",
                    "people": [{"name": "Alice"}, {"name": "Bob"}],
                },
            ],
        },
    }
    assert NotionLoader._extract_property_text(rollup_array) == "Note, Alice, Bob"


def test_notion_loader_handles_http_error(monkeypatch):
    loader = build_loader()

    class DummyResp:
        ok = False
        status_code = 404

        @staticmethod
        def json():
            return {"object": "error"}

    monkeypatch.setattr(
        notion_loader.requests, "post", lambda *args, **kwargs: DummyResp()
    )

    tracks, years = loader.get_all_track_data()

    assert years == [2024]
    assert tracks
    assert all(value == 0 for value in tracks.values())
    assert loader.number_list


def test_notion_loader_handles_request_exception(monkeypatch):
    loader = build_loader()

    def fake_post(*args, **kwargs):
        raise requests.RequestException("boom")

    monkeypatch.setattr(notion_loader.requests, "post", fake_post)

    tracks, years = loader.get_all_track_data()

    assert years == [2024]
    assert tracks
    assert all(value == 0 for value in tracks.values())
    assert loader.number_list
