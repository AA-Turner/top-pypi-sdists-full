"""Config management — persists token, instances, and session data."""

import json
import os

DEFAULT_CONFIG_DIR = os.path.expanduser("~/.config/pw-agent")
CONFIG_FILE = "config.json"


def _config_path(config_dir: str = "") -> str:
    d = config_dir or DEFAULT_CONFIG_DIR
    return os.path.join(d, CONFIG_FILE)


def load_config(config_dir: str = "") -> dict:
    """Load saved config, or return empty dict.

    Config structure:
    {
        "config_dir": "~/.config/pw-agent",
        "active": "cloud-slot2",          # key of the active instance
        "instances": {
            "cloud-slot2": {
                "mode": "cloud",
                "name": "jugnau P100",
                "token": "pw_...",
                "slot": 2,
                "device_id": "linux-abc",
                "device_name": "jugnau-vm",
                "model": "qwen3.5:4b"
            },
            "local-41789": {
                "mode": "brain",
                "name": "Local RTX 4090",
                "brain_url": "http://localhost:41789",
                "model": "qwen3.5:4b"
            }
        }
    }
    """
    path = _config_path(config_dir)
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r") as f:
            cfg = json.load(f)
        # Migrate old flat config to new instances format
        if "instances" not in cfg and ("mode" in cfg or "token" in cfg or "brain_url" in cfg):
            cfg = _migrate_flat_config(cfg)
            save_config(cfg, config_dir)
        return cfg
    except (json.JSONDecodeError, OSError):
        return {}


def _migrate_flat_config(old: dict) -> dict:
    """Convert old single-connection config to multi-instance format."""
    instance = {}
    for k in ["mode", "token", "slot", "device_id", "device_name", "model", "brain_url"]:
        if k in old:
            instance[k] = old[k]

    if instance.get("mode") == "brain":
        key = f"local-{instance.get('brain_url', 'unknown').split(':')[-1]}"
        instance["name"] = f"Local ({instance.get('model', 'ollama')})"
    else:
        key = f"cloud-slot{instance.get('slot', 0)}"
        instance["name"] = instance.get("device_name", "Cloud GPU")

    return {
        "config_dir": old.get("config_dir", DEFAULT_CONFIG_DIR),
        "active": key,
        "instances": {key: instance},
    }


def save_config(data: dict, config_dir: str = "") -> str:
    """Save config and return the file path."""
    d = config_dir or DEFAULT_CONFIG_DIR
    os.makedirs(d, exist_ok=True)
    path = os.path.join(d, CONFIG_FILE)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    return path


def has_config(config_dir: str = "") -> bool:
    """Check if a config file exists."""
    return os.path.exists(_config_path(config_dir))


def get_active_instance(cfg: dict) -> dict:
    """Get the currently active instance config, or empty dict."""
    instances = cfg.get("instances", {})
    active_key = cfg.get("active", "")
    return instances.get(active_key, {})


def add_instance(cfg: dict, key: str, instance: dict, set_active: bool = True) -> dict:
    """Add an instance to the config. Returns updated config."""
    if "instances" not in cfg:
        cfg["instances"] = {}
    cfg["instances"][key] = instance
    if set_active:
        cfg["active"] = key
    return cfg


def remove_instance(cfg: dict, key: str) -> dict:
    """Remove an instance. If it was active, clear active."""
    cfg.get("instances", {}).pop(key, None)
    if cfg.get("active") == key:
        remaining = list(cfg.get("instances", {}).keys())
        cfg["active"] = remaining[0] if remaining else ""
    return cfg


def instance_key_for_brain(brain_url: str) -> str:
    """Generate a unique key for a brain instance."""
    port = brain_url.split(":")[-1].rstrip("/")
    return f"local-{port}"


def instance_key_for_cloud(slot: int) -> str:
    """Generate a unique key for a cloud instance."""
    return f"cloud-slot{slot}"


# ─── Session persistence ─────────────────────────────────────────────────────

def _sessions_dir(config_dir: str = "") -> str:
    d = config_dir or DEFAULT_CONFIG_DIR
    return os.path.join(d, "sessions")


def _session_key(cwd: str, session_id: str = "") -> str:
    import hashlib
    if session_id:
        # Sanitize: keep alphanumeric + dash/underscore, truncate to 64 chars
        safe = "".join(c for c in session_id if c.isalnum() or c in "-_")[:64]
        return safe or hashlib.md5(cwd.encode()).hexdigest()[:10]
    return hashlib.md5(cwd.encode()).hexdigest()[:10]


def save_session(conversation: list[dict], cwd: str, config_dir: str = "", session_id: str = "") -> str:
    """Save conversation to a session file. Returns the path."""
    d = _sessions_dir(config_dir)
    os.makedirs(d, exist_ok=True)
    key = _session_key(cwd, session_id)
    path = os.path.join(d, f"{key}.json")
    data = {"cwd": cwd, "session_id": session_id, "conversation": conversation}
    with open(path, "w") as f:
        json.dump(data, f)
    return path


def load_session(cwd: str, config_dir: str = "", session_id: str = "") -> list[dict]:
    """Load the session for a given cwd/session_id, or return empty list."""
    d = _sessions_dir(config_dir)
    key = _session_key(cwd, session_id)
    path = os.path.join(d, f"{key}.json")
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r") as f:
            data = json.load(f)
        # When session_id is given, skip the cwd check — ID is the key
        if session_id or data.get("cwd") == cwd:
            return data.get("conversation", [])
    except (json.JSONDecodeError, OSError):
        pass
    return []


def clear_session(cwd: str, config_dir: str = "", session_id: str = ""):
    """Delete the session for a given cwd/session_id."""
    d = _sessions_dir(config_dir)
    key = _session_key(cwd, session_id)
    path = os.path.join(d, f"{key}.json")
    if os.path.exists(path):
        os.remove(path)
