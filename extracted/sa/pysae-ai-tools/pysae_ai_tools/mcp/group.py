"""``mcp`` command group — the resolver shim invoked by MCP client configs."""

from ..common.lazy_group import LazyGroup

app = LazyGroup(
    name="mcp",
    help="MCP resolver shim — resolve a server's secrets at launch and exec the real server.",
    no_args_is_help=True,
    lazy_subcommands={
        "run": "pysae_ai_tools.mcp.run:main",
        "write-manifest": "pysae_ai_tools.mcp.write_manifest:main",
    },
)
