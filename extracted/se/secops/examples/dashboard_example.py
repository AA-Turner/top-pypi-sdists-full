#!/usr/bin/env python
#
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
"""Example script demonstrating Chronicle Dashboard functionality."""

import argparse
import json
import time
import uuid
from typing import Optional

from secops.chronicle.client import ChronicleClient


def get_client(
    project_id: str, customer_id: str, region: str
) -> ChronicleClient:
    """Initialize and return the Chronicle client.

    Args:
        project_id: Google Cloud Project ID
        customer_id: Chronicle Customer ID (UUID)
        region: Chronicle region (us or eu)

    Returns:
        Chronicle client instance
    """
    return ChronicleClient(
        project_id=project_id, customer_id=customer_id, region=region
    )


def example_create_dashboard(chronicle: ChronicleClient) -> Optional[str]:
    """Create a new dashboard.

    Args:
        chronicle: ChronicleClient instance

    Returns:
        Created dashboard ID if successful, None otherwise
    """
    print("\n=== Create Dashboard ===")

    display_name = f"Test Dashboard - {uuid.uuid4()}"
    description = "A test dashboard created via API example"
    access_type = "PRIVATE"

    try:
        print(f"\nCreating dashboard: {display_name}")
        new_dashboard = chronicle.create_dashboard(
            display_name=display_name,
            description=description,
            access_type=access_type,
        )
        dashboard_id = new_dashboard["name"].split("/")[-1]
        print(f"Created dashboard with ID: {dashboard_id}")
        print(json.dumps(new_dashboard, indent=2))
        return dashboard_id
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Error creating dashboard: {e}")
        return None


def example_get_dashboard(
    chronicle: ChronicleClient, dashboard_id: str
) -> None:
    """Get a specific dashboard by ID.

    Args:
        chronicle: ChronicleClient instance
        dashboard_id: ID of the dashboard to retrieve
    """
    print("\n=== Get Dashboard ===")

    try:
        print(f"\nGetting dashboard with ID: {dashboard_id}")
        dashboard = chronicle.get_dashboard(dashboard_id=dashboard_id)
        print("Dashboard details:")
        print(json.dumps(dashboard, indent=2))
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Error getting dashboard: {e}")


def example_list_dashboards(chronicle: ChronicleClient) -> None:
    """List all available dashboards with pagination.

    Args:
        chronicle: ChronicleClient instance
    """
    print("\n=== List Dashboards ===")

    try:
        print("\nListing dashboards (page 1, size 5):")
        page_size = 5
        dashboards = chronicle.list_dashboards(page_size=page_size)

        # Print first page
        dashboard_list = dashboards.get("nativeDashboards", [])
        print(f"Retrieved {len(dashboard_list)} dashboards")
        for i, dashboard in enumerate(dashboard_list, start=1):
            print(
                f"{i}. {dashboard.get('displayName')} "
                f"(ID: {dashboard.get('name').split('/')[-1]})"
            )

        # Check for pagination
        if "nextPageToken" in dashboards:
            page_token = dashboards["nextPageToken"]
            print("\nListing dashboards (page 2, size 5):")
            next_page = chronicle.list_dashboards(
                page_size=page_size, page_token=page_token
            )
            next_list = next_page.get("nativeDashboards", [])
            for i, dashboard in enumerate(
                next_list, start=len(dashboard_list) + 1
            ):
                print(
                    f"{i}. {dashboard.get('displayName')} "
                    f"(ID: {dashboard.get('name').split('/')[-1]})"
                )
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Error listing dashboards: {e}")


def example_update_dashboard(
    chronicle: ChronicleClient, dashboard_id: str
) -> None:
    """Update an existing dashboard.

    Args:
        chronicle: ChronicleClient instance
        dashboard_id: ID of the dashboard to update
    """
    print("\n=== Update Dashboard ===")

    try:
        # First get current dashboard to preserve values we don't want to change
        current = chronicle.get_dashboard(dashboard_id=dashboard_id)

        # Update display name and description
        updated_name = f"Updated Dashboard - {uuid.uuid4()}"
        updated_description = "This dashboard was updated via API example"

        print(f"\nUpdating dashboard {dashboard_id} to: {updated_name}")
        updated = chronicle.update_dashboard(
            dashboard_id=dashboard_id,
            display_name=updated_name,
            description=updated_description,
        )

        print("Dashboard updated successfully:")
        print(
            f"Name changed: {current.get('displayName')} -> "
            f"{updated.get('displayName')}"
        )
        print(f"Description updated to: {updated.get('description')}")
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Error updating dashboard: {e}")


