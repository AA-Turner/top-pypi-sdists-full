"""Get a run's logs from the MosaicML platform"""
from __future__ import annotations

import base64
import logging
from concurrent.futures import Future
from typing import Any, Dict, Generator, Optional, Union, overload

import gql
from typing_extensions import Literal

from mcli.api.engine.engine import MAPIConnection
from mcli.api.model.run import Run
from mcli.config import MCLIConfig
from mcli.utils.utils_message_decoding import MessageDecoder

logger = logging.getLogger(__name__)

QUERY_FUNCTION = 'getRunLogsV2'
VARIABLE_DATA_NAME = 'getRunLogsInput'
QUERY = f"""
subscription Subscription(${VARIABLE_DATA_NAME}: GetRunLogsInput!) {{
    {QUERY_FUNCTION}({VARIABLE_DATA_NAME}: ${VARIABLE_DATA_NAME}) {{
        chunk
        endOffset
    }}
}}"""


@overload
def get_run_logs(
    run: Union[str, Run],
    rank: Optional[int] = None,
    *,
    node_rank: Optional[int] = None,
    local_gpu_rank: Optional[int] = None,
    global_gpu_rank: Optional[int] = None,
    first_exception: Optional[bool] = False,
    timeout: Optional[float] = None,
    future: Literal[False] = False,
    failed: Optional[bool] = False,
    resumption: Optional[int] = None,
    tail: Optional[int] = None,
    container: Optional[str] = None,
) -> Generator[str, None, None]:
    ...


@overload
def get_run_logs(
    run: Union[str, Run],
    rank: Optional[int] = None,
    *,
    node_rank: Optional[int] = None,
    local_gpu_rank: Optional[int] = None,
    global_gpu_rank: Optional[int] = None,
    first_exception: Optional[bool] = False,
    timeout: Optional[float] = None,
    future: Literal[True] = True,
    failed: Optional[bool] = False,
    resumption: Optional[int] = None,
    tail: Optional[int] = None,
    container: Optional[str] = None,
) -> Generator[Future[str], None, None]:
    ...


