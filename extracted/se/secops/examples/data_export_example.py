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
"""Example script for demonstrating Chronicle Data Export API functionality."""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from time import sleep
from secops import SecOpsClient
from secops.exceptions import APIError


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Chronicle Data Export API Example")
    parser.add_argument("--project_id", required=True, help="GCP project ID")
    parser.add_argument("--customer_id", required=True, help="Chronicle customer ID")
    parser.add_argument("--region", default="us", help="Chronicle region (default: us)")
    parser.add_argument("--bucket", help="GCS bucket name for export")
    parser.add_argument(
        "--days", type=int, default=1, help="Number of days to look back (default: 1)"
    )
    parser.add_argument("--log_type", help="Single log type to export (deprecated)")
    parser.add_argument(
        "--log_types",
        help="Comma-separated list of log types to export (e.g., WINDOWS,LINUX)"
    )
    parser.add_argument("--all_logs", action="store_true", help="Export all log types")
    parser.add_argument(
        "--list_only",
        action="store_true",
        help="Only list available log types, don't create export",
    )
    parser.add_argument("--credentials", help="Path to service account JSON key file")
    
    # Additional options for demonstrating list/update functionality
    parser.add_argument(
        "--list_exports", 
        action="store_true",
        help="List recent data exports"
    )
    parser.add_argument(
        "--list_count", 
        type=int, 
        default=5,
        help="Number of exports to list when using --list_exports"
    )
    parser.add_argument(
        "--update",
        help="Update an existing export with the given ID (must be in IN_QUEUE state)"
    )
    parser.add_argument(
        "--new_bucket",
        help="New bucket name when updating an export"
    )
    parser.add_argument(
        "--new_log_types",
        help="New comma-separated list of log types when updating an export"
    )

    return parser.parse_args()


