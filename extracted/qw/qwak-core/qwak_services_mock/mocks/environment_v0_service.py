from typing import Optional

import grpc

from _qwak_proto.qwak.administration.v0.environments.environment_pb2 import (
    QwakEnvironment,
)
from _qwak_proto.qwak.administration.v0.environments.environment_service_pb2 import (
    CreateEnvironmentResponse,
    GetEnvironmentApplicationUserCredentialsResponse,
    GetEnvironmentResponse,
    ListEnvironmentsResponse,
    SetEnvironmentApplicationUserCredentialsResponse,
    UpdateEnvironmentConfigurationResponse,
    UpdateEnvironmentPersonalizationResponse,
)
from _qwak_proto.qwak.administration.v0.environments.environment_service_pb2_grpc import (
    EnvironmentServiceServicer,
)


class EnvironmentV0ServiceMock(EnvironmentServiceServicer):
    def __init__(self):
        super().__init__()
        self.__create_environment_response: Optional[CreateEnvironmentResponse] = None
        self.__create_environment_error: Optional[grpc.StatusCode] = None

        self.__get_environment_response: Optional[GetEnvironmentResponse] = None
        self.__get_environment_error: Optional[grpc.StatusCode] = None

        self.__update_environment_configuration_response: Optional[
            UpdateEnvironmentConfigurationResponse
        ] = None
        self.__update_environment_configuration_error: Optional[grpc.StatusCode] = None

        self.__update_environment_personalization_response: Optional[
            UpdateEnvironmentPersonalizationResponse
        ] = None
        self.__update_environment_personalization_error: Optional[grpc.StatusCode] = (
            None
        )

        self.__list_environments_response: Optional[ListEnvironmentsResponse] = None
        self.__list_environments_error: Optional[grpc.StatusCode] = None

        self.__get_credentials_response: Optional[
            GetEnvironmentApplicationUserCredentialsResponse
        ] = None
        self.__get_credentials_error: Optional[grpc.StatusCode] = None

        self.__set_credentials_response: Optional[
            SetEnvironmentApplicationUserCredentialsResponse
        ] = None
        self.__set_credentials_error: Optional[grpc.StatusCode] = None

    def given_create_environment(
        self,
        response: Optional[CreateEnvironmentResponse] = None,
        error_code: Optional[grpc.StatusCode] = None,
    ):
        self.__create_environment_response = response
        self.__create_environment_error = error_code

    def given_get_environment(
        self,
        response: Optional[GetEnvironmentResponse] = None,
        error_code: Optional[grpc.StatusCode] = None,
    ):
        self.__get_environment_response = response
        self.__get_environment_error = error_code

    def given_update_environment_configuration(
        self,
        response: Optional[UpdateEnvironmentConfigurationResponse] = None,
        error_code: Optional[grpc.StatusCode] = None,
    ):
        self.__update_environment_configuration_response = response
        self.__update_environment_configuration_error = error_code

    def given_update_environment_personalization(
        self,
        response: Optional[UpdateEnvironmentPersonalizationResponse] = None,
        error_code: Optional[grpc.StatusCode] = None,
    ):
        self.__update_environment_personalization_response = response
        self.__update_environment_personalization_error = error_code

    def given_list_environments(
        self,
        response: Optional[ListEnvironmentsResponse] = None,
        error_code: Optional[grpc.StatusCode] = None,
    ):
        self.__list_environments_response = response
        self.__list_environments_error = error_code

    def given_get_credentials(
        self,
        response: Optional[GetEnvironmentApplicationUserCredentialsResponse] = None,
        error_code: Optional[grpc.StatusCode] = None,
    ):
        self.__get_credentials_response = response
        self.__get_credentials_error = error_code

    def given_set_credentials(
        self,
        response: Optional[SetEnvironmentApplicationUserCredentialsResponse] = None,
        error_code: Optional[grpc.StatusCode] = None,
    ):
        self.__set_credentials_response = response
        self.__set_credentials_error = error_code

    def CreateEnvironment(self, request, context):
        if self.__create_environment_error:
            context.set_code(self.__create_environment_error)
            context.set_details("Failed to create environment")
            return CreateEnvironmentResponse()
        if self.__create_environment_response:
            return self.__create_environment_response
        return CreateEnvironmentResponse(environment=QwakEnvironment(id="mock-env-id"))

    def GetEnvironment(self, request, context):
        if self.__get_environment_error:
            context.set_code(self.__get_environment_error)
            context.set_details("Failed to get environment")
            return GetEnvironmentResponse()
        if self.__get_environment_response:
            return self.__get_environment_response
        return GetEnvironmentResponse(
            environment=QwakEnvironment(id=request.environment_id)
        )

    def UpdateEnvironmentConfiguration(self, request, context):
        if self.__update_environment_configuration_error:
            context.set_code(self.__update_environment_configuration_error)
            context.set_details("Failed to update environment configuration")
            return UpdateEnvironmentConfigurationResponse()
        if self.__update_environment_configuration_response:
            return self.__update_environment_configuration_response
        return UpdateEnvironmentConfigurationResponse()

    def UpdateEnvironmentPersonalization(self, request, context):
        if self.__update_environment_personalization_error:
            context.set_code(self.__update_environment_personalization_error)
            context.set_details("Failed to update environment personalization")
            return UpdateEnvironmentPersonalizationResponse()
        if self.__update_environment_personalization_response:
            return self.__update_environment_personalization_response
        return UpdateEnvironmentPersonalizationResponse()

    def ListEnvironments(self, request, context):
        if self.__list_environments_error:
            context.set_code(self.__list_environments_error)
            context.set_details("Failed to list environments")
            return ListEnvironmentsResponse()
        if self.__list_environments_response:
            return self.__list_environments_response
        return ListEnvironmentsResponse()

    def GetEnvironmentApplicationUserCredentials(self, request, context):
        if self.__get_credentials_error:
            context.set_code(self.__get_credentials_error)
            context.set_details("Failed to get credentials")
            return GetEnvironmentApplicationUserCredentialsResponse()
        if self.__get_credentials_response:
            return self.__get_credentials_response
        return GetEnvironmentApplicationUserCredentialsResponse()

    def SetEnvironmentApplicationUserCredentials(self, request, context):
        if self.__set_credentials_error:
            context.set_code(self.__set_credentials_error)
            context.set_details("Failed to set credentials")
            return SetEnvironmentApplicationUserCredentialsResponse()
        if self.__set_credentials_response:
            return self.__set_credentials_response
        return SetEnvironmentApplicationUserCredentialsResponse()
