"""Utility modules for EmDash."""

from .logger import log, setup_logger

from .image import (
    is_clipboard_image_available,
    read_clipboard_image,
    encode_image_to_base64,
    encode_image_for_llm,
    get_image_info,
    estimate_image_tokens,
    read_and_prepare_image,
    ClipboardImageError,
    ImageProcessingError,
    ImageFormat,
)

from .git import (
    get_git_remote_url,
    normalize_repo_url,
    get_normalized_remote_url,
)

__all__ = [
    # Logger
    "log",
    "setup_logger",
    # Image
    "is_clipboard_image_available",
    "read_clipboard_image",
    "encode_image_to_base64",
    "encode_image_for_llm",
    "get_image_info",
    "estimate_image_tokens",
    "read_and_prepare_image",
    "ClipboardImageError",
    "ImageProcessingError",
    "ImageFormat",
    # Git
    "get_git_remote_url",
    "normalize_repo_url",
    "get_normalized_remote_url",
]
