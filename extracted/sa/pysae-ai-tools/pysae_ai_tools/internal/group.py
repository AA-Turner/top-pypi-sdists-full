"""``internal`` command group — utilities used by Pysae tooling itself."""

from ..common.lazy_group import LazyGroup

app = LazyGroup(
    name="internal",
    help="Internal utilities (used by Pysae tooling itself)",
    no_args_is_help=True,
    lazy_subcommands={
        "parse-stream": "pysae_ai_tools.internal.parse_stream.parser:main",
        "detect-context": "pysae_ai_tools.internal.detect_context.detect:main",
        "scan-skill": "pysae_ai_tools.internal.scan_skill:main",
        "secret-scan": "pysae_ai_tools.internal.secret_scan:main",
        "webhook-reply": "pysae_ai_tools.internal.webhook_reply:app",
    },
)
