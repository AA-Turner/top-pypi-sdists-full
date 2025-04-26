"""A service for interacting with the filesystem."""

import json
import os
from typing import List

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
    def append_dict_to_json_file(file_name: str, content_to_append: dict) -> None:
        """
        Append the given dict to the specified file in json format.

        :param file_name: File to append to.
        :param content_to_append: Content to append to file.
        """
        try:
            with open(file_name, "r") as file:
                content_json = json.load(file)
        except Exception:
            content_json = None

        try:
            content_dict = dict(content_json)
            content_dict.update(content_to_append)
        except Exception:
            content_dict = content_to_append

        with open(file_name, "w") as file:
            json.dump(content_dict, file, indent=2)
