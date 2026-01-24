from unittest import mock

import pytest

from snowflake.core import PollingOperation
from snowflake.core.artifact_repository import ArtifactRepository, ArtifactRepositoryResource

from ...utils import BASE_URL, extra_params, mock_http_response


API_CLIENT_REQUEST = "snowflake.core._generated.api_client.ApiClient.request"
ARTIFACT_REPOSITORY = ArtifactRepository(
    name="my_artifact_repository", type="PIP", api_integration="my_api_integration"
)

ARTIFACT_REPOSITORY_WITH_COMMENT = ArtifactRepository(
    name="my_artifact_repository_with_comment",
    type="PIP",
    api_integration="my_api_integration",
    comment="Test comment for artifact repository",
)


@pytest.fixture
def artifact_repositories(schema):
    return schema.artifact_repositories


@pytest.fixture
def artifact_repository(artifact_repositories):
    return artifact_repositories["my_artifact_repository"]


def test_create_artifact_repository(fake_root, artifact_repositories):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/artifact-repositories",
    )
    kwargs = extra_params(
        query_params=[],
        body={"name": "my_artifact_repository", "type": "PIP", "api_integration": "my_api_integration"},
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        artifact_repo_res = artifact_repositories.create(ARTIFACT_REPOSITORY)
        assert isinstance(artifact_repo_res, ArtifactRepositoryResource)
        assert artifact_repo_res.name == "my_artifact_repository"
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = artifact_repositories.create_async(ARTIFACT_REPOSITORY)
        assert isinstance(op, PollingOperation)
        artifact_repo_res = op.result()
        assert artifact_repo_res.name == "my_artifact_repository"
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_create_or_alter_artifact_repository(fake_root, artifact_repositories):
    args = (
        fake_root,
        "PUT",
        BASE_URL + "/databases/my_db/schemas/my_schema/artifact-repositories/my_artifact_repository",
    )
    kwargs = extra_params(
        body={"name": "my_artifact_repository", "type": "PIP", "api_integration": "my_api_integration"},
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        result = artifact_repositories["my_artifact_repository"].create_or_alter(ARTIFACT_REPOSITORY)
        assert result is None  # create_or_alter returns None
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = artifact_repositories["my_artifact_repository"].create_or_alter_async(ARTIFACT_REPOSITORY)
        assert isinstance(op, PollingOperation)
        result = op.result()
        assert result is None  # create_or_alter_async also returns None
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_artifact_repository(fake_root, artifact_repositories):
    args = (fake_root, "GET", BASE_URL + "/databases/my_db/schemas/my_schema/artifact-repositories")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        artifact_repositories.iter()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = artifact_repositories.iter_async()
        assert isinstance(op, PollingOperation)
        it = op.result()
        assert list(it) == []
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_show_limit_deprecation_warning(fake_root, artifact_repositories):
    """Test that show_limit parameter triggers deprecation warning."""
    args = (
        fake_root,
        "GET",
        BASE_URL + "/databases/my_db/schemas/my_schema/artifact-repositories?showLimit=10",
    )
    kwargs = extra_params(query_params=[("showLimit", 10)])

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        with pytest.warns(DeprecationWarning, match="'show_limit' is deprecated, use 'limit' instead"):
            list(artifact_repositories.iter(show_limit=10))
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        with pytest.warns(DeprecationWarning, match="'show_limit' is deprecated, use 'limit' instead"):
            artifact_repositories.iter_async(show_limit=10).result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_show_limit(fake_root, artifact_repositories):
    args = (
        fake_root,
        "GET",
        BASE_URL + "/databases/my_db/schemas/my_schema/artifact-repositories?showLimit=10",
    )
    kwargs = extra_params(query_params=[("showLimit", 10)])

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        list(artifact_repositories.iter(limit=10))
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        artifact_repositories.iter_async(limit=10).result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_limit_and_show_limit_conflict(artifact_repositories):
    """Test that providing both limit and show_limit raises ValueError."""
    with pytest.raises(ValueError, match="Cannot specify both 'limit' and 'show_limit'"):
        list(artifact_repositories.iter(limit=10, show_limit=5))

    with pytest.raises(ValueError, match="Cannot specify both 'limit' and 'show_limit'"):
        artifact_repositories.iter_async(limit=10, show_limit=5).result()


def test_iter_with_like_filter(fake_root, artifact_repositories):
    args = (
        fake_root,
        "GET",
        BASE_URL + "/databases/my_db/schemas/my_schema/artifact-repositories?like=test_repo",
    )
    kwargs = extra_params(query_params=[("like", "test_repo")])

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        list(artifact_repositories.iter(like="test_repo"))
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_with_starts_with_filter(fake_root, artifact_repositories):
    args = (
        fake_root,
        "GET",
        BASE_URL + "/databases/my_db/schemas/my_schema/artifact-repositories?startsWith=test",
    )
    kwargs = extra_params(query_params=[("startsWith", "test")])

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        list(artifact_repositories.iter(starts_with="test"))
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_with_from_name(fake_root, artifact_repositories):
    args = (
        fake_root,
        "GET",
        BASE_URL + "/databases/my_db/schemas/my_schema/artifact-repositories?fromName=start_repo",
    )
    kwargs = extra_params(query_params=[("fromName", "start_repo")])

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        list(artifact_repositories.iter(from_name="start_repo"))
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_fetch_artifact_repository(fake_root, artifact_repository):
    from snowflake.core.artifact_repository._generated.models import ArtifactRepository as ArtifactRepositoryModel

    model = ArtifactRepositoryModel(name="my_artifact_repository", type="PIP", api_integration="my_api_integration")
    args = (
        fake_root,
        "GET",
        BASE_URL + "/databases/my_db/schemas/my_schema/artifact-repositories/my_artifact_repository",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(model.to_json())
        artifact_repository.fetch()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(model.to_json())
        op = artifact_repository.fetch_async()
        assert isinstance(op, PollingOperation)
        fetched_repo = op.result()
        assert fetched_repo.to_dict() == ARTIFACT_REPOSITORY.to_dict()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_drop_artifact_repository(fake_root, artifact_repository):
    args = (
        fake_root,
        "DELETE",
        BASE_URL + "/databases/my_db/schemas/my_schema/artifact-repositories/my_artifact_repository",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        artifact_repository.drop()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = artifact_repository.drop_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_drop_artifact_repository_if_exists(fake_root, artifact_repository):
    args = (
        fake_root,
        "DELETE",
        BASE_URL + "/databases/my_db/schemas/my_schema/artifact-repositories/my_artifact_repository?ifExists=True",
    )
    kwargs = extra_params(query_params=[("ifExists", True)])

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        artifact_repository.drop(if_exists=True)
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_rename_artifact_repository(fake_root, artifact_repository):
    args = (
        fake_root,
        "POST",
        BASE_URL
        + "/databases/my_db/schemas/my_schema/artifact-repositories/my_artifact_repository:rename?targetName=new_name",
    )
    kwargs = extra_params(query_params=[("targetName", "new_name")])

    with (
        mock.patch(API_CLIENT_REQUEST) as mocked_request,
        mock.patch.object(artifact_repository, "_rename_finalizer") as mock_finalizer,
    ):
        artifact_repository.rename("new_name")
        mock_finalizer.assert_called_once()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with (
        mock.patch(API_CLIENT_REQUEST) as mocked_request,
        mock.patch.object(artifact_repository, "_rename_finalizer") as mock_finalizer,
    ):
        op = artifact_repository.rename_async("new_name")
        assert isinstance(op, PollingOperation)
        op.result()
        mock_finalizer.assert_called_once()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_rename_artifact_repository_with_options(fake_root, artifact_repository):
    args = (
        fake_root,
        "POST",
        BASE_URL
        + "/databases/my_db/schemas/my_schema/artifact-repositories/my_artifact_repository:rename?"
        + "ifExists=True&targetDatabase=other_db&targetSchema=other_schema&targetName=new_name",
    )
    kwargs = extra_params(
        query_params=[
            ("ifExists", True),
            ("targetDatabase", "other_db"),
            ("targetSchema", "other_schema"),
            ("targetName", "new_name"),
        ]
    )

    with (
        mock.patch(API_CLIENT_REQUEST) as mocked_request,
        mock.patch.object(artifact_repository, "_rename_finalizer") as mock_finalizer,
    ):
        artifact_repository.rename("new_name", if_exists=True, target_database="other_db", target_schema="other_schema")
        mock_finalizer.assert_called_once()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_create_with_mode_or_replace(fake_root, artifact_repositories):
    from snowflake.core._common import CreateMode

    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/artifact-repositories?createMode=orReplace",
    )
    kwargs = extra_params(
        query_params=[("createMode", "orReplace")],
        body={"name": "my_artifact_repository", "type": "PIP", "api_integration": "my_api_integration"},
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        artifact_repositories.create(ARTIFACT_REPOSITORY, mode=CreateMode.or_replace)
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_create_with_mode_if_not_exists(fake_root, artifact_repositories):
    from snowflake.core._common import CreateMode

    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/artifact-repositories?createMode=ifNotExists",
    )
    kwargs = extra_params(
        query_params=[("createMode", "ifNotExists")],
        body={"name": "my_artifact_repository", "type": "PIP", "api_integration": "my_api_integration"},
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        artifact_repositories.create(ARTIFACT_REPOSITORY, mode=CreateMode.if_not_exists)
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_create_with_string_mode(fake_root, artifact_repositories):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/artifact-repositories?createMode=orReplace",
    )
    kwargs = extra_params(
        query_params=[("createMode", "orReplace")],
        body={"name": "my_artifact_repository", "type": "PIP", "api_integration": "my_api_integration"},
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        artifact_repositories.create(ARTIFACT_REPOSITORY, mode="or_replace")
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_with_multiple_filters(fake_root, artifact_repositories):
    """Test iter with multiple filter parameters combined."""
    args = (
        fake_root,
        "GET",
        BASE_URL
        + "/databases/my_db/schemas/my_schema/artifact-repositories?"
        + "like=test%&startsWith=test&showLimit=50&fromName=start_repo",
    )
    kwargs = extra_params(
        query_params=[
            ("like", "test%"),
            ("startsWith", "test"),
            ("showLimit", 50),
            ("fromName", "start_repo"),
        ]
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        list(artifact_repositories.iter(like="test%", starts_with="test", limit=50, from_name="start_repo"))
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_create_or_alter_name_mismatch(artifact_repositories):
    """Test that create_or_alter raises ValueError when names don't match."""
    mismatched_repo = ArtifactRepository(name="different_name", type="PIP", api_integration="my_api_integration")

    with pytest.raises(ValueError, match="Cannot call create_or_alter on a resource with a different name"):
        artifact_repositories["my_artifact_repository"].create_or_alter(mismatched_repo)


def test_resource_string_representation(artifact_repositories):
    """Test string representation of resources."""
    artifact_repo = artifact_repositories["my_artifact_repository"]
    assert "my_artifact_repository" in str(artifact_repo)
    assert "ArtifactRepositoryResource" in str(artifact_repo)


def test_collection_indexing(artifact_repositories):
    """Test collection indexing and item access."""
    # Test __getitem__
    repo = artifact_repositories["test_repo"]
    assert repo.name == "test_repo"

    # Test that different names create different resource instances
    repo1 = artifact_repositories["repo1"]
    repo2 = artifact_repositories["repo2"]
    assert repo1.name != repo2.name


def test_create_or_alter_new_resource(fake_root, artifact_repositories):
    """Test create_or_alter on a non-existing resource (creation scenario)."""
    new_repo = ArtifactRepository(
        name="brand_new_repository",
        type="PIP",
        api_integration="my_api_integration",
        comment="Created via create_or_alter",
    )

    args = (
        fake_root,
        "PUT",
        BASE_URL + "/databases/my_db/schemas/my_schema/artifact-repositories/brand_new_repository",
    )
    kwargs = extra_params(
        body={
            "name": "brand_new_repository",
            "type": "PIP",
            "api_integration": "my_api_integration",
            "comment": "Created via create_or_alter",
        },
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        result = artifact_repositories["brand_new_repository"].create_or_alter(new_repo)
        assert result is None  # create_or_alter returns None for both create and update
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_invalid_repository_type():
    """Test that invalid repository type raises validation error."""
    with pytest.raises(ValueError, match="must validate the enum values"):
        ArtifactRepository(
            name="test_repo",
            type="INVALID_TYPE",  # Invalid type - only PIP is supported
            api_integration="test_api_integration",
        )


def test_invalid_repository_name():
    """Test that invalid repository name raises validation error."""
    with pytest.raises(ValueError, match="must validate the regular expression"):
        ArtifactRepository(
            name="invalid-name-with-hyphens!",  # Invalid characters
            type="PIP",
            api_integration="test_api_integration",
        )
