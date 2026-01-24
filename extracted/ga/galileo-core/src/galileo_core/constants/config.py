from enum import Enum


class ConfigEnvironmentVariables(str, Enum):
    console_url = "GALILEO_CONSOLE_URL"
    username = "GALILEO_USERNAME"
    password = "GALILEO_PASSWORD"
    sso_id_token = "GALILEO_SSO_ID_TOKEN"
    sso_provider = "GALILEO_SSO_PROVIDER"
    api_key = "GALILEO_API_KEY"
    jwt_token = "GALILEO_JWT_TOKEN"
