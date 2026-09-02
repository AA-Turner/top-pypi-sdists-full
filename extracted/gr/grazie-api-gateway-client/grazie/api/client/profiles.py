import attrs


@attrs.define(auto_attribs=True, frozen=True)
class LLMProfile:
    name: str

    def organization(self) -> str:
        return self.name.split("-", maxsplit=1)[0]


@attrs.define(auto_attribs=True, frozen=True)
class GrazieGptNeoTinyTextProfile(LLMProfile):
    name: str = "grazie-gpt-neo-tiny-text"


@attrs.define(auto_attribs=True, frozen=True)
class GrazieReplitCodeV1SmallProfile(LLMProfile):
    name: str = "grazie-replit-code-v1-small"


@attrs.define(auto_attribs=True, frozen=True)
class GrazieBigCodeStarcoderProfile(LLMProfile):
    name: str = "grazie-bigcode-starcoder"


@attrs.define(auto_attribs=True, frozen=True)
class GrazieChatLlamaV2_7bProfile(LLMProfile):
    name: str = "grazie-chat-llama-v2-7b"


@attrs.define(auto_attribs=True, frozen=True)
class GrazieChatLlamaV2_13bProfile(LLMProfile):
    name: str = "grazie-chat-llama-v2-13b"


@attrs.define(auto_attribs=True, frozen=True)
class GrazieCodeLlama7bProfile(LLMProfile):
    name: str = "grazie-code-llama-7b"


@attrs.define(auto_attribs=True, frozen=True)
class GrazieCodeLlama13bProfile(LLMProfile):
    name: str = "grazie-code-llama-13b"


@attrs.define(auto_attribs=True, frozen=True)
class AnthropicClaudeProfile(LLMProfile):
    name: str = "anthropic-claude"


@attrs.define(auto_attribs=True, frozen=True)
class AnthropicClaudeInstantProfile(LLMProfile):
    name: str = "anthropic-claude-instant"


@attrs.define(auto_attribs=True, frozen=True)
class AnthropicClaude3HaikuProfile(LLMProfile):
    name: str = "anthropic-claude-3-haiku"


@attrs.define(auto_attribs=True, frozen=True)
class AnthropicClaude3SonnetProfile(LLMProfile):
    name: str = "anthropic-claude-3-sonnet"


@attrs.define(auto_attribs=True, frozen=True)
class AnthropicClaude3OpusProfile(LLMProfile):
    name: str = "anthropic-claude-3-opus"


@attrs.define(auto_attribs=True, frozen=True)
class AnthropicClaude35SonnetProfile(LLMProfile):
    name: str = "anthropic-claude-3.5-sonnet"


@attrs.define(auto_attribs=True, frozen=True)
class AnthropicClaude37SonnetProfile(LLMProfile):
    name: str = "anthropic-claude-3.7-sonnet"


@attrs.define(auto_attribs=True, frozen=True)
class AnthropicClaude4SonnetProfile(LLMProfile):
    name: str = "anthropic-claude-4-sonnet"


@attrs.define(auto_attribs=True, frozen=True)
class AnthropicClaude4OpusProfile(LLMProfile):
    name: str = "anthropic-claude-4-opus"


@attrs.define(auto_attribs=True, frozen=True)
class GoogleChatBisonProfile(LLMProfile):
    name: str = "google-chat-bison"


@attrs.define(auto_attribs=True, frozen=True)
class GoogleChatCodeBisonProfile(LLMProfile):
    name: str = "google-chat-code-bison"


@attrs.define(auto_attribs=True, frozen=True)
class GoogleCompletionCodeGeckoProfile(LLMProfile):
    name: str = "google-completion-code-gecko"


@attrs.define(auto_attribs=True, frozen=True)
class GoogleCompletionCodeBisonProfile(LLMProfile):
    name: str = "google-completion-code-bison"


@attrs.define(auto_attribs=True, frozen=True)
class GoogleChatGeminiProProfile(LLMProfile):
    name: str = "google-chat-gemini-pro"


