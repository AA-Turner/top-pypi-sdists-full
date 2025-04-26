""" GraphQL Query Engine """
from __future__ import annotations

import asyncio
import atexit
import json
import logging
import os
import queue
import signal
import sys
import threading
import time
from concurrent.futures import Future, ThreadPoolExecutor, wait
from http import HTTPStatus
from threading import Event
from typing import Any, AsyncGenerator, Awaitable, Callable, Dict, Generator, List, Optional, Type, TypeVar, cast

import backoff
import requests
from gql.client import Client, ReconnectingAsyncClientSession
from gql.transport import AsyncTransport
from gql.transport.exceptions import TransportQueryError
from gql.transport.websockets import WebsocketsTransport
from graphql import DocumentNode
from websockets.exceptions import ConnectionClosed, PayloadTooBig, WebSocketException

from mcli.api.engine.retry import retry_with_backoff
from mcli.api.exceptions import ERROR_AUTH_KEY_MISSING, MAPIException, MCLIConfigError, MultiMAPIException
from mcli.api.schema.generic_model import DeserializableModel
from mcli.api.utils import check_python_certificates
from mcli.config import MCLIConfig, MCLIMode, get_timeout
from mcli.models.common import ObjectList, ObjectType
from mcli.version import __version__

logger = logging.getLogger(__name__)

# pylint: disable-next=invalid-name
THREADPOOL_WORKERS = 10
THREADPOOL: Optional[ThreadPoolExecutor] = None


def _create_threadpool() -> ThreadPoolExecutor:
    """Create a global threadpool for requests
    """
    logger.debug("Creating default threadpool")
    global THREADPOOL
    THREADPOOL = ThreadPoolExecutor(max_workers=THREADPOOL_WORKERS, thread_name_prefix='mosaicml-api')
    return THREADPOOL


def start_background_loop(loop: asyncio.AbstractEventLoop, terminate: Event):
    asyncio.set_event_loop(loop)

    async def wait_for_terminate():
        while not terminate.is_set():
            await asyncio.sleep(0.1)

    loop.run_until_complete(wait_for_terminate())


T = TypeVar("T")  # pylint: disable=invalid-name


