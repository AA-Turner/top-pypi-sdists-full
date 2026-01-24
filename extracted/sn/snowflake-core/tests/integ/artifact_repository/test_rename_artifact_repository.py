import pytest

from snowflake.core.artifact_repository import ArtifactRepository
from snowflake.core.exceptions import NotFoundError
from tests.integ.utils import random_string


def test_rename_artifact_repository(artifact_repositories, temp_pypi_api_integration):
    """Test basic rename functionality for artifact repositories."""
    original_name = random_string(10, "test_original_artifact_repo_")
    new_name = random_string(10, "test_renamed_artifact_repo_")

    ar_def = ArtifactRepository(
        name=original_name,
        type="PIP",
        api_integration=temp_pypi_api_integration,
        comment="Original artifact repository for rename test",
    )
    ar_handle = artifact_repositories.create(ar_def)

    try:
        fetched_ar = ar_handle.fetch()
        assert fetched_ar.name == original_name.upper()

        ar_handle.rename(new_name)

        fetched_ar = ar_handle.fetch()
        assert fetched_ar.name == new_name.upper()
        assert fetched_ar.schema_name == artifact_repositories.schema.name.upper()
        assert fetched_ar.database_name == artifact_repositories.database.name.upper()

        with pytest.raises(NotFoundError):
            artifact_repositories[original_name].fetch()

    finally:
        ar_handle.drop(if_exists=True)


def test_rename_nonexistent_artifact_repository(artifact_repositories):
    """Test renaming a non-existent artifact repository raises NotFoundError."""
    nonexistent_name = random_string(10, "test_nonexistent_artifact_repo_")
    new_name = random_string(10, "test_new_artifact_repo_")

    with pytest.raises(NotFoundError):
        artifact_repositories[nonexistent_name].rename(new_name)


def test_rename_artifact_repository_with_if_exists(artifact_repositories):
    """Test renaming with if_exists=True doesn't error for non-existent repositories."""
    nonexistent_name = random_string(10, "test_nonexistent_artifact_repo_")
    new_name = random_string(10, "test_new_artifact_repo_")

    artifact_repositories[nonexistent_name].rename(new_name, if_exists=True)


def test_rename_artifact_repository_cross_schema(artifact_repositories, temp_schema, temp_pypi_api_integration):
    """Test renaming artifact repository across schemas."""
    original_name = random_string(10, "test_cross_schema_artifact_repo_")
    new_name = random_string(10, "test_renamed_cross_schema_artifact_repo_")

    ar_def = ArtifactRepository(
        name=original_name,
        type="PIP",
        api_integration=temp_pypi_api_integration,
        comment="Cross-schema rename test repository",
    )
    ar_handle = artifact_repositories.create(ar_def)

    try:
        ar_handle.rename(new_name, target_schema=temp_schema.name, target_database=ar_handle.database.name)

        fetched_ar = ar_handle.fetch()
        assert fetched_ar.name.upper() == new_name.upper()
        assert fetched_ar.schema_name.upper() == temp_schema.name.upper()
        assert fetched_ar.database_name.upper() == ar_handle.database.name.upper()

        with pytest.raises(NotFoundError):
            artifact_repositories[original_name].fetch()

    finally:
        ar_handle.drop(if_exists=True)


def test_rename_artifact_repository_cross_database(artifact_repositories, temp_db, temp_pypi_api_integration):
    """Test renaming artifact repository across databases."""
    original_name = random_string(10, "test_cross_db_artifact_repo_")
    new_name = random_string(10, "test_renamed_cross_db_artifact_repo_")

    ar_def = ArtifactRepository(
        name=original_name,
        type="PIP",
        api_integration=temp_pypi_api_integration,
        comment="Cross-database rename test repository",
    )
    ar_handle = artifact_repositories.create(ar_def)

    try:
        ar_handle.rename(new_name, target_database=temp_db.name, target_schema="PUBLIC")

        fetched_ar = ar_handle.fetch()
        assert fetched_ar.name.upper() == new_name.upper()
        assert fetched_ar.database_name.upper() == temp_db.name.upper()
        assert fetched_ar.schema_name.upper() == "PUBLIC"

        with pytest.raises(NotFoundError):
            artifact_repositories[original_name].fetch()

    finally:
        ar_handle.drop(if_exists=True)
