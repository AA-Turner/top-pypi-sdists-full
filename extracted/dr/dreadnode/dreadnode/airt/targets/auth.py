"""HTTP authentication strategies.

Each auth mode reads its credential/identity from the environment or the platform's
credential chain — never from the spec. Provider SDKs (boto3, azure-identity,
google-auth) are imported dynamically so they stay off the SDK's hard-dependency set.
"""

import importlib
import os

from dreadnode.airt.targets.spec import TargetSpec


def apply_auth(
    spec: TargetSpec, headers: dict[str, str], url: str, content: bytes
) -> dict[str, str]:
    """Return the request headers with the spec's auth applied.

    For ``aws_sigv4`` the returned dict is the fully signed header set (which depends on
    ``url`` and ``content``); every other mode just adds an authorization header.
    """
    auth = spec.auth
    headers = dict(headers)
    if auth.type == "api_key":
        headers[auth.header] = auth.value_prefix + os.environ.get(auth.env_var, "")
    elif auth.type == "bearer":
        headers["Authorization"] = "Bearer " + os.environ.get(auth.env_var, "")
    elif auth.type == "azure_ad":
        headers["Authorization"] = "Bearer " + azure_ad_token(auth.scope)
    elif auth.type == "gcp":
        headers["Authorization"] = "Bearer " + gcp_token(auth.scope)
    elif auth.type == "aws_sigv4":
        headers = sign_sigv4(url, content, headers, auth.region, auth.service)
    return headers


def sign_sigv4(
    url: str, body: bytes, headers: dict[str, str], region: str, service: str
) -> dict[str, str]:
    """Sign a POST with AWS SigV4 using the default credential chain (env/profile/role)."""
    boto3 = importlib.import_module("boto3")
    sigv4_auth = importlib.import_module("botocore.auth").SigV4Auth
    aws_request = importlib.import_module("botocore.awsrequest").AWSRequest

    creds = boto3.Session().get_credentials()
    if creds is None:
        raise RuntimeError("aws_sigv4 auth requires AWS credentials (env vars, profile, or role)")
    req = aws_request(method="POST", url=url, data=body, headers=headers)
    sigv4_auth(creds.get_frozen_credentials(), service, region).add_auth(req)
    return dict(req.headers)


def azure_ad_token(scope: str) -> str:
    """Acquire an Entra token via DefaultAzureCredential (managed identity, workload
    identity, env creds, or ``az login`` — in that precedence)."""
    default_azure_credential = importlib.import_module("azure.identity").DefaultAzureCredential

    return default_azure_credential().get_token(scope).token


def gcp_token(scope: str) -> str:
    """Acquire a token via Google Application Default Credentials (service account,
    workload identity, or ``gcloud`` login)."""
    google_auth = importlib.import_module("google.auth")
    request_cls = importlib.import_module("google.auth.transport.requests").Request

    scopes = (
        [scope]
        if scope and scope.startswith("http")
        else ["https://www.googleapis.com/auth/cloud-platform"]
    )
    creds, _ = google_auth.default(scopes=scopes)
    creds.refresh(request_cls())
    return creds.token
