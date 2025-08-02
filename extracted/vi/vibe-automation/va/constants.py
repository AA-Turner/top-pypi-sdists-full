"""
Constants used throughout the VA (Vibe Automation) framework.
"""

import os

REVIEW_TIMEOUT = 600  # Default timeout in seconds for review operations

# Environment variable flags
VA_DISABLE_FALLBACK = os.environ.get("VA_DISABLE_FALLBACK") is not None

VA_DISABLE_LOGIN_REVIEW = os.environ.get("VA_DISABLE_LOGIN_REVIEW") is not None
