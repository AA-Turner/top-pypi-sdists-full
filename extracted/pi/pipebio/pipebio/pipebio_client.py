"""Top-level entry point for the PipeBio Python SDK.

This module exposes :class:`PipebioClient`, the object most callers create first.
It wires together the per-resource service objects (``entities``, ``jobs``,
``sequences``, ``shareables``, ``organization_lists`` and ``workflows``), handles
authentication from environment variables, and provides high-level convenience
helpers for uploading and exporting documents.

Example:
    Create a client and upload a file::

        from pipebio.pipebio_client import PipebioClient

        # Reads PIPE_API_KEY from the environment (or a local .env file).
        client = PipebioClient(url="https://app.pipebio.com")
        job = client.upload_file(
            file_name="sequences.fasta",
            absolute_file_location="/tmp/sequences.fasta",
            parent_id="123",
            project_id="456",
            poll_job=True,
        )
"""

import importlib.metadata
import os
import re
import shutil
import sys
import tempfile
import warnings
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, Iterator, List, Optional, Tuple, Union
from urllib.request import urlopen
from zipfile import ZipFile

from dotenv import load_dotenv
from requests_toolbelt import sessions
from requests_toolbelt.sessions import BaseUrlSession

from pipebio.column import Column
from pipebio.entities import Entities
from pipebio.jobs import Jobs
from pipebio.models.export_format import ExportFormat
from pipebio.models.job_status import JobStatus
from pipebio.models.job_type import JobType
from pipebio.models.table_column_type import TableColumnType
from pipebio.models.upload_detail import UploadDetail
from pipebio.multipart_upload import (
    MULTIPART_THRESHOLD,
    upload_multipart_aws,
)
from pipebio.organization_lists import OrganizationLists
from pipebio.sequences import Sequences
from pipebio.shareables import Shareables
from pipebio.util import Util
from pipebio.workflows import Workflows

# Per-socket-operation timeout for export downloads. Without it, urlopen
# inherits the global socket default of None and a stalled connection hangs
# the caller (typically a notebook kernel) indefinitely.
DOWNLOAD_READ_TIMEOUT_SECONDS = 300

# Extensions for the artifacts actually downloaded from ExportJob. Parquet and
# DuckDB exports are ZIP archives containing the requested data, rather than
# standalone .parquet or .duckdb files. These are used to warn about misleading
# user-provided filenames, not to rewrite them.
EXPORT_OUTPUT_EXTENSIONS = {
    ExportFormat.FASTA.value: '.fasta',
    ExportFormat.FASTQ.value: '.fastq',
    ExportFormat.GENBANK.value: '.gb',
    ExportFormat.TSV.value: '.tsv',
    ExportFormat.CSV.value: '.csv',
    ExportFormat.EXCEL.value: '.xlsx',
    ExportFormat.PARQUET.value: '.zip',
    ExportFormat.DUCKDB.value: '.zip',
}

# Keep the Parquet-backed record iterator suitable for low-memory machines.
# This also avoids requiring the optional ``pyarrow.dataset`` module, which is
# not present in every supported PyArrow build.
PARQUET_BUFFER_SIZE = 64 * 1024


