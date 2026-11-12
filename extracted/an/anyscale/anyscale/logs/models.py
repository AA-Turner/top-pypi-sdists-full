"""Models for `anyscale logs query`, `anyscale <resource> logs` and `anyscale.logs`."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from anyscale._private.models import ModelBase


# The resources logs can be read for. The private SDK maps each to the query parameter
# the backend expects (job -> ha_job_id, the others -> <type>_id).
RESOURCE_TYPES: List[str] = ["cluster", "workspace", "job", "service"]

# Which lines a query searches: the workload's own output, or Ray's own files (raylet,
# gcs, core_worker), which reach the store at WARNING and above only.
LOG_TYPES: List[str] = ["application", "system"]


@dataclass(frozen=True)
class LogsResource(ModelBase):
    """The cluster, workspace, job or service whose logs to read.

    The backend scopes every query to this resource, so logs of other resources in the
    same cloud are never returned.
    """

    __doc_py_example__ = """\
from anyscale.logs.models import LogsResource

# resource_type is one of: cluster, workspace, job, service.
resource = LogsResource(resource_type="job", resource_id="prodjob_abc123")
"""

    resource_type: str = field(
        metadata={"docstring": "The kind of resource: cluster, workspace, job or service."}
    )
    resource_id: str = field(metadata={"docstring": "ID of the resource, e.g. prodjob_abc123."})

    def _validate_resource_type(self, resource_type: str):
        if resource_type not in RESOURCE_TYPES:
            raise ValueError(
                f"resource_type must be one of {RESOURCE_TYPES}, got {resource_type!r}."
            )

    def _validate_resource_id(self, resource_id: str):
        if not isinstance(resource_id, str) or not resource_id:
            raise ValueError("resource_id must be a non-empty string.")


@dataclass(frozen=True)
class LogLine(ModelBase):
    """One log line matched by a query."""

    __doc_py_example__ = """\
from datetime import datetime, timedelta, timezone

import anyscale
from anyscale.logs.models import LogsResource

end = datetime.now(timezone.utc)
for line in anyscale.logs.query(
    '{} |= "OOM"',
    LogsResource(resource_type="job", resource_id="prodjob_abc123"),
    start=end - timedelta(hours=1),
    end=end,
):
    print(line.timestamp, line.fields.get("level"), line.message)
"""

    timestamp: datetime = field(
        metadata={"docstring": "When the line was written, as a timezone-aware UTC datetime."}
    )
    message: str = field(metadata={"docstring": "The line's text."})
    fields: Dict[str, Any] = field(
        metadata={
            "docstring": "Everything else the store holds for the line: its stream labels "
            "(instance_id, cluster_id, ...) and any fields parsed from a JSON line (level, "
            "component_name, ...)."
        }
    )

    def _validate_timestamp(self, timestamp: datetime):
        if not isinstance(timestamp, datetime):
            raise TypeError("timestamp must be a datetime.")

    def _validate_message(self, message: str):
        if not isinstance(message, str):
            raise TypeError("message must be a string.")

    def _validate_fields(self, fields: Dict[str, Any]):
        if not isinstance(fields, dict) or not all(isinstance(key, str) for key in fields):
            raise TypeError("fields must be a dict with string keys.")


# The resources log files can be read for. Two of them have a different name on the wire
# (job -> production_job, cluster -> session); the private SDK owns that mapping.
ENTITY_TYPES: List[str] = ["job", "service", "workspace", "cluster"]

# Which files to read: the workload's own output, Ray's own files (raylet, gcs_server,
# the autoscaler monitor, ...), or everything the cluster wrote.
LOG_FILE_TYPES: List[str] = ["application", "system", "all"]

# Which nodes' files to read. On the wire these are head-node and worker-nodes.
NODE_TYPES: List[str] = ["head", "worker"]

# The backend lists at most this many chunks per page.
MAX_PAGE_SIZE = 1000

# `anyscale.logs.read_page` and `anyscale <resource> logs` return at most this many lines.
MAX_LINES_PER_PAGE = 1000


@dataclass(frozen=True)
class LogFilesFilter(ModelBase):
    """Which resource to read log files for, and which of its files to keep.

    The backend resolves the resource to one cluster: a job to its latest run's cluster
    (or the run named by ``job_run``), a service to its primary version's cluster (or the
    version named by ``service_version``), a workspace to its cluster. A job with
    application logs and no glob or node filter keeps only its output file, as
    ``anyscale job logs`` does.
    """

    __doc_py_example__ = """\
from anyscale.logs.models import LogFilesFilter

