import subprocess
import sys
from pathlib import Path
from typing import List, Optional

from abstra_internals.consts.filepaths import SMARTCHAT_PACKAGES_DIR_PATH
from abstra_internals.environment import SMARTCHAT_PACKAGES_FOLDER
from abstra_internals.settings import Settings


def get_smartchat_packages_dir() -> Path:
    if SMARTCHAT_PACKAGES_FOLDER:
        path = Path(SMARTCHAT_PACKAGES_FOLDER)
    else:
        # Local/dev fallback: the project's .abstra dir. It is gitignored (so it
        # never gets committed or deployed) and is where other per-project
        # runtime state already lives (e.g. SMARTCHAT_SNIPPETS_DIR_PATH).
        path = Settings.root_path / SMARTCHAT_PACKAGES_DIR_PATH
    path.mkdir(parents=True, exist_ok=True)
    return path


def add_smartchat_packages_to_path() -> bool:
    """Append the overlay to sys.path so a snippet can import packages installed
    into it. Returns True iff the overlay was added.

    No-ops on an empty overlay: there is nothing to import and nothing that
    could leak into a later stage run, so the executor stays clean and can be
    returned to the pool instead of recycled. A True return marks the executor
    tainted (it must not run a stage next).
    """
    overlay = get_smartchat_packages_dir()
    if not any(overlay.iterdir()):
        return False
    overlay_str = str(overlay)
    if overlay_str not in sys.path:
        sys.path.append(overlay_str)
    return True


def ensure_snippet_requirements(requirements: Optional[List[str]]) -> None:
    """Install the packages a snippet declared into the overlay.

    Uses ``pip install --target`` so nothing lands in the project's site
    packages or requirements.txt. pip skips packages already present in the
    target, so repeat snippets that reuse a library pay no reinstall cost.
    """
    if not requirements:
        return

    overlay = get_smartchat_packages_dir()
    cmd = [
        sys.executable,
        "-m",
        "pip",
        "install",
        "--target",
        str(overlay),
        *requirements,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(
            f"Failed to install Smart Chat snippet requirements {requirements}: {detail}"
        )
