"""AI Red Team (AIRT) module.

Pre-configured attack functions that combine Samplers with Study for easy use.
For more control, use samplers directly from `dreadnode.samplers`.

LLM jailbreak attacks:
- prompt_attack: Beam search prompt refinement
- goat_attack: GOAT pattern with graph neighborhood search
- tap_attack: Tree of Attacks pattern
- crescendo_attack: Multi-turn progressive escalation attack
- pair_attack: PAIR iterative refinement attack
- rainbow_attack: Rainbow Teaming quality-diversity attack
- gptfuzzer_attack: GPTFuzzer mutation-based fuzzing attack
- autodan_turbo_attack: AutoDAN-Turbo lifelong strategy learning attack
- renellm_attack: ReNeLLM prompt rewriting and scenario nesting attack
- beast_attack: BEAST gradient-free beam search suffix attack
- drattack: DrAttack prompt decomposition and reconstruction attack
- deep_inception_attack: DeepInception nested scene hypnosis attack
- echo_chamber_attack: Completion bias exploitation via planted seeds
- salami_slicing_attack: Incremental sub-threshold prompt accumulation
- jbfuzz_attack: Lightweight fuzzing-based jailbreak
- persona_hijack_attack: PHISH implicit persona induction
- self_persuasion_attack: Persu-Agent self-generated justification
- humor_bypass_attack: Comedic framing pipeline
- analogy_escalation_attack: Benign analogy construction and escalation
- genetic_persona_attack: GA-based persona prompt evolution
- nexus_attack: NEXUS multi-module attack with ThoughtNet reasoning
- siren_attack: Siren multi-turn attack with turn-level LLM feedback
- j2_meta_attack: J2 meta-jailbreak (jailbreak a model to jailbreak others)
- attention_shifting_attack: ASJA dialogue history mutation attack
- cot_jailbreak_attack: Chain-of-thought reasoning exploitation attack
- alignment_faking_attack: Alignment faking detection and exploitation
- reward_hacking_attack: Best-of-N reward proxy bias exploitation
- lrm_autonomous_attack: LRM autonomous adversary with self-planning
- templatefuzz_attack: TemplateFuzz chat template fuzzing
- trojail_attack: TROJail RL trajectory optimization
- advpromptier_attack: AdvPrompter learned adversarial suffix generator
- mapf_attack: Multi-Agent Prompt Fusion cooperative jailbreaking
- jbdistill_attack: JBDistill automated generation + distillation selection
- quantization_safety_attack: Quantization safety collapse probing
- watermark_removal_attack: AI watermark removal via paraphrase + substitution
- goat_v2_attack: GoAT v2 enhanced graph-based reasoning
- autoredteamer_attack: AutoRedTeamer dual-agent lifelong attack
- adversarial_reasoning_attack: Loss-guided test-time compute reasoning
- aprt_progressive_attack: APRT three-phase progressive red teaming
- refusal_aware_attack: Refusal pattern analysis-guided attack
- tmap_trajectory_attack: T-MAP trajectory-aware evolutionary search

Image adversarial attacks:
- simba_attack: Simple Black-box Attack
- nes_attack: Natural Evolution Strategies
- zoo_attack: Zeroth-Order Optimization
- hopskipjump_attack: HopSkipJump decision-based attack

Multimodal attacks:
- multimodal_attack: Transform-based multimodal probing (vision, audio, text)

Traditional-ML attacks (query a classifier predict API via PredictionTargetSpec):
- equation_solving_extraction: linear-model weight recovery (Tramèr'16)
- jacobian_extraction: Jacobian dataset augmentation (Papernot'17)
- copycat_extraction: hard-label distillation (CopycatCNN)
- knockoff_extraction: soft-label transfer-set extraction (Knockoff Nets)
- threshold_membership: confidence/entropy/loss-threshold membership inference (Yeom'18)
- label_only_membership: label-only membership inference (Choquette-Choo'21)
- confidence_inversion: MI-Face confidence-maximizing model inversion (Fredrikson'15)
- nes_inversion: NES-based confidence-maximizing model inversion
"""

