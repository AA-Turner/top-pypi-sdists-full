from enum import StrEnum
from typing import TypedDict

from localstack.aws.api import RequestContext, ServiceException, ServiceRequest, handler

Arn = str
Boolean = bool
BoxedBoolean = bool
BoxedDouble = float
BoxedFloat = float
BoxedInteger = int
DbName = str
ErrorMessage = str
FormattedSqlRecords = str
Id = str
Integer = int
ParameterName = str
SqlStatement = str
String = str
TransactionStatus = str


class DecimalReturnType(StrEnum):
    STRING = "STRING"
    DOUBLE_OR_LONG = "DOUBLE_OR_LONG"


class LongReturnType(StrEnum):
    STRING = "STRING"
    LONG = "LONG"


class RecordsFormatType(StrEnum):
    NONE = "NONE"
    JSON = "JSON"


class TypeHint(StrEnum):
    JSON = "JSON"
    UUID = "UUID"
    TIMESTAMP = "TIMESTAMP"
    DATE = "DATE"
    TIME = "TIME"
    DECIMAL = "DECIMAL"


class AccessDeniedException(ServiceException):
    """You don't have sufficient access to perform this action."""

    code: str = "AccessDeniedException"
    sender_fault: bool = True
    status_code: int = 403


class BadRequestException(ServiceException):
    """There is an error in the call or in a SQL statement. (This error only
    appears in calls from Aurora Serverless v1 databases.)
    """

    code: str = "BadRequestException"
    sender_fault: bool = True
    status_code: int = 400


class DatabaseErrorException(ServiceException):
    """There was an error in processing the SQL statement."""

    code: str = "DatabaseErrorException"
    sender_fault: bool = True
    status_code: int = 400


class DatabaseNotFoundException(ServiceException):
    """The DB cluster doesn't have a DB instance."""

    code: str = "DatabaseNotFoundException"
    sender_fault: bool = True
    status_code: int = 404


class DatabaseResumingException(ServiceException):
    """A request was cancelled because the Aurora Serverless v2 DB instance was
    paused. The Data API request automatically resumes the DB instance. Wait
    a few seconds and try again.
    """

    code: str = "DatabaseResumingException"
    sender_fault: bool = True
    status_code: int = 400


class DatabaseUnavailableException(ServiceException):
    """The writer instance in the DB cluster isn't available."""

    code: str = "DatabaseUnavailableException"
    sender_fault: bool = False
    status_code: int = 504


class ForbiddenException(ServiceException):
    """There are insufficient privileges to make the call."""

    code: str = "ForbiddenException"
    sender_fault: bool = True
    status_code: int = 403


class HttpEndpointNotEnabledException(ServiceException):
    """The HTTP endpoint for using RDS Data API isn't enabled for the DB
    cluster.
    """

    code: str = "HttpEndpointNotEnabledException"
    sender_fault: bool = True
    status_code: int = 400


class InternalServerErrorException(ServiceException):
    """An internal error occurred."""

    code: str = "InternalServerErrorException"
    sender_fault: bool = False
    status_code: int = 500


class InvalidResourceStateException(ServiceException):
    """The resource is in an invalid state."""

    code: str = "InvalidResourceStateException"
    sender_fault: bool = True
    status_code: int = 400


class InvalidSecretException(ServiceException):
    """The Secrets Manager secret used with the request isn't valid."""

    code: str = "InvalidSecretException"
    sender_fault: bool = True
    status_code: int = 400


class NotFoundException(ServiceException):
    """The ``resourceArn``, ``secretArn``, or ``transactionId`` value can't be
    found.
    """

    code: str = "NotFoundException"
    sender_fault: bool = True
    status_code: int = 404


class SecretsErrorException(ServiceException):
    """There was a problem with the Secrets Manager secret used with the
    request, caused by one of the following conditions:

    -  RDS Data API timed out retrieving the secret.

    -  The secret provided wasn't found.

    -  The secret couldn't be decrypted.
    """

    code: str = "SecretsErrorException"
    sender_fault: bool = True
    status_code: int = 400


class ServiceUnavailableError(ServiceException):
    """The service specified by the ``resourceArn`` parameter isn't available."""

    code: str = "ServiceUnavailableError"
    sender_fault: bool = False
    status_code: int = 503


Long = int


class StatementTimeoutException(ServiceException):
    """The execution of the SQL statement timed out."""

    code: str = "StatementTimeoutException"
    sender_fault: bool = True
    status_code: int = 400
    dbConnectionId: Long | None


