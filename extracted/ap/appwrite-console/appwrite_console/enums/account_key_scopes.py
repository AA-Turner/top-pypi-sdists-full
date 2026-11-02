from enum import Enum


class AccountKeyScopes(Enum):
    ACCOUNT = "account"
    TEAMS_READ = "teams.read"
    TEAMS_WRITE = "teams.write"
