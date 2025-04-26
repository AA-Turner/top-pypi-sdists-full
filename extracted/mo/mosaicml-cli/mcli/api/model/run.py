""" GraphQL representation of MCLIJob"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from http import HTTPStatus
from typing import Any, Dict, List, Optional, Tuple

from mcli.api.exceptions import MAPIException
from mcli.api.model.run_event import FormattedRunEvent
from mcli.api.schema.generic_model import DeserializableModel, convert_datetime
from mcli.models.run_config import RunConfig
from mcli.utils.utils_run_status import RunStatus


@dataclass
class Node(DeserializableModel):
    """Node linked to a run
    """

    rank: int
    name: str
    status: str
    reason: str = ''

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]) -> Node:
        return Node(rank=response.get('rank', 0),
                    name=response.get('name', 'Unknown'),
                    status=response.get('status', ''),
                    reason=response.get('reason', ''))

    def to_dict(self):
        return {'rank': str(self.rank), 'name': self.name, 'status': self.status, 'reason': self.reason}


@dataclass
class Resumption:
    """Data from a run resumption. The first instantiation of a Run will
         have a Resumption with index `0`
    """

    index: int
    cluster: str
    gpus: int
    cpus: int
    gpu_type: str
    node_count: int
    status: RunStatus
    estimated_end_time: Optional[datetime] = None
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    reason: Optional[str] = None

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]) -> Resumption:
        estimated_end_time = response.get('estimatedEndTime', None)
        if estimated_end_time:
            estimated_end_time = convert_datetime(estimated_end_time)

        return Resumption(index=response['executionIndex'],
                          cluster=response['clusterName'],
                          gpus=response['gpus'],
                          cpus=response['cpus'],
                          gpu_type=response['gpuType'],
                          node_count=response['nodes'],
                          status=RunStatus.from_string(response['status']),
                          started_at=convert_datetime(response['startTime']) if response['startTime'] else None,
                          ended_at=convert_datetime(response['endTime']) if response['endTime'] else None,
                          estimated_end_time=estimated_end_time,
                          reason=response.get('reason', ''))

    def to_dict(self):
        return {
            'index': self.index,
            'cluster': self.cluster,
            'gpus': str(self.gpus),
            'cpus': str(self.cpus),
            'gpu_type': self.gpu_type,
            'node_count': str(self.node_count),
            'status': str(self.status),
            'started_at': str(self.started_at),
            'ended_at': str(self.ended_at),
            'estimated_end_time': str(self.estimated_end_time)
        }


@dataclass
class RunLifecycle:
    """Status of a run at a moment in time
    """

    resumption_index: int
    status: RunStatus
    started_at: datetime
    ended_at: Optional[datetime] = None
    reason: Optional[str] = None
    estimated_end_time: Optional[str] = None

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]) -> RunLifecycle:
        return RunLifecycle(
            resumption_index=response['executionIndex'],
            status=RunStatus.from_string(response['status']),
            started_at=convert_datetime(response['startTime']),
            ended_at=convert_datetime(response['endTime']) if response['endTime'] else None,
            reason=response.get('reason'),
        )

    def to_dict(self):
        return {
            'resumption_id': str(self.resumption_index),
            'status': self.status,
            'started_at': str(self.started_at),
            'ended_at': str(self.ended_at),
            'reason': self.reason
        }


class RunType(Enum):
    """Possible run types
    """
    # Anything created with createRun directly
    TRAINING = 'TRAINING'
    # A run created with createSecretTest
    SECRET_TEST = 'SECRET_TEST'
    # A run created with createInteractiveRun
    INTERACTIVE = 'INTERACTIVE'
    # A long running training run, run on reserved compute.
    # Currently created via createRun with isHeroRun=true inside the metadata
    HERO_RUN = 'HERO_RUN'
    # A run created with createFinetune (see finetuneTypeDefs.ts)
    FINETUNING = 'FINETUNING'
    # A run created with createPretrain (see pretrainTypeDefs.ts)
    PRETRAINING = 'PRETRAINING'

    # Forwards compatibility
    UNKNOWN = 'UNKNOWN'

    @staticmethod
    def from_string(value: str) -> RunType:
        """Convert a string to a RunType

        Args:
            value (str): The string to convert

        Returns:
            The RunType corresponding to the string
        """

        try:
            return RunType(value)
        except ValueError:
            return RunType.UNKNOWN


@dataclass
class Run(DeserializableModel):
    """A run that has been launched on the MosaicML platform

    Args:
        run_uid (`str`): Unique identifier for the run
        name (`str`): User-defined name of the run
        status (:class:`~mcli.utils.utils_run_status.RunStatus`): Status of the run at a moment in time
        created_at (`datetime`): Date and time when the run was created
        updated_at (`datetime`): Date and time when the run was last updated
        created_by (`str`): Email of the user who created the run
        priority (`str`): Priority of the run; defaults to `auto` but can be updated to `low` or `lowest`
        preemptible (`bool`): Whether the run can be stopped and re-queued by higher priority jobs
        retry_on_system_failure (`bool`): Whether the run should be retried on system failure
        cluster (`str`): Cluster the run is running on
        gpus (`int`): Number of GPUs the run is using
        gpu_type (`str`): Type of GPU the run is using
        cpus (`int`): Number of CPUs the run is using
        node_count (`int`): Number of nodes the run is using
        latest_resumption (:class:`~mcli.api.model.run.Resumption`): Latest resumption of the run
        max_retries (`Optional[int]`): Maximum number of times the run can be retried
        reason (`Optional[str]`): Reason the run was stopped
        nodes (`List[:class:`~mcli.api.model.run.Node`]`): Nodes the run is using
        submitted_config (`Optional[:class:`~mcli.models.run_config.RunConfig`]`): Submitted run configuration
        metadata (`Optional[Dict[str, Any]]`): Metadata associated with the run
        last_resumption_id (`Optional[str]`): ID of the last resumption of the run
        resumptions (`List[:class:`~mcli.api.model.run.Resumption`]`): Resumptions of the run
        lifecycle (`List[:class:`~mcli.api.model.run.RunLifecycle`]`): Lifecycle of the run
        image (`Optional[str]`): Image the run is using
    """

    run_uid: str
    name: str
    status: RunStatus
    created_at: datetime
    updated_at: datetime
    created_by: str
    priority: str
    preemptible: bool
    retry_on_system_failure: bool
    cluster: str
    gpus: int
    gpu_type: str
    cpus: int
    node_count: int
    latest_resumption: Resumption
    is_deleted: bool
    run_type: RunType

    max_retries: Optional[int] = None
    reason: Optional[str] = None
    nodes: List[Node] = field(default_factory=list)
    submitted_config: Optional[RunConfig] = None
    metadata: Optional[Dict[str, Any]] = None
    last_resumption_id: Optional[str] = None
    resumptions: List[Resumption] = field(default_factory=list)
    events: List[FormattedRunEvent] = field(default_factory=list)
    lifecycle: List[RunLifecycle] = field(default_factory=list)
    image: Optional[str] = None

    max_duration: Optional[float] = None

    _required_properties: Tuple[str] = tuple([
        'id', 'name', 'status', 'createdAt', 'updatedAt', 'reason', 'createdByEmail', 'priority', 'preemptible',
        'retryOnSystemFailure', 'resumptions', 'isDeleted', 'runType'
    ])

    @property
    def started_at(self) -> Optional[datetime]:
        """The time the run was first started

        If there are multiple resumptions, this will be the earliest start time
        Started At will be None if the first resumption has not been started

        Returns:
            The time the run was first started
        """
        for resumption in self.resumptions:
            if resumption.started_at:
                return resumption.started_at

        return None

    @property
    def completed_at(self) -> Optional[datetime]:
        """The time the run was completed

        If there are multiple resumptions, this will be the last end time
        Completed At will be None if the last resumption has not been completed

        Returns:
            The time the run was last completed
        """

        for resumption in self.resumptions[::-1]:
            if resumption.ended_at:
                return resumption.ended_at

            # Stopped resumptions are special: you can technically stop a resumption
            # before it starts, resulting in a resumption with no start or end time.
            # For these cases, use the previous resumption's end time (if it exists)

            # Otherwise, if ended_at is None, the resumption is still running
            if resumption.status != RunStatus.STOPPED:
                return None

        return None

    def _get_time_in_status(self, status: RunStatus) -> float:
        """Returns the time spent in a given status

        Args:
            status (:class:`~mcli.utils.utils_run_status.RunStatus`): The status to get the time for

        Returns:
            The time (seconds) spent in the given status
        """
        res = 0
        if self.lifecycle:
            for status_update in self.lifecycle:
                if status_update.status == status:
                    ended = status_update.ended_at
                    if not ended:
                        ended = datetime.now(tz=status_update.started_at.tzinfo)
                    res += (ended - status_update.started_at).total_seconds()
        return res

    @property
    def display_name(self) -> str:
        """The name of the run to display in the CLI

        Returns:
            The name of the run
        """
        if self.retry_on_system_failure:
            return f'{self.name} 🐕'

        if self.is_deleted is True:
            return f'{self.name} (Deleted)'

        return self.name

    @property
    def cumulative_pending_time(self) -> float:
        """Cumulative time spent in the PENDING state

        Returns:
            The cumulative time (seconds) spent in the PENDING state
        """
        return self._get_time_in_status(RunStatus.PENDING)

    @property
    def cumulative_running_time(self) -> float:
        """Cumulative time spent in the RUNNING state

        Returns:
            The cumulative time (seconds) spent in the RUNNING state
        """
        return self._get_time_in_status(RunStatus.RUNNING)

    @property
    def resumption_count(self) -> int:
        """Number of times the run has been resumed

        Returns:
            The number of times the run has been resumed
        """
        return len(self.resumptions)

    @property
    def max_duration_seconds(self) -> Optional[int]:
        if self.max_duration:
            return int(self.max_duration * 3600)

    def get_gpu_hours(self) -> float:
        total = 0
        for resumption in self.resumptions:
            if not resumption.started_at:
                continue

            ended_at = resumption.ended_at
            if not ended_at:
                if self.latest_resumption.index == resumption.index:
                    ended_at = datetime.now(timezone.utc)
                else:
                    continue
            total += resumption.gpus * (ended_at - resumption.started_at).total_seconds() / (60 * 60)

        return total

    def clone(
        self,
        name: Optional[str] = None,
        image: Optional[str] = None,
        cluster: Optional[str] = None,
        instance: Optional[str] = None,
        nodes: Optional[int] = None,
        gpu_type: Optional[str] = None,
        gpus: Optional[int] = None,
        priority: Optional[str] = None,
        preemptible: Optional[bool] = None,
        max_retries: Optional[int] = None,
        max_duration: Optional[float] = None,
    ) -> Run:
        """
        Submits a new run with the same configuration as this run

        Args:
            name (str): Override the name of the run
            image (str): Override the image of the run
            cluster (str): Override the cluster of the run
            instance (str): Override the instance of the run
            nodes (int): Override the number of nodes of the run
            gpu_type (str): Override the GPU type of the run
            gpus (int): Override the number of GPUs of the run
            priority (str): Override the default priority of the run from `auto` to `low` or `lowest`
            preemptible (bool): Override whether the run can be stopped and re-queued by higher priority jobs
            max_retries (int): Override the max number of times the run can be retried
            max_duration (float): Override the max duration (in hours) that a run can run for

        Returns:
            New :class:`~mcli.api.model.run.Run` object
        """
        # pylint: disable-next=import-outside-toplevel,cyclic-import
        from mcli.api.runs import create_run

        submitted_config = self.submitted_config
        if submitted_config is None:
            refreshed_run = self.refresh()
            submitted_config = refreshed_run.submitted_config

        if not submitted_config:
            raise MAPIException(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                f'Could not find the submitted run config for run {self.name}',
            )

        if name:
            submitted_config.name = name
        if image:
            submitted_config.image = image
        if cluster:
            submitted_config.compute['cluster'] = cluster
        if instance:
            submitted_config.compute['instance'] = instance
        if nodes is not None:
            submitted_config.compute['nodes'] = nodes
        if gpu_type:
            submitted_config.compute['gpu_type'] = gpu_type
        if gpus is not None:
            submitted_config.compute['gpus'] = gpus
        if priority:
            submitted_config.scheduling['priority'] = priority
        if preemptible is not None:
            submitted_config.scheduling['preemptible'] = preemptible
        if max_retries is not None:
            submitted_config.scheduling['max_retries'] = max_retries
        if max_duration is not None:
            submitted_config.scheduling['max_duration'] = max_duration

        return create_run(submitted_config)

    def refresh(self) -> Run:
        """
        Refreshes the data on the run object

        Returns:
            Refreshed :class:`~mcli.api.model.run.Run` object
        """
        # pylint: disable-next=import-outside-toplevel,cyclic-import
        from mcli.api.runs import get_run

        return get_run(self)

    def stop(self) -> Run:
        """
        Stops the run

        Returns:
            Stopped :class:`~mcli.api.model.run.Run` object
        """
        # pylint: disable-next=import-outside-toplevel,cyclic-import
        from mcli.api.runs import stop_run

        return stop_run(self)

    def delete(self) -> Run:
        """
        Deletes the run

        Returns:
            Deleted :class:`~mcli.api.model.run.Run` object
        """
        # pylint: disable-next=import-outside-toplevel,cyclic-import
        from mcli.api.runs import delete_run
        return delete_run(self)

    def update(self,
               preemptible: Optional[bool] = None,
               priority: Optional[str] = None,
               max_retries: Optional[int] = None,
               retry_on_system_failure: Optional[bool] = None,
               max_duration: Optional[float] = None) -> Run:
        """
        Updates the run's data

        Args:
            preemptible (bool): Update whether the run can be stopped and re-queued by higher priority jobs;
                default is False
            priority (str): Update the default priority of the run from `auto` to `low` or `lowest`
            max_retries (int): Update the max number of times the run can be retried; default is 0
            retry_on_system_failure (bool): Update whether the run should be retried on system failure
                (i.e. a node failure); default is False

        Returns:
            Updated :class:`~mcli.api.model.run.Run` object
        """
        # pylint: disable-next=import-outside-toplevel,cyclic-import
        from mcli.api.runs import update_run
        return update_run(self,
                          preemptible=preemptible,
                          priority=priority,
                          max_retries=max_retries,
                          retry_on_system_failure=retry_on_system_failure,
                          max_duration=max_duration)

    def update_metadata(self, metadata: Dict[str, Any]) -> Run:
        """
        Updates the run's metadata

        Args:
            metadata (`Dict[str, Any]`): The metadata to update the run with. This will be merged with
                the existing metadata. Keys not specified in this dictionary will not be modified.

        Returns:
            Updated :class:`~mcli.api.model.run.Run` object
        """
        # pylint: disable-next=import-outside-toplevel,cyclic-import
        from mcli.api.runs import update_run_metadata

        return update_run_metadata(self, metadata)

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]) -> Run:
        missing = set(cls._required_properties) - set(response)
        if missing:
            raise MAPIException(
                status=HTTPStatus.BAD_REQUEST,
                message=f'Missing required key(s) in response to deserialize Run object: {", ".join(missing)}',
            )

        resumptions = [Resumption.from_mapi_response(r) for r in response['resumptions']]
        latest_resumption = resumptions[-1]

        max_duration = response.get('maxDurationSeconds', None)
        if max_duration:
            max_duration /= 3600

        args = {
            'run_uid': response['id'],
            'name': response['name'],
            'created_at': convert_datetime(response['createdAt']),
            'updated_at': convert_datetime(response['updatedAt']),
            'status': RunStatus.from_string(response['status']),
            'reason': latest_resumption.reason,
            'created_by': response['createdByEmail'],
            'priority': response['priority'],
            'max_retries': response.get('maxRetries'),
            'preemptible': response['preemptible'],
            'resumptions': resumptions,
            'latest_resumption': latest_resumption,
            'retry_on_system_failure': response['retryOnSystemFailure'],
            'max_duration': max_duration,
            'cluster': latest_resumption.cluster,
            'gpus': latest_resumption.gpus,
            'gpu_type': latest_resumption.gpu_type,
            'cpus': latest_resumption.cpus,
            'node_count': latest_resumption.node_count,

            # If it's not included in the response, assume it's not deleted
            'is_deleted': response['isDeleted'],
            'run_type': RunType.from_string(response['runType']),
        }

        details = response.get('details', {})
        if details:
            submitted_run_input = details.get('originalRunInput')
            args['submitted_config'] = RunConfig.from_mapi_response(
                submitted_run_input) if submitted_run_input is not None else None

            args['metadata'] = details.get('metadata')
            args['last_resumption_id'] = details.get('lastExecutionId')
            args['lifecycle'] = [RunLifecycle.from_mapi_response(l) for l in details.get('lifecycle', [])]
            args['events'] = [FormattedRunEvent.from_mapi_response(l) for l in details.get('formattedRunEvents', [])]
            args['nodes'] = [Node.from_mapi_response(n) for n in details.get('nodes', [])]
            args['image'] = details.get('image')

        return cls(**args)
