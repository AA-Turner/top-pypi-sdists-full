"""``code`` command group — code & repo utilities."""

from ..common.lazy_group import LazyGroup

app = LazyGroup(
    name="code",
    help="Code & repo utilities",
    no_args_is_help=True,
    lazy_subcommands={
        "changelog": "pysae_ai_tools.code.changelog:app",
        "configure": "pysae_ai_tools.code.configure:app",
        "ensure-repo": "pysae_ai_tools.code.ensure_repo:app",
        "release-content": "pysae_ai_tools.code.release_content:main",
        "release-notes": "pysae_ai_tools.code.release_notes:app",
    },
)
