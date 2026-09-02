"""
Slack Blocks Markdown - Convert Markdown to Slack Block Kit blocks
"""

from typing import Any

from slack_sdk.models.blocks import Block

from .blocks import TableBlock
from .renderer import SlackBlocksRenderer


# Convenience function for simple usage
def markdown_to_blocks(
    markdown_text: str,
    expand_sections: bool | None = True,
) -> list[dict[str, Any]]:
    """
    Convert markdown text to Slack blocks as dictionaries.

    Args:
        markdown_text: The markdown text to convert
        expand_sections: Whether to expand all section blocks by default.
            If True (default), section blocks will always be fully expanded.
            If False, Slack may show "Show more" button for long content.
            If None, uses Slack's default behavior.

    Returns:
        List of block dictionaries ready to use with Slack API
    """
    from mistletoe import Document  # type: ignore[import-untyped]

    with SlackBlocksRenderer(expand_sections=expand_sections) as renderer:
        document = Document(markdown_text)
        blocks = renderer.render(document)
    return [block.to_dict() for block in blocks]


def markdown_to_block_objects(
    markdown_text: str,
    expand_sections: bool | None = True,
) -> list[Block]:
    """
    Convert markdown text to Slack Block objects.

    This function returns Block objects that can be modified before being
    converted to dictionaries with .to_dict() method.

    Args:
        markdown_text: The markdown text to convert
        expand_sections: Whether to expand all section blocks by default.
            If True (default), section blocks will always be fully expanded.
            If False, Slack may show "Show more" button for long content.
            If None, uses Slack's default behavior.

    Returns:
        List of Block objects from slack_sdk

    Example:
        >>> blocks = markdown_to_block_objects("# Hello\\nWorld")
        >>> # Modify blocks as needed
        >>> blocks[0].text.text = "Modified Header"
        >>> # Convert to dicts when ready to send
        >>> block_dicts = [b.to_dict() for b in blocks]
    """
    from mistletoe import Document  # type: ignore[import-untyped]

    with SlackBlocksRenderer(expand_sections=expand_sections) as renderer:
        document = Document(markdown_text)
        # render() returns list[Block] when called with a Document
        return renderer.render(document)  # type: ignore[no-any-return]


__all__ = [
    "SlackBlocksRenderer",
    "TableBlock",
    "markdown_to_block_objects",
    "markdown_to_blocks",
]
__version__ = "0.2.0"
