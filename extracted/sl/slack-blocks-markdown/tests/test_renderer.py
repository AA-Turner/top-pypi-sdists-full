"""
Tests for SlackBlocksRenderer functionality
"""

import pytest
from mistletoe import Document
from slack_sdk.models.blocks import (
    DividerBlock,
    HeaderBlock,
    RichTextBlock,
    SectionBlock,
)

from slack_blocks_markdown import SlackBlocksRenderer


class TestBasicRendering:
    """Test basic markdown element rendering"""

    def test_heading_renders_to_header_block(self, renderer):
        """Test that headings become HeaderBlocks"""
        markdown = "# Test Heading"
        document = Document(markdown)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        assert isinstance(blocks[0], HeaderBlock)
        assert blocks[0].text.text == "Test Heading"

    def test_heading_with_bold_strips_formatting(self, renderer):
        """Test that bold formatting in headings is stripped (plain text only)"""
        markdown = "### **Chapter 5**"
        document = Document(markdown)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        assert isinstance(blocks[0], HeaderBlock)
        # Should be plain text without asterisks
        assert blocks[0].text.text == "Chapter 5"
        assert "*" not in blocks[0].text.text

    def test_heading_with_italic_strips_formatting(self, renderer):
        """Test that italic formatting in headings is stripped"""
        markdown = "## _Important Section_"
        document = Document(markdown)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        assert isinstance(blocks[0], HeaderBlock)
        assert blocks[0].text.text == "Important Section"
        assert "_" not in blocks[0].text.text

    def test_heading_with_inline_code_strips_formatting(self, renderer):
        """Test that inline code in headings is stripped"""
        markdown = "# Working with `config.json`"
        document = Document(markdown)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        assert isinstance(blocks[0], HeaderBlock)
        assert blocks[0].text.text == "Working with config.json"
        assert "`" not in blocks[0].text.text

    def test_heading_with_mixed_formatting(self, renderer):
        """Test that mixed formatting in headings is all stripped"""
        markdown = "## **Bold** and _italic_ with `code`"
        document = Document(markdown)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        assert isinstance(blocks[0], HeaderBlock)
        assert blocks[0].text.text == "Bold and italic with code"
        assert "*" not in blocks[0].text.text
        assert "_" not in blocks[0].text.text
        assert "`" not in blocks[0].text.text

    def test_paragraph_renders_to_section_block(self, renderer):
        """Test that paragraphs become SectionBlocks"""
        markdown = "This is a paragraph with **bold** text."
        document = Document(markdown)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        assert isinstance(blocks[0], SectionBlock)
        assert blocks[0].text.text == "This is a paragraph with *bold* text."

    def test_horizontal_rule_renders_to_divider(self, renderer):
        """Test that horizontal rules become DividerBlocks"""
        markdown = "---"
        document = Document(markdown)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        assert isinstance(blocks[0], DividerBlock)


class TestInlineFormatting:
    """Test inline markdown formatting"""

    @pytest.mark.parametrize(
        ("markdown", "expected"),
        [
            ("**bold**", "*bold*"),
            ("_italic_", "_italic_"),
            ("`code`", "`code`"),
            ("~strikethrough~", "~strikethrough~"),
            ("[link](https://example.com)", "<https://example.com|link>"),
        ],
    )
    def test_inline_formatting(self, renderer, markdown, expected):
        """Test various inline formatting conversions"""
        document = Document(markdown)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        assert blocks[0].text.text == expected


