"""Scoring: deterministic business score + LLM signal (Task 7)."""

import json
import os
from datetime import datetime, timezone
from functools import cache

from ..common.llm import LLMClient, LLMUsage, get_llm_client
from .models import CompletenessAssessment, ScoredTicket, Ticket, TicketAssessment
from .tracking import log_usage

PRIORITY_SCORES: dict[str, int] = {
    "priority::P1": 100,
    "priority::P2": 66,
    "priority::P3": 33,
}
_BIZ_WEIGHT = 0.7
_LLM_WEIGHT = 0.3
TYPE_BONUS: dict[str, int] = {
    "type::bug": 15,
    "Support": 15,
}
AGE_THRESHOLD_DAYS = 21
AGE_BONUS_CAP_DAYS = 180
AGE_BONUS_MAX = 10


def _priority_score(labels: list[str]) -> int:
    for lbl, score in PRIORITY_SCORES.items():
        if lbl in labels:
            return score
    return 0


def _type_bonus(labels: list[str]) -> int:
    return sum(bonus for lbl, bonus in TYPE_BONUS.items() if lbl in labels)


def _age_bonus(updated_at: datetime) -> int:
    now = datetime.now(timezone.utc)
    age_days = max(0, (now - updated_at).days)
    if age_days < AGE_THRESHOLD_DAYS:
        return 0
    span = AGE_BONUS_CAP_DAYS - AGE_THRESHOLD_DAYS
    progress = min(1.0, (age_days - AGE_THRESHOLD_DAYS) / span)
    return int(round(progress * AGE_BONUS_MAX))


def business_score(ticket: Ticket) -> int:
    return _priority_score(ticket.labels) + _type_bonus(ticket.labels) + _age_bonus(ticket.updated_at)


_ASSESSMENT_MODEL = os.environ.get("ANTHROPIC_RANK_MODEL", "claude-haiku-4-5")
_COMPLETENESS_MODEL = os.environ.get("ANTHROPIC_COMPLETENESS_MODEL", "claude-sonnet-4-6")


@cache
def _llm_client() -> LLMClient:
    """Build the LLM client used for the rank step (provider via ``PYSAE_LLM_PROVIDER``).

    Prefers `ANTHROPIC_CI_AUTOPILOT_API_KEY` (dedicated budget) then
    `ANTHROPIC_API_KEY`. A key is only *required* when the resolved provider
    needs one (the SDK-based `anthropic`); the CLI providers (`claude-cli`,
    `codex-cli`, the default) reuse their own auth and run keyless.
    """
    key = os.environ.get("ANTHROPIC_CI_AUTOPILOT_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")
    client = get_llm_client(api_key=key)
    if client.api_key_envs and not key:
        raise RuntimeError(
            "set ANTHROPIC_CI_AUTOPILOT_API_KEY (preferred) or ANTHROPIC_API_KEY "
            "to run scoring with the anthropic provider, set PYSAE_LLM_PROVIDER=claude-cli, "
            "or pass --skip-llm-rank"
        )
    return client


_ASSESSMENT_PROMPT = (
    "You evaluate whether an autonomous coding agent (Claude Code Opus)"
    " can implement a ticket without human help.\n\n"
    "TICKET:\nTitle: {title}\nLabels: {labels}\nDescription:\n{description}\n\n"
    "Output a JSON object with EXACTLY these keys:\n"
    "- success_probability (int 0-100): how likely the agent succeeds end-to-end without escalating\n"
    "- sensitive_domain_match (bool): see definition below\n"
    "- rationale (string, max 200 chars): one sentence explaining your scoring\n\n"
    "Set sensitive_domain_match=true IF AND ONLY IF the ticket clearly"
    " touches one of these categories. If unsure or unclear, set false.\n\n"
    "AUTHENTICATION & AUTHORIZATION:\n"
    "  - login, signup, password reset flows\n"
    "  - OAuth / SSO (Auth0, Google, etc.)\n"
    "  - session management, JWT, cookie auth\n"
    "  - role/permission checks, RBAC policies\n"
    "  - API key auth, service accounts\n\n"
    "SECRETS & CREDENTIALS:\n"
    "  - secret rotation or new secret/key generation\n"
    "  - .env or secret-manager configuration\n"
    "  - API tokens, encryption keys\n"
    "  - database connection strings\n\n"
    "DATA INTEGRITY (production):\n"
    "  - DB schema migrations (Alembic, Prisma migrate, raw DDL)\n"
    "  - multi-tenant isolation (tenant_id, RLS, ownership checks)\n"
    "  - PII handling, GDPR compliance\n"
    "  - data backfills or one-shot data migrations\n\n"
    "PRODUCTION INFRASTRUCTURE:\n"
    "  - Kubernetes manifests, Helm charts, ArgoCD applications\n"
    "  - Terraform / IaC modules\n"
    "  - DNS, TLS, ingress, cert-manager\n"
    "  - deploy pipelines that ship code to production\n"
    "  - production environment variables\n\n"
    "PERFORMANCE & SCALING:\n"
    "  - new or changed DB indexes (any column, any table)\n"
    "  - query optimization on hot paths (N+1 fixes, joins, denormalization)\n"
    "  - cache strategy changes (Redis keys, TTL, invalidation)\n"
    "  - rate limiting, throttling, circuit breakers\n"
    "  - pagination, batching, streaming for large datasets\n"
    "  - background job concurrency, worker pool sizing\n\n"
    "MONEY & BILLING:\n"
    "  - Stripe or billing integration\n"
    "  - pricing, subscription, quota enforcement\n"
    "  - invoice generation, payment processing\n\n"
    "PUBLIC API CONTRACTS:\n"
    "  - breaking change to a public REST/GraphQL endpoint\n"
    "  - webhook payload contract changes\n"
    "  - SDK / OpenAPI schema versioning\n\n"
    "If none of the above match, sensitive_domain_match=false. Tooling"
    " and dev-experience changes (test config, lint rules, dev deps,"
    " bundler config, docs, lint/test CI jobs) are NEVER sensitive.\n\n"
    "Output ONLY the JSON object, no preamble, no markdown fences."
)


