# database_factory.py - Simplified PostgreSQL-only version
from ..helpers.env_helper import EnvHelper
from .postgresdbservice import PostgresConversationClient

class DatabaseFactory:
    @staticmethod
    def get_conversation_client():
        env_helper: EnvHelper = EnvHelper()
        
        # Validate required PostgreSQL environment variables
        required_vars = ["POSTGRESQL_USER", "POSTGRESQL_HOST", "POSTGRESQL_DATABASE"]
        for var in required_vars:
            if not getattr(env_helper, var, None):
                raise ValueError(f"Environment variable {var} is required.")

        return PostgresConversationClient(
            user=env_helper.POSTGRESQL_USER,
            host=env_helper.POSTGRESQL_HOST,
            database=env_helper.POSTGRESQL_DATABASE,
        )
