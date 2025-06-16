from typing import Optional  # Keep for other fields
from ragformance.generators.base_config import BaseGeneratorConfig


class LLMPromptGeneratorConfig(BaseGeneratorConfig):
    data_path: str  # Overrides base to make it mandatory, formerly data_path
    llm_api_key: str  # Overrides base to make it mandatory
    llm_base_url: str  # Overrides base to make it mandatory
    llm_model_name: str  # Overrides base to make it mandatory
    # output_path is inherited (mandatory str)

    # Fields specific to LLMPromptGeneratorConfig
    query_gen_prompt_template: Optional[str] = None
    answer_gen_prompt_template: Optional[str] = None
    max_questions_per_doc: int = 5
    process_pdfs: bool = True
    process_markdown: bool = True

    @staticmethod
    def generate_example_config() -> dict:
        """Generates an example configuration dictionary."""
        return {
            "output_path": "/path/to/output/directory",  # Inherited, mandatory
            "data_path": "/path/to/your/input_data",  # Mandatory
            "llm_api_key": "your_llm_api_key_here",  # Mandatory
            "llm_base_url": "your_llm_base_url_here",  # Mandatory
            "llm_model_name": "your_llm_model_name_here",  # Mandatory
            "query_gen_prompt_template": "Generate questions for the following text: {text}",  # Optional, example
            "answer_gen_prompt_template": "Answer the following question based on the text: {question} {text}",  # Optional, example
            "max_questions_per_doc": 5,  # Default value
            "process_pdfs": True,  # Default value
            "process_markdown": True,  # Default value
        }