def get_run_logs(
    run: Union[str, Run],
    rank: Optional[int] = None,
    *,
    node_rank: Optional[int] = None,
    local_gpu_rank: Optional[int] = None,
    global_gpu_rank: Optional[int] = None,
    first_exception: Optional[bool] = False,
    timeout: Optional[float] = None,
    future: bool = False,
    failed: Optional[bool] = False,
    resumption: Optional[int] = None,
    tail: Optional[int] = None,
    container: Optional[str] = None,
) -> Union[Generator[str, None, None], Generator[Future[str], None, None]]:
    """Get the current logs for an active or completed run

    Get the current logs for an active or completed run in the MosaicML platform.
    This returns the full logs as a ``str``, as they exist at the time the request is
    made. If you want to follow the logs for an active run line-by-line, use
    :func:`follow_run_logs`.

    Args:
        run (:obj:`str` | :class:`~mcli.api.model.run.Run`): The run to get logs for. If a
            name is provided, the remaining required run details will be queried with :func:`~mcli.get_runs`.
        rank (``Optional[int]``): [DEPRECATED, Use node_rank instead] Node rank of a run to get logs for.
            Defaults to the lowest available rank. This will usually be rank 0 unless something has gone wrong.
        node_rank (``Optional[int]``): Specifies the node rank within a multi-node run to
            fetch logs for. Defaults to lowest available rank. Indexing starts from 0.
        local_gpu_rank (``Optional[int]``): Specifies the GPU rank on the specified node to
            fetch logs for. Cannot be used with global_gpu_rank. Indexing starts from 0.
            Note: GPU rank logs are only available for runs using `Composer <https://github.com/mosaicml/composer>`_
            and/or `LLM Foundry <https://github.com/mosaicml/llm-foundry>`_ and MAIN container logs.
        global_gpu_rank (``Optional[int]``): Specifies the global GPU rank to fetch logs for.
            Cannot be used with node_rank and local_gpu_rank. Indexing starts from 0.
            Note: GPU rank logs are only available for runs using `Composer <https://github.com/mosaicml/composer>`_
            and/or `LLM Foundry <https://github.com/mosaicml/llm-foundry>`_ and MAIN container logs.
        timeout (``Optional[float]``): Time, in seconds, in which the call should complete.
            If the the call takes too long, a :exc:`~concurrent.futures.TimeoutError`
            will be raised. If ``future`` is ``True``, this value will be ignored.
        future (``bool``): Return the output as a :class:`~concurrent.futures.Future` . If True, the
            call to :func:`get_run_logs` will return immediately and the request will be
            processed in the background. This takes precedence over the ``timeout``
            argument. To get the log text, use ``return_value.result()`` with an optional
            ``timeout`` argument.
        failed (``bool``): Return the logs of the first failed rank for the provided resumption if ``True``.
            ``False`` by default.
        resumption (``Optional[int]``): Resumption (0-indexed) of a run to get logs for. Defaults to the last resumption
        tail (``Optional[int]``): Number of chars to read from the end of the log. Defaults to reading the entire log.
        container (``Optional[str]``): Container name of a run to get logs for. Defaults to the MAIN container.

    Returns:
        If future is False:
            The full log text for a run at the time of the request as a :obj:`str`
        Otherwise:
            A :class:`~concurrent.futures.Future` for the log text
    """
    # Convert to strings
    run_name = run.name if isinstance(run, Run) else run

    # set failed to true with --first-exception to differentiate between future features
    # that can specify the node and GPU rank for the first exception
    filters: Dict[str, Any] = {
        'name': run_name,
        'follow': False,
        'failed': True if first_exception else failed,
        'exceptionOnly': first_exception
    }
    if node_rank is not None and rank is not None:
        raise ValueError("""Node rank and rank are both provided and are aliases of each other.
            Please use node rank to specify node rank logs. The rank parameter will
            be deprecated in a future release.""")  # TODO: update after deprecating rank

    if rank is not None:
        filters['nodeRank'] = rank

    if node_rank is not None:
        filters['nodeRank'] = node_rank

    if failed and filters.get('nodeRank') is not None:
        raise ValueError('Node rank and failed cannot be provided together. Please specify one or the other.')

    if local_gpu_rank is not None:
        if container is not None and container != 'MAIN':
            raise ValueError(f'GPU rank logs are not available for {container} container.')

        if global_gpu_rank is not None:
            raise ValueError(
                'Global GPU rank and local GPU rank cannot be provided together. Please specify one or the other.')
        filters['localGpuRank'] = local_gpu_rank

    if global_gpu_rank is not None:
        if container is not None and container != 'MAIN':
            raise ValueError(f'GPU rank logs are not available for {container} container.')
        if failed:
            raise ValueError('Global GPU rank and failed cannot be provided together. Please specify one or the other.')
        if filters.get('nodeRank') is not None:
            raise ValueError(
                'Global GPU rank and node rank cannot be provided together. Please specify one or the other.')
        filters['globalGpuRank'] = global_gpu_rank

    # first-exception and only localGpuRank input are mutually exclusive
    if first_exception:
        if (filters.get('localGpuRank') is not None and filters.get('nodeRank') is None and
                filters.get('globalGpuRank') is None):
            raise ValueError(
                'Cannot use --first-exception with only local GPU rank specified. ' \
                'Please specify the node rank or provide the global GPU rank.'
                )

    if resumption is not None:
        filters['attemptIndex'] = resumption

    if tail is not None:
        filters['tail'] = tail

    if container is not None:
        filters['containerName'] = container

    cfg = MCLIConfig.load_config()
    cfg.update_entity(filters)

    variables = {VARIABLE_DATA_NAME: filters}
    for message in _get_logs(QUERY, variables, QUERY_FUNCTION):
        if not future:
            try:
                yield message.result(timeout)
            except StopAsyncIteration:
                break
        else:
            yield message


@overload
def follow_run_logs(
    run: Union[str, Run],
    rank: Optional[int] = None,
    *,
    node_rank: Optional[int] = None,
    local_gpu_rank: Optional[int] = None,
    global_gpu_rank: Optional[int] = None,
    timeout: Optional[float] = None,
    future: Literal[False] = False,
    resumption: Optional[int] = None,
    tail: Optional[int] = None,
    container: Optional[str] = None,
) -> Generator[str, None, None]:
    ...


@overload
def follow_run_logs(
    run: Union[str, Run],
    rank: Optional[int] = None,
    *,
    node_rank: Optional[int] = None,
    local_gpu_rank: Optional[int] = None,
    global_gpu_rank: Optional[int] = None,
    timeout: Optional[float] = None,
    future: Literal[True] = True,
    resumption: Optional[int] = None,
    tail: Optional[int] = None,
    container: Optional[str] = None,
) -> Generator[Future[str], None, None]:
    ...


