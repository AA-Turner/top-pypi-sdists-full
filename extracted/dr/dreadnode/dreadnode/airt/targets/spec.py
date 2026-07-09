"""Declarative target and auth models."""

import typing as t

from pydantic import BaseModel, Field

Transport = t.Literal["http", "streaming"]
AuthType = t.Literal["none", "api_key", "bearer", "aws_sigv4", "azure_ad", "gcp"]


class TargetAuth(BaseModel):
    """How to authenticate to the target. Secrets/identities come from the environment
    (env vars, cloud instance identity, or the local credential chain) — never inline.

    - ``api_key`` / ``bearer`` — static credential from ``env_var``.
    - ``aws_sigv4`` — SigV4 request signing via the AWS credential chain (env / profile /
      IAM role), for Bedrock / SageMaker.
    - ``azure_ad`` — an Entra token from ``azure.identity.DefaultAzureCredential`` (covers
      **managed identity**, workload identity, ``az login``, env creds), for Azure ML / AI
      Foundry / Azure OpenAI. Auto-acquired and refreshed — no static token to expire.
    - ``gcp`` — a token from Google Application Default Credentials (service account /
      workload identity / ``gcloud`` login), for Vertex AI.
    """

    type: AuthType = "none"
    #: Env var holding the credential (api_key / bearer token). Not used for cloud identities.
    env_var: str = "TARGET_API_KEY"
    #: Header name for ``api_key`` auth (e.g. ``api-key`` for Azure, ``X-API-Key``).
    header: str = "Authorization"
    #: For ``api_key``: a prefix prepended to the value (e.g. ``"Bearer "``). Empty by default.
    value_prefix: str = ""
    #: AWS region for ``aws_sigv4`` signing.
    region: str = "us-east-1"
    #: AWS service name for ``aws_sigv4`` (e.g. ``sagemaker``, ``bedrock``).
    service: str = "sagemaker"
    #: OAuth scope for ``azure_ad`` / ``gcp`` token acquisition.
    scope: str = "https://cognitiveservices.azure.com/.default"


class TargetSpec(BaseModel):
    """Declarative description of a custom target → build a ``@task`` with
    :func:`dreadnode.airt.targets.build_target`."""

    transport: Transport = "http"
    #: HTTP endpoint URL, or (for streaming) the region/identifier the adapter needs.
    endpoint: str
    #: Streaming protocol adapter to use when ``transport == "streaming"``.
    protocol: t.Literal["nova_sonic"] | None = None
    auth: TargetAuth = Field(default_factory=TargetAuth)
    #: JSON request body template with ``{prompt}``/``{image_b64}``/``{audio_b64}``/``{video_b64}``.
    request_template: str = '{"prompt": "{prompt}"}'
    #: JSONPath (jsonpath_ng) to the response text.
    response_text_path: str = "$.response"
    timeout_s: float = 120.0
    name: str = "custom_target"
    #: Free-form options passed to a streaming adapter (voice, system_prompt, model_id, ...).
    options: dict[str, t.Any] = Field(default_factory=dict)
