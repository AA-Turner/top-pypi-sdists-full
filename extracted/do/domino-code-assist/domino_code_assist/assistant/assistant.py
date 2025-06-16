import json
import os
import textwrap
import traceback
from pathlib import Path
from typing import Any, Callable, Dict, Optional, cast

import ipyvuetify as vy
import ipywidgets
import plotly
import reacton
import reacton.ipyvuetify as v
import solara as sol
import solara.lab
import traitlets
from pandas.core.frame import DataFrame
from solara.components.code_highlight_css import CodeHighlightCss

import domino_code_assist.actions_store as actions_store
import domino_code_assist.assistant.notebook
from domino_code_assist import (
    __version__,
    action,
    app,
    crossfilter_widgets,
    css,
    data,
    sample_project_md,
    util,
)
from domino_code_assist.assistant import drawer, handle_user_install, mixpanel, notebook
from domino_code_assist.code import Code
from domino_code_assist.layout import CardGridLayoutBuilder
from domino_code_assist.serialize import dumps, loads
from domino_code_assist.settings import settings
from domino_code_assist.util import get_vars
from domino_code_assist.viz.state import Viz

from ..action import ActionFilter, ActionUseNbLocals
from ..automl.drawer import AutoMlDrawer
from ..automl.store import MLTask
from ..crossfilter_widgets import WidgetState, _generate_map, to_json
from ..foundation_models.drawer import FoundationDrawer
from ..foundation_models.store import TuneConfig
from ..load_data.drawer import LoadDataDrawer
from ..snippets import snippets, snippets_ui
from ..snippets.snippet_drawer import SnippetDrawer
from ..tour.tour import TourWidget
from ..transform.transform_drawer import TransformDrawer
from ..viz import plot_builder
from ..viz.drawer import VisualizationDrawer

server_software = os.environ.get("SERVER_SOFTWARE", "")
if server_software.lower().startswith("solara"):
    import nbformat

    nb: nbformat.NotebookNode = nbformat.read(settings.domino_notebook_deploy_filename, 4)
    notebook.markdown_cells = {cell["id"]: cell["source"] for cell in nb.cells if cell["cell_type"] == "markdown"}


