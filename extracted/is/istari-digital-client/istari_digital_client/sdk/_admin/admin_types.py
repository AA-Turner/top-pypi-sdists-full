"""Rich domain types for the IstariAdmin surface.

These subclass the generated DTOs and add manager binding (ClientHaving).
Fields are inherited — no re-declaration.
"""

from __future__ import annotations

from istari_digital_client.sdk._base import ClientHaving
from istari_digital_client.sdk._generated.v2.models.personal_access_token import (
    PersonalAccessToken as _GenPersonalAccessToken,
)
from istari_digital_client.sdk._generated.v2.models.user import User as _GenUser


class PersonalAccessToken(_GenPersonalAccessToken, ClientHaving):
    """A personal access token with manager binding.

    Fields (inherited from generated DTO):
        id: The token record UUID.
        created: When the token was created.
        machine_user_id: The machine user ID.
        token: The token value (only populated at creation time).
        token_id: The token ID.
        name: The human-readable token name.
        user_type: HUMAN or AGENT.
        created_by_id: The user who created the token.
    """

    pass  # Behavior can be added here if needed


class User(_GenUser, ClientHaving):
    """A user with manager binding.

    Fields (inherited from generated DTO):
        id: The user UUID.
        created: When the user was created.
        provider_name: Auth provider name (e.g., "azure_ad").
        provider_user_id: User ID from the auth provider.
        user_type: HUMAN or AGENT.
        personal_access_tokens: List of PATs for this user.
        display_name: Human-readable display name.
        email: User email address.
        first_name: First name.
        last_name: Last name.
        control_tags: Access control tags.
        infosec_level: Assigned infosec level.
    """

    pass