class TransactionNotFoundException(ServiceException):
    """The transaction ID wasn't found."""

    code: str = "TransactionNotFoundException"
    sender_fault: bool = True
    status_code: int = 404


class UnsupportedResultException(ServiceException):
    """There was a problem with the result because of one of the following
    conditions:

    -  It contained an unsupported data type.

    -  It contained a multidimensional array.

    -  The size was too large.
    """

    code: str = "UnsupportedResultException"
    sender_fault: bool = True
    status_code: int = 400


ArrayOfArray = list["ArrayValue"]
StringArray = list[String]
DoubleArray = list[BoxedDouble]
BoxedLong = int
LongArray = list[BoxedLong]
BooleanArray = list[BoxedBoolean]


class ArrayValue(TypedDict, total=False):
    """Contains an array."""

    booleanValues: BooleanArray | None
    longValues: LongArray | None
    doubleValues: DoubleArray | None
    stringValues: StringArray | None
    arrayValues: ArrayOfArray | None


ArrayValueList = list["Value"]


class StructValue(TypedDict, total=False):
    """A structure value returned by a call.

    This data structure is only used with the deprecated ``ExecuteSql``
    operation. Use the ``BatchExecuteStatement`` or ``ExecuteStatement``
    operation instead.
    """

    attributes: ArrayValueList | None


Blob = bytes


class Value(TypedDict, total=False):
    """Contains the value of a column.

    This data structure is only used with the deprecated ``ExecuteSql``
    operation. Use the ``BatchExecuteStatement`` or ``ExecuteStatement``
    operation instead.
    """

    isNull: BoxedBoolean | None
    bitValue: BoxedBoolean | None
    bigIntValue: BoxedLong | None
    intValue: BoxedInteger | None
    doubleValue: BoxedDouble | None
    realValue: BoxedFloat | None
    stringValue: String | None
    blobValue: Blob | None
    arrayValues: ArrayValueList | None
    structValue: StructValue | None


class Field(TypedDict, total=False):
    """Contains a value."""

    isNull: BoxedBoolean | None
    booleanValue: BoxedBoolean | None
    longValue: BoxedLong | None
    doubleValue: BoxedDouble | None
    stringValue: String | None
    blobValue: Blob | None
    arrayValue: ArrayValue | None


class SqlParameter(TypedDict, total=False):
    """A parameter used in a SQL statement."""

    name: ParameterName | None
    value: Field | None
    typeHint: TypeHint | None


SqlParametersList = list[SqlParameter]
SqlParameterSets = list[SqlParametersList]


class BatchExecuteStatementRequest(ServiceRequest):
    """The request parameters represent the input of a SQL statement over an
    array of data.
    """

    resourceArn: Arn
    secretArn: Arn
    sql: SqlStatement
    database: DbName | None
    schema: DbName | None
    parameterSets: SqlParameterSets | None
    transactionId: Id | None


FieldList = list[Field]


class UpdateResult(TypedDict, total=False):
    """The response elements represent the results of an update."""

    generatedFields: FieldList | None


UpdateResults = list[UpdateResult]


class BatchExecuteStatementResponse(TypedDict, total=False):
    """The response elements represent the output of a SQL statement over an
    array of data.
    """

    updateResults: UpdateResults | None


class BeginTransactionRequest(ServiceRequest):
    """The request parameters represent the input of a request to start a SQL
    transaction.
    """

    resourceArn: Arn
    secretArn: Arn
    database: DbName | None
    schema: DbName | None


class BeginTransactionResponse(TypedDict, total=False):
    """The response elements represent the output of a request to start a SQL
    transaction.
    """

    transactionId: Id | None


class ColumnMetadata(TypedDict, total=False):
    name: String | None
    type: Integer | None
    typeName: String | None
    label: String | None
    schemaName: String | None
    tableName: String | None
    isAutoIncrement: Boolean | None
    isSigned: Boolean | None
    isCurrency: Boolean | None
    isCaseSensitive: Boolean | None
    nullable: Integer | None
    precision: Integer | None
    scale: Integer | None
    arrayBaseColumnType: Integer | None


class CommitTransactionRequest(ServiceRequest):
    """The request parameters represent the input of a commit transaction
    request.
    """

    resourceArn: Arn
    secretArn: Arn
    transactionId: Id


class CommitTransactionResponse(TypedDict, total=False):
    """The response elements represent the output of a commit transaction
    request.
    """

    transactionStatus: TransactionStatus | None