class MAPIConnection:
    """Connection to a user's MAPI instance

    Args:
        api_key: The user's API key. If not specified, the value of the $MOSAICML_API_KEY
            environment variable will be used. If that does not exist, the value in the
            user's config file will be used. If that does not exist, then the access token
            will be used.
        access_token: The access token in the Main Container.
        endpoint: The MAPI URL to hit for all requests. If not specified, the value of the
            $MOSAICML_API_ENDPOINT environment variable will be used. If that does not
            exist, the default setting will be used.
        pool: An optional threadpool to use for all connection requests. If not provided,
            a shared pool will be used for all requests.

    Raises:
        MAPIException: Raised if the user does not have an API key set
    """
    endpoint: str
    override_api_key: Optional[str]

    def __init__(self,
                 api_key: Optional[str] = None,
                 endpoint: Optional[str] = None,
                 pool: Optional[ThreadPoolExecutor] = None):
        self._load_from_environment(endpoint)
        self.override_api_key = api_key
        self._pool = pool
        self._protected = set()
        self._updated_sigterm_handler = False
        self._prev: Optional[MAPIConnection] = None

        # MAPI websocket client connections
        self.connected = False
        self._client: Optional[Client] = None
        self._session: Optional[ReconnectingAsyncClientSession] = None
        self._loop = asyncio.new_event_loop()
        self._terminate = Event()

    def _load_from_environment(self, endpoint: Optional[str] = None) -> None:
        conf = MCLIConfig.load_config()

        # We usually default to the API key, but in the Databricks env, default to the PAT token
        # set in the token file
        if conf.mcli_mode in MCLIMode.get_dbx_modes():
            self.override_api_key = ''

        if endpoint is None:
            endpoint = conf.endpoint
        self.endpoint = endpoint

    @staticmethod
    def _set_connection(connection: Optional[MAPIConnection]) -> None:
        """Set the current connection instance

        Args:
            connection: The desired connection instance
        """
        global _CONNECTION
        _CONNECTION = connection

    @property
    def pool(self) -> ThreadPoolExecutor:
        """The ThreadPoolExecutor that will contain all MAPI requests
        """
        if self._pool is None:
            self._pool = THREADPOOL or _create_threadpool()

        return self._pool

    def protect_future_from_sigterm(self, future: Future[Any]) -> None:
        """Protect a future from being canceled by a SIGTERM"""
        if not self._updated_sigterm_handler:
            self.set_protecting_sigterm_handler()
        self._protected.add(future)
        logger.debug('Submitted future will be protected from SIGTERM')

    def cancel_unprotected_futures(self) -> None:
        """Cancel all unprotected futures in the threadpool's queue"""
        while True:
            try:
                item = self.pool._work_queue.get_nowait()  # pylint: disable=protected-access
                if item.future not in self._protected:
                    logger.debug('Canceling unprotected future')
                    item.future.cancel()

            except queue.Empty:
                logger.debug('Futures queue is empty')
                break

    def set_protecting_sigterm_handler(self) -> None:
        old_handler = signal.getsignal(signal.SIGTERM)

        def handler(signum, frame):
            del signum
            del frame
            try:
                # Cancel all unprotected futures
                self.cancel_unprotected_futures()

                # Wait for all protected futures
                if self._protected:
                    logger.debug('Waiting for protected futures')
                    wait(self._protected, timeout=None, return_when="ALL_COMPLETED")
            finally:
                logger.debug('Resetting SIGTERM handler and re-throwing')
                signal.signal(signal.SIGTERM, old_handler)
                os.kill(os.getpid(), signal.SIGTERM)

        logger.debug('Added a SIGTERM handler')
        signal.signal(signal.SIGTERM, handler)
        self._updated_sigterm_handler = True

    @property
    def request_header(self):
        # Make sure to use the latest access token
        conf = MCLIConfig.load_config()
        access_token = conf.access_token
        if conf.mcli_mode in MCLIMode.get_dbx_modes():
            api_key = ''  # set to empty string to force use of access token
            if len(access_token) == 0:
                raise MCLIConfigError('Access token must be set for Databricks staging')
        else:
            api_key = self.override_api_key or conf.api_key
        if len(api_key) == 0 and len(access_token) == 0:
            raise MCLIConfigError(ERROR_AUTH_KEY_MISSING)

        # Use the API key to auth, if specified. Otherwise, use the JWT token
        if len(api_key) != 0:
            auth = api_key
        else:
            auth = f'Bearer {access_token}'
        return {
            'Authorization': auth,
            'Content-Type': 'application/json',
            'x-mosaicml-client': 'mcli',
            'x-mosaicml-client-version': __version__
        }

    def create_websocket_connection(self) -> Client:
        if self._client is None:
            # Start the event loop if it's not already running
            if not self._loop.is_running():
                logger.debug("Starting threaded asyncio event loop")
                self.pool.submit(start_background_loop, self._loop, self._terminate)

            # Create the graphql client
            logger.debug("Creating websocket client in threaded event loop")
            self._client = asyncio.run_coroutine_threadsafe(self._create_gql_client(),
                                                            self._loop).result(timeout=get_timeout(10))
            logger.debug("Websocket client created")
            if (sys.version_info.major >= 3 and sys.version_info.minor >= 9) and hasattr(threading, '_register_atexit'):
                # This is only in python >= 3.9, but checking attribute to be extra safe
                # pylint: disable-next=protected-access,no-member
                threading._register_atexit(self.close)  # type: ignore
                logger.debug("Registered threading close")
            else:
                # In python < 3.9, this should work
                atexit.register(self.close)
                logger.debug("Registered exit close")

        self.connected = True
        return self._client

    @property
    def client(self) -> Client:
        return self.create_websocket_connection()

    async def _create_gql_client(self) -> Client:
        ws_endpoint = self.endpoint.replace("http://", "ws://").replace("https://", "wss://")
        headers = self.request_header
        logger.debug(f"Connecting to websocket server at endpoint {ws_endpoint}")
        transport = WebsocketsTransport(url=ws_endpoint, init_payload=headers)
        return Client(transport=transport, fetch_schema_from_transport=False)

    def subscribe(
        self,
        query: DocumentNode,
        variables: Dict[str, Any],
        callback: Callable[[Dict[str, Any]], T],
        retry_callback: Callable[[Dict[str, Any]], Dict[str, Any]],
    ) -> Generator[Future[T], None, None]:
        """Subscribe to the given query and return a generator of futures

        Args:
            query (DocumentNode): The GraphQL query document
            variables (Dict[str, Any]): A dictionary of variables to supply with the query

        Yields:
            Generator[Future[Dict[str, Any]], None, None]: A generator of futures for subscription results
        """

        if not self.connected:
            self.create_websocket_connection()

        async_gen = self._async_subscribe(query, variables, retry_callback)

        # get past session connect - if necessary
        asyncio.run_coroutine_threadsafe(async_gen.__anext__(), self._loop).result()

        try:
            while True:
                yield asyncio.run_coroutine_threadsafe(
                    # Handle errors before they are wrapped in a future so they can be
                    # properly set for the user
                    self._transform_subscription_result(async_gen.__anext__(), callback),
                    self._loop,
                )

        finally:
            async_gen.aclose()

    async def init_session(self):
        check_python_certificates()
        session = await self.client.connect_async(
            reconnecting=True,
            retry_connect=backoff.on_exception(
                backoff.expo,
                # This needs to be Exception - do not change to more specific subclass
                # https://github.com/graphql-python/gql/blob/master/gql/client.py#L1304
                Exception,
                max_value=300,  # default is 60 seconds
            ))
        return cast(ReconnectingAsyncClientSession, session)

    async def _async_subscribe(
        self,
        query: DocumentNode,
        variables: Dict[str, Any],
        retry_callback: Callable[[Dict[str, str]], Dict[str, Any]],
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Async version of subscribe that actually does the calling

        If a session connecting to MAPI doesn't exist, one will be created
        """

        # Yield to let caller know session is connected.
        # Yielding an empty dict to preserve typing
        yield {}

        max_retries = 10
        delay_in_seconds = 1
        backoff_factor = 2

        while max_retries > 0:

            current_variables = retry_callback(variables)

            if not self._session:
                logger.debug("No websocket session found. Creating initial session")
                self._session = await self.init_session()

            async_generator = self._session.subscribe(query, variable_values=current_variables)
            try:
                async for result in async_generator:
                    yield result
                break

            except (ConnectionClosed, PayloadTooBig) as e:
                # This frees up resources from the old generator, otherwise we run into websocket exceptions
                # https://github.com/aaugustin/websockets/blame/8e1628a14e0dd2ca98871c7500484b5d42d16b67/src/websockets/legacy/protocol.py#L922
                async_generator.aclose()
                await self._session.stop_connecting_task()
                max_retries = max_retries - 1
                if max_retries == 0:
                    # Error can be transient and just requires running the command again.
                    raise MAPIException(
                        status=HTTPStatus.INTERNAL_SERVER_ERROR,
                        message="Connection error. This may be transient. Please try running your command again") from e
                else:
                    time.sleep(delay_in_seconds)
                    delay_in_seconds = delay_in_seconds * backoff_factor
                    self._session = await self.init_session()

            except WebSocketException as e:
                # We catch and retry some subset of websocket exceptions (ConnectionClosed, PayloadTooBig)
                # For remainder, we raise a generic MAPIException with specific message for debugging
                reason = getattr(e, 'reason', str(e))
                raise MAPIException(status=HTTPStatus.INTERNAL_SERVER_ERROR,
                                    message=f'Error connecting to MAPI service: {reason}') from e

            except TransportQueryError as e:
                message = e.errors[0].get('message', str(e)) if e.errors else str(e)
                raise MAPIException(status=HTTPStatus.BAD_REQUEST, message=message) from e

    async def _transform_subscription_result(
        self,
        aw: Awaitable[Dict[str, Any]],
        callback: Callable[[Dict[str, Any]], T],
    ) -> T:
        """Awaits the awaitable argument and catches query errors so they can be
        passed as MAPIExceptions

        Args:
            aw (Awaitable[T]): Any awaitable

        Raises:
            MAPIException: Raised when a TransportQueryError is hit

        Returns:
            The awaited result
        """

        output = await aw
        return callback(output)

    @staticmethod
    def get_current_connection() -> MAPIConnection:
        """Get the current connection instance
        """
        return _CONNECTION or _create_default_connection()

    @staticmethod
    def reset_connection() -> None:
        """Create a new connection instance
        """
        _create_default_connection()

    def close(self):
        """Close any existing connection to the MAPI service
        """
        if self._loop.is_running():
            if self._session:
                logger.debug("Disconnecting existing websocket session")
                asyncio.run_coroutine_threadsafe(self._session.stop_connecting_task(), self._loop).result()
                logger.debug("Websocket session disconnected")

            if self._client:
                logger.debug("Closing websocket transport")
                transport = cast(AsyncTransport, self._client.transport)
                asyncio.run_coroutine_threadsafe(transport.close(), self._loop).result()
                logger.debug("Websocket transport closed")

            logger.debug("Terminating event loop")
            self._terminate.set()

    def __enter__(self) -> MAPIConnection:
        self._prev = _CONNECTION
        self._set_connection(self)
        return self

    def __exit__(self, type_, value, traceback):
        self.close()
        self._set_connection(self._prev)

    def __del__(self):
        self.close()


_CONNECTION: Optional[MAPIConnection] = None


def _create_default_connection() -> MAPIConnection:
    """Creates the default MAPIConnection object
    """
    global _CONNECTION
    _CONNECTION = MAPIConnection()
    return _CONNECTION


ThreadedOutput = TypeVar('ThreadedOutput')


def run_in_threadpool(
    f: Callable[..., ThreadedOutput],
    *args: Any,
    connection: Optional[MAPIConnection] = None,
    **kwargs: Any,
) -> Future[ThreadedOutput]:
    """Run the provided function in the MAPI threadpool and return a Future

    Args:
        f: An arbitrary function
        *args, **kwargs: Arbitrary arguments with which to call ``f``
        connection: Optional :type MAPIConnection: whose threadpool will be used

    Returns:
        A Future for the return value of ``f``
    """
    if not connection:
        connection = MAPIConnection.get_current_connection()
    return connection.pool.submit(f, *args, **kwargs)


ModelT = TypeVar('ModelT', bound=DeserializableModel)


def run_plural_mapi_request(
    query: str,
    query_function: str,
    return_model_type: Type[ModelT],
    variables: Optional[Dict[str, Any]] = None,
    connection: Optional[MAPIConnection] = None,
    protect: bool = False,
) -> Future[ObjectList[ModelT]]:
    """Run a GraphQL query against MAPI and return a future for a list of items

    Args:
        query: Query to run
        query_function: GraphQL endpoint for the query (e.g. 'createRun')
        return_model_type: The data type into which the response should be deserialized.
        variables: Variables to be passed to the GraphQL endpoint. Defaults to None.
        connection: The MAPI connection that should be used. Defaults to the connection
            returned by `MAPIConnection.get_current_connection()`.
        protect: If True, the future will be protected from SIGTERM. Defaults to False.

    Returns:
        A `concurrent.futures.Future` for the request. You can retrieve the data using
        `future.result()` with an optional `timeout` argument.

    Raises:
        MAPIException: Raised if the request fails. See ``MAPIException`` for details on
        exception status codes
    """
    if not connection:
        connection = MAPIConnection.get_current_connection()

    future = connection.pool.submit(
        _threaded_plural_mapi_request,
        headers=connection.request_header,
        endpoint=connection.endpoint,
        query=query,
        variables=variables,
        query_function=query_function,
        model_type=return_model_type,
    )
    if protect:
        connection.protect_future_from_sigterm(future)
    future = cast('Future[ObjectList[ModelT]]', future)

    return future


# TODO: Refactor this when we have more paginated endpoints
def run_paginated_mapi_request(
    query: str,
    query_function: str,
    return_model_type: Type[ModelT],
    variables: Optional[Dict[str, Any]] = None,
    connection: Optional[MAPIConnection] = None,
    protect: bool = False,
) -> Future[ObjectList[ModelT]]:
    """Run a GraphQL query against a paginated MAPI endpoint and return a future for a list of items

    Args:
        query: Query to run
        query_function: GraphQL endpoint for the query (e.g. 'createRun')
        return_model_type: The data type into which the response should be deserialized.
        variables: Variables to be passed to the GraphQL endpoint. Defaults to None.
        connection: The MAPI connection that should be used. Defaults to the connection
            returned by `MAPIConnection.get_current_connection()`.
        protect: If True, the future will be protected from SIGTERM. Defaults to False.

    Returns:
        A `concurrent.futures.Future` for the request. You can retrieve the data using
        `future.result()` with an optional `timeout` argument.

    Raises:
        MAPIException: Raised if the request fails. See ``MAPIException`` for details on
        exception status codes
    """
    if not connection:
        connection = MAPIConnection.get_current_connection()

    future = connection.pool.submit(
        _threaded_paginated_mapi_request,
        headers=connection.request_header,
        endpoint=connection.endpoint,
        query=query,
        variables=variables,
        query_function=query_function,
        model_type=return_model_type,
        paginated=True,
    )
    if protect:
        connection.protect_future_from_sigterm(future)
    future = cast('Future[ObjectList[ModelT]]', future)

    return future


class PaginatedObjectList(ObjectList):
    """
    A list of objects that is paginated
    """

    has_next_page: bool = False

    def __init__(
        self,
        data: Dict[str, Any],
        obj: Type[ModelT],
        query_function: str,
        pagination_function: Any,
    ):

        self.type = ObjectType.from_model_type(obj)
        self.obj = obj
        self.query_function = query_function
        self.pagination_function = pagination_function

        # Paginated results should have the following return type:
        #   type <Model>Page {
        #       <Model>s: [<Model>!]
        #       cursor: String
        #       hasNextPage: Boolean
        #    }

        self.cursor = data['cursor']
        self.has_next_page = data['hasNextPage']

        # This is flexible to support not having to provide a name of the
        # model, or explicitly needing to select the pagination fields
        keys = set(data.keys()) - {'cursor', 'hasNextPage'}
        # However, if there's more than one key, we don't know which one
        # to use, so we raise an error
        if len(keys) > 1:
            raise ValueError('Expected only one key in paginated response')
        resp_objects = data[list(keys)[0]]

        list_of_objects = [obj.from_mapi_response(i) for i in resp_objects]
        super().__init__(list_of_objects, self.type)

    def next_page(self, limit: Optional[int] = None) -> "PaginatedObjectList":
        """ Returns the next page of results
        """
        if not self.has_next_page:
            raise StopIteration('No next page')

        try:
            response = self.pagination_function(self.cursor, limit=limit)
        except requests.exceptions.ConnectionError as e:
            mapi_error = MAPIException.from_requests_error(e)
            raise mapi_error from e

        # Expression of type "ObjectList[ModelT@__init__]" cannot be assigned to return type "PaginatedObjectList"
        return _deserialize_response(response, self.query_function, self.obj, self.pagination_function)  # type: ignore


@retry_with_backoff
def _threaded_paginated_mapi_request(
    headers: Dict[str, str],
    endpoint: str,
    query: str,
    variables: Optional[Dict[str, Any]],
    query_function: str,
    model_type: Type[ModelT],
    paginated: bool = False,
) -> ObjectList[ModelT]:
    """Run a graphql request in a thread and return a list of items
    """

    def run_request_and_maybe_paginate(cursor: str = '', limit: Optional[int] = None):
        if variables is not None and paginated:
            # Pagination would never be supported for a query with no variables
            primary_key = list(variables.keys())[0]

            if cursor:
                variables[primary_key]['cursor'] = cursor
            if limit is not None:
                variables[primary_key]['limit'] = limit

        return _run_graphql_request(headers, endpoint, query, variables)

    try:
        response = run_request_and_maybe_paginate()
    except requests.exceptions.ConnectionError as e:
        mapi_error = MAPIException.from_requests_error(e)
        raise mapi_error from e

    return _deserialize_response(
        response,
        query_function,
        model_type,
        run_request_and_maybe_paginate if paginated else None,
    )


@retry_with_backoff
def _threaded_plural_mapi_request(
    headers: Dict[str, str],
    endpoint: str,
    query: str,
    variables: Optional[Dict[str, Any]],
    query_function: str,
    model_type: Type[ModelT],
) -> ObjectList[ModelT]:
    """Run a graphql request in a thread and return a list of items
    """
    try:
        response = _run_graphql_request(headers, endpoint, query, variables)
    except requests.exceptions.ConnectionError as e:
        mapi_error = MAPIException.from_requests_error(e)
        raise mapi_error from e

    return _deserialize_response(response, query_function, model_type)


def run_singular_mapi_request(
    query: str,
    query_function: str,
    return_model_type: Type[ModelT],
    variables: Optional[Dict[str, Any]] = None,
    connection: Optional[MAPIConnection] = None,
    protect: bool = False,
) -> Future[ModelT]:
    """Run a GraphQL query against MAPI and return a future for a singular item

    Args:
        query: Query to run
        query_function: GraphQL endpoint for the query (e.g. 'createRun')
        return_model_type: The data type into which the response should be deserialized.
            Required if data is expected to be returned.
        variables: Variables to be passed to the GraphQL endpoint. Defaults to None.
        connection: The MAPI connection that should be used. Defaults to the connection
            returned by `MAPIConnection.get_current_connection()`.
        protect: If True, the future will be protected from SIGTERM. Defaults to False.

    Returns:
        A `concurrent.futures.Future` for the request. You can retrieve the data using
        `future.result()` with an optional `timeout` argument.

    Raises:
        MAPIException: Raised if the request fails. See ``MAPIException`` for details on
        exception status codes
    """
    if not connection:
        connection = MAPIConnection.get_current_connection()
    future = connection.pool.submit(
        _threaded_singular_mapi_request,
        headers=connection.request_header,
        endpoint=connection.endpoint,
        query=query,
        variables=variables,
        query_function=query_function,
        model_type=return_model_type,
    )
    if protect:
        connection.protect_future_from_sigterm(future)
    future = cast('Future[ModelT]', future)

    return future


def _threaded_singular_mapi_request(
    headers: Dict[str, str],
    endpoint: str,
    query: str,
    variables: Optional[Dict[str, Any]],
    query_function: str,
    model_type: Type[ModelT],
) -> ModelT:
    """Run a graphql request in a thread and return a single item

    Raises:
        MAPIException: Raised if no items were found
    """

    items = _threaded_plural_mapi_request(
        headers=headers,
        endpoint=endpoint,
        query=query,
        variables=variables,
        query_function=query_function,
        model_type=model_type,
    )
    if len(items) == 1:
        return items[0]
    else:
        raise MAPIException(status=HTTPStatus.INTERNAL_SERVER_ERROR,
                            message='Request returned no items, but expected 1')


def _run_graphql_request(
    headers: Dict[str, str],
    endpoint: str,
    query: str,
    variables: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:

    if variables is None:
        variables = {}
    variables = {key.replace('$', ''): value for key, value in variables.items()}

    payload = json.dumps({'query': query, 'variables': variables})
    logger.debug(f'Running graphql request {endpoint} {payload}')

    # Don't want timeout since this will be run in a background thread
    # pylint: disable-next=missing-timeout
    response = requests.request(
        'POST',
        endpoint,
        headers=headers,
        data=payload,
    )

    try:
        return response.json()
    except requests.JSONDecodeError as e:
        mapi_error = MAPIException.from_bad_response(response)
        raise mapi_error from e


def _deserialize_response(
    response: Dict[str, Any],
    query_function: str,
    model_type: Optional[Type[ModelT]],
    pagination_function: Optional[Any] = None,
) -> ObjectList[ModelT]:
    """Given response, function, and model object, deserializes data

    raises
        MAPIException: Something on the MAPI side went wrong (400s) or the
            response didn't match the expected format (500)
        MultiMAPIException: Multiple errors encountered in graphql
    """

    # Check response for errors in the header (typically 401/403)
    error_to_raise = [MAPIException.from_mapi_error_response(e) for e in response.get('errors', [])]
    if error_to_raise:
        raise MultiMAPIException(error_to_raise)

    if model_type is None:
        return ObjectList([], ObjectType.UNKNOWN)

    try:
        data = response['data']
        query_response: List[Any] = data[query_function]

        if pagination_function:
            if not isinstance(query_response, dict):
                raise ValueError('Expected paginated response to be a dict')

            return PaginatedObjectList(query_response, model_type, query_function, pagination_function)

        return ObjectList([model_type.from_mapi_response(i) for i in query_response],
                          ObjectType.from_model_type(model_type))
    except (KeyError, TypeError, AttributeError) as e:
        raise MAPIException(status=HTTPStatus.INTERNAL_SERVER_ERROR,
                            message=('Internal Server Error: Malformed response data '
                                     f'raised {e.__class__.__name__}. '
                                     f'Response received: {response}')) from e


def get_return_response(response, future: bool = False, timeout: Optional[float] = 10.0):
    if future:
        return response
    timeout = get_timeout(default_timeout=timeout)
    return response.result(timeout=timeout)


def convert_plural_future_to_singleton(
    future: Future[ObjectList[ModelT]],
    error_message: Optional[str] = None,
) -> Future[ModelT]:
    """Convert a future for a list of models to a future for a single model

    This is useful if you know that the query will only return one result, but
    you want to use the same code to handle both cases.

    Args:
        future: A future that will resolve to a list of models
        error_message: The error message to use if the plural future resolves to
            an empty list. If None, no error will be raised. This is used can be used
            resolvers that do not raise an error if nothing is found (eg getRuns)

    Returns:
        A future that will resolve to a single model

    Raises:
        MAPIException: If the plural future resolves to an empty list
    """
    future_obj: Future[ModelT] = Future()

    def callback(f: Future[ObjectList[ModelT]]) -> None:
        try:
            res = f.result()
        except Exception as e:  # pylint: disable=broad-except
            # Propagate any exception to the new future
            future_obj.set_exception(e)
        else:
            if res:
                future_obj.set_result(res[0])

            else:
                # Most mapi mutation resolvers will raise their own error, this is for
                # resolvers that do not raise an error if nothing is found (eg getRuns)
                msg = error_message or 'No results found'
                future_obj.set_exception(MAPIException(status=HTTPStatus.NOT_FOUND, message=msg))

    future.add_done_callback(callback)
    return future_obj
