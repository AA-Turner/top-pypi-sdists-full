import base64
import re
from typing import Dict, List


def extract_content_by_tags(text: str, tags: list[str]) -> dict[str, str | None]:
    """Extracts the first occurrence of content inside specified tags and returns a dictionary.

    Parameters:
        text (str): The input string containing various tags.
        tags (list[str]): A list of tag names to extract content from.

    Returns:
        dict[str, Optional[str]]: A dictionary where keys are tag names,
            and values are the first content string or None if the tag is not found.
    """
    extracted: dict[str, str | None] = {}

    for tag in tags:
        # Build a regex pattern dynamically for each tag
        pattern = rf"<{tag}>(.*?)</{tag}>"
        # Find the first match for the current tag
        match = re.search(pattern, text, re.DOTALL)
        # Assign None if no match, otherwise assign the matched string
        extracted[tag] = match.group(1) if match else None

    return extracted


def simple_prompt_to_messages(
    prompt: str, images: Dict[str, bytes] = None
) -> List[Dict]:
    """
    Simple version of prompt_to_messages that handles image placeholders.

    Args:
        prompt: Prompt string with <image:name> placeholders
        images: Dictionary of image_name -> image_bytes

    Returns:
        OpenAI messages format
    """
    if not images:
        return [{"role": "user", "content": prompt}]

    content = []

    # Process prompt to handle image placeholders
    parts = re.split(r"(<image:[^>]+>)", prompt)

    for part in parts:
        if part.startswith("<image:"):
            # Extract image name
            img_name = part[7:-1]  # Remove <image: and >

            if img_name in images:
                # Add image to content
                img_base64 = base64.b64encode(images[img_name]).decode("utf-8")
                content.append(
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{img_base64}"},
                    }
                )
        elif part.strip():
            # Add text part
            content.append({"type": "text", "text": part})

    return [{"role": "user", "content": content}]
