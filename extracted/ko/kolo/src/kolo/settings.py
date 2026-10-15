import json
from typing import Literal, TypedDict

from . import kv

WEBAPP_SETTINGS_KEY = "webapp_settings"


class WebappSettings(TypedDict):
    auto_delete_old_traces: bool
    default_text_editor: Literal["vscode", "pycharm"]


default_webapp_settings: WebappSettings = {
    "auto_delete_old_traces": True,
    "default_text_editor": "vscode",
}


def _is_valid_setting(key: str, value: object) -> bool:
    if key == "auto_delete_old_traces":
        return isinstance(value, bool)
    if key == "default_text_editor":
        return value in ("vscode", "pycharm")
    return False


def validate_webapp_settings(value: object) -> WebappSettings:
    if not isinstance(value, dict):
        raise ValueError("Settings must be a JSON object")
    for key, setting in value.items():
        if not _is_valid_setting(key, setting):
            # ascii() keeps the message safe for the standalone server, which
            # sends it as a Latin-1 HTTP reason phrase.
            raise ValueError(f"Invalid setting: {key!a}")
    return value  # type: ignore


def get_webapp_settings() -> WebappSettings:
    try:
        value = kv.get_value(WEBAPP_SETTINGS_KEY)
    except KeyError:
        return default_webapp_settings
    try:
        saved_settings = json.loads(value) if value else {}
    except ValueError:
        return default_webapp_settings
    if not isinstance(saved_settings, dict):
        return default_webapp_settings
    valid_settings = {
        key: setting
        for key, setting in saved_settings.items()
        if _is_valid_setting(key, setting)
    }
    return {**default_webapp_settings, **valid_settings}


def save_webapp_settings(settings: WebappSettings):
    kv.set(WEBAPP_SETTINGS_KEY, json.dumps(settings))
