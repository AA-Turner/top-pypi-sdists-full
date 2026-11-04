"""What a GPU client needs to know: the provider's key, the bucket, the limits.

A plain model, not environment-bound: a world receives it inside its launch
config (the platform fills the secrets with ``${VAR}`` placeholders Chronos
resolves at launch), a person builds it from the environment with
:meth:`GpuSettings.from_env`.
"""

from __future__ import annotations

import os

from pydantic import BaseModel, Field


class GpuSettings(BaseModel):
    """Credentials and limits for one GPU provider and one bucket."""

    provider: str = Field(default="runpod", description="The provider's name; runpod is the only one today")
    # The private bucket scenes, frames, pod assets and recordings move
    # through: every grant handed to a worker or a pod is one presigned URL
    # on it, so no machine ever holds these credentials.
    bucket: str = ""
    region: str = "us-west-2"
    # AWS credentials for the bucket. Empty = boto3's default chain (a
    # person's profile); a world gets explicit ones for the bucket alone.
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_session_token: str = ""
    # Runpod.
    runpod_api_key: str = ""
    runpod_rest_url: str = "https://rest.runpod.io/v1"
    runpod_api_url: str = "https://api.runpod.ai/v2"
    # The serverless endpoint that renders .blend files (sims/gpu-box-runpod).
    runpod_render_endpoint_id: str = ""
    # A registry credential stored at Runpod (POST /containerregistryauth):
    # pods pull private images with it. Empty = public images only.
    runpod_registry_auth_id: str = ""
    # A pod with no MCP call for this long ends itself, in case its owner
    # never does.
    pod_idle_minutes: int = 20
    # Whether pods may be created at all: a whole machine billed by the hour
    # is handed out more carefully than a serverless job.
    pods_allowed: bool = False

    @property
    def renders_configured(self) -> bool:
        return bool(self.bucket and self.runpod_api_key and self.runpod_render_endpoint_id)

    @property
    def pods_configured(self) -> bool:
        return bool(self.bucket and self.runpod_api_key)

    @classmethod
    def from_env(cls, environ: dict[str, str] | None = None) -> GpuSettings:
        """Settings from ``PLATO_GPU_*`` (``PLATO_GPU_BUCKET``,
        ``PLATO_GPU_REGION``, ``PLATO_GPU_PODS_ALLOWED``, ...) with the
        provider's own names (``RUNPOD_API_KEY``, ``RUNPOD_RENDER_ENDPOINT_ID``)
        and ``AWS_*`` as fallbacks."""

        env = os.environ if environ is None else environ

        def read(name: str, *fallbacks: str, default: str = "") -> str:
            for key in (f"PLATO_GPU_{name}", *fallbacks):
                value = env.get(key, "")
                if value:
                    return value
            return default

        return cls(
            provider=read("PROVIDER", default="runpod"),
            bucket=read("BUCKET", "GPU_BOX_BUCKET"),
            region=read("REGION", default="us-west-2"),
            aws_access_key_id=read("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=read("AWS_SECRET_ACCESS_KEY"),
            aws_session_token=read("AWS_SESSION_TOKEN"),
            runpod_api_key=read("RUNPOD_API_KEY", "RUNPOD_API_KEY"),
            runpod_rest_url=read("RUNPOD_REST_URL", default="https://rest.runpod.io/v1"),
            runpod_api_url=read("RUNPOD_API_URL", default="https://api.runpod.ai/v2"),
            runpod_render_endpoint_id=read(
                "RUNPOD_RENDER_ENDPOINT_ID", "RUNPOD_RENDER_ENDPOINT_ID", "RUNPOD_ENDPOINT_ID"
            ),
            runpod_registry_auth_id=read("RUNPOD_REGISTRY_AUTH_ID", "RUNPOD_REGISTRY_AUTH_ID"),
            pod_idle_minutes=int(read("POD_IDLE_MINUTES", default="20")),
            pods_allowed=read("PODS_ALLOWED", default="1").lower() in ("1", "true", "yes"),
        )
