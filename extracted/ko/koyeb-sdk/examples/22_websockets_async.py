#!/usr/bin/env python3
"""WebSocket communication via exposed port (async variant)"""

import asyncio
import os
import sys
import json

from websockets.asyncio.client import connect

import random
import string
from koyeb import AsyncSandbox

WS_SERVER_SCRIPT = r'''
import asyncio
import websockets
import json

async def handler(ws):
    async for message in ws:
        data = json.loads(message)
        response = {"echo": data, "server": "sandbox"}
        await ws.send(json.dumps(response))

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        await asyncio.Future()

asyncio.run(main())
'''


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
            name=f"websockets-{suffix}",
            wait_ready=True,
            api_token=api_token,
        )

        # Install websockets in the sandbox and start the server
        print("Installing websockets in sandbox...")
        result = await sandbox.exec("pip install websockets")
        if result.exit_code != 0:
            print(f"Failed to install websockets: {result.stderr}")
            return 1

        print("Starting WebSocket server...")
        await sandbox.filesystem.write_file("/tmp/ws_server.py", WS_SERVER_SCRIPT)
        process_id = await sandbox.launch_process("python3 /tmp/ws_server.py")
        print(f"Server started with process ID: {process_id}")
        await asyncio.sleep(3)

        # Expose the WebSocket port
        print("\nExposing port 8765...")
        exposed = await sandbox.expose_port(8765)
        print(f"Exposed at: {exposed.exposed_at}")
        await asyncio.sleep(2)

        # Connect and exchange messages
        ws_url = exposed.exposed_at.replace("https://", "wss://").replace("http://", "ws://")
        print(f"\nConnecting to {ws_url}...")

        async with connect(ws_url) as ws:
            for i in range(3):
                payload = json.dumps({"msg": f"hello {i + 1}"})
                await ws.send(payload)
                response = json.loads(await ws.recv())
                print(f"  Sent: {payload}")
                print(f"  Received: {json.dumps(response)}")
                assert response["echo"]["msg"] == f"hello {i + 1}"

        print("\n✓ WebSocket echo test passed")
        return 0

    finally:
        if sandbox:
            await sandbox.delete()


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
