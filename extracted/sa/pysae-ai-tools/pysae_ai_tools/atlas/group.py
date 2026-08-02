"""``atlas`` command group — MongoDB Atlas tooling."""

from ..common.lazy_group import LazyGroup

app = LazyGroup(
    name="atlas",
    help="MongoDB Atlas tooling",
    no_args_is_help=True,
    lazy_subcommands={
        "access-list": "pysae_ai_tools.atlas.access_list:app",
    },
)