class ExecuteSqlRequest(ServiceRequest):
    """The request parameters represent the input of a request to run one or
    more SQL statements.
    """

    dbClusterOrInstanceArn: Arn
    awsSecretStoreArn: Arn
    sqlStatements: SqlStatement
    database: DbName | None
    schema: DbName | None


RecordsUpdated = int
Row = list[Value]


class Record(TypedDict, total=False):
    """A record returned by a call.

    This data structure is only used with the deprecated ``ExecuteSql``
    operation. Use the ``BatchExecuteStatement`` or ``ExecuteStatement``
    operation instead.
    """

    values: Row | None


Records = list[Record]
Metadata = list[ColumnMetadata]


class ResultSetMetadata(TypedDict, total=False):
    """The metadata of the result set returned by a SQL statement."""

    columnCount: Long | None
    columnMetadata: Metadata | None


class ResultFrame(TypedDict, total=False):
    """The result set returned by a SQL statement.

    This data structure is only used with the deprecated ``ExecuteSql``
    operation. Use the ``BatchExecuteStatement`` or ``ExecuteStatement``
    operation instead.
    """

    resultSetMetadata: ResultSetMetadata | None
    records: Records | None


class SqlStatementResult(TypedDict, total=False):
    """The result of a SQL statement.

    This data structure is only used with the deprecated ``ExecuteSql``
    operation. Use the ``BatchExecuteStatement`` or ``ExecuteStatement``
    operation instead.
    """

    resultFrame: ResultFrame | None
    numberOfRecordsUpdated: RecordsUpdated | None


SqlStatementResults = list[SqlStatementResult]


class ExecuteSqlResponse(TypedDict, total=False):
    """The response elements represent the output of a request to run one or
    more SQL statements.
    """

    sqlStatementResults: SqlStatementResults | None


class ResultSetOptions(TypedDict, total=False):
    """Options that control how the result set is returned."""

    decimalReturnType: DecimalReturnType | None
    longReturnType: LongReturnType | None


class ExecuteStatementRequest(ServiceRequest):
    """The request parameters represent the input of a request to run a SQL
    statement against a database.
    """

    resourceArn: Arn
    secretArn: Arn
    sql: SqlStatement
    database: DbName | None
    schema: DbName | None
    parameters: SqlParametersList | None
    transactionId: Id | None
    includeResultMetadata: Boolean | None
    continueAfterTimeout: Boolean | None
    resultSetOptions: ResultSetOptions | None
    formatRecordsAs: RecordsFormatType | None


SqlRecords = list[FieldList]


class ExecuteStatementResponse(TypedDict, total=False):
    """The response elements represent the output of a request to run a SQL
    statement against a database.
    """

    records: SqlRecords | None
    columnMetadata: Metadata | None
    numberOfRecordsUpdated: RecordsUpdated | None
    generatedFields: FieldList | None
    formattedRecords: FormattedSqlRecords | None


class RollbackTransactionRequest(ServiceRequest):
    """The request parameters represent the input of a request to perform a
    rollback of a transaction.
    """

    resourceArn: Arn
    secretArn: Arn
    transactionId: Id


class RollbackTransactionResponse(TypedDict, total=False):
    """The response elements represent the output of a request to perform a
    rollback of a transaction.
    """

    transactionStatus: TransactionStatus | None


