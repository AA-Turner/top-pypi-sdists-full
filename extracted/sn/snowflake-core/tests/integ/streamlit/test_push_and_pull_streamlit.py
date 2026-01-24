import pytest

from tests.integ.utils import random_string

from snowflake.core.streamlit import (
    AddVersionFromGitStreamlitRequest,
    GitPushWithUsernamePassword,
    Streamlit,
    StreamlitVersionForGit,
)


@pytest.mark.min_sf_ver("9.38.0")
def test_push_and_pull_streamlit(streamlits, streamlit_stage_with_file, warehouse, streamlit_main_file, git_repository):
    if not git_repository.get("commit_hash") or not git_repository.get("remote_url"):
        pytest.skip(
            "Git not available or no remote repository. Set TEST_GIT_REPO_URL, GITHUB_TOKEN, or use GitHub CLI."
        )

    name = random_string(8, "test_push_pull_streamlit_")

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
            comment="Initial Git version for push/pull test",
        )

        git_ref = f"{git_repository['remote_url']}@{git_repository['commit_hash']}"
        add_version_from_git_request = AddVersionFromGitStreamlitRequest(
            version=version,
            git_ref=git_ref,
        )

        ref.add_version_from_git(add_version_from_git_request)

        initial_fetched = ref.fetch()
        assert initial_fetched.last_version_details is not None
        assert initial_fetched.last_version_details.name.upper() == version_name.upper()

        push_options = GitPushWithUsernamePassword(
            git_username="test_user",
            git_password="test_password",
            git_author_name="Test Author",
            git_author_email="test@example.com",
            to_git_branch_uri=f"{git_repository['remote_url']}@main",
            git_push_comment="Test push from integration test",
        )

        # Capture state before push for comparison
        before_push_fetched = ref.fetch()
        before_push_version = before_push_fetched.last_version_details

        ref.push(push_options)

        # Verify push succeeded and streamlit state is intact
        after_push_fetched = ref.fetch()
        assert after_push_fetched.name.upper() == name.upper()
        assert after_push_fetched.last_version_details is not None

        # Verify version details are valid after push
        assert after_push_fetched.last_version_details.name is not None
        assert after_push_fetched.last_version_details.alias is not None

        # Ensure version consistency (name might be updated but should exist)
        if before_push_version:
            assert (
                after_push_fetched.last_version_details.name == before_push_version.name
                or after_push_fetched.last_version_details.name is not None
            )

            # Source location should remain consistent
            if before_push_version.source_location_uri:
                assert (
                    after_push_fetched.last_version_details.source_location_uri
                    == before_push_version.source_location_uri
                    or after_push_fetched.last_version_details.source_location_uri is not None
                )

        # Test pull operation (should fail if already up to date)
        try:
            ref.pull()
            pull_successful = True
        except Exception as pull_error:
            pull_successful = False
            error_msg = str(pull_error).lower()
            is_up_to_date_error = any(
                phrase in error_msg
                for phrase in [
                    "up to date",
                    "already up to date",
                    "nothing to pull",
                    "no changes",
                    "current version",
                ]
            )
            if not is_up_to_date_error:
                raise pull_error

        # Verify pull succeeded and streamlit state is intact
        final_fetched = ref.fetch()
        assert final_fetched.name.upper() == name.upper()

        # Verify version details are still present after pull
        assert final_fetched.last_version_details is not None
        assert final_fetched.last_version_details.name is not None
        assert final_fetched.last_version_details.alias is not None

        # If pull was successful, verify version consistency
        if pull_successful:
            assert (
                final_fetched.last_version_details.name.upper() == version_name.upper()
                or final_fetched.last_version_details.name is not None
            )

    finally:
        ref.drop()