class PipebioClient:
    """Authenticated client for the PipeBio API.

    The client authenticates on construction (using ``PIPE_API_KEY`` by default)
    and exposes per-resource service objects as attributes:

    Attributes:
        session: The underlying authenticated :class:`requests` session. Use it
            directly to call endpoints not yet wrapped by the SDK.
        shareables: Operations on shareables (projects/folders ownership).
        entities: Operations on entities (documents, folders).
        jobs: Operations on jobs (create, list, poll, update).
        sequences: Operations on sequence documents (download, upload, import).
        organization_lists: Operations on organization-level lists.
        workflows: Operations on workflows.
        user: The authenticated user object, or ``None`` when manual auth is used.
    """

    session: BaseUrlSession
    shareables: Shareables
    entities: Entities
    jobs: Jobs
    sequences: Sequences
    organization_lists: OrganizationLists
    workflows: Workflows
    user: Any

    _url: str
    _is_aws: bool

    def __init__(self, url: Optional[str] = None) -> None:
        """Create and authenticate a client.

        Args:
            url: Base URL of the PipeBio instance, e.g.
                ``"https://app.pipebio.com"``. Required.

        Raises:
            Exception: If ``url`` is missing, or if no authentication token is
                available and ``PIPEBIO_MANUAL_AUTH`` is not set to ``"true"``.
        """
        __version__ = importlib.metadata.version("pipebio")
        print(f"PipeBio SDK version {__version__}")
        self._is_aws = None
        self._url = url
        # Load .env: try script directory first, then project root (e.g. when run via pytest)
        path = os.path.dirname(sys.argv[0])
        full_path = os.path.join(os.path.abspath(path), ".env")
        if not load_dotenv(full_path):
            # Fallback: project root (parent of pipebio package)
            _project_root = Path(__file__).resolve().parent.parent
            load_dotenv(_project_root / ".env")

        def first_not_none(*values):
            return next((v for v in values if v is not None), None)

        manual_auth = os.environ.get("PIPEBIO_MANUAL_AUTH", "false").lower() == "true"
        benchling_s2s_token = os.environ.get("BENCHLING_S2S_TOKEN") or None
        api_key = os.environ.get("PIPE_API_KEY") or None
        # User tokens are used by plugins running inside PipeBio and only ever set by Pipebio.
        # They are never used by users directly, they should always use PIPE_API_KEY.
        user_token = os.environ.get("USER_TOKEN") or None

        # Strip whitespace (e.g. from .env inline comments) - can cause 401 if present
        def _strip(s):
            return s.strip() if s else None

        benchling_s2s_token = _strip(benchling_s2s_token)
        api_key = _strip(api_key)
        user_token = _strip(user_token)

        token = first_not_none(user_token, benchling_s2s_token, api_key)

        if token is None and not manual_auth:
            print(f"PIPE_API_KEY={api_key}")
            raise Exception("PIPE_API_KEY required.")

        if url is None:
            raise Exception("url required.")

        base_url = f"{url}/api/v2/"

        self.session = sessions.BaseUrlSession(base_url=base_url)
        self.session.headers.update({"User-Agent": f"pipebio-sdk/{__version__}"})

        # Set Bearer token header with API KEY, Benchling S2S token or USER TOKEN.
        if token is not None:
            self.session.headers.update({"Authorization": f"Bearer {token}"})
            # Will also check api_key and fail fast, with friendly error if auth fails.
            self.user = self.get_user()
            first_name = self.user.get("firstName", "")
            last_name = self.user.get("lastName", "")
            print(f"\nUsing api key for {first_name} {last_name}.\n")
        else:
            self.user = None

        self.shareables = Shareables(self.session)
        self._init_user_dependent_services()
        self.internal_tools = _InternalTools(self)

    def _init_user_dependent_services(self):
        job_id = os.environ["JOB_ID"] if "JOB_ID" in os.environ else None
        self.entities = Entities(self.session, self.user)
        self.sequences = Sequences(self.session, self.is_aws, self.user)
        self.jobs = Jobs(self.session, self.user, job_id)
        self.organization_lists = OrganizationLists(self.session, self.user)
        self.workflows = Workflows(
            self.session, self.organization_lists, self.user, self.jobs
        )

    @staticmethod
    def sanitize_baseurl(url: str) -> str:
        """Validate and normalise a PipeBio base URL.

        Args:
            url: The base URL to sanitise.

        Returns:
            The URL with surrounding whitespace and any trailing slash removed.

        Raises:
            ValueError: If the URL does not start with ``https://``.
        """
        url = url.strip()

        if not url.startswith("https://"):
            raise ValueError(
                "Base URL must start with 'https://'. Please provide a full URL like 'https://app.pipebio.com' or 'https://your-company.pipebio.benchling.com'"
            )

        if url != "https://" and url.endswith("/"):
            url = url[:-1]

        return url

    def get_user(self) -> Dict[str, Any]:
        """Fetch the authenticated user from the ``me`` endpoint.

        Returns:
            The user object as returned by the API.

        Raises:
            ValueError: If authentication fails (HTTP 401).

        .. API reference (generated - do not edit) ::

        **GET** ``/me``

        Get me

        Returns information about the currently authenticated user

        .. end API reference ::
        """
        response = self.session.get("me")
        if response.status_code == 401:
            raise ValueError("Failed to authenticate, please check PIPE_API_KEY")
        user = response.json()
        return user

    def upload_file(
        self,
        file_name: str,
        absolute_file_location: str,
        parent_id: str,
        project_id: str,
        organization_id: Optional[str] = None,
        details: Optional[List[UploadDetail]] = None,
        file_name_id: Optional[str] = None,
        poll_job: bool = False,
        on_progress: Optional[Callable[[int, int], None]] = None,
    ) -> Dict[str, Any]:
        """Upload a single local file as a new document.

        Large files (at or above the multipart threshold) are uploaded with a
        multipart upload on AWS instances; otherwise a single signed upload is
        used.

        Args:
            file_name: Friendly name shown in the PipeBio UI.
            absolute_file_location: Absolute path to the file on local disk.
            parent_id: Id of the parent folder/document the upload belongs to.
            project_id: Id of the project (shareable) to upload into.
            organization_id: Organization id. Defaults to the user's default org.
            details: Optional per-file upload details/metadata.
            file_name_id: Optional client-supplied id used to correlate the file.
            poll_job: If ``True``, block until the parsing job finishes and
                return the completed job.
            on_progress: Optional callback receiving ``(bytes_sent, total_bytes)``
                during multipart uploads.

        Returns:
            The upload/parse job object. When ``poll_job`` is ``True`` this is the
            completed job; otherwise it is the in-progress job.
        """
        _organization_id = (
            organization_id
            if organization_id is not None
            else Util.get_organization_id(self.user)
        )

        # Normalize file_name to use forward slashes for cross-platform compatibility.
        normalized_file_name = file_name.replace("\\", "/")
        file_size = os.path.getsize(absolute_file_location)
        use_multipart = file_size >= MULTIPART_THRESHOLD

        if use_multipart and Util.is_aws():
            job = upload_multipart_aws(
                session=self.session,
                absolute_file_location=absolute_file_location,
                file_name=normalized_file_name,
                parent_id=parent_id,
                project_id=project_id,
                organization_id=_organization_id,
                details=details,
                file_name_id=file_name_id,
                on_progress=on_progress,
            )
            job_id = job["id"]
        else:
            print(f"Uploading {normalized_file_name}.")
            response = self.jobs.create_signed_upload(
                file_name=normalized_file_name,
                parent_id=parent_id,
                project_id=project_id,
                details=details,
                file_name_id=file_name_id,
                organization_id=_organization_id,
            )
            url = response["data"]["url"]
            job = response["data"]["job"]
            job_id = job["id"]
            headers = response["data"]["headers"]

            self.jobs.upload_data_to_signed_url(absolute_file_location, url, headers)

        print(f"Upload complete for {normalized_file_name}. Parsing contents.\n")

        if poll_job:
            return self.jobs.poll_job(job_id)
        else:
            return job

    def export(
        self,
        entity_id: str,
        format: ExportFormat,
        destination_folder: Optional[str] = None,
        destination_filename: Optional[str] = None,
        params: Optional[dict] = None,
        timeout_seconds: Optional[int] = None,
        read_timeout_seconds: int = DOWNLOAD_READ_TIMEOUT_SECONDS,
        allow_deleted_entities: bool = False,
    ) -> List[str]:
        """Export an entity to a file and download the result.

        Runs an ``ExportJob`` server-side, waits for completion, then downloads
        every output link to ``destination_folder``. Parquet and DuckDB exports
        are returned as ZIP archives and are not automatically extracted.

        The delimited formats (``TSV``, ``CSV``, ``EXCEL``) are sanitized
        server-side so the output is safe to open in a spreadsheet: a value
        starting with ``=``, ``+``, ``@`` or a non-numeric ``-`` is prefixed
        with an apostrophe, a whitespace-only value becomes empty, and embedded
        tabs and newlines are replaced with spaces. Use ``PARQUET`` or
        ``DUCKDB`` when cell values must be byte-faithful.

        Args:
            entity_id: Id of the entity to export.
            format: The :class:`~pipebio.models.export_format.ExportFormat` to
                produce (e.g. GenBank, FASTA).
            destination_folder: Local folder to write the downloaded file(s) to;
                it is created if it does not already exist. Defaults to the
                current working directory.
            destination_filename: Optional output filename; defaults to the
                entity name. The SDK preserves an explicitly requested name and
                emits a :class:`UserWarning` if its extension conflicts with
                the ExportJob artifact type; Parquet and DuckDB exports are ZIP
                archives.
            params: Optional extra export parameters merged into the job params.
            timeout_seconds: Maximum time to wait for the export job to complete.
                When omitted or ``None``, polling continues until the job
                finishes. Pass an explicit value to cap the wait.
            read_timeout_seconds: Per-socket-operation timeout for the download.
                Defaults to 300 seconds, so a stalled connection raises rather
                than hanging forever. Raise it for a slow link.
            allow_deleted_entities: Whether to allow referencing entities that
                have been soft-deleted.

        Returns:
            The list of local file paths that were downloaded.
        """
        entity = self.entities.get(
            entity_id,
            allow_deleted=allow_deleted_entities,
        )
        entity_name = entity["name"]
        user = self.user

        params = {} if params is None else params
        params["format"] = format.value if "format" not in params else params["format"]
        params["fileName"] = (
            entity_name if "fileName" not in params else params["fileName"]
        )

        requested_destination_filename = (
            destination_filename if destination_filename else None
        )
        destination_filename = requested_destination_filename or params["fileName"]

        # Create the folder before the job is created: a missing folder would
        # otherwise cost a complete export before open() fails, hours later.
        destination_folder = destination_folder or os.getcwd()
        os.makedirs(destination_folder, exist_ok=True)

        print(f"Exporting {entity_id} to {destination_folder}/{destination_filename}")
        job_id = self.jobs.create(
            owner_id=user["org"]["id"],
            shareable_id=entity["ownerId"],
            job_type=JobType.ExportJob,
            name="Export from python client",
            input_entity_ids=[entity_id],
            params=params,
            allow_deleted_entities=allow_deleted_entities,
        )

        # Print the resume invocation before we start waiting: if polling or
        # downloading fails, the user can copy-paste this rather than re-running
        # the whole export. Note this resumes the *job*; an interrupted download
        # still restarts from byte zero.
        # !r rather than hand-quoting: a Windows path in a double-quoted literal
        # is a SyntaxError (destination_folder="C:\Users\..." is a truncated
        # \U escape), and it quotes the job id correctly whether int or str.
        resume_filename = (
            f', destination_filename={destination_filename!r}'
            if requested_destination_filename
            else ''
        )
        print(
            f"Export job id: {job_id}\n"
            f"If this is interrupted, resume the download with:\n"
            f"    client.download_export_output({job_id!r}, "
            f"destination_folder={destination_folder!r}{resume_filename})"
        )

        return self.download_export_output(
            job_id,
            destination_folder=destination_folder,
            destination_filename=requested_destination_filename,
            timeout_seconds=timeout_seconds,
            read_timeout_seconds=read_timeout_seconds,
        )

    @staticmethod
    def _warn_if_export_filename_extension_mismatches(
        filename: str, export_format: Optional[str]
    ) -> None:
        """Warn when an explicit-looking filename mislabels a known artifact."""
        extension = EXPORT_OUTPUT_EXTENSIONS.get(export_format)
        if (
            extension is None
            or not Path(filename).suffix
            or filename.lower().endswith(extension)
        ):
            return

        if extension == '.zip':
            artifact = f'ZIP archive produced by the {export_format} export'
        else:
            artifact = f'{export_format} export output'
        warnings.warn(
            f'Destination filename {filename!r} does not match the {artifact}. '
            f'The SDK will keep the filename you requested. Use a name ending '
            f'in {extension!r} to silence this warning.',
            UserWarning,
            stacklevel=3,
        )

    def export_to_path(
        self,
        entity_id: str,
        destination: Union[str, os.PathLike[str]],
        format: ExportFormat = ExportFormat.TSV,
        params: Optional[dict] = None,
        timeout_seconds: Optional[int] = None,
        read_timeout_seconds: int = DOWNLOAD_READ_TIMEOUT_SECONDS,
        allow_deleted_entities: bool = False,
    ) -> str:
        """Export one entity to a specific local file path.

        This is a convenience adapter for callers migrating from
        :meth:`Sequences.download`: unlike :meth:`export`, it accepts one
        ``destination`` path and returns one path instead of a list.

        See :meth:`export` for the spreadsheet sanitization applied to the
        delimited formats.

        Args:
            entity_id: Id of the entity to export.
            destination: Local file path to write. The SDK preserves this path
                exactly and warns when its extension conflicts with the output
                type. In particular, Parquet and DuckDB exports are ZIP
                archives and are not automatically extracted.
            format: Export format. Defaults to TSV.
            params: Optional ExportJob parameters.
            timeout_seconds: Maximum time to wait for the ExportJob.
            read_timeout_seconds: Per-socket-operation download timeout.
            allow_deleted_entities: Whether to allow exporting a soft-deleted
                entity.

        Returns:
            The local output path.

        Raises:
            ValueError: If the ExportJob produces multiple outputs. Use
                :meth:`export` to receive all output paths in that case.
        """
        destination_path = Path(destination)
        outputs = self.export(
            entity_id,
            format,
            destination_folder=str(destination_path.parent),
            destination_filename=destination_path.name,
            params=params,
            timeout_seconds=timeout_seconds,
            read_timeout_seconds=read_timeout_seconds,
            allow_deleted_entities=allow_deleted_entities,
        )
        if len(outputs) == 0:
            raise ValueError(
                f'Export of entity {entity_id} produced no output files.'
            )
        if len(outputs) > 1:
            raise ValueError(
                f'Export of entity {entity_id} produced {len(outputs)} outputs; '
                'use client.export() to receive all output paths.'
            )
        return outputs[0]

    def iter_sequence_records(
        self,
        entity_ids: Iterable[str],
        timeout_seconds: Optional[int] = None,
        read_timeout_seconds: int = DOWNLOAD_READ_TIMEOUT_SECONDS,
        allow_deleted_entities: bool = True,
    ) -> Iterator[Tuple[str, Dict[str, Any]]]:
        """Yield legacy-shaped sequence records through ``ExportJob``.

        Each entity is exported to a temporary Parquet artifact, then parsed one
        row at a time. Parquet output is delivered by ExportJob as a ZIP
        archive; the SDK safely extracts it, removes the archive, and scans the
        enclosed Parquet dataset in bounded batches. This avoids building the
        complete result map in memory, unlike
        :meth:`Sequences.download_to_memory`.

        Parquet is the only transport this iterator offers. Unlike the
        delimited formats it reproduces cell values verbatim, so records match
        the legacy ``_extract`` output; see :meth:`export` for the rewriting
        the delimited formats apply. ``DUCKDB`` is byte-faithful as well, but
        reading it back one row at a time would require a database engine.

        The yielded ``(compound_id, record)`` pairs have the same shape as the
        entries in ``download_to_memory()``: ``compound_id`` is
        ``"<entity_id>##@##<sequence_id>"`` and ``record`` has ``id``, ``name``,
        ``sequence``, ``annotations``, and ``type`` keys. For a document, the
        prefix preserves the ID supplied by the caller. A folder export contains
        several documents, so each record instead uses its source document ID.
        Constructing a ``dict`` from the iterator deliberately recreates the
        legacy memory-intensive behavior. The server does not guarantee an
        ordering for Parquet shards, so callers must not rely on yielded record
        order.

        Args:
            entity_ids: Ids of the sequence documents to export. The caller's
                ID is preserved in each document's compound ID prefix. Folder
                exports use the source document ID from each dataset.
            timeout_seconds: Maximum time to wait for each ExportJob.
            read_timeout_seconds: Per-socket-operation download timeout.
            allow_deleted_entities: Whether to allow referencing input documents
                that have been soft-deleted. This authorizes the export of a
                deleted document; it does not add soft-deleted sequences to the
                output of a live one.

        Yields:
            Tuples of compound id and parsed sequence record.
        """
        columns = [
            Column('id', TableColumnType.STRING),
            Column('name', TableColumnType.STRING),
            Column('sequence', TableColumnType.STRING),
            Column('annotations', TableColumnType.STRING),
            Column('type', TableColumnType.STRING),
        ]

        for entity_id in entity_ids:
            with tempfile.TemporaryDirectory(
                prefix='pipebio-sequence-export-'
            ) as destination_folder:
                output_paths = self.export(
                    entity_id,
                    ExportFormat.PARQUET,
                    destination_folder=destination_folder,
                    destination_filename='sequences.zip',
                    timeout_seconds=timeout_seconds,
                    read_timeout_seconds=read_timeout_seconds,
                    allow_deleted_entities=allow_deleted_entities,
                )
                for output_index, output_path in enumerate(output_paths):
                    parquet_datasets = self._extract_parquet_archive(
                        archive_path=Path(output_path),
                        destination=Path(destination_folder)
                        / f'parquet-{output_index}',
                    )
                    single_dataset = len(parquet_datasets) == 1
                    for parquet_entity_id, parquet_directory in parquet_datasets:
                        id_prefix = (
                            str(entity_id) if single_dataset else parquet_entity_id
                        )
                        yield from self._iter_parquet_sequence_entries(
                            parquet_directory,
                            id_prefix,
                            columns,
                        )

    @staticmethod
    def _extract_parquet_archive(
        archive_path: Path,
        destination: Path,
    ) -> List[Tuple[str, Path]]:
        """Safely extract an ExportJob Parquet archive and return its datasets."""
        destination.mkdir()
        destination_root = destination.resolve()
        with ZipFile(archive_path) as archive:
            for member in archive.infolist():
                member_path = (destination_root / member.filename).resolve()
                if not member_path.is_relative_to(destination_root):
                    raise ValueError(
                        f'Parquet archive {archive_path} contains an unsafe path: '
                        f'{member.filename!r}.'
                    )
            archive.extractall(destination_root)
        archive_path.unlink()

        parquet_directories = sorted(
            path
            for path in destination_root.rglob('*.parquet')
            if path.is_dir()
            and any(
                child.is_file() and child.suffix == '.parquet'
                for child in path.iterdir()
            )
        )
        if not parquet_directories:
            raise ValueError(
                f'Expected at least one Parquet dataset directory in {archive_path}.'
            )
        return [
            (
                PipebioClient._entity_id_from_parquet_directory(parquet_directory),
                parquet_directory,
            )
            for parquet_directory in parquet_directories
        ]

    @staticmethod
    def _entity_id_from_parquet_directory(parquet_directory: Path) -> str:
        """Extract the source entity ID from an ExportJob dataset directory."""
        _, separator, entity_id = parquet_directory.stem.rpartition(' - ')
        if not separator or not entity_id:
            raise ValueError(
                f'Could not determine an entity ID from Parquet dataset directory '
                f'{parquet_directory.name!r}.'
            )
        return entity_id

    @staticmethod
    def _iter_parquet_sequence_entries(
        parquet_directory: Path,
        id_prefix: str,
        columns: List[Column],
    ) -> Iterator[Tuple[str, Dict[str, Any]]]:
        """Yield legacy-shaped sequence entries from a Parquet dataset."""
        import pyarrow.parquet as pq

        parquet_files = sorted(
            path
            for path in parquet_directory.rglob('*.parquet')
            if path.is_file()
        )
        if not parquet_files:
            raise ValueError(f'Parquet dataset {parquet_directory} has no files.')

        for parquet_path in parquet_files:
            with pq.ParquetFile(
                str(parquet_path),
                buffer_size=PARQUET_BUFFER_SIZE,
                pre_buffer=False,
            ) as parquet_file:
                available_columns = set(parquet_file.schema_arrow.names)
                if 'id' not in available_columns:
                    raise ValueError(
                        f'Parquet file {parquet_path} has no id column.'
                    )

                selected_columns = [
                    column.name for column in columns if column.name in available_columns
                ]
                for batch in parquet_file.iter_batches(
                    batch_size=1024,
                    columns=selected_columns,
                    use_threads=False,
                ):
                    values = batch.to_pydict()
                    for row_index in range(batch.num_rows):
                        parsed = {}
                        for column in columns:
                            if column.name in values:
                                value = values[column.name][row_index]
                                parsed[column.name] = column.parse(
                                    '' if value is None else str(value)
                                )
                            else:
                                parsed[column.name] = column.parse('')

                        yield (
                            f'{id_prefix}{Sequences._merge_delimiter}{parsed["id"]}',
                            parsed,
                        )

    def download_export_output(
        self,
        job_id: Union[int, str],
        destination_folder: Optional[str] = None,
        destination_filename: Optional[str] = None,
        timeout_seconds: Optional[int] = None,
        read_timeout_seconds: int = DOWNLOAD_READ_TIMEOUT_SECONDS,
    ) -> List[str]:
        """Wait for an export job to finish and download its output links.

        Split out of :meth:`export` so that a download interrupted by a dropped
        connection, a timeout or a dead kernel can be retried against an
        already-running (or already-finished) job. Note that this resumes the
        *job*: the download itself restarts from the beginning.

        The window is not unlimited: an ``ExportJob`` presigns its output links
        for 24 hours, so retrying a day later fails with a bare ``HTTPError:
        403`` from storage rather than anything mentioning expiry. Past that
        point, re-run :meth:`export`.

        Each file is streamed to a ``.part`` sibling and moved into place only
        once it has been downloaded in full, so no returned path ever holds a
        truncated file. Atomicity is per file, not per export: if a job with
        several output links fails partway, the files already downloaded stay on
        disk and are named in the raised error. Retrying overwrites them.

        Args:
            job_id: Id of the ``ExportJob`` to poll, as printed by :meth:`export`.
            destination_folder: Local folder to write the downloaded file(s) to;
                it is created if it does not already exist. Defaults to the
                current working directory.
            destination_filename: Output filename. Defaults to the exported
                file name recorded on the job. When the job produces more than
                one output link, an index is appended to the stem
                (``name_1.tsv``, ``name_2.tsv``, ...). Archive outputs remain
                ZIP files; the SDK warns only when an explicitly supplied
                filename has an incompatible extension.
            timeout_seconds: Maximum time to wait for the export job to complete.
                When omitted or ``None``, polling continues until the job
                finishes. Pass an explicit value to cap the wait.
            read_timeout_seconds: Per-socket-operation timeout for the download.
                Defaults to 300 seconds, so a stalled connection raises rather
                than hanging forever.

        Returns:
            The list of local file paths that were downloaded.

        Raises:
            Exception: If the export job failed, or produced no output links.
        """
        # Wait for the file to be exported.
        job = self.jobs.poll_job(job_id, timeout_seconds=timeout_seconds)

        # poll_job returns normally for FAILED as well as COMPLETE, so check the
        # status explicitly rather than reporting success with nothing downloaded.
        status = job.get("status")
        if status != JobStatus.COMPLETE.value:
            messages = job.get("messages") or []
            detail = f": {'; '.join(messages)}" if messages else ""
            raise Exception(f"Export job {job_id} did not complete ({status}){detail}")

        links = job.get("outputLinks") or []
        if len(links) == 0:
            raise Exception(f"Export job {job_id} produced no output links.")

        requested_destination_filename = destination_filename
        if destination_filename is None:
            destination_filename = (job.get("params") or {}).get("fileName")
        if not destination_filename:
            raise Exception(
                f"No destination_filename given and export job {job_id} does not "
                f"record one; pass destination_filename explicitly."
            )
        if requested_destination_filename is not None:
            self._warn_if_export_filename_extension_mismatches(
                destination_filename, (job.get("params") or {}).get("format")
            )

        destination_folder = destination_folder or os.getcwd()
        os.makedirs(destination_folder, exist_ok=True)

        outputs = []

        for index, link in enumerate(links):
            filename = destination_filename
            if len(links) > 1:
                stem, extension = Util.split_extension(destination_filename)
                filename = f"{stem}_{index + 1}{extension}"
            destination = os.path.join(destination_folder, filename)
            partial = f"{destination}.part"

            # Stream the response to disk; exports can be tens of gigabytes and
            # must never be buffered in memory. Write to a .part file and rename
            # only on success, so a truncated download cannot masquerade as a
            # complete export at the path we promise to produce.
            try:
                with urlopen(link["url"], timeout=read_timeout_seconds) as response:
                    expected = response.headers.get("Content-Length")
                    with open(partial, "wb") as file:
                        shutil.copyfileobj(response, file, length=1024 * 1024)
                        copied = file.tell()

                if expected is not None and copied != int(expected):
                    raise Exception(
                        f"Incomplete download of {destination}: expected "
                        f"{expected} bytes, got {copied}."
                    )

                os.replace(partial, destination)
            except BaseException as error:
                # Leave nothing behind that could be mistaken for the export.
                # Swallow cleanup failures (read-only dir, Windows file lock, a
                # .part that never got created): the download error is the one
                # the user needs to see, so it must stay the primary exception.
                try:
                    os.remove(partial)
                except OSError:
                    pass
                # Earlier links are already on disk and the caller has no return
                # value to learn that from, so name them. Only for Exception:
                # wrapping KeyboardInterrupt would break Ctrl-C.
                if outputs and isinstance(error, Exception):
                    raise Exception(
                        f"Export download failed on link {index + 1} of "
                        f"{len(links)}. These files were already downloaded and "
                        f"are still on disk: {', '.join(outputs)}. Retrying "
                        f"overwrites them."
                    ) from error
                raise

            outputs.append(destination)

        return outputs

    @staticmethod
    def _get_file_list(filename_pattern: str, local_folder_path: str):
        """
        Helper function for getting file list from local folder.
        :param filename_pattern:
        :param local_folder_path:
        :return:
        """
        if filename_pattern is not None:
            try:
                re.compile(filename_pattern)
            except re.error:
                raise ValueError("Invalid filename_pattern")

        local_files_to_upload: List[Dict[str, str]] = []
        for dir_path, dir_names, filenames in os.walk(local_folder_path):
            for filename in filenames:
                if filename_pattern is None or re.search(filename_pattern, filename):
                    local_files_to_upload.append(
                        {
                            "filename": filename,
                            "full_path": os.path.join(local_folder_path, filename),
                        }
                    )

        local_file_count = len(local_files_to_upload)
        if local_file_count == 0:
            raise ValueError(
                f"No files to upload, is the folder empty or your filename_pattern "
                f'"{filename_pattern}" incorrect?'
            )

        return local_files_to_upload

    def upload_files(
        self,
        absolute_folder_path: str,
        parent_id: str,
        project_id: str,
        organization_id: Optional[str] = None,
        filename_pattern: Optional[str] = None,
        poll_jobs: bool = False,
    ) -> List[Dict[str, Any]]:
        """Upload multiple files from a folder, one document per file.

        Useful for uploading a number of files to a single folder, e.g. ab1
        files. Uploads are started in parallel and parsing is not awaited unless
        ``poll_jobs`` is set.

        Args:
            absolute_folder_path: Full path to the folder containing the files.
            parent_id: Id of the parent folder/document.
            project_id: Id of the project (shareable) to upload into.
            organization_id: Organization id. Defaults to the user's default org.
            filename_pattern: Optional regex matched against filenames, e.g.
                ``r".*\\.ab1"``.
            poll_jobs: If ``True``, block until all parsing jobs finish.

        Returns:
            The list of upload job objects (completed when ``poll_jobs`` is set).
        """
        # Use organization_id if supplied, otherwise use default org id.
        _organization_id = (
            organization_id
            if organization_id is not None
            else Util.get_organization_id(self.user)
        )

        local_files_to_upload = self._get_file_list(
            filename_pattern, absolute_folder_path
        )
        local_file_count = len(local_files_to_upload)
        print(f"Uploading {local_file_count} files")

        # Upload the data, but don't wait for parsing to complete. Just to be efficient.
        index = 1
        upload_ids = []
        upload_jobs = []
        for local_file in local_files_to_upload:
            filename = local_file["filename"]
            print(f"Uploading file {index}/{local_file_count} ({filename})")

            upload_job = self.upload_file(
                # Friendly name that will be shown in PipeBio ui.
                file_name=filename,
                # Path on local disk.
                absolute_file_location=local_file["full_path"],
                # Optional.
                parent_id=parent_id,
                project_id=project_id,
                organization_id=_organization_id,
            )

            upload_ids.append(upload_job["id"])
            upload_jobs.append(upload_job)
            index += 1

        if poll_jobs:
            jobs = self.jobs.poll_jobs(upload_ids, None)
            print("Finished uploading files.")
            return jobs
        else:
            print("Uploading files.")
            return upload_jobs

    def upload_files_as_zip(
        self,
        absolute_folder_path: str,
        parent_id: str,
        project_id: str,
        organization_id: Optional[str] = None,
        filename_pattern: Optional[str] = None,
        poll_jobs: bool = False,
    ) -> Dict[str, Any]:
        """Zip the matching files in a folder and upload them as one document.

        Useful for uploading a number of files as a single document, e.g. ab1
        files.

        Args:
            absolute_folder_path: Full path to the folder containing the files.
            parent_id: Id of the parent folder/document.
            project_id: Id of the project (shareable) to upload into.
            organization_id: Organization id. Defaults to the user's default org.
            filename_pattern: Optional regex matched against filenames, e.g.
                ``r".*\\.ab1"``.
            poll_jobs: If ``True``, block until the parsing job finishes.

        Returns:
            The single upload job object (completed when ``poll_jobs`` is set).
        """
        # Use organization_id if supplied, otherwise use default org id.
        _organization_id = (
            organization_id
            if organization_id is not None
            else Util.get_organization_id(self.user)
        )

        local_files_to_upload = self._get_file_list(
            filename_pattern, absolute_folder_path
        )
        local_file_count = len(local_files_to_upload)
        print(f"Uploading {local_file_count} files")

        file = tempfile.NamedTemporaryFile()
        with ZipFile(file.name, "w") as zip_file:
            for local_file in local_files_to_upload:
                zip_file.write(
                    filename=local_file["full_path"], arcname=local_file["filename"]
                )

        upload_job = self.upload_file(
            # Friendly name that will be shown in PipeBio ui.
            file_name=os.path.basename(absolute_folder_path),
            # Path on local disk.
            absolute_file_location=file.name,
            # Optional.
            parent_id=parent_id,
            project_id=project_id,
            organization_id=_organization_id,
        )

        if poll_jobs:
            job = self.jobs.poll_job(upload_job["id"], None)
            print("Finished uploading files.")
            return job
        else:
            print("Uploading files.")
            return upload_job

    def set_correlation_id(self, correlation_id: str) -> None:
        """Set a correlation ID sent as an X-Correlation-Id header on every subsequent API request.

        Use this to link all API calls belonging to a single logical operation
        so they can be correlated in PipeBio server logs.

        Args:
            correlation_id: An opaque identifier for the operation being performed.
        """
        self.session.headers.update({"X-Correlation-Id": correlation_id})

    @property
    def is_aws(self) -> bool:
        """Whether the connected PipeBio instance runs on AWS.

        The result is determined once from the ``/debug/about`` endpoint and
        cached for the lifetime of the client.

        Returns:
            ``True`` if the instance is an AWS deployment, otherwise ``False``.
        """
        if self._is_aws is None:
            url = f"{self._url}/debug/about"
            response = self.session.get(url)
            Util.raise_detailed_error(response)
            # Stack is not set in GCP, so we use that as a flag that we are running in AWS here.
            self._is_aws = "stack" in response.json()
            os.environ["IS_AWS"] = str(self._is_aws)

        return self._is_aws


class _InternalTools:
    """Internal tools for Benchling integration use only. Not for external SDK users."""

    def __init__(self, client: PipebioClient):
        self._client = client

    def set_s2s_token(self, token: str) -> None:
        """
        Set the S2S (Service-to-Service) authentication token programmatically.

        This is for internal Benchling integration use only. Regular SDK users should
        use the PIPE_API_KEY environment variable.

        Requires PIPEBIO_MANUAL_AUTH=true to be set when instantiating the client.

        Args:
            token: The S2S token to use for authentication
        """
        self._client.session.headers.update({"Authorization": f"Bearer {token}"})
        self._client.user = self._client.get_user()
        self._client._init_user_dependent_services()
        first_name = self._client.user.get("firstName", "")
        last_name = self._client.user.get("lastName", "")
        print(f"Authenticated as {first_name} {last_name}.\n")
