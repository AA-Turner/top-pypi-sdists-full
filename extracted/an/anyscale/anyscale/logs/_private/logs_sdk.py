import base64
import binascii
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from itertools import islice
import json
import os
from typing import Any, Dict, Iterator, List, Optional, Tuple

from anyscale._private.sdk.base_sdk import BaseSDK
from anyscale.client.openapi_client.models import LogDownloadResult, LogFileChunk
from anyscale.controllers.logs_controller import (
    DEFAULT_PARALLELISM,
    DEFAULT_READ_TIMEOUT,
    LogsController,
)
from anyscale.logs.models import (
    LOG_TYPES,
    LogChunk,
    LogFileLine,
    LogFilesFilter,
    LogFilesPage,
    LogLine,
    LogLinesPage,
    LogsResource,
    MAX_LINES_PER_PAGE,
)
from anyscale.utils.logs_utils import LogGroup


# What the SDK calls a resource -> the query parameter the backend expects. Exactly one
# is sent; the backend resolves it to the cloud, checks permission, and pins the query's
# stream selector to that resource.
_RESOURCE_PARAM: Dict[str, str] = {
    "cluster": "cluster_id",
    "workspace": "workspace_id",
    "job": "ha_job_id",
    "service": "service_id",
}

# The backend caps one query at this many lines (`limit`, le=1000).
MAX_LIMIT = 1000
DEFAULT_LIMIT = 400


# What the CLI/SDK calls a resource -> what the backend's files route calls the same thing.
_ENTITY_TYPE_ON_THE_WIRE: Dict[str, str] = {
    "job": "production_job",
    "service": "service",
    "workspace": "workspace",
    "cluster": "session",
}

# What the CLI/SDK calls a node type <-> the backend's NodeType values.
_NODE_TYPE_ON_THE_WIRE: Dict[str, str] = {"head": "head-node", "worker": "worker-nodes"}
_NODE_TYPE_FROM_THE_WIRE: Dict[str, str] = {
    wire: ours for ours, wire in _NODE_TYPE_ON_THE_WIRE.items()
}

# `read` and `read_page` stop after this many lines unless told otherwise.
DEFAULT_MAX_LINES = 1000

_READ_TOKEN_PREFIX = "lines1_"


@dataclass(frozen=True)
class _ReadCursor:
    """Where a `read_page` stopped: the next page starts at the line after it.

    Encoded into the page token, so the token alone carries the position; the filter is
    passed again by the caller, the same way `anyscale.events.list_page` works.
    """

    # The backend token that lists the page holding `chunk_name`; None for the first page.
    page_token: Optional[str]
    # Full bucket name of the chunk the last line came from.
    chunk_name: str
    # A line boundary in that chunk, counted from its top: oldest first resumes at
    # lines[line:], newest first at lines[:line] read backwards. Counting from the top
    # keeps the boundary right when a live chunk grows at the bottom.
    line: int
    newest_first: bool

    def encode(self) -> str:
        payload = json.dumps(
            {"p": self.page_token, "c": self.chunk_name, "l": self.line, "n": self.newest_first},
            separators=(",", ":"),
        )
        return _READ_TOKEN_PREFIX + base64.urlsafe_b64encode(payload.encode()).decode()

    @classmethod
    def decode(cls, token: str) -> "_ReadCursor":
        invalid = ValueError("page_token is not a token returned by an earlier read_page.")
        if not isinstance(token, str) or not token.startswith(_READ_TOKEN_PREFIX):
            raise invalid
        try:
            raw = json.loads(base64.urlsafe_b64decode(token[len(_READ_TOKEN_PREFIX) :]))
            cursor = cls(
                page_token=raw["p"], chunk_name=raw["c"], line=raw["l"], newest_first=raw["n"]
            )
        except (binascii.Error, ValueError, TypeError, KeyError):
            raise invalid from None
        if (
            not (cursor.page_token is None or isinstance(cursor.page_token, str))
            or not isinstance(cursor.chunk_name, str)
            or not isinstance(cursor.line, int)
            or isinstance(cursor.line, bool)
            or cursor.line < 0
            or not isinstance(cursor.newest_first, bool)
        ):
            raise invalid
        return cursor


