from typing import Optional  # Keep for llm_prompt_template
from ragformance.generators.base_config import BaseGeneratorConfig


class MicGeneratorConfig(BaseGeneratorConfig):
    data_path: str  # Overrides base to make it mandatory, formerly data_path
    llm_model_name: str  # Overrides base to make it mandatory
    # output_path is inherited (mandatory str)
    # llm_api_key is inherited (Optional[str])
    # llm_base_url is inherited (Optional[str])

    # Fields specific to MicGeneratorConfig
    llm_prompt_template: Optional[str] = None
    llm_batch_size: int = 16
    num_queries_to_generate: int = 20

    @staticmethod
    def generate_example_config() -> dict:
        """Generates an example configuration dictionary."""
        return {
            "output_path": "/path/to/output/directory",  # Inherited, mandatory
            "data_path": "/path/to/your/input_data.json",  # Mandatory
            "llm_model_name": "your_llm_model_name_here",  # Mandatory
            "llm_api_key": "your_llm_api_key_here_if_needed",  # Optional
            "llm_base_url": "your_llm_base_url_here_if_needed",  # Optional
            "llm_prompt_template": "Generate queries based on the following text: {text}",  # Optional, example
            "llm_batch_size": 16,  # Default value
            "num_queries_to_generate": 20,  # Default value
        }
