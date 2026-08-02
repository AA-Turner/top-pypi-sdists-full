"""``env`` command group — environment variable and secret management."""

from ..common.lazy_group import LazyGroup

app = LazyGroup(
    name="env",
    help="Environment variable and secret management",
    no_args_is_help=True,
    lazy_subcommands={
        "resolve": "pysae_ai_tools.env.resolve:app",
        "list": "pysae_ai_tools.env.list_cmd:main",
        "activate": "pysae_ai_tools.env.activate:main",
        "deactivate": "pysae_ai_tools.env.deactivate:main",
        "run": "pysae_ai_tools.env.run:app",
        "dotenv": "pysae_ai_tools.env.dotenv:main",
        "shell-init": "pysae_ai_tools.env.shell_init:main",
    },
)
