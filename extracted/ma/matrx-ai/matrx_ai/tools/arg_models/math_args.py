from pydantic import BaseModel


class CalculateArgs(BaseModel):
    expression: str
