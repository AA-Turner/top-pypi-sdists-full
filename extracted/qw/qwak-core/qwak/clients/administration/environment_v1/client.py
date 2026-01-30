"""Environment V1 API client.

Provides wrapper methods for the Environment V1 gRPC service with proper error handling.
"""

from _qwak_proto.qwak.administration.v1.environments.environment_pb2 import (
    EnvironmentRuntimeConfigSpec,
)
from _qwak_proto.qwak.administration.v1.environments.environment_service_pb2 import (
    CreateEnvironmentRequest,
    CreateEnvironmentResponse,
)
from _qwak_proto.qwak.administration.v1.environments.environment_service_pb2_grpc import (
    EnvironmentServiceStub,
)
from dependency_injector.wiring import Provide
from qwak.inner.di_configuration import QwakContainer
from qwak.inner.tool.grpc.grpc_try_wrapping import grpc_try_catch_wrapper


class EnvironmentV1Client:
    """Client for interacting with the Environment V1 API.

    This client wraps the gRPC stub and provides methods with proper error handling
    using the grpc_try_catch_wrapper decorator.
    """

    def __init__(self, grpc_channel=Provide[QwakContainer.core_grpc_channel]):
        self.__environment_service = EnvironmentServiceStub(grpc_channel)

    @grpc_try_catch_wrapper("Failed to create environment {environment_name}")
    def create_environment(
        self,
        environment_name: str,
        cluster_id: str,
        spec: EnvironmentRuntimeConfigSpec,
    ) -> CreateEnvironmentResponse:
        """Create a new environment.

        Args:
            environment_name: The name of the environment.
            cluster_id: The cluster ID the environment belongs to.
            spec: The environment runtime configuration specification.

        Returns:
            CreateEnvironmentResponse with the created environment.
        """
        request = CreateEnvironmentRequest(
            environment_name=environment_name,
            cluster_id=cluster_id,
            spec=spec,
        )
        return self.__environment_service.CreateEnvironment(request)
