"""Platform-level capability bundles shipped with matrx-ai.

Bundles here are the ones that exist regardless of who is hosting matrx-ai.
Matrix Local calls matrx-ai directly today; sandboxes will soon. Both need
the platform-level capabilities (sandbox-fs, shell routing, etc.) to work
out of the box.

Product-specific bundles (``editor-state`` for VSCode, ``aidream-app``,
future ``chrome-extension``-specific shapes) live in the host application
and are registered via ``matrx_ai.configure(capabilities=[...])``. matrx-ai
must never import from a host.

Module import side-effect: registers every bundle defined here into the
global registry. Re-imports are idempotent (``register_capability`` is
no-op when called with the same instance).
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from matrx_ai.tools.specs import RegisteredToolSpec

from .models import Capability
from .registry import register_capability


class SandboxFsPayload(BaseModel):
    """Wire-validated mirror of ``matrx_ai.tools._sandbox_proxy.SandboxBinding``.

    The runtime ``SandboxBinding`` is a frozen dataclass; this Pydantic mirror
    exists purely to validate the request payload before it's stashed on
    ``AppContext`` for fs/shell tools to read. Keep the field set in lockstep
    with ``SandboxBinding``.
    """

    sandbox_id: str = Field(min_length=1)
    base_url: str = Field(min_length=1)
    access_token: str = Field(min_length=1)
    root_path: str = "/home/agent"
    target_kind: Literal["sandbox", "local_machine"] = "sandbox"
    """Semantic target namespace; never infer it from OS-specific paths."""


# The coding toolset auto-armed whenever a sandbox is attached. These are
# ordinary server-executed tools (``delegate=False`` default) that already
# detect ``ctx.metadata["active_sandbox"]`` at runtime and proxy fs/shell/git
# operations into the container. Declaring them here is what makes "attach a
# box" actually give the agent hands — without it the binding is inert because
# a normal agent carries none of these tools. This rides the canonical
# capability auto-injection path (resolve_client_capabilities → enabled_tools),
# the same mechanism behind editor-state → vsc_get_state and browser-dom.
_SANDBOX_FS_TOOLS = (
    RegisteredToolSpec(name="fs_read"),
    RegisteredToolSpec(name="fs_write"),
    RegisteredToolSpec(name="fs_edit"),
    RegisteredToolSpec(name="fs_patch"),
    RegisteredToolSpec(name="fs_list"),
    RegisteredToolSpec(name="fs_mkdir"),
    RegisteredToolSpec(name="fs_search"),
    RegisteredToolSpec(name="shell_execute"),
    RegisteredToolSpec(name="shell_python"),
    RegisteredToolSpec(name="git_ingest"),
)

_SANDBOX_FS = Capability(
    name="sandbox-fs",
    description=(
        "Caller has an attached Matrx Sandbox container with filesystem and "
        "shell. matrx-ai's fs_* and shell_* tools route through the sandbox "
        "proxy instead of executing on the host filesystem."
    ),
    payload_model=SandboxFsPayload,
    enabled_tools=_SANDBOX_FS_TOOLS,
    requires_auth=True,
)


# Platform-level skills capability. Every authenticated agent gets the unified
# ``skill`` tool (action=list|get|search) unless the agent's
# ``skill_config.disabled = true`` kill switch is set (honored at request prep
# in apply_unified_skills). The capability itself carries no payload — per-agent
# tiering lives on ``agx_agent.skill_config``, not in a client envelope (SK-S1/S4).
_AGENT_SKILLS_TOOLS = (RegisteredToolSpec(name="skill"),)

_AGENT_SKILLS = Capability(
    name="agent-skills",
    description=(
        "Markdown skill library — discoverable conventions, workflows, "
        "references, modes, and agent-behavior bundles. The agent gets one "
        "action-dispatched tool to browse (list), fetch (get), and search."
    ),
    enabled_tools=_AGENT_SKILLS_TOOLS,
    requires_auth=True,
)


# Durable, per-user filesystem WITHOUT a sandbox. Arms the SAME server-executed fs/shell
# tools as sandbox-fs, but carries NO binding payload: with no sandbox attached and a durable
# VFS backend installed, those tools route to the user's persistent code_files store (home =
# /home/agent). A sandbox, when present, still wins (real container). This is the opt-in switch
# for "give this agent real, persistent hands" — attach it to the specific agents that need it;
# small agents that carry it not are unaffected.
_AGENT_FS_TOOLS = (
    RegisteredToolSpec(name="fs_read"),
    RegisteredToolSpec(name="fs_write"),
    RegisteredToolSpec(name="fs_edit"),
    RegisteredToolSpec(name="fs_list"),
    RegisteredToolSpec(name="fs_mkdir"),
    RegisteredToolSpec(name="fs_search"),
    RegisteredToolSpec(name="shell_execute"),
)

_AGENT_FS = Capability(
    name="agent-fs",
    description=(
        "The agent has a DURABLE, per-user filesystem backed by the user's code files "
        "(code.code_files), reachable with fs_read/fs_write/fs_edit/fs_list/fs_mkdir/"
        "fs_search and shell_execute even with NO sandbox attached. Files persist across "
        "conversations and appear in the user's Code Snippets. Home is /home/agent "
        "(projects/, scratch/, .matrx/). If a sandbox IS attached, these tools use the "
        "container instead."
    ),
    enabled_tools=_AGENT_FS_TOOLS,
    requires_auth=True,
)


def _register_built_ins() -> None:
    register_capability(_SANDBOX_FS)
    register_capability(_AGENT_FS)
    register_capability(_AGENT_SKILLS)
    # browser-dom — matrx-extend Chrome extension. The first multi-tool
    # capability with a discovery tool; serves as the template for future
    # Chrome-extension-style bundles. See ``browser_dom.py``.
    from matrx_ai.capabilities.browser_dom import BROWSER_DOM

    register_capability(BROWSER_DOM)
    # desktop-native — matrx-local desktop app. Same discovery-tool shape as
    # browser-dom: boots with only ``load_desktop_tools``; the 19 desktop
    # mega-tools (executor matrx-local) load per-category on demand and
    # delegate to the user's machine. See ``desktop_native.py``.
    from matrx_ai.capabilities.desktop_native import DESKTOP_NATIVE

    register_capability(DESKTOP_NATIVE)


_register_built_ins()
