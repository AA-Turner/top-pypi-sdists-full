"""Compatibility facade for CCR review-body finding parsers."""

from __future__ import annotations

from agentic_devtools.cli.github.ccr_finding_content_key import (
    _finding_content_key as _finding_content_key,
)
from agentic_devtools.cli.github.ccr_finding_content_start import (
    _finding_start_matches as _finding_start_matches,
)
from agentic_devtools.cli.github.ccr_finding_content_start import (
    _is_explanatory_standalone_location as _is_explanatory_standalone_location,
)

__all__ = [
    "_finding_content_key",
    "_finding_start_matches",
    "_is_explanatory_standalone_location",
]
