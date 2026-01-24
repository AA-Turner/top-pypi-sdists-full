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
"""Example for using the Chronicle find_udm_field_values API.

This example demonstrates how to use the find_udm_field_values method
from the Chronicle API client to search for UDM field values matching a query.
"""

import argparse
import json
import os
from typing import Dict, Any, Optional

from secops.chronicle.client import ChronicleClient
from secops.exceptions import SecOpsError


def example_find_udm_field_values(
    client: ChronicleClient,
    query: str,
    page_size: Optional[int] = None,
) -> Dict[str, Any]:
    """Find UDM field values that match a query.

    Args:
        client: Authenticated ChronicleClient instance
        query: The partial UDM field value to match
        page_size: The maximum number of value matches to return

    Returns:
        Dictionary containing field values that match the query

    Raises:
        SecOpsError: If the API request fails
    """
    print("\n=== Find UDM Field Values ===\n")

    try:
        print(f"Finding UDM field values for query: '{query}'")
        if page_size:
            print(f"Using page size: {page_size}")

        results = client.find_udm_field_values(query=query, page_size=page_size)

        print("\nResults:\n")
        print(json.dumps(results, indent=4))
        return results

    except SecOpsError as e:
        print(f"Error finding UDM field values: {e}")
        raise


def main() -> None:
    """Run the example."""
    parser = argparse.ArgumentParser(
        description="Example for Chronicle find_udm_field_values API"
    )
    parser.add_argument(
        "--project_id", required=True, help="Google Cloud project ID"
    )
    parser.add_argument(
        "--customer_id", required=True, help="Chronicle customer ID"
    )
    parser.add_argument(
        "--region", default="us", help="Chronicle region (default: us)"
    )
    # Using fixed values for query and page_size in the example

    args = parser.parse_args()

    # Initialize the Chronicle client
    client = ChronicleClient(
        project_id=args.project_id,
        customer_id=args.customer_id,
        region=args.region,
    )

    try:
        # Call the find_udm_field_values method
        example_find_udm_field_values(
            client=client,
            query="source",
            page_size=5,
        )

    except Exception as e:
        print(f"Failed to find UDM field values: {e}")
        raise


if __name__ == "__main__":
    main()
