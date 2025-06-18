from typing_extensions import Literal, Required, TypedDict, Union
from openai.types.chat.completion_create_params import ResponseFormat as OpenAIResponseFormat


class ResponseFormatGrammar(TypedDict, total=False):
    type: Required[Literal["grammar"]]
    """The type of response format being defined. Always `text`."""

    grammar: str
    """See https://fireworks.ai/docs/structured-responses/structured-output-grammar-based"""


ResponseFormat = Union[OpenAIResponseFormat, ResponseFormatGrammar]
