from metaflow.user_decorators.mutable_flow import MutableFlow
from .external_chckpt import _ExternalCheckpointFlowDeco
import os

NEBIUS_ENDPOINT_URL = "https://storage.eu-north1.nebius.cloud:443"


class nebius_checkpoints(_ExternalCheckpointFlowDeco):

    """

    This decorator is used for setting the nebius's S3 compatible object store as the artifact store for
    checkpoints/models created by the flow.

    Parameters
    ----------
    secrets: list
        A list of secrets to be added to the step. These secrets should contain any secrets that are required globally and the secret
        for the nebius object store. The secret should contain the following keys:
        - NEBIUS_ACCESS_KEY
        - NEBIUS_SECRET_KEY

    bucket_path: str
        The path to the bucket to store the checkpoints/models.

    endpoint_url: str
        The endpoint url for the nebius object store. Defaults to `https://storage.eu-north1.nebius.cloud:443`

    Usage
    -----
    ```python
    from metaflow import checkpoint, step, FlowSpec, nebius_checkpoints

    @nebius_checkpoints(secrets=[], bucket_path=None)
    class MyFlow(FlowSpec):
        @checkpoint
        @step
        def start(self):
            # Saves the checkpoint in the nebius object store
            current.checkpoint.save("./foo.txt")

        @step
        def end(self):
            pass
    ```
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def init(self, *args, **kwargs):
        super().init(*args, **kwargs)
        self.nebius_endpoint_url = kwargs.get("endpoint_url", NEBIUS_ENDPOINT_URL)

    def pre_mutate(self, mutable_flow: MutableFlow) -> None:
        from metaflow import (
            with_artifact_store,
        )

        def _nebius_config():
            return {
                "root": self.bucket_path,
                "client_params": {
                    "aws_access_key_id": os.environ.get("NEBIUS_ACCESS_KEY"),
                    "aws_secret_access_key": os.environ.get("NEBIUS_SECRET_KEY"),
                    "endpoint_url": self.nebius_endpoint_url,
                },
            }

        mutable_flow.add_decorator(
            with_artifact_store, deco_kwargs=dict(type="s3", config=_nebius_config)
        )
        self._swap_secrets(mutable_flow)
