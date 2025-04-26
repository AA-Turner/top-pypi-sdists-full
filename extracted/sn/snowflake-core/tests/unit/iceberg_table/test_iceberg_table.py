from itertools import combinations
from unittest import mock
from unittest.mock import MagicMock

import pytest

from snowflake.core import Clone, CreateMode
from snowflake.core.iceberg_table import IcebergTable, IcebergTableCollection, IcebergTableResource
from snowflake.core.iceberg_table._generated import (
    ConvertToManagedIcebergTableRequest,
    IcebergTableAsSelect,
    IcebergTableClone,
    IcebergTableFromAWSGlueCatalog,
    IcebergTableFromDelta,
    IcebergTableFromIcebergFiles,
    IcebergTableFromIcebergRest,
    IcebergTableLike,
    RefreshIcebergTableRequest,
)
from snowflake.core.schema import SchemaResource


@pytest.fixture
def _mock_collection():
    return MagicMock(database=MagicMock())


@pytest.fixture
def _mock_schema(_mock_collection):
    return SchemaResource("test_schema", _mock_collection)


@pytest.fixture
def _mock_iceberg_tables_collection(_mock_schema):
    return IcebergTableCollection(schema=_mock_schema)


@pytest.fixture
def _mock_api():
    with mock.patch("snowflake.core.iceberg_table._iceberg_table.IcebergTableApi") as mock_api:
        yield mock_api.return_value


def parametrize_if_exists():
    return pytest.mark.parametrize("if_exists", [True, False])


def parametrize_mode():
    return pytest.mark.parametrize("mode", [CreateMode.error_if_exists, CreateMode.if_not_exists])


def parametrize_copy_grants():
    return pytest.mark.parametrize("copy_grants", [True, False])

def parametrize_async():
    return pytest.mark.parametrize("is_async", [True, False])


