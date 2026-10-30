from __future__ import annotations

import json
import logging
import re
from dataclasses import asdict, dataclass, field, make_dataclass
from typing import Any, Dict, List, Optional, Union

import boto3
from botocore.client import BaseClient
from botocore.exceptions import ClientError

from sagemaker_studio import local_kernel
from sagemaker_studio.connections.providers import ConnectionProvider
from sagemaker_studio.connections.providers.app_api import athena_workgroup
from sagemaker_studio.connections.providers.datazone import DataZoneConnectionProvider
from sagemaker_studio.data_models import ClientConfig
from sagemaker_studio.exceptions import AWSClientException

from .catalog import Catalog

# Supported Glue connection types for spark_options
SUPPORTED_GLUE_CONNECTION_TYPES = [
    "SNOWFLAKE",
    "BIGQUERY",
    "DOCUMENTDB",
    "DYNAMODB",
    "MYSQL",
    "OPENSEARCH",
    "ORACLE",
    "POSTGRESQL",
    "REDSHIFT",
    "SAPHANA",
    "SQLSERVER",
    "TERADATA",
    "VERTICA",
    "WORKDAYLDQ",
]

SUPPORTED_IRC_GLUE_CONNECTION_TYPES = [
    "WORKDAYICEBERGRESTCATALOG",
    "DATABRICKSICEBERGRESTCATALOG",
    "SNOWFLAKEICEBERGRESTCATALOG",
    "ICEBERGRESTCATALOG",
]


class MaskedDict(dict):
    """Dictionary that masks password values when printed but allows normal access."""

    def __repr__(self):
        masked = self.copy()
        if "password" in masked:
            masked["password"] = "****"
        return dict.__repr__(masked)

    def __str__(self):
        return self.__repr__()


@dataclass
class PhysicalEndpoint:
    """
    Represents the physical endpoint details of a connection.

    Attributes:
        access_role (Optional[str]): The IAM role associated with the physical endpoint.
        aws_account_id (Optional[str]): The AWS account ID associated with the physical endpoint.
        aws_region (Optional[str]): The AWS region associated with the physical endpoint.
        iam_connection_id (Optional[str]): The IAM connection ID associated with the physical endpoint.
        glue_connection_name (Optional[str]): The Glue connection name associated with the physical endpoint.
        host (Optional[str]): The host of the physical endpoint.
        port (Optional[str]): The port of the physical endpoint.
        protocol (Optional[str]): The protocol of the physical endpoint.
        stage (Optional[str]): The stage of the physical endpoint.
    """

    _connection_instance: Connection
    access_role: Optional[str] = None
    aws_account_id: Optional[str] = None
    aws_region: Optional[str] = None
    iam_connection_id: Optional[str] = None
    glue_connection_name: Optional[str] = None
    host: Optional[str] = None
    port: Optional[str] = None
    protocol: Optional[str] = None
    stage: Optional[str] = None
    _glue_connection: Optional[Dict] = field(default=None)

    @property
    def glue_connection(self) -> Optional[Dict]:
        """
        Returns the Glue connection associated with this physical endpoint.
        """
        if self._glue_connection is None:
            self._connection_instance._invoke_get_connection_and_populate_fields()
            if self._connection_instance.physical_endpoints:
                return self._connection_instance.physical_endpoints[0]._glue_connection
        return self._glue_connection

    def __str__(self) -> str:
        """
        Returns a string representation of the PhysicalEndpoint object.

        This method creates a string containing all non-null attributes of the PhysicalEndpoint object.
        It excludes any attributes with None values.

        Returns:
            str: A string representation of the PhysicalEndpoint object in the format:
                 "PhysicalEndpoint(attribute1='value1', attribute2='value2', ...)"
        """
        return self.__repr__()

    def __repr__(self) -> str:
        """
        Returns a string representation of the PhysicalEndpoint object.

        This method creates a string containing all non-null attributes of the PhysicalEndpoint object.
        It excludes any attributes with None values.

        Returns:
            str: A string representation of the PhysicalEndpoint object in the format:
                 "PhysicalEndpoint(attribute1='value1', attribute2='value2', ...)"
        """
        non_null_fields = []
        for key, value in self.__dict__.items():
            if not key.startswith("_") and value is not None:
                non_null_fields.append(f"{key}='{value}'")
        if self._glue_connection is not None:
            non_null_fields.append(f"glue_connection='{self._glue_connection}'")
        return f"PhysicalEndpoint({', '.join(non_null_fields)})"


