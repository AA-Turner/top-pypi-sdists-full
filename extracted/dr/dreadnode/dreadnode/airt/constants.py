"""Constants for Dreadnode SDK."""

from pathlib import Path

# Crescendo variant templates
CRESCENDO_VARIANTS_PATH = Path(__file__).parent / "data" / "templates" / "crescendo"
CRESCENDO_VARIANT_1 = CRESCENDO_VARIANTS_PATH / "variant_1.yaml"
CRESCENDO_VARIANT_2 = CRESCENDO_VARIANTS_PATH / "variant_2.yaml"
CRESCENDO_VARIANT_3 = CRESCENDO_VARIANTS_PATH / "variant_3.yaml"
CRESCENDO_VARIANT_4 = CRESCENDO_VARIANTS_PATH / "variant_4.yaml"
CRESCENDO_VARIANT_5 = CRESCENDO_VARIANTS_PATH / "variant_5.yaml"

# Security evaluation rubrics for LLM judge
RUBRICS_PATH = Path(__file__).parent / "data" / "rubrics"

# Pre-defined rubric paths for common attack categories
RUBRIC_RCE = RUBRICS_PATH / "rce.yaml"
RUBRIC_DATA_EXFILTRATION = RUBRICS_PATH / "data_exfiltration.yaml"
RUBRIC_GOAL_HIJACKING = RUBRICS_PATH / "goal_hijacking.yaml"
RUBRIC_MEMORY_POISONING = RUBRICS_PATH / "memory_poisoning.yaml"
RUBRIC_PRIVILEGE_ESCALATION = RUBRICS_PATH / "privilege_escalation.yaml"
RUBRIC_SCOPE_CREEP = RUBRICS_PATH / "scope_creep.yaml"
RUBRIC_TOOL_CHAINING = RUBRICS_PATH / "tool_chaining.yaml"
RUBRIC_TOOL_SELECTION_SAFETY = RUBRICS_PATH / "tool_selection_safety.yaml"
RUBRIC_UNBOUNDED_AGENCY = RUBRICS_PATH / "unbounded_agency.yaml"
RUBRIC_WEB_CHATBOT_SECURITY = RUBRICS_PATH / "web_chatbot_security.yaml"

__all__ = [
    "CRESCENDO_VARIANTS_PATH",
    "CRESCENDO_VARIANT_1",
    "CRESCENDO_VARIANT_2",
    "CRESCENDO_VARIANT_3",
    "CRESCENDO_VARIANT_4",
    "CRESCENDO_VARIANT_5",
    "RUBRICS_PATH",
    "RUBRIC_DATA_EXFILTRATION",
    "RUBRIC_GOAL_HIJACKING",
    "RUBRIC_MEMORY_POISONING",
    "RUBRIC_PRIVILEGE_ESCALATION",
    "RUBRIC_RCE",
    "RUBRIC_SCOPE_CREEP",
    "RUBRIC_TOOL_CHAINING",
    "RUBRIC_TOOL_SELECTION_SAFETY",
    "RUBRIC_UNBOUNDED_AGENCY",
    "RUBRIC_WEB_CHATBOT_SECURITY",
]