class AssistantWidget(vy.VuetifyTemplate):
    template_file = (__file__, "assistant.vue")

    menu = traitlets.Any().tag(sync=True, **ipywidgets.widget_serialization)
    cell_id = traitlets.Any().tag(sync=True)
    code = traitlets.Dict(allow_none=True).tag(sync=True)
    code_up = traitlets.Dict(allow_none=True).tag(sync=True)
    notebook_path = traitlets.Unicode(allow_none=True).tag(sync=True)
    save_counter = traitlets.Int(0).tag(sync=True)
    markdown_cells = traitlets.Dict(allow_none=True).tag(sync=True)
    snippet_prefix = traitlets.Unicode(snippets.EDIT_SNIPPET_PREFIX).tag(sync=True)
    snippet_saved_snackbar = traitlets.Bool(False).tag(sync=True)
    snippet_saved_count = traitlets.Int(0).tag(sync=True)
    snippet_edit_mode = traitlets.Bool(False).tag(sync=True)
    snippet_add_dialog_open = traitlets.Bool(False).tag(sync=True)
    snippet_add_header = traitlets.Unicode(allow_none=True).tag(sync=True)
    in_user_install_mode = traitlets.Bool(handle_user_install.in_user_install_mode()).tag(sync=True)
    version = traitlets.Unicode(__version__).tag(sync=True)
    tour = traitlets.Any().tag(sync=True, **ipywidgets.widget_serialization)
    sample_project = traitlets.List().tag(sync=True)

    def __init__(self, *args, **kwargs):
        self._on_saved: Optional[Callable[[bool], None]] = None
        super().__init__(*args, **kwargs)
        notebook.save_notebook = self.save_notebook

    def save_notebook(self, on_saved: Callable[[bool], None]):
        self._on_saved = on_saved
        self.send({"method": "save_notebook", "args": []})
        self.save_counter += 1

    def vue_notebook_saved(self, result):
        self._on_saved and self._on_saved(result)
        self._on_saved = None

    def vue_save_snippet(self, code):
        snippets.save_snippet(code)
        self.snippet_saved_count += 1

    def vue_insert_sample_project(self, _):
        load_data = action.ActionDemo(df_var_out="df_palmer_penguins", df_name="palmerpenguins")
        transform = [
            ActionUseNbLocals(df_var_out="df_palmer_penguins", var_name="df_palmer_penguins"),
            ActionFilter(df_var_out="df_penguins_clean", col="bill_length_mm", dtype="float64", op="!=", value="nan", is_string=False),
            ActionFilter(df_var_out="df_penguins_clean", col="sex", dtype="object", op="!=", value="nan", is_string=False),
        ]
        plot_1 = Viz(
            name="Untitled",
            plot_type="scatter",
            id="910a55b1-de6e-4a22-8387-18e6e92c87c1",
            col_args={"x": "bill_length_mm", "y": "bill_depth_mm", "color": "species", "facet_col": "sex"},
            df_var_name="df_penguins_clean",
            plot_var_name="plot_1",
            crossfilter_enabled=True,
        )
        plot_2 = Viz(
            name="Untitled",
            plot_type="histogram",
            id="c3a304dc-8071-4641-a138-33c903870f26",
            col_args={"x": "island", "y": "bill_length_mm", "histfunc": "avg", "color": None},
            df_var_name="df_penguins_clean",
            plot_var_name="plot_2",
            crossfilter_enabled=True,
        )
        widget_year = WidgetState(
            df_var="df_penguins_clean", widget="Select", column="year", configurable=True, invert=False, mode=">", multiple=True, out_var="widget_year"
        )
        layout = [
            {"i": "plot_1", "w": 12, "h": 15, "x": 0, "y": 9},
            {"i": "df_penguins_clean", "w": 3, "h": 9, "x": 0, "y": 27},
            {"i": "plot_2", "w": 9, "h": 12, "x": 3, "y": 24},
            {"i": "widget_year", "w": 3, "h": 3, "x": 0, "y": 24},
            {"i": "4293a57d", "w": 12, "h": 4, "x": 0, "y": 0},
            {"i": "ec27252e", "w": 6, "h": 5, "x": 0, "y": 4},
            {"i": "f7cd73bb", "w": 6, "h": 5, "x": 6, "y": 4},
        ]

        self.sample_project = [
            {"code": sample_project_md.md1, "type_": "markdown", "id": "4293a57d"},
            {"code": sample_project_md.md2, "type_": "markdown"},
            {"code": load_data.render_code("") + f"\n{load_data.df_var_out}", "meta": dumps(load_data)},
            {"code": sample_project_md.md3, "type_": "markdown"},
            {"code": action.render_code(action.render_code_chunks(transform)), "meta": dumps(actions_store.ActionsState(actions=transform))},
            {"code": sample_project_md.md4, "type_": "markdown"},
            {"code": plot_builder.generate_code(plot_1), "meta": dumps(plot_1)},
            {"code": sample_project_md.md5, "type_": "markdown"},
            {"code": plot_builder.generate_code(plot_2), "meta": dumps(plot_2)},
            {"code": sample_project_md.md6, "type_": "markdown"},
            {"code": _generate_map[widget_year.widget or "mypy"](widget_year), "meta": json.dumps(to_json(widget_year))},
            {"code": sample_project_md.md7, "type_": "markdown"},
            {"code": sample_project_md.md8, "type_": "markdown", "id": "ec27252e"},
            {"code": sample_project_md.md9, "type_": "markdown", "id": "f7cd73bb"},
            {"code": sample_project_md.md10, "type_": "markdown"},
            make_app_code_cell(
                layout,
                {
                    "4293a57d": sample_project_md.md1,
                    "ec27252e": sample_project_md.md8,
                    "f7cd73bb": sample_project_md.md9,
                },
            ),
        ]


class MenuWidget(vy.VuetifyTemplate):
    template_file = (__file__, "menu.vue")

    logo = traitlets.Unicode(util.logo).tag(sync=True)
    items = traitlets.List(default_value=[]).tag(sync=True)
    selected = traitlets.Dict(allow_none=True).tag(sync=True)
    snippet_edit_mode = traitlets.Bool(False).tag(sync=True)
    overlay_open = traitlets.Bool().tag(sync=True)
    disabled = traitlets.Bool(True).tag(sync=True)
    overwrite = traitlets.Bool(False).tag(sync=True)


