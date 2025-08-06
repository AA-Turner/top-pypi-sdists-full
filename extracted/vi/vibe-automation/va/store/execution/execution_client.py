from dotenv import load_dotenv
import grpc
import os
import logging

load_dotenv(".env.dev")

logger = logging.getLogger(__name__)


class ExecutionClient:
    """Singleton Execution client for API calls (e.g, requesting review) to Execution engine"""

    _instance = None

    def __init__(self):
        if ExecutionClient._instance is not None:
            raise RuntimeError(
                "ExecutionClient is a singleton. Use ExecutionClient.get_instance() instead."
            )
        # Initialize base_url and client_id from environment variables
        self.base_url = os.getenv("ORBY_BASE_URL")
        if not self.base_url:
            logger.error("Environment variable for Orby missing")
            raise
        self._grpc_channel = None
        self._setup_grpc_channel()

    @classmethod
    def get_instance(cls) -> "ExecutionClient":
        """Get the singleton instance of OrbyClient"""
        if cls._instance is None:
            instance = cls.__new__(cls)
            instance.__init__()
            cls._instance = instance
        return cls._instance

    def _setup_grpc_channel(self):
        """Setup gRPC channel for all gRPC calls"""
        try:
            grpc_address = self.base_url.replace("https://", "")
            logger.info(f"Setting up gRPC channel: {grpc_address}")

            credentials = grpc.ssl_channel_credentials()
            self._grpc_channel = grpc.secure_channel(grpc_address, credentials)

        except Exception as e:
            logger.warning(f"Warning: Could not setup gRPC channel: {e}")
            self._grpc_channel = None

    def call_grpc_channel(
        self, stub_method, request, metadata: list[tuple[str, str]] | None = None
    ):
        """Helper to call any gRPC method"""
        if not self._grpc_channel:
            raise RuntimeError("gRPC channel not available")

        try:
            # Pass along metadata (e.g. org_id) when provided.
            if metadata:
                response = stub_method(request, metadata=metadata)
            else:
                response = stub_method(request)
            return response
        except grpc.RpcError as e:
            logger.error(f"gRPC call failed: {e.code()} - {e.details()}")
            raise
        except Exception as e:
            logger.exception(f"Unexpected error during gRPC call: {e}")
            raise


# Convenience function to get the singleton instance
def get_execution_client() -> ExecutionClient:
    """Get the OrbyClient singleton instance"""
    return ExecutionClient.get_instance()
