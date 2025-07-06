import json
import os

CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".intclt", "config.json")


def load_config() -> dict:
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_config(cfg: dict) -> None:
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)


def apply_env(cfg: dict) -> None:
    mapping = {
        "user_uuid": "USER_UUID",
        "organization_uuid": "ORG_UUID",
        "workspace_uuid": "WORKSPACE_UUID",
        "region": "REGION",
        "project_id": "PROJECT_ID",
        "secret_name": "SECRET_NAME",
        "intellithing_key": "INTELLITHING_KEY",
        "environment": "ENVIRONMENT",
}

    for key, env in mapping.items():
        if key in cfg and cfg[key] is not None:
            os.environ[env] = str(cfg[key])