class PrivateLogsSDK(BaseSDK):
    def query(  # noqa: PLR0913
        self,
        logql_query: str,
        resource: LogsResource,
        *,
        start: datetime,
        end: datetime,
        log_type: str = "application",
        limit: int = DEFAULT_LIMIT,
        newest_first: bool = True,
    ) -> List[LogLine]:
        """Lines of `resource` matching `logql_query` within [start, end].

        At most `limit` lines come back; `newest_first` reads from the end of the window
        backwards (the newest `limit` lines, newest first), else from the start forwards.
        """
        if log_type not in LOG_TYPES:
            raise ValueError(f"log_type must be one of {LOG_TYPES}, got {log_type!r}.")
        if not 1 <= limit <= MAX_LIMIT:
            raise ValueError(f"limit must be between 1 and {MAX_LIMIT}, got {limit}.")
        start_ns, end_ns = _epoch_ns(start), _epoch_ns(end)
        if end_ns <= start_ns:
            raise ValueError("end must be after start.")

        batch = self.client.query_logs(
            logql_query=logql_query,
            resource={_RESOURCE_PARAM[resource.resource_type]: resource.resource_id},
            start_ns=start_ns,
            end_ns=end_ns,
            source_type=log_type,
            limit=limit,
            reverse_sort=newest_first,
        )
        return [_to_line(item) for item in batch.items or []]

    def list_files(self, files_filter: LogFilesFilter) -> LogFilesPage:
        """One page of the chunks matching `files_filter`, oldest first."""
        page = self._list_page(files_filter, files_filter.next_page_token)
        return LogFilesPage(
            chunks=[_to_chunk(chunk) for chunk in page.log_chunks or []],
            next_page_token=page.next_page_token,
            bearer_token=page.bearer_token,
        )

    def download(
        self,
        files_filter: LogFilesFilter,
        *,
        download_dir: Optional[str] = None,
        unpack: bool = True,
        parallelism: int = DEFAULT_PARALLELISM,
    ) -> str:
        """Write every chunk matching `files_filter` under `download_dir`, mirroring the
        bucket layout, and return that directory's absolute path.

        Pages through the whole listing unless `files_filter.latest` is set, in which case
        only the newest page is written.
        """
        group = LogGroup()
        for page in self._pages(files_filter):
            group.bearer_token = page.bearer_token or group.bearer_token
            for chunk in page.log_chunks or []:
                group.insert_chunk(chunk)

        target = os.path.abspath(download_dir or os.getcwd())
        chunks = group.get_chunks()
        if not chunks:
            self.logger.info("No log files matched.")
            return target
        self.logger.info(
            f"Downloading {len(group.get_files())} log files ({len(chunks)} chunks) to {target}."
        )
        # The controller already streams chunks to disk, joins them per file, unpacks
        # combined-worker.log and reports disk-space errors; only its listing is bypassed.
        LogsController(log=self.logger, initialize_auth_api_client=False)._download_or_stdout(  # noqa: SLF001
            log_group=group,
            parallelism=parallelism,
            read_timeout=timedelta(seconds=DEFAULT_READ_TIMEOUT),
            download_dir=target,
            write_to_stdout=False,
            show_progress_bar=True,
            unpack=unpack,
        )
        return target

    def read(
        self,
        files_filter: LogFilesFilter,
        *,
        max_lines: int = DEFAULT_MAX_LINES,
        parallelism: int = DEFAULT_PARALLELISM,
    ) -> List[LogFileLine]:
        """At most `max_lines` lines of the files matching `files_filter`.

        With `files_filter.latest` the newest chunks are read first and each chunk's lines
        come newest first, so the result is the end of the logs read backwards; otherwise
        reading starts at the first chunk and lines come oldest first. Only the chunks
        needed to fill the budget are downloaded.
        """
        _check_max_lines(max_lines)
        return [
            line for line, _ in islice(self._lines(files_filter, None, parallelism), max_lines)
        ]

    def read_page(
        self,
        files_filter: LogFilesFilter,
        *,
        max_lines: int = DEFAULT_MAX_LINES,
        page_token: Optional[str] = None,
        parallelism: int = DEFAULT_PARALLELISM,
    ) -> LogLinesPage:
        """One page of at most `max_lines` lines, from `page_token` on, and a next token.

        Lines come in the same order as `read`. The next token is set only when at least
        one more line exists.
        """
        _check_max_lines(max_lines)
        if max_lines > MAX_LINES_PER_PAGE:
            raise ValueError(
                f"max_lines must be at most {MAX_LINES_PER_PAGE} for one page, got {max_lines}."
            )
        cursor = None
        if page_token is not None:
            if files_filter.next_page_token is not None:
                raise ValueError("Pass page_token or files_filter.next_page_token, not both.")
            cursor = _ReadCursor.decode(page_token)
            if cursor.newest_first != files_filter.latest:
                raise ValueError(
                    "page_token was returned by a read with latest="
                    f"{cursor.newest_first}; read it with the same filter."
                )

        taken: List[Tuple[LogFileLine, _ReadCursor]] = []
        for item in self._lines(files_filter, cursor, parallelism):
            if len(taken) == max_lines:
                # One more line exists, so the next page starts right after the last one
                # returned. Peeking at it may download one more batch of chunks.
                return LogLinesPage(
                    lines=[line for line, _ in taken], next_page_token=taken[-1][1].encode()
                )
            taken.append(item)
        return LogLinesPage(lines=[line for line, _ in taken])

    def _lines(
        self, files_filter: LogFilesFilter, cursor: Optional[_ReadCursor], parallelism: int
    ) -> Iterator[Tuple[LogFileLine, _ReadCursor]]:
        """Every line of the matching files in reading order, from `cursor` on, each with
        the cursor that resumes right after it. Chunks are downloaded a batch at a time, as
        the lines are consumed."""
        newest_first = files_filter.latest
        page_token = cursor.page_token if cursor else files_filter.next_page_token
        while True:
            page = self._list_page(files_filter, page_token)
            chunks = list(page.log_chunks or [])
            if newest_first:
                chunks.reverse()
            resume_at: Optional[int] = None
            if cursor is not None:
                names = [chunk.chunk_name for chunk in chunks]
                if cursor.chunk_name not in names:
                    raise ValueError(
                        "page_token no longer matches the log files: the chunk it points to "
                        "is not in the listing any more. Start again without it."
                    )
                chunks = chunks[names.index(cursor.chunk_name) :]
                resume_at = cursor.line
                cursor = None
            for start in range(0, len(chunks), parallelism):
                batch = chunks[start : start + parallelism]
                texts = self.client.download_log_chunks(
                    batch, bearer_token=page.bearer_token, parallelism=parallelism
                )
                for chunk, text in zip(batch, texts):
                    chunk_lines = text.splitlines()
                    for index in _line_order(len(chunk_lines), resume_at, newest_first):
                        line = LogFileLine(
                            file_name=chunk.file_name,
                            node_ip=chunk.node_ip or None,
                            instance_id=chunk.instance_id or None,
                            line=chunk_lines[index],
                        )
                        after = _ReadCursor(
                            page_token=page_token,
                            chunk_name=chunk.chunk_name,
                            line=index if newest_first else index + 1,
                            newest_first=newest_first,
                        )
                        yield line, after
                    # Only the cursor's own chunk starts part-way.
                    resume_at = None
            page_token = page.next_page_token
            if newest_first or not page_token:
                return

    def _pages(self, files_filter: LogFilesFilter) -> Iterator[LogDownloadResult]:
        """Every page from `files_filter.next_page_token` on; one page under `latest`."""
        token = files_filter.next_page_token
        while True:
            page = self._list_page(files_filter, token)
            yield page
            token = page.next_page_token
            if files_filter.latest or not token:
                return

    def _list_page(self, files_filter: LogFilesFilter, token: Optional[str]) -> LogDownloadResult:
        node_type = files_filter.node_type
        return self.client.list_log_files(
            entity_type=_ENTITY_TYPE_ON_THE_WIRE[files_filter.entity_type],
            entity_id=files_filter.entity_id,
            log_type=files_filter.log_type,
            latest=files_filter.latest,
            page_size=files_filter.page_size,
            next_page_token=token,
            job_run=files_filter.job_run,
            service_version=files_filter.service_version,
            ray_session=files_filter.ray_session,
            node_type=_NODE_TYPE_ON_THE_WIRE[node_type] if node_type else None,
            node_ip=files_filter.node_ip,
            instance_id=files_filter.instance_id,
            glob=files_filter.glob,
            start_time=files_filter.start_time,
            end_time=files_filter.end_time,
        )


