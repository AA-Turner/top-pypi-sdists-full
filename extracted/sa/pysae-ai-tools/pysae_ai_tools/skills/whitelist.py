"""Skills allowed to be published to the Anthropic Workspace Skills API.

Only pure-prompt skills (or skills usable with the standard Pysae stack
installed locally) belong here. Any change to this tuple is reviewed in MR
because publishing exposes a skill org-wide on claude.ai / Claude Desktop.
"""

PUBLISHED_SKILLS: tuple[str, ...] = (
    "pysae-design",
    "clawd-skill-review",
    "clawd-compound",
    "post-mortem",
    "product-discover",
)
