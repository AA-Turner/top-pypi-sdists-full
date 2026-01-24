#!/usr/bin/env python3

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
"""Example demonstrating entity import functionality with Chronicle."""

import argparse
import uuid
from typing import Any, Dict

from secops import SecOpsClient
from secops.exceptions import APIError


def create_sample_user_entity() -> Dict[str, Any]:
    """Create a sample user entity.

    Returns:
        A dictionary representing a user entity in Chronicle format
    """

    # Generate a unique ID for this entity
    user_id = f"user_{uuid.uuid4().hex[:8]}"

    # Create sample user entity
    return {
        "metadata": {
            "collectedTimestamp": "1970-01-01T03:25:45.000000124Z",
            "vendorName": "vendor",
            "productName": "product",
            "entityType": "USER",
        },
        "entity": {
            "user": {"userid": user_id, "productObjectId": "dev google"}
        },
    }


def create_sample_file_entity() -> Dict[str, Any]:
    """Create a sample file entity.

    Returns:
        A dictionary representing a file entity in Chronicle format
    """
    # Create sample file entity
    return {
        "metadata": {
            "collected_timestamp": "1970-01-01T03:25:45.000000124Z",
            "entity_type": "FILE",
            "vendor_name": "Sample Vendor",
            "product_name": "Entity Import Example",
        },
        "entity": {
            "file": {
                "md5": "d41d8cd98f00b204e9800998ecf8427e",  # MD5 of empty file
                "sha1": "da39a3ee5e6b4b0d3255bfef95601890afd80709",  # SHA1 of empty file
                "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",  # SHA256 of empty file
                "full_path": "/path/to/example.txt",
                "size": "0",
                "mimeType": "text/plain",
            }
        },
    }


def import_single_entity(chronicle_client):
    """Demonstrate importing a single entity.

    Args:
        chronicle_client: Initialized Chronicle client
    """
    print("\n=== Importing a Single Entity (User) ===")

    # Create a sample user entity
    user_entity = create_sample_user_entity()
    user_id = user_entity["entity"]["user"]["userid"]

    print(f"Entity ID: {user_id}")

    try:
        # Import the entity
        result = chronicle_client.import_entities(
            entities=user_entity, log_type="OKTA"
        )

        print("Entity successfully imported!")
        print(f"API Response: {result}")

    except APIError as e:
        print(f"Error importing entity: {e}")


def import_multiple_entities(chronicle_client):
    """Demonstrate importing multiple entities of different types.

    Args:
        chronicle_client: Initialized Chronicle client
    """
    print("\n=== Importing Multiple Entities (Different Types) ===")

    # Create sample entities of different types
    user_entity = create_sample_user_entity()
    file_entity = create_sample_file_entity()

    entities = [user_entity, file_entity]

    print(f"Number of entities: {len(entities)}")
    print(f"Entity Types: USER, FILE")

    try:
        # Import multiple entities in a single API call
        result = chronicle_client.import_entities(
            entities=entities, log_type="OKTA"
        )

        print("All entities successfully imported!")
        print(f"API Response: {result}")

    except APIError as e:
        print(f"Error importing entities: {e}")


def main():
    """Run the example."""
    parser = argparse.ArgumentParser(
        description="Example of entity import with Chronicle"
    )
    parser.add_argument(
        "--customer_id", required=True, help="Chronicle instance ID"
    )
    parser.add_argument("--project_id", required=True, help="GCP project ID")
    parser.add_argument("--region", default="us", help="Chronicle API region")

    args = parser.parse_args()

    # Initialize the client
    client = SecOpsClient()

    # Configure Chronicle client
    chronicle = client.chronicle(
        customer_id=args.customer_id,
        project_id=args.project_id,
        region=args.region,
    )

    # Run examples
    import_single_entity(chronicle)
    import_multiple_entities(chronicle)


if __name__ == "__main__":
    main()
