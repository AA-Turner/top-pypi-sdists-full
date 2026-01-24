# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""Integration tests for Chronicle forwarder methods."""
import pytest
import uuid

from secops import SecOpsClient
from secops.exceptions import APIError
from ..config import CHRONICLE_CONFIG, SERVICE_ACCOUNT_JSON


@pytest.mark.integration
def test_forwarder_lifecycle():
    """Test complete lifecycle of forwarders with API.

    Tests the following client methods:
    - create_forwarder
    - list_forwarders
    - get_forwarder
    - update_forwarder
    - delete_forwarder
    - get_or_create_forwarder (both for existing and new)
    """
    # Initialize client
    client = SecOpsClient(service_account_info=SERVICE_ACCOUNT_JSON)
    chronicle = client.chronicle(**CHRONICLE_CONFIG)

    # Generate unique forwarder name to avoid conflicts
    unique_id = str(uuid.uuid4())[:8]
    display_name = f"Test-Forwarder-{unique_id}"

    # Tracking created forwarder IDs for cleanup
    created_forwarders = []

    try:
        print(f"\n--- Testing Forwarder Lifecycle ---")
        print(f"Using display_name: {display_name}")

        # Step 1: Create a new forwarder
        print("\n1. Testing create_forwarder()")
        forwarder = chronicle.create_forwarder(display_name=display_name)

        # Verify forwarder was created
        assert forwarder is not None
        assert "name" in forwarder
        assert "displayName" in forwarder
        assert forwarder["displayName"] == display_name

        # Store forwarder ID for cleanup
        forwarder_id = forwarder["name"].split("/")[-1]
        created_forwarders.append(forwarder_id)
        print(f"Created forwarder with ID: {forwarder_id}")

        # Step 2: List forwarders and verify our forwarder is in the list
        print("\n2. Testing list_forwarders()")
        forwarders = chronicle.list_forwarders()

        # Verify list returned results
        assert forwarders is not None
        assert "forwarders" in forwarders

        # Find our forwarder in the list
        found = False
        for f in forwarders["forwarders"]:
            if f["name"].split("/")[-1] == forwarder_id:
                found = True
                break

        assert (
            found
        ), f"Created forwarder {forwarder_id} not found in list results"
        print(f"Successfully found forwarder {forwarder_id} in list results")

        # Step 3: Get specific forwarder
        print("\n3. Testing get_forwarder()")
        get_result = chronicle.get_forwarder(forwarder_id=forwarder_id)

        # Verify get returned the correct forwarder
        assert get_result is not None
        assert get_result["name"].split("/")[-1] == forwarder_id
        assert get_result["displayName"] == display_name
        print(f"Successfully retrieved forwarder {forwarder_id}")

        # Step 4: Update forwarder
        print("\n4. Testing update_forwarder()")
        updated_display_name = f"{display_name}-updated"
        updated_forwarder = chronicle.update_forwarder(
            forwarder_id=forwarder_id,
            display_name=updated_display_name,
            metadata={"labels": {"env": "test"}},
        )

        # Verify update was successful
        assert updated_forwarder is not None
        assert updated_forwarder["name"].split("/")[-1] == forwarder_id
        assert updated_forwarder["displayName"] == updated_display_name
        print(f"Successfully updated forwarder to {updated_display_name}")

        # Verify the update was applied by getting the forwarder again
        updated_get_result = chronicle.get_forwarder(forwarder_id=forwarder_id)
        assert updated_get_result["displayName"] == updated_display_name
        assert (
            updated_get_result["config"]["metadata"]["labels"]["env"] == "test"
        )
        print("Verified update was applied correctly")

        # Step 5: Test get_or_create_forwarder for existing forwarder
        print("\n5. Testing get_or_create_forwarder() with existing forwarder")
        existing_result = chronicle.get_or_create_forwarder(
            display_name=updated_display_name
        )

        # Verify we got the existing forwarder
        assert existing_result is not None
        assert existing_result["name"].split("/")[-1] == forwarder_id
        assert existing_result["displayName"] == updated_display_name
        print(f"Successfully retrieved existing forwarder {forwarder_id}")

        # Step 6: Test get_or_create_forwarder for new forwarder
        print("\n6. Testing get_or_create_forwarder() with new forwarder")
        new_display_name = f"New-Test-Forwarder-{unique_id}"
        new_result = chronicle.get_or_create_forwarder(
            display_name=new_display_name
        )

        # Verify we created a new forwarder
        assert new_result is not None
        assert "name" in new_result
        assert new_result["displayName"] == new_display_name

        # Store forwarder ID for cleanup
        new_forwarder_id = new_result["name"].split("/")[-1]
        created_forwarders.append(new_forwarder_id)
        print(f"Created new forwarder with ID: {new_forwarder_id}")

        # Step 7: Test delete_forwarder
        print("\n7. Testing delete_forwarder()")
        delete_result = chronicle.delete_forwarder(forwarder_id=forwarder_id)

        # Verify delete was successful
        assert delete_result is not None
        print(f"Successfully deleted forwarder {forwarder_id}")

        # Verify forwarder was actually deleted by trying to get it
        try:
            chronicle.get_forwarder(forwarder_id=forwarder_id)
            pytest.fail(f"Forwarder {forwarder_id} still exists after deletion")
        except APIError as e:
            # Expected error for deleted resource
            assert "not found" in str(e).lower() or "404" in str(e)
            print("Verified deletion by confirming forwarder no longer exists")

        # Remove from cleanup list since it's already deleted
        created_forwarders.remove(forwarder_id)

    except APIError as e:
        print(f"\nAPI Error details: {str(e)}")
        # Skip the test rather than fail if permissions are not available
        if "permission" in str(e).lower():
            pytest.skip("Insufficient permissions to manage forwarders")
        raise

    finally:
        # Cleanup any remaining created forwarders
        print("\n--- Cleanup Phase ---")
        for fwd_id in created_forwarders:
            try:
                print(f"Cleaning up forwarder {fwd_id}")
                chronicle.delete_forwarder(forwarder_id=fwd_id)
            except Exception as e:
                print(f"Error during cleanup of forwarder {fwd_id}: {str(e)}")
