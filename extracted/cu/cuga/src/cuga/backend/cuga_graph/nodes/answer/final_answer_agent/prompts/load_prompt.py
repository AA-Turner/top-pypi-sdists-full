from typing import List, Literal

from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field


class FinalAnswerOutput(BaseModel):
    thoughts: List[str] = Field(..., description="Your thoughts that leads to final answer")

    final_answer: str = Field(..., description="Final answer")


class FinalAnswerAppworldOutput(BaseModel):
    """
    Represents the output structure for the AI assistant's response.
    """

    thoughts: List[str] = Field(
        ...,
        description="A list of strings, where each string is a distinct point in the reasoning process for arriving at the final_answer.",
    )
    final_answer: str = Field(
        ...,
        description="The determined output value based on the user intent and system answer. Can be an empty string, a specific extracted value, or the original system answer.",
    )
    final_answer_type: Literal['str', 'int', 'float'] = Field(
        ..., description="The Python data type of the final_answer. Must be 'str', 'int', or 'float'."
    )


parser = PydanticOutputParser(pydantic_object=FinalAnswerOutput)
