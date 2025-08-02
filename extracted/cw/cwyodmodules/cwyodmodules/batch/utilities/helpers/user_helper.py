from .postgres_db import PostgresDB
from mgmt_config import logger

class UserHelper:
    def __init__(self):
        self.db = PostgresDB()

    def get_users(self):
        """Get all unique users from conversations table."""
        try:
            query = "SELECT DISTINCT user_id FROM conversations ORDER BY user_id"
            result = self.db.execute_query(query, fetch="all")
            logger.info(f"Found {len(result) if result else 0} users in conversations table")
            return result
        except Exception as e:
            logger.error(f"Error getting users: {e}")
            return []

    def get_user_by_id(self, user_id: str):
        """Get specific user information."""
        try:
            query = "SELECT DISTINCT user_id FROM conversations WHERE user_id = %s"
            result = self.db.execute_query(query, (user_id,), fetch="one")
            return result
        except Exception as e:
            logger.error(f"Error getting user {user_id}: {e}")
            return None

    def get_users_with_conversation_count(self):
        """Get users with their conversation counts."""
        try:
            query = """
                SELECT user_id, COUNT(*) as conversation_count 
                FROM conversations 
                GROUP BY user_id 
                ORDER BY conversation_count DESC, user_id
            """
            result = self.db.execute_query(query, fetch="all")
            logger.info(f"Found {len(result) if result else 0} users with conversation counts")
            return result
        except Exception as e:
            logger.error(f"Error getting users with conversation counts: {e}")
            return [] 