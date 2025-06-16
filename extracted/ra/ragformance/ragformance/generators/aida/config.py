from ragformance.generators.base_config import BaseGeneratorConfig


class AidaGeneratorConfig(BaseGeneratorConfig):
    data_path: str  # Overrides base to make it mandatory, formerly seed_questions_path
    llm_api_key: str  # Overrides base to make it mandatory
    llm_base_url: str  # Overrides base to make it mandatory
    # output_path is inherited from BaseGeneratorConfig as 'str'
    # llm_model_name is inherited from BaseGeneratorConfig as 'Optional[str]'

    # Fields specific to AidaGeneratorConfig
    data_dir: str
    hf_embed_model: str
    capella_xml_path: str
    entity_model_name: str
    qa_model_name: str
    chunk_size: int = 750
    chunk_overlap: int = 100
    persist_dir: str = "chroma_index"
    k_pdf: int = 5
    k_capella: int = 8

    @staticmethod
    def generate_example_config() -> dict:
        """Generates an example configuration dictionary."""
        return {
            "output_path": "/path/to/output/directory",  # Inherited, assuming it's a path
            "data_path": "/path/to/your/seed_questions.json",  # Mandatory
            "llm_api_key": "your_llm_api_key_here",  # Mandatory
            "llm_base_url": "your_llm_base_url_here",  # Mandatory
            "llm_model_name": "gpt-3.5-turbo",  # Optional, example value
            "data_dir": "/path/to/your/data_directory",  # Mandatory
            "hf_embed_model": "sentence-transformers/all-MiniLM-L6-v2",  # Mandatory, example value
            "capella_xml_path": "/path/to/your/capella.xml",  # Mandatory
            "entity_model_name": "your_entity_model_name_here",  # Mandatory
            "qa_model_name": "your_qa_model_name_here",  # Mandatory
            "chunk_size": 750,  # Default value
            "chunk_overlap": 100,  # Default value
            "persist_dir": "chroma_index",  # Default value
            "k_pdf": 5,  # Default value
            "k_capella": 8,  # Default value
        }
