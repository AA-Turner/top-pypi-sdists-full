"""
Integration tests for complete markdown to Slack blocks conversion
"""

import json

from mistletoe import Document

from slack_blocks_markdown import SlackBlocksRenderer, markdown_to_blocks


class TestIntegrationScenarios:
    """Test complete conversion scenarios"""

    def test_readme_example(self):
        """Test the example from README works correctly"""
        markdown = """# Project Update

This is a **bold** announcement!

- Feature A completed
- Feature B in progress

Check out our [documentation](https://example.com) for details."""

        blocks = markdown_to_blocks(markdown)

        assert len(blocks) >= 3  # Header, paragraph, list
        assert blocks[0]["type"] == "header"
        assert blocks[0]["text"]["text"] == "Project Update"
        assert "*bold*" in blocks[1]["text"]["text"]

    def test_complex_document_conversion(self):
        """Test conversion of complex technical document"""
        markdown = """# API Documentation

## Authentication

All requests require authentication:

```bash
curl -H "Authorization: Bearer TOKEN" https://api.example.com
```

### Rate Limits

| Endpoint | Limit |
|----------|-------|
| /users   | 100/min |
| /data    | 50/min |

> **Important**: Store tokens securely

For more info, see our [docs](https://docs.example.com).

---

© 2025 Example Corp"""

        blocks = markdown_to_blocks(markdown)

        # Should have multiple different block types
        block_types = [block["type"] for block in blocks]
        assert "header" in block_types
        assert "section" in block_types
        assert "table" in block_types
        assert "divider" in block_types

        # Verify JSON serialization works
        json_str = json.dumps({"blocks": blocks}, indent=2)
        assert len(json_str) > 100

        # Should be valid JSON
        parsed = json.loads(json_str)
        assert "blocks" in parsed

    def test_slack_api_compatibility(self):
        """Test that output is compatible with Slack API format"""
        markdown = "# Test\n\nThis is a test message with **formatting**."

        blocks = markdown_to_blocks(markdown)

        # Each block should have required fields for Slack API
        for block in blocks:
            assert "type" in block

            if block["type"] == "header":
                assert "text" in block
                assert block["text"]["type"] == "plain_text"

            elif block["type"] == "section":
                assert "text" in block
                assert block["text"]["type"] == "mrkdwn"

    def test_error_handling_gracefully(self):
        """Test that malformed input doesn't crash"""
        test_cases = [
            "",  # Empty
            "   ",  # Whitespace only
            "# \n\n",  # Empty header
            "[]() invalid link",  # Malformed link
        ]

        for markdown in test_cases:
            # Should not raise exceptions
            blocks = markdown_to_blocks(markdown)
            assert isinstance(blocks, list)

    def test_performance_with_large_documents(self):
        """Test performance with reasonably large documents"""
        import time

        # Generate large but reasonable markdown
        large_markdown = "# Large Document\n\n"
        for i in range(100):
            large_markdown += (
                f"## Section {i}\n\nThis is paragraph {i} with **bold** text.\n\n"
            )
            large_markdown += f"- Item {i}a\n- Item {i}b\n\n"

        start_time = time.time()
        blocks = markdown_to_blocks(large_markdown)
        end_time = time.time()

        # Should complete reasonably quickly (under 5 seconds)
        assert (end_time - start_time) < 5.0
        assert len(blocks) > 200  # Should generate many blocks

    def test_convenience_function_vs_direct_usage(self):
        """Test that convenience function matches direct usage"""
        markdown = """# Test

This is a **test** with:
- Item 1
- Item 2

> Quote here"""

        # Using convenience function
        blocks1 = markdown_to_blocks(markdown)

        # Using direct renderer
        with SlackBlocksRenderer() as renderer:
            document = Document(markdown)
            blocks_objects = renderer.render(document)
        blocks2 = [block.to_dict() for block in blocks_objects]

        # Should produce identical results
        assert len(blocks1) == len(blocks2)
        for b1, b2 in zip(blocks1, blocks2, strict=False):
            assert b1["type"] == b2["type"]
            if "text" in b1:
                assert b1["text"]["text"] == b2["text"]["text"]

    def test_table_integration(self):
        """Test table handling in complete document"""
        markdown = """# Data Report

Here's our performance data:

| Metric | Q1 | Q2 |
|--------|----|----|
| Users | 100 | 150 |
| Revenue | $10K | $15K |

> Great progress this quarter!"""

        blocks = markdown_to_blocks(markdown)

        # Should have header, paragraph, table, and quote
        assert len(blocks) == 4

        # Find the table block
        table_block = next((b for b in blocks if b["type"] == "table"), None)
        assert table_block is not None
        assert "rows" in table_block
        assert len(table_block["rows"]) == 3  # Header + 2 data rows

    def test_mixed_inline_formatting(self):
        """Test complex inline formatting combinations"""
        markdown = """This paragraph has **bold**, _italic_, `code`, ~strikethrough~, and [links](https://example.com)."""

        blocks = markdown_to_blocks(markdown)

        assert len(blocks) == 1
        text = blocks[0]["text"]["text"]
        assert "*bold*" in text
        assert "_italic_" in text
        assert "`code`" in text
        assert "~strikethrough~" in text
        assert "<https://example.com|links>" in text
