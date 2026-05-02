import os
import asyncio
from pathlib import Path
from ..exceptions import FileNotFound, FileError, ComponentError
from .FileBase import FileBase


class FileRename(FileBase):
    """
    FileRename.

    **Overview**

    This component renames a file asynchronously based on provided source and destination paths.
    It supports handling missing files and offers optional behavior for ignoring missing source files.
    It performs basic validation to ensure the destination doesn't overwrite existing files.


    :widths: auto

    | directory (str)          |   Yes    | Path to the directory containing the source file.                                                 |
    | destination (str)        |   Yes    | New filename (with optional variable replacement using `set_variables` and `mask_replacement`)    |
    |                          |          | for the file.                                                                                     |
    | ignore_missing (bool)    |    No    | Flag indicating whether to ignore missing source files (defaults to False).                       |
    | source (str)             |   Yes    | Filename (with optional variable replacement using `set_variables` and `mask_replacement`)        |
    |                          |          | of the file to rename.                                                                            |




        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          FileRename:
          Group: ICIMSRename
          ignore_missing: true
          directory: /home/ubuntu/symbits/icims/files/forms/
          source: '{form_id}_{form_data_id}.txt'
          destination: '{form_id}_{form_data_id}_{associate_id} - {full_name}.txt'
        ```
    """
    _version = "1.0.0"

    async def start(self, **kwargs) -> bool:
        """Check for File and Directory information."""
        self._source: str = None
        self._destination: str = None
        if not hasattr(self, "ignore_missing"):
            self.ignore_missing = False
        if not hasattr(self, "directory"):
            raise ComponentError("Missing Source Directory.")
        if isinstance(self.directory, str):
            self.directory = Path(self.directory).resolve()
        if hasattr(self, "source"):
            # processing source
            filename = self.set_variables(self.mask_replacement(self.source))
            self._logger.notice(f"Source File {filename}")
            path = self.directory.joinpath(filename)
            if "*" in filename:
                raise ComponentError(
                    "FileRename: Cannot Support wildcard on filenames."
                )
            else:
                if path.is_file():
                    self._logger.debug(f"Source Filename: {filename}")
                    self._source = path
                else:
                    if self.ignore_missing is False:
                        raise FileNotFound(f"File {path} was not found.")
        else:
            raise ComponentError("FileRename: Missing Source information.")
        if hasattr(self, "destination"):
            # processing destination
            filename = self.set_variables(self.mask_replacement(self.destination))
            path = self.directory.joinpath(filename)
            if (
                self._source and path.exists()
            ):  # we cannot rename a file overwriting another.
                raise FileError(f"Cannot Rename to {filename}, file Exists")
            self._destination = path
        else:
            raise FileNotFound("FileRename: Missing Destination.")
        await super(FileRename, self).start(**kwargs)
        return True

    async def run(self):
        """Delete File(s)."""
        self._result = {}
        if self._source is not None and self._source.exists():
            await asyncio.to_thread(os.rename, self._source, self._destination)
            self._result[self._source] = self._destination
            self.add_metric("FILE_RENAMED", self._result)
        if self.ignore_missing is False:
            raise FileNotFound(f"Source File {self._source} was not found.")
        return self._result

    async def close(self):
        """Method."""
