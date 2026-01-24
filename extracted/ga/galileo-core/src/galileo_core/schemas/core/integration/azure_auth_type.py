from enum import Enum


class AzureAuthenticationType(str, Enum):
    api_key = "api_key"
    client_secret = "client_secret"
    username_password = "username_password"
    custom_oauth2 = "custom_oauth2"
