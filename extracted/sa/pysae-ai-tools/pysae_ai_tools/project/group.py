"""``project`` command group — per-repo .pysae-ai-tools.yaml config."""

from ..common.lazy_group import LazyGroup

app = LazyGroup(
    name="project",
    help="Per-repo .pysae-ai-tools.yaml config (init, show, list, domains, group, flag)",
    no_args_is_help=True,
    lazy_subcommands={
        "init": "pysae_ai_tools.project.init:main",
        "show": "pysae_ai_tools.project.show:main",
        "list": "pysae_ai_tools.project.list_cmd:main",
        "domains": "pysae_ai_tools.project.domains_cmd:main",
        "group": "pysae_ai_tools.project.group_cmd:main",
        "flag": "pysae_ai_tools.project.flag:main",
    },
)
