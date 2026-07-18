# -*- coding: utf-8 -*-
"""
File to house the   class.

Created on Fri Jul 17 18:28:42 2026

@author: Richard Kellnberger
"""

import os
import shutil
from typing import Any

from pylsp_mypy import log


def get_cmd(settings: dict[str, Any], cmd: str) -> list[str]:
    """
    Get the command to run from settings, falling back to searching the PATH.
    If the command is not found in the settings and is not available on the PATH, an
    empty list is returned.
    """
    command_key = f"{cmd}_command"
    command: list[str] = settings.get(command_key, [])

    if not (command and os.getenv("PYLSP_MYPY_ALLOW_DANGEROUS_CODE_EXECUTION")):
        # env var is required to allow command from settings
        if shutil.which(cmd):  # Fallback to PATH
            log.debug(
                f"'{command_key}' not found in settings or not allowed, using '{cmd}' from PATH"
            )
            command = [cmd]
        else:  # Fallback to API
            command = []

    log.debug(f"Using {cmd} command: {command}")

    return command
