from typing import List, Optional
from ragformance.generators.base_config import BaseGeneratorConfig


class BasedLLMSummaryGeneratorConfig(BaseGeneratorConfig):
    data_path: str  # Overrides base to make it mandatory, formerly data_source_path
    llm_api_key: str  # Overrides base to make it mandatory
    # output_path is inherited (mandatory str)
    # llm_base_url is inherited (Optional[str])
    # llm_model_name is inherited (Optional[str])

    # Fields specific to BasedLLMSummaryGeneratorConfig
    include_extensions: List[str] = [".md"]
    llm_summary_model_name: str
    llm_qa_model_name: str
    use_proxy: bool = False
    proxy_url: Optional[str] = None
    no_proxy_list: Optional[str] = None
    ca_bundle_path: Optional[str] = None

    @staticmethod
    def generate_example_config() -> dict:
        """Generates an example configuration dictionary."""
        return {
            "output_path": "/path/to/output/directory",  # Inherited, mandatory
            "data_path": "/path/to/your/data_source",  # Mandatory
            "llm_api_key": "your_llm_api_key_here",  # Mandatory
            "llm_base_url": "your_llm_base_url_here_if_needed",  # Optional
            "llm_model_name": "default_llm_model_for_generation",  # Optional
            "include_extensions": [".md"],  # Default value
            "llm_summary_model_name": "your_summary_model_name_here",  # Mandatory
            "llm_qa_model_name": "your_qa_model_name_here",  # Mandatory
            "use_proxy": False,  # Default value
            "proxy_url": "http://your_proxy_url_here:port",  # Optional
            "no_proxy_list": "localhost,127.0.0.1",  # Optional
            "ca_bundle_path": "/path/to/your/ca_bundle.pem",  # Optional
        }
