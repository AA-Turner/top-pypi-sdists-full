from pathlib import Path
from typing import Callable, Dict, List, Optional, cast

import reacton
import reacton.ipyvuetify as v
import solara as sol
import traitlets
from ipyvuetify import VuetifyTemplate
from solara.components.code_highlight_css import CodeHighlightCss

from domino_code_assist import util
from domino_code_assist.code import Code
from domino_code_assist.settings import settings
from domino_code_assist.snippets.snippets import Snippet


class TreeWidget(VuetifyTemplate):
    template_file = (__file__, "tree.vue")

    path = traitlets.List(default_value=[]).tag(sync=True)
    items = traitlets.List().tag(sync=True)
    scroll_pos = traitlets.Int(allow_none=True).tag(sync=True)
    refresh_count = traitlets.Int(0).tag(sync=True)


@reacton.component
def TreeBrowser(
    path: List,
    items: List,
    on_path: Callable[[List], None] = None,
    scroll_pos: int = None,
    on_scroll_pos: Callable[[int], None] = None,
    on_refresh_count: Callable[[int], None] = None,
):
    return TreeWidget.element(path=path, items=items, on_path=on_path, scroll_pos=scroll_pos, on_scroll_pos=on_scroll_pos, on_refresh_count=on_refresh_count)


@reacton.component
def SnippetsPanel(
    get_items: Callable[[List], List],
    get_content: Callable[[List], Snippet],
    path,
    on_path,
    edit_mode,
    on_edit_mode,
    writable_paths,
    on_edit_snippet,
    on_delete_snippet,
    on_add_snippet,
    on_snippet: Callable[[Optional[Snippet]], None] = lambda s: None,
    on_refresh_count: Callable[[int], None] = None,
):
    items, set_items = reacton.use_state(cast(List[Dict], []))
    content, set_content = reacton.use_state(cast(Optional[Snippet], None))

    scroll_pos_stack, set_scroll_pos_stack = reacton.use_state([0])  # pre add 1 item for the root
    scroll_pos, set_scroll_pos = reacton.use_state(0)

    delete_dialog, set_delete_dialog = reacton.use_state(False)
    add_dialog, set_add_dialog = reacton.use_state(False)
    add_name, set_add_name = reacton.use_state(None)
    add_path, set_add_path = reacton.use_state(None)

    def on_path_change():
        if not path[-1]["leaf"]:
            set_content(None)
            set_items(get_items(path))

            if len(path) >= len(scroll_pos_stack):
                set_scroll_pos_stack(scroll_pos_stack + [scroll_pos])
                set_scroll_pos(0)
            else:
                set_scroll_pos(scroll_pos_stack[len(path)])
                set_scroll_pos_stack(scroll_pos_stack[: len(path)])
        else:
            set_items(get_items(path[:-1]))
            set_content(get_content(path))

    reacton.use_memo(on_path_change, [path, get_items])

    def on_content():
        on_snippet(content)

    reacton.use_memo(on_content, [content])

    def is_writable(path: Path):
        def starts_with(a: Path, b: Path):
            try:
                b.relative_to(a)
                return True
            except ValueError:
                return False

        return any(starts_with(Path(p), path) for p in [wp["path"] for wp in writable_paths if wp["writable"]])

    def delete_snippet():
        on_delete_snippet(content)
        set_delete_dialog(False)

    with sol.Div(style_="height: 100%; display: flex; flex-direction: column;") as main:
        with sol.Div(style_="display: flex; flex-grow: 1; min-height: 0"):
            with sol.Div(style_="height: 100%; width: 50%; max-width: 50%;"):
                TreeBrowser(path, items, on_path, scroll_pos, set_scroll_pos, on_refresh_count)
            with sol.Div(style_="width: 50%; max-width: 50%; overflow: auto"):
                if content:
                    v.Html(tag="h3", class_="pt-2", children=[content.name.replace(".py", "")])
                    v.Html(tag="p", children=[content.description])
                    CodeHighlightCss()
                    Code(
                        code_chunks=[content.code],
                        on_event=lambda a: None,
                        error=None,
                    )
                else:
                    v.Html(tag="h3", class_="ma-4", children=["Please select a snippet to preview."])
        with sol.Div(style_="display: flex").meta(ref="button-bar"):
            v.Tooltip(
                bottom=True,
                v_slots=[
                    {
                        "name": "activator",
                        "variable": "tooltip",
                        "children": sol.Button(
                            v_on="tooltip.on",
                            icon_name="mdi-pencil" if edit_mode else "mdi-pencil-off",
                            color="primary" if edit_mode else "",
                            on_click=lambda: on_edit_mode(not edit_mode),
                            icon=True,
                        ).meta(ref="toggle-edit"),
                    }
                ],
                children=["Snippet editing enabled. Click to disable." if edit_mode else "Snippet editing disabled. Click to enable."],
            )
            if edit_mode:
                v.Tooltip(
                    bottom=True,
                    v_slots=[
                        {
                            "name": "activator",
                            "variable": "tooltip",
                            "children": sol.Button(
                                "add",
                                v_on="tooltip.on",
                                icon_name="mdi-plus",
                                color="primary",
                                on_click=lambda: set_add_dialog(True),
                                class_="mx-2",
                            ).meta(ref="btn-add"),
                        }
                    ],
                    children=["Add a snippet to the current folder."],
                )
                if content:
                    sol.Button(
                        "edit",
                        color="primary",
                        disabled=not is_writable(content.base_path),
                        on_click=lambda: on_edit_snippet(content),
                        icon_name="mdi-pencil",
                        class_="mx-2",
                    ).meta(ref="btn-edit")
                    sol.Button(
                        "delete",
                        color="primary",
                        disabled=not is_writable(content.base_path),
                        on_click=lambda: set_delete_dialog(True),
                        icon_name="mdi-trash-can",
                        class_="mx-2",
                    ).meta(ref="btn-delete")

        with v.Dialog(width="400px", v_model=delete_dialog, on_v_model=lambda v: set_delete_dialog(v)).meta(ref="dialog-delete"):
            with v.Card():
                v.CardTitle(children=["Are you sure you want to delete this snippet?"])
                with v.CardActions():
                    sol.Button("Cancel", outlined=True, color="primary", on_click=lambda: set_delete_dialog(False))
                    sol.Button("Delete", color="primary", on_click=delete_snippet, class_="mx-2")
        AddDialog(writable_paths, add_dialog, set_add_dialog, on_add_snippet, path)

    return main


