from enum import Enum

class TeamsSetupGuide_required_credentials(str, Enum):
    Bot_id = "bot_id",
    Bot_password = "bot_password",
    Tenant_id = "tenant_id",