class TestIcebergTableResource:

    @parametrize_async()
    def test_fetch_iceberg_table(self, _mock_collection, is_async):
        table = IcebergTableResource(name="my_table", collection=_mock_collection)
        if not is_async:
            table.fetch()
        else:
            table.fetch_async()
        _mock_collection._api.fetch_iceberg_table.assert_called_once_with(
            _mock_collection.schema.database.name,
            _mock_collection.schema.name,
            "my_table",
            async_req=is_async,
        )

    @parametrize_if_exists()
    @parametrize_async()
    def test_drop_iceberg_table(self, _mock_collection, if_exists, is_async):
        table = IcebergTableResource(name="my_table", collection=_mock_collection)
        if not is_async:
            table.drop(if_exists=if_exists)
        else:
            table.drop_async(if_exists=if_exists)
        _mock_collection._api.drop_iceberg_table.assert_called_once_with(
            _mock_collection.schema.database.name,
            _mock_collection.schema.name,
            "my_table",
            if_exists=if_exists,
            async_req=is_async,
        )

    @parametrize_if_exists()
    @parametrize_async()
    def test_convert_to_managed_iceberg_table(self, _mock_collection, if_exists, is_async):
        table = IcebergTableResource(name="my_table", collection=_mock_collection)
        convert_fn = table.convert_to_managed_async if is_async else table.convert_to_managed
        convert_fn(
            base_location="test_base_location",
            storage_serialization_policy="COMPATIBLE",
            if_exists=if_exists,
        )
        _mock_collection._api.convert_to_managed_iceberg_table.assert_called_once_with(
            _mock_collection.schema.database.name,
            _mock_collection.schema.name,
            "my_table",
            convert_to_managed_iceberg_table_request=ConvertToManagedIcebergTableRequest(
                base_location="test_base_location",
                storage_serialization_policy="COMPATIBLE",
            ),
            if_exists=if_exists,
            async_req=is_async,
        )

    @parametrize_if_exists()
    @parametrize_async()
    def test_refresh_iceberg_table(self, _mock_collection, if_exists, is_async):
        table = IcebergTableResource(name="my_table", collection=_mock_collection)
        refresh_fn = table.refresh_async if is_async else table.refresh
        refresh_fn(
            metadata_file_relative_path="test_metadata_file_relative_path",
            if_exists=if_exists,
        )
        _mock_collection._api.refresh_iceberg_table.assert_called_once_with(
            _mock_collection.schema.database.name,
            _mock_collection.schema.name,
            "my_table",
            refresh_iceberg_table_request=RefreshIcebergTableRequest(
                metadata_file_relative_path="test_metadata_file_relative_path",
            ),
            if_exists=if_exists,
            async_req=is_async,
        )

    @parametrize_if_exists()
    @parametrize_async()
    def test_resume_recluster_table(self, _mock_collection, if_exists, is_async):
        table = IcebergTableResource(name="my_table", collection=_mock_collection)
        if not is_async:
            table.resume_recluster(if_exists=if_exists)
        else:
            table.resume_recluster_async(if_exists=if_exists)
        _mock_collection._api.resume_recluster_iceberg_table.assert_called_once_with(
            _mock_collection.schema.database.name,
            _mock_collection.schema.name,
            "my_table",
            if_exists=if_exists,
            async_req=is_async,
        )

    @parametrize_if_exists()
    @parametrize_async()
    def test_suspend_recluster_table(self, _mock_collection, if_exists, is_async):
        table = IcebergTableResource(name="my_table", collection=_mock_collection)
        if not is_async:
            table.suspend_recluster(if_exists=if_exists)
        else:
            table.suspend_recluster_async(if_exists=if_exists)
        _mock_collection._api.suspend_recluster_iceberg_table.assert_called_once_with(
            _mock_collection.schema.database.name,
            _mock_collection.schema.name,
            "my_table",
            if_exists=if_exists,
            async_req=is_async,
        )

    @parametrize_async()
    def test_undrop_table(self, _mock_collection, is_async):
        table = IcebergTableResource(name="my_table", collection=_mock_collection)
        if not is_async:
            table.undrop()
        else:
            table.undrop_async()
        _mock_collection._api.undrop_iceberg_table.assert_called_once_with(
            _mock_collection.schema.database.name,
            _mock_collection.schema.name,
            "my_table",
            async_req=is_async,
        )


