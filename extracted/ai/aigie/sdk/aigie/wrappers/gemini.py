"""Tracing wrapper for the Google Gemini client.

Not implemented. `wrap_gemini` accepts a client, warns, and hands it straight
back untraced, which is what it has always done — moved here unchanged so every
provider has a module, rather than because anything was fixed. Implementing it
is separate work.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


def wrap_gemini(client: Any, aigie_client: Any | None = None) -> Any:
    """
    Wrap Google Gemini client for automatic tracing.

    Args:
        client: Gemini client instance
        aigie_client: Optional Aigie client

    Returns:
        The client unchanged — this wrapper does not trace yet.

    Example:
        import google.generativeai as genai
        from aigie.wrappers import wrap_gemini

        genai.configure(api_key="...")
        model = wrap_gemini(genai.GenerativeModel('gemini-pro'))

        response = model.generate_content("Hello")
    """
    logger.warning("Gemini wrapper not yet fully implemented")
    return client
