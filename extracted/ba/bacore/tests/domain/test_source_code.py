"""Test cases for domain.source_code entities."""

import pytest
from bacore.domain.source_code import (
    ClassModel,
    DirectoryModel,
    FunctionModel,
    ModuleModel,
)
from pathlib import Path
from random import choice
from types import ModuleType
from typing import Callable


class TestDirectoryModel:
    src_dir = DirectoryModel(path=Path("python/bacore"), package_root="bacore")

    def test_path(self):
        assert self.src_dir.path == Path("python/bacore")

    def test_name(self):
        assert self.src_dir.name == "bacore", f"expected 'bacore' but got {self.src_dir.name}"

    def test_src_files(self):
        module = choice(self.src_dir.modules)
        assert isinstance(module, ModuleModel), f"should be of type ModuleModel, not {module}"

    def test_directories(self):
        directory = choice(self.src_dir.directories)
        assert isinstance(directory, DirectoryModel), f"should be of type DirectoryModel, not {directory}"


class TestModuleModel:
    init_module = ModuleModel(path=Path("python/bacore/__init__.py"), package_root="bacore")
    source_code_module = ModuleModel(path=Path("python/bacore/domain/source_code.py"), package_root="bacore")
    source_code_reader_module = ModuleModel(
        path=Path("python/bacore/interactors/source_code_reader.py"),
        package_root="bacore",
    )
    web_main_module = ModuleModel(path=Path("python/bacore/web/main.py"), package_root="bacore")

    def test_name(self):
        assert self.init_module.name == "bacore", self.source_code_module.name
        assert self.source_code_module.name == "source code", self.source_code_module.name
        assert self.source_code_reader_module.name == "source code reader", self.source_code_module.name
        assert self.web_main_module.name == "main", self.web_main_module.name

    def test_uri(self):
        assert self.init_module.uri == "bacore.__init__"
        assert self.source_code_module.uri == "bacore.domain.source_code"
        assert self.source_code_reader_module.uri == "bacore.interactors.source_code_reader"
        assert self.web_main_module.uri == "bacore.web.main"

    def test_as_module(self):
        assert isinstance(self.init_module._as_module(), ModuleType)
        assert isinstance(self.source_code_module._as_module(), ModuleType)
        assert isinstance(self.source_code_reader_module._as_module(), ModuleType)
        assert isinstance(self.web_main_module._as_module(), ModuleType)

    def test_doc(self):
        assert self.init_module.doc.splitlines()[0] == "# BACore main init module"
        assert self.source_code_module.doc.splitlines()[0] == "Source code entities."
        assert self.source_code_reader_module.doc.splitlines()[0] == "Source code reader module."
        assert self.web_main_module.doc.splitlines()[0] == "BACore documentation with FastHTML."

    def test_functions(self):
        assert len(self.init_module.functions()) == 0, self.init_module.functions()
        assert len(self.source_code_module.functions()) == 0, self.source_code_module.functions()

        source_code_reader_function = choice(self.source_code_reader_module.functions())
        assert isinstance(source_code_reader_function, FunctionModel)

        assert len(self.web_main_module.functions()) == 3, self.web_main_module.functions()

    def test_classes(self):
        assert len(self.init_module.classes()) == 0, self.init_module.classes()

        source_code_module_class = choice(self.source_code_module.classes())
        assert isinstance(source_code_module_class, ClassModel), self.source_code_module.classes()

        assert len(self.source_code_reader_module.classes()) == 1, self.source_code_reader_module.classes()


class TestSrcClass:
    source_code_model = ModuleModel(path=Path("python/bacore/domain/source_code.py"), package_root="bacore").classes()[
        0
    ]

    def test_name(self):
        assert self.source_code_model.name == "ClassModel"

    def test_doc(self):
        assert self.source_code_model.doc == "Python class model."

    def test_functions(self):
        assert len(self.source_code_model.functions()) != 0, self.source_code_model.functions()

    @pytest.mark.skip("Need to implement a recursive function for finding sub-classes.")
    def test_classes(self):
        assert len(self.source_code_model.classes()) != 0, self.source_code_model.classes()


class TestSrcFunc:
    function_model = ModuleModel(
        path=Path("python/bacore/interactors/file_handler.py"), package_root="bacore"
    ).functions()[0]

    def test_func(self):
        assert isinstance(self.function_model.func, Callable)

    def test_name(self):
        assert self.function_model.name == "delete files"

    def test_doc(self):
        assert self.function_model.doc.splitlines()[0] == "Delete files older than x days."