files_filter = LogFilesFilter(
    # One of: job, service, workspace, cluster.
    entity_type="job",
    # ID of that resource.
    entity_id="prodjob_abc123",
    # Optional: application (the default), system or all.
    log_type="application",
    # Optional, jobs only: one run by name or id. Defaults to the latest run.
    job_run=None,
    # Optional, services only: one version by name or id. Defaults to the primary version.
    service_version=None,
    # Optional: only files of one Ray session, node type, node IP or instance.
    ray_session=None,
    node_type=None,
    node_ip=None,
    instance_id=None,
    # Optional: only files whose bucket path matches this glob, e.g. "raylet*".
    glob=None,
    # Optional: only chunks written inside this window, as timezone-aware datetimes.
    start_time=None,
    end_time=None,
    # True reads the newest page_size chunks of the window instead of its first page.
    latest=False,
    # Chunks per page, 1 to 1000.
    page_size=1000,
)
"""

    entity_type: str = field(
        metadata={"docstring": "The kind of resource: job, service, workspace or cluster."}
    )
    entity_id: str = field(metadata={"docstring": "ID of the resource, e.g. prodjob_abc123."})
    log_type: str = field(
        default="application",
        metadata={
            "docstring": "Which files to read: 'application' (the workload's own output, the "
            "default), 'system' (Ray's own files such as raylet, gcs_server and the "
            "autoscaler monitor) or 'all'."
        },
    )
    job_run: Optional[str] = field(
        default=None,
        metadata={
            "docstring": "Jobs only: the name or ID of one run. Defaults to the latest run."
        },
    )
    service_version: Optional[str] = field(
        default=None,
        metadata={
            "docstring": "Services only: the name or ID of one version. Defaults to the "
            "primary version."
        },
    )
    ray_session: Optional[str] = field(
        default=None,
        metadata={
            "docstring": "Only files of this Ray session. A cluster that restarted Ray has "
            "several; None means all of them."
        },
    )
    node_type: Optional[str] = field(
        default=None,
        metadata={"docstring": "Only files of the 'head' node or of the 'worker' nodes."},
    )
    node_ip: Optional[str] = field(
        default=None, metadata={"docstring": "Only files of the node with this IP."}
    )
    instance_id: Optional[str] = field(
        default=None, metadata={"docstring": "Only files of this instance."}
    )
    glob: Optional[str] = field(
        default=None,
        metadata={"docstring": "Only files whose bucket path matches this glob, e.g. 'raylet*'."},
    )
    start_time: Optional[datetime] = field(
        default=None,
        metadata={"docstring": "Only chunks written at or after this time. None means no bound."},
    )
    end_time: Optional[datetime] = field(
        default=None,
        metadata={"docstring": "Only chunks written at or before this time. None means no bound."},
    )
    latest: bool = field(
        default=False,
        metadata={
            "docstring": "Read the newest page_size chunks of the window instead of its first "
            "page. Such a page carries no next_page_token."
        },
    )
    page_size: int = field(
        default=MAX_PAGE_SIZE,
        metadata={"docstring": "Chunks per page, 1 to 1000."},
    )
    next_page_token: Optional[str] = field(
        default=None,
        metadata={
            "docstring": "Token from the previous page, to read the next one. Cannot be "
            "combined with latest."
        },
    )

    def _validate_entity_type(self, entity_type: str):
        if entity_type not in ENTITY_TYPES:
            raise ValueError(f"entity_type must be one of {ENTITY_TYPES}, got {entity_type!r}.")

    def _validate_entity_id(self, entity_id: str):
        if not isinstance(entity_id, str) or not entity_id:
            raise ValueError("entity_id must be a non-empty string.")

    def _validate_log_type(self, log_type: str):
        if log_type not in LOG_FILE_TYPES:
            raise ValueError(f"log_type must be one of {LOG_FILE_TYPES}, got {log_type!r}.")

    def _validate_job_run(self, job_run: Optional[str]):
        if job_run is None:
            return
        if not isinstance(job_run, str):
            raise TypeError("job_run must be a string.")
        if self.entity_type != "job":
            raise ValueError("job_run applies to jobs only.")

    def _validate_service_version(self, service_version: Optional[str]):
        if service_version is None:
            return
        if not isinstance(service_version, str):
            raise TypeError("service_version must be a string.")
        if self.entity_type != "service":
            raise ValueError("service_version applies to services only.")

    def _validate_ray_session(self, ray_session: Optional[str]):
        if ray_session is not None and not isinstance(ray_session, str):
            raise TypeError("ray_session must be a string.")

    def _validate_node_type(self, node_type: Optional[str]):
        if node_type is not None and node_type not in NODE_TYPES:
            raise ValueError(f"node_type must be one of {NODE_TYPES}, got {node_type!r}.")

    def _validate_node_ip(self, node_ip: Optional[str]):
        if node_ip is not None and not isinstance(node_ip, str):
            raise TypeError("node_ip must be a string.")

    def _validate_instance_id(self, instance_id: Optional[str]):
        if instance_id is not None and not isinstance(instance_id, str):
            raise TypeError("instance_id must be a string.")

    def _validate_glob(self, glob: Optional[str]):
        if glob is not None and not isinstance(glob, str):
            raise TypeError("glob must be a string.")

    def _validate_start_time(self, start_time: Optional[datetime]):
        if start_time is not None and not isinstance(start_time, datetime):
            raise TypeError("start_time must be a datetime.")

    def _validate_end_time(self, end_time: Optional[datetime]):
        if end_time is not None and not isinstance(end_time, datetime):
            raise TypeError("end_time must be a datetime.")
        if end_time is not None and self.start_time is not None and end_time < self.start_time:
            raise ValueError("end_time must not be before start_time.")

    def _validate_latest(self, latest: bool):
        if not isinstance(latest, bool):
            raise TypeError("latest must be a boolean.")

    def _validate_page_size(self, page_size: int):
        if (
            not isinstance(page_size, int)
            or isinstance(page_size, bool)
            or not 1 <= page_size <= MAX_PAGE_SIZE
        ):
            raise ValueError(
                f"page_size must be between 1 and {MAX_PAGE_SIZE}, got {page_size!r}."
            )

    def _validate_next_page_token(self, next_page_token: Optional[str]):
        if next_page_token is None:
            return
        if not isinstance(next_page_token, str):
            raise TypeError("next_page_token must be a string.")
        if self.latest:
            raise ValueError("next_page_token cannot be combined with latest.")


@dataclass(frozen=True)
class LogChunk(ModelBase):
    """One chunk of a log file in the cloud bucket. A file that grew past the chunk size
    has several, named so that they sort oldest first."""

    __doc_py_example__ = """\
