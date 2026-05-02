from tqdm import tqdm
from ..exceptions import FileError
from .FileBase import FileBase


class FileDelete(FileBase):
    """
    FileDelete


    Overview

        This component remove all files in a Directory.

       :widths: auto


    | file         |   Yes    | A dictionary containing two values, "pattern" and "value",        |
    |              |          | "pattern" and "value", "pattern" contains the path of the         |
    |              |          | file on the server, If it contains the mask "{value}", then       |
    |              |          | "value" is used to set the value of that mask                     |
    | pattern      |   Yes    | Allows you to replace values ( ".xls", ".csv", )                  |
    | directory    |   Yes    | The directory where are the files to delete                       |
    | value        |   Yes    | Name of the function and the arguments it receives for example    |
    |              |          | [ "current_date", { "mask":"%Y&m%d" } -> 20220909                 |
    | dictionary   |   Yes    | Path where to validate if the file exist                          |



        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          FileDelete:
          file:
          pattern: '*.csv'
          value: ''
          directory: /home/ubuntu/symbits/bayardad/files/job_advertising/bulk/
        ```
    """
    _version = "1.0.0"
    progress: bool = True

    async def run(self):
        """Delete File(s)."""
        self._result = {}
        if self.progress is True:
            filelist = list(self.get_filelist())
            with tqdm(total=len(filelist)) as pbar:
                for file in filelist:
                    # remove all files based on pattern.
                    try:
                        file.unlink(missing_ok=True)
                        self.add_metric("FILE_DELETED", file)
                        pbar.update(1)
                    except OSError as err:
                        raise FileError(
                            f"FileDelete: Error was raised when delete a File {err}"
                        ) from err
        else:
            filelist = self.get_filelist()
            for file in filelist:
                try:
                    file.unlink(missing_ok=True)
                    self.add_metric("FILE_DELETED", file)
                except OSError as err:
                    raise FileError(
                        f"FileDelete: Error was raised when delete a File {err}"
                    ) from err
        self._result = self.input  # passthroug the previous result.
        return self._result

    async def close(self):
        """Method."""
