import asyncio
from collections import OrderedDict
from datetime import timedelta
import errno
import json
import os
import tempfile
from typing import Any, List, Optional, Tuple

import aiohttp
import click
from rich.console import Console
from rich.progress import track

from anyscale.api_utils.job_util import _get_job_run_id
from anyscale.cli_logger import BlockLogger
from anyscale.client.openapi_client.models import (
    LogDownloadConfig,
    LogDownloadRequest,
    LogDownloadResult,
    LogFileChunk,
    LogFilter,
)
from anyscale.controllers.base_controller import BaseController
from anyscale.sdk.anyscale_client.models.cluster import Cluster
from anyscale.sdk.anyscale_client.models.session_state import SessionState
from anyscale.utils.logs_utils import LogGroup


# Page size for listing bucket
DEFAULT_PAGE_SIZE = 1000

# Timeout for API Requests
DEFAULT_TIMEOUT = 30

# Timeout for Downloading Files
DEFAULT_READ_TIMEOUT = 30

DEFAULT_TTL = 14400
DEFAULT_PARALLELISM = 10

# Most users should have be able to handle this many open file descriptors,
# but add ability to override just in case.
DEFAULT_UNPACK_MAX_FILE_DESCRIPTORS = int(
    os.environ.get("ANYSCALE_LOGS_UNPACK_MAX_FILE_DESCRIPTORS", "100")
)


