"""Main API client used by the Python SDK and CLI."""

import typing as t
from urllib.parse import quote as _url_quote

import httpx

from dreadnode.app.api.models import (
    AutoRefillConfig,
    CheckoutSession,
    CreateOptimizationJobBase,
    CreateTrainingJobBase,
    CreditBalance,
    CreditsPricing,
    HealthCheck,
    OptimizationJob,
    OptimizationJobArtifacts,
    OptimizationJobCreateRequest,
    OptimizationJobList,
    OptimizationJobLogList,
    OptimizationJobProgressUpdateRequest,
    Organization,
    Package,
    PaymentMethod,
    Project,
    ProviderPresetsList,
    StorageCredentials,
    TrainingCatalogResponse,
    TrainingJob,
    TrainingJobArtifacts,
    TrainingJobCreateRequest,
    TrainingJobList,
    TrainingJobLogList,
    TrainingJobProgressUpdateRequest,
    TrainingRLContext,
    UsageLimits,
    User,
    UserSecret,
    UserSecretsList,
    WebSearchResponse,
    Workspace,
)
from dreadnode.core.exceptions import InsufficientCreditsError
from dreadnode.version import VERSION

_TRANSPORT_ERRORS = (
    httpx.ReadError,
    httpx.ConnectError,
    httpx.RemoteProtocolError,
    httpx.ReadTimeout,
    httpx.ConnectTimeout,
)


class AuthenticationError(RuntimeError):
    """Raised when the platform returns HTTP 401."""


class NotFoundError(RuntimeError):
    """Raised when the platform returns HTTP 404 for a resource lookup.

    Subclass of :class:`RuntimeError` so existing ``except RuntimeError``
    handlers keep working; callers that want 404-specific recovery (e.g.
    idempotent deletes that tolerate already-gone resources) can catch
    this directly instead of pattern-matching on error message strings.
    """


class ConflictError(RuntimeError):
    """Raised when the platform returns HTTP 409 for a state conflict.

    Subclass of :class:`RuntimeError` so existing ``except RuntimeError``
    handlers keep working; callers that want conflict-specific UX (e.g.
    refusing to delete a session linked to an evaluation) can catch this
    directly instead of pattern-matching on error message strings.
    """


class PlatformBackendUnavailableError(RuntimeError):
    """Raised when the platform endpoint is transiently unavailable.

    Used by the hosted web-search endpoint to signal that the SDK should
    fall through to another configured backend (5xx, including 503 from
    deployments without a Brave key, and transport errors).
    """


