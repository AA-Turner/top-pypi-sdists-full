"""MCLI abstractions for run debug information."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from http import HTTPStatus
from typing import Any, Dict, List, Optional, Tuple

from rich.table import Table

from mcli.api.exceptions import MAPIException
from mcli.api.schema.generic_model import DeserializableModel, convert_datetime
from mcli.utils.utils_date import TimestampPrecision, format_timestamp
from mcli.utils.utils_logging import console


@dataclass
class ContainerStatusUpdate:
    """Status update for a container in a run.
    """
    node_rank: int
    container_name: str
    status: str
    reached_at: datetime
    reason: Optional[str] = None

    _required_properties: Tuple[str] = tuple([
        'nodeRank',
        'containerName',
        'status',
        'reachedAt',
    ])

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]) -> ContainerStatusUpdate:
        missing = set(cls._required_properties) - set(response)
        if missing:
            raise MAPIException(
                status=HTTPStatus.BAD_REQUEST,
                message='Missing required key(s) in response to deserialize ContainerStatusUpdate object: '
                f'{", ".join(missing)}',
            )

        return ContainerStatusUpdate(
            node_rank=response['nodeRank'],
            container_name=response['containerName'],
            status=response['status'],
            reached_at=convert_datetime(response['reachedAt']),
            reason=response.get('reason'),
        )


@dataclass
class PodStatusUpdate:
    """Status update for a pod in a run.
    """
    node_rank: int
    status: str
    reached_at: datetime
    node_name: Optional[str] = None
    reason: Optional[str] = None

    _required_properties: Tuple[str] = tuple([
        'nodeRank',
        'status',
        'reachedAt',
    ])

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]) -> PodStatusUpdate:
        missing = set(cls._required_properties) - set(response)
        if missing:
            raise MAPIException(
                status=HTTPStatus.BAD_REQUEST,
                message=
                f'Missing required key(s) in response to deserialize PodStatusUpdate object: {", ".join(missing)}',
            )

        return PodStatusUpdate(
            node_rank=response['nodeRank'],
            node_name=response['nodeName'],
            status=response['status'],
            reached_at=convert_datetime(response['reachedAt']),
            reason=response.get('reason'),
        )


@dataclass
class ExecutionStatusUpdates:
    """Container and pod status updates for a single execution of a run."""
    id: str
    execution_index: int
    container_status_updates: List[ContainerStatusUpdate]
    pod_status_updates: List[PodStatusUpdate]

    _required_properties: Tuple[str] = tuple([
        'id',
        'executionIndex',
        'containerStatusUpdates',
        'podStatusUpdates',
    ])

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]) -> ExecutionStatusUpdates:
        missing = set(cls._required_properties) - set(response)
        if missing:
            raise MAPIException(
                status=HTTPStatus.BAD_REQUEST,
                message=f'Missing required key(s) in response to deserialize ExecutionStatusUpdates object: '
                f'{", ".join(missing)}',
            )
        return ExecutionStatusUpdates(
            id=response['id'],
            execution_index=response['executionIndex'],
            container_status_updates=[
                ContainerStatusUpdate.from_mapi_response(csu) for csu in response['containerStatusUpdates']
            ],
            pod_status_updates=[PodStatusUpdate.from_mapi_response(psu) for psu in response['podStatusUpdates']])


@dataclass
class RunDebugInfo(DeserializableModel):
    """Debug information for a run."""
    id: str
    executions_status_updates: List[ExecutionStatusUpdates]

    _required_properties: Tuple[str] = tuple([
        'id',
        'executionsStatusUpdates',
    ])

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]) -> RunDebugInfo:
        missing = set(cls._required_properties) - set(response)
        if missing:
            raise MAPIException(
                status=HTTPStatus.BAD_REQUEST,
                message=f'Missing required key(s) in response to deserialize RunDebugInfo object: {", ".join(missing)}',
            )
        return RunDebugInfo(
            id=response['id'],
            executions_status_updates=[
                ExecutionStatusUpdates.from_mapi_response(esu) for esu in response['executionsStatusUpdates']
            ])

    def print(self, resumption: int):
        """Formats and displays the run debug info for the given resumption index."""
        print(f'Run ID: {self.id}')
        out_of = f'{resumption + 1}/{len(self.executions_status_updates)}'
        print(f'Execution ID: {self.executions_status_updates[resumption].id} ({out_of})\n')

        console.print('[bold italic]Pod Status Updates[/]')
        console.print(self._format_pod_status_updates(resumption))
        console.print()
        console.print('[bold italic]Container Status Updates[/]')
        console.print(self._format_container_status_updates(resumption))

    def _get_node_names(self, resumption: int) -> Dict[int, str]:
        """Returns a mapping from node rank to node names by rank for the given resumption."""
        rank_to_node_name = {}

        for pod_status_update in self.executions_status_updates[resumption].pod_status_updates:
            if pod_status_update.node_name:
                rank_to_node_name[pod_status_update.node_rank] = pod_status_update.node_name

        return rank_to_node_name

    def _format_pod_status_updates(self, resumption: int):
        """Formats pod status updates for the given resumption into a table."""
        grid = Table(expand=False, padding=(0, 2, 0, 2))
        grid.add_column(header='Node Rank', justify='center')
        grid.add_column(header='Node Name', justify='center')
        grid.add_column(header='Status', justify='left')
        grid.add_column(header='Reason', justify='left')
        grid.add_column(header='Time', justify='left')

        # Track previous node rank to add a new section when node rank changes.
        prev_node_rank = None
        rank_to_node_name = self._get_node_names(resumption)
        for pod_status_update in self.executions_status_updates[resumption].pod_status_updates:
            formatted_node_rank = ''
            formatted_node_name = ''

            # Only display the node rank and name if it's the first pod status update for that node.
            if prev_node_rank is None or pod_status_update.node_rank != prev_node_rank:
                formatted_node_rank = str(pod_status_update.node_rank)
                formatted_node_name = rank_to_node_name.get(pod_status_update.node_rank, '')
                prev_node_rank = pod_status_update.node_rank
                grid.add_section()

            grid.add_row(
                formatted_node_rank,
                formatted_node_name,
                pod_status_update.status,
                pod_status_update.reason or '-',
                format_timestamp(pod_status_update.reached_at, precision=TimestampPrecision.SECOND),
            )

        return grid

    def _format_container_status_updates(self, resumption: int):
        """Formats container status updates for the given resumption into a table."""
        grid = Table(expand=False, padding=(0, 2, 0, 2))
        grid.add_column(header='Node Rank', justify='center')
        grid.add_column(header='Container Name', justify='left')
        grid.add_column(header='Status', justify='left')
        grid.add_column(header='Reason', justify='left')
        grid.add_column(header='Time', justify='left')

        # Track previous node rank to add a new section when node rank changes.
        prev_node_rank = None
        for container_status_update in self.executions_status_updates[resumption].container_status_updates:
            formatted_node_rank = ''
            if prev_node_rank is None or container_status_update.node_rank != prev_node_rank:
                formatted_node_rank = str(container_status_update.node_rank)
                prev_node_rank = container_status_update.node_rank
                grid.add_section()

            grid.add_row(
                formatted_node_rank,
                container_status_update.container_name,
                container_status_update.status,
                container_status_update.reason or '-',
                format_timestamp(container_status_update.reached_at, precision=TimestampPrecision.SECOND),
            )

        return grid
