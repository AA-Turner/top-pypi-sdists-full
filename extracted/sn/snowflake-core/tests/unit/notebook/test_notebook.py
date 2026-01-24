from unittest import mock

import pytest

from snowflake.core import PollingOperation, Root
from snowflake.core.notebook import Notebook, NotebookResource

from ...utils import BASE_URL, extra_params, mock_http_response


API_CLIENT_REQUEST = "snowflake.core._generated.api_client.ApiClient.request"
NOTEBOOK = Notebook(name="my_notebook")


@pytest.fixture
def notebooks(schema):
    return schema.notebooks


@pytest.fixture
def notebook(notebooks):
    return notebooks["my_notebook"]


def test_create_notebook(fake_root, notebooks):
    args = (fake_root, "POST", BASE_URL + "/databases/my_db/schemas/my_schema/notebooks?createMode=errorIfExists")
    kwargs = extra_params(query_params=[("createMode", "errorIfExists")], body={"name": "my_notebook"})

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        notebook_res = notebooks.create(NOTEBOOK)
        assert isinstance(notebook_res, NotebookResource)
        assert notebook_res.name == "my_notebook"
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = notebooks.create_async(NOTEBOOK)
        assert isinstance(op, PollingOperation)
        notebook_res = op.result()
        assert notebook_res.name == "my_notebook"
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_notebook(fake_root, notebooks):
    args = (fake_root, "GET", BASE_URL + "/databases/my_db/schemas/my_schema/notebooks")
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


def test_iter_notebook_with_parameters(fake_root, notebooks):
    """Test iter notebook with various filter parameters."""
    # The API uses showLimit instead of limit for the actual parameter name
    args = (
        fake_root,
        "GET",
        BASE_URL + "/databases/my_db/schemas/my_schema/notebooks?like=test"
        "%&startsWith=test&showLimit=100&fromName=start_name",
    )
    kwargs = extra_params(
        query_params=[
            ("like", "test%"),
            ("startsWith", "test"),
            ("showLimit", 100),
            ("fromName", "start_name"),
        ]
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        notebooks.iter(like="test%", starts_with="test", limit=100, from_name="start_name")
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_show_limit_deprecation_warning(fake_root, notebooks):
    """Test that show_limit parameter triggers deprecation warning."""
    args = (
        fake_root,
        "GET",
        BASE_URL + "/databases/my_db/schemas/my_schema/notebooks?showLimit=10",
    )
    kwargs = extra_params(query_params=[("showLimit", 10)])

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        with pytest.warns(DeprecationWarning, match="'show_limit' is deprecated, use 'limit' instead"):
            list(notebooks.iter(show_limit=10))
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        with pytest.warns(DeprecationWarning, match="'show_limit' is deprecated, use 'limit' instead"):
            notebooks.iter_async(show_limit=10).result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_limit_and_show_limit_conflict(notebooks):
    """Test that providing both limit and show_limit raises ValueError."""
    with pytest.raises(ValueError, match="Cannot specify both 'limit' and 'show_limit'"):
        list(notebooks.iter(limit=10, show_limit=5))

    with pytest.raises(ValueError, match="Cannot specify both 'limit' and 'show_limit'"):
        notebooks.iter_async(limit=10, show_limit=5).result()


def test_fetch_notebook(fake_root, notebook):
    from snowflake.core.notebook._generated.models import Notebook as NotebookModel

    model = NotebookModel(name="my_notebook")
    args = (fake_root, "GET", BASE_URL + "/databases/my_db/schemas/my_schema/notebooks/my_notebook")
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
    args = (fake_root, "DELETE", BASE_URL + "/databases/my_db/schemas/my_schema/notebooks/my_notebook")
    kwargs = extra_params(query_params=[])

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        notebook.drop()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = notebook.drop_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_drop_notebook_with_if_exists(fake_root, notebook):
    """Test drop notebook with if_exists parameter."""
    args = (
        fake_root,
        "DELETE",
        BASE_URL + "/databases/my_db/schemas/my_schema/notebooks/my_notebook?ifExists=True",
    )
    kwargs = extra_params(query_params=[("ifExists", True)])

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        notebook.drop(if_exists=True)
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = notebook.drop_async(if_exists=True)
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_rename_notebook(fake_root, notebook, notebooks):
    def format_args(notebook_name: str) -> tuple[Root, str, str]:
        return (
            fake_root,
            "POST",
            BASE_URL
            + f"/databases/my_db/schemas/my_schema/notebooks/{notebook_name}:rename?"
            + "targetName=new_notebook",
        )

    kwargs = extra_params(
        query_params=[
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

    assert notebooks["my_notebook"].name == "my_notebook"
    assert notebooks["new_notebook"].name == "new_notebook"


def test_rename_notebook_with_target_database_and_schema(fake_root, notebook):
    """Test rename notebook with explicit target database and schema."""
    args = (
        fake_root,
        "POST",
        BASE_URL
        + "/databases/my_db/schemas/my_schema/notebooks/my_notebook:rename?"
        + "targetDatabase=target_db&targetSchema=target_schema&targetName=new_notebook",
    )
    kwargs = extra_params(
        query_params=[
            ("targetDatabase", "target_db"),
            ("targetSchema", "target_schema"),
            ("targetName", "new_notebook"),
        ]
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        notebook.rename("new_notebook", target_database="target_db", target_schema="target_schema")
        assert notebook.name == "new_notebook"
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_rename_notebook_with_if_exists(fake_root, notebook):
    """Test rename notebook with if_exists parameter."""
    # The API puts ifExists first in the query string
    args = (
        fake_root,
        "POST",
        BASE_URL
        + "/databases/my_db/schemas/my_schema/notebooks/my_notebook:rename?"
        + "ifExists=True&targetName=new_notebook",
    )
    kwargs = extra_params(
        query_params=[
            ("ifExists", True),
            ("targetName", "new_notebook"),
        ]
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        notebook.rename("new_notebook", if_exists=True)
        assert notebook.name == "new_notebook"
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_execute_notebook(fake_root, notebook):
    args = (fake_root, "POST", BASE_URL + "/databases/my_db/schemas/my_schema/notebooks/my_notebook:execute")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        notebook.execute()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = notebook.execute_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_execute_notebook_with_async_exec(fake_root, notebook):
    """Test execute notebook with async_exec parameter."""
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/notebooks/my_notebook:execute?asyncExec=True",
    )
    kwargs = extra_params(query_params=[("asyncExec", True)])

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        notebook.execute(async_exec=True)
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = notebook.execute_async(async_exec=False)
        assert isinstance(op, PollingOperation)
        op.result()
    # Should have asyncExec=False in the URL
    expected_args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/notebooks/my_notebook:execute?asyncExec=False",
    )
    expected_kwargs = extra_params(query_params=[("asyncExec", False)])
    mocked_request.assert_called_once_with(*expected_args, **expected_kwargs)


def test_commit_notebook(fake_root, notebook):
    args = (fake_root, "POST", BASE_URL + "/databases/my_db/schemas/my_schema/notebooks/my_notebook:commit")
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
    args = (fake_root, "POST", BASE_URL + "/databases/my_db/schemas/my_schema/notebooks/my_notebook:add-live-version")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        notebook.add_live_version()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = notebook.add_live_version_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)
