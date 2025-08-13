"""
Constants used throughout the VA (Vibe Automation) framework.
"""

import os

REVIEW_TIMEOUT = 600  # Default timeout in seconds for review operations

# Disable the fallback for page.get_by_prompt and page.step
VA_DISABLE_FALLBACK = os.environ.get("VA_DISABLE_FALLBACK") is not None

# Enable global exception capturing and recovery, this is turned off by default until rollout
VA_ENABLE_RECOVERY = os.environ.get("VA_ENABLE_RECOVERY") is not None

VA_DISABLE_LOGIN_REVIEW = os.environ.get("VA_DISABLE_LOGIN_REVIEW") is not None

VA_ENABLE_SUBTASK_AGENT = os.environ.get("VA_ENABLE_SUBTASK_AGENT") is not None
