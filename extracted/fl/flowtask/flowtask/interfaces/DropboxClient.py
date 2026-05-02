from abc import ABC
from typing import Union
from pathlib import Path
import asyncio
import aiofiles
import dropbox
from dropbox.exceptions import ApiError
from dropbox.files import WriteMode
from ..exceptions import ComponentError


class DropboxClient(ABC):
    """
    Dropbox Client for downloading and uploading files and folders to/from Dropbox.
    """
    def __init__(
        self,
        *args,
        access_key: Union[str, dict] = None,
        **kwargs
    ):
        self.access_key: str = access_key
        self.dbx = dropbox.Dropbox(self.access_key)
        super().__init__(*args, **kwargs)

    async def download_file(
        self,
        source_filename: str,
        destination_dir: Union[str, Path] = "."
    ) -> Path:
        """
        Download a file from Dropbox by its name.
        """
        try:
            search_result = await asyncio.to_thread(
                self.dbx.files_search_v2,
                query=source_filename
            )
            if not search_result.matches:
                raise ComponentError(
                    f"File '{source_filename}' not found in Dropbox."
                )

            file_path = Path(destination_dir) / source_filename
            file_metadata = search_result.matches[0].metadata
            file_id = file_metadata.metadata.id

            async with aiofiles.open(file_path, 'wb') as f:
                _, res = await asyncio.to_thread(self.dbx.files_download, file_id)
                await f.write(res.content)

            return file_path

        except ApiError as error:
            raise ComponentError(
                f"Error downloading file from Dropbox: {error}"
            )

    async def download_folder(
        self,
        folder_name: str,
        destination_dir: Union[str, Path] = "."
    ) -> None:
        """
        Download all files within a specified Dropbox folder by name.
        """
        try:
            search_result = await asyncio.to_thread(
                self.dbx.files_search_v2,
                query=folder_name
            )
            if not search_result.matches:
                raise ComponentError(
                    f"Folder '{folder_name}' not found in Dropbox."
                )

            folder_metadata = search_result.matches[0].metadata
            folder_id = folder_metadata.metadata.id
            destination_dir = Path(destination_dir) / folder_name
            destination_dir.mkdir(parents=True, exist_ok=True)

            entries = await asyncio.to_thread(
                self.dbx.files_list_folder,
                folder_id
            )

            for entry in entries.entries:
                if isinstance(entry, dropbox.files.FileMetadata):
                    file_name = entry.name
                    file_path = destination_dir / file_name

                    async with aiofiles.open(file_path, 'wb') as f:
                        _, res = await asyncio.to_thread(self.dbx.files_download, entry.id)
                        await f.write(res.content)

                    print(
                        f"Downloaded '{file_name}' to '{file_path}'."
                    )

        except ApiError as error:
            raise ComponentError(
                f"Error downloading folder '{folder_name}' from Dropbox: {error}"
            )

    async def upload_file(
        self,
        source_filepath: Union[str, Path],
        destination_path: Union[str, Path] = "/"
    ) -> None:
        """
        Upload a file to Dropbox.
        """
        source_filepath = Path(source_filepath)
        if not source_filepath.exists() or not source_filepath.is_file():
            raise ComponentError(
                f"Source file '{source_filepath}' does not exist."
            )

        try:
            async with aiofiles.open(source_filepath, 'rb') as f:
                file_data = await f.read()
                destination_path = str(Path(destination_path) / source_filepath.name)

                await asyncio.to_thread(
                    self.dbx.files_upload,
                    file_data,
                    destination_path,
                    mode=WriteMode.overwrite
                )
                print(
                    f"Uploaded file '{source_filepath.name}' to '{destination_path}'."
                )

        except ApiError as error:
            raise ComponentError(
                f"Error uploading file '{source_filepath}': {error}"
            )

    async def upload_folder(
        self,
        source_dir: Union[str, Path],
        destination_path: Union[str, Path] = "/"
    ) -> None:
        """
        Upload all files within a specified local folder to Dropbox.
        """
        source_dir = Path(source_dir)
        if not source_dir.exists() or not source_dir.is_dir():
            raise ComponentError(
                f"Source directory '{source_dir}' does not exist."
            )

        for file_path in source_dir.rglob('*'):
            if file_path.is_file():
                # Preserve directory structure within Dropbox
                relative_path = file_path.relative_to(source_dir)
                dropbox_path = str(Path(destination_path) / relative_path)

                try:
                    async with aiofiles.open(file_path, 'rb') as f:
                        file_data = await f.read()
                        await asyncio.to_thread(
                            self.dbx.files_upload,
                            file_data,
                            dropbox_path,
                            mode=WriteMode.overwrite
                        )
                        print(f"Uploaded '{file_path}' to '{dropbox_path}'.")

                except ApiError as error:
                    raise ComponentError(
                        f"Error uploading file '{file_path}': {error}"
                    )
