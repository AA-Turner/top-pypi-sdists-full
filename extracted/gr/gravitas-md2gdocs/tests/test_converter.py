"""Tests for gravitas-md2gdocs."""

from gravitas_md2gdocs import DocsRequestBuilder, MarkdownParser, to_requests


class TestMarkdownParser:
    """Tests for the MarkdownParser class."""

    def test_parse_header(self):
        parser = MarkdownParser("# Hello")
        paragraphs = parser.parse()

        assert len(paragraphs) == 1
        assert paragraphs[0].heading_level == 1
        assert paragraphs[0].runs[0].text == "Hello"

    def test_parse_multiple_header_levels(self):
        parser = MarkdownParser("# H1\n## H2\n### H3")
        paragraphs = parser.parse()

        assert len(paragraphs) == 3
        assert paragraphs[0].heading_level == 1
        assert paragraphs[1].heading_level == 2
        assert paragraphs[2].heading_level == 3

    def test_parse_bold(self):
        parser = MarkdownParser("This is **bold** text")
        paragraphs = parser.parse()

        assert len(paragraphs) == 1
        runs = paragraphs[0].runs
        assert runs[0].text == "This is "
        assert runs[0].bold is False
        assert runs[1].text == "bold"
        assert runs[1].bold is True
        assert runs[2].text == " text"

    def test_parse_italic(self):
        parser = MarkdownParser("This is *italic* text")
        paragraphs = parser.parse()

        runs = paragraphs[0].runs
        assert runs[1].text == "italic"
        assert runs[1].italic is True

    def test_parse_bold_italic(self):
        parser = MarkdownParser("This is ***both*** text")
        paragraphs = parser.parse()

        runs = paragraphs[0].runs
        assert runs[1].text == "both"
        assert runs[1].bold is True
        assert runs[1].italic is True

    def test_parse_strikethrough(self):
        parser = MarkdownParser("This is ~~struck~~ text")
        paragraphs = parser.parse()

        runs = paragraphs[0].runs
        assert runs[1].text == "struck"
        assert runs[1].strikethrough is True

    def test_parse_inline_code(self):
        parser = MarkdownParser("Use `print()` function")
        paragraphs = parser.parse()

        runs = paragraphs[0].runs
        assert runs[1].text == "print()"
        assert runs[1].code is True

    def test_parse_link(self):
        parser = MarkdownParser("Click [here](https://example.com)")
        paragraphs = parser.parse()

        runs = paragraphs[0].runs
        assert runs[1].text == "here"
        assert runs[1].link == "https://example.com"

    def test_parse_bullet_list(self):
        parser = MarkdownParser("- Item one\n- Item two")
        paragraphs = parser.parse()

        assert len(paragraphs) == 2
        assert paragraphs[0].is_list_item is True
        assert paragraphs[0].list_type == "BULLET"
        assert paragraphs[0].runs[0].text == "Item one"

    def test_parse_numbered_list(self):
        parser = MarkdownParser("1. First\n2. Second")
        paragraphs = parser.parse()

        assert len(paragraphs) == 2
        assert paragraphs[0].is_list_item is True
        assert paragraphs[0].list_type == "NUMBER"

    def test_parse_blockquote(self):
        parser = MarkdownParser("> This is quoted")
        paragraphs = parser.parse()

        assert len(paragraphs) == 1
        assert paragraphs[0].is_blockquote is True
        assert paragraphs[0].runs[0].text == "This is quoted"

    def test_parse_code_block(self):
        parser = MarkdownParser("```\ncode here\n```")
        paragraphs = parser.parse()

        assert len(paragraphs) == 1
        assert paragraphs[0].is_code_block is True
        assert paragraphs[0].runs[0].code is True


class TestDocsRequestBuilder:
    """Tests for the DocsRequestBuilder class."""

    def test_build_returns_list(self):
        parser = MarkdownParser("Hello")
        paragraphs = parser.parse()
        builder = DocsRequestBuilder()

        requests = builder.build(paragraphs)
        assert isinstance(requests, list)

    def test_insert_text_request(self):
        parser = MarkdownParser("Hello")
        paragraphs = parser.parse()
        builder = DocsRequestBuilder()

        requests = builder.build(paragraphs)

        insert_requests = [r for r in requests if "insertText" in r]
        assert len(insert_requests) == 1
        assert insert_requests[0]["insertText"]["text"] == "Hello\n"

    def test_heading_style_request(self):
        parser = MarkdownParser("# Header")
        paragraphs = parser.parse()
        builder = DocsRequestBuilder()

        requests = builder.build(paragraphs)

        style_requests = [r for r in requests if "updateParagraphStyle" in r]
        assert len(style_requests) == 1
        assert (
            style_requests[0]["updateParagraphStyle"]["paragraphStyle"]["namedStyleType"]
            == "HEADING_1"
        )

    def test_bold_style_request(self):
        parser = MarkdownParser("**bold**")
        paragraphs = parser.parse()
        builder = DocsRequestBuilder()

        requests = builder.build(paragraphs)

        text_style_requests = [r for r in requests if "updateTextStyle" in r]
        assert len(text_style_requests) >= 1

        bold_request = next(
            r for r in text_style_requests if r["updateTextStyle"]["textStyle"].get("bold") is True
        )
        assert bold_request is not None

    def test_start_index_parameter(self):
        parser = MarkdownParser("Hello")
        paragraphs = parser.parse()
        builder = DocsRequestBuilder(start_index=50)

        requests = builder.build(paragraphs)

        insert_request = next(r for r in requests if "insertText" in r)
        assert insert_request["insertText"]["location"]["index"] == 50


class TestToRequests:
    """Tests for the main to_requests function."""

    def test_basic_conversion(self):
        requests = to_requests("# Hello\n\nWorld")
        assert isinstance(requests, list)
        assert len(requests) > 0

    def test_start_index(self):
        requests = to_requests("Hello", start_index=100)

        insert_request = next(r for r in requests if "insertText" in r)
        assert insert_request["insertText"]["location"]["index"] == 100

    def test_empty_string(self):
        requests = to_requests("")
        assert requests == []

    def test_complex_markdown(self):
        markdown = """
# Title

This is **bold** and *italic*.

- Item 1
- Item 2

> Quote

```
code
```
"""
        requests = to_requests(markdown)

        # Should have multiple request types
        request_types = set()
        for r in requests:
            request_types.update(r.keys())

        assert "insertText" in request_types
        assert "updateTextStyle" in request_types
        assert "updateParagraphStyle" in request_types
        assert "createParagraphBullets" in request_types
