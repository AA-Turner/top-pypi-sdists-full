import os
from typing import Callable, List, Optional, Tuple

from .file import VolumeFile


class AbstractVolume:
    def __init__(self):
        raise NotImplementedError()

    def list(self, path: str) -> List[VolumeFile]:
        """
        Lists a directory from the volume.

        The result will contain all files, including ones in subdirectories, under this directory.

        If such path does not exist (i.e. there is no such file or directory), this function will
        return an empty list.

        Arguments:
            path (str):
                Reference to the path in this volume.
        """
        raise NotImplementedError()

    def download_file(
        self,
        file: VolumeFile,
        destination: str,
        progress_callback: Optional[Callable[[int], None]] = None,
    ):
        """
        Downloads a file from the volume to local path.

        Arguments:
            file (str):
                Reference to the file in this volume.

            destination (str):
                Local path to which the file will be downloaded.

            progress_callback ((int) -> None, optional):
                Callback. This function will be called with: (downloaded bytes)
        """
        raise NotImplementedError()

    def download_directory(
        self,
        directory: str,
        destination: str,
        progress_callback: Optional[Callable[[int, int, int, int, int], None]] = None,
    ):
        """
        Downloads a directory from the volume to local path.

        Arguments:
            directory (str):
                Path of the directory in this volume.

            destination (str):
                Local path to which the file will be downloaded.  This should be a directory.
                If such path does not exist, it will be created.

            progress_callback ((int) -> None, optional):
                Callback. This function will be called with:
                    (
                        total file count,
                        1-based index of current file,
                        size of current file,
                        downloaded bytes of current file,
                        total downloaded bytes,
                    )
        """
        raise NotImplementedError()

    def _download_directory_serially(
        self,
        directory: str,
        destination: str,
        progress_callback: Optional[Callable[[int, int, int, int, int], None]] = None,
    ):
        """
        Example implementation of download_directory() that simply calls list(), and
        calls download_file() to each.
        """
        files = self.list(directory)

        total_files = len(files)
        total_bytes_downloaded = 0

        for file_idx, file in enumerate(files, 1):
            if progress_callback is not None:

                def _callback(current_bytes_downloaded: int):
                    progress_callback(
                        total_files,
                        file_idx,
                        file.size,
                        current_bytes_downloaded,
                        total_bytes_downloaded + current_bytes_downloaded,
                    )
            else:
                _callback = None

            relative_path = os.path.relpath(file.path, directory)

            self.download_file(
                file=file,
                destination=os.path.join(destination, relative_path),
                progress_callback=_callback,
            )

            total_bytes_downloaded += file.size

    def upload_file(
        self,
        local_file: str,
        destination: str,
        progress_callback: Optional[Callable[[int], None]] = None,
    ):
        """
        Uploads a local file to the volume.

        Arguments:
            local_file (str):
                Path of the local file.

            destination (str):
                Path in volume to which upload this file. If such path already exists,
                it will be overwritten.

            progress_callback ((int) -> None, optional):
                Callback. This function will be called with: (uploaded bytes)
        """
        raise NotImplementedError()

    def upload_directory(
        self,
        local_directory: str,
        destination: str,
        progress_callback: Optional[Callable[[int, int, int, int, int], None]] = None,
    ):
        """
        Uploads a local directory to the volume.

        Example:
            The following code,

                ```python
                vessl.upload_directory(
                    local_path="/a/b",
                    destination="c/d",
                )
                ```

            will upload a local file `/a/b/x/y.txt` to the volume path `c/d/x/y.txt`.

        Arguments:
            local_directory (str):
                Path of the local directory.

            destination (str):
                Path in volume to which upload this file.

            progress_callback ((int) -> None, optional):
                Callback. This function will be called with:
                    (
                        total file count,
                        1-based index of current file,
                        size of current file,
                        uploaded bytes of current file,
                        total uploaded bytes,
                    )
        """

        # [(local_path, remote_path, size_bytes), ...]
        file_list: List[Tuple[str, str, int]] = []

        for root, dirs, files in os.walk(local_directory):
            for filename in files:
                local_path = os.path.join(root, filename)
                relative_path = os.path.relpath(local_path, local_directory)
                remote_path = os.path.join(destination, relative_path)
                file_list.append((local_path, remote_path, os.stat(local_path).st_size))

        total_files = len(file_list)
        total_bytes_uploaded = 0
        for i, file in enumerate(file_list, 1):
            local_path, remote_path, size = file

            if progress_callback is not None:

                def callback(current_bytes_uploaded: int):
                    progress_callback(
                        total_files,
                        i,
                        size,
                        current_bytes_uploaded,
                        total_bytes_uploaded + current_bytes_uploaded,
                    )
            else:
                callback = None

            self.upload_file(local_path, remote_path, callback)

            total_bytes_uploaded += size

    def delete_file(self, path: str):
        """
        Deletes a file from the volume.

        Arguments:
             path (str): Path of the file to delete.
        """
        raise NotImplementedError()

    def delete_directory(self, path: str):
        """
        Deletes a directory from the volume.

        Arguments:
             path (str): Path of the directory to delete.
        """
        raise NotImplementedError()
