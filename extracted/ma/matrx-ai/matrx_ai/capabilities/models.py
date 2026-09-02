"""Capability data types.

A ``Capability`` is the unit the registry stores. A ``ClientContext`` is the
unit the request envelope carries. Both are immutable: the registry is
populated at startup and read at request time; the client context is parsed
from the request body and never mutated server-side.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator

from matrx_ai.tools.specs import ToolSpec


@dataclass(frozen=True)
class Capability:
    """A named bundle of (a) typed client state and (b) tool enablements.

    A capability is the surface's manifest entry for one logical client
    integration. When a request declares this capability, its tools become
    candidates for the session toolset — the merge then decides which
    candidates are actually injected based on disposition + agent request.

    Disposition (default vs optional) is per-tool-list, not per-spec:

    - ``enabled_tools`` / ``enabled_tools_factory`` → ``default`` disposition.
      Auto-injected on every request that declares this capability, unless
      excluded by agent.forbidden or user.remove.
    - ``optional_tools`` / ``optional_tools_factory`` → ``optional`` disposition.
      Injected only when the agent's or user's tool list names the tool
      explicitly.

    Both pairs may be set; both are merged into their respective bucket. A
    capability with empty defaults + empty optionals still carries a payload
    (e.g. ``sandbox-fs``) — declaring the capability brings no tools but
    routes existing tools differently via ``AppContext`` metadata.
    """

    name: str
    payload_model: type[BaseModel] | None = None
    enabled_tools: tuple[ToolSpec, ...] = ()
    enabled_tools_factory: Callable[[], tuple[ToolSpec, ...]] | None = None
    optional_tools: tuple[ToolSpec, ...] = ()
    optional_tools_factory: Callable[[], tuple[ToolSpec, ...]] | None = None
    requires_auth: bool = True
    description: str = ""


class SurfaceAmendments(BaseModel):
    """Per-request delta against the surface's cached/declared manifest.

    Per TOOL_ROUTING_RULES.md §11:
      - ``add``:    extra tool specs the surface is bringing in this request.
                    Treated as ``default`` disposition. Logged loudly for
                    well-known surfaces (a signal that DB or surface code
                    is out of sync).
      - ``remove``: names to drop from the surface manifest for this
                    request. Logged loudly for well-known surfaces.

    ``rebind`` (changing executor binding for an already-bound name) is a
    future field and not yet wired.
    """

    add: list[ToolSpec] = Field(default_factory=list)
    remove: list[str] = Field(default_factory=list)


class ClientContext(BaseModel):
    """Request envelope describing the calling client's surface + capabilities + state.

    Two orthogonal concepts ride on this envelope:

    - ``surface`` — single string naming the UI context the request originated
      from (e.g. ``matrx-user/chat``, ``chrome-extension/pilot``). The host
      resolves this against its surface registry (``ui.ui_surface`` in
      aidream) to derive the default tool set + value bindings, with
      inheritance from ``matrx-default/default``.

    - ``capabilities`` — list of payload-bearing capabilities the client is
      activating (e.g. ``editor-state``, ``sandbox-fs``, ``browser-dom``).
      Each capability has a Pydantic payload validator registered in the
      capability registry and may bring extra tools online. Multiple may
      activate simultaneously (a coding-IDE-on-a-browser-page declares both
      ``editor-state`` and ``browser-dom``).

    Wire shape::

        {
          "surface": "matrx-user/chat",
          "capabilities": ["editor-state"],
          "state": { "editor-state": {"active_file": {...}, ...} },
          "amendments": { "add": [...], "remove": [...] },
          "mcp": ["openai-tools", "stripe-mcp"]
        }

    The ``surface`` field is host-validated: an unknown name surfaces as a
    422. ``amendments`` apply on top of whatever the surface resolution
    produced. ``mcp`` adds session-only MCP server slugs.
    """

    surface: str | None = None
    capabilities: list[str] = Field(default_factory=list)
    state: dict[str, dict[str, Any]] = Field(default_factory=dict)
    amendments: SurfaceAmendments | None = None
    mcp: list[str] = Field(default_factory=list)
    apply_policy: Literal["auto", "ask", "off"] | None = None
    """Surface layer of the output-directive apply cascade (agent → SURFACE →
    user). The calling surface's policy for model-emitted side effects; overrides
    the agent's own setting on conflict. None ⇒ the surface defers to the agent.
    A surface dedicated to one action (e.g. a create-project modal) sets ``auto``;
    a general chat surface leaves it None (system default ``ask``). The host
    resolves the cascade — see aidream output_directives/policy.py."""

    @model_validator(mode="after")
    def _normalize_desktop_state_compatibility(self) -> ClientContext:
        """Treat a desktop payload as the canonical capability declaration.

        Early Tier-2 clients shipped ``state['desktop-native']`` before they
        also emitted the matching capabilities entry.  Keeping that wire form
        compatible is safe because normal capability resolution still applies
        the desktop bundle's authentication and payload validation gates.
        """
        if "desktop-native" not in self.state:
            return self
        if "desktop-native" in self.capabilities:
            return self
        self.capabilities = [*self.capabilities, "desktop-native"]
        return self


class UserOverrides(BaseModel):
    """Per-request user-level inclusion / exclusion overrides.

    Per TOOL_ROUTING_RULES.md §5–§6, the user's add/remove pair has the
    highest inclusion precedence: ``user.remove`` beats everything;
    ``user.add`` beats ``agent.forbidden`` and surface defaults' implicit
    silence on optional tools.

    Validation: ``add ∩ remove`` must be empty — the merge primitive
    rejects the request with HTTP 422 when the sets overlap.
    """

    add: list[str] = Field(default_factory=list)
    remove: list[str] = Field(default_factory=list)
    apply_policy: Literal["auto", "ask", "off"] | None = None
    """User layer of the output-directive apply cascade (agent → surface → USER).
    The big boss: overrides both the agent and the surface. ``auto`` = "just do
    it", ``ask`` = "always confirm", ``off`` = "suppress". None ⇒ defer to surface
    /agent. Resolved by the host — see aidream output_directives/policy.py."""


class CapabilityResolutionError(ValueError):
    """Raised when a client capability declaration is invalid.

    Triggered by:
      - Unknown capability name (the client declared something the server
        doesn't know about — strict, no silent drops).
      - Auth requirement violated (capability marked ``requires_auth=True``
        but the request is unauthenticated).
      - Payload validation failure (``state[name]`` doesn't match the
        capability's ``payload_model`` schema).

    The error message names every violation so a misbehaving client gets
    actionable feedback in one shot rather than failing one capability at a
    time.
    """