@reacton.component
def AddDialog(writable_paths, open, on_open, on_add_snippet, path=[{}]):
    add_name, set_add_name = reacton.use_state("")
    add_path, set_add_path = reacton.use_state("")
    with v.Dialog(width="600px", v_model=open, on_v_model=lambda v: on_open(v)).meta(ref="add-dialog") as main:
        with v.Card():
            v.CardTitle(children=["Add snippet"])
            with v.CardText():
                sol.Div(children=["Folder: " + "/".join([p["id"] for p in path[1:] if not p["leaf"]])])
                v.TextField(label="Name", v_model=add_name, on_v_model=set_add_name, autofocus=True)
                sol.Div(children=["Repository"])
                with v.List():
                    with v.ListItemGroup(v_model=add_path, on_v_model=set_add_path, color="primary"):
                        for item in writable_paths:
                            label = item
                            icon = ""
                            git_path = settings.domino_repos_dir or settings.domino_imported_code_dir
                            if str(item["path"]).startswith(settings.domino_working_dir):
                                label = "current project"
                            elif git_path and str(item["path"]).startswith(git_path):
                                icon = "mdi-git"
                                label = str(item["path"])[len(git_path) + 1 :]
                            with v.ListItem(value=str(item["path"]), disabled=not item["writable"]).key(str(item)):
                                with v.ListItemIcon():
                                    if icon:
                                        v.Icon(children=[icon])
                                    else:
                                        v.Img(
                                            src=util.logo_black,
                                            style_="height: 24px; max-width: 24px; border-radius: 12px",
                                        )
                                with v.ListItemContent():
                                    v.ListItemTitle(
                                        children=[
                                            str(label),
                                            sol.Tooltip(
                                                "Read only. The configured credentials don't have write access to this repository.",
                                                children=[sol.Text(" (read only)", style="pointer-events: all")],
                                            )
                                            if not item["writable"]
                                            else "",
                                        ]
                                    )
            with v.CardActions():
                sol.Button("Cancel", outlined=True, color="primary", on_click=lambda: on_open(False), icon_name="mdi-close")
                sol.Button(
                    "add",
                    color="primary",
                    on_click=lambda: on_add_snippet(add_path, path, add_name),
                    class_="mx-2",
                    disabled=not add_path or not add_name,
                    icon_name="mdi-plus",
                ).meta(ref="btn-add")
    return main
