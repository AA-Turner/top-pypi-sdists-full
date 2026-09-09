import pytest
from matrx_scraper.parser.browser_json import decode_browser_json_document


def test_chromium_json_document_decodes_entities_once():
    assert decode_browser_json_document('<html><body><pre>{"title":"A &amp; B", "count":2}</pre></body></html>') == {'title': 'A & B', 'count': 2}


@pytest.mark.parametrize('html', ['<title>Client Challenge</title>', '<pre>not JSON</pre>', '<pre>{}</pre><pre>{}</pre>'])
def test_non_document_is_rejected(html):
    with pytest.raises(ValueError):
        decode_browser_json_document(html)