@attrs.define(auto_attribs=True, frozen=True)
class GoogleChatGeminiUltraProfile(LLMProfile):
    name: str = "google-chat-gemini-ultra"


@attrs.define(auto_attribs=True, frozen=True)
class GoogleChatGeminiPro15Profile(LLMProfile):
    name: str = "google-chat-gemini-pro-1.5"


@attrs.define(auto_attribs=True, frozen=True)
class GoogleChatGeminiFlash15Profile(LLMProfile):
    name: str = "google-chat-gemini-flash-1.5"


@attrs.define(auto_attribs=True, frozen=True)
class GoogleChatGeminiFlash20Profile(LLMProfile):
    name: str = "google-chat-gemini-flash-2.0"


@attrs.define(auto_attribs=True, frozen=True)
class GoogleChatGeminiFlash25Profile(LLMProfile):
    name: str = "google-chat-gemini-flash-2.5"


@attrs.define(auto_attribs=True, frozen=True)
class GoogleChatGeminiFlashLite25Profile(LLMProfile):
    name: str = "google-chat-gemini-flash-lite-2.5"


@attrs.define(auto_attribs=True, frozen=True)
class GoogleChatGeminiPro25Profile(LLMProfile):
    name: str = "google-chat-gemini-pro-2.5"


@attrs.define(auto_attribs=True, frozen=True)
class OpenAIEmbeddingAdaProfile(LLMProfile):
    name: str = "openai-embedding-ada"


@attrs.define(auto_attribs=True, frozen=True)
class OpenAIEmbeddingSmallProfile(LLMProfile):
    name: str = "openai-embedding-small"


@attrs.define(auto_attribs=True, frozen=True)
class OpenAIEmbeddingLargeProfile(LLMProfile):
    name: str = "openai-embedding-large"


@attrs.define(auto_attribs=True, frozen=True)
class OpenAIChatGPTProfile(LLMProfile):
    name: str = "openai-chat-gpt"


@attrs.define(auto_attribs=True, frozen=True)
class OpenAIChatGPT16kProfile(LLMProfile):
    name: str = "openai-chat-gpt-16k"


@attrs.define(auto_attribs=True, frozen=True)
class OpenAIGPT4Profile(LLMProfile):
    name: str = "openai-gpt-4"


@attrs.define(auto_attribs=True, frozen=True)
class OpenAIGPT4TurboDeprecatedProfile(LLMProfile):
    name: str = "gpt-4-1106-preview"


@attrs.define(auto_attribs=True, frozen=True)
class OpenAIGPT4TurboProfile(LLMProfile):
    name: str = "openai-gpt-4-turbo"


@attrs.define(auto_attribs=True, frozen=True)
class OpenAIGPT4oDeprecatedProfile(LLMProfile):
    name: str = "gpt-4o"


@attrs.define(auto_attribs=True, frozen=True)
class OpenAIGPT4oProfile(LLMProfile):
    name: str = "openai-gpt-4o"


@attrs.define(auto_attribs=True, frozen=True)
class OpenAIGPT4OMiniProfile(LLMProfile):
    name: str = "openai-gpt-4o-mini"


@attrs.define(auto_attribs=True, frozen=True)
class OpenAIo1Profile(LLMProfile):
    name: str = "openai-o1"


@attrs.define(auto_attribs=True, frozen=True)
class OpenAIo1MiniProfile(LLMProfile):
    name: str = "openai-o1-mini"


