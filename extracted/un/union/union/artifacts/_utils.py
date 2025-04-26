import datetime
import typing
from typing import Union

from flyteidl.core import artifact_id_pb2 as art_id
from flytekit.core.artifact import ArtifactQuery, Partitions, TimePartition
from google.protobuf.timestamp_pb2 import Timestamp

from union.internal.artifacts import artifacts_pb2


def _construct_artifact_key(
    project: typing.Optional[str] = None,
    domain: typing.Optional[str] = None,
    name: typing.Optional[str] = None,
    artifact_key: typing.Optional[art_id.ArtifactKey] = None,
    query: typing.Optional[ArtifactQuery] = None,
) -> art_id.ArtifactKey:
    if artifact_key:
        ak = artifact_key
    elif query:
        p = query.artifact.project or project
        d = query.artifact.domain or domain
        n = query.artifact.name  # if a query is given, name should be specified in the artifact
        ak = _get_artifact_key(p, d, n)
    else:
        ak = _get_artifact_key(project, domain, name)
    return ak


def _construct_partitions(
    query: typing.Optional[ArtifactQuery] = None,
    partitions: typing.Optional[Union[Partitions, typing.Dict[str, str]]] = None,
) -> typing.Optional[art_id.Partitions]:
    idl_partitions = None
    if query and query.partitions:
        if partitions:
            raise ValueError("Cannot specify partitions in both query and as an argument.")
        idl_partitions = query.partitions.to_flyte_idl()
    elif isinstance(partitions, Partitions):
        idl_partitions = partitions.to_flyte_idl()
    elif partitions:
        idl_partitions = Partitions(partitions).to_flyte_idl()
    return idl_partitions


def _construct_time_stamp(
    query: typing.Optional[ArtifactQuery] = None,
    time_partition: typing.Optional[Union[datetime.datetime, TimePartition]] = None,
) -> typing.Optional[Timestamp]:
    idl_time_partition = None
    if query and query.time_partition:
        if time_partition:
            raise ValueError("Cannot specify time partition in both query and as an argument.")
        idl_time_partition = query.time_partition.value.time_value
    elif isinstance(time_partition, TimePartition):
        idl_time_partition = time_partition.to_flyte_idl().value.time_value
    elif time_partition:
        if not isinstance(time_partition, datetime.datetime):
            raise ValueError("Time partition must be a datetime or TimePartition object.")
        idl_time_partition = Timestamp()
        idl_time_partition.FromDatetime(time_partition)
    return idl_time_partition


def construct_search_artifact_request(
    project: typing.Optional[str] = None,
    domain: typing.Optional[str] = None,
    name: typing.Optional[str] = None,
    artifact_key: typing.Optional[art_id.ArtifactKey] = None,
    query: typing.Optional[ArtifactQuery] = None,
    partitions: typing.Optional[Union[Partitions, typing.Dict[str, str]]] = None,
    time_partition: typing.Optional[Union[datetime.datetime, TimePartition]] = None,
    group_by_key: bool = False,
    limit: int = 100,
    token: typing.Optional[str] = None,
) -> artifacts_pb2.SearchArtifactsRequest:
    # Construct key - must have either an artifact key or project, domain, name specified, or a query input
    ak = _construct_artifact_key(project, domain, name, artifact_key, query)

    # Construct partitions object, if applicable, can be None
    idl_partitions = _construct_partitions(query, partitions)

    # Construct time partition object, if applicable, can be None
    idl_time_partition = _construct_time_stamp(query, time_partition)

    # Construct search options based on input args
    search_options = artifacts_pb2.SearchOptions(
        strict_partitions=False,  # always set this to false so the user doesn't have to specify all partitions
        latest_by_key=group_by_key,
    )

    search_request = artifacts_pb2.SearchArtifactsRequest(
        artifact_key=ak,
        partitions=idl_partitions,
        time_partition_value=idl_time_partition,
        options=search_options,
        limit=limit,
        token=token,
        version=None,  # leave this empty, if you have the version, use get instead.
        principal=None,  # leave this empty for now, we don't have a nice way to get okta id
        granularity=None,  # leave this empty for now until time partition is handled
    )
    return search_request


def _get_artifact_key(
    project: typing.Optional[str] = None,
    domain: typing.Optional[str] = None,
    name: typing.Optional[str] = None,
) -> art_id.ArtifactKey:
    if not project or not domain or not name:
        raise ValueError("Project, domain, and name are required to create an artifact key")

    return art_id.ArtifactKey(
        project=project,
        domain=domain,
        name=name,
    )
