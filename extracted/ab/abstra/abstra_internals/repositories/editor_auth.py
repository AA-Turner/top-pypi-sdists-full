import abc
from typing import Optional

from abstra_internals.cloud_api.http_client import HTTPClient
from abstra_internals.logger import AbstraLogger


class EditorAuthRepository(abc.ABC):
    @abc.abstractmethod
    def renew_token(self, current_token: str) -> Optional[str]:
        raise NotImplementedError()


class WebEditorAuthRepository(EditorAuthRepository):
    """Renews the web editor session token against cloud-api.

    Wired into both editor bundles: the web editor one, and the local one —
    which also serves the legacy web editor (see build_editor_repositories).
    In the local editor itself this is inert: there is no editor_auth cookie
    to renew."""

    def __init__(self, client: "HTTPClient"):
        self.client = client

    def renew_token(self, current_token: str) -> Optional[str]:
        """Ask cloud-api to re-issue the web editor session token.

        Returns the fresh token, or None on any failure — renewal is
        best-effort and the caller retries on a later request."""
        try:
            response = self.client.post(
                endpoint="/web-editor/renew-token",
                headers={"Web-Editor-Authorization": f"Bearer {current_token}"},
            )
            if not response.ok:
                AbstraLogger.warning(
                    f"[EditorAuthRepository] renew-token failed with status {response.status_code}"
                )
                return None
            token = response.json().get("token")
            if isinstance(token, str) and token:
                return token
            return None
        except Exception as e:
            AbstraLogger.capture_exception(e)
            return None


class ProductionEditorAuthRepository(EditorAuthRepository):
    """No-op: deployed apps have no editor session cookie to renew, and the
    production http_client points at /apps, where the renew endpoint does
    not exist."""

    def renew_token(self, current_token: str) -> Optional[str]:
        return None
