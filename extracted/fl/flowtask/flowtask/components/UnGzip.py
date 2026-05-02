import os
import logging
import asyncio
from typing import List
from collections.abc import Callable
from pathlib import PosixPath, Path, PurePath
import tarfile
from ..exceptions import FileError, ComponentError, FileNotFound
from .FileCopy import FileCopy
from ..utils import check_empty
from ..interfaces.compress import CompressSupport


class UnGzip(CompressSupport, FileCopy):
    """
    UnGzip

        Overview

            The UnGzip class is a component for decompressing Gzip (.gz) files, including compressed tarballs (e.g., .tar.gz, .tar.bz2, .tar.xz).
            This component extracts the specified Gzip or tarball file into a target directory and supports optional source file deletion
            after extraction.

        :widths: auto

            | filename       |   Yes    | The path to the Gzip file to uncompress.                                  |
            | directory      |   Yes    | The target directory where files will be extracted.                       |
            | delete_source  |   No     | Boolean indicating if the source file should be deleted post-extraction.  |
            | extract        |   No     | Dictionary specifying filenames to extract and/or output directory.       |

        Returns

            This component extracts files from a specified Gzip or tarball archive into the designated directory
            and returns a list of paths to the extracted files. It tracks metrics for the output directory and the source
            Gzip file. If configured, the original compressed file is deleted after extraction. Errors encountered during
            extraction or directory creation are logged and raised as exceptions.


        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          UnGzip:
          source:
          directory: /home/ubuntu/symbits/mso/files/commissions_statements/pr/
          filename: STATEMENT_STATEMENT-*.CSV.gz
          destination:
          directory: /home/ubuntu/symbits/mso/files/commissions_statements/pr/
          delete_source: true
        ```
    """
    _version = "1.0.0"

    _namelist = []
    _directory = ""

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        """Init Method."""
        self._output: PurePath = None
        self._filenames: List = []
        self.delete_source: bool = False
        self._as_list: bool = kwargs.pop('as_list', False)
        self._binary_sources: dict = None
        super(UnGzip, self).__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        if self.previous and not check_empty(self.input) and getattr(self, "ignore_previous", False) is False:
            if isinstance(self.input, dict):
                self._binary_sources = self.input.get('files', {})
                return True
        await super().start(**kwargs)
        # Handle extraction settings
        if hasattr(self, "destination"):
            # New format using destination
            if isinstance(self.destination, dict) and "directory" in self.destination:
                directory = self.destination["directory"]
                if isinstance(directory, str) and "{" in directory:
                    directory = self.mask_replacement(directory)
                self._destination = Path(directory).resolve()
            else:
                directory = self.destination
                if isinstance(directory, str) and "{" in directory:
                    directory = self.mask_replacement(directory)
                self._destination = Path(directory).resolve()
        elif hasattr(self, "extract"):
            # Legacy format using extract
            for _, filename in enumerate(self.extract["filenames"]):
                filename = self.mask_replacement(filename)
                self._filenames.append(filename)
            if "directory" in self.extract:
                directory = self.extract["directory"]
                if isinstance(directory, str) and "{" in directory:
                    directory = self.mask_replacement(directory)
                self._destination = Path(directory).resolve()
            else:
                # same directory as source
                self._destination = Path(self.directory)
        else:
            # If no destination specified, use source directory
            self._destination = Path(self.directory)
        # Create destination directory if it doesn't exist
        try:
            self._destination.mkdir(parents=True, exist_ok=True)
        except Exception as err:
            logging.error(f"Error creating directory {self._destination}: {err}")
            raise ComponentError(
                f"Error creating directory {self._destination}: {err}"
            ) from err
        # For backwards compatibility
        self._output = self._destination
        return True

    async def close(self):
        pass

    async def run(self):
        # Check if file exists
        self._result = {}
        filenames = []
        if self._binary_sources:
            for filename, contents in self._binary_sources.items():
                # get binary contents:
                data = contents.get('data')
                data.seek(0)  # restarts from beginning
                # Uncompress gzip contents in memory:
                try:
                    f = await self.uncompress_gzip(
                        source=data,
                        destination=None
                    )
                    filenames.append(
                        {"filename": filename, "data": f}
                    )
                except RuntimeError as err:
                    raise FileError(f"UnGzip failed: {err}")
            self._result = filenames
        elif self._sources:
            for file in self._sources:
                if not file.exists() or not file.is_file():
                    raise FileNotFound(
                        f"Compressed File doesn't exist: {file}"
                    )
                # Uncompress the gzip/tar.gz file
                try:
                    files = await self.uncompress_gzip(
                        source=file,
                        destination=self._destination,
                        remove_source=self.delete_source,
                    )
                except (FileNotFoundError, ComponentError) as err:
                    raise FileError(f"UnGzip failed: {err}")
                except RuntimeError as err:
                    raise FileError(f"UnGzip failed: {err}")

                if self.delete_source:
                    file.unlink(missing_ok=True)

                filenames = []
                for filename in files:
                    filenames.append(filename)
                self._result[str(file)] = filenames
            if self._as_list is True:
                self._result = filenames
            self.add_metric("OUTPUT_DIRECTORY", self._destination)
        self.add_metric("FILES_UNCOMPRESS", len(filenames))
        # Support both metrics for backwards compatibility
        return self._result
