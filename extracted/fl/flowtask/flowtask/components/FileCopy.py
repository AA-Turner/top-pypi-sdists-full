from typing import List
import asyncio
import shutil
import glob
from pathlib import Path
from tqdm import tqdm
from ..exceptions import FileNotFound, FileError, ComponentError
from .FileBase import FileBase
from ..utils import check_empty
from .FileList import FileList


class FileCopy(FileBase):
    """
    FileCopy

    **Overview**

        Copies files from a source directory to a destination directory.

    **Properties** (inherited from FileBase)

        :widths: auto

        | create_destination |   No     | Boolean flag indicating whether to create the destination                     |
        |                    |          | directory if it doesn't exist (default: True).                                |
        | source             |   Yes    | A dictionary specifying the source directory and filename.                    |
        |                    |          | (e.g., {"directory": "/path/to/source", "filename": "myfile.txt"})            |
        | destination        |   Yes    | A dictionary specifying the destination directory and optionally filename.    |
        |                    |          | (e.g., {"directory": "/path/to/destination", "filename": "renamed_file.txt"}) |
        | rename             |   No     | Boolean flag indicating if the file have a new name                           |
        | remove_source      |   No     | Boolean flag indicating whether to remove the source file(s) after            |
        |                    |          | copying (default: False).                                                     |



        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          FileCopy:
          source:
          filename: '*.xlsx'
          directory: /home/ubuntu/symbits/bose/stores/
          remove_source: true
          destination:
          directory: /home/ubuntu/symbits/bose/stores/backup/
        ```
    """
    _version = "1.0.0"

    progress: bool = True

    async def start(self, **kwargs) -> bool:
        """Check for File and Directory information."""
        self._sources: List = []
        self._source: str = None
        self._destination: str = None
        self._rename: bool = False
        await super(FileCopy, self).start(**kwargs)
        if hasattr(self, "move"):
            self.remove_source = self.move
        elif not hasattr(self, "remove_source"):
            self.remove_source = False
        if self.previous and not check_empty(self.input) and (not hasattr(self, "ignore_previous") or self.ignore_previous is False):
            if isinstance(self.previous, FileList):
                self._sources = self.input
                return True
        if hasattr(self, "source"):
            # processing source
            if "directory" not in self.source:
                raise ComponentError(
                    "FileCopy: Missing Source Directory."
                )
            directory = self.source["directory"]
            if isinstance(directory, str) and "{" in directory:
                directory = self.mask_replacement(directory)
            self._source = Path(directory).resolve()
            filename = self.source["filename"]
            if "*" in filename:
                # is a glob list of files
                path = self._source.joinpath(filename)
                listing = glob.glob(str(path))  # TODO using glob from pathlib
                for fname in listing:
                    self._logger.debug(f"Filename > {fname}")
                    self._sources.append(Path(fname))
            else:
                filename = self.mask_replacement(filename)
                path = self._source.joinpath(filename)
                if path.is_file():
                    self._logger.debug(f"Source Filename: {filename}")
                    self._sources.append(path)
        else:
            raise ComponentError(
                "FileCopy: Missing Source information."
            )
        if hasattr(self, "destination"):
            # processing destination
            if "directory" not in self.destination:
                raise ComponentError("FileCopy: Missing Destination Directory.")
            directory = self.destination["directory"]
            if isinstance(directory, str) and "{" in directory:
                directory = self.mask_replacement(directory)
            self._destination = Path(directory).resolve()
            if not self._destination.exists():  # create the destination directory
                self._logger.debug(
                    f"Creating new destination directory: {self._destination}"
                )
                try:
                    self._destination.mkdir(parents=True, exist_ok=True)
                except OSError as ex:
                    raise FileError(
                        f"FileCopy: Error creating destination directory: \
                        {self._destination}"
                    ) from ex
            if "filename" in self.destination:
                # this is for renaming the file:
                filename = self.destination["filename"]
                filename = self.mask_replacement(filename)
                path = self._destination.joinpath(filename)
                if self.destination["rename"] is True:
                    self._rename = True
                    self._destination = path
                    if path.is_file():
                        self._logger.warning(
                            f"FileCopy: Warning, File {path} already exists,\
                            will be overwritten"
                        )
                else:
                    self._rename = False
                    if path.is_file():
                        self._logger.warning(
                            f"FileCopy: Warning, File {path} already exists, \
                            will be overwritten"
                        )
            else:
                filename = None
                self._rename = False
        else:
            raise FileNotFound(
                "FileCopy: Missing Destination."
            )
        return True

    async def run(self):
        """
        Delete File(s).
        """
        self._result = {}
        print(f"::::: FileCopy: {self._sources}")
        if self.progress is True:
            with tqdm(total=len(self._sources)) as pbar:
                for file in self._sources:
                    if self._rename is True:
                        destination = self._destination
                    else:
                        destination = self._destination.joinpath(file.name)
                    if self.remove_source is True:
                        await asyncio.to_thread(shutil.move, file, destination)
                    else:
                        await asyncio.to_thread(shutil.copyfile, file, destination)
                    pbar.update(1)
                    self._result[file.name] = destination
        else:
            for file in self._sources:
                if self._rename is True:
                    destination = self._destination
                else:
                    destination = self._destination.joinpath(file.name)
                if self.remove_source is True:
                    await asyncio.to_thread(shutil.move, file, destination)
                else:
                    await asyncio.to_thread(shutil.copyfile, file, destination)
                self._result[file.name] = destination
        self.add_metric("FILES_COPIED", self._result)
        return self._result

    async def close(self):
        """Method."""
