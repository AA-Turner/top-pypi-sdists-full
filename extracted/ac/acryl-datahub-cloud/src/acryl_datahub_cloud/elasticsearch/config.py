import os
from typing import Optional

import pydantic

from datahub.configuration import ConfigModel


def _env_true(name: str) -> bool:
    return os.getenv(name, "").lower() == "true"


class ElasticSearchClientConfig(ConfigModel):
    host: str = os.getenv("ELASTICSEARCH_HOST", "localhost")
    port: int = int(os.getenv("ELASTICSEARCH_PORT", "9200"))
    use_ssl: bool = _env_true("ELASTICSEARCH_USE_SSL")
    verify_certs: bool = False
    ca_certs: Optional[str] = None
    client_cert: Optional[str] = None
    client_key: Optional[str] = None
    username: Optional[str] = os.getenv("ELASTICSEARCH_USERNAME", "admin")
    password: Optional[str] = os.getenv("ELASTICSEARCH_PASSWORD", "admin")
    index_prefix: str = os.getenv("INDEX_PREFIX", "")
    opensearch_dialect: bool = False

    # AWS IAM (SigV4) auth for managed OpenSearch domains. On IAM-auth domains
    # the Helm chart withholds ELASTICSEARCH_PASSWORD (it only sets a dummy
    # ELASTICSEARCH_AUTH_HEADER to trigger the Java clients' SigV4 path), so
    # basic auth here falls back to the bogus "admin" default and 401s. When
    # use_iam_auth is set we instead sign requests with the pod's ambient AWS
    # credentials (IRSA / instance role) — the same identity the chart maps into
    # the domain's fine-grained access control via createUserIamRoleArn.
    #
    # Auto-detected from ELASTICSEARCH_AUTH_HEADER (set by the chart exactly when
    # IAM is enabled) so no extra per-instance config is needed; ELASTICSEARCH_USE_IAM
    # is an explicit override. When set, this selects the signed OpenSearch client
    # regardless of opensearch_dialect (SigV4 only applies to AWS OpenSearch).
    use_iam_auth: bool = _env_true("ELASTICSEARCH_USE_IAM") or bool(
        os.getenv("ELASTICSEARCH_AUTH_HEADER")
    )
    # Region for SigV4 signing. Defaults to the pod's AWS region env vars.
    aws_region: Optional[str] = os.getenv("AWS_REGION") or os.getenv(
        "AWS_DEFAULT_REGION"
    )
    # AWS service name for signing: "es" for managed OpenSearch domains,
    # "aoss" for OpenSearch Serverless.
    aws_service: str = "es"

    @pydantic.validator("index_prefix", always=True)
    def index_prefix_must_end_with_underscore_if_not_empty(cls, v: str) -> str:
        if v and not v.endswith("_"):
            return f"{v}_"
        return v

    @property
    def endpoint(self) -> str:
        if self.host and not self.port:
            return f"{self.host}"
        elif self.host:
            return f"{self.host}:{self.port}"
        else:
            raise ValueError("ElasticSearch host must be provided.")
