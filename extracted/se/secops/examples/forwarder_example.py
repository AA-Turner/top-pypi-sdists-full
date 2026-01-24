#!/usr/bin/env python3
"""Example usage of Google SecOps SDK for Chronicle Forwarder Management.

This example demonstrates how to use the Chronicle Forwarder Management API 
via the Google SecOps SDK to create, list, get, update, and delete forwarders.
"""

import argparse
import json
import time
from datetime import datetime

from secops import SecOpsClient
from secops.chronicle import ChronicleClient
from secops.exceptions import APIError


def get_client(project_id, customer_id, region):
    """Initialize and return the Chronicle client.

    Args:
        project_id: Google Cloud Project ID.
        customer_id: Chronicle Customer ID (UUID).
        region: Chronicle region (us or eu).

    Returns:
        Chronicle client instance.
    """
    client = SecOpsClient()
    chronicle = client.chronicle(
        customer_id=customer_id, project_id=project_id, region=region
    )
    return chronicle


def example_create_forwarder(chronicle: ChronicleClient):
    """Example: Create a new log forwarder in Chronicle.

    Args:
        chronicle: Initialized Chronicle client.

    Returns:
        The created forwarder ID.
    """
    print("\n=== Example: Create a log forwarder ===")

    # Generate a unique name for our example forwarder using current timestamp
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    display_name = f"Example-Forwarder-{timestamp}"

    try:
        # Create a forwarder with some basic configuration
        forwarder = chronicle.create_forwarder(
            display_name=display_name,
            metadata={"labels": {"env": "test", "purpose": "sdk-example"}},
            upload_compression=True,
            enable_server=False,
            http_settings={"port": 8080, "host": "192.168.0.100"},
        )

        forwarder_id = forwarder["name"].split("/")[-1]
        print(f"Successfully created forwarder:")
        print(f"  ID: {forwarder_id}")
        print(f"  Display Name: {forwarder.get('displayName')}")
        print(f"  Upload Compression: {forwarder.get('uploadCompression')}")

        # Return forwarder ID for use in other examples
        return forwarder_id

    except APIError as e:
        print(f"Error creating forwarder: {e}")
        return None


def example_get_forwarder(chronicle: ChronicleClient, forwarder_id: str):
    """Example: Get a forwarder by ID.

    Args:
        chronicle: Initialized Chronicle client.
        forwarder_id: ID of the forwarder to retrieve.
    """
    print("\n=== Example: Get a forwarder by ID ===")

    try:
        forwarder = chronicle.get_forwarder(forwarder_id=forwarder_id)

        print(f"Retrieved forwarder details:")
        print(f"  ID: {forwarder_id}")
        print(f"  Display Name: {forwarder.get('displayName')}")
        print(f"  Create Time: {forwarder.get('createTime')}")
        print(f"  Config: {json.dumps(forwarder.get('config', {}), indent=2)}")

    except APIError as e:
        print(f"Error retrieving forwarder: {e}")


def example_list_forwarders(chronicle: ChronicleClient):
    """Example: List all forwarders in Chronicle.

    Args:
        chronicle: Initialized Chronicle client.
    """
    print("\n=== Example: List all forwarders ===")

    try:
        # Get first page of forwarders with a small page size for demo
        response = chronicle.list_forwarders(page_size=5)
        forwarders = response.get("forwarders", [])

        print(f"Retrieved {len(forwarders)} forwarders:")

        for idx, forwarder in enumerate(forwarders, 1):
            forwarder_id = forwarder["name"].split("/")[-1]
            print(
                f"  {idx}. {forwarder.get('displayName')} (ID: {forwarder_id})"
            )

        # Check if there are more pages
        if "nextPageToken" in response:
            print(
                f"\nMore forwarders available. Next page token: {response['nextPageToken']}"
            )

    except APIError as e:
        print(f"Error listing forwarders: {e}")


def example_update_forwarder(chronicle: ChronicleClient, forwarder_id: str):
    """Example: Update an existing forwarder.

    Args:
        chronicle: Initialized Chronicle client.
        forwarder_id: ID of the forwarder to update.
    """
    print("\n=== Example: Update a forwarder ===")

    try:
        # First, get current forwarder to show before/after
        before = chronicle.get_forwarder(forwarder_id=forwarder_id)
        print("Current forwarder configuration:")
        print(f"  Display Name: {before.get('displayName')}")
        print(f"  Config: {json.dumps(before.get('config', {}), indent=2)}")

        # Update the forwarder with new metadata
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        updated_name = f"{before.get('displayName')}-Updated-{timestamp}"

        # Update specific fields
        updated = chronicle.update_forwarder(
            forwarder_id=forwarder_id,
            display_name=updated_name,
            metadata={
                "labels": {
                    "env": "test",
                    "purpose": "sdk-example",
                    "updated": "true",
                }
            },
        )

        print("\nUpdated forwarder configuration:")
        print(f"  Display Name: {updated.get('displayName')}")
        print(f"  Config: {updated.get('config')}")

    except APIError as e:
        print(f"Error updating forwarder: {e}")


def example_delete_forwarder(chronicle: ChronicleClient, forwarder_id: str):
    """Example: Delete a forwarder.

    Args:
        chronicle: Initialized Chronicle client.
        forwarder_id: ID of the forwarder to delete.
    """
    print("\n=== Example: Delete a forwarder ===")

    try:
        # Delete the forwarder
        chronicle.delete_forwarder(forwarder_id=forwarder_id)
        print(f"Successfully deleted forwarder with ID: {forwarder_id}")

        # Verify deletion by trying to get the forwarder (should fail)
        print("\nVerifying deletion...")
        try:
            chronicle.get_forwarder(forwarder_id=forwarder_id)
            print("Error: Forwarder still exists!")
        except APIError as e:
            if "not found" in str(e).lower():
                print("Verification successful: Forwarder no longer exists")
            else:
                print(f"Error during verification: {e}")

    except APIError as e:
        print(f"Error deleting forwarder: {e}")


def main():
    """Run the forwarder management examples."""
    parser = argparse.ArgumentParser(
        description="Example usage of Google SecOps SDK for Chronicle Forwarder Management"
    )
    parser.add_argument("--project-id", required=True, help="GCP project ID")
    parser.add_argument(
        "--customer-id", required=True, help="Chronicle customer ID"
    )
    parser.add_argument(
        "--region", default="us", choices=["us", "eu"], help="Chronicle region"
    )
    args = parser.parse_args()

    # Initialize the Chronicle client
    chronicle = get_client(args.project_id, args.customer_id, args.region)

    print("Google SecOps SDK - Chronicle Forwarder Management Examples")
    print("----------------------------------------------------------")

    # Run the example to create a new test forwarder
    forwarder_id = example_create_forwarder(chronicle)
    if not forwarder_id:
        print("Failed to create test forwarder. Exiting.")
        return

    # Wait a moment for the forwarder to be fully created
    print("\nWaiting for forwarder to be ready...")
    time.sleep(2)

    # Run the example to get a forwarder by ID
    example_get_forwarder(chronicle, forwarder_id)

    # Run the example to list all forwarders
    example_list_forwarders(chronicle)

    # Run the example to update the forwarder
    example_update_forwarder(chronicle, forwarder_id)

    # Finally, run the example to delete the forwarder
    example_delete_forwarder(chronicle, forwarder_id)


if __name__ == "__main__":
    main()