def follow_run_logs(
    run: Union[str, Run],
    rank: Optional[int] = None,
    *,
    node_rank: Optional[int] = None,
    local_gpu_rank: Optional[int] = None,
    global_gpu_rank: Optional[int] = None,
    timeout: Optional[float] = None,
    future: bool = False,
    resumption: Optional[int] = None,
    tail: Optional[int] = None,
    container: Optional[str] = None,
) -> Union[Generator[str, None, None], Generator[Future[str], None, None]]:
    """Follow the logs for an active or completed run in the MosaicML platform

    This returns a :obj:`generator` of individual log lines, line-by-line, and will wait until
    new lines are produced if the run is still active.

    Args:
        run (:obj:`str` | :class:`~mcli.api.model.run.Run`): The run to get logs for. If a
            name is provided, the remaining required run details will be queried with
            :func:`~mcli.get_runs`.
        rank (``Optional[int]``): Node rank of a run to get logs for. Defaults to the lowest
            available rank. This will usually be rank 0 unless something has gone wrong.
        timeout (``Optional[float]``): Time, in seconds, in which the call should complete.
            If the call takes too long, a :exc:`~concurrent.futures.TimeoutError`
            will be raised. If ``future`` is ``True``, this value will be ignored. A run may
            take some time to generate logs, so you likely do not want to set a timeout.
        future (``bool``): Return the output as a :class:`~concurrent.futures.Future` . If True, the
            call to :func:`follow_run_logs` will return immediately and the request will be
            processed in the background. The generator returned by the `~concurrent.futures.Future`
            will yield a `~concurrent.futures.Future` for each new log string returned from the cloud.
            This takes precedence over the ``timeout`` argument. To get the generator,
            use ``return_value.result()`` with an optional ``timeout`` argument and
            ``log_future.result()`` for each new log string.
        resumption (``Optional[int]``): Resumption (0-indexed) of a run to get logs for. Defaults to the last resumption
        tail (``Optional[int]``): Number of chars to read from the end of the log. Defaults to reading the entire log.
        container (``Optional[str]``): Container name of a run to get logs for. Defaults to the MAIN container.

    Returns:
        If future is False:
            A line-by-line :obj:`Generator` of the logs for a run
        Otherwise:
            A :class:`~concurrent.futures.Future` of a line-by-line generator of the logs for a run
    """
    # Convert to strings
    run_name = run.name if isinstance(run, Run) else run

    filters: Dict[str, Any] = {'name': run_name, 'follow': True}
    if node_rank is not None and rank is not None:
        raise ValueError("""Node rank and rank are both provided and are aliases of each other.
            Please use node rank to specify node rank logs. The rank parameter will
            be deprecated in a future release.""")  # TODO: update after deprecating rank

    if rank is not None:
        filters['nodeRank'] = rank

    if node_rank is not None:
        filters['nodeRank'] = node_rank

    if local_gpu_rank is not None:
        if container is not None and container != 'MAIN':
            raise ValueError(f'GPU rank logs are not available for {container} container.')

        if global_gpu_rank is not None:
            raise ValueError(
                'Global GPU rank and local GPU rank cannot be provided together. Please specify one or the other.')
        filters['localGpuRank'] = local_gpu_rank

    if global_gpu_rank is not None:
        if container is not None and container != 'MAIN':
            raise ValueError(f'GPU rank logs are not available for {container} container.')
        if filters.get('nodeRank') is not None:
            raise ValueError(
                'Global GPU rank and node rank cannot be provided together. Please specify one or the other.')
        filters['globalGpuRank'] = global_gpu_rank

    if resumption is not None:
        filters['attemptIndex'] = resumption

    if tail is not None:
        filters['tail'] = tail

    if container is not None:
        filters['containerName'] = container

    cfg = MCLIConfig.load_config()
    cfg.update_entity(filters)

    variables = {VARIABLE_DATA_NAME: filters}
    for message in _get_logs(QUERY, variables, QUERY_FUNCTION):
        if not future:
            try:
                yield message.result(timeout)
            except StopAsyncIteration:
                break
        else:
            yield message


def _get_logs(query: str, variables: Dict[str, Any], return_key: str) -> Generator[Future[str], None, None]:

    gql_query = gql.gql(query)
    connection = MAPIConnection.get_current_connection()
    decoder = LogsDecoder(return_key=return_key)
    yield from connection.subscribe(
        query=gql_query,
        variables=variables,
        callback=decoder.parse_message,
        retry_callback=decoder.update_offset,
    )


class LogsDecoder(MessageDecoder):
    """Decode log messages and update read offset
    """
    end_offset: int = 0

    def __init__(self, return_key: str):
        self.return_key = return_key
        super().__init__()

    def update_offset(self, variables: Dict[str, Any]) -> Dict[str, Any]:
        resolver_input = variables['getRunLogsInput'] if self.return_key == 'getRunLogsV2' else variables[
            'getInferenceDeploymentLogsInput']
        # We set the offset to read from the end of the last message, or zero if this is the first message
        resolver_input['offset'] = self.end_offset
        # If we have already read some bytes with the tail parameter set, we must have already calculated
        # the tail offset. Thus, we can simply continue reading normally, without the tail parameter.
        if self.end_offset != 0 and 'tail' in resolver_input:
            del resolver_input['tail']
        return variables

    def parse_message(self, data: Dict[str, Any]) -> str:
        """Get the next message from the GraphQL logging subscription
        """
        # Convert from base64 string to a bytestring
        message_data = data['getRunLogsV2'] if self.return_key == 'getRunLogsV2' else data[
            'getInferenceDeploymentLogsV2']
        b64_message = message_data['chunk']
        b64_bytes = b64_message.encode('utf8')
        message_bytes = base64.b64decode(b64_bytes)
        self.end_offset = message_data['endOffset']

        return self.decode(message_bytes)
