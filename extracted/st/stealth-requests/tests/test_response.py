from types import SimpleNamespace

from stealth_requests.response import StealthResponse


def make_response(html, url='https://example.com'):
    """Create a StealthResponse from raw HTML and a fake URL."""
    raw = SimpleNamespace(
        content=html.encode(),
        text=html,
        url=url,
        status_code=200,
    )
    return StealthResponse(raw, elapsed=0.1)


# ── Tables ──────────────────────────────────────────────────────────────


class TestTables:
    def test_basic_thead_tbody(self):
        html = """
        <html><body>
        <table>
            <thead><tr><th>Name</th><th>Age</th></tr></thead>
            <tbody>
                <tr><td>Alice</td><td>30</td></tr>
                <tr><td>Bob</td><td>25</td></tr>
            </tbody>
        </table>
        </body></html>
        """
        resp = make_response(html)
        assert resp.tables == [{'Name': ['Alice', 'Bob'], 'Age': ['30', '25']}]

    def test_table_without_thead(self):
        html = """
        <html><body>
        <table>
            <tr><th>Color</th><th>Hex</th></tr>
            <tr><td>Red</td><td>#FF0000</td></tr>
            <tr><td>Blue</td><td>#0000FF</td></tr>
        </table>
        </body></html>
        """
        resp = make_response(html)
        assert resp.tables == [{'Color': ['Red', 'Blue'], 'Hex': ['#FF0000', '#0000FF']}]

    def test_multiple_tables(self):
        html = """
        <html><body>
        <table>
            <thead><tr><th>X</th></tr></thead>
            <tbody><tr><td>1</td></tr></tbody>
        </table>
        <table>
            <thead><tr><th>Y</th></tr></thead>
            <tbody><tr><td>2</td></tr></tbody>
        </table>
        </body></html>
        """
        resp = make_response(html)
        assert len(resp.tables) == 2
        assert resp.tables[0] == {'X': ['1']}
        assert resp.tables[1] == {'Y': ['2']}

    def test_table_no_headers_skipped(self):
        html = """
        <html><body>
        <table>
            <tr><td>no</td><td>headers</td></tr>
            <tr><td>at</td><td>all</td></tr>
        </table>
        </body></html>
        """
        resp = make_response(html)
        assert resp.tables == []

    def test_table_empty_headers_skipped(self):
        html = """
        <html><body>
        <table>
            <thead><tr><th></th><th></th></tr></thead>
            <tbody><tr><td>a</td><td>b</td></tr></tbody>
        </table>
        </body></html>
        """
        resp = make_response(html)
        assert resp.tables == []

    def test_row_with_fewer_cells(self):
        html = """
        <html><body>
        <table>
            <thead><tr><th>A</th><th>B</th><th>C</th></tr></thead>
            <tbody>
                <tr><td>1</td><td>2</td></tr>
            </tbody>
        </table>
        </body></html>
        """
        resp = make_response(html)
        assert resp.tables == [{'A': ['1'], 'B': ['2'], 'C': ['']}]

    def test_tables_cached(self):
        html = """
        <html><body>
        <table>
            <thead><tr><th>Col</th></tr></thead>
            <tbody><tr><td>val</td></tr></tbody>
        </table>
        </body></html>
        """
        resp = make_response(html)
        first = resp.tables
        second = resp.tables
        assert first is second

    def test_no_tables(self):
        html = '<html><body><p>No tables here</p></body></html>'
        resp = make_response(html)
        assert resp.tables == []

    def test_nested_elements_in_cells(self):
        html = """
        <html><body>
        <table>
            <thead><tr><th>Link</th><th>Info</th></tr></thead>
            <tbody>
                <tr><td><a href="/page">Click here</a></td><td><strong>Bold</strong> text</td></tr>
            </tbody>
        </table>
        </body></html>
        """
        resp = make_response(html)
        assert resp.tables == [{'Link': ['Click here'], 'Info': ['Bold text']}]

    def test_whitespace_in_cells(self):
        html = """
        <html><body>
        <table>
            <thead><tr><th>  Name  </th><th>  Value  </th></tr></thead>
            <tbody>
                <tr><td>  foo  </td><td>  bar  </td></tr>
            </tbody>
        </table>
        </body></html>
        """
        resp = make_response(html)
        assert resp.tables == [{'Name': ['foo'], 'Value': ['bar']}]

    def test_single_column_table(self):
        html = """
        <html><body>
        <table>
            <thead><tr><th>Items</th></tr></thead>
            <tbody>
                <tr><td>Apple</td></tr>
                <tr><td>Banana</td></tr>
                <tr><td>Cherry</td></tr>
            </tbody>
        </table>
        </body></html>
        """
        resp = make_response(html)
        assert resp.tables == [{'Items': ['Apple', 'Banana', 'Cherry']}]

    def test_many_columns(self):
        html = """
        <html><body>
        <table>
            <thead><tr><th>A</th><th>B</th><th>C</th><th>D</th><th>E</th></tr></thead>
            <tbody>
                <tr><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td></tr>
                <tr><td>6</td><td>7</td><td>8</td><td>9</td><td>10</td></tr>
            </tbody>
        </table>
        </body></html>
        """
        resp = make_response(html)
        assert resp.tables == [{'A': ['1', '6'], 'B': ['2', '7'], 'C': ['3', '8'], 'D': ['4', '9'], 'E': ['5', '10']}]

    def test_empty_tbody(self):
        html = """
        <html><body>
        <table>
            <thead><tr><th>Name</th><th>Age</th></tr></thead>
            <tbody></tbody>
        </table>
        </body></html>
        """
        resp = make_response(html)
        assert resp.tables == [{'Name': [], 'Age': []}]

    def test_mixed_valid_and_invalid_tables(self):
        html = """
        <html><body>
        <table>
            <thead><tr><th>Good</th></tr></thead>
            <tbody><tr><td>yes</td></tr></tbody>
        </table>
        <table>
            <tr><td>no</td><td>headers</td></tr>
        </table>
        <table>
            <thead><tr><th>Also Good</th></tr></thead>
            <tbody><tr><td>yep</td></tr></tbody>
        </table>
        </body></html>
        """
        resp = make_response(html)
        assert len(resp.tables) == 2
        assert resp.tables[0] == {'Good': ['yes']}
        assert resp.tables[1] == {'Also Good': ['yep']}

    def test_row_with_extra_cells(self):
        html = """
        <html><body>
        <table>
            <thead><tr><th>A</th><th>B</th></tr></thead>
            <tbody>
                <tr><td>1</td><td>2</td><td>3</td></tr>
            </tbody>
        </table>
        </body></html>
        """
        resp = make_response(html)
        # Extra cells beyond the header count are ignored
        assert resp.tables == [{'A': ['1'], 'B': ['2']}]

    def test_special_characters_in_cells(self):
        html = """
        <html><body>
        <table>
            <thead><tr><th>Symbol</th><th>Price</th></tr></thead>
            <tbody>
                <tr><td>AT&amp;T</td><td>$25.50</td></tr>
                <tr><td>O'Reilly</td><td>&euro;30.00</td></tr>
            </tbody>
        </table>
        </body></html>
        """
        resp = make_response(html)
        assert resp.tables[0]['Symbol'] == ['AT&T', "O'Reilly"]
        assert resp.tables[0]['Price'] == ['$25.50', '\u20ac30.00']

    def test_nested_table_parsed_separately(self):
        html = """
        <html><body>
        <table>
            <thead><tr><th>Outer</th></tr></thead>
            <tbody>
                <tr><td>
                    <table>
                        <thead><tr><th>Inner</th></tr></thead>
                        <tbody><tr><td>nested</td></tr></tbody>
                    </table>
                </td></tr>
            </tbody>
        </table>
        </body></html>
        """
        resp = make_response(html)
        # Both the outer and inner table should be parsed
        assert len(resp.tables) == 2
        inner = next(t for t in resp.tables if 'Inner' in t)
        assert inner == {'Inner': ['nested']}

    def test_malformed_missing_td_skipped(self):
        html = """
        <html><body>
        <table>
            <thead><tr><th>A</th><th>B</th></tr></thead>
            <tbody>
                <tr></tr>
            </tbody>
        </table>
        </body></html>
        """
        resp = make_response(html)
        # Row with zero cells — both columns get empty strings
        assert resp.tables == [{'A': [''], 'B': ['']}]

    def test_malformed_empty_table_tag(self):
        html = '<html><body><table></table></body></html>'
        resp = make_response(html)
        assert resp.tables == []

    def test_malformed_thead_no_th(self):
        html = """
        <html><body>
        <table>
            <thead><tr></tr></thead>
            <tbody><tr><td>data</td></tr></tbody>
        </table>
        </body></html>
        """
        resp = make_response(html)
        assert resp.tables == []

    def test_malformed_unclosed_tags(self):
        html = """
        <html><body>
        <table>
            <thead><tr><th>X</th><th>Y</th></tr></thead>
            <tbody>
                <tr><td>1<td>2</tr>
                <tr><td>3</td><td>4</td></tr>
            </tbody>
        </table>
        </body></html>
        """
        resp = make_response(html)
        # lxml fixes up the broken HTML — table should still parse
        assert len(resp.tables) == 1
        assert resp.tables[0]['X'] == ['1', '3']

    def test_malformed_only_thead_no_tbody(self):
        html = """
        <html><body>
        <table>
            <thead><tr><th>Header</th></tr></thead>
        </table>
        </body></html>
        """
        resp = make_response(html)
        # Headers exist but no data rows
        assert resp.tables == [{'Header': []}]


