"""
  DownloadFromSmartSheet
  Download an Excel file from SmartSheet.


        Example:

        ```yaml
        DownloadFromSmartSheet:
          comments: Download an SmartSheet Tab into an Excel file.
          file_id: '373896609326980'
          file_format: application/vnd.ms-excel
          destination:
            filename: WORP MPL 2022.xlsx
            directory: /home/ubuntu/symbits/worp/files/stores/
        ```

    """
import asyncio
from collections.abc import Callable
from pathlib import Path
from ..exceptions import ComponentError, FileNotFound
from .DownloadFrom import DownloadFromBase
from ..interfaces.smartsheet import SmartSheetClient

class DownloadFromSmartSheet(SmartSheetClient, DownloadFromBase):
    """
    DownloadFromSmartSheet

    Overview

        Download an Excel file or CSV file from SmartSheet.

    Properties (inherited from DownloadFromBase)

        :widths: auto

        | credentials        |   Yes    | Credentials to establish connection with SharePoint site (username and password) |
        |                    |          | get credentials from environment if null.                                        |
        | create_destination |   No     | Boolean flag indicating whether to create the destination directory if it        |
        |                    |          | doesn't exist (default: True).                                                   |
        | api_key            |   No     | The SmartSheet API key (can be provided as an environment variable or directly   |
        |                    |          | set as a property). If not provided, tries to use the `SMARTSHEET_API_KEY`       |
        |                    |          | environment variable.                                                            |
        | url                |   No     | Base URL for the SmartSheet Sheets API (default:                                 |
        |                    |          | https://api.smartsheet.com/2.0/sheets/).                                         |
        | file_id            |   Yes    | The ID of the SmartSheet file to download.                                       |
        | file_format        |   No     | The desired file format for the downloaded data (default:                        |
        |                    |          | "application/vnd.ms-excel"). Supported formats are:                              |
        |                    |          | * "application/vnd.ms-excel" (Excel)                                             |
        |                    |          | * "text/csv" (CSV)                                                               |
        | filename           |   Yes    | The filename to use for the downloaded file.                                     |

        Save the downloaded files on the new destination.

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          DownloadFromSmartSheet:
          comments: Download an SmartSheet Tab into an Excel file.
          file_id: '373896609326980'
          file_format: application/vnd.ms-excel
          destination:
          filename: WORP MPL 2022.xlsx
          directory: /home/ubuntu/symbits/worp/files/stores/
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
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        if self.file_format not in ["application/vnd.ms-excel", "text/csv"]:
            # only supported
            raise ComponentError(
                f"SmartSheet: Format {self.file_format} is not suported"
            )
        try:
            self.accept = (
                "text/csv" if self.file_format == "dataframe" else self.file_format
            )
        except Exception as err:
            print(err)
        await super(DownloadFromSmartSheet, self).start(**kwargs)
        return True

    async def close(self):
        pass

    async def run(self):
        self._result = None
        try:
            self._logger.info(f"Downloading SmartSheet file: {self.file_id}")
            # check if self.filename is a relative path:
            if isinstance(self.filename, str):
                self.filename = Path(self.filename)
            if not self.filename.is_absolute():
                self.filename = self.directory.joinpath(self.filename)
            if await self.download_file(file_id=self.file_id, destination=self.filename):
                self._filenames = [str(self.filename)]
                self._result = self._filenames
                self.add_metric("SMARTSHEET_FILE", self.filename)
            return self._result
        except ComponentError as err:
            raise FileNotFound(f"DownloadFromSmartSheet Error: {err}") from err
        except Exception as err:
            raise ComponentError(
                f"DownloadFromSmartSheet: Unknown Error: {err}"
            ) from err
