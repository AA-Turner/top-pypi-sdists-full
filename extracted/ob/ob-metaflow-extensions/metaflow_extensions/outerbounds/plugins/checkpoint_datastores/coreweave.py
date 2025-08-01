from metaflow.user_decorators.user_flow_decorator import FlowMutator
from metaflow.user_decorators.mutable_flow import MutableFlow
from metaflow.user_decorators.mutable_step import MutableStep
from .external_chckpt import _ExternalCheckpointFlowDeco
import os


class coreweave_checkpoints(_ExternalCheckpointFlowDeco):

    """

    This decorator is used for setting the coreweave object store as the artifact store for checkpoints/models created by the flow.

    Parameters
    ----------
    secrets: list
        A list of secrets to be added to the step. These secrets should contain any secrets that are required globally and the secret
        for the coreweave object store. The secret should contain the following keys:
        - COREWEAVE_ACCESS_KEY
        - COREWEAVE_SECRET_KEY

    bucket_path: str
        The path to the bucket to store the checkpoints/models.

    Usage
    -----
    ```python
    from metaflow import checkpoint, step, FlowSpec, coreweave_checkpoints

    @coreweave_checkpoints(secrets=[], bucket_path=None)
    class MyFlow(FlowSpec):
        @checkpoint
        @step
        def start(self):
            # Saves the checkpoint in the coreweave object store
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
        self.coreweave_endpoint_url = f"https://cwobject.com"

    def pre_mutate(self, mutable_flow: MutableFlow) -> None:
        from metaflow import (
            with_artifact_store,
        )

        def _coreweave_config():
            return {
                "root": self.bucket_path,
                "client_params": {
                    "aws_access_key_id": os.environ.get("COREWEAVE_ACCESS_KEY"),
                    "aws_secret_access_key": os.environ.get("COREWEAVE_SECRET_KEY"),
                    "endpoint_url": self.coreweave_endpoint_url,
                    "config": dict(s3={"addressing_style": "virtual"}),
                },
            }

        mutable_flow.add_decorator(
            with_artifact_store,
            deco_kwargs=dict(type="coreweave", config=_coreweave_config),
        )
        self._swap_secrets(mutable_flow)
