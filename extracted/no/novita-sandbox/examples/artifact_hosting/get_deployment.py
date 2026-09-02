#!/usr/bin/env python3
"""
Get deployment details and status within a project.

Prerequisites:
    Configure environment variables:
    - NOVITA_API_KEY: Novita API Key

Usage:
    cd sdk-python/examples/artifact_hosting
    python get_deployment.py -p <project_id> -d <deployment_id>
    python get_deployment.py -p <project_id> -d <deployment_id> --logs  # Stream deployment logs
"""

import argparse
import logging
import os
import sys
from pathlib import Path

import dotenv

# Load .env file
dotenv.load_dotenv(Path(__file__).parent / ".env")

# Add SDK to Python path (development environment)
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from novita_sandbox.artifact_hosting import DeploymentClient


# API Configuration (URL is fixed in SDK: https://artifact.novita.ai/v1)
API_KEY = os.environ.get("NOVITA_API_KEY")


def main():
    parser = argparse.ArgumentParser(description="Get deployment details within a project")
    parser.add_argument("-p", "--project", required=True, help="Project ID")
    parser.add_argument("-d", "--deployment", required=True, help="Deployment ID")
    parser.add_argument("--logs", action="store_true", help="Stream deployment logs")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
    args = parser.parse_args()

    # Configure logging
    if args.verbose:
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

    # Validate configuration
    if not API_KEY:
        print("❌ Please set NOVITA_API_KEY environment variable")
        sys.exit(1)

    with DeploymentClient(api_key=API_KEY) as client:
        try:
            project = client.get_project(args.project)
        except Exception as e:
            print(f"❌ Failed to get project: {e}")
            sys.exit(1)

        try:
            deployment = project.get_deployment(args.deployment)
        except Exception as e:
            print(f"❌ Failed to get deployment: {e}")
            sys.exit(1)

        is_current = deployment.id == project.current_deployment_id

        print()
        print("=" * 70)
        print("🚀 Deployment Details")
        print("=" * 70)
        print(f"  ID:                  {deployment.id}")
        print(f"  Project ID:          {deployment.project_id}")
        print(f"  Status:              {deployment.status.name}")
        print(f"  Is Current:          {'✅ Yes' if is_current else '❌ No'}")
        print(f"  Message:             {deployment.message or '-'}")
        if deployment.error_message:
            print(f"  Error:               {deployment.error_message}")
        print()
        print("📦 Artifacts Source")
        print("-" * 70)
        print(f"  Sandbox ID:          {deployment.artifacts_source.sandbox_id}")
        print(f"  Path:                {deployment.artifacts_source.path}")
        print()
        print("⚙️  Configuration")
        print("-" * 70)
        print(f"  HTTP Port:           {deployment.http_port}")
        print(f"  Health Check Path:   {deployment.metadata.check_health_path or '-'}")
        print(f"  CPU:                 {deployment.cpu}")
        print(f"  Memory:              {deployment.memory}")
        print(f"  Min Replicas:        {deployment.min_replicas}")
        print(f"  Max Replicas:        {deployment.max_replicas}")
        print()
        if deployment.environment_variables:
            print("🔑 Environment Variables")
            print("-" * 70)
            for key, value in deployment.environment_variables.items():
                # Mask sensitive values
                masked = value[:4] + "****" if len(value) > 4 else "****"
                print(f"  {key:20s} = {masked}")
            print()
        print("📅 Timestamps")
        print("-" * 70)
        print(f"  Created:             {deployment.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        print("👤 Account Info")
        print("-" * 70)
        print(f"  Account ID:          {deployment.account_info.account_id}")
        print(f"  Team ID:             {deployment.account_info.team_id or '-'}")
        print(f"  Member ID:           {deployment.account_info.member_id or '-'}")
        print("=" * 70)

        # Stream logs if requested
        if args.logs:
            print()
            print("📋 Deployment Logs")
            print("-" * 70)

            try:
                count = 0
                for log_entry in deployment.stream_logs():
                    print(f"  {log_entry.message}")
                    count += 1

                if count == 0:
                    print("  (No logs available)")
            except KeyboardInterrupt:
                print()
                print("  (Log streaming interrupted)")
            except Exception as e:
                print(f"  ❌ Failed to stream logs: {e}")

            print("-" * 70)

        print()


if __name__ == "__main__":
    main()
