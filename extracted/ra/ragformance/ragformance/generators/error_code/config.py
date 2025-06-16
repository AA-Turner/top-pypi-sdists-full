from typing import List  # Retain List from typing
from ragformance.generators.base_config import BaseGeneratorConfig


class ErrorCodeGeneratorConfig(BaseGeneratorConfig):
    data_path: str  # Overrides base to make it mandatory, formerly data_path
    llm_api_key: str  # Overrides base to make it mandatory
    llm_base_url: str  # Overrides base to make it mandatory
    llm_model_name: str  # Overrides base to make it mandatory
    # output_path is inherited (mandatory str)

    # Fields specific to ErrorCodeGeneratorConfig
    corpus_id_prefix: str
    document_title: str
    error_keywords: str = "error, information, or alarm codes (e.g., E09)"
    max_token_context: int = 64000
    question_tags: List[str] = []
    question_category: str = "error code"

    @staticmethod
    def generate_example_config() -> dict:
        """Generates an example configuration dictionary."""
        return {
            "output_path": "/path/to/output/directory",  # Inherited, mandatory
            "data_path": "/path/to/your/input_data.json",  # Mandatory
            "llm_api_key": "your_llm_api_key_here",  # Mandatory
            "llm_base_url": "your_llm_base_url_here",  # Mandatory
            "llm_model_name": "your_llm_model_name_here",  # Mandatory
            "corpus_id_prefix": "your_corpus_id_prefix",  # Mandatory
            "document_title": "Your Document Title",  # Mandatory
            "error_keywords": "error, information, or alarm codes (e.g., E09)",  # Default value
            "max_token_context": 64000,  # Default value
            "question_tags": [],  # Default value
            "question_category": "error code",  # Default value
        }