class ApiClient:
    """
    Main API client implementing the routes used by the Python SDK and CLI.
    """

    def __init__(
        self,
        base_url: str,
        *,
        api_key: str | None = None,
        timeout: int = 30,
        default_org: str | None = None,
    ):
        """
        Initialize the API client.

        Args:
            base_url: The base URL of the Dreadnode API.
            api_key: API key for authentication (X-API-Key header).
            timeout: Request timeout in seconds.
            default_org: Optional default organization key for org-scoped endpoints.
        """
        api_base_url, server_root_url = self._normalize_base_urls(base_url)
        self._base_url = api_base_url
        self._server_root_url = server_root_url
        self._api_key = api_key
        self._default_org = default_org
        self._credits = CreditsClient(self, default_org)

        headers = {
            "User-Agent": f"dreadnode-sdk/{VERSION}",
            "Accept": "application/json",
        }
        if api_key:
            headers["X-API-Key"] = api_key

        self._client = httpx.Client(
            headers=headers,
            base_url=self._base_url,
            timeout=httpx.Timeout(timeout, connect=5),
        )

    @property
    def credits(self) -> "CreditsClient":
        """Access credits and billing endpoints."""
        return self._credits

    @property
    def server_root_url(self) -> str:
        """Web root URL for the platform — same host as the API, with the
        ``/api/v1`` suffix stripped. Used to build deep links into the UI
        (session viewer, reports tab) from in-process callers like the TUI.
        """
        return self._server_root_url

    @staticmethod
    def _normalize_base_urls(base_url: str) -> tuple[str, str]:
        base_url = base_url.rstrip("/")
        if base_url.endswith("/api/v1"):
            return base_url, base_url.removesuffix("/api/v1")
        if base_url.endswith("/api"):
            return base_url, base_url.removesuffix("/api")
        return f"{base_url}/api/v1", base_url

    def _get_error_message(self, response: httpx.Response) -> str:
        """Extract error message from HTTP response."""
        try:
            obj = response.json()
            detail = obj.get("detail", str(obj))
        except (TypeError, ValueError):
            return f"{response.status_code}: {response.content!r}"
        else:
            return f"{response.status_code}: {detail}"

    @staticmethod
    def _is_credit_related_429(detail: str) -> bool:
        lowered = detail.lower()
        return "credit" in lowered

    def _request(
        self,
        method: str,
        path: str,
        params: dict[str, t.Any] | None = None,
        json_data: dict[str, t.Any] | None = None,
        data: dict[str, t.Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> httpx.Response:
        """Make a raw HTTP request without raising on errors."""
        return self._client.request(
            method,
            path,
            params=params,
            json=json_data,
            data=data,
            headers=headers,
        )

    def request(
        self,
        method: str,
        path: str,
        params: dict[str, t.Any] | None = None,
        json_data: dict[str, t.Any] | None = None,
        data: dict[str, t.Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> httpx.Response:
        """Make an HTTP request and raise on errors."""
        response = self._request(method, path, params, json_data, data, headers)
        if response.status_code == 401:
            raise AuthenticationError(self._get_error_message(response))
        if response.status_code == 404:
            raise NotFoundError(self._get_error_message(response))
        if response.status_code == 409:
            raise ConflictError(self._get_error_message(response))
        if response.status_code == 429:
            error_message = self._get_error_message(response)
            detail = error_message.split(": ", 1)[1] if ": " in error_message else error_message
            if self._is_credit_related_429(detail):
                raise InsufficientCreditsError(detail)
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise RuntimeError(self._get_error_message(response)) from e
        return response

    # =========================================================================
    # Health & Config (public routes)
    # =========================================================================

    def health_check(self) -> HealthCheck:
        """GET /api/ or GET /api/health - Health check."""
        response = self.request("GET", "/health")
        return HealthCheck(**response.json())

    # =========================================================================
    # Auth (public routes)
    # =========================================================================

    def create_device_code(self) -> dict[str, t.Any]:
        """POST /api/v1/auth/device/code - Create a device code."""
        response = self.request(
            "POST",
            "/auth/device/code",
        )
        return t.cast("dict[str, t.Any]", response.json())

    def poll_device_code(self, device_code: str) -> tuple[int, dict[str, t.Any] | None]:
        """GET /api/v1/auth/device/code/{device_code} - Poll device code status."""
        response = self._request(
            "GET",
            f"/auth/device/code/{device_code}",
        )
        if response.is_success:
            return response.status_code, t.cast("dict[str, t.Any]", response.json())
        return response.status_code, None

    def exchange_device_code(self, device_code: str) -> dict[str, t.Any]:
        """POST /api/v1/auth/device/token - Exchange device code for tokens."""
        response = self.request(
            "POST",
            "/auth/device/token",
            json_data={"device_code": device_code},
        )
        return t.cast("dict[str, t.Any]", response.json())

    def create_api_key_with_jwt(
        self,
        access_token: str,
        name: str | None = None,
        *,
        allow_self_revoke: bool = False,
        org_id: str | None = None,
        workspace_id: str | None = None,
        allowed_scopes: list[str] | None = None,
    ) -> dict[str, t.Any]:
        """POST /api/user/api-keys - Create an API key using JWT bearer auth."""
        payload: dict[str, t.Any] = {
            "name": name,
            "allow_self_revoke": allow_self_revoke,
        }
        if org_id is not None:
            payload["org_id"] = org_id
        if workspace_id is not None:
            payload["workspace_id"] = workspace_id
        if allowed_scopes is not None:
            payload["allowed_scopes"] = allowed_scopes

        response = self.request(
            "POST",
            "/user/api-keys",
            json_data=payload,
            headers={"Authorization": f"Bearer {access_token}"},
        )
        return t.cast("dict[str, t.Any]", response.json())

    def revoke_self_api_key(self) -> None:
        """DELETE /api/user/api-keys/self - Revoke the current API key."""
        self.request("DELETE", "/user/api-keys/self")

    # =========================================================================
    # User (authenticated routes)
    # =========================================================================

    def get_user(self) -> User:
        """GET /api/user - Get current user."""
        response = self.request("GET", "/user")
        return User(**response.json())

    # =========================================================================
    # Inference (authenticated routes)
    # =========================================================================

    def list_system_models(self) -> list[dict[str, t.Any]]:
        """GET /api/v1/inference - List platform system models (dn/ models)."""
        response = self.request("GET", "/inference")
        return t.cast("list[dict[str, t.Any]]", response.json().get("models", []))

    def list_catalog_models(
        self,
        *,
        query: str | None = None,
        limit: int | None = None,
        provider: str | None = None,
        capabilities: list[str] | None = None,
        open_weights: bool | None = None,
        min_context: int | None = None,
        max_context: int | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        featured: bool = False,
    ) -> list[dict[str, t.Any]]:
        """GET /api/v1/inference/catalog - List featured or searched BYOK catalog models."""
        params: dict[str, t.Any] = {}
        if query is not None:
            params["query"] = query
        if limit is not None:
            params["limit"] = limit
        if provider is not None:
            params["provider"] = provider
        if capabilities:
            params["capabilities"] = capabilities
        if open_weights is not None:
            params["open_weights"] = open_weights
        if min_context is not None:
            params["min_context"] = min_context
        if max_context is not None:
            params["max_context"] = max_context
        if min_price is not None:
            params["min_price"] = min_price
        if max_price is not None:
            params["max_price"] = max_price
        if featured:
            params["featured"] = True
        response = self.request("GET", "/inference/catalog", params=params)
        return t.cast("list[dict[str, t.Any]]", response.json().get("models", []))

    def validate_inference_model(self, model_id: str) -> dict[str, t.Any]:
        """POST /api/v1/inference/validate - Validate a model ID via LiteLLM."""
        response = self.request(
            "POST",
            "/inference/validate",
            json_data={"model_id": model_id},
        )
        return t.cast("dict[str, t.Any]", response.json())

    def get_user_preferences(self, *, org: str | None = None) -> dict[str, t.Any]:
        """GET /api/v1/user/preferences - Get user's enabled models with status.

        When ``org`` is provided, preferences are scoped to the active
        organization for org-specific model access filtering.
        """
        params: dict[str, t.Any] | None = None
        if isinstance(org, str) and org.strip():
            params = {"org": org.strip()}
        response = self.request("GET", "/user/preferences", params=params)
        return t.cast("dict[str, t.Any]", response.json())

    def provision_inference_key(self, org_key: str, client_id: str) -> dict[str, t.Any]:
        """POST /api/v1/org/{org}/inference/keys - Provision a litellm virtual key."""
        response = self.request(
            "POST",
            f"/org/{org_key}/inference/keys",
            json_data={"client_id": client_id},
        )
        return t.cast("dict[str, t.Any]", response.json())

    # =========================================================================
    # Hosted tools
    # =========================================================================

    def search_web(
        self,
        *,
        query: str,
        num_results: int,
        org: str | None = None,
    ) -> WebSearchResponse:
        """POST /api/v1/org/{org}/tools/search - Hosted web search (Brave-backed).

        Distinguishes 5xx (transient — caller should fall through to another
        backend) from 4xx (surface). Raises:

        * ``PlatformBackendUnavailableError`` for 5xx and transport errors.
        * ``AuthenticationError`` for 401.
        * ``InsufficientCreditsError`` for 402.
        * ``RuntimeError`` for any other 4xx.
        """
        org_key = org or self._default_org
        if not org_key:
            raise RuntimeError(
                "search_web requires an organization (pass org=... or configure "
                "default_org on the ApiClient)."
            )
        try:
            response = self._request(
                "POST",
                f"/org/{org_key}/tools/search",
                json_data={"query": query, "num_results": num_results},
            )
        except _TRANSPORT_ERRORS as exc:
            raise PlatformBackendUnavailableError(f"transport error: {exc}") from exc

        if response.status_code >= 500:
            raise PlatformBackendUnavailableError(self._get_error_message(response))
        if response.status_code == 401:
            raise AuthenticationError(self._get_error_message(response))
        if response.status_code == 402:
            raise InsufficientCreditsError(self._get_error_message(response))
        if response.status_code >= 400:
            raise RuntimeError(self._get_error_message(response))
        return WebSearchResponse(**response.json())

    # =========================================================================
    # Secrets
    # =========================================================================

    def list_secrets(self) -> UserSecretsList:
        """GET /api/user/secrets - List all user secrets."""
        response = self.request("GET", "/user/secrets")
        return UserSecretsList(**response.json())

    def get_secret(self, secret_id: str) -> UserSecret:
        """GET /api/user/secrets/{secret_id} - Get a specific secret."""
        response = self.request("GET", f"/user/secrets/{secret_id}")
        return UserSecret(**response.json())

    def get_secret_presets(self) -> ProviderPresetsList:
        """GET /api/user/secrets/presets - Get available provider presets."""
        response = self.request("GET", "/user/secrets/presets")
        return ProviderPresetsList(**response.json())

    def create_secret(self, name: str, value: str) -> UserSecret:
        """POST /api/user/secrets - Create a custom secret."""
        response = self.request(
            "POST",
            "/user/secrets",
            json_data={"name": name, "value": value},
        )
        return UserSecret(**response.json())

    def create_secret_from_preset(self, provider: str, value: str) -> UserSecret:
        """POST /api/user/secrets/preset - Create a secret from a provider preset."""
        response = self.request(
            "POST",
            "/user/secrets/preset",
            json_data={"provider": provider, "value": value},
        )
        return UserSecret(**response.json())

    def update_secret(self, secret_id: str, value: str) -> UserSecret:
        """PUT /api/user/secrets/{secret_id} - Update a secret's value."""
        response = self.request(
            "PUT",
            f"/user/secrets/{secret_id}",
            json_data={"value": value},
        )
        return UserSecret(**response.json())

    def delete_secret(self, secret_id: str) -> None:
        """DELETE /api/user/secrets/{secret_id} - Delete a secret."""
        self.request("DELETE", f"/user/secrets/{secret_id}")

    # =========================================================================
    # Limits
    # =========================================================================

    def get_usage_limits(self) -> UsageLimits:
        """GET /api/user/limits - Get usage limits for current user."""
        response = self.request("GET", "/user/limits")
        return UsageLimits(**response.json())

    def get_limits(self) -> UsageLimits:
        """Compatibility alias for get_usage_limits()."""
        return self.get_usage_limits()

    # =========================================================================
    # OTEL Ingestion
    # =========================================================================

    def ingest_traces(self, org: str, traces: list[dict[str, t.Any]]) -> dict[str, t.Any]:
        """POST /api/org/{org}/otel/traces - Ingest traces from SDK."""
        response = self.request(
            "POST",
            f"/org/{org}/otel/traces",
            json_data={"traces": traces},
        )
        return t.cast("dict[str, t.Any]", response.json())

    # =========================================================================
    # Organization
    # =========================================================================

    def get_organization(self, org: str) -> Organization:
        """GET /api/org/{org} - Get org details."""
        response = self.request("GET", f"/org/{org}")
        return Organization(**response.json())

    def list_user_organizations(self) -> list[Organization]:
        """GET /api/user/organizations - List organizations visible to the current user."""
        response = self.request("GET", "/user/organizations")
        return [Organization(**org) for org in response.json()]

    def list_organization_workspaces(self, org: str) -> list[Workspace]:
        """GET /api/org/{org}/ws - List workspaces in an organization."""
        response = self.request("GET", f"/org/{org}/ws")
        data = response.json()
        items = data.get("workspaces", data) if isinstance(data, dict) else data
        return [Workspace(**ws) for ws in items]

    def list_workspaces(self, org: str) -> list[Workspace]:
        """Compatibility alias for list_organization_workspaces()."""
        return self.list_organization_workspaces(org)

    # =========================================================================
    # Packages - Type Aliases
    # =========================================================================

    def list_datasets(
        self,
        org: str,
        *,
        name: str | None = None,
        search: str | None = None,
        tags: list[str] | None = None,
        license: list[str] | None = None,
        task_categories: list[str] | None = None,
        format: list[str] | None = None,
        size_category: list[str] | None = None,
        include_public: bool = False,
        sort_by: str = "created_at",
        sort_dir: str = "desc",
        page: int = 1,
        limit: int = 50,
    ) -> list[Package]:
        """GET /api/org/{org}/datasets - List datasets."""
        params: dict[str, t.Any] = {
            "sort_by": sort_by,
            "sort_dir": sort_dir,
            "page": page,
            "limit": limit,
            "include_public": include_public,
        }
        if name:
            params["name"] = name
        if search:
            params["search"] = search
        if tags:
            params["tags"] = tags
        if license:
            params["license"] = license
        if task_categories:
            params["task_categories"] = task_categories
        if format:
            params["format"] = format
        if size_category:
            params["size_category"] = size_category
        response = self.request("GET", f"/org/{org}/datasets", params=params)
        payload = response.json()
        items = (
            payload.get("datasets", payload.get("items", payload))
            if isinstance(payload, dict)
            else payload
        )
        return [self._package_from_dataset_payload(p) for p in items]

    def get_dataset(self, org: str, name: str, version: str | None = None) -> Package:
        """GET /api/org/{org}/datasets/{name}[/{version}] - Get dataset details."""
        path = f"/org/{org}/datasets/{name}/{version}" if version else f"/org/{org}/datasets/{name}"
        response = self.request("GET", path)
        return self._package_from_dataset_payload(response.json())

    def delete_dataset(self, org: str, name: str, version: str) -> None:
        """DELETE /api/org/{org}/datasets/{name}/{version} - Delete dataset artifact."""
        self.request("DELETE", f"/org/{org}/datasets/{name}/{version}")

    def download_dataset(
        self, org: str, name: str, version: str, *, format: str = "raw", split: str | None = None
    ) -> dict:
        """POST /api/org/{org}/datasets/{name}/{version}/download - Get presigned download URL."""
        body: dict[str, t.Any] = {"format": format}
        if split:
            body["split"] = split
        response = self.request(
            "POST", f"/org/{org}/datasets/{name}/{version}/download", json_data=body
        )
        return response.json()

    def list_dataset_versions(self, org: str, name: str) -> dict:
        """GET /api/org/{org}/datasets/{name}/versions - List available versions."""
        response = self.request("GET", f"/org/{org}/datasets/{name}/versions")
        return response.json()

    def get_dataset_facets(
        self,
        org: str,
        *,
        search: str | None = None,
        tags: list[str] | None = None,
        license: list[str] | None = None,
        task_categories: list[str] | None = None,
        format: list[str] | None = None,
        size_category: list[str] | None = None,
        include_public: bool = False,
    ) -> dict[str, t.Any]:
        """GET /api/org/{org}/datasets/facets - Get dataset filter facets."""
        params: dict[str, t.Any] = {"include_public": include_public}
        if search:
            params["search"] = search
        if tags:
            params["tags"] = tags
        if license:
            params["license"] = license
        if task_categories:
            params["task_categories"] = task_categories
        if format:
            params["format"] = format
        if size_category:
            params["size_category"] = size_category
        response = self.request("GET", f"/org/{org}/datasets/facets", params=params)
        return t.cast("dict[str, t.Any]", response.json())

    def list_dataset_activity(
        self,
        org: str,
        *,
        limit: int = 50,
        offset: int = 0,
        user_id: str | None = None,
        dataset_name: str | None = None,
    ) -> dict[str, t.Any]:
        """GET /api/org/{org}/datasets/activity - List dataset download activity."""
        params: dict[str, t.Any] = {"limit": limit, "offset": offset}
        if user_id is not None:
            params["user_id"] = user_id
        if dataset_name is not None:
            params["dataset_name"] = dataset_name
        response = self.request("GET", f"/org/{org}/datasets/activity", params=params)
        return t.cast("dict[str, t.Any]", response.json())

    def update_dataset_visibility(self, org: str, name: str, *, is_public: bool) -> dict:
        """PATCH /api/org/{org}/datasets/{name}/visibility - Update visibility."""
        response = self.request(
            "PATCH",
            f"/org/{org}/datasets/{name}/visibility",
            json_data={"is_public": is_public},
        )
        return response.json()

    def list_models(
        self,
        org: str,
        *,
        name: str | None = None,
        search: str | None = None,
        tags: list[str] | None = None,
        license: list[str] | None = None,
        task_categories: list[str] | None = None,
        framework: list[str] | None = None,
        size_category: list[str] | None = None,
        include_public: bool = False,
        sort_by: str = "created_at",
        sort_dir: str = "desc",
        page: int = 1,
        limit: int = 50,
    ) -> list[Package]:
        """GET /api/org/{org}/models - List models."""
        params: dict[str, t.Any] = {
            "sort_by": sort_by,
            "sort_dir": sort_dir,
            "page": page,
            "limit": limit,
            "include_public": include_public,
        }
        if name:
            params["name"] = name
        if search:
            params["search"] = search
        if tags:
            params["tags"] = tags
        if license:
            params["license"] = license
        if task_categories:
            params["task_categories"] = task_categories
        if framework:
            params["framework"] = framework
        if size_category:
            params["size_category"] = size_category
        response = self.request("GET", f"/org/{org}/models", params=params)
        payload = response.json()
        if isinstance(payload, dict):
            items = payload.get("models", payload.get("items", payload))
        else:
            items = payload
        return [self._package_from_model_payload(p) for p in items]

    def get_model(self, org: str, name: str, version: str | None = None) -> Package:
        """GET /api/org/{org}/models/{name}[/{version}] - Get model details."""
        path = f"/org/{org}/models/{name}/{version}" if version else f"/org/{org}/models/{name}"
        response = self.request("GET", path)
        return self._package_from_model_payload(response.json())

    def delete_model(self, org: str, name: str, version: str) -> None:
        """DELETE /api/org/{org}/models/{name}/{version} - Delete model artifact."""
        self.request("DELETE", f"/org/{org}/models/{name}/{version}")

    def download_model(self, org: str, name: str, version: str) -> dict:
        """POST /api/org/{org}/models/{name}/{version}/download - Get presigned download URL."""
        response = self.request("POST", f"/org/{org}/models/{name}/{version}/download")
        return response.json()

    def list_model_versions(self, org: str, name: str) -> dict:
        """GET /api/org/{org}/models/{name}/versions - List available versions."""
        response = self.request("GET", f"/org/{org}/models/{name}/versions")
        return response.json()

    def get_model_facets(
        self,
        org: str,
        *,
        search: str | None = None,
        tags: list[str] | None = None,
        license: list[str] | None = None,
        task_categories: list[str] | None = None,
        framework: list[str] | None = None,
        size_category: list[str] | None = None,
        include_public: bool = False,
    ) -> dict[str, t.Any]:
        """GET /api/org/{org}/models/facets - Get model filter facets."""
        params: dict[str, t.Any] = {"include_public": include_public}
        if search:
            params["search"] = search
        if tags:
            params["tags"] = tags
        if license:
            params["license"] = license
        if task_categories:
            params["task_categories"] = task_categories
        if framework:
            params["framework"] = framework
        if size_category:
            params["size_category"] = size_category
        response = self.request("GET", f"/org/{org}/models/facets", params=params)
        return t.cast("dict[str, t.Any]", response.json())

    def list_model_activity(
        self,
        org: str,
        *,
        limit: int = 50,
        offset: int = 0,
        user_id: str | None = None,
        model_name: str | None = None,
    ) -> dict[str, t.Any]:
        """GET /api/org/{org}/models/activity - List model download activity."""
        params: dict[str, t.Any] = {"limit": limit, "offset": offset}
        if user_id is not None:
            params["user_id"] = user_id
        if model_name is not None:
            params["model_name"] = model_name
        response = self.request("GET", f"/org/{org}/models/activity", params=params)
        return t.cast("dict[str, t.Any]", response.json())

    def compare_model_versions(self, org: str, name: str, versions: list[str]) -> dict:
        """GET /api/org/{org}/models/{name}/compare - Compare versions side-by-side."""
        response = self.request(
            "GET", f"/org/{org}/models/{name}/compare", params={"versions": versions}
        )
        return response.json()

    def set_model_alias(self, org: str, name: str, version: str, alias: str) -> dict:
        """POST /api/org/{org}/models/{name}/{version}/aliases - Set a named alias."""
        response = self.request(
            "POST", f"/org/{org}/models/{name}/{version}/aliases", json_data={"alias": alias}
        )
        return response.json()

    def remove_model_alias(self, org: str, name: str, version: str, alias: str) -> None:
        """DELETE /api/org/{org}/models/{name}/{version}/aliases/{alias} - Remove an alias."""
        self.request("DELETE", f"/org/{org}/models/{name}/{version}/aliases/{alias}")

    def update_model_visibility(self, org: str, name: str, *, is_public: bool) -> dict:
        """PATCH /api/org/{org}/models/{name}/visibility - Update visibility."""
        response = self.request(
            "PATCH",
            f"/org/{org}/models/{name}/visibility",
            json_data={"is_public": is_public},
        )
        return response.json()

    def update_model_metrics(
        self, org: str, name: str, version: str, metrics: dict[str, float | int | str]
    ) -> dict:
        """PUT /api/org/{org}/models/{name}/{version}/metrics - Update evaluation metrics."""
        response = self.request(
            "PUT", f"/org/{org}/models/{name}/{version}/metrics", json_data=metrics
        )
        return response.json()

    @staticmethod
    def _package_from_dataset_payload(payload: dict[str, t.Any]) -> Package:
        """Normalize dataset artifact responses into the generic Package model."""
        if "full_name" in payload:
            return Package(**payload)

        canonical_name = str(payload["name"])
        local_name = canonical_name.split("/", 1)[1] if "/" in canonical_name else canonical_name
        version = payload.get("latest_version") or payload.get("version")

        return Package(
            id=payload.get("id"),
            name=local_name,
            full_name=canonical_name,
            package_type="dataset",
            type="dataset",
            summary=payload.get("summary"),
            visibility="public" if payload.get("is_public") else "private",
            created_at=payload.get("created_at"),
            updated_at=payload.get("updated_at"),
            versions=payload.get("versions", [version] if version is not None else []),
            latest_version=version,
        )

    @staticmethod
    def _package_from_model_payload(payload: dict[str, t.Any]) -> Package:
        """Normalize model artifact responses into the generic Package model."""
        if "full_name" in payload:
            return Package(**payload)

        canonical_name = str(payload["name"])
        local_name = canonical_name.split("/", 1)[1] if "/" in canonical_name else canonical_name
        version = payload.get("latest_version") or payload.get("version")
        summary = payload.get("summary")
        if summary is None:
            framework = payload.get("framework")
            task = payload.get("task")
            architecture = payload.get("architecture")
            parts = [part for part in (framework, task, architecture) if part]
            summary = " · ".join(parts) if parts else None

        return Package(
            id=payload.get("id"),
            name=local_name,
            full_name=canonical_name,
            package_type="model",
            type="model",
            summary=summary,
            visibility="public" if payload.get("is_public") else "private",
            created_at=payload.get("created_at"),
            updated_at=payload.get("updated_at"),
            versions=payload.get("versions", [version] if version is not None else []),
            latest_version=version,
        )

    # =========================================================================
    # Storage
    # =========================================================================

    def get_storage_access(self, org: str, key: str) -> StorageCredentials:
        """GET /org/{org}/ws/{key}/storage/credentials - Get credentials."""
        response = self.request("GET", f"/org/{org}/ws/{key}/storage/credentials")
        return StorageCredentials(**response.json())

    # =========================================================================
    # Workspace
    # =========================================================================

    def get_workspace(self, org: str, workspace: str) -> Workspace:
        """GET /org/{org}/ws/{workspace} - Get workspace details."""
        response = self.request("GET", f"/org/{org}/ws/{workspace}")
        return Workspace(**response.json())

    def create_workspace(
        self,
        org: str,
        name: str,
        key: str,
        description: str | None = None,
    ) -> Workspace:
        """POST /org/{org}/ws - Create a new workspace."""
        payload: dict[str, t.Any] = {"name": name, "key": key}
        if description:
            payload["description"] = description
        response = self.request("POST", f"/org/{org}/ws", json_data=payload)
        return Workspace(**response.json())

    # =========================================================================
    # Projects
    # =========================================================================

    def list_projects(self, org: str, workspace: str) -> list[Project]:
        """GET /org/{org}/ws/{workspace}/projects - List projects."""
        response = self.request("GET", f"/org/{org}/ws/{workspace}/projects")
        return [Project(**p) for p in response.json()]

    def get_default_project_key(self, org: str, workspace: str) -> str | None:
        """Return the default project key for a workspace, falling back to the first project."""
        projects = self.list_projects(org, workspace)
        for project in projects:
            if project.is_default or project.key == "default":
                return project.key
        return projects[0].key if projects else None

    def get_project(self, org: str, workspace: str, project: str) -> Project:
        """GET /org/{org}/ws/{workspace}/projects/{project} - Get project details."""
        response = self.request("GET", f"/org/{org}/ws/{workspace}/projects/{project}")
        return Project(**response.json())

    def create_project(
        self,
        org: str,
        workspace: str,
        name: str,
        key: str,
        description: str | None = None,
    ) -> Project:
        """POST /org/{org}/ws/{workspace}/projects - Create a new project."""
        payload: dict[str, t.Any] = {"name": name, "key": key}
        if description:
            payload["description"] = description
        response = self.request("POST", f"/org/{org}/ws/{workspace}/projects", json_data=payload)
        return Project(**response.json())

    def delete_project(self, org: str, workspace: str, project: str) -> None:
        """DELETE /org/{org}/ws/{workspace}/projects/{project} - Delete a project."""
        self.request("DELETE", f"/org/{org}/ws/{workspace}/projects/{project}")

    # =========================================================================
    # Items (structured records emitted by agents)
    # =========================================================================

    def create_item(
        self,
        org: str,
        workspace: str,
        project: str,
        *,
        item_type: str,
        data: dict[str, t.Any],
        ref: str | None = None,
        title: str | None = None,
        status: str | None = None,
        notes: str | None = None,
        session_id: str | None = None,
        trace_id: str | None = None,
        span_id: str | None = None,
        capability: str | None = None,
        capability_version: str | None = None,
        schema_ref: str | None = None,
        source: str = "runtime",
        dedupe_key: str | None = None,
        links: list[dict[str, t.Any]] | None = None,
    ) -> dict[str, t.Any]:
        """POST /org/{org}/ws/{workspace}/projects/{project}/items - Create an item.

        Used by the runtime ``report_item`` tool to emit structured records
        (findings, assets, …) during a run. ``dedupe_key`` makes the create
        idempotent so a retry or later span-extraction reconciles to one row.
        ``status``/``notes`` populate the mutable disposition overlay (a finding's
        severity lives in ``data``). ``links`` are inline
        ``{"target_item_id"/"target_ref", "relationship"}`` edges created with the
        item. Returns the created item dict (including its ``id``).
        """
        payload: dict[str, t.Any] = {
            "item_type": item_type,
            "data": data,
            "source": source,
        }
        if ref is not None:
            payload["ref"] = ref
        if dedupe_key is not None:
            payload["dedupe_key"] = dedupe_key
        if title is not None:
            payload["title"] = title
        if status is not None:
            payload["status"] = status
        if notes is not None:
            payload["notes"] = notes
        if session_id is not None:
            payload["session_id"] = session_id
        if trace_id is not None:
            payload["trace_id"] = trace_id
        if span_id is not None:
            payload["span_id"] = span_id
        if capability is not None:
            payload["capability"] = capability
        if capability_version is not None:
            payload["capability_version"] = capability_version
        if schema_ref is not None:
            payload["schema_ref"] = schema_ref
        if links:
            payload["links"] = links

        response = self.request(
            "POST",
            f"/org/{org}/ws/{workspace}/projects/{project}/items",
            json_data=payload,
        )
        return t.cast("dict[str, t.Any]", response.json())

    def resolve_item_ref(self, org: str, workspace: str, project: str, ref: str) -> str | None:
        """Resolve an agent-assigned ref to an item id, or None if not found."""
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/projects/{project}/items",
            params={"ref": ref, "limit": 1},
        )
        items = response.json().get("items", [])
        return str(items[0]["id"]) if items else None

    def update_item(
        self,
        org: str,
        workspace: str,
        project: str,
        item_id: str,
        *,
        data: dict[str, t.Any] | None = None,
        title: str | None = None,
        status: str | None = None,
        notes: str | None = None,
    ) -> dict[str, t.Any]:
        """PATCH …/projects/{project}/items/{item_id} - Edit an item.

        ``data`` is a partial patch: provided keys are shallow-merged onto the
        existing payload then re-validated (so e.g. a finding's ``severity`` can
        be patched alone; omitted keys are unchanged, not deleted). ``title``
        updates the promoted label; ``status``/``notes`` route into the mutable
        disposition overlay. Only provided fields change.
        """
        payload: dict[str, t.Any] = {}
        if data is not None:
            payload["data"] = data
        if title is not None:
            payload["title"] = title
        if status is not None:
            payload["status"] = status
        if notes is not None:
            payload["notes"] = notes
        response = self.request(
            "PATCH",
            f"/org/{org}/ws/{workspace}/projects/{project}/items/{item_id}",
            json_data=payload,
        )
        return t.cast("dict[str, t.Any]", response.json())

    def create_item_link(
        self,
        org: str,
        workspace: str,
        project: str,
        item_id: str,
        *,
        target_item_id: str | None = None,
        target_ref: str | None = None,
        relationship: str,
    ) -> dict[str, t.Any]:
        """POST …/items/{item_id}/links - Link this item to another (same project).

        Target by id or agent-assigned ref (exactly one).
        """
        body: dict[str, t.Any] = {"relationship": relationship}
        if target_ref is not None:
            body["target_ref"] = target_ref
        else:
            body["target_item_id"] = target_item_id
        response = self.request(
            "POST",
            f"/org/{org}/ws/{workspace}/projects/{project}/items/{item_id}/links",
            json_data=body,
        )
        return t.cast("dict[str, t.Any]", response.json())

    # =========================================================================
    # Project Memory
    # =========================================================================

    def list_project_memories(
        self,
        org: str,
        workspace: str,
        project: str,
        *,
        scope_kind: str = "project",
        project_filter: str | None = None,
        include_closed: bool = False,
        subtype: str | None = None,
        limit: int = 50,
    ) -> dict[str, t.Any]:
        """POST /org/{org}/ws/{workspace}/projects/{project}/project-memory/list."""
        payload: dict[str, t.Any] = {
            "scope_kind": scope_kind,
            "include_closed": include_closed,
            "limit": limit,
        }
        if project_filter is not None:
            payload["project_filter"] = project_filter
        if subtype is not None:
            payload["subtype"] = subtype

        response = self.request(
            "POST",
            f"/org/{org}/ws/{workspace}/projects/{project}/project-memory/list",
            json_data=payload,
        )
        return t.cast("dict[str, t.Any]", response.json())

    def list_project_memory_preload(
        self,
        org: str,
        workspace: str,
        project: str,
        *,
        scope_kind: str = "project",
        limit: int = 20,
    ) -> dict[str, t.Any]:
        """List recent open project memories for prompt preload context."""
        return self.list_project_memories(
            org,
            workspace,
            project,
            scope_kind=scope_kind,
            include_closed=False,
            limit=limit,
        )

    def get_project_memory(
        self,
        org: str,
        workspace: str,
        project: str,
        *,
        memory_id: str,
        scope_kind: str = "project",
        project_filter: str | None = None,
        include_closed: bool = False,
    ) -> dict[str, t.Any]:
        """POST /org/{org}/ws/{workspace}/projects/{project}/project-memory/get."""
        payload: dict[str, t.Any] = {
            "memory_id": memory_id,
            "scope_kind": scope_kind,
            "include_closed": include_closed,
        }
        if project_filter is not None:
            payload["project_filter"] = project_filter

        response = self.request(
            "POST",
            f"/org/{org}/ws/{workspace}/projects/{project}/project-memory/get",
            json_data=payload,
        )
        return t.cast("dict[str, t.Any]", response.json())

    def save_project_memory(
        self,
        org: str,
        workspace: str,
        project: str,
        *,
        title: str,
        body: str,
        scope_kind: str = "project",
        summary: str | None = None,
        subtype: str | None = None,
        payload_json: dict[str, t.Any] | None = None,
        memory_id: str | None = None,
        expected_version: int | None = None,
        runtime_id: str | None = None,
        session_id: str | None = None,
        run_id: str | None = None,
        tool_event_id: str | None = None,
        capability_id: str | None = None,
        audit_note: str | None = None,
        project_id: str | None = None,
    ) -> dict[str, t.Any]:
        """POST /org/{org}/ws/{workspace}/projects/{project}/project-memory/save."""
        payload: dict[str, t.Any] = {
            "scope_kind": scope_kind,
            "title": title,
            "body": body,
        }
        if summary is not None:
            payload["summary"] = summary
        if subtype is not None:
            payload["subtype"] = subtype
        if payload_json is not None:
            payload["payload_json"] = payload_json
        if memory_id is not None:
            payload["memory_id"] = memory_id
        if expected_version is not None:
            payload["expected_version"] = expected_version
        if runtime_id is not None:
            payload["runtime_id"] = runtime_id
        if session_id is not None:
            payload["session_id"] = session_id
        if run_id is not None:
            payload["run_id"] = run_id
        if tool_event_id is not None:
            payload["tool_event_id"] = tool_event_id
        if capability_id is not None:
            payload["capability_id"] = capability_id
        if audit_note is not None:
            payload["audit_note"] = audit_note
        if project_id is not None:
            payload["project_id"] = project_id

        response = self.request(
            "POST",
            f"/org/{org}/ws/{workspace}/projects/{project}/project-memory/save",
            json_data=payload,
        )
        return t.cast("dict[str, t.Any]", response.json())

    def close_project_memory(
        self,
        org: str,
        workspace: str,
        project: str,
        *,
        memory_id: str,
        expected_version: int,
        close_reason: str,
        scope_kind: str = "project",
        runtime_id: str | None = None,
        session_id: str | None = None,
        run_id: str | None = None,
        tool_event_id: str | None = None,
        capability_id: str | None = None,
        note: str | None = None,
    ) -> dict[str, t.Any]:
        """POST /org/{org}/ws/{workspace}/projects/{project}/project-memory/close."""
        payload: dict[str, t.Any] = {
            "memory_id": memory_id,
            "scope_kind": scope_kind,
            "expected_version": expected_version,
            "close_reason": close_reason,
        }
        if runtime_id is not None:
            payload["runtime_id"] = runtime_id
        if session_id is not None:
            payload["session_id"] = session_id
        if run_id is not None:
            payload["run_id"] = run_id
        if tool_event_id is not None:
            payload["tool_event_id"] = tool_event_id
        if capability_id is not None:
            payload["capability_id"] = capability_id
        if note is not None:
            payload["note"] = note

        response = self.request(
            "POST",
            f"/org/{org}/ws/{workspace}/projects/{project}/project-memory/close",
            json_data=payload,
        )
        return t.cast("dict[str, t.Any]", response.json())

    # =========================================================================
    # OCI Registry
    # =========================================================================

    @property
    def oci_registry_url(self) -> str:
        """Get the OCI Distribution v2 registry URL."""
        return self._server_root_url

    @property
    def oci_basic_auth(self) -> tuple[str, str] | None:
        """Get basic auth credentials for OCI registry."""
        if self._api_key:
            return ("__token__", self._api_key)
        return None

    # =========================================================================
    # Trace Endpoints
    # =========================================================================

    def execute_workspace_query(
        self,
        org: str,
        workspace: str,
        query: str,
        *,
        project_id: str | None = None,
        max_rows: int = 10_000,
    ) -> dict[str, t.Any]:
        """POST /org/{org}/ws/{workspace}/query - Execute a workspace-scoped OTEL query."""
        payload: dict[str, t.Any] = {"query": query, "max_rows": max_rows}
        if project_id is not None:
            payload["project_id"] = project_id
        response = self.request(
            "POST",
            f"/org/{org}/ws/{workspace}/query",
            json_data=payload,
        )
        return t.cast("dict[str, t.Any]", response.json())

    @staticmethod
    def _raise_query_exception(result: dict[str, t.Any]) -> None:
        """Raise a RuntimeError if the query endpoint returned an exception payload."""
        exception = result.get("exception")
        if exception:
            raise RuntimeError(str(exception))

    def get_trace_spans(
        self,
        org: str,
        workspace: str,
        project: str,
        trace_id: str,
        *,
        limit: int = 100,
        offset: int = 0,
        order_by: str = "Timestamp",
        order_dir: str = "ASC",
    ) -> dict[str, t.Any]:
        """Get paginated spans for a trace from remote storage.

        Args:
            org: Organization key.
            workspace: Workspace key.
            project: Project key.
            trace_id: Trace identifier.
            limit: Number of spans per page (1-1000).
            offset: Number of spans to skip.
            order_by: Column to sort by.
            order_dir: Sort direction (ASC or DESC).

        Returns:
            Dict with 'data', 'rows', and 'meta' keys.
        """
        _ = project
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/traces/{trace_id}/spans",
            params={
                "limit": limit,
                "offset": offset,
                "order_by": order_by,
                "order_dir": order_dir,
            },
        )
        return t.cast("dict[str, t.Any]", response.json())

    def get_run_spans(
        self,
        org: str,
        workspace: str,
        project: str,
        run_id: str,
        *,
        limit: int = 100,
        offset: int = 0,
        order_by: str = "Timestamp",
        order_dir: str = "ASC",
    ) -> dict[str, t.Any]:
        """Compatibility alias for get_trace_spans()."""
        return self.get_trace_spans(
            org,
            workspace,
            project,
            run_id,
            limit=limit,
            offset=offset,
            order_by=order_by,
            order_dir=order_dir,
        )

    def get_trace_stats(
        self,
        org: str,
        workspace: str,
        project: str,
        trace_id: str,
    ) -> dict[str, t.Any]:
        """Get aggregated statistics for a trace from remote storage.

        Args:
            org: Organization key.
            workspace: Workspace key.
            project: Project key.
            trace_id: Trace identifier.

        Returns:
            Dict with trace statistics (total_spans, error_spans, duration, etc.).
        """
        _ = project
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/traces/{trace_id}/stats",
        )
        return t.cast("dict[str, t.Any]", response.json())

    def get_run_stats(
        self,
        org: str,
        workspace: str,
        project: str,
        run_id: str,
    ) -> dict[str, t.Any]:
        """Compatibility alias for get_trace_stats()."""
        return self.get_trace_stats(org, workspace, project, run_id)

    def list_traces(
        self,
        org: str,
        workspace: str,
        project: str | None,
        *,
        page: int = 1,
        page_size: int = 50,
        span_type: str | None = None,
    ) -> dict[str, t.Any]:
        """List workspace traces with explicit filters.

        Returns:
            Dict with 'traces', 'total', 'page', 'limit', 'total_pages',
            'has_next', 'has_previous'.
        """
        params: dict[str, t.Any] = {"page": page, "page_size": page_size}
        if project is not None:
            project_record = self.get_project(org, workspace, project)
            params["project_id"] = project_record.id
        if span_type is not None:
            params["span_type"] = span_type
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/traces",
            params=params,
        )
        return t.cast("dict[str, t.Any]", response.json())

    def get_trace(
        self,
        org: str,
        workspace: str,
        project: str | None,
        trace_id: str,
    ) -> dict[str, t.Any]:
        """Get root trace details for a workspace-visible trace."""
        _ = project
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/traces/{trace_id}",
        )
        return t.cast("dict[str, t.Any]", response.json())

    # =========================================================================
    # Sandboxes
    # =========================================================================

    def list_sandboxes(
        self,
        org: str,
        *,
        state: str | list[str] | None = None,
        project_id: str | None = None,
        limit: int = 50,
        cursor: str | None = None,
    ) -> dict[str, t.Any]:
        """GET /org/{org}/sandboxes - List sandboxes.

        Returns:
            Dict with 'items' (list of sandbox dicts) and 'next_cursor'.
        """
        params: dict[str, t.Any] = {"limit": limit}
        if state is not None:
            params["state"] = ",".join(state) if isinstance(state, list) else state
        if project_id is not None:
            params["project_id"] = project_id
        if cursor is not None:
            params["cursor"] = cursor
        response = self.request("GET", f"/org/{org}/sandboxes", params=params)
        return t.cast("dict[str, t.Any]", response.json())

    def get_sandbox_usage(self, org: str) -> dict[str, t.Any]:
        """GET /org/{org}/sandboxes/usage - Aggregate sandbox usage for the caller."""
        response = self.request("GET", f"/org/{org}/sandboxes/usage")
        return t.cast("dict[str, t.Any]", response.json())

    def get_sandbox(self, org: str, sandbox_id: str) -> dict[str, t.Any]:
        """GET /org/{org}/sandboxes/{sandbox_id} - Get sandbox details by provider sandbox ID."""
        response = self.request("GET", f"/org/{org}/sandboxes/{sandbox_id}")
        return t.cast("dict[str, t.Any]", response.json())

    # =========================================================================
    # Runtimes
    # =========================================================================

    def list_runtimes(
        self,
        org: str,
        workspace: str,
        *,
        state: str | list[str] | None = None,
        project_id: str | None = None,
        limit: int = 50,
        cursor: str | None = None,
    ) -> dict[str, t.Any]:
        """GET /org/{org}/ws/{workspace}/runtimes - List interactive runtimes."""
        params: dict[str, t.Any] = {"limit": limit}
        if state is not None:
            params["state"] = ",".join(state) if isinstance(state, list) else state
        if project_id is not None:
            params["project_id"] = project_id
        if cursor is not None:
            params["cursor"] = cursor
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/runtimes",
            params=params,
        )
        return t.cast("dict[str, t.Any]", response.json())

    def get_runtime(self, org: str, workspace: str, runtime_id: str) -> dict[str, t.Any]:
        """GET /org/{org}/ws/{workspace}/runtimes/{runtime_id} - Get runtime details."""
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/runtimes/{runtime_id}",
        )
        return t.cast("dict[str, t.Any]", response.json())

    def create_runtime(
        self,
        org: str,
        workspace: str,
        project: str | None = None,
        *,
        key: str | None = None,
        name: str | None = None,
        description: str | None = None,
        config: dict[str, t.Any] | None = None,
        requested_runtime_limit_seconds: int | None = None,
    ) -> dict[str, t.Any]:
        """POST /org/{org}/ws/{workspace}/runtimes - Ensure a runtime exists."""
        payload: dict[str, t.Any] = {}
        if project is not None:
            payload["project"] = project
        if key is not None:
            payload["key"] = key
        if name is not None:
            payload["name"] = name
        if description is not None:
            payload["description"] = description
        if config is not None:
            payload["config"] = config
        if requested_runtime_limit_seconds is not None:
            payload["requested_runtime_limit_seconds"] = requested_runtime_limit_seconds
        response = self.request(
            "POST",
            f"/org/{org}/ws/{workspace}/runtimes",
            json_data=payload,
        )
        return t.cast("dict[str, t.Any]", response.json())

    def get_runtime_config(
        self,
        org: str,
        workspace: str,
        runtime_id: str,
    ) -> dict[str, t.Any]:
        """GET /org/{org}/ws/{workspace}/runtimes/{runtime_id}/config - Get runtime config."""
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/runtimes/{runtime_id}/config",
        )
        return t.cast("dict[str, t.Any]", response.json())

    def update_runtime_config(
        self,
        org: str,
        workspace: str,
        runtime_id: str,
        config: dict[str, t.Any],
    ) -> dict[str, t.Any]:
        """PUT /org/{org}/ws/{workspace}/runtimes/{runtime_id}/config - Replace runtime config."""
        response = self.request(
            "PUT",
            f"/org/{org}/ws/{workspace}/runtimes/{runtime_id}/config",
            json_data={"config": config},
        )
        return t.cast("dict[str, t.Any]", response.json())

    def pause_runtime(self, org: str, workspace: str, runtime_id: str) -> dict[str, t.Any]:
        """POST /org/{org}/ws/{workspace}/runtimes/{runtime_id}/pause - Pause a runtime."""
        response = self.request(
            "POST",
            f"/org/{org}/ws/{workspace}/runtimes/{runtime_id}/pause",
        )
        return t.cast("dict[str, t.Any]", response.json())

    def resume_runtime(self, org: str, workspace: str, runtime_id: str) -> dict[str, t.Any]:
        """POST /org/{org}/ws/{workspace}/runtimes/{runtime_id}/resume - Resume a runtime."""
        response = self.request(
            "POST",
            f"/org/{org}/ws/{workspace}/runtimes/{runtime_id}/resume",
        )
        return t.cast("dict[str, t.Any]", response.json())

    def reset_runtime(self, org: str, workspace: str, runtime_id: str) -> dict[str, t.Any]:
        """POST /org/{org}/ws/{workspace}/runtimes/{runtime_id}/reset - Reset a runtime."""
        response = self.request(
            "POST",
            f"/org/{org}/ws/{workspace}/runtimes/{runtime_id}/reset",
        )
        return t.cast("dict[str, t.Any]", response.json())

    def keepalive_runtime(
        self,
        org: str,
        workspace: str,
        runtime_id: str,
        *,
        extend_seconds: int = 300,
    ) -> dict[str, t.Any]:
        """POST /org/{org}/ws/{workspace}/runtimes/{runtime_id}/keepalive - Extend timeout."""
        response = self.request(
            "POST",
            f"/org/{org}/ws/{workspace}/runtimes/{runtime_id}/keepalive",
            json_data={"extend_seconds": extend_seconds},
        )
        return t.cast("dict[str, t.Any]", response.json())

    def start_runtime(
        self,
        org: str,
        workspace: str,
        runtime_id: str,
        *,
        secret_ids: list[str] | None = None,
        requested_runtime_limit_seconds: int | None = None,
    ) -> dict[str, t.Any]:
        """POST /org/{org}/ws/{workspace}/runtimes/{runtime_id}/start - Start or resume a runtime."""
        json_data: dict[str, t.Any] | None = None
        if secret_ids is not None:
            json_data = {"secret_ids": secret_ids}
        if requested_runtime_limit_seconds is not None:
            if json_data is None:
                json_data = {}
            json_data["requested_runtime_limit_seconds"] = requested_runtime_limit_seconds
        response = self.request(
            "POST",
            f"/org/{org}/ws/{workspace}/runtimes/{runtime_id}/start",
            json_data=json_data,
        )
        return t.cast("dict[str, t.Any]", response.json())

    def delete_sandbox(self, org: str, sandbox_id: str) -> None:
        """DELETE /org/{org}/sandboxes/{sandbox_id} - Delete (kill) a sandbox."""
        self.request("DELETE", f"/org/{org}/sandboxes/{sandbox_id}")

    def get_sandbox_logs(self, org: str, sandbox_id: str) -> str:
        """GET /org/{org}/sandboxes/{sandbox_id}/logs - Get sandbox server logs.

        Args:
            sandbox_id: The provider sandbox ID (e.g. E2B sandbox ID).

        Returns:
            Log contents as a string.
        """
        response = self.request("GET", f"/org/{org}/sandboxes/{sandbox_id}/logs")
        return t.cast("str", response.json().get("logs", ""))

    # =========================================================================
    # Evaluations
    # =========================================================================

    def list_evaluation_jobs(
        self,
        org: str,
        workspace: str,
        *,
        page: int = 1,
        page_size: int = 50,
        project_id: str | None = None,
        status: str | None = None,
    ) -> dict[str, t.Any]:
        """GET /org/{org}/ws/{workspace}/evaluations - List evaluation jobs.

        Returns:
            Dict with 'items', 'total', 'page', 'page_size'.
        """
        params: dict[str, t.Any] = {"page": page, "page_size": page_size}
        if project_id is not None:
            params["project_id"] = project_id
        if status is not None:
            params["status"] = status
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/evaluations",
            params=params,
        )
        return t.cast("dict[str, t.Any]", response.json())

    def create_evaluation(
        self,
        org: str,
        workspace: str,
        request: dict[str, t.Any],
    ) -> dict[str, t.Any]:
        """POST /org/{org}/ws/{workspace}/evaluation - Create an evaluation job.

        Returns:
            Dict with evaluation job details.
        """
        response = self.request(
            "POST",
            f"/org/{org}/ws/{workspace}/evaluation",
            json_data=request,
        )
        return t.cast("dict[str, t.Any]", response.json())

    def get_evaluation_job(
        self,
        org: str,
        workspace: str,
        evaluation_id: str,
    ) -> dict[str, t.Any]:
        """GET /org/{org}/ws/{workspace}/evaluation/{id} - Get evaluation job details."""
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/evaluation/{evaluation_id}",
        )
        return t.cast("dict[str, t.Any]", response.json())

    def list_evaluation_items(
        self,
        org: str,
        workspace: str,
        evaluation_id: str,
    ) -> dict[str, t.Any]:
        """GET /org/{org}/ws/{workspace}/evaluation/{id}/items - List evaluation items."""
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/evaluation/{evaluation_id}/items",
        )
        return t.cast("dict[str, t.Any]", response.json())

    def get_evaluation_item_transcript(
        self,
        org: str,
        workspace: str,
        evaluation_id: str,
        item_id: str,
    ) -> dict[str, t.Any]:
        """GET /org/{org}/ws/{workspace}/evaluation/{id}/items/{item_id}/transcript."""
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/evaluation/{evaluation_id}/items/{item_id}/transcript",
        )
        return t.cast("dict[str, t.Any]", response.json())

    def cancel_evaluation(self, org: str, workspace: str, evaluation_id: str) -> dict[str, t.Any]:
        """POST /org/{org}/ws/{workspace}/evaluation/{id}/cancel - Cancel an evaluation."""
        response = self.request(
            "POST",
            f"/org/{org}/ws/{workspace}/evaluation/{evaluation_id}/cancel",
        )
        return t.cast("dict[str, t.Any]", response.json())

    def retry_failed_evaluation(
        self, org: str, workspace: str, evaluation_id: str
    ) -> dict[str, t.Any]:
        """POST /org/{org}/ws/{workspace}/evaluation/{id}/retry-failed - Retry failed items."""
        response = self.request(
            "POST",
            f"/org/{org}/ws/{workspace}/evaluation/{evaluation_id}/retry-failed",
        )
        return t.cast("dict[str, t.Any]", response.json())

    def get_evaluation_item(
        self,
        org: str,
        workspace: str,
        evaluation_id: str,
        item_id: str,
    ) -> dict[str, t.Any]:
        """GET /org/{org}/ws/{workspace}/evaluation/{id}/items/{item_id} - Get evaluation item."""
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/evaluation/{evaluation_id}/items/{item_id}",
        )
        return t.cast("dict[str, t.Any]", response.json())

    def get_evaluation_analytics(
        self, org: str, workspace: str, evaluation_id: str
    ) -> dict[str, t.Any]:
        """GET /org/{org}/ws/{workspace}/evaluation/{id}/analytics - Get evaluation analytics."""
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/evaluation/{evaluation_id}/analytics",
        )
        return t.cast("dict[str, t.Any]", response.json())

    def get_evaluation_trace_stats(
        self, org: str, workspace: str, evaluation_id: str
    ) -> dict[str, t.Any]:
        """GET /org/{org}/ws/{workspace}/evaluation/{id}/traces - Get evaluation trace stats."""
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/evaluation/{evaluation_id}/traces",
        )
        return t.cast("dict[str, t.Any]", response.json())

    def list_evaluation_item_traces(
        self, org: str, workspace: str, evaluation_id: str
    ) -> dict[str, t.Any]:
        """GET /org/{org}/ws/{workspace}/evaluation/{id}/traces/items - List item traces."""
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/evaluation/{evaluation_id}/traces/items",
        )
        return t.cast("dict[str, t.Any]", response.json())

    # =========================================================================
    # Environments (task environment primitive; domain-neutral)
    # =========================================================================

    def create_environment(
        self,
        org: str,
        workspace: str,
        request: dict[str, t.Any],
    ) -> dict[str, t.Any]:
        """POST /org/{org}/ws/{workspace}/environments - Provision a task environment."""
        response = self.request(
            "POST",
            f"/org/{org}/ws/{workspace}/environments",
            json_data=request,
        )
        return t.cast("dict[str, t.Any]", response.json())

    def list_environments(
        self,
        org: str,
        workspace: str,
        *,
        state: list[str] | None = None,
        page: int = 1,
        limit: int = 50,
    ) -> dict[str, t.Any]:
        """GET /org/{org}/ws/{workspace}/environments - Paginated list."""
        params: dict[str, t.Any] = {"page": page, "limit": limit}
        if state:
            params["state"] = list(state)
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/environments",
            params=params,
        )
        return t.cast("dict[str, t.Any]", response.json())

    def get_environment(self, org: str, workspace: str, environment_id: str) -> dict[str, t.Any]:
        """GET /org/{org}/ws/{workspace}/environments/{id} - Get a task environment."""
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/environments/{environment_id}",
        )
        return t.cast("dict[str, t.Any]", response.json())

    def get_environment_status(
        self, org: str, workspace: str, environment_id: str
    ) -> dict[str, t.Any]:
        """GET /org/{org}/ws/{workspace}/environments/{id}/status - Lightweight state snapshot."""
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/environments/{environment_id}/status",
        )
        return t.cast("dict[str, t.Any]", response.json())

    def delete_environment(self, org: str, workspace: str, environment_id: str) -> None:
        """DELETE /org/{org}/ws/{workspace}/environments/{id} - Tear down a task environment."""
        self.request(
            "DELETE",
            f"/org/{org}/ws/{workspace}/environments/{environment_id}",
        )

    def execute_in_environment(
        self,
        org: str,
        workspace: str,
        environment_id: str,
        *,
        command: str,
        timeout_sec: int = 30,
        execute_token: str,
    ) -> dict[str, t.Any]:
        """POST /org/{org}/ws/{workspace}/environments/{id}/execute - Run a command inside a task environment."""
        response = self.request(
            "POST",
            f"/org/{org}/ws/{workspace}/environments/{environment_id}/execute",
            json_data={"command": command, "timeout_sec": timeout_sec},
            headers={"X-Environment-Token": f"Bearer {execute_token}"},
        )
        return t.cast("dict[str, t.Any]", response.json())

    def get_environment_logs(
        self, org: str, workspace: str, environment_id: str
    ) -> dict[str, t.Any]:
        """GET /org/{org}/ws/{workspace}/environments/{id}/logs - Tail sandbox server logs."""
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/environments/{environment_id}/logs",
        )
        return t.cast("dict[str, t.Any]", response.json())

    # =========================================================================
    # Training
    # =========================================================================

    def create_training_job(
        self,
        org: str,
        workspace: str,
        request: TrainingJobCreateRequest | dict[str, t.Any],
    ) -> TrainingJob:
        """POST /org/{org}/ws/{workspace}/training/jobs - Create a training job."""
        json_data: dict[str, t.Any]
        if isinstance(request, CreateTrainingJobBase):
            json_data = request.model_dump(mode="json", exclude_none=True)
        else:
            json_data = request
        response = self.request(
            "POST",
            f"/org/{org}/ws/{workspace}/training/jobs",
            json_data=json_data,
        )
        return TrainingJob(**response.json())

    def list_training_jobs(
        self,
        org: str,
        workspace: str,
        *,
        page: int = 1,
        page_size: int = 20,
        status: str | None = None,
        backend: str | None = None,
        trainer_type: str | None = None,
        project_ref: str | None = None,
    ) -> TrainingJobList:
        """GET /org/{org}/ws/{workspace}/training/jobs - List training jobs."""
        params: dict[str, t.Any] = {"page": page, "page_size": page_size}
        if status is not None:
            params["status"] = status
        if backend is not None:
            params["backend"] = backend
        if trainer_type is not None:
            params["trainer_type"] = trainer_type
        if project_ref is not None:
            params["project_ref"] = project_ref
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/training/jobs",
            params=params,
        )
        return TrainingJobList(**response.json())

    def get_training_job(self, org: str, workspace: str, job_id: str) -> TrainingJob:
        """GET /org/{org}/ws/{workspace}/training/jobs/{job_id} - Get a training job."""
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/training/jobs/{job_id}",
        )
        return TrainingJob(**response.json())

    def cancel_training_job(self, org: str, workspace: str, job_id: str) -> TrainingJob:
        """POST /org/{org}/ws/{workspace}/training/jobs/{job_id}/cancel - Cancel a training job."""
        response = self.request(
            "POST",
            f"/org/{org}/ws/{workspace}/training/jobs/{job_id}/cancel",
        )
        return TrainingJob(**response.json())

    def retry_training_job(self, org: str, workspace: str, job_id: str) -> TrainingJob:
        """POST /org/{org}/ws/{workspace}/training/jobs/{job_id}/retry - Retry a training job."""
        response = self.request(
            "POST",
            f"/org/{org}/ws/{workspace}/training/jobs/{job_id}/retry",
        )
        return TrainingJob(**response.json())

    def list_training_job_logs(self, org: str, workspace: str, job_id: str) -> TrainingJobLogList:
        """GET /org/{org}/ws/{workspace}/training/jobs/{job_id}/logs - List training logs."""
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/training/jobs/{job_id}/logs",
        )
        return TrainingJobLogList(**response.json())

    def get_training_job_artifacts(
        self, org: str, workspace: str, job_id: str
    ) -> TrainingJobArtifacts:
        """GET /org/{org}/ws/{workspace}/training/jobs/{job_id}/artifacts - Get training artifacts."""
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/training/jobs/{job_id}/artifacts",
        )
        return TrainingJobArtifacts(**response.json())

    def get_training_catalog(
        self,
        *,
        query: str | None = None,
        family: str | None = None,
        algorithm: str | None = None,
        min_size_b: float | None = None,
        max_size_b: float | None = None,
        limit: int = 20,
    ) -> TrainingCatalogResponse:
        """GET /training/catalog - Browse supported training base models."""
        params: dict[str, t.Any] = {"limit": limit}
        if query is not None:
            params["query"] = query
        if family is not None:
            params["family"] = family
        if algorithm is not None:
            params["algorithm"] = algorithm
        if min_size_b is not None:
            params["min_size_b"] = min_size_b
        if max_size_b is not None:
            params["max_size_b"] = max_size_b
        response = self.request("GET", "/training/catalog", params=params)
        return TrainingCatalogResponse(**response.json())

    def get_training_job_rl_context(
        self, org: str, workspace: str, job_id: str
    ) -> TrainingRLContext:
        """GET /org/{org}/ws/{workspace}/training/jobs/{job_id}/rl-context - Fetch RL context."""
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/training/jobs/{job_id}/rl-context",
        )
        return TrainingRLContext(**response.json())

    def post_training_job_progress(
        self,
        org: str,
        workspace: str,
        job_id: str,
        request: TrainingJobProgressUpdateRequest | dict[str, t.Any],
    ) -> TrainingJob:
        """POST /org/{org}/ws/{workspace}/training/jobs/{job_id}/progress - Post a progress update."""
        payload = (
            request.model_dump(mode="json", exclude_none=True)
            if isinstance(request, TrainingJobProgressUpdateRequest)
            else TrainingJobProgressUpdateRequest.model_validate(request).model_dump(
                mode="json",
                exclude_none=True,
            )
        )
        response = self.request(
            "POST",
            f"/org/{org}/ws/{workspace}/training/jobs/{job_id}/progress",
            json_data=payload,
        )
        return TrainingJob(**response.json())

    # =========================================================================
    # Optimization
    # =========================================================================

    def create_optimization_job(
        self,
        org: str,
        workspace: str,
        request: OptimizationJobCreateRequest | dict[str, t.Any],
    ) -> OptimizationJob:
        """POST /org/{org}/ws/{workspace}/optimization/jobs - Create an optimization job."""
        json_data: dict[str, t.Any]
        if isinstance(request, CreateOptimizationJobBase):
            json_data = request.model_dump(mode="json", exclude_none=True)
        else:
            json_data = request
        response = self.request(
            "POST",
            f"/org/{org}/ws/{workspace}/optimization/jobs",
            json_data=json_data,
        )
        return OptimizationJob(**response.json())

    def list_optimization_jobs(
        self,
        org: str,
        workspace: str,
        *,
        page: int = 1,
        page_size: int = 20,
        status: str | None = None,
        backend: str | None = None,
        target_kind: str | None = None,
        project: str | None = None,
    ) -> OptimizationJobList:
        """GET /org/{org}/ws/{workspace}/optimization/jobs - List optimization jobs."""
        params: dict[str, t.Any] = {"page": page, "page_size": page_size}
        if status is not None:
            params["status"] = status
        if backend is not None:
            params["backend"] = backend
        if target_kind is not None:
            params["target_kind"] = target_kind
        if project is not None:
            params["project"] = project
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/optimization/jobs",
            params=params,
        )
        return OptimizationJobList(**response.json())

    def get_optimization_job(self, org: str, workspace: str, job_id: str) -> OptimizationJob:
        """GET /org/{org}/ws/{workspace}/optimization/jobs/{job_id} - Get an optimization job."""
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/optimization/jobs/{job_id}",
        )
        return OptimizationJob(**response.json())

    def cancel_optimization_job(self, org: str, workspace: str, job_id: str) -> OptimizationJob:
        """POST /org/{org}/ws/{workspace}/optimization/jobs/{job_id}/cancel - Cancel an optimization job."""
        response = self.request(
            "POST",
            f"/org/{org}/ws/{workspace}/optimization/jobs/{job_id}/cancel",
        )
        return OptimizationJob(**response.json())

    def retry_optimization_job(self, org: str, workspace: str, job_id: str) -> OptimizationJob:
        """POST /org/{org}/ws/{workspace}/optimization/jobs/{job_id}/retry - Retry an optimization job."""
        response = self.request(
            "POST",
            f"/org/{org}/ws/{workspace}/optimization/jobs/{job_id}/retry",
        )
        return OptimizationJob(**response.json())

    def list_optimization_job_logs(
        self, org: str, workspace: str, job_id: str
    ) -> OptimizationJobLogList:
        """GET /org/{org}/ws/{workspace}/optimization/jobs/{job_id}/logs - List optimization logs."""
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/optimization/jobs/{job_id}/logs",
        )
        return OptimizationJobLogList(**response.json())

    def post_optimization_job_progress(
        self,
        org: str,
        workspace: str,
        job_id: str,
        request: OptimizationJobProgressUpdateRequest | dict[str, t.Any],
    ) -> OptimizationJob:
        """POST /org/{org}/ws/{workspace}/optimization/jobs/{job_id}/progress - Post a live progress update."""
        payload = (
            request.model_dump(mode="json", exclude_none=True)
            if isinstance(request, OptimizationJobProgressUpdateRequest)
            else OptimizationJobProgressUpdateRequest.model_validate(request).model_dump(
                mode="json",
                exclude_none=True,
            )
        )
        response = self.request(
            "POST",
            f"/org/{org}/ws/{workspace}/optimization/jobs/{job_id}/progress",
            json_data=payload,
        )
        return OptimizationJob(**response.json())

    def get_optimization_job_artifacts(
        self, org: str, workspace: str, job_id: str
    ) -> OptimizationJobArtifacts:
        """GET /org/{org}/ws/{workspace}/optimization/jobs/{job_id}/artifacts - Get optimization artifacts."""
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/optimization/jobs/{job_id}/artifacts",
        )
        return OptimizationJobArtifacts(**response.json())

    # =========================================================================
    # Capabilities
    # =========================================================================

    def list_capabilities(
        self,
        org: str,
        *,
        name: str | None = None,
        search: str | None = None,
        keywords: list[str] | None = None,
        author: list[str] | None = None,
        license_filter: list[str] | None = None,
        sort_by: str = "created_at",
        sort_dir: str = "desc",
        page: int = 1,
        limit: int = 50,
        include_public: bool = False,
    ) -> dict[str, t.Any]:
        """GET /org/{org}/capabilities - List capability artifacts."""
        params: dict[str, t.Any] = {
            "page": page,
            "limit": limit,
            "sort_by": sort_by,
            "sort_dir": sort_dir,
        }
        if name is not None:
            params["name"] = name
        if search is not None:
            params["search"] = search
        if keywords:
            params["keywords"] = keywords
        if author:
            params["author"] = author
        if license_filter:
            params["license"] = license_filter
        if include_public:
            params["include_public"] = True
        response = self.request("GET", f"/org/{org}/capabilities", params=params)
        return t.cast("dict[str, t.Any]", response.json())

    def get_capability_facets(
        self,
        org: str,
        *,
        name: str | None = None,
        search: str | None = None,
        keywords: list[str] | None = None,
        author: list[str] | None = None,
        license_filter: list[str] | None = None,
        include_public: bool = False,
    ) -> dict[str, t.Any]:
        """GET /org/{org}/capabilities/facets - Get capability filter facets."""
        params: dict[str, t.Any] = {"include_public": include_public}
        if name is not None:
            params["name"] = name
        if search is not None:
            params["search"] = search
        if keywords:
            params["keywords"] = keywords
        if author:
            params["author"] = author
        if license_filter:
            params["license"] = license_filter
        response = self.request("GET", f"/org/{org}/capabilities/facets", params=params)
        return t.cast("dict[str, t.Any]", response.json())

    def list_capability_versions(self, org: str, name: str) -> dict[str, t.Any]:
        """GET /org/{org}/capabilities/{name}/versions - List all versions."""
        safe_name = _url_quote(name, safe="")
        response = self.request("GET", f"/org/{org}/capabilities/{safe_name}/versions")
        return t.cast("dict[str, t.Any]", response.json())

    def get_capability(self, org: str, name: str, version: str | None = None) -> dict[str, t.Any]:
        """GET /org/{org}/capabilities/{name}[/{version}] - Get artifact detail."""
        safe_name = _url_quote(name, safe="")
        path = (
            f"/org/{org}/capabilities/{safe_name}/{version}"
            if version
            else f"/org/{org}/capabilities/{safe_name}"
        )
        response = self.request("GET", path)
        return t.cast("dict[str, t.Any]", response.json())

    def get_capability_file(self, org: str, name: str, version: str, file_path: str) -> bytes:
        """GET /org/{org}/capabilities/{name}/{version}/files/{path} - Download file."""
        safe_name = _url_quote(name, safe="")
        response = self.request(
            "GET", f"/org/{org}/capabilities/{safe_name}/{version}/files/{file_path}"
        )
        return response.content

    def get_capability_readme(
        self, org: str, name: str, version: str | None = None
    ) -> dict[str, t.Any]:
        """GET /org/{org}/capabilities/{name}[/{version}]/readme - Fetch bundle README."""
        safe_name = _url_quote(name, safe="")
        path = (
            f"/org/{org}/capabilities/{safe_name}/{version}/readme"
            if version
            else f"/org/{org}/capabilities/{safe_name}/readme"
        )
        response = self.request("GET", path)
        return t.cast("dict[str, t.Any]", response.json())

    def get_capability_bundle_url(self, org: str, name: str, version: str) -> dict[str, t.Any]:
        """GET /org/{org}/capabilities/{name}/{version}/bundle - Get bundle download URL."""
        response = self.request("GET", f"/org/{org}/capabilities/{name}/{version}/bundle")
        return t.cast("dict[str, t.Any]", response.json())

    def download_capability_bundle(self, org: str, name: str, version: str) -> bytes:
        """Download the tar.gz bundle for a capability via presigned URL."""
        info = self.get_capability_bundle_url(org, name, version)
        resp = httpx.get(info["download_url"], timeout=httpx.Timeout(120, connect=10))
        resp.raise_for_status()
        return resp.content

    def delete_capability(self, org: str, name: str, version: str) -> None:
        """DELETE /org/{org}/capabilities/{name}/{version} - Delete artifact."""
        safe_name = _url_quote(name, safe="")
        self.request("DELETE", f"/org/{org}/capabilities/{safe_name}/{version}")

    def update_capability_visibility(
        self,
        org: str,
        name: str,
        *,
        is_public: bool,
    ) -> dict[str, t.Any]:
        """PATCH /org/{org}/capabilities/{name}/visibility - Update visibility."""
        safe_name = _url_quote(name, safe="")
        response = self.request(
            "PATCH",
            f"/org/{org}/capabilities/{safe_name}/visibility",
            json_data={"is_public": is_public},
        )
        return t.cast("dict[str, t.Any]", response.json())

    def list_runtime_capabilities(
        self, org: str, workspace: str, runtime_id: str
    ) -> dict[str, t.Any]:
        """GET /org/{org}/ws/{workspace}/runtimes/{runtime_id}/capabilities - List bindings."""
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/runtimes/{runtime_id}/capabilities",
        )
        return t.cast("dict[str, t.Any]", response.json())

    def install_runtime_capability(
        self,
        org: str,
        workspace: str,
        runtime_id: str,
        *,
        name: str,
        version: str | None = None,
    ) -> dict[str, t.Any]:
        """POST /org/{org}/ws/{workspace}/runtimes/{runtime_id}/capabilities."""
        payload: dict[str, t.Any] = {"name": name}
        if version is not None:
            payload["version"] = version
        response = self.request(
            "POST",
            f"/org/{org}/ws/{workspace}/runtimes/{runtime_id}/capabilities",
            json_data=payload,
        )
        return t.cast("dict[str, t.Any]", response.json())

    def toggle_runtime_capability(
        self,
        org: str,
        workspace: str,
        runtime_id: str,
        binding_id: str,
        *,
        enabled: bool,
    ) -> dict[str, t.Any]:
        """PATCH /org/{org}/ws/{workspace}/runtimes/{runtime_id}/capabilities/{binding_id}."""
        response = self.request(
            "PATCH",
            f"/org/{org}/ws/{workspace}/runtimes/{runtime_id}/capabilities/{binding_id}",
            json_data={"enabled": enabled},
        )
        return t.cast("dict[str, t.Any]", response.json())

    def set_runtime_capability_flags(
        self,
        org: str,
        workspace: str,
        runtime_id: str,
        binding_id: str,
        *,
        flags: dict[str, bool | None],
    ) -> dict[str, t.Any]:
        """PATCH /org/{org}/ws/{workspace}/runtimes/{runtime_id}/capabilities/{binding_id}."""
        response = self.request(
            "PATCH",
            f"/org/{org}/ws/{workspace}/runtimes/{runtime_id}/capabilities/{binding_id}",
            json_data={"flags": flags},
        )
        return t.cast("dict[str, t.Any]", response.json())

    def update_runtime_capability(
        self,
        org: str,
        workspace: str,
        runtime_id: str,
        binding_id: str,
        *,
        version: str,
    ) -> dict[str, t.Any]:
        """PATCH /org/{org}/ws/{workspace}/runtimes/{runtime_id}/capabilities/{binding_id}."""
        response = self.request(
            "PATCH",
            f"/org/{org}/ws/{workspace}/runtimes/{runtime_id}/capabilities/{binding_id}",
            json_data={"version": version},
        )
        return t.cast("dict[str, t.Any]", response.json())

    def uninstall_runtime_capability(
        self, org: str, workspace: str, runtime_id: str, binding_id: str
    ) -> None:
        """DELETE /org/{org}/ws/{workspace}/runtimes/{runtime_id}/capabilities/{binding_id}."""
        self.request(
            "DELETE",
            f"/org/{org}/ws/{workspace}/runtimes/{runtime_id}/capabilities/{binding_id}",
        )

    def get_runtime_capabilities_resolved(
        self, org: str, workspace: str, runtime_id: str
    ) -> dict[str, t.Any]:
        """GET /org/{org}/ws/{workspace}/runtimes/{runtime_id}/capabilities/resolved."""
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/runtimes/{runtime_id}/capabilities/resolved",
        )
        return t.cast("dict[str, t.Any]", response.json())

    # =========================================================================
    # Tasks
    # =========================================================================

    def list_tasks(
        self,
        org: str,
        *,
        page: int = 1,
        limit: int = 50,
        difficulty: list[str] | None = None,
        tags: list[str] | None = None,
        search: str | None = None,
        author: list[str] | None = None,
        source: list[str] | None = None,
        include_public: bool = False,
    ) -> dict[str, t.Any]:
        """GET /org/{org}/tasks - List tasks."""
        params: dict[str, t.Any] = {}
        params["page"] = page
        params["limit"] = limit
        if difficulty is not None:
            params["difficulty"] = difficulty
        if tags is not None:
            params["tags"] = tags
        if search is not None:
            params["search"] = search
        if author is not None:
            params["author"] = author
        if source is not None:
            params["source"] = source
        if include_public:
            params["include_public"] = True
        response = self.request("GET", f"/org/{org}/tasks", params=params)
        return t.cast("dict[str, t.Any]", response.json())

    def get_task_facets(
        self,
        org: str,
        *,
        difficulty: list[str] | None = None,
        search: str | None = None,
        tags: list[str] | None = None,
        author: list[str] | None = None,
        source: list[str] | None = None,
        include_public: bool = False,
    ) -> dict[str, t.Any]:
        """GET /org/{org}/tasks/facets - Get task filter facets."""
        params: dict[str, t.Any] = {"include_public": include_public}
        if difficulty is not None:
            params["difficulty"] = difficulty
        if search is not None:
            params["search"] = search
        if tags is not None:
            params["tags"] = tags
        if author is not None:
            params["author"] = author
        if source is not None:
            params["source"] = source
        response = self.request("GET", f"/org/{org}/tasks/facets", params=params)
        return t.cast("dict[str, t.Any]", response.json())

    def get_task(self, org: str, name: str, version: str | None = None) -> dict[str, t.Any]:
        """GET /org/{org}/tasks/{name}[/{version}] - Get task details."""
        path = f"/org/{org}/tasks/{name}/{version}" if version else f"/org/{org}/tasks/{name}"
        response = self.request("GET", path)
        return t.cast("dict[str, t.Any]", response.json())

    def list_task_versions(self, org: str, name: str) -> dict[str, t.Any]:
        """GET /org/{org}/tasks/{name}/versions - List all versions of a task."""
        response = self.request("GET", f"/org/{org}/tasks/{name}/versions")
        return t.cast("dict[str, t.Any]", response.json())

    def get_task_readme(self, org: str, name: str) -> dict[str, t.Any]:
        """GET /org/{org}/tasks/{name}/readme - Fetch task archive README."""
        response = self.request("GET", f"/org/{org}/tasks/{name}/readme")
        return t.cast("dict[str, t.Any]", response.json())

    def get_task_instruction(
        self,
        org: str,
        task_name: str,
        *,
        sandbox_id: str | None = None,
    ) -> dict[str, t.Any]:
        """GET /org/{org}/tasks/{task_name}/instruction - Get task instructions."""
        params = {"sandbox_id": sandbox_id} if sandbox_id is not None else None
        response = self.request(
            "GET",
            f"/org/{org}/tasks/{task_name}/instruction",
            params=params,
        )
        return t.cast("dict[str, t.Any]", response.json())

    def delete_task(self, org: str, name: str, version: str) -> None:
        """DELETE /org/{org}/tasks/{name}/{version} - Delete a task version."""
        self.request("DELETE", f"/org/{org}/tasks/{name}/{version}")

    def update_task_visibility(
        self,
        org: str,
        name: str,
        *,
        is_public: bool,
    ) -> dict[str, t.Any]:
        """PATCH task or environment visibility for all versions of a name."""
        response = self.request(
            "PATCH",
            f"/org/{org}/tasks/{name}/visibility",
            json_data={"is_public": is_public},
        )
        return t.cast("dict[str, t.Any]", response.json())

    # =========================================================================
    # Task sets (platform)
    # =========================================================================

    def list_task_sets(
        self,
        org: str,
        *,
        source: list[str] | None = None,
        search: str | None = None,
        tags: list[str] | None = None,
        contains: str | None = None,
        sort_by: str = "created_at",
        sort_dir: str = "desc",
        page: int = 1,
        limit: int = 50,
        include_public: bool = False,
    ) -> dict[str, t.Any]:
        """GET /org/{org}/task-sets - List task sets (TSS-CAT-001/002)."""
        params: dict[str, t.Any] = {
            "sort_by": sort_by,
            "sort_dir": sort_dir,
            "page": page,
            "limit": limit,
            "include_public": include_public,
        }
        if source is not None:
            params["source"] = source
        if search is not None:
            params["search"] = search
        if tags is not None:
            params["tags"] = tags
        if contains is not None:
            params["contains"] = contains
        response = self.request("GET", f"/org/{org}/task-sets", params=params)
        return t.cast("dict[str, t.Any]", response.json())

    def get_task_set_facets(
        self,
        org: str,
        *,
        source: list[str] | None = None,
        search: str | None = None,
        tags: list[str] | None = None,
        include_public: bool = False,
    ) -> dict[str, t.Any]:
        """GET /org/{org}/task-sets/facets - Task set filter facets (TSS-CAT-005)."""
        params: dict[str, t.Any] = {"include_public": include_public}
        if source is not None:
            params["source"] = source
        if search is not None:
            params["search"] = search
        if tags is not None:
            params["tags"] = tags
        response = self.request("GET", f"/org/{org}/task-sets/facets", params=params)
        return t.cast("dict[str, t.Any]", response.json())

    def get_task_set(self, org: str, name: str) -> dict[str, t.Any]:
        """GET /org/{org}/task-sets/{name} - Detail with per-caller member resolution (TSS-CAT-004)."""
        response = self.request("GET", f"/org/{org}/task-sets/{name}")
        return t.cast("dict[str, t.Any]", response.json())

    def create_task_set(self, org: str, request: dict[str, t.Any]) -> dict[str, t.Any]:
        """POST /org/{org}/task-sets - Create a task set from a manifest body."""
        response = self.request("POST", f"/org/{org}/task-sets", json_data=request)
        return t.cast("dict[str, t.Any]", response.json())

    def update_task_set(self, org: str, name: str, request: dict[str, t.Any]) -> dict[str, t.Any]:
        """PUT /org/{org}/task-sets/{name} - Replace the full manifest (TSS-MUT-001)."""
        response = self.request("PUT", f"/org/{org}/task-sets/{name}", json_data=request)
        return t.cast("dict[str, t.Any]", response.json())

    def update_task_set_visibility(
        self, org: str, name: str, *, is_public: bool
    ) -> dict[str, t.Any]:
        """PATCH /org/{org}/task-sets/{name}/visibility - Flip is_public (TSS-VIS-002)."""
        response = self.request(
            "PATCH",
            f"/org/{org}/task-sets/{name}/visibility",
            json_data={"is_public": is_public},
        )
        return t.cast("dict[str, t.Any]", response.json())

    def delete_task_set(self, org: str, name: str) -> dict[str, t.Any]:
        """DELETE /org/{org}/task-sets/{name} - Hard delete (TSS-MUT-006)."""
        response = self.request("DELETE", f"/org/{org}/task-sets/{name}")
        return t.cast("dict[str, t.Any]", response.json())

    # =========================================================================
    # Sessions (platform)
    # =========================================================================

    def save_session(
        self,
        org: str,
        workspace: str,
        session_id: str,
        model: str,
        *,
        agent: str | None = None,
        title: str | None = None,
        message_count: int = 0,
        project_id: str | None = None,
        runtime_id: str | None = None,
        group_id: str | None = None,
        labels: dict[str, list[str]] | None = None,
        visibility: t.Literal["private", "workspace"] = "private",
        origin: t.Literal["user", "eval", "worker"] = "user",
    ) -> dict[str, t.Any]:
        """POST /org/{org}/ws/{workspace}/sessions - Create or save a session."""
        payload: dict[str, t.Any] = {
            "id": session_id,
            "model": model,
            "message_count": message_count,
            "visibility": visibility,
        }
        # SES-ORG-003: only send ``origin`` on the wire when non-default —
        # the platform's ``user`` default applies otherwise.
        if origin != "user":
            payload["origin"] = origin
        if agent is not None:
            payload["agent"] = agent
        if title is not None:
            payload["title"] = title
        if project_id is not None:
            payload["project_id"] = project_id
        if runtime_id is not None:
            payload["runtime_id"] = runtime_id
        if group_id is not None:
            payload["group_id"] = group_id
        if labels is not None:
            payload["labels"] = labels
        response = self.request("POST", f"/org/{org}/ws/{workspace}/sessions", json_data=payload)
        return t.cast("dict[str, t.Any]", response.json())

    def create_session_group(
        self,
        org: str,
        workspace: str,
        *,
        project_id: str,
        kind: t.Literal["worker_run", "evaluation_item", "workflow"] = "workflow",
        title: str | None = None,
        status: t.Literal["running", "completed", "failed", "cancelled"] | None = "running",
        runtime_id: str | None = None,
        capability: str | None = None,
        capability_version: str | None = None,
        worker: str | None = None,
        evaluation_id: str | None = None,
        evaluation_item_id: str | None = None,
        evaluation_item_attempt_id: str | None = None,
        metadata: dict[str, t.Any] | None = None,
    ) -> dict[str, t.Any]:
        """POST /org/{org}/ws/{workspace}/sessions/groups - Create a group."""
        payload: dict[str, t.Any] = {
            "kind": kind,
            "project_id": project_id,
            "status": status,
            "metadata": metadata or {},
        }
        if title is not None:
            payload["title"] = title
        if runtime_id is not None:
            payload["runtime_id"] = runtime_id
        if capability is not None:
            payload["capability"] = capability
        if capability_version is not None:
            payload["capability_version"] = capability_version
        if worker is not None:
            payload["worker"] = worker
        if evaluation_id is not None:
            payload["evaluation_id"] = evaluation_id
        if evaluation_item_id is not None:
            payload["evaluation_item_id"] = evaluation_item_id
        if evaluation_item_attempt_id is not None:
            payload["evaluation_item_attempt_id"] = evaluation_item_attempt_id
        response = self.request(
            "POST",
            f"/org/{org}/ws/{workspace}/sessions/groups",
            json_data=payload,
        )
        return t.cast("dict[str, t.Any]", response.json())

    def update_session_group(
        self,
        org: str,
        workspace: str,
        group_id: str,
        *,
        title: str | None = None,
        status: t.Literal["running", "completed", "failed", "cancelled"] | None = None,
    ) -> dict[str, t.Any]:
        """PATCH /org/{org}/ws/{workspace}/sessions/groups/{id}."""
        payload: dict[str, t.Any] = {}
        if title is not None:
            payload["title"] = title
        if status is not None:
            payload["status"] = status
        response = self.request(
            "PATCH",
            f"/org/{org}/ws/{workspace}/sessions/groups/{group_id}",
            json_data=payload,
        )
        return t.cast("dict[str, t.Any]", response.json())

    def update_session(
        self,
        org: str,
        workspace: str,
        session_id: str,
        *,
        model: str | None = None,
        agent: str | None = None,
        title: str | None = None,
        message_count: int | None = None,
        labels: dict[str, list[str]] | None = None,
        visibility: t.Literal["private", "workspace"] | None = None,
    ) -> dict[str, t.Any]:
        """PATCH /org/{org}/ws/{workspace}/sessions/{session_id} - Update a session.

        ``labels`` full-replaces non-reserved labels when provided (SES-LBL-042).
        ``visibility`` may only promote ``private`` → ``workspace``; downgrade
        returns 403 (SES-ACL-005). Omit fields to leave them unchanged.
        """
        payload: dict[str, t.Any] = {}
        if model is not None:
            payload["model"] = model
        if agent is not None:
            payload["agent"] = agent
        if title is not None:
            payload["title"] = title
        if message_count is not None:
            payload["message_count"] = message_count
        if labels is not None:
            payload["labels"] = labels
        if visibility is not None:
            payload["visibility"] = visibility
        response = self.request(
            "PATCH",
            f"/org/{org}/ws/{workspace}/sessions/{session_id}",
            json_data=payload,
        )
        return t.cast("dict[str, t.Any]", response.json())

    def archive_session(
        self,
        org: str,
        workspace: str,
        session_id: str,
    ) -> dict[str, t.Any]:
        """POST /org/{org}/ws/{workspace}/sessions/{id}/archive — idempotent."""
        response = self.request(
            "POST",
            f"/org/{org}/ws/{workspace}/sessions/{session_id}/archive",
        )
        return t.cast("dict[str, t.Any]", response.json())

    def delete_session(
        self,
        org: str,
        workspace: str,
        session_id: str,
    ) -> None:
        """DELETE /org/{org}/ws/{workspace}/sessions/{id}.

        Raises :class:`NotFoundError` if the session does not exist. Callers
        that want to tolerate already-gone sessions (e.g. delete propagation
        for sessions that were never registered with the platform) should
        catch :class:`NotFoundError` explicitly.
        """
        self.request(
            "DELETE",
            f"/org/{org}/ws/{workspace}/sessions/{session_id}",
        )

    def unarchive_session(
        self,
        org: str,
        workspace: str,
        session_id: str,
    ) -> dict[str, t.Any]:
        """POST /org/{org}/ws/{workspace}/sessions/{id}/unarchive — idempotent."""
        response = self.request(
            "POST",
            f"/org/{org}/ws/{workspace}/sessions/{session_id}/unarchive",
        )
        return t.cast("dict[str, t.Any]", response.json())

    def freeze_session(
        self,
        org: str,
        workspace: str,
        session_id: str,
    ) -> dict[str, t.Any]:
        """POST /org/{org}/ws/{workspace}/sessions/{id}/freeze — terminal, idempotent."""
        response = self.request(
            "POST",
            f"/org/{org}/ws/{workspace}/sessions/{session_id}/freeze",
        )
        return t.cast("dict[str, t.Any]", response.json())

    def list_sessions(
        self,
        org: str,
        workspace: str,
        *,
        page: int = 1,
        limit: int = 20,
        project_id: str | list[str] | None = None,
        user_id: str | None = None,
        archived: t.Literal["active", "archived", "any"] = "active",
        label: list[str] | None = None,
        origin: list[str] | None = None,
        sort_by: t.Literal[
            "updated_at", "last_message_at", "created_at", "message_count"
        ] = "updated_at",
        sort_dir: t.Literal["asc", "desc"] = "desc",
        search: str | None = None,
        include_workload_sessions: bool = False,
    ) -> dict[str, t.Any]:
        """GET /org/{org}/ws/{workspace}/sessions - List sessions.

        ``archived`` defaults to ``active`` so archived rows are hidden by
        default. ``label`` is a repeated ``key:value`` filter (SES-LBL-050).
        ``project_id`` accepts a single id or a list of ids (repeatable,
        OR combine — SES-LST-006). ``sort_by`` must be one of
        ``updated_at`` (default), ``last_message_at``, ``created_at``, or
        ``message_count``. ``search`` is the full-text filter (SES-LST-007).
        """
        params: dict[str, t.Any] = {
            "page": page,
            "limit": limit,
            "archived": archived,
            "sort_by": sort_by,
            "sort_dir": sort_dir,
        }
        if include_workload_sessions:
            params["include_workload_sessions"] = True
        if project_id is not None:
            params["project_id"] = project_id
        if user_id is not None:
            params["user_id"] = user_id
        if label:
            params["label"] = label
        if origin:
            params["origin"] = origin
        if search:
            params["search"] = search
        response = self.request("GET", f"/org/{org}/ws/{workspace}/sessions", params=params)
        return t.cast("dict[str, t.Any]", response.json())

    def get_session_facets(
        self,
        org: str,
        workspace: str,
        *,
        project_id: str | list[str] | None = None,
        user_id: str | None = None,
        archived: t.Literal["active", "archived", "any"] = "active",
        label: list[str] | None = None,
        origin: list[str] | None = None,
        search: str | None = None,
        include_workload_sessions: bool = False,
    ) -> dict[str, t.Any]:
        """GET /org/{org}/ws/{workspace}/sessions/facets - Per-key label value counts.

        Takes the same filter set as :meth:`list_sessions` (minus pagination
        / sort). ``project_id`` accepts a single id or a list. The response
        shape is ``{"labels": {key: [{"value": ..., "count": ...}, ...]}}``.
        """
        params: dict[str, t.Any] = {"archived": archived}
        if include_workload_sessions:
            params["include_workload_sessions"] = True
        if project_id is not None:
            params["project_id"] = project_id
        if user_id is not None:
            params["user_id"] = user_id
        if label:
            params["label"] = label
        if origin:
            params["origin"] = origin
        if search:
            params["search"] = search
        response = self.request("GET", f"/org/{org}/ws/{workspace}/sessions/facets", params=params)
        return t.cast("dict[str, t.Any]", response.json())

    def get_session(
        self,
        org: str,
        workspace: str,
        session_id: str,
        *,
        limit: int = 1000,
        after_sequence: int | None = None,
    ) -> dict[str, t.Any]:
        """GET /org/{org}/ws/{workspace}/sessions/{session_id} - Get session with events."""
        params: dict[str, t.Any] = {"limit": limit}
        if after_sequence is not None:
            params["after_sequence"] = after_sequence
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/sessions/{session_id}",
            params=params,
        )
        return t.cast("dict[str, t.Any]", response.json())

    def get_session_trajectory(
        self,
        org: str,
        workspace: str,
        session_id: str,
        *,
        format: t.Literal["atif", "openai", "native"] = "atif",
        include_compacted: bool = False,
    ) -> t.Any:
        """GET /org/{org}/ws/{workspace}/sessions/{id}/trajectory.

        Returns the session's trajectory in the requested format. ``atif``
        emits an ATIF v1.7 dict; ``openai`` emits a Chat Completions
        ``messages`` list; ``native`` emits a Dreadnode bundle of session
        metadata, transcript messages, and ClickHouse events.
        ``include_compacted=True`` requests full history.
        """
        params: dict[str, t.Any] = {
            "format": format,
            "include_compacted": include_compacted,
        }
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/sessions/{session_id}/trajectory",
            params=params,
        )
        return response.json()

    def get_evaluation_item_trajectory(
        self,
        org: str,
        workspace: str,
        evaluation_id: str,
        item_id: str,
        *,
        format: t.Literal["atif", "openai"] = "atif",
        include_compacted: bool = False,
    ) -> t.Any:
        """GET /org/{org}/ws/{workspace}/evaluation/{id}/items/{item_id}/trajectory.

        Convenience alias that resolves the linked session and delegates
        (SES-TRAJ-031). 404 if the eval item has no linked session.
        """
        params: dict[str, t.Any] = {
            "format": format,
            "include_compacted": include_compacted,
        }
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/evaluation/{evaluation_id}/items/{item_id}/trajectory",
            params=params,
        )
        return response.json()

    # ------------------------------------------------------------------
    # Session transcripts (message-level persistence)
    # ------------------------------------------------------------------

    @staticmethod
    def _message_to_transcript_dict(msg: t.Any) -> dict[str, t.Any]:
        """Convert an SDK Message to the API's MessageCreate shape.

        Handles the structural difference between SDK ToolCall
        (nested ``function.name`` / ``function.arguments``) and the
        API's flat ``name`` / ``arguments`` representation.
        """
        d: dict[str, t.Any] = {
            "role": str(msg.role),
            "content": msg.content or "",
        }

        if hasattr(msg, "uuid") and msg.uuid is not None:
            d["id"] = str(msg.uuid)

        if msg.tool_calls:
            d["tool_calls"] = [
                {
                    "id": tc.id,
                    "name": tc.function.name if hasattr(tc, "function") else tc.get("name", ""),
                    "arguments": (
                        tc.function.arguments
                        if hasattr(tc, "function")
                        else tc.get("arguments", "")
                    ),
                }
                for tc in msg.tool_calls
            ]

        if msg.tool_call_id:
            d["tool_call_id"] = msg.tool_call_id

        if hasattr(msg, "metadata") and msg.metadata:
            d["metadata"] = msg.metadata

        return d

    def append_transcript(
        self,
        org: str,
        workspace: str,
        session_id: str,
        messages: list[t.Any],
        *,
        context: dict[str, t.Any] | None = None,
        usage_by_uuid: dict[str, dict[str, t.Any]] | None = None,
    ) -> dict[str, t.Any]:
        """POST /org/{org}/ws/{workspace}/sessions/{session_id}/transcript — Append messages.

        Args:
            org: Organization key.
            workspace: Workspace key.
            session_id: Session UUID string.
            messages: List of SDK Message objects to persist.
            context: Optional dict with ``model``, ``agent``, ``system_prompt``
                     — include on first call or when agent/model changes.
            usage_by_uuid: Optional mapping of message uuid (str) → usage dict
                     with ``input_tokens`` / ``output_tokens`` /
                     ``cache_read_input_tokens`` / ``cache_creation_input_tokens`` /
                     ``cost_usd``. Entries are attached to the matching message
                     payload.
        """
        payload_messages: list[dict[str, t.Any]] = []
        for m in messages:
            d = self._message_to_transcript_dict(m)
            msg_id = d.get("id")
            if usage_by_uuid and isinstance(msg_id, str) and msg_id in usage_by_uuid:
                d["usage"] = usage_by_uuid[msg_id]
            payload_messages.append(d)

        payload: dict[str, t.Any] = {"messages": payload_messages}
        if context is not None:
            payload["context"] = context

        response = self.request(
            "POST",
            f"/org/{org}/ws/{workspace}/sessions/{session_id}/transcript",
            json_data=payload,
        )
        return t.cast("dict[str, t.Any]", response.json())

    def get_transcript(
        self,
        org: str,
        workspace: str,
        session_id: str,
        *,
        include_compacted: bool = False,
        after_seq: int | None = None,
        limit: int = 1000,
    ) -> dict[str, t.Any]:
        """GET /org/{org}/ws/{workspace}/sessions/{session_id}/transcript — Get transcript.

        Returns ``SessionTranscriptResponse`` dict with ``session``,
        ``messages``, ``current_system_prompt``, ``has_more``.
        """
        params: dict[str, t.Any] = {"limit": limit}
        if include_compacted:
            params["include_compacted"] = True
        if after_seq is not None:
            params["after_seq"] = after_seq

        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/sessions/{session_id}/transcript",
            params=params,
        )
        return t.cast("dict[str, t.Any]", response.json())

    def compact_transcript(
        self,
        org: str,
        workspace: str,
        session_id: str,
        *,
        up_to_seq: int,
        summary_message: t.Any,
    ) -> dict[str, t.Any]:
        """POST /org/{org}/ws/{workspace}/sessions/{session_id}/transcript/compact.

        Args:
            up_to_seq: Compact all messages with seq <= this value.
            summary_message: SDK Message object to insert as compaction summary.
        """
        response = self.request(
            "POST",
            f"/org/{org}/ws/{workspace}/sessions/{session_id}/transcript/compact",
            json_data={
                "up_to_seq": up_to_seq,
                "summary": self._message_to_transcript_dict(summary_message),
            },
        )
        return t.cast("dict[str, t.Any]", response.json())

    def rewind_transcript(
        self,
        org: str,
        workspace: str,
        session_id: str,
        *,
        from_seq: int,
    ) -> dict[str, t.Any]:
        """POST /org/{org}/ws/{workspace}/sessions/{session_id}/rewind.

        Hard-truncates the transcript at ``from_seq`` (target user-message
        seq). Returns ``RewindTranscriptResponse`` dict with
        ``deleted_count``, ``target_seq``, and ``restored_content``.
        """
        response = self.request(
            "POST",
            f"/org/{org}/ws/{workspace}/sessions/{session_id}/rewind",
            json_data={"from_seq": from_seq},
        )
        return t.cast("dict[str, t.Any]", response.json())

    # =========================================================================
    # Worlds
    # =========================================================================

    def create_world_manifest(
        self,
        org: str,
        workspace: str,
        *,
        name: str | None = None,
        project_id: str | None = None,
        preset: str | None = None,
        seed: int | None = None,
        num_users: int | None = None,
        num_hosts: int | None = None,
        domains: list[str] | None = None,
    ) -> dict[str, t.Any]:
        """POST /org/{org}/ws/{workspace}/worlds/manifests - Create a world manifest job."""
        payload: dict[str, t.Any] = {}
        if name is not None:
            payload["name"] = name
        if project_id is not None:
            payload["project_id"] = project_id
        if preset is not None:
            payload["preset"] = preset
        if seed is not None:
            payload["seed"] = seed
        if num_users is not None:
            payload["num_users"] = num_users
        if num_hosts is not None:
            payload["num_hosts"] = num_hosts
        if domains is not None:
            payload["domains"] = domains
        response = self.request(
            "POST",
            f"/org/{org}/ws/{workspace}/worlds/manifests",
            json_data=payload,
        )
        return t.cast("dict[str, t.Any]", response.json())

    def list_world_manifests(
        self,
        org: str,
        workspace: str,
        *,
        project_id: str | None = None,
        created_by: str | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> dict[str, t.Any]:
        """GET /org/{org}/ws/{workspace}/worlds/manifests - List manifests."""
        params: dict[str, t.Any] = {"page": page, "page_size": page_size}
        if project_id is not None:
            params["project_id"] = project_id
        if created_by is not None:
            params["created_by"] = created_by
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/worlds/manifests",
            params=params,
        )
        return t.cast("dict[str, t.Any]", response.json())

    def get_world_manifest(
        self,
        org: str,
        workspace: str,
        manifest_id: str,
    ) -> dict[str, t.Any]:
        """GET /org/{org}/ws/{workspace}/worlds/manifests/{manifest_id} - Get a manifest."""
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/worlds/manifests/{manifest_id}",
        )
        return t.cast("dict[str, t.Any]", response.json())

    def get_world_manifest_graph_nodes(
        self,
        org: str,
        workspace: str,
        manifest_id: str,
        *,
        limit: int = 1000,
        offset: int = 0,
    ) -> dict[str, t.Any]:
        """GET /org/{org}/ws/{workspace}/worlds/manifests/{manifest_id}/graph/nodes."""
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/worlds/manifests/{manifest_id}/graph/nodes",
            params={"limit": limit, "offset": offset},
        )
        return t.cast("dict[str, t.Any]", response.json())

    def get_world_manifest_graph_edges(
        self,
        org: str,
        workspace: str,
        manifest_id: str,
        *,
        limit: int = 5000,
        offset: int = 0,
    ) -> dict[str, t.Any]:
        """GET /org/{org}/ws/{workspace}/worlds/manifests/{manifest_id}/graph/edges."""
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/worlds/manifests/{manifest_id}/graph/edges",
            params={"limit": limit, "offset": offset},
        )
        return t.cast("dict[str, t.Any]", response.json())

    def get_world_manifest_subgraph(
        self,
        org: str,
        workspace: str,
        manifest_id: str,
        *,
        center: str,
        depth: int = 2,
    ) -> dict[str, t.Any]:
        """GET /org/{org}/ws/{workspace}/worlds/manifests/{manifest_id}/graph/subgraph."""
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/worlds/manifests/{manifest_id}/graph/subgraph",
            params={"center": center, "depth": depth},
        )
        return t.cast("dict[str, t.Any]", response.json())

    def search_world_manifest_principals(
        self,
        org: str,
        workspace: str,
        manifest_id: str,
        *,
        query: str | None = None,
        principal_type: str | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> dict[str, t.Any]:
        """GET /org/{org}/ws/{workspace}/worlds/manifests/{manifest_id}/principals/search."""
        params: dict[str, t.Any] = {"page": page, "page_size": page_size}
        if query is not None:
            params["query"] = query
        if principal_type is not None:
            params["principal_type"] = principal_type
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/worlds/manifests/{manifest_id}/principals/search",
            params=params,
        )
        return t.cast("dict[str, t.Any]", response.json())

    def get_world_manifest_principal(
        self,
        org: str,
        workspace: str,
        manifest_id: str,
        principal_id: str,
    ) -> dict[str, t.Any]:
        """GET /org/{org}/ws/{workspace}/worlds/manifests/{manifest_id}/principals/{principal_id}."""
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/worlds/manifests/{manifest_id}/principals/{principal_id}",
        )
        return t.cast("dict[str, t.Any]", response.json())

    def get_world_manifest_principal_details(
        self,
        org: str,
        workspace: str,
        manifest_id: str,
        principal_id: str,
    ) -> dict[str, t.Any]:
        """GET /org/{org}/ws/{workspace}/worlds/manifests/{manifest_id}/principals/{principal_id}/details."""
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/worlds/manifests/{manifest_id}/principals/{principal_id}/details",
        )
        return t.cast("dict[str, t.Any]", response.json())

    def get_world_manifest_host(
        self,
        org: str,
        workspace: str,
        manifest_id: str,
        host_id: str,
    ) -> dict[str, t.Any]:
        """GET /org/{org}/ws/{workspace}/worlds/manifests/{manifest_id}/hosts/{host_id}."""
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/worlds/manifests/{manifest_id}/hosts/{host_id}",
        )
        return t.cast("dict[str, t.Any]", response.json())

    def get_world_manifest_host_details(
        self,
        org: str,
        workspace: str,
        manifest_id: str,
        host_id: str,
    ) -> dict[str, t.Any]:
        """GET /org/{org}/ws/{workspace}/worlds/manifests/{manifest_id}/hosts/{host_id}/details."""
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/worlds/manifests/{manifest_id}/hosts/{host_id}/details",
        )
        return t.cast("dict[str, t.Any]", response.json())

    def list_world_manifest_commands(
        self,
        org: str,
        workspace: str,
        manifest_id: str,
    ) -> dict[str, t.Any]:
        """GET /org/{org}/ws/{workspace}/worlds/manifests/{manifest_id}/commands."""
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/worlds/manifests/{manifest_id}/commands",
        )
        return t.cast("dict[str, t.Any]", response.json())

    def create_world_trajectory(
        self,
        org: str,
        workspace: str,
        *,
        manifest_id: str,
        name: str | None = None,
        project_id: str | None = None,
        goal: str = "Domain Admins",
        count: int = 1,
        strategy: str = "random",
        max_steps: int = 100,
        seed: int = 42,
        threads: int = 1,
        only_successful: bool = False,
        mode: str = "kali",
        runtime_id: str | None = None,
        capability_name: str | None = None,
        agent_name: str | None = None,
        agent_model: str | None = None,
    ) -> dict[str, t.Any]:
        """POST /org/{org}/ws/{workspace}/worlds/trajectories - Create a trajectory job."""
        payload: dict[str, t.Any] = {
            "manifest_id": manifest_id,
            "goal": goal,
            "count": count,
            "strategy": strategy,
            "max_steps": max_steps,
            "seed": seed,
            "threads": threads,
            "only_successful": only_successful,
            "mode": mode,
        }
        if name is not None:
            payload["name"] = name
        if project_id is not None:
            payload["project_id"] = project_id
        if runtime_id is not None:
            payload["runtime_id"] = runtime_id
        if capability_name is not None:
            payload["capability_name"] = capability_name
        if agent_name is not None:
            payload["agent_name"] = agent_name
        if agent_model is not None:
            payload["agent_model"] = agent_model
        response = self.request(
            "POST",
            f"/org/{org}/ws/{workspace}/worlds/trajectories",
            json_data=payload,
        )
        return t.cast("dict[str, t.Any]", response.json())

    def list_world_trajectories(
        self,
        org: str,
        workspace: str,
        *,
        manifest_id: str | None = None,
        project_id: str | None = None,
        created_by: str | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> dict[str, t.Any]:
        """GET /org/{org}/ws/{workspace}/worlds/trajectories - List trajectories."""
        params: dict[str, t.Any] = {"page": page, "page_size": page_size}
        if manifest_id is not None:
            params["manifest_id"] = manifest_id
        if project_id is not None:
            params["project_id"] = project_id
        if created_by is not None:
            params["created_by"] = created_by
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/worlds/trajectories",
            params=params,
        )
        return t.cast("dict[str, t.Any]", response.json())

    def get_world_trajectory(
        self,
        org: str,
        workspace: str,
        trajectory_id: str,
    ) -> dict[str, t.Any]:
        """GET /org/{org}/ws/{workspace}/worlds/trajectories/{trajectory_id}."""
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/worlds/trajectories/{trajectory_id}",
        )
        return t.cast("dict[str, t.Any]", response.json())

    def list_world_manifest_trajectories(
        self,
        org: str,
        workspace: str,
        manifest_id: str,
        *,
        page: int = 1,
        page_size: int = 20,
    ) -> dict[str, t.Any]:
        """GET /org/{org}/ws/{workspace}/worlds/manifests/{manifest_id}/trajectories."""
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/worlds/manifests/{manifest_id}/trajectories",
            params={"page": page, "page_size": page_size},
        )
        return t.cast("dict[str, t.Any]", response.json())

    def list_world_jobs(
        self,
        org: str,
        workspace: str,
        *,
        project_id: str | None = None,
        created_by: str | None = None,
        kind: str | None = None,
        status: str | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> dict[str, t.Any]:
        """GET /org/{org}/ws/{workspace}/worlds/jobs - List world jobs."""
        params: dict[str, t.Any] = {"page": page, "page_size": page_size}
        if project_id is not None:
            params["project_id"] = project_id
        if created_by is not None:
            params["created_by"] = created_by
        if kind is not None:
            params["kind"] = kind
        if status is not None:
            params["status"] = status
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/worlds/jobs",
            params=params,
        )
        return t.cast("dict[str, t.Any]", response.json())

    def get_world_job(
        self,
        org: str,
        workspace: str,
        job_id: str,
    ) -> dict[str, t.Any]:
        """GET /org/{org}/ws/{workspace}/worlds/jobs/{job_id} - Get a world job."""
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/worlds/jobs/{job_id}",
        )
        return t.cast("dict[str, t.Any]", response.json())

    def cancel_world_job(
        self,
        org: str,
        workspace: str,
        job_id: str,
    ) -> dict[str, t.Any]:
        """POST /org/{org}/ws/{workspace}/worlds/jobs/{job_id}/cancel - Cancel a world job."""
        response = self.request(
            "POST",
            f"/org/{org}/ws/{workspace}/worlds/jobs/{job_id}/cancel",
        )
        return t.cast("dict[str, t.Any]", response.json())

    # =========================================================================
    # AIRT (AI Red Teaming)
    # =========================================================================

    def create_airt_assessment(
        self,
        org: str,
        workspace: str,
        *,
        name: str,
        project_id: str,
        runtime_id: str | None = None,
        description: str | None = None,
        session_id: str | None = None,
        target_model: str | None = None,
        attacker_model: str | None = None,
        judge_model: str | None = None,
        target_config: dict[str, t.Any] | None = None,
        attacker_config: dict[str, t.Any] | None = None,
        attack_manifest: dict[str, t.Any] | None = None,
        workflow_run_id: str | None = None,
        workflow_script: str | None = None,
    ) -> dict[str, t.Any]:
        """POST /org/{org}/ws/{workspace}/airt/assessments - Create an AIRT assessment."""
        payload: dict[str, t.Any] = {"name": name}
        if description is not None:
            payload["description"] = description
        if session_id is not None:
            payload["session_id"] = session_id
        if runtime_id is not None:
            payload["runtime_id"] = runtime_id
        if target_model is not None:
            payload["target_model"] = target_model
        if attacker_model is not None:
            payload["attacker_model"] = attacker_model
        if judge_model is not None:
            payload["judge_model"] = judge_model
        if target_config is not None:
            payload["target_config"] = target_config
        if attacker_config is not None:
            payload["attacker_config"] = attacker_config
        if attack_manifest is not None:
            payload["attack_manifest"] = attack_manifest
        if workflow_run_id is not None:
            payload["workflow_run_id"] = workflow_run_id
        if workflow_script is not None:
            payload["workflow_script"] = workflow_script
        response = self.request(
            "POST",
            f"/org/{org}/ws/{workspace}/airt/assessments",
            json_data=payload,
            params={"project_id": project_id},
        )
        return t.cast("dict[str, t.Any]", response.json())

    def update_airt_assessment(
        self,
        org: str,
        workspace: str,
        assessment_id: str,
        *,
        status: str | None = None,
        name: str | None = None,
        description: str | None = None,
    ) -> dict[str, t.Any]:
        """PATCH /org/{org}/ws/{workspace}/airt/assessments/{id} - Update an AIRT assessment."""
        payload: dict[str, t.Any] = {}
        if status is not None:
            payload["status"] = status
        if name is not None:
            payload["name"] = name
        if description is not None:
            payload["description"] = description
        response = self.request(
            "PATCH",
            f"/org/{org}/ws/{workspace}/airt/assessments/{assessment_id}",
            json_data=payload,
        )
        return t.cast("dict[str, t.Any]", response.json())

    def upload_airt_report(
        self,
        org: str,
        workspace: str,
        assessment_id: str,
        *,
        report_type: str,
        content: str | None = None,
        content_json: dict[str, t.Any] | None = None,
    ) -> dict[str, t.Any]:
        """POST /org/{org}/ws/{workspace}/airt/assessments/{id}/reports - Upload a report."""
        payload: dict[str, t.Any] = {"report_type": report_type}
        if content is not None:
            payload["content"] = content
        if content_json is not None:
            payload["content_json"] = content_json
        response = self.request(
            "POST",
            f"/org/{org}/ws/{workspace}/airt/assessments/{assessment_id}/reports",
            json_data=payload,
        )
        return t.cast("dict[str, t.Any]", response.json())

    def get_airt_assessment(
        self,
        org: str,
        workspace: str,
        assessment_id: str,
    ) -> dict[str, t.Any]:
        """GET /org/{org}/ws/{workspace}/airt/assessments/{id} - Get assessment details."""
        response = self.request(
            "GET", f"/org/{org}/ws/{workspace}/airt/assessments/{assessment_id}"
        )
        return t.cast("dict[str, t.Any]", response.json())

    def list_airt_assessments(
        self,
        org: str,
        workspace: str,
        *,
        project_id: str | None = None,
        page: int = 1,
        page_size: int = 50,
    ) -> dict[str, t.Any]:
        """GET /org/{org}/ws/{workspace}/airt/assessments - List assessments."""
        params: dict[str, t.Any] = {"page": page, "page_size": page_size}
        if project_id is not None:
            params["project_id"] = project_id
        response = self.request("GET", f"/org/{org}/ws/{workspace}/airt/assessments", params=params)
        return t.cast("dict[str, t.Any]", response.json())

    def delete_airt_assessment(self, org: str, workspace: str, assessment_id: str) -> None:
        """DELETE /org/{org}/ws/{workspace}/airt/assessments/{id}."""
        self.request(
            "DELETE",
            f"/org/{org}/ws/{workspace}/airt/assessments/{assessment_id}",
        )

    def get_airt_assessment_sandbox(
        self, org: str, workspace: str, assessment_id: str
    ) -> dict[str, t.Any]:
        """GET /org/{org}/ws/{workspace}/airt/assessments/{id}/sandbox."""
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/airt/assessments/{assessment_id}/sandbox",
        )
        return t.cast("dict[str, t.Any]", response.json())

    def list_airt_reports(
        self, org: str, workspace: str, assessment_id: str
    ) -> list[dict[str, t.Any]]:
        """GET /org/{org}/ws/{workspace}/airt/assessments/{id}/reports."""
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/airt/assessments/{assessment_id}/reports",
        )
        return t.cast("list[dict[str, t.Any]]", response.json())

    def get_airt_report(
        self, org: str, workspace: str, assessment_id: str, report_id: str
    ) -> dict[str, t.Any]:
        """GET /org/{org}/ws/{workspace}/airt/assessments/{id}/reports/{rid}."""
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/airt/assessments/{assessment_id}/reports/{report_id}",
        )
        return t.cast("dict[str, t.Any]", response.json())

    def get_airt_analytics(self, org: str, workspace: str, assessment_id: str) -> dict[str, t.Any]:
        """GET /org/{org}/ws/{workspace}/airt/assessments/{id}/analytics."""
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/airt/assessments/{assessment_id}/analytics",
        )
        return t.cast("dict[str, t.Any]", response.json())

    def get_airt_trace_stats(
        self, org: str, workspace: str, assessment_id: str
    ) -> dict[str, t.Any]:
        """GET /org/{org}/ws/{workspace}/airt/assessments/{id}/traces."""
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/airt/assessments/{assessment_id}/traces",
        )
        return t.cast("dict[str, t.Any]", response.json())

    def get_airt_attack_spans(
        self, org: str, workspace: str, assessment_id: str
    ) -> list[dict[str, t.Any]]:
        """GET /org/{org}/ws/{workspace}/airt/assessments/{id}/traces/attacks."""
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/airt/assessments/{assessment_id}/traces/attacks",
        )
        return t.cast("list[dict[str, t.Any]]", response.json())

    def get_airt_trial_spans(
        self,
        org: str,
        workspace: str,
        assessment_id: str,
        *,
        attack_name: str | None = None,
        min_score: float | None = None,
        jailbreaks_only: bool = False,
        limit: int = 100,
    ) -> list[dict[str, t.Any]]:
        """GET /org/{org}/ws/{workspace}/airt/assessments/{id}/traces/trials."""
        params: dict[str, t.Any] = {"limit": limit}
        if attack_name is not None:
            params["attack_name"] = attack_name
        if min_score is not None:
            params["min_score"] = min_score
        if jailbreaks_only:
            params["jailbreaks_only"] = True
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/airt/assessments/{assessment_id}/traces/trials",
            params=params,
        )
        return t.cast("list[dict[str, t.Any]]", response.json())

    def get_airt_project_summary(self, org: str, workspace: str, project: str) -> dict[str, t.Any]:
        """GET /org/{org}/ws/{workspace}/airt/projects/{project}/summary."""
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/airt/projects/{project}/summary",
        )
        return t.cast("dict[str, t.Any]", response.json())

    def get_airt_project_findings(
        self,
        org: str,
        workspace: str,
        project: str,
        *,
        severity: str | None = None,
        category: str | None = None,
        attack_name: str | None = None,
        min_score: float | None = None,
        sort_by: str = "score",
        sort_dir: str = "desc",
        page: int = 1,
        page_size: int = 50,
    ) -> dict[str, t.Any]:
        """GET /org/{org}/ws/{workspace}/airt/projects/{project}/findings."""
        params: dict[str, t.Any] = {
            "sort_by": sort_by,
            "sort_dir": sort_dir,
            "page": page,
            "page_size": page_size,
        }
        if severity is not None:
            params["severity"] = severity
        if category is not None:
            params["category"] = category
        if attack_name is not None:
            params["attack_name"] = attack_name
        if min_score is not None:
            params["min_score"] = min_score
        response = self.request(
            "GET",
            f"/org/{org}/ws/{workspace}/airt/projects/{project}/findings",
            params=params,
        )
        return t.cast("dict[str, t.Any]", response.json())

    def generate_airt_project_report(
        self,
        org: str,
        workspace: str,
        project: str,
        *,
        fmt: str = "both",
        model_profile: str | None = None,
    ) -> dict[str, t.Any]:
        """POST /org/{org}/ws/{workspace}/airt/projects/{project}/reports/generate."""
        payload: dict[str, t.Any] = {"format": fmt}
        if model_profile is not None:
            payload["model_profile"] = model_profile
        response = self.request(
            "POST",
            f"/org/{org}/ws/{workspace}/airt/projects/{project}/reports/generate",
            json_data=payload,
        )
        return t.cast("dict[str, t.Any]", response.json())


