"""
  DownloadFromSmartSheet
  Download an Excel file from SmartSheet.


        Example:

        ```yaml
        DownloadFromFTP:
          host: trendmicro_host
          port: trendmicro_port
          use_tls: false
          file:
            pattern: '{monday}.*-Limited852StoreReport.{saturday}.csv'
            values:
              monday:
              - date_dow
              - day_of_week: monday
                mask: '%Y%m%d'
              saturday:
              - date_diff_dow
              - diff: 7
                day_of_week: saturday
                mask: '%Y-%m-%d'
            directory: /Limited852Report
          credentials:
            user: trendmicro_user
            password: trendmicro_password
          download:
            directory: /home/ubuntu/symbits/trendmicro/files/market_share/
        ```

    """
import re
import asyncio
from pathlib import Path
from ..exceptions import ComponentError, FileError
from .DownloadFrom import DownloadFromBase
from ..interfaces.FTPClient import FTPClient


class DownloadFromFTP(FTPClient, DownloadFromBase):
    """
    DownloadFromFTP

    Overview

        Downloads files from a remote FTP server using the functionality from DownloadFrom.

    Properties

        :widths: auto

    | credentials  |   Yes    | Dictionary containing username and password for FTP authentication.|
    |              |          | (default: {"user": str, "password": str})                          |
    | whole_dir    |   Yes    | Boolean flag indicating whether to download the entire directory   |
    |              |          | or specific files. (default: False)                                |
    | use_tls      |   Yes    | Boolean for indicate if we need to use the TLS protocol            |

    Save the downloaded files on the new destination.

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          DownloadFromFTP:
          host: trendmicro_host
          port: trendmicro_port
          use_tls: false
          file:
          pattern: '{monday}.*-Limited852StoreReport.{saturday}.csv'
          values:
          monday:
          - date_dow
          - day_of_week: monday
          mask: '%Y%m%d'
          saturday:
          - date_diff_dow
          - diff: 7
          day_of_week: saturday
          mask: '%Y-%m-%d'
          directory: /Limited852Report
          credentials:
          user: trendmicro_user
          password: trendmicro_password
          download:
          directory: /home/ubuntu/symbits/trendmicro/files/market_share/
        ```
    """
    _version = "1.0.0"
    _credentials: dict = {"user": str, "password": str}

    async def start(self, **kwargs):
        await super().start(**kwargs)
        self._path: str = None
        self.whole_dir: bool = False
        if hasattr(self, "source"):
            if "algorithms" in self.source:
                self.algorithms.append(self.source["algorithms"])
            # change filosophy of source/destination
            self.whole_dir = (
                self.source["whole_dir"] if "whole_dir" in self.source else False
            )
        await super(DownloadFromFTP, self).start(**kwargs)
        if hasattr(self, "download"):
            self.directory = Path(self.download["directory"])
        return True

    async def download_files(self):
        try:
            self._connection = await self.init_connection(
                self.host, self.port, credentials=self.credentials, ssl=self.ssl
            )
        except asyncio.CancelledError:
            self._logger.info(f"{self.host} CANCELED~")
            # break
        except ComponentError:
            raise
        except (TimeoutError, asyncio.TimeoutError) as ex:
            raise ComponentError(f"Timeout: {ex}") from ex
        except Exception as err:
            raise ComponentError(f"DownloadFromFTP Error: {err}") from err
        if self._connection:
            if not await self.directory_exists(self.source_dir):
                raise ComponentError(f"FTP Directory doesn't exists: {self.source_dir}")
            try:
                await self.change_directory(self.source_dir)
            except Exception as err:
                raise ComponentError(
                    f"FTP Unable to connect to: {self.source_dir}, error: {err}"
                ) from err
            # getting stats for directory
            filelist = []
            files = []
            stats = await self._connection.list(
                self.source_dir, recursive=False, raw_command="MLSD"
            )
            pbar = self.start_pbar(total=len(stats))
            if self.whole_dir is True:
                await self.download_file(
                    file=self.source_dir, destination=self.directory
                )
                for path, info in stats:
                    if info["type"] == "file":
                        file = {"filename": path, **info}
                        # all files downloaded:
                        pbar.update(1)
                        files.append(file)
                        filelist.append(path)
                self.add_metric("FTP_FILES", files)
                pbar.close()
            else:
                if self.source_file is not None:
                    self._srcfiles = [self.source_file]
                for file in self._srcfiles:
                    # Extract filename from dictionary if it's a dict, otherwise use as is
                    if isinstance(file, dict):
                        filename = file.get('filename')
                        if not filename:
                            raise ComponentError(f"File entry without filename: {file}")
                        file = filename
                    else:
                        file = str(file)
                    
                    if not self.source_dir.endswith("/"):
                        self.source_dir = "{}/".format(self.source_dir)
                    pattern = re.compile(f"^{self.source_dir}{file}+$")
                    self._logger.debug(f"Calculated Pattern for lookup {pattern}")
                    for path, info in stats:
                        if info["type"] == "file":
                            # first case, match the extension:
                            if hasattr(self, "source"):
                                if "suffix" in self.source:
                                    # download all files match with suffix:
                                    if path.suffix == self.source["suffix"]:
                                        file = {"filename": path, **info}
                                        await self.download_file(
                                            file=path, destination=self.directory
                                        )
                                        files.append(file)
                                        filelist.append(path)
                            elif pattern.match(str(path)):
                                self._logger.debug(f"Looking for matching file {path}")
                                file = {"filename": path, **info}
                                files.append(file)
                                filelist.append(path)
                                # using regex to check file
                                await self.download_file(
                                    file=path, destination=self.directory
                                )
                            pbar.update(1)
                            pbar.set_description(f"Processing {path}")
                self.add_metric("FTP_FILES", files)
                pbar.close()
            self._result = ["{}/{}".format(self.directory, v.name) for v in filelist]
            print(self._result)
            return True
        else:
            return False

    async def run(self):
        self._result = None
        if self._debug:
            self._logger.info(f"Downloading FTP files: {self._filenames}")
        try:
            status = await self.download_files()
        except (ComponentError, Exception) as err:
            self._logger.error(err)
            raise
        if not status:
            raise FileError(f"File(s) Not Found: {self.source_file}")
        return self._result
