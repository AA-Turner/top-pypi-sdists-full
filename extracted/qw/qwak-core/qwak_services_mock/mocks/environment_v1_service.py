from typing import Optional

import grpc

from _qwak_proto.qwak.administration.v0.environments.environment_pb2 import (
    QwakEnvironment,
)
from _qwak_proto.qwak.administration.v1.environments.environment_service_pb2 import (
    CreateEnvironmentResponse,
)
from _qwak_proto.qwak.administration.v1.environments.environment_service_pb2_grpc import (
    EnvironmentServiceServicer,
)


class EnvironmentV1ServiceMock(EnvironmentServiceServicer):
    def __init__(self):
        super().__init__()
        self.__create_environment_response: Optional[CreateEnvironmentResponse] = None
        self.__create_environment_error: Optional[grpc.StatusCode] = None

    def given_create_environment(
        self,
        response: Optional[CreateEnvironmentResponse] = None,
        error_code: Optional[grpc.StatusCode] = None,
    ):
        self.__create_environment_response = response
        self.__create_environment_error = error_code

    def CreateEnvironment(self, request, context):
        if self.__create_environment_error:
            context.set_code(self.__create_environment_error)
            context.set_details("Failed to create environment")
            return CreateEnvironmentResponse()
        if self.__create_environment_response:
            return self.__create_environment_response
        return CreateEnvironmentResponse(environment=QwakEnvironment(id="mock-env-id"))