class TestIcebergTableCollection:

    @parametrize_async()
    def test_iter(self, _mock_api, _mock_schema, _mock_iceberg_tables_collection, is_async):
        iter_fn = _mock_iceberg_tables_collection.iter_async if is_async else _mock_iceberg_tables_collection.iter
        iter_fn(
            like="%my_table",
            starts_with="bar",
            show_limit=42,
            from_name="foo",
        )

        _mock_api.list_iceberg_tables.assert_called_once_with(
            database=_mock_iceberg_tables_collection.schema.database.name,
            var_schema=_mock_iceberg_tables_collection.schema.name,
            like="%my_table",
            starts_with="bar",
            show_limit=42,
            from_name="foo",
            async_req=is_async,
        )

    @pytest.mark.parametrize(
        "options",
        combinations(
            ["as_select",
             "like",
             "from_aws_glue_catalog",
             "from_delta",
             "from_iceberg_files",
             "from_iceberg_rest",
             "clone_iceberg_table"
             ],
            2
        )
    )
    def test_validate_iceberg_table(self, options, _mock_iceberg_tables_collection):
        kwargs = {o: True for o in options}
        with pytest.raises(ValueError) as err:
            _mock_iceberg_tables_collection.create(
                iceberg_table=IcebergTable(name="foo"),
                **kwargs
            )
        assert "are mutually exclusive" in str(err)

    @parametrize_mode()
    @parametrize_copy_grants()
    @parametrize_async()
    def test_create_iceberg_table_as_select(
        self, _mock_api, _mock_iceberg_tables_collection, mode, copy_grants, is_async
    ):
        iceberg_table = IcebergTable(
            name="fooObject",
            base_location="@stage/path",
        )

        create_fn = _mock_iceberg_tables_collection.create_async if is_async else _mock_iceberg_tables_collection.create
        create_fn(
            iceberg_table=iceberg_table,
            as_select="select * from bar",
            mode=mode,
            copy_grants=copy_grants,
        )

        _mock_api.create_snowflake_managed_iceberg_table_as_select.assert_called_once_with(
            database=_mock_iceberg_tables_collection.schema.database.name,
            var_schema=_mock_iceberg_tables_collection.schema.name,
            query="select * from bar",
            iceberg_table_as_select=IcebergTableAsSelect(**iceberg_table.to_dict()),
            create_mode=mode,
            copy_grants=copy_grants,
            async_req=is_async,
        )

    @parametrize_mode()
    @parametrize_copy_grants()
    @parametrize_async()
    def test_create_iceberg_table_like(self, _mock_api, _mock_iceberg_tables_collection, mode, copy_grants, is_async):
        iceberg_table = IcebergTable(name="fooObject")
        create_fn = _mock_iceberg_tables_collection.create_async if is_async else _mock_iceberg_tables_collection.create
        create_fn(
            iceberg_table=iceberg_table,
            like="barTable",
            mode=mode,
            copy_grants=copy_grants,
        )

        _mock_api.create_snowflake_managed_iceberg_table_like.assert_called_once_with(
            database=_mock_iceberg_tables_collection.schema.database.name,
            var_schema=_mock_iceberg_tables_collection.schema.name,
            name="barTable",
            iceberg_table_like=IcebergTableLike(**iceberg_table.to_dict()),
            create_mode=mode,
            copy_grants=copy_grants,
            target_database=_mock_iceberg_tables_collection.schema.database.name,
            target_schema=_mock_iceberg_tables_collection.schema.name,
            async_req=is_async,
        )

    @parametrize_mode()
    @parametrize_async()
    def test_create_iceberg_table_from_aws_glue_catalog(
        self, _mock_api, _mock_iceberg_tables_collection, mode, is_async
    ):
        iceberg_table = IcebergTable(
            name="fooObject",
            catalog_table_name="fooCatalogTable",
        )
        create_fn = _mock_iceberg_tables_collection.create_async if is_async else _mock_iceberg_tables_collection.create
        create_fn(
            iceberg_table=iceberg_table,
            from_aws_glue_catalog=True,
            mode=mode,
        )

        _mock_api.create_unmanaged_iceberg_table_from_aws_glue_catalog.assert_called_once_with(
            database=_mock_iceberg_tables_collection.schema.database.name,
            var_schema=_mock_iceberg_tables_collection.schema.name,
            iceberg_table_from_aws_glue_catalog=IcebergTableFromAWSGlueCatalog(**iceberg_table.to_dict()),
            create_mode=mode,
            async_req=is_async,
        )

    @parametrize_mode()
    @parametrize_async()
    def test_create_iceberg_table_from_delta(self, _mock_api, _mock_iceberg_tables_collection, mode, is_async):
        iceberg_table = IcebergTable(
            name="fooObject",
            base_location="@stage/path",
        )
        create_fn = _mock_iceberg_tables_collection.create_async if is_async else _mock_iceberg_tables_collection.create
        create_fn(
            iceberg_table=iceberg_table,
            from_delta=True,
            mode=mode,
        )

        _mock_api.create_unmanaged_iceberg_table_from_delta.assert_called_once_with(
            database=_mock_iceberg_tables_collection.schema.database.name,
            var_schema=_mock_iceberg_tables_collection.schema.name,
            iceberg_table_from_delta=IcebergTableFromDelta(**iceberg_table.to_dict()),
            create_mode=mode,
            async_req=is_async,
        )

    @parametrize_mode()
    @parametrize_async()
    def test_create_iceberg_table_from_iceberg_files(self, _mock_api, _mock_iceberg_tables_collection, mode, is_async):
        iceberg_table = IcebergTable(
            name="fooObject",
            metadata_file_path="@stage/path"
        )
        create_fn = _mock_iceberg_tables_collection.create_async if is_async else _mock_iceberg_tables_collection.create
        create_fn(
            iceberg_table=iceberg_table,
            from_iceberg_files=True,
            mode=mode,
        )

        _mock_api.create_unmanaged_iceberg_table_from_iceberg_files.assert_called_once_with(
            database=_mock_iceberg_tables_collection.schema.database.name,
            var_schema=_mock_iceberg_tables_collection.schema.name,
            iceberg_table_from_iceberg_files=IcebergTableFromIcebergFiles(**iceberg_table.to_dict()),
            create_mode=mode,
            async_req=is_async,
        )

    @parametrize_mode()
    @parametrize_async()
    def test_create_iceberg_table_from_iceberg_rest(self, _mock_api, _mock_iceberg_tables_collection, mode, is_async):
        iceberg_table = IcebergTable(
            name="fooObject",
            catalog_table_name="fooCatalogTable",
        )
        create_fn = _mock_iceberg_tables_collection.create_async if is_async else _mock_iceberg_tables_collection.create
        create_fn(
            iceberg_table=iceberg_table,
            from_iceberg_rest=True,
            mode=mode,
        )

        _mock_api.create_unmanaged_iceberg_table_from_iceberg_rest.assert_called_once_with(
            database=_mock_iceberg_tables_collection.schema.database.name,
            var_schema=_mock_iceberg_tables_collection.schema.name,
            iceberg_table_from_iceberg_rest=IcebergTableFromIcebergRest(**iceberg_table.to_dict()),
            create_mode=mode,
            async_req=is_async,
        )

    @parametrize_mode()
    @parametrize_copy_grants()
    @parametrize_async()
    def test_create_iceberg_table_clone_iceberg_table(
            self, _mock_api, _mock_iceberg_tables_collection, mode, copy_grants, is_async
    ):
        iceberg_table = IcebergTable(name="fooObject")
        create_fn = _mock_iceberg_tables_collection.create_async if is_async else _mock_iceberg_tables_collection.create
        create_fn(
            iceberg_table=iceberg_table,
            clone_iceberg_table=Clone(source="barTable"),
            mode=mode,
            copy_grants=copy_grants,
        )

        _mock_api.clone_snowflake_managed_iceberg_table.assert_called_once_with(
            _mock_iceberg_tables_collection.schema.database.name,
            _mock_iceberg_tables_collection.schema.name,
            "barTable",
            iceberg_table_clone=IcebergTableClone(
                point_of_time=None,
                name=iceberg_table.name,
            ),
            create_mode=mode,
            async_req=is_async,
            target_database=_mock_iceberg_tables_collection.schema.database.name,
            target_schema=_mock_iceberg_tables_collection.schema.name,
            copy_grants=copy_grants,
        )

    @parametrize_mode()
    @parametrize_copy_grants()
    @parametrize_async()
    def test_create_iceberg_table(self, _mock_api, _mock_iceberg_tables_collection, mode, copy_grants, is_async):
        iceberg_table = IcebergTable(name="fooObject")
        create_fn = _mock_iceberg_tables_collection.create_async if is_async else _mock_iceberg_tables_collection.create
        create_fn(
            iceberg_table=iceberg_table,
            mode=mode,
            copy_grants=copy_grants,
        )

        _mock_api.create_snowflake_managed_iceberg_table.assert_called_once_with(
            _mock_iceberg_tables_collection.schema.database.name,
            _mock_iceberg_tables_collection.schema.name,
            iceberg_table,
            create_mode=mode,
            async_req=is_async,
            copy_grants=copy_grants,
        )
