from matrx_connect.emitters.log_truncation import is_scrape_data_log, truncate_strings_for_log


def test_is_scrape_data_log_recognizes_fetch_results() -> None:
    assert is_scrape_data_log({"type": "fetch_results", "results": []})
    assert is_scrape_data_log({"response_type": "fetch_results", "results": []})
    assert not is_scrape_data_log({"type": "search_results", "results": []})


def test_truncate_strings_for_log_limits_nested_strings() -> None:
    payload = {
        "type": "fetch_results",
        "results": [
            {
                "url": "https://example.com",
                "title": "x" * 120,
                "content": "y" * 200,
                "ai_content": "z" * 150,
            }
        ],
    }

    truncated = truncate_strings_for_log(payload)

    assert truncated["results"][0]["url"] == "https://example.com"
    assert truncated["results"][0]["title"] == "x" * 100 + "…[truncated 20 chars]"
    assert truncated["results"][0]["content"] == "y" * 100 + "…[truncated 100 chars]"
    assert truncated["results"][0]["ai_content"] == "z" * 100 + "…[truncated 50 chars]"
