"""``openapi`` command group — OpenAPI tooling."""

from ..common.lazy_group import LazyGroup

app = LazyGroup(
    name="openapi",
    help="OpenAPI tooling",
    no_args_is_help=True,
    lazy_subcommands={
        "to-postman": "pysae_ai_tools.openapi.to_postman:main",
        "to-bruno": "pysae_ai_tools.openapi.to_bruno:main",
    },
)
