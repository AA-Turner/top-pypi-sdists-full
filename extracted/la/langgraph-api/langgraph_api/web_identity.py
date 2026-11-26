"""Keep LangSmith workload identity token files fresh so the AWS, Azure and Google SDKs can federate with them."""

import asyncio
import json
import os
import re
import shutil
import tempfile
import urllib.parse
from collections.abc import Awaitable, Callable, Sequence
from typing import Any, Protocol

import httpx
import structlog

from langgraph_api import agent_auth, config
from langgraph_api.asyncio import create_task

logger = structlog.stdlib.get_logger(__name__)

AWS_AUDIENCE = "sts.amazonaws.com/langsmith-agents"
AZURE_AUDIENCE = "api://AzureADTokenExchange/langsmith-agents"
GCP_AUDIENCE = "https://iam.googleapis.com/langsmith-agents"
_RETRY_SECONDS = 5.0
_MAX_RETRY_SECONDS = 60.0
_REQUEST_TIMEOUT_SECONDS = 10.0
_DEFAULT_TOKEN_LIFETIME_SECONDS = 300
# 408 and 429 ask the caller to retry, and a 404 can mean Agent Auth is mid-deploy. Every
# other 4xx, such as binding_not_found or a revoked key, is a refusal that fails startup.
_RETRYABLE_CLIENT_STATUSES = frozenset({404, 408, 429})


class WebIdentityConfigError(RuntimeError):
    """LangSmith refused the token for a reason only configuration can fix."""


def _write_atomically(path: str, token: str) -> None:
    fd, tmp_path = tempfile.mkstemp(dir=os.path.dirname(path), prefix=".token-")
    try:
        with os.fdopen(fd, "w") as f:
            f.write(token)
        os.replace(tmp_path, path)
    except BaseException:
        os.unlink(tmp_path)
        raise


def _ls_error(response: httpx.Response) -> str | None:
    try:
        body = response.json()
    except ValueError:
        return None
    value = body.get("ls_error") if isinstance(body, dict) else None
    return value if isinstance(value, str) else None


class Proof(Protocol):
    name: str

    async def request_token(
        self, client: httpx.AsyncClient, url: str, audience: str
    ) -> httpx.Response: ...


class DeploymentKey:
    name = "deployment_key"

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    async def request_token(
        self, client: httpx.AsyncClient, url: str, audience: str
    ) -> httpx.Response:
        return await client.post(
            url,
            data={"grant_type": "client_credentials", "resource": audience},
            headers={"X-Api-Key": self.api_key},
        )


class PodToken:
    name = "pod_token"

    async def request_token(
        self, client: httpx.AsyncClient, url: str, audience: str
    ) -> httpx.Response:
        return await client.post(url, data=await agent_auth.pod_token_form(audience))


