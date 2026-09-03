"""OWASP Top 10 for Agentic Applications (2026).

This module provides compliance tags for the OWASP Top 10 for Agentic Applications,
which addresses security risks specific to autonomous AI agents. These complement
the OWASP LLM Top 10 which focuses on LLM-specific risks.

Reference: https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/

Example:
    ```python
    from dreadnode.airt.compliance.owasp_agentic import (
        OWASPAgenticCategory,
        get_attacks_for_category,
    )

    # Get recommended attacks for a category
    attacks = get_attacks_for_category(OWASPAgenticCategory.TOOL_MISUSE)
    # ['tap_attack', 'goat_attack']
    ```
"""

from enum import StrEnum


class OWASPAgenticCategory(StrEnum):
    """
    OWASP Top 10 for Agentic Applications (2026).

    Reference: https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/

    These categories address security risks specific to autonomous AI agents,
    complementing the OWASP LLM Top 10 which focuses on LLM-specific risks.
    """

    # ASI01: Agent Behavior Hijacking
    # Attackers manipulate agent decision-making through prompt injection,
    # goal manipulation, or context poisoning
    AGENT_BEHAVIOR_HIJACKING = "agentic_asi01_behavior_hijacking"

    # ASI02: Tool Misuse & Exploitation
    # Agents abuse their tool access in unintended ways, even within
    # authorized permissions
    TOOL_MISUSE = "agentic_asi02_tool_misuse"

    # ASI03: Identity & Privilege Abuse
    # Agents inherit or escalate privileges inappropriately,
    # or impersonate other agents/users
    IDENTITY_PRIVILEGE_ABUSE = "agentic_asi03_identity_abuse"

    # ASI04: Agentic Supply Chain Vulnerabilities (2026)
    # Malicious/compromised tools, MCP descriptors, agent cards, packages, or
    # prompt templates enter the agent's runtime-composed execution chain
    AGENTIC_SUPPLY_CHAIN = "agentic_asi04_supply_chain"

    # ASI05: Unexpected Code Execution (RCE) (2026)
    # Prompt injection / tool misuse / unsafe eval escalates text into executed
    # code (shell, deserialization, eval, tool chains) -> host/container compromise
    UNEXPECTED_CODE_EXECUTION = "agentic_asi05_code_execution"

    # --- 2025 draft categories, retained for back-compat (folded into the 2026
    # ASI02/ASI04/ASI05 above). Existing findings/tags keep resolving. ---
    # ASI04 (2025): Insecure Data Handling
    INSECURE_DATA_HANDLING = "agentic_asi04_data_handling"
    # ASI05 (2025): Insecure Output Handling
    INSECURE_OUTPUT_HANDLING = "agentic_asi05_output_handling"

    # ASI06: Memory Poisoning
    # Attackers corrupt agent long-term memory to influence
    # future behavior
    MEMORY_POISONING = "agentic_asi06_memory_poisoning"

    # ASI07: Insecure Inter-Agent Communication
    # Communication between agents is spoofed, intercepted,
    # or manipulated
    INSECURE_INTER_AGENT_COMM = "agentic_asi07_insecure_comms"

    # ASI08: Cascading Failures
    # Failures propagate through multi-agent systems with
    # escalating impact
    CASCADING_FAILURES = "agentic_asi08_cascading_failures"

    # ASI09: Human-Agent Trust Exploitation
    # Agents exploit human trust through confident, polished
    # but incorrect outputs
    HUMAN_AGENT_TRUST = "agentic_asi09_human_trust"

    # ASI10: Rogue Agents
    # Agents exhibit misalignment, concealment, or self-directed
    # action outside intended scope
    ROGUE_AGENTS = "agentic_asi10_rogue_agents"


# The 2025 ASI04/ASI05 members retained as back-compat aliases (superseded by
# AGENTIC_SUPPLY_CHAIN / UNEXPECTED_CODE_EXECUTION in the 2026 taxonomy). They stay in
# the enum so existing findings/tags keep resolving, but they are NOT part of the
# canonical Top 10 - excluded from the default suite run and the compliance matrix so
# ASI04/ASI05 aren't double-counted.
LEGACY_ALIAS_CATEGORIES: "frozenset[OWASPAgenticCategory]" = frozenset(
    {
        OWASPAgenticCategory.INSECURE_DATA_HANDLING,
        OWASPAgenticCategory.INSECURE_OUTPUT_HANDLING,
    }
)

# The canonical 2026 OWASP-ASI Top 10, in ASI01..ASI10 order (enum order minus the
# legacy aliases). Single source of truth for "the ten categories".
CANONICAL_AGENTIC_CATEGORIES: "tuple[OWASPAgenticCategory, ...]" = tuple(
    category for category in OWASPAgenticCategory if category not in LEGACY_ALIAS_CATEGORIES
)