def assess_with_llm(ticket: Ticket) -> TicketAssessment:
    """Call Haiku 4.5 to assess success probability and sensitive-domain match."""
    prompt = _ASSESSMENT_PROMPT.format(
        title=ticket.title,
        labels=", ".join(ticket.labels) or "(none)",
        description=(ticket.description or "(empty)")[:4000],
    )
    response = _llm_client().complete(
        model=_ASSESSMENT_MODEL,
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    _log_llm_usage(response.usage, caller="haiku-scoring", model=_ASSESSMENT_MODEL, ticket=ticket)
    data = json.loads(_strip_code_fences(response.text))
    return TicketAssessment.model_validate(data)


_COMPLETENESS_PROMPT = (
    "You are a senior tech lead reviewing whether a GitLab ticket has enough"
    " spec for an autonomous coding agent (Claude Code Opus) to implement it"
    " end-to-end WITHOUT asking the human any clarifying question.\n\n"
    "TICKET:\nTitle: {title}\nLabels: {labels}\nDescription:\n{description}\n\n"
    "Audit the ticket against this concrete checklist. A missing answer to ANY"
    " of these is a blocker — list the gap explicitly in `missing_specs`:\n\n"
    "  1. Acceptance criteria: are they explicit, testable, and unambiguous?\n"
    "  2. File scope: are the files/modules to change named (paths, not vague)?\n"
    "  3. Inputs: are edge cases for empty/null/max/boundary values specified?\n"
    "  4. Error paths: what should happen if dependency X fails or returns 4xx/5xx?\n"
    "  5. External integrations: API contracts (auth, payload, idempotency,\n"
    "     timeouts) specified for any third-party call?\n"
    "  6. Concurrency / ordering: if multiple actors can act on the same\n"
    "     resource, is the expected ordering or locking strategy stated?\n"
    "  7. Migration / backward-compatibility: if data shape or config changes,\n"
    "     is the migration path described (cutover, rollback, deprecation)?\n"
    "  8. Out-of-scope: is what the ticket does NOT cover clearly stated?\n\n"
    "Strict rules for the verdict:\n"
    "  - 'complete' = every applicable checklist item is answered. Items that\n"
    "    are genuinely N/A for this ticket (e.g. no external integration) do\n"
    "    not count as missing.\n"
    "  - 'incomplete' = at least one applicable item is unanswered.\n\n"
    "Do NOT invent abstract concerns ('what about scalability?'). Only list"
    " gaps tied to the concrete checklist above. Each `missing_specs` entry"
    " must be a precise question the agent would have to ask the human"
    " (e.g. 'What happens if `device_id` is null in the payload?').\n\n"
    "Output a JSON object with EXACTLY these keys:\n"
    "  - verdict: 'complete' or 'incomplete'\n"
    "  - missing_specs: list of strings (max 5 items, each <= 200 chars).\n"
    "    Empty list when verdict is 'complete'.\n"
    "  - rationale: one short sentence summarising the verdict (<= 200 chars).\n\n"
    "Output ONLY the JSON object, no preamble, no markdown fences."
)


def assess_completeness_with_sonnet(ticket: Ticket) -> CompletenessAssessment:
    """Call Sonnet 4.6 to audit the ticket spec against a concrete checklist.

    Sonnet (not Haiku) because detecting implicit gaps requires reasoning
    that Haiku consistently misses. Run only on tickets that already passed
    the Haiku sensitive + proba-floor gates, so cost stays bounded.
    """
    prompt = _COMPLETENESS_PROMPT.format(
        title=ticket.title,
        labels=", ".join(ticket.labels) or "(none)",
        description=(ticket.description or "(empty)")[:8000],
    )
    response = _llm_client().complete(
        model=_COMPLETENESS_MODEL,
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}],
    )
    _log_llm_usage(response.usage, caller="sonnet-completeness", model=_COMPLETENESS_MODEL, ticket=ticket)
    data = json.loads(_strip_code_fences(response.text))
    return CompletenessAssessment.model_validate(data)


