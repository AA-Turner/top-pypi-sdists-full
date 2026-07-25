"""gRPC client wrapper for Query Cache API."""

from __future__ import annotations

import sys
import logging
import traceback
import typing as t
from types import TracebackType

import grpc
from dbt_state.auth import GrpcAuthPlugin, sso_auth
from dbt_state import events
from dbt_state.config import get_env
from dbt_state.errors import (
    AuthenticationError,
    CertificateError,
    RecoverableAuthenticationError,
)
from dbt_state.grpc.interceptors import (
    InvocationInfoInterceptor,
    OrgIdInterceptor,
    RequestIdInterceptor,
    SessionIdInterceptor,
    SubmittedAtEpochInterceptor,
    SystemInfoInterceptor,
)
from dbt_state.utils import str_to_bool
from dbt_state.config import RunCacheConfig
from query_cache_protobuf.query_cache.services import (
    clone_service_pb2_grpc,
    execution_service_pb2_grpc,
    sql_service_pb2_grpc,
    client_telemetry_service_pb2_grpc,
    client_validation_service_pb2_grpc,
    explain_service_pb2_grpc,
)
from dbt_state.version import __version__
from query_cache_common.constants import REQUEST_ID_HEADER
from query_cache_common.models.services import (
    client_validation_service_models,
    explain_service_models,
    sql_service_models,
    clone_service_models,
    execution_service_models,
)


if t.TYPE_CHECKING:
    from dbt_state._typing import SpeculativeSubmitResponse, SQLSubmitResponse

    if sys.version_info >= (3, 11):
        from typing import Self
    else:
        from typing_extensions import Self

WEB_APP_URL = get_env("WEB_APP_URL", "https://app.state.dbt.com")
"""Base URL of the standalone web app"""

logger = logging.getLogger(__name__)