@dataclass
class ConnectionCredentials:
    """
    Represents the connection credentials details of a connection.

    Attributes:
        access_key_id (Optional[str]): The access key ID associated with the connection credentials.
        secret_access_key (Optional[str]): The secret access key associated with the connection credentials.
        session_token (Optional[str]): The session token associated with the connection credentials.
        expiration (Optional[str]): The expiration associated with the connection credentials.
    """

    access_key_id: Optional[str] = None
    secret_access_key: Optional[str] = None
    session_token: Optional[str] = None
    expiration: Optional[str] = None


@dataclass
class Connection:
    """
    Represents a connection within a SageMaker Unified Studio Project. Connection allows a user to retrieve information
    about a connection, including its name, databases, IAM role (if applicable), physical endpoints, username/password,
    JDBC URL (if applicable), and more.

    Attributes:
        name (Optional[str]): The name of the connection.
        type (Optional[str]): The type of the connection.
        id (Optional[str]): The unique identifier of the connection.
        connection_creds (Optional[ConnectionCredentials]): The connection credentials associated with the connection.
        domain_id (Optional[str]): The unique identifier of the domain the connection belongs to.
        domain_unit_id (Optional[str]): The unique identifier of the domain unit the connection belongs to.
        environment_id (Optional[str]): The unique identifier of the environment the connection belongs to.
        physical_endpoints (Optional[List[PhysicalEndpoint]]): The physical endpoints associated with the connection.
        project_id (Optional[str]): The unique identifier of the project the connection belongs to.
        iam_role (Optional[str]): The IAM role associated with the connection.

    Args:
        connection_data (Dict[str, Any]): The raw connection data.
        glue_api (BaseClient): The Glue client.
    """

    __connection_data: Dict[str, Any] = field(init=False, repr=False)
    name: Optional[str] = None
    type: Optional[str] = None
    id: Optional[str] = None
    _connection_creds: Optional[ConnectionCredentials] = field(default=None, repr=False)
    domain_id: Optional[str] = None
    domain_unit_id: Optional[str] = None
    environment_id: Optional[str] = None
    physical_endpoints: Optional[List[PhysicalEndpoint]] = None
    project_id: Optional[str] = None
    iam_role: Optional[str] = None

    def __init__(
        self,
        connection_data: Dict[str, Any],
        glue_api: BaseClient,
        datazone_api: Optional[BaseClient],
        secrets_manager_api: BaseClient,
        kms_api: BaseClient,
        project_config: ClientConfig,
        provider: Optional[ConnectionProvider] = None,
    ):
        """
        Initializes a new instance of the Connection class.

        Args:
            connection_data (Dict[str, Any]): The raw connection data.
            glue_api (BaseClient): The Glue client.
            datazone_api (BaseClient): The DataZone client, for environment queries. With no
                ``provider`` it is also what the connection fetches itself again through.
            provider: The :class:`~sagemaker_studio.connections.providers.ConnectionProvider`
                this record came from. The connection asks it for the full record again
                (``GetConnection`` ``withSecret``) when it needs credentials it does not have
                and, for a provider that re-vends them, shortly before the ones it has expire.
                Defaults to the DataZone provider over ``datazone_api``.
        """
        self._datazone_api = datazone_api
        self.__connection_data = connection_data
        self.name = self.__connection_data.get("name", None)
        self.type = self.__connection_data.get("type", None)
        self.id = self.__connection_data.get("connectionId", None)
        connection_credentials = self.__connection_data.get("connectionCredentials", None)
        self._connection_creds = self._map_connection_credentials_field(connection_credentials)
        self.domain_id = self.__connection_data.get("domainId", None)
        self.domain_unit_id = self.__connection_data.get("domainUnitId", None)
        self.environment_id = self.__connection_data.get("environmentId", None)
        physical_endpoints_data = self.__connection_data.get("physicalEndpoints", [])
        self.physical_endpoints = [
            self._map_physical_endpoint_fields(endpoint) for endpoint in physical_endpoints_data
        ]
        self.project_id = self.__connection_data.get("projectId", None)
        self.iam_role = self.__connection_data.get("environmentUserRole", None)
        self._project_config = project_config
        if provider is None and datazone_api is not None:
            provider = DataZoneConnectionProvider(datazone_api, self.domain_id, self.project_id)
        self._provider: Optional[ConnectionProvider] = provider
        if (
            self.type in ["LAKEHOUSE", "IAM"]
            or self.type in SUPPORTED_GLUE_CONNECTION_TYPES
            or self.type in SUPPORTED_IRC_GLUE_CONNECTION_TYPES
        ):
            self._glue_api: BaseClient = self._get_aws_client_with_connection_credentials(
                "glue", self._connection_creds, glue_api
            )
        self._secrets_manager_api = secrets_manager_api
        self._kms_api = kms_api

    def __str__(self) -> str:
        """
        Returns a string representation of the Connection object.

        This method creates a string containing all non-null attributes of the Connection object.
        It excludes any private attributes and attributes with None values.

        Returns:
            str: A string representation of the Connection object in the format:
                 "Connection(attribute1='value1', attribute2='value2', ...)"
        """
        return self.__repr__()

    def __repr__(self) -> str:
        """
        Returns a string representation of the Connection object.

        This method creates a string containing all non-null attributes of the Connection object.
        It excludes any private attributes and attributes with None values.

        Returns:
            str: A string representation of the Connection object in the format:
                 "Connection(attribute1='value1', attribute2='value2', ...)"
        """
        non_null_fields = []
        for key, value in self.__dict__.items():
            if not key.startswith("_") and value is not None:
                if isinstance(value, list) and len(value) > 0:
                    non_null_fields.append(f"{key}={value}")
                elif isinstance(value, str):
                    non_null_fields.append(f"{key}='{value}'")
        return f"Connection({', '.join(non_null_fields)})"

    @property
    def connection_creds(self):
        if self._connection_creds is None or self._credentials_need_refresh():
            self._invoke_get_connection_and_populate_fields()
        return self._connection_creds

    def _credentials_need_refresh(self) -> bool:
        """
        Whether to ask the provider for credentials again before use: it re-vends them
        (``refreshes_credentials``) and the ones held reach their ``expiration`` within
        :data:`sagemaker_studio.local_kernel.REFRESH_WINDOW`.
        """
        if self._provider is None or self._connection_creds is None:
            return False
        if not self._provider.refreshes_credentials:
            return False
        return local_kernel.expires_soon(self._connection_creds.expiration)

    @property
    def athena_workgroup(self) -> Optional[str]:
        """
        The Athena workgroup this connection names: ``props.athenaProperties.workgroupName`` for
        an ``ATHENA`` connection, the ``athena`` entry of ``configurations`` for a ``LAKEHOUSE``
        catalog connection. ``None`` when the connection names none.
        """
        return athena_workgroup(self.__connection_data)

    @property
    def sql_engine_type(self) -> Optional[str]:
        """
        The engine ``sql()`` runs this connection's statements on. Usually the connection type;
        ``ATHENA`` for a ``LAKEHOUSE`` catalog connection that names an Athena workgroup, which
        is how the AWS Notebook app describes a data catalog to query through Athena.
        """
        if self.type == "LAKEHOUSE" and self.athena_workgroup:
            return "ATHENA"
        return self.type

    @property
    def data(self):
        """
        Retrieves all the detailed connection data as a ConnectionData object.

        Returns:
            ConnectionData: The connection data.
        """
        return self._create_connection_data(self.__connection_data)

    @property
    def catalogs(self) -> List[Catalog]:
        """
        Retrieves all catalogs for IAM connections.

        Returns:
            List[Catalog]: A list of all available catalogs.

        Raises:
            AttributeError: If catalogs are not available for this connection type.
            RuntimeError: If there's an error retrieving the catalogs.
        """
        if self.type not in ["LAKEHOUSE", "IAM"]:
            raise AttributeError("Catalogs are only available for IAM or LAKEHOUSE connections")

        try:
            connection_catalogs: List[Catalog] = []
            next_token = None
            first_call = True
            while next_token is not None or first_call:
                first_call = False
                params: Dict[str, Any] = {"HasDatabases": True, "Recursive": True}
                if next_token:
                    params["NextToken"] = next_token
                get_catalogs_response = self._glue_api.get_catalogs(**params)  # type: ignore
                for catalog in get_catalogs_response.get("CatalogList", []):
                    connection_catalogs.append(self._catalog_builder(catalog))
                next_token = get_catalogs_response.get("NextToken")
            return connection_catalogs
        except ClientError as e:
            raise RuntimeError(
                "Encountered an error getting catalogs for the connection", AWSClientException(e)
            )
        except Exception as e:
            raise RuntimeError(
                "Encountered an unexpected exception getting catalogs for the connection", e
            )

    def catalog(self, id: Optional[str] = None) -> Catalog:
        """
        Retrieves a specific catalog for IAM connections.

        Args:
            id (Optional[str]): The identifier of the catalog. Defaults to the connections default Catalog identified by its accountId

        Returns:
            Catalog: The requested catalog.

        Raises:
            AttributeError: If catalogs are not available for this connection type.
            RuntimeError: If there's an error retrieving the catalog.
        """
        if self.type not in ["LAKEHOUSE", "IAM"]:
            raise AttributeError("Catalogs are only available for IAM or LAKEHOUSE connections")

        aws_account_id = None
        # AwsAccountId is required only when id is None or id is not prefixed with AwsAccountId
        if not id or not self._validate_catalog_id(id):
            if self.physical_endpoints is None or len(self.physical_endpoints) == 0:
                raise RuntimeError("No physical endpoints found for the connection")
            aws_account_id = self.physical_endpoints[0].aws_account_id  # type: ignore

        try:
            if not id:
                get_catalog_response = self._glue_api.get_catalog(CatalogId=aws_account_id).get("Catalog")  # type: ignore
                return self._catalog_builder(get_catalog_response)

            if not self._validate_catalog_id(id):
                id = f"{aws_account_id}:{id}" if not self._validate_aws_account_id(id) else id

            get_catalog_response = self._glue_api.get_catalog(CatalogId=id).get("Catalog")  # type: ignore
            return self._catalog_builder(get_catalog_response)
        except ClientError as e:
            raise AttributeError(
                f"Unable to access catalog '{id or aws_account_id}': {AWSClientException(e)}"
            )
        except Exception as e:
            raise RuntimeError(f"Encountered an error getting catalog '{id or aws_account_id}", e)

    @property
    def secret(self) -> Union[Dict[str, str], str]:
        """
        Retrieves the secret associated with the connection from
        SecretsManager.

        Returns:
            Dict[str, Any] | str: The secret associated with the connection.

        Raises:
            RuntimeError: If the connection is a DocumentDB connection using IAM
                authentication (which has no secret), or if there's an error
                retrieving the secret.
        """
        if len(self.physical_endpoints) >= 1 and not self.physical_endpoints[0].glue_connection:  # type: ignore
            self._invoke_get_connection_and_populate_fields()

        # Check if this is a DocumentDB IAM-authenticated connection (no secret expected)
        if self.type == "DOCUMENTDB" and self._is_iam_authenticated():
            raise RuntimeError(
                f"Connection '{self.name}' uses IAM authentication and does not have an "
                f"associated secret. Authentication uses the execution role's credentials "
                f"automatically."
            )

        if len(self.physical_endpoints) >= 1 and self.physical_endpoints[0].glue_connection:  # type: ignore
            self._secrets_manager_api: BaseClient = self._get_aws_client_with_connection_credentials(  # type: ignore
                "secretsmanager", self._connection_creds, self._secrets_manager_api
            )
            secret_arn = self._find_secret_arn()
            try:
                secret = self._secrets_manager_api.get_secret_value(SecretId=secret_arn)  # type: ignore
            except ClientError as e:
                raise RuntimeError(
                    f"Encountered an error getting secret for the connection:{self.name} {AWSClientException(e)}"
                )

            return self._parse_secret(secret)
        else:
            if hasattr(self.data, "credentials") and self.data.credentials.get("usernamePassword"):
                credentials = self.data.credentials.get("usernamePassword")
                if (
                    credentials
                    and isinstance(credentials, dict)
                    and credentials.get("username")
                    and credentials.get("password")
                ):
                    return {
                        "username": credentials.get("username"),
                        "password": credentials.get("password"),
                    }
            raise RuntimeError(
                f"Connection {self.name} does not have associated secret. Please check the connection type"
            )

    def _spark_options(self) -> Optional[Dict]:
        """
        Returns the Spark option properties using GlueConnectionLib.
        """
        if self.type is None or self.type not in SUPPORTED_GLUE_CONNECTION_TYPES:
            raise AttributeError(f"Connection Type {self.type} not supported")

        if self.physical_endpoints and self.physical_endpoints[0].glue_connection_name:
            from .glue_connection_lib import GlueConnectionWrapper, GlueConnectionWrapperInputs

            try:
                glue_connection_name = self.physical_endpoints[0].glue_connection_name
                connection = self._glue_api.get_connection(
                    Name=glue_connection_name, ApplyOverrideForComputeEnvironment="SPARK"
                )["Connection"]

                kms_client: BaseClient = self._get_aws_client_with_connection_credentials(
                    "kms", self._connection_creds, self._kms_api
                )

                secrets_manager_client: BaseClient = self._get_aws_client_with_connection_credentials(  # type: ignore
                    "secretsmanager", self._connection_creds, self._secrets_manager_api
                )

                wrapper_input = GlueConnectionWrapperInputs(
                    connection=connection,
                    kms_client=kms_client,
                    secrets_manager_client=secrets_manager_client,
                    additional_options={},
                )

                wrapper = GlueConnectionWrapper.create(wrapper_input)
                resolved_connection = wrapper.get_resolved_connection()
                spark_properties = resolved_connection.get("SparkProperties")

                if spark_properties:
                    return MaskedDict(spark_properties)
                return spark_properties

            except Exception as e:
                raise RuntimeError(
                    f"Encountered an error getting spark options for the connection:{self.name} {e}"
                )
        return None

    def _spark_catalog_configs(self, force_token_refresh: bool = False) -> Optional[Dict]:
        """
        Returns the Spark catalog configurations using GlueConnectionLib.

        Args:
            force_token_refresh: Force an OAuth2 token refresh instead of using the
                token already stored on the connection's secret. Set by the query
                layer after the catalog rejects the stored token as unauthorized.
        """
        if self.type is None or self.type not in SUPPORTED_IRC_GLUE_CONNECTION_TYPES:
            raise AttributeError(f"Connection Type {self.type} not supported")

        if self.physical_endpoints and self.physical_endpoints[0].glue_connection_name:
            from .glue_connection_lib import GlueConnectionWrapper, GlueConnectionWrapperInputs

            try:
                glue_connection_name = self.physical_endpoints[0].glue_connection_name
                connection = self._glue_api.get_connection(Name=glue_connection_name)["Connection"]

                kms_client: BaseClient = self._get_aws_client_with_connection_credentials(
                    "kms", self._connection_creds, self._kms_api
                )

                secrets_manager_client: BaseClient = self._get_aws_client_with_connection_credentials(  # type: ignore
                    "secretsmanager", self._connection_creds, self._secrets_manager_api
                )

                additional_options = {}
                if force_token_refresh:
                    additional_options["forceTokenRefresh"] = "true"

                wrapper_input = GlueConnectionWrapperInputs(
                    connection=connection,
                    kms_client=kms_client,
                    secrets_manager_client=secrets_manager_client,
                    additional_options=additional_options,
                    # Required by IRC connection types that delegate OAuth2 token
                    # acquisition to Glue's RefreshOAuth2Tokens API.
                    glue_client=self._glue_api,
                )

                wrapper = GlueConnectionWrapper.create(wrapper_input)
                catalog_configs = wrapper.get_catalog_configs()

                return catalog_configs

            except Exception as e:
                raise RuntimeError(
                    f"Encountered an error getting spark catalog options for the connection:{self.name} {e}"
                )
        return None

    def create_client(self, service_name: Optional[str] = None) -> BaseClient:
        """
        Returns a boto3 client initialized with the connection's credentials.

        Args:
            service_name (Optional[str]): The AWS service name of the boto3 client to initialize

        Returns:
            BaseClient: A boto3 client
        """
        default_aws_services_by_connection_type = {
            "ATHENA": "athena",
            "DYNAMODB": "dynamodb",
            "REDSHIFT": "redshift",
            "S3": "s3",
            "S3_FOLDER": "s3",
        }
        if not service_name and self.type not in default_aws_services_by_connection_type:
            raise RuntimeError("Please specify a service name to initialize a client")
        return self._get_aws_client_with_connection_credentials(
            service_name or default_aws_services_by_connection_type[self.type],
            self._connection_creds,
            self._secrets_manager_api,
        )

    def _create_client_with_session(self, service_name: str, botocore_session: Any) -> BaseClient:
        """Create a client signed by a prepared session for internal SDK use."""
        return self._get_aws_client_with_connection_credentials(
            service_name,
            self._connection_creds,
            self._secrets_manager_api,
            botocore_session=botocore_session,
        )

    def _is_iam_authenticated(self) -> bool:
        """
        Check if this connection uses IAM authentication.

        Returns:
            bool: True if the connection uses IAM auth, False otherwise.
        """
        try:
            if self.physical_endpoints and len(self.physical_endpoints) >= 1:
                endpoint = self.physical_endpoints[0]
                glue_conn = getattr(endpoint, "glue_connection", None)
                if glue_conn is not None:
                    auth_config = getattr(glue_conn, "authentication_configuration", None)
                    if auth_config and isinstance(auth_config, dict):
                        return auth_config.get("authenticationType", "").upper() == "IAM"
        except (AttributeError, IndexError, TypeError):
            pass
        return False

    def _find_secret_arn(self) -> str:
        """
        Finds the ARN of the secret associated with the connection. Looks in
        connection.data.glueProperties for DNA connections and DataZone GetConnection
        for redshift compute connections

        Returns:
                str: The ARN of the secret associated with the connection.

            Raises:
            RuntimeError: If there's an error finding the secret ARN.
        """
        secret_arn = None
        if len(self.physical_endpoints) >= 1 and self.physical_endpoints[0].glue_connection:  # type: ignore
            endpoint = self.physical_endpoints[0]  # type: ignore
            auth_config = getattr(endpoint.glue_connection, "authentication_configuration", None)
            if auth_config and isinstance(auth_config, dict):
                secret_arn = auth_config.get("secretArn")
        elif self.type == "REDSHIFT" and self._provider is not None:
            connection_without_secret = self._provider.get_connection_by_id(
                self.id, with_secret=False
            )
            secret_arn = (
                connection_without_secret.get("props", {})
                .get("redshiftProperties", {})
                .get("credentials", {})
                .get("secretArn")
            )
        if not secret_arn:
            raise AttributeError(f"Connection {self.name} does not have associated secret")
        return secret_arn

    def _parse_secret(self, secret: Dict[str, Any]):
        """
        Parses the secret data and sets the appropriate attributes.

        Args:
            secret (Dict[str, Any]): The secret data.
        """
        if "SecretString" in secret:
            try:
                return json.loads(secret["SecretString"])
            except json.JSONDecodeError:
                return secret["SecretString"]
        else:
            return secret["SecretBinary"]

    def _map_connection_credentials_field(
        self, creds: Dict[str, Any]
    ) -> Optional[ConnectionCredentials]:
        if not creds:
            return None
        snake_case_creds = {self._camel_to_snake(key): value for key, value in creds.items()}
        if "expiration" in snake_case_creds and isinstance(snake_case_creds["expiration"], str):
            # ISO 8601 text as the AWS Notebook app serialises it (trailing ``Z``), parsed by the
            # one parser that also tolerates text it cannot read (logged, treated as no
            # expiration) instead of failing the lookup; DataZone's expirations arrive as datetimes.
            snake_case_creds["expiration"] = local_kernel.parse_iso_datetime(
                snake_case_creds["expiration"]
            )
        return ConnectionCredentials(**snake_case_creds)

    def _map_physical_endpoint_fields(self, endpoint: Dict[str, Any]) -> PhysicalEndpoint:
        snake_case_endpoint = {self._camel_to_snake(k): v for k, v in endpoint.items()}
        aws_location = endpoint.get("awsLocation", {})
        snake_case_endpoint["aws_region"] = aws_location.get("awsRegion", None)
        snake_case_endpoint["aws_account_id"] = aws_location.get("awsAccountId", None)
        snake_case_endpoint["access_role"] = aws_location.get("accessRole", None)
        snake_case_endpoint["iam_connection_id"] = aws_location.get("iamConnectionId", None)
        snake_case_endpoint.pop("aws_location", None)
        glue_connection_data = endpoint.get("glueConnection", {})
        if glue_connection_data:
            glue_connection_class = make_dataclass(
                "GlueConnection",
                [(self._camel_to_snake(k), type(v), None) for k, v in glue_connection_data.items()],
            )
            glue_connection_instance = glue_connection_class(
                **{self._camel_to_snake(k): v for k, v in glue_connection_data.items()}
            )
            snake_case_endpoint["_glue_connection"] = glue_connection_instance
            snake_case_endpoint.pop("glue_connection", None)
            snake_case_endpoint["host"] = glue_connection_data.get("connectionProperties", {}).get(
                "HOST", None
            )
            snake_case_endpoint["port"] = glue_connection_data.get("connectionProperties", {}).get(
                "PORT", None
            )

        snake_case_endpoint["_connection_instance"] = self

        # Filter out fields that are not defined in PhysicalEndpoint to avoid TypeError
        # Get the field names that PhysicalEndpoint accepts
        physical_endpoint_fields = {f.name for f in PhysicalEndpoint.__dataclass_fields__.values()}

        # Only pass fields that PhysicalEndpoint knows about
        filtered_endpoint = {
            k: v for k, v in snake_case_endpoint.items() if k in physical_endpoint_fields
        }

        # Create the PhysicalEndpoint instance with only known fields
        physical_endpoint = PhysicalEndpoint(**filtered_endpoint)

        # Add any extra fields as attributes dynamically
        for key, value in snake_case_endpoint.items():
            if key not in physical_endpoint_fields:
                setattr(physical_endpoint, key, value)

        return physical_endpoint

    def _create_connection_data(self, connection_data: Dict[str, Any]):
        fields = []
        connection_data_snake_case = {}
        # Flattening fields (only 1 level deep) to be accessed using connection.data.<field_name>
        for key, value in connection_data.items():
            if key == "props" and isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    # This level contains PropertiesOutput key
                    if isinstance(sub_value, dict):
                        for prop_key, prop_value in sub_value.items():
                            if isinstance(prop_value, (dict, list)):
                                fields.append(
                                    (
                                        self._camel_to_snake(prop_key),
                                        type(prop_value),
                                        field(default_factory=self._default_factory(prop_value)),
                                    )
                                )
                            else:
                                fields.append(
                                    (
                                        self._camel_to_snake(prop_key),
                                        type(prop_value),
                                        field(default=prop_value),
                                    )
                                )
                            connection_data_snake_case[self._camel_to_snake(prop_key)] = prop_value
                    else:
                        fields.append(
                            (
                                self._camel_to_snake(sub_key),
                                type(sub_value),
                                field(default=sub_value),
                            )
                        )
                        connection_data_snake_case[self._camel_to_snake(sub_key)] = sub_value
            elif key != "ResponseMetadata" and key != "connectionCredentials":
                if isinstance(value, (dict, list)):
                    fields.append(
                        (
                            self._camel_to_snake(key),
                            type(value),
                            field(default_factory=self._default_factory(value)),
                        )
                    )
                else:
                    fields.append((self._camel_to_snake(key), type(value), field(default=value)))
                connection_data_snake_case[self._camel_to_snake(key)] = value
        connection_data_class_name = "ConnectionData"
        connection_data_class = make_dataclass(connection_data_class_name, fields)

        def custom_repr_for_credentials_password(self):
            data_dict = asdict(self)
            if data_dict.get("credentials") and "usernamePassword" in data_dict["credentials"]:
                data_dict["credentials"]["usernamePassword"]["password"] = "****"
            data_fields = []
            for data_key, data_value in data_dict.items():
                if (isinstance(data_value, list) or isinstance(data_value, dict)) and len(
                    data_value
                ) > 0:
                    data_fields.append(f"{data_key}={data_value}")
                elif isinstance(data_value, str):
                    data_fields.append(f"{data_key}='{data_value}'")
            return f"{connection_data_class_name}({','.join(data_fields)})"

        setattr(connection_data_class, "__repr__", custom_repr_for_credentials_password)
        return connection_data_class(**connection_data_snake_case)

    def _default_factory(self, value):
        return lambda: value

    def _camel_to_snake(self, name: str) -> str:
        s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
        return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()

    def _get_aws_client_with_connection_credentials(
        self,
        service_name: str,
        connection_credentials: Optional[ConnectionCredentials],
        existing_client: BaseClient,
        botocore_session: Optional[Any] = None,
    ) -> BaseClient:
        local_client = self._local_kernel_client(service_name, existing_client)
        if local_client is not None:
            return local_client
        if botocore_session is None and connection_credentials is None:
            self._invoke_get_connection_and_populate_fields()
            connection_credentials = self._connection_creds

        project_override_config = self._project_config.overrides.get(service_name, {})
        endpoint_region_name = (
            self.physical_endpoints[0].aws_region if self.physical_endpoints else None
        )
        region_name = (
            project_override_config.get("region")
            or endpoint_region_name
            or existing_client.meta.region_name
        )
        override_endpoint_url = project_override_config.get("endpoint_url")

        if botocore_session is not None:
            session = boto3.Session(
                botocore_session=botocore_session,
                region_name=region_name,
            )
            return session.client(service_name, endpoint_url=override_endpoint_url)  # type: ignore

        if connection_credentials is not None:
            # A session token is optional: DataZone-vended credentials always carry one, but a
            # connection vended by another provider may hold static keys without one.
            if any(
                getattr(connection_credentials, key) is None
                for key in ["access_key_id", "secret_access_key"]
            ):
                raise RuntimeError("Unable to find credentials for default IAM connection")
            return boto3.client(  # type: ignore
                service_name=service_name,
                region_name=region_name,
                endpoint_url=override_endpoint_url,
                aws_access_key_id=connection_credentials.access_key_id,
                aws_secret_access_key=connection_credentials.secret_access_key,
                aws_session_token=connection_credentials.session_token,
            )
        raise RuntimeError(f"Encountered an error getting AWS client for {service_name}.")

    def _local_kernel_client(
        self, service_name: str, existing_client: BaseClient
    ) -> Optional[BaseClient]:
        """
        For a provider that re-vends credentials (the AWS Notebook app), a client whose
        credentials are fetched again through it (``GetConnection`` ``withSecret``) shortly
        before the ``expiration`` it reported, so a long-lived client follows the app's session
        instead of signing with expired keys. ``None`` for any other provider, where the
        connection's static credentials are used as before.

        Fails fast, as a client built from static keys did: signed out, the typed error is raised
        here rather than at the first request.
        """
        if self._provider is None or not self._provider.refreshes_credentials:
            return None
        credentials = local_kernel.refreshable_credentials(lambda: self.connection_creds)
        project_override_config = self._project_config.overrides.get(service_name, {})
        endpoint = self.physical_endpoints[0] if self.physical_endpoints else None
        region_name = (
            project_override_config.get("region")
            or (endpoint.aws_region if endpoint else None)
            or getattr(getattr(existing_client, "meta", None), "region_name", None)
        )
        import botocore.session

        botocore_session = botocore.session.get_session()
        botocore_session._credentials = credentials  # type: ignore[attr-defined]
        session = boto3.Session(botocore_session=botocore_session, region_name=region_name)
        return session.client(  # type: ignore
            service_name, endpoint_url=project_override_config.get("endpoint_url")
        )

    def _catalog_builder(self, get_catalog_response) -> Catalog:
        catalog_name = get_catalog_response.get("Name")
        parent_catalog_names = "_".join(get_catalog_response.get("ParentCatalogNames", []))
        spark_catalog_name = (
            f"{parent_catalog_names}_{catalog_name}" if parent_catalog_names else catalog_name
        )
        return Catalog(
            name=catalog_name,
            id=get_catalog_response.get("CatalogId"),
            type=get_catalog_response.get("CatalogType"),
            spark_catalog_name=spark_catalog_name,
            resource_arn=get_catalog_response.get("ResourceArn"),
            federated_catalog=get_catalog_response.get("FederatedCatalog", {}),
            domain_id=str(self.domain_id),
            project_id=str(self.project_id),
            glue_api=self._glue_api,
            datazone_api=self._datazone_api,
        )

    def _validate_catalog_id(self, catalog_id: str) -> bool:
        """
        A catalog name starts with an aws account followed by a catalog name

        Args:
            catalog_id (str): The identifier of the catalog. Defaults to the connections default Catalog identified by its accountId

        Returns:
            bool
        """
        pattern = r"^\d{12}:.+"
        return bool(re.match(pattern, catalog_id))

    def _validate_aws_account_id(self, id: str) -> bool:
        """
        A catalog name starts with an aws account followed by a catalog name

        Args:
            catalog_id (str): The identifier of the catalog. Defaults to the connections default Catalog identified by its accountId

        Returns:
            bool
        """
        pattern = r"^\d{12}"
        return bool(re.match(pattern, id))

    def _invoke_get_connection_and_populate_fields(self):
        """
        Fetch this connection again through its provider (``GetConnection`` ``withSecret``) and
        take the credentials, endpoints and data from the fresh record.

        A ``ClientError`` from DataZone is logged and the connection keeps what it has, as it
        always did. A provider's typed errors (signed out, the connection gone) happen before
        any AWS call and reach the caller.
        """
        if self._provider is None:
            logging.debug(
                f"Connection {self.name} has no connection provider; skipping GetConnection refresh"
            )
            return
        try:
            self._populate_fields(dict(self._provider.get_connection_by_id(self.id)))
        except ClientError as e:
            logging.warning(
                f"Encountered an error getting connection details for connection {self.name}: {AWSClientException(e)}"
            )

    def _populate_fields(self, connection_response: Dict[str, Any]) -> None:
        """Take credentials, physical endpoints and data from a freshly fetched record."""
        connection_credentials = connection_response.get("connectionCredentials", None)
        self._connection_creds = self._map_connection_credentials_field(connection_credentials)

        self.physical_endpoints = [
            self._map_physical_endpoint_fields(endpoint)
            for endpoint in connection_response.get("physicalEndpoints", [])
        ]

        self.__connection_data = connection_response