def main():
    """Run the example."""
    args = parse_args()

    # Set up time range for export
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=args.days)

    print(f"Time range: {start_time.isoformat()} to {end_time.isoformat()}")

    # Initialize the client
    if args.credentials:
        print(f"Using service account credentials from {args.credentials}")
        client = SecOpsClient(service_account_path=args.credentials)
    else:
        print("Using application default credentials")
        client = SecOpsClient()

    # Get Chronicle client
    chronicle = client.chronicle(
        customer_id=args.customer_id, project_id=args.project_id, region=args.region
    )

    try:
        # Check if we should just list exports
        if args.list_exports:
            print("\nListing recent data exports...")
            list_result = chronicle.list_data_export(page_size=args.list_count)
            exports = list_result.get("dataExports", [])
            print(f"Found {len(exports)} exports")
            
            for i, export_item in enumerate(exports, 1):
                export_id = export_item["name"].split("/")[-1]
                stage = export_item["dataExportStatus"]["stage"]
                start = export_item.get("startTime", "N/A")
                end = export_item.get("endTime", "N/A")
                
                print(f"\n{i}. Export ID: {export_id}")
                print(f"   Status: {stage}")
                print(f"   Time range: {start} to {end}")
                print(f"   GCS Bucket: {export_item.get('gcsBucket', 'N/A')}")
                
                # Get the log types
                log_types = export_item.get("includeLogTypes", [])
                if log_types:
                    log_type_names = [lt.split("/")[-1] for lt in log_types[:3]]
                    if len(log_types) <= 3:
                        print(f"   Log types: {', '.join(log_type_names)}")
                    else:
                        print(f"   Log types: {', '.join(log_type_names)} and {len(log_types) - 3} more")
                        
            if "nextPageToken" in list_result:
                print(f"\nNext page token: {list_result['nextPageToken']}")
            
            return 0
            
        # Handle update command if specified
        if args.update:
            print(f"\nUpdating export ID: {args.update}")
            
            # Get current status to verify it's in queue state
            status = chronicle.get_data_export(args.update)
            stage = status["dataExportStatus"]["stage"]
            
            if stage != "IN_QUEUE":
                print(f"Cannot update export: current status is {stage} but must be IN_QUEUE")
                return 1
                
            update_params = {"data_export_id": args.update}
            updated = False
            
            # Add GCS bucket if provided
            if args.new_bucket:
                new_gcs_bucket = f"projects/{args.project_id}/buckets/{args.new_bucket}"
                update_params["gcs_bucket"] = new_gcs_bucket
                print(f"Setting new GCS bucket: {new_gcs_bucket}")
                updated = True
                
            # Add log types if provided
            if args.new_log_types:
                new_log_types_list = [lt.strip() for lt in args.new_log_types.split(',')]
                update_params["log_types"] = new_log_types_list
                print(f"Setting new log types: {', '.join(new_log_types_list)}")
                updated = True
                
            if not updated:
                print("No update parameters provided. Use --new_bucket or --new_log_types")
                return 1
                
            # Perform the update
            result = chronicle.update_data_export(**update_params)
            print("\nExport updated successfully!")
            print(f"Status: {result['dataExportStatus']['stage']}")
            
            return 0
            
        # Fetch available log types for regular create flow
        print("\nFetching available log types for export...")
        result = chronicle.fetch_available_log_types(
            start_time=start_time, end_time=end_time
        )

        log_types = result["available_log_types"]
        print(f"Found {len(log_types)} available log types for export")

        # Print available log types
        for i, log_type in enumerate(log_types[:10], 1):  # Show first 10
            short_name = log_type.log_type.split("/")[-1]
            print(f"{i}. {log_type.display_name} ({short_name})")
            print(f"   Available from {log_type.start_time} to {log_type.end_time}")

        if len(log_types) > 10:
            print(f"... and {len(log_types) - 10} more")

        # If list_only flag is set, exit here
        if args.list_only:
            print("\nList-only mode, not creating export")
            return 0

        # Validate export options
        option_count = sum([bool(args.all_logs), bool(args.log_type), bool(args.log_types)])
        
        if option_count > 1:
            print("Error: Can only specify one of: --all_logs, --log_type, or --log_types")
            return 1
            
        if option_count == 0:
            print("Error: Must specify one of: --all_logs, --log_type, or --log_types")
            return 1

        if not hasattr(args, "bucket") or not args.bucket:
            print("Error: Must specify a GCS bucket name")
            return 1
        # Format GCS bucket path
        gcs_bucket = f"projects/{args.project_id}/buckets/{args.bucket}"
        print(f"\nExporting to GCS bucket: {gcs_bucket}")

        # Create data export
        if args.log_type:
            # Find the matching log type to verify it exists
            matching_log_types = [
                lt for lt in log_types if lt.log_type.split("/")[-1] == args.log_type
            ]
            if not matching_log_types:
                print(
                    f"Warning: Log type '{args.log_type}' not found in available log types"
                )
                print("Available log types include:")
                for i, lt in enumerate(log_types[:5], 1):
                    print(f"  {lt.log_type.split('/')[-1]}")
                proceed = input("Proceed anyway? (y/n): ")
                if proceed.lower() != "y":
                    return 1

            print(f"Creating data export for log type: {args.log_type}")
            export = chronicle.create_data_export(
                gcs_bucket=gcs_bucket,
                start_time=start_time,
                end_time=end_time,
                log_type=args.log_type,
            )
        elif args.log_types:
            # Parse and validate comma-separated log types
            log_types_list = [lt.strip() for lt in args.log_types.split(',')]
            print(f"Creating data export for log types: {', '.join(log_types_list)}")
            
            # Create export with multiple log types
            export = chronicle.create_data_export(
                gcs_bucket=gcs_bucket,
                start_time=start_time,
                end_time=end_time,
                log_types=log_types_list,
            )
        else:
            print("Creating data export for ALL log types")
            export = chronicle.create_data_export(
                gcs_bucket=gcs_bucket,
                start_time=start_time,
                end_time=end_time,
                export_all_logs=True,
            )

        # Get the export ID and print details
        export_id = export["name"].split("/")[-1]
        print(f"\nExport created successfully!")
        print(f"Export ID: {export_id}")
        
        if "dataExportStatus" in export:
            print(f"Status: {export['dataExportStatus']['stage']}")
        else:
            print(f"Status: {export['data_export_status']['stage']}")

        # Poll for status a few times to show progress
        print("\nChecking export status:")

        for i in range(3):
            status = chronicle.get_data_export(export_id)
            
            if "dataExportStatus" in status:
                stage = status["dataExportStatus"]["stage"]
                progress = status["dataExportStatus"].get("progressPercentage", 0)
            else:
                stage = status["data_export_status"]["stage"]
                progress = status["data_export_status"].get("progress_percentage", 0)

            print(f"  Status: {stage}, Progress: {progress}%")

            if stage in ["FINISHED_SUCCESS", "FINISHED_FAILURE", "CANCELLED"]:
                break

            if i < 2:  # Don't wait after the last check
                print("  Waiting 5 seconds...")
                sleep(5)

        print("\nExport job is running. You can check its status or manage it with:")
        print(f"  # Check Status:")
        print(f"  python export_status.py --export_id {export_id} ...")
        print(f"  # List all exports:")
        print(f"  python data_export_example.py --project_id={args.project_id} --customer_id={args.customer_id} --list_exports")
        print(f"  \n  # Update the export if still in queue:")
        print(f"  python data_export_example.py --project_id={args.project_id} --customer_id={args.customer_id} --bucket={args.bucket} --update={export_id} --new_log_types=WINDOWS,LINUX")

        return 0

    except APIError as e:
        print(f"Error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