def example_duplicate_dashboard(
    chronicle: ChronicleClient, dashboard_id: str
) -> Optional[str]:
    """Duplicate an existing dashboard.

    Args:
        chronicle: ChronicleClient instance
        dashboard_id: ID of the dashboard to duplicate

    Returns:
        New dashboard ID if successful, None otherwise
    """
    print("\n=== Duplicate Dashboard ===")

    try:
        duplicate_name = f"Duplicate Dashboard - {uuid.uuid4()}"
        print(f"\nDuplicating dashboard {dashboard_id} to: {duplicate_name}")

        duplicated = chronicle.duplicate_dashboard(
            dashboard_id=dashboard_id,
            display_name=duplicate_name,
            access_type="PRIVATE",
        )

        duplicate_id = duplicated["name"].split("/")[-1]
        print(f"Dashboard duplicated successfully with ID: {duplicate_id}")
        return duplicate_id
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Error duplicating dashboard: {e}")
        return None


def example_export_dashboard(
    chronicle: ChronicleClient, dashboard_ids: list
) -> dict:
    """Export one or more dashboards.

    Args:
        chronicle: ChronicleClient instance
        dashboard_ids: List of dashboard IDs to export

    Returns:
        Dictionary containing exported dashboard data if successful, None otherwise
    """
    print("\n=== Export Dashboard ===")

    try:
        print(f"\nExporting {len(dashboard_ids)} dashboard(s): {dashboard_ids}")
        result = chronicle.export_dashboard(dashboard_ids)
        print("\nDashboard export successful. Result:")
        print(
            "- Total dashboards exported: "
            f'{len(result.get("inlineDestination",{}).get("dashboards", []))}'
        )
        # Print a sample of the exported data
        if result.get("inlineDestination", {}).get("dashboards"):
            print("\nExported dashboard details:")
            for i, dashboard in enumerate(
                result["inlineDestination"]["dashboards"]
            ):
                print(f"\nDashboard {i+1}:")
                print(
                    f"- Name: {dashboard.get('dashboard').get('name', 'N/A')}"
                )
                print(
                    f"- Display Name: {dashboard.get('dashboard').get('displayName', 'N/A')}"
                )
                print(
                    f"- Description: {dashboard.get('dashboard').get('description', 'N/A')}"
                )
                print(
                    f"- Type: {dashboard.get('dashboard').get('type', 'N/A')}"
                )

        print("\nFull export response available in the returned result.")
        return result
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Error exporting dashboard: {e}")
        return None


def example_import_dashboard(chronicle: ChronicleClient) -> str:
    """Import a dashboard from a JSON file.

    Args:
        chronicle: ChronicleClient instance
    Returns:
        New dashboard ID if successful, None otherwise
    """
    print("\n=== Import Dashboard ===")

    import_payload = {
        "dashboard": {
            "name": "50221a9e-afd7-4f7b-8043-35a925454995",
            "displayName": "Source Dashboard 8f736a58",
            "description": "Source dashboard for import test",
            "definition": {
                "filters": [
                    {
                        "id": "GlobalTimeFilter",
                        "dataSource": "GLOBAL",
                        "filterOperatorAndFieldValues": [
                            {
                                "filterOperator": "PAST",
                                "fieldValues": ["1", "DAY"],
                            }
                        ],
                        "displayName": "Global Time Filter",
                        "isStandardTimeRangeFilter": True,
                        "isStandardTimeRangeFilterEnabled": True,
                    }
                ]
            },
            "type": "CUSTOM",
            "etag": "9bcb466d09e461d19aa890d0f5eb38a5496fa085dc2605954e4457b408acd916",
            "access": "DASHBOARD_PRIVATE",
        }
    }

    try:
        print("\nImporting dashboard...")
        result = chronicle.import_dashboard(import_payload)
        print("Dashboard imported successfully:")
        print(json.dumps(result, indent=2))
        if result.get("results"):
            return result.get("results")[0]["dashboard"].split("/")[-1]
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Error importing dashboard: {e}")


