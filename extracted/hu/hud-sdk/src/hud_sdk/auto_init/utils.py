################################################################################
# Shared utilities for auto_init entrypoints.
# This file can be imported by both hud_entrypoint.py and __main__.py
# Do not import any modules from the hud_sdk package here.
################################################################################

import os
import sys


def log_to_user(msg: str) -> None:
    print(msg, file=sys.stderr)


def set_config_path(config_path: str) -> None:
    os.environ["HUD_CONFIG_PATH"] = config_path


def set_key(key: str) -> None:
    os.environ["HUD_KEY"] = key


def set_service(service: str) -> None:
    os.environ["HUD_SERVICE"] = service
