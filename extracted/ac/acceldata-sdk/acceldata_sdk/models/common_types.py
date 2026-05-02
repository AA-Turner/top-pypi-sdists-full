from enum import Enum, auto
from typing import List, Optional, Dict, Any


class ExecutionType(Enum):
    SELECTIVE = 'SELECTIVE'
    FULL = 'FULL'
    INCREMENTAL = 'INCREMENTAL'

    def to_dict(self):
        return self.name


class MarkerConfig:
    def __init__(self, type: str):
        self.type = type

    def to_dict(self) -> Dict:
        return {'type': self.type}


class BoundsIdMarkerConfig(MarkerConfig):
    def __init__(self, baseAssetId: Optional[int] = None, idColumnName: str = "",
                 fromId: Optional[int] = None, toId: Optional[int] = None, *args, **kwargs):
        """
        Initializes a BoundsIdMarkerConfig object.

        Args:
            baseAssetId (Optional[int]): The base asset ID. Defaults to None.
            idColumnName (str): The ID column name. Defaults to "".
            fromId (Optional[int]): The starting ID. Defaults to None.
            toId (Optional[int]): The ending ID. Defaults to None.
        """
        super().__init__("bound")
        self.baseAssetId = baseAssetId
        self.idColumnName = idColumnName
        self.fromId = fromId
        self.toId = toId

    def to_dict(self) -> Dict:
        data = super().to_dict()
        data.update({
            'baseAssetId': self.baseAssetId,
            'idColumnName': self.idColumnName,
            'fromId': self.fromId,
            'toId': self.toId
        })
        return data


class BoundsFileEventMarkerConfig(MarkerConfig):
    def __init__(self, baseAssetId: Optional[int] = None, dateColumnName: str = "event_time",
                 timeZoneId: str = "UTC", fromDate: Optional[str] = None, toDate: Optional[str] = None):
        """
        Initializes a BoundsFileEventMarkerConfig object.

        Args:
            baseAssetId (Optional[int]): The base asset ID. Defaults to None.
            dateColumnName (str): The name of the date column. Defaults to "event_time".
            timeZoneId (str): The ID of the time zone. Defaults to "UTC".
            fromDate (Optional[str]): The starting date. Defaults to None.
            toDate (Optional[str]): The ending date. Defaults to None.
        """
        super().__init__("boundFileEvent")
        self.baseAssetId = baseAssetId
        self.dateColumnName = dateColumnName
        self.timeZoneId = timeZoneId
        self.fromDate = fromDate
        self.toDate = toDate

    def to_dict(self) -> Dict:
        data = super().to_dict()
        data.update({
            'baseAssetId': self.baseAssetId,
            'dateColumnName': self.dateColumnName,
            'timeZoneId': self.timeZoneId,
            'fromDate': self.fromDate,
            'toDate': self.toDate
        })
        return data


class BoundsDateTimeMarkerConfig(MarkerConfig):
    def __init__(self, baseAssetId: Optional[int] = None, dateColumnName: str = "",
                 format: str = "", timeZoneId: str = "UTC", fromDate: Optional[str] = None,
                 toDate: Optional[str] = None):
        """
        Initializes a BoundsDateTimeMarkerConfig object.

        Args:
            baseAssetId (Optional[int]): The base asset ID. Defaults to None.
            dateColumnName (str): The name of the date column. Defaults to "".
            format (str): The format of the date. Defaults to "".
            timeZoneId (str): The ID of the time zone. Defaults to "UTC".
            fromDate (Optional[str]): The starting date. Defaults to None.
            toDate (Optional[str]): The ending date. Defaults to None.
        """
        super().__init__("boundDateTime")
        self.baseAssetId = baseAssetId
        self.dateColumnName = dateColumnName
        self.format = format
        self.timeZoneId = timeZoneId
        self.fromDate = fromDate
        self.toDate = toDate

    def to_dict(self) -> Dict:
        data = super().to_dict()
        data.update({
            'baseAssetId': self.baseAssetId,
            'dateColumnName': self.dateColumnName,
            'format': self.format,
            'timeZoneId': self.timeZoneId,
            'fromDate': self.fromDate,
            'toDate': self.toDate
        })
        return data


