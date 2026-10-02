"""Tokens manager (IstariAdmin surface).

``Tokens`` manages personal access tokens (PATs) for users and agents.
"""

from __future__ import annotations

from typing import Any

from istari_digital_client.sdk._base import Page, _Manager
from istari_digital_client.sdk._admin.admin_types import PersonalAccessToken as TokenType
from istari_digital_client.sdk._exceptions import APIStatusError, PATsDeprecatedError

_PATS_DEPRECATED_MESSAGE = (
    "Personal access token creation is disabled: PATs are deprecated in favour of "
    "Access Keys. Register an Access Key instead (admin.keys / client.keys.exchange_pat())."
)


def _raise_if_pats_deprecated(exc: APIStatusError) -> None:
    """Re-raise a 405 from a PAT-creation endpoint as ``PATsDeprecatedError``.

    Creation returns 405 only when PATs are deprecated (Identity Service enabled);
    other statuses propagate unchanged.
    """
    if exc.status_code == 405:
        raise PATsDeprecatedError(
            _PATS_DEPRECATED_MESSAGE,
            status_code=exc.status_code,
            request_id=exc.request_id,
            response=exc.response,
        ) from exc


class Tokens(_Manager):
    """Manage legacy personal access tokens (API keys) — deprecated; prefer admin.keys.

    Aliases: api-key token pat


    Reached via ``admin.tokens``. Personal access tokens allow programmatic
    access to the registry API without interactive login.

    Usage::

        # 1. Create a user PAT
        pat = admin.tokens.create(name="my-automation-token")
        print(f"Token: {pat.token}")  # Only shown once!

        # 2. Create an agent PAT
        agent_pat = admin.tokens.create_agent_token(name="agent-token")

        # 3. List all PATs
        for token in admin.tokens.list():
            print(token.name, token.created)

        # 4. Delete a PAT
        admin.tokens.delete(pat.id)
    """

    def create(self, *, name: str) -> TokenType:
        """Create a legacy personal access token / API key (deprecated; prefer admin.keys).

        Mutates: true

        Aliases: api-key token pat


        Args:
            name: A human-readable name for the token.

        Returns:
            A PersonalAccessToken with the ``token`` field populated.
            **Important**: The token value is only returned once at creation
            time. Store it securely.

        Raises:
            PATsDeprecatedError: If PAT creation is disabled (the Identity Service
                is enabled). Register an Access Key instead.
        """
        try:
            dto = self._call(
                self._engine.v2_api.create_personal_access_token,
                name,
            )
        except APIStatusError as exc:
            _raise_if_pats_deprecated(exc)
            raise
        return TokenType._bind(dto, mgr=self)

    def create_agent_token(self, *, name: str) -> TokenType:
        """Create a new personal access token for an agent.

        Mutates: true

        Args:
            name: A human-readable name for the token.

        Returns:
            A PersonalAccessToken with the ``token`` field populated.
            **Important**: The token value is only returned once at creation
            time. Store it securely.

        Raises:
            PATsDeprecatedError: If PAT creation is disabled (the Identity Service
                is enabled). Register an Access Key instead.
        """
        try:
            dto = self._call(
                self._engine.v2_api.create_agent_personal_access_token,
                name,
            )
        except APIStatusError as exc:
            _raise_if_pats_deprecated(exc)
            raise
        return TokenType._bind(dto, mgr=self)

    def list(
        self,
        *,
        page: int | None = None,
        size: int | None = None,
        sort: str | None = None,
    ) -> Page[TokenType]:
        """List personal access tokens for the current user.

        Iterating the returned Page automatically fetches subsequent pages.

        Args:
            page: Optional page number (1-indexed).
            size: Optional page size (max 100).
            sort: Sort field and order (e.g., "-created").

        Returns:
            A Page of PersonalAccessToken objects. Note that the ``token``
            field will be empty for listed tokens (only shown at creation).
        """

        def fetch(page_num: int) -> Any:
            return self._call(
                self._engine.v2_api.list_personal_access_tokens,
                page=page_num,
                size=size,
                sort=sort,
            )

        return self._paginate_offset(
            fetch, lambda d: TokenType._bind(d, mgr=self), start_page=page or 1
        )

    def delete(self, token_id: str) -> None:
        """Delete (revoke) a personal access token.

        Mutates: true

        Args:
            token_id: The UUID of the token to delete.

        Raises:
            NotFoundError: If no token with that id exists.
        """
        self._call(self._engine.v2_api.delete_personal_access_token, token_id)