class QueryCacheGrpcClient:
    """gRPC client for Query Cache API."""

    def __init__(
        self,
        server_address: str,
        timeout: float = 60.0,
        channel_credentials: t.Optional[grpc.ChannelCredentials] = None,
        session_id: t.Optional[str] = None,
        org_id: t.Optional[str] = None,
        system_user_id: str = "",
        os_name: str = "",
        invocation_id: str = "",
        cloud_run_id: str = "",
    ):
        """Initialize gRPC client.

        Args:
            server_address: gRPC server address (e.g., "localhost:50051")
            timeout: Request timeout in seconds
            channel_credentials: gRPC ChannelCredentials for secure connection
            session_id: Session ID for tracking
            org_id: Organization ID for this request. Should always be set except when running locally
            system_user_id: Persistent system user UUID
            os_name: Client operating system name
            invocation_id: dbt's per-invocation UUID for this run
            cloud_run_id: dbt platform run ID, if running on the dbt platform (else empty)
        """
        self._session_id = session_id
        self.server_address = server_address
        self.timeout = timeout

        interceptors: list[grpc.UnaryUnaryClientInterceptor] = [
            RequestIdInterceptor(),
            SessionIdInterceptor(session_id=self._session_id),
            SubmittedAtEpochInterceptor(),
            SystemInfoInterceptor(system_user_id=system_user_id, os_name=os_name),
            InvocationInfoInterceptor(invocation_id=invocation_id, cloud_run_id=cloud_run_id),
        ]

        if channel_credentials:
            channel = grpc.secure_channel(server_address, channel_credentials)
            if not org_id:
                raise ValueError("Organization ID must be provided when using secure channel")
            interceptors.append(OrgIdInterceptor(org_id))
        else:
            channel = grpc.insecure_channel(server_address)

        self.channel = grpc.intercept_channel(channel, *interceptors)

        self._is_closed = False

        # Initialize service stubs
        self.sql_stub = sql_service_pb2_grpc.SQLStub(self.channel)
        self.clone_stub = clone_service_pb2_grpc.CloneStub(self.channel)
        self.execution_stub = execution_service_pb2_grpc.ExecutionStub(self.channel)
        self.client_telemetry_stub = client_telemetry_service_pb2_grpc.ClientTelemetryStub(
            self.channel
        )
        self.client_validation_stub = client_validation_service_pb2_grpc.ClientValidationStub(
            self.channel
        )
        self.explain_stub = explain_service_pb2_grpc.ExplainStub(self.channel)

    @classmethod
    def create(
        cls,
        run_cache_config: RunCacheConfig,
        session_id: str,
        system_user_id: str = "",
        os_name: str = "",
        invocation_id: str = "",
        cloud_run_id: str = "",
    ) -> QueryCacheGrpcClient:
        grpc_address = get_env("API_URL", "api.state.dbt.com:443")
        if not grpc_address:
            raise ValueError(
                "RUN_CACHE_API_URL environment variable is required. "
                "Example: RUN_CACHE_API_URL=localhost:50051"
            )
        secure_str = get_env("API_SECURE")
        if secure_str:
            secure = str_to_bool(secure_str)
        else:
            secure = grpc_address.strip().endswith(":443")

        org_id = None
        if secure:
            sso = sso_auth(
                client_id=run_cache_config.oauth_client_id,
                client_secret=run_cache_config.oauth_client_secret,
                org_id=run_cache_config.org_id,
                dbt_platform_tokens=run_cache_config.dbt_platform_tokens,
            )
            try:
                sso.refresh_token()
            except Exception as e:
                logger.debug(
                    "Token refresh failed, proceeding with regular authentication flow: %s", str(e)
                )
            ssl_creds = grpc.ssl_channel_credentials(_get_root_certificates())
            call_creds = grpc.metadata_call_credentials(GrpcAuthPlugin(sso))
            channel_credentials = grpc.composite_channel_credentials(ssl_creds, call_creds)

            # Eagerly authenticate during client creation to avoid delays on first RPC call.
            # For users without credentials, this triggers the OAuth flow before first use.
            #
            # Note: org_id()/refresh_token() only perform OAuth over HTTP plus local JWT
            # parsing — they never make a gRPC call — so no grpc.RpcError can originate here.
            # A locked account surfaces server-side as PERMISSION_DENIED/UNAUTHENTICATED on
            # the first real RPC (e.g. is_client_version_supported), which the runner already
            # treats as non-fatal and fails open on.
            try:
                org_id = sso.org_id(login=True)
            except AuthenticationError:
                # Re-raise as-is: the message is already good and the type already encodes
                # the correct fail-open (RecoverableAuthenticationError) vs. fail-closed
                # behavior. In particular, bad/expired credentials surface here as a plain
                # (fail-closed) AuthenticationError, so they still halt the run with an
                # actionable error rather than silently disabling state.
                raise
            except Exception as e:
                # Unexpected, non-credential errors (e.g. the OAuth/token endpoint is
                # unreachable) are plausibly our fault, so fail open rather than block the run.
                logger.error("Unexpected error during eager authentication: %s", e)
                raise RecoverableAuthenticationError(
                    f"Failed to authenticate with dbt State: {e}."
                ) from e

            if sso.is_personal_org():
                events.fire_warn_event(
                    "You are using a personal sandbox org. To collaborate and manage a "
                    "team, create a real organization: {}/new-organization",
                    WEB_APP_URL,
                )
        else:
            channel_credentials = None

        return QueryCacheGrpcClient(
            server_address=grpc_address,
            timeout=float(run_cache_config.api_client_timeout),
            channel_credentials=channel_credentials,
            org_id=org_id,
            session_id=session_id,
            system_user_id=system_user_id,
            os_name=os_name,
            invocation_id=invocation_id,
            cloud_run_id=cloud_run_id,
        )

    def _check_channel_state(self, method_name: str) -> None:
        """Check if channel is closed before making RPC call."""
        if self._is_closed:
            error_msg = (
                f"[CLIENT {self._session_id}] Attempted to call {method_name} on closed channel! "
                f"Server: {self.server_address}"
            )
            logger.error(error_msg)
            logger.error(
                f"[CLIENT {self._session_id}] Call stack:\n{''.join(traceback.format_stack())}"
            )
            raise RuntimeError(error_msg)

    def submit_sql(
        self,
        request: sql_service_models.SubmitEnrichedSQLRequest,
        request_id: t.Optional[str] = None,
    ) -> SQLSubmitResponse:
        """Submit SQL for query cache processing.

        Args:
            request: SubmitEnrichedSQLRequest
            request_id: Optional UUID string

        Returns:
            One of: ReadyToExecuteResponse, SkipExecutionResponse, or ReadyToCloneResponse

        Raises:
            grpc.RpcError: If the RPC fails
        """
        self._check_channel_state("submit_sql")

        metadata = [(REQUEST_ID_HEADER, request_id)] if request_id else None
        response = self.sql_stub.SubmitEnrichedSQL(
            request.to_proto(), timeout=self.timeout, metadata=metadata
        )

        # Extract the actual response from the oneof wrapper
        which = response.WhichOneof("response")
        if which == "ready_to_execute":
            return sql_service_models.ReadyToExecuteResponse.from_proto(response.ready_to_execute)
        if which == "skip_execution":
            return sql_service_models.SkipExecutionResponse.from_proto(response.skip_execution)
        if which == "ready_to_clone":
            return clone_service_models.ReadyToCloneResponse.from_proto(response.ready_to_clone)
        raise ValueError(f"Unexpected response type: {which}")

    def submit_sql_speculative(
        self,
        request: sql_service_models.SubmitEnrichedSQLRequest,
        request_id: t.Optional[str] = None,
    ) -> SpeculativeSubmitResponse:
        """Submit enriched SQL for a speculative cache decision using whatever
        dependency timestamps are currently available.

        Args:
            request: SubmitEnrichedSQLRequest
            request_id: Optional UUID string

        Returns:
            One of: ReadyToExecuteUntrackedResponse, SkipExecutionResponse,
            ReadyToCloneResponse, or UndecidedResponse

        Raises:
            grpc.RpcError: If the RPC fails
        """
        self._check_channel_state("submit_sql_speculative")

        metadata = [(REQUEST_ID_HEADER, request_id)] if request_id else None
        response = self.sql_stub.SubmitEnrichedSQLSpeculative(
            request.to_proto(), timeout=self.timeout, metadata=metadata
        )

        which = response.WhichOneof("response")
        if which == "ready_to_execute_untracked":
            return sql_service_models.ReadyToExecuteUntrackedResponse.from_proto(
                response.ready_to_execute_untracked
            )
        if which == "skip_execution":
            return sql_service_models.SkipExecutionResponse.from_proto(response.skip_execution)
        if which == "ready_to_clone":
            return clone_service_models.ReadyToCloneResponse.from_proto(response.ready_to_clone)
        if which == "undecided":
            return sql_service_models.UndecidedResponse.from_proto(response.undecided)
        raise ValueError(f"Unexpected response type: {which}")

    def submit_values(
        self,
        request: sql_service_models.SubmitValuesRequest,
        request_id: t.Optional[str] = None,
    ) -> t.Union[
        sql_service_models.ReadyToExecuteResponse,
        sql_service_models.SkipExecutionResponse,
        clone_service_models.ReadyToCloneResponse,
    ]:
        """Submit a pre-computed values hash for cache processing (e.g. seed models).

        Args:
            request: SubmitValuesRequest with target table and values hash
            request_id: Optional UUID string for request tracking

        Returns:
            One of: ReadyToExecuteResponse, SkipExecutionResponse, or ReadyToCloneResponse

        Raises:
            grpc.RpcError: If the RPC fails
        """
        self._check_channel_state("submit_values")

        metadata = [(REQUEST_ID_HEADER, request_id)] if request_id else None
        response = self.sql_stub.SubmitValues(
            request.to_proto(), timeout=self.timeout, metadata=metadata
        )

        which = response.WhichOneof("response")
        if which == "ready_to_execute":
            return sql_service_models.ReadyToExecuteResponse.from_proto(response.ready_to_execute)
        if which == "skip_execution":
            return sql_service_models.SkipExecutionResponse.from_proto(response.skip_execution)
        if which == "ready_to_clone":
            return clone_service_models.ReadyToCloneResponse.from_proto(response.ready_to_clone)
        raise ValueError(f"Unexpected response type: {which}")

    def register_clone(
        self, request: clone_service_models.CloneRequest
    ) -> t.Union[
        clone_service_models.ReadyToCloneResponse, clone_service_models.UnableToCloneResponse
    ]:
        """Attempts to register a clone table request.

        Args:
            request: CloneRequest with clone details

        Returns:
            Either ReadyToCloneResponse or UnableToCloneResponse

        Raises:
            grpc.RpcError: If the RPC fails
        """
        self._check_channel_state("register_clone")

        response = self.clone_stub.RegisterClone(request.to_proto(), timeout=self.timeout)

        # Can remove has field check once old services are deprecated
        if response.HasField("ready_to_clone"):
            return clone_service_models.ReadyToCloneResponse.from_proto(response.ready_to_clone)
        if response.HasField("unable_to_clone"):
            return clone_service_models.UnableToCloneResponse.from_proto(response.unable_to_clone)

        # Extract the actual response from the oneof wrapper
        which = response.WhichOneof("response")
        if which == "ready_to_clone_v1":
            return clone_service_models.ReadyToCloneResponse.from_proto(response.ready_to_clone_v1)

        raise ValueError(f"Unexpected response type: {which}")

    def confirm_execution(self, request: execution_service_models.ConfirmExecutionRequest) -> None:
        """Confirm that an execution has completed.

        Args:
            request: ConfirmExecutionRequest with execution details

        Raises:
            grpc.RpcError: If the RPC fails
        """
        self._check_channel_state("confirm_execution")

        self.execution_stub.ConfirmExecution(request.to_proto(), timeout=self.timeout)

    def record_executions(
        self, request: execution_service_models.RecordExecutionsRequest
    ) -> execution_service_models.RecordExecutionsResponse:
        """Bypass the cache flow and directly record executions that happened

        Args:
            request: RecordExecutionsRequest with a batch of ExecutionRecord's to write directly.
                each ExecutionRecord should record the outcome of either:
                    - SQLExecution (model execution), or
                    - ValuesExecution (seed execution)

        Raises:
            grpc.RpcError: If the RPC fails
        """
        self._check_channel_state("record_executions")

        response = self.execution_stub.RecordExecutions(request.to_proto(), timeout=self.timeout)

        return execution_service_models.RecordExecutionsResponse.from_proto(response)

    def is_client_version_supported(self) -> bool:
        """Check whether the current client version is supported by the server.

        Returns:
            True if the server considers this version supported, False otherwise.

        Raises:
            grpc.RpcError: If the RPC fails.
        """
        self._check_channel_state("is_client_version_supported")
        request = client_validation_service_models.ValidateClientVersionRequest(
            dbt_run_cache_version=__version__
        )
        response = self.client_validation_stub.ValidateClientVersion(
            request.to_proto(), timeout=self.timeout
        )
        return client_validation_service_models.ValidateClientVersionResponse.from_proto(
            response
        ).is_supported

    def get_explain_messages(
        self, request: explain_service_models.GetExplainMessagesRequest
    ) -> explain_service_models.GetExplainMessagesResponse:
        self._check_channel_state("get_explain_messages")
        response = self.explain_stub.GetExplainMessages(request.to_proto(), timeout=self.timeout)
        return explain_service_models.GetExplainMessagesResponse.from_proto(response)

    def close(self) -> None:
        """Close the gRPC channel."""
        if self._is_closed:
            logger.warning(f"[CLIENT {self._session_id}] close() called but already closed")
            return

        self._is_closed = True
        self.channel.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: t.Optional[type[BaseException]],
        exc_val: t.Optional[BaseException],
        exc_tb: t.Optional[TracebackType],
    ) -> None:
        self.close()