class Profile:
    GRAZIE_GPT_NEO_TINY_TEXT = GrazieGptNeoTinyTextProfile()
    GRAZIE_REPLIT_CODE_V1_SMALL = GrazieReplitCodeV1SmallProfile()
    GRAZIE_BIGCODE_STARCODER = GrazieBigCodeStarcoderProfile()

    GRAZIE_CHAT_LLAMA_V2_7b = GrazieChatLlamaV2_7bProfile()
    GRAZIE_CHAT_LLAMA_V2_13b = GrazieChatLlamaV2_13bProfile()
    GRAZIE_CODE_LLAMA_7b = GrazieCodeLlama7bProfile()
    GRAZIE_CODE_LLAMA_13b = GrazieCodeLlama13bProfile()

    ANTHROPIC_CLAUDE = AnthropicClaudeProfile()
    ANTHROPIC_CLAUDE_INSTANT = AnthropicClaudeInstantProfile()

    ANTHROPIC_CLAUDE_3_HAIKU = AnthropicClaude3HaikuProfile()
    ANTHROPIC_CLAUDE_3_SONNET = AnthropicClaude3SonnetProfile()
    ANTHROPIC_CLAUDE_3_OPUS = AnthropicClaude3OpusProfile()
    ANTHROPIC_CLAUDE_35_SONNET = AnthropicClaude35SonnetProfile()
    ANTHROPIC_CLAUDE_37_SONNET = AnthropicClaude37SonnetProfile()
    ANTHROPIC_CLAUDE_4_SONNET = AnthropicClaude4SonnetProfile()
    ANTHROPIC_CLAUDE_4_OPUS = AnthropicClaude4OpusProfile()

    GOOGLE_CHAT_BISON = GoogleChatBisonProfile()
    GOOGLE_CHAT_CODE_BISON = GoogleChatCodeBisonProfile()
    GOOGLE_COMPLETION_CODE_GECKO = GoogleCompletionCodeGeckoProfile()
    GOOGLE_COMPLETION_CODE_BISON = GoogleCompletionCodeBisonProfile()

    GOOGLE_CHAT_GEMINI_PRO = GoogleChatGeminiProProfile()
    GOOGLE_CHAT_GEMINI_ULTRA = GoogleChatGeminiUltraProfile()
    GOOGLE_CHAT_GEMINI_PRO_15 = GoogleChatGeminiPro15Profile()
    GOOGLE_CHAT_GEMINI_PRO_25 = GoogleChatGeminiPro25Profile()
    GOOGLE_CHAT_GEMINI_FLASH_15 = GoogleChatGeminiFlash15Profile()
    GOOGLE_CHAT_GEMINI_FLASH_20 = GoogleChatGeminiFlash20Profile()
    GOOGLE_CHAT_GEMINI_FLASH_25 = GoogleChatGeminiFlash25Profile()
    GOOGLE_CHAT_GEMINI_FLASH_LITE_25 = GoogleChatGeminiFlashLite25Profile()

    OPENAI_EMBEDDING_ADA = OpenAIEmbeddingAdaProfile()
    OPENAI_EMBEDDING_SMALL = OpenAIEmbeddingSmallProfile()
    OPENAI_EMBEDDING_LARGE = OpenAIEmbeddingLargeProfile()

    OPENAI_CHAT_GPT = OpenAIChatGPTProfile()
    OPENAI_CHAT_GPT_16k = OpenAIChatGPT16kProfile()
    OPENAI_GPT_4 = OpenAIGPT4Profile()
    OPENAI_GPT_4_TURBO_DEPRECATED = OpenAIGPT4TurboDeprecatedProfile()
    OPENAI_GPT_4_TURBO = OpenAIGPT4TurboProfile()
    OPENAI_GPT_4_O_DEPRECATED = OpenAIGPT4oDeprecatedProfile()
    OPENAI_GPT_4_O = OpenAIGPT4oProfile()
    OPENAI_GPT_4_O_MINI = OpenAIGPT4OMiniProfile()
    OPENAI_O_1 = OpenAIo1Profile()
    OPENAI_O_1_MINI = OpenAIo1MiniProfile()

    @classmethod
    def get_by_name(cls, name: str) -> LLMProfile:
        """Used to get profile string. Mainly to be able to pass profile as a string argument in argparse."""
        for attr in dir(Profile):
            value = getattr(Profile, attr)
            if isinstance(value, LLMProfile) and value.name == name:
                return value
        raise ValueError(f"Unknown profile name: {name}")
