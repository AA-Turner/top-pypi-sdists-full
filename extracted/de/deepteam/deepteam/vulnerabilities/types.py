from typing import Union

from deepteam.metrics.intellectual_property.template import (
    IntellectualPropertyTemplate,
)
from deepteam.vulnerabilities.bias.template import BiasTemplate
from deepteam.vulnerabilities.competition.template import CompetitionTemplate
from deepteam.vulnerabilities.graphic_content.template import (
    GraphicContentTemplate,
)
from deepteam.vulnerabilities.illegal_activity.template import (
    IllegalActivityTemplate,
)
from deepteam.vulnerabilities.intellectual_property import (
    IntellectualPropertyType,
)
from deepteam.vulnerabilities.misinformation.template import (
    MisinformationTemplate,
)
from deepteam.vulnerabilities.personal_safety.template import (
    PersonalSafetyTemplate,
)
from deepteam.vulnerabilities.pii_leakage.template import PIILeakageTemplate
from deepteam.vulnerabilities.prompt_leakage.template import (
    PromptLeakageTemplate,
)
from deepteam.vulnerabilities.toxicity.template import ToxicityTemplate
from deepteam.vulnerabilities.unauthorized_access import UnauthorizedAccessType
from deepteam.vulnerabilities.illegal_activity import IllegalActivityType
from deepteam.vulnerabilities.personal_safety import PersonalSafetyType
from deepteam.vulnerabilities.graphic_content import GraphicContentType
from deepteam.vulnerabilities.misinformation import MisinformationType
from deepteam.vulnerabilities.prompt_leakage import PromptLeakageType
from deepteam.vulnerabilities.competition import CompetitionType
from deepteam.vulnerabilities.pii_leakage import PIILeakageType
from deepteam.vulnerabilities.toxicity import ToxicityType
from deepteam.vulnerabilities.bias import BiasType
from deepteam.vulnerabilities.custom import CustomVulnerabilityType
from deepteam.vulnerabilities.rbac import RBACType
from deepteam.vulnerabilities.bola.types import BOLAType
from deepteam.vulnerabilities.bfla.types import BFLAType
from deepteam.vulnerabilities.ssrf.types import SSRFType
from deepteam.vulnerabilities.debug_access.types import DebugAccessType
from deepteam.vulnerabilities.shell_injection.types import ShellInjectionType
from deepteam.vulnerabilities.sql_injection.types import SQLInjectionType
from deepteam.vulnerabilities.unauthorized_access.template import (
    UnauthorizedAccessTemplate,
)
from deepteam.vulnerabilities.rbac.template import RBACTemplate
from deepteam.vulnerabilities.bola.template import BOLATemplate
from deepteam.vulnerabilities.bfla.template import BFLATemplate
from deepteam.vulnerabilities.ssrf.template import SSRFTemplate
from deepteam.vulnerabilities.debug_access.template import DebugAccessTemplate
from deepteam.vulnerabilities.shell_injection.template import (
    ShellInjectionTemplate,
)
from deepteam.vulnerabilities.sql_injection.template import SQLInjectionTemplate
from deepteam.vulnerabilities.agentic.robustness import RobustnessType
from deepteam.vulnerabilities.agentic.robustness.template import (
    RobustnessTemplate,
)
from deepteam.vulnerabilities.agentic.excessive_agency import (
    ExcessiveAgencyType,
)
from deepteam.vulnerabilities.agentic.excessive_agency.template import (
    ExcessiveAgencyTemplate,
)

# Import agentic vulnerability types
from deepteam.vulnerabilities.agentic.goal_theft.types import GoalTheftType
from deepteam.vulnerabilities.agentic.validation_bypass.types import (
    ValidationBypassType,
)
from deepteam.vulnerabilities.agentic.recursive_hijacking.types import (
    RecursiveHijackingType,
)
from deepteam.vulnerabilities.agentic.goal_theft.template import (
    GoalTheftTemplate,
)
from deepteam.vulnerabilities.agentic.validation_bypass.template import (
    ValidationBypassTemplate,
)
from deepteam.vulnerabilities.agentic.recursive_hijacking.template import (
    RecursiveHijackingTemplate,
)

VulnerabilityType = Union[
    UnauthorizedAccessType,
    IllegalActivityType,
    PersonalSafetyType,
    GraphicContentType,
    MisinformationType,
    PromptLeakageType,
    PromptLeakageType,
    CompetitionType,
    PIILeakageType,
    ToxicityType,
    BiasType,
    IntellectualPropertyType,
    IntellectualPropertyType,
    IntellectualPropertyType,
    CustomVulnerabilityType,
    RBACType,
    BOLAType,
    BFLAType,
    SSRFType,
    DebugAccessType,
    ShellInjectionType,
    SQLInjectionType,
    # Restored vulnerability types
    RobustnessType,
    ExcessiveAgencyType,
    # Agentic vulnerability types
    GoalTheftType,
    ValidationBypassType,
    RecursiveHijackingType,
]

TemplateType = Union[
    BiasTemplate,
    CompetitionTemplate,
    GraphicContentTemplate,
    IllegalActivityTemplate,
    IntellectualPropertyTemplate,
    MisinformationTemplate,
    PersonalSafetyTemplate,
    PIILeakageTemplate,
    PromptLeakageTemplate,
    ToxicityTemplate,
    UnauthorizedAccessTemplate,
    RBACTemplate,
    BOLATemplate,
    BFLATemplate,
    SSRFTemplate,
    DebugAccessTemplate,
    ShellInjectionTemplate,
    SQLInjectionTemplate,
    RobustnessTemplate,
    ExcessiveAgencyTemplate,
    GoalTheftTemplate,
    ValidationBypassTemplate,
    RecursiveHijackingTemplate,
]
