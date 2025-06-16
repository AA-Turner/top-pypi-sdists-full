import os
from typing import Any, Callable, Dict, Tuple, cast

import pandas as pd
import reacton
import reacton.ipyvuetify as v
import solara as sol
from solara.components.file_drop import FileDrop

_replacements = reacton.create_context(cast(Tuple[Dict[str, Any], Callable[[str, Any], None]], ({}, lambda key, value: None)))


def get_replacement(name: str) -> Any:
    if not reacton.core.get_render_context(required=False):
        return None
    replacements, _ = reacton.get_context(_replacements)
    return replacements.get(name)


def use_set_replacement():
    _, set_ = reacton.get_context(_replacements)
    return set_


class ReactiveDf:
    def __init__(self, var_name: str, initial_df_fn: Callable[[], pd.DataFrame], label: str):
        self.var_name = var_name
        self.initial_df_fn = initial_df_fn
        self.label = label

        if get_replacement(var_name) is None:
            self.df = initial_df_fn()
        else:
            self.df = get_replacement(var_name)

    def get(self):
        return self.df


@reacton.component
def DropDataframe(var_name: str, label: str):
    progress, set_progress = reacton.use_state(0)
    set_replacement = use_set_replacement()

    def on_file(file):
        fn_name = file["name"].lower().split(".")[-1]
        new_df = getattr(pd, f"read_{fn_name}")(file["file_obj"])
        set_replacement(var_name, new_df)

    server_software = os.environ.get("SERVER_SOFTWARE", "")
    is_in_solara = server_software.startswith("solara")

    with sol.Div() as main:
        FileDrop(
            label=label if is_in_solara else label + " (Note: does not work in preview mode)",
            on_total_progress=set_progress,
            on_file=on_file,
        )
        v.ProgressLinear(value=progress)

    return main
