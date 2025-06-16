import typing
from typing import Callable, List, Tuple

import grpc
from cognite.seismic._version import get_version
from grpc import ClientCallDetails, UnaryStreamClientInterceptor, UnaryUnaryClientInterceptor

if typing.TYPE_CHECKING:
    from grpc import CallFuture, CallIterator, Metadata, TRequest, TResponse


class ApiKeyAuth(grpc.AuthMetadataPlugin):
    "Inject the api-key header with an API key in GRPC requests"

    _metadata: List[Tuple[str, str]]

    def __init__(self, project_name: str, api_key: str):
        if project_name is None:
            self._metadata = [("api-key", api_key)]
        else:
            self._metadata = [("api-key", api_key), ("cdf-project-name", project_name)]

    def __call__(self, context, callback):
        callback(self._metadata, None)


class BearerTokenAuth(grpc.AuthMetadataPlugin):
    "Inject an authorization header with a bearer token in GRPC requests"

    def __init__(self, project_name: str, token_supplier: Callable[[], str]):
        self._project_metadata = ("cdf-project-name", project_name)
        self._token_supplier = token_supplier

    def __call__(self, context, callback):
        callback((("authorization", "Bearer " + self._token_supplier()), self._project_metadata), None)


class SdkVersionedCall(ClientCallDetails):
    metadata: "Metadata"

    def __init__(self, client_call_details: ClientCallDetails):
        version = ("x-cdp-sdk", f"CogniteSeismicPythonSDK:{get_version()}")
        if client_call_details.metadata is None:
            self.metadata = (version,)
        else:
            self.metadata = (version, *client_call_details.metadata)


def interceptor_internal(client_call_details: ClientCallDetails):
    return SdkVersionedCall(client_call_details)


class UnaryUnaryMetadataInterceptor(UnaryUnaryClientInterceptor):
    def intercept_unary_unary(
        self,
        continuation: typing.Callable[[ClientCallDetails, "TRequest"], "CallFuture[TResponse]"],
        client_call_details: ClientCallDetails,
        request: "TRequest",
    ) -> "CallFuture[TResponse]":
        details = interceptor_internal(client_call_details)
        return continuation(details, request)


class UnaryStreamMetadataInterceptor(UnaryStreamClientInterceptor):
    def intercept_unary_stream(
        self,
        continuation: typing.Callable[[ClientCallDetails, "TRequest"], "CallIterator[TResponse]"],
        client_call_details: ClientCallDetails,
        request: "TRequest",
    ) -> "CallIterator[TResponse]":
        details = interceptor_internal(client_call_details)
        return continuation(details, request)
