from datetime import datetime
from enum import StrEnum
from typing import TypedDict

from localstack.aws.api import RequestContext, ServiceException, ServiceRequest, handler

Boolean = bool
BoxedBoolean = bool
BoxedDouble = float
ClientToken = str
ClusterIdentifierString = str
Integer = int
ListStatementsLimit = int
PageSize = int
ParameterName = str
ParameterValue = str
SecretArn = str
SessionAliveSeconds = int
StatementNameString = str
StatementString = str
String = str
UUID = str
WorkgroupNameString = str
bool = bool


class ResultFormatString(StrEnum):
    JSON = "JSON"
    CSV = "CSV"


class StatementStatusString(StrEnum):
    SUBMITTED = "SUBMITTED"
    PICKED = "PICKED"
    STARTED = "STARTED"
    FINISHED = "FINISHED"
    ABORTED = "ABORTED"
    FAILED = "FAILED"


class StatusString(StrEnum):
    SUBMITTED = "SUBMITTED"
    PICKED = "PICKED"
    STARTED = "STARTED"
    FINISHED = "FINISHED"
    ABORTED = "ABORTED"
    FAILED = "FAILED"
    ALL = "ALL"


class ActiveSessionsExceededException(ServiceException):
    """The Amazon Redshift Data API operation failed because the maximum number
    of active sessions exceeded.
    """

    code: str = "ActiveSessionsExceededException"
    sender_fault: bool = False
    status_code: int = 400


class ActiveStatementsExceededException(ServiceException):
    """The number of active statements exceeds the limit."""

    code: str = "ActiveStatementsExceededException"
    sender_fault: bool = False
    status_code: int = 400


class BatchExecuteStatementException(ServiceException):
    """An SQL statement encountered an environmental error while running."""

    code: str = "BatchExecuteStatementException"
    sender_fault: bool = False
    status_code: int = 400
    StatementId: String


class DatabaseConnectionException(ServiceException):
    """Connection to a database failed."""

    code: str = "DatabaseConnectionException"
    sender_fault: bool = False
    status_code: int = 400


class ExecuteStatementException(ServiceException):
    """The SQL statement encountered an environmental error while running."""

    code: str = "ExecuteStatementException"
    sender_fault: bool = False
    status_code: int = 400
    StatementId: String


class InternalServerException(ServiceException):
    """The Amazon Redshift Data API operation failed due to invalid input."""

    code: str = "InternalServerException"
    sender_fault: bool = False
    status_code: int = 400


class QueryTimeoutException(ServiceException):
    """The Amazon Redshift Data API operation failed due to timeout."""

    code: str = "QueryTimeoutException"
    sender_fault: bool = False
    status_code: int = 400


class ResourceNotFoundException(ServiceException):
    """The Amazon Redshift Data API operation failed due to a missing resource."""

    code: str = "ResourceNotFoundException"
    sender_fault: bool = False
    status_code: int = 400
    ResourceId: String


class ValidationException(ServiceException):
    """The Amazon Redshift Data API operation failed due to invalid input."""

    code: str = "ValidationException"
    sender_fault: bool = False
    status_code: int = 400


SqlList = list[StatementString]


class BatchExecuteStatementInput(ServiceRequest):
    Sqls: SqlList
    ClusterIdentifier: ClusterIdentifierString | None
    SecretArn: SecretArn | None
    DbUser: String | None
    Database: String | None
    WithEvent: Boolean | None
    StatementName: StatementNameString | None
    WorkgroupName: WorkgroupNameString | None
    ClientToken: ClientToken | None
    ResultFormat: ResultFormatString | None
    SessionKeepAliveSeconds: SessionAliveSeconds | None
    SessionId: UUID | None


DbGroupList = list[String]
Timestamp = datetime


class BatchExecuteStatementOutput(TypedDict, total=False):
    Id: UUID | None
    CreatedAt: Timestamp | None
    ClusterIdentifier: ClusterIdentifierString | None
    DbUser: String | None
    DbGroups: DbGroupList | None
    Database: String | None
    SecretArn: SecretArn | None
    WorkgroupName: WorkgroupNameString | None
    SessionId: UUID | None


Blob = bytes
BoxedLong = int


class CancelStatementRequest(ServiceRequest):
    Id: UUID


class CancelStatementResponse(TypedDict, total=False):
    Status: Boolean | None


