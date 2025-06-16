"""Dominocode"""
print("Initializing Domino Code Assist, please wait...")  # noqa: T201
import os  # noqa: E402
import ipyvuetify as v  # noqa: E402
from IPython.display import display  # noqa: E402

# don't show progress bar when run as an app
if not os.environ.get("SERVER_SOFTWARE", "").lower().startswith("solara"):
    display(v.ProgressLinear(indeterminate=True, style_="width: 395px"))  # noqa: E402
__version__ = "1.4.2"

import os  # noqa: E402

# isort: skip_file

import domino_code_assist.logging_workaround  # noqa: E402

from . import data  # noqa: E402
from .assistant import init  # noqa: E402
from .components import MarkdownFromCell, CardGridLayout  # noqa: E402
from .util import mlflow_log_notebook  # noqa: E402
from .foundation_models import df_to_ds, df_to_ds_ner, img_df_to_ds  # noqa: E402

try:
    if not os.environ.get("DOMINO_PROJECT_ID"):
        from dotenv import load_dotenv

        load_dotenv()
except ImportError:
    pass


def _prefix():
    import sys
    from pathlib import Path

    prefix = sys.prefix
    here = Path(__file__).parent
    # for when in dev mode
    if (here.parent / "prefix").exists():
        prefix = str(here.parent)
    return prefix


def _jupyter_labextension_paths():
    return [
        {
            "src": f"{_prefix()}/prefix/share/jupyter/labextensions/domino-code-assist/",
            "dest": "domino-code-assist",
        }
    ]


def _jupyter_nbextension_paths():
    return [
        {
            "section": "notebook",
            "src": f"{_prefix()}/prefix/share/jupyter/nbextensions/domino-code-assist/",
            "dest": "domino-code-assist",
            "require": "domino-code-assist/extension",
        }
    ]


def _jupyter_server_extension_points():
    return [
        {
            "module": "myextension.app",
        }
    ]
