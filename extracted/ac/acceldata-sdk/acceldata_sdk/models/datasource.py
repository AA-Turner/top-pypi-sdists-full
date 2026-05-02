from dataclasses import dataclass
from typing import List, Dict
from enum import Enum, auto

from acceldata_sdk.models.connection import Connection


@dataclass
class ConfigProperty:
    key = None
    value = None

    def __init__(self,
                 key=None,
                 value=None, *args, **kwargs):
        self.key = key
        self.value = value


@dataclass
class Crawler:
    name = None

    def __init__(self, name=None, *args, **kwargs):
        self.name = name

    def __repr__(self):
        return f"Crawler({self.__dict__})"


@dataclass
class DatasourceType:
    id = None
    name = None

    def __init__(self,
                 id=None,
                 name=None, *args, **kwargs):
        self.name = name
        self.id = id


@dataclass
class DatasourceSourceModel:
    id = None
    name = None

    def __init__(self,
                 id=None,
                 name=None, *args, **kwargs):
        self.name = name
        self.id = id


@dataclass
class DatasourceSourceType:

    def __init__(self, id, name, sourceModel=None, connectionTypeId=None, *args, **kwargs):
        """
            Description:
                Datasource source type
        :param id: id of the source type
        :param name: name of the source type
        :param sourceModel: source model
        :param connectionTypeId: (int) connection type id for the given source type
        """
        self.id = id
        self.name = name
        self.connectionTypeId = connectionTypeId
        if isinstance(sourceModel, dict):
            self.sourceModel = DatasourceSourceModel(**sourceModel)
        else:
            self.sourceModel = sourceModel

    def __repr__(self):
        return f"DatasourceSourceType({self.__dict__})"

class PropertyType(Enum):
    INT = auto()
    FLOAT = auto()
    STRING = auto()
    BOOLEAN = auto()
    JSON = auto()
    DURATION = auto()
    OBJECT = auto()
    OPTIONS = auto()
    URL = auto()
    URI = auto()
    PASSWORD = auto()
    EMAIL = auto()
    CRONEXPRESSION = auto()
    FILE = auto()
    ARRAY = auto()

    class SubPropertyType(Enum):
        STRING = auto()
        INT = auto()
        FLOAT = auto()
        BOOLEAN = auto()


class OptionTypes(Enum):

    CSV = auto()
    PARQUET = auto()
    ORC = auto()
    JSON = auto()
    AVRO = auto()
    CONFLUENT_AVRO = auto()

    PLAINTEXT = auto()
    SASL_PLAINTEXT = auto()
    SASL_SSL = auto()
    SSL = auto()
    BASIC_AUTH = auto()

    STANDALONE = auto()
    ORACLE_CLOUD_AUTONOMOUS_DB = auto()

    # Postgresql Environments
    ON_PREMISE = auto()
    AMAZON_RDS = auto()

    # Analysis Service Data Processor types
    HADOOP = auto()
    KUBERNETES = auto()
    DATABRICKS = auto()

    # Kafka Schema Naming Strategies
    TOPIC_NAME = auto()
    RECORD_NAME = auto()
    TOPIC_RECORD_NAME = auto()
    KEY = auto()
    VALUE = auto()

    # Torch Result Location Types
    HDFS = auto()
    S3 = auto()


@dataclass
class PropertyTemplate:
    key: str = None
    description: str = None
    displayLabel: str = None
    type: PropertyType = None
    options: List[OptionTypes] = None
    subType: PropertyType.SubPropertyType = None
    required: bool = None
    children: object = None
    visibility: str = None
    value: str = None
    replacementFor: str = None
    hidden: bool = None
    readOnly: bool = None
    configKey: str = None
    configValue: str = None
    multiSelect: bool = None


@dataclass
class PropertyTemplates:
    connections: Dict[str, List[PropertyTemplate]] = None
    assemblies: Dict[str, List[PropertyTemplate]] = None


@dataclass
class SourceModel:
    id = None,
    name = None

    def __init__(self,
                 id=None,
                 name=None, *args, **kwargs):
        self.name = name
        self.id = id


@dataclass
class SourceType:
    id: str = None
    name: str = None
    sourceModel: SourceModel = None
    connectionTypeId: str = None
    miniProfiling: bool = None
    propertyTemplates: PropertyTemplates = None


@dataclass
class SecurityConfig:
    type = None
    config = None

    def __init__(self,
                 type=None,
                 config=None, *args, **kwargs):
        self.type = type
        self.config = config


class DataSource:

    def __init__(self,
                 name: str = None,
                 isSecured: bool = None,
                 isVirtual: bool = None,
                 id: int = None,
                 createdAt: str = None,
                 updatedAt: str = None,
                 assemblyProperties = None,
                 conn: Connection = None,
                 connectionId: int = None,
                 crawler: Crawler = None,
                 currentSnapshot: str = None,
                 description: str = None,
                 sourceType: SourceType = None,
                 securityConfig: SecurityConfig = None,
                 schedule: str = None,
                 configuration=None,
                 client=None,
                 autoProfile: bool = None,
                 tenantId: str = None,
                 integrationId: str = None,
                 subIntegrationId: str = None,
                 isProtectedResource: bool = None,
                 createdBy: str = None,
                 *args, **kwargs
                 ):
        """
            Description:
                datasource class.
        :param name: name of the datasource
        :param isSecured: is secured or not
        :param isVirtual: is virtual datasource or not
        :param id: id of the datasource
        :param createdAt: creation time of the datasource
        :param updatedAt: updated time of the datasource
        :param assemblyProperties: datasource properties
        :param conn: connection details for the ds
        :param connectionId: connection id of the datasource
        :param crawler: crawler details of the datasource
        :param currentSnapshot: current version of the datasource
        :param description: desc of the datasource
        :param sourceType: (DatasourceSourceModel) source type details
        :param securityConfig: security configuration for the given ds
        :param schedule: scheduled exp
        :param configuration: configurations
        """
        self.name = name
        self.isSecured = isSecured
        self.isVirtual = isVirtual
        self.id = id
        self.createdAt = createdAt
        self.updatedAt = updatedAt
        self.assemblyProperties = assemblyProperties
        if isinstance(conn, dict):
            self.conn = Connection(**conn)
        else:
            self.conn = conn
        self.connectionId = connectionId
        if isinstance(crawler, dict):
            self.crawler = Crawler(**crawler)
        else:
            self.crawler = crawler
        self.currentSnapshot = currentSnapshot
        self.description = description
        if isinstance(securityConfig, dict):
            self.securityConfig = SecurityConfig(**securityConfig)
        else:
            self.securityConfig = securityConfig
        self.schedule = schedule
        self.configuration = configuration
        if isinstance(sourceType, dict):
            self.sourceType = SourceType(**sourceType)
        else:
            self.sourceType = sourceType
        self. autoProfile = autoProfile
        self.tenantId = tenantId
        self.integrationId = integrationId
        self.subIntegrationId = subIntegrationId
        self.isProtectedResource = isProtectedResource
        self.createdBy = createdBy

        self.client = client

    def __repr__(self):
        return f"DataSource({self.__dict__})"

    def start_crawler(self):
        return self.client.start_crawler(self.name)

    def get_crawler_status(self):
        return self.client.get_crawler_status(self.name)


class CrawlerStatus:
    def __init__(self, assemblyName, isSuccess=None, status=None, *args, **kwargs):
        self.assemblyName = assemblyName
        if status is not None:
            self.status = status
        if isSuccess is not None:
            self.isSuccess = isSuccess

    def __repr__(self):
        return f"CrawlerStatus({self.__dict__})"
