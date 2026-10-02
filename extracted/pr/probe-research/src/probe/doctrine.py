"""The destination vocabulary every write surface must teach.

WHAT THIS FILE IS NOT, ANY MORE. It held the tracking doctrine in fragments,
composed into the always-loaded pointer block (`cli/agent_rules.POINTER_BODY`)
and the MCP instruction sheet (`mcp/server.MCP_INSTRUCTIONS`). Two surfaces
teaching the same rules had drifted once -- a routing rework reached one and not
the other, and agents were handed two contradictory doctrines in the same
session -- so writing the sentences once made drift impossible rather than
tested for.

That stopped being true on 2026-09-05, when the write doctrine was cut from the
read-only MCP sheet: no fragment had a second reader, and the indirection only
hid each prompt from the person editing it. The prose now lives in the one
surface that ships it, and the fragments were inlined byte-for-byte on
2026-09-13; the body itself was rewritten on 2026-09-17 (POINTER_VERSION 33).

WHAT IS STILL SHARED, and why it survives the inlining: these two tuples are not
prose. They are the checklist `tests/test_doctrine_sync.py` runs against the
`track-work` skill markdown, which cannot import Python and therefore cannot be
held to the prompt by construction -- only by census. The failure that census
repairs was measured: a tenant's agents wrote 140k characters of notes and
uploaded zero files, because every destination the prompts enumerated was prose.
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
    "AI Summary",
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
