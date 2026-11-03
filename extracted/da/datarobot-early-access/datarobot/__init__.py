# flake8: noqa
# Aliased under underscores so they do not land in the public `datarobot`
# namespace (and so `dir(dr)` stays the documented surface).
from typing import Any as _Any, List as _List

from ._version import __version__
from .client import Client
from .context import Context
from .enums import (
    AUTOPILOT_MODE,
    KeyValueCategory,
    KeyValueEntityType,
    KeyValueType,
    NETWORK_EGRESS_POLICY,
    PredictionEnvironmentPlatform,
    QUEUE_STATUS,
    SCORING_TYPE,
    SNAPSHOT_POLICY,
    TARGET_TYPE,
    VERBOSITY_LEVEL,
)
from .errors import AppPlatformError
from .helpers import *
from .models import (
    Application,
    AutomatedDocument,
    CustomApplication,
    CustomApplicationSource,
    BatchMonitoringJob,
    BatchMonitoringJobDefinition,
    BatchPredictionJob,
    BatchPredictionJobDefinition,
    BlenderModel,
    Blueprint,
    BlueprintChart,
    BlueprintTaskDocument,
    CalendarFile,
    Cluster,
    ClusteringModel,
    ClusterInsight,
    CombinedModel,
    ComplianceDocTemplate,
    Connector,
    Credential,
    CustomInferenceModel,
    CustomModelTest,
    CustomModelVersion,
    CustomModelVersionDependencyBuild,
    CustomTask,
    CustomTaskVersion,
    CustomTemplate,
    DataDriver,
    DataEngineQueryGenerator,
    Dataset,
    DatasetDetails,
    DatasetFeature,
    DatasetFeatureHistogram,
    DatasetFeaturelist,
    DataSlice,
    DataSliceSizeInfo,
    DataSource,
    DataSourceParameters,
    DataStore,
    DatetimeModel,
    Deployment,
    ExecutionEnvironment,
    ExecutionEnvironmentVersion,
    ExternalConfusionChart,
    ExternalLiftChart,
    ExternalMulticlassLiftChart,
    ExternalResidualsChart,
    ExternalRocCurve,
    ExternalScores,
    Event,
    Feature,
    FeatureAssociationFeaturelists,
    FeatureAssociationMatrix,
    FeatureAssociationMatrixDetails,
    FeatureHistogram,
    FeatureImpactJob,
    FeatureLineage,
    Featurelist,
    Files,
    FilesCatalogSearch,
    FilesDetails,
    FrozenModel,
    genai,
    InteractionFeature,
    Job,
    KeyValue,
    MemorySpace,
    Model,
    ModelBlueprintChart,
    ModelingFeature,
    ModelingFeaturelist,
    ModelJob,
    ModelRecommendation,
    OCREngineSpecificParameters,
    OCRJobDatasetLanguage,
    OCRJobResource,
    OCRJobStatusEnum,
    PayoffMatrix,
    PredictionDataset,
    PredictionEnvironment,
    PredictionExplanations,
    PredictionExplanationsInitialization,
    Predictions,
    PredictionServer,
    PredictJob,
    PrimeFile,
    PrimeModel,
    Project,
    RatingTable,
    RatingTableModel,
    Recipe,
    RegisteredModel,
    RegisteredModelVersion,
    registry,
    RelationshipsConfiguration,
    Ruleset,
    SecondaryDatasetConfigurations,
    SegmentationTask,
    SegmentInfo,
    Session,
    ShapImpact,
    ShapMatrix,
    ShapMatrixJob,
    SharingAccess,
    SharingRole,
    StartOCRJobResponse,
    TrainingPredictions,
    TrainingPredictionsJob,
    UseCase,
    UserBlueprint,
    JdbcPreview,
    JdbcPreviewData,
    JdbcResultSchemaEntry,
)

DR_TRACKABLE = True

