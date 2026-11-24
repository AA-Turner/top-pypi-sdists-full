"""ONE seam for the tool layer's size limits as an organization's knob rows.

A tool's limit (how much of a file one ``fs_read`` returns, how big one SQL cell may be, how
much page text the summarizer is handed) is an opinion, so it is a row an admin changes
(``platform.feature_knob``), never a constant (law 6, ``limits-are-knobs-agents-set-them``).
matrx-ai may not import the host, so the host installs ONE reader with
:func:`set_tool_knob_resolver`; every tool reads through :func:`tool_knob_int`.

With no reader (matrx-ai standalone) the KNOB MIRROR the call site passes is the honest answer.
With a reader, a MISSING row is filed to the error queue (``feature_knob_missing``) through
``matrx_utils.knob_fallback`` and the mirror — the value the seed row carries — is used; any
other failure raises to the tool, whose executor records it (feature-knobs rule 3).

The knob addresses live in :data:`TOOL_KNOBS` so the host and the seed rows name the same keys.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable

from matrx_utils.knob_fallback import knob_or_declared_default

#: ``async (feature, key, organization_id) -> int``.
ToolKnobResolver = Callable[[str, str, str | None], Awaitable[int]]

#: Every tool limit read through this seam: name → (feature, key). The seed rows use these.
TOOL_KNOBS: dict[str, tuple[str, str]] = {
    "fs_read_max_chars": ("tools.fs_read", "read_max_chars"),
    "cloud_file_result_max_chars": ("tools.cloud_file", "result_max_chars"),
    "sql_cell_max_chars": ("tools.sql", "cell_max_chars"),
    "summarize_max_input_chars": ("agents.web_read", "summarize_max_input_chars"),
}

#: KNOB MIRROR of platform.feature_knob "agents.web_read" "summarize_max_input_chars": the most
#: page text one summarize call hands the ``tools.summarize_content`` mandate.
SUMMARIZE_MAX_INPUT_CHARS = 100_000

_resolver: ToolKnobResolver | None = None


def set_tool_knob_resolver(resolver: ToolKnobResolver | None) -> None:
    """Install the host's per-organization knob reader (``None`` = standalone)."""
    global _resolver
    _resolver = resolver


async def tool_knob_int(name: str, mirror: int, organization_id: str | None) -> int:
    """This organization's value of the tool knob ``name`` (a key of :data:`TOOL_KNOBS`).

    ``mirror`` is the KNOB MIRROR the call site declares (the seed row's value)."""
    feature, key = TOOL_KNOBS[name]
    resolver = _resolver
    if resolver is None:
        return mirror

    async def _read() -> int:
        return int(await resolver(feature, key, organization_id))

    value = await knob_or_declared_default(
        _read,
        feature=feature,
        key=key,
        declared_default=mirror,
        consequence=f"the tool runs on the code mirror {mirror:,} until the row is seeded",
    )
    return value if value > 0 else mirror
