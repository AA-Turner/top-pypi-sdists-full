"""Compatibility façade for the meta-installer.

The implementation now lives in single-responsibility modules:

- :mod:`registry` — the declarative ``TOOLS`` registry and its types.
- :mod:`orchestrator` — the install/configure engine and env resolution.
- :mod:`selection` — the interactive tool-selection checklist.
- :mod:`render` — terminal rendering.
- :mod:`cli` — the ``pysae-ai-tools tools`` Typer app.

This module re-exports the historical public surface so existing imports
(``from pysae_ai_tools.install.all import TOOLS``) and the ``tools`` CLI
target keep working unchanged.
"""

from .cli import _resolve_tools as _resolve_tools
from .cli import app as app
from .cli import configure as configure
from .cli import install as install
from .cli import require as require
from .cli import status as status
from .orchestrator import Result as Result
from .orchestrator import _classify as _classify
from .orchestrator import _configure_env_vars as _configure_env_vars
from .orchestrator import _configure_one as _configure_one
from .orchestrator import _ensure_system_deps as _ensure_system_deps
from .orchestrator import _ensure_tool_deps as _ensure_tool_deps
from .orchestrator import _install_one as _install_one
from .orchestrator import _install_pretty as _install_pretty
from .orchestrator import _preload_secrets as _preload_secrets
from .orchestrator import _resolve_env_section as _resolve_env_section
from .orchestrator import _resolve_post_configure as _resolve_post_configure
from .orchestrator import _result_for_unselected as _result_for_unselected
from .orchestrator import _state_dict as _state_dict
from .orchestrator import install_all as install_all
from .orchestrator import uninstall_mcp_servers as uninstall_mcp_servers
from .registry import CATEGORY_ORDER as CATEGORY_ORDER
from .registry import TOOL_NAMES as TOOL_NAMES
from .registry import TOOLS as TOOLS
from .registry import Category as Category
from .registry import Mode as Mode
from .registry import Tool as Tool
from .registry import ToolEnv as ToolEnv
from .registry import _find_tool as _find_tool
from .registry import _instance as _instance
from .registry import _module_env as _module_env
from .registry import _tools_by_category as _tools_by_category
from .render import CATEGORY_HEADER as CATEGORY_HEADER
from .render import CATEGORY_ICON as CATEGORY_ICON
from .render import SECTION_ENV as SECTION_ENV
from .render import SECTION_RULE as SECTION_RULE
from .render import SECTION_SUMMARY as SECTION_SUMMARY
from .render import _binary_probe as _binary_probe
from .render import _category_header as _category_header
from .render import _extract_identity as _extract_identity
from .render import _render_install_result as _render_install_result
from .render import _render_tool_status as _render_tool_status
from .render import _section_header as _section_header
from .render import _status_all as _status_all
from .render import _status_binaries as _status_binaries
from .render import _status_one as _status_one
from .render import _version_hint as _version_hint
from .selection import _checklist_label as _checklist_label
from .selection import _effective_known as _effective_known
from .selection import _initial_selected_set as _initial_selected_set
from .selection import _prompt_tool_selection as _prompt_tool_selection

if __name__ == "__main__":
    app()
