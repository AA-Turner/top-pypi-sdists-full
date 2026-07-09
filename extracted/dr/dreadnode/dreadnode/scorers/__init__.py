import importlib
import typing as t

from dreadnode.core.scorer import (
    add,
    and_,
    avg,
    clip,
    equals,
    forward,
    invert,
    normalize,
    not_,
    or_,
    remap_range,
    scale,
    subtract,
    task_input,
    task_output,
    threshold,
    weighted_avg,
)
from dreadnode.scorers.advanced_jailbreak_detection import (
    fictional_framing_detected,
    guardrail_dos_detected,
    invisible_character_detected,
    likert_exploitation_detected,
    memory_poisoning_detected,
    pipeline_manipulation_detected,
    prefill_bypass_detected,
    sycophancy_detected,
    tool_chain_attack_detected,
    xdr_summary_compromised,
)
from dreadnode.scorers.agent_security import (
    agent_config_tampered,
    agent_identity_leaked,
    bootstrap_hook_injected,
    heartbeat_manipulation,
    memory_injection_detected,
    permission_escalation_detected,
    skill_integrity_compromised,
    skill_supply_chain_attack,
    workspace_poisoning_detected,
)
from dreadnode.scorers.agentic import (
    any_tool_invoked,
    cascade_propagation,
    dangerous_tool_args,
    indirect_injection_success,
    mcp_tool_manipulation,
    tool_count,
    tool_invoked,
    tool_selection_safety,
    tool_sequence,
)
from dreadnode.scorers.agentic_workflow import (
    agentic_workflow_attack,
    cypher_injection_detected,
    intent_manipulation_detected,
    malformed_json_injection_detected,
    mode_confusion_detected,
    phase_bypass_detected,
    phase_downgrade_detected,
    session_state_poisoning_detected,
    sql_injection_via_nlp_detected,
    success_indicator_spoofing_detected,
    todo_list_manipulation_detected,
    tool_priority_manipulation_detected,
    tool_restriction_bypass_detected,
    wordlist_exhaustion_detected,
    workflow_disruption_detected,
)
from dreadnode.scorers.attack_outcome import (
    cumulative_harm,
    malicious_intent_fulfilled,
    practical_outcome,
    resilience_gap,
)
from dreadnode.scorers.classification import (
    detect_refusal_with_zero_shot,
    zero_shot_classification,
)
from dreadnode.scorers.consistency import character_consistency
from dreadnode.scorers.contains import (
    contains,
    detect_ansi_escapes,
    detect_bias,
    detect_refusal,
    detect_sensitive_keywords,
    detect_unsafe_shell_content,
)
from dreadnode.scorers.credentials import credential_leakage
from dreadnode.scorers.documentation_security import (
    env_var_exfiltration,
    favicon_exfiltration,
    hidden_documentation_injection,
    package_readme_poisoning,
    resource_hint_exfil,
)
from dreadnode.scorers.exfiltration_detection import (
    dns_exfil_detected,
    markdown_exfil_detected,
    ssrf_exfil_detected,
    unicode_exfil_detected,
)
from dreadnode.scorers.format import is_json, is_xml
from dreadnode.scorers.ide_security import (
    config_persistence,
    covert_exfiltration,
    rug_pull_detection,
    shadowing_detection,
    tool_squatting,
)
from dreadnode.scorers.judge_ensemble import (
    agent_as_judge,
    multi_judge_consensus,
    rubric_judge,
)
from dreadnode.scorers.length import length_in_range, length_ratio, length_target
from dreadnode.scorers.lexical import type_token_ratio
from dreadnode.scorers.mcp_security import (
    ansi_cloaking_detected,
    cross_server_shadow_detected,
    implicit_tool_poison_detected,
    rug_pull_detected,
    sampling_injection_detected,
    schema_poisoned,
    tool_description_poisoned,
    tool_output_injected,
)
from dreadnode.scorers.memorization import training_data_memorization
from dreadnode.scorers.multi_agent_security import (
    agent_config_overwrite_detected,
    agent_spoofing_detected,
    consensus_poisoned,
    delegation_exploit_detected,
    prompt_infection_detected,
    session_smuggling_detected,
)
from dreadnode.scorers.pii import detect_pii, detect_pii_with_presidio
from dreadnode.scorers.prompt_leak import system_prompt_leaked
from dreadnode.scorers.readability import readability
from dreadnode.scorers.reasoning_security import (
    cot_backdoor_detected,
    escalation_detected,
    goal_drift_detected,
    reasoning_dos_detected,
    reasoning_hijack_detected,
    reasoning_loop_detected,
)
from dreadnode.scorers.sentiment import sentiment, sentiment_with_perspective
from dreadnode.scorers.structural_detection import (
    echo_chamber_detected,
    m2s_reformatting_detected,
    stego_acrostic_detected,
    template_exploit_detected,
)
from dreadnode.scorers.supply_chain_detection import (
    merge_backdoor_detected,
    package_hallucination,
    skill_poisoning_detected,
)

if t.TYPE_CHECKING:
    from dreadnode.scorers.crucible import contains_crucible_flag
    from dreadnode.scorers.harm import detect_harm_with_openai
    from dreadnode.scorers.image import image_distance
    from dreadnode.scorers.json import json_path
    from dreadnode.scorers.judge import llm_judge, multimodal_judge
    from dreadnode.scorers.similarity import (
        bleu,
        similarity,
        similarity_with_litellm,
        similarity_with_sentence_transformers,
        similarity_with_tf_idf,
    )

