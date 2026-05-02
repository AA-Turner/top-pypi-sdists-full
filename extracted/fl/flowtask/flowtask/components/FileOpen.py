from pathlib import Path, PurePath
import io
import aiofiles
from ..exceptions import FileNotFound, FileError

from .FileBase import FileBase


class FileOpen(FileBase):
    """
    FileOpen.

        **Overview**

        This component opens one or more files asynchronously and returns their contents as streams.
        It supports handling both individual filenames and lists of filenames.
        It provides error handling for missing files or invalid file types.


        :widths: auto

    | directory (str)     |   Yes    | Path to the directory containing the files to be listed.                                              |
    | pattern (str)       |    No    | Optional glob pattern for filtering files (overrides individual files if provided).                   |
    | filename (str)      |    No    | Name of the files                                                                                     |
    | file (dict)         |    No    | A dictionary containing two values, "pattern" and "value", "pattern" and "value",                     |
    |                     |          | "pattern" contains the path of the file on the server, If it contains the mask "{value}",             |
    |                     |          | then "value" is used to set the value of that mask                                                    |

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          FileOpen:
          # attributes here
        ```
    """
    _version = "1.0.0"

    async def run(self):
        """Run File checking."""
        self._result = {}
        file = None
        if isinstance(self._filenames, list) and len(self._filenames) > 0:
            # concatenate all files in one result:
            for file in self._filenames:
                if isinstance(file, str):
                    file = Path(file)
                if file.exists() and file.is_file():
                    async with aiofiles.open(file, "r+") as afp:
                        content = await afp.read()
                        stream = io.StringIO(content)
                        stream.seek(0)
                        self._result[file.name] = stream
                else:
                    self._logger.error(f"FileExists: File doesn't exists: {file}")
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
                    stream = io.StringIO(content)
                    stream.seek(0)
                    self._result[file.name] = stream
            else:
                raise FileNotFound(f"FileExists: Empty result: {self._filenames}")
        # add metric:
        self.add_metric("FILENAME", self._filenames)
        return self._result