def create_api_client(*, profile: str | None = None) -> ApiClient:
    """Create an authenticated API client using stored API key configuration data."""
    from dreadnode.app.config import UserConfig

    user_config = UserConfig.read()
    api_config = user_config.get_server_config(profile)

    if not api_config.api_key:
        raise RuntimeError("API key missing, use [bold]dreadnode login <api-key>[/]")

    return ApiClient(
        api_config.url,
        api_key=api_config.api_key,
        default_org=api_config.default_organization,
    )


class CreditsClient:
    """Client for credit balance and plan management endpoints."""

    def __init__(self, api: ApiClient, org: str | None = None) -> None:
        self._api = api
        self._org = org

    def with_org(self, org: str) -> "CreditsClient":
        """Return a credits client scoped to the given organization."""
        return CreditsClient(self._api, org)

    def _require_org(self) -> str:
        if not self._org:
            raise RuntimeError("Organization is required for credits operations")
        return self._org

    def get_balance(self) -> CreditBalance:
        """GET /org/{org}/credits - Get credit balance."""
        org = self._require_org()
        response = self._api.request("GET", f"/org/{org}/credits")
        return CreditBalance(**response.json())

    def get_plan(self) -> CreditsPricing:
        """GET /org/{org}/credits/price - Get credits pricing details."""
        org = self._require_org()
        response = self._api.request("GET", f"/org/{org}/credits/price")
        return CreditsPricing(**response.json())

    def checkout(self, quantity: int = 1, *, success_url: str, cancel_url: str) -> CheckoutSession:
        """POST /org/{org}/credits/checkout - Create a credits checkout session."""
        org = self._require_org()
        response = self._api.request(
            "POST",
            f"/org/{org}/credits/checkout",
            json_data={
                "quantity": quantity,
                "success_url": success_url,
                "cancel_url": cancel_url,
            },
        )
        return CheckoutSession(**response.json())

    def get_auto_refill(self) -> AutoRefillConfig:
        """GET /org/{org}/credits/auto-refill - Get auto-refill configuration."""
        org = self._require_org()
        response = self._api.request("GET", f"/org/{org}/credits/auto-refill")
        return AutoRefillConfig(**response.json())

    def configure_auto_refill(
        self,
        *,
        enabled: bool,
        threshold: int,
        quantity: int,
        monthly_cap: int,
    ) -> AutoRefillConfig:
        """PUT /org/{org}/credits/auto-refill - Configure auto-refill settings."""
        org = self._require_org()
        response = self._api.request(
            "PUT",
            f"/org/{org}/credits/auto-refill",
            json_data={
                "enabled": enabled,
                "threshold": threshold,
                "quantity": quantity,
                "monthly_cap": monthly_cap,
            },
        )
        return AutoRefillConfig(**response.json())

    def disable_auto_refill(self) -> None:
        """DELETE /org/{org}/credits/auto-refill - Disable auto-refill."""
        org = self._require_org()
        self._api.request("DELETE", f"/org/{org}/credits/auto-refill")

    def get_payment_method(self) -> PaymentMethod:
        """GET /org/{org}/credits/payment-method - Get saved payment method details."""
        org = self._require_org()
        response = self._api.request("GET", f"/org/{org}/credits/payment-method")
        return PaymentMethod(**response.json())
