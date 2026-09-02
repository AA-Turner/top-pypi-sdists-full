from abc import ABC
from pathlib import Path
from typing import Union
import asyncio
from google.cloud import storage
from google.auth.exceptions import GoogleAuthError
from .GoogleClient import GoogleClient
from ..exceptions import ComponentError


class GoogleCloudStorageClient(GoogleClient, ABC):
    """
    Google Cloud Storage Client for interacting with Google Cloud Storage (GCS).
    Provides methods for file and folder operations.
    """

    def __init__(self, *args, bucket_name: str, **kwargs):
        super().__init__(*args, **kwargs)
        self.bucket_name = bucket_name
        self._bucket = None

    async def get_bucket(self):
        """Get the GCS bucket, with caching."""
        if not self._bucket:
            try:
                client = await asyncio.to_thread(storage.Client, credentials=self.credentials)
                self._bucket = client.bucket(self.bucket_name)
            except GoogleAuthError as e:
                raise ComponentError(f"Google GCS authentication error: {e}")
        return self._bucket

    async def create_folder(self, folder_name: str):
        """Create a folder in GCS by creating an empty blob with a trailing '/'."""
        bucket = await self.get_bucket()
        blob = bucket.blob(f"{folder_name}/")
        await asyncio.to_thread(blob.upload_from_string, "")
        print(f"Folder '{folder_name}' created in GCS.")

    async def upload_file(self, source_path: Union[str, Path], destination_path: str):
        """Upload a file to GCS."""
        bucket = await self.get_bucket()
        blob = bucket.blob(destination_path)
        await asyncio.to_thread(blob.upload_from_filename, str(source_path))
        print(f"File '{source_path}' uploaded to '{destination_path}' in GCS.")

    async def download_file(self, source_path: str, destination_dir: Union[str, Path]):
        """Download a file from GCS."""
        bucket = await self.get_bucket()
        blob = bucket.blob(source_path)
        destination_file = Path(destination_dir) / Path(source_path).name
        await asyncio.to_thread(blob.download_to_filename, str(destination_file))
        print(f"File '{source_path}' downloaded to '{destination_file}'.")

    async def delete_file(self, file_path: str):
        """Delete a file from GCS."""
        bucket = await self.get_bucket()
        blob = bucket.blob(file_path)
        await asyncio.to_thread(blob.delete)
        print(f"File '{file_path}' deleted from GCS.")

    async def upload_folder(self, source_folder: Union[str, Path], destination_folder: str):
        """Upload all files from a local folder to a GCS folder."""
        source_folder = Path(source_folder)
        tasks = []
        for file_path in source_folder.glob("**/*"):
            if file_path.is_file():
                relative_path = file_path.relative_to(source_folder)
                destination_path = f"{destination_folder}/{relative_path}"
                tasks.append(self.upload_file(file_path, destination_path))
        await asyncio.gather(*tasks)
        print(f"Folder '{source_folder}' uploaded to '{destination_folder}' in GCS.")

    async def download_folder(self, source_folder: str, destination_folder: Union[str, Path]):
        """Download all files from a GCS folder to a local folder."""
        bucket = await self.get_bucket()
        blobs = bucket.list_blobs(prefix=f"{source_folder}/")
        destination_folder = Path(destination_folder) / source_folder
        destination_folder.mkdir(parents=True, exist_ok=True)

        tasks = []
        async for blob in blobs:
            if not blob.name.endswith("/"):  # Skip "directory" entries
                relative_path = Path(blob.name).relative_to(source_folder)
                local_file_path = destination_folder / relative_path
                local_file_path.parent.mkdir(parents=True, exist_ok=True)
                tasks.append(asyncio.to_thread(blob.download_to_filename, str(local_file_path)))
        await asyncio.gather(*tasks)
        print(f"Folder '{source_folder}' downloaded to '{destination_folder}'.")

