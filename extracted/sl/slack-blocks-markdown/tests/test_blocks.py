"""
Tests for custom Slack Block implementations
"""

import pytest

from slack_blocks_markdown.blocks import TableBlock


class TestTableBlock:
    """Test custom TableBlock functionality"""

    def test_table_block_creation(self):
        """Test basic TableBlock creation"""
        rows = [
            [{"type": "raw_text", "text": "Header 1"}],
            [{"type": "raw_text", "text": "Cell 1"}],
        ]

        table = TableBlock(rows=rows)

        assert table.type == "table"
        assert len(table.rows) == 2
        assert table.rows[0][0]["text"] == "Header 1"

    def test_table_block_to_dict(self):
        """Test TableBlock serialization"""
        rows = [
            [
                {"type": "raw_text", "text": "Name"},
                {"type": "raw_text", "text": "Value"},
            ],
            [{"type": "raw_text", "text": "Test"}, {"type": "raw_text", "text": "123"}],
        ]

        table = TableBlock(rows=rows, block_id="test_table")
        table_dict = table.to_dict()

        assert table_dict["type"] == "table"
        assert table_dict["block_id"] == "test_table"
        assert len(table_dict["rows"]) == 2
        assert table_dict["rows"][0][0]["text"] == "Name"

    def test_table_constraints(self):
        """Test TableBlock constraint validation"""
        # Test row limit
        too_many_rows = [[{"type": "raw_text", "text": f"Row {i}"}] for i in range(101)]

        with pytest.raises(ValueError, match="cannot have more than 100 rows"):
            TableBlock(rows=too_many_rows)

        # Test column limit
        too_many_cols = [{"type": "raw_text", "text": f"Col {i}"} for i in range(21)]

        with pytest.raises(ValueError, match="cannot have more than 20 columns"):
            TableBlock(rows=[too_many_cols])

        # Test block_id length limit
        long_id = "x" * 256

        with pytest.raises(ValueError, match="cannot be longer than 255 characters"):
            TableBlock(rows=[[{"type": "raw_text", "text": "test"}]], block_id=long_id)

    def test_table_block_with_column_settings(self):
        """Test TableBlock with column settings"""
        rows = [
            [
                {"type": "raw_text", "text": "Name"},
                {"type": "raw_text", "text": "Value"},
            ],
            [{"type": "raw_text", "text": "Test"}, {"type": "raw_text", "text": "123"}],
        ]
        column_settings = [
            {"header_style": "primary"},
            {"align": "right"},
        ]

        table = TableBlock(rows=rows, column_settings=column_settings)
        table_dict = table.to_dict()

        assert "column_settings" in table_dict
        assert len(table_dict["column_settings"]) == 2
        assert table_dict["column_settings"][0]["header_style"] == "primary"

    def test_table_block_without_optional_fields(self):
        """Test TableBlock without optional fields"""
        rows = [
            [{"type": "raw_text", "text": "Simple"}],
        ]

        table = TableBlock(rows=rows)
        table_dict = table.to_dict()

        assert table_dict["type"] == "table"
        assert "rows" in table_dict
        assert "block_id" not in table_dict
        assert "column_settings" not in table_dict
