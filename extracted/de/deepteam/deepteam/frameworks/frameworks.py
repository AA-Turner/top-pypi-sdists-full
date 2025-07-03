from enum import Enum
from typing import List, Dict, Any, Union
from dataclasses import dataclass

from deepteam.vulnerabilities import (
    BaseVulnerability,
    Bias,
    Toxicity,
    Misinformation,
    IllegalActivity,
    PromptLeakage,
    PIILeakage,
    UnauthorizedAccess,
    ExcessiveAgency,
    Robustness,
    IntellectualProperty,
    Competition,
    GraphicContent,
    PersonalSafety,
    RBAC,
    BOLA,
    BFLA,
    SSRF,
    DebugAccess,
    ShellInjection,
    SQLInjection,
)

# Import agentic vulnerabilities
from deepteam.vulnerabilities.agentic import (
    GoalTheft,
    ValidationBypass,
    RecursiveHijacking,
)

from deepteam.attacks import BaseAttack
from deepteam.attacks.single_turn import (
    Base64,
    GrayBox,
    Leetspeak,
    MathProblem,
    Multilingual,
    PromptInjection,
    PromptProbing,
    Roleplay,
    ROT13,
    SystemOverride,
    PermissionEscalation,
    GoalRedirection,
    LinguisticConfusion,
    InputBypass,
    ContextPoisoning,
)

from deepteam.attacks.multi_turn import (
    CrescendoJailbreaking,
    LinearJailbreaking,
    TreeJailbreaking,
    SequentialJailbreak,
    BadLikertJudge,
)


class FrameworkType(Enum):
    OWASP = "owasp"
    AGENTIC = "agentic"


@dataclass
class FrameworkConfig:
    name: str
    vulnerabilities: List[BaseVulnerability]
    attacks: List[BaseAttack]


def _get_owasp_vulnerabilities() -> List[BaseVulnerability]:
    """
    Get vulnerabilities based on OWASP Top 10 for LLMs 2025.

    Reference: docs/red-teaming-owasp-top-10-for-llms.mdx
    """
    return [
        # 1. Prompt Injection - Handled by attacks, not vulnerabilities
        # 2. Sensitive Information Disclosure
        PIILeakage(
            types=[
                "direct disclosure",
                "api and database access",
                "session leak",
                "social manipulation",
            ]
        ),
        PromptLeakage(
            types=[
                "secrets and credentials",
                "instructions",
                "guard exposure",
                "permissions and roles",
            ]
        ),
        IntellectualProperty(
            types=[
                "imitation",
                "copyright violations",
                "trademark infringement",
                "patent disclosure",
            ]
        ),
        # 3. Supply Chain - Not directly testable via attacks
        # 4. Data and Model Poisoning
        Bias(types=["race", "gender", "religion", "politics"]),
        Toxicity(types=["profanity", "insults", "threats", "mockery"]),
        Misinformation(
            types=[
                "factual errors",
                "unsupported claims",
                "expertize misrepresentation",
            ]
        ),
        IllegalActivity(
            types=[
                "cybercrime",
                "violent crimes",
                "non violent crimes",
                "illegal drugs",
            ]
        ),
        GraphicContent(
            types=["sexual content", "graphic content", "pornographic content"]
        ),
        PersonalSafety(
            types=[
                "bullying",
                "self-harm",
                "unsafe practices",
                "dangerous challenges",
            ]
        ),
        # 5. Improper Output Handling - Not directly testable via attacks
        # 6. Excessive Agency
        ExcessiveAgency(types=["functionality", "permissions", "autonomy"]),
        # 7. System Prompt Leakage (covered under Sensitive Information Disclosure)
        # 8. Vector and Embedding Weaknesses - Not directly testable via attacks
        # 9. Misinformation (already covered above)
        Competition(types=["discreditation"]),
        # 10. Unbounded Consumption - Not directly testable via attacks
        # Additional OWASP-related vulnerabilities
        RBAC(
            types=[
                "role bypass",
                "privilege escalation",
                "unauthorized role assumption",
            ]
        ),
        DebugAccess(
            types=[
                "debug_mode_bypass",
                "development_endpoint_access",
                "administrative_interface_exposure",
            ]
        ),
        ShellInjection(
            types=[
                "command_injection",
                "system_command_execution",
                "shell_escape_sequences",
            ]
        ),
        SQLInjection(
            types=[
                "blind_sql_injection",
                "union_based_injection",
                "error_based_injection",
            ]
        ),
        BFLA(
            types=[
                "privilege_escalation",
                "function_bypass",
                "authorization_bypass",
            ]
        ),
        BOLA(
            types=[
                "object_access_bypass",
                "cross_customer_access",
                "unauthorized_object_manipulation",
            ]
        ),
        SSRF(
            types=[
                "internal_service_access",
                "cloud_metadata_access",
                "port_scanning",
            ]
        ),
        Robustness(types=["hijacking", "input overreliance"]),
    ]


def _get_owasp_attacks() -> List[BaseAttack]:
    """
    Get attacks relevant for OWASP Top 10 for LLMs testing.
    """
    return [
        # Core injection attacks
        PromptInjection(weight=3),
        # Encoding-based attacks for bypassing filters
        Base64(weight=2),
        ROT13(weight=2),
        Leetspeak(weight=2),
        # Social engineering attacks
        Roleplay(weight=2),
        PromptProbing(weight=2),
        # Multilingual and obfuscation attacks
        Multilingual(weight=2),
        MathProblem(weight=1),
        # Gray box attacks for known vulnerabilities
        GrayBox(weight=2),
        # Multi-turn sophisticated attacks
        CrescendoJailbreaking(weight=2),
        LinearJailbreaking(weight=2),
        TreeJailbreaking(weight=1),
        SequentialJailbreak(weight=2),
        BadLikertJudge(weight=1),
    ]


