"""Template-driven recommendations.

Each :class:`GoalCategory` has a pre-written recommendation template with
compliance references and mitigation guidance.  Templates are populated
with the actual attack vectors that succeeded during the campaign.

No LLM calls -- recommendations are deterministic and auditable.
"""

from __future__ import annotations

from dreadnode.airt.analytics.types import (
    Finding,
    GoalCategory,
    Recommendation,
    Severity,
)

# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------

_TEMPLATES: dict[GoalCategory, Recommendation] = {
    GoalCategory.SYSTEM_PROMPT_LEAK: Recommendation(
        severity=Severity.INFO,  # overridden per-finding
        category=GoalCategory.SYSTEM_PROMPT_LEAK,
        title="Harden system prompt isolation",
        description=(
            "The model leaked its system prompt under adversarial pressure. "
            "Mitigations: (1) Move sensitive instructions to tool-level guardrails "
            "rather than system prompts. (2) Add output filtering for instruction-like "
            "content. (3) Fine-tune the model to refuse meta-questions about its "
            "configuration. (4) Implement a response classifier that detects and "
            "blocks system prompt content in outputs."
        ),
        compliance_refs=["OWASP LLM07", "ATLAS AML.T0051.001"],
    ),
    GoalCategory.HARMFUL_CONTENT: Recommendation(
        severity=Severity.INFO,
        category=GoalCategory.HARMFUL_CONTENT,
        title="Strengthen content safety filters",
        description=(
            "The model generated harmful content when adversarial transforms were "
            "applied. Mitigations: (1) Layer input classifiers before the model. "
            "(2) Add output safety classifiers (OpenAI Moderation, Perspective API). "
            "(3) Fine-tune on refusal data for the specific attack patterns that "
            "succeeded. (4) Consider multi-turn conversation monitoring to detect "
            "escalation patterns like Crescendo."
        ),
        compliance_refs=["OWASP LLM02", "ATLAS AML.T0054"],
    ),
    GoalCategory.CREDENTIAL_LEAK: Recommendation(
        severity=Severity.INFO,
        category=GoalCategory.CREDENTIAL_LEAK,
        title="Prevent credential and secret exposure",
        description=(
            "The model exposed credentials or API keys under adversarial probing. "
            "Mitigations: (1) Never include real credentials in system prompts or "
            "context. (2) Implement secret scanning on all model outputs. "
            "(3) Use credential vaults with dynamic references instead of static "
            "values. (4) Add regex-based output filters for key patterns "
            "(API keys, tokens, passwords)."
        ),
        compliance_refs=["OWASP LLM06", "ATLAS AML.T0051"],
    ),
    GoalCategory.PII_EXTRACTION: Recommendation(
        severity=Severity.INFO,
        category=GoalCategory.PII_EXTRACTION,
        title="Protect personally identifiable information",
        description=(
            "The model disclosed PII from its training data or context. "
            "Mitigations: (1) Apply PII redaction to all context fed to the model. "
            "(2) Add output-side PII detection (Presidio, custom NER). "
            "(3) Fine-tune on privacy-preserving refusal patterns. "
            "(4) Minimise PII in training data and RAG context."
        ),
        compliance_refs=["OWASP LLM06", "NIST AI RMF MG-3.2"],
    ),
    GoalCategory.TOOL_MISUSE: Recommendation(
        severity=Severity.INFO,
        category=GoalCategory.TOOL_MISUSE,
        title="Restrict tool and agent capabilities",
        description=(
            "The model was manipulated into misusing tools or escalating privileges. "
            "Mitigations: (1) Implement least-privilege tool access. "
            "(2) Add human-in-the-loop approval for dangerous operations. "
            "(3) Validate tool arguments against allowlists. "
            "(4) Monitor tool call sequences for anomalous patterns."
        ),
        compliance_refs=["OWASP LLM06", "OWASP ASI02", "ATLAS AML.T0053"],
    ),
    GoalCategory.JAILBREAK_GENERAL: Recommendation(
        severity=Severity.INFO,
        category=GoalCategory.JAILBREAK_GENERAL,
        title="Improve general jailbreak resistance",
        description=(
            "The model's safety alignment was bypassed by adversarial prompting. "
            "Mitigations: (1) Adversarial fine-tuning using the successful attack "
            "prompts from this campaign. (2) Input perplexity filtering to detect "
            "encoded/obfuscated prompts. (3) Multi-model consensus (route through "
            "a safety classifier before responding). (4) Regular re-testing with "
            "updated attack techniques."
        ),
        compliance_refs=["OWASP LLM01", "ATLAS AML.T0054", "NIST AI RMF MS-2.7"],
    ),
    GoalCategory.REFUSAL_BYPASS: Recommendation(
        severity=Severity.INFO,
        category=GoalCategory.REFUSAL_BYPASS,
        title="Strengthen refusal mechanisms",
        description=(
            "The model's refusal behaviour was circumvented. "
            "Mitigations: (1) Train refusal on diverse prompt reformulations. "
            "(2) Add a secondary classifier that detects harmful intent regardless "
            "of surface form. (3) Implement conversation-level intent tracking "
            "(not just per-message). (4) Test with the specific transform "
            "categories that bypassed refusal."
        ),
        compliance_refs=["OWASP LLM01", "ATLAS AML.T0054"],
    ),
    GoalCategory.BIAS_FAIRNESS: Recommendation(
        severity=Severity.INFO,
        category=GoalCategory.BIAS_FAIRNESS,
        title="Address bias and fairness gaps",
        description=(
            "The model exhibited biased behaviour under adversarial probing. "
            "Mitigations: (1) Audit training data for representation gaps. "
            "(2) Fine-tune with counter-bias examples. (3) Add fairness "
            "constraints to the model's objective function. (4) Implement "
            "demographic parity checks on outputs."
        ),
        compliance_refs=["NIST AI RMF MS-2.11"],
    ),
    GoalCategory.CONTENT_POLICY: Recommendation(
        severity=Severity.INFO,
        category=GoalCategory.CONTENT_POLICY,
        title="Tighten content policy enforcement",
        description=(
            "The model violated content policies under adversarial conditions. "
            "Mitigations: (1) Review and tighten content policy definitions. "
            "(2) Add output classifiers aligned to specific policy categories. "
            "(3) Fine-tune on policy-violation examples. (4) Implement "
            "escalation workflows for borderline cases."
        ),
        compliance_refs=["OWASP LLM02"],
    ),
    GoalCategory.REASONING_EXPLOITATION: Recommendation(
        severity=Severity.CRITICAL,
        category=GoalCategory.REASONING_EXPLOITATION,
        title="Harden reasoning model safety",
        description=(
            "Chain-of-thought or reasoning processes were exploited to bypass "
            "safety measures. Mitigations: (1) Add reasoning-step monitoring. "
            "(2) Implement thinking-token validation. (3) Limit reasoning depth. "
            "(4) Add output verification independent of reasoning chain."
        ),
        compliance_refs=["OWASP LLM01", "ATLAS AML.T0051"],
    ),
    GoalCategory.SUPPLY_CHAIN: Recommendation(
        severity=Severity.CRITICAL,
        category=GoalCategory.SUPPLY_CHAIN,
        title="Strengthen supply chain security",
        description=(
            "Supply chain vulnerabilities were exploited (package hallucination, "
            "model merging backdoors, skill poisoning). Mitigations: (1) Validate "
            "all package references against registries. (2) Audit model provenance. "
            "(3) Scan skill/plugin files for malicious patterns. (4) Implement "
            "dependency pinning and integrity verification."
        ),
        compliance_refs=["OWASP LLM03", "ATLAS AML.T0049"],
    ),
    GoalCategory.RESOURCE_EXHAUSTION: Recommendation(
        severity=Severity.HIGH,
        category=GoalCategory.RESOURCE_EXHAUSTION,
        title="Implement resource consumption limits",
        description=(
            "Adversarial inputs caused excessive resource consumption. "
            "Mitigations: (1) Set token generation limits. (2) Add reasoning "
            "depth caps. (3) Implement timeout mechanisms. (4) Monitor and "
            "alert on anomalous computation patterns."
        ),
        compliance_refs=["OWASP LLM10"],
    ),
    GoalCategory.QUANTIZATION_SAFETY: Recommendation(
        severity=Severity.HIGH,
        category=GoalCategory.QUANTIZATION_SAFETY,
        title="Validate safety under quantization",
        description=(
            "Model safety degraded under quantized (INT4/INT8) inference. "
            "Mitigations: (1) Re-evaluate safety benchmarks post-quantization. "
            "(2) Apply safety fine-tuning after quantization. (3) Use "
            "quantization-aware training for safety-critical models."
        ),
        compliance_refs=["ATLAS AML.T0018"],
    ),
    GoalCategory.ALIGNMENT_INTEGRITY: Recommendation(
        severity=Severity.CRITICAL,
        category=GoalCategory.ALIGNMENT_INTEGRITY,
        title="Verify alignment integrity",
        description=(
            "Alignment faking, watermark removal, or training data extraction "
            "was detected. Mitigations: (1) Implement behavioral monitoring "
            "across contexts. (2) Use robust watermarking schemes. (3) Apply "
            "membership inference defenses. (4) Test alignment consistency."
        ),
        compliance_refs=["OWASP LLM06", "ATLAS AML.T0049"],
    ),
    GoalCategory.MULTI_TURN_ESCALATION: Recommendation(
        severity=Severity.CRITICAL,
        category=GoalCategory.MULTI_TURN_ESCALATION,
        title="Defend against multi-turn escalation",
        description=(
            "Multi-turn conversations were exploited to progressively escalate "
            "from benign to harmful content. Mitigations: (1) Implement "
            "conversation-level safety scoring. (2) Track cumulative harm "
            "across turns. (3) Reset safety context periodically. (4) Add "
            "escalation detection classifiers."
        ),
        compliance_refs=["OWASP LLM01", "ATLAS AML.T0051"],
    ),
}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def generate_recommendations(
    findings: list[Finding],
) -> list[Recommendation]:
    """Produce a de-duplicated list of recommendations from top findings.

    One recommendation per ``GoalCategory`` that appears in *findings*.
    The recommendation's ``severity`` is set to the maximum severity among
    findings in that category, and ``attack_vectors`` lists the unique
    attack names that triggered it.
    """
    # Group findings by category
    by_category: dict[GoalCategory, list[Finding]] = {}
    for f in findings:
        by_category.setdefault(f.goal_category, []).append(f)

    recs: list[Recommendation] = []
    for category, cat_findings in by_category.items():
        template = _TEMPLATES.get(category)
        if template is None:
            continue

        # Worst severity among findings for this category
        worst = min(cat_findings, key=lambda f: f.severity.rank)
        # Unique attack names
        vectors = sorted({f.attack_name for f in cat_findings})

        recs.append(
            Recommendation(
                severity=worst.severity,
                category=category,
                title=template.title,
                description=template.description,
                compliance_refs=list(template.compliance_refs),
                attack_vectors=vectors,
            )
        )

    # Sort by severity (most severe first)
    recs.sort(key=lambda r: r.severity.rank)
    return recs
