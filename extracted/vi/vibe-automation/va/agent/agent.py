import os
from typing import List

import anthropic
import instructor
from anthropic.types import (
    TextBlockParam,
    ImageBlockParam,
    MessageParam,
)


def create_user_message(prompt: str, screenshot: str | None = None) -> MessageParam:
    text_block: TextBlockParam = {
        "type": "text",
        "text": prompt,
    }
    blocks: List[TextBlockParam | ImageBlockParam] = [text_block]
    if screenshot is not None:
        image_block: ImageBlockParam = {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": "image/png",
                "data": screenshot,
            },
        }
        blocks.append(image_block)
    return {
        "role": "user",
        "content": blocks,
    }


class Agent:
    """Base agent class for general automation."""

    def __init__(self):
        """Create a new Agent instance."""
        self.model = "claude-sonnet-4-20250514"
        self.max_iterations = 100  # Maximum number of actions to prevent infinite loops

        # Use API key from environment variable if not provided
        anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")

        if not anthropic_api_key:
            raise ValueError(
                "Claude API key not provided. Please provide it via the api_key parameter "
                "or set the ANTHROPIC_API_KEY environment variable."
            )

        self.client = anthropic.Anthropic(api_key=anthropic_api_key)
        # provides structured output
        self.instructor_client = instructor.from_anthropic(self.client)
