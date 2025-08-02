import psycopg2
from psycopg2.extras import execute_values, RealDictCursor
from mgmt_config import identity
from .llm_helper import LLMHelper
from ...utilities.helpers.env_helper import EnvHelper

from mgmt_config import logger
env_helper: EnvHelper = EnvHelper()
log_execution = env_helper.LOG_EXECUTION
log_args = env_helper.LOG_ARGS
log_result = env_helper.LOG_RESULT


class AzurePostgresHelper:
    def __init__(self):
        self.llm_helper = LLMHelper()
        self.env_helper = EnvHelper()

    @logger.trace_function(log_execution=log_execution, log_args=log_args, log_result=False)
    def _create_search_client(self):
        """
        Creates a new connection to Azure PostgreSQL using AAD authentication.
        """
        try:
            user = self.env_helper.POSTGRESQL_USER
            host = self.env_helper.POSTGRESQL_HOST
            dbname = self.env_helper.POSTGRESQL_DATABASE

            # Acquire the access token
            access_information = identity.get_token(
                scopes="https://ossrdbms-aad.database.windows.net/.default"
            )
            token = access_information.token
            # Use the token in the connection string
            conn_string = f"host={host} user={user} dbname={dbname} password={token}"
            keepalive_kwargs = {
                "keepalives": 1,
                "keepalives_idle": 30,
                "keepalives_interval": 5,
                "keepalives_count": 5,
            }
            conn = psycopg2.connect(conn_string, **keepalive_kwargs)
            logger.info("Connected to Azure PostgreSQL successfully.")
            return conn
        except Exception as e:
            logger.error(f"Error establishing a connection to PostgreSQL: {e}")
            raise

    @logger.trace_function(log_execution=log_execution, log_args=log_args, log_result=False)
    def get_search_client(self):
        """
        Creates a new database connection for each operation.
        """
        return self._create_search_client()

    @logger.trace_function(log_execution=log_execution, log_args=False, log_result=False)
    def get_vector_store(self, embedding_array):
        """
        Fetches search indexes from PostgreSQL based on an embedding vector.
        """
        conn = self.get_search_client()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """
                    SELECT id, title, chunk, "offset", page_number, content, source
                    FROM vector_store
                    ORDER BY content_vector <=> %s::vector
                    LIMIT %s
                    """,
                    (
                        embedding_array,
                        self.env_helper.AZURE_POSTGRES_SEARCH_TOP_K,
                    ),
                )
                search_results = cur.fetchall()
                logger.info(f"Retrieved {len(search_results)} search results.")
                return search_results
        except Exception as e:
            logger.error(f"Error executing search query: {e}")
            raise
        finally:
            # Only close connection if it exists and is open
            if conn and conn.closed == 0:
                conn.close()

    @logger.trace_function(log_execution=log_execution, log_args=False, log_result=log_result)
    def create_vector_store(self, documents_to_upload):
        """
        Inserts documents into the `vector_store` table in batch mode.
        """
        conn = self.get_search_client()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                data_to_insert = [
                    (
                        d["id"],
                        d["title"],
                        d["chunk"],
                        d["chunk_id"],
                        d["offset"],
                        d["page_number"],
                        d["content"],
                        d["source"],
                        d["metadata"],
                        d["content_vector"],
                    )
                    for d in documents_to_upload
                ]

                # Batch insert using execute_values for efficiency
                query = """
                    INSERT INTO vector_store (
                        id, title, chunk, chunk_id, "offset", page_number,
                        content, source, metadata, content_vector
                    ) VALUES %s
                """
                batch_size = 100  # Insert in smaller batches to avoid connection resets
                for start_idx in range(0, len(data_to_insert), batch_size):
                    batch = data_to_insert[start_idx : start_idx + batch_size]
                    execute_values(cur, query, batch, page_size=batch_size)
                logger.info(
                    f"Inserted {len(documents_to_upload)} documents successfully."
                )

            conn.commit()  # Commit the transaction
        except Exception as e:
            logger.error(f"Error during index creation: {e}")
            # Only attempt rollback if connection is still open
            if conn and conn.closed == 0:
                try:
                    conn.rollback()
                except Exception as rollback_error:
                    logger.warning(f"Failed to rollback transaction: {rollback_error}")
            raise
        finally:
            # Only close connection if it exists and is open
            if conn and conn.closed == 0:
                conn.close()

    @logger.trace_function(log_execution=log_execution, log_args=False, log_result=log_result)
    def get_files(self):
        """
        Fetches distinct titles from the PostgreSQL database.

        Returns:
            list[dict] or None: A list of dictionaries (each with a single key 'title')
            or None if no titles are found or an error occurs.
        """
        conn = self.get_search_client()
        try:
            # Using a cursor to execute the query
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                    SELECT id, title
                    FROM vector_store
                    WHERE title IS NOT NULL
                    ORDER BY title;
                """
                cursor.execute(query)
                # Fetch all results
                results = cursor.fetchall()
                # Return results or None if empty
                return results if results else None
        except psycopg2.Error as db_err:
            logger.error(f"Database error while fetching titles: {db_err}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error while fetching titles: {e}")
            raise
        finally:
            # Only close connection if it exists and is open
            if conn and conn.closed == 0:
                conn.close()

    @logger.trace_function(log_execution=log_execution, log_args=log_args, log_result=log_result)
    def delete_documents(self, ids_to_delete):
        """
        Deletes documents from the PostgreSQL database based on the provided ids.

        Args:
            ids_to_delete (list): A list of document IDs to delete.

        Returns:
            int: The number of deleted rows.
        """
        conn = self.get_search_client()
        try:
            if not ids_to_delete:
                logger.warning("No IDs provided for deletion.")
                return 0

            # Using a cursor to execute the query
            with conn.cursor() as cursor:
                # Construct the DELETE query with the list of ids_to_delete only
                query = """
                    DELETE FROM vector_store
                    WHERE id = ANY(%s)
                """
                # Extract the 'id' values from the list of dictionaries (ids_to_delete)
                ids_to_delete_values = [item["id"] for item in ids_to_delete]

                # Execute the query, passing the list of IDs as parameters
                cursor.execute(query, (ids_to_delete_values,))

                # Commit the transaction
                conn.commit()

                # Return the number of deleted rows
                deleted_rows = cursor.rowcount
                logger.info(f"Deleted {deleted_rows} documents.")
                return deleted_rows
        except psycopg2.Error as db_err:
            logger.error(f"Database error while deleting documents: {db_err}")
            # Only attempt rollback if connection is still open
            if conn and conn.closed == 0:
                try:
                    conn.rollback()
                except Exception as rollback_error:
                    logger.warning(f"Failed to rollback transaction: {rollback_error}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error while deleting documents: {e}")
            # Only attempt rollback if connection is still open
            if conn and conn.closed == 0:
                try:
                    conn.rollback()
                except Exception as rollback_error:
                    logger.warning(f"Failed to rollback transaction: {rollback_error}")
            raise
        finally:
            # Only close connection if it exists and is open
            if conn and conn.closed == 0:
                conn.close()

    @logger.trace_function(log_execution=log_execution, log_args=log_args, log_result=False)
    def perform_search(self, title):
        """
        Fetches search results from PostgreSQL based on the title.

        Args:
            title (str): The title to search for

        Returns:
            list[dict] or None: Search results or None if no results found
        """
        # Establish connection to PostgreSQL
        conn = self.get_search_client()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                # Execute query to fetch title, content, and metadata without tenant filtering
                cur.execute(
                    """
                    SELECT title, content, metadata
                    FROM vector_store
                    WHERE title = %s
                    """,
                    (title,),
                )
                results = cur.fetchall()  # Fetch all matching results
                logger.info(f"Retrieved {len(results)} search result(s).")
                return results
        except Exception as e:
            logger.error(f"Error executing search query: {e}")
            raise
        finally:
            # Only close connection if it exists and is open
            if conn and conn.closed == 0:
                conn.close()

    @logger.trace_function(log_execution=log_execution, log_args=log_args, log_result=log_result)
    def get_unique_files(self):
        """
        Fetches unique titles from PostgreSQL.

        Returns:
            list[dict] or None: A list of dictionaries (each with a single key 'title')
            or None if no titles are found or an error occurs.
        """
        # Establish connection to PostgreSQL
        conn = self.get_search_client()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                # Execute query to fetch distinct titles for all tenants
                cur.execute(
                    """
                    SELECT DISTINCT title
                    FROM vector_store
                    """
                )
                results = cur.fetchall()  # Fetch all results as RealDictRow objects
                logger.info(f"Retrieved {len(results)} unique title(s).")
                return results
        except Exception as e:
            logger.error(f"Error executing search query: {e}")
            raise
        finally:
            # Only close connection if it exists and is open
            if conn and conn.closed == 0:
                conn.close()

    @logger.trace_function(log_execution=log_execution, log_args=log_args, log_result=log_result)
    def search_by_blob_url(self, blob_url):
        """
        Fetches unique titles from PostgreSQL based on a given blob URL.
        """
        # Establish connection to PostgreSQL
        conn = self.get_search_client()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                # Execute parameterized query to fetch results
                cur.execute(
                    """
                    SELECT id, title
                    FROM vector_store
                    WHERE source = %s
                    """,
                    (f"{blob_url}_SAS_TOKEN_PLACEHOLDER_",),
                )
                results = cur.fetchall()  # Fetch all results as RealDictRow objects
                logger.info(f"Retrieved {len(results)} unique title(s).")
                return results
        except Exception as e:
            logger.error(f"Error executing search query: {e}")
            raise
        finally:
            # Only close connection if it exists and is open
            if conn and conn.closed == 0:
                conn.close()
