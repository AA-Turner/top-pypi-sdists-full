"""
Type annotations for simspaceweaver service Client.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_simspaceweaver/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_simspaceweaver.client import SimSpaceWeaverClient

    session = Session()
    client: SimSpaceWeaverClient = session.client("simspaceweaver")
    ```
"""

from __future__ import annotations

import sys
from typing import Any

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .type_defs import (
    CreateSnapshotInputTypeDef,
    DeleteAppInputTypeDef,
    DeleteSimulationInputTypeDef,
    DescribeAppInputTypeDef,
    DescribeAppOutputTypeDef,
    DescribeSimulationInputTypeDef,
    DescribeSimulationOutputTypeDef,
    ListAppsInputTypeDef,
    ListAppsOutputTypeDef,
    ListSimulationsInputTypeDef,
    ListSimulationsOutputTypeDef,
    ListTagsForResourceInputTypeDef,
    ListTagsForResourceOutputTypeDef,
    StartAppInputTypeDef,
    StartAppOutputTypeDef,
    StartClockInputTypeDef,
    StartSimulationInputTypeDef,
    StartSimulationOutputTypeDef,
    StopAppInputTypeDef,
    StopClockInputTypeDef,
    StopSimulationInputTypeDef,
    TagResourceInputTypeDef,
    UntagResourceInputTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Dict, Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("SimSpaceWeaverClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class SimSpaceWeaverClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/simspaceweaver.html#SimSpaceWeaver.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_simspaceweaver/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SimSpaceWeaverClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/simspaceweaver.html#SimSpaceWeaver.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_simspaceweaver/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/simspaceweaver/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_simspaceweaver/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/simspaceweaver/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_simspaceweaver/client/#generate_presigned_url)
        """

    def create_snapshot(self, **kwargs: Unpack[CreateSnapshotInputTypeDef]) -> Dict[str, Any]:
        """
        Creates a snapshot of the specified simulation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/simspaceweaver/client/create_snapshot.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_simspaceweaver/client/#create_snapshot)
        """

    def delete_app(self, **kwargs: Unpack[DeleteAppInputTypeDef]) -> Dict[str, Any]:
        """
        Deletes the instance of the given custom app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/simspaceweaver/client/delete_app.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_simspaceweaver/client/#delete_app)
        """

    def delete_simulation(self, **kwargs: Unpack[DeleteSimulationInputTypeDef]) -> Dict[str, Any]:
        """
        Deletes all SimSpace Weaver resources assigned to the given simulation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/simspaceweaver/client/delete_simulation.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_simspaceweaver/client/#delete_simulation)
        """

    def describe_app(self, **kwargs: Unpack[DescribeAppInputTypeDef]) -> DescribeAppOutputTypeDef:
        """
        Returns the state of the given custom app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/simspaceweaver/client/describe_app.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_simspaceweaver/client/#describe_app)
        """

    def describe_simulation(
        self, **kwargs: Unpack[DescribeSimulationInputTypeDef]
    ) -> DescribeSimulationOutputTypeDef:
        """
        Returns the current state of the given simulation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/simspaceweaver/client/describe_simulation.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_simspaceweaver/client/#describe_simulation)
        """

    def list_apps(self, **kwargs: Unpack[ListAppsInputTypeDef]) -> ListAppsOutputTypeDef:
        """
        Lists all custom apps or service apps for the given simulation and domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/simspaceweaver/client/list_apps.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_simspaceweaver/client/#list_apps)
        """

    def list_simulations(
        self, **kwargs: Unpack[ListSimulationsInputTypeDef]
    ) -> ListSimulationsOutputTypeDef:
        """
        Lists the SimSpace Weaver simulations in the Amazon Web Services account used
        to make the API call.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/simspaceweaver/client/list_simulations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_simspaceweaver/client/#list_simulations)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        Lists all tags on a SimSpace Weaver resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/simspaceweaver/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_simspaceweaver/client/#list_tags_for_resource)
        """

    def start_app(self, **kwargs: Unpack[StartAppInputTypeDef]) -> StartAppOutputTypeDef:
        """
        Starts a custom app with the configuration specified in the simulation schema.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/simspaceweaver/client/start_app.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_simspaceweaver/client/#start_app)
        """

    def start_clock(self, **kwargs: Unpack[StartClockInputTypeDef]) -> Dict[str, Any]:
        """
        Starts the simulation clock.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/simspaceweaver/client/start_clock.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_simspaceweaver/client/#start_clock)
        """

    def start_simulation(
        self, **kwargs: Unpack[StartSimulationInputTypeDef]
    ) -> StartSimulationOutputTypeDef:
        """
        Starts a simulation with the given name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/simspaceweaver/client/start_simulation.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_simspaceweaver/client/#start_simulation)
        """

    def stop_app(self, **kwargs: Unpack[StopAppInputTypeDef]) -> Dict[str, Any]:
        """
        Stops the given custom app and shuts down all of its allocated compute
        resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/simspaceweaver/client/stop_app.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_simspaceweaver/client/#stop_app)
        """

    def stop_clock(self, **kwargs: Unpack[StopClockInputTypeDef]) -> Dict[str, Any]:
        """
        Stops the simulation clock.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/simspaceweaver/client/stop_clock.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_simspaceweaver/client/#stop_clock)
        """

    def stop_simulation(self, **kwargs: Unpack[StopSimulationInputTypeDef]) -> Dict[str, Any]:
        """
        Stops the given simulation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/simspaceweaver/client/stop_simulation.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_simspaceweaver/client/#stop_simulation)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceInputTypeDef]) -> Dict[str, Any]:
        """
        Adds tags to a SimSpace Weaver resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/simspaceweaver/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_simspaceweaver/client/#tag_resource)
        """

    def untag_resource(self, **kwargs: Unpack[UntagResourceInputTypeDef]) -> Dict[str, Any]:
        """
        Removes tags from a SimSpace Weaver resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/simspaceweaver/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_simspaceweaver/client/#untag_resource)
        """