class ColumnMetadata(TypedDict, total=False):
    """The properties (metadata) of a column."""

    isCaseSensitive: bool | None
    isCurrency: bool | None
    isSigned: bool | None
    label: String | None
    name: String | None
    nullable: Integer | None
    precision: Integer | None
    scale: Integer | None
    schemaName: String | None
    tableName: String | None
    typeName: String | None
    length: Integer | None
    columnDefault: String | None


ColumnList = list[ColumnMetadata]
ColumnMetadataList = list[ColumnMetadata]
DatabaseList = list[String]


class DescribeStatementRequest(ServiceRequest):
    Id: UUID


Long = int


class SubStatementData(TypedDict, total=False):
    """Information about an SQL statement."""

    Id: UUID
    Duration: Long | None
    Error: String | None
    Status: StatementStatusString | None
    CreatedAt: Timestamp | None
    UpdatedAt: Timestamp | None
    QueryString: StatementString | None
    ResultRows: Long | None
    ResultSize: Long | None
    RedshiftQueryId: Long | None
    HasResultSet: Boolean | None


SubStatementList = list[SubStatementData]


class SqlParameter(TypedDict, total=False):
    """A parameter used in a SQL statement."""

    name: ParameterName
    value: ParameterValue


SqlParametersList = list[SqlParameter]


class DescribeStatementResponse(TypedDict, total=False):
    Id: UUID
    SecretArn: SecretArn | None
    DbUser: String | None
    Database: String | None
    ClusterIdentifier: String | None
    Duration: Long | None
    Error: String | None
    Status: StatusString | None
    CreatedAt: Timestamp | None
    UpdatedAt: Timestamp | None
    RedshiftPid: Long | None
    HasResultSet: Boolean | None
    QueryString: StatementString | None
    ResultRows: Long | None
    ResultSize: Long | None
    RedshiftQueryId: Long | None
    QueryParameters: SqlParametersList | None
    SubStatements: SubStatementList | None
    WorkgroupName: WorkgroupNameString | None
    ResultFormat: ResultFormatString | None
    SessionId: String | None


class DescribeTableRequest(ServiceRequest):
    ClusterIdentifier: ClusterIdentifierString | None
    SecretArn: SecretArn | None
    DbUser: String | None
    Database: String
    ConnectedDatabase: String | None
    Schema: String | None
    Table: String | None
    NextToken: String | None
    MaxResults: PageSize | None
    WorkgroupName: WorkgroupNameString | None


class DescribeTableResponse(TypedDict, total=False):
    TableName: String | None
    ColumnList: ColumnList | None
    NextToken: String | None


class ExecuteStatementInput(ServiceRequest):
    Sql: StatementString
    ClusterIdentifier: ClusterIdentifierString | None
    SecretArn: SecretArn | None
    DbUser: String | None
    Database: String | None
    WithEvent: Boolean | None
    StatementName: StatementNameString | None
    Parameters: SqlParametersList | None
    WorkgroupName: WorkgroupNameString | None
    ClientToken: ClientToken | None
    ResultFormat: ResultFormatString | None
    SessionKeepAliveSeconds: SessionAliveSeconds | None
    SessionId: UUID | None


class ExecuteStatementOutput(TypedDict, total=False):
    Id: UUID | None
    CreatedAt: Timestamp | None
    ClusterIdentifier: ClusterIdentifierString | None
    DbUser: String | None
    DbGroups: DbGroupList | None
    Database: String | None
    SecretArn: SecretArn | None
    WorkgroupName: WorkgroupNameString | None
    SessionId: UUID | None


class Field(TypedDict, total=False):
    """A data value in a column."""

    isNull: BoxedBoolean | None
    booleanValue: BoxedBoolean | None
    longValue: BoxedLong | None
    doubleValue: BoxedDouble | None
    stringValue: String | None
    blobValue: Blob | None


FieldList = list[Field]


class QueryRecords(TypedDict, total=False):
    """The results of the SQL statement."""

    CSVRecords: String | None


FormattedSqlRecords = list[QueryRecords]


class GetStatementResultRequest(ServiceRequest):
    Id: UUID
    NextToken: String | None


SqlRecords = list[FieldList]


class GetStatementResultResponse(TypedDict, total=False):
    Records: SqlRecords
    ColumnMetadata: ColumnMetadataList | None
    TotalNumRows: Long | None
    NextToken: String | None


class GetStatementResultV2Request(ServiceRequest):
    Id: UUID
    NextToken: String | None


class GetStatementResultV2Response(TypedDict, total=False):
    Records: FormattedSqlRecords
    ColumnMetadata: ColumnMetadataList | None
    TotalNumRows: Long | None
    ResultFormat: ResultFormatString | None
    NextToken: String | None


