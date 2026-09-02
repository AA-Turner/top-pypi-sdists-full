"""``desktop-native`` capability — matrx-local desktop client bundle (W7).

The matrx-local desktop app is the platform's portal to the user's machine:
files, shell, windows, input, media, local browser, macOS/Windows app
integrations. Its tool surface is the 19 action-enum mega-tools bound to the
``matrx-local`` executor (collapsed from 115 flat tools, 2026-07-14).

Even 19 mega-tools is too many to advertise up front, so this capability
follows the ``browser-dom`` discovery pattern: the agent boots with ONE
tool — ``load_desktop_tools`` — and calls it with a category to pull the
relevant mega-tools into the active toolset on demand.

Tool definitions and routing live exclusively in the database:
  - ``tool.definition`` — the 19 ``local_*`` mega-tool rows, each carrying a
    ``category`` in the desktop bundle taxonomy: ``desktop`` (machine
    control) or ``desktop-web`` (internet access from the machine).
    Consolidated from the original 9-way ``desktop-*`` split, 2026-07-17.
  - ``tool.binding`` — rows binding them to executor ``matrx-local``, which
    is what makes ``resolve_executor_binding`` route the calls to the client
    (suspend/delegation) instead of the server.
  - ``ui.ui_surface`` row ``matrx-local/desktop`` (executor ``matrx-local``)
    puts the desktop in the active-executor set for surface-driven requests.

All lookups are lazy (first request after startup) so this module never
touches the DB at import time.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from matrx_ai.capabilities.models import Capability
from matrx_ai.tools.specs import RegisteredToolSpec, ToolSpec

# ---------------------------------------------------------------------------
# Payload model — validates ``client.state["desktop-native"]`` on the wire.
# ---------------------------------------------------------------------------

TunnelState = Literal["none", "active", "error"]


class DesktopNativePayload(BaseModel):
    """Runtime state from the matrx-local desktop engine that drives
    tool-routing decisions in ``load_desktop_tools``.

    Orchestration metadata consumed by the server-side discovery handler,
    not the LLM.
    """

    platform: str = Field(
        default="",
        description="The desktop's ``sys.platform`` value (``darwin`` / "
        "``win32`` / ``linux``). Discovery filters OS-gated mega-tools "
        "(desktop-mac / desktop-windows) against it. Empty = unknown, "
        "nothing is filtered.",
    )
    engine_version: str = Field(
        default="",
        description="matrx-local engine version string.",
    )
    instance_id: str = Field(
        default="",
        description="The desktop instance id (cloud_sync identity) so "
        "multi-device users can be disambiguated downstream.",
    )
    target_instance_id: str = Field(
        default="",
        description="Optional desktop instance id selected by a non-desktop "
        "surface for this turn. Delegated matrx-local tool calls are stamped "
        "with this target so only that desktop claims them.",
    )
    tunnel_state: TunnelState = Field(
        default="none",
        description="Reachability of the desktop over its public tunnel. "
        "Informational for routing hints; Broadcast rpc works without it.",
    )
    permissions_granted: list[str] = Field(
        default_factory=list,
        description="OS-level permissions the user has granted the desktop "
        "app (e.g. screen-recording, accessibility, contacts). Currently "
        "informational; per-tool permission gating can key off it later.",
    )
    loaded_categories: list[str] = Field(
        default_factory=list,
        description="Desktop categories already discovered earlier in this "
        "conversation; ``load_desktop_tools`` short-circuits re-loads.",
    )


# ---------------------------------------------------------------------------
# Identifiers
# ---------------------------------------------------------------------------

MATRX_LOCAL_EXECUTOR = "matrx-local"
DESKTOP_SURFACE = "matrx-local/desktop"


def _enabled_tools() -> tuple[ToolSpec, ...]:
    """The desktop boots with exactly ONE advertised tool: the discovery
    loader. The mega-tools themselves are pulled in per-category by
    ``load_desktop_tools`` (matrx_ai/tools/implementations/desktop_discovery.py).
    """
    return (RegisteredToolSpec(name="load_desktop_tools", delegate=False),)


DESKTOP_NATIVE = Capability(
    name="desktop-native",
    description=(
        "Caller has a matrx-local desktop engine online — the user's own "
        "machine as a tool executor (private files, shell, windows, input, "
        "media, local browser, OS app integrations). Platform / engine "
        "version / tunnel state ride in state['desktop-native']. The agent "
        "boots with only ``load_desktop_tools``; calling it with a category "
        "loads the relevant desktop mega-tools on demand, and their calls "
        "delegate to the desktop for execution."
    ),
    payload_model=DesktopNativePayload,
    enabled_tools_factory=_enabled_tools,
    requires_auth=True,
)
