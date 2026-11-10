import asyncio
import json
import logging
import os
import sys
import types
import typing
import uuid
import zlib
from datetime import datetime, timezone
from typing import (
    Any,
    AsyncIterator,
    Awaitable,
    Callable,
    Dict,
    List,
    Optional,
    Type,
    TypeVar,
)
from urllib.parse import urlparse

import aiofiles
import aiohttp
from rich.markup import escape
from strong_typing.serialization import object_to_json

from . import ui
from .auth import TableAccess
from .channel import DapApiChannel, DownloadChannel, default_headers
from .commands.global_options import read_dap_tracking_env_var
from .concurrency import gather_n
from .dap_error import (
    AccountDisabledError,
    AccountNotOnboardedError,
    AccountUnderMaintenanceError,
    AuthenticationError,
    DAPClientError,
    DownloadError,
    OAuthTokenError,
    OperationError,
    ServerError,
)
from .dap_types import (
    CompleteIncrementalJob,
    CompleteJob,
    CompleteSnapshotJob,
    Credentials,
    DownloadTableDataResult,
    Format,
    GetTableDataResult,
    IncrementalQuery,
    Job,
    JobID,
    JobStatus,
    NamespaceList,
    Object,
    ObjectID,
    Query,
    Resource,
    ResourceResult,
    SnapshotQuery,
    TableList,
    VersionedSchema,
)
from .tracking import TrackingData, send_tracking_data

logger = logging.getLogger("dap")

T = TypeVar("T")

# prevent "RuntimeError: Event loop is closed" on Windows platforms
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # type: ignore


DOWNLOAD_CONCURRENCY = 4

EXPIRE_AT_VERY_CLOSE_SECONDS = 30


class DAPClient:
    """
    Client proxy for the Data Access Platform (DAP) server-side API.

    In order to invoke high-level functionality such as initializing and synchronizing a database or data warehouse, or
    low-level functionality such as triggering a snapshot or incremental query, you need to instantiate a client, which
    acts as a proxy to DAP API.

    Tracking for usage analytics is done here as it is needed for both CLI and library use cases,
    additionally this way it's tied to operations where the DAP service is used (e.g. no tracking for local dropdb)
    """

    _base_url: str
    _credentials: Credentials
    _dap_session: Optional["DAPSession"]
    _tracking: bool

    def __init__(
        self,
        base_url: Optional[str] = None,
        credentials: Optional[Credentials] = None,
        tracking: Optional[bool] = None,
    ) -> None:
        "Initializes a new client proxy to communicate with the DAP back-end."

        if not base_url:
            base_url = os.getenv("DAP_API_URL")
            if not base_url:
                raise DAPClientError(
                    "Missing DAP API base URL. Please provide the base URL of your "
                    "regional API Gateway before proceeding."
                )

        if credentials is None:
            client_id = os.getenv("DAP_CLIENT_ID")
            if not client_id:
                raise DAPClientError(
                    "Missing DAP client ID. Please provide the client ID before proceeding. Obtain it from identity.instructure.com"
                )

            client_secret = os.getenv("DAP_CLIENT_SECRET")
            if not client_secret:
                raise DAPClientError(
                    "Missing DAP client secret. Please provide the client secret before proceeding. Obtain it from identity.instructure.com"
                )

            credentials = Credentials.create(
                client_id=client_id, client_secret=client_secret
            )

        if tracking is None:
            self._tracking = read_dap_tracking_env_var()
        else:
            self._tracking = tracking

        self._base_url = base_url.rstrip("/")
        self._credentials = credentials

    async def __aenter__(self) -> "DAPSession":
        "Initiates a new client session."

        tracking_data = (
            TrackingData(client_id=self._credentials.client_id)
            if self._tracking
            else None
        )
        self._dap_session = DAPSession(self._base_url, self._credentials, tracking_data)
        return self._dap_session

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[types.TracebackType],
    ) -> None:
        "Terminates a client session."

        if self._dap_session is not None:
            if self._dap_session.tracking_data is not None:
                await send_tracking_data(self._dap_session.tracking_data)
            await self._dap_session.close()
            self._dap_session = None