items = [
    {
        "title": "Load data",
        "icon": "mdi-cloud-upload-outline",
        "action": "load_data",
    },
    {
        "title": "Foundation Models",
        "icon": "mdi-vector-triangle",
        "action": "foundation_models",
    },
    {
        "title": "Transformations",
        "icon": "mdi-function-variant",
        "action": "transformations",
    },
    {
        "title": "AutoML",
        "icon": "mdi-head-cog-outline",
        "action": "automl",
    },
    {
        "title": "Visualizations",
        "icon": "mdi-chart-bar-stacked",
        "action": "visualizations",
    },
    {
        "title": "Crossfilter widgets",
        "icon": "mdi-filter",
        "action": "x-widgets",
    },
    {
        "title": "App",
        "icon": "mdi-apps",
        "action": "app",
    },
    {
        "title": "Enter text",
        "icon": "mdi-text",
        "action": "markdown",
    },
    {
        "title": "Insert snippet",
        "icon": "mdi-card-text-outline",
        "action": "snippets",
    },
]


@reacton.component
def Menu(selected, on_selected, decoded, snippet_edit_mode, on_snippet_edit_mode, disabled, overwrite):
    menu_action = None
    if decoded and decoded.__class__ in [action.ActionOpen, action.ActionDownloadDataSource, action.ActionDemo]:
        menu_action = "load_data"
    elif decoded and type(decoded) is MLTask:
        menu_action = "automl"
    elif decoded and type(decoded) is TuneConfig:
        menu_action = "foundation_models"
    elif decoded and isinstance(decoded, actions_store.ActionsState):
        menu_action = "transformations"
    elif decoded and type(decoded) is Viz:
        menu_action = "visualizations"
    elif decoded and isinstance(decoded, crossfilter_widgets.WidgetState):
        menu_action = "x-widgets"
    elif decoded and "type_card_grid_layout" in decoded:
        menu_action = "app"
    elif decoded and "markdown" in decoded:
        menu_action = "markdown"

    overlay_open, set_overlay_open = reacton.use_state(False)

    def close_overlay():
        set_overlay_open(False)

    # note: use_effect is used here over use_memo, so the overlay is closed last
    reacton.use_effect(close_overlay, [selected])

    return MenuWidget.element(
        items=[{"icon": "mdi-pencil", "title": "Edit", "action": menu_action, "edit": True}, *items] if decoded else items,
        selected=selected,
        on_selected=lambda v: v and on_selected(v),
        snippet_edit_mode=snippet_edit_mode,
        on_snippet_edit_mode=on_snippet_edit_mode,
        overlay_open=overlay_open,
        on_overlay_open=set_overlay_open,
        disabled=disabled,
        overwrite=overwrite,
    )


@reacton.component
def MarkdownPanel(edit_action, set_code, open, edit, on_close, overwrite_warning=None):
    def on_apply():
        mixpanel.api.track_with_defaults(
            "inserted code",
            {
                "section": "Enter markdown",
            },
        )
        set_code(
            {
                "code": markdown_text,
                "meta": {},
                "type_": "markdown",
            }
        )
        on_close()

    markdown_text, set_markdown_text = reacton.use_state("")

    def update_markdown():
        if open and edit and edit_action and "markdown" in edit_action:
            set_markdown_text(edit_action["markdown"])
        else:
            set_markdown_text("")

    reacton.use_memo(update_markdown, [edit_action, edit])

    with drawer.RightDrawer(
        open=open,
        on_open=lambda v: on_close() if not v else None,
        title="Markdown",
        edit=bool(edit),
        on_apply=on_apply,
        warning_widget=overwrite_warning,
    ) as main:
        with sol.Div(class_="markdown-drawer", style_="min-width: 800px; max-width: 800px"):
            if open:
                sol.MarkdownEditor(markdown_text, on_value=set_markdown_text)
    return main


class Symbol:
    def __init__(self, name: str):
        self._name = name

    def __repr__(self):
        return self._name


def make_app_code_cell(layout, markdown_cells=None):
    def filter_keys(d: Dict):
        return {k: v for k, v in d.items() if k in ["w", "h", "x", "y"]}

    def layout_item(item: Dict):
        obj: Any = Symbol(item["i"])
        if markdown_cells and item["i"] in markdown_cells:
            obj = Symbol(f'dca.MarkdownFromCell({item["i"]!r})')
        return {"item": obj, **filter_keys(item)}

    layout_with_items = [layout_item(item) for item in layout]
    layout_lines = (",\n" + (" " * 24)).join(str(k) for k in layout_with_items)
    code = textwrap.dedent(
        f"""\
                from domino_code_assist.deploy import Deployer
                import solara


                @solara.component
                def Page():
                    return dca.CardGridLayout([
                        {layout_lines}
                    ])

                Deployer(Page)"""
    )
    return {"code": code, "meta": json.dumps({"type_card_grid_layout": layout})}


