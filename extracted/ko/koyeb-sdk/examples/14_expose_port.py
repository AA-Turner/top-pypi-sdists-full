#!/usr/bin/env python3
"""Port exposure via TCP proxy"""

import os
import sys
import time

import httpx


import random
import string
from koyeb import Sandbox


def main():
    api_token = os.getenv("KOYEB_API_TOKEN")
    if not api_token:
        print("Error: KOYEB_API_TOKEN not set")
        sys.exit(1)
        return

    sandbox = None
    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    try:
        sandbox = Sandbox.create(
            image="koyeb/sandbox:slim",
            name=f"expose-port-{suffix}",
            wait_ready=True,
            api_token=api_token,
        )

        # Create a test file to serve
        print("\nCreating test file...")
        sandbox.filesystem.write_file(
            "/tmp/test.html", "<h1>Hello from Sandbox!</h1><p>Port 8080</p>"
        )
        print("Test file created")

        # Start a simple HTTP server on port 8080
        print("\nStarting HTTP server on port 8080...")
        process_id = sandbox.launch_process(
            "python3 -m http.server 8080",
            cwd="/tmp",
        )
        print(f"Server started with process ID: {process_id}")

        # Wait for server to start
        print("Waiting for server to start...")
        time.sleep(3)

        # Expose port 8080
        print("\nExposing port 8080...")
        exposed = sandbox.expose_port(8080)
        print(f"Port exposed: {exposed.port}")
        print(f"Exposed at: {exposed.exposed_at}")

        # Wait a bit for the port to be ready
        print("Waiting for port to be ready...")
        time.sleep(2)

        # Make a request to verify it's working
        print("\nMaking HTTP request to verify port exposure...")
        try:
            response = httpx.get(f"{exposed.exposed_at}/test.html", timeout=10)
            response.raise_for_status()
            print(f"✓ Request successful! Status: {response.status_code}")
            print(f"✓ Response content: {response.text.strip()}")
        except httpx.HTTPError as e:
            print(f"⚠ Request failed: {e}")
            print("Note: Port may still be propagating. Try again in a few seconds.")
            return 1

        # List processes to show the server is running
        print("\nRunning processes:")
        processes = sandbox.list_processes()
        for process in processes:
            if process.status == "running":
                print(f"  {process.id}: {process.command} - {process.status}")

        # Switch to a different port (e.g., 8081)
        print("\nSwitching to port 8081...")
        # Create a different test file for port 8081
        sandbox.filesystem.write_file(
            "/tmp/test2.html", "<h1>Hello from Sandbox!</h1><p>Port 8081</p>"
        )
        # Start a new server on 8081
        sandbox.launch_process(
            "python3 -m http.server 8081",
            cwd="/tmp",
        )
        print("Waiting for server to start...")
        time.sleep(3)

        # Expose the new port (this will automatically unbind the previous port)
        exposed_2 = sandbox.expose_port(8081)
        print(f"Port exposed: {exposed_2.port}")
        print(f"Exposed at: {exposed_2.exposed_at}")

        # Wait a bit for the port to be ready
        print("Waiting for port to be ready...")
        time.sleep(2)

        # Make a request to verify the new port is working
        print("\nMaking HTTP request to verify port 8081...")
        try:
            response = httpx.get(f"{exposed_2.exposed_at}/test2.html", timeout=10)
            response.raise_for_status()
            print(f"✓ Request successful! Status: {response.status_code}")
            print(f"✓ Response content: {response.text.strip()}")
        except httpx.HTTPError as e:
            print(f"⚠ Request failed: {e}")
            print("Note: Port may still be propagating. Try again in a few seconds.")
            return 1

        # Unexpose the port
        print("\nUnexposing port...")
        sandbox.unexpose_port()
        print("Port unexposed")

        return 0

    finally:
        if sandbox:
            sandbox.delete()

if __name__ == "__main__":
    sys.exit(main())
