import os
import re
from contextlib import contextmanager
from keyword import iskeyword
from typing import Any, Callable, Dict, List, Optional

import nbformat as nbf
import reacton
import reacton.ipyvuetify as v
import solara.util as sutil
from IPython import get_ipython
from solara.lab import Ref

from .settings import settings


def get_nb_locals():
    def get_frame():
        try:
            assert False
        except Exception as e:
            return e.__traceback__.tb_frame if e.__traceback__ is not None else None

    def find_nb_locals(current):
        while current is not None:
            if current.f_locals.get("__doc__") == "Automatically created module for IPython interactive environment":
                return current.f_locals

            current = current.f_back

    return find_nb_locals(get_frame())


nb_locals = get_nb_locals()


def get_vars(filter: Callable[[Any], bool]):
    return [k for k, v in nb_locals.items() if not re.search(r"^_.*$", k) and k != "Page" and filter(v)]


def generate_var_name(prefix):
    count = 0
    while True:
        count += 1
        name = f"{prefix}_{count}"
        if [x for x in get_vars(lambda v: True) if x == name]:
            continue
        return name


logo = sutil.load_file_as_data_url(os.path.join(os.path.dirname(__file__), "DominoLogoWhite.svg"), "image/svg+xml")

logo_black = sutil.load_file_as_data_url(os.path.join(os.path.dirname(__file__), "DominoLogoBlack.svg"), "image/svg+xml")


@reacton.component
def DominoHeader(title, show_logo=True):
    main = v.CardTitle(
        class_="text-h5",
        style_="background-color: #2d71c7; color: white",
        children=[
            title,
            *(
                [
                    v.Spacer(),
                    v.Img(
                        src=logo,
                        style_="height: 32px; max-width: 32px; border-radius: 16px",
                    ),
                ]
                if show_logo
                else []
            ),
        ],
    )
    return main


def eq_by_ref(a, b):
    return a is b


def copy_upload(file_obj, name):
    import errno
    import shutil
    from datetime import datetime

    now = datetime.now()
    dt_string = now.strftime("%Y%m%d%H%M%S")
    data_dir = os.path.join(settings.domino_working_dir, "domino_code_assist_data")
    try:
        os.makedirs(data_dir)
    except OSError as e:
        if not e.errno == errno.EEXIST:
            raise
    dest_name = os.path.join(data_dir, dt_string + "_" + name)
    destination = open(dest_name, "wb")
    shutil.copyfileobj(file_obj, destination)

    return dest_name


def python_safe_name(name, used=None):
    if used is None:
        used = []
    first, rest = name[0], name[1:]
    name = re.sub("[^a-zA-Z_]", "_", first) + re.sub("[^a-zA-Z_0-9]", "_", rest)
    if name in used:
        nr = 1
        while name + ("_%d" % nr) in used:
            nr += 1
        name = name + ("_%d" % nr)
    return name


def in_dev_mode():
    return settings.domino_code_assist_dev


def supported_object_store_types():
    return ["S3Config", "GCSConfig", "ADLSConfig"]


def remove_keys(d: Dict, keys: List[str]):
    return {k: v for k, v in d.items() if k not in keys}


def is_valid_variable_name(name):
    return name.isidentifier() and not iskeyword(name)


def store_notebook(file_name: str):
    ipython = get_ipython()
    nb = nbf.v4.new_notebook()
    nb["cells"] = [nbf.v4.new_code_cell(code) for code in ipython.history_manager.input_hist_raw]
    nbf.write(nb, file_name)


def mlflow_log_notebook(run_name: str):
    file_name = f"{run_name}_run_log.ipynb"
    store_notebook(file_name)

    try:
        from mlflow import log_artifact

        log_artifact(file_name)
    finally:
        os.remove(file_name)


def to_float(s: Optional[str]):
    if s is None:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def to_int(s: Optional[str]):
    if s is None:
        return None
    try:
        return int(s)
    except ValueError:
        return None


def bind_v_model(field):
    ref = Ref(field)
    return {
        "v_model": ref.value,
        "on_v_model": ref.set,
    }


@contextmanager
def handle_errors():
    try:
        yield
    except RuntimeError as e:
        if str(e).startswith("CUDA out of memory."):
            raise Exception(
                "CUDA out of memory error was thrown. There are a few strategies that can be taken to help fix this."
                + " Please refer to: https://huggingface.co/docs/transformers/v4.18.0/performance."
                + " You must restart the kernel before trying again."
            )
        elif str(e).startswith("CUDA error: device-side assert triggered"):
            raise Exception(
                "CUDA device-side assert triggered. This is most likely due to invalid input data or an incorrect input of the loss function."
                + " You must restart the kernel before trying again."
            )
        else:
            raise e
