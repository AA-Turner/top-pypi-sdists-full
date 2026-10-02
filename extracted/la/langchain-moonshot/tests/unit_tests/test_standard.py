from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

import pytest
from langchain_core.language_models import BaseChatModel

from langchain_moonshot import ChatMoonshot

if TYPE_CHECKING:
    from langchain_tests.unit_tests import ChatModelUnitTests as _ChatModelUnitTests
else:
    _ChatModelUnitTests = pytest.importorskip(
        "langchain_tests.unit_tests"
    ).ChatModelUnitTests


class TestChatMoonshotStandard(_ChatModelUnitTests):
    @property
    def chat_model_class(self) -> type[BaseChatModel]:
        return ChatMoonshot

    @property
    def chat_model_params(self) -> dict[str, Any]:
        return {
            "model": "kimi-k2.5",
            "api_key": "test-key",
            "base_url": "https://example.com/v1",
            "thinking": False,
            "temperature": 0.6,
        }

    @property
    def has_tool_calling(self) -> bool:
        return True

    @property
    def has_tool_choice(self) -> bool:
        return False

    @property
    def has_structured_output(self) -> bool:
        return True

    @property
    def supports_json_mode(self) -> bool:
        return True

    @property
    def supports_image_inputs(self) -> bool:
        return True

    @property
    def supports_video_inputs(self) -> bool:
        return False

    @property
    def returns_usage_metadata(self) -> bool:
        return True

    @property
    def supports_anthropic_inputs(self) -> bool:
        return False

    @property
    def supports_image_tool_message(self) -> bool:
        return False

    @property
    def supported_usage_metadata_details(
        self,
    ) -> dict[
        Literal["invoke", "stream"],
        list[
            Literal[
                "audio_input",
                "audio_output",
                "reasoning_output",
                "cache_read_input",
                "cache_creation_input",
            ]
        ],
    ]:
        return {"invoke": [], "stream": []}

    @property
    def init_from_env_params(
        self,
    ) -> tuple[dict[str, str], dict[str, object], dict[str, str]]:
        return (
            {
                "MOONSHOT_API_KEY": "env-key",
                "MOONSHOT_API_BASE": "https://example.com/v1",
            },
            {"model": "kimi-k2.5", "thinking": False, "temperature": 0.6},
            {"api_key": "env-key", "api_base": "https://example.com/v1"},
        )