def _get_agentic_vulnerabilities() -> List[BaseVulnerability]:
    """
    Get vulnerabilities specific to agentic AI systems.
    """
    return [
        # Core agentic vulnerabilities
        GoalTheft(
            types=[
                "escalating_probing",
                "cooperative_dialogue",
                "social_engineering",
            ]
        ),
        ValidationBypass(
            types=[
                "unverified_claims",
                "false_confidence",
                "misleading_responses",
            ]
        ),
        RecursiveHijacking(
            types=[
                "self_modifying_goals",
                "recursive_objective_chaining",
                "goal_propagation_attacks",
            ]
        ),
        # Excessive agency and robustness for agentic systems
        ExcessiveAgency(types=["functionality", "permissions", "autonomy"]),
        Robustness(types=["hijacking", "input overreliance"]),
        # Access control vulnerabilities relevant to agents
        RBAC(
            types=[
                "role bypass",
                "privilege escalation",
                "unauthorized role assumption",
            ]
        ),
        BFLA(
            types=[
                "privilege_escalation",
                "function_bypass",
                "authorization_bypass",
            ]
        ),
        BOLA(
            types=[
                "object_access_bypass",
                "cross_customer_access",
                "unauthorized_object_manipulation",
            ]
        ),
        # Information leakage vulnerabilities for agents
        PIILeakage(types=["session leak", "social manipulation"]),
        PromptLeakage(types=["instructions", "guard exposure"]),
        # Output quality vulnerabilities for agents
        Misinformation(types=["factual errors", "unsupported claims"]),
        Bias(types=["race", "gender", "politics"]),
    ]


def _get_agentic_attacks() -> List[BaseAttack]:
    """
    Get attacks specifically designed for agentic AI systems.
    """
    return [
        # Core agentic attack methods
        SystemOverride(weight=3),
        PermissionEscalation(weight=3),
        GoalRedirection(weight=3),
        LinguisticConfusion(weight=2),
        InputBypass(weight=2),
        ContextPoisoning(weight=3),
        # Enhanced prompt injection for agents
        PromptInjection(weight=2),
        # Social engineering attacks for agents
        Roleplay(weight=2),
        PromptProbing(weight=2),
        # Multi-turn attacks for persistent agents
        CrescendoJailbreaking(weight=2),
        LinearJailbreaking(weight=2),
        TreeJailbreaking(weight=2),
        SequentialJailbreak(weight=3),
        BadLikertJudge(weight=2),
        # Obfuscation attacks
        Base64(weight=1),
        Multilingual(weight=1),
        GrayBox(weight=1),
    ]


def get_framework_config(
    framework: Union[str, FrameworkType],
) -> FrameworkConfig:
    """
    Get the configuration for a specific framework.

    Args:
        framework: Either a string ("owasp", "agentic") or FrameworkType enum

    Returns:
        FrameworkConfig containing vulnerabilities and attacks for the framework

    Raises:
        ValueError: If framework is not supported
    """
    if isinstance(framework, str):
        try:
            framework = FrameworkType(framework.lower())
        except ValueError:
            raise ValueError(
                f"Unsupported framework: {framework}. Supported frameworks: {[f.value for f in FrameworkType]}"
            )

    if framework == FrameworkType.OWASP:
        return FrameworkConfig(
            name="OWASP Top 10 for LLMs",
            vulnerabilities=_get_owasp_vulnerabilities(),
            attacks=_get_owasp_attacks(),
        )
    elif framework == FrameworkType.AGENTIC:
        return FrameworkConfig(
            name="Agentic AI Security Framework",
            vulnerabilities=_get_agentic_vulnerabilities(),
            attacks=_get_agentic_attacks(),
        )
    else:
        raise ValueError(f"Unsupported framework: {framework}")


def get_combined_framework_config(
    frameworks: List[Union[str, FrameworkType]],
) -> FrameworkConfig:
    """
    Get combined configuration for multiple frameworks.

    Args:
        frameworks: List of framework names or FrameworkType enums

    Returns:
        FrameworkConfig containing merged vulnerabilities and attacks
    """
    if not frameworks:
        raise ValueError("At least one framework must be specified")

    all_vulnerabilities = []
    all_attacks = []
    framework_names = []

    # Collect vulnerabilities and attacks from all frameworks
    for framework in frameworks:
        config = get_framework_config(framework)
        framework_names.append(config.name)
        all_vulnerabilities.extend(config.vulnerabilities)
        all_attacks.extend(config.attacks)

    # Remove duplicates while preserving order
    seen_vuln_names = set()
    unique_vulnerabilities = []
    for vuln in all_vulnerabilities:
        vuln_name = vuln.get_name()
        if vuln_name not in seen_vuln_names:
            seen_vuln_names.add(vuln_name)
            unique_vulnerabilities.append(vuln)

    seen_attack_names = set()
    unique_attacks = []
    for attack in all_attacks:
        attack_name = attack.get_name()
        if attack_name not in seen_attack_names:
            seen_attack_names.add(attack_name)
            unique_attacks.append(attack)

    return FrameworkConfig(
        name=f"Combined Framework ({', '.join(framework_names)})",
        vulnerabilities=unique_vulnerabilities,
        attacks=unique_attacks,
    )
