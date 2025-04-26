from typing import Optional

from tecton.identities import okta
from tecton_core import conf
from tecton_core.metadata_service_impl.providers import AuthProvider


class InternalAuthProvider(AuthProvider):
    def get_auth_header(self) -> Optional[str]:
        token = okta.get_token_refresh_if_needed()
        if token:
            return f"Bearer {token}"

        token = conf.get_or_none("TECTON_API_KEY")
        if token:
            return f"Tecton-key {token}"

        return None