def example_add_chart(
    chronicle: ChronicleClient, dashboard_id: str
) -> Optional[dict]:
    """Add a chart to an existing dashboard.

    Args:
        chronicle: ChronicleClient instance
        dashboard_id: ID of the dashboard to add chart to
    """
    print("\n=== Add Chart to Dashboard ===")

    try:
        chart_name = f"Example Chart - {uuid.uuid4()}"

        # Sample chart query
        query = """
        metadata.event_type = "NETWORK_DNS"
        match:
        principal.hostname
        outcome:
        $dns_query_count = count(metadata.id)
        order:
        principal.hostname asc
        """

        # Chart layout and configuration
        chart_layout = {"startX": 0, "spanX": 12, "startY": 0, "spanY": 8}

        chart_datasource = {"dataSources": ["UDM"]}

        interval = {"relativeTime": {"timeUnit": "DAY", "startTimeVal": "1"}}

        print(f"\nAdding chart '{chart_name}' to dashboard {dashboard_id}")
        result = chronicle.add_chart(
            dashboard_id=dashboard_id,
            display_name=chart_name,
            chart_layout=chart_layout,
            query=query,
            chart_datasource=chart_datasource,
            interval=interval,
        )

        print("Chart added successfully:")
        print(json.dumps(result, indent=2))
        return result

    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Error adding chart to dashboard: {e}")


def example_get_chart(
    chronicle: ChronicleClient, chart_id: str
) -> Optional[dict]:
    """Get details of a specific chart.

    Args:
        chronicle: ChronicleClient instance
        chart_id: ID of the chart to retrieve
    """
    print("\n=== Get Dashboard Chart Details ===")

    try:
        chart_details = chronicle.get_chart(chart_id=chart_id)

        print("\nChart details:")
        print(f"- Name: {chart_details.get('name')}")
        print(f"- Display Name: {chart_details.get('displayName')}")
        print(f"- Description: {chart_details.get('description', 'N/A')}")
        print(f"- ETag: {chart_details.get('etag')}")

        print("\nFull chart details:")
        print(json.dumps(chart_details, indent=2))

        return chart_details
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Error getting chart details: {e}")
        return None


def example_edit_chart(
    chronicle: ChronicleClient, dashboard_id: str, chart_id: str
) -> None:
    """Edit an existing chart in a dashboard.

    Args:
        chronicle: ChronicleClient instance
        dashboard_id: ID of the dashboard containing the chart
        chart_id: ID of the chart to edit
    """
    print("\n=== Edit Dashboard Chart ===")

    try:
        # First get the chart details to obtain the etag
        chart_details = chronicle.get_chart(chart_id=chart_id)
        if not chart_details:
            print("Could not retrieve chart details for editing")
            return

        # Prepare the updated chart details
        updated_chart_name = f"Updated Chart {uuid.uuid4()}"

        updated_dashboard_chart = {
            "name": chart_details["name"],
            "displayName": updated_chart_name,
            "description": "This chart was updated by the example script",
            "etag": chart_details["etag"],
        }

        print(f"\nUpdating chart with new name: {updated_chart_name}")

        # Edit the chart
        result = chronicle.edit_chart(
            dashboard_id=dashboard_id,
            dashboard_chart=updated_dashboard_chart,
        )

        print("\nChart updated successfully!")
        print(f"- Updated Name: {result['dashboardChart']['displayName']}")
        print(f"- Updated ETag: {result['dashboardChart']['etag']}")

    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Error editing chart: {e}")


def example_remove_chart(
    chronicle: ChronicleClient, dashboard_id: str, chart_id: str
) -> None:
    """Remove a chart from a dashboard.

    Args:
        chronicle: ChronicleClient instance
        dashboard_id: ID of the dashboard containing the chart
        chart_id: ID of the chart to remove
    """
    print("\n=== Remove Dashboard Chart ===")

    try:
        print(f"\nDeleting chart with ID: {chart_id}")
        chronicle.remove_chart(dashboard_id=dashboard_id, chart_id=chart_id)
        print("Chart removed successfully")
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Error deleting chart: {e}")


def example_delete_dashboard(
    chronicle: ChronicleClient, dashboard_id: str
) -> None:
    """Delete a dashboard.

    Args:
        chronicle: ChronicleClient instance
        dashboard_id: ID of the dashboard to delete
    """
    print("\n=== Delete Dashboard ===")

    try:
        print(f"\nDeleting dashboard with ID: {dashboard_id}")
        chronicle.delete_dashboard(dashboard_id=dashboard_id)
        print("Dashboard deleted successfully")
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Error deleting dashboard: {e}")


