"""``auth0`` command group — read-only access to the prod Auth0 tenant."""

from ..common.lazy_group import LazyGroup

app = LazyGroup(
    name="auth0",
    help="Read-only Auth0 tooling (Management API token, CLI login).",
    no_args_is_help=True,
    lazy_subcommands={
        "token": "pysae_ai_tools.auth0.token:main",
        "login": "pysae_ai_tools.auth0.login:main",
    },
)