class TokenFileRefresher:
    """Owns a private token file and the Agent Auth client that keeps it fresh until closed."""

    def __init__(
        self,
        url: str,
        proofs: Sequence[Proof],
        client: httpx.AsyncClient,
        audience: str,
    ):
        self.url = url
        self.proofs = list(proofs)
        self.client = client
        self.audience = audience
        self.path = os.path.join(
            tempfile.mkdtemp(prefix="langsmith-web-identity-"), "token"
        )
        self.failures = 0

    async def refresh(self) -> float:
        """Fetch and write a token, returning the delay before the next attempt."""
        try:
            response = await self.proofs[0].request_token(
                self.client, self.url, self.audience
            )
        except (httpx.HTTPError, OSError) as exc:
            return await self._failed(error=type(exc).__name__)
        if response.status_code != 200:
            ls_error = _ls_error(response)
            status = response.status_code
            if 400 <= status < 500 and status not in _RETRYABLE_CLIENT_STATUSES:
                if len(self.proofs) > 1:
                    return await self._refresh_with_the_next_proof(
                        ls_error or f"HTTP {status}"
                    )
                raise WebIdentityConfigError(
                    f"LangSmith refused the {self.audience} web identity token: "
                    f"{ls_error or f'HTTP {status}'}"
                )
            return await self._failed(status=response.status_code, ls_error=ls_error)
        try:
            body = response.json()
            token = body["access_token"]
            lifetime = int(body.get("expires_in") or _DEFAULT_TOKEN_LIFETIME_SECONDS)
            if not isinstance(token, str) or not token:
                raise ValueError("access_token is not a non-empty string")
        except (ValueError, KeyError, TypeError):
            return await self._failed(error="malformed token response")
        _write_atomically(self.path, token)
        if self.failures:
            await logger.ainfo(
                "Web identity token refreshed after failures", audience=self.audience
            )
        self.failures = 0
        return max(lifetime / 2, _RETRY_SECONDS)

    async def _refresh_with_the_next_proof(self, refusal: str) -> float:
        refused = self.proofs.pop(0)
        await logger.awarning(
            "LangSmith refused a web identity proof, so the next one is used",
            audience=self.audience,
            refused=refused.name,
            next=self.proofs[0].name,
            error=refusal,
        )
        return await self.refresh()

    async def _failed(
        self, log: Callable[..., Awaitable[Any]] | None = None, **fields: Any
    ) -> float:
        delay = min(_RETRY_SECONDS * 2 ** min(self.failures, 4), _MAX_RETRY_SECONDS)
        self.failures += 1
        await (log or logger.awarning)(
            "Failed to refresh web identity token",
            audience=self.audience,
            retry_in_seconds=delay,
            **fields,
        )
        return delay

    async def run(self, delay: float) -> None:
        """Refresh until cancelled, then close the client and remove the token file."""
        try:
            while True:
                await asyncio.sleep(delay)
                try:
                    delay = await self.refresh()
                except WebIdentityConfigError as exc:
                    # A refusal after startup may be temporary, so keep backing off.
                    delay = await self._failed(logger.aerror, error=str(exc))
                except Exception as exc:
                    # Raising would end the loop and leave the token to expire.
                    delay = await self._failed(error=str(exc), exc_info=exc)
        finally:
            await self.aclose()

    async def aclose(self) -> None:
        try:
            await self.client.aclose()
        finally:
            shutil.rmtree(os.path.dirname(self.path), ignore_errors=True)


