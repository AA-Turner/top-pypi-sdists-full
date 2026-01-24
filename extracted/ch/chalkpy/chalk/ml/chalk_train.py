from typing import Any, Dict, List, Optional, Protocol

from chalk.client.client_grpc import ChalkGRPCClient
from chalk.client.exc import ChalkAuthException
from chalk.client.models import RegisterModelArtifactResponse
from chalk.config.auth_config import load_token
from chalk.ml.utils import MODEL_TRAIN_METADATA_RUN_NAME, get_model_metadata_run_name_from_env


class Checkpointer(Protocol):
    def checkpoint(
        self,
        model: Any,
        additional_files: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        run_name: Optional[str] = None,
    ) -> RegisterModelArtifactResponse:
        ...


class ClientCheckpointer:
    def __init__(self):
        self._client: Optional[ChalkGRPCClient] = None
        super().__init__()

    def _get_client(self) -> ChalkGRPCClient:
        if self._client is None:
            token = load_token(client_id=None, client_secret=None, active_environment=None, api_server=None)

            if token is None:
                raise ChalkAuthException()

            self._client = ChalkGRPCClient(
                client_id=token.clientId,
                client_secret=token.clientSecret,
                environment=token.activeEnvironment,
                api_server=token.apiServer,
            )
        return self._client

    def checkpoint(
        self,
        model: Any,
        additional_files: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        run_name: Optional[str] = None,
    ) -> RegisterModelArtifactResponse:
        client = self._get_client()

        if metadata is None:
            metadata = {}
        metadata[MODEL_TRAIN_METADATA_RUN_NAME] = run_name if run_name else get_model_metadata_run_name_from_env()

        return client._upload_model_artifact(  # pyright: ignore[reportPrivateUsage]
            model=model, additional_files=additional_files, metadata=metadata
        )


CheckpointClass: Checkpointer = ClientCheckpointer()


def checkpoint(
    model: Any,
    additional_files: Optional[List[str]] = None,
    metadata: Optional[Dict[str, Any]] = None,
    run_name: Optional[str] = None,
) -> RegisterModelArtifactResponse:
    return CheckpointClass.checkpoint(
        model=model, additional_files=additional_files, metadata=metadata, run_name=run_name
    )
