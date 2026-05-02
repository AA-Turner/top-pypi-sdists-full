import os
from dataclasses import dataclass, field
from typing import Optional

from spotipyio.auth.spotify_grant_type import SpotifyGrantType
from spotipyio.logic.consts.env_consts import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI


@dataclass
class ClientCredentials:
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    redirect_uri: Optional[str] = None
    grant_type: Optional[SpotifyGrantType] = field(default_factory=lambda: SpotifyGrantType.CLIENT_CREDENTIALS)
    access_code: Optional[str] = None

    def __post_init__(self) -> None:
        self._validate_existing_credentials()
        self._validate_access_code()

    def _validate_existing_credentials(self) -> None:
        field_to_env_var_mapping = {
            "client_id": SPOTIPY_CLIENT_ID,
            "client_secret": SPOTIPY_CLIENT_SECRET,
            "redirect_uri": SPOTIPY_REDIRECT_URI,
        }

        for field_name, env_var in field_to_env_var_mapping.items():
            self._set_default_or_raise(field_name, env_var)

    def _set_default_or_raise(self, field_name: str, env_var: str) -> None:
        field_value = getattr(self, field_name)
        if field_value is not None:
            return

        default_value = os.getenv(env_var)
        if default_value is None:
            raise ValueError(
                f"Missing credential for field `{field_name}`! You must explicitly set this field or set the "
                f"`{env_var}` environment variable."
            )

        setattr(self, field_name, default_value)

    def _validate_access_code(self) -> None:
        if self.grant_type != SpotifyGrantType.CLIENT_CREDENTIALS and self.access_code is None:
            raise ValueError(
                f"Missing access code! When using the `{SpotifyGrantType.AUTHORIZATION_CODE.value}` or "
                f"`{SpotifyGrantType.REFRESH_TOKEN.value}` flows, you must pass an access code or a refresh token in "
                f"the access_code field"
            )