async def start() -> list[asyncio.Task[None]]:
    """Start a token file for each configured cloud and return their running refresh loops."""
    role_arn = config.LANGSMITH_AWS_ROLE_ARN
    client_id = config.LANGSMITH_AZURE_CLIENT_ID
    tenant_id = config.LANGSMITH_AZURE_TENANT_ID
    provider = config.LANGSMITH_GCP_WORKLOAD_IDENTITY_PROVIDER
    service_account = config.LANGSMITH_GCP_SERVICE_ACCOUNT
    if not (role_arn or client_id or tenant_id or provider or service_account):
        return []
    # Check every cloud's settings before minting, so a typo fails startup instead of leaving a refresher behind.
    if bool(client_id) != bool(tenant_id):
        raise ValueError(
            "LANGSMITH_AZURE_CLIENT_ID and LANGSMITH_AZURE_TENANT_ID must both be set"
        )
    if provider and not re.fullmatch(
        r"//iam\.googleapis\.com/projects/[0-9]+/locations/[a-z0-9-]+/workloadIdentityPools/[a-z0-9-]+/providers/[a-z0-9-]+",
        provider,
    ):
        raise ValueError(
            "LANGSMITH_GCP_WORKLOAD_IDENTITY_PROVIDER must be "
            "//iam.googleapis.com/projects/<number>/locations/<location>/workloadIdentityPools/<pool>/providers/<provider>"
        )
    if service_account and not provider:
        raise ValueError(
            "LANGSMITH_GCP_SERVICE_ACCOUNT requires LANGSMITH_GCP_WORKLOAD_IDENTITY_PROVIDER"
        )
    proofs = _proofs()
    if role_arn and os.environ.get("AWS_ACCESS_KEY_ID"):
        await logger.awarning(
            "AWS_ACCESS_KEY_ID is set, so AWS SDKs use it instead of LANGSMITH_AWS_ROLE_ARN"
        )
    if client_id:
        for credential in (
            "AZURE_CLIENT_SECRET",
            "AZURE_CLIENT_CERTIFICATE_PATH",
            "AZURE_USERNAME",
        ):
            if os.environ.get(credential):
                raise ValueError(
                    f"Unset {credential} to use Azure workload identity; "
                    "DefaultAzureCredential tries it before workload identity"
                )
    if provider and os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        await logger.awarning(
            "GOOGLE_APPLICATION_CREDENTIALS is set and will point at LangSmith workload identity instead"
        )
    aws = azure = gcp = None
    # Every refresh loop is ours to stop until all configured clouds have started.
    try:
        if role_arn:
            aws = await _start_refresher(AWS_AUDIENCE, proofs, role_arn=role_arn)
        if client_id and tenant_id:
            azure = await _start_refresher(
                AZURE_AUDIENCE, proofs, client_id=client_id, tenant_id=tenant_id
            )
        if provider:
            gcp = await _start_refresher(
                GCP_AUDIENCE,
                proofs,
                provider=provider,
                service_account=service_account,
            )
            credentials: dict[str, Any] = {
                "type": "external_account",
                "audience": provider,
                "subject_token_type": "urn:ietf:params:oauth:token-type:jwt",
                "token_url": "https://sts.googleapis.com/v1/token",
                "credential_source": {"file": gcp[1]},
            }
            if service_account:
                credentials["service_account_impersonation_url"] = (
                    "https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/"
                    f"{urllib.parse.quote(service_account, safe='@')}:generateAccessToken"
                )
            credentials_path = os.path.join(
                os.path.dirname(gcp[1]), "google-credentials.json"
            )
            with open(credentials_path, "w") as f:
                json.dump(credentials, f)
    except BaseException:
        for started in (aws, azure, gcp):
            if started:
                started[0].cancel()
                await asyncio.wait([started[0]])
        raise
    # Nothing awaits after this, so a cancelled start never leaves these pointing at a removed file.
    if role_arn and aws:
        os.environ["AWS_ROLE_ARN"] = role_arn
        os.environ["AWS_WEB_IDENTITY_TOKEN_FILE"] = aws[1]
        if config.LANGSMITH_HOST_PROJECT_ID:
            os.environ.setdefault(
                "AWS_ROLE_SESSION_NAME", f"langsmith-{config.LANGSMITH_HOST_PROJECT_ID}"
            )
    if client_id and tenant_id and azure:
        os.environ["AZURE_CLIENT_ID"] = client_id
        os.environ["AZURE_TENANT_ID"] = tenant_id
        os.environ["AZURE_FEDERATED_TOKEN_FILE"] = azure[1]
        # Some azure-identity versions and ManagedIdentityCredential use workload identity only when this is set.
        os.environ.setdefault(
            "AZURE_AUTHORITY_HOST", "https://login.microsoftonline.com"
        )
    if gcp:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(
            os.path.dirname(gcp[1]), "google-credentials.json"
        )
    return [started[0] for started in (aws, azure, gcp) if started]


def _proofs() -> list[Proof]:
    proofs: list[Proof] = []
    if config.LANGSMITH_AGENT_AUTH_POD_TOKEN_PATH:
        proofs.append(PodToken())
    if api_key := config.LANGSMITH_CONTROL_PLANE_API_KEY:
        proofs.append(DeploymentKey(api_key))
    if not proofs:
        raise ValueError(
            "Workload identity requires LANGSMITH_API_KEY or LANGSMITH_CONTROL_PLANE_API_KEY"
        )
    return proofs


async def _start_refresher(
    audience: str, proofs: Sequence[Proof], **log_fields: Any
) -> tuple[asyncio.Task[None], str]:
    refresher = TokenFileRefresher(
        config.langsmith_api_url("/agent-auth/token"),
        proofs,
        httpx.AsyncClient(timeout=_REQUEST_TIMEOUT_SECONDS),
        audience,
    )
    # The refresher is ours to close until its refresh loop is running.
    task: asyncio.Task[None] | None = None
    try:
        delay = await refresher.refresh()
        if os.path.exists(refresher.path):
            await logger.ainfo(
                "Configured web identity", audience=audience, **log_fields
            )
        else:
            await logger.awarning(
                "Started without a web identity token; cloud calls fail until a refresh succeeds",
                audience=audience,
                **log_fields,
            )
        task = create_task(refresher.run(delay))
        # Let run() enter its try block, so cancelling the task always cleans up.
        await asyncio.sleep(0)
    except BaseException:
        if task is not None:
            task.cancel()
            await asyncio.wait([task])
        await refresher.aclose()
        raise
    return task, refresher.path