# Mapping to SDK capabilities for each OWASP Agentic category
OWASP_AGENTIC_CAPABILITY_MAP: dict[OWASPAgenticCategory, dict[str, list[str]]] = {
    OWASPAgenticCategory.AGENT_BEHAVIOR_HIJACKING: {
        "attacks": [
            "tap_attack",
            "goat_attack",
            "crescendo_attack",
            "echo_chamber_attack",
            "salami_slicing_attack",
            "alignment_faking_attack",
            "persona_hijack_attack",
            "self_persuasion_attack",
        ],
        "scorers": [
            "tool_sequence",
            "tool_invoked",
            "indirect_injection_success",
            "echo_chamber_detected",
            "sycophancy_detected",
            "visual_injection_followed",
            "navigation_hijacked",
        ],
        "rubrics": ["goal_hijacking"],
    },
    OWASPAgenticCategory.TOOL_MISUSE: {
        "attacks": [
            "tap_attack",
            "goat_attack",
            "tmap_trajectory_attack",
        ],
        "scorers": [
            "tool_selection_safety",
            "dangerous_tool_args",
            "any_tool_invoked",
            "tool_description_poisoned",
            "implicit_tool_poison_detected",
            "tool_output_injected",
            "clickfix_executed",
            "domain_validation_bypassed",
        ],
        "rubrics": ["tool_selection_safety", "tool_chaining"],
    },
    OWASPAgenticCategory.IDENTITY_PRIVILEGE_ABUSE: {
        "attacks": [
            "crescendo_attack",
            "autoredteamer_attack",
        ],
        "scorers": [
            "permission_escalation_detected",
            "agent_spoofing_detected",
        ],
        "rubrics": ["privilege_escalation"],
    },
    OWASPAgenticCategory.INSECURE_DATA_HANDLING: {
        "attacks": ["tap_attack"],
        "scorers": [
            "credential_leakage",
            "detect_pii",
            "markdown_exfil_detected",
            "dns_exfil_detected",
            "unicode_exfil_detected",
            "ssrf_exfil_detected",
            "search_query_exfil_detected",
            "trusted_domain_exfil_detected",
        ],
        "rubrics": [],
    },
    OWASPAgenticCategory.INSECURE_OUTPUT_HANDLING: {
        "attacks": [
            "tap_attack",
            "reward_hacking_attack",
        ],
        "scorers": [
            "detect_unsafe_shell_content",
            "package_hallucination",
            "xdr_summary_compromised",
        ],
        "rubrics": [],
    },
    OWASPAgenticCategory.AGENTIC_SUPPLY_CHAIN: {
        "attacks": [
            "tap_attack",
            "goat_attack",
        ],
        "scorers": [
            "tool_description_poisoned",
            "schema_poisoned",
            "rug_pull_detected",
            "skill_poisoning_detected",
            "package_hallucination",
        ],
        "rubrics": [],
    },
    OWASPAgenticCategory.UNEXPECTED_CODE_EXECUTION: {
        "attacks": [
            "tap_attack",
            "goat_attack",
            "tmap_trajectory_attack",
        ],
        "scorers": [
            "detect_unsafe_shell_content",
            "package_hallucination",
        ],
        "rubrics": ["tool_selection_safety"],
    },
    OWASPAgenticCategory.MEMORY_POISONING: {
        "attacks": [
            "crescendo_attack",
            "echo_chamber_attack",
        ],
        "scorers": [
            "memory_poisoning_detected",
            "memory_injection_detected",
            "prompt_infection_detected",
        ],
        "rubrics": ["memory_poisoning"],
    },
    OWASPAgenticCategory.INSECURE_INTER_AGENT_COMM: {
        "attacks": [
            "mapf_attack",
            "nexus_attack",
        ],
        "scorers": [
            "agent_spoofing_detected",
            "consensus_poisoned",
            "delegation_exploit_detected",
            "session_smuggling_detected",
            "agent_config_overwrite_detected",
        ],
        "rubrics": [],
    },
    OWASPAgenticCategory.CASCADING_FAILURES: {
        "attacks": [
            "tap_attack",
            "salami_slicing_attack",
        ],
        "scorers": [
            "cascade_propagation",
            "cumulative_harm",
            "reasoning_dos_detected",
        ],
        "rubrics": [],
    },
    OWASPAgenticCategory.HUMAN_AGENT_TRUST: {
        "attacks": [
            "crescendo_attack",
            "humor_bypass_attack",
            "analogy_escalation_attack",
        ],
        "scorers": [
            "sycophancy_detected",
            "resilience_gap",
            "human_trust_exploited",
        ],
        "rubrics": ["sycophancy"],
    },
    OWASPAgenticCategory.ROGUE_AGENTS: {
        "attacks": [
            "tap_attack",
            "goat_attack",
            "lrm_autonomous_attack",
            "alignment_faking_attack",
        ],
        "scorers": [
            "tool_count",
            "goal_drift_detected",
            "skill_poisoning_detected",
        ],
        "rubrics": ["unbounded_agency", "scope_creep"],
    },
}


def get_attacks_for_category(category: OWASPAgenticCategory) -> list[str]:
    """Get recommended attacks for an OWASP Agentic category."""
    return OWASP_AGENTIC_CAPABILITY_MAP.get(category, {}).get("attacks", [])


def get_scorers_for_category(category: OWASPAgenticCategory) -> list[str]:
    """Get recommended scorers for an OWASP Agentic category."""
    return OWASP_AGENTIC_CAPABILITY_MAP.get(category, {}).get("scorers", [])


def get_rubrics_for_category(category: OWASPAgenticCategory) -> list[str]:
    """Get recommended rubrics for an OWASP Agentic category."""
    return OWASP_AGENTIC_CAPABILITY_MAP.get(category, {}).get("rubrics", [])
