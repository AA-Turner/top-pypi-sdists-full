"""``pysae api`` command group — authenticate and call the Pysae HTTP API (dev/prod)."""

from ...common.lazy_group import LazyGroup

app = LazyGroup(
    name="api",
    help="Authenticate and call the Pysae HTTP API (dev/prod).",
    no_args_is_help=True,
    lazy_subcommands={
        "auth": "pysae_ai_tools.pysae.api.auth:app",
        "request": "pysae_ai_tools.pysae.api.request:app",
        "spec": "pysae_ai_tools.pysae.api.spec:app",
    },
)
