import os
import asyncio
import re
from typing import List
from collections.abc import Callable
import aiofiles
from botocore.exceptions import ClientError
from ..exceptions import FileError, ComponentError, FileNotFound
from .DownloadFrom import DownloadFromBase
from ..interfaces.Boto3Client import Boto3Client


class DownloadFromS3(Boto3Client, DownloadFromBase):
    """
    DownloadFromS3.

    **Overview**

        Download a file from an Amazon S3 bucket using the functionality from DownloadFrom.

    **Properties**

        :widths: auto

        | credentials        |   Yes    | Credentials to establish connection with S3 service (username and password) |
        | bucket             |   Yes    | The name of the S3 bucket to download files from.                           |
        | source_dir         |   No     | The directory path within the S3 bucket to download files from.             |
        |                    |          | Defaults to the root directory (`/`).                                       |
        | source             |   No     | A dictionary specifying the filename to download.                           |
        |                    |          | If provided, takes precedence over `source_dir` and `_srcfiles`.            |
        | _srcfiles          |   No     | A list of filenames to download from the S3 bucket.                         |
        |                    |          | Used in conjunction with `source_dir`.                                      |
        | rename             |   No     | A new filename to use for the downloaded file.                              |
        | directory          |   Yes    | The local directory path to save the downloaded files.                      |
        | create_destination |   No     | A boolean flag indicating whether to create the destination directory       |
        |                    |          | if it doesn't exist. Defaults to `True`.                                    |

        save the file on the new destination.

    **Methods**

    * start()
    * close()
    * run()
    * s3_list(s3_client, suffix="")
    * save_attachment(self, filepath, content)
    * download_file(self, filename, obj)


        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          DownloadFromS3:
          credentials:
          use_credentials: false
          region_name: us-east-2
          bucket: placer-navigator-data
          source_dir: placer-analytics/bulk-export/monthly-weekly/2025-03-06/metadata/
          destination:
          directory: /nfs/symbits/placerai/2025-03-06/metadata/
          create_destination: true
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
        self.url: str = None
        self.folder = None
        self.rename: str = None
        self.context = None
        super().__init__(
            loop=loop, job=job, stat=stat, **kwargs
        )

    async def start(self, **kwargs):
        await super(DownloadFromS3, self).start(**kwargs)
        if isinstance(self.directory, str) and "{" in self.directory:
            self.directory = self.mask_replacement(self.directory)
            print(f"Directory after mask replacement: {self.directory}")
        if hasattr(self, 'source_dir') and self.source_dir and isinstance(self.source_dir, str) and "{" in self.source_dir:
            self.source_dir = self.mask_replacement(self.source_dir)
            print(f"Source directory after mask replacement: {self.source_dir}")
        if self.source_dir and not self.source_dir.endswith("/"):
            self.source_dir = self.source_dir + "/"
        return True

    async def run(self):
        try:
            if not self.directory.exists():
                if self.create_destination is True:
                    try:
                        self.directory.mkdir(parents=True, exist_ok=True)
                    except Exception as e:
                        raise ComponentError(
                            f"S3: Error creating destination directory: {e}"
                        ) from e
                else:
                    raise ComponentError(
                        f"S3: destination directory doesn't exists: {self.directory}"
                    )
        except Exception as err:
            self._logger.error(f"S3: Error creating destination directory: {err}")
            raise ComponentError(
                f"S3: Error creating destination directory: {err}"
            ) from err
        errors = {}
        files = {}
        if not self._connection:
            await self.open(credentials=self.credentials)
        if hasattr(self, "file"):
            # find src files using get_list:
            s3_files = await self.s3_list(self._connection)
            for obj in s3_files:
                try:
                    file = obj["Key"]
                    try:
                        obj = await self._connection.get_object(
                            Bucket=self.bucket, Key=file
                        )
                    except Exception as e:
                        raise ComponentError(
                            f"S3: Error getting object from Bucket: {e}"
                        ) from e
                    result = await self.download_file(os.path.basename(file), obj)
                    if isinstance(result, BaseException):
                        errors[file] = result
                    else:
                        files[file] = result
                except Exception as e:
                    raise ComponentError(f"{e!s}") from e
        else:
            if not self._srcfiles:
                # Download all files from source_dir
                s3_files = await self.s3_list()
                files = {}
                for file in s3_files:
                    try:
                        # Extraer la Key del objeto S3
                        file_key = file["Key"] if isinstance(file, dict) else file
                        obj = await self.get_s3_object(
                            bucket=self.bucket, filename=file_key
                        )
                    except FileNotFound:
                        raise
                    except Exception as e:
                        raise ComponentError(
                            f"S3: Error getting object from Bucket: {e}"
                        ) from e
                    result = await self.download_file(os.path.basename(file_key), obj)
                    if isinstance(result, BaseException):
                        errors[file_key] = result
                    else:
                        files[file_key] = result
            else:
                for file in self._srcfiles:
                    if self.source_dir:
                        filename = f"{self.source_dir}{file}"
                    else:
                        filename = file
                    print(f"Downloading file: {filename}")
                    try:
                        self._logger.debug(f"S3: Downloading File {filename}")
                        obj = await self.get_s3_object(
                            bucket=self.bucket, filename=filename
                        )
                    except FileNotFound:
                        raise
                    except Exception as e:
                        raise ComponentError(
                            f"S3: Error getting object from Bucket: {e}"
                        ) from e
                    result = await self.download_file(file, obj)
                    if isinstance(result, BaseException):
                        errors[file] = result
                    else:
                        files[file] = result
        # at end, create the result:
        self._result = {"files": files, "errors": errors}
        self.add_metric("S3_FILES", files)
        return self._result