class LogsController(BaseController):
    def __init__(
        self, log: Optional[BlockLogger] = None, initialize_auth_api_client: bool = True
    ):
        if log is None:
            log = BlockLogger()

        super().__init__(initialize_auth_api_client=initialize_auth_api_client)
        self.log = log
        self.console = Console()
        # Track if we've already sent the unpack log message, so that we don't
        # spam the CLI output when users have had multiple sessions.
        self._unpack_log_sent = False

    def get_cluster_id_for_last_prodjob_run(self, prodjob_id: str):
        last_job_run_id = _get_job_run_id(self.anyscale_api_client, job_id=prodjob_id)
        last_job_run = self.api_client.get_decorated_job_api_v2_decorated_jobs_job_id_get(
            job_id=last_job_run_id
        )
        return last_job_run.result.cluster_id

    def render_logs(
        self, log_group: LogGroup, parallelism: int, read_timeout: timedelta, tail: int
    ):
        self._download_or_stdout(
            log_group=log_group,
            parallelism=parallelism,
            read_timeout=read_timeout,
            write_to_stdout=True,
            tail=tail,
            show_progress_bar=False,
        )

    def get_log_group(
        self,
        filter: LogFilter,  # noqa: A002
        page_size: Optional[int],
        ttl_seconds: Optional[int],
        timeout: timedelta,
    ) -> LogGroup:
        if filter.cluster_id:
            cluster: Cluster = self.anyscale_api_client.get_cluster(
                filter.cluster_id
            ).result
            if cluster.state == SessionState.RUNNING:
                self.log.warning(
                    "The latest 24 hours of logs are not guaranteed if the cluster is still running. "
                    "If so, please view logs via the Anyscale UI or Ray dashboard."
                )
        chunks, bearer_token = self._list_log_chunks(
            log_filter=filter,
            page_size=page_size,
            ttl_seconds=ttl_seconds,
            timeout=timeout,
        )
        log_group = self._group_log_chunk_list(chunks, bearer_token)
        return log_group

    def download_logs(  # noqa: PLR0913
        self,
        # Provide filters
        filter: LogFilter,  # noqa: A002
        # List files config
        page_size: int = DEFAULT_PAGE_SIZE,
        ttl_seconds: int = DEFAULT_TTL,
        timeout: timedelta = timedelta(seconds=DEFAULT_TIMEOUT),
        read_timeout: timedelta = timedelta(seconds=DEFAULT_READ_TIMEOUT),
        # Download config
        parallelism: int = DEFAULT_PARALLELISM,
        download_dir: Optional[str] = None,
        write_to_stdout: bool = False,
        unpack: bool = True,
    ) -> None:
        log_group = self.get_log_group(filter, page_size, ttl_seconds, timeout)
        self.console.log(
            f"Discovered {len(log_group.get_files())} log files across {len(log_group.get_chunks())} chunks."
        )

        self._download_or_stdout(
            download_dir=download_dir,
            read_timeout=read_timeout,
            parallelism=parallelism,
            log_group=log_group,
            show_progress_bar=True,
            write_to_stdout=write_to_stdout,
            unpack=unpack,
        )

    # TODO (shomilj): Refactor this method. It's too nested.
    def _download_or_stdout(  # noqa: PLR0913
        self,
        log_group: LogGroup,
        parallelism: int,
        read_timeout: timedelta,
        download_dir: Optional[str] = None,
        write_to_stdout: bool = False,
        tail: int = -1,
        show_progress_bar: bool = False,
        unpack: bool = True,
    ):
        if len(log_group.get_chunks()) == 0:
            return

        try:
            with tempfile.TemporaryDirectory() as tmp_dir:
                # Download all files to a temporary directory.
                asyncio.run(
                    # TODO (shomilj): Add efficient tailing method here.
                    self._download_files(
                        base_folder=tmp_dir,
                        log_chunks=log_group.get_chunks(),
                        bearer_token=log_group.bearer_token,
                        parallelism=parallelism,
                        read_timeout=read_timeout,
                        show_progress_bar=show_progress_bar,
                    )
                )

                for log_file in log_group.get_files():
                    is_tail = tail > 0
                    chunks = log_file.get_chunks(reverse=is_tail)
                    if write_to_stdout:
                        # Write to standard out
                        lines_read = 0
                        for chunk in chunks:
                            with open(
                                os.path.join(tmp_dir, chunk.chunk_name), errors="ignore"
                            ) as source:
                                if tail > 0:
                                    # Tail is enabled, so read log lines in reverse.
                                    # TODO (shomilj): Make this more efficient (don't read everything into memory before reversing it)
                                    # For now, this is fine (the chunks are <10 MB, so this isn't that inefficient).
                                    for line in reversed(source.readlines()):
                                        print(line.strip())
                                        lines_read += 1
                                        if lines_read >= tail:
                                            return
                                else:
                                    # Read log lines normally.
                                    print(source.read())
                    else:
                        # Write to destination files
                        real_path = os.path.join(
                            download_dir or "", log_file.get_target_path()
                        )
                        real_dir = os.path.dirname(real_path)
                        if not os.path.exists(real_dir):
                            os.makedirs(real_dir)

                        chunks_written = 0
                        with open(real_path, "w") as dest:
                            for chunk in chunks:
                                downloaded_chunk_path = os.path.join(
                                    tmp_dir, chunk.chunk_name
                                )
                                if not os.path.exists(downloaded_chunk_path):
                                    self.log.error(
                                        "Download failed for file: ", chunk.chunk_name
                                    )
                                    continue
                                with open(
                                    downloaded_chunk_path, errors="ignore"
                                ) as source:
                                    for line in source:
                                        dest.write(line)
                                    dest.write("\n")
                                chunks_written += 1

                        if unpack:
                            self._unpack_structured_log(real_path)

                        if chunks_written == 0:
                            os.remove(real_path)

                if not write_to_stdout:
                    if not download_dir:
                        download_dir = os.getcwd()
                    sample_chunk = log_group.get_chunks()[0]
                    cluster_id = sample_chunk.cluster_id
                    download_dir = download_dir + f"/logs/{cluster_id}"
                    self.console.log(
                        f"Download complete! Files have been downloaded to {download_dir}"
                    )
        except OSError as err:
            if err.errno == errno.EMFILE:
                raise click.ClickException(
                    "Too many open files. Try doubling your open files limit by running \n"
                    "ulimit -n $(($(ulimit -n) * 2))"
                )

    def _group_log_chunk_list(
        self, chunks: List[LogFileChunk], bearer_token: Optional[str] = None
    ) -> LogGroup:
        # This has to happen locally because it happens after we retrieve all file metadata through the paginated
        # backend API for listing S3/GCS buckets.
        group = LogGroup(bearer_token)
        for chunk in chunks:
            group.insert_chunk(chunk=chunk)
        return group

    def _list_log_chunks(
        self,
        log_filter: LogFilter,
        page_size: Optional[int],
        ttl_seconds: Optional[int],
        timeout: timedelta,
    ) -> Tuple[List[LogFileChunk], Optional[str]]:
        next_page_token: Optional[str] = None
        all_log_chunks: List[LogFileChunk] = []
        bearer_token = None

        with self.console.status("Scanning available logs...") as status:
            while True:
                request = LogDownloadRequest(
                    filter=log_filter,
                    config=LogDownloadConfig(
                        next_page_token=next_page_token,
                        page_size=page_size,
                        ttl_seconds=ttl_seconds,
                        use_bearer_token=True,
                    ),
                )
                result: LogDownloadResult = self.api_client.get_log_files_api_v2_logs_get_log_files_post(
                    log_download_request=request, _request_timeout=timeout
                ).result
                bearer_token = result.bearer_token
                all_log_chunks.extend(result.log_chunks)
                if status:
                    status.update(
                        f"Scanning available logs...discovered {len(all_log_chunks)} log file chunks."
                    )
                if (
                    result.next_page_token is None
                    or result.next_page_token == next_page_token
                ):
                    break
                next_page_token = result.next_page_token

        return all_log_chunks, bearer_token

    async def _download_file(  # noqa: PLR0913
        self,
        sem: asyncio.Semaphore,
        pos: int,  # noqa: ARG002
        file_name: str,
        url: str,
        size: int,  # noqa: ARG002
        session: aiohttp.ClientSession,
        read_timeout: timedelta,
        bearer_token: Optional[str] = None,
    ) -> None:
        async with sem:
            download_dir = os.path.dirname(file_name)
            if download_dir and not os.path.exists(download_dir):
                os.makedirs(download_dir)

            timeout = aiohttp.ClientTimeout(
                total=None, sock_connect=30, sock_read=read_timeout.seconds
            )
            headers = (
                {"Authorization": f"Bearer {bearer_token}"} if bearer_token else {}
            )
            async with session.get(url, timeout=timeout, headers=headers) as response:
                if response.status == 200:
                    with open(file_name, "wb") as fhand:
                        async for chunk in response.content.iter_chunked(1024):
                            fhand.write(chunk)
                else:
                    self.log.error(
                        f"Unable to download file {file_name}! response: [{response.status}, {await response.text()}]"
                    )

    async def _download_files(
        self,
        base_folder: Optional[str],
        log_chunks: List[LogFileChunk],
        parallelism: int,
        read_timeout: timedelta,
        show_progress_bar: bool = False,
        bearer_token: Optional[str] = None,
    ) -> List[str]:
        sem = asyncio.Semaphore(parallelism)
        downloads = []
        connector = aiohttp.TCPConnector(limit_per_host=parallelism)
        paths = []
        async with aiohttp.ClientSession(connector=connector) as session:
            for pos, log_chunk in enumerate(log_chunks):
                path = os.path.join(base_folder or "", log_chunk.chunk_name.lstrip("/"))
                paths.append(path)
                downloads.append(
                    asyncio.create_task(
                        self._download_file(
                            sem,
                            pos,
                            path,
                            log_chunk.chunk_url,
                            log_chunk.size,
                            session,
                            read_timeout,
                            bearer_token=bearer_token,
                        )
                    )
                )

            if show_progress_bar:
                for task in track(
                    asyncio.as_completed(downloads),
                    description="Downloading...",
                    total=len(downloads),
                    transient=True,
                ):
                    await task
            else:
                await asyncio.gather(*downloads)

        return paths

    def _unpack_structured_log(self, log_path: str):
        directory = os.path.dirname(log_path)
        fname = os.path.basename(log_path)
        if fname != "combined-worker.log":
            return
        if not self._unpack_log_sent:
            self.console.log("Unpacking `combined-worker.log` into separate files.")
            self._unpack_log_sent = True
        error_count = 0
        seen = set()
        with _FileDescriptorCache(DEFAULT_UNPACK_MAX_FILE_DESCRIPTORS) as fds, open(
            log_path
        ) as f:
            for line in f.readlines():
                try:
                    j = json.loads(line)
                    msg = j["message"]
                    filename = os.path.join(directory, j["filename"])

                    # Track files we've seen. The first time we see a file,
                    # we should use "wt" to overwrite previous content, for
                    # example if a user uses the download command multiple
                    # times. On subsequent times, we use "at" to append to
                    # existing content, in case the file descriptor has been
                    # closed in the meantime.
                    if filename in seen:
                        mode = "at"
                    else:
                        seen.add(filename)
                        mode = "wt"

                    f = fds.get(filename, mode)
                    f.write(f"{msg}\n")
                except KeyboardInterrupt:
                    raise
                except OSError as err:
                    if err.errno == errno.EMFILE:
                        raise
                    error_count += 1
                except Exception:  # noqa: BLE001
                    # Soft fail on unpacking the combined log. Worst case scenario,
                    # users can still parse the combined log manually
                    error_count += 1
        if error_count:
            self.log.warning(
                f"{error_count} error(s) while unpacking {fname}. Check combined-worker.log "
                "for the full contents of worker logs."
            )


class _FileDescriptorCache:
    """
    LRU Cache for file descriptors to use while uncombining worker logs, since
    opening and closing a file descriptor per line would be slow.
    """

    def __init__(self, max_entries: int):
        self.max_entries = max_entries
        # Recently used entries are near the "end"
        self.cache: OrderedDict[str, Any] = OrderedDict()

    def __enter__(self) -> "_FileDescriptorCache":
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, tb: Any):
        for f in self.cache.values():
            try:
                f.close()
            except Exception:  # noqa: BLE001
                # There's not much we can do if we fail to close a file descriptor,
                # just move on to the next one.
                continue

    def get(self, filename: str, mode: str):
        if filename in self.cache:
            # Update position in cache
            self.cache.move_to_end(filename)
            return self.cache[filename]
        if len(self.cache) >= self.max_entries:
            # Pop and close file descriptor closest to the "front"
            _, f = self.cache.popitem(last=False)
            f.close()
        self.cache[filename] = open(filename, mode)  # noqa: SIM115
        return self.cache[filename]
