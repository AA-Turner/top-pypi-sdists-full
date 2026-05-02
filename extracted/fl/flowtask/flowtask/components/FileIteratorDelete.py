import asyncio
from typing import Any, List
from collections.abc import Callable
from pathlib import Path, PurePath
from tqdm import tqdm
from ..exceptions import ComponentError
from .IteratorBase import IteratorBase


class FileIteratorDelete(IteratorBase):
    """
    FileIteratorDelete

    Overview

        The FileIteratorDelete class is a component for removing all files in a specified directory. It extends the
        IteratorBase class and provides methods for directory validation, file listing based on patterns, and file deletion.

    :widths: auto

        | directory        |   Yes    | The directory from which files will be deleted.                                                  |
        | _filenames       |   No     | A list to store filenames that match the pattern.                                                |
        | _path            |   No     | The Path object for the directory.                                                               |
        | pattern          |   No     | The pattern to match files for deletion.                                                         |
    Return

        The methods in this class manage the deletion of files in a specified directory, including initialization, file listing,
        and deletion.

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          FileIteratorDelete:
          # attributes here
        ```
    """
    _version = "1.0.0"

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        """Init Method."""
        # self.directory: str = None
        self._filenames: List[PurePath] = []
        self.directory: str = None
        self._path: str = None
        self.pattern = None
        super(FileIteratorDelete, self).__init__(
            loop=loop, job=job, stat=stat, **kwargs
        )

    async def start(self, **kwargs):
        """Check if Directory exists."""
        await super(FileIteratorDelete, self).start()
        if not self.directory:
            raise ComponentError(
                "FileIteratorDelete Error: need to specify a Directory", status=404
            )
        # check if directory exists
        p = Path(self.directory)
        if p.exists() and p.is_dir():
            self._path = p
        else:
            raise ComponentError(
                "FileIteratorDelete Error: Directory doesn't exist!", status=404
            )

    def get_filelist(self) -> List[Any]:
        if self.pattern:
            value = self.pattern
            if hasattr(self, "masks"):
                for mask, replace in self._mask.items():
                    value = str(value).replace(mask, replace)
            if self._variables:
                value = value.format(**self._variables)
            files = (f for f in self._path.glob(value))
        elif hasattr(self, "file"):
            # using pattern/file version
            value = self.get_filepattern()
            files = (f for f in self._path.glob(value))
        else:
            files = (f for f in self._path.iterdir() if f.is_file())
        # files = sorted(files, key=os.path.getmtime)
        return files

    async def run(self):
        if not self._path:
            return False
        iterator = list(self.get_filelist())
        with tqdm(total=len(iterator)) as pbar:
            deleted = []
            for file in iterator:
                # remove all files based on pattern.
                try:
                    file.unlink(missing_ok=True)
                    deleted.append(file)
                    pbar.update(1)
                except OSError as err:
                    raise ComponentError(
                        f"FileIteratorDelete: Error was raised when delete a File {err}"
                    ) from err
            self.add_metric("FILES_DELETED", deleted)
        self._result = self.input  # passthroug the previous result.
        return self._result

    async def close(self):
        pass
