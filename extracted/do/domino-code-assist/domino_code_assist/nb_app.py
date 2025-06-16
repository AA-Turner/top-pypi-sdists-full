from typing import Any, Dict, cast

import nbformat
import reacton
import reacton.ipyvuetify as v
import solara as sol

from domino_code_assist import app, settings

cell_ast_list = []

nb: nbformat.NotebookNode = nbformat.read(".dca_deployed.ipynb", 4)
for cell_index, cell in enumerate(nb.cells):
    cell_index += 1  # used 1 based
    if cell.cell_type == "code":
        source = cell.source
        cell_path = f"{settings.settings.domino_notebook_deploy_filename} input cell {cell_index}"
        cell_ast_list.append(compile(source, cell_path, "exec"))


class ReferenceEqualityWrapper:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        if not isinstance(other, ReferenceEqualityWrapper):
            return False
        return self.value is other.value


@reacton.component
def NbApp(handle_error: bool = True):
    replacements, set_replacements_ = reacton.use_state(cast(Dict[str, Any], {}), eq=lambda a, b: a is b)
    page, set_page = reacton.use_state(sol.Div())

    def set_replacement(key, value):
        set_replacements_(lambda x: {**x, key: value})

    app._replacements.provide((replacements, set_replacement))

    def exec_nb():
        user_ns: Dict[str, Any] = {}
        try:
            for ast in cell_ast_list:
                exec(ast, user_ns)
            set_page(user_ns["Page"]())
        except Exception:
            if handle_error:
                import traceback

                tb = traceback.format_exc()
                set_page(
                    sol.Div(
                        children=[
                            v.Html(tag="pre", children=[str(tb)]),
                            sol.Button(children=["Restart"], class_="ma-2", on_click=lambda: set_replacements_({})),
                        ]
                    )
                )
            else:
                raise

    reacton.use_memo(exec_nb, [ReferenceEqualityWrapper(replacements)])
    return page


@reacton.component
def Page():
    return NbApp()
