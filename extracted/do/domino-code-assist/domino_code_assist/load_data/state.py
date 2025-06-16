import dataclasses
from dataclasses import field
from pathlib import Path
from typing import Dict, Optional

import plotly
import solara
import solara.lab
from solara.lab import Ref

import domino_code_assist
from domino_code_assist.action import ActionDownloadDataSource

from .. import settings, util

options = [x for x in dir(plotly.data) if not x.startswith("_")] + [x for x in dir(domino_code_assist.data) if not x.startswith("_")]


@dataclasses.dataclass(frozen=True)
class LoadData:
    tab: int = 4
    data_source: ActionDownloadDataSource = ActionDownloadDataSource()
    dataset_dir: Path = field(default_factory=lambda: Path(settings.settings.domino_datasets_dir))
    dataset_file: Optional[str] = None
    project_dir: Path = field(default_factory=lambda: Path(settings.settings.domino_working_dir))
    project_file: Optional[str] = None
    upload_file: Optional[Dict] = None
    demo_df_name: str = "palmerpenguins"
    df_out: str = "df"
    reactive: bool = False

    def valid(self):
        if self.tab == 0:
            if self.data_source and self.data_source.type_ in util.supported_object_store_types() and self.data_source.database:
                return True
            elif self.data_source.type_ == "BigQueryConfig":
                return bool(self.data_source and (self.data_source.query if self.data_source.use_query else self.data_source.schema and self.data_source.table))
            else:
                return bool(
                    self.data_source and (self.data_source.query if self.data_source.use_query else self.data_source.database and self.data_source.table)
                )
        if self.tab == 1:
            return bool(self.dataset_file)
        if self.tab == 2:
            return bool(self.project_file)
        if self.tab == 3:
            return bool(self.upload_file)
        if self.tab == 4:
            return True


class ReactiveDataSource(solara.lab.Reactive[ActionDownloadDataSource]):
    def set_type(self, type_):
        self.update(type_=type_, region="default" if type_ == "BigQueryConfig" else None, use_query=False)

    def set_name(self, name):
        self.update(name=name, database=None, schema=None, table=None, project=None)

    def set_database(self, value):
        self.update(database=value, schema=None, table=None)

    def set_schema(self, value):
        self.update(schema=value, table=None)

    def set_sample(self, value):
        if value != self.get().sample:
            self.update(sample=value)

    def set_project(self, value):
        self.update(project=value, schema=None, table=None)

    def set_region(self, value):
        self.update(region=value, schema=None, table=None)


class ReactiveLoadData(solara.lab.Reactive[LoadData]):

    data_source: ReactiveDataSource

    def __post__init__(self):
        self.data_source = ReactiveDataSource(Ref(self.fields.data_source))

    def on_dataset_dir_change(self, path: Path):
        self.update(dataset_dir=path, dataset_file=None)

    def on_project_dir_change(self, path: Path):
        self.update(project_dir=path, project_file=None)

    def on_dataset_file_change(self, path: Path):
        self.update(dataset_file=path)


load_data = ReactiveLoadData(LoadData())
