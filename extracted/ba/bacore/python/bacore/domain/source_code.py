"""Source code entities."""

import inspect
from importlib import import_module
from pathlib import Path
from pydantic import BaseModel, computed_field, field_validator
from types import ModuleType
from typing import Callable, Optional


class FunctionModel(BaseModel):
    """Python function model."""

    func: Callable

    @computed_field
    @property
    def name(self) -> str:
        """Function name."""
        return self.func.__name__.replace("_", " ")

    @computed_field
    @property
    def doc(self) -> str | None:
        """Function docstring."""
        return inspect.getdoc(self.func)


class ClassModel(BaseModel):
    """Python class model."""

    klass: type

    @computed_field
    @property
    def name(self) -> str:
        """Name of class without underscores."""
        return self.klass.__name__.replace("_", " ")

    @computed_field
    @property
    def doc(self) -> str | None:
        return inspect.getdoc(self.klass)

    def functions(self) -> list[FunctionModel]:
        """Get functions as members from module and type as 'SrcFunc' class."""
        return [
            FunctionModel(func=member)
            for _, member in inspect.getmembers(self.klass)
            if (inspect.isfunction(member) or inspect.ismethod(member) or hasattr(member, "__wrapped__"))
            and member.__module__.startswith(self.klass.__module__)
        ]

    def classes(self) -> list["ClassModel"]:
        """Get classes as members from module and type as 'SrcClass' class.

        **Todo:** Recreate this function as recursive.
        """
        return [
            ClassModel(klass=member)
            for _, member in inspect.getmembers(self.klass)
            if inspect.isclass(member) and member.__module__.startswith(self.klass.__module__)
        ]


class ModuleModel(BaseModel):
    """Python source file."""

    path: Path
    package_root: Optional[str] = None

    def __lt__(self, other: "ModuleModel") -> bool:
        """Defining ordering by module name."""
        return self.path < other.path

    @field_validator("path")
    @classmethod
    def path_must_be_file(cls, v):
        if not v.is_file():
            ValueError(f"path must point to a file, not {v}")
        return v

    @computed_field
    @property
    def name(self) -> str:
        if self.path.name.startswith("__init__.py"):
            return self.path.parent.name
        else:
            return self.path.name[:-3].replace("_", " ")

    @computed_field
    @property
    def uri(self) -> str:
        """Returns the path to the module with dot notation as a string and removes '.py'"""
        src_file_without_suffix = self.path.with_suffix("")
        src_file_parts = src_file_without_suffix.parts
        if self.package_root is None:
            return ".".join(src_file_parts)
        else:
            src_root_index_start = src_file_parts.index(self.package_root)
            return ".".join(src_file_parts[src_root_index_start:])

    def _as_module(self) -> ModuleType:
        try:
            return import_module(self.uri)
        except ImportError:
            raise ImportError(f"Failed to import {self.uri}")

    @property
    def doc(self) -> str | None:
        return self._as_module().__doc__

    def functions(self) -> list[FunctionModel]:
        """Class members of source file."""
        return [
            FunctionModel(func=member)
            for _, member in inspect.getmembers(self._as_module())
            if (inspect.isfunction(member) or inspect.ismethod(member) or hasattr(member, "__wrapped__"))
            and member.__module__.startswith(self.uri)
        ]

    def classes(self) -> list[ClassModel]:
        """Get the members of a module which belong to the file."""
        return [
            ClassModel(klass=member)
            for _, member in inspect.getmembers(self._as_module())
            if inspect.isclass(member) and member.__module__.startswith(self.uri)
        ]


class DirectoryModel(BaseModel):
    """Source directory."""

    path: Path
    package_root: Optional[str] = None

    def __lt__(self, other: "DirectoryModel"):
        return self.path < other.path

    @computed_field
    @property
    def name(self) -> str:
        return self.path.name

    @computed_field
    @property
    def modules(self) -> list[ModuleModel]:
        module_list = [
            ModuleModel(path=dir_path, package_root=self.package_root)
            for dir_path in self.path.glob("*.py")
            if dir_path.is_file()
        ]
        return sorted(module_list)

    @computed_field
    @property
    def directories(self) -> list["DirectoryModel"]:
        directory_list = [
            DirectoryModel(path=dir_path, package_root=self.package_root)
            for dir_path in self.path.glob("*")
            if dir_path.is_dir() and not (dir_path.name.startswith("__") or dir_path.name.startswith(".mypy_cache"))
        ]
        return sorted(directory_list)
