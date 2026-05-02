"""Enterprise app class."""

from reflex.app import App
from reflex.config import get_config
from reflex.utils import console
from reflex.utils.exec import is_prod_mode
from reflex_cli.utils.hosting import save_token_to_config

from reflex_enterprise import constants
from reflex_enterprise.config import ConfigEnterprise
from reflex_enterprise.environment import environment
from reflex_enterprise.utils import (
    check_config_option_in_tier,
    get_user_tier,
    is_deploy_context,
    is_new_session,
)


class AppEnterprise(App):
    """Enterprise app class."""

    def __post_init__(self):
        """Post-initialization."""
        super().__post_init__()
        self._check_and_setup_access_token()
        self._check_login()
        self._verify_and_setup_badge()
        self._verify_and_setup_proxy()

    def _check_and_setup_access_token(self):
        if environment.REFLEX_ACCESS_TOKEN.is_set():
            access_token = environment.REFLEX_ACCESS_TOKEN.get()
            if access_token is not None:
                save_token_to_config(access_token)

    def _check_login(self):
        """Check if the user is logged in.

        Raises:
            RuntimeError: If the user is not logged in.
        """
        current_tier = get_user_tier()
        if (
            current_tier == "anonymous"
            and not environment.REFLEX_BACKEND_ONLY.get()
            and not environment.CI.get()
        ):
            msg = (
                "`reflex-enterprise` is free to use but you must be logged in. "
                "Run `reflex login` or set the environment variable REFLEX_ACCESS_TOKEN with your token."
            )
            console.error(msg)
            exit()

    def _verify_and_setup_badge(self):
        config = get_config()
        deploy = is_deploy_context()

        check_config_option_in_tier(
            option_name="show_built_with_reflex",
            allowed_tiers=(
                ["pro", "team", "enterprise"] if deploy else ["team", "enterprise"]
            ),
            fallback_value=True,
            help_link=constants.SHOW_BUILT_WITH_REFLEX_INFO,
        )

        if is_prod_mode() and config.show_built_with_reflex:
            self._setup_sticky_badge()

    def _verify_and_setup_proxy(self):
        config = get_config()
        deploy = is_deploy_context()

        if (
            isinstance(config, ConfigEnterprise)
            and config.use_single_port
            and not environment.REFLEX_BACKEND_ONLY.get()
        ):
            if deploy:
                console.warn(
                    "Single port mode is not supported when deploying to Reflex Cloud. Ignoring the setting."
                )
                return
            if is_new_session():
                console.info("Single port proxy mode enabled")
            # Enable proxying to frontend server.
            from .proxy import proxy_middleware

            self.register_lifespan_task(proxy_middleware)


App = AppEnterprise
