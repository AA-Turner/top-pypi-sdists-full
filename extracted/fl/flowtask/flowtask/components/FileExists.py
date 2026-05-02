import logging
from pathlib import Path, PurePath
from ..exceptions import FileNotFound, FileError, ComponentError
from .FileBase import FileBase


class FileExists(FileBase):
    """
    FileExists
     Overview

        This component validate if a file or a list of files exist in a directory.

       :widths: auto


    | file         |   Yes    | A dictionary containing two values, "pattern" and "value",        |
    |              |          | "pattern" and "value", "pattern" contains the path of the         |
    |              |          | file on the server, If it contains the mask "{value}", then       |
    |              |          | "value" is used to set the value of that mask                     |
    | pattern      |   Yes    | Allows you to replace values ( ".xls", ".csv"  )                  |
    | value        |   No     | Name of the function and the arguments it receives for example    |
    |              |          | [ "current_date", { "mask":"%Y&m%d" } -> 20220909                 |
    | mask         |   No     | A mask is applied with the today attribute, with date format      |
    |              |          | {“Y-m-d”}                                                         |
    | directory    |   Yes    | Path to validate if the file exists                               |
    | date         |   No     | File date                                                         |
    | diff         |   No     | Evaluate the difference in the file                               |
    | depens       |   No     | The file depends on a previous process                            |
    | filename     |   Yes    | Identify the file name                                            |

      Return the validation if the file exist or not



        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          FileExists:
          file:
          pattern: '{value}-adp_worker.csv'
          value:
          - today
          - mask: '%Y-%m-%d'
          directory: /home/ubuntu/symbits/walmart/files/adfs/
        ```
    """
    _version = "1.0.0"

    async def run(self):
        """Run File checking."""
        self._result = {}
        file = None
        if isinstance(self._filenames, list) and len(self._filenames) > 0:
            if hasattr(self, "last_file") or hasattr(self, "first_file"):
                # only return the last/first file of the list
                if hasattr(self, "first_file"):
                    file = self._filenames[0]
                else:
                    file = self._filenames[-1]
                if file.exists() and file.is_file():
                    self._result[file] = True
                    self.setTaskVar("DIRECTORY", file.parent)
                    self.setTaskVar("FILENAME", str(file.name))
                    self.setTaskVar("FILEPATH", self._path)
                    if self._debug:
                        logging.debug(f"fileExists> {file}")
                else:
                    raise FileNotFound(f"FileExists: File doesn't exists: {file}")
            else:
                # processing a list of files
                for file in self._filenames:
                    logging.debug(f" ::: Checking for File: {file}")
                    if isinstance(file, dict) and "filename" in file:
                        file = file["filename"]
                    if isinstance(file, str):
                        file = Path(file)
                    if file.exists() and file.is_file():
                        self._result[file] = True
                        if self._debug:
                            logging.debug(f"fileExists> {file}")
                        filename = Path(file)
                        self.setTaskVar("DIRECTORY", filename.parent)
                        self.setTaskVar("FILENAME", str(filename.name))
                        self.setTaskVar("FILEPATH", filename)
                    else:
                        raise FileNotFound(f"FileExists: File doesn't exists: {file}")
        elif isinstance(self._filenames, dict):
            for _, val in self._filenames.items():
                if "file" in val:
                    file = val["file"]
                elif "filename" in val:
                    file = val["filename"]
                else:
                    raise ComponentError(f"FileExists: Wrong Inherit format: {val!r}")
                if isinstance(file, str):
                    file = Path(file)
                elif isinstance(file, PurePath):
                    file = file.resolve()
                else:
                    raise FileError(
                        f"FileExists: unrecognized type for Filename: {type(file)}"
                    )
                logging.debug(f" ::: Checking for File: {file}")
                if file.exists() and file.is_file():
                    self._result[file] = True
                    self.setTaskVar("DIRECTORY", file.parent)
                    self.setTaskVar("FILENAME", str(file.name))
                    self.setTaskVar("FILEPATH", file)
                else:
                    raise FileNotFound(f"FileExists: Empty result: {file}")
        elif hasattr(self, "filename"):
            if isinstance(self.filename, str):
                file = Path(self.filename)
            elif isinstance(self.filename, PurePath):
                file = self.filename.resolve()
            else:
                raise FileError(
                    f"FileExists: unrecognized type for Filename: {type(self.filename)}"
                )
            logging.debug(f" ::: Checking for File: {file}")
            if file.exists() and file.is_file():
                self._result[file] = True
                self.setTaskVar("DIRECTORY", file.parent)
                self.setTaskVar("FILENAME", str(file.name))
                self.setTaskVar("FILEPATH", file)
            else:
                print("RAISE THIS >> ")
                raise FileNotFound(f"FileExists: Empty result: {file}")
        # add metric:
        self.add_metric("FILENAME", self._filenames)
        return self._result

    async def close(self):
        """Method."""
