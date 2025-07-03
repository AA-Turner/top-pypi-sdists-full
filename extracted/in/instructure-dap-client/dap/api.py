import asyncio
import json
import logging
import os
import sys
import types
import typing
import uuid
import zlib
from datetime import datetime, timedelta, timezone
from http import HTTPStatus
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
    Union,
)
from urllib.parse import urlparse

import aiofiles
import aiohttp
import jwt
from aiohttp_retry import ExponentialRetry, RetryClient
from strong_typing.serialization import json_dump_string, json_to_object, object_to_json

from . import __version__, ui
from .commands.global_options import DAP_API_URL_DEFAULT, read_dap_tracking_env_var
from .concurrency import gather_n
from .dap_error import (
    AccountDisabledError,
    AccountNotOnboardedError,
    AccountUnderMaintenanceError,
    AuthenticationError,
    NotFoundError,
    OperationError,
    OutOfRangeError,
    ProcessingError,
    ServerError,
    SnapshotRequiredError,
    ValidationError,
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
    Object,
    ObjectID,
    Query,
    Resource,
    ResourceResult,
    SnapshotQuery,
    TableList,
    TokenProperties,
    VersionedSchema,
)
from .networking import get_content_type
from .tracking import TrackingData, send_tracking_data

logger = logging.getLogger("dap")

T = TypeVar("T")

# prevent "RuntimeError: Event loop is closed" on Windows platforms
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # type: ignore


class DAPClientError(RuntimeError):
    pass


REQUEST_RETRY_COUNT = 3
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
    _session: Optional["DAPSession"]
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
                base_url = DAP_API_URL_DEFAULT

        if credentials is None:
            client_id = os.getenv("DAP_CLIENT_ID")
            if not client_id:
                raise DAPClientError("Missing DAP client ID. Please provide the client ID before proceeding. Obtain it from identity.instructure.com")

            client_secret = os.getenv("DAP_CLIENT_SECRET")
            if not client_secret:
                raise DAPClientError("Missing DAP client secret. Please provide the client secret before proceeding. Obtain it from identity.instructure.com")

            credentials = Credentials.create(
                client_id=client_id, client_secret=client_secret
            )

        if tracking is None:
            self._tracking = read_dap_tracking_env_var()
        else:
            self._tracking = tracking

        self._base_url = base_url.rstrip("/")
        self._credentials = credentials

        logger.debug(f"Client region: {self._credentials.client_region}")

    async def __aenter__(self) -> "DAPSession":
        "Initiates a new client session."

        session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30 * 60, connect=30),
        )
        tracking_data = TrackingData(client_id=self._credentials.client_id) if self._tracking else None
        self._session = DAPSession(session, self._base_url, self._credentials, tracking_data)
        return self._session

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[types.TracebackType],
    ) -> None:
        "Terminates a client session."

        if self._session is not None:
            if self._session.tracking_data is not None:
                await send_tracking_data(self._session.tracking_data)
            await self._session.close()
            self._session = None


class AccessToken:
    """
    A JWT access token. This object is immutable.

    The access token counts as sensitive information not to be exposed (e.g. in logs).
    """

    _token: str
    _expiry: datetime

    def __init__(self, jwt_token: str) -> None:
        "Creates a new JWT access token."

        self._token = jwt_token
        decoded_jwt = jwt.decode(jwt_token, options={"verify_signature": False})
        expiry = int(decoded_jwt["exp"])
        self._expiry = datetime.fromtimestamp(expiry, tz=timezone.utc)

    def __str__(self) -> str:
        "Returns the string representation of the JWT access token."

        return self._token

    def is_expiring(self) -> bool:
        """
        Checks if the token is about to expire.

        :returns: True if the token is about to expire.
        """

        latest_accepted_expiry = datetime.now(tz=timezone.utc) + timedelta(minutes=5)
        return self._expiry < latest_accepted_expiry


