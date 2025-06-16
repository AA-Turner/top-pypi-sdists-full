import os
from pathlib import Path

import reacton
import reacton.ipyvuetify as v
import solara as sol

from domino_code_assist.assistant import drawer, mixpanel

from . import snippets, snippets_ui
from .snippets import EDIT_SNIPPET_PREFIX, Snippet


@reacton.component
def SnippetDrawer(set_code, open, on_close, save_count, edit_mode, on_edit_mode, writable_paths, overwrite_warning=None):
    root = {"label": "home", "id": 0, "leaf": False}
    path_, set_path = reacton.use_state([root])
    refresh_count, set_refresh_count = reacton.use_state(0)

    nr_of_snippets, get_items, get_content, adjust_path = reacton.use_memo(snippets.make_fns, [save_count, refresh_count])

    path = reacton.use_memo(lambda: adjust_path(path_), [adjust_path, path_])

    def on_apply():
        mixpanel.api.track_with_defaults(
            "inserted code",
            {
                "section": "Insert snippet",
            },
        )
        set_code(
            {
                "code": snippet_code,
                "meta": None,
            }
        )
        on_close()

    snippet_code, set_snippet_code = reacton.use_state("")

    def on_edit(content: Snippet):
        set_code(
            {
                "code": f"{EDIT_SNIPPET_PREFIX} {content.base_path / content.path / content.name}\n" + content.code,
            }
        )
        on_close()

    def on_delete(content: Snippet):
        os.remove(content.base_path / content.path / content.name)
        set_refresh_count(refresh_count + 1)

    def on_add_snippet(base_path, path, name):
        set_code(
            {
                "code": f"{EDIT_SNIPPET_PREFIX} {Path(base_path) / 'snippets' / Path(*[p['id'] for p in path[1:] if not p['leaf']] + [name + '.py'])}\n",
            }
        )
        on_close()

    with drawer.RightDrawer(
        open=open,
        on_open=lambda v: on_close() if not v else None,
        title="Snippets",
        edit=False,
        on_apply=on_apply,
        apply_disabled=not snippet_code,
        show_default_buttons=bool(nr_of_snippets),
        warning_widget=overwrite_warning,
    ) as main:
        with sol.Div(style_="min-width: 1200px; max-width: 1200px; height: 100%;"):
            if open:
                if nr_of_snippets:
                    snippets_ui.SnippetsPanel(
                        get_items,
                        get_content,
                        path,
                        set_path,
                        edit_mode,
                        on_edit_mode,
                        writable_paths,
                        on_edit,
                        on_delete,
                        on_add_snippet,
                        on_snippet=lambda snippet: set_snippet_code(snippet.code if snippet else ""),
                        on_refresh_count=set_refresh_count,
                    ).key("snippets")
                else:
                    with sol.Div(class_="text-center"):
                        v.Html(
                            tag="h3",
                            class_="ma-4",
                            children=["No snippets found. Snippets can be added by adding a shared project or shared dataset that has a snippets directory."],
                        )

    return main