def example_execute_dashboard_query(chronicle: ChronicleClient) -> None:
    """Execute a dashboard query.

    Args:
        chronicle: ChronicleClient instance
    """
    print("\n=== Execute Dashboard Query ===")

    try:
        # Sample query
        query = """
        metadata.event_type = "USER_LOGIN"
        match:
        principal.user.userid
        outcome:
        $logon_count = count(metadata.id)
        order:
        $logon_count desc
        limit: 10
        """

        interval = {"relativeTime": {"timeUnit": "DAY", "startTimeVal": "1"}}

        print("\nExecuting dashboard query:")
        print(query)

        result = chronicle.execute_dashboard_query(
            query=query,
            interval=interval,
        )

        print("\nQuery results:")
        if "results" in result and result["results"]:
            # Display the first few results
            for i, item in enumerate(result["results"][:3], start=1):
                print(f"Result {i}:")
                print(json.dumps(item, indent=2))
            print(f"... (total: {len(result['results'])} results)")
        else:
            print("No results returned")
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Error executing dashboard query: {e}")


def example_get_dashboard_query(
    chronicle: ChronicleClient, query_id: str
) -> Optional[dict]:
    """Get a dashboard query.

    Args:
        chronicle: ChronicleClient instance
        query_id: Dashboard query ID

    Returns:
        Dashboard query details as a dictionary, or None if not found
    """
    print("\n=== Get Dashboard Query ===")

    try:
        print(f"\nGetting dashboard query: {query_id}")

        result = chronicle.get_dashboard_query(query_id=query_id)

        if result:
            print("\nQuery details:")
            print(json.dumps(result, indent=2))
        else:
            print("Dashboard query not found")
        return result
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Error getting dashboard query: {e}")
        return None


# Map of example functions
EXAMPLES = {
    "1": example_create_dashboard,
    "2": example_get_dashboard,
    "3": example_list_dashboards,
    "4": example_update_dashboard,
    "5": example_duplicate_dashboard,
    "6": example_delete_dashboard,
    "7": example_add_chart,
    "8": example_get_chart,
    "9": example_edit_chart,
    "10": example_remove_chart,
    "11": example_execute_dashboard_query,
    "12": example_get_dashboard_query,
    "13": example_import_dashboard,
    "14": example_export_dashboard,
}


