from pydantic import BaseModel
from typing import Optional, Dict
from ragformance.rag.base_config import BaseRagConfig

class NaiveRagConfig(BaseRagConfig):
    """
    Configuration for Naive RAG model.
    """
    LLM_ENDPOINT: Optional[str] = "https://localhost:8000/v1/chat/completions"
    LLM_KEY: Optional[str] = None
    LLM_MODEL: Optional[str] = None
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    @staticmethod
    def generate_example_config() -> Dict:
        """
        Generates an example configuration dictionary.
        """
        config = BaseRagConfig.generate_example_config()
        config.update({
            "LLM_ENDPOINT": "https://localhost:8000/v1/chat/completions",
            "LLM_KEY": "your_llm_key_here",
            "LLM_MODEL": "your_llm_model_here",
            "EMBEDDING_MODEL": "all-MiniLM-L6-v2",
        })
        return config


class MultiEmbeddingLLMRagConfig(BaseRagConfig):
    """
    Configuration for MultiEmbeddingLLM RAG model.
    """
    EMBEDDING_MODELS: Dict[str, str] = {
        "bge-small": "BAAI/bge-small-en-v1.5",
        "e5-small": "intfloat/e5-small-v2"
    }
    LLMS: Dict[str, str] = {
        "llama3-70b": "llama3-70b-8192",
        "gemma-9b": "gemma2-9b-it"
    }
    GROQ_API_KEY: Optional[str] = None
    CORPUS_TEXT_KEY: str = "text"
    QUERIES_TEXT_KEY: str = "query_text"
    SIMILARITY_TOP_K: int = 1 # This seems to be a duplicate of SIMILARITY_THRESHOLD in BaseRagConfig. Keeping it for now as it's in the multi_rag_configuration.json

    @staticmethod
    def generate_example_config() -> Dict:
        """
        Generates an example configuration dictionary.
        """
        config = BaseRagConfig.generate_example_config()
        config.update({
            "EMBEDDING_MODELS": {
                "bge-small": "BAAI/bge-small-en-v1.5",
                "e5-small": "intfloat/e5-small-v2"
            },
            "LLMS": {
                "llama3-70b": "llama3-70b-8192",
                "gemma-9b": "gemma2-9b-it"
            },
            "GROQ_API_KEY": "your_groq_api_key_here",
            "CORPUS_TEXT_KEY": "text",
            "QUERIES_TEXT_KEY": "query_text",
            "SIMILARITY_TOP_K": 1,
        })
        return config

class OpenWebUIRagConfig(BaseRagConfig):
    """
    Configuration for OpenWebUI RAG model.
    """
    LLM_NAME: Optional[str] = None
    COLLECTION_NAME: str = "not_referenced"
    CLIENT_EMAIL: str = "admin@example.com"
    CLIENT_MDP: str = "admin" # Consider security implications for storing passwords in config
    OPENWEBUI_URL: str = "http://localhost:3000"
    OLLAMA_URL: str = "http://localhost:11434"
    COLLECTION_ID: Optional[str] = None # This is populated during runtime

    @staticmethod
    def generate_example_config() -> Dict:
        """
        Generates an example configuration dictionary.
        """
        config = BaseRagConfig.generate_example_config()
        config.update({
            "LLM_NAME": "your_llm_name_here",
            "COLLECTION_NAME": "my_collection",
            "CLIENT_EMAIL": "admin@example.com",
            "CLIENT_MDP": "admin_password",
            "OPENWEBUI_URL": "http://localhost:3000",
            "OLLAMA_URL": "http://localhost:11434",
            "COLLECTION_ID": None,
        })
        return config

class HaystackRagConfig(BaseRagConfig):
    """
    Configuration for Haystack RAG model.
    """
    EMBEDDING_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"
    OLLAMA_MODEL: Optional[str] = None
    OLLAMA_URL: Optional[str] = None
    # Add other Haystack-specific configurations here if needed

    @staticmethod
    def generate_example_config() -> Dict:
        """
        Generates an example configuration dictionary.
        """
        config = BaseRagConfig.generate_example_config()
        config.update({
            "EMBEDDING_MODEL_NAME": "sentence-transformers/all-MiniLM-L6-v2",
            "OLLAMA_MODEL": "your_ollama_model_here",
            "OLLAMA_URL": "your_ollama_url_here",
            # Add other Haystack-specific example configurations here
        })
        return config
