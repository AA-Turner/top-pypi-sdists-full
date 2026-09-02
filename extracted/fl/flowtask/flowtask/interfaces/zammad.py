from navigator.conf import (
    ZAMMAD_INSTANCE,
    ZAMMAD_TOKEN,
    ZAMMAD_DEFAULT_CUSTOMER,
    ZAMMAD_DEFAULT_GROUP,
    ZAMMAD_DEFAULT_CATALOG,
    ZAMMAD_ORGANIZATION,
    ZAMMAD_DEFAULT_ROLE,
)
from ..exceptions import ComponentError
from .http import HTTPService


class zammad(HTTPService):
    """
    zammad

    Overview

        The `zammad` class provides a generic interface for managing Zammad instances via its RESTful API.
        It extends the HTTPService class and offers methods for creating users and generating user tokens with
        specific permissions in a Zammad instance. This class is pre-configured with the necessary Zammad instance
        settings, such as tokens and default roles, making it easier to interact with the Zammad API.

    .. table:: Properties
    :widths: auto

        +------------------+----------+-----------+--------------------------------------------------------------------------------------+
        | Name             | Required | Description                                                                                      |
        +------------------+----------+-----------+--------------------------------------------------------------------------------------+
        | credentials      |   No     | A dictionary holding authentication credentials.                                                 |
        +------------------+----------+-----------+--------------------------------------------------------------------------------------+
        | auth             |   Yes    | Authentication token for the Zammad API, derived from the ZAMMAD_TOKEN configuration.            |
        +------------------+----------+-----------+--------------------------------------------------------------------------------------+
        | article_base     |   No     | Default base dictionary for articles, specifying type and visibility.                            |
        +------------------+----------+-----------+--------------------------------------------------------------------------------------+
        | permissions_base |   No     | Base permissions for creating user tokens.                                                       |
        +------------------+----------+-----------+--------------------------------------------------------------------------------------+

    Return

        The methods in this class facilitate interaction with the Zammad API, including creating users and generating
        user access tokens. Each method returns the relevant response from the Zammad API, or an error if the operation fails.

    """  # noqa

    accept: str = "application/json"
    token_type: str = "Bearer"
    auth_type: str = "apikey"

    article_base: dict = {"type": "note", "internal": False}
    permissions_base: dict = {
        "name": "api_user_token",
        "label": "User Token",
        "permissions": ["api"],
    }

    def __init__(self, **kwargs):
        self.credentials: dict = {}
        HTTPService.__init__(self, **kwargs)
        self.auth = {self.token_type: ZAMMAD_TOKEN}

    async def get_user_token(self, **kwargs):
        """get_user_token.


        Usage: using X-On-Behalf-Of to getting User Token.

        """
        self.url = f"{ZAMMAD_INSTANCE}api/v1/user_access_token"
        self.method = "post"
        permissions: list = kwargs.pop("permissions", [])
        user = kwargs.pop("user", ZAMMAD_DEFAULT_CUSTOMER)
        token_name = kwargs.pop("token_name")
        self.headers["X-On-Behalf-Of"] = user
        self.accept = "application/json"
        ## create payload for access token:
        data = {
            **self.permissions_base,
            **{"name": token_name, permissions: permissions},
        }
        result, _ = await self.async_request(self.url, self.method, data, use_json=True)
        return result["token"]

    async def create_user(self, **kwargs):
        """create_user.

        Create a new User.

        TODO: Adding validation with dataclasses.
        """
        self.url = f"{ZAMMAD_INSTANCE}api/v1/users"
        self.method = "post"
        result = None
        error = None
        organization = kwargs.pop("organization", ZAMMAD_ORGANIZATION)
        roles = kwargs.pop("roles", [ZAMMAD_DEFAULT_ROLE])
        if not isinstance(roles, list):
            roles = ["Customer"]
        data = {"organization": organization, "roles": roles, **kwargs}
        try:
            result, error = await self.async_request(self.url, self.method, data=data)
            if error:
                raise ComponentError(f"Error creating Zammad User: {error}")
        except Exception as e:
            error = str(e)
        return result, error
