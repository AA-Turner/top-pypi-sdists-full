from enum import Enum


class SettingSourceSourceEnum(str, Enum):
    ADMIN = "admin"
    API = "api"
    APPLICATION = "application"
    CLI = "cli"
    DEPLOYMENT = "deployment"
    MIGRATION = "migration"

    def __str__(self) -> str:
        return str(self.value)
