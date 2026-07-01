#!/usr/bin/env python3
"""Create a sandbox using an existing app instead of creating a new one"""

import os
import sys
import random
import string
import time

from koyeb import Sandbox
from koyeb.api.models.create_app import CreateApp
from koyeb.sandbox.utils import get_api_clients


def main():
    api_token = os.getenv("KOYEB_API_TOKEN")
    if not api_token:
        print("Error: KOYEB_API_TOKEN not set")
        return 1

    app_id = None
    sandbox = None
    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))

    try:
        # Step 1: Create an app first
        print("=" * 60)
        print(" CREATING APP")
        print("=" * 60)
        print()

        apps_api = get_api_clients(api_token).apps

        app_name = f"my-sandbox-app-{int(time.time())}"
        print(f"  Creating app: {app_name}")

        app_response = apps_api.create_app(app=CreateApp(name=app_name))
        app_id = app_response.app.id

        print(f"  App created successfully!")
        print(f"  App ID: {app_id}")
        print(f"  App Name: {app_response.app.name}")
        print()

        # Step 2: Create a sandbox using the existing app
        print("=" * 60)
        print(" CREATING SANDBOX WITH EXISTING APP")
        print("=" * 60)
        print()

        print(f"  Creating sandbox in app: {app_id}")
        sandbox = Sandbox.create(
            image="koyeb/sandbox:slim",
            name=f"sandbox-in-existing-app-{suffix}",
            wait_ready=True,
            api_token=api_token,
            app_id=app_id,  # Use the existing app instead of creating a new one
        )

        print(f"  Sandbox created successfully!")
        print(f"  Service ID: {sandbox.service_id}")
        print(f"  App ID: {sandbox.app_id}")
        print()

        # Verify the sandbox is using the same app
        assert sandbox.app_id == app_id, "Sandbox should use the provided app_id"
        print("  Verified: Sandbox is using the existing app")
        print()

        # Step 3: Test the sandbox
        print("=" * 60)
        print(" TESTING SANDBOX")
        print("=" * 60)
        print()

        is_healthy = sandbox.is_healthy()
        print(f"  Healthy: {is_healthy}")

        result = sandbox.exec("echo 'Hello from sandbox in existing app!'")
        print(f"  Output: {result.stdout.strip()}")
        print()

        print("Demo completed successfully!")

        return 0

    finally:
        # Clean up: delete the app (which will also delete the sandbox service)
        if app_id:
            print()
            print("Cleaning up...")
            try:
                apps_api.delete_app(app_id)
                print(f"  Deleted app: {app_id}")
            except Exception as e:
                print(f"  Error deleting app: {e}")


if __name__ == "__main__":
    sys.exit(main())
