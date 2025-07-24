# canonmap/services/db_mysql/helpers/cloud_sql.py

import os
import logging
from typing import Optional

from canonmap.services.db_mysql.config import CanonMapMySQLConfig
from canonmap.services.db_mysql.core import CanonMapMySQLClient

logger = logging.getLogger(__name__)

def create_cloud_sql_client(
    project_id: Optional[str] = None,
    region: Optional[str] = None,
    instance_name: Optional[str] = None,
    database_name: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
) -> CanonMapMySQLClient:
    """
    Create a CanonMapMySQLClient configured for Google Cloud SQL.
    
    Args:
        project_id: GCP project ID (defaults to GOOGLE_CLOUD_PROJECT env var)
        region: Cloud SQL region (defaults to DB_REGION env var)
        instance_name: Cloud SQL instance name (defaults to DB_INSTANCE env var)
        database_name: Database name (defaults to DB_NAME env var)
        user: MySQL username (defaults to DB_USER env var)
        password: MySQL password (defaults to DB_PASSWORD env var)
    
    Returns:
        CanonMapMySQLClient configured for Cloud SQL
    """
    # Get values from environment if not provided
    project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
    region = region or os.getenv("DB_REGION")
    instance_name = instance_name or os.getenv("DB_INSTANCE")
    database_name = database_name or os.getenv("DB_NAME")
    user = user or os.getenv("DB_USER")
    password = password or os.getenv("DB_PASSWORD")
    
    if not all([project_id, region, instance_name, database_name, user, password]):
        raise ValueError(
            "Missing required Cloud SQL configuration. Please provide all parameters "
            "or set the following environment variables:\n"
            "- GOOGLE_CLOUD_PROJECT (or project_id parameter)\n"
            "- DB_REGION (or region parameter)\n"
            "- DB_INSTANCE (or instance_name parameter)\n"
            "- DB_NAME (or database_name parameter)\n"
            "- DB_USER (or user parameter)\n"
            "- DB_PASSWORD (or password parameter)"
        )
    
    # Construct Unix socket path for Cloud SQL
    unix_socket = f"/cloudsql/{project_id}:{region}:{instance_name}"
    
    config = CanonMapMySQLConfig(
        host="localhost",  # Not used with Unix socket
        user=user,
        password=password,
        database=database_name,
        unix_socket=unix_socket,
    )
    
    logger.info(f"Creating Cloud SQL client for instance: {project_id}:{region}:{instance_name}")
    return CanonMapMySQLClient(config)

def create_client_from_env() -> CanonMapMySQLClient:
    """
    Create a CanonMapMySQLClient using environment variables.
    
    This function will automatically detect whether to use Cloud SQL (Unix socket)
    or regular MySQL (TCP) based on the presence of DB_UNIX_SOCKET environment variable.
    
    Environment variables:
    - For Cloud SQL: DB_UNIX_SOCKET, DB_USER, DB_PASSWORD, DB_NAME
    - For regular MySQL: DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
    """
    config = CanonMapMySQLConfig.from_environment()
    logger.info("Creating MySQL client from environment configuration")
    return CanonMapMySQLClient(config) 