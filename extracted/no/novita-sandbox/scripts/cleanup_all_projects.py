#!/usr/bin/env python3
"""Clean up all projects in the account.

Usage:
    python scripts/cleanup_all_projects.py [--dry-run]

Options:
    --dry-run  Only list projects, don't delete
"""

import os
import sys
import argparse
import dotenv
from pathlib import Path

dotenv.load_dotenv()

# Add src to path for local development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from novita_sandbox.artifact_hosting import DeploymentClient


def delete_all_deployments(project) -> tuple[int, int]:
    """Delete all deployments for a project.
    
    Returns:
        Tuple of (deleted_count, failed_count)
    """
    deleted = 0
    failed = 0
    
    try:
        deployments = list(project.list_deployments())
        if not deployments:
            return 0, 0
        
        print(f"    Found {len(deployments)} deployment(s), deleting...")
        for dep in deployments:
            try:
                dep.delete()
                print(f"      Deleted deployment: {dep.id} ✓")
                deleted += 1
            except Exception as e:
                print(f"      Failed to delete deployment {dep.id}: {e}")
                failed += 1
    except Exception as e:
        print(f"    Failed to list deployments: {e}")
    
    return deleted, failed


def main():
    parser = argparse.ArgumentParser(description="Clean up all projects")
    parser.add_argument("--dry-run", action="store_true", help="Only list projects, don't delete")
    args = parser.parse_args()
    
    # Get API key from environment
    api_key = os.getenv("NOVITA_API_KEY")
    
    if not api_key:
        print("Error: NOVITA_API_KEY environment variable not set")
        sys.exit(1)
    
    print("Connecting to: https://artifact.novita.ai/v1")
    client = DeploymentClient(api_key=api_key)
    
    # List all projects
    print("\nListing all projects...")
    projects = list(client.list_projects())
    
    if not projects:
        print("No projects found.")
        return
    
    print(f"\nFound {len(projects)} project(s):\n")
    for p in projects:
        print(f"  - {p.id}: {p.name} (deployments: {p.deployment_count})")
    
    if args.dry_run:
        print("\n[DRY RUN] No projects were deleted.")
        return
    
    # Confirm deletion
    print(f"\n⚠️  This will delete ALL {len(projects)} projects and their deployments!")
    confirm = input("Type 'yes' to confirm: ")
    
    if confirm.lower() != "yes":
        print("Aborted.")
        return
    
    # Delete all projects
    print("\nDeleting projects...")
    projects_deleted = 0
    projects_failed = 0
    total_deployments_deleted = 0
    total_deployments_failed = 0
    
    for p in projects:
        print(f"  Processing {p.id} ({p.name})...")
        
        # First delete all deployments
        if p.deployment_count > 0:
            dep_deleted, dep_failed = delete_all_deployments(p)
            total_deployments_deleted += dep_deleted
            total_deployments_failed += dep_failed
        
        # Then delete the project
        try:
            print(f"    Deleting project...", end=" ")
            client.delete_project(p.id)
            print("✓")
            projects_deleted += 1
        except Exception as e:
            print(f"✗ Error: {e}")
            projects_failed += 1
    
    print(f"\nDone.")
    print(f"  Projects: {projects_deleted} deleted, {projects_failed} failed")
    print(f"  Deployments: {total_deployments_deleted} deleted, {total_deployments_failed} failed")


if __name__ == "__main__":
    main()
