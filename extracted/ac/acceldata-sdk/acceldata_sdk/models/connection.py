from enum import Enum, auto
from dataclasses import dataclass
from typing import List


class ConnectionType:

    def __init__(self, id, type, *args, **kwargs):
        self.id = id
        self.type = type

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return f"ConnectionType({self.__dict__})"


class SecretsManagerType(Enum):
    AWS_SECRETS_MANAGER = auto()


@dataclass
class SecretManagerConfiguration:
    name: str = None
    type: SecretsManagerType = None

    def __init__(self,
                 name: str = None,
                 type: SecretsManagerType = None, *args, **kwargs):
        self.name = name
        if isinstance(type, dict):
            self.type = SecretsManagerType(**type)
        else:
            self.type = type


@dataclass
class SecretManagerConfigurationWithOption:
    secretManagerConfig: List[SecretManagerConfiguration] = None
    defaultOption: bool = None

    def __init__(self,
                 secretManagerConfig: List[SecretManagerConfiguration] = None,
                 defaultOption: bool = None, *args, **kwargs):
        self.defaultOption = defaultOption
        self.secretManagerConfig = list()
        if secretManagerConfig is not None:
            for obj in secretManagerConfig:
                if isinstance(obj, dict):
                    self.secretManagerConfig.append(SecretManagerConfiguration(**obj))
                else:
                    self.secretManagerConfig.append(obj)


@dataclass
class LivyComputeConfig:
    isEnabled = None
    executorMemory = None
    executorCores = None
    numExecutors = None

    def __init__(self,
                 isEnabled: bool = None,
                 executorMemory: str = None,
                 executorCores=None,
                 numExecutors=None, *args, **kwargs):
        self.isEnabled = isEnabled
        self.executorMemory = executorMemory
        self.executorCores = executorCores
        self.numExecutors = numExecutors

    def __repr__(self):
        return f"LivyComputeConfig({self.__dict__})"


@dataclass
class DatabricksComputeConfig:
    isEnabled = None
    minWorkers = None
    maxWorkers = None
    clusterWorkerType = None
    clusterDriverType = None
    jobClusterType = None

    def __init__(self,
                 isEnabled: bool = None,
                 minWorkers=None,
                 maxWorkers=None,
                 clusterWorkerType: str = None,
                 clusterDriverType: str = None,
                 jobClusterType: str = None,
                 *args, **kwargs):
        self.isEnabled = isEnabled
        self.minWorkers = minWorkers
        self.maxWorkers = maxWorkers
        self.clusterWorkerType = clusterWorkerType
        self.clusterDriverType = clusterDriverType
        self.jobClusterType = jobClusterType

    def __repr__(self):
        return f"DatabricksComputeConfig({self.__dict__})"


@dataclass
class YunikornComputeConfig:
    isEnabled = None
    executorMemory = None
    executorCores = None
    minExecutors = None
    maxExecutors = None

    def __init__(self,
                 isEnabled: bool = None,
                 executorMemory: str = None,
                 executorCores=None,
                 minExecutors=None,
                 maxExecutors=None, *args, **kwargs):
        self.isEnabled = isEnabled
        self.executorMemory = executorMemory
        self.executorCores = executorCores
        self.minExecutors = minExecutors
        self.maxExecutors = maxExecutors


@dataclass
class PipelineComputeConfig:
    livy: LivyComputeConfig = None
    databricks: DatabricksComputeConfig = None
    yunikorn: YunikornComputeConfig = None

    def __init__(self,
                 livy: LivyComputeConfig = None,
                 databricks: DatabricksComputeConfig = None,
                 yunikorn: YunikornComputeConfig = None, *args, **kwargs):
        if isinstance(livy, dict):
            self.livy = LivyComputeConfig(**livy)
        else:
            self.livy = livy
        if isinstance(databricks, dict):
            self.databricks = DatabricksComputeConfig(**databricks)
        else:
            self.databricks = databricks
        if isinstance(yunikorn, dict):
            self.yunikorn = YunikornComputeConfig(**yunikorn)
        else:
            self.yunikorn = yunikorn

    def __repr__(self):
        return f"PipelineComputeConfig({self.__dict__})"


class PipelineType(Enum):
    ANALYSIS = auto()
    MONITOR = auto()
    QUERY_ANALYSIS = auto()


@dataclass
class ProcessMetrics:
    status = None
    reportingTime = None
    
    def __init__(self,
                 status=None,
                 reportingTime=None, *args, **kwargs):
        self.status = status
        self.reportingTime = reportingTime

    def __repr__(self):
        return f"ProcessMetrics({self.__dict__})"