# ── Metadata ────────────────────────────────────────────────────────────


class TestMetadata:
    def test_all_meta_fields(self):
        html = """
        <html><head>
            <title>Test Page</title>
            <meta name="description" content="A test page">
            <meta property="og:image" content="https://example.com/img.png">
            <meta name="author" content="Alice">
            <meta name="keywords" content="python, scraping">
            <meta name="twitter:site" content="@alice">
            <meta name="robots" content="index, follow">
            <link rel="canonical" href="https://example.com/canonical">
        </head><body></body></html>
        """
        resp = make_response(html)
        meta = resp.meta
        assert meta.title == 'Test Page'
        assert meta.description == 'A test page'
        assert meta.thumbnail == 'https://example.com/img.png'
        assert meta.author == 'Alice'
        assert meta.keywords == ('python', 'scraping')
        assert meta.twitter_handle == '@alice'
        assert meta.robots == ('index', 'follow')
        assert meta.canonical == 'https://example.com/canonical'

    def test_missing_meta_fields(self):
        html = '<html><head></head><body></body></html>'
        resp = make_response(html)
        meta = resp.meta
        assert meta.title is None
        assert meta.description is None
        assert meta.thumbnail is None
        assert meta.author is None
        assert meta.keywords is None
        assert meta.twitter_handle is None
        assert meta.robots is None
        assert meta.canonical is None

    def test_meta_cached(self):
        html = '<html><head><title>Hi</title></head><body></body></html>'
        resp = make_response(html)
        first = resp.meta
        second = resp.meta
        assert first is second


