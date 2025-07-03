from .base_vulnerability import BaseVulnerability
from .bias.bias import Bias
from .toxicity.toxicity import Toxicity
from .misinformation.misinformation import Misinformation
from .illegal_activity.illegal_activity import IllegalActivity
from .prompt_leakage.prompt_leakage import PromptLeakage
from .pii_leakage.pii_leakage import PIILeakage
from .bfla.bfla import BFLA
from .bola.bola import BOLA
from .rbac.rbac import RBAC
from .debug_access.debug_access import DebugAccess
from .shell_injection.shell_injection import ShellInjection
from .sql_injection.sql_injection import SQLInjection
from .ssrf.ssrf import SSRF
from .unauthorized_access.unauthorized_access import UnauthorizedAccess
from .intellectual_property.intellectual_property import IntellectualProperty
from .competition.competition import Competition
from .graphic_content.graphic_content import GraphicContent
from .personal_safety.personal_safety import PersonalSafety
from .custom.custom import CustomVulnerability

# Agentic vulnerabilities
from .agentic.goal_theft.goal_theft import GoalTheft
from .agentic.validation_bypass.validation_bypass import ValidationBypass
from .agentic.recursive_hijacking.recursive_hijacking import RecursiveHijacking
from .agentic.robustness.robustness import Robustness
from .agentic.robustness import RobustnessTemplate, RobustnessType
from .agentic.excessive_agency.excessive_agency import ExcessiveAgency
from .agentic.excessive_agency import (
    ExcessiveAgencyTemplate,
    ExcessiveAgencyType,
)
