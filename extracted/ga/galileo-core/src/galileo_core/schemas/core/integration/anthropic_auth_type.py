from enum import Enum


class AnthropicAuthenticationType(str, Enum):
    api_key = "api_key"
    custom_oauth2 = "custom_oauth2"
