import httpx
from typing import List, Optional


class ShellClient:
    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=base_url, timeout=timeout)

    async def create_session(self, agent_id: str):
        response = await self.client.post("/shell/session/create", json={"agent_id": agent_id})
        response.raise_for_status()
        return response.json()

    async def stop_session(self, agent_id: str):
        response = await self.client.post("/shell/session/stop", json={"agent_id": agent_id})
        response.raise_for_status()
        return response.json()

    async def run_command(self, agent_id: str, command: List[str]):
        response = await self.client.post("/shell/command/run", json={"agent_id": agent_id, "command": command})
        response.raise_for_status()
        return response.json()

    async def get_file(self, agent_id: str, path: str):
        response = await self.client.post("/shell/file/get", json={"agent_id": agent_id, "path": path})
        response.raise_for_status()
        return response.json()

    async def get_folder(self, agent_id: str, container_path: str, local_path: str):
        response = await self.client.post("/shell/folder/get", json={
            "agent_id": agent_id,
            "container_path": container_path,
            "local_path": local_path,
        })
        response.raise_for_status()
        return response.json()


    async def close(self):
        await self.client.aclose()


############### example ###########

import asyncio
import os

AGENT_ID = "agent-123"
TEST_COMMAND = ["echo", "Hello, world!"]
FILE_PATH = "./"
CONTAINER_FOLDER_PATH = "/tmp"
LOCAL_FOLDER_PATH = "./downloaded-folder"
LOCAL_DOWNLOAD_PATH = "./downloaded-folder/test.txt"

async def main():
    client = ShellClient(base_url="http://localhost:8000")

    try:
        # 1. Create a shell session
        print("Creating session...")
        response = await client.create_session(AGENT_ID)
        print("Session:", response)

        # 2. Run a shell command
        print("Running command...")
        command_output = await client.run_command(AGENT_ID, TEST_COMMAND)
        print("Command output:", command_output)

        # Step 1: Create the file inside the container
        await client.run_command(AGENT_ID, ["bash", "-c", "echo 'This is a test file' > /tmp/test.txt"])

        # Step 2: Get the file content
        file_content = await client.get_file(AGENT_ID, "/tmp/test.txt")
        print("File content:", file_content)

        # 4. Get a folder from the container to the local machine
        print("Getting folder...")
        folder_result = await client.get_folder(AGENT_ID, CONTAINER_FOLDER_PATH, LOCAL_FOLDER_PATH)
        print("Folder result:", folder_result)

      

    except Exception as e:
        print("Error during operation:", e)

    finally:
        # 6. Stop the shell session
        print("Stopping session...")
        stop_result = await client.stop_session(AGENT_ID)
        print("Session stopped:", stop_result)

        # Close the HTTPX client
        await client.close()

# Run the full test
if __name__ == "__main__":
    asyncio.run(main())