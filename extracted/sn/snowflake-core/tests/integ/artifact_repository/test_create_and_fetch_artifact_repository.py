import pytest

from snowflake.core import CreateMode
from snowflake.core.artifact_repository import ArtifactRepository
from snowflake.core.exceptions import ConflictError
from tests.integ.utils import random_string


def test_create_and_fetch_artifact_repository(artifact_repositories, temp_pypi_api_integration):
    """Test creating and fetching an artifact repository."""
    ar_name = random_string(10, "test_artifact_repository_")
    ar_def = ArtifactRepository(
        name=ar_name,
        type="PIP",
        api_integration=temp_pypi_api_integration,
        comment="created by test_create_and_fetch_artifact_repository",
    )
    ar = artifact_repositories.create(ar_def)
    try:
        fetched_ar = ar.fetch()
        assert fetched_ar.name == ar_name.upper()
        assert fetched_ar.type == ar_def.type
        assert fetched_ar.api_integration == temp_pypi_api_integration
        assert fetched_ar.comment == ar_def.comment
        assert fetched_ar.created_on is not None
        assert fetched_ar.database_name is not None
        assert fetched_ar.schema_name is not None
        assert fetched_ar.owner is not None
        assert fetched_ar.owner_role_type is not None
    finally:
        ar.drop()


def test_create_and_fetch_artifact_repository_minimal(artifact_repositories, temp_pypi_api_integration):
    """Test creating artifact repository with minimal required fields only."""
    ar_name = random_string(10, "test_artifact_repository_minimal_")
    ar_def = ArtifactRepository(
        name=ar_name,
        type="PIP",
        api_integration=temp_pypi_api_integration,
    )
    ar = artifact_repositories.create(ar_def)
    try:
        fetched_ar = ar.fetch()
        assert fetched_ar.name == ar_name.upper()
        assert fetched_ar.type == "PIP"
        assert fetched_ar.api_integration == temp_pypi_api_integration
        assert fetched_ar.comment is None
        assert fetched_ar.created_on is not None
        assert fetched_ar.database_name is not None
        assert fetched_ar.schema_name is not None
        assert fetched_ar.owner is not None
    finally:
        ar.drop()


def test_create_mode_error_if_exists(artifact_repositories, temp_pypi_api_integration):
    """Test CreateMode.error_if_exists - should fail when resource already exists."""
    ar_name = random_string(10, "test_artifact_repository_error_if_exists_")
    ar_def = ArtifactRepository(
        name=ar_name,
        type="PIP",
        api_integration=temp_pypi_api_integration,
        comment="test CreateMode.error_if_exists",
    )

    ar = artifact_repositories.create(ar_def)
    try:
        with pytest.raises(ConflictError):
            artifact_repositories.create(ar_def, mode=CreateMode.error_if_exists)
    finally:
        ar.drop()


def test_create_mode_or_replace(artifact_repositories, temp_pypi_api_integration):
    """Test CreateMode.or_replace - should replace existing resource."""
    ar_name = random_string(10, "test_artifact_repository_or_replace_")
    ar_def = ArtifactRepository(
        name=ar_name,
        type="PIP",
        api_integration=temp_pypi_api_integration,
        comment="original comment",
    )

    ar = artifact_repositories.create(ar_def)
    try:
        updated_ar_def = ArtifactRepository(
            name=ar_name,
            type="PIP",
            api_integration=temp_pypi_api_integration,
            comment="replaced comment",
        )
        artifact_repositories.create(updated_ar_def, mode=CreateMode.or_replace)

        fetched_ar = ar.fetch()
        assert fetched_ar.comment == "replaced comment"
    finally:
        ar.drop()


def test_create_mode_if_not_exists(artifact_repositories, temp_pypi_api_integration):
    """Test CreateMode.if_not_exists - should not error if resource exists and should not replace it."""
    ar_name = random_string(10, "test_artifact_repository_if_not_exists_")
    ar_def = ArtifactRepository(
        name=ar_name,
        type="PIP",
        api_integration=temp_pypi_api_integration,
        comment="original comment",
    )

    ar = artifact_repositories.create(ar_def, mode=CreateMode.if_not_exists)
    try:
        # Different comment to verify resource is not replaced
        different_ar_def = ArtifactRepository(
            name=ar_name,
            type="PIP",
            api_integration=temp_pypi_api_integration,
            comment="this comment should be ignored because resource already exists",
        )
        artifact_repositories.create(different_ar_def, mode=CreateMode.if_not_exists)

        fetched_ar = ar.fetch()
        assert fetched_ar.comment == "original comment"
    finally:
        ar.drop()