class TestLists:
    """Test list rendering functionality"""

    def test_unordered_list_rendering(self, renderer):
        """Test unordered list conversion to RichTextBlock"""
        markdown = "- Item 1\n- Item 2\n- Item 3"
        document = Document(markdown)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        assert isinstance(blocks[0], RichTextBlock)
        block_dict = blocks[0].to_dict()
        assert block_dict["type"] == "rich_text"
        assert len(block_dict["elements"]) == 1
        assert block_dict["elements"][0]["type"] == "rich_text_list"
        assert block_dict["elements"][0]["style"] == "bullet"
        # Check list items
        list_items = block_dict["elements"][0]["elements"]
        assert len(list_items) == 3
        assert list_items[0]["elements"][0]["text"] == "Item 1"
        assert list_items[1]["elements"][0]["text"] == "Item 2"
        assert list_items[2]["elements"][0]["text"] == "Item 3"

    def test_ordered_list_rendering(self, renderer):
        """Test ordered list conversion to RichTextBlock"""
        markdown = "1. First\n2. Second\n3. Third"
        document = Document(markdown)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        assert isinstance(blocks[0], RichTextBlock)
        block_dict = blocks[0].to_dict()
        assert block_dict["type"] == "rich_text"
        assert block_dict["elements"][0]["type"] == "rich_text_list"
        assert block_dict["elements"][0]["style"] == "ordered"
        # Check list items
        list_items = block_dict["elements"][0]["elements"]
        assert len(list_items) == 3
        assert list_items[0]["elements"][0]["text"] == "First"
        assert list_items[1]["elements"][0]["text"] == "Second"
        assert list_items[2]["elements"][0]["text"] == "Third"

    def test_nested_bullet_in_ordered_list(self, renderer):
        """Test bullet list nested in ordered list - basic case from bug report"""
        markdown = """1. Hello
    - World
    - Neptune
    - Sun

2. Bye
    - Night
    - Moon"""
        document = Document(markdown)
        blocks = renderer.render(document)

        # Should be a single RichTextBlock, not multiple blocks
        assert len(blocks) == 1
        assert isinstance(blocks[0], RichTextBlock)

        block_dict = blocks[0].to_dict()
        elements = block_dict["elements"]

        # Should have 4 rich_text_list elements in sequence:
        # 1. Ordered list with "Hello" (parent #1)
        # 2. Bullet list with ["World", "Neptune", "Sun"] (nested under #1)
        # 3. Ordered list with "Bye" (parent #2)
        # 4. Bullet list with ["Night", "Moon"] (nested under #2)
        assert len(elements) == 4

        # First element: ordered list with "Hello"
        assert elements[0]["type"] == "rich_text_list"
        assert elements[0]["style"] == "ordered"
        assert len(elements[0]["elements"]) == 1
        assert elements[0]["elements"][0]["elements"][0]["text"] == "Hello"

        # Second element: bullet list with nested items from first parent
        assert elements[1]["type"] == "rich_text_list"
        assert elements[1]["style"] == "bullet"
        assert elements[1]["indent"] == 1
        assert len(elements[1]["elements"]) == 3
        assert elements[1]["elements"][0]["elements"][0]["text"] == "World"
        assert elements[1]["elements"][1]["elements"][0]["text"] == "Neptune"
        assert elements[1]["elements"][2]["elements"][0]["text"] == "Sun"

        # Third element: ordered list with "Bye"
        assert elements[2]["type"] == "rich_text_list"
        assert elements[2]["style"] == "ordered"
        assert len(elements[2]["elements"]) == 1
        assert elements[2]["elements"][0]["elements"][0]["text"] == "Bye"

        # Fourth element: bullet list with nested items from second parent
        assert elements[3]["type"] == "rich_text_list"
        assert elements[3]["style"] == "bullet"
        assert elements[3]["indent"] == 1
        assert len(elements[3]["elements"]) == 2
        assert elements[3]["elements"][0]["elements"][0]["text"] == "Night"
        assert elements[3]["elements"][1]["elements"][0]["text"] == "Moon"

    def test_nested_ordered_in_bullet_list(self, renderer):
        """Test ordered list nested in bullet list"""
        markdown = """- First
    1. One
    2. Two

- Second
    1. Alpha
    2. Beta"""
        document = Document(markdown)
        blocks = renderer.render(document)

        # Should be a single RichTextBlock
        assert len(blocks) == 1
        assert isinstance(blocks[0], RichTextBlock)

        block_dict = blocks[0].to_dict()
        elements = block_dict["elements"]

        # Should have 4 elements in sequence
        assert len(elements) == 4

        # First: bullet list with "First"
        assert elements[0]["type"] == "rich_text_list"
        assert elements[0]["style"] == "bullet"
        assert elements[0]["elements"][0]["elements"][0]["text"] == "First"

        # Second: ordered list nested under "First"
        assert elements[1]["type"] == "rich_text_list"
        assert elements[1]["style"] == "ordered"
        assert elements[1]["indent"] == 1
        assert len(elements[1]["elements"]) == 2
        assert elements[1]["elements"][0]["elements"][0]["text"] == "One"
        assert elements[1]["elements"][1]["elements"][0]["text"] == "Two"

        # Third: bullet list with "Second"
        assert elements[2]["type"] == "rich_text_list"
        assert elements[2]["style"] == "bullet"
        assert elements[2]["elements"][0]["elements"][0]["text"] == "Second"

        # Fourth: ordered list nested under "Second"
        assert elements[3]["type"] == "rich_text_list"
        assert elements[3]["style"] == "ordered"
        assert elements[3]["indent"] == 1
        assert len(elements[3]["elements"]) == 2
        assert elements[3]["elements"][0]["elements"][0]["text"] == "Alpha"
        assert elements[3]["elements"][1]["elements"][0]["text"] == "Beta"

    def test_deeply_nested_lists(self, renderer):
        """Test 3+ levels of nesting"""
        markdown = """1. Level 1
    - Level 2a
        - Level 3a
        - Level 3b
    - Level 2b

2. Another L1"""
        document = Document(markdown)
        blocks = renderer.render(document)

        # Should be a single RichTextBlock
        assert len(blocks) == 1
        assert isinstance(blocks[0], RichTextBlock)

        block_dict = blocks[0].to_dict()
        elements = block_dict["elements"]

        # Should have multiple list elements with proper indentation
        assert len(elements) >= 4

        # Verify indent levels are progressive
        found_indent_0 = any(
            e.get("indent", 0) == 0 for e in elements if e["type"] == "rich_text_list"
        )
        found_indent_1 = any(
            e.get("indent") == 1 for e in elements if e["type"] == "rich_text_list"
        )
        found_indent_2 = any(
            e.get("indent") == 2 for e in elements if e["type"] == "rich_text_list"
        )

        assert found_indent_0
        assert found_indent_1
        assert found_indent_2

    def test_multiple_items_with_nested_lists(self, renderer):
        """Test list with multiple parent items that each have nested children"""
        markdown = """- Parent A
    - Child A1
    - Child A2

- Parent B
    - Child B1

- Parent C
    - Child C1
    - Child C2
    - Child C3"""
        document = Document(markdown)
        blocks = renderer.render(document)

        # Should be a single RichTextBlock
        assert len(blocks) == 1
        assert isinstance(blocks[0], RichTextBlock)

        block_dict = blocks[0].to_dict()
        elements = block_dict["elements"]

        # Should have: parent A, nested A, parent B, nested B, parent C, nested C = 6 elements
        assert len(elements) == 6

        # All parent lists should have no indent (or indent=0)
        parent_elements = [elements[0], elements[2], elements[4]]
        for parent in parent_elements:
            assert parent["type"] == "rich_text_list"
            assert parent["style"] == "bullet"
            assert parent.get("indent", 0) == 0

        # All nested lists should have indent=1
        nested_elements = [elements[1], elements[3], elements[5]]
        for nested in nested_elements:
            assert nested["type"] == "rich_text_list"
            assert nested["style"] == "bullet"
            assert nested["indent"] == 1

        # Verify item counts
        assert len(elements[1]["elements"]) == 2  # A1, A2
        assert len(elements[3]["elements"]) == 1  # B1
        assert len(elements[5]["elements"]) == 3  # C1, C2, C3