class DAPSession:
    """
    Represents an authenticated session to DAP.

    Talks to the outside world over two independent HTTP channels: `_dap_api`
    for the authenticated DAP API, and `_downloads` for pre-signed resource
    URLs, which carry their own authorization and must never receive the API
    bearer token. Each owns its own connection pool.
    """

    _base_url: str
    _dap_api: DapApiChannel
    _downloads: DownloadChannel
    tracking_data: Optional[TrackingData]

    def _generate_traceparent(self) -> str:
        trace_id = uuid.uuid4()  # use for all http calls in this session
        span_id = "0000000000000001"  # a.k.a. parent_id, not used
        trace_flags = "00"
        return f"00-{trace_id}-{span_id}-{trace_flags}"

    def __init__(
        self,
        base_url: str,
        credentials: Credentials,
        tracking_data: Optional[TrackingData] = None,
    ) -> None:
        """
        Creates a new logical session by opening the channels it talks over.
        """

        self._base_url = base_url
        self.tracking_data = tracking_data
        headers = default_headers(self._generate_traceparent())
        self._dap_api = DapApiChannel(base_url, credentials, headers)
        self._downloads = DownloadChannel(headers)
        logger.debug(
            f"DAP API Client created with base URL: {self._base_url} using headers: {headers}"
        )

    async def close(self) -> None:
        """
        Closes the underlying network sockets.
        """

        await self._dap_api.close()
        await self._downloads.close()

    async def _get(
        self,
        path: str,
        response_type: Type[T],
        table_access: Optional[TableAccess] = None,
    ) -> T:
        "Sends a GET request over the API channel. See `DapApiChannel.get`."

        return await self._dap_api.get(path, response_type, table_access)

    async def _post(
        self,
        path: str,
        request_data: Any,
        response_type: Type[T],
        table_access: Optional[TableAccess] = None,
    ) -> T:
        "Sends a POST request over the API channel. See `DapApiChannel.post`."

        return await self._dap_api.post(path, request_data, response_type, table_access)

    async def authenticate(self, table_access: Optional[TableAccess] = None) -> None:
        """
        Authenticates with API key to receive a table-restricted JWT, and pins it
        as the access level for subsequent requests on this session.

        See `DapApiChannel.authenticate` for the caching and access level rules.

        :param table_access: The table the requested JWT should be restricted to.
            Omit to reuse the most recently used access level on this session if one exists,
            otherwise a token with no table access is requested (e.g. on a fresh session).
        """

        await self._dap_api.authenticate(table_access)

    async def query_snapshot(
        self, namespace: str, table: str, query: SnapshotQuery
    ) -> Job:
        """
        Starts a snapshot query.
        """

        logger.debug(f"Query snapshot of table: {table}. Query: {query}")

        table_access = TableAccess(namespace=namespace, table=table)
        job = await self._post(
            f"/dap/query/{namespace}/table/{table}/data",
            query,
            Job,  # type: ignore
            table_access,
        )
        return job

    async def query_incremental(
        self, namespace: str, table: str, query: IncrementalQuery
    ) -> Job:
        """
        Starts an incremental query.
        """

        logger.debug(f"Query updates for table: {table}")
        table_access = TableAccess(namespace=namespace, table=table)
        job = await self._post(
            f"/dap/query/{namespace}/table/{table}/data",
            query,
            Job,  # type: ignore
            table_access,
        )
        return job

    async def get_tables(self, namespace: str) -> List[str]:
        """
        Retrieves the list of tables available for querying.

        :param namespace: A namespace identifier such as `canvas` or `mastery`.
        :returns: A list of tables available for querying in the given namespace.
        """
        if self.tracking_data:
            self.tracking_data.set_cmd_info("list-tables", namespace, None)
        logger.debug(f"Get list of tables from namespace: {namespace}")
        ui.info("Retrieving list of tables...")
        table_access = TableAccess(namespace=None, table=None)
        table_list = await self._get(
            f"/dap/query/{namespace}/table", TableList, table_access
        )
        return table_list.tables

    async def get_namespaces(self) -> List[str]:
        """
        Retrieves the list of namespaces available for querying.

        :returns: A list of namespaces available for querying.
        """
        if self.tracking_data:
            self.tracking_data.set_cmd_info("list-namespaces", None, None)
        logger.debug("Get list of namespaces")
        ui.info("Retrieving list of namespaces...")
        table_access = TableAccess(namespace=None, table=None)
        namespace_list = await self._get(
            "/dap/query/namespace", NamespaceList, table_access
        )
        return namespace_list.namespaces

    async def get_table_list(self, namespace: str, table_param: str) -> List[str]:
        """
        Returns a list of tables on which an operation should be performed.
        In case of "all" the list of tables for that namespace is retrieved.

        :param namespace: A namespace identifier such as `canvas` or `mastery`.
        :param table_param: can be a single table, a comma separated list of table names or the special "all".
        """
        if table_param == "all":
            return await self.get_tables(namespace)
        else:
            return table_param.split(",")

    def _log_error(self, operation_name: str, e: BaseException) -> None:
        if isinstance(e, OperationError):
            err_str = f"Operation {operation_name} failed. Reason: {e.message} ({e.type}, {e.uuid})"
            ui.error(escape(err_str))
            logger.error(err_str)
        elif isinstance(e, (asyncio.exceptions.CancelledError, KeyboardInterrupt)):
            err_str = (
                f"Operation {operation_name} was interrupted: {e.__class__.__name__}"
            )
            ui.warning(err_str)
            logger.error(err_str)
        else:
            reason = e.describe() if isinstance(e, OAuthTokenError) else str(e)
            err_str = f"Operation {operation_name} failed. Reason: {reason}"
            ui.error(escape(err_str))
            logger.error(err_str)

    async def execute_operation_on_tables(
        self,
        namespace: str,
        tables: str,
        operation_name: str,
        operation: Callable[[str, str], Awaitable[T]],
    ) -> None:
        """
        Executes given operation on multiple tables in the given namespace.
        The operations are currently executed in a sequential manner,
        independently of each other but some error types stop the execution
        of subsequent operations since in these cases they would also fail.

        :param namespace: A namespace identifier such as `canvas` or `mastery`.
        :param tables: A single table, a comma separated list of table names or the special "all".
        :param operation_name: The CLI command that is being executed.
        :param operation: The operation to execute on a single table.
        """

        table_list = await self.get_table_list(namespace, tables)
        results: list[T] = []
        exceptions: list[BaseException] = []
        for idx, table in enumerate(table_list):
            if idx > 0:
                print()  # empty lines between tables for better readability
            tables_idx_progress_str = ""
            if len(table_list) > 1:
                tables_idx_progress_str = f" ({idx + 1} of {len(table_list)})"
            try:
                ui.title(
                    f"Executing [bold]{operation_name}[/bold] on table [bold]{table}[/bold]{tables_idx_progress_str}"
                )
                logger.info(
                    f"Starting {operation_name} of table '{table}'{tables_idx_progress_str}"
                )
                result = await operation(namespace, table)
                ui.success(
                    f"Operation [bold]{operation_name}[/bold] completed successfully "
                    f"on table [bold]{table}[/bold]{tables_idx_progress_str}"
                )
                logger.info(
                    f"Finished {operation_name} of table '{table}'{tables_idx_progress_str}"
                )
                results.append(result)
            # fatal error types
            except (
                ServerError,
                AuthenticationError,
                OAuthTokenError,
                AccountNotOnboardedError,
                AccountDisabledError,
                AccountUnderMaintenanceError,
                DAPClientError,
                NotImplementedError,
                asyncio.exceptions.CancelledError,
                KeyboardInterrupt,
            ) as e:
                self._log_error(operation_name, e)
                ui.error(
                    f"Operation [bold]{operation_name}[/bold] failed for table [bold]{table}[/bold]{tables_idx_progress_str}"
                )
                logger.error(
                    f"Operation {operation_name} failed for table '{table}'{tables_idx_progress_str}"
                )
                exceptions.append(e)
                break
            except Exception as e:
                self._log_error(operation_name, e)
                ui.error(
                    f"Operation [bold]{operation_name}[/bold] failed for table [bold]{table}[/bold]{tables_idx_progress_str}"
                )
                logger.error(
                    f"Operation {operation_name} failed for table '{table}'{tables_idx_progress_str}"
                )
                exceptions.append(e)
        if self.tracking_data:
            self.tracking_data.set_cmd_info(operation_name, namespace, tables)
        skipped_table_count = len(table_list) - (len(results) + len(exceptions))
        if len(exceptions) > 0:
            skipped_tables_str = (
                f", {skipped_table_count} skipped" if skipped_table_count > 0 else ""
            )
            raise BaseExceptionGroup(
                f"Operation {operation_name} completed with issues: {len(exceptions)} failed{skipped_tables_str} out of {len(table_list)} table(s).",
                exceptions,
            )

    async def download_tables_data(
        self, namespace: str, tables: str, query: Query, output_directory: str
    ) -> None:
        async def download_fn(namespace: str, table: str) -> DownloadTableDataResult:
            return await self.download_table_data(
                namespace, table, query, output_directory
            )

        await self.execute_operation_on_tables(
            namespace,
            tables,
            "snapshot" if isinstance(query, SnapshotQuery) else "incremental",
            download_fn,
        )

    async def download_tables_schema(
        self, namespace: str, tables: str, output_directory: str
    ) -> None:
        async def download_fn(namespace: str, table: str) -> None:
            await self.download_table_schema(namespace, table, output_directory)

        await self.execute_operation_on_tables(namespace, tables, "schema", download_fn)

    async def get_table_schema(self, namespace: str, table: str) -> VersionedSchema:
        """
        Retrieves the versioned schema of a table.

        :param namespace: A namespace identifier such as `canvas` or `mastery`.
        :param table: A table identifier such as `submissions`, `quizzes`, or `users`.
        :returns: The schema of the table as exposed by DAP API.
        """

        logger.debug(f"Get schema of table: {table}")
        table_access = TableAccess(namespace=None, table=None)
        versioned_schema = await self._get(
            f"/dap/query/{namespace}/table/{table}/schema",
            VersionedSchema,
            table_access,
        )
        if self.tracking_data:
            self.tracking_data.set_cmd_info("schema", namespace, table)
        return versioned_schema

    async def download_table_schema(
        self, namespace: str, table: str, output_directory: str
    ) -> None:
        """
        Saves the schema as a JSON file into a local directory.

        :param namespace: A namespace identifier such as `canvas` or `mastery`.
        :param table: A table identifier such as `submissions`, `quizzes`, or `users`.
        :param output_directory: Path to the directory to save the JSON file to.
        """

        versioned_schema = await self.get_table_schema(namespace, table)
        schema_version = versioned_schema.version
        json_object = object_to_json(versioned_schema)

        os.makedirs(output_directory, exist_ok=True)
        file_name = f"{table}_schema_version_{schema_version}.json"
        file_path = os.path.join(output_directory, file_name)
        with open(file_path, "w") as file:
            json.dump(json_object, file, indent=4)
        ui.info(f"Schema saved to [underline]{escape(file_path)}[/underline]")
        logger.info(f"JSON schema downloaded to file {file_path}")

    async def get_job(self, job_id: JobID, namespace: str, table: str) -> Job:
        """
        Retrieve job status.

        :param job_id: Identifier of the job to check.
        :param namespace: The namespace the job's query was restricted to.
        :param table: The table the job's query was restricted to.
        """

        logger.debug(f"Retrieving job state for job {job_id}")
        table_access = TableAccess(namespace=namespace, table=table)
        job = await self._get(f"/dap/job/{job_id}", Job, table_access)  # type: ignore
        return job

    async def get_job_status(
        self, job_id: JobID, namespace: str, table: str
    ) -> JobStatus:
        """
        Retrieve job status.
        """

        job = await self.get_job(job_id, namespace, table)
        return job.status

    async def get_objects(
        self, job_id: JobID, namespace: str, table: str
    ) -> List[Object]:
        """
        Retrieve object IDs once the query is completed successfully.

        :param job_id: Identifier of the job to retrieve object IDs for.
        :param namespace: The namespace the job's query was restricted to.
        :param table: The table the job's query was restricted to.
        """

        logger.debug(f"Retrieving object IDs for job {job_id}")
        table_access = TableAccess(namespace=namespace, table=table)
        job = await self._get(f"/dap/job/{job_id}", Job, table_access)  # type: ignore
        return typing.cast(CompleteJob, job).objects

    async def get_resources(
        self, objects: List[Object], namespace: str, table: str
    ) -> Dict[ObjectID, Resource]:
        """
        Retrieve URLs to data stored remotely.

        :param objects: List of output objects to retrieve resource URLs for.
        :param namespace: The namespace the objects' query was restricted to.
        :param table: The table the objects' query was restricted to.
        """

        logger.debug("Retrieve resource URLs for objects:")
        logger.debug([o.id for o in objects])

        table_access = TableAccess(namespace=namespace, table=table)
        response = await self._post(
            "/dap/object/url", objects, ResourceResult, table_access
        )

        return response.urls

    async def download_resources(
        self, resources: List[Resource], output_directory: str, decompress: bool = False
    ) -> List[str]:
        """
        Save data stored remotely into a local directory.

        :param resources: List of output resources to be downloaded.
        :param output_directory: Path to the target directory to save downloaded files to.
        :param decompress: If True, the file will be decompressed after downloading. Default is False.
        :returns: A list of paths to files saved in the local file system.
        """

        downloads = [
            self.download_resource(resource, output_directory, decompress)
            for resource in resources
        ]
        local_files = await gather_n(downloads, concurrency=DOWNLOAD_CONCURRENCY)
        logger.info(f"Files from server downloaded to folder: {output_directory}")
        return local_files

    async def download_resource(
        self, resource: Resource, output_directory: str, decompress: bool = False
    ) -> str:
        """
        Save a single remote file to a local directory.

        :param resource: Resource to download.
        :param output_directory: Path of the target directory to save the downloaded file.
        :param decompress: If True, the file will be decompressed after downloading. Default is False.
        :returns: A path of the file saved in the local file system.
        """

        os.makedirs(output_directory, exist_ok=True)
        url = str(resource.url)
        parsed_url = urlparse(url)
        file_name = os.path.basename(parsed_url.path)
        file_path = os.path.join(output_directory, file_name)

        if decompress:
            file_path = file_path.removesuffix(".gz")

        # Ensure the resolved path stays within the target directory. The file
        # name is derived from a server-supplied URL, so guard against path
        # traversal before opening the file for writing.
        output_root = os.path.realpath(output_directory)
        resolved_path = os.path.realpath(file_path)
        if os.path.commonpath([output_root, resolved_path]) != output_root:
            raise DownloadError(
                f"refusing to write outside the output directory: {file_name}"
            )

        logger.debug(f"Downloading: {url} to {resolved_path}")

        async with aiofiles.open(resolved_path, "wb") as output_file:
            decompressor = (
                zlib.decompressobj(16 + zlib.MAX_WBITS) if decompress else None
            )
            async for stream in self.stream_resource(resource):
                async for chunk in stream.iter_chunked(64 * 1024):
                    await output_file.write(
                        decompressor.decompress(chunk) if decompressor else chunk
                    )

        logger.debug(f"Download complete of {url} to {file_path}")

        return file_path

    async def download_objects(
        self,
        objects: List[Object],
        namespace: str,
        table: str,
        output_directory: str,
        decompress: bool = False,
    ) -> List[str]:
        """
        Save data stored remotely into a local directory.

        :param objects: List of output objects to be downloaded.
        :param namespace: The namespace the objects' query was restricted to.
        :param table: The table the objects' query was restricted to.
        :param output_directory: Path to the target directory to save downloaded files to.
        :param decompress: If True, the file will be decompressed after downloading. Default is False.
        :returns: A list of paths to files saved in the local file system.
        """
        with ui.JobProgress(
            "Downloading files from server...", total_steps=len(objects)
        ) as progress:
            downloads = [
                self.download_object(
                    object, namespace, table, output_directory, decompress, progress
                )
                for object in objects
            ]
            local_files = await gather_n(downloads, concurrency=DOWNLOAD_CONCURRENCY)

        return local_files

    async def download_object(
        self,
        object: Object,
        namespace: str,
        table: str,
        output_directory: str,
        decompress: bool,
        progress: ui.JobProgress | None = None,
    ) -> str:
        """
        Save a single remote file to a local directory.

        :param object: Object to download.
        :param namespace: The namespace the object's query was restricted to.
        :param table: The table the object's query was restricted to.
        :param output_directory: Path of the target directory to save the downloaded file.
        :param decompress: If True, the file will be decompressed after downloading. Default is False.
        :param progress: A progress bar to update during the download.
        :returns: A path of the file saved in the local file system.
        """

        resource = (await self.get_resources([object], namespace, table))[object.id]
        file_path = await self.download_resource(resource, output_directory, decompress)
        if progress is not None:
            progress.update(advance=1)
        return file_path

    async def stream_resource(
        self, resource: Resource
    ) -> AsyncIterator[aiohttp.StreamReader]:
        """
        Creates a stream reader for the given resource.

        :param resource: Resource to download.
        :yields: An asynchronous generator that can be used with an asynchronous context manager.
        :raises DownloadError: Raised when the host returns an HTTP error
            response, and rejects the request.
        """

        async with self._downloads.get(str(resource.url)) as response:
            yield response.content

    async def wait_seconds(self, seconds: float) -> None:
        await asyncio.sleep(seconds)

    async def await_job(self, job: Job, namespace: str, table: str) -> Job:
        """
        Wait until a job terminates.

        :param job: A job that might be still running.
        :param namespace: The namespace the job's query was restricted to.
        :param table: The table the job's query was restricted to.
        :returns: A job that has completed with success or terminated with failure.
        """
        with ui.JobProgress("Waiting for query job to finish ...") as _:
            while not job.status.isTerminal():
                delay = 5
                logger.info(
                    f"Query job still in status: {job.status.value}. Checking again in {delay} seconds..."
                )
                await self.wait_seconds(delay)

                job = await self.get_job(job.id, namespace, table)

        ui.info(f"Query job finished with status {job.status.value} (ID: {job.id})")
        logger.debug(f"Query job finished with status: {job.status.value}")
        return job

    async def __execute_query(self, namespace: str, table: str, query: Query) -> Job:
        if isinstance(query, SnapshotQuery):
            job = await self.query_snapshot(namespace, table, query)
        elif isinstance(query, IncrementalQuery):
            job = await self.query_incremental(namespace, table, query)
        else:
            raise TypeError(f"Internal error, invalid query type: {type(query)}")
        return job

    async def execute_job(
        self,
        namespace: str,
        table: str,
        query: Query,
    ) -> Job:
        """
        Start a query job and wait until it terminates.
        """

        job = await self.__execute_query(namespace, table, query)

        current_time = datetime.now(timezone.utc)
        if (
            job.status is JobStatus.Complete
            and job.expires_at is not None
            and (job.expires_at - current_time).total_seconds()
            < EXPIRE_AT_VERY_CLOSE_SECONDS
        ):
            logger.info(
                "Existing completed job is about to expire, waiting and requesting a new job..."
            )
            await self.wait_seconds(EXPIRE_AT_VERY_CLOSE_SECONDS + 5)
            job = await self.__execute_query(namespace, table, query)

        if job.status.isTerminal():
            logger.info(
                f"Query job already finished with ID {job.id} and status {job.status.value}"
            )
            return job

        logger.info(f"Query started with job ID: {job.id}")

        job = await self.await_job(job, namespace, table)
        return job

    async def download_table_data(
        self,
        namespace: str,
        table: str,
        query: Query,
        output_directory: str,
        decompress: bool = False,
    ) -> DownloadTableDataResult:
        """
        Executes a query job and downloads data to a local directory.

        :param namespace: A namespace identifier such as `canvas` or `mastery`.
        :param table: A table identifier such as `submissions`, `quizzes`, or `users`.
        :param query: An object that encapsulates the parameters of the snapshot or incremental query to execute.
        :param output_directory: Path to the directory to save downloaded files to.
        :param decompress: If True, the file will be decompressed after downloading. Default is False.
        :returns: Result of the query, including a list of paths to files saved in the local file system.
        :raises DAPClientError: Raised when the query returned an error or fetching data has failed.
        """

        # fail early if query format is Parquet and decompression is requested
        if decompress and query.format == Format.Parquet:
            raise DAPClientError(
                "Decompression is not supported for 'parquet' format. Please use another format."
            )

        # fail early if output directory does not exist and cannot be created
        os.makedirs(output_directory, exist_ok=True)

        job = await self.execute_job(namespace, table, query)

        if job.status is not JobStatus.Complete:
            raise DAPClientError(
                f"Query job ended with status: {job.status.value}. Please review the job logs."
            )

        objects = await self.get_objects(job.id, namespace, table)
        directory = os.path.join(output_directory, f"job_{job.id}")

        downloaded_files = await self.download_objects(
            objects, namespace, table, directory, decompress
        )
        file_count_str = (
            f"{len(downloaded_files)} files" if len(downloaded_files) > 1 else "file"
        )
        ui.info(
            f"Downloaded {file_count_str} to [underline]{escape(directory)}[/underline]",
        )
        logger.info(f"Files from server downloaded to folder: {directory}")

        if isinstance(job, CompleteSnapshotJob):
            logger.info(
                f"Snapshot query results have been successfully retrieved:\n{job.json()}"
            )
            return DownloadTableDataResult(
                job.schema_version, job.at, job.id, downloaded_files
            )
        elif isinstance(job, CompleteIncrementalJob):
            logger.info(
                f"Incremental query results have been successfully retrieved:\n{job.json()}"
            )
            return DownloadTableDataResult(
                job.schema_version, job.until, job.id, downloaded_files
            )
        else:
            raise DAPClientError(
                f"Unexpected job type: {type(job)}. Please verify the input."
            )

    async def get_table_data(
        self, namespace: str, table: str, query: Query
    ) -> GetTableDataResult:
        """
        Executes a query job on a given table.

        :param namespace: A namespace identifier such as `canvas` or `mastery`.
        :param table: A table identifier such as `submissions`, `quizzes`, or `users`.
        :param query: An object that encapsulates the parameters of the snapshot or incremental query to execute.
        :returns: Result of the query, including metadata.
        :raises DAPClientError: Raised when the query returned an error or fetching data has failed.
        """

        job = await self.execute_job(namespace, table, query)

        if job.status is JobStatus.Complete:
            objects = await self.get_objects(job.id, namespace, table)

            if isinstance(job, CompleteSnapshotJob):
                logger.info(f"Data has been successfully retrieved:\n{job.json()}")
                return GetTableDataResult(job.schema_version, job.at, job.id, objects)

            elif isinstance(job, CompleteIncrementalJob):
                logger.info(f"Data has been successfully retrieved:\n{job.json()}")
                return GetTableDataResult(
                    job.schema_version, job.until, job.id, objects
                )

            else:
                raise DAPClientError(
                    f"Unexpected job type: {type(job)}. Please verify the input."
                )

        else:
            raise DAPClientError(
                f"Query job ended with status: {job.status.value}. Please review the job logs."
            )
