from cnvrgv2.config.config import SSO_VERSION
from cnvrgv2.proxy import Proxy, HTTP
from cnvrgv2.modules.users.user import User
from cnvrgv2.utils.json_api_format import JAF
from cnvrgv2.errors import CnvrgArgumentsError, CnvrgHttpError, CnvrgLoginError, CnvrgError
from cnvrgv2.config import routes, error_messages
from cnvrgv2.config.error_messages import FAULTY_VALUE
from cnvrgv2.utils.validators import validate_url, validate_email, validate_username


class UsersClient:
    def __init__(self, domain, token=None):
        if not validate_url(domain):
            raise CnvrgArgumentsError(error_messages.INVALID_URL)

        self._domain = domain
        self._token = token
        self._proxy = Proxy(domain=domain, token=token)
        self.sso_version = self._get_sso_version()
        self._proxy._sso_version = self.sso_version

    def _get_sso_version(self):
        """
        Find sso version based on version api response
        @return: sso version
        """
        response = self._proxy.call_api(
            route=routes.VERSION,
            http_method=HTTP.GET,
        )

        return response.attributes.get("sso_version", SSO_VERSION.CAPI)

    def login(self, user, password, token=None):
        """
        Authenticates the user with the given username/password
        @param user: The users Email
        @param password: the users password
        @raise CnvrgHttpError: If the user data is incorrect
        @return: token, first user organization (if exists), boolean sso_enabled and digest cryptographic hash
        @param token: the users token
        """

        try:
            # If authentication fails, the proxy will throw unauthorized error
            response = self._proxy.call_api(
                route=routes.USER_LOGIN,
                http_method=HTTP.POST,
                payload={
                    "username": user,
                    "password": password,
                    "token": token
                },
            )

            token = response.meta.get("jwt")
            organization = response.meta.get("organization", None)
            sso_enabled = response.meta.get("sso_enabled", True)
            digest = response.meta.get("digest", None)

        # update token and proxy for further usage
            self._token = token
            self._proxy = Proxy(domain=self._domain, token=self._token)

            return token, organization, sso_enabled, digest
        except (CnvrgHttpError, CnvrgError):
            raise CnvrgLoginError(error_messages.INVALID_CREDENTIALS) from None

    def register(self, username, email, password):
        """
        Creates a new user using the provided argumnets
        @param username: The username
        @param email: The email
        @param password: The password
        @raise CnvrgHttpError: if the user already exists
        @return: True if the registration is successful
        """

        if not validate_email(email):
            raise CnvrgArgumentsError(FAULTY_VALUE.format(email))

        if not validate_username(username):
            raise CnvrgArgumentsError(FAULTY_VALUE.format(username))

        attributes = {
            "email": email,
            "username": username,
            "password": password
        }

        response = self._proxy.call_api(
            route=routes.USER_BASE,
            http_method=HTTP.POST,
            payload=JAF.serialize(type="user", attributes=attributes)
        )

        return User(
            domain=self._domain,
            token=response.meta["jwt"],
            attributes=response.attributes
        )

    def me(self):
        """
        Retrieves current user information
        @raise CnvrgError: If the current context does not hold a user
        @return: Token, first user organization (if exists)
        """
        if self._token is None:
            raise CnvrgArgumentsError(error_messages.CONTEXT_CANT_SAVE)

        response = self._proxy.call_api(
            route=routes.USER_CURRENT,
            http_method=HTTP.GET
        )

        return User(domain=self._domain, token=self._token, attributes=response.attributes)
