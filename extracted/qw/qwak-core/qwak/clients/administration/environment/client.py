import grpc
from _qwak_proto.qwak.administration.v0.environments.environment_pb2 import (
    QwakEnvironmentStatus,
)
from _qwak_proto.qwak.administration.v0.environments.configuration_pb2 import (
    QwakEnvironmentConfiguration,
)
from _qwak_proto.qwak.administration.v0.environments.environment_service_pb2 import (
    GetEnvironmentApplicationUserCredentialsRequest,
    GetEnvironmentApplicationUserCredentialsResponse,
    ListEnvironmentsRequest,
    ListEnvironmentsResponse,
    GetEnvironmentResponse,
    GetEnvironmentRequest,
    UpdateEnvironmentConfigurationRequest,
    UpdateEnvironmentConfigurationResponse,
)
from _qwak_proto.qwak.administration.v0.environments.environment_service_pb2_grpc import (
    EnvironmentServiceStub,
)
from dependency_injector.wiring import Provide
from qwak.exceptions import QwakException
from qwak.inner.di_configuration import QwakContainer
from qwak.inner.tool.grpc.grpc_try_wrapping import grpc_try_catch_wrapper


class EnvironmentClient:
    """
    Used for interacting with Qwak's Environemt
    """

    def __init__(self, grpc_channel=Provide[QwakContainer.core_grpc_channel]):
        self._environment_service = EnvironmentServiceStub(grpc_channel)

    def list_environments(self) -> ListEnvironmentsResponse:
        """
        List of all environment without filter
        Return ListEnvironmentsResponse
        """
        request = ListEnvironmentsRequest()
        try:
            return self._environment_service.ListEnvironments(request)
        except grpc.RpcError as e:
            raise QwakException(
                f"Failed to get List of environments, error is {e.details()}"
            )

    def list_environments_by_status(
        self, status: QwakEnvironmentStatus
    ) -> ListEnvironmentsResponse:
        """
        List of all environment without filter
        Args: status which filter environment by
        Return: ListEnvironmentsResponse

        """
        try:
            request = ListEnvironmentsRequest(
                filter=ListEnvironmentsRequest.Filter(environment_status=status)
            )
            return self._environment_service.ListEnvironments(request)
        except grpc.RpcError as e:
            raise QwakException(
                f"Failed to get List of environments with status, error is {e.details()}"
            )

    def get_environment_application_user(
        self, environment_id: str
    ) -> GetEnvironmentApplicationUserCredentialsResponse:
        """
        Get application user by environment id
        Return: GetEnvironmentApplicationUserCredentialsResponse
        """
        request = GetEnvironmentApplicationUserCredentialsRequest(
            environment_id=environment_id
        )
        try:
            return self._environment_service.GetEnvironmentApplicationUserCredentials(
                request
            )
        except grpc.RpcError as e:
            raise QwakException(
                f"Failed to get application user, error is {e.details()}"
            )

    def get_environment(self, environment_id: str) -> GetEnvironmentResponse:
        """
        Get Environment by id
        :param environment_id:
        Return: GetEnvironmentResponse
        """
        request = GetEnvironmentRequest(environment_id=environment_id)
        try:
            return self._environment_service.GetEnvironment(request)
        except grpc.RpcError as e:
            raise QwakException(
                f"Failed to get environment {environment_id}, error is {e}"
            )

    @grpc_try_catch_wrapper(
        "Failed to update environment configuration for {environment_id}"
    )
    def update_environment_configuration(
        self, environment_id: str, configuration: QwakEnvironmentConfiguration
    ) -> UpdateEnvironmentConfigurationResponse:
        """
        Update environment configuration.

        Args:
            environment_id: The environment ID to update.
            configuration: The new environment configuration.

        Returns:
            UpdateEnvironmentConfigurationResponse
        """
        request = UpdateEnvironmentConfigurationRequest(
            environment_id=environment_id,
            configuration=configuration,
        )
        return self._environment_service.UpdateEnvironmentConfiguration(request)
