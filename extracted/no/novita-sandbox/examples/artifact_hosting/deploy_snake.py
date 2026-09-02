#!/usr/bin/env python3
"""
Deploy snake game project using pre-built template

The template already contains snake game source code, no need to upload code during deployment.

Prerequisites:
1. Build template (in snake directory):
   novita-sandbox-cli template build -d novita.Dockerfile -n snake

2. Configure environment variables:
   - NOVITA_API_KEY: Novita API Key

Usage:
    cd sdk-python/examples/artifact_hosting
    python deploy_snake.py -p my-snake-game
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

from novita_sandbox.code_interpreter import Sandbox
from novita_sandbox.artifact_hosting import DeploymentClient, DeploymentStatus, DeploymentError, is_successful


# Configuration
TEMPLATE_NAME = "snake"
SOURCE_DIR_IN_SANDBOX = "/app"
DOCKERFILE_PATH = Path(__file__).parent / "snake" / "Dockerfile"

# API Configuration (URL is fixed in SDK: https://artifact.novita.ai/v1)
API_KEY = os.environ.get("NOVITA_API_KEY")


def main():
    parser = argparse.ArgumentParser(description="Deploy snake game using pre-built template")
    parser.add_argument("-p", "--project", required=True, help="Project name")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging (DEBUG)")
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default=None,
        help="Log level (default: no logging, -v is equivalent to DEBUG)"
    )
    parser.add_argument(
        "--sandbox-timeout",
        type=int,
        default=600,
        help="Sandbox timeout in seconds, default 600"
    )
    args = parser.parse_args()

    # Configure logging
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    elif args.log_level:
        logging.basicConfig(level=getattr(logging, args.log_level), format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    project_name = args.project

    # Validate configuration
    if not API_KEY:
        print("❌ Please set NOVITA_API_KEY environment variable")
        sys.exit(1)

    if not DOCKERFILE_PATH.exists():
        print(f"❌ Dockerfile not found: {DOCKERFILE_PATH}")
        sys.exit(1)

    # Read Dockerfile content
    dockerfile_content = DOCKERFILE_PATH.read_text()

    print("=" * 60)
    print("🐍 Snake Game Deployment (Using Pre-built Template)")
    print("=" * 60)
    print(f"📦 Project name: {project_name}")
    print(f"🐳 Template: {TEMPLATE_NAME}")
    print(f"📁 Source directory: {SOURCE_DIR_IN_SANDBOX}")
    print()

    sandbox = None

    try:
        # 1. Create Sandbox from template (already contains source code)
        print("🔧 Creating Sandbox...")
        sandbox = Sandbox.create(TEMPLATE_NAME, timeout=args.sandbox_timeout)
        full_sandbox_id = sandbox.sandbox_id
        # Extract sandbox_id (part before "-")
        sandbox_id = full_sandbox_id.split("-")[0] if "-" in full_sandbox_id else full_sandbox_id
        print(f"✅ Sandbox created successfully: {full_sandbox_id} -> Using ID: {sandbox_id}")
        print()

        # 2. Deploy to Artifact Hosting
        with DeploymentClient(api_key=API_KEY) as client:
            # Check if project exists
            print("🔍 Checking if project exists...")
            project = None

            for p in client.list_projects():
                if p.name == project_name:
                    project = p
                    print(f"✅ Found existing project: {project.id}")
                    break

            if project is None:
                print(f"📝 Creating new project: {project_name}")
                project = client.create_project(
                    name=project_name,
                    description="Snake Game - Static HTML/CSS/JS served by Nginx",
                )
                print(f"✅ Project created successfully: {project.id}")

            print()

            # Start deployment
            print("🚀 Starting deployment...")

            def on_status_change(deployment):
                print(f"   📍 Status changed: {deployment.status.name}")

            deployment = project.deploy(
                sandbox_id=sandbox_id,
                arti_dir=SOURCE_DIR_IN_SANDBOX,
                dockerfile=dockerfile_content,
                message="Deploy from snake template",
                environment_variables={
                    "NODE_ENV": "production",
                },
                http_port=80,  # Nginx serves on port 80
                check_health_path="/",  # Root path returns HTML
                wait=True,
                on_status_change=on_status_change,
            )

            print()
            # Both RUNNING and IDLE are successful states (IDLE = idle state when no traffic)
            if is_successful(deployment.status):
                print("=" * 60)
                print("🎉 Deployment successful!")
                print("=" * 60)
                print(f"   Deployment ID: {deployment.id}")
                print(f"   Status: {deployment.status.name}")
                print()
                
                # Get project URL
                project = client.get_project(project.id)
                if project.endpoint and project.endpoint.default_url:
                    print("🎮 Play the game:")
                    print(f"   {project.endpoint.default_url}")
                else:
                    print(f"⚠️  URL not retrieved (endpoint: {project.endpoint})")
            else:
                print(f"❌ Deployment failed: {deployment.status.name}")
                if deployment.error_message:
                    print(f"   Error: {deployment.error_message}")
                
                # Stream logs to diagnose failure
                print()
                print("📋 Deployment Logs:")
                print("-" * 60)
                try:
                    for log in deployment.stream_logs():
                        print(log.message)
                except Exception as log_err:
                    print(f"⚠️  Failed to stream logs: {log_err}")
                print("-" * 60)
                sys.exit(1)

    except DeploymentError as e:
        print(f"❌ Deployment failed: {e}")
        
        # Try to stream logs for the failed deployment
        print()
        print("📋 Deployment Logs:")
        print("-" * 60)
        try:
            # Get the latest deployment from the project
            with DeploymentClient(api_key=API_KEY) as client:
                for p in client.list_projects():
                    if p.name == project_name:
                        # Get the most recent deployment
                        for dep in p.list_deployments():
                            print(f"Streaming logs for deployment: {dep.id}")
                            print()
                            for log in dep.stream_logs():
                                print(log.message)
                            break
                        break
        except Exception as log_err:
            print(f"⚠️  Failed to stream logs: {log_err}")
        print("-" * 60)
        sys.exit(1)

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    finally:
        # 3. Cleanup Sandbox
        if sandbox:
            print()
            print("🧹 Cleaning up Sandbox...")
            try:
                sandbox.kill()
                print("✅ Sandbox cleaned up")
            except Exception as e:
                print(f"⚠️  Failed to cleanup Sandbox: {e}")


if __name__ == "__main__":
    main()
