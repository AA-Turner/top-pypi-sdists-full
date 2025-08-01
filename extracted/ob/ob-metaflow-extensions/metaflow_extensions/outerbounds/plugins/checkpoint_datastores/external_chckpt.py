from metaflow.user_decorators.user_flow_decorator import FlowMutator
from metaflow.user_decorators.mutable_flow import MutableFlow
from metaflow.user_decorators.mutable_step import MutableStep
import os


class _ExternalCheckpointFlowDeco(FlowMutator):
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
        if self.secrets is None:
            raise ValueError(
                "`secrets` keyword argument is required for the coreweave_datastore"
            )

    def _swap_secrets(self, mutable_flow: MutableFlow) -> None:
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
            for d in step.decorator_specs:
                name, _, _, deco_kwargs = d
                if name in swapping_decos:
                    decos_to_add.append((name, deco_kwargs))
                elif name == "secrets":
                    already_has_secrets = True
                    secrets_present_in_deco.extend(deco_kwargs["sources"])

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
                    deco_kwargs=dict(
                        sources=secrets_to_add,
                    ),
                )
                return

            for d, _ in decos_to_add:
                step.remove_decorator(d)

            step.add_decorator(
                secrets,
                deco_kwargs=dict(
                    sources=secrets_to_add,
                ),
            )
            for d, attrs in decos_to_add:
                _deco_to_add = swapping_decos[d]
                step.add_decorator(_deco_to_add, deco_kwargs=attrs)

        for step_name, step in mutable_flow.steps:
            _add_secrets(step)
