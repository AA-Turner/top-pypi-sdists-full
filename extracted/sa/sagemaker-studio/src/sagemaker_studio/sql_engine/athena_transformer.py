import logging
from typing import Any, Dict, List, Optional

from botocore.credentials import RefreshableCredentials
from botocore.session import get_session

from .database_transformer import DatabaseTransformer
from .resource_fetching_definition import ResourceFetchingDefinition, SQLAlchemyMetadataAction

logger = logging.getLogger(__name__)


class AthenaTransformer(DatabaseTransformer):
    """
    Database transformer for Amazon Athena connections.

    This transformer converts Athena connection configuration into SQLAlchemy-compatible
    format using the PyAthena driver. It handles Athena-specific requirements including
    workgroup configuration. The S3 query result location is resolved by the
    workgroup rather than passed client-side.
    """

    @classmethod
    def get_dialect(cls) -> Optional[str]:
        # sqlglot's dedicated Athena dialect treats DDL as HiveQL (keeps `string`,
        # `int`, etc.) and DML as Trino, unlike "presto" which forces Trino types
        # onto DDL and turns `string` into `VARCHAR`. the Athena dialect is still the correct source
        # grammar for parsing Athena-specific syntax.
        return "athena"

    @staticmethod
    def get_execution_metadata(cursor: Any) -> Optional[Dict[str, Any]]:
        """Extract Athena execution metadata from the PyAthena cursor."""
        try:
            metadata: Dict[str, Any] = {}
            if hasattr(cursor, "query_id") and cursor.query_id:
                metadata["query_execution_id"] = cursor.query_id
            if (
                hasattr(cursor, "data_scanned_in_bytes")
                and cursor.data_scanned_in_bytes is not None
            ):
                metadata["data_scanned_bytes"] = cursor.data_scanned_in_bytes
            if (
                hasattr(cursor, "engine_execution_time_in_millis")
                and cursor.engine_execution_time_in_millis is not None
            ):
                metadata["engine_execution_time_ms"] = cursor.engine_execution_time_in_millis
            if (
                hasattr(cursor, "total_execution_time_in_millis")
                and cursor.total_execution_time_in_millis is not None
            ):
                metadata["total_execution_time_ms"] = cursor.total_execution_time_in_millis
            if (
                hasattr(cursor, "query_queue_time_in_millis")
                and cursor.query_queue_time_in_millis is not None
            ):
                metadata["query_queue_time_ms"] = cursor.query_queue_time_in_millis
            if (
                hasattr(cursor, "query_planning_time_in_millis")
                and cursor.query_planning_time_in_millis is not None
            ):
                metadata["query_planning_time_ms"] = cursor.query_planning_time_in_millis
            if (
                hasattr(cursor, "service_processing_time_in_millis")
                and cursor.service_processing_time_in_millis is not None
            ):
                metadata["service_processing_time_ms"] = cursor.service_processing_time_in_millis
            if hasattr(cursor, "submission_date_time") and cursor.submission_date_time:
                metadata["submission_time"] = cursor.submission_date_time.isoformat()
            if hasattr(cursor, "completion_date_time") and cursor.completion_date_time:
                metadata["completion_time"] = cursor.completion_date_time.isoformat()
            if hasattr(cursor, "state") and cursor.state:
                metadata["state"] = cursor.state
            if hasattr(cursor, "output_location") and cursor.output_location:
                metadata["output_location"] = cursor.output_location
            return metadata if metadata else None
        except Exception:
            logger.debug("Failed to extract Athena metadata", exc_info=True)
            return None

    @staticmethod
    def get_required_fields() -> List[str]:
        """
        Get required fields for Athena connections.

        Returns:
            List[str]: List containing "work_group" as the mandatory field
                for Athena connections. The S3 query result location is supplied
                by the workgroup configuration rather than client-side.
        """
        return ["work_group"]

    @staticmethod
    def to_sqlalchemy_config(connection_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform Athena connection data into SQLAlchemy configuration.

        Creates a SQLAlchemy connection string using the awsathena+rest driver
        and passes all connection data as connect_args for PyAthena.

        Args:
            connection_data (Dict[str, Any]): Athena connection configuration containing
                work_group, region, and AWS credentials.

        Returns:
            Dict[str, Any]: SQLAlchemy configuration with:
                - connection_string: awsathena+rest:// URL for the specified region
                - connect_args: Original connection_data passed to PyAthena driver

        Raises:
            ValueError: If required fields (work_group) are missing.
        """
        AthenaTransformer.validate_required_fields(
            AthenaTransformer.get_required_fields(), connection_data
        )

        region = connection_data.get("region")

        connection_string = f"awsathena+rest://@athena.{region}.amazonaws.com"

        # Copy before mutating so callers that retain the input dict don't observe
        # our credential-provider→botocore_session rewrite as a side effect.
        connect_args = dict(connection_data)

        # PyAthena does not support a `credential_provider` kwarg: unknown args land in
        # its internal _kwargs and are filtered out against a boto3 allowlist, so the
        # callable is silently discarded and PyAthena falls back to the ambient default
        # credential chain — the wrong account for cross-account workgroups. Convert the
        # provider into a refreshable `botocore_session`, which *is* on PyAthena's
        # allowlist, so credentials are actually applied (and refreshed on expiry).
        credential_provider = connect_args.pop("credential_provider", None)
        if credential_provider is not None:
            connect_args["botocore_session"] = AthenaTransformer._build_botocore_session(
                credential_provider
            )

        return {"connection_string": connection_string, "connect_args": connect_args}

    @staticmethod
    def _build_botocore_session(credential_provider):
        """Wrap a credential-provider callable in a refreshable botocore session.

        PyAthena forwards `botocore_session` to boto3.Session, so credentials sourced
        this way are honoured and auto-refreshed before expiry — the same mechanism the
        Redshift Data API dialect uses.
        """

        def refresh():
            creds = credential_provider()
            required_keys = ["access_key_id", "secret_access_key", "expiration"]
            missing = [k for k in required_keys if k not in creds]
            if missing:
                raise ValueError(
                    f"credential_provider must return a dict with keys: {required_keys}. "
                    f"Missing: {missing}"
                )
            return {
                "access_key": creds["access_key_id"],
                "secret_key": creds["secret_access_key"],
                "token": creds.get("session_token"),
                "expiry_time": creds.get("expiration"),
            }

        session_credentials = RefreshableCredentials.create_from_metadata(
            metadata=refresh(),
            refresh_using=refresh,
            method="custom-provider",
            advisory_timeout=60,  # Refresh 1 minute before expiry
        )
        botocore_session = get_session()
        botocore_session._credentials = session_credentials
        return botocore_session

    @staticmethod
    def get_resources_action(
        resource_type: Optional[str], parents: Optional[Dict[str, str]] = None
    ) -> ResourceFetchingDefinition:
        """
        Build a definition for metadata-based resource discovery.

        Returns a `ResourceFetchingDefinition` configured to use SQLAlchemy’s
        Inspector for listing resources, based on the requested `resource_type`.
        If `resource_type` is `None`, it defaults to the database level.

        This method does **not** read `parents`; any required parent context
        (e.g., schema when listing tables) is supplied later by the consumer
        when executing the definition.

        Args:
          resource_type: Which level to discover. Supported values:
            `"DATABASE"`, `"TABLE"`, `"COLUMN"`. If `None`, treated as `"DATABASE"`.
          parents: Optional mapping of parent identifiers. Ignored here, kept
            for syntax purposes.

        Returns:
          A `ResourceFetchingDefinition` in SQLAlchemy-metadata mode with:
            - `GET_TABLE_NAMES` for `"TABLE"` (children: `("COLUMN",)`),
            - `GET_COLUMN_NAMES` for `"COLUMN"` (children: `()`),
            - `GET_SCHEMA_NAMES` for `"DATABASE"` or `None` (children: `("TABLE",)`).

        Raises:
          ValueError: If `resource_type` is not one of the supported values.
        """
        match resource_type:
            case "TABLE":
                return ResourceFetchingDefinition.from_sqlalchemy_metadata(
                    SQLAlchemyMetadataAction.GET_TABLE_NAMES,
                    default_type="TABLE",
                    children=("COLUMN",),
                )
            case "COLUMN":
                return ResourceFetchingDefinition.from_sqlalchemy_metadata(
                    SQLAlchemyMetadataAction.GET_COLUMN_NAMES,
                    default_type="COLUMN",
                    children=(),
                )
            case "DATABASE" | None:
                return ResourceFetchingDefinition.from_sqlalchemy_metadata(
                    SQLAlchemyMetadataAction.GET_SCHEMA_NAMES,
                    default_type="DATABASE",
                    children=("TABLE",),
                )
            case other:
                raise ValueError(f"Unsupported resource type: {other!r}")