class TimestampBasedMarkerConfig(MarkerConfig):
    def __init__(self, baseAssetId: Optional[int] = None, format: str = "",
                 timeZoneId: str = "UTC", initialOffset: Optional[str] = None,
                 toDateTime: Optional[str] = None, fromOffsets: Optional[str] = None):
        """
        Initializes a TimestampBasedMarkerConfig object.

        Args:
            baseAssetId (Optional[int]): The base asset ID. Defaults to None.
            format (str): The format of the timestamp. Defaults to "".
            timeZoneId (str): The ID of the time zone. Defaults to "UTC".
            initialOffset (Optional[str]): The initial offset of the timestamp. Defaults to None.
            toDateTime (Optional[str]): The end date and time of the timestamp. Defaults to None.
            fromOffsets (Optional[str]): The offsets of the timestamp. Defaults to None.
        """
        super().__init__("timestamp")
        self.baseAssetId = baseAssetId
        self.format = format
        self.timeZoneId = timeZoneId
        self.initialOffset = initialOffset
        self.toDateTime = toDateTime
        self.fromOffsets = fromOffsets

    def to_dict(self) -> Dict:
        data = super().to_dict()
        data.update({
            'baseAssetId': self.baseAssetId,
            'format': self.format,
            'timeZoneId': self.timeZoneId,
            'initialOffset': self.initialOffset,
            'toDateTime': self.toDateTime,
            'fromOffsets': self.fromOffsets
        })
        return data


class AssetMarkerConfig:
    def __init__(self, assetId: Optional[int] = None, markerConfig: MarkerConfig = None):
        self.assetId = assetId
        self.markerConfig = markerConfig

    def to_dict(self):
        return {
            'assetId': self.assetId,
            'markerConfig': self.markerConfig.to_dict()
        }


class YunikornConfig:
    def __init__(self, minExecutors: int, maxExecutors: int, executorCores: int, executorMemory: str, driverCores: int,
                 driverMemory: str):
        """
        Initializes an instance of the YunikornConfig class.

        Args:
            minExecutors (int): The minimum number of executors.
            maxExecutors (int): The maximum number of executors.
            executorCores (int): The number of cores per executor.
            executorMemory (str): The memory configuration for the executors.
            driverCores (int): The number of cores for the driver.
            driverMemory (str): The memory configuration for the driver.
        """
        self.minExecutors = minExecutors
        self.maxExecutors = maxExecutors
        self.executorCores = executorCores
        self.executorMemory = executorMemory
        self.driverCores = driverCores
        self.driverMemory = driverMemory

    def to_dict(self):
        return self.__dict__


class SparkResourceConfig:
    def __init__(self, yunikorn: YunikornConfig, additionalConfiguration: Dict[str, str]):
        """
        Initializes an instance of the SparkResourceConfig class.

        Args:
            yunikorn (YunikornConfig): The configuration for Yunikorn.
            additionalConfiguration (Dict[str, str]): Additional configuration for Spark.
        """
        self.yunikorn = yunikorn
        self.additionalConfiguration = additionalConfiguration

    def to_dict(self):
        return {
            'yunikorn': self.yunikorn.to_dict(),
            'additionalConfiguration': self.additionalConfiguration
        }


class Mapping:
    def __init__(self, key: str, isColumnVariable: Optional[bool] = None, value: Optional[str] = None):
        """
        Initializes a Mapping object.

        Args:
            key (str): The key of the mapping.
            isColumnVariable (Optional[bool]): A flag indicating if the mapping is a column variable.
            value (Optional[str]): The value of the mapping.
        """
        self.key = key
        self.isColumnVariable = isColumnVariable
        self.value = value

    def to_dict(self) -> Dict[str, Any]:
        return {
            "key": self.key,
            "isColumnVariable": self.isColumnVariable,
            "value": self.value
        }


