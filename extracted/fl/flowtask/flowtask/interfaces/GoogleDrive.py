from abc import ABC
from typing import Union
from pathlib import Path, PurePath
import asyncio
import aiofiles
import pandas as pd
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from .GoogleClient import GoogleClient
from ..exceptions import ComponentError


class GoogleDriveClient(GoogleClient, ABC):
    """
    Google Drive Client for downloading files from Google Drive.
    """

    async def download_file(
        self,
        source_filename: str,
        destination_dir: Union[str, Path] = "."
    ) -> PurePath:
        """
        Download a file from Google Drive by its name.

        Args:
            source_filename (str): The name of the file to download.
            destination_dir (str or Path): Directory where the file will be saved (default is current directory).

        Returns:
            str: Path to the downloaded file.
        """
        try:
            drive_service = await asyncio.to_thread(self.get_drive_client)

            # Search for the file by name
            results = await asyncio.to_thread(
                drive_service.files().list,
                q=f"name='{source_filename}'",
                fields="files(id, name)",
                pageSize=1
            )
            files = results.execute().get('files', [])
            if not files:
                raise ComponentError(f"File '{source_filename}' not found on Google Drive.")

            file_id = files[0]['id']
            request = drive_service.files().get_media(fileId=file_id)
            file_path = Path(destination_dir) / source_filename

            # Asynchronously open the file with aiofiles
            async with aiofiles.open(file_path, 'wb') as f:
                downloader = MediaIoBaseDownload(f, request)
                done = False
                while not done:
                    # Run the next_chunk call in a separate thread
                    status, done = await asyncio.to_thread(downloader.next_chunk)
                    print(f"Download {int(status.progress() * 100)}%.")

            return file_path

        except HttpError as error:
            raise ComponentError(f"Error downloading file from Google Drive: {error}")

    async def download_folder(
        self,
        folder_name: str,
        destination_dir: Union[str, Path] = "."
    ) -> None:
        """
        Download all files within a specified Google Drive folder by name.

        Args:
            folder_name (str): The name of the folder to download.
            destination_dir (str or Path): Directory where the files will be saved.

        Returns:
            None
        """
        try:
            drive_service = await asyncio.to_thread(self.get_drive_client)

            # Search for the folder by name to get the folder ID
            folder_results = await asyncio.to_thread(
                drive_service.files().list,
                q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'",
                fields="files(id, name)",
                pageSize=1
            )
            folders = folder_results.execute().get('files', [])
            if not folders:
                raise ComponentError(f"Folder '{folder_name}' not found on Google Drive.")

            folder_id = folders[0]['id']
            destination_dir = Path(destination_dir) / folder_name
            destination_dir.mkdir(parents=True, exist_ok=True)

            # List all files in the folder
            file_results = await asyncio.to_thread(
                drive_service.files().list,
                q=f"'{folder_id}' in parents and mimeType != 'application/vnd.google-apps.folder'",
                fields="files(id, name)"
            )
            files = file_results.execute().get('files', [])

            if not files:
                print(f"No files found in folder '{folder_name}'.")
                return

            # Download each file in the folder
            for file_info in files:
                file_id = file_info['id']
                file_name = file_info['name']
                file_path = destination_dir / file_name

                request = drive_service.files().get_media(fileId=file_id)
                async with aiofiles.open(file_path, 'wb') as f:
                    downloader = MediaIoBaseDownload(f, request)
                    done = False
                    while not done:
                        status, done = await asyncio.to_thread(downloader.next_chunk)
                        print(f"Downloading '{file_name}' - {int(status.progress() * 100)}% complete.")

                print(f"Downloaded '{file_name}' to '{file_path}'.")

        except HttpError as error:
            raise ComponentError(f"Error downloading folder '{folder_name}' from Google Drive: {error}")
