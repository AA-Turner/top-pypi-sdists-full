#!/usr/bin/env python3
"""Port exposure via TCP proxy (async variant)"""

import asyncio
import sys
import os
import sys

import httpx


import random
import string
from koyeb import AsyncSandbox


async def main():
    api_token = os.getenv("KOYEB_API_TOKEN")
    if not api_token:
        print("Error: KOYEB_API_TOKEN not set")
        return 1

    sandbox = None
    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    try:
        sandbox = await AsyncSandbox.create(
            image="koyeb/sandbox:slim",
            name=f"expose-port-{suffix}",
            wait_ready=True,
            api_token=api_token,
        )

        # Create a test file to serve
        print("\nCreating test file...")
        await sandbox.filesystem.write_file(
            "/tmp/test.html", "<h1>Hello from Sandbox!</h1><p>Port 8080</p>"
        )
        print("Test file created")

        # Start a simple HTTP server on port 8080
        print("\nStarting HTTP server on port 8080...")
        process_id = await sandbox.launch_process(
            "python3 -m http.server 8080",
            cwd="/tmp",
        )
        print(f"Server started with process ID: {process_id}")

        # Wait for server to start
        print("Waiting for server to start...")
        await asyncio.sleep(3)

        # Expose port 8080
        print("\nExposing port 8080...")
        exposed = await sandbox.expose_port(8080)
        print(f"Port exposed: {exposed.port}")
        print(f"Exposed at: {exposed.exposed_at}")

        # Wait a bit for the port to be ready
        print("Waiting for port to be ready...")
        await asyncio.sleep(2)

        # Make a request to verify it's working
        print("\nMaking HTTP request to verify port exposure...")
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{exposed.exposed_at}/test.html", timeout=10)
            response.raise_for_status()
            print(f"✓ Request successful! Status: {response.status_code}")
            print(f"✓ Response content: {response.text.strip()}")
        except Exception as e:
            print(f"⚠ Request failed: {e}")
            print("Note: Port may still be propagating. Try again in a few seconds.")

        # List processes to show the server is running
        print("\nRunning processes:")
        processes = await sandbox.list_processes()
        for process in processes:
            if process.status == "running":
                print(f"  {process.id}: {process.command} - {process.status}")

        # Switch to a different port (e.g., 8081)
        print("\nSwitching to port 8081...")
        # Create a different test file for port 8081
        await sandbox.filesystem.write_file(
            "/tmp/test2.html", "<h1>Hello from Sandbox!</h1><p>Port 8081</p>"
        )
        # Start a new server on 8081
        await sandbox.launch_process(
            "python3 -m http.server 8081",
            cwd="/tmp",
        )
        print("Waiting for server to start...")
        await asyncio.sleep(3)

        # Expose the new port (this will automatically unbind the previous port)
        exposed_2 = await sandbox.expose_port(8081)
        print(f"Port exposed: {exposed_2.port}")
        print(f"Exposed at: {exposed_2.exposed_at}")

        # Wait a bit for the port to be ready
        print("Waiting for port to be ready...")
        await asyncio.sleep(2)

        # Make a request to verify the new port is working
        print("\nMaking HTTP request to verify port 8081...")
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{exposed_2.exposed_at}/test2.html", timeout=10)
            response.raise_for_status()
            print(f"✓ Request successful! Status: {response.status_code}")
            print(f"✓ Response content: {response.text.strip()}")
        except Exception as e:
            print(f"⚠ Request failed: {e}")
            print("Note: Port may still be propagating. Try again in a few seconds.")

        # Unexpose the port
        print("\nUnexposing port...")
        await sandbox.unexpose_port()
        print("Port unexposed")

        return 0

    finally:
        if sandbox:
            await sandbox.delete()


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
