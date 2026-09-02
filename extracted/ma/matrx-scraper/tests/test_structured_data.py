from __future__ import annotations

from matrx_scraper.structured_data import (
    extract_structured_data,
    extract_structured_payload,
)


def test_extract_structured_data_flattens_graph_and_finds_microdata() -> None:
    html = """
    <html><head>
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@graph": [
        {"@type": "Article", "headline": "Hello", "image": "https://x/img.jpg", "datePublished": "2026-01-01"},
        {"@type": "Organization", "name": "Acme", "url": "https://acme.example"}
      ]
    }
    </script>
    </head>
    <body>
      <div itemscope itemtype="https://schema.org/Product">
        <span itemprop="name">Widget</span>
      </div>
    </body></html>
    """
    blocks = extract_structured_data(html, "https://example.com/")
    sources = {b.source for b in blocks}
    assert "json-ld" in sources
    assert "microdata" in sources
    json_ld_types = {t for b in blocks if b.source == "json-ld" for t in b.types}
    assert "Article" in json_ld_types
    assert "Organization" in json_ld_types
    microdata_types = {t for b in blocks if b.source == "microdata" for t in b.types}
    assert "Product" in microdata_types


def test_extract_structured_data_empty_html_returns_empty_list() -> None:
    assert extract_structured_data("", "https://example.com/") == []
    assert extract_structured_data("<html></html>", "") == []


def test_extract_structured_data_malformed_json_ld_is_skipped_not_raised() -> None:
    html = '<script type="application/ld+json">{not valid json</script>'
    assert extract_structured_data(html, "https://example.com/") == []


def test_complete_payload_preserves_every_raw_json_ld_script() -> None:
    html = """
    <script type="application/ld+json">
      {"@type":"Article","headline":"One"}
    </script>
    <script type="application/ld+json">
      [{"@type":"VideoObject","name":"Two"},{"name":"Untyped evidence"}]
    </script>
    <script type="application/ld+json">{broken</script>
    """

    payload = extract_structured_payload(html, "https://example.com/")

    assert len(payload.json_ld_raw) == 3
    assert len(payload.json_ld) == 2
    assert payload.schema_types == ["Article", "VideoObject"]
    assert [block.data.get("name") for block in payload.blocks] == [
        None,
        "Two",
        "Untyped evidence",
    ]
    assert payload.blocks[-1].types == []
    assert payload.parse_errors[0]["source"] == "json-ld"
