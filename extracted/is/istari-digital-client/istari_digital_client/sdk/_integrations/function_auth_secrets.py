"""Function Auth Secrets manager (IstariIntegrations surface)."""

from __future__ import annotations


from istari_digital_client.sdk._base import Page, _Manager
from istari_digital_client.sdk._integrations.integration_types import FunctionAuthSecret as SecretType
from istari_digital_client.sdk._generated.v2.models.auth_integration_type import AuthIntegrationType
from istari_digital_client.sdk._generated.v2.models.function_auth_type import FunctionAuthType
from istari_digital_client.sdk._generated.v2.models.new_function_auth_secret import NewFunctionAuthSecret


class FunctionAuthSecrets(_Manager):
    """Store and manage credentials (function auth secrets) for function execution.

    Aliases: credential secret api-key token login password oauth windchill
    """

    def create(self, new_function_auth_secret: NewFunctionAuthSecret) -> SecretType:
        """Store a new credential (auth secret) used when running a function.

        Mutates: true

        Aliases: add store save credential api-key token oauth
        """
        dto = self._call(
            self._engine.v2_api._create_function_auth_secret,
            new_function_auth_secret,
        )
        return SecretType._bind(dto, mgr=self)

    def get(self, secret_id: str) -> SecretType:
        """Fetch a stored credential (function auth secret) by UUID."""
        dto = self._call(self._engine.v2_api.fetch_function_auth_secret, secret_id)
        return SecretType._bind(dto, mgr=self)

    def list(
        self,
        *,
        auth_integration_type: AuthIntegrationType | None = None,
        function_auth_type: FunctionAuthType | None = None,
        latest: bool | None = None,
    ) -> Page[SecretType]:
        """List stored credentials (function auth secrets), e.g. Windchill/OAuth logins.

        Aliases: credentials secrets api-keys tokens logins

        Note: The underlying API returns all results as a list (not paginated).
        This method wraps the results in a Page for consistency with other managers.

        Args:
            auth_integration_type: Optional filter by auth integration type
                (e.g. AuthIntegrationType.WINDCHILL).
            function_auth_type: Optional filter by function auth type
                (e.g. FunctionAuthType.OAUTH2).
            latest: Optional filter to only latest secrets.

        Returns:
            A Page containing all matching function auth secrets.
        """
        # API returns List[FunctionAuthSecret], not paginated
        secrets_list = self._call(
            self._engine.v2_api.find_function_auth_secret,
            auth_integration_type=auth_integration_type,
            function_auth_type=function_auth_type,
            latest=latest,
        )
        # Bind all secrets to manager
        bound_secrets = [SecretType._bind(s, mgr=self) for s in secrets_list]
        # Wrap in a single-page Page
        return Page(bound_secrets, fetch_next=None, total=len(bound_secrets))
