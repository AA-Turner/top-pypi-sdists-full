from pydantic.version import VERSION as PYDANTIC_VERSION

IS_PYDANTIC_V1 = PYDANTIC_VERSION.startswith("1.")

if IS_PYDANTIC_V1:
    from .generated_models_pydantic_v1 import QueueMessage
    from .generated_models_pydantic_v1 import QueueMessageV1
    from .generated_models_pydantic_v1 import QueueRecord
    from .generated_models_pydantic_v1 import DataLakeData
    from .generated_models_pydantic_v1 import TelemetryData
    from .generated_models_pydantic_v1 import ArtifactUploadRequest
    from .generated_models_pydantic_v1 import ArtifactMetadata
    from .generated_models_pydantic_v1 import ArtifactBuildMetadata
    from .generated_models_pydantic_v1 import SqaAppBuildResult
    from .generated_models_pydantic_v1 import SqaTestResult
    from .generated_models_pydantic_v1 import SqaTestSession
    from .generated_models_pydantic_v1 import LogEvent
    from .generated_models_pydantic_v1 import ExceptionEvent
    from .generated_models_pydantic_v1 import TestRailResult
    from .generated_models_pydantic_v1 import TestResultCustomProps
    from .generated_models_pydantic_v1 import XrayInfo
    from .generated_models_pydantic_v1 import XrayStep
    from .generated_models_pydantic_v1 import XrayParameter
    from .generated_models_pydantic_v1 import XrayCustomField
    from .generated_models_pydantic_v1 import XrayIteration
    from .generated_models_pydantic_v1 import XrayTestInfo
    from .generated_models_pydantic_v1 import XrayTestExecUpdate
    from .generated_models_pydantic_v1 import XrayImportTestExecution
else:
    from .generated_models_pydantic_v2 import QueueMessage
    from .generated_models_pydantic_v2 import QueueMessageV1
    from .generated_models_pydantic_v2 import QueueRecord
    from .generated_models_pydantic_v2 import DataLakeData
    from .generated_models_pydantic_v2 import TelemetryData
    from .generated_models_pydantic_v2 import ArtifactUploadRequest
    from .generated_models_pydantic_v2 import ArtifactMetadata
    from .generated_models_pydantic_v2 import ArtifactBuildMetadata
    from .generated_models_pydantic_v2 import SqaAppBuildResult
    from .generated_models_pydantic_v2 import SqaTestResult
    from .generated_models_pydantic_v2 import SqaTestSession
    from .generated_models_pydantic_v2 import LogEvent
    from .generated_models_pydantic_v2 import ExceptionEvent
    from .generated_models_pydantic_v2 import TestRailResult
    from .generated_models_pydantic_v2 import TestResultCustomProps
    from .generated_models_pydantic_v2 import XrayInfo
    from .generated_models_pydantic_v2 import XrayStep
    from .generated_models_pydantic_v2 import XrayParameter
    from .generated_models_pydantic_v2 import XrayCustomField
    from .generated_models_pydantic_v2 import XrayIteration
    from .generated_models_pydantic_v2 import XrayTestInfo
    from .generated_models_pydantic_v2 import XrayTestExecUpdate
    from .generated_models_pydantic_v2 import XrayImportTestExecution

__all__ = [
    "QueueMessage",
    "QueueMessageV1",
    "QueueRecord",
    "DataLakeData",
    "TelemetryData",
    "ArtifactUploadRequest",
    "ArtifactMetadata",
    "ArtifactBuildMetadata",
    "SqaAppBuildResult",
    "SqaTestResult",
    "SqaTestSession",
    "LogEvent",
    "ExceptionEvent",
    "TestRailResult",
    "TestResultCustomProps",
    "XrayInfo",
    "XrayStep",
    "XrayParameter",
    "XrayCustomField",
    "XrayIteration",
    "XrayTestInfo",
    "XrayTestExecUpdate",
    "XrayImportTestExecution",
]
