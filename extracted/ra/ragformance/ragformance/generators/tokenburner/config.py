from typing import List
from pydantic import BaseModel

class TokenBurnerGeneratorConfig(BaseModel):
    pdf_path: str
    categories_file_path: str
    user_queries: List[str]
    output_path: str
    llm_model_name: str
    llm_api_key: str
    llm_base_url: str

    @staticmethod
    def generate_example_config() -> dict:
        """Generates an example configuration dictionary."""
        return {
            "pdf_path": "/path/to/your/document.pdf",
            "categories_file_path": "/path/to/your/categories.json",
            "user_queries": ["What is the main topic?", "Summarize section 3."],
            "output_path": "/path/to/output_folder",
            "llm_model_name": "your_llm_model_name",
            "llm_api_key": "your_llm_api_key",
            "llm_base_url": "your_llm_base_url"
        }
