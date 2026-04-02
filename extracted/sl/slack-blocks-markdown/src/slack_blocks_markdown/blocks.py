"""
Custom Slack Block implementations
"""

from typing import Any

from slack_sdk.models.blocks import Block


class TableBlock(Block):
    """
    Custom Table Block implementation for Slack Block Kit.

    Since the Slack SDK doesn't include TableBlock, this implements it
    according to the official Slack documentation.
    """

    def __init__(
        self,
        rows: list[list[dict[str, Any]]],
        block_id: str | None = None,
        column_settings: list[dict[str, Any]] | None = None,
    ):
        """
        Initialize a Table block.

        Args:
            rows: List of rows, where each row is a list of cell objects
            block_id: Optional unique identifier for the block (max 255 chars)
            column_settings: Optional list of column configuration objects
        """
        # Initialize parent Block with correct parameters
        super().__init__(type="table", block_id=block_id)

        # Validate constraints
        if len(rows) > 100:
            msg = "Table cannot have more than 100 rows"
            raise ValueError(msg)

        for i, row in enumerate(rows):
            if len(row) > 20:
                msg = f"Row {i} cannot have more than 20 columns"
                raise ValueError(msg)

        if block_id and len(block_id) > 255:
            msg = "block_id cannot be longer than 255 characters"
            raise ValueError(msg)

        self.rows = rows
        self.column_settings = column_settings

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the TableBlock to a dictionary for JSON serialization.
        """
        result: dict[str, Any] = {
            "type": self.type,
            "rows": self.rows,
        }

        if self.block_id:
            result["block_id"] = self.block_id

        if self.column_settings:
            result["column_settings"] = self.column_settings

        return result
