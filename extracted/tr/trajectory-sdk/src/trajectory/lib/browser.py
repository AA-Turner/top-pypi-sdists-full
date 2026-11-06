from __future__ import annotations

import os
import subprocess
import sys


def open_default_browser(url: str) -> bool:
  try:
    if sys.platform == "win32":
      os.startfile(url)
      return True
    if sys.platform == "darwin":
      command = ["open", url]
    elif os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"):
      command = ["xdg-open", url]
    else:
      return False
    environment = os.environ.copy()
    environment.pop("BROWSER", None)
    result = subprocess.run(
      command,
      stdin=subprocess.DEVNULL,
      stdout=subprocess.DEVNULL,
      stderr=subprocess.DEVNULL,
      env=environment,
      timeout=5,
      check=False,
    )
    return result.returncode == 0
  except (OSError, subprocess.TimeoutExpired):
    return False
