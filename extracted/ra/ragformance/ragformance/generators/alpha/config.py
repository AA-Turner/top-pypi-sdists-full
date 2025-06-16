from ragformance.generators.base_config import BaseGeneratorConfig


class AlphaGeneratorConfig(BaseGeneratorConfig):
    data_path: str  # Overrides base to make it mandatory, formerly data_path
    llm_api_key: str  # Overrides base to make it mandatory
    llm_base_url: str  # Overrides base to make it mandatory
    llm_model_name: str  # Overrides base to make it mandatory
    # output_path is inherited from BaseGeneratorConfig as 'str'

    # Fields specific to AlphaGeneratorConfig
    temporary_folder: str = "converted_data"

    @staticmethod
    def generate_example_config() -> dict:
        """Generates an example configuration dictionary."""
        return {
            "output_path": "/path/to/output/directory",  # Inherited, assuming it's a path
            "data_path": "/path/to/your/input_data.json",  # Mandatory
            "llm_api_key": "your_llm_api_key_here",  # Mandatory
            "llm_base_url": "your_llm_base_url_here",  # Mandatory
            "llm_model_name": "your_llm_model_name_here",  # Mandatory
            "temporary_folder": "converted_data",  # Default value
        }
