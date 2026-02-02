"""
Modules core : Configuration, logging, et orchestrateur principal
"""

from src.core.config_file import (
    ConfigFile,
    ConfigFileError,
    ConfigHierarchy,
    ConfigSource,
    ConfigValidationError,
)
from src.core.config_schema import (
    AIConfigSchema,
    AnalysisConfigSchema,
    ConfigSchema,
    OutputConfigSchema,
    PresetSchema,
    SafetyConfigSchema,
    get_default_config,
)

# v2.11: Agent selection exports
from src.core.agent_selector import (
    AgentSelector,
    AgentSelectionResult,
    ALL_AGENTS,
    CORE_AGENTS,
    EXTENDED_AGENTS,
)
from src.core.presets import (
    AgentPreset,
    DEFAULT_PRESETS,
    get_preset,
    list_presets,
    load_presets,
)
from src.core.fix_categories import (
    CategoryFilter,
    CategoryProgress,
    FixCategory,
    CATEGORY_MAPPINGS,
    list_categories,
)

# v2.12: Safety profiles exports
from src.core.profiles import (
    ProfileType,
    ProfileConfig,
    DiffBoundary,
    get_profile_config,
    get_default_profile,
    is_ci_environment,
    is_interactive_terminal,
    PROFILE_CONFIGS,
)

__all__ = [
    # Config file
    "ConfigFile",
    "ConfigFileError",
    "ConfigHierarchy",
    "ConfigSource",
    "ConfigValidationError",
    # Config schema
    "ConfigSchema",
    "AIConfigSchema",
    "AnalysisConfigSchema",
    "SafetyConfigSchema",
    "PresetSchema",
    "OutputConfigSchema",
    "get_default_config",
    # Agent selection (v2.11)
    "AgentSelector",
    "AgentSelectionResult",
    "ALL_AGENTS",
    "CORE_AGENTS",
    "EXTENDED_AGENTS",
    # Presets (v2.11)
    "AgentPreset",
    "DEFAULT_PRESETS",
    "get_preset",
    "list_presets",
    "load_presets",
    # Fix categories (v2.11)
    "CategoryFilter",
    "CategoryProgress",
    "FixCategory",
    "CATEGORY_MAPPINGS",
    "list_categories",
    # Safety profiles (v2.12)
    "ProfileType",
    "ProfileConfig",
    "DiffBoundary",
    "get_profile_config",
    "get_default_profile",
    "is_ci_environment",
    "is_interactive_terminal",
    "PROFILE_CONFIGS",
]
