from snowflake.core.artifact_repository import ArtifactRepository
from tests.integ.utils import random_string


def test_create_or_alter_artifact_repository(artifact_repositories, temp_pypi_api_integration):
    """Test create_or_alter functionality - creating new artifact repository."""
    ar_name = random_string(10, "test_artifact_repository_create_or_alter_")
    ar_def = ArtifactRepository(
        name=ar_name,
        type="PIP",
        api_integration=temp_pypi_api_integration,
        comment="created by test_create_or_alter_artifact_repository",
    )
    ar = artifact_repositories[ar_name]
    ar.create_or_alter(ar_def)
    try:
        fetched_ar = ar.fetch()
        assert fetched_ar.name == ar_name.upper()
        assert fetched_ar.type == ar_def.type
        assert fetched_ar.api_integration == temp_pypi_api_integration
        assert fetched_ar.comment == ar_def.comment

        fetched_ar.comment = "altered by test_create_or_alter_artifact_repository"
        ar.create_or_alter(fetched_ar)

        altered_ar = ar.fetch()
        assert altered_ar.name == ar_name.upper()
        assert altered_ar.type == ar_def.type
        assert altered_ar.api_integration == temp_pypi_api_integration
        assert altered_ar.comment == "altered by test_create_or_alter_artifact_repository"
    finally:
        ar.drop()


def test_create_or_alter_unset_comment(artifact_repositories, temp_pypi_api_integration):
    """Test create_or_alter unsetting comment field."""
    ar_name = random_string(10, "test_artifact_repository_unset_comment_")
    ar_def = ArtifactRepository(
        name=ar_name,
        type="PIP",
        api_integration=temp_pypi_api_integration,
        comment="comment to be removed",
    )
    ar = artifact_repositories.create(ar_def)
    try:
        updated_ar_def = ArtifactRepository(
            name=ar_name,
            type="PIP",
            api_integration=temp_pypi_api_integration,
            comment=None,
        )
        ar.create_or_alter(updated_ar_def)

        fetched_ar = ar.fetch()
        assert fetched_ar.name == ar_name.upper()
        assert fetched_ar.comment is None
    finally:
        ar.drop()
