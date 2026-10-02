from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any

import pytest
from langchain_core.language_models import BaseChatModel

from langchain_moonshot import ChatMoonshot
from tests.integration_tests._live_config import (
    DEFAULT_API_BASE,
    LIVE_MAX_RETRIES,
    LIVE_RATE_LIMITER,
)

if TYPE_CHECKING:
    from langchain_tests.integration_tests import (
        ChatModelIntegrationTests as _ChatModelIntegrationTests,
    )
else:
    _ChatModelIntegrationTests = pytest.importorskip(
        "langchain_tests.integration_tests"
    ).ChatModelIntegrationTests

pytestmark = pytest.mark.skipif(
    not (
        os.getenv("RUN_MOONSHOT_INTEGRATION") == "1"
        and os.getenv("MOONSHOT_API_KEY")
    ),
    reason=(
        "Set RUN_MOONSHOT_INTEGRATION=1 and MOONSHOT_API_KEY to run live "
        "Moonshot integration tests."
    ),
)


class TestChatMoonshotIntegrationStandard(_ChatModelIntegrationTests):
    @property
    def chat_model_class(self) -> type[BaseChatModel]:
        return ChatMoonshot

    @property
    def chat_model_params(self) -> dict[str, Any]:
        return {
            "model": "kimi-k2.5",
            "api_key": os.environ["MOONSHOT_API_KEY"],
            "base_url": os.getenv("MOONSHOT_API_BASE", DEFAULT_API_BASE),
            "thinking": False,
            "temperature": 0.6,
            "max_retries": LIVE_MAX_RETRIES,
            "rate_limiter": LIVE_RATE_LIMITER,
        }

    @property
    def has_tool_choice(self) -> bool:
        return False

    @property
    def supports_json_mode(self) -> bool:
        return True

    @property
    def supports_image_inputs(self) -> bool:
        return True

    @property
    def enable_vcr_tests(self) -> bool:
        return True

    @pytest.mark.xfail(
        condition=False,
        reason=(
            "Moonshot output_version='v1' can stream a natural-language preamble "
            "before tool-call chunks, so the final v1 content blocks do not "
            "consistently preserve the parsed tool-call payload."
        ),
    )
    @pytest.mark.parametrize("model", [{}, {"output_version": "v1"}], indirect=True)
    def test_tool_calling(self, model: BaseChatModel) -> None:
        if getattr(model, "output_version", None) == "v1":
            pytest.xfail(
                "Moonshot output_version='v1' does not reliably normalize streamed "
                "tool-call content blocks."
            )
        super().test_tool_calling(model)
