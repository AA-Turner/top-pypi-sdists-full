import configparser
import os
from dataclasses import dataclass
from typing import Optional

import click

import montecarlodata.settings as settings
from montecarlodata.fs_utils import mkdirs


@dataclass
class Config:
    mcd_id: Optional[str]
    mcd_token: Optional[str]
    mcd_api_endpoint: str
    mcd_agent_image_host: Optional[str] = None
    mcd_agent_image_org: Optional[str] = None
    mcd_agent_image_repo: Optional[str] = None
    # OAuth (client-credentials) auth. When set, these are used instead of mcd_id/mcd_token.
    mcd_oauth_client_id: Optional[str] = None
    mcd_oauth_client_secret: Optional[str] = None
    # Deployment instance ID (e.g. us1, eu1); required for OAuth so the global gateway can route to
    # the right instance.
    mcd_instance_id: Optional[str] = None
    # Optional overrides for the OAuth token / GraphQL endpoints (otherwise the SDK derives them
    # from mcd_api_endpoint).
    mcd_token_endpoint: Optional[str] = None
    mcd_oauth_api_endpoint: Optional[str] = None

    @property
    def is_oauth(self) -> bool:
        return bool(self.mcd_oauth_client_id and self.mcd_oauth_client_secret)


class ConfigManager:
    """
    Token is generated at https://github.com/monte-carlo-data/monolith-django/blob/a18ffc64ea2517166e66f0d3e85417b582398513/monolith/service/account.py#L236
    with the function call as `secrets.token_urlsafe(42)`, which is always 56 characters
    Details in https://docs.python.org/3/library/secrets.html#secrets.token_urlsafe
    """

    TOKEN_LENGTH = 56
    MCD_TOKEN = "mcd_token"
    # Auth-credential options per auth type. On reconfigure we clear the opposing type's options
    # so a re-`configure` is authoritative and never leaves stale (live) credentials on disk.
    API_KEY_OPTIONS = ("mcd_id", "mcd_token")
    OAUTH_OPTIONS = (
        "mcd_oauth_client_id",
        "mcd_oauth_client_secret",
        "mcd_instance_id",
        "mcd_token_endpoint",
        "mcd_oauth_api_endpoint",
    )

    def __init__(
        self,
        profile_name: str,
        base_path: str,
        config_parser: Optional[configparser.ConfigParser] = None,
    ):
        self._profile_name = profile_name
        self._base_path = base_path
        self._profile_config_file = os.path.join(self._base_path, settings.PROFILE_FILE_NAME)

        self._config = config_parser or configparser.ConfigParser()
        self._config.read(self._profile_config_file)

    """
        There is a circular dependency between ConfigManager and montecarlodata.errors
        so the decorator is imported here instead at top of the file with the other local imports.
        TODO: Move the config class into common.
    """
    from montecarlodata.errors import manage_errors

    @manage_errors
    def write(self, **kwargs) -> None:
        """
        Write any configuration key value pairs to the specified section (profile name)
        """
        if self._profile_name not in self._config.sections():
            # if the section does not exist add it
            self._config.add_section(self._profile_name)

        for k, v in kwargs.items():
            if k == self.MCD_TOKEN and len(v) != self.TOKEN_LENGTH:
                raise ValueError(
                    f"{self.MCD_TOKEN} received should have {self.TOKEN_LENGTH} length "
                    f"but received {len(v)}"
                )
            self._config.set(self._profile_name, k, v)

        mkdirs(self._base_path)
        with open(self._profile_config_file, "w") as cf:
            self._config.write(cf)

    def remove_options(self, options) -> None:
        """Remove the given options from the profile section, if present (in memory; persisted on
        the next ``write``). Used to drop the opposing auth type's credentials on reconfigure."""
        if self._profile_name in self._config.sections():
            for option in options:
                self._config.remove_option(self._profile_name, option)

    def read(self) -> Optional[Config]:
        """
        Return configuration from section (profile name) if it exists.
        Any MCD values can be overwritten by the environment. Uses system default for AWS
        if not set.

        When OAuth client credentials are present (config-file or environment), they are used
        instead of the mcd_id/mcd_token API key.
        """
        try:
            oauth_client_id = settings.MCD_DEFAULT_OAUTH_CLIENT_ID or self._config.get(
                self._profile_name, "mcd_oauth_client_id", fallback=None
            )
            oauth_client_secret = settings.MCD_DEFAULT_OAUTH_CLIENT_SECRET or self._config.get(
                self._profile_name, "mcd_oauth_client_secret", fallback=None
            )
            is_oauth = bool(oauth_client_id and oauth_client_secret)

            return Config(
                mcd_id=(
                    None
                    if is_oauth
                    else settings.MCD_DEFAULT_API_ID
                    or self._config.get(self._profile_name, "mcd_id")
                ),
                mcd_token=(
                    None
                    if is_oauth
                    else settings.MCD_DEFAULT_API_TOKEN
                    or self._config.get(self._profile_name, "mcd_token")
                ),
                mcd_oauth_client_id=oauth_client_id,
                mcd_oauth_client_secret=oauth_client_secret,
                mcd_instance_id=settings.MCD_DEFAULT_INSTANCE_ID
                or self._config.get(self._profile_name, "mcd_instance_id", fallback=None),
                mcd_token_endpoint=self._config.get(
                    self._profile_name, "mcd_token_endpoint", fallback=None
                ),
                mcd_oauth_api_endpoint=self._config.get(
                    self._profile_name, "mcd_oauth_api_endpoint", fallback=None
                ),
                mcd_api_endpoint=settings.MCD_API_ENDPOINT
                or self._config.get(
                    self._profile_name,
                    "mcd_api_endpoint",
                    fallback=settings.MCD_DEFAULT_API_ENDPOINT,
                ),
                mcd_agent_image_host=settings.MCD_AGENT_IMAGE_HOST
                or self._config.get(
                    self._profile_name,
                    "mcd_agent_image_host",
                    fallback=settings.MCD_DEFAULT_AGENT_IMAGE_HOST,
                ),
                mcd_agent_image_org=settings.MCD_AGENT_IMAGE_ORG
                or self._config.get(
                    self._profile_name,
                    "mcd_agent_image_org",
                    fallback=settings.MCD_DEFAULT_AGENT_IMAGE_ORG,
                ),
                mcd_agent_image_repo=settings.MCD_AGENT_IMAGE_REPO
                or self._config.get(
                    self._profile_name,
                    "mcd_agent_image_repo",
                    fallback=settings.MCD_DEFAULT_AGENT_IMAGE_REPO,
                ),
            )
        except configparser.NoSectionError:
            click.echo(
                f"Failed to find configuration for '{self._profile_name}'. "
                "Please setup using 'configure' first"
            )
