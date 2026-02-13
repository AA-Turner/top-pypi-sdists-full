import json

from unittest import mock

import pytest

from snowflake.core import PollingOperation
from snowflake.core.exceptions import NotFoundError
from snowflake.core.iceberg_table._generated import TagAssignment, TagReference
from snowflake.core.tag import TagValue

from ...utils import BASE_URL, extra_params, mock_http_response


API_CLIENT_REQUEST = "snowflake.core._generated.api_client.ApiClient.request"


@pytest.fixture
def iceberg_tables(schema):
    return schema.iceberg_tables


@pytest.fixture
def iceberg_table(iceberg_tables):
    return iceberg_tables["my_table"]


def test_set_tags(fake_root, iceberg_table, tag, tags):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/iceberg-tables/my_table:set-tags",
    )
    tag_assignments = {tag: TagValue(value="value")}
    kwargs = extra_params(
        body=[
            TagAssignment(
                tag_value=v.value, tag_name=k.name, tag_schema=k.schema.name, tag_database=k.database.name
            ).to_dict()
            for k, v in tag_assignments.items()
        ]
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        iceberg_table.set_tags(tag_assignments)
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = iceberg_table.set_tags_async(tag_assignments)
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)

    # Check if `NotFoundError` will be propagated.
    missing_tag = tags["does_not_exist"]
    missing_kwargs = extra_params(
        body=[
            TagAssignment(
                tag_value="value",
                tag_name=missing_tag.name,
                tag_schema=missing_tag.schema.name,
                tag_database=missing_tag.database.name,
            ).to_dict()
        ]
    )

    with mock.patch(API_CLIENT_REQUEST, side_effect=NotFoundError("not found")) as mocked_request:
        with pytest.raises(NotFoundError):
            iceberg_table.set_tags({missing_tag: TagValue(value="value")})
    mocked_request.assert_called_once_with(*args, **missing_kwargs)


@pytest.mark.parametrize("if_exists", [True, False])
def test_set_tags_with_query_parameters(fake_root, iceberg_table, tag, if_exists):
    args = (
        fake_root,
        "POST",
        BASE_URL + f"/databases/my_db/schemas/my_schema/iceberg-tables/my_table:set-tags?ifExists={if_exists}",
    )
    tags = {tag: TagValue(value="value")}
    kwargs = extra_params(
        query_params=[("ifExists", if_exists)],
        body=[
            TagAssignment(
                tag_value=v.value, tag_name=k.name, tag_schema=k.schema.name, tag_database=k.database.name
            ).to_dict()
            for k, v in tags.items()
        ],
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        iceberg_table.set_tags(tags, if_exists=if_exists)
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = iceberg_table.set_tags_async(tags, if_exists=if_exists)
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_unset_tag(fake_root, iceberg_table, tag, tags):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/iceberg-tables/my_table:unset-tags",
    )
    tag_resources = {tag}
    kwargs = extra_params(
        body=[
            TagReference(
                tag_name=tag_res.name, tag_schema=tag_res.schema.name, tag_database=tag_res.database.name
            ).to_dict()
            for tag_res in tag_resources
        ]
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        iceberg_table.unset_tags(tag_resources)
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = iceberg_table.unset_tags_async(tag_resources)
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)

    # Check if `NotFoundError` will be propagated.
    missing_tag = tags["does_not_exist"]
    missing_kwargs = extra_params(
        body=[
            TagReference(
                tag_name=missing_tag.name,
                tag_schema=missing_tag.schema.name,
                tag_database=missing_tag.database.name,
            ).to_dict()
        ]
    )

    with mock.patch(API_CLIENT_REQUEST, side_effect=NotFoundError("not found")) as mocked_request:
        with pytest.raises(NotFoundError):
            iceberg_table.unset_tags({missing_tag})
    mocked_request.assert_called_once_with(*args, **missing_kwargs)


@pytest.mark.parametrize("if_exists", [True, False])
def test_unset_tags_with_query_parameters(fake_root, iceberg_table, tag, if_exists):
    args = (
        fake_root,
        "POST",
        BASE_URL + f"/databases/my_db/schemas/my_schema/iceberg-tables/my_table:unset-tags?ifExists={if_exists}",
    )
    tag_resources = {tag}
    kwargs = extra_params(
        query_params=[("ifExists", if_exists)],
        body=[
            TagReference(
                tag_name=tag_res.name, tag_schema=tag_res.schema.name, tag_database=tag_res.database.name
            ).to_dict()
            for tag_res in tag_resources
        ],
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        iceberg_table.unset_tags(tag_resources, if_exists=if_exists)
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = iceberg_table.unset_tags_async(tag_resources, if_exists=if_exists)
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_get_tags(fake_root, iceberg_table, tag):
    args = (
        fake_root,
        "GET",
        BASE_URL + "/databases/my_db/schemas/my_schema/iceberg-tables/my_table:get-tags",
    )
    kwargs = extra_params()
    fake_root.databases = tag.database.collection
    tag_assignment = TagAssignment(
        tag_value="value",
        tag_name=tag.name,
        tag_schema=tag.schema.name,
        tag_database=tag.database.name,
        level="TABLE",
    )
    response = mock_http_response(json.dumps([tag_assignment.to_dict()]))

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = response
        assert iceberg_table.get_tags() == {tag: TagValue("value", "TABLE")}
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = response
        op = iceberg_table.get_tags_async()
        assert isinstance(op, PollingOperation)
        assert op.result() == {tag: TagValue("value", "TABLE")}
    mocked_request.assert_called_once_with(*args, **kwargs)

    # Check if `NotFoundError` will be propagated.
    with mock.patch(API_CLIENT_REQUEST, side_effect=NotFoundError("not found")) as mocked_request:
        with pytest.raises(NotFoundError):
            iceberg_table.get_tags()
    mocked_request.assert_called_once_with(*args, **kwargs)


@pytest.mark.parametrize("with_lineage", [False, True])
def test_get_tags_with_lineage_query_params(fake_root, iceberg_table, with_lineage):
    args = (
        fake_root,
        "GET",
        BASE_URL
        + "/databases/my_db/schemas/my_schema/iceberg-tables/my_table:get-tags"
        + f"?withLineage={with_lineage}",
    )
    kwargs = extra_params(query_params=[("withLineage", with_lineage)])
    response = mock_http_response(json.dumps([]))

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = response
        iceberg_table.get_tags(with_lineage=with_lineage)
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = response
        op = iceberg_table.get_tags_async(with_lineage=with_lineage)
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)