def _get_root_certificates() -> t.Optional[bytes]:
    """Load root CA certificates for gRPC TLS connections.

    Resolution order:
    1. RUN_CACHE_CA_BUNDLE environment variable (explicit file path)
    2. macOS Keychain certificates (on Darwin)
    3. System certificate store via ssl.create_default_context()
    4. None (falls back to gRPC's built-in certificates)
    """
    cert_path = get_env("CA_BUNDLE")
    if cert_path:
        try:
            with open(cert_path, "rb") as cert_file:
                return cert_file.read()
        except Exception as e:
            raise CertificateError(f"Failed to read CA bundle from {cert_path}: {e}")

    return _get_system_certificates()


def _get_system_certificates() -> t.Optional[bytes]:
    """Load CA certificates from the OS certificate store.

    On macOS, Python's bundled OpenSSL does not read from the system Keychain,
    so corporate or custom CAs installed there are invisible to
    ``ssl.create_default_context()``. We export them directly via the
    ``security`` CLI instead.
    """
    if sys.platform == "darwin":
        certs = _get_macos_keychain_certificates()
        if certs:
            return certs

    import ssl

    try:
        ctx = ssl.create_default_context()
        der_certs = ctx.get_ca_certs(binary_form=True)
        if not der_certs:
            return None
        return b"".join(ssl.DER_cert_to_PEM_cert(c).encode() for c in der_certs)
    except Exception:
        events.fire_debug_event("Failed to load system certificates, falling back to gRPC defaults")
        return None


def _get_macos_keychain_certificates() -> t.Optional[bytes]:
    """Export trusted CA certificates from macOS Keychains."""
    import subprocess

    try:
        result = subprocess.run(
            [
                "security",
                "find-certificate",
                "-a",
                "-p",
                "/System/Library/Keychains/SystemRootCertificates.keychain",
                "/Library/Keychains/System.keychain",
            ],
            capture_output=True,
        )
        if result.returncode == 0 and result.stdout:
            events.fire_debug_event("Loaded CA certificates from macOS Keychain")
            return result.stdout
        return None
    except Exception:
        events.fire_debug_event("Failed to export macOS Keychain certificates")
        return None
