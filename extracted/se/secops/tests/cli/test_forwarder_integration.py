"""Integration tests for the SecOps CLI forwarder commands."""

import pytest
import subprocess
import json
import uuid


@pytest.mark.integration
def test_cli_forwarder_lifecycle(cli_env, common_args):
    """Test forwarder creation, update, deletion, and retrieval (full lifecycle)."""
    # Generate a unique display name for testing
    test_display_name = f"test-forwarder-{uuid.uuid4().hex[:8]}"
    forwarder_ids = []

    try:
        # 1. Create a forwarder
        create_cmd = (
            [
                "secops",
            ]
            + common_args
            + [
                "forwarder",
                "create",
                "--display-name",
                test_display_name,
                "--metadata",
                json.dumps(
                    {
                        "labels": {"environment": "integration_test"},
                    }
                ),
                "--upload-compression",
                "true",
                "--enable-server",
                "true",
            ]
        )

        create_result = subprocess.run(
            create_cmd, env=cli_env, capture_output=True, text=True
        )

        # Check that the command executed successfully
        assert (
            create_result.returncode == 0
        ), f"Forwarder creation failed: {create_result.stderr}\n{create_result.stdout}"

        # Parse the output to get the forwarder ID
        try:
            created_data = json.loads(create_result.stdout)
            forwarder_id = created_data.get("name").split("/")[-1]
            assert (
                forwarder_id
            ), "Failed to get forwarder ID from creation response"
            forwarder_ids.append(forwarder_id)
            print(f"Created forwarder with ID: {forwarder_id}")
        except json.JSONDecodeError:
            pytest.fail(
                f"Could not parse JSON from create command output: {create_result.stdout}"
            )

        # 2. List forwarders and verify our created forwarder is in the list
        list_cmd = (
            [
                "secops",
            ]
            + common_args
            + ["forwarder", "list"]
        )

        list_result = subprocess.run(
            list_cmd, env=cli_env, capture_output=True, text=True
        )

        assert (
            list_result.returncode == 0
        ), f"List forwarders failed: {list_result.stderr}\n{list_result.stdout}"

        listed_forwarders = json.loads(list_result.stdout)
        forwarders = listed_forwarders.get("forwarders", [])

        assert len(forwarders) > 0, "No forwarders returned in list response"

        # Find our created forwarder in the list
        found_in_list = any(
            f.get("name").split("/")[-1] == forwarder_id for f in forwarders
        )
        assert (
            found_in_list
        ), f"Created forwarder {forwarder_id} not found in listed forwarders"

        # 3. Get the specific forwarder
        get_cmd = (
            [
                "secops",
            ]
            + common_args
            + ["forwarder", "get", "--id", forwarder_id]
        )

        get_result = subprocess.run(
            get_cmd, env=cli_env, capture_output=True, text=True
        )

        # Check that the get command executed successfully
        assert (
            get_result.returncode == 0
        ), f"Get forwarder failed: {get_result.stderr}\n{get_result.stdout}"

        get_data = json.loads(get_result.stdout)
        assert (
            get_data["name"].split("/")[-1] == forwarder_id
        ), "Retrieved forwarder ID doesn't match created ID"
        assert (
            get_data["displayName"] == test_display_name
        ), "Display name mismatch"
        assert get_data["config"]["metadata"], "Metadata not properly set"

        # 4. Update the forwarder (patch)
        updated_display_name = f"{test_display_name}-updated"
        updated_metadata = json.dumps(
            {"labels": {"environment": "updated_test"}}
        )

        patch_cmd = (
            [
                "secops",
            ]
            + common_args
            + [
                "forwarder",
                "update",
                "--id",
                forwarder_id,
                "--display-name",
                updated_display_name,
                "--metadata",
                updated_metadata,
                "--upload-compression",
                "false",
            ]
        )

        patch_result = subprocess.run(
            patch_cmd, env=cli_env, capture_output=True, text=True
        )

        # Check that the update command executed successfully
        assert (
            patch_result.returncode == 0
        ), f"Update forwarder failed: {patch_result.stderr}\n{patch_result.stdout}"

        # Verify the update was successful
        get_updated_cmd = (
            [
                "secops",
            ]
            + common_args
            + ["forwarder", "get", "--id", forwarder_id]
        )

        get_updated_result = subprocess.run(
            get_updated_cmd, env=cli_env, capture_output=True, text=True
        )

        # Check that the get command executed successfully
        assert (
            get_updated_result.returncode == 0
        ), f"Get updated forwarder failed: {get_updated_result.stderr}\n{get_updated_result.stdout}"

        get_updated_data = json.loads(get_updated_result.stdout)
        assert (
            get_updated_data["displayName"] == updated_display_name
        ), "Updated display name not applied"
        assert get_updated_data["config"][
            "metadata"
        ], "Metadata not properly set"

        # 5. Test get-or-create with the same display name (should retrieve existing)
        get_or_create_cmd = (
            [
                "secops",
            ]
            + common_args
            + [
                "forwarder",
                "get-or-create",
                "--display-name",
                updated_display_name,
            ]
        )

        get_or_create_result = subprocess.run(
            get_or_create_cmd, env=cli_env, capture_output=True, text=True
        )

        # Check that the command executed successfully
        assert (
            get_or_create_result.returncode == 0
        ), f"Get-or-create forwarder failed: {get_or_create_result.stderr}\n{get_or_create_result.stdout}"

        get_or_create_data = json.loads(get_or_create_result.stdout)
        assert (
            get_or_create_data["name"].split("/")[-1] == forwarder_id
        ), "Get-or-create retrieved a different forwarder ID"

        # 6. Test get-or-create with a new display name (should create new)
        new_display_name = f"test-forwarder-new-{uuid.uuid4().hex[:8]}"
        get_or_create_new_cmd = (
            [
                "secops",
            ]
            + common_args
            + ["forwarder", "get-or-create", "--display-name", new_display_name]
        )

        get_or_create_new_result = subprocess.run(
            get_or_create_new_cmd, env=cli_env, capture_output=True, text=True
        )

        # Check that the command executed successfully
        assert (
            get_or_create_new_result.returncode == 0
        ), f"Get-or-create new forwarder failed: {get_or_create_new_result.stderr}\n{get_or_create_new_result.stdout}"

        get_or_create_new_data = json.loads(get_or_create_new_result.stdout)
        new_forwarder_id = get_or_create_new_data["name"].split("/")[-1]
        forwarder_ids.append(new_forwarder_id)
        assert (
            new_forwarder_id != forwarder_id
        ), "Should have created a new forwarder"
        assert (
            get_or_create_new_data["displayName"] == new_display_name
        ), "New display name not set correctly"

        # 7. Delete the forwarders
        for f_id in forwarder_ids:
            delete_cmd = (
                [
                    "secops",
                ]
                + common_args
                + ["forwarder", "delete", "--id", f_id]
            )

            delete_result = subprocess.run(
                delete_cmd, env=cli_env, capture_output=True, text=True
            )

            # Check that the delete command executed successfully
            assert (
                delete_result.returncode == 0
            ), f"Delete forwarder failed: {delete_result.stderr}\n{delete_result.stdout}"

            # Verify the forwarder was actually deleted by trying to get it (should fail)
            verify_delete_cmd = (
                [
                    "secops",
                ]
                + common_args
                + ["forwarder", "get", "--id", f_id]
            )

            verify_delete_result = subprocess.run(
                verify_delete_cmd, env=cli_env, capture_output=True, text=True
            )

            # Should fail with an error since the forwarder was deleted
            assert (
                verify_delete_result.returncode != 0
            ), "Forwarder still exists after deletion"

            if verify_delete_result.returncode == 0:
                forwarder_ids.remove(f_id)
            print(f"Successfully deleted forwarder with ID: {f_id}")

    except Exception as e:
        # Attempt to clean up any created forwarders if test fails
        for f_id in forwarder_ids:
            try:
                cleanup_cmd = (
                    [
                        "secops",
                    ]
                    + common_args
                    + ["forwarder", "delete", "--id", f_id]
                )
                subprocess.run(
                    cleanup_cmd, env=cli_env, capture_output=True, text=True
                )
                print(
                    f"Cleaned up forwarder with ID: {f_id} "
                    "during exception handling"
                )
            except Exception:
                print(
                    f"Failed to clean up forwarder with ID: {f_id} "
                    "during exception handling"
                )
                pass

        pytest.fail(f"Unexpected error in CLI forwarder test: {str(e)}")


@pytest.mark.integration
def test_cli_forwarder_list_pagination(cli_env, common_args):
    """Test the forwarder list command with pagination."""
    # Execute the CLI command with a small page size
    cmd = (
        [
            "secops",
        ]
        + common_args
        + ["forwarder", "list", "--page-size", "1"]
    )

    result = subprocess.run(cmd, env=cli_env, capture_output=True, text=True)

    # Check that the command executed successfully
    assert (
        result.returncode == 0
    ), f"Command failed: {result.stderr}\n{result.stdout}"

    # Try to parse the output as JSON
    try:
        output = json.loads(result.stdout)
        assert "forwarders" in output
        # With page size 1, we should have only 1 forwarder or empty list if none exist
        if "forwarders" in output and output["forwarders"]:
            assert len(output["forwarders"]) == 1
    except json.JSONDecodeError:
        # If not valid JSON, check for expected error messages
        assert "Error:" not in result.stdout