class RdsDataApi:
    service: str = "rds-data"
    version: str = "2018-08-01"

    @handler("BatchExecuteStatement")
    def batch_execute_statement(
        self,
        context: RequestContext,
        resource_arn: Arn,
        secret_arn: Arn,
        sql: SqlStatement,
        database: DbName | None = None,
        schema: DbName | None = None,
        parameter_sets: SqlParameterSets | None = None,
        transaction_id: Id | None = None,
        **kwargs,
    ) -> BatchExecuteStatementResponse:
        """Runs a batch SQL statement over an array of data.

        You can run bulk update and insert operations for multiple records using
        a DML statement with different parameter sets. Bulk operations can
        provide a significant performance improvement over individual insert and
        update operations.

        If a call isn't part of a transaction because it doesn't include the
        ``transactionID`` parameter, changes that result from the call are
        committed automatically.

        There isn't a fixed upper limit on the number of parameter sets.
        However, the maximum size of the HTTP request submitted through the Data
        API is 4 MiB. If the request exceeds this limit, the Data API returns an
        error and doesn't process the request. This 4-MiB limit includes the
        size of the HTTP headers and the JSON notation in the request. Thus, the
        number of parameter sets that you can include depends on a combination
        of factors, such as the size of the SQL statement and the size of each
        parameter set.

        The response size limit is 1 MiB. If the call returns more than 1 MiB of
        response data, the call is terminated.

        :param resource_arn: The Amazon Resource Name (ARN) of the Aurora Serverless DB cluster.
        :param secret_arn: The ARN of the secret that enables access to the DB cluster.
        :param sql: The SQL statement to run.
        :param database: The name of the database.
        :param schema: The name of the database schema.
        :param parameter_sets: The parameter set for the batch operation.
        :param transaction_id: The identifier of a transaction that was started by using the
        ``BeginTransaction`` operation.
        :returns: BatchExecuteStatementResponse
        :raises SecretsErrorException:
        :raises HttpEndpointNotEnabledException:
        :raises DatabaseErrorException:
        :raises DatabaseResumingException:
        :raises DatabaseUnavailableException:
        :raises TransactionNotFoundException:
        :raises InvalidSecretException:
        :raises InvalidResourceStateException:
        :raises ServiceUnavailableError:
        :raises ForbiddenException:
        :raises DatabaseNotFoundException:
        :raises AccessDeniedException:
        :raises BadRequestException:
        :raises StatementTimeoutException:
        :raises InternalServerErrorException:
        """
        raise NotImplementedError

    @handler("BeginTransaction")
    def begin_transaction(
        self,
        context: RequestContext,
        resource_arn: Arn,
        secret_arn: Arn,
        database: DbName | None = None,
        schema: DbName | None = None,
        **kwargs,
    ) -> BeginTransactionResponse:
        """Starts a SQL transaction.

        A transaction can run for a maximum of 24 hours. A transaction is
        terminated and rolled back automatically after 24 hours.

        A transaction times out if no calls use its transaction ID in three
        minutes. If a transaction times out before it's committed, it's rolled
        back automatically.

        For Aurora MySQL, DDL statements inside a transaction cause an implicit
        commit. We recommend that you run each MySQL DDL statement in a separate
        ``ExecuteStatement`` call with ``continueAfterTimeout`` enabled.

        :param resource_arn: The Amazon Resource Name (ARN) of the Aurora Serverless DB cluster.
        :param secret_arn: The name or ARN of the secret that enables access to the DB cluster.
        :param database: The name of the database.
        :param schema: The name of the database schema.
        :returns: BeginTransactionResponse
        :raises SecretsErrorException:
        :raises HttpEndpointNotEnabledException:
        :raises DatabaseErrorException:
        :raises DatabaseResumingException:
        :raises DatabaseUnavailableException:
        :raises TransactionNotFoundException:
        :raises InvalidSecretException:
        :raises InvalidResourceStateException:
        :raises ServiceUnavailableError:
        :raises ForbiddenException:
        :raises DatabaseNotFoundException:
        :raises AccessDeniedException:
        :raises BadRequestException:
        :raises StatementTimeoutException:
        :raises InternalServerErrorException:
        """
        raise NotImplementedError

    @handler("CommitTransaction")
    def commit_transaction(
        self,
        context: RequestContext,
        resource_arn: Arn,
        secret_arn: Arn,
        transaction_id: Id,
        **kwargs,
    ) -> CommitTransactionResponse:
        """Ends a SQL transaction started with the ``BeginTransaction`` operation
        and commits the changes.

        :param resource_arn: The Amazon Resource Name (ARN) of the Aurora Serverless DB cluster.
        :param secret_arn: The name or ARN of the secret that enables access to the DB cluster.
        :param transaction_id: The identifier of the transaction to end and commit.
        :returns: CommitTransactionResponse
        :raises SecretsErrorException:
        :raises HttpEndpointNotEnabledException:
        :raises DatabaseErrorException:
        :raises DatabaseUnavailableException:
        :raises TransactionNotFoundException:
        :raises InvalidSecretException:
        :raises InvalidResourceStateException:
        :raises ServiceUnavailableError:
        :raises ForbiddenException:
        :raises DatabaseNotFoundException:
        :raises AccessDeniedException:
        :raises BadRequestException:
        :raises StatementTimeoutException:
        :raises InternalServerErrorException:
        :raises NotFoundException:
        """
        raise NotImplementedError

    @handler("ExecuteSql")
    def execute_sql(
        self,
        context: RequestContext,
        db_cluster_or_instance_arn: Arn,
        aws_secret_store_arn: Arn,
        sql_statements: SqlStatement,
        database: DbName | None = None,
        schema: DbName | None = None,
        **kwargs,
    ) -> ExecuteSqlResponse:
        """Runs one or more SQL statements.

        This operation isn't supported for Aurora Serverless v2 and provisioned
        DB clusters. For Aurora Serverless v1 DB clusters, the operation is
        deprecated. Use the ``BatchExecuteStatement`` or ``ExecuteStatement``
        operation.

        :param db_cluster_or_instance_arn: The ARN of the Aurora Serverless DB cluster.
        :param aws_secret_store_arn: The Amazon Resource Name (ARN) of the secret that enables access to the
        DB cluster.
        :param sql_statements: One or more SQL statements to run on the DB cluster.
        :param database: The name of the database.
        :param schema: The name of the database schema.
        :returns: ExecuteSqlResponse
        :raises AccessDeniedException:
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises ServiceUnavailableError:
        """
        raise NotImplementedError

    @handler("ExecuteStatement")
    def execute_statement(
        self,
        context: RequestContext,
        resource_arn: Arn,
        secret_arn: Arn,
        sql: SqlStatement,
        database: DbName | None = None,
        schema: DbName | None = None,
        parameters: SqlParametersList | None = None,
        transaction_id: Id | None = None,
        include_result_metadata: Boolean | None = None,
        continue_after_timeout: Boolean | None = None,
        result_set_options: ResultSetOptions | None = None,
        format_records_as: RecordsFormatType | None = None,
        **kwargs,
    ) -> ExecuteStatementResponse:
        """Runs a SQL statement against a database.

        If a call isn't part of a transaction because it doesn't include the
        ``transactionID`` parameter, changes that result from the call are
        committed automatically.

        If the binary response data from the database is more than 1 MB, the
        call is terminated.

        :param resource_arn: The Amazon Resource Name (ARN) of the Aurora Serverless DB cluster.
        :param secret_arn: The ARN of the secret that enables access to the DB cluster.
        :param sql: The SQL statement to run.
        :param database: The name of the database.
        :param schema: The name of the database schema.
        :param parameters: The parameters for the SQL statement.
        :param transaction_id: The identifier of a transaction that was started by using the
        ``BeginTransaction`` operation.
        :param include_result_metadata: A value that indicates whether to include metadata in the results.
        :param continue_after_timeout: A value that indicates whether to continue running the statement after
        the call times out.
        :param result_set_options: Options that control how the result set is returned.
        :param format_records_as: A value that indicates whether to format the result set as a single JSON
        string.
        :returns: ExecuteStatementResponse
        :raises SecretsErrorException:
        :raises HttpEndpointNotEnabledException:
        :raises DatabaseErrorException:
        :raises DatabaseResumingException:
        :raises DatabaseUnavailableException:
        :raises TransactionNotFoundException:
        :raises InvalidSecretException:
        :raises InvalidResourceStateException:
        :raises ServiceUnavailableError:
        :raises ForbiddenException:
        :raises DatabaseNotFoundException:
        :raises AccessDeniedException:
        :raises BadRequestException:
        :raises StatementTimeoutException:
        :raises InternalServerErrorException:
        :raises UnsupportedResultException:
        """
        raise NotImplementedError

    @handler("RollbackTransaction")
    def rollback_transaction(
        self,
        context: RequestContext,
        resource_arn: Arn,
        secret_arn: Arn,
        transaction_id: Id,
        **kwargs,
    ) -> RollbackTransactionResponse:
        """Performs a rollback of a transaction. Rolling back a transaction cancels
        its changes.

        :param resource_arn: The Amazon Resource Name (ARN) of the Aurora Serverless DB cluster.
        :param secret_arn: The name or ARN of the secret that enables access to the DB cluster.
        :param transaction_id: The identifier of the transaction to roll back.
        :returns: RollbackTransactionResponse
        :raises SecretsErrorException:
        :raises HttpEndpointNotEnabledException:
        :raises DatabaseErrorException:
        :raises DatabaseUnavailableException:
        :raises TransactionNotFoundException:
        :raises InvalidSecretException:
        :raises InvalidResourceStateException:
        :raises ServiceUnavailableError:
        :raises ForbiddenException:
        :raises DatabaseNotFoundException:
        :raises AccessDeniedException:
        :raises BadRequestException:
        :raises StatementTimeoutException:
        :raises InternalServerErrorException:
        :raises NotFoundException:
        """
        raise NotImplementedError