def _epoch_ns(value: datetime) -> int:
    # A naive datetime is taken as UTC, matching the CLI's time flags.
    aware = value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    return int(aware.timestamp() * 1_000_000_000)


def _to_line(item: Any) -> LogLine:
    """A generated `LogItem` -> model.

    The backend's payload is the line parsed as JSON (or ``{"message": line}`` for plain
    text), merged with the stream's labels; `message` becomes the line's text and the
    rest its fields. A JSON line without a `message` key keeps its whole object as text,
    so nothing is lost.
    """
    fields: Dict[str, Any] = dict(item.payload or {})
    message = fields.pop("message", None)
    if message is None:
        message = json.dumps(fields, sort_keys=True)
    return LogLine(
        timestamp=datetime.fromtimestamp(item.timestamp_ns / 1_000_000_000, tz=timezone.utc),
        message=str(message),
        fields=fields,
    )


def _check_max_lines(max_lines: int) -> None:
    if not isinstance(max_lines, int) or isinstance(max_lines, bool) or max_lines < 1:
        raise ValueError(f"max_lines must be a positive integer, got {max_lines!r}.")


def _line_order(count: int, resume_at: Optional[int], newest_first: bool) -> range:
    """Indexes of a chunk's lines in reading order, starting at a cursor boundary if any."""
    if newest_first:
        stop = count if resume_at is None else min(resume_at, count)
        return range(stop - 1, -1, -1)
    return range(resume_at or 0, count)


def _to_chunk(raw: LogFileChunk) -> LogChunk:
    node_type: Any = raw.node_type
    return LogChunk(
        cluster_id=raw.cluster_id,
        ray_session=raw.session_id,
        node_type=_NODE_TYPE_FROM_THE_WIRE.get(str(node_type), "unknown"),
        # Driver and webterminal logs belong to no node; the backend sends "" for them.
        node_ip=raw.node_ip or None,
        instance_id=raw.instance_id or None,
        file_name=raw.file_name,
        chunk_name=raw.chunk_name,
        size=raw.size,
        url=raw.chunk_url,
    )
