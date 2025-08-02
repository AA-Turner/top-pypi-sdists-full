from enum import Enum


class EditCopilotConfigJsonBodyCodeCompletionModelProvider(str, Enum):
    ANTHROPIC = "anthropic"
    AZURE_OPENAI = "azure_openai"
    CUSTOMAI = "customai"
    DEEPSEEK = "deepseek"
    GOOGLEAI = "googleai"
    GROQ = "groq"
    MISTRAL = "mistral"
    OPENAI = "openai"
    OPENROUTER = "openrouter"
    TOGETHERAI = "togetherai"

    def __str__(self) -> str:
        return str(self.value)
