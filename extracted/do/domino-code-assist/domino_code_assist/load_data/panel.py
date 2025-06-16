# import reacton
import sys

import reacton.ipyvuetify as v
import solara
from solara.components.file_browser import FileBrowser
from solara.components.file_drop import FileDrop
from solara.lab.toestand import Ref

from ..assistant import mixpanel
from ..domino_api import get_domino_api
from .data_source import DataSourcePanel
from .quick_start import QuickStart
from .state import load_data

supported_extensions = [
    "csv",
    "excel",
    "feather",
    "fwf",
    "gbq",
    "hdf",
    "html",
    "json",
    "orc",
    "parquet",
    "pickle",
    "sas",
    "spss",
    "sql",
    "sql_query",
    "sql_table",
    "stata",
    "table",
    "xml",
    "nocode",
]


@solara.component
def LoadDataPanel():
    progress, set_progress = solara.use_state(0, key="progress")
    load_data.use()
    tab = Ref(load_data.fields.tab).get()

    def on_tab():
        tabs = ["'Data Sources'", "'Datasets'", "'Project Files'", "'Uploads'", "'Demo'"]
        mixpanel.api.track_with_defaults(
            "interaction",
            {
                "section": "load_data",
                "type": "select tab",
                "tab": tabs[tab],
            },
        )

    solara.use_memo(on_tab, [tab])

    with solara.Div(style_="max-width: 700px; max-width: 700px") as main:
        with v.Tabs(v_model=tab, on_v_model=Ref(load_data.fields.tab).set):
            v.Tab(children=["Data Sources"])
            v.Tab(children=["Datasets"])
            v.Tab(children=["Project Files"])
            v.Tab(children=["Upload"])
            v.Tab(children=["Quick-start"])
            with v.TabItem():
                version = get_domino_api().get_domino_version()
                if not (version.startswith("5") or version.startswith("0")):
                    solara.Div(children=["Data Sources are not available in Domino 4.x and earlier."], class_="ma-4")
                elif sys.version_info.minor == 6:
                    solara.Div(children=["Data Sources are not available in Python 3.6."], class_="ma-4")
                else:
                    DataSourcePanel(
                        columns=None,
                        visible=tab == 0,
                    ).meta(ref="datasource")
            with v.TabItem():
                dataset_dir = Ref(load_data.fields.dataset_dir).get()
                if dataset_dir.exists():
                    with solara.Div(style_="height: calc(100vh - 166px); padding-bottom: 0px; overflow: hidden; display: flex; flex-direction: column;"):
                        solara.Div(class_="my-4", children=[f"Select a file with one of the following extensions: {', '.join(supported_extensions)}"])
                        with solara.Div(style_="display: flex; flex-direction: column; flex-grow: 1; overflow: hidden;"):
                            with solara.Div(style_="flex-grow: 1; overflow: hidden;"):
                                FileBrowser(
                                    directory=dataset_dir,
                                    on_directory_change=load_data.on_dataset_dir_change,
                                    on_file_name=Ref(load_data.fields.dataset_file).set,
                                ).key("DatasetsFileBrowser").meta(ref="datasets")
                            v.Switch(label="reactive").connect(Ref(load_data.fields.reactive))
                else:
                    solara.Div(children=["This project has no datasets."], class_="ma-4")
            with v.TabItem():
                with solara.Div(
                    style_="height: calc(100vh - 166px); overflow: auto; padding-bottom: 0px; overflow: hidden; display: flex; flex-direction: column;"
                ):
                    solara.Div(class_="my-4", children=[f"Select a file with one of the following extensions: {', '.join(supported_extensions)}"])
                    with solara.Div(style_="display: flex; flex-direction: column; flex-grow: 1; overflow: hidden;"):
                        FileBrowser(
                            directory=load_data.value.project_dir,
                            on_directory_change=load_data.on_project_dir_change,
                            on_file_name=Ref(load_data.fields.project_file).set,
                        ).key("ProjectFileBrowser").meta(ref="project")
                        v.Switch(label="reactive").connect(Ref(load_data.fields.reactive))
            with v.TabItem():
                solara.Div(class_="my-4", children=[f"Drag a file with one of the following extensions: {', '.join(supported_extensions)}"])
                FileDrop(
                    label="Drop dataset here",
                    on_total_progress=set_progress,
                    on_file=Ref(load_data.fields.upload_file).set,
                ).meta(ref="upload")
                v.ProgressLinear(value=progress)
                v.Switch(label="reactive").connect(Ref(load_data.fields.reactive))
            with v.TabItem():
                QuickStart()
                v.Switch(label="reactive").connect(Ref(load_data.fields.reactive))

    return main
