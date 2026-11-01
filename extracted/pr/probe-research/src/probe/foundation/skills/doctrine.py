"""The destination vocabulary every write surface must teach: the checklist
`tests/test_doctrine_sync.py` runs against the `track-work` skill markdown. DESIGN.md (doctrine.py).
"""

from __future__ import annotations

#: Destinations the track-work skill markdown must NAME. The test censuses the
#: skill; the pointer block routes to it and is not censused.
CORE_DESTINATIONS: tuple[str, ...] = (
    "artifacts",
    "metrics",
    "span",
    "notes",
    "lineage",
    "workspace",
    "Shared folder",
    "description",
    # A project's or experiment's summary (writer-owns-summary): the researcher's block is theirs,
    # the rest the recorder's.
    "summary",
    "question",
    "team note",
    "secrets",
    "reference",
)

#: Named by the skill; the pointer block and the MCP sheet stay shorter.
DETAIL_DESTINATIONS: tuple[str, ...] = (
    "group",
    "version",
)
