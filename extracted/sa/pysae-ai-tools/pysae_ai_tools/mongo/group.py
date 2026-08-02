"""``mongo`` command group — MongoDB analysis tooling (mongosh-based)."""

from ..common.lazy_group import LazyGroup

app = LazyGroup(
    name="mongo",
    help="MongoDB analysis tooling (mongosh-based)",
    no_args_is_help=True,
    lazy_subcommands={
        "index-usage": "pysae_ai_tools.mongo.index_usage:main",
    },
)
