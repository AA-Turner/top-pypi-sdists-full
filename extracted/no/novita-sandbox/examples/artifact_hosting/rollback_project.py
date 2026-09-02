#!/usr/bin/env python3
"""
Rollback a project to a specific deployment version.

Prerequisites:
    Configure environment variables:
    - NOVITA_API_KEY: Novita API Key

Usage:
    cd sdk-python/examples/artifact_hosting
    python rollback_project.py -p <project_id> -d <deployment_id> [-r <reason>]

Examples:
    # Rollback to a specific deployment
    python rollback_project.py -p b1edeec5-07e5-4cb2-be92-ca02d5a367c3 -d abc123

    # List deployments first to find a target
    python rollback_project.py -p b1edeec5-07e5-4cb2-be92-ca02d5a367c3 --list
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


def list_deployments(client: DeploymentClient, project_id: str):
    """List all deployments for a project."""
    print(f"\n📋 Deployments for project: {project_id}")
    print("-" * 70)
    
    project = client.get_project(project_id)
    current_deployment_id = project.current_deployment_id
    
    for dep in project.list_deployments():
        is_current = "👈 CURRENT" if dep.id == current_deployment_id else ""
        print(f"  {dep.id}  [{dep.status.name:15}]  {dep.created_at.strftime('%Y-%m-%d %H:%M:%S')}  {is_current}")
    
    print("-" * 70)
    print()


def main():
    parser = argparse.ArgumentParser(description="Rollback a project to a specific deployment")
    parser.add_argument("-p", "--project", required=True, help="Project ID")
    parser.add_argument("-d", "--deployment", help="Target deployment ID to rollback to")
    parser.add_argument("-r", "--reason", help="Reason for rollback")
    parser.add_argument("--list", action="store_true", help="List all deployments for the project")
    parser.add_argument("-y", "--yes", action="store_true", help="Skip confirmation")
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

    print("=" * 60)
    print("🔄 Project Rollback Tool")
    print("=" * 60)
    print(f"📦 Project ID: {args.project}")
    print()

    with DeploymentClient(api_key=API_KEY) as client:
        # List mode
        if args.list:
            list_deployments(client, args.project)
            return

        # Rollback mode requires deployment ID
        if not args.deployment:
            print("❌ Please specify target deployment ID with -d/--deployment")
            print("   Use --list to see available deployments")
            sys.exit(1)

        # Get project and current deployment info
        project = client.get_project(args.project)
        print(f"📦 Project: {project.name}")
        print(f"   Current deployment: {project.current_deployment_id}")
        print(f"   Target deployment:  {args.deployment}")
        
        if args.reason:
            print(f"   Reason: {args.reason}")
        print()

        # Check if target is already current
        if project.current_deployment_id == args.deployment:
            print("⚠️  Target deployment is already the current deployment")
            sys.exit(0)

        # Confirmation
        if not args.yes:
            confirm = input("⚠️  Confirm rollback? (y/N): ")
            if confirm.lower() != 'y':
                print("❌ Cancelled")
                sys.exit(0)

        # Perform rollback
        print("🔄 Rolling back...")
        try:
            result = project.rollback(
                target_deployment_id=args.deployment,
                reason=args.reason,
            )
            
            print()
            print("=" * 60)
            print("✅ Rollback successful!")
            print("=" * 60)
            print(f"   Project ID:              {result['project_id']}")
            print(f"   Previous deployment:     {result['previous_deployment_id']}")
            print(f"   Current deployment:      {result['current_deployment_id']}")
            print()

            # Get updated project info
            project = client.get_project(args.project)
            if project.endpoint and project.endpoint.default_url:
                print("📱 Access application:")
                print(f"   {project.endpoint.default_url}")

        except Exception as e:
            print(f"❌ Rollback failed: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
