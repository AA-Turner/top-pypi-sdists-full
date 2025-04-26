import typing
from logging import getLogger
from typing import AsyncIterable, Callable

import grpc
from flytekit.clients.auth.authenticator import Authenticator

from union._interceptor import generate_random_str

DEFAULT_KUBERNETES_TOKEN_PATH = "/var/run/secrets/kubernetes.io/serviceaccount/token"

logger = getLogger(__name__)


# See https://github.com/grpc/grpc/issues/34537 and proposed fix https://github.com/grpc/grpc/pull/36487
# Unfortunately we can't use one interceptor for unary and streaming endpoints
class ServiceAccountMetadataInterceptor:
    """
    Defines middleware to attach the service account token as authorization metadata for clients calling object store
    in an execution context
    """

    def __init__(self):
        self._service_account_token = self._read_service_account_token()

    def _read_service_account_token(self) -> typing.Optional[None]:
        try:
            with open(DEFAULT_KUBERNETES_TOKEN_PATH, "r") as token_file:
                token = token_file.read()
            return token
        except Exception as e:
            logger.debug(f"Error reading service account token: {e}, not adding to request")
            return None

    def _inject_default_metadata(self, client_call_details: grpc.aio.ClientCallDetails) -> grpc.aio.ClientCallDetails:
        if self._service_account_token is None:
            return client_call_details

        if client_call_details.metadata is not None:
            old_metadata = list(client_call_details.metadata)
        else:
            old_metadata = []

        new_metadata = [*old_metadata, ("authorization", f"Bearer {self._service_account_token}")]

        new_details = grpc.aio.ClientCallDetails(
            method=client_call_details.method,
            timeout=client_call_details.timeout,
            metadata=new_metadata,
            credentials=client_call_details.credentials,
            wait_for_ready=client_call_details.wait_for_ready,
        )
        return new_details


class UnaryUnaryClientServiceAccountMetadataInterceptor(
    grpc.aio.UnaryUnaryClientInterceptor, ServiceAccountMetadataInterceptor
):
    async def intercept_unary_unary(
        self, continuation: Callable, client_call_details: grpc.aio.ClientCallDetails, request: typing.Any
    ) -> typing.Any:
        new_client_call_details = super()._inject_default_metadata(client_call_details)
        return await continuation(new_client_call_details, request)


class UnaryStreamClientServiceAccountMetadataInterceptor(
    grpc.aio.UnaryStreamClientInterceptor, ServiceAccountMetadataInterceptor
):
    async def intercept_unary_stream(
        self, continuation: Callable, client_call_details: grpc.aio.ClientCallDetails, request: any
    ) -> AsyncIterable:
        new_client_call_details = super()._inject_default_metadata(client_call_details)
        return await continuation(new_client_call_details, request)


class StreamUnaryClientServiceAccountMetadataInterceptor(
    grpc.aio.StreamUnaryClientInterceptor, ServiceAccountMetadataInterceptor
):
    async def intercept_stream_unary(
        self,
        continuation: Callable,
        client_call_details: grpc.aio.ClientCallDetails,
        request_iterator: any,
    ) -> grpc.aio.StreamUnaryCall:
        new_client_call_details = super()._inject_default_metadata(client_call_details)
        return await continuation(new_client_call_details, request_iterator)


class StreamStreamClientServiceAccountMetadataInterceptor(
    grpc.aio.StreamStreamClientInterceptor, ServiceAccountMetadataInterceptor
):
    async def intercept_stream_stream(
        self,
        continuation: Callable,
        client_call_details: grpc.aio.ClientCallDetails,
        request_iterator: typing.AsyncIterator[any],
    ) -> grpc.aio.Call:
        new_client_call_details = super()._inject_default_metadata(client_call_details)
        return await continuation(new_client_call_details, request_iterator)


class AuthInterceptor:
    def __init__(self, authenticator: Authenticator):
        self._authenticator = authenticator

    async def _call_details_with_auth_metadata(
        self, client_call_details: grpc.aio.ClientCallDetails
    ) -> grpc.aio.ClientCallDetails:
        """
        Returns new ClientCallDetails with metadata added.
        """
        request_id = f"u-{generate_random_str(20)}"
        metadata = []
        if client_call_details.metadata:
            metadata.extend(list(client_call_details.metadata))
        metadata.append(("x-request-id", request_id))
        auth_metadata = self._authenticator.fetch_grpc_call_auth_metadata()
        if auth_metadata:
            metadata.append(auth_metadata)

        return grpc.aio.ClientCallDetails(
            method=client_call_details.method,
            timeout=client_call_details.timeout,
            metadata=metadata,
            credentials=client_call_details.credentials,
            wait_for_ready=client_call_details.wait_for_ready,
        )


class UnaryUnaryClientAuthInterceptor(grpc.aio.UnaryUnaryClientInterceptor, AuthInterceptor):
    async def intercept_unary_unary(
        self, continuation: Callable, client_call_details: grpc.aio.ClientCallDetails, request: typing.Any
    ) -> typing.Any:
        new_client_call_details = await super()._call_details_with_auth_metadata(client_call_details)
        try:
            continuation = await continuation(new_client_call_details, request)
            return continuation
        except Exception as e:
            if not hasattr(e, "code"):
                raise e
            if e.code() == grpc.StatusCode.UNAUTHENTICATED or e.code() == grpc.StatusCode.UNKNOWN:
                self._authenticator.refresh_credentials()
                updated_call_details = await super()._call_details_with_auth_metadata(client_call_details)
                return continuation(updated_call_details, request)


class UnaryStreamClientAuthInterceptor(grpc.aio.UnaryStreamClientInterceptor, AuthInterceptor):
    async def intercept_unary_stream(
        self, continuation: Callable, client_call_details: grpc.aio.ClientCallDetails, request: any
    ) -> AsyncIterable:
        new_client_call_details = await super()._call_details_with_auth_metadata(client_call_details)
        return await continuation(new_client_call_details, request)


class StreamUnaryClientAuthInterceptor(grpc.aio.StreamUnaryClientInterceptor, AuthInterceptor):
    async def intercept_stream_unary(
        self,
        continuation: Callable,
        client_call_details: grpc.aio.ClientCallDetails,
        request_iterator: any,
    ) -> grpc.aio.StreamUnaryCall:
        new_client_call_details = await super()._call_details_with_auth_metadata(client_call_details)
        return await continuation(new_client_call_details, request_iterator)


class StreamStreamClientAuthInterceptor(grpc.aio.StreamStreamClientInterceptor, AuthInterceptor):
    async def intercept_stream_stream(
        self,
        continuation: Callable,
        client_call_details: grpc.aio.ClientCallDetails,
        request_iterator: typing.AsyncIterator[any],
    ) -> grpc.aio.Call:
        new_client_call_details = await super()._call_details_with_auth_metadata(client_call_details)
        return await continuation(new_client_call_details, request_iterator)
