import pytest

from snowflake.core.artifact_repository import ArtifactRepository
from snowflake.core.exceptions import NotFoundError
from tests.integ.utils import random_string


def test_drop_artifact_repository(artifact_repositories, temp_pypi_api_integration):
    """Test dropping an artifact repository."""
    ar_name = random_string(10, "test_artifact_repository_drop_")
    ar_def = ArtifactRepository(
        name=ar_name,
        type="PIP",
        api_integration=temp_pypi_api_integration,
        comment="created by test_drop_artifact_repository",
    )
    ar = artifact_repositories.create(ar_def)

    fetched_ar = ar.fetch()
    assert fetched_ar.name == ar_name.upper()

    ar.drop()

    with pytest.raises(NotFoundError):
        ar.fetch()


def test_drop_artifact_repository_if_exists(artifact_repositories, temp_pypi_api_integration):
    """Test dropping an artifact repository with if_exists=True."""
    ar_name = random_string(10, "test_artifact_repository_drop_if_exists_")
    ar_def = ArtifactRepository(
        name=ar_name,
        type="PIP",
        api_integration=temp_pypi_api_integration,
        comment="created by test_drop_artifact_repository_if_exists",
    )
    ar = artifact_repositories.create(ar_def)

    ar.drop(if_exists=True)

    with pytest.raises(NotFoundError):
        ar.fetch()


def test_drop_nonexistent_artifact_repository_if_exists(artifact_repositories):
    """Test dropping a non-existent artifact repository with if_exists=True."""
    ar_name = random_string(10, "test_artifact_repository_nonexistent_")
    ar = artifact_repositories[ar_name]

    ar.drop(if_exists=True)


def test_drop_nonexistent_artifact_repository_without_if_exists(artifact_repositories):
    """Test dropping a non-existent artifact repository without if_exists."""
    ar_name = random_string(10, "test_artifact_repository_nonexistent_no_if_exists_")
    ar = artifact_repositories[ar_name]

    with pytest.raises(NotFoundError):
        ar.drop()