@reacton.component
def AppPanel(edit_data, set_code, open, edit, on_close, markdown_cells: Optional[Dict] = None, overwrite_warning=None):
    layout, on_layout = sol.use_state_or_update(open and edit and edit_data and edit_data["type_card_grid_layout"] or [])

    plot_vars = get_vars(lambda v: isinstance(v, plotly.graph_objs._figure.Figure) or isinstance(v, reacton.core.Element))
    dfs = get_vars(lambda v: isinstance(v, (DataFrame, app.ReactiveDf)))

    df_quick_start_created, set_df_quick_start_created = reacton.use_state(False)
    plot_quick_start_created, set_plot_quick_start_created = reacton.use_state(False)

    if not plot_vars and open and "df_quick_start" not in (dfs or []):
        set_df_quick_start_created(True)
        util.nb_locals["df_quick_start"] = data.palmerpenguins()
        dfs = ["df_quick_start"] + (dfs or [])

    if not plot_vars and open and "plot_quick_start" not in plot_vars:
        set_plot_quick_start_created(True)
        import plotly.express as px

        util.nb_locals["plot_quick_start"] = px.scatter(util.nb_locals["df_quick_start"], x="bill_depth_mm", y="bill_length_mm", color="species")
        util.nb_locals["plot_quick_start"].update_layout(margin=dict(l=0, r=0, t=0, b=0))
        plot_vars = ["plot_quick_start"] + plot_vars

    def make_code():
        should_remove_df_quick_start = True
        should_remove_plot_quick_start = True

        qs_used = [True for item in layout if item["i"] == "df_quick_start"]
        if qs_used and df_quick_start_created:
            new_action = action.ActionDemo(df_var_out="df_quick_start", df_name="palmerpenguins")
            set_code({"code": new_action.render_code("df") + f"\n{new_action.df_var_out}", "meta": dumps(new_action), "modifier": "insert-above"})
            should_remove_df_quick_start = False

        qs_plot_used = [True for item in layout if item["i"] == "plot_quick_start"]
        if qs_plot_used and plot_quick_start_created:
            viz = Viz(
                plot_type="scatter",
                col_args={"x": "bill_depth_mm", "y": "bill_length_mm", "color": "species"},
                df_var_name="df_quick_start",
                plot_var_name="plot_quick_start",
                crossfilter_enabled=False,
            )
            set_code({"code": plot_builder.generate_code(viz), "meta": dumps(viz), "modifier": "insert-above"})
            should_remove_plot_quick_start = False

        set_code(make_app_code_cell(layout, markdown_cells))
        mixpanel.api.track_with_defaults("inserted code", {"section": "app"})
        on_close_(should_remove_df_quick_start, should_remove_plot_quick_start)

    def on_close_(should_remove_df_quick_start=True, should_remove_plot_quick_start=True):
        on_close()
        on_layout([])
        if df_quick_start_created and should_remove_df_quick_start:
            util.nb_locals.pop("df_quick_start", None)
        if plot_quick_start_created and should_remove_plot_quick_start:
            util.nb_locals.pop("plot_quick_start", None)

    def on_toggle(on):
        mixpanel.api.track_with_defaults(
            "interaction",
            {
                "section": "app",
                "type": "toggle variable",
                "state": bool(on),
            },
        )

    with drawer.RightDrawer(
        open=open,
        on_open=lambda v: on_close_() if not v else None,
        title="App",
        edit=bool(edit),
        on_apply=make_code,
        width="100%",
        warning_widget=overwrite_warning,
    ) as main:
        if open:
            CardGridLayoutBuilder(obj_vars=plot_vars + (dfs or []), layout=layout, on_layout=on_layout, markdown_cells=markdown_cells, on_toggle=on_toggle).key(
                "grid-layout"
            )

    return main


