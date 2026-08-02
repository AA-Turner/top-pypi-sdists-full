"""``ci`` command group — GitLab CI/CD tooling (with nested ``ci release``)."""

from ..common.lazy_group import LazyGroup

app = LazyGroup(
    name="ci",
    help="GitLab CI/CD tooling",
    no_args_is_help=True,
    lazy_subcommands={
        "prepare": "pysae_ai_tools.ci.prepare:main",
        "run": "pysae_ai_tools.ci.run.__main__:app",
        "run-local": "pysae_ai_tools.ci.run_local.__main__:app",
        "artifacts": "pysae_ai_tools.ci.artifacts:app",
        "test-report": "pysae_ai_tools.ci.test_report:main",
        "release": "pysae_ai_tools.ci.release.group:app",
    },
)