# ── Emails ──────────────────────────────────────────────────────────────


class TestEmails:
    def test_extracts_emails(self):
        html = '<html><body>Contact us at info@example.com or support@test.org</body></html>'
        resp = make_response(html)
        assert set(resp.emails) == {'info@example.com', 'support@test.org'}

    def test_no_emails(self):
        html = '<html><body>No emails here</body></html>'
        resp = make_response(html)
        assert resp.emails == ()

    def test_deduplicates_emails(self):
        html = '<html><body>a@b.com and a@b.com again</body></html>'
        resp = make_response(html)
        assert resp.emails == ('a@b.com',)


# ── Phone Numbers ───────────────────────────────────────────────────────


class TestPhoneNumbers:
    def test_standard_formats(self):
        html = '<html><body>(800) 123-4567 and 212-555-7890</body></html>'
        resp = make_response(html)
        assert '(800) 123-4567' in resp.phone_numbers
        assert '212-555-7890' in resp.phone_numbers

    def test_with_country_code(self):
        html = '<html><body>+1 800-123-4567</body></html>'
        resp = make_response(html)
        assert len(resp.phone_numbers) == 1

    def test_no_phone_numbers(self):
        html = '<html><body>No phones</body></html>'
        resp = make_response(html)
        assert resp.phone_numbers == ()


# ── Links ───────────────────────────────────────────────────────────────


class TestLinks:
    def test_absolute_links(self):
        html = '<html><body><a href="https://other.com/page">link</a></body></html>'
        resp = make_response(html)
        assert 'https://other.com/page' in resp.links

    def test_relative_links_qualified(self):
        html = '<html><body><a href="/about">about</a></body></html>'
        resp = make_response(html)
        assert 'https://example.com/about' in resp.links

    def test_no_links(self):
        html = '<html><body><p>No links</p></body></html>'
        resp = make_response(html)
        assert resp.links == ()

    def test_links_cached(self):
        html = '<html><body><a href="/a">a</a></body></html>'
        resp = make_response(html)
        first = resp.links
        second = resp.links
        assert first is second


# ── Images ──────────────────────────────────────────────────────────────


class TestImages:
    def test_extracts_images(self):
        html = '<html><body><img src="https://example.com/logo.png"></body></html>'
        resp = make_response(html)
        assert 'https://example.com/logo.png' in resp.images

    def test_relative_images_qualified(self):
        html = '<html><body><img src="/img/logo.png"></body></html>'
        resp = make_response(html)
        assert 'https://example.com/img/logo.png' in resp.images

    def test_no_images(self):
        html = '<html><body><p>No images</p></body></html>'
        resp = make_response(html)
        assert resp.images == ()


# ── Repr ────────────────────────────────────────────────────────────────


class TestRepr:
    def test_repr(self):
        resp = make_response('<html></html>')
        assert 'Status: 200' in repr(resp)
        assert 'Elapsed Time' in repr(resp)
