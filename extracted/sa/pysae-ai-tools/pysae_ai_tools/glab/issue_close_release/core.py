"""Pure parsing logic for ``glab issue-close-release`` (no I/O — unit-testable).

An annotated release tag carries the changelog section in its message (written
by ``ci/release/run.py`` as ``section_raw``). Every shipped ticket is referenced
there, either as a same-project ref ``(#1234)`` or a cross-project ref
``(op#1722)`` / ``(gtfsrt-to-siri#16)`` / ``(pysae/op#1705)``. This module turns
that text into the list of issues to close.
"""

import re
from dataclasses import dataclass

from ...common.group import ensure_group_namespace

# Lenient refs — match the opening "(" or "([" without requiring the closing
# paren, mirroring the proven behaviour of issue-workflow-update's _ISSUE_REF.
# The two patterns are disjoint: the internal one needs "#" right after "(" or
# "([", while the external one needs at least one path char there instead.
#   (#1234)              / ([#1234](url))            → same project
#   (op#1722)            / ([op#1722](url))          → cross-project (short path)
#   (pysae/op#1705)      / ([pysae/op#1705](url))    → cross-project (full path)
_INTERNAL_REF = re.compile(r"\(\[?#(\d+)")
_EXTERNAL_REF = re.compile(r"\(\[?([\w.-]+(?:/[\w.-]+)*)#(\d+)")


@dataclass(frozen=True)
class IssueRef:
    """A ticket referenced in a release. ``project_path`` is ``None`` for the
    release's own project, or the ``group/project`` path for a cross-project
    ref (namespaced under the resolved group)."""

    project_path: str | None
    iid: int


def parse_issue_refs(text: str, group: str) -> list[IssueRef]:
    """Extract the unique issue references from a release tag message / changelog.

    Same-project refs become ``IssueRef(None, iid)``; cross-project refs become
    ``IssueRef("<group>/<project>", iid)`` — bare project names are namespaced under
    ``group`` (resolved by the caller; this module stays pure / I/O-free). Results are
    de-duplicated and sorted (own project first, then by path, then by IID).
    """
    refs: set[IssueRef] = set()
    for match in _INTERNAL_REF.finditer(text):
        refs.add(IssueRef(None, int(match.group(1))))
    for match in _EXTERNAL_REF.finditer(text):
        refs.add(IssueRef(ensure_group_namespace(match.group(1), group), int(match.group(2))))
    return sorted(refs, key=lambda r: (r.project_path or "", r.iid))