__all__ = [
    "add",
    "agent_as_judge",
    "agent_config_overwrite_detected",
    "agent_config_tampered",
    "agent_identity_leaked",
    "agent_spoofing_detected",
    "agentic_workflow_attack",
    "and_",
    "ansi_cloaking_detected",
    "any_tool_invoked",
    "avg",
    "bleu",
    "bootstrap_hook_injected",
    "cascade_propagation",
    "character_consistency",
    "clip",
    "config_persistence",
    "consensus_poisoned",
    "contains",
    "contains_crucible_flag",
    "cot_backdoor_detected",
    "covert_exfiltration",
    "credential_leakage",
    "cross_server_shadow_detected",
    "cumulative_harm",
    "cypher_injection_detected",
    "dangerous_tool_args",
    "delegation_exploit_detected",
    "detect_ansi_escapes",
    "detect_bias",
    "detect_harm_with_openai",
    "detect_pii",
    "detect_pii_with_presidio",
    "detect_refusal",
    "detect_refusal_with_zero_shot",
    "detect_sensitive_keywords",
    "detect_unsafe_shell_content",
    "dns_exfil_detected",
    "echo_chamber_detected",
    "env_var_exfiltration",
    "equals",
    "escalation_detected",
    "favicon_exfiltration",
    "fictional_framing_detected",
    "forward",
    "goal_drift_detected",
    "guardrail_dos_detected",
    "heartbeat_manipulation",
    "hidden_documentation_injection",
    "image_distance",
    "implicit_tool_poison_detected",
    "indirect_injection_success",
    "intent_manipulation_detected",
    "invert",
    "invisible_character_detected",
    "is_json",
    "is_xml",
    "json_path",
    "length_in_range",
    "length_ratio",
    "length_target",
    "likert_exploitation_detected",
    "llm_judge",
    "m2s_reformatting_detected",
    "malformed_json_injection_detected",
    "malicious_intent_fulfilled",
    "markdown_exfil_detected",
    "mcp_tool_manipulation",
    "memory_injection_detected",
    "memory_poisoning_detected",
    "merge_backdoor_detected",
    "mode_confusion_detected",
    "multi_judge_consensus",
    "multimodal_judge",
    "normalize",
    "not_",
    "or_",
    "package_hallucination",
    "package_readme_poisoning",
    "permission_escalation_detected",
    "phase_bypass_detected",
    "phase_downgrade_detected",
    "pipeline_manipulation_detected",
    "practical_outcome",
    "prefill_bypass_detected",
    "prompt_infection_detected",
    "readability",
    "reasoning_dos_detected",
    "reasoning_hijack_detected",
    "reasoning_loop_detected",
    "remap_range",
    "resilience_gap",
    "resource_hint_exfil",
    "rubric_judge",
    "rug_pull_detected",
    "rug_pull_detection",
    "sampling_injection_detected",
    "scale",
    "schema_poisoned",
    "sentiment",
    "sentiment_with_perspective",
    "session_smuggling_detected",
    "session_state_poisoning_detected",
    "shadowing_detection",
    "similarity",
    "similarity_with_litellm",
    "similarity_with_sentence_transformers",
    "similarity_with_tf_idf",
    "skill_integrity_compromised",
    "skill_poisoning_detected",
    "skill_supply_chain_attack",
    "sql_injection_via_nlp_detected",
    "ssrf_exfil_detected",
    "stego_acrostic_detected",
    "subtract",
    "success_indicator_spoofing_detected",
    "sycophancy_detected",
    "system_prompt_leaked",
    "task_input",
    "task_output",
    "template_exploit_detected",
    "threshold",
    "todo_list_manipulation_detected",
    "tool_chain_attack_detected",
    "tool_count",
    "tool_description_poisoned",
    "tool_invoked",
    "tool_output_injected",
    "tool_priority_manipulation_detected",
    "tool_restriction_bypass_detected",
    "tool_selection_safety",
    "tool_sequence",
    "tool_squatting",
    "training_data_memorization",
    "type_token_ratio",
    "unicode_exfil_detected",
    "weighted_avg",
    "wordlist_exhaustion_detected",
    "workflow_disruption_detected",
    "workspace_poisoning_detected",
    "xdr_summary_compromised",
    "zero_shot_classification",
]

__lazy_submodules__: list[str] = []
__lazy_components__: dict[str, str] = {
    "llm_judge": "dreadnode.scorers.judge",
    "multimodal_judge": "dreadnode.scorers.judge",
    "detect_harm_with_openai": "dreadnode.scorers.harm",
    "contains_crucible_flag": "dreadnode.scorers.crucible",
    "similarity": "dreadnode.scorers.similarity",
    "similarity_with_sentence_transformers": "dreadnode.scorers.similarity",
    "similarity_with_tf_idf": "dreadnode.scorers.similarity",
    "similarity_with_litellm": "dreadnode.scorers.similarity",
    "bleu": "dreadnode.scorers.similarity",
    "json_path": "dreadnode.scorers.json",
    "image_distance": "dreadnode.scorers.image",
}


def __getattr__(name: str) -> t.Any:
    if name in __lazy_submodules__:
        module = importlib.import_module(f".{name}", __name__)
        globals()[name] = module
        return module

    if name in __lazy_components__:
        module_name = __lazy_components__[name]
        module = importlib.import_module(module_name)
        component = getattr(module, name)
        globals()[name] = component
        return component

    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
