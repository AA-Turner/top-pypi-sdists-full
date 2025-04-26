import logging
from typing import Any

from scope_client.api_bindings import Configuration

from .session import ArthurAPISession


class ArthurOAuthSessionAPIConfiguration(Configuration):
    """
    This class is a subclass of the Configuration API configuration class that overrides the access_token field, so that
    the client can refresh the access token before making a request, rather than trying to use a
    never-updated instance variable. The access_token field is set to a property object which, when fetched, checks if
    the token response object is within leeway seconds of expiring, and if so, refreshes the token before
    returning it.
    """

    def __init__(
        self,
        session: ArthurAPISession,
        leeway_seconds: int = 30,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        host = session.host()
        super().__init__(*args, host=host, **kwargs)
        self.session = session
        self.leeway_seconds = leeway_seconds
        self.logger = logging.getLogger(__name__)

    @property
    def access_token(self) -> str:
        return self.session.token(leeway=self.leeway_seconds)["access_token"]

    @access_token.setter
    def access_token(self, token: str) -> None:
        # the constructor of the base class attempts to set None for the access token, ignore it
        pass