class ListDatabasesRequest(ServiceRequest):
    ClusterIdentifier: ClusterIdentifierString | None
    Database: String
    SecretArn: SecretArn | None
    DbUser: String | None
    NextToken: String | None
    MaxResults: PageSize | None
    WorkgroupName: WorkgroupNameString | None


class ListDatabasesResponse(TypedDict, total=False):
    Databases: DatabaseList | None
    NextToken: String | None


class ListSchemasRequest(ServiceRequest):
    ClusterIdentifier: ClusterIdentifierString | None
    SecretArn: SecretArn | None
    DbUser: String | None
    Database: String
    ConnectedDatabase: String | None
    SchemaPattern: String | None
    NextToken: String | None
    MaxResults: PageSize | None
    WorkgroupName: WorkgroupNameString | None


SchemaList = list[String]


class ListSchemasResponse(TypedDict, total=False):
    Schemas: SchemaList | None
    NextToken: String | None


class ListStatementsRequest(ServiceRequest):
    NextToken: String | None
    MaxResults: ListStatementsLimit | None
    StatementName: StatementNameString | None
    Status: StatusString | None
    RoleLevel: Boolean | None
    Database: String | None
    ClusterIdentifier: ClusterIdentifierString | None
    WorkgroupName: WorkgroupNameString | None


StatementStringList = list[StatementString]


class StatementData(TypedDict, total=False):
    """The SQL statement to run."""

    Id: UUID
    QueryString: StatementString | None
    QueryStrings: StatementStringList | None
    SecretArn: SecretArn | None
    Status: StatusString | None
    StatementName: StatementNameString | None
    CreatedAt: Timestamp | None
    UpdatedAt: Timestamp | None
    QueryParameters: SqlParametersList | None
    IsBatchStatement: Boolean | None
    ResultFormat: ResultFormatString | None
    SessionId: UUID | None


StatementList = list[StatementData]


class ListStatementsResponse(TypedDict, total=False):
    Statements: StatementList
    NextToken: String | None


class ListTablesRequest(ServiceRequest):
    ClusterIdentifier: ClusterIdentifierString | None
    SecretArn: SecretArn | None
    DbUser: String | None
    Database: String
    ConnectedDatabase: String | None
    SchemaPattern: String | None
    TablePattern: String | None
    NextToken: String | None
    MaxResults: PageSize | None
    WorkgroupName: WorkgroupNameString | None


class TableMember(TypedDict, total=False):
    name: String | None
    type: String | None
    schema: String | None


TableList = list[TableMember]


class ListTablesResponse(TypedDict, total=False):
    Tables: TableList | None
    NextToken: String | None


