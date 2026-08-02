"""``design`` command group — design system tooling (kit, generate proto, check, coverage)."""

from ..common.lazy_group import LazyGroup

app = LazyGroup(
    name="design",
    help="Design system tooling (kit, generate proto, check, coverage)",
    no_args_is_help=True,
    lazy_subcommands={
        "check": "pysae_ai_tools.design.check:main",
        "coverage": "pysae_ai_tools.design.coverage:main",
        "kit": "pysae_ai_tools.design.kit:main",
    },
)
