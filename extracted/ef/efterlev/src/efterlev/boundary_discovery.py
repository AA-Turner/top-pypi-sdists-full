"""Boundary discovery — surface candidate in-boundary dependencies from IaC.

`efterlev boundary set` lets a customer DECLARE their authorization boundary.
But a first-time FedRAMP 20x customer's literal first question is "what *is* my
boundary?" — and nobody serves it. Efterlev already parses the IaC, so it can
surface the external touchpoints a boundary has to account for: non-AWS provider
integrations, cross-account references, remote state, hardcoded third-party SaaS
endpoints, and external data sources.

This is RECONNAISSANCE, not auto-scoping. We surface candidates and explain why
each matters; the in/out-of-boundary JUDGMENT stays with the human (and their
3PAO). Auto-drawing a boundary that's wrong would mis-scope an authorization —
worse than no help. Deterministic: no LLM, no network, no writes.

v0 scope: Terraform `.tf` files. CloudFormation / CDK signals follow.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from efterlev.terraform.parser import parse_terraform_tree

# Third-party / external-service Terraform providers. Presence of one means the
# system integrates with an external SaaS or platform the authorization boundary
# must account for (data flow + shared-responsibility split). name -> label.
_THIRD_PARTY_PROVIDERS: dict[str, str] = {
    "datadog": "Datadog (monitoring)",
    "newrelic": "New Relic (monitoring)",
    "splunk": "Splunk (logging/SIEM)",
    "sumologic": "Sumo Logic (logging)",
    "cloudflare": "Cloudflare (CDN/DNS/WAF)",
    "fastly": "Fastly (CDN)",
    "auth0": "Auth0 (identity)",
    "okta": "Okta (identity)",
    "pagerduty": "PagerDuty (incident response)",
    "sentry": "Sentry (error tracking)",
    "snowflake": "Snowflake (data warehouse)",
    "mongodbatlas": "MongoDB Atlas (database)",
    "vault": "HashiCorp Vault (secrets)",
    "github": "GitHub (source control / CI)",
    "gitlab": "GitLab (source control / CI)",
    "kubernetes": "Kubernetes (external cluster)",
    "helm": "Helm (Kubernetes workloads)",
    "twilio": "Twilio (communications)",
    "sendgrid": "SendGrid (email)",
}

# Known SaaS endpoint substrings. A hardcoded reference in the IaC is an
# external-dependency signal. Matched case-insensitively as a substring.
_SAAS_ENDPOINTS: dict[str, str] = {
    "datadoghq.com": "Datadog",
    "auth0.com": "Auth0",
    "okta.com": "Okta",
    "api.stripe.com": "Stripe",
    "sentry.io": "Sentry",
    "pagerduty.com": "PagerDuty",
    "newrelic.com": "New Relic",
    "hooks.slack.com": "Slack",
    "splunkcloud.com": "Splunk Cloud",
    "sumologic.com": "Sumo Logic",
    "twilio.com": "Twilio",
    "api.sendgrid.com": "SendGrid",
    "snowflakecomputing.com": "Snowflake",
    "mongodb.net": "MongoDB Atlas",
}

# External-system data sources: these reach outside the workspace at plan/apply.
_EXTERNAL_DATA_TYPES: dict[str, str] = {
    "http": "an HTTP endpoint",
    "external": "an external program",
}

_PROVIDER_RE = re.compile(r'^\s*provider\s+"([a-z0-9_-]+)"\s*\{')
# Block form `backend "s3" {` only — the `backend = "s3"` *attribute* (used inside
# a terraform_remote_state config) has an `=` and won't match. `\b` (not `^`) so
# a compact single-line `terraform { backend "s3" {...} }` is still caught.
_BACKEND_RE = re.compile(r'\bbackend\s+"([a-z0-9_-]+)"\s*\{')
_ALIAS_RE = re.compile(r"^\s*alias\s*=")
_ARN_ACCOUNT_RE = re.compile(r"arn:aws[a-z-]*:[a-z0-9-]*:[a-z0-9-]*:(\d{12}):")
_ACCOUNT_ASSIGN_RE = re.compile(r'account_id\s*=\s*"(\d{12})"')

# Stable category ordering for display (highest-precision / most-actionable first).
_CATEGORY_ORDER = (
    "external-provider",
    "cross-account",
    "remote-state",
    "saas-endpoint",
    "external-data",
)
CATEGORY_LABELS: dict[str, str] = {
    "external-provider": "External service integrations",
    "cross-account": "Cross-account AWS references",
    "remote-state": "Remote / external state",
    "saas-endpoint": "Third-party SaaS endpoints",
    "external-data": "External data sources",
}


@dataclass(frozen=True)
class BoundarySignal:
    """One candidate boundary dependency found in the IaC.

    `category` is a stable id (see `_CATEGORY_ORDER`); `locations` are
    `file:line` strings (repo-relative), sorted and deduped.
    """

    category: str
    title: str
    detail: str
    locations: tuple[str, ...]


def _block_end(lines: list[str], start: int) -> int:
    """`start` is the 1-indexed line of a `... {` opener; return the 1-indexed
    line just past its matching close (brace-balance; tolerant of real-world TF)."""
    depth = 0
    for off, line in enumerate(lines[start - 1 :], start=start):
        depth += line.count("{") - line.count("}")
        if depth <= 0 and off >= start:
            return off + 1
    return len(lines) + 1


def discover_boundary_signals(target_dir: Path) -> list[BoundarySignal]:
    """Walk `target_dir`'s Terraform for candidate in-boundary dependencies.

    Returns an ordered, deduped list of `BoundarySignal`. Never raises on a
    non-directory or empty tree — returns `[]` so the CLI can give a clean
    "nothing found" message rather than a traceback.
    """
    target_dir = Path(target_dir)
    if not target_dir.is_dir():
        return []

    third_party: dict[str, list[str]] = {}
    multiaccount: list[str] = []
    backends: dict[str, list[str]] = {}
    accounts: dict[str, list[str]] = {}
    endpoints: dict[str, list[str]] = {}

    for tf in sorted(target_dir.rglob("*.tf")):
        try:
            lines = tf.read_text(encoding="utf-8").splitlines()
        except OSError:
            continue
        rel = tf.relative_to(target_dir)
        for i, line in enumerate(lines, start=1):
            loc = f"{rel}:{i}"
            prov = _PROVIDER_RE.match(line)
            if prov:
                name = prov.group(1)
                if name in _THIRD_PARTY_PROVIDERS:
                    third_party.setdefault(name, []).append(loc)
                elif name == "aws":
                    block = lines[i - 1 : _block_end(lines, i) - 1]
                    if any("assume_role" in b or _ALIAS_RE.match(b) for b in block):
                        multiaccount.append(loc)
            back = _BACKEND_RE.search(line)
            if back and back.group(1) != "local":
                backends.setdefault(back.group(1), []).append(loc)
            for m in _ARN_ACCOUNT_RE.finditer(line):
                accounts.setdefault(m.group(1), []).append(loc)
            for m in _ACCOUNT_ASSIGN_RE.finditer(line):
                accounts.setdefault(m.group(1), []).append(loc)
            low = line.lower()
            for domain in _SAAS_ENDPOINTS:
                if domain in low:
                    endpoints.setdefault(domain, []).append(loc)

    signals: list[BoundarySignal] = []

    for name, locs in third_party.items():
        signals.append(
            BoundarySignal(
                category="external-provider",
                title=_THIRD_PARTY_PROVIDERS[name],
                detail=(
                    "Configured as a Terraform provider — an external service your "
                    "boundary must account for (data flow + shared-responsibility split)."
                ),
                locations=_locs(locs),
            )
        )

    if multiaccount:
        signals.append(
            BoundarySignal(
                category="cross-account",
                title="Multi-account AWS provider (assume_role / alias)",
                detail=(
                    "Provider blocks assume roles into or alias other AWS accounts — "
                    "cross-account access is an authorization-boundary consideration."
                ),
                locations=_locs(multiaccount),
            )
        )

    if len(accounts) > 1:
        acct_list = ", ".join(sorted(accounts))
        all_locs = [loc for locs in accounts.values() for loc in locs]
        signals.append(
            BoundarySignal(
                category="cross-account",
                title=f"{len(accounts)} distinct AWS account IDs referenced",
                detail=(
                    f"ARNs reference multiple accounts ({acct_list}). Resources in "
                    "other accounts are typically external dependencies — decide which "
                    "are in-boundary."
                ),
                locations=_locs(all_locs),
            )
        )

    for btype, locs in backends.items():
        signals.append(
            BoundarySignal(
                category="remote-state",
                title=f"Remote state backend ({btype})",
                detail=(
                    "Terraform state lives in an external store; it holds infrastructure "
                    "metadata and is part of your operational boundary."
                ),
                locations=_locs(locs),
            )
        )

    for domain, locs in endpoints.items():
        signals.append(
            BoundarySignal(
                category="saas-endpoint",
                title=f"{_SAAS_ENDPOINTS[domain]} endpoint ({domain})",
                detail="A hardcoded third-party SaaS endpoint — an external integration.",
                locations=_locs(locs),
            )
        )

    # data-source signals from the parser (terraform_remote_state, http, external)
    parsed = parse_terraform_tree(target_dir)
    remote_state_locs: list[str] = []
    for r in parsed.resources:
        if r.kind != "data":
            continue
        loc = _ref_loc(r.source_ref)
        if r.type == "terraform_remote_state":
            remote_state_locs.append(loc)
        elif r.type in _EXTERNAL_DATA_TYPES:
            signals.append(
                BoundarySignal(
                    category="external-data",
                    title=f"data.{r.type}.{r.name}",
                    detail=(
                        f"Reads from {_EXTERNAL_DATA_TYPES[r.type]} at plan/apply time — "
                        "an external dependency outside the managed infrastructure."
                    ),
                    locations=(loc,),
                )
            )
    if remote_state_locs:
        signals.append(
            BoundarySignal(
                category="remote-state",
                title="Reads another Terraform stack's state",
                detail=(
                    "`data.terraform_remote_state` pulls outputs from a separate stack — "
                    "a cross-stack dependency whose resources may sit in or beside your boundary."
                ),
                locations=_locs(remote_state_locs),
            )
        )

    signals.sort(key=lambda s: (_CATEGORY_ORDER.index(s.category), s.title))
    return signals


def _locs(locs: list[str]) -> tuple[str, ...]:
    return tuple(sorted(set(locs)))


def _ref_loc(ref: object) -> str:
    file = getattr(ref, "file", "?")
    line = getattr(ref, "line_start", None)
    return f"{file}:{line}" if line else str(file)
