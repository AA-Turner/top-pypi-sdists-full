import asyncio
from collections.abc import Callable
import asyncssh
from ..exceptions import ComponentError, FileNotFound
from .UploadTo import UploadToBase
from ..interfaces.SSHClient import SSHClient


class UploadToSFTP(SSHClient, UploadToBase):
    """
    UploadToSFTP

        Overview

            The UploadToSFTP class is a component for uploading files or entire directories to an SSH/SFTP server.
            It supports various configurations, including recursive directory uploads, customizable transfer settings,
            and real-time upload progress tracking.

        :widths: auto

            | source         |   Yes    | A dictionary specifying the source directory, filename, and/or            |
            |                |          | recursive setting for selecting files to upload.                          |
            | destination    |   Yes    | A dictionary defining the target directory on the SFTP server.            |
            | whole_dir      |   No     | Boolean indicating if the entire source directory should be uploaded.     |
            | block_size     |   No     | Integer defining the block size for file transfer, defaults to 65356.     |
            | max_requests   |   No     | Integer setting the max number of parallel requests, defaults to 1.       |

        Returns

            This component uploads files to the specified SFTP directory and returns a list of uploaded files on success.
            If no files are found or a connection error occurs, it raises a relevant exception. Metrics on the number of
            files uploade


        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          UploadToSFTP:
          host: sftp.example.com
          port: 22
          credentials:
          username: sftpuser
          password: abcd1234
          destination:
          directory: /incoming/
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
        self.mdate = None
        self.local_name = None
        self.filename: str = ""
        self.whole_dir: bool = False
        self.preserve = True
        self.block_size: int = 65356
        self.max_requests: int = 1
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        """start Method."""
        await super(UploadToSFTP, self).start(**kwargs)
        if hasattr(self, "source"):
            self.whole_dir = (
                self.source["whole_dir"] if "whole_dir" in self.source else False
            )
        if hasattr(self, "destination"):
            self.directory = self.destination["directory"]
        try:
            if self.previous and self.input:
                self.filename = self.input
            elif self.file:
                self.filename = self.process_pattern("file")
        except (NameError, KeyError):
            pass
        return self

    def upload_progress(self, srcpath, dstpath, bytes_copied, total_bytes):
        self._pb.reset(total=total_bytes)
        self._pb.update(bytes_copied)
        self._pb.refresh()

    async def run(self):
        """Running Download file."""
        self._result = None
        status = False
        try:
            async with await self.open(
                host=self.host,
                port=self.port,
                tunnel=self.tunnel,
                credentials=self.credentials,
            ):
                async with self._connection.start_sftp_client() as sftp:
                    # check all versions of functionalities
                    args = {
                        "block_size": self.block_size,
                        "max_requests": self.max_requests,
                        "progress_handler": self.upload_progress,
                        "error_handler": self.err_handler,
                    }
                    if self.whole_dir is True:
                        self._logger.debug(
                            f"Uploading all files on directory {self.source_dir}"
                        )
                        file = "{}/*".format(self.source_dir)
                        p = self.source_dir.glob("**/*")
                        self.filename = [x for x in p if x.is_file()]
                    else:
                        file = self.filename
                    args["remotepath"] = self.directory
                    if hasattr(self, "source"):
                        args["recurse"] = True if "recursive" in self.source else False
                    if not file:
                        raise FileNotFound(f"There is no local File: {file}")
                    self.start_progress(total=len(file))
                    try:
                        self._logger.debug(f"Uploading file: {file} to {self.directory}")
                        status = await sftp.mput(file, **args)
                        self.close_progress()
                    except OSError as err:
                        self._logger.error(f"Upload SFTP local error: {err}")
                        return False
                    except asyncssh.sftp.SFTPError as err:
                        self._logger.error(f"SFTP UploadTo Server error: {err}")
                        return False
                    except asyncssh.Error as err:
                        self._logger.error(f"Upload 2 SFTP: connection failed: {err}")
                    except Exception as err:
                        self._logger.exception(err)
                        raise
        except asyncio.CancelledError:
            self._logger.info(
                f"{self.host} CANCELED~"
            )
            # break
        except (asyncio.TimeoutError, ComponentError) as err:
            raise ComponentError(f"{err!s}") from err
        except Exception as err:
            raise ComponentError(f"{err!s}") from err
        if status is False:
            return False
        else:
            self.add_metric("SFTP_FILES", self.filename)
            self._result = self.filename
            return self._result