@reacton.component
def ExceptionGuard(children):
    busy, set_busy = reacton.use_state(False)
    exception, clear_exception = sol.use_exception()
    terminated, set_terminated = reacton.use_state(False)

    def reset():
        set_busy(True)
        clear_exception()
        set_busy(False)

    def terminate():
        set_terminated(True)
        clear_exception()

    if exception:
        with v.Dialog(v_model=bool(exception), on_v_model=lambda v: reset() if not v else None) as dialog:
            with v.Card():
                with v.CardTitle(class_="headline"):
                    v.Html(tag="h3", children=["Unexpected error"])
                with v.CardText():
                    if exception is None or exception.__traceback__ is None:
                        trace = ""
                    else:
                        trace = "".join(reversed(traceback.format_exception(None, exception, exception.__traceback__)[1:]))
                    v.Html(tag="pre", children=[trace], style_="max-height: 300px; overflow: auto;")
                with v.CardActions():
                    sol.Button("Close", color="primary", loading=busy, text=True, on_click=reset)
                    sol.Button("Terminate Code Assistant", color="primary", loading=busy, text=True, on_click=terminate)
        return dialog
    else:
        if terminated:
            sol.Error("Code Assistant terminated. Please restart the notebook. Consider reporting this bug.")
        else:
            return children


@reacton.component
def OverWriteWarning(code, type_):
    with sol.Div(class_="pa-4") as main:
        v.Html(tag="h4", children=[f"Warning: the {'text' if type_ == 'markdown' else 'code'} below will be overwritten."])
        if type_ == "markdown":
            with v.Sheet(elevation=2, class_="pa-2"):
                sol.Markdown(code)
        else:
            CodeHighlightCss()
            Code(
                code_chunks=[code],
                on_event=lambda a: None,
                error=None,
            )
    return main


@reacton.component
def Assistant():
    if settings.domino_code_assist_exception_guard:
        return ExceptionGuard(children=AssistantMain())
    else:
        return AssistantMain()


