from metaflow.user_configs.config_decorators import (
    MutableFlow,
    MutableStep,
    CustomFlowDecorator,
)
import os


class coreweave_checkpoints(CustomFlowDecorator):

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
        self.bucket_path = kwargs.get("bucket_path", None)

        self.secrets = kwargs.get("secrets", [])
        if self.bucket_path is None:
            raise ValueError(
                "`bucket_path` keyword argument is required for the coreweave_datastore"
            )
        if not self.bucket_path.startswith("s3://"):
            raise ValueError(
                "`bucket_path` must start with `s3://` for the coreweave_datastore"
            )

        self.coreweave_endpoint_url = f"https://cwobject.com"
        if self.secrets is None:
            raise ValueError(
                "`secrets` keyword argument is required for the coreweave_datastore"
            )

    def evaluate(self, mutable_flow: MutableFlow) -> None:
        from metaflow import (
            checkpoint,
            model,
            huggingface_hub,
            secrets,
            with_artifact_store,
        )

        def _add_secrets(step: MutableStep) -> None:
            decos_to_add = []
            swapping_decos = {
                "huggingface_hub": huggingface_hub,
                "model": model,
                "checkpoint": checkpoint,
            }
            already_has_secrets = False
            secrets_present_in_deco = []
            for d in step.decorators:
                if d.name in swapping_decos:
                    decos_to_add.append((d.name, d.attributes))
                elif d.name == "secrets":
                    already_has_secrets = True
                    secrets_present_in_deco.extend(d.attributes["sources"])

            # If the step aleady has secrets then take all the sources in
            # the secrets and add the addtional secrets to the existing secrets
            secrets_to_add = self.secrets
            if already_has_secrets:
                secrets_to_add.extend(secrets_present_in_deco)

            secrets_to_add = list(set(secrets_to_add))

            if len(decos_to_add) == 0:
                if already_has_secrets:
                    step.remove_decorator("secrets")

                step.add_decorator(
                    secrets,
                    sources=secrets_to_add,
                )
                return

            for d, _ in decos_to_add:
                step.remove_decorator(d)

            step.add_decorator(
                secrets,
                sources=secrets_to_add,
            )
            for d, attrs in decos_to_add:
                _deco_to_add = swapping_decos[d]
                step.add_decorator(_deco_to_add, **attrs)

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
            type="coreweave",
            config=_coreweave_config,
        )

        for step_name, step in mutable_flow.steps:
            _add_secrets(step)
