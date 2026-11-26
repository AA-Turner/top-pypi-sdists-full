"""VendorScanner: only the shared rules with a maker's fixed shape (`sk-…`, `hf_…`, `probe_…`, a PEM block), keyword-gated,
no decoding. What source files and output files get: ~8x cheaper than the full rules, and it never reads code as a key (T51)."""

from __future__ import annotations

from .....foundation.transcripts.credential_scan import _RULES
from .....foundation.transcripts.credential_scan.credential_scan import Finding

#: Shared rules this pass runs. Every name in `_RULES` is in exactly one of these two sets
#: (`test_source_rules.py`), so a new rule cannot reach or skip source files by accident.
VENDOR_RULE_NAMES = frozenset({
    "aws-access-key-id", "anthropic-api-key", "probe-token", "probe-ingest-token", "probe-node-credential",
    "probe-run-token", "openai-api-key", "openai-api-key-classic", "github-token", "github-fine-grained-pat",
    "huggingface-token", "capy-api-key", "slack-token", "slack-webhook", "gcp-api-key", "stripe-live-key",
    "gitlab-pat", "npm-token", "wandb-key", "private-key-block",
})
#: Shapes that ordinary code also has (a docstring's `Authorization: Bearer …`, a test JWT, a DSN template).
HEURISTIC_RULE_NAMES = frozenset({"jwt", "bearer-token", "basic-auth", "credential-uri"})

_VENDOR_RULES = tuple(rule for rule in _RULES if rule.name in VENDOR_RULE_NAMES)


class VendorScanner:
    """Each vendor rule over the whole text, only when one of its keywords is in it."""

    def scan(self, text: str) -> list[Finding]:
        lowered = text.lower()
        return [
            Finding(rule.name, match.start(), match.end())
            for rule in _VENDOR_RULES
            if any(keyword in lowered for keyword in rule.keywords)
            for match in rule.pattern.finditer(text)
        ]