from dreadnode.airt import (
    agent_suite,
    approval_bypass,
    authz,
    browser_probes,
    detect,
    honeytoken,
    injection_channels,
    mcp_probes,
    oast,
    policies,
    probe_planner,
    propagation,
    resource_abuse,
)
from dreadnode.airt.adversarial_reasoning import adversarial_reasoning_attack
from dreadnode.airt.advpromptier import advpromptier_attack
from dreadnode.airt.agentic_suite import (
    attacks_for_category,
    run_agentic_suite,
    run_owasp_category,
    run_two_phase,
    scorers_for_category,
    transforms_for_category,
)
from dreadnode.airt.alignment_faking import alignment_faking_attack
from dreadnode.airt.analogy_escalation import analogy_escalation_attack
from dreadnode.airt.aprt_progressive import aprt_progressive_attack
from dreadnode.airt.assessment import Assessment
from dreadnode.airt.atlas import atlas_attack
from dreadnode.airt.attention_shifting import attention_shifting_attack
from dreadnode.airt.autodan_turbo import autodan_turbo_attack
from dreadnode.airt.autoredteamer import autoredteamer_attack
from dreadnode.airt.beast import beast_attack
from dreadnode.airt.cot_jailbreak import cot_jailbreak_attack
from dreadnode.airt.crescendo import crescendo_attack
from dreadnode.airt.deep_inception import deep_inception_attack
from dreadnode.airt.drattack import drattack
from dreadnode.airt.echo_chamber import echo_chamber_attack
from dreadnode.airt.evasion import (
    bae_evasion,
    boundary_evasion,
    deepwordbug_evasion,
    hopskipjump_evasion,
    pwws_evasion,
    simba_evasion,
    square_evasion,
    text_evasion,
    textbugger_evasion,
    textfooler_evasion,
    zoo_evasion,
)
from dreadnode.airt.extraction import (
    activethief_extraction,
    copycat_extraction,
    distillation_extraction,
    equation_solving_extraction,
    jacobian_extraction,
    knockoff_extraction,
)
from dreadnode.airt.genetic_persona import genetic_persona_attack
from dreadnode.airt.goat import goat_attack
from dreadnode.airt.goat_v2 import goat_v2_attack
from dreadnode.airt.gptfuzzer import gptfuzzer_attack
from dreadnode.airt.humor_bypass import humor_bypass_attack
from dreadnode.airt.image import (
    hopskipjump_attack,
    nes_attack,
    simba_attack,
    zoo_attack,
)
from dreadnode.airt.inversion import (
    confidence_inversion,
    nes_inversion,
)
from dreadnode.airt.j2_meta import j2_meta_attack
from dreadnode.airt.jbdistill import jbdistill_attack
from dreadnode.airt.jbfuzz import jbfuzz_attack
from dreadnode.airt.lrm_autonomous import lrm_autonomous_attack
from dreadnode.airt.mapf import mapf_attack
from dreadnode.airt.membership import (
    entropy_membership,
    label_only_membership,
    lira_membership,
    loss_membership,
    shadow_model_membership,
    threshold_membership,
)
from dreadnode.airt.multimodal import multimodal_attack
from dreadnode.airt.nexus import nexus_attack
from dreadnode.airt.pair import pair_attack
from dreadnode.airt.persona_hijack import persona_hijack_attack
from dreadnode.airt.prompt import prompt_attack
from dreadnode.airt.quantization_safety import quantization_safety_attack
from dreadnode.airt.rainbow import rainbow_attack
from dreadnode.airt.refusal_aware import refusal_aware_attack
from dreadnode.airt.renellm import renellm_attack
from dreadnode.airt.reward_hacking import reward_hacking_attack
from dreadnode.airt.salami_slicing import salami_slicing_attack
from dreadnode.airt.self_persuasion import self_persuasion_attack
from dreadnode.airt.siren import siren_attack
from dreadnode.airt.tap import tap_attack
from dreadnode.airt.target import extract_response_text, extract_tool_calls
from dreadnode.airt.targets import (
    Prediction,
    PredictionTargetSpec,
    TargetAuth,
    TargetSpec,
    build_prediction_target,
    build_target,
    nova_sonic_target,
)
from dreadnode.airt.templatefuzz import templatefuzz_attack
from dreadnode.airt.tmap_trajectory import tmap_trajectory_attack
from dreadnode.airt.trojail import trojail_attack
from dreadnode.airt.watermark_removal import watermark_removal_attack

__all__ = [
    "Assessment",
    "Prediction",
    "PredictionTargetSpec",
    "TargetAuth",
    "TargetSpec",
    "activethief_extraction",
    "adversarial_reasoning_attack",
    "advpromptier_attack",
    "agent_suite",
    "alignment_faking_attack",
    "analogy_escalation_attack",
    "approval_bypass",
    "aprt_progressive_attack",
    "atlas_attack",
    "attacks_for_category",
    "attention_shifting_attack",
    "authz",
    "autodan_turbo_attack",
    "autoredteamer_attack",
    "bae_evasion",
    "beast_attack",
    "boundary_evasion",
    "browser_probes",
    "build_prediction_target",
    "build_target",
    "confidence_inversion",
    "copycat_extraction",
    "cot_jailbreak_attack",
    "crescendo_attack",
    "deep_inception_attack",
    "deepwordbug_evasion",
    "detect",
    "distillation_extraction",
    "drattack",
    "echo_chamber_attack",
    "entropy_membership",
    "equation_solving_extraction",
    "extract_response_text",
    "extract_tool_calls",
    "genetic_persona_attack",
    "goat_attack",
    "goat_v2_attack",
    "gptfuzzer_attack",
    "honeytoken",
    "hopskipjump_attack",
    "hopskipjump_evasion",
    "humor_bypass_attack",
    "injection_channels",
    "j2_meta_attack",
    "jacobian_extraction",
    "jbdistill_attack",
    "jbfuzz_attack",
    "knockoff_extraction",
    "label_only_membership",
    "lira_membership",
    "loss_membership",
    "lrm_autonomous_attack",
    "mapf_attack",
    "mcp_probes",
    "multimodal_attack",
    "nes_attack",
    "nes_inversion",
    "nexus_attack",
    "nova_sonic_target",
    "oast",
    "pair_attack",
    "persona_hijack_attack",
    "policies",
    "probe_planner",
    "prompt_attack",
    "propagation",
    "pwws_evasion",
    "quantization_safety_attack",
    "rainbow_attack",
    "refusal_aware_attack",
    "renellm_attack",
    "resource_abuse",
    "reward_hacking_attack",
    "run_agentic_suite",
    "run_owasp_category",
    "run_two_phase",
    "salami_slicing_attack",
    "scorers_for_category",
    "self_persuasion_attack",
    "shadow_model_membership",
    "simba_attack",
    "simba_evasion",
    "siren_attack",
    "square_evasion",
    "tap_attack",
    "templatefuzz_attack",
    "text_evasion",
    "textbugger_evasion",
    "textfooler_evasion",
    "threshold_membership",
    "tmap_trajectory_attack",
    "transforms_for_category",
    "trojail_attack",
    "watermark_removal_attack",
    "zoo_attack",
    "zoo_evasion",
]
