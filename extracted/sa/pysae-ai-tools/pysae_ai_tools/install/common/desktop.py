"""Desktop-integration helpers for GUI app installers (Linux ``.desktop`` files).

Shared by the Postman and Bruno installers to register a custom URL scheme
(``postman://`` / ``bruno://``) so an app's OAuth2 "Authorize using browser" flow
can hand the auth code back to the app.
"""

import shutil
import subprocess
from pathlib import Path


def register_url_scheme(apps_dir: Path, desktop_file: str, scheme: str) -> str:
    """Make ``<scheme>://`` open ``desktop_file`` via ``xdg-mime``.

    ``desktop_file`` is the basename (e.g. ``bruno.desktop``) of an entry already
    written under ``apps_dir``. Returns ``registered`` / ``failed`` / ``skipped``
    (no ``xdg-mime`` on this system). ``stdin`` is closed so a sudo-less xdg call
    never blocks on a prompt.
    """
    if shutil.which("xdg-mime") is None:
        return "skipped"
    handler = f"x-scheme-handler/{scheme}"
    for cmd in (["update-desktop-database", str(apps_dir)], ["xdg-mime", "default", desktop_file, handler]):
        try:
            subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                stdin=subprocess.DEVNULL,
                check=False,
            )
        except FileNotFoundError:
            continue
    q = subprocess.run(
        ["xdg-mime", "query", "default", handler],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    return "registered" if desktop_file in (q.stdout or "") else "failed"
