from functools import cached_property
from typing import Optional

from pydantic import BaseModel, Field, model_validator


class Payload(BaseModel):
    input: Optional[str] = Field(default=None, description="Input text to be processed.")
    output: Optional[str] = Field(default=None, description="Output text to be processed.")

    @model_validator(mode="after")
    def ensure_input_or_output(self) -> "Payload":
        if not self.input and not self.output:
            raise ValueError("Either input or output must be set.")
        return self

    @cached_property
    def text(self) -> str:
        if self.output:
            return self.output
        elif self.input:
            return self.input
        else:
            raise ValueError("Either input or output must be set.")
