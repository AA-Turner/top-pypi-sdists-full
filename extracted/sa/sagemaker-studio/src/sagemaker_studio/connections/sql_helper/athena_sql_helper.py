from typing import Any, Dict

from sagemaker_studio.connections.connection import Connection
from sagemaker_studio.connections.sql_helper.sql_helper import SqlHelper


class AthenaSqlHelper(SqlHelper):
    """
    SQL helper for Amazon Athena connections.

    This class transforms DataZone Athena connection data into a standardized format
    for SQL interface consumption. It handles Athena-specific configuration
    including workgroup settings and AWS credentials. The S3 query result
    location is resolved by the Athena workgroup itself rather than passed
    client-side.
    """

    @staticmethod
    def to_sql_config(connection: Connection, **kwargs) -> Dict[str, Any]:
        """
        Transform DataZone Athena connection data into SQL interface configuration.

        Extracts Athena-specific parameters including region, workgroup,
        and AWS credentials from the DataZone connection data and formats them for SQL interface use.

        Returns:
            Dict[str, Any]: Configuration dictionary containing:
                - region: AWS region for Athena service
                - work_group: Athena workgroup name
                - aws_access_key_id: AWS access key
                - aws_secret_access_key: AWS secret key
                - aws_session_token: AWS session token (if present)
        """
        connection_data = SqlHelper.get_connection_data(connection)
        physical_endpoints = connection_data["physical_endpoints"]
        aws_location = physical_endpoints[0].get("awsLocation", {}) if physical_endpoints else {}
        region = aws_location.get("awsRegion")
        # ``props.athenaProperties.workgroupName`` for an ATHENA connection; a LAKEHOUSE catalog
        # connection names its workgroup in ``configurations`` (see Connection.athena_workgroup).
        work_group = connection_data.get("workgroup_name") or getattr(
            connection, "athena_workgroup", None
        )
        if not work_group:
            name = getattr(connection, "name", None)
            raise RuntimeError(f"Connection {name} names no Athena workgroup")
        # A query-level catalog (USE ... / catalog.database.table) wins; otherwise the catalog the
        # connection itself names applies (AWS Notebook connections carry a top-level ``catalog``;
        # DataZone records carry none, so the workgroup's default is used).
        catalog_name = kwargs.get("catalog_name") or connection_data.get("catalog")
        schema_name = kwargs.get("schema_name")

        config = {
            "region": region,
            "work_group": work_group,
        }

        # Use credential_provider if provided, otherwise use static credentials
        credential_provider = kwargs.get("credential_provider")

        if credential_provider is not None:
            config["credential_provider"] = credential_provider
        else:
            connection_creds = connection_data["connection_creds"]
            config["aws_access_key_id"] = connection_creds.get("access_key_id")
            config["aws_secret_access_key"] = connection_creds.get("secret_access_key")
            if connection_creds.get("session_token"):
                config["aws_session_token"] = connection_creds.get("session_token")

        if catalog_name:
            config["catalog_name"] = catalog_name
        if schema_name:
            config["schema_name"] = schema_name

        return config
