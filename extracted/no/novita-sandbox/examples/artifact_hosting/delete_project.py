#!/usr/bin/env python3
"""
Delete project

Configure environment variables before use:
- NOVITA_API_KEY: Novita API Key

Usage:
    cd sdk-python/examples/artifact_hosting
    python delete_project.py -p my-project-name
    python delete_project.py -p my-project-name -y  # Skip confirmation
"""

import argparse
import os
import sys
from pathlib import Path

import dotenv

dotenv.load_dotenv()

# Add SDK to Python path (development environment)
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from novita_sandbox.artifact_hosting import DeploymentClient


# API Configuration (URL is fixed in SDK: https://artifact.novita.ai/v1)
API_KEY = os.environ.get("NOVITA_API_KEY")


def main():
    parser = argparse.ArgumentParser(description="Delete project")
    parser.add_argument("-p", "--project", required=True, help="Project name")
    parser.add_argument("-y", "--yes", action="store_true", help="Skip confirmation")
    args = parser.parse_args()

    project_name = args.project

    if not API_KEY:
        print("❌ Please set NOVITA_API_KEY environment variable")
        sys.exit(1)

    print(f"📦 Project name: {project_name}")
    print()

    with DeploymentClient(api_key=API_KEY) as client:
        # Find project
        print("🔍 Looking for project...")
        project = None

        for p in client.list_projects():
            if p.name == project_name:
                project = p
                break

        if project is None:
            print(f"❌ Project not found: {project_name}")
            sys.exit(1)

        print(f"✅ Found project: {project.id}")
        print(f"   Name: {project.name}")
        print(f"   Status: {project.status.name}")
        print(f"   Deployment count: {project.deployment_count}")
        if project.url:
            print(f"   URL: {project.url}")
        print()

        # Confirm deletion
        if not args.yes:
            confirm = input("⚠️  Confirm deletion of this project? (y/N): ")
            if confirm.lower() != "y":
                print("❌ Cancelled")
                sys.exit(0)

        # Delete project
        print("🗑️  Deleting project...")
        try:
            client.delete_project(project.id)
            print("✅ Project deleted")
        except Exception as e:
            print(f"❌ Deletion failed: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