def main() -> None:
    """Main function to run examples."""
    parser = argparse.ArgumentParser(
        description="Run Chronicle Dashboard API examples"
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
            "Example number to run (1-14). "
            "1: Create Dashboard, "
            "2: Get Dashboard, "
            "3: List Dashboards, "
            "4: Update Dashboard, "
            "5: Duplicate Dashboard, "
            "6: Delete Dashboard, "
            "7: Add Chart, "
            "8: Get Chart, "
            "9: Edit Chart, "
            "10: Delete Chart, "
            "11: Execute Dashboard Query, "
            "12: Get Dashboard Query, "
            "13: Import Dashboard, "
            "14: Export Dashboard, "
            "0: Run All Examples"
        ),
    )
    parser.add_argument(
        "--dashboard_id", help="Dashboard ID for examples requiring a dashboard"
    )
    parser.add_argument(
        "--chart_id", help="Chart ID for examples requiring a chart"
    )
    parser.add_argument(
        "--query_id", help="Query ID for examples requiring a query"
    )

    args = parser.parse_args()

    # Initialize the Chronicle client
    chronicle = get_client(
        project_id=args.project_id,
        customer_id=args.customer_id,
        region=args.region,
    )

    dashboard_ids = []
    chart_id = args.chart_id

    try:
        if args.example == "1":
            # Create Dashboard example
            created_dash = example_create_dashboard(chronicle)
            if created_dash:
                dashboard_ids.append(created_dash)

        elif args.example == "2":
            # Get Dashboard example
            if not args.dashboard_id:
                print("Error: dashboard_id is required for this example")
                return
            example_get_dashboard(chronicle, args.dashboard_id)

        elif args.example == "3":
            # List Dashboards example
            example_list_dashboards(chronicle)

        elif args.example == "4":
            # Update Dashboard example
            if not args.dashboard_id:
                print("Error: dashboard_id is required for this example")
                return
            example_update_dashboard(chronicle, args.dashboard_id)

        elif args.example == "5":
            # Duplicate Dashboard example
            if not args.dashboard_id:
                print("Error: dashboard_id is required for this example")
                return
            duplicated = example_duplicate_dashboard(
                chronicle, args.dashboard_id
            )
            if duplicated:
                dashboard_ids.append(duplicated)

        elif args.example == "6":
            # Delete Dashboard example
            if not args.dashboard_id:
                print("Error: dashboard_id is required for this example")
                return
            example_delete_dashboard(chronicle, args.dashboard_id)

        elif args.example == "7":
            # Add Chart example
            if not args.dashboard_id:
                print("Error: dashboard_id is required for this example")
                return
            result = example_add_chart(chronicle, args.dashboard_id)
            if result and "dashboardChart" in result:
                chart_id = result["dashboardChart"]["name"].split("/")[-1]
                print(f"Created chart ID: {chart_id}")

        elif args.example == "8":
            # Get Chart example
            if not args.chart_id:
                print("Error: chart_id is required for this example")
                return
            example_get_chart(chronicle, args.chart_id)

        elif args.example == "9":
            # Edit Chart example
            if not args.dashboard_id or not args.chart_id:
                print(
                    "Error: dashboard_id and chart_id "
                    "are required for this example"
                )
                return
            example_edit_chart(chronicle, args.dashboard_id, args.chart_id)

        elif args.example == "10":
            # Delete Chart example
            if not args.dashboard_id or not args.chart_id:
                print(
                    "Error: dashboard_id and chart_id are "
                    "required for this example"
                )
                return
            example_remove_chart(chronicle, args.dashboard_id, args.chart_id)

        elif args.example == "11":
            # Execute Dashboard Query example
            example_execute_dashboard_query(chronicle)

        elif args.example == "12":
            # Get Dashboard Query example
            if not args.query_id:
                print("Error: query_id is required for this example")
                return
            example_get_dashboard_query(chronicle, args.query_id)

        elif args.example == "13":
            # Import Dashboard example
            new_dashboard_id = example_import_dashboard(chronicle)

            if new_dashboard_id:
                # Add new dashboard Id for Cleanup
                dashboard_ids.append(new_dashboard_id)

        elif args.example == "14":
            # Export Dashboard example
            if not args.dashboard_id:
                print(
                    "Error: At least one dashboard_id is required for this example"
                )
                return

            # Convert single dashboard_id to list or split comma-separated values
            dashboard_ids_to_export = []
            if "," in args.dashboard_id:
                dashboard_ids_to_export = args.dashboard_id.split(",")
            else:
                dashboard_ids_to_export = [args.dashboard_id]

            example_export_dashboard(chronicle, dashboard_ids_to_export)

        elif args.example == "0" or not args.example:
            # Run all examples (create workflow)
            print("=== Running All Examples ===")

            # Create a dashboard
            dashboard_id = example_create_dashboard(chronicle)
            if not dashboard_id:
                print("Failed to create dashboard, stopping examples")
                return

            dashboard_ids.append(dashboard_id)

            # Get dashboard details
            example_get_dashboard(chronicle, dashboard_id)
            time.sleep(1)

            # List dashboards
            example_list_dashboards(chronicle)
            time.sleep(1)

            # Update dashboard
            example_update_dashboard(chronicle, dashboard_id)
            time.sleep(1)

            # Add chart to dashboard
            chart_result = example_add_chart(chronicle, dashboard_id)
            if chart_result:
                chart_id = chart_result["dashboardChart"]["name"].split("/")[-1]
                print(f"Created chart ID: {chart_id}")
                time.sleep(2)  # Wait for chart to be fully created

                # Get chart details

                chart_details = example_get_chart(chronicle, chart_id)
                time.sleep(1)

                # Edit chart
                example_edit_chart(chronicle, dashboard_id, chart_id)
                time.sleep(1)

                query_id = chart_details["chartDatasource"][
                    "dashboardQuery"
                ].split("/")[-1]
                example_get_dashboard_query(chronicle, query_id)

                # Delete chart
                example_remove_chart(chronicle, dashboard_id, chart_id)
                time.sleep(1)

            # Duplicate dashboard
            duplicated = example_duplicate_dashboard(chronicle, dashboard_id)
            if duplicated:
                dashboard_ids.append(duplicated)

            example_execute_dashboard_query(chronicle)

            # Import dashboard
            imported_dashboard_id = example_import_dashboard(chronicle)
            if imported_dashboard_id:
                dashboard_ids.append(imported_dashboard_id)

            # Export dashboards
            if dashboard_ids:
                example_export_dashboard(chronicle, [imported_dashboard_id])

    finally:
        # Clean up all created dashboards
        print("\n=== Cleaning up resources ===")
        for dash_id in dashboard_ids:
            try:
                example_delete_dashboard(chronicle, dash_id)
            except Exception as e:  # pylint: disable=broad-exception-caught
                print(f"Error during cleanup of dashboard {dash_id}: {e}")


if __name__ == "__main__":
    main()
