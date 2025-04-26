from unittest import mock

import pytest

from snowflake.core import PollingOperation, Root
from snowflake.core.notebook import Notebook

from ...utils import BASE_URL, extra_params, mock_http_response


API_CLIENT_REQUEST = "snowflake.core.notebook._generated.api_client.ApiClient.request"
NOTEBOOK = Notebook(name="my_notebook")


@pytest.fixture
def notebooks(schema):
    return schema.notebooks


@pytest.fixture
def notebook(notebooks):
    return notebooks["my_notebook"]


def test_create_notebook(fake_root, notebooks):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/notebooks?createMode=errorIfExists",
    )
    kwargs = extra_params(
        query_params=[("createMode", "errorIfExists")],
        body={"name": "my_notebook"},
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        notebooks.create(NOTEBOOK)
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = notebooks.create_async(NOTEBOOK)
        assert isinstance(op, PollingOperation)
        notebook_res = op.result()
        assert notebook_res.name == "my_notebook"
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_notebook(fake_root, notebooks):
    args = (
        fake_root,
        "GET",
        BASE_URL + "/databases/my_db/schemas/my_schema/notebooks",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        notebooks.iter()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = notebooks.iter_async()
        assert isinstance(op, PollingOperation)
        it = op.result()
        assert list(it) == []
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_fetch_notebook(fake_root, notebook):
    from snowflake.core.notebook._generated.models import Notebook as NotebookModel

    model = NotebookModel(name="my_notebook")
    args = (
        fake_root,
        "GET",
        BASE_URL + "/databases/my_db/schemas/my_schema/notebooks/my_notebook",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(model.to_json())
        notebook.fetch()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(model.to_json())
        op = notebook.fetch_async()
        assert isinstance(op, PollingOperation)
        tab = op.result()
        assert tab.to_dict() == NOTEBOOK.to_dict()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_drop_notebook(fake_root, notebook):
    args = (
        fake_root,
        "DELETE",
        BASE_URL + "/databases/my_db/schemas/my_schema/notebooks/my_notebook?ifExists=False",
    )
    kwargs = extra_params(query_params=[("ifExists", False)])

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        notebook.drop()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = notebook.drop_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_rename_notebook(fake_root, notebook, notebooks):
    def format_args(notebook_name: str) -> tuple[Root, str, str]:
        return (
            fake_root,
            "POST",
            BASE_URL + f"/databases/my_db/schemas/my_schema/notebooks/{notebook_name}:rename?" + \
                "targetDatabase=my_db&targetSchema=my_schema&targetName=new_notebook",
        )
    kwargs = extra_params(
        query_params=[
            ("targetDatabase", notebooks.database.name),
            ("targetSchema", notebooks.schema.name),
            ("targetName", "new_notebook"),
        ]
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        notebook.rename("new_notebook")
        assert notebook.name == "new_notebook"
    mocked_request.assert_called_once_with(*format_args("my_notebook"), **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        et_res = notebooks["another_table"]
        op = et_res.rename_async("new_notebook")
        assert isinstance(op, PollingOperation)
        op.result()
        assert et_res.name == "new_notebook"
    mocked_request.assert_called_once_with(*format_args("another_table"), **kwargs)


def test_execute_notebook(fake_root, notebook):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/notebooks/my_notebook:execute",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        notebook.execute()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = notebook.execute_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_commit_notebook(fake_root, notebook):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/notebooks/my_notebook:commit",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        notebook.commit()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = notebook.commit_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_add_live_version_notebook(fake_root, notebook):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/notebooks/my_notebook:add-live-version",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        notebook.add_live_version()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = notebook.add_live_version_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)
