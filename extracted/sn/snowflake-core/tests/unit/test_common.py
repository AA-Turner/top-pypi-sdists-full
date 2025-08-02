#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#
import importlib

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from snowflake.core._common import CreateMode, SchemaObjectCollectionParent, SchemaObjectReferenceMixin
from snowflake.core.database import DatabaseCollection
from snowflake.core.schema import SchemaResource


PROJECT_SRC = Path(__file__).parent.parent.parent / "src" / "snowflake" / "core"
DEPRECATED_METHODS = ["delete", "undelete", "create_or_update", "download_file", "upload_file"]
IGNORED_METHODS = DEPRECATED_METHODS + ["get", "put"]  # StageResource.get, StageResource.put


class XyzCollection(SchemaObjectCollectionParent["XyzReference"]):
    def __init__(self, schema: "SchemaResource") -> None:
        super().__init__(schema, XyzResource)


class XyzResource(SchemaObjectReferenceMixin):
    def __init__(self, name: str, collection: "XyzCollection") -> None:
        self.collection = collection
        self.name = name


class ArgsCollection(SchemaObjectCollectionParent["ArgsResource"]):
    def __init__(self, schema: "SchemaResource") -> None:
        super().__init__(schema, ArgsResource)


class ArgsResource(SchemaObjectReferenceMixin):
    def __init__(self, name_with_args: str, collection: "ArgsCollection") -> None:
        self.collection = collection
        self.name_with_args = name_with_args


def test_collection_and_references():
    mock_session = MagicMock()
    db_collection = DatabaseCollection(mock_session)
    my_db_ref = db_collection["my_db"]
    assert my_db_ref.name == "my_db"
    assert my_db_ref.schemas.database.collection is db_collection

    schema_collection = my_db_ref.schemas
    my_schema_ref = schema_collection["my_schema"]
    assert my_schema_ref.name == "my_schema"
    assert my_schema_ref.database.name == "my_db"
    assert my_schema_ref.collection is schema_collection
    assert my_schema_ref.collection.database is my_db_ref is my_schema_ref.database
    assert my_schema_ref.qualified_name == "my_db.my_schema"

    xyz_collection = XyzCollection(my_schema_ref)
    my_xyz_ref = xyz_collection["my_xyz"]

    assert my_xyz_ref.name == "my_xyz"
    assert my_xyz_ref.schema.name == "my_schema"
    assert my_xyz_ref.database.name == "my_db"
    assert my_xyz_ref.schema is my_schema_ref
    assert my_xyz_ref.database is my_db_ref
    assert my_xyz_ref.collection is xyz_collection
    assert my_xyz_ref.fully_qualified_name == "my_db.my_schema.my_xyz"

    for key in xyz_collection:
        assert key == "my_xyz"

    for key in xyz_collection.keys():
        assert key == "my_xyz"

    for item in xyz_collection.items():
        assert item[0] == "my_xyz"
        assert item[1] is my_xyz_ref

    for value in xyz_collection.values():
        assert value is my_xyz_ref


def test_repr():
    db_collection = DatabaseCollection(MagicMock())
    my_db_ref = db_collection["my_db"]
    assert repr(db_collection) == "<DatabaseCollection>"
    assert repr(my_db_ref) == "<DatabaseResource: 'my_db'>"

    schema_collection = my_db_ref.schemas
    my_schema_ref = schema_collection['"my_schema"']
    assert repr(schema_collection) == "<SchemaCollection: 'my_db'>"
    assert repr(my_schema_ref) == """<SchemaResource: 'my_db."my_schema"'>"""

    xyz_collection = XyzCollection(my_schema_ref)
    my_xyz_ref = xyz_collection["my_xyz"]
    assert repr(xyz_collection) == """<XyzCollection: 'my_db."my_schema"'>"""
    assert repr(my_xyz_ref) == """<XyzResource: 'my_db."my_schema".my_xyz'>"""

    args_collection = ArgsCollection(my_schema_ref)
    my_args_ref = args_collection["my_args(float)"]
    assert repr(args_collection) == """<ArgsCollection: 'my_db."my_schema"'>"""
    assert repr(my_args_ref) == """<ArgsResource: 'my_db."my_schema".my_args(float)'>"""


def test_createmode():
    assert CreateMode["orREPlace"] is CreateMode.or_replace
    assert CreateMode["orREPlace"] == CreateMode.or_replace.value
    assert CreateMode["ifNOTExists"] is CreateMode.if_not_exists
    assert CreateMode["ErroRifexists"] is CreateMode.error_if_exists


def _generate_all_resources():
    for module in Path(PROJECT_SRC).iterdir():
        if module.name.startswith("_") or module.is_file():
            continue
        if module.name in [
            "cortex",  # Needs getting into underlying package
            "cortex_analyst",
            "session",  # Session is not resource
        ]:
            continue

        import_path = ".".join(module.parts[-3:])
        resource_module = importlib.import_module(import_path)
        yield resource_module, module.name


def _generate_all_classes(suffix=""):
    for resource_module, module_name in _generate_all_resources():
        class_name = "".join(s.capitalize() for s in module_name.split("_")) + suffix
        if hasattr(resource_module, class_name):
            a_class = getattr(resource_module, class_name)
            yield a_class


@pytest.mark.parametrize("model_class", _generate_all_classes())
def test_all_resources_have_to_dict_method(model_class):
    assert hasattr(model_class, "to_dict"), f"{model_class.__name__} missing to_dict method"


@pytest.mark.parametrize("collection_class", _generate_all_classes(suffix="Collection"))
@pytest.mark.parametrize("method", ("create", "iter"))
def test_collection_defines_async_methods(collection_class, method):
    method_name = f"{method}_async"
    assert hasattr(collection_class, method_name), f"{collection_class.__name__} missing {method_name} method"


@pytest.mark.parametrize("resource_class", _generate_all_classes(suffix="Resource"))
def test_resource_defines_async_methods(resource_class):
    method_names = (
        f"{m}_async"
        for m in dir(resource_class)
        if callable(getattr(resource_class, m))
        and not m.startswith("_")
        and not m.endswith("async")
        and m not in IGNORED_METHODS
    )
    for method_name in method_names:
        assert hasattr(resource_class, method_name), f"{resource_class.__name__} missing {method_name} method"