class TestCodeBlocks:
    """Test code block handling"""

    def test_code_block_rendering(self, renderer):
        """Test code block formatting with RichTextBlock"""
        markdown = "```python\ndef hello():\n    return 'world'\n```"
        document = Document(markdown)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        assert isinstance(blocks[0], RichTextBlock)
        block_dict = blocks[0].to_dict()
        assert block_dict["type"] == "rich_text"
        assert block_dict["elements"][0]["type"] == "rich_text_preformatted"
        # Check the code content
        code_text = block_dict["elements"][0]["elements"][0]["text"]
        assert "def hello():" in code_text
        assert "return 'world'" in code_text


class TestBlockquotes:
    """Test blockquote rendering"""

    def test_simple_blockquote(self, renderer):
        """Test basic blockquote formatting with RichTextBlock"""
        markdown = "> This is a quote"
        document = Document(markdown)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        assert isinstance(blocks[0], RichTextBlock)
        block_dict = blocks[0].to_dict()
        assert block_dict["type"] == "rich_text"
        assert block_dict["elements"][0]["type"] == "rich_text_quote"
        # Check quote content
        quote_text = block_dict["elements"][0]["elements"][0]["text"]
        assert "This is a quote" in quote_text

    def test_multiline_blockquote(self, renderer):
        """Test multiline blockquote handling with RichTextBlock"""
        markdown = "> First line\n>\n> Second paragraph"
        document = Document(markdown)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        assert isinstance(blocks[0], RichTextBlock)
        block_dict = blocks[0].to_dict()
        assert block_dict["elements"][0]["type"] == "rich_text_quote"
        # Check that content is preserved (exact structure may vary)
        elements = block_dict["elements"][0]["elements"]
        # Should have multiple text elements
        assert len(elements) > 0


