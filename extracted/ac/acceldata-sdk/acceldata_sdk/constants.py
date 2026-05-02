from enum import Enum, IntEnum, auto
from dataclasses import dataclass


class RuleExecutionStatus(Enum):
    STARTED = 1
    RUNNING = 2
    ERRORED = 3
    WARNING = 4
    SUCCESSFUL = 5
    ABORTED = 6
    WAITING = 7


class FailureStrategy(IntEnum):
    DoNotFail = auto()
    FailOnError = auto()
    FailOnWarning = auto()


class PolicyType(Enum):
    DATA_QUALITY = 'DATA-QUALITY'
    RECONCILIATION = 'RECONCILIATION'
    DATA_CADENCE = 'DATA_CADENCE'


class AssetSourceType(Enum):
    BIGQUERY = 'BIGQUERY'
    REDSHIFT = 'REDSHIFT'
    SNOWFLAKE = 'SNOWFLAKE'
    TERADATA = 'TERADATA'
    HIVE = 'HIVE'
    HBASE = 'HBASE'
    AZURE_MSSQL = 'AZURE_MSSQL'
    AZURE_DATALAKE = 'AZURE_DATALAKE'
    AWS_GLUE = 'AWS_GLUE'
    AWS_S3 = 'AWS_S3'
    HDFS = 'HDFS'
    GCS = 'GCS'
    KAFKA = 'KAFKA'
    MYSQL = 'MYSQL'
    MEMSQL = 'MEMSQL'
    POSTGRESQL = 'POSTGRESQL'
    TABLEAU = 'TABLEAU'
    ORACL = 'ORACLE'
    AWS_ATHENA = 'AWS_ATHENA'
    DATABRICKS = 'DATABRICKS'
    MONGO = 'MONGO'
    MODEL_BAG = 'MODEL_BAG'
    FEATURE_BAG = 'FEATURE_BAG'
    PRESTO = 'PRESTO'
    DB2 = 'DB2'
    CLICKHOUSE = 'CLICKHOUSE'
    VIRTUAL_DATASOURCE = 'VIRTUAL_DATASOURCE'


DATA_QUALITY = 'DATA_QUALITY'
RECONCILIATION = 'RECONCILIATION'

# MIN_TORCH_BACKEND_VERSION_SUPPORTED is the minimum torch backend version supported by SDK.

MIN_TORCH_BACKEND_VERSION_SUPPORTED = '2.2.0'

# minimum torch backend version supported for the api /api/rules/{identifier}
MIN_TORCH_BACKEND_VERSION_FOR_RULE_ID_API = '2.12.0'

#connection timeout
TORCH_CONNECTION_TIMEOUT_MS = 5000

#read timeout
TORCH_READ_TIMEOUT_MS = 15000

@dataclass
class TorchBuildVersion:
    buildVersion = None
    buildDate = None

    def __init__(self, buildVersion=None, buildDate=None, *args, **kwargs):
        self.buildVersion = buildVersion
        self.buildDate = buildDate

    def __repr__(self):
        return f"TorchBuildVersion({self.__dict__})"


@dataclass
class SdkSupportedVersions:
    maxVersion = None
    minVersion = None

    def __init__(self, maxVersion=None, minVersion=None, *args, **kwargs):
        self.maxVersion = maxVersion
        self.minVersion = minVersion

    def __repr__(self):
        return f"SdkSupportedVersions({self.__dict__})"