import json
import os
import logging

logger = logging.getLogger("state_manager")

STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".server_state.json")
STATE_FILE = os.path.normpath(STATE_FILE)


def load_state(env_root: str = "", env_url: str = "") -> dict:
    """
    Load persisted state from disk. Falls back to env variables if no
    state file exists, and to empty strings if neither is set.
    """
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
            logger.info(f"Loaded state from {STATE_FILE}")
            return {
                "project_root": env_root or saved.get("project_root", ""),
                "spring_boot_url": env_url or saved.get("spring_boot_url", ""),
            }
        except Exception as e:
            logger.warning(f"Could not read state file: {e} — using defaults")

    return {
        "project_root": env_root,
        "spring_boot_url": env_url,
    }


def save_state(state: dict) -> None:
    """Persist current state to disk."""
    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
        logger.debug(f"State saved to {STATE_FILE}")
    except Exception as e:
        logger.warning(f"Could not save state: {e}")


def clear_state() -> None:
    """Delete the persisted state file."""
    if os.path.exists(STATE_FILE):
        try:
            os.remove(STATE_FILE)
            logger.info("State file cleared")
        except Exception as e:
            logger.warning(f"Could not clear state file: {e}")