#!/usr/bin/env python3
"""
Deploy ecomm project using pre-built template

The template already contains ecomm source code, no need to upload code during deployment.

Prerequisites:
1. Build template (in ecomm directory):
   novita-sandbox-cli template build -d novita.Dockerfile -n ecomm-site

2. Configure environment variables:
   - NOVITA_API_KEY: Novita API Key
   - DATABASE_URL: Neon PostgreSQL connection string

Usage:
    cd sdk-python/examples/artifact_hosting
    python deploy_with_template.py -p my-ecomm-project
"""

import argparse
import logging
import os
import sys
from pathlib import Path

import dotenv

# Load .env files (current directory first, then ecomm directory)
dotenv.load_dotenv(Path(__file__).parent / ".env")
dotenv.load_dotenv(Path(__file__).parent / "ecomm" / ".env")

# Add SDK to Python path (development environment)
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from novita_sandbox.code_interpreter import Sandbox
from novita_sandbox.artifact_hosting import DeploymentClient, DeploymentStatus, DeploymentError, is_successful


# Configuration
TEMPLATE_NAME = "ecomm-site"
SOURCE_DIR_IN_SANDBOX = "/app"
DOCKERFILE_PATH = Path(__file__).parent / "ecomm" / "Dockerfile"

# API Configuration (URL is fixed in SDK: https://artifact.novita.ai/v1)
API_KEY = os.environ.get("NOVITA_API_KEY")
DATABASE_URL = os.environ.get("DATABASE_URL")


def main():
    parser = argparse.ArgumentParser(description="Deploy ecomm project using pre-built template")
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

    if not DATABASE_URL:
        print("❌ Please set DATABASE_URL environment variable")
        sys.exit(1)

    if not DOCKERFILE_PATH.exists():
        print(f"❌ Dockerfile not found: {DOCKERFILE_PATH}")
        sys.exit(1)

    # Read Dockerfile content
    dockerfile_content = DOCKERFILE_PATH.read_text()

    print("=" * 60)
    print("🛒 E-commerce Project Deployment (Using Pre-built Template)")
    print("=" * 60)
    print(f"📦 Project name: {project_name}")
    print(f"🐳 Template: {TEMPLATE_NAME}")
    print(f"📁 Source directory: {SOURCE_DIR_IN_SANDBOX}")
    print(f"🗄️  DATABASE_URL: {DATABASE_URL[:50]}...")
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

        # Delete node_modules (to avoid large build context, Dockerfile will reinstall)
        print("🗑️  Cleaning build context...")
        result = sandbox.commands.run(f"sudo rm -rf {SOURCE_DIR_IN_SANDBOX}/node_modules {SOURCE_DIR_IN_SANDBOX}/.env {SOURCE_DIR_IN_SANDBOX}/dist")
        print("✅ Build context cleaned")
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
                    description="E-commerce site - Based on Hono + Node.js + Neon PostgreSQL",
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
                message="Deploy from ecomm-site template",
                environment_variables={
                    "DATABASE_URL": DATABASE_URL,
                    "NODE_ENV": "production",
                },
                http_port=3000,
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
                    print("📱 Access application:")
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
