"""``pysae`` command group — Pysae product tooling (with nested ``pysae api``)."""

from ..common.lazy_group import LazyGroup

app = LazyGroup(
    name="pysae",
    help="Pysae product tooling",
    no_args_is_help=True,
    lazy_subcommands={
        "api": "pysae_ai_tools.pysae.api.group:app",
    },
)