class TestTables:
    """Test table rendering functionality"""

    def test_simple_table_rendering(self, renderer):
        """Test basic table conversion to TableBlock"""
        markdown = """| Name | Value |
|------|--------|
| Test | 123 |
| Demo | 456 |"""

        document = Document(markdown)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        # Should be our custom TableBlock
        assert blocks[0].type == "table"
        assert len(blocks[0].rows) == 3  # Header + 2 data rows

    def test_table_with_bold_text_strips_formatting(self, renderer):
        """Test that bold formatting in table cells is stripped (raw_text only)"""
        markdown = """| Name | Status |
|------|--------|
| **Important** | Done |
| Task | **Complete** |"""

        document = Document(markdown)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        assert blocks[0].type == "table"

        # Check header row (first row)
        header_row = blocks[0].rows[0]
        assert header_row[0]["text"] == "Name"
        assert header_row[1]["text"] == "Status"

        # Check data rows - should not have asterisks
        row1 = blocks[0].rows[1]
        assert row1[0]["text"] == "Important"
        assert "*" not in row1[0]["text"]
        assert row1[1]["text"] == "Done"

        row2 = blocks[0].rows[2]
        assert row2[0]["text"] == "Task"
        assert row2[1]["text"] == "Complete"
        assert "*" not in row2[1]["text"]

    def test_table_with_italic_text_strips_formatting(self, renderer):
        """Test that italic formatting in table cells is stripped"""
        markdown = """| Item | _Priority_ |
|------|------------|
| Fix | _High_ |"""

        document = Document(markdown)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        header_row = blocks[0].rows[0]
        assert header_row[1]["text"] == "Priority"
        assert "_" not in header_row[1]["text"]

        row1 = blocks[0].rows[1]
        assert row1[1]["text"] == "High"
        assert "_" not in row1[1]["text"]

    def test_table_with_code_text_strips_formatting(self, renderer):
        """Test that inline code in table cells is stripped"""
        markdown = """| Config | Value |
|--------|-------|
| `debug` | true |"""

        document = Document(markdown)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        row1 = blocks[0].rows[1]
        assert row1[0]["text"] == "debug"
        assert "`" not in row1[0]["text"]

    def test_table_with_mixed_formatting(self, renderer):
        """Test that mixed formatting in table cells is all stripped"""
        markdown = """| Feature | Status |
|---------|--------|
| **Auth** with `API` | _Ready_ |"""

        document = Document(markdown)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        row1 = blocks[0].rows[1]
        assert row1[0]["text"] == "Auth with API"
        assert "*" not in row1[0]["text"]
        assert "`" not in row1[0]["text"]
        assert row1[1]["text"] == "Ready"
        assert "_" not in row1[1]["text"]


class TestConstraints:
    """Test Slack Block Kit constraint handling"""

    def test_long_heading_truncation(self, renderer):
        """Test that long headings are truncated to 150 chars"""
        long_title = "A" * 200
        markdown = f"# {long_title}"
        document = Document(markdown)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        assert len(blocks[0].text.text) <= 150
        assert blocks[0].text.text.endswith("...")

    def test_long_paragraph_truncation(self, renderer):
        """Test that long paragraphs are truncated to 3000 chars"""
        long_text = "This is a very long paragraph. " * 200
        document = Document(long_text)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        assert len(blocks[0].text.text) <= 3000
        assert blocks[0].text.text.endswith("...")


