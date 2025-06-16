from typing import Optional
from pydantic import BaseModel


class BaseGeneratorConfig(BaseModel):
    output_path: str
    data_path: Optional[str] = None
    llm_api_key: Optional[str] = None
    llm_base_url: Optional[str] = None
    llm_model_name: Optional[str] = None

    class Config:
        extra = "allow"