def _log_llm_usage(usage: LLMUsage, *, caller: str, model: str, ticket: Ticket) -> None:
    """Translate a normalized :class:`LLMUsage` to a tracking event."""
    log_usage(
        caller=caller,
        model=model,
        input_tokens=usage.input_tokens,
        output_tokens=usage.output_tokens,
        cache_creation_tokens=usage.cache_creation_tokens,
        cache_read_tokens=usage.cache_read_tokens,
        ticket_iid=ticket.iid,
        project=ticket.project_path,
    )


def _strip_code_fences(text: str) -> str:
    """Strip markdown code fences from an LLM response.

    Haiku occasionally wraps JSON in ```json ... ``` despite explicit
    instructions not to. Defensive parsing: peel fences if present, else
    return as-is.
    """
    s = text.strip()
    if s.startswith("```"):
        s = s.split("\n", 1)[1] if "\n" in s else s[3:]
        if s.endswith("```"):
            s = s[:-3]
    return s.strip()


def weighted_final_score(business: float, success_probability: int) -> float:
    """Combine business score and LLM success probability into the final score.

    Weighted average, not a pure multiplier: a P1 judged 0% keeps a
    ``_BIZ_WEIGHT * business`` floor (stays visible) instead of dropping to 0,
    while a P3 judged 100% cannot leapfrog a P1 judged 30%. Single source of the
    formula, shared by :func:`score_ticket` and the ``agent rank`` CLI.
    """
    return _BIZ_WEIGHT * business + _LLM_WEIGHT * (success_probability * business / 100.0)


def score_ticket(ticket: Ticket, assessment: TicketAssessment) -> ScoredTicket:
    """Apply the business + LLM weighting to a ticket given a precomputed assessment.

    Shared by :func:`rank_tickets` (which computes the assessment via the LLM
    layer) and the ``agent rank`` CLI (which receives assessments produced
    out-of-band, e.g. by in-session scoring subagents).
    """
    biz = float(business_score(ticket))
    return ScoredTicket(
        ticket=ticket,
        business_score=biz,
        success_probability=assessment.success_probability,
        sensitive_domain_match=assessment.sensitive_domain_match,
        final_score=weighted_final_score(biz, assessment.success_probability),
        rationale=assessment.rationale,
    )


def rank_tickets(
    tickets: list[Ticket],
    skip_llm: bool = False,
    *,
    check_completeness: bool = False,
    min_success_probability: int = 0,
) -> list[ScoredTicket]:
    """Score and rank tickets, descending by final score.

    When `check_completeness=True`, runs a second LLM pass (Sonnet) to audit
    spec completeness — but only on tickets that are not sensitive and have
    success_probability >= min_success_probability. The pass is intentionally
    skipped on low-proba/sensitive tickets because they would be escalated
    pre-pickup anyway and a Sonnet call would burn tokens for nothing.
    """
    scored: list[ScoredTicket] = []
    for t in tickets:
        if skip_llm:
            biz = float(business_score(t))
            scored.append(
                ScoredTicket(
                    ticket=t,
                    business_score=biz,
                    success_probability=100,
                    sensitive_domain_match=False,
                    final_score=biz,
                    rationale=None,
                )
            )
            continue

        assessment = assess_with_llm(t)
        scored_ticket = score_ticket(t, assessment)
        eligible = (
            check_completeness
            and not assessment.sensitive_domain_match
            and assessment.success_probability >= min_success_probability
        )
        if eligible:
            completeness = assess_completeness_with_sonnet(t)
            scored_ticket = scored_ticket.model_copy(
                update={
                    "completeness_verdict": completeness.verdict,
                    "missing_specs": completeness.missing_specs,
                    "completeness_rationale": completeness.rationale,
                }
            )
        scored.append(scored_ticket)
    scored.sort(key=lambda s: s.final_score, reverse=True)
    return scored
