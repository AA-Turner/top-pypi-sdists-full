from __future__ import annotations as _annotations

from collections import defaultdict
from os import PathLike
from pathlib import Path
from typing import Literal, List, Union

from pydantic import BaseModel, model_serializer

STATES = Literal["n/a", "n/i", "full"]


class BaseMatrix(BaseModel):
    id: str
    name: str

    def __repr__(self):
        return self.name


class Version(BaseMatrix, BaseModel):
    updated: str


class Category(BaseMatrix, BaseModel):
    versionId: str


class Task(BaseMatrix, BaseModel):
    versionId: str
    categoryId: str
    isNew: bool
    description: str


class Vendor(BaseMatrix, BaseModel):
    versionId: str
    isNew: bool


class Family(BaseMatrix, BaseModel):
    versionId: str
    vendorId: str
    isNew: bool


class Status(BaseModel):
    id: str
    familyId: str
    taskId: str
    versionId: str
    vendorId: str
    state: STATES


class Entry(BaseModel):
    category: Category
    task: Task
    vendor: Vendor
    family: Family
    status: Status

    @model_serializer
    def _dump(self):
        return dict(
            category=self.category.name,
            taskName=self.task.name,
            taskDescription=self.task.description,
            vendor=self.vendor.name,
            family=self.family.name,
            status=self.status.state,
        )


class SupportMatrix(BaseModel):
    version: Version
    matrix: list[Entry]

    @staticmethod
    def _compare(value, obj) -> bool:
        if value is None:
            return True
        elif isinstance(value, List):
            return obj.lower() in [_.lower() for _ in value]
        elif isinstance(value, (str, int)):
            return obj.lower() == str(value).lower()

    def _compare_obj(self, _id, name, obj) -> bool:
        checks = set()
        if _id:
            checks.add(self._compare(_id, obj.id))
        if name:
            checks.add(self._compare(name, obj.name))
        return False not in checks

    def filter(
        self,
        category_id: Union[str, list[str]] = None,
        category_name: Union[str, list[str]] = None,
        task_id: Union[str, list[str]] = None,
        task_name: Union[str, list[str]] = None,
        task_description: str = "",
        vendor_id: Union[str, list[str]] = None,
        vendor_name: Union[str, list[str]] = None,
        family_id: Union[str, list[str]] = None,
        family_name: Union[str, list[str]] = None,
        status: Union[STATES, list[STATES]] = None,
    ) -> SupportMatrix:
        tmp = []
        for entry in self.matrix:
            checks = {self._compare(status, entry.status.state)}
            checks.add(self._compare_obj(category_id, category_name, entry.category))
            checks.add(self._compare_obj(task_id, task_name, entry.task))
            checks.add(self._compare_obj(vendor_id, vendor_name, entry.vendor))
            checks.add(self._compare_obj(family_id, family_name, entry.family))
            if task_description:
                checks.add(task_description.lower() in entry.task.description.lower())
            if False not in checks:
                tmp.append(entry)
        return SupportMatrix(version=self.version, matrix=tmp)

    def to_df(self):
        try:
            import pandas as pd
        except ImportError:
            raise ImportError("Pandas not installed, please install using `pip install pandas`.")

        idx, cols = set(), set()
        data = {(entry.vendor.name, entry.family.name): defaultdict(dict) for entry in self.matrix}

        for entry in self.matrix:
            idx.add((entry.category.name, entry.task.name, entry.task.description))
            cols.add((entry.vendor.name, entry.family.name))
            data[(entry.vendor.name, entry.family.name)][
                (entry.category.name, entry.task.name, entry.task.description)
            ] = entry.status.state

        df = pd.DataFrame(
            data=data,
            columns=pd.MultiIndex.from_tuples(sorted(cols), names=["Vendor", "Family"]),
            index=pd.MultiIndex.from_tuples(sorted(idx), names=["category", "taskName", "taskDescription"]),
        )
        return df

    @staticmethod
    def _style_df(v):
        color = {
            "full": "color: green; border: 1px solid black",
            "n/i": "color: blue; border: 1px solid black",
            "n/a": "color: red; border: 1px solid black",
        }
        return [color[_] if isinstance(_, str) and _ in color else "color: #000000" for _ in v]

    def to_excel(self, filename: Union[str, PathLike]):
        filename = Path(filename).resolve().with_suffix(".xlsx").absolute()
        try:
            import openpyxl, jinja2  # noqa: E401,F401
        except ImportError:
            raise ImportError(
                "openpyxl and jinja2 not installed; please install using: "
                "`pip install openpyxl jinja2` or `pip install ipfabric[matrix]`."
            )
        self.to_df().style.apply(self._style_df, axis="columns").to_excel(filename, sheet_name=self.version.name)

    def to_csv(self, filename: Union[None, str, PathLike] = None):
        filename = Path(filename).resolve().with_suffix(".csv").absolute() if filename else None
        return self.to_df().to_csv(path_or_buf=filename)
