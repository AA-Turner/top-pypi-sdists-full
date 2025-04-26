import base64
import logging
from collections import defaultdict
from types import ModuleType
from typing import List

from google.protobuf.message import Message

from tecton_core import http
from tecton_core.metadata_service_impl import base_stub
from tecton_core.metadata_service_impl import error_lib
from tecton_core.metadata_service_impl import providers
from tecton_core.metadata_service_impl.response import MDSResponse
from tecton_core.metadata_service_impl.service_calls import GrpcCall
from tecton_core.metadata_service_impl.service_calls import get_method_name_to_grpc_call


logger = logging.getLogger(__name__)

requests_session = http.session()


class PureHTTPStub(base_stub.BaseStub):
    def __init__(self, request_provider: providers.RequestProvider, grpc_service_modules: List[ModuleType]) -> None:
        """
        PureHTTPStub mimics the interface exposed by a gRPC client for MetadataService.
        Callers can invoke a method like stub.GetFeatureView and it's transformed for an HTTP
        request using _InternalHTTPStub in the __getattr__ method below.
        """
        self._stub_obj = _InternalHTTPStub(request_provider)
        self._method_name_to_grpc_call = get_method_name_to_grpc_call(grpc_service_modules)

    def __getattr__(self, method_name):
        """
        Transforms methods called directly on PureHTTPStub to _InternalHTTPStub requests.
        E.g. PureHTTPStub::SomeMethod(request) is transformed to _InternalHTTPStub::execute('SomeMethod', request).

        An AttributeError is raised if the method invoked does not match a MetadataService RPC method.
        """
        if method_name not in self._method_name_to_grpc_call:
            msg = f"Nonexistent MetadataService method: {method_name}"
            raise AttributeError(msg)

        def method(request: Message, timeout_sec: float = 300.0) -> MDSResponse:
            return self._stub_obj.execute(self._method_name_to_grpc_call[method_name], request, timeout_sec)

        return method

    def close(self):
        pass


class _InternalHTTPStub:
    def __init__(self, request_provider: providers.RequestProvider) -> None:
        self.request_provider = request_provider

    def execute(self, grpc_call: GrpcCall, request: Message, timeout_sec: float) -> MDSResponse:
        """
        :param grpc_call: gRPC call object representation
        :param request: Request proto.
        :param timeout_sec: timeout for request in seconds

        :return: Response proto.
        """
        json_request = {}
        json_request["method"] = grpc_call.method
        json_request["metadata"] = self.request_provider.request_headers()
        json_request["request"] = base64.encodebytes(grpc_call.request_serializer(request)).decode("utf-8")

        request_url = self.request_provider.request_url()
        response = requests_session.post(request_url, json=json_request, timeout=timeout_sec)
        response.raise_for_status()
        body = response.json()

        code = body["status"]["code"]
        if code != error_lib.gRPCStatus.OK.value:
            details = body["status"]["detail"]
            error_lib.raise_for_grpc_status(code, details, request_url, self.request_provider)

        response_bytes = base64.decodebytes(body["response"].encode("utf-8"))
        response_proto = grpc_call.response_deserializer(response_bytes)
        metadata = body.get("metadata", "")
        return MDSResponse(response_proto, defaultdict(str, metadata))
