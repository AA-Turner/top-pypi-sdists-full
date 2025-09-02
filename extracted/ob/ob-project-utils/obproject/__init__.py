import os
import sys
from pathlib import Path

from .projectbase import ProjectFlow
from .project_events import ProjectEvent, project_trigger
from highlight_card import highlight

METAFLOW_PACKAGE_POLICY = "include"
INCLUDE_IN_PYTHONPATH = ["src"]


def _populate_pythonpath():
    REQUIRED = (".git", "obproject.toml")
    for path in Path(os.path.abspath(sys.argv[0])).parents:
        if all(os.path.exists(os.path.join(path, x)) for x in REQUIRED):
            for x in INCLUDE_IN_PYTHONPATH:
                sys.path.append(os.path.join(path, x))
            break
    else:
        if os.environ.get("OBPROJECT_DEBUG"):
            print(
                """
WARNING: It seems you are importing `obproject` outside 
of a project repository with obproject.toml. Automatic
importing of `src/` packages won't work. If you need those
packages, set PYTHONPATH manually.
"""
            )


_populate_pythonpath()
