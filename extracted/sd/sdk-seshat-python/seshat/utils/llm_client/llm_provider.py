from enum import StrEnum


class LLMProvider(StrEnum):
    OPENAI = "openai"
    BEDROCK = "bedrock"
    GOOGLE = "google"
    PROXY = "proxy"
