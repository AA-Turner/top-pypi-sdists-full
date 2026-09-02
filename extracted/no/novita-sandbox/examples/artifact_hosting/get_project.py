#!/usr/bin/env python3
"""
Get project details and status.

Prerequisites:
    Configure environment variables:
    - NOVITA_API_KEY: Novita API Key

Usage:
    cd sdk-python/examples/artifact_hosting
    python get_project.py -p <project_id>
    python get_project.py -p <project_id> --deployments  # Include deployment history
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
    parser = argparse.ArgumentParser(description="Get project details and status")
    parser.add_argument("-p", "--project", required=True, help="Project ID")
    parser.add_argument("--deployments", action="store_true", help="Show deployment history")
    parser.add_argument("-n", "--limit", type=int, default=10, help="Max deployments to show (default: 10)")
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

        print()
        print("=" * 70)
        print("📦 Project Details")
        print("=" * 70)
        print(f"  ID:                  {project.id}")
        print(f"  Name:                {project.name}")
        print(f"  Description:         {project.description or '-'}")
        print(f"  Status:              {project.status.name}")
        print()
        print("🔗 Endpoint")
        print("-" * 70)
        if project.endpoint:
            print(f"  Default URL:         {project.endpoint.default_url or '-'}")
            print(f"  Custom URL:          {project.endpoint.custom_url or '-'}")
        else:
            print("  (No endpoint configured)")
        print()
        print("📊 Deployment Info")
        print("-" * 70)
        print(f"  Current Deployment:  {project.current_deployment_id or '-'}")
        print(f"  Total Deployments:   {project.deployment_count}")
        print()
        print("📅 Timestamps")
        print("-" * 70)
        print(f"  Created:             {project.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  Updated:             {project.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        print("👤 Account Info")
        print("-" * 70)
        print(f"  Account ID:          {project.account_info.account_id}")
        print(f"  Team ID:             {project.account_info.team_id or '-'}")
        print(f"  Member ID:           {project.account_info.member_id or '-'}")
        print("=" * 70)

        # Show deployment history if requested
        if args.deployments:
            print()
            print("📋 Deployment History")
            print("-" * 70)
            
            count = 0
            for dep in project.list_deployments():
                if count >= args.limit:
                    print(f"  ... (showing {args.limit} of {project.deployment_count})")
                    break
                    
                is_current = "👈 CURRENT" if dep.id == project.current_deployment_id else ""
                print(f"  {dep.id}")
                print(f"    Status:   {dep.status.name:15} {is_current}")
                print(f"    Message:  {dep.message or '-'}")
                print(f"    Created:  {dep.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
                if dep.error_message:
                    print(f"    Error:    {dep.error_message}")
                print()
                count += 1
            
            if count == 0:
                print("  (No deployments)")
            print("-" * 70)

        print()


if __name__ == "__main__":
    main()