class RuleSparkSQLDynamicFilterVariableMapping:
    def __init__(self, ruleName: str = None, mapping: Optional[List[Mapping]] = None):
        """
        Initializes a `RuleSparkSQLDynamicFilterVariableMapping` object.
        Args:
            ruleName (str, optional): The name of the rule. Defaults to None.
            mapping (List[Mapping], optional): The list of mappings. Defaults to None.
        """
        self.ruleName = ruleName
        self.mapping = mapping if mapping is not None else []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ruleName": self.ruleName,
            "mapping": [m.to_dict() for m in self.mapping]
        }


class PolicyExecutionRequest:
    def __init__(self, executionType: ExecutionType,
                 markerConfigs: Optional[List[AssetMarkerConfig]] = None,
                 ruleItemSelections: Optional[List[int]] = None,
                 includeInQualityScore: bool = True,
                 pipelineRunId: Optional[int] = None,
                 sparkSQLDynamicFilterVariableMapping: Optional[List[RuleSparkSQLDynamicFilterVariableMapping]] = None,
                 sparkFilterSelectedColumns: Optional[List[str]] = None,
                 sparkResourceConfig: Optional[SparkResourceConfig] = None):
        """
        Initializes a PolicyExecutionRequest object.

        Args:
            executionType (ExecutionType): The type of execution. Supported types: (SELECTIVE, FULL, INCREMENTAL)
            markerConfigs (List[AssetMarkerConfig], optional): The list of marker configurations. Defaults to None.
            ruleItemSelections (List[int], optional): The list of rule item selections. Defaults to None. If not passed all the rule item definitions will be executed.
            includeInQualityScore (bool, optional): Whether to include in quality score. Defaults to True.
            pipelineRunId (int, optional): ID of the pipeline run for attaching policy execution to the asset. Defaults to None.
            sparkSQLDynamicFilterVariableMapping (List[RuleSparkSQLDynamicFilterVariableMapping], optional): The list of Spark SQL dynamic filter variable mappings applicable for a Data Quality Policy. Defaults to None.
            sparkFilterSelectedColumns (List[str], optional): The list of Spark filter selected columns. Defaults to None.
            sparkResourceConfig (SparkResourceConfig, optional): The Spark resource configuration. Defaults to None.
        """
        self.executionType = executionType
        self.markerConfigs = markerConfigs
        self.ruleItemSelections = ruleItemSelections
        self.includeInQualityScore = includeInQualityScore
        self.pipelineRunId = pipelineRunId
        self.sparkSQLDynamicFilterVariableMapping = sparkSQLDynamicFilterVariableMapping if sparkSQLDynamicFilterVariableMapping is not None else []
        self.sparkFilterSelectedColumns = sparkFilterSelectedColumns
        self.sparkResourceConfig = sparkResourceConfig

    def to_dict(self) -> Dict[str, Any]:
        return {
            key: value for key, value in {
                "executionType": self.executionType.to_dict(),
                "markerConfigs": [config.to_dict() for config in self.markerConfigs] if self.markerConfigs else None,
                "ruleItemSelections": self.ruleItemSelections,
                "includeInQualityScore": self.includeInQualityScore,
                "pipelineRunId": self.pipelineRunId,
                "sparkSQLDynamicFilterVariableMapping": [mapping.to_dict() for mapping in
                                                         self.sparkSQLDynamicFilterVariableMapping],
                "sparkFilterSelectedColumns": self.sparkFilterSelectedColumns,
                "sparkResourceConfig": self.sparkResourceConfig.to_dict() if self.sparkResourceConfig else None
            }.items() if value is not None
        }
