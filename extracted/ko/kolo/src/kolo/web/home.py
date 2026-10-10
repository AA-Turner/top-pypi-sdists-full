from __future__ import annotations

import json
import os

from ..config import create_kolo_directory
from ..settings import get_webapp_settings
from ..version import __version__


def _script_json(value) -> str:
    # json.dumps doesn't escape "</script>", so a stored value could break out
    # of the inline <script> block. Unicode escapes are equivalent in JS.
    return (
        json.dumps(value)
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("&", "\\u0026")
    )


def web_home_html(running_in_user_django: bool):
    kolo_dir = create_kolo_directory()
    project_folder = kolo_dir.parent
    settings = get_webapp_settings()

    source_dir = os.path.dirname(__file__)
    with open(f"{source_dir}/templates/home.html") as f:
        html = f.read().format(
            settings=_script_json(settings),
            __version__=_script_json(__version__),
            project_folder=_script_json(str(project_folder)),
            running_in_user_django=_script_json(running_in_user_django),
        )
    return html
