import pathlib
import time
from functools import cached_property
from json import JSONDecodeError
from webbrowser import open_new

import httpx
from pydantic import BaseModel, PositiveInt, ValidationError
from rich.align import Align
from rich.console import Console, Group
from rich.panel import Panel

import arraylake
from arraylake.cli.utils import print_user_details
from arraylake.config import config
from arraylake.exceptions import AuthException
from arraylake.types import (
    AuthProviderConfig,
    OauthTokens,
    OauthTokensResponse,
    UserInfo,
)


class Auth0UrlCode(BaseModel):
    url: str
    user_code: str
    device_code: str
    interval: PositiveInt
    expires_in: PositiveInt


class TokenHandler:
    """
    Class used to handle OAuth2
    """

    token_path: pathlib.Path
    tokens: OauthTokens | None
    proxy: str | None

    def __init__(
        self,
        api_endpoint: str = "https://api.earthmover.io",
        scopes: list[str] = ["email", "openid", "profile", "offline_access"],
        raise_if_not_logged_in: bool = False,
    ):
        # Auto-detect proxy from configuration and environment
        # Import locally to avoid circular imports
        from arraylake.api_utils import _get_proxy_from_env

        self.api_endpoint = api_endpoint
        self.scopes = scopes

        self.token_path = pathlib.Path(config.get("service.token_path", None) or "~/.arraylake/token.json").expanduser()

        # Headers for requests to arraylake and auth0 services
        self.arraylake_headers = {
            "accept": "application/vnd.earthmover+json",
            "client-version": arraylake.__version__,
        }
        self.auth0_headers = {"content-type": "application/x-www-form-urlencoded"}

        self.verify_ssl = bool(config.get("service.ssl.verify", True))
        self.ssl_cafile: str | None = config.get("service.ssl.cafile", None)

        self.proxy = _get_proxy_from_env()

        self.console = Console()
        self.error_console = Console(stderr=True, style="red")

        # Get cached tokens
        self.tokens = None
        try:
            with self.token_path.open() as f:
                self.tokens = OauthTokens.model_validate_json(f.read())
        except (ValidationError, JSONDecodeError):
            if raise_if_not_logged_in:
                raise AuthException("⚠️ Found malformed auth tokens, logout and log back in")
        except FileNotFoundError:
            if raise_if_not_logged_in:
                raise AuthException("⚠️ Not logged in, please log in with `arraylake auth login`")

    def _create_client(self, **kwargs) -> httpx.Client:
        """Create an httpx.Client with proxy and SSL configuration"""
        client_kwargs = {"verify": self.verify_ssl, "cert": self.ssl_cafile, **kwargs}

        # Add proxy configuration if available
        if self.proxy:
            # Import locally to avoid circular imports and handle version compatibility
            from arraylake.api_utils import _maybe_cast_proxy

            client_kwargs["proxy"] = _maybe_cast_proxy(self.proxy)

        return httpx.Client(**client_kwargs)

    def _create_async_client(self, **kwargs) -> httpx.AsyncClient:
        """Create an httpx.AsyncClient with proxy and SSL configuration"""
        client_kwargs = {"verify": self.verify_ssl, "cert": self.ssl_cafile, **kwargs}

        # Add proxy configuration if available
        if self.proxy:
            # Import locally to avoid circular imports and handle version compatibility
            from arraylake.api_utils import _maybe_cast_proxy

            client_kwargs["proxy"] = _maybe_cast_proxy(self.proxy)

        return httpx.AsyncClient(**client_kwargs)

    @cached_property
    def auth_provider_config(self) -> AuthProviderConfig:
        """
        Get Auth0 configuration dynamically for Arraylake client/cli
        """
        try:
            with self._create_client() as client:
                response = client.get(f"{self.api_endpoint}/auth/config?target=client")
                response.raise_for_status()
                return AuthProviderConfig.model_validate_json(response.text)
        except httpx.HTTPStatusError as e:
            raise AuthException(f"⚠️ Error getting auth configuration: {e.response.status_code} from {e.request.url!r}")
        except httpx.ConnectError:
            raise AuthException(f"⚠️ Could not connect to {self.api_endpoint}. Check your network connection and service URI.")

    async def get_authorize_info(self) -> Auth0UrlCode:
        """
        Get login url and codes for Auth0 Device flow
        """
        try:
            async with self._create_async_client() as client:
                response = await client.post(
                    f"https://{self.auth_provider_config.domain}/oauth/device/code",
                    headers=self.auth0_headers,
                    data={"client_id": self.auth_provider_config.client_id, "scope": " ".join(self.scopes)},
                )

            response.raise_for_status()
            device_code_data = response.json()

            return Auth0UrlCode(
                url=device_code_data["verification_uri_complete"],
                user_code=device_code_data["user_code"],
                device_code=device_code_data["device_code"],
                interval=device_code_data["interval"],
                expires_in=device_code_data["expires_in"],
            )

        except httpx.HTTPStatusError as e:
            self.error_console.print(f"Error response {e.response.status_code} while requesting {e.request.url!r}.")
            raise AuthException("Error getting authorization login url!")

    async def get_token(self, device_code: str, interval: int, expires_in: int) -> None:
        """
        Request token from Auth0 during Device code flow
        """
        token_payload = {
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
            "device_code": device_code,
            "client_id": self.auth_provider_config.client_id,
        }

        try:
            start_time = time.time()

            async with self._create_async_client() as client:
                while True:
                    # Check for time
                    elapsed_time = time.time() - start_time
                    if elapsed_time > expires_in:
                        raise AuthException("Authentication link expired. Please try again.")

                    response = await client.post(
                        f"https://{self.auth_provider_config.domain}/oauth/token", headers=self.auth0_headers, data=token_payload
                    )

                    try:
                        token_data = response.json()
                    except JSONDecodeError:
                        raise AuthException(f"Error getting token! {response.text}")

                    if response.status_code == 200:
                        tokens = OauthTokensResponse.model_validate(token_data)
                        break
                    elif token_data["error"] not in ("authorization_pending", "slow_down"):
                        raise AuthException(f"Error getting token! {token_data['error']}")
                    else:
                        time.sleep(interval)

        except httpx.HTTPStatusError as e:
            self.error_console.print(f"Error response {e.response.status_code} while requesting {e.request.url!r}.")
            raise AuthException(f"Error getting token! {e}")

        self.update(tokens)

    @property
    def refresh_request(self) -> httpx.Request:
        if self.tokens is None:
            raise ValueError("Must be logged in to refresh tokens!")

        refresh_url = f"https://{self.auth_provider_config.domain}/oauth/token"

        payload = {
            "grant_type": "refresh_token",
            "client_id": self.auth_provider_config.client_id,
            "refresh_token": self.tokens.refresh_token.get_secret_value(),
        }

        return httpx.Request("POST", refresh_url, data=payload, headers=self.auth0_headers)

    async def refresh_token(self) -> None:
        """
        Get a refresh token
        @see https://auth0.com/docs/get-started/authentication-and-authorization-flow/device-authorization-flow/call-your-api-using-the-device-authorization-flow#refresh-tokens # noqa: E501
        """

        try:
            async with self._create_async_client() as client:
                response = await client.send(self.refresh_request)
                new_tokens = OauthTokensResponse.model_validate_json(response.text)
        except httpx.HTTPStatusError as e:
            self.console.print(f"Error response {e.response.status_code} while requesting {e.request.url!r}.")
            raise AuthException(f"Error getting refresh token! {e}")

        # A refresh token is persisted over time
        # performing a fresh yields a new id + access token
        # perform an update with the new values, but maintain
        # the refresh token
        self.update(new_tokens)
        user = await self._get_user()  # checks that the new tokens are valid

        self.console.print(f"[green][bold]Successfully refreshed tokens![/bold][/green] [dim]Token stored at {self.token_path}[/dim]")
        print_user_details(user)

    def update(self, new_token_data: OauthTokensResponse | dict) -> None:
        if isinstance(new_token_data, OauthTokensResponse):
            # converting to a dict allows us to update only non-default fields
            new_token_data = new_token_data.model_dump(exclude_none=True)

        if self.tokens is None:
            self.tokens = OauthTokens.model_validate(new_token_data)
        else:
            # a little work to make sure we write back
            # an OauthTokens object with the correct value types
            staged_token_data = self.tokens.model_dump()
            staged_token_data.update(new_token_data)
            self.tokens = OauthTokens.model_validate(staged_token_data)
        self.cache()

    def cache(self) -> None:
        if not self.tokens:
            raise ValueError("Error saving tokens, no tokens to cache")
        self.token_path.parent.mkdir(exist_ok=True)
        with self.token_path.open(mode="w") as fp:
            fp.write(self.tokens.model_dump_json(exclude_unset=True))
        self.token_path.chmod(0o100600)  # -rw-------

    def purge_cache(self) -> None:
        self.token_path.unlink()
        self.tokens = None

    async def _get_user(self) -> UserInfo:
        if self.tokens is None:
            raise AuthException("Not logged in")
        headers = {"Authorization": f"Bearer {self.tokens.id_token.get_secret_value()}", **self.arraylake_headers}
        async with self._create_async_client() as client:
            response = await client.get(f"{self.api_endpoint}/user", headers=headers)
        if response.status_code != httpx.codes.OK:
            raise AuthException(f"Error fetching user: {response.status_code} {response.text}")
        return UserInfo.model_validate_json(response.content)

    async def _update_user_profile(self) -> UserInfo:
        if self.tokens is None:
            raise AuthException("Not logged in")
        headers = {"Authorization": f"Bearer {self.tokens.id_token.get_secret_value()}", **self.arraylake_headers}
        async with self._create_async_client() as client:
            response = await client.post(f"{self.api_endpoint}/auth/update-user", headers=headers)
        if response.status_code != httpx.codes.OK:
            raise AuthException(f"Error updating user profile: {response.status_code} {response.text}")
        return UserInfo.model_validate_json(response.content)

    async def login(self, *, browser: bool = False) -> None:
        if self.tokens is not None:
            # try to refresh tokens if they are present but fail gracefully, the user is already expecting to log in
            try:
                await self.refresh_token()
                return  # refresh_token already prints success message and user details
            except Exception:
                pass

        try:
            auth_info = await self.get_authorize_info()

            content = []

            if not browser:
                content.append(
                    Align(f"\nCopy and paste the following [link={auth_info.url}]link[/link] into your browser:\n", align="center")
                )
                content.append(Align(f"[blue]{auth_info.url}[/blue]\n", align="center"))

            content.append(Align("Ensure the code in your browser matches:", align="center"))
            content.append(Align(Panel.fit(f"[bold yellow]{auth_info.user_code}[/bold yellow]", border_style="yellow"), align="center"))
            content.append(Align("\nThen follow the instructions in your browser to login.", align="center"))
            docs_link = "https://docs.earthmover.io/setup/org-access#authenticating-as-a-user"
            content.append(Align(f"[dim]Visit [link={docs_link}]docs.earthmover.io[/link] for help.[/dim]\n", align="center"))

            panel = Align(Panel(Group(*content), title="[bold]Login[/bold]", expand=False), align="center")
            self.console.print(panel)

            if browser:
                open_new(auth_info.url)

            with self.console.status("Waiting for login...", spinner="dots", spinner_style="#A653FF"):
                await self.get_token(device_code=auth_info.device_code, interval=auth_info.interval, expires_in=auth_info.expires_in)

        except KeyboardInterrupt:
            self.error_console.print("\n[bold red]❌ Login cancelled by user.[/bold red]")
            return

        # check that the user is valid, and update the user profile if necessary only on login
        try:
            user = await self._update_user_profile()
            self.console.print(f"[green][bold]Successfully logged in![/bold][/green] [dim]Token stored at {self.token_path}[/dim]")
            print_user_details(user)

        except AuthException as e:
            self.console.print(f"[green][bold]Successfully logged in![/bold][/green] [dim]Token stored at {self.token_path}[/dim]")
            self.error_console.print(f"\n[bold red]⚠️ Could not update user profile: {e}[/bold red]")

    async def _logout(self) -> None:
        try:
            async with self._create_async_client() as client:
                response = await client.get(f"https://{self.auth_provider_config.domain}/v2/logout")
                response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise AuthException(e)

    async def logout(self) -> None:
        try:
            await self._logout()
            self.purge_cache()

            self.console.print("\n[yellow][bold]🔒 Successfully logged out![/bold][/yellow]")
            self.console.print(f"[dim]> Token removed from {self.token_path}[/dim]")
        except FileNotFoundError:
            self.error_console.print("\n[red][bold]🔒 Not logged in[/bold][/red]")
            self.error_console.print(f"[dim]> No token currently exists at: {self.token_path}[/dim]")
        except AuthException as e:
            self.error_console.print(f"\n[red][bold]❌ There was an error logging out:[/bold][/red]\n{e}")


def get_auth_handler(api_endpoint: str) -> TokenHandler:
    return TokenHandler(api_endpoint=api_endpoint)