class RedshiftDataApi:
    service: str = "redshift-data"
    version: str = "2019-12-20"

    @handler("BatchExecuteStatement")
    def batch_execute_statement(
        self,
        context: RequestContext,
        sqls: SqlList,
        cluster_identifier: ClusterIdentifierString | None = None,
        secret_arn: SecretArn | None = None,
        db_user: String | None = None,
        database: String | None = None,
        with_event: Boolean | None = None,
        statement_name: StatementNameString | None = None,
        workgroup_name: WorkgroupNameString | None = None,
        client_token: ClientToken | None = None,
        result_format: ResultFormatString | None = None,
        session_keep_alive_seconds: SessionAliveSeconds | None = None,
        session_id: UUID | None = None,
        **kwargs,
    ) -> BatchExecuteStatementOutput:
        """Runs one or more SQL statements, which can be data manipulation language
        (DML) or data definition language (DDL). Depending on the authorization
        method, use one of the following combinations of request parameters:

        -  Secrets Manager - when connecting to a cluster, provide the
           ``secret-arn`` of a secret stored in Secrets Manager which has
           ``username`` and ``password``. The specified secret contains
           credentials to connect to the ``database`` you specify. When you are
           connecting to a cluster, you also supply the database name, If you
           provide a cluster identifier (``dbClusterIdentifier``), it must match
           the cluster identifier stored in the secret. When you are connecting
           to a serverless workgroup, you also supply the database name.

        -  Temporary credentials - when connecting to your data warehouse,
           choose one of the following options:

           -  When connecting to a serverless workgroup, specify the workgroup
              name and database name. The database user name is derived from the
              IAM identity. For example, ``arn:iam::123456789012:user:foo`` has
              the database user name ``IAM:foo``. Also, permission to call the
              ``redshift-serverless:GetCredentials`` operation is required.

           -  When connecting to a cluster as an IAM identity, specify the
              cluster identifier and the database name. The database user name
              is derived from the IAM identity. For example,
              ``arn:iam::123456789012:user:foo`` has the database user name
              ``IAM:foo``. Also, permission to call the
              ``redshift:GetClusterCredentialsWithIAM`` operation is required.

           -  When connecting to a cluster as a database user, specify the
              cluster identifier, the database name, and the database user name.
              Also, permission to call the ``redshift:GetClusterCredentials``
              operation is required.

        For more information about the Amazon Redshift Data API and CLI usage
        examples, see `Using the Amazon Redshift Data
        API <https://docs.aws.amazon.com/redshift/latest/mgmt/data-api.html>`__
        in the *Amazon Redshift Management Guide*.

        :param sqls: One or more SQL statements to run.
        :param cluster_identifier: The cluster identifier.
        :param secret_arn: The name or ARN of the secret that enables access to the database.
        :param db_user: The database user name.
        :param database: The name of the database.
        :param with_event: A value that indicates whether to send an event to the Amazon
        EventBridge event bus after the SQL statements run.
        :param statement_name: The name of the SQL statements.
        :param workgroup_name: The serverless workgroup name or Amazon Resource Name (ARN).
        :param client_token: A unique, case-sensitive identifier that you provide to ensure the
        idempotency of the request.
        :param result_format: The data format of the result of the SQL statement.
        :param session_keep_alive_seconds: The number of seconds to keep the session alive after the query
        finishes.
        :param session_id: The session identifier of the query.
        :returns: BatchExecuteStatementOutput
        :raises ValidationException:
        :raises ActiveSessionsExceededException:
        :raises ResourceNotFoundException:
        :raises ActiveStatementsExceededException:
        :raises BatchExecuteStatementException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("CancelStatement")
    def cancel_statement(
        self, context: RequestContext, id: UUID, **kwargs
    ) -> CancelStatementResponse:
        """Cancels a running query. To be canceled, a query must be running.

        For more information about the Amazon Redshift Data API and CLI usage
        examples, see `Using the Amazon Redshift Data
        API <https://docs.aws.amazon.com/redshift/latest/mgmt/data-api.html>`__
        in the *Amazon Redshift Management Guide*.

        :param id: The identifier of the SQL statement to cancel.
        :returns: CancelStatementResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises QueryTimeoutException:
        :raises InternalServerException:
        :raises DatabaseConnectionException:
        """
        raise NotImplementedError

    @handler("DescribeStatement")
    def describe_statement(
        self, context: RequestContext, id: UUID, **kwargs
    ) -> DescribeStatementResponse:
        """Describes the details about a specific instance when a query was run by
        the Amazon Redshift Data API. The information includes when the query
        started, when it finished, the query status, the number of rows
        returned, and the SQL statement.

        For more information about the Amazon Redshift Data API and CLI usage
        examples, see `Using the Amazon Redshift Data
        API <https://docs.aws.amazon.com/redshift/latest/mgmt/data-api.html>`__
        in the *Amazon Redshift Management Guide*.

        :param id: The identifier of the SQL statement to describe.
        :returns: DescribeStatementResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("DescribeTable")
    def describe_table(
        self,
        context: RequestContext,
        database: String,
        cluster_identifier: ClusterIdentifierString | None = None,
        secret_arn: SecretArn | None = None,
        db_user: String | None = None,
        connected_database: String | None = None,
        schema: String | None = None,
        table: String | None = None,
        next_token: String | None = None,
        max_results: PageSize | None = None,
        workgroup_name: WorkgroupNameString | None = None,
        **kwargs,
    ) -> DescribeTableResponse:
        """Describes the detailed information about a table from metadata in the
        cluster. The information includes its columns. A token is returned to
        page through the column list. Depending on the authorization method, use
        one of the following combinations of request parameters:

        -  Secrets Manager - when connecting to a cluster, provide the
           ``secret-arn`` of a secret stored in Secrets Manager which has
           ``username`` and ``password``. The specified secret contains
           credentials to connect to the ``database`` you specify. When you are
           connecting to a cluster, you also supply the database name, If you
           provide a cluster identifier (``dbClusterIdentifier``), it must match
           the cluster identifier stored in the secret. When you are connecting
           to a serverless workgroup, you also supply the database name.

        -  Temporary credentials - when connecting to your data warehouse,
           choose one of the following options:

           -  When connecting to a serverless workgroup, specify the workgroup
              name and database name. The database user name is derived from the
              IAM identity. For example, ``arn:iam::123456789012:user:foo`` has
              the database user name ``IAM:foo``. Also, permission to call the
              ``redshift-serverless:GetCredentials`` operation is required.

           -  When connecting to a cluster as an IAM identity, specify the
              cluster identifier and the database name. The database user name
              is derived from the IAM identity. For example,
              ``arn:iam::123456789012:user:foo`` has the database user name
              ``IAM:foo``. Also, permission to call the
              ``redshift:GetClusterCredentialsWithIAM`` operation is required.

           -  When connecting to a cluster as a database user, specify the
              cluster identifier, the database name, and the database user name.
              Also, permission to call the ``redshift:GetClusterCredentials``
              operation is required.

        For more information about the Amazon Redshift Data API and CLI usage
        examples, see `Using the Amazon Redshift Data
        API <https://docs.aws.amazon.com/redshift/latest/mgmt/data-api.html>`__
        in the *Amazon Redshift Management Guide*.

        :param database: The name of the database that contains the tables to be described.
        :param cluster_identifier: The cluster identifier.
        :param secret_arn: The name or ARN of the secret that enables access to the database.
        :param db_user: The database user name.
        :param connected_database: A database name.
        :param schema: The schema that contains the table.
        :param table: The table name.
        :param next_token: A value that indicates the starting point for the next set of response
        records in a subsequent request.
        :param max_results: The maximum number of tables to return in the response.
        :param workgroup_name: The serverless workgroup name or Amazon Resource Name (ARN).
        :returns: DescribeTableResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises QueryTimeoutException:
        :raises InternalServerException:
        :raises DatabaseConnectionException:
        """
        raise NotImplementedError

    @handler("ExecuteStatement")
    def execute_statement(
        self,
        context: RequestContext,
        sql: StatementString,
        cluster_identifier: ClusterIdentifierString | None = None,
        secret_arn: SecretArn | None = None,
        db_user: String | None = None,
        database: String | None = None,
        with_event: Boolean | None = None,
        statement_name: StatementNameString | None = None,
        parameters: SqlParametersList | None = None,
        workgroup_name: WorkgroupNameString | None = None,
        client_token: ClientToken | None = None,
        result_format: ResultFormatString | None = None,
        session_keep_alive_seconds: SessionAliveSeconds | None = None,
        session_id: UUID | None = None,
        **kwargs,
    ) -> ExecuteStatementOutput:
        """Runs an SQL statement, which can be data manipulation language (DML) or
        data definition language (DDL). This statement must be a single SQL
        statement. Depending on the authorization method, use one of the
        following combinations of request parameters:

        -  Secrets Manager - when connecting to a cluster, provide the
           ``secret-arn`` of a secret stored in Secrets Manager which has
           ``username`` and ``password``. The specified secret contains
           credentials to connect to the ``database`` you specify. When you are
           connecting to a cluster, you also supply the database name, If you
           provide a cluster identifier (``dbClusterIdentifier``), it must match
           the cluster identifier stored in the secret. When you are connecting
           to a serverless workgroup, you also supply the database name.

        -  Temporary credentials - when connecting to your data warehouse,
           choose one of the following options:

           -  When connecting to a serverless workgroup, specify the workgroup
              name and database name. The database user name is derived from the
              IAM identity. For example, ``arn:iam::123456789012:user:foo`` has
              the database user name ``IAM:foo``. Also, permission to call the
              ``redshift-serverless:GetCredentials`` operation is required.

           -  When connecting to a cluster as an IAM identity, specify the
              cluster identifier and the database name. The database user name
              is derived from the IAM identity. For example,
              ``arn:iam::123456789012:user:foo`` has the database user name
              ``IAM:foo``. Also, permission to call the
              ``redshift:GetClusterCredentialsWithIAM`` operation is required.

           -  When connecting to a cluster as a database user, specify the
              cluster identifier, the database name, and the database user name.
              Also, permission to call the ``redshift:GetClusterCredentials``
              operation is required.

        For more information about the Amazon Redshift Data API and CLI usage
        examples, see `Using the Amazon Redshift Data
        API <https://docs.aws.amazon.com/redshift/latest/mgmt/data-api.html>`__
        in the *Amazon Redshift Management Guide*.

        :param sql: The SQL statement text to run.
        :param cluster_identifier: The cluster identifier.
        :param secret_arn: The name or ARN of the secret that enables access to the database.
        :param db_user: The database user name.
        :param database: The name of the database.
        :param with_event: A value that indicates whether to send an event to the Amazon
        EventBridge event bus after the SQL statement runs.
        :param statement_name: The name of the SQL statement.
        :param parameters: The parameters for the SQL statement.
        :param workgroup_name: The serverless workgroup name or Amazon Resource Name (ARN).
        :param client_token: A unique, case-sensitive identifier that you provide to ensure the
        idempotency of the request.
        :param result_format: The data format of the result of the SQL statement.
        :param session_keep_alive_seconds: The number of seconds to keep the session alive after the query
        finishes.
        :param session_id: The session identifier of the query.
        :returns: ExecuteStatementOutput
        :raises ValidationException:
        :raises ActiveSessionsExceededException:
        :raises ResourceNotFoundException:
        :raises ExecuteStatementException:
        :raises ActiveStatementsExceededException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("GetStatementResult")
    def get_statement_result(
        self, context: RequestContext, id: UUID, next_token: String | None = None, **kwargs
    ) -> GetStatementResultResponse:
        """Fetches the temporarily cached result of an SQL statement in JSON
        format. The ``ExecuteStatement`` or ``BatchExecuteStatement`` operation
        that ran the SQL statement must have specified ``ResultFormat`` as
        ``JSON`` , or let the format default to JSON. A token is returned to
        page through the statement results.

        For more information about the Amazon Redshift Data API and CLI usage
        examples, see `Using the Amazon Redshift Data
        API <https://docs.aws.amazon.com/redshift/latest/mgmt/data-api.html>`__
        in the *Amazon Redshift Management Guide*.

        :param id: The identifier of the SQL statement whose results are to be fetched.
        :param next_token: A value that indicates the starting point for the next set of response
        records in a subsequent request.
        :returns: GetStatementResultResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("GetStatementResultV2")
    def get_statement_result_v2(
        self, context: RequestContext, id: UUID, next_token: String | None = None, **kwargs
    ) -> GetStatementResultV2Response:
        """Fetches the temporarily cached result of an SQL statement in CSV format.
        The ``ExecuteStatement`` or ``BatchExecuteStatement`` operation that ran
        the SQL statement must have specified ``ResultFormat`` as ``CSV``. A
        token is returned to page through the statement results.

        For more information about the Amazon Redshift Data API and CLI usage
        examples, see `Using the Amazon Redshift Data
        API <https://docs.aws.amazon.com/redshift/latest/mgmt/data-api.html>`__
        in the *Amazon Redshift Management Guide*.

        :param id: The identifier of the SQL statement whose results are to be fetched.
        :param next_token: A value that indicates the starting point for the next set of response
        records in a subsequent request.
        :returns: GetStatementResultV2Response
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("ListDatabases")
    def list_databases(
        self,
        context: RequestContext,
        database: String,
        cluster_identifier: ClusterIdentifierString | None = None,
        secret_arn: SecretArn | None = None,
        db_user: String | None = None,
        next_token: String | None = None,
        max_results: PageSize | None = None,
        workgroup_name: WorkgroupNameString | None = None,
        **kwargs,
    ) -> ListDatabasesResponse:
        """List the databases in a cluster. A token is returned to page through the
        database list. Depending on the authorization method, use one of the
        following combinations of request parameters:

        -  Secrets Manager - when connecting to a cluster, provide the
           ``secret-arn`` of a secret stored in Secrets Manager which has
           ``username`` and ``password``. The specified secret contains
           credentials to connect to the ``database`` you specify. When you are
           connecting to a cluster, you also supply the database name, If you
           provide a cluster identifier (``dbClusterIdentifier``), it must match
           the cluster identifier stored in the secret. When you are connecting
           to a serverless workgroup, you also supply the database name.

        -  Temporary credentials - when connecting to your data warehouse,
           choose one of the following options:

           -  When connecting to a serverless workgroup, specify the workgroup
              name and database name. The database user name is derived from the
              IAM identity. For example, ``arn:iam::123456789012:user:foo`` has
              the database user name ``IAM:foo``. Also, permission to call the
              ``redshift-serverless:GetCredentials`` operation is required.

           -  When connecting to a cluster as an IAM identity, specify the
              cluster identifier and the database name. The database user name
              is derived from the IAM identity. For example,
              ``arn:iam::123456789012:user:foo`` has the database user name
              ``IAM:foo``. Also, permission to call the
              ``redshift:GetClusterCredentialsWithIAM`` operation is required.

           -  When connecting to a cluster as a database user, specify the
              cluster identifier, the database name, and the database user name.
              Also, permission to call the ``redshift:GetClusterCredentials``
              operation is required.

        For more information about the Amazon Redshift Data API and CLI usage
        examples, see `Using the Amazon Redshift Data
        API <https://docs.aws.amazon.com/redshift/latest/mgmt/data-api.html>`__
        in the *Amazon Redshift Management Guide*.

        :param database: The name of the database.
        :param cluster_identifier: The cluster identifier.
        :param secret_arn: The name or ARN of the secret that enables access to the database.
        :param db_user: The database user name.
        :param next_token: A value that indicates the starting point for the next set of response
        records in a subsequent request.
        :param max_results: The maximum number of databases to return in the response.
        :param workgroup_name: The serverless workgroup name or Amazon Resource Name (ARN).
        :returns: ListDatabasesResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises QueryTimeoutException:
        :raises InternalServerException:
        :raises DatabaseConnectionException:
        """
        raise NotImplementedError

    @handler("ListSchemas")
    def list_schemas(
        self,
        context: RequestContext,
        database: String,
        cluster_identifier: ClusterIdentifierString | None = None,
        secret_arn: SecretArn | None = None,
        db_user: String | None = None,
        connected_database: String | None = None,
        schema_pattern: String | None = None,
        next_token: String | None = None,
        max_results: PageSize | None = None,
        workgroup_name: WorkgroupNameString | None = None,
        **kwargs,
    ) -> ListSchemasResponse:
        """Lists the schemas in a database. A token is returned to page through the
        schema list. Depending on the authorization method, use one of the
        following combinations of request parameters:

        -  Secrets Manager - when connecting to a cluster, provide the
           ``secret-arn`` of a secret stored in Secrets Manager which has
           ``username`` and ``password``. The specified secret contains
           credentials to connect to the ``database`` you specify. When you are
           connecting to a cluster, you also supply the database name, If you
           provide a cluster identifier (``dbClusterIdentifier``), it must match
           the cluster identifier stored in the secret. When you are connecting
           to a serverless workgroup, you also supply the database name.

        -  Temporary credentials - when connecting to your data warehouse,
           choose one of the following options:

           -  When connecting to a serverless workgroup, specify the workgroup
              name and database name. The database user name is derived from the
              IAM identity. For example, ``arn:iam::123456789012:user:foo`` has
              the database user name ``IAM:foo``. Also, permission to call the
              ``redshift-serverless:GetCredentials`` operation is required.

           -  When connecting to a cluster as an IAM identity, specify the
              cluster identifier and the database name. The database user name
              is derived from the IAM identity. For example,
              ``arn:iam::123456789012:user:foo`` has the database user name
              ``IAM:foo``. Also, permission to call the
              ``redshift:GetClusterCredentialsWithIAM`` operation is required.

           -  When connecting to a cluster as a database user, specify the
              cluster identifier, the database name, and the database user name.
              Also, permission to call the ``redshift:GetClusterCredentials``
              operation is required.

        For more information about the Amazon Redshift Data API and CLI usage
        examples, see `Using the Amazon Redshift Data
        API <https://docs.aws.amazon.com/redshift/latest/mgmt/data-api.html>`__
        in the *Amazon Redshift Management Guide*.

        :param database: The name of the database that contains the schemas to list.
        :param cluster_identifier: The cluster identifier.
        :param secret_arn: The name or ARN of the secret that enables access to the database.
        :param db_user: The database user name.
        :param connected_database: A database name.
        :param schema_pattern: A pattern to filter results by schema name.
        :param next_token: A value that indicates the starting point for the next set of response
        records in a subsequent request.
        :param max_results: The maximum number of schemas to return in the response.
        :param workgroup_name: The serverless workgroup name or Amazon Resource Name (ARN).
        :returns: ListSchemasResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises QueryTimeoutException:
        :raises InternalServerException:
        :raises DatabaseConnectionException:
        """
        raise NotImplementedError

    @handler("ListStatements")
    def list_statements(
        self,
        context: RequestContext,
        next_token: String | None = None,
        max_results: ListStatementsLimit | None = None,
        statement_name: StatementNameString | None = None,
        status: StatusString | None = None,
        role_level: Boolean | None = None,
        database: String | None = None,
        cluster_identifier: ClusterIdentifierString | None = None,
        workgroup_name: WorkgroupNameString | None = None,
        **kwargs,
    ) -> ListStatementsResponse:
        """List of SQL statements. By default, only finished statements are shown.
        A token is returned to page through the statement list.

        When you use identity-enhanced role sessions to list statements, you
        must provide either the ``cluster-identifier`` or ``workgroup-name``
        parameter. This ensures that the IdC user can only access the Amazon
        Redshift IdC applications they are assigned. For more information, see
        `Trusted identity propagation
        overview <https://docs.aws.amazon.com/singlesignon/latest/userguide/trustedidentitypropagation-overview.html>`__.

        For more information about the Amazon Redshift Data API and CLI usage
        examples, see `Using the Amazon Redshift Data
        API <https://docs.aws.amazon.com/redshift/latest/mgmt/data-api.html>`__
        in the *Amazon Redshift Management Guide*.

        :param next_token: A value that indicates the starting point for the next set of response
        records in a subsequent request.
        :param max_results: The maximum number of SQL statements to return in the response.
        :param statement_name: The name of the SQL statement specified as input to
        ``BatchExecuteStatement`` or ``ExecuteStatement`` to identify the query.
        :param status: The status of the SQL statement to list.
        :param role_level: A value that filters which statements to return in the response.
        :param database: The name of the database when listing statements run against a
        ``ClusterIdentifier`` or ``WorkgroupName``.
        :param cluster_identifier: The cluster identifier.
        :param workgroup_name: The serverless workgroup name or Amazon Resource Name (ARN).
        :returns: ListStatementsResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("ListTables")
    def list_tables(
        self,
        context: RequestContext,
        database: String,
        cluster_identifier: ClusterIdentifierString | None = None,
        secret_arn: SecretArn | None = None,
        db_user: String | None = None,
        connected_database: String | None = None,
        schema_pattern: String | None = None,
        table_pattern: String | None = None,
        next_token: String | None = None,
        max_results: PageSize | None = None,
        workgroup_name: WorkgroupNameString | None = None,
        **kwargs,
    ) -> ListTablesResponse:
        """List the tables in a database. If neither ``SchemaPattern`` nor
        ``TablePattern`` are specified, then all tables in the database are
        returned. A token is returned to page through the table list. Depending
        on the authorization method, use one of the following combinations of
        request parameters:

        -  Secrets Manager - when connecting to a cluster, provide the
           ``secret-arn`` of a secret stored in Secrets Manager which has
           ``username`` and ``password``. The specified secret contains
           credentials to connect to the ``database`` you specify. When you are
           connecting to a cluster, you also supply the database name, If you
           provide a cluster identifier (``dbClusterIdentifier``), it must match
           the cluster identifier stored in the secret. When you are connecting
           to a serverless workgroup, you also supply the database name.

        -  Temporary credentials - when connecting to your data warehouse,
           choose one of the following options:

           -  When connecting to a serverless workgroup, specify the workgroup
              name and database name. The database user name is derived from the
              IAM identity. For example, ``arn:iam::123456789012:user:foo`` has
              the database user name ``IAM:foo``. Also, permission to call the
              ``redshift-serverless:GetCredentials`` operation is required.

           -  When connecting to a cluster as an IAM identity, specify the
              cluster identifier and the database name. The database user name
              is derived from the IAM identity. For example,
              ``arn:iam::123456789012:user:foo`` has the database user name
              ``IAM:foo``. Also, permission to call the
              ``redshift:GetClusterCredentialsWithIAM`` operation is required.

           -  When connecting to a cluster as a database user, specify the
              cluster identifier, the database name, and the database user name.
              Also, permission to call the ``redshift:GetClusterCredentials``
              operation is required.

        For more information about the Amazon Redshift Data API and CLI usage
        examples, see `Using the Amazon Redshift Data
        API <https://docs.aws.amazon.com/redshift/latest/mgmt/data-api.html>`__
        in the *Amazon Redshift Management Guide*.

        :param database: The name of the database that contains the tables to list.
        :param cluster_identifier: The cluster identifier.
        :param secret_arn: The name or ARN of the secret that enables access to the database.
        :param db_user: The database user name.
        :param connected_database: A database name.
        :param schema_pattern: A pattern to filter results by schema name.
        :param table_pattern: A pattern to filter results by table name.
        :param next_token: A value that indicates the starting point for the next set of response
        records in a subsequent request.
        :param max_results: The maximum number of tables to return in the response.
        :param workgroup_name: The serverless workgroup name or Amazon Resource Name (ARN).
        :returns: ListTablesResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises QueryTimeoutException:
        :raises InternalServerException:
        :raises DatabaseConnectionException:
        """
        raise NotImplementedError
