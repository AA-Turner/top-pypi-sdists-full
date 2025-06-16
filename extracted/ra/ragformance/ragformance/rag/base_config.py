from pydantic import BaseModel
from typing import Dict

class BaseRagConfig(BaseModel):
    """
    Base configuration for RAG models.
    """
    BATCH_SIZE: int = 32
    SIMILARITY_THRESHOLD: float = 0.5

    @staticmethod
    def generate_example_config() -> Dict:
        """
        Generates an example configuration dictionary.
        """
        return {
            "BATCH_SIZE": 32,
            "SIMILARITY_THRESHOLD": 0.5,
        }
