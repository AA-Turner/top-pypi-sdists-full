import os
import asyncio
import logging
import posixpath
from collections.abc import Callable
from pathlib import Path, PurePosixPath
from stat import S_ISREG
from typing import Any, Optional
from tqdm import tqdm
from threading import Semaphore
import asyncssh
from asyncdb.exceptions import NoDataFound, ProviderError
from ..exceptions import ComponentError, NotSupported, FileNotFound, DataNotFound
from .IteratorBase import IteratorBase, ThreadJob
from ..interfaces.SSHClient import SSHClient
from ..interfaces.skip_policy import (
    ConsecutiveFailureTracker,
    SKIPPED_ITERATION,
)


class FileList(SSHClient, IteratorBase):
    """
    FileList with optional Parallelization Support.

    Overview

    This component iterates through a specified directory and returns a list of files based on a provided pattern or individual files.
    It supports asynchronous processing and offers options for managing empty results and detailed error handling.
    When `sftp_config` is given, the directory is scanned on a remote sFTP server instead of the local filesystem,
    and every item is the full remote path of a file (useful to feed a `DownloadFromSFTP` step).


    :widths: auto

    | directory (str)     |   Yes    | Path to the directory containing the files to be listed. Not required with `sftp_config`;             |
    |                     |          | when set in remote mode it is only forwarded to the iterated component.                               |
    | sftp_config (dict)  |    No    | List files on a remote sFTP server (connection handled by SSHClient). Keys: `host`, `port`            |
    |                     |          | (default 22), `directory` (remote directory to scan), optional `tunnel` (same shape as SSHClient)     |
    |                     |          | and the credentials: `username`, `password`, `client_keys`, `known_hosts`. `host`, `port`,           |
    |                     |          | `username` and `password` may be environment variable names.                                          |
    | pattern (str)       |    No    | Optional glob pattern for filtering files (overrides individual files if provided).                   |
    | filename (str)      |    No    | Name of the files                                                                                     |
    | iterate (bool)      |    No    | Flag indicating whether to iterate through the files and process them sequentially (defaults to True).|
    | generator (bool)    |    No    | Flag controlling the output format: `True` returns a generator, `False` (default) returns a list.     |
    | file (dict)         |    No    | A dictionary containing two values, "pattern" and "value", "pattern" and "value",                     |
    |                     |          | "pattern" contains the path of the file on the server, If it contains the mask "{value}",             |
    |                     |          | then "value" is used to set the value of that mask                                                    |
    | parallelize         |    No    | If True, the iterator will process rows in parallel. Default is False.                                |
    | num_threads         |    No    | Number of threads to use if parallelize is True. Default is 10.                                       |

    Return the list of files in a Directory


        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          FileList:
          directory: /home/ubuntu/symbits/bayardad/files/job_advertising/bulk/
          pattern: '*.csv'
          iterate: true
        ```

        ```yaml
          FileList:
            sftp_config:
              host: 10.0.22.233
              username: jlara
              client_keys: ~/.ssh/jesuslara.pem
              directory: /nfs/symbits/epson/files/sales
            pattern: '*.TXT'
            iterate: false
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
        self.generator: bool = False
        self._path = None
        self.pattern = None
        self.data = None
        self.directory: str = None
        self._num_threads: int = kwargs.pop("num_threads", 10)
        self._parallelize: bool = kwargs.pop("parallelize", False)
        self.sftp_config: Optional[dict] = kwargs.pop("sftp_config", None)
        self._remote_directory: Optional[str] = None
        if self.sftp_config:
            # sftp_config is translated into the SSHClient connection arguments.
            sftp = dict(self.sftp_config)
            self._remote_directory = sftp.pop("directory", None)
            kwargs["host"] = sftp.pop("host", None)
            kwargs["port"] = sftp.pop("port", 22)
            kwargs["tunnel"] = sftp.pop("tunnel", None)
            kwargs["credentials"] = sftp
        super(FileList, self).__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        """Check if Directory exists."""
        await super(FileList, self).start()
        if self.sftp_config:
            self.define_host()
            self.processing_credentials()
            missing = [
                key for key, value in (
                    ("host", self.host),
                    ("username", self.credentials.get("username")),
                    ("directory", self._remote_directory),
                ) if not value
            ]
            if missing:
                raise ComponentError(
                    f"FileList: sftp_config is missing required keys: {', '.join(missing)}"
                )
            if "{" in self._remote_directory:
                self._remote_directory = self.mask_replacement(self._remote_directory)
            if isinstance(self.directory, str) and "{" in self.directory:
                self.directory = self.mask_replacement(self.directory)
            return True
        if not self.directory:
            raise ComponentError("Error: need to specify a Directory")
        if isinstance(self.directory, str) and "{" in self.directory:
            self.directory = self.mask_replacement(self.directory)
            print(f"Directory: {self.directory}")
        # check if directory exists
        p = Path(self.directory)
        if p.exists() and p.is_dir():
            self._path = p
        else:
            raise ComponentError("Error: Directory doesn't exist!")
        return True

    def _get_pattern(self) -> Optional[str]:
        """Resolve the glob pattern from `pattern` or `file`.

        Returns:
            The pattern with masks and variables replaced, or None when
            neither `pattern` nor `file` is defined.
        """
        if self.pattern:
            value = self.pattern
            if "{" in value:
                value = self.mask_replacement(value)
            if self._variables:
                value = value.format(**self._variables)
            return value
        if hasattr(self, "file"):
            # using pattern/file version
            return self.get_filepattern()
        return None

    def get_filelist(self):
        value = self._get_pattern()
        if self.pattern:
            files = (f for f in self._path.glob(value))
        elif value is not None:
            files = (f for f in self._path.glob(value) if f.is_file())
        else:
            files = (f for f in self._path.iterdir() if f.is_file())
        files = sorted(files, key=os.path.getmtime)
        return files

    @staticmethod
    def _is_remote_file(attrs: asyncssh.SFTPAttrs) -> bool:
        """Return True when the sFTP attributes describe a regular file."""
        if attrs.type == asyncssh.FILEXFER_TYPE_REGULAR:
            return True
        if attrs.type == asyncssh.FILEXFER_TYPE_UNKNOWN and attrs.permissions is not None:
            return S_ISREG(attrs.permissions)
        return False

    async def get_remote_filelist(self) -> list[PurePosixPath]:
        """List the files of the remote sFTP directory.

        Returns:
            Full remote paths of the regular files matching the pattern,
            sorted by modification time (oldest first).

        Raises:
            ComponentError: if the connection fails or the remote directory
                doesn't exist.
        """
        directory = self._remote_directory
        pattern = self._get_pattern()
        await self.open(
            host=self.host,
            port=self.port,
            tunnel=self.tunnel,
            credentials=self.credentials,
        )
        try:
            async with self._connection.start_sftp_client() as sftp:
                if not await sftp.isdir(directory):
                    raise ComponentError(
                        f"FileList: remote directory {directory} doesn't exist on {self.host}"
                    )
                entries: list[Any]
                if pattern:
                    try:
                        entries = await sftp.glob_sftpname(
                            posixpath.join(directory, pattern)
                        )
                    except asyncssh.SFTPNoSuchFile:
                        entries = []
                else:
                    entries = [
                        asyncssh.SFTPName(
                            posixpath.join(directory, entry.filename), attrs=entry.attrs
                        )
                        for entry in await sftp.readdir(directory)
                    ]
        except ComponentError:
            raise
        except (OSError, asyncssh.Error) as err:
            raise ComponentError(
                f"FileList: sFTP error listing {directory} on {self.host}: {err}"
            ) from err
        finally:
            await self.close()
        files = [entry for entry in entries if self._is_remote_file(entry.attrs)]
        files.sort(key=lambda entry: entry.attrs.mtime or 0)
        return [PurePosixPath(entry.filename) for entry in files]

    async def _collect_files(self) -> list:
        """Return the file list from the sFTP server or the local directory."""
        if self.sftp_config:
            return await self.get_remote_filelist()
        return list(self.get_filelist())

    async def run(self):
        status = False
        if not self._path and not self.sftp_config:
            return False
        if self.iterate:
            files = await self._collect_files()
            step, target, params = self.get_step()
            step_name = step.name
            if self._parallelize:
                # Parallelized execution
                threads = []
                semaphore = Semaphore(self._num_threads)
                tracker = ConsecutiveFailureTracker(self.max_consecutive_failures)
                with tqdm(total=len(files)) as pbar:
                    for file in files:
                        self._result = file
                        params["filename"] = file
                        if self.directory:
                            params["directory"] = self.directory
                        job = self.get_job(target, **params)
                        if job:
                            pbar.set_description(f"Processing {file.name}")
                            thread = ThreadJob(job, step_name, semaphore)
                            threads.append(thread)
                            thread.start()
                    # wait for all threads to finish
                    results = []
                    for thread in threads:
                        thread.join()
                        # check if thread raised any exceptions
                        if thread.exc is not None:
                            if isinstance(thread.exc, (NoDataFound, DataNotFound, FileNotFound)):
                                # D3: continue INCONDICIONAL, y NO cuenta
                                # para el umbral — paridad con el camino
                                # secuencial.
                                self._logger.debug(
                                    f"Data not Found for {step_name}, got: {thread.exc}"
                                )
                                continue
                            raise thread.exc
                        # check if iteration was skipped
                        if thread.result is SKIPPED_ITERATION:
                            should_abort = tracker.record_skip(ComponentError("Skipped iteration for file"))
                            if should_abort:
                                tracker.publish(self)
                                raise ComponentError(
                                    f"FileList: Aborted due to {tracker.consecutive} consecutive failures. Last error: {tracker.last_error}"
                                ) from tracker.last_error
                        else:
                            tracker.record_success()
                            results.append(thread.result)
                        pbar.update(1)
                tracker.publish(self)
                if not results:
                    return False
                else:
                    self._result = results
                    return self._result
            else:
                # generate and iterator
                tracker = ConsecutiveFailureTracker(self.max_consecutive_failures)
                with tqdm(total=len(files)) as pbar:
                    for file in files:
                        self._result = file
                        params["filename"] = file
                        if self.directory:
                            params["directory"] = self.directory
                        logging.debug(f" :: Loading File: {file}")
                        status = False
                        job = self.get_job(target, **params)
                        if job:
                            pbar.set_description(f"Processing {file.name}")
                            try:
                                status = await self.async_job(job, step_name)
                            except (NoDataFound, DataNotFound, FileNotFound) as err:
                                # D3: continue INCONDICIONAL, y NO cuenta para el umbral.
                                self._logger.debug(f"Data not Found for {step_name}, got: {err}")
                                continue
                            except (ProviderError, ComponentError, NotSupported):
                                # async_job ya consulto skipError: si llega aqui era ENFORCE.
                                raise
                            except Exception as err:
                                raise ComponentError(
                                    f"Component Error on {step_name}, error: {err}"
                                ) from err
                            
                            if status is SKIPPED_ITERATION:
                                should_abort = tracker.record_skip(ComponentError(f"Skipped iteration for file {file.name}"))
                                if should_abort:
                                    tracker.publish(self)
                                    raise ComponentError(
                                        f"FileList: Aborted due to {tracker.consecutive} consecutive failures at file {file.name}. Last error: {tracker.last_error}"
                                    ) from tracker.last_error
                            else:
                                tracker.record_success()
                            pbar.update(1)
                tracker.publish(self)
                return tracker.successes > 0
        else:
            files = await self._collect_files()
            if files:
                if self.generator is False:
                    self._result = list(files)
                else:
                    self._result = files
                if len(self._result) < 100:
                    self.add_metric("FILE_LIST", self._result)
                self.add_metric(
                    "FILE_LIST_COUNT", len(self._result)
                )
                return self._result
            else:
                raise FileNotFound(f"FileList: No files found {files}")

    async def close(self):
        """Close the sFTP connection (and tunnel) if one is open."""
        await super(FileList, self).close()
