from typing import Literal
from pydantic import BaseModel


class NonRefusal(BaseModel):
    classification: Literal["Non-refusal", "Refusal"]
