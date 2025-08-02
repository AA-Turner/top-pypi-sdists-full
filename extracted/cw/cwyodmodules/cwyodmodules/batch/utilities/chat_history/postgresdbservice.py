import psycopg
import json
from psycopg.rows import dict_row
from datetime import datetime, timezone
from .database_client_base import DatabaseClientBase
from ...utilities.helpers.env_helper import EnvHelper
from mgmt_config import logger, identity
env_helper: EnvHelper = EnvHelper()
log_execution = env_helper.LOG_EXECUTION
log_args = env_helper.LOG_ARGS
log_result = env_helper.LOG_RESULT


class PostgresConversationClient(DatabaseClientBase):

    def __init__(
        self, user: str, host: str, database: str, enable_message_feedback: bool = False
    ):
        self.user = user
        self.host = host
        self.database = database
        self.enable_message_feedback = enable_message_feedback
        self.conn = None

    @logger.trace_function(log_execution=log_execution, log_args=log_args, log_result=log_result)
    def connect(self):
        try:
            access_information = identity.get_token(scopes="https://ossrdbms-aad.database.windows.net/.default")
            token = access_information.token
            self.conn = psycopg.connect(
                user=self.user,
                host=self.host,
                dbname=self.database,
                password=token,
                port=5432,
                sslmode="require",
                row_factory=dict_row
            )
            logger.info("Successfully connected to PostgreSQL")
        except Exception as e:
            logger.error("Failed to connect to PostgreSQL: %s", e, exc_info=True)
            raise

    @logger.trace_function(log_execution=log_execution, log_args=log_args, log_result=log_result)
    def close(self):
        if self.conn:
            self.conn.close()
            logger.info("PostgreSQL connection closed")

    @logger.trace_function(log_execution=log_execution, log_args=log_args, log_result=log_result)
    def ensure(self):
        if not self.conn:
            logger.warning("PostgreSQL client not initialized correctly")
            return False, "PostgreSQL client not initialized correctly"
        logger.info("PostgreSQL client initialized successfully")
        return True, "PostgreSQL client initialized successfully"

    @logger.trace_function(log_execution=log_execution, log_args=log_args, log_result=log_result)
    def create_conversation(self, conversation_id, user_id, title=""):
        utc_now = datetime.now(timezone.utc)
        createdAt = utc_now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        query = """
            INSERT INTO conversations (id, conversation_id, type, "createdAt", "updatedAt", user_id, title)
            VALUES (%s, %s, 'conversation', %s, %s, %s, %s)
            RETURNING *
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    query, (conversation_id, conversation_id, createdAt, createdAt, user_id, title)
                )
                conversation = cur.fetchone()
                self.conn.commit()
            if conversation:
                logger.info(f"Conversation created with id: {conversation_id}")
                return conversation
            else:
                logger.warning(
                    f"Failed to create conversation with id: {conversation_id}"
                )
                return False
        except Exception as e:
            logger.error(
                f"Error creating conversation with id: {conversation_id}: {e}",
                exc_info=True,
            )
            self.conn.rollback()
            raise

    @logger.trace_function(log_execution=log_execution, log_args=log_args, log_result=log_result)
    def upsert_conversation(self, conversation):
        query = """
            INSERT INTO conversations (id, conversation_id, type, "createdAt", "updatedAt", user_id, title)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO UPDATE SET
                "updatedAt" = EXCLUDED."updatedAt",
                title = EXCLUDED.title
            RETURNING *
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    query,
                    (
                        conversation["id"],
                        conversation["conversation_id"],
                        conversation["type"],
                        conversation["createdAt"],
                        conversation["updatedAt"],
                        conversation["user_id"],
                        conversation["title"],
                    ),
                )
                updated_conversation = cur.fetchone()
                self.conn.commit()
            if updated_conversation:
                logger.info(f"Conversation upserted with id: {conversation['id']}")
                return updated_conversation
            else:
                logger.warning(
                    f"Failed to upsert conversation with id: {conversation['id']}"
                )
                return False
        except Exception as e:
            logger.error(
                f"Error upserting conversation with id: {conversation['id']}: {e}",
                exc_info=True,
            )
            self.conn.rollback()
            raise

    @logger.trace_function(log_execution=log_execution, log_args=log_args, log_result=log_result)
    def delete_conversation(self, user_id, conversation_id):
        query = "DELETE FROM conversations WHERE conversation_id = %s AND user_id = %s"
        try:
            with self.conn.cursor() as cur:
                cur.execute(query, (conversation_id, user_id))
                self.conn.commit()
            logger.info(
                f"Conversation deleted with conversation_id: {conversation_id} and user_id: {user_id}"
            )
            return True
        except Exception as e:
            logger.error(
                f"Error deleting conversation with conversation_id: {conversation_id} and user_id: {user_id}: {e}",
                exc_info=True,
            )
            self.conn.rollback()
            raise

    @logger.trace_function(log_execution=log_execution, log_args=log_args, log_result=log_result)
    def delete_messages(self, conversation_id, user_id):
        query = "DELETE FROM messages WHERE conversation_id = %s AND user_id = %s RETURNING *"
        try:
            with self.conn.cursor() as cur:
                cur.execute(query, (conversation_id, user_id))
                messages = cur.fetchall()
                self.conn.commit()
            logger.info(
                f"Messages deleted for conversation_id: {conversation_id} and user_id: {user_id}"
            )
            return messages
        except Exception as e:
            logger.error(
                f"Error deleting messages for conversation_id: {conversation_id} and user_id: {user_id}: {e}",
                exc_info=True,
            )
            self.conn.rollback()
            raise

    @logger.trace_function(log_execution=log_execution, log_args=log_args, log_result=log_result)
    def get_conversations(self, user_id, limit=None, sort_order="DESC", offset=0):
        try:
            offset = int(offset)  # Ensure offset is an integer
        except ValueError:
            logger.error("Offset must be an integer.", exc_info=True)
            raise ValueError("Offset must be an integer.")
        
        params = [user_id]
        
        # Base query without LIMIT and OFFSET
        query = f"""
            SELECT * FROM conversations
            WHERE user_id = %s AND type = 'conversation'
            ORDER BY "updatedAt" {sort_order}
        """
        
        # Append LIMIT and OFFSET to the query if limit is specified
        if limit is not None:
            try:
                limit = int(limit)  # Ensure limit is an integer
                query += " LIMIT %s OFFSET %s"
                params.extend([limit, offset])
                # Fetch records with LIMIT and OFFSET
                with self.conn.cursor() as cur:
                    cur.execute(query, tuple(params))
                    conversations = cur.fetchall()
                logger.info(
                    f"Retrieved conversations for user_id: {user_id} with limit: {limit} and offset: {offset}"
                )
            except ValueError:
                logger.error("Limit must be an integer.", exc_info=True)
                raise ValueError("Limit must be an integer.")
        else:
            # Fetch records without LIMIT and OFFSET
            with self.conn.cursor() as cur:
                cur.execute(query, tuple(params))
                conversations = cur.fetchall()
            logger.info(
                f"Retrieved conversations for user_id: {user_id}"
            )
        
        return conversations

    @logger.trace_function(log_execution=log_execution, log_args=log_args, log_result=log_result)
    def get_conversation(self, user_id, conversation_id):
        query = "SELECT * FROM conversations WHERE conversation_id = %s AND user_id = %s"
        try:
            with self.conn.cursor() as cur:
                cur.execute(query, (conversation_id, user_id))
                conversation = cur.fetchone()
            if conversation:
                logger.info(
                    f"Retrieved conversation with conversation_id: {conversation_id} and user_id: {user_id}"
                )
            else:
                logger.warning(
                    f"Conversation not found with conversation_id: {conversation_id} and user_id: {user_id}"
                )
            return conversation
        except Exception as e:
            logger.error(
                f"Error retrieving conversation with conversation_id: {conversation_id} and user_id: {user_id}: {e}",
                exc_info=True,
            )
            raise

    @logger.trace_function(log_execution=log_execution, log_args=log_args, log_result=log_result)
    def create_message(self, uuid, conversation_id, user_id, input_message: dict):
        utc_now = datetime.now(timezone.utc)
        createdAt = utc_now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        query = """
            INSERT INTO messages (id, type, "createdAt", "updatedAt", user_id, conversation_id, role, content)
            VALUES (%s, 'message', %s, %s, %s, %s, %s, %s)
            RETURNING *
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    query,
                    (
                        uuid,
                        createdAt,
                        createdAt,
                        user_id,
                        conversation_id,
                        input_message["role"],
                        input_message["content"],
                    ),
                )
                message = cur.fetchone()
                self.conn.commit()
            if message:
                logger.info(
                    f"Message created with id: {uuid} for conversation_id: {conversation_id}"
                )
            else:
                logger.warning(
                    f"Failed to create message with id: {uuid} for conversation_id: {conversation_id}"
                )
            return message
        except Exception as e:
            logger.error(
                f"Error creating message with id: {uuid} for conversation_id: {conversation_id}: {e}",
                exc_info=True,
            )
            self.conn.rollback()
            raise

    @logger.trace_function(log_execution=log_execution, log_args=log_args, log_result=log_result)
    def update_message_feedback(self, user_id, message_id, feedback):
        query = "UPDATE messages SET feedback = %s WHERE id = %s AND user_id = %s RETURNING *"
        try:
            with self.conn.cursor() as cur:
                cur.execute(query, (feedback, message_id, user_id))
                message = cur.fetchone()
                self.conn.commit()
            if message:
                logger.info(
                    f"Message feedback updated for message_id: {message_id} and user_id: {user_id}"
                )
            else:
                logger.warning(
                    f"Failed to update message feedback for message_id: {message_id} and user_id: {user_id}"
                )
            return message
        except Exception as e:
            logger.error(
                f"Error updating message feedback for message_id: {message_id} and user_id: {user_id}: {e}",
                exc_info=True,
            )
            self.conn.rollback()
            raise

    @logger.trace_function(log_execution=log_execution, log_args=log_args, log_result=log_result)
    def get_messages(self, user_id, conversation_id):
        query = "SELECT * FROM messages WHERE conversation_id = %s AND user_id = %s ORDER BY \"createdAt\""
        try:
            with self.conn.cursor() as cur:
                cur.execute(query, (conversation_id, user_id))
                messages = cur.fetchall()
            logger.info(
                f"Retrieved {len(messages)} messages for conversation_id: {conversation_id} and user_id: {user_id}"
            )
            return messages
        except Exception as e:
            logger.error(
                f"Error retrieving messages for conversation_id: {conversation_id} and user_id: {user_id}: {e}",
                exc_info=True,
            )
            raise
