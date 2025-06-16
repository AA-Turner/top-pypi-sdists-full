from typing import List, Optional, Dict, Any
from pydantic import BaseModel  # Keep for nested models
from ragformance.generators.base_config import BaseGeneratorConfig


class LLMConfigItem(BaseModel):  # Stays as is
    name: str
    provider: str
    model: str
    api_key_env: str
    params: Dict[str, Any] = {}


class EmbeddingConfigItem(BaseModel):  # Stays as is
    name: str
    provider: str
    model: str
    api_key_env: str
    params: Dict[str, Any] = {}


class QuestionDistributionItem(BaseModel):  # Stays as is
    type: str
    ratio: float


class RagasGeneratorConfig(BaseGeneratorConfig):  # Inherits from BaseGeneratorConfig
    data_path: str  # Overrides base to make it mandatory, formerly data_path
    # output_path is inherited (mandatory str)
    # llm_api_key, llm_base_url, llm_model_name are inherited (Optional[str]) and can be ignored

    # Fields specific to RagasGeneratorConfig
    llm_config: LLMConfigItem
    embedding_config: EmbeddingConfigItem
    critique_llm_config: Optional[LLMConfigItem] = None
    n_questions: int = 10
    save_ragas_kg: bool = True
    question_distribution: Optional[List[QuestionDistributionItem]] = None

    @staticmethod
    def generate_example_config() -> dict:
        """Generates an example configuration dictionary."""
        return {
            "output_path": "/path/to/output/directory",  # Inherited, mandatory
            "data_path": "/path/to/your/input_data.json",  # Mandatory
            "llm_config": {
                "name": "generator_llm",
                "provider": "OpenAI",
                "model": "gpt-3.5-turbo",
                "api_key_env": "OPENAI_API_KEY",
                "params": {},
            },
            "embedding_config": {
                "name": "generator_embedding",
                "provider": "OpenAI",
                "model": "text-embedding-ada-002",
                "api_key_env": "OPENAI_API_KEY",
                "params": {},
            },
            "critique_llm_config": {
                "name": "critique_llm",
                "provider": "OpenAI",
                "model": "gpt-4",
                "api_key_env": "OPENAI_API_KEY",
                "params": {},
            },
            "n_questions": 10,  # Default value
            "save_ragas_kg": True,  # Default value
            "question_distribution": [
                {"type": "simple", "ratio": 0.4},
                {"type": "reasoning", "ratio": 0.3},
                {"type": "multi_context", "ratio": 0.3},
            ],
            # llm_api_key, llm_base_url, llm_model_name are omitted as RagasGenerator uses llm_config
        }