class DAPSession:
    """
    Represents an authenticated session to DAP.
    """

    _base_url: str
    _session: aiohttp.ClientSession
    _credentials: Credentials
    _access_token: Optional[AccessToken] = None
    _retry_client: RetryClient
    _resources_download_client: RetryClient
    _headers: Dict[str, str]
    tracking_data: Optional[TrackingData]

    def _generate_traceparent(self) -> str:
        trace_id = uuid.uuid4()  # use for all http calls in this session
        span_id = "0000000000000001"  # a.k.a. parent_id, not used
        trace_flags = "00"
        return f"00-{trace_id}-{span_id}-{trace_flags}"

    def __init__(
        self, session: aiohttp.ClientSession, base_url: str, credentials: Credentials, tracking_data: Optional[TrackingData] = None
    ) -> None:
        """
        Creates a new logical session by encapsulating a network connection.
        """

        self._base_url = base_url
        self._session = session
        self._credentials = credentials
        self.tracking_data = tracking_data
        self._retry_client = RetryClient(
            client_session=self._session,
            retry_options=ExponentialRetry(attempts=REQUEST_RETRY_COUNT),
            raise_for_status=True,
        )
        resources_session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30 * 60, connect=30),
        )
        self._resources_download_client = RetryClient(
            client_session=resources_session,
            retry_options=ExponentialRetry(attempts=REQUEST_RETRY_COUNT),
            raise_for_status=True,
        )
        self._headers = {
            "User-Agent": f"DataAccessPlatform/{__version__}",
            "traceparent": self._generate_traceparent(),
        }
        logger.debug(
            f"DAP API Client created with base URL: {self._base_url} using headers: {self._headers}"
        )

    async def close(self) -> None:
        """
        Closes the underlying network sockets.
        """

        await self._session.close()
        await self._resources_download_client.close()

    async def _get(self, path: str, response_type: Type[T]) -> T:
        """
        Sends a request to the server and parses the response into the expected type.

        :param path: The path component of the endpoint to invoke.
        :param response_type: The object type the endpoint returns on success.
        :returns: The object returned on success.
        :raises Exception: The object returned on failure.
        """

        await self.authenticate()
        async with self._retry_client.get(
            f"{self._base_url}{path}", headers=self._headers
        ) as response:
            return await self._process(response, response_type)

    @typing.no_type_check # mypy shits itself on Union type used in json_to_object
    def _map_to_error_type(
        self, status_code: int, response_body: Any
    ) -> Union[
        ValidationError,
        NotFoundError,
        OutOfRangeError,
        SnapshotRequiredError,
        AuthenticationError,
        AccountDisabledError,
        AccountNotOnboardedError,
        AccountUnderMaintenanceError,
        ProcessingError,
        ServerError,
    ]:
        """
        Maps error body and status to Python error object.
        """

        if "error" not in response_body:
            return ServerError(response_body)

        response_body_error = response_body["error"]
        try:
            if status_code == HTTPStatus.UNAUTHORIZED.value:
                return json_to_object(AuthenticationError, response_body_error)
            elif status_code == HTTPStatus.FORBIDDEN.value:
                return json_to_object(
                    Union[AccountDisabledError, AccountNotOnboardedError, AccountUnderMaintenanceError],
                    response_body_error,
                )
            else:
                return json_to_object(
                    Union[ValidationError, NotFoundError, OutOfRangeError, SnapshotRequiredError, ProcessingError],
                    response_body_error,
                )
        except:
            return ServerError(response_body_error)

    async def _post(self, path: str, request_data: Any, response_type: Type[T]) -> T:
        """
        Sends a request to the server by serializing a payload object, and parses the response into the expected type.

        :param path: The path component of the endpoint to invoke.
        :param request_data: The object to pass in the request body.
        :param response_type: The object type the endpoint returns on success.
        :returns: The object returned on success.
        :raises Exception: The object returned on failure.
        """

        await self.authenticate()

        request_payload = object_to_json(request_data)
        logger.debug(f"POST request payload:\n{repr(request_payload)}")

        async with self._session.post(
            f"{self._base_url}{path}",
            data=json_dump_string(request_payload),
            headers={"Content-Type": "application/json"} | self._headers,
        ) as response:
            return await self._process(response, response_type)

    async def _post_auth_request(self, basic_credentials: str) -> TokenProperties:
        """
        Sends an authentication request to the Identity Service through Instructure API Gateway,
        and parses the response into a TokenProperties object.

        :param basic_credentials: Basic credentials.
        :returns: An access token and metadata.
        :raises Exception: The object returned on failure.
        """

        async with self._session.post(
            f"{self._base_url}/ids/auth/login",
            data={"grant_type": "client_credentials"},
            headers={"Authorization": "Basic " + basic_credentials} | self._headers,
        ) as response:
            return await self._process(response, TokenProperties, suppress_output=True)

    async def _process(
        self,
        response: aiohttp.ClientResponse,
        response_type: Type[T],
        suppress_output: bool = False,
    ) -> T:
        """
        Extracts an object instance from an HTTP response body.
        """

        content_type = get_content_type(response.headers.get("Content-Type", ""))
        if content_type == "application/json":
            response_payload = await response.json()
        else:
            response_text = await response.text()
            if response_text:
                logger.error(f"Unexpected response from server. Unable to parse the HTTP response. \n{response_text}")

            raise DAPClientError("Unexpected response from server. Unable to parse the HTTP response.")

        if not suppress_output:
            logger.debug(f"GET/POST response payload:\n{repr(response_payload)}")

        # HTTP status codes between 400 (inclusive) and 600 (exclusive) indicate an error
        # (includes non-standard 5xx server-side error codes)
        if HTTPStatus.BAD_REQUEST.value <= response.status < 600:
            error_object = self._map_to_error_type(response.status, response_payload)
            logger.warning(f"Received error in response: {error_object}")
            raise error_object
        else:
            return json_to_object(response_type, response_payload)

    async def authenticate(self) -> None:
        """
        Authenticates with API key to receive a JWT.
        """

        if self._access_token is not None and not self._access_token.is_expiring():
            return

        logger.debug(
            f"Authenticating to DAP in region {self._credentials.client_region}"
        )

        # drop expired auth header, re-authentication will set new one
        self._session.headers.pop("Authorization", None)

        properties = await self._post_auth_request(self._credentials.basic_credentials)
        self._access_token = AccessToken(properties.access_token)
        self._session.headers.update(
            {"Authorization": "Bearer " + str(self._access_token)}
        )

    async def query_snapshot(
        self, namespace: str, table: str, query: SnapshotQuery
    ) -> Job:
        """
        Starts a snapshot query.
        """

        logger.debug(f"Query snapshot of table: {table}. Query: {query}")

        job = await self._post(f"/dap/query/{namespace}/table/{table}/data", query, Job)  # type: ignore
        return job

    async def query_incremental(
        self, namespace: str, table: str, query: IncrementalQuery
    ) -> Job:
        """
        Starts an incremental query.
        """

        logger.debug(f"Query updates for table: {table}")
        job = await self._post(f"/dap/query/{namespace}/table/{table}/data", query, Job)  # type: ignore
        return job

    async def get_tables(self, namespace: str) -> List[str]:
        """
        Retrieves the list of tables available for querying.

        :param namespace: A namespace identifier such as `canvas` or `mastery`.
        :returns: A list of tables available for querying in the given namespace.
        """
        if self.tracking_data:
            self.tracking_data.set_cmd_info("list", namespace, None)
        logger.debug(f"Get list of tables from namespace: {namespace}")
        ui.info("Retrieving list of tables...")
        table_list = await self._get(f"/dap/query/{namespace}/table", TableList)
        return table_list.tables

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
            err_str = f"Operation {operation_name} failed. Reason: {e.message} {e.uuid}"
            ui.error(err_str)
            logger.error(err_str)
        elif isinstance(e, (asyncio.exceptions.CancelledError, KeyboardInterrupt)):
            err_str = f"Operation {operation_name} was interrupted: {e.__class__.__name__}"
            ui.warning(err_str)
            logger.error(err_str)
        else:
            err_str = f"Operation {operation_name} failed. Reason: {e}"
            ui.error(err_str)
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
                print() # empty lines between tables for better readability
            tables_idx_progress_str = ""
            if len(table_list) > 1:
                tables_idx_progress_str = f" ({idx + 1} of {len(table_list)})"
            try:
                ui.title(f"Executing [bold]{operation_name}[/bold] on table [bold]{table}[/bold]{tables_idx_progress_str}")
                logger.info(
                    f"Starting {operation_name} of table '{table}'{tables_idx_progress_str}"
                )
                result = await operation(namespace, table)
                ui.success(f"Operation [bold]{operation_name}[/bold] completed successfully "
                           f"on table [bold]{table}[/bold]{tables_idx_progress_str}")
                logger.info(
                    f"Finished {operation_name} of table '{table}'{tables_idx_progress_str}"
                )
                results.append(result)
            # fatal error types
            except (
                ServerError,
                AuthenticationError,
                AccountNotOnboardedError,
                AccountDisabledError,
                AccountUnderMaintenanceError,
                DAPClientError,
                NotImplementedError,
                asyncio.exceptions.CancelledError,
                KeyboardInterrupt,
            ) as e:
                self._log_error(operation_name, e)
                ui.error(f"Operation [bold]{operation_name}[/bold] failed for table [bold]{table}[/bold]{tables_idx_progress_str}")
                logger.error(
                    f"Operation {operation_name} failed for table '{table}'{tables_idx_progress_str}"
                )
                exceptions.append(e)
                break
            except Exception as e:
                self._log_error(operation_name, e)
                ui.error(f"Operation [bold]{operation_name}[/bold] failed for table [bold]{table}[/bold]{tables_idx_progress_str}")
                logger.error(
                    f"Operation {operation_name} failed for table '{table}'{tables_idx_progress_str}"
                )
                exceptions.append(e)
        if self.tracking_data:
            self.tracking_data.set_cmd_info(operation_name, namespace, tables)
        skipped_table_count = len(table_list) - (len(results) + len(exceptions))
        if len(exceptions) > 0:
            skipped_tables_str = f", {skipped_table_count} skipped" if skipped_table_count > 0 else ""
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
            namespace, tables,
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
        versioned_schema = await self._get(
            f"/dap/query/{namespace}/table/{table}/schema", VersionedSchema
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
        ui.info(f"Schema saved to [underline]{file_path}[/underline]")
        logger.info(f"JSON schema downloaded to file {file_path}")

    async def get_job(self, job_id: JobID) -> Job:
        """
        Retrieve job status.
        """

        logger.debug(f"Retrieving job state for job {job_id}")
        job = await self._get(f"/dap/job/{job_id}", Job)  # type: ignore
        return job

    async def get_job_status(self, job_id: JobID) -> JobStatus:
        """
        Retrieve job status.
        """

        job = await self.get_job(job_id)
        return job.status

    async def get_objects(self, job_id: JobID) -> List[Object]:
        """
        Retrieve object IDs once the query is completed successfully.
        """

        logger.debug(f"Retrieving object IDs for job {job_id}")
        job = await self._get(f"/dap/job/{job_id}", Job)  # type: ignore
        return typing.cast(CompleteJob, job).objects

    async def get_resources(self, objects: List[Object]) -> Dict[ObjectID, Resource]:
        """
        Retrieve URLs to data stored remotely.
        """

        logger.debug("Retrieve resource URLs for objects:")
        logger.debug([o.id for o in objects])

        response = await self._post("/dap/object/url", objects, ResourceResult)

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

        logger.debug(f"Downloading: {url} to {file_path}")

        async with aiofiles.open(file_path, "wb") as output_file:
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
        self, objects: List[Object], output_directory: str, decompress: bool = False
    ) -> List[str]:
        """
        Save data stored remotely into a local directory.

        :param objects: List of output objects to be downloaded.
        :param output_directory: Path to the target directory to save downloaded files to.
        :param decompress: If True, the file will be decompressed after downloading. Default is False.
        :returns: A list of paths to files saved in the local file system.
        """
        with ui.JobProgress("Downloading files from server...",
                            total_steps=len(objects)) as progress:
            downloads = [
                self.download_object(object, output_directory, decompress, progress)
                for object in objects
            ]
            local_files = await gather_n(downloads, concurrency=DOWNLOAD_CONCURRENCY)

        return local_files

    async def download_object(
        self, object: Object, output_directory: str, decompress: bool, progress: ui.JobProgress | None = None
    ) -> str:
        """
        Save a single remote file to a local directory.

        :param object: Object to download.
        :param output_directory: Path of the target directory to save the downloaded file.
        :param decompress: If True, the file will be decompressed after downloading. Default is False.
        :param progress: A progress bar to update during the download.
        :returns: A path of the file saved in the local file system.
        """

        resource = (await self.get_resources([object]))[object.id]
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
        :raises DownloadError: Raised when the host returns an HTTP error response, and rejects the request.
        """

        async with self._resources_download_client.get(
            str(resource.url), headers=self._headers
        ) as response:
            if not response.ok:
                raise DownloadError(f"Request failed with HTTP status code: {response.status}")

            yield response.content

    async def wait_seconds(self, seconds: float) -> None:
        await asyncio.sleep(seconds)

    async def await_job(self, job: Job) -> Job:
        """
        Wait until a job terminates.

        :param job: A job that might be still running.
        :returns: A job that has completed with success or terminated with failure.
        """
        with ui.JobProgress("Waiting for query job to finish ...") as _:
            while not job.status.isTerminal():
                delay = 5
                logger.info(
                    f"Query job still in status: {job.status.value}. Checking again in {delay} seconds..."
                )
                await self.wait_seconds(delay)

                job = await self.get_job(job.id)

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

        job = await self.await_job(job)
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
            raise DAPClientError("Decompression is not supported for ‘parquet’ format. Please use another format.")

        # fail early if output directory does not exist and cannot be created
        os.makedirs(output_directory, exist_ok=True)

        job = await self.execute_job(namespace, table, query)

        if job.status is not JobStatus.Complete:
            raise DAPClientError(f"Query job ended with status: {job.status.value}. Please review the job logs.")

        objects = await self.get_objects(job.id)
        directory = os.path.join(output_directory, f"job_{job.id}")

        downloaded_files = await self.download_objects(objects, directory, decompress)
        file_count_str = f"{len(downloaded_files)} files" if len(downloaded_files) > 1 else "file"
        ui.info(f"Downloaded {file_count_str} to [underline]{directory}[/underline]", )
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
            raise DAPClientError(f"Unexpected job type: {type(job)}. Please verify the input.")

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
            objects = await self.get_objects(job.id)

            if isinstance(job, CompleteSnapshotJob):
                logger.info(f"Data has been successfully retrieved:\n{job.json()}")
                return GetTableDataResult(job.schema_version, job.at, job.id, objects)

            elif isinstance(job, CompleteIncrementalJob):
                logger.info(f"Data has been successfully retrieved:\n{job.json()}")
                return GetTableDataResult(
                    job.schema_version, job.until, job.id, objects
                )

            else:
                raise DAPClientError(f"Unexpected job type: {type(job)}. Please verify the input.")

        else:
            raise DAPClientError(f"Query job ended with status: {job.status.value}. Please review the job logs.")


class DownloadError(DAPClientError):
    def __init__(self, response_str: str) -> None:
        super().__init__(f"download error: {response_str}")
