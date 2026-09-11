from typing import Any, Dict, List, Optional

from sqlalchemy.engine import URL

from .database_transformer import DatabaseTransformer


class DocumentDBTransformer(DatabaseTransformer):
    """
    Database transformer for Amazon DocumentDB connections.

    Transforms DocumentDB connection configuration into SQLAlchemy-compatible format
    using the pymongosql driver. Supports both BASIC (username/password) and IAM
    (MONGODB-AWS) authentication mechanisms.
    """

    @classmethod
    def get_dialect(cls) -> Optional[str]:
        return None  # MongoDB query language, not a SQL dialect supported by sqlglot

    @staticmethod
    def get_required_fields() -> List[str]:
        return ["host", "port", "database"]

    @staticmethod
    def to_sqlalchemy_config(connection_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform DocumentDB connection data into SQLAlchemy configuration.

        Builds the connection URL with SQLAlchemy ``URL.create()``, which safely
        encodes every component (host, database, credentials and query options).
        This prevents connection-string injection: URI metacharacters in an
        attacker-influenced host or database are percent-encoded (or confined to
        the host field) rather than interpreted, so they can never inject query
        options such as ``tls=false`` that would override the hardcoded security
        parameters below.

        Handles both BASIC auth (username/password) and IAM auth (MONGODB-AWS mechanism).

        The connection follows AWS DocumentDB recommended patterns:
        - retryWrites=false (DocumentDB does not support retryable writes)
        - replicaSet=rs0 (connect as replica set for cluster endpoints)
        - readPreference=secondaryPreferred (distribute reads to replicas)

        Args:
            connection_data (Dict[str, Any]): DocumentDB connection configuration containing:
                - host (required): DocumentDB cluster endpoint
                - port (required): Port number (typically 27017)
                - database (required): Database name
                - auth_mechanism (optional): "MONGODB-AWS" for IAM auth, None for BASIC
                - user (optional): Username for BASIC auth
                - password (optional): Password for BASIC auth
                - tls (optional): Whether to use TLS (default True)

        Returns:
            Dict[str, Any]: SQLAlchemy configuration with:
                - connection_string: SQLAlchemy ``URL`` object for the connection

        Raises:
            ValueError: If required fields are missing.
        """
        DocumentDBTransformer.validate_required_fields(
            DocumentDBTransformer.get_required_fields(), connection_data
        )

        host = connection_data["host"]
        port = connection_data["port"]
        database = connection_data["database"]
        auth_mechanism = connection_data.get("auth_mechanism")
        tls = connection_data.get("tls", True)

        # Query parameters following AWS DocumentDB best practices. URL.create()
        # encodes these values, so no manual escaping is required.
        query: Dict[str, str] = {
            "retryWrites": "false",
            "replicaSet": "rs0",
            "readPreference": "secondaryPreferred",
        }

        if tls:
            query["tls"] = "true"

        username: Optional[str] = None
        password: Optional[str] = None
        if auth_mechanism == "MONGODB-AWS":
            # IAM auth — no credentials in the URL; pymongo picks up AWS
            # credentials from the environment via the MONGODB-AWS mechanism.
            query["authMechanism"] = "MONGODB-AWS"
            query["authSource"] = "$external"
        else:
            # BASIC auth — URL.create() encodes the credentials safely.
            username = connection_data.get("user")
            password = connection_data.get("password")

        connection_url = URL.create(
            drivername="mongodb",
            username=username,
            password=password,
            host=host,
            port=int(port),
            database=database,
            query=query,
        )

        return {"connection_string": connection_url}

    @staticmethod
    def get_loggers() -> List[str]:
        """
        Get the list of loggers used for this database connection type.

        Returns:
            List[str]: List of loggers that are used for DocumentDB connections.
        """
        return ["pymongo", "pymongosql"]