@reacton.component
def AssistantMain():
    code, set_code = reacton.use_state(cast(Optional[Dict], None))
    code_up, set_code_up = reacton.use_state(cast(Optional[Dict], None))
    selected, set_selected = reacton.use_state(cast(Optional[Dict], None))

    notebook_path, set_notebook_path = reacton.use_state(cast(Optional[str], None))

    def sync_notebook_browser_path():
        if notebook_path:
            domino_code_assist.assistant.notebook.notebook_browser_path.value = notebook_path

    solara.use_memo(sync_notebook_browser_path, dependencies=[notebook_path])

    edit_data, set_edit_data = reacton.use_state(cast(Optional[Dict["str", Any]], None))
    markdown_cells, set_markdown_cells = reacton.use_state(cast(Optional[Dict], None))

    snippet_saved_count, set_snippet_saved_count = reacton.use_state(0)
    snippet_edit_mode, set_snippet_edit_mode = reacton.use_state(False)

    snippet_add_header, set_snippet_add_header = reacton.use_state(cast(Optional[str], None))
    add_dialog_open, set_add_dialog_open = reacton.use_state(False)

    def handle_code_up():
        if code_up and code_up.get("type_") == "markdown":
            set_edit_data({"markdown": code_up["code"]})
        elif code_up and code_up.get("meta"):
            set_edit_data(loads(code_up.get("meta")))
        else:
            set_edit_data(None)

    reacton.use_memo(handle_code_up, [code_up])

    dfs = get_vars(lambda v: isinstance(v, DataFrame))

    def update_markdown():
        notebook.markdown_cells = markdown_cells

    reacton.use_memo(update_markdown, [markdown_cells])

    def on_selected():
        if selected and selected.get("action"):
            mixpanel.api.track_with_defaults(
                "open",
                {
                    "section": selected.get("action"),
                    "edit": bool(selected.get("edit")),
                },
            )

    reacton.use_memo(on_selected, [selected])
    writable_paths = reacton.use_memo(snippets.get_writable_paths, [])

    overwrite = bool(code_up is not None and code_up["code"].strip())

    overwrite_warning = sol.use_memo(
        lambda: OverWriteWarning(code_up["code"], code_up.get("type_")) if code_up and selected and not selected.get("edit") and overwrite else None
    )

    with v.Sheet() as main:
        css.Css()

        if mixpanel.mixpanel_widget:
            sol.Div(children=[mixpanel.mixpanel_widget])
        AssistantWidget.element(
            menu=Menu(
                selected=selected,
                on_selected=set_selected,
                decoded=edit_data,
                snippet_edit_mode=snippet_edit_mode,
                on_snippet_edit_mode=set_snippet_edit_mode,
                disabled=bool(code_up is None or "dca.init()" in code_up["code"]),
                overwrite=overwrite,
            ),
            code=code,
            on_code=set_code,
            on_notebook_path=set_notebook_path,
            on_code_up=set_code_up,
            markdown_cells=markdown_cells,
            on_markdown_cells=set_markdown_cells,
            on_snippet_saved_count=set_snippet_saved_count,
            snippet_edit_mode=snippet_edit_mode,
            snippet_add_header=snippet_add_header,
            snippet_add_dialog_open=add_dialog_open,
            on_snippet_add_dialog_open=set_add_dialog_open,
            tour=TourWidget.element(),
        )

        MarkdownPanel(
            edit_data,
            set_code,
            open=(selected and selected.get("action")) == "markdown",
            edit=selected and selected.get("edit"),
            on_close=lambda: set_selected(None),
            overwrite_warning=overwrite_warning,
        )

        LoadDataDrawer(
            edit_data,
            set_code,
            open=(selected and selected.get("action")) == "load_data",
            edit=selected and selected.get("edit"),
            on_close=lambda: set_selected(None),
            overwrite_warning=overwrite_warning,
        ).meta(ref="load_data")

        AutoMlDrawer(
            edit_data,
            set_code,
            dfs,
            is_open=(selected and selected.get("action")) == "automl",
            edit=selected and selected.get("edit"),
            on_close=lambda: set_selected(None),
            on_load_own_data=lambda: set_selected({"title": "Load data", "icon": "mdi-cloud-upload-outline", "action": "load_data"}),
            overwrite_warning=overwrite_warning,
        ).key("automl-drawer")

        FoundationDrawer(
            edit_data,
            set_code,
            dfs,
            is_open=(selected and selected.get("action")) == "foundation_models",
            edit=selected and selected.get("edit"),
            on_close=lambda: set_selected(None),
            on_load_own_data=lambda: set_selected({"title": "Load data", "icon": "mdi-cloud-upload-outline", "action": "load_data"}),
            overwrite_warning=overwrite_warning,
        ).key("foundation-drawer")

        TransformDrawer(
            edit_data,
            set_code,
            dfs,
            open=(selected and selected.get("action")) == "transformations",
            edit=selected and selected.get("edit"),
            on_close=lambda: set_selected(None),
            on_load_own_data=lambda: set_selected({"title": "Load data", "icon": "mdi-cloud-upload-outline", "action": "load_data"}),
            overwrite_warning=overwrite_warning,
        ).key(f'trans-edit-{selected and selected.get("edit")}').meta(ref="transformations")

        VisualizationDrawer(
            cast(Viz, edit_data),
            set_code,
            dfs,
            open=(selected and selected.get("action")) == "visualizations",
            edit=(selected and selected.get("edit")),
            on_close=lambda: set_selected(None),
            on_load_own_data=lambda: set_selected({"title": "Load data", "icon": "mdi-cloud-upload-outline", "action": "load_data"}),
            overwrite_warning=overwrite_warning,
        ).key(f'viz-edit-{selected and selected.get("edit")}').meta(ref="viz")

        crossfilter_widgets.CrossFilterWidgetsPanel(
            cast(Optional[crossfilter_widgets.WidgetState], edit_data),
            set_code,
            dfs,
            open=(selected and selected.get("action")) == "x-widgets",
            edit=selected and selected.get("edit"),
            on_close=lambda: set_selected(None),
            overwrite_warning=overwrite_warning,
        ).key(f'crossfilter-edit-{selected and selected.get("edit")}')

        AppPanel(
            edit_data,
            set_code,
            open=(selected and selected.get("action")) == "app",
            edit=selected and selected.get("edit"),
            on_close=lambda: set_selected(None),
            markdown_cells=markdown_cells,
            overwrite_warning=overwrite_warning,
        )

        SnippetDrawer(
            set_code,
            open=(selected and selected.get("action")) == "snippets",
            on_close=lambda: set_selected(None),
            save_count=snippet_saved_count,
            edit_mode=snippet_edit_mode,
            on_edit_mode=set_snippet_edit_mode,
            writable_paths=writable_paths,
            overwrite_warning=overwrite_warning,
        )

        def on_add_snippet(base_path, path, name):
            set_snippet_add_header(
                f"{snippets.EDIT_SNIPPET_PREFIX} {Path(base_path) / 'snippets' / Path(*[p['id'] for p in path[1:] if not p['leaf']] + [name + '.py'])}\n"
            )
            set_add_dialog_open(False)

        if writable_paths:
            snippets_ui.AddDialog(writable_paths, add_dialog_open, set_add_dialog_open, on_add_snippet)

        def close():
            set_selected(None)

    return main
