from ..env_helper import EnvHelper
from .postgres_embedder import PostgresEmbedder
from mgmt_config import storage_accounts
storage_account = storage_accounts.get("main") if storage_accounts else None

class EmbedderFactory:
    @staticmethod
    def create(env_helper: EnvHelper):
        """
        Creates and returns a PostgreSQL embedder instance.
        
        Args:
            env_helper (EnvHelper): Environment helper instance
            
        Returns:
            PostgresEmbedder: PostgreSQL embedder instance
        """
        return PostgresEmbedder(storage_account, env_helper)
