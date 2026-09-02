"""Independent single-fence oracle for the batched fence trim-priority pass.

This is the reference implementation of the fence ranking rules used by
:func:`agentic_devtools.cli.ci.github_provider._enforce_comment_size_limit`. It ranks
*one* fence at a time by re-deriving that fence's fence-stripped prefix from scratch,
which is the obvious-but-quadratic form the production trim loop replaced with
``_split_fence_gaps`` + ``_priorities_from_cleaned``.

It lives in the test tree because production no longer calls it, and it deliberately
imports the section pattern and the classification rule from production so the oracle
stays structurally pinned to the shipped rules: only the prefix-stripping wrapper is
duplicated here. ``test__priorities_from_cleaned.py`` pins the batched pass to it.
"""

import re

from agentic_devtools.cli.ci.github_provider import (
    _FENCE_BLOCK_RE,
    _SECTION_MARKER_RE,
    _classify_fence_priority,
    _section_marker_name,
)


def _last_section_name(text: str) -> str:
    """Return the name of the last :data:`_SECTION_MARKER_RE` match in *text*, else ``""``."""
    name = ""
    for marker in _SECTION_MARKER_RE.finditer(text):
        name = _section_marker_name(marker)
    return name


def _get_fence_trim_priority(body: str, match: re.Match[str]) -> int:
    """Rank a single fenced block so reference material is trimmed before actionable content.

    See :func:`agentic_devtools.cli.ci.github_provider._classify_fence_priority` for the
    0/2 ranking these rules produce.
    """
    # Strip completed fenced blocks from the prefix before searching for structural
    # section headings.  Without this, a review-comment body containing a literal
    # "<summary>CI Failures</summary>" string would be mistaken for a structural
    # marker and cause the fence (and any subsequent actionable comment fences) to
    # receive a lower trim priority than intended.
    prefix_without_fences = _FENCE_BLOCK_RE.sub("", body[: match.start()])

    return _classify_fence_priority(_last_section_name(prefix_without_fences))
