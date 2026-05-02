"""
DEPRECATED: duckduckgo-mcp has been renamed to web-forager.

Install the new package: pip install web-forager
"""

import warnings

warnings.warn(
    "The 'duckduckgo-mcp' package has been renamed to 'web-forager'. "
    "Please install 'web-forager' instead: pip install web-forager",
    DeprecationWarning,
    stacklevel=2,
)

# Re-export everything from web_forager for backward compatibility
from web_forager import *  # noqa: F401, F403
from web_forager import __version__
