#!/usr/bin/env python3
"""
Example script for Chronicle Parser Extensions operations.
"""

import argparse
import time
from typing import Optional

from secops import SecOpsClient


def example_list_parser_extensions(chronicle) -> None:
    """Example 1: List parser extensions for a log type.

    Args:
        chronicle: Initialized ChronicleClient instance
    """
    print("\n=== Example 1: List Parser Extensions ===")
    log_type = "OKTA"

    try:
        print(f"Listing parser extensions for log type: {log_type}")
        extensions = chronicle.list_parser_extensions(log_type)

        print(f"Found {len(extensions)} parser extensions:")
        for i, extension in enumerate(extensions["parserExtensions"], 1):
            extension_id = extension.get("name", "").split("/")[-1]
            state = extension.get("state", "UNKNOWN")
            print(f"  {i}. ID: {extension_id} (State: {state})")

    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Error listing parser extensions: {e}")


def example_get_parser_extension(chronicle, extension_id) -> None:
    """Example 2: Get details of a specific parser extension.

    Args:
        chronicle: Initialized ChronicleClient instance
        extension_id: The ID of the parser extension to update
    """
    print("\n=== Example 2: Get Parser Extension Details ===")
    log_type = "OKTA"

    try:
        print(f"Getting details for extension ID: {extension_id}")

        extension = chronicle.get_parser_extension(log_type, extension_id)
        print("Extension details:")
        print(f"  Name: {extension.get('name', 'N/A')}")

    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Error getting parser extension details: {e}")


def example_create_parser_extension(chronicle) -> Optional[str]:
    """Example 3: Create a new parser extension.

    Args:
        chronicle: Initialized ChronicleClient instance

    Returns:
        Optional[str]: The ID of the created parser extension,
            or None on failure
    """
    print("\n=== Example 3: Create Parser Extension ===")
    log_type = "OKTA"

    # Sample extension configuration

    try:
        print("Creating new parser extension...")
        result = chronicle.create_parser_extension(
            log_type,
            field_extractors=(
                '{"extractors": [{"preconditionPath": "displayMessage"'
                ',"preconditionValue": "User login to Okta","preconditionOp": '
                '"EQUALS","fieldPath": "displayMessage","destinationPath": '
                '"udm.metadata.description"    }],"logFormat": "JSON",'
                '"appendRepeatedFields": true}'
            ),
        )

        extension_id = result.get("name", "").split("/")[-1]
        print(f"Successfully created parser extension with ID: {extension_id}")
        return extension_id

    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Error creating parser extension: {e}")
        return None


def example_activate_parser_extension(chronicle, extension_id: str) -> None:
    """Example 4: Activate a parser extension.

    Args:
        chronicle: Initialized ChronicleClient instance
        extension_id: The ID of the parser extension to activate
    """
    print("\n=== Example 4: Activate Parser Extension ===")
    log_type = "OKTA"

    try:
        print(f"Activating parser extension with ID: {extension_id}")
        chronicle.activate_parser_extension(log_type, extension_id)
        print("Parser extension activated successfully")

    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Error activating parser extension: {e}")


def example_delete_parser_extension(chronicle, extension_id: str) -> None:
    """Example 5: Delete a parser extension.

    Args:
        chronicle: Initialized ChronicleClient instance
        extension_id: The ID of the parser extension to delete
    """
    print("\n=== Example 5: Delete Parser Extension ===")
    log_type = "OKTA"

    try:
        print(f"Deleting parser extension with ID: {extension_id}")
        chronicle.delete_parser_extension(log_type, extension_id)
        print("Parser extension deleted successfully")

    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Error deleting parser extension: {e}")


# Map of example functions
EXAMPLES = {
    "1": example_list_parser_extensions,
    "2": example_get_parser_extension,
    "3": example_create_parser_extension,
    "4": example_activate_parser_extension,
    "5": example_delete_parser_extension,
}


def main() -> None:
    """Main function to run parser extension examples."""
    parser = argparse.ArgumentParser(
        description="Run Chronicle Parser Extension examples"
    )
    parser.add_argument(
        "--project_id", required=True, help="Google Cloud Project ID"
    )
    parser.add_argument(
        "--customer_id", required=True, help="Chronicle Customer ID (UUID)"
    )
    parser.add_argument(
        "--region", default="us", help="Chronicle region (us or eu)"
    )
    parser.add_argument(
        "--example",
        "-e",
        help=(
            "Example number to run (1-7). If not specified, runs all examples."
        ),
    )

    args = parser.parse_args()

    # Initialize the client
    secops = SecOpsClient()
    chronicle = secops.chronicle(
        customer_id=args.customer_id,
        project_id=args.project_id,
        region=args.region,
    )

    if args.example:
        if args.example not in EXAMPLES:
            print(
                f"Invalid example number. Available examples: "
                f"{', '.join(EXAMPLES.keys())}"
            )
            return
        EXAMPLES[args.example](chronicle)
    else:
        # Create a new extension for the other examples
        extension_id = EXAMPLES["3"](chronicle)
        if not extension_id:
            print("Failed to create parser extension. Stopping examples.")
            return

        # Run the remaining examples that require an extension ID
        EXAMPLES["2"](chronicle, extension_id)
        # Run list
        EXAMPLES["1"](chronicle)
        # Waiting till validation completes
        time.sleep(5)
        EXAMPLES["4"](chronicle, extension_id)
        EXAMPLES["5"](chronicle, extension_id)


if __name__ == "__main__":
    main()
