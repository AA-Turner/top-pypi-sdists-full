# vnstock/core/utils/agents.py

"""
Thin wrapper for AI Agent skills and environment management.
The actual implementation is safely encapsulated in the `vnai` tier package.
NOT part of the public vnstock API. Do not add to __init__.py exports.
"""

import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


def load_skill_catalog() -> Optional[Dict[str, Any]]:
    """
    Fetch the catalog of all available AI skills.
    Requires vnai tier to be installed.
    """
    try:
        from vnai import load_skill_catalog as _load_catalog

        return _load_catalog()
    except ImportError:
        logger.warning(
            "Tính năng này yêu cầu gói 'vnai'. "
            "Vui lòng cài đặt bằng lệnh: pip install -U vnai"
        )
        return None
    except Exception as e:
        logger.error(f"Lỗi khi tải danh mục skill: {e}")
        return None


def load_skill(name: str, component: str = "content") -> Optional[str]:
    """
    Load protected skill content for in-session use.
    Requires vnai tier to be installed.

    Args:
        name: Skill slug (e.g., "market-analyzer")
        component: "content", "config", "script:<filename>", "reference:<filename>"
    """
    try:
        from vnai import load_skill as _load_skill

        return _load_skill(name, component)
    except ImportError:
        logger.warning(
            "Tính năng này yêu cầu gói 'vnai'. "
            "Vui lòng cài đặt bằng lệnh: pip install -U vnai"
        )
        return None
    except Exception as e:
        logger.error(f"Lỗi khi tải skill '{name}': {e}")
        return None


def clear_cache() -> None:
    """Clear in-memory skill cache."""
    try:
        from vnai import clear_skill_cache

        clear_skill_cache()
    except ImportError:
        pass


def list_cached() -> list:
    """List currently cached skill components."""
    try:
        from vnai import list_cached_skills

        return list_cached_skills()
    except ImportError:
        return []


_UPGRADE_HINT = (
    "Tính năng này yêu cầu vnai >= 2.6.0. "
    "Vui lòng cập nhật bằng lệnh: pip install -U vnai"
)


def init_agent_environment(project_root: str = ".", async_mode: bool = True) -> bool:
    """
    Write the vnstock agent bootstrap instruction into the rules files of the AI
    assistants vnai knows about.

    This touches `AGENTS.md` in `project_root` **and three machine-wide memory
    files**: `~/.gemini/GEMINI.md` (Antigravity), `~/.claude/CLAUDE.md` (Claude
    Code) and `~/.codex/AGENTS.md` (Codex). Each can be switched off on its own - see
    `agent_status()` and `disable_agent()`, or the `VNSTOCK_AGENT_TARGETS`,
    `VNSTOCK_DISABLE_GLOBAL_AGENT` and `VNSTOCK_DISABLE_AGENT_SETUP` environment
    variables.

    This feature requires the 'vnai' tier to be installed.

    Args:
        project_root: The root directory of the user's project. Default is current dir.
        async_mode: If True, runs the initialization in a background thread. Note
            that the thread is a daemon: a short-lived process may exit before it
            finishes, so pass async_mode=False when the result must be
            deterministic.

    Returns:
        bool: True if successfully started or completed, False otherwise.
    """
    try:
        if async_mode:
            from vnai import async_setup_agent_environment

            async_setup_agent_environment(project_root)
            return True
        else:
            from vnai import setup_agent_environment

            return setup_agent_environment(project_root)
    except ImportError:
        # Silently fail if vnai is not present during library init, to avoid spamming users
        return False
    except Exception as e:
        logger.error(f"Lỗi khi cấu hình agent environment: {e}")
        return False


def agent_status(project_root: str = ".") -> Optional[Dict[str, Any]]:
    """
    Report what the agent bootstrap would write and why.

    Returns a dict with the resolved per-target decision, the path of each rules
    file, whether it already exists, the config file location and any environment
    variable currently overriding the configuration.
    """
    try:
        from vnai import agent_status as _status

        return _status(project_root)
    except ImportError:
        logger.warning(_UPGRADE_HINT)
        return None


def disable_agent(*targets: str) -> Optional[Dict[str, Any]]:
    """
    Turn the agent bootstrap off and remember the choice.

    No arguments disables it entirely. Pass `"global"` to keep only the project's
    own `AGENTS.md`, or individual target names (`"antigravity"`, `"claude"`,
    `"codex"`, `"project"`).

    The choice is stored in `~/.vnstock/config/agent.json` and survives restarts.
    """
    try:
        from vnai import disable_agent_setup

        return disable_agent_setup(*targets)
    except ImportError:
        logger.warning(_UPGRADE_HINT)
        return None


def enable_agent(*targets: str) -> Optional[Dict[str, Any]]:
    """Re-enable the agent bootstrap, entirely or for the named targets."""
    try:
        from vnai import enable_agent_setup

        return enable_agent_setup(*targets)
    except ImportError:
        logger.warning(_UPGRADE_HINT)
        return None


def remove_agent_files(*targets: str) -> Optional[Dict[str, str]]:
    """
    Take the vnstock block back out of the rules files it was written into.

    Files that held nothing else are deleted; files the user also wrote in keep
    their own content. No arguments means the active targets; `"global"` leaves
    the project's `AGENTS.md` alone, `"legacy"` cleans up the paths versions
    before 2.6.0 wrote to (Cursor, Windsurf, Cline, Copilot, `~/.clauderc`,
    `~/.gemini/config/AGENTS.md`, `~/AGENTS.md`), and `"all"` does both.

    Disabling and removing are separate steps - call `disable_agent()` too, or
    the next import writes the files again.
    """
    try:
        from vnai import remove_agent_files as _remove

        return _remove(*targets)
    except ImportError:
        logger.warning(_UPGRADE_HINT)
        return None
