"""A service for interacting with the filesystem."""

import os
from pydantic import TypeAdapter

from db_contrib_tool.setup_repro_env.request_models import DownloadRequest
from typing import List, Set

import structlog

LOGGER = structlog.get_logger(__name__)


class FileService:
    """A service for interacting with the filesystem."""

    @staticmethod
    def write_windows_install_paths(target_file: str, paths: List[str]) -> None:
        """
        Write the given list of paths to the target file.

        :param target_file: File to write paths to.
        :param paths: Paths to write to file.
        """
        with open(target_file, "a") as out:
            if os.stat(target_file).st_size > 0:
                out.write(os.pathsep)
            out.write(os.pathsep.join(paths))

        LOGGER.info(f"Finished writing binary paths on Windows to {target_file}")

    @staticmethod
    def delete_file(file_name: str) -> None:
        """
        Delete the given file from the filesystem.

        :param file_name: File to delete.
        """
        os.remove(file_name)

    @staticmethod
    def append_downloads_to_json_file(file_name: str, downloads: Set[DownloadRequest]) -> None:
        """
        Append DownloadRequest's the specified file in json format.

        :param file_name: File to append to.
        :param downloads: DownloadRequest's to append to file.
        """

        adapter = TypeAdapter(Set[DownloadRequest])

        all_downloads = FileService.load_downloads_from_json_file(file_name)
        all_downloads.update(downloads)
        with open(file_name, "wb") as file:
            file.write(adapter.dump_json(all_downloads, indent=2, round_trip=True))

    @staticmethod
    def load_downloads_from_json_file(file_name: str) -> Set[DownloadRequest]:
        """
        Load DownloadRequest's from specified file in json format.

        :param file_name: File to load from.
        """

        adapter = TypeAdapter(Set[DownloadRequest])
        try:
            with open(file_name, "r") as file:
                downloads = adapter.validate_json(file.read())
        except Exception as e:
            LOGGER.error("Failed to load download URLS from existing versions file", reason=str(e))
            downloads = set()
        return downloads
