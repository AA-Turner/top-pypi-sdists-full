import logging
import base64
import os
from typing import Type, TypeVar, Union, overload, List
from pydantic import BaseModel
from .agent.agent import Agent

log = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


def _load_image_as_base64(file_path: str) -> tuple[str, str]:
    """
    Load an image file and convert it to base64.

    Args:
        file_path: Path to the image file

    Returns:
        Tuple of (base64_data, media_type)

    Raises:
        ValueError: If file doesn't exist or unsupported format
    """
    if not os.path.exists(file_path):
        raise ValueError(f"Image file not found: {file_path}")

    # Get file extension to determine media type
    _, ext = os.path.splitext(file_path.lower())

    if ext in [".jpg", ".jpeg"]:
        media_type = "image/jpeg"
    elif ext == ".png":
        media_type = "image/png"
    else:
        raise ValueError(
            f"Unsupported image format: {ext}. Only JPG and PNG are supported."
        )

    # Read and encode the file
    with open(file_path, "rb") as f:
        image_data = f.read()

    base64_data = base64.b64encode(image_data).decode("utf-8")
    return base64_data, media_type


def _create_message_with_attachments(
    prompt_text: str, attachments: List[str] = []
) -> dict:
    """
    Create a message dictionary with text and optional image attachments.

    Args:
        prompt_text: The text content of the message
        attachments: Optional list of image file paths

    Returns:
        Message dictionary formatted for Anthropic API
    """
    content_blocks = [{"type": "text", "text": prompt_text}]

    if attachments:
        for attachment_path in attachments:
            try:
                filename = os.path.basename(attachment_path)
                filename_block = {"type": "text", "text": f"\nFile: {filename}"}
                content_blocks.append(filename_block)

                base64_data, media_type = _load_image_as_base64(attachment_path)
                image_block = {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": media_type,
                        "data": base64_data,
                    },
                }
                content_blocks.append(image_block)
                log.info(f"Added image attachment: {attachment_path}")
            except Exception as e:
                log.error(f"Failed to load image {attachment_path}: {e}")
                raise

    return {"role": "user", "content": content_blocks}


@overload
async def prompt(
    prompt_text: str,
    response_model: Type[T],
    max_retries: int = 3,
    attachments: List[str] = [],
) -> T: ...


@overload
async def prompt(
    prompt_text: str,
    response_model: Type[str] = str,
    max_retries: int = 3,
    attachments: List[str] = [],
) -> str: ...


async def prompt(
    prompt_text: str,
    response_model: Union[Type[T], Type[str]] = str,
    max_retries: int = 3,
    attachments: List[str] = [],
) -> Union[T, str]:
    """
    Sends a prompt to the LLM and returns a response.

    Args:
        prompt_text: The text prompt to send to the LLM.
        response_model: If a Pydantic model is provided, the response will be a validated JSON object.
                        If not provided or set to str, it will be a string.
        max_retries: The maximum number of times to retry if the LLM response is not valid.
        attachments: Optional list of image file paths (JPG/PNG) to include with the prompt.

    Returns:
        If response_model is a Pydantic model, an instance of that model.
        Otherwise, the response from the LLM as a string.
    """
    agent = Agent()

    message = _create_message_with_attachments(prompt_text, attachments)

    if response_model is str:
        response = agent.client.messages.create(
            model=agent.model,
            max_tokens=4000,
            messages=[message],
        )
        if response.content and len(response.content) > 0:
            return response.content[0].text
        return ""
    else:
        response = agent.instructor_client.messages.create(
            model=agent.model,
            max_tokens=4000,
            messages=[message],
            response_model=response_model,
            max_retries=max_retries,
        )
        return response
