"""``figma`` command group — Figma REST tooling."""

from ..common.lazy_group import LazyGroup

app = LazyGroup(
    name="figma",
    help="Figma REST tooling",
    no_args_is_help=True,
    lazy_subcommands={
        "fetch-node": "pysae_ai_tools.figma.fetch_node:main",
    },
)
