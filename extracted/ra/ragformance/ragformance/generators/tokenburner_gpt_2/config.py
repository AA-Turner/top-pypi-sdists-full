from typing import Optional
from pydantic import BaseModel

class TokenBurnerGPT2GeneratorConfig(BaseModel):
    pdf_path: str
    output_path: str
    model_path: Optional[str] = None
    max_pages: Optional[int] = None
    llm_api_key: str
    llm_base_url: str
    llm_model_name: str

    @staticmethod
    def generate_example_config() -> dict:
        """Generates an example configuration dictionary."""
        return {
            "pdf_path": "/path/to/your/document.pdf",
            "output_path": "/path/to/output_folder",
            "model_path": None,  # Optional, example value
            "max_pages": 100,  # Optional, example value
            "llm_api_key": "your_llm_api_key",
            "llm_base_url": "your_llm_base_url",
            "llm_model_name": "your_llm_model_name"
        }