class TestEdgeCases:
    """Test edge cases and error conditions"""

    def test_empty_document(self, renderer):
        """Test handling of empty markdown"""
        markdown = ""
        document = Document(markdown)
        blocks = renderer.render(document)

        assert blocks == []

    def test_whitespace_only(self, renderer):
        """Test handling of whitespace-only content"""
        markdown = (
            "   \n\n   \n"  # Just spaces, no tabs (which would create code block)
        )
        document = Document(markdown)
        blocks = renderer.render(document)

        assert blocks == []

    def test_mixed_complex_content(self, renderer):
        """Test complex mixed content document"""
        markdown = """# Main Title

This paragraph has **bold**, _italic_, and `code` formatting.

## Subsection

- First item with [link](https://example.com)
- Second item with *emphasis*

```javascript
console.log('hello world');
```

> Important note about the code above

| Feature | Status | Notes |
|---------|--------|-------|
| Auth | Done | Ready |
| API | Progress | Testing |

---

Final paragraph after divider.
"""

        document = Document(markdown)
        blocks = renderer.render(document)

        # Should generate multiple blocks of different types
        assert len(blocks) > 5

        # Check we have different block types
        block_types = [block.type for block in blocks]
        assert "header" in block_types
        assert "section" in block_types  # paragraphs
        assert "rich_text" in block_types  # lists, quotes, code blocks
        assert "divider" in block_types
        assert "table" in block_types


class TestExpandSections:
    """Test expand_sections option for SectionBlocks (paragraphs only)

    Note: Lists, quotes, and code blocks now use RichTextBlock which doesn't
    support the expand parameter. Only paragraphs still use SectionBlock.
    """

    def test_expand_sections_true_on_paragraph(self):
        """Test that expand_sections=True sets expand=True on paragraph SectionBlocks"""
        renderer = SlackBlocksRenderer(expand_sections=True)
        markdown = "This is a paragraph."
        document = Document(markdown)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        assert isinstance(blocks[0], SectionBlock)
        assert blocks[0].expand is True

    def test_expand_sections_false_on_paragraph(self):
        """Test that expand_sections=False sets expand=False on paragraph SectionBlocks"""
        renderer = SlackBlocksRenderer(expand_sections=False)
        markdown = "This is a paragraph."
        document = Document(markdown)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        assert isinstance(blocks[0], SectionBlock)
        assert blocks[0].expand is False

    def test_expand_sections_none_on_paragraph(self):
        """Test that expand_sections=None sets expand=None on paragraph SectionBlocks"""
        renderer = SlackBlocksRenderer(expand_sections=None)
        markdown = "This is a paragraph."
        document = Document(markdown)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        assert isinstance(blocks[0], SectionBlock)
        assert blocks[0].expand is None

    def test_default_expand_sections_is_true(self):
        """Test that default renderer has expand=True"""
        renderer = SlackBlocksRenderer()
        markdown = "This is a paragraph."
        document = Document(markdown)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        assert isinstance(blocks[0], SectionBlock)
        assert blocks[0].expand is True

    def test_expand_sections_only_affects_paragraphs(self):
        """Test that expand_sections only affects paragraph SectionBlocks, not RichTextBlocks"""
        renderer = SlackBlocksRenderer(expand_sections=True)
        markdown = """This is a paragraph.

```python
code block
```

> A quote

- List item 1
- List item 2
"""
        document = Document(markdown)
        blocks = renderer.render(document)

        # Filter only SectionBlocks (should be just the paragraph)
        section_blocks = [b for b in blocks if isinstance(b, SectionBlock)]

        # Should have 1 SectionBlock (just the paragraph)
        assert len(section_blocks) == 1

        # The paragraph should have expand=True
        assert section_blocks[0].expand is True

        # Verify we also have RichTextBlocks for code, quote, and list
        rich_text_blocks = [b for b in blocks if isinstance(b, RichTextBlock)]
        assert len(rich_text_blocks) == 3  # code, quote, list