@dataclass
class KubernetesMetrics:
    status = None
    reportingTime = None

    def __init__(self,
                 status=None,
                 reportingTime=None, *args, **kwargs):
        self.status = status
        self.reportingTime = reportingTime


@dataclass
class DataplaneHealthMetrics:
    reportingTime: str = None
    process: ProcessMetrics = None
    kubernetes: KubernetesMetrics = None

    def __init__(self,
                 reportingTime=None,
                 process: ProcessMetrics = None,
                 kubernetes: KubernetesMetrics = None, *args, **kwargs):
        self.reportingTime = reportingTime
        if isinstance(process, dict):
            self.process = ProcessMetrics(**process)
        else:
            self.process = process
        if isinstance(kubernetes, dict):
            self.kubernetes = KubernetesMetrics(**kubernetes)
        else:
            self.kubernetes = kubernetes

    def __repr__(self):
        return f"DataplaneHealthMetrics({self.__dict__})"


class AnalyticsPipeline:

    def __init__(self, id, name, createdAt, updatedAt, url, externalUrl, description=None, hbaseEnabled=None,
                 hdfsEnabled=None, hiveEnabled=None, secretsManagerConfiguration=None, measureResultFsType=None,
                 tenantId = None, pipelineComputeConfig=None, pipelineType=None, version=None,
                 statusReportInterval=None, status=None, lastStatusReportTime=None, healthReport=None,
                 sparkMajorVersion=None, parentPipelineId=None, helmTemplateValues=None, **kwargs):
        self.name = name
        self.createdAt = createdAt
        self.updatedAt = updatedAt
        self.url = url
        self.id = id
        self.externalUrl = externalUrl
        self.description = description
        self.hbaseEnabled = hbaseEnabled
        self.hdfsEnabled = hdfsEnabled
        self.hiveEnable = hiveEnabled
        if isinstance(secretsManagerConfiguration, dict):
            self.secretsManagerConfiguration = SecretManagerConfigurationWithOption(**secretsManagerConfiguration)
        else:
            self.secretsManagerConfiguration = secretsManagerConfiguration

        self.measureResultFsType = measureResultFsType
        self.tenantId = tenantId
        if isinstance(pipelineComputeConfig, dict):
            self.pipelineComputeConfig = PipelineComputeConfig(**pipelineComputeConfig)
        else:
            self.pipelineComputeConfig = pipelineComputeConfig
        if isinstance(pipelineType, dict):
            self.pipelineType = PipelineType(**pipelineType)
        else:
            self.pipelineType = pipelineType

        self.version = version
        self.statusReportInterval = statusReportInterval
        self.status = status,
        self.lastStatusReportTime = lastStatusReportTime
        if isinstance(healthReport, dict):
            self.healthReport = DataplaneHealthMetrics(**healthReport)
        else:
            self.healthReport = healthReport
        self.sparkMajorVersion = sparkMajorVersion
        self.parentPipelineId = parentPipelineId
        self.helmTemplateValues = helmTemplateValues

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return f"AnalyticsPipeline({self.__dict__})"


class ConfigProperty:

    def __init__(self, key, value, id=None, **kwargs):
        self.key = key
        self.value = value
        self.id = id

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return f"ConfigProperty({self.__dict__})"


class Connection:

    def __init__(self, name, connectionType, createdAt, updatedAt, analyticsPipeline, configuration, assemblyCount=0,
                 description=None, properties=None,
                 id=None, **kwargs):
        self.name = name
        self.configuration = configuration
        self.connectionType = connectionType
        self.createdAt = createdAt
        self.updatedAt = updatedAt
        self.assemblyCount = assemblyCount
        self.description = description
        self.id = id
        if isinstance(connectionType, dict):
            self.connectionType = ConnectionType(**connectionType)
        else:
            self.connectionType = connectionType
        if isinstance(analyticsPipeline, dict):
            self.analyticsPipeline = AnalyticsPipeline(**analyticsPipeline)
        else:
            self.analyticsPipeline = analyticsPipeline
        self.properties = list()
        if properties is not None:
            for obj in properties:
                if isinstance(obj, dict):
                    self.properties.append(ConfigProperty(**obj))
                else:
                    self.properties.append(obj)

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return f"Connection({self.__dict__})"


class ConnectionCheckStatus(Enum):
    SUCCESS = 1
    FAILURE = 2


class ConnectionCheck:

    def __init__(self, message=None, status=None, **kwargs):
        self.message = message
        self.status = status

    def __repr__(self):
        return f"ConnectionCheckResponse({self.__dict__})"
