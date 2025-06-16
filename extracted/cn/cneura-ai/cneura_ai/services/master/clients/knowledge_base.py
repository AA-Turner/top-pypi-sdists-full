import httpx
from typing import Optional
import os

class KnowledgeBaseClient:
    def __init__(self, base_url: str, timeout: int = 60):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=timeout)

    async def upload_document(
        self,
        file_path: str,
        key: str,
        namespace: str,
        metadata: Optional[str] = None,
    ) -> Optional[dict]:
        """
        Uploads a document to the knowledge base for background processing.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File does not exist: {file_path}")

        url = f"{self.base_url}/knowledge-base/upload-doc"
        files = {"file": (os.path.basename(file_path), open(file_path, "rb"))}
        data = {
            "key": key,
            "namespace": namespace,
        }
        if metadata:
            data["metadata"] = metadata

        try:
            response = await self.client.post(url, data=data, files=files)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            print(f"Error uploading document: {str(e)}")
        finally:
            files["file"][1].close()  # Close the file handle

        return None

    async def close(self):
        await self.client.aclose()


############### example ##############
import asyncio

async def main():
    client = KnowledgeBaseClient(base_url="http://localhost:8000")
    
    result = await client.upload_document(
        file_path="example.pdf",
        key="doc-key-001",
        namespace="project-xyz",
        metadata="{'source': 'internal upload'}"
    )

    if result:
        print("Upload result:", result)
    else:
        print("Upload failed.")

    await client.close()

asyncio.run(main())