from .core import CanonMap
from .services.db_mysql.config import CanonMapMySQLConfig
from .services.db_mysql.core import CanonMapMySQLClient
from .services.db_mysql.schemas import EntityMappingRequest, EntityMappingResponse, SingleMappedEntity, TableField, FieldTransform, FieldTransformType

# Cloud SQL helper functions
def create_cloud_sql_client(project_id=None, region=None, instance_name=None, database_name=None, user=None, password=None):
    """
    Create a CanonMapMySQLClient configured for Google Cloud SQL.
    
    This function avoids circular imports by importing locally.
    """
    from .services.db_mysql.helpers.cloud_sql import create_cloud_sql_client as _create_cloud_sql_client
    return _create_cloud_sql_client(project_id, region, instance_name, database_name, user, password)

def create_client_from_env():
    """
    Create a CanonMapMySQLClient using environment variables.
    
    This function avoids circular imports by importing locally.
    """
    from .services.db_mysql.helpers.cloud_sql import create_client_from_env as _create_client_from_env
    return _create_client_from_env()

__all__ = [
    "CanonMap",
    "CanonMapMySQLConfig",
    "CanonMapMySQLClient",
    "EntityMappingRequest",
    "EntityMappingResponse",
    "SingleMappedEntity",
    "TableField",
    "FieldTransform",
    "FieldTransformType",
    "create_cloud_sql_client",
    "create_client_from_env",
]