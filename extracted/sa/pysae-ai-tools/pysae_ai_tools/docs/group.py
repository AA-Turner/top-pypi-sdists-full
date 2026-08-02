"""``docs`` command group — documentation sync checks (README<->skills, dead links)."""

from ..common.lazy_group import LazyGroup

app = LazyGroup(
    name="docs",
    help="Documentation sync checks (README<->skills, dead links)",
    no_args_is_help=True,
    lazy_subcommands={
        "check": "pysae_ai_tools.docs.check:main",
    },
)
