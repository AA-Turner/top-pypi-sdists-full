import pytest

from tests.integ.utils import random_string

from snowflake.core.streamlit import (
    AddVersionFromGitStreamlitRequest,
    Streamlit,
    StreamlitVersionForGit,
)


@pytest.mark.min_sf_ver("9.38.0")
def test_add_version_from_git_streamlit(
    streamlits, streamlit_stage_with_file, warehouse, streamlit_main_file, git_repository
):
    if not git_repository.get("commit_hash") or not git_repository.get("remote_url"):
        pytest.skip(
            "Git not available or no remote repository. Set TEST_GIT_REPO_URL, GITHUB_TOKEN, or use GitHub CLI."
        )

    name = random_string(8, "test_add_version_from_git_streamlit_")

    st = Streamlit(
        name=name,
        query_warehouse=warehouse.name,
        source_location=f"@{streamlit_stage_with_file.name}",
        main_file=streamlit_main_file,
    )

    ref = streamlits.create(st)
    try:
        version_name = random_string(8, "git_version_")
        version = StreamlitVersionForGit(
            name=version_name,
            comment="Test Git version for integration testing",
        )

        # Use remote URL with commit hash
        git_ref = f"{git_repository['remote_url']}@{git_repository['commit_hash']}"

        add_version_from_git_request = AddVersionFromGitStreamlitRequest(
            version=version,
            git_ref=git_ref,
        )

        ref.add_version_from_git(add_version_from_git_request)

        fetched = ref.fetch()
        assert fetched.name.upper() == name.upper()

        assert fetched.last_version_details is not None
        assert fetched.last_version_details.name is not None
        assert fetched.last_version_details.alias.upper() == version_name.upper()

    finally:
        ref.drop()