import anyscale
from anyscale.logs.models import LogFilesFilter

page = anyscale.logs.list_files(
    LogFilesFilter(entity_type="cluster", entity_id="ses_abc123", log_type="system"),
)
for chunk in page.chunks:
    print(chunk.node_ip, chunk.file_name, chunk.size, chunk.url)
"""

    cluster_id: str = field(metadata={"docstring": "ID of the cluster that wrote the file."})
    ray_session: str = field(metadata={"docstring": "The Ray session the file belongs to."})
    node_type: str = field(
        metadata={"docstring": "'head', 'worker', or 'unknown' for a file no node owns."}
    )
    node_ip: Optional[str] = field(
        metadata={"docstring": "IP of the node that wrote the file, if it came from one."}
    )
    instance_id: Optional[str] = field(
        metadata={"docstring": "Instance that wrote the file, if it came from one."}
    )
    file_name: str = field(
        metadata={
            "docstring": "Path of the file inside the node's log directory, e.g. raylet.out."
        }
    )
    chunk_name: str = field(metadata={"docstring": "The chunk's full object name in the bucket."})
    size: int = field(metadata={"docstring": "Size of the chunk in bytes."})
    url: str = field(
        metadata={
            "docstring": "Presigned URL to download the chunk. On GCP, send the page's "
            "bearer_token as a Bearer Authorization header with it."
        }
    )

    def _validate_cluster_id(self, cluster_id: str):
        if not isinstance(cluster_id, str):
            raise TypeError("cluster_id must be a string.")

    def _validate_ray_session(self, ray_session: str):
        if not isinstance(ray_session, str):
            raise TypeError("ray_session must be a string.")

    def _validate_node_type(self, node_type: str):
        if not isinstance(node_type, str):
            raise TypeError("node_type must be a string.")

    def _validate_node_ip(self, node_ip: Optional[str]):
        if node_ip is not None and not isinstance(node_ip, str):
            raise TypeError("node_ip must be a string.")

    def _validate_instance_id(self, instance_id: Optional[str]):
        if instance_id is not None and not isinstance(instance_id, str):
            raise TypeError("instance_id must be a string.")

    def _validate_file_name(self, file_name: str):
        if not isinstance(file_name, str):
            raise TypeError("file_name must be a string.")

    def _validate_chunk_name(self, chunk_name: str):
        if not isinstance(chunk_name, str):
            raise TypeError("chunk_name must be a string.")

    def _validate_size(self, size: int):
        if not isinstance(size, int) or isinstance(size, bool) or size < 0:
            raise ValueError("size must be a non-negative integer.")

    def _validate_url(self, url: str):
        if not isinstance(url, str):
            raise TypeError("url must be a string.")


@dataclass(frozen=True)
class LogFilesPage(ModelBase):
    """One page of log file chunks, as listed by the backend."""

    __doc_py_example__ = """\
