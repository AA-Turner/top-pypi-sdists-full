from unittest import TestCase
from unittest import mock

from google.protobuf.empty_pb2 import Empty

from tecton._internals.metadata_service_impl.auth_lib import InternalAuthProvider
from tecton._internals.metadata_service_impl.request_lib import InternalRequestProvider
from tecton._internals.metadata_service_impl.service_modules import GRPC_SERVICE_MODULES
from tecton_core.errors import FailedPreconditionError
from tecton_core.errors import TectonAbortedError
from tecton_core.errors import TectonAlreadyExistsError
from tecton_core.errors import TectonAPIInaccessibleError
from tecton_core.errors import TectonAPIValidationError
from tecton_core.errors import TectonDeadlineExceededError
from tecton_core.errors import TectonNotFoundError
from tecton_core.errors import TectonNotImplementedError
from tecton_core.errors import TectonOperationCancelledError
from tecton_core.errors import TectonResourceExhaustedError
from tecton_core.metadata_service_impl import error_lib
from tecton_core.metadata_service_impl import http_client
from tecton_core.metadata_service_impl.service_calls import GrpcCall


@mock.patch(
    "tecton._internals.metadata_service_impl.request_lib.InternalRequestProvider.request_url",
    return_value="https://test.tecton.ai/api",
)
@mock.patch("tecton.identities.okta.get_token_refresh_if_needed", lambda: None)
class HttpClientTest(TestCase):
    @mock.patch("tecton_core.metadata_service_impl.http_client._InternalHTTPStub.execute")
    def test_valid_request(self, mock_execute, _):
        """
        Tests the translation of the PureHTTPStub Nop(proto) method to _InternalHTTPStub.execute('Nop', proto).
        """
        expected_grpc_call = GrpcCall(
            "/tecton_proto.metadataservice.MetadataService/Nop", Empty.SerializeToString, Empty.FromString
        )
        mock_execute.return_value = Empty()
        stub = http_client.PureHTTPStub(InternalRequestProvider(InternalAuthProvider()), GRPC_SERVICE_MODULES)
        response = stub.Nop(Empty())
        mock_execute.assert_called_once()
        mock_execute.assert_called_with(expected_grpc_call, Empty(), 300.0)
        assert response == Empty()

    @mock.patch("tecton_core.metadata_service_impl.http_client._InternalHTTPStub.execute")
    def test_timeout_param(self, mock_execute, _):
        """
        Test passing in a timeout to a method called on PureHTTPStub
        """
        expected_grpc_call = GrpcCall(
            "/tecton_proto.metadataservice.MetadataService/Nop", Empty.SerializeToString, Empty.FromString
        )
        mock_execute.return_value = Empty()
        stub = http_client.PureHTTPStub(InternalRequestProvider(InternalAuthProvider()), GRPC_SERVICE_MODULES)
        response = stub.Nop(Empty(), timeout_sec=5.0)
        mock_execute.assert_called_once()
        mock_execute.assert_called_with(expected_grpc_call, Empty(), 5.0)
        assert response == Empty()

    @mock.patch("tecton_core.metadata_service_impl.http_client._InternalHTTPStub.execute")
    def test_invalid_method(self, mock_execute, _):
        """
        Tests error handling of a method called on PureHTTPStub that doesn't map to a valid MetadataService method.
        """
        stub = http_client.PureHTTPStub(InternalRequestProvider(InternalAuthProvider()), GRPC_SERVICE_MODULES)
        with self.assertRaisesRegex(AttributeError, "Nonexistent MetadataService method: InvalidRequestName"):
            stub.InvalidRequestName(Empty())
        mock_execute.assert_not_called()

    @mock.patch("requests.Session.request")
    def test_unauthenticated_request(self, mock_request, _):
        """
        Test when unauthenticated status is returned
        """

        class FakeResponse:
            def raise_for_status(self):
                pass

            def json(self):
                return {"status": {"code": error_lib.gRPCStatus.UNAUTHENTICATED.value, "detail": "thedetail"}}

        mock_request.return_value = FakeResponse()
        stub = http_client.PureHTTPStub(InternalRequestProvider(InternalAuthProvider()), GRPC_SERVICE_MODULES)
        with self.assertRaises(PermissionError) as context:
            stub.Nop(Empty())
        assert "Tecton credentials are invalid, not configured, or expired" in str(context.exception)

    @mock.patch("requests.Session.request")
    def test_permission_denied_request(self, mock_request, _):
        """
        Test when permission denied (unauthorized) status is returned
        """

        class FakeResponse:
            def raise_for_status(self):
                pass

            def json(self):
                return {"status": {"code": error_lib.gRPCStatus.PERMISSION_DENIED.value, "detail": "thedetail"}}

        mock_request.return_value = FakeResponse()
        stub = http_client.PureHTTPStub(InternalRequestProvider(InternalAuthProvider()), GRPC_SERVICE_MODULES)
        with self.assertRaisesRegex(PermissionError, ".*Insufficient permissions.*"):
            stub.Nop(Empty())

    @mock.patch("requests.Session.request")
    def test_permission_denied_unauthenticated_request(self, mock_request, _):
        """
        Test when permission denied (unauthorized) status is returned
        """

        class FakeResponse:
            def raise_for_status(self):
                pass

            def json(self):
                return {
                    "status": {
                        "code": error_lib.gRPCStatus.PERMISSION_DENIED.value,
                        "detail": "UNAUTHENTICATED: InvalidToken",
                    }
                }

        mock_request.return_value = FakeResponse()
        stub = http_client.PureHTTPStub(InternalRequestProvider(InternalAuthProvider()), GRPC_SERVICE_MODULES)
        with self.assertRaisesRegex(PermissionError, ".*Insufficient permissions.*"):
            stub.Nop(Empty())

    # TODO: Remove with https://tecton.atlassian.net/browse/TEC-9107
    #  (once the metadata service no longer returns PERMISSION_DENIED when authentication is required but not included)
    @mock.patch("requests.Session.request")
    def test_permission_denied_no_header_request(self, mock_request, _):
        """
        Test when permission denied (unauthorized) status is returned
        """

        class FakeResponse:
            def raise_for_status(self):
                pass

            def json(self):
                return {"status": {"code": error_lib.gRPCStatus.PERMISSION_DENIED.value, "detail": "thedetail"}}

        mock_request.return_value = FakeResponse()
        stub = http_client.PureHTTPStub(InternalRequestProvider(InternalAuthProvider()), GRPC_SERVICE_MODULES)
        with self.assertRaisesRegex(PermissionError, ".*Insufficient permissions.*"):
            stub.Nop(Empty())

    @mock.patch("requests.Session.request")
    def test_cancelled_request(self, mock_request, _):
        """
        Test when a request is cancelled
        """

        class FakeResponse:
            def raise_for_status(self):
                pass

            def json(self):
                return {"status": {"code": error_lib.gRPCStatus.CANCELLED.value, "detail": "Operation cancelled"}}

        mock_request.return_value = FakeResponse()
        stub = http_client.PureHTTPStub(InternalRequestProvider(InternalAuthProvider()), GRPC_SERVICE_MODULES)
        with self.assertRaises(TectonOperationCancelledError) as context:
            stub.Nop(Empty())
        self.assertIn("Operation cancelled", str(context.exception))

    @mock.patch("requests.Session.request")
    def test_deadline_exceeded_request(self, mock_request, _):
        """
        Test when a request deadline is exceeded
        """

        class FakeResponse:
            def raise_for_status(self):
                pass

            def json(self):
                return {"status": {"code": error_lib.gRPCStatus.DEADLINE_EXCEEDED.value, "detail": "Deadline exceeded"}}

        mock_request.return_value = FakeResponse()
        stub = http_client.PureHTTPStub(InternalRequestProvider(InternalAuthProvider()), GRPC_SERVICE_MODULES)
        with self.assertRaises(TectonDeadlineExceededError) as context:
            stub.Nop(Empty())
        self.assertIn("Deadline exceeded", str(context.exception))

    @mock.patch("requests.Session.request")
    def test_already_exists_request(self, mock_request, _):
        """
        Test when a resource already exists
        """

        class FakeResponse:
            def raise_for_status(self):
                pass

            def json(self):
                return {
                    "status": {"code": error_lib.gRPCStatus.ALREADY_EXISTS.value, "detail": "Resource already exists"}
                }

        mock_request.return_value = FakeResponse()
        stub = http_client.PureHTTPStub(InternalRequestProvider(InternalAuthProvider()), GRPC_SERVICE_MODULES)
        with self.assertRaises(TectonAlreadyExistsError) as context:
            stub.Nop(Empty())
        self.assertIn("Resource already exists", str(context.exception))

    @mock.patch("requests.Session.request")
    def test_resource_exhausted_request(self, mock_request, _):
        """
        Test when a resource is exhausted
        """

        class FakeResponse:
            def raise_for_status(self):
                pass

            def json(self):
                return {
                    "status": {"code": error_lib.gRPCStatus.RESOURCE_EXHAUSTED.value, "detail": "Resource exhausted"}
                }

        mock_request.return_value = FakeResponse()
        stub = http_client.PureHTTPStub(InternalRequestProvider(InternalAuthProvider()), GRPC_SERVICE_MODULES)
        with self.assertRaises(TectonResourceExhaustedError) as context:
            stub.Nop(Empty())
        self.assertIn("Resource exhausted", str(context.exception))

    @mock.patch("requests.Session.request")
    def test_aborted_request(self, mock_request, _):
        """
        Test when a request is aborted
        """

        class FakeResponse:
            def raise_for_status(self):
                pass

            def json(self):
                return {"status": {"code": error_lib.gRPCStatus.ABORTED.value, "detail": "Operation aborted"}}

        mock_request.return_value = FakeResponse()
        stub = http_client.PureHTTPStub(InternalRequestProvider(InternalAuthProvider()), GRPC_SERVICE_MODULES)
        with self.assertRaises(TectonAbortedError) as context:
            stub.Nop(Empty())
        self.assertIn("Operation aborted", str(context.exception))

    @mock.patch("requests.Session.request")
    def test_out_of_range_request(self, mock_request, _):
        """
        Test when a value is out of range
        """

        class FakeResponse:
            def raise_for_status(self):
                pass

            def json(self):
                return {"status": {"code": error_lib.gRPCStatus.OUT_OF_RANGE.value, "detail": "Value out of range"}}

        mock_request.return_value = FakeResponse()
        stub = http_client.PureHTTPStub(InternalRequestProvider(InternalAuthProvider()), GRPC_SERVICE_MODULES)
        with self.assertRaises(TectonAPIValidationError) as context:
            stub.Nop(Empty())
        self.assertIn("Value out of range", str(context.exception))

    @mock.patch("requests.Session.request")
    def test_unavailable_request(self, mock_request, _):
        """
        Test when the API is unavailable
        """

        class FakeResponse:
            def raise_for_status(self):
                pass

            def json(self):
                return {"status": {"code": error_lib.gRPCStatus.UNAVAILABLE.value, "detail": "API unavailable"}}

        mock_request.return_value = FakeResponse()
        stub = http_client.PureHTTPStub(InternalRequestProvider(InternalAuthProvider()), GRPC_SERVICE_MODULES)
        with self.assertRaises(TectonAPIInaccessibleError) as context:
            stub.Nop(Empty())
        self.assertIn("API unavailable", str(context.exception))

    @mock.patch("requests.Session.request")
    def test_invalid_argument_request(self, mock_request, _):
        """
        Test when an invalid argument is provided
        """

        class FakeResponse:
            def raise_for_status(self):
                pass

            def json(self):
                return {"status": {"code": error_lib.gRPCStatus.INVALID_ARGUMENT.value, "detail": "Invalid argument"}}

        mock_request.return_value = FakeResponse()
        stub = http_client.PureHTTPStub(InternalRequestProvider(InternalAuthProvider()), GRPC_SERVICE_MODULES)
        with self.assertRaises(TectonAPIValidationError) as context:
            stub.Nop(Empty())
        self.assertIn("Invalid argument", str(context.exception))

    @mock.patch("requests.Session.request")
    def test_failed_precondition_request(self, mock_request, _):
        """
        Test when a precondition fails
        """

        class FakeResponse:
            def raise_for_status(self):
                pass

            def json(self):
                return {
                    "status": {"code": error_lib.gRPCStatus.FAILED_PRECONDITION.value, "detail": "Precondition failed"}
                }

        mock_request.return_value = FakeResponse()
        stub = http_client.PureHTTPStub(InternalRequestProvider(InternalAuthProvider()), GRPC_SERVICE_MODULES)
        with self.assertRaises(FailedPreconditionError) as context:
            stub.Nop(Empty())
        self.assertIn("Precondition failed", str(context.exception))

    @mock.patch("requests.Session.request")
    def test_not_found_request(self, mock_request, _):
        """
        Test when a resource is not found
        """

        class FakeResponse:
            def raise_for_status(self):
                pass

            def json(self):
                return {"status": {"code": error_lib.gRPCStatus.NOT_FOUND.value, "detail": "Resource not found"}}

        mock_request.return_value = FakeResponse()
        stub = http_client.PureHTTPStub(InternalRequestProvider(InternalAuthProvider()), GRPC_SERVICE_MODULES)
        with self.assertRaises(TectonNotFoundError) as context:
            stub.Nop(Empty())
        self.assertIn("Resource not found", str(context.exception))

    @mock.patch("requests.Session.request")
    def test_unimplemented_request(self, mock_request, _):
        """
        Test when a feature is not implemented
        """

        class FakeResponse:
            def raise_for_status(self):
                pass

            def json(self):
                return {
                    "status": {"code": error_lib.gRPCStatus.UNIMPLEMENTED.value, "detail": "Feature not implemented"}
                }

        mock_request.return_value = FakeResponse()
        stub = http_client.PureHTTPStub(InternalRequestProvider(InternalAuthProvider()), GRPC_SERVICE_MODULES)
        with self.assertRaises(TectonNotImplementedError) as context:
            stub.Nop(Empty())
        self.assertIn("Feature not implemented", str(context.exception))
