"""``ci release`` command group — release tooling."""

from ...common.lazy_group import LazyGroup

app = LazyGroup(
    name="release",
    help="Release tooling",
    no_args_is_help=True,
    lazy_subcommands={
        "next-version": "pysae_ai_tools.ci.release.next_version:main",
        "run": "pysae_ai_tools.ci.release.run:main",
        "verify": "pysae_ai_tools.ci.release.verify:app",
    },
)