# Pipelines. The REST/control-plane surface is plain trafaret over HTTP and is
# imported eagerly -- it costs ~3ms and works on every interpreter the rest of
# the SDK supports.
#
# The covalent-backed authoring names (task, pipeline, dispatch, CloudExecutor,
# Deps*) are NOT imported here: covalent costs ~380ms to import and requires
# Python 3.10+, so charging that to every `import datarobot` would make the SDK
# 2.2x slower to load for everyone, including users who never touch pipelines.
# They are resolved on first attribute access by the module `__getattr__` below,
# which forwards to datarobot.pipelines and raises there with an actionable
# message if the interpreter is too old or the vendored runtime is missing.
#
# Side-effect import: datarobot._vendor prepends the vendored covalent /
# covalent-cloud packages to sys.path, so a later `import covalent` resolves to
# the bundled copy. It is pure path manipulation and cannot fail. `from ...
# import` (rather than `import datarobot._vendor`) avoids binding the top-level
# `datarobot` name into our own namespace, which would break the dir(dr)
# inventory test.
from datarobot import _vendor  # noqa: F401,E402

from datarobot.pipelines import (  # noqa: E402
    Pipeline as Pipeline,
    PipelineVersion as PipelineVersion,
    PipelineTask as PipelineTask,
    TaskParameter as TaskParameter,
    PipelineDispatch as PipelineDispatch,
    PipelineInput as PipelineInput,
    PipelineSchedule as PipelineSchedule,
    PipelineImage as PipelineImage,
    PipelineImageVersion as PipelineImageVersion,
    PipelineTaskExecution as PipelineTaskExecution,
    PipelineMode as PipelineMode,
    PipelineVersionStatus as PipelineVersionStatus,
    PipelineDispatchStatus as PipelineDispatchStatus,
    PipelineDispatchTrigger as PipelineDispatchTrigger,
    PipelineInputState as PipelineInputState,
    PipelineScheduleStatus as PipelineScheduleStatus,
    PipelineImageStatus as PipelineImageStatus,
    TaskExecutionStatus as TaskExecutionStatus,
    Pipelines as Pipelines,
)

# Covalent-backed pipeline authoring names, forwarded lazily to
# datarobot.pipelines. Keep in sync with `_LAZY_ATTRS` there.
_COVALENT_ATTRS = frozenset({
    "task",
    "pipeline",
    "wait",
    "get_context",
    "dispatch",
    "dispatch_sync",
    "get_result",
    "executor",
    "fs_strategies",
    "DepsBash",
    "DepsCall",
    "DepsModule",
    "DepsPip",
    "CloudExecutor",
    "PipelineTaskExecutor",
})


# Subpackages that are optional installs, forwarded lazily so `dr.<name>`
# resolves without importing them at startup. `fs` needs the [fs] extra.
_LAZY_SUBMODULES = frozenset({"fs"})


def __getattr__(name: str) -> _Any:
    """Resolve a lazily-exported name on first access (PEP 562).

    Anything unavailable raises AttributeError, never RuntimeError/ImportError:
    `hasattr` and `inspect.getmembers` only swallow AttributeError, so any other
    type turns routine introspection into a crash. datarobot.pipelines puts the
    actionable explanation in the AttributeError message.
    """
    if name in _COVALENT_ATTRS:
        from datarobot import pipelines

        value = getattr(pipelines, name)  # AttributeError if unavailable
        globals()[name] = value  # cache: __getattr__ is not consulted again
        return value

    if name in _LAZY_SUBMODULES:
        import importlib

        try:
            value = importlib.import_module(f"datarobot.{name}")
        except ImportError as exc:
            raise AttributeError(
                f"datarobot.{name} could not be imported ({exc}). It ships in an "
                f"optional extra -- try `pip install datarobot[{name}]`."
            ) from exc

        globals()[name] = value
        return value

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__() -> _List[str]:
    """Names for `dir(datarobot)`, which drives IPython tab-completion.

    The lazy names are listed unconditionally, even where they cannot currently
    be resolved. Two reasons, and the first one is the bug that made this a
    review finding in the first place:

    * `inspect.getmembers` calls `dir()` and then `getattr()`, swallowing
      AttributeError -- so an unresolvable name here is simply omitted from its
      result rather than crashing it. Listing it is safe now that `__getattr__`
      raises AttributeError and nothing else.
    * Hiding the name is worse than showing it. On a PyPI install the vendored
      runtime is always present, so the only environment where these cannot
      resolve is a source checkout before `make vendor` -- exactly where a
      developer typing `dr.<tab>` and not seeing `task` would conclude the SDK
      has no authoring surface at all. Listed plus an actionable AttributeError
      is better discovery than silently absent.

    This also keeps the name inventory a property of the package rather than of
    the environment, which is what `tests/test_client.py` asserts on.
    """
    return sorted(set(globals()) | _COVALENT_ATTRS | _LAZY_SUBMODULES | {"pipelines"})