import anyscale
from anyscale.logs.models import LogFilesFilter

files_filter = LogFilesFilter(entity_type="job", entity_id="prodjob_abc123")
page = anyscale.logs.list_files(files_filter)
while page.next_page_token:
    page = anyscale.logs.list_files(
        files_filter.options(next_page_token=page.next_page_token),
    )
"""

    chunks: List[LogChunk] = field(
        metadata={"docstring": "The chunks of this page, oldest first."}
    )
    next_page_token: Optional[str] = field(
        default=None,
        metadata={"docstring": "Token for the next page, or None when this is the last one."},
    )
    bearer_token: Optional[str] = field(
        default=None,
        metadata={
            "docstring": "GCP only: the token to send as a Bearer Authorization header when "
            "downloading the chunks' URLs."
        },
    )

    def _validate_chunks(self, chunks: List[LogChunk]):
        if not isinstance(chunks, list) or not all(isinstance(c, LogChunk) for c in chunks):
            raise TypeError("chunks must be a list of LogChunk.")

    def _validate_next_page_token(self, next_page_token: Optional[str]):
        if next_page_token is not None and not isinstance(next_page_token, str):
            raise TypeError("next_page_token must be a string.")

    def _validate_bearer_token(self, bearer_token: Optional[str]):
        if bearer_token is not None and not isinstance(bearer_token, str):
            raise TypeError("bearer_token must be a string.")


@dataclass(frozen=True)
class LogFileLine(ModelBase):
    """One line read from a log file, with the file and node it came from."""

    __doc_py_example__ = """\
import anyscale
from anyscale.logs.models import LogFilesFilter

for line in anyscale.logs.read(
    LogFilesFilter(entity_type="job", entity_id="prodjob_abc123", latest=True),
    max_lines=200,
):
    print(line.node_ip, line.file_name, line.line)
"""

    file_name: str = field(metadata={"docstring": "The file the line was read from."})
    node_ip: Optional[str] = field(
        metadata={"docstring": "IP of the node that wrote the file, if it came from one."}
    )
    instance_id: Optional[str] = field(
        metadata={"docstring": "Instance that wrote the file, if it came from one."}
    )
    line: str = field(metadata={"docstring": "The line's text, without its newline."})

    def _validate_file_name(self, file_name: str):
        if not isinstance(file_name, str):
            raise TypeError("file_name must be a string.")

    def _validate_node_ip(self, node_ip: Optional[str]):
        if node_ip is not None and not isinstance(node_ip, str):
            raise TypeError("node_ip must be a string.")

    def _validate_instance_id(self, instance_id: Optional[str]):
        if instance_id is not None and not isinstance(instance_id, str):
            raise TypeError("instance_id must be a string.")

    def _validate_line(self, line: str):
        if not isinstance(line, str):
            raise TypeError("line must be a string.")


@dataclass(frozen=True)
class LogLinesPage(ModelBase):
    """One page of log lines, and the token that reads the next page."""

    __doc_py_example__ = """\
import anyscale
from anyscale.logs.models import LogFilesFilter

files_filter = LogFilesFilter(entity_type="job", entity_id="prodjob_abc123", latest=True)
page = anyscale.logs.read_page(files_filter, max_lines=200)
for line in page.lines:
    print(line.line)
if page.next_page_token is not None:
    # The same filter, continued after the last line of the first page.
    page = anyscale.logs.read_page(files_filter, page_token=page.next_page_token)
"""

    lines: List[LogFileLine] = field(metadata={"docstring": "The lines of this page."})
    next_page_token: Optional[str] = field(
        default=None,
        metadata={
            "docstring": "Pass this as page_token, with the same filter, to read the next "
            "page. None when there are no more lines."
        },
    )

    def _validate_lines(self, lines: List[LogFileLine]):
        if not isinstance(lines, list) or not all(isinstance(x, LogFileLine) for x in lines):
            raise TypeError("lines must be a list of LogFileLine.")

    def _validate_next_page_token(self, next_page_token: Optional[str]):
        if next_page_token is not None and not isinstance(next_page_token, str):
            raise TypeError("next_page_token must be a string.")
