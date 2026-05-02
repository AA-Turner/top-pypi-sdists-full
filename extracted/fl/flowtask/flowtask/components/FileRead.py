from collections.abc import Callable
import asyncio
from pathlib import Path, PurePath
import io
import aiofiles
from ..exceptions import FileNotFound, FileError
from ..utils.json import json_decoder
from .FileBase import FileBase
from ..interfaces.dataframes.pandas import PandasDataframe


class FileRead(FileBase, PandasDataframe):
    """
    FileRead.

        **Overview**

        Read an String File and returned as string (non-binary)


        :widths: auto

    | directory (str)     |   Yes    | Path to the directory containing the files to be listed.                                              |
    | pattern (str)       |    No    | Optional glob pattern for filtering files (overrides individual files if provided).                   |
    | filename (str)      |    No    | Name of the files                                                                                     |
    | file (dict)         |    No    | A dictionary containing two values, "pattern" and "value", "pattern" and "value",                     |
    |                     |          | "pattern" contains the path of the file on the server, If it contains the mask "{value}",             |
    |                     |          | then "value" is used to set the value of that mask                                                    |



        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          FileRead:
          file: recap_response_payloads.json
          directory: recaps/
          is_json: true
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
        self._use_taskstorage = kwargs.get('use_taskstorage', False)
        super(FileRead, self).__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def close(self):
        """Method."""

    async def start(self, **kwargs):
        """Check for File and Directory information."""
        if not hasattr(self, "directory"):
            if self._use_taskstorage:
                self.directory = self._taskstore.get_path().joinpath(self._program, 'files')
            else:
                self.directory = self._filestore.get_directory('')
        await super().start(**kwargs)
        return True

    async def run(self):
        """Run File checking."""
        self._result = {}
        file = None
        result = ""
        if isinstance(self._filenames, list) and len(self._filenames) > 0:
            # concatenate all files in one result:
            for file in self._filenames:
                if isinstance(file, str):
                    file = Path(file)
                if file.exists() and file.is_file():
                    async with aiofiles.open(file, "r+") as afp:
                        content = await afp.read()
                        result += content
                else:
                    self._logger.error(
                        f"FileExists: File doesn't exists: {file}"
                    )
        elif hasattr(self, "filename"):
            if isinstance(self.filename, str):
                file = Path(file)
            elif isinstance(self.filename, PurePath):
                file = self.filename.resolve()
            else:
                raise FileError(
                    f"FileExists: unrecognized type for Filename: {type(self.filename)}"
                )
            if file.exists() and file.is_file():
                async with aiofiles.open(file, "r+") as afp:
                    content = await afp.read()
                    result = result + content
            else:
                raise FileNotFound(f"FileExists: Empty result: {self._filenames}")
        # add metric:
        if hasattr(self, 'is_json'):
            try:
                result = json_decoder(result)
            except Exception as exc:
                self._logger.error(
                    f":: Error decoding JSON: {exc}"
                )
                return None
        if getattr(self, 'as_dataframe', False):
            result = await self.create_dataframe(result)
        self._result = result
        self.add_metric("FILENAMES", self._filenames)
        return self._result
