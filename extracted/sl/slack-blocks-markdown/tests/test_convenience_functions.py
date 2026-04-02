"""
Tests for convenience functions (markdown_to_blocks and markdown_to_block_objects)
"""

import pytest
from slack_sdk.models.blocks import Block, DividerBlock, HeaderBlock, SectionBlock

from slack_blocks_markdown import markdown_to_block_objects, markdown_to_blocks


class TestMarkdownToBlocks:
    """Test the markdown_to_blocks function (returns dicts)"""

    def test_returns_list_of_dicts(self):
        """Test that markdown_to_blocks returns a list of dictionaries"""
        markdown = "# Hello\n\nThis is a paragraph."
        blocks = markdown_to_blocks(markdown)

        assert isinstance(blocks, list)
        assert len(blocks) == 2
        assert all(isinstance(block, dict) for block in blocks)

    def test_dict_structure(self):
        """Test that returned dicts have proper structure"""
        markdown = "# Test Header"
        blocks = markdown_to_blocks(markdown)

        assert len(blocks) == 1
        assert blocks[0]["type"] == "header"
        assert "text" in blocks[0]
        assert blocks[0]["text"]["type"] == "plain_text"
        assert blocks[0]["text"]["text"] == "Test Header"

    def test_expand_sections_parameter(self):
        """Test that expand_sections parameter is passed through"""
        markdown = "This is a paragraph."

        # Test with expand_sections=True
        blocks_expanded = markdown_to_blocks(markdown, expand_sections=True)
        assert blocks_expanded[0]["expand"] is True

        # Test with expand_sections=False
        blocks_collapsed = markdown_to_blocks(markdown, expand_sections=False)
        assert blocks_collapsed[0]["expand"] is False

        # Test with expand_sections=None (default)
        blocks_default = markdown_to_blocks(markdown, expand_sections=None)
        assert (
            "expand" not in blocks_default[0] or blocks_default[0].get("expand") is None
        )


class TestMarkdownToBlockObjects:
    """Test the markdown_to_block_objects function (returns Block objects)"""

    def test_returns_list_of_blocks(self):
        """Test that markdown_to_block_objects returns a list of Block objects"""
        markdown = "# Hello\n\nThis is a paragraph."
        blocks = markdown_to_block_objects(markdown)

        assert isinstance(blocks, list)
        assert len(blocks) == 2
        assert all(isinstance(block, Block) for block in blocks)

    def test_returns_proper_block_types(self):
        """Test that proper Block types are returned"""
        markdown = "# Header\n\nParagraph\n\n---"
        blocks = markdown_to_block_objects(markdown)

        assert len(blocks) == 3
        assert isinstance(blocks[0], HeaderBlock)
        assert isinstance(blocks[1], SectionBlock)
        assert isinstance(blocks[2], DividerBlock)

    def test_blocks_can_be_modified(self):
        """Test that returned Block objects can be modified"""
        markdown = "# Original Header"
        blocks = markdown_to_block_objects(markdown)

        # Modify the block
        blocks[0].text.text = "Modified Header"

        assert blocks[0].text.text == "Modified Header"

    def test_blocks_can_be_converted_to_dicts(self):
        """Test that Block objects can be converted to dicts with to_dict()"""
        markdown = "# Test"
        blocks = markdown_to_block_objects(markdown)

        # Convert to dict
        block_dict = blocks[0].to_dict()

        assert isinstance(block_dict, dict)
        assert block_dict["type"] == "header"
        assert block_dict["text"]["text"] == "Test"

    def test_expand_sections_parameter(self):
        """Test that expand_sections parameter is passed through"""
        markdown = "This is a paragraph."

        # Test with expand_sections=True
        blocks_expanded = markdown_to_block_objects(markdown, expand_sections=True)
        assert blocks_expanded[0].expand is True

        # Test with expand_sections=False
        blocks_collapsed = markdown_to_block_objects(markdown, expand_sections=False)
        assert blocks_collapsed[0].expand is False

        # Test with expand_sections=None (default)
        blocks_default = markdown_to_block_objects(markdown, expand_sections=None)
        assert blocks_default[0].expand is None

    def test_complex_document(self):
        """Test with complex markdown containing multiple block types"""
        markdown = """# Main Title

This paragraph has **bold** and _italic_ text.

## Subsection

- Item 1
- Item 2

```python
def hello():
    return "world"
```

> A quote

---

Final paragraph.
"""
        blocks = markdown_to_block_objects(markdown)

        # Should have multiple blocks
        assert len(blocks) > 5

        # All should be Block instances
        assert all(isinstance(block, Block) for block in blocks)

        # Should have different block types
        block_types = {block.type for block in blocks}
        assert "header" in block_types
        assert "section" in block_types
        assert "divider" in block_types


class TestFunctionEquivalence:
    """Test that both functions produce equivalent results"""

    @pytest.mark.parametrize(
        "markdown",
        [
            "# Simple Header",
            "This is a paragraph with **bold** text.",
            "- Item 1\n- Item 2\n- Item 3",
            "```python\ncode\n```",
            "> Quote",
            "---",
        ],
    )
    def test_equivalent_output(self, markdown):
        """Test that both functions produce equivalent output"""
        # Get blocks as dicts
        blocks_dict = markdown_to_blocks(markdown)

        # Get blocks as objects and convert to dicts
        blocks_obj = markdown_to_block_objects(markdown)
        blocks_obj_as_dict = [block.to_dict() for block in blocks_obj]

        # Should be equivalent
        assert blocks_dict == blocks_obj_as_dict

    def test_edit_workflow(self):
        """Test typical workflow: get objects, edit, convert to dicts"""
        markdown = "# Original Title\n\nOriginal paragraph."

        # Get Block objects
        blocks = markdown_to_block_objects(markdown)

        # Modify the header
        blocks[0].text.text = "Custom Title"

        # Modify the paragraph text
        blocks[1].text.text = "Custom paragraph with *formatting*."

        # Convert to dicts for Slack API
        block_dicts = [block.to_dict() for block in blocks]

        # Verify modifications are reflected
        assert block_dicts[0]["text"]["text"] == "Custom Title"
        assert block_dicts[1]["text"]["text"] == "Custom paragraph with *formatting*."
