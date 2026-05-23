import json
from typing import Any
from unittest.mock import patch

import pytest

pytest.importorskip(
    "langchain_community.chat_models.ollama",
    reason=(
        "`langchain_community.chat_models.ollama` was removed in "
        "`langchain-community>=0.4.2`; `OllamaFunctions` is unusable without it."
    ),
)

from langchain_core.prompts import ChatPromptTemplate  # noqa: E402
from pydantic import BaseModel  # noqa: E402

from langchain_experimental.llms.ollama_functions import OllamaFunctions  # noqa: E402


class Schema(BaseModel):
    pass


@patch.object(OllamaFunctions, "_create_stream")
def test_convert_image_prompt(
    _create_stream_mock: Any,
) -> None:
    response = {"message": {"content": '{"tool": "Schema", "tool_input": {}}'}}
    _create_stream_mock.return_value = [json.dumps(response)]

    prompt = ChatPromptTemplate.from_messages(
        [("human", [{"image_url": "data:image/jpeg;base64,{image_url}"}])]
    )

    lmm = prompt | OllamaFunctions().with_structured_output(schema=Schema)

    schema_instance = lmm.invoke(dict(image_url=""))

    assert schema_instance is not None
