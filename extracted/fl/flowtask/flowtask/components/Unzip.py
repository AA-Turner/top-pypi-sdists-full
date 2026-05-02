import os
import logging
import asyncio
from typing import List
from collections.abc import Callable
from pathlib import PosixPath, Path, PurePath
from zipfile import ZipFile, BadZipFile
from ..exceptions import FileError, ComponentError, FileNotFound
from .FileCopy import FileCopy
from ..interfaces.compress import CompressSupport


class Unzip(CompressSupport, FileCopy):
    """
    Unzip

        Overview

            The Unzip class is a component for decompressing ZIP files in specified directories.
            It supports selecting specific files within the archive, applying directory masks, and
            optionally deleting the source ZIP file after extraction.

        :widths: auto

            | filename       |   Yes    | The name of the ZIP file to decompress.                                   |
            | directory      |   Yes    | The target directory for decompression.                                   |
            | extract        |   No     | Dictionary specifying files to extract and/or target output directory.    |
            | delete_source  |   No     | Boolean indicating if the ZIP file should be deleted after extraction.    |
            | password       |   No     | Optional password for encrypted ZIP files.                                |

        Returns

            This component extracts the specified files from a ZIP archive into the target directory and
            returns a list of extracted file paths. Metrics such as the output directory and ZIP file name
            are tracked, and any errors related to file extraction or directory creation are logged for
            debugging purposes. If specified, the original ZIP file is deleted after extraction.

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          Unzip:
          # attributes here
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
        super(Unzip, self).__init__(
            loop=loop,
            job=job,
            stat=stat,
            **kwargs
        )

    async def start(self, **kwargs):
        await super().start(**kwargs)
        return True

    async def close(self):
        pass

    async def run(self):
        # Check if File exists
        self._result = {}
        for file in self._sources:
            if not file.exists() or not file.is_file():
                raise FileNotFound(
                    f"Compressed File doesn't exists: {file}"
                )
            try:
                files = await self.uncompress_zip(
                    source=file,
                    destination=self._destination,
                    source_files=self._filenames,
                    password=self.password if hasattr(self, "password") else None,
                    remove_source=self.delete_source,
                )
            except (FileNotFoundError, ComponentError) as err:
                raise FileError(
                    f"UnZip failed: {err}"
                )
            except RuntimeError as err:
                raise FileError(
                    f"UnZip failed: {err}"
                )
            if self.delete_source:
                file.unlink(missing_ok=True)

            filenames = []
            for filename in files:
                filenames.append(filename)
            self._result[str(file)] = filenames
        return self._result
