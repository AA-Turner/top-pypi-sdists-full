import shlex
from dataclasses import dataclass
from typing import List, Optional, Union

from flytekit.core.artifact import ArtifactQuery
from flytekit.core.pod_template import PodTemplate

from union import ImageSpec
from union.app import App, Input

FLASH_INFER_INDEX_URL = "https://flashinfer.ai/whl/cu124/torch2.5"
DEFAULT_SGLANG_IMAGE = "ghcr.io/unionai/serving-sglang:py3.12-latest"
OPTIMIZED_SGLANG_IMAGE = "managed.cr.union.ai/sglang:stable"


@dataclass
class SGLangApp(App):
    """
    App backed by FastAPI.

    :param name: The name of the application.
    :param container_image: The container image to use for the application.
    :param args: Entrypoint to start application.
    :param command: Command to start application.
    :param port: Port application listens to.
    :param requests: Compute resource requests for application.
    :param secrets: Secrets that are requested for application.
    :param limits: Compute resource limits for application.
    :param include: Files to include for your application.
    :param inputs: Inputs for the application.
    :param env: Environment variables to set for the application.
    :param min_replicas: Minimum number of replicas (ignore if autoscaling is set).
    :param max_replicas: Maximum number of replicas (ignore if autoscaling is set).
    :param scaledown_after: Time to wait before scaling down a replica after it has been idle.
    :param scaling_metric: Autoscale based on a parameter, e.g. request rate or concurrency
      (others may be added in the future).
    :param cluster_pool: The target cluster_pool where the app should be deployed.
    :param requires_auth: Public URL does not require any authentication
    :param type: Type of app
    :param description: Description of app
    :param subdomain: Custom subdomain for your app.
    :param custom_domain: Custom full domain for your app.
    :param extra_args: Extra args to pass to `python -m sglang.launch_server`. See
        https://docs.sglang.ai/backend/server_arguments.html for details.
    :param model: Artifact URI for model.
        - If `str`, it should start with `flyte://`.
        - Use `ArtifactQuery` to dynamically query an artifact.
    :param model_id: model id that is exposed by vllm.
    :param stream_model: Set to True to stream model from blob store to the GPU directly.
      If False, the model will be downloaded to the local file system first and then loaded
      into the GPU.
    """

    port: int = 8000
    type: str = "SGLang"
    container_image: Optional[Union[str, ImageSpec, PodTemplate]] = None
    extra_args: Union[str, List[str]] = ""
    model: Union[str, ArtifactQuery] = ""
    model_id: str = ""
    stream_model: bool = True

    def __post_init__(self):
        if self.model_id == "":
            raise ValueError("model_id must be defined")

        if self.args:
            raise ValueError("args can not be set for SGLangApp. Use `extra_args` to add extra arguments to SGLang")

        if isinstance(self.extra_args, str):
            extra_args = shlex.split(self.extra_args)
        else:
            extra_args = self.extra_args

        self.args = [
            "union-model-loader-sglang",
            "--model-path",
            "/root/union",
            "--served-model-name",
            self.model_id,
            "--port",
            str(self.port),
            *extra_args,
        ]

        if self.inputs:
            raise ValueError("inputs can not be set for SGLangApp")

        if isinstance(self.model, str):
            input_type = Input.Type._ArtifactUri
        elif isinstance(self.model, ArtifactQuery):
            input_type = None
        else:
            msg = "model must be a string or ArtifactQuery"
            raise TypeError(msg)

        if self.container_image is None:
            self.container_image = DEFAULT_SGLANG_IMAGE
        elif isinstance(self.container_image, ImageSpec):
            # NOTE: the flashinfer index url has to be included because the
            # union builder fails to install the nvidia drivers needed to
            # install flashinfer.
            if (
                self.container_image.pip_extra_index_url
                and FLASH_INFER_INDEX_URL not in self.container_image.pip_extra_index_url
            ):
                self.container_image.pip_extra_index_url.append(FLASH_INFER_INDEX_URL)
            elif self.container_image.pip_extra_index_url is None:
                self.container_image.pip_extra_index_url = [FLASH_INFER_INDEX_URL]

        input_kwargs = {}
        if self.stream_model:
            self.env["UNION_MODEL_LOADER_STREAM_SAFETENSORS"] = "true"
            input_kwargs["env_var"] = "UNION_MODEL_LOADER_REMOTE_MODEL_PATH"
            input_kwargs["download"] = False
        else:
            self.env["UNION_MODEL_LOADER_STREAM_SAFETENSORS"] = "false"
            input_kwargs["download"] = True
            input_kwargs["mount"] = "/root/union"

        self.inputs = [Input(name="model", value=self.model, type=input_type, **input_kwargs)]

        self.env["UNION_MODEL_LOADER_LOCAL_MODEL_PATH"] = "/root/union"

        super().__post_init__()
