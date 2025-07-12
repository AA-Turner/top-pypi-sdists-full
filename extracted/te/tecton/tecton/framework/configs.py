"""Configs and dataclasses used to construct Tecton objects.

Classes in this file should be simple data classes (i.e. do not have much functionality) and should not depend directly
on Tecton objects (to avoid circular dependencies).
"""

import datetime
import functools
import inspect
import json
import sys
from enum import Enum
from types import MappingProxyType
from typing import Any
from typing import Callable
from typing import ClassVar
from typing import Dict
from typing import List
from typing import Mapping
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union

import pandas
import pyarrow
from google.protobuf import struct_pb2
from pyspark.sql import DataFrame
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType
from typeguard import typechecked
from typing_extensions import Literal


if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import logging

from tecton import types
from tecton._internals import type_utils
from tecton._internals.repo import function_serialization
from tecton._internals.tecton_pydantic import StrictModel
from tecton._internals.tecton_pydantic import pydantic_v1
from tecton.aggregation_functions import AggregationFunction
from tecton.framework.utils import Secret
from tecton.framework.utils import convert_secret_to_sanitized_reference
from tecton.framework.utils import get_transformation_mode_enum
from tecton.types import Field
from tecton_core import feature_view_utils
from tecton_core import specs
from tecton_core import time_utils
from tecton_core.compute_mode import BatchComputeMode
from tecton_core.compute_mode import default_batch_compute_mode
from tecton_core.errors import TectonValidationError
from tecton_core.filter_context import FilterContext
from tecton_proto.args import data_source__client_pb2 as data_source_pb2
from tecton_proto.args import feature_service__client_pb2 as feature_service_pb2
from tecton_proto.args import feature_view__client_pb2 as feature_view_pb2
from tecton_proto.args import virtual_data_source__client_pb2 as virtual_data_source_pb2
from tecton_proto.common import python_version__client_pb2 as python_version_pb2
from tecton_proto.common import scaling_config__client_pb2 as scaling_config_pb2
from tecton_proto.common import time_window__client_pb2 as time_window_pb2
from tecton_spark import data_source_helper
from tecton_spark import spark_schema_wrapper


logger = logging.getLogger(__name__)


AVAILABILITY_SPOT = "spot"
AVAILABILITY_ON_DEMAND = "on_demand"
AVAILABILITY_SPOT_FALLBACK = "spot_with_fallback"
DATABRICKS_SUPPORTED_AVAILABILITY = {AVAILABILITY_SPOT, AVAILABILITY_ON_DEMAND, AVAILABILITY_SPOT_FALLBACK}
EMR_SUPPORTED_AVAILABILITY = {AVAILABILITY_SPOT, AVAILABILITY_ON_DEMAND, AVAILABILITY_SPOT_FALLBACK}


class SparkVersions(str, Enum):
    Emr6_9 = "emr-6.9.0"
    Emr6_9_1 = "emr-6.9.1"
    Emr6_12 = "emr-6.12.0"
    Emr7_0 = "emr-7.0.0"
    Dbr10_4 = "10.4.x-scala2.12"
    Dbr11_3 = "11.3.x-scala2.12"
    Dbr12_2 = "12.2.x-scala2.12"
    Dbr13_3 = "13.3.x-scala2.12"
    Dbr14_3 = "14.3.x-scala2.12"
    Dbr15_4 = "15.4.x-scala2.12"
    Dbr16_4 = "16.4.x-scala2.12"


class PythonVersionEMR(Enum):
    """Defines the Python version to use for EMR clusters."""

    CLUSTER_DEFAULT = python_version_pb2.PythonVersion.CLUSTER_DEFAULT
    PYTHON_3_9_13 = python_version_pb2.PythonVersion.PYTHON_3_9_13


# keep databricks_spark_version in sync with integration_tests/pool_warmup/api_helper.py spark_version in create_cluster func
DEFAULT_SPARK_VERSIONS = {
    "databricks_spark_version": SparkVersions.Dbr13_3,
    "emr_spark_version": SparkVersions.Emr6_12,
    "emr_python_version": PythonVersionEMR.PYTHON_3_9_13.value,
}
EMR_SUPPORTED_SPARK = {
    SparkVersions.Emr6_9_1,
    SparkVersions.Emr6_12,
    SparkVersions.Emr7_0,
}
DATABRICKS_SUPPORTED_SPARK = {
    SparkVersions.Dbr11_3,
    SparkVersions.Dbr12_2,
    SparkVersions.Dbr13_3,
    SparkVersions.Dbr14_3,
    SparkVersions.Dbr15_4,
    SparkVersions.Dbr16_4,
}

TECTON_COMPUTE_DEFAULTS = {"tecton_compute_instance_type": "m6a.2xlarge"}


# Keep up-to-date with UnityCatalogAccessMode from tecton_proto/args/data_source.proto
class UnityCatalogAccessMode(Enum):
    SINGLE_USER = data_source_pb2.UnityCatalogAccessMode.UNITY_CATALOG_ACCESS_MODE_SINGLE_USER
    SINGLE_USER_WITH_FGAC = data_source_pb2.UnityCatalogAccessMode.UNITY_CATALOG_ACCESS_MODE_SINGLE_USER_WITH_FGAC
    SHARED = data_source_pb2.UnityCatalogAccessMode.UNITY_CATALOG_ACCESS_MODE_SHARED


RECOMMENDED_PYTHON_VERSION_EMR = "python_3_9_13"

PYTHON_VERSION_EMR = {
    "default": PythonVersionEMR.CLUSTER_DEFAULT,
    "python_3_9_13": PythonVersionEMR.PYTHON_3_9_13,
}


def _string_to_timedelta(value: Any) -> Any:
    if isinstance(value, str):
        return time_utils.parse_to_timedelta(value)
    return value


def _date_to_datetime(value: Any) -> Any:
    if isinstance(value, datetime.date):
        return datetime.datetime(year=value.year, month=value.month, day=value.day)
    return value


def _str_to_json_struct(value: Any) -> Any:
    if isinstance(value, str):
        return json.loads(value)
    return value


class WallClockTime(StrictModel):
    """AggregationLeadingEdge configuration to configure the stream feature views to use wall clock time for the leading
    aggregation edge.

    An aggregation window will be calculated with respect to the feature request server wall clock time.
    """

    # Used for YAML parsing as a Pydantic discriminator.
    kind: Literal["WallClockTime"] = "WallClockTime"

    def _to_proto(self) -> feature_view_pb2.AggregationLeadingEdge.AGGREGATION_MODE_WALL_CLOCK_TIME:
        return feature_view_pb2.AggregationLeadingEdge.AGGREGATION_MODE_WALL_CLOCK_TIME


class LatestEventTime(StrictModel):
    """AggregationLeadingEdge configuration to configure the stream feature views to use the latest event time
    for the leading aggregation edge. This is also known as the stream high watermark timestamp for the stream source.

    This timestamp is used for all aggregation features in the feature view. All aggregation windows will be with
    respect to this stream high watermark.

    Warning: This option will be deprecated soon in Tecton 1.1. Please see the Tecton documentation behind deprecating
    this option.
    """

    # Used for YAML parsing as a Pydantic discriminator.
    kind: Literal["LatestEventTime"] = "LatestEventTime"

    def _to_proto(self) -> feature_view_pb2.AggregationLeadingEdge.AGGREGATION_MODE_LATEST_EVENT_TIME:
        return feature_view_pb2.AggregationLeadingEdge.AGGREGATION_MODE_LATEST_EVENT_TIME


AggregationLeadingEdgeTypes = Union[
    WallClockTime,
    LatestEventTime,
]


class _DefaultClusterConfig(StrictModel):
    """A default cluster configuration. Should not be explicitly set by users.

    Used to couple changes to default compute settings to SDK releases.
    """

    # Used for YAML parsing as a Pydantic discriminator.
    kind: Literal["_DefaultClusterConfig"] = "_DefaultClusterConfig"

    def _to_cluster_proto(self) -> feature_view_pb2.ClusterConfig:
        return feature_view_pb2.ClusterConfig(
            implicit_config=feature_view_pb2.DefaultClusterConfig(
                **{
                    **DEFAULT_SPARK_VERSIONS,
                    **TECTON_COMPUTE_DEFAULTS,
                }
            )
        )


class ExistingClusterConfig(StrictModel):
    """Use an existing Databricks cluster.

    :param existing_cluster_id: ID of the existing cluster.
    """

    # Used for YAML parsing as a Pydantic discriminator.
    kind: Literal["ExistingClusterConfig"] = "ExistingClusterConfig"
    existing_cluster_id: str

    def _to_proto(self) -> feature_view_pb2.ExistingClusterConfig:
        proto = feature_view_pb2.ExistingClusterConfig()
        proto.existing_cluster_id = self.existing_cluster_id

        return proto

    def _to_cluster_proto(self) -> feature_view_pb2.ClusterConfig:
        return feature_view_pb2.ClusterConfig(existing_cluster=self._to_proto())


def _to_json_cluster_proto(value: Mapping[str, Any]) -> feature_view_pb2.JsonClusterConfig:
    json_struct = struct_pb2.Struct()
    json_struct.update(value)
    return feature_view_pb2.JsonClusterConfig(json=json_struct)


class EMRClusterConfig(StrictModel):
    """Configuration used to specify materialization cluster options on EMR.

    This class describes the attributes of the new clusters which are created in EMR during
    materialization jobs. You can configure options of these clusters, like cluster size and extra pip dependencies.

    Note on `extra_pip_dependencies`: This is a list of packages that will be installed during materialization.
    To use PyPI packages, specify the package name and optionally the version, e.g. `"tensorflow"` or `"tensorflow==2.2.0"`.
    To use custom code, package it as a Python wheel or egg file in S3 or DBFS, then specify the path to the file,
    e.g. `"s3://my-bucket/path/custom.whl"`, or `"dbfs:/path/to/custom.whl"`.

    These libraries will only be available to use inside Spark UDFs. For example, if you set
    `extra_pip_dependencies=["tensorflow"]`, you can use it in your transformation as shown below.

    ```python
    from tecton import batch_feature_view, Input, EMRClusterConfig

    @batch_feature_view(
        sources=[credit_scores_batch],
        # Can be an argument instance to a batch feature view decorator
        batch_compute = EMRClusterConfig(
            instance_type = 'm5.2xlarge',
            number_of_workers=4,
            extra_pip_dependencies=["tensorflow==2.2.0"],
        ),
        # Other named arguments to batch feature view
        ...
    )

    # Use the tensorflow package in the UDF since tensorflow will be installed
    # on the EMR Spark cluster. The import has to be within the UDF body. Putting it at the
    # top of the file or inside transformation function won't work.

    @transformation(mode='pyspark')
    def test_transformation(transformation_input):
        from pyspark.sql import functions as F
        from pyspark.sql.types import IntegerType

        def my_tensorflow(x):
            import tensorflow as tf
            return int(tf.math.log1p(float(x)).numpy())

        my_tensorflow_udf = F.udf(my_tensorflow, IntegerType())

        return transformation_input.select(
            'entity_id',
            'timestamp',
            my_tensorflow_udf('clicks').alias('log1p_clicks')
        )
    ```

    :param instance_type: Instance type for the cluster. Must be a valid type as listed in [this AWS documentation](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-supported-instance-types.html).
        Additionally, Graviton instances such as the m6g family are not supported. If not specified, a value determined by the Tecton backend is used.
    :param instance_availability: Instance availability for the cluster : "spot", "on_demand", or "spot_with_fallback". defaults to `spot`.
    :param number_of_workers: Number of instances for the materialization job. If not specified, a value determined by the Tecton backend is used
    :param first_on_demand: The first `first_on_demand` nodes of the cluster will use on_demand instances. The rest will use the type specified by instance_availability.
        If first_on_demand >= 1, the master node will use on_demand instance type. `first_on_demand` is recommended to be set >= 1 for cluster configs for critical streaming features.
    :param root_volume_size_in_gb: Size of the root volume in GB per instance for the materialization job.
        If not specified, a value determined by the Tecton backend is used.
    :param extra_pip_dependencies: Extra pip dependencies to be installed on the materialization cluster. Must be PyPI packages, or wheels/eggs in S3 or DBFS.
    :param spark_config: Map of Spark configuration options and their respective values that will be passed to the
        FeatureView materialization Spark cluster.
    :param emr_version: EMR version of the cluster. Supported EMR versions can be found on [this page](https://docs.tecton.ai/docs/materializing-features/configure-spark-materialization/using-pinned-emr-and-databricks-runtime-releases#overview).
    :param python_version: Python version for cluster to use. Options are "default" and "python_3_9_13" (python 3.9.13). "default" uses the default Python version on the EMR cluster. Defaults to `python_3_9_13` for emr-6.X and `default` for emr-7.X.
    """

    kind: Literal["EMRClusterConfig"] = "EMRClusterConfig"  # Used for YAML parsing as a Pydantic discriminator.
    instance_type: Optional[str] = None
    instance_availability: Optional[str] = None
    number_of_workers: Optional[int] = None
    first_on_demand: Optional[int] = None
    root_volume_size_in_gb: Optional[int] = None
    extra_pip_dependencies: Optional[List[str]] = None
    spark_config: Optional[Dict[str, str]] = None
    emr_version: str = DEFAULT_SPARK_VERSIONS["emr_spark_version"]
    python_version: Optional[str] = None

    def _get_python_version(self) -> str:
        if self.python_version is not None:
            return self.python_version

        if self.emr_version.startswith("emr-6."):
            return "python_3_9_13"
        else:
            return "default"

    def _to_proto(self) -> feature_view_pb2.NewClusterConfig:
        proto = feature_view_pb2.NewClusterConfig()
        python_version = self._get_python_version()

        if self.instance_type:
            proto.instance_type = self.instance_type
        if self.instance_availability:
            if self.instance_availability not in EMR_SUPPORTED_AVAILABILITY:
                msg = f"Instance availability {self.instance_availability} is not supported. Choose one of {EMR_SUPPORTED_AVAILABILITY}"
                raise ValueError(msg)
            proto.instance_availability = self.instance_availability
        if self.emr_version not in EMR_SUPPORTED_SPARK:
            msg = f"EMR version {self.emr_version} is not supported. Supported versions: {_build_pretty_string_from_supported_versions(EMR_SUPPORTED_SPARK)}"
            raise ValueError(msg)
        if python_version not in PYTHON_VERSION_EMR:
            msg = (
                f"Python version {python_version} is not supported. Supported versions: {[*PYTHON_VERSION_EMR.keys()]}"
            )
            raise ValueError(msg)
        if self.number_of_workers:
            proto.number_of_workers = self.number_of_workers
        if self.first_on_demand:
            proto.first_on_demand = self.first_on_demand
        if self.root_volume_size_in_gb:
            proto.root_volume_size_in_gb = self.root_volume_size_in_gb
        if self.extra_pip_dependencies:
            proto.extra_pip_dependencies.extend(self.extra_pip_dependencies)
        if self.spark_config:
            spark_config = SparkConfigWrapper(spark_config_map=self.spark_config)._to_proto()
            proto.spark_config.CopyFrom(spark_config)
        proto.pinned_spark_version = self.emr_version
        proto.python_version = PYTHON_VERSION_EMR[python_version].value
        return proto

    def _to_cluster_proto(self) -> feature_view_pb2.ClusterConfig:
        return feature_view_pb2.ClusterConfig(new_emr=self._to_proto())


class EMRJsonClusterConfig(StrictModel):
    """Configuration used to specify materialization clusters using json on EMR.

    This class describes the attributes of the new clusters which are created in EMR during
    materialization jobs. Please find more details in this [User Guide](https://docs.tecton.ai/docs/materializing-features/configure-spark-materialization/configuring-job-clusters-via-json#configuring-emr-job-clusters)

    :param json: A JSON string used to directly configure the cluster used in materialization.

    """

    # Used for YAML parsing as a Pydantic discriminator.
    kind: Literal["EMRJsonClusterConfig"] = "EMRJsonClusterConfig"

    # Use json_ with an alias to avoid conflicting with a Pydantic BaseModel method json(). Shadow that method with
    # a json property so that callers can access the field intuitively.
    json_: Dict[str, Any] = pydantic_v1.Field(alias="json")

    # A Pydantic pre-validator to convert json strings to a native python object.
    _json_str_to_dict = pydantic_v1.validator("json_", allow_reuse=True, pre=True)(_str_to_json_struct)

    def _to_cluster_proto(self) -> feature_view_pb2.ClusterConfig:
        return feature_view_pb2.ClusterConfig(json_emr=_to_json_cluster_proto(self.json))

    @property
    def json(self) -> Dict[str, Any]:
        return self.json_


class DatabricksJsonClusterConfig(StrictModel):
    """Configuration used to specify materialization clusters using json on Databricks.

    This class describes the attributes of the new clusters which are created in Databricks during
    materialization jobs. Please find more details in [User Guide](https://docs.tecton.ai/docs/materializing-features/configure-spark-materialization/configuring-job-clusters-via-json#configuring-databricks-job-clusters)

    :param json: A JSON string used to directly configure the cluster used in materialization.
    """

    # Used for YAML parsing as a Pydantic discriminator.
    kind: Literal["DatabricksJsonClusterConfig"] = "DatabricksJsonClusterConfig"

    # Use json_ with an alias to avoid conflicting with a Pydantic BaseModel method json(). Shadow that method with
    # a json property so that callers can access the field intuitively.
    json_: Dict[str, Any] = pydantic_v1.Field(alias="json")

    # A Pydantic pre-validator to convert json strings to a native python object.
    _json_str_to_dict = pydantic_v1.validator("json_", allow_reuse=True, pre=True)(_str_to_json_struct)

    def _to_cluster_proto(self) -> feature_view_pb2.ClusterConfig:
        return feature_view_pb2.ClusterConfig(json_databricks=_to_json_cluster_proto(self.json))

    @property
    def json(self) -> Dict[str, Any]:
        return self.json_


class DatabricksClusterConfig(StrictModel):
    """Configuration used to specify materialization cluster options on Databricks.

    This class describes the attributes of the new clusters which are created in Databricks during
    materialization jobs. You can configure options of these clusters, like cluster size and extra pip dependencies.

    Note on `extra_pip_dependencies`: This is a list of packages that will be installed during materialization.
    To use PyPI packages, specify the package name and optionally the version, e.g. `"tensorflow"` or `"tensorflow==2.2.0"`.
    To use custom code, package it as a Python wheel or egg file in S3 or DBFS, then specify the path to the file,
    e.g. `"s3://my-bucket/path/custom.whl"`, or `"dbfs:/path/to/custom.whl"`.

    These libraries will only be available to use inside Spark UDFs. For example, if you set
    `extra_pip_dependencies=["tensorflow"]`, you can use it in your transformation as shown below.

    ```python

    from tecton import batch_feature_view, Input, DatabricksClusterConfig

    @batch_feature_view(
        sources=[credit_scores_batch],
        # Can be an argument instance to a batch feature view decorator
        batch_compute = DatabricksClusterConfig(
            instance_type = 'm5.2xlarge',
            spark_config = {"spark.executor.memory" : "12g"}
            extra_pip_dependencies=["tensorflow"],
        ),
        # Other named arguments to batch feature view
        ...
    )

    # Use the tensorflow package in the UDF since tensorflow will be installed
    # on the Databricks Spark cluster. The import has to be within the UDF body. Putting it at the
    # top of the file or inside transformation function won't work.

    @transformation(mode='pyspark')
    def test_transformation(transformation_input):
        from pyspark.sql import functions as F
        from pyspark.sql.types import IntegerType

        def my_tensorflow(x):
            import tensorflow as tf
            return int(tf.math.log1p(float(x)).numpy())

        my_tensorflow_udf = F.udf(my_tensorflow, IntegerType())

        return transformation_input.select(
            'entity_id',
            'timestamp',
            my_tensorflow_udf('clicks').alias('log1p_clicks')
        )
    ```

    :param instance_type: Instance type for the cluster. Must be a valid type as listed in [this Databricks documentation](https://databricks.com/product/aws-pricing/instance-types).
        Additionally, Graviton instances such as the m6g family are not supported. If not specified, a value determined by the Tecton backend is used.
    :param instance_availability: Instance availability for the cluster : "spot", "on_demand", or "spot_with_fallback". defaults to `spot`.
    :param first_on_demand: The first `first_on_demand` nodes of the cluster will use on_demand instances. The rest will use the type specified by instance_availability.
        If first_on_demand >= 1, the driver node use on_demand instance type.
    :param number_of_workers: Number of instances for the materialization job. If not specified, a value determined by the Tecton backend is used.
        If set to 0 then jobs will be run in single-node clusters.
    :param extra_pip_dependencies: Extra pip dependencies to be installed on the materialization cluster. Must be PyPI packages, or wheels/eggs in S3 or DBFS.
    :param spark_config: Map of Spark configuration options and their respective values that will be passed to the
        FeatureView materialization Spark cluster.
    :param dbr_version: Databricks runtime version of the cluster. Supported versions can be found on [this page](https://docs.tecton.ai/docs/materializing-features/configure-spark-materialization/using-pinned-emr-and-databricks-runtime-releases#overview)
    """

    # Used for YAML parsing as a Pydantic discriminator.
    kind: Literal["DatabricksClusterConfig"] = "DatabricksClusterConfig"
    instance_type: Optional[str] = None
    instance_availability: Optional[str] = None
    number_of_workers: Optional[int] = None
    first_on_demand: Optional[int] = None
    extra_pip_dependencies: Optional[List[str]] = None
    spark_config: Optional[Dict[str, str]] = None
    dbr_version: str = DEFAULT_SPARK_VERSIONS["databricks_spark_version"]

    def _to_proto(self) -> feature_view_pb2.NewClusterConfig:
        proto = feature_view_pb2.NewClusterConfig()
        if self.instance_type:
            proto.instance_type = self.instance_type
        if self.instance_availability:
            if self.instance_availability not in DATABRICKS_SUPPORTED_AVAILABILITY:
                msg = f"Instance availability {self.instance_availability} is not supported. Choose {AVAILABILITY_SPOT}, {AVAILABILITY_ON_DEMAND} or {AVAILABILITY_SPOT_FALLBACK}"
                raise ValueError(msg)
            proto.instance_availability = self.instance_availability
        if self.dbr_version not in DATABRICKS_SUPPORTED_SPARK:
            msg = f"Databricks version {self.dbr_version} is not supported. Supported versions: {_build_pretty_string_from_supported_versions(DATABRICKS_SUPPORTED_SPARK)}"
            raise ValueError(msg)

        if self.number_of_workers is not None:
            proto.number_of_workers = self.number_of_workers
        if self.first_on_demand:
            proto.first_on_demand = self.first_on_demand
        if self.extra_pip_dependencies:
            # Pretty easy to do e.g. extra_pip_dependencies="tensorflow" by mistake and end up with
            # [t, e, n, s, o, r, f, l, o, w] as a list of dependencies passed to the Spark job.
            #
            # Since this is annoying to debug, we check for that here.
            if isinstance(self.extra_pip_dependencies, str):
                msg = "extra_pip_dependencies must be a list"
                raise ValueError(msg)
            proto.extra_pip_dependencies.extend(self.extra_pip_dependencies)
        if self.spark_config:
            spark_config = SparkConfigWrapper(spark_config_map=self.spark_config)._to_proto()
            proto.spark_config.CopyFrom(spark_config)
        proto.pinned_spark_version = self.dbr_version

        return proto

    def _to_cluster_proto(self) -> feature_view_pb2.ClusterConfig:
        return feature_view_pb2.ClusterConfig(new_databricks=self._to_proto())


class RiftBatchConfig(StrictModel):
    """Configuration used to specify materialization compute options on Rift.

    :param instance_type: Instance type for the materialization job. Must be a valid EC2 instance type as listed in
        https://aws.amazon.com/ec2/instance-types/. If not specified, a value determined by the Tecton backend is used.
    :param root_volume_size_in_gb: Size of the root volume in GB per instance for the materialization job.
        If not specified, a value determined by the Tecton backend is used. Defaults to "150".
    """

    # Used for YAML parsing as a Pydantic discriminator.
    kind: Literal["RiftBatchConfig"] = "RiftBatchConfig"
    instance_type: Optional[str] = None
    root_volume_size_in_gb: int = 500

    def _to_proto(self) -> feature_view_pb2.RiftClusterConfig:
        proto = feature_view_pb2.RiftClusterConfig()
        if self.instance_type:
            proto.instance_type = self.instance_type

        proto.root_volume_size_in_gb = self.root_volume_size_in_gb

        return proto

    def _to_cluster_proto(self) -> feature_view_pb2.ClusterConfig:
        return feature_view_pb2.ClusterConfig(rift=self._to_proto())


class SparkConfigWrapper(StrictModel):
    spark_config_map: Dict[str, str]

    HARDCODED_OPTS: ClassVar[Dict[str, str]] = {
        "spark.driver.memory": "spark_driver_memory",
        "spark.executor.memory": "spark_executor_memory",
        "spark.driver.memoryOverhead": "spark_driver_memory_overhead",
        "spark.executor.memoryOverhead": "spark_executor_memory_overhead",
    }

    def _to_proto(self):
        proto = feature_view_pb2.SparkConfig()
        for opt, val in self.spark_config_map.items():
            if opt in self.HARDCODED_OPTS:
                setattr(proto, self.HARDCODED_OPTS[opt], val)
            else:
                proto.spark_conf[opt] = val

        return proto


class ParquetConfig(StrictModel):
    """(Config Class) ParquetConfig Class.

    This class describes the attributes of Parquet-based offline feature store storage for the feature definition.

    :param subdirectory_override: This is for the location of the feature data in the offline store. By default, all feature views will be under the subdirectory <workspace_name> if this param is not specified.
    """

    kind: Literal["ParquetConfig"] = "ParquetConfig"  # Used for YAML parsing as a Pydantic discriminator.
    subdirectory_override: Optional[str] = None

    def _to_proto(self):
        store_config = feature_view_pb2.OfflineFeatureStoreConfig()
        store_config.parquet.SetInParent()
        if self.subdirectory_override:
            store_config.subdirectory_override = self.subdirectory_override
        return store_config

    @classmethod
    def from_proto(cls, proto: feature_view_pb2.OfflineFeatureStoreConfig):
        return cls(subdirectory_override=proto.subdirectory_override or None)


class DeltaConfig(StrictModel):
    """(Config Class) DeltaConfig Class.

    This class describes the attributes of DeltaLake-based offline feature store storage for the feature definition.

    :param time_partition_size: The size of a time partition in the DeltaLake table, specified as a datetime.timedelta. defaults to `24 hours`.
    :param subdirectory_override: This is for the location of the feature data in the offline store. By default, all feature views will be under the subdirectory <workspace_name> if this param is not specified.
    """

    kind: Literal["DeltaConfig"] = "DeltaConfig"  # Used for YAML parsing as a Pydantic discriminator.
    time_partition_size: Optional[datetime.timedelta] = datetime.timedelta(hours=24)
    subdirectory_override: Optional[str] = None

    @pydantic_v1.validator("time_partition_size", pre=True)
    def _string_to_timedelta(cls, value):
        if isinstance(value, str):
            return time_utils.parse_to_timedelta(value)
        return value

    def _to_proto(self):
        store_config = feature_view_pb2.OfflineFeatureStoreConfig()
        store_config.delta.time_partition_size.FromTimedelta(self.time_partition_size)
        if self.subdirectory_override:
            store_config.subdirectory_override = self.subdirectory_override
        return store_config

    @classmethod
    def from_proto(cls, proto: feature_view_pb2.OfflineFeatureStoreConfig):
        return cls(subdirectory_override=proto.subdirectory_override or None)


class OfflineStoreConfig(StrictModel):
    """Configuration options to specify how a Feature View should materialize to the Offline Store.

    :param staging_table_format: The table format for the staging table. The staging table contains partially
        transformed feature values that have not been fully aggregated.
    :param publish_full_features: If True, Tecton will publish a full feature values to a separate table after
        materialization jobs to the staging table have completed. Users can query these feature values directly
        without further transformations or aggregations.
    :param publish_start_time: If set, Tecton will publish features starting from the feature time. If not set,
        Tecton will default to the Feature View's feature_start_time.
    """

    # Import IcebergConfig locally to avoid circular dependency
    from tecton.vnext import IcebergConfig

    kind: Literal["OfflineStoreConfig"] = "OfflineStoreConfig"  # Used for YAML parsing as a Pydantic discriminator.
    staging_table_format: Union[DeltaConfig, ParquetConfig, IcebergConfig] = pydantic_v1.Field(
        default_factory=DeltaConfig, discriminator="kind"
    )
    publish_full_features: bool = False
    publish_start_time: Optional[datetime.datetime] = None

    @pydantic_v1.validator("publish_start_time", pre=True)
    def _date_to_datetime(cls, value):
        if isinstance(value, datetime.date):
            return datetime.datetime(year=value.year, month=value.month, day=value.day)
        return value

    def _to_proto(self) -> feature_view_pb2.OfflineStoreConfig:
        return feature_view_pb2.OfflineStoreConfig(
            staging_table_format=self.staging_table_format._to_proto(),
            publish_full_features=self.publish_full_features,
            publish_start_time=time_utils.datetime_to_proto(self.publish_start_time),
        )


class DynamoConfig(StrictModel):
    """(Config Class) DynamoConfig Class.

    This class describes the attributes of DynamoDB based online feature store for the feature definition.
    Users can specify online_store = DynamoConfig()

    :param replica_regions: A list of AWS regions to constrain replication of the online store to.
        If not specified, the online store will be replicated to all available regions. An empty list
        indicates that the DynamoDB table will only exist in the primary region, and will not be
        replicated to any other regions. Only regions that are configured for the Tecton deployment
        are valid inputs.
    """

    kind: Literal["DynamoConfig"] = "DynamoConfig"  # Used for YAML parsing as a Pydantic discriminator.
    replica_regions: Optional[List[str]] = None

    def _to_proto(self):
        dynamo_config = feature_view_pb2.DynamoDbOnlineStore(enabled=True)
        if self.replica_regions is not None:
            dynamo_config.replica_regions.values.extend(self.replica_regions)
        return feature_view_pb2.OnlineStoreConfig(dynamo=dynamo_config)


class RedisConfig(StrictModel):
    """(Config Class) RedisConfig Class.

    This class describes the attributes of Redis-based online feature store for the feature definition.
    Note : Your Tecton deployment needs to be connected to Redis before you can use this configuration option. See https://docs.tecton.ai/docs/setting-up-tecton/setting-up-other-components/connecting-redis-as-an-online-store for details and please contact Tecton Support if you need assistance.

    :param primary_endpoint: Primary endpoint for the Redis Cluster. This is optional and if absent, Tecton will use the default Redis Cluster configured for your deployment.
    :param authentication_token: Authentication token for the Redis Cluster, must be provided if primary_endpoint is present.
    """

    kind: Literal["RedisConfig"] = "RedisConfig"  # Used for YAML parsing as a Pydantic discriminator.
    primary_endpoint: Optional[str] = None
    authentication_token: Optional[str] = None

    def _to_proto(self):
        # TODO(TEC-13889): Remove the tls_enabled field from proto and backend as this should always be set to true
        return feature_view_pb2.OnlineStoreConfig(
            redis=feature_view_pb2.RedisOnlineStore(
                enabled=True,
                primary_endpoint=self.primary_endpoint,
                authentication_token=self.authentication_token,
            )
        )


class BigtableConfig(StrictModel):
    """(Config Class) BigtableConfig Class.

    This class describes the attributes of Bigtable based online feature store for the feature definition.
    Currently there are no attributes for this class.
    Users can specify online_store = BigtableConfig()

    """

    kind: Literal["BigtableConfig"] = "BigtableConfig"  # Used for YAML parsing as a Pydantic discriminator.

    def _to_proto(self):
        store_config = feature_view_pb2.OnlineStoreConfig()
        store_config.bigtable.enabled = True
        store_config.bigtable.SetInParent()
        return store_config


class MonitoringConfig(StrictModel):
    """Configuration used to specify monitoring options.

    This class describes the FeatureView materialization freshness and alerting configurations. Requires
    materialization to be enabled. Freshness monitoring requires online materialization to be enabled.
    See `Monitoring Materialization`_ for more details.


    An example declaration of a MonitorConfig

    ```python
    from datetime import timedelta
    from tecton import batch_feature_view, Input, MonitoringConfig
    # For all named arguments to the batch feature view, see docs for details and types.
    @batch_feature_view(
        sources=[credit_scores_batch],
        # Can be an argument instance to a batch feature view decorator
        monitoring = MonitoringConfig(
            monitor_freshness=True,
            expected_freshness=timedelta(weeks=1),
            alert_email="brian@tecton.ai"
        ),
        # Other named arguments
        ...
    )

    # Your batch feature view function
    def credit_batch_feature_view(credit_scores):
      ...
    ```

    _Monitoring Materialization: https://docs.tecton.ai/docs/monitoring/monitoring-materialization

    :param monitor_freshness: Defines the enabled/disabled state of monitoring when feature data is materialized to the online feature store.
    :type monitor_freshness: bool
    :param expected_freshness: Threshold used to determine if recently materialized feature data is stale.
        Data is stale if `now - anchor_time(most_recent_feature_value) > expected_freshness`.
        Value must be at least 2 times the feature tile length.
        If not specified, a value determined by the Tecton backend is used
    :type expected_freshness: timedelta, optional
    :param alert_email: Email that alerts for this FeatureView will be sent to.
    :type alert_email: str, optional
    """

    monitor_freshness: bool
    expected_freshness: Optional[datetime.timedelta] = None
    alert_email: Optional[str] = None

    def _to_proto(self) -> feature_view_pb2.MonitoringConfig:
        proto = feature_view_pb2.MonitoringConfig()

        if self.expected_freshness:
            proto.expected_freshness.FromTimedelta(self.expected_freshness)

        proto.alert_email = self.alert_email or ""
        proto.monitor_freshness = self.monitor_freshness
        return proto


class LoggingConfig(StrictModel):
    """
    Configuration used to describe feature and request logging for Feature Services.

    An example of LoggingConfig declaration as part of FeatureService

    ```python
    from tecton import FeatureService, LoggingConfig

    # LoggingConfig is normaly used as a named argument parameter to a FeatureService instance definition.
    my_feature_service = FeatureService(
        name="An example of Feature Service"
        # Other named arguments
        ...
        # A LoggingConfig instance
        logging=LoggingConfig(
                sample_rate=0.5,
                log_effective_times=False,
        )
        ...
    )
    ```

    :param sample_rate: The rate of logging features. Must be between (0, 1]. defaults to `1`.
    :param log_effective_times: Whether to log the timestamps of the last update of the logged feature values. defaults to `False`.
    """

    sample_rate: float = 1.0
    log_effective_times: bool = False

    def _to_proto(self) -> feature_service_pb2.LoggingConfigArgs:
        return feature_service_pb2.LoggingConfigArgs(
            sample_rate=self.sample_rate, log_effective_times=self.log_effective_times
        )

    @classmethod
    def _from_proto(cls, logging_config_proto: feature_service_pb2.LoggingConfigArgs) -> "LoggingConfig":
        return LoggingConfig(logging_config_proto.sample_rate, logging_config_proto.log_effective_times)


class OutputStream(StrictModel):
    """Base class for output stream configs."""

    def _to_proto() -> feature_view_pb2.OutputStream:
        raise NotImplementedError

    @classmethod
    def from_proto(cls, proto: feature_view_pb2.OutputStream):
        raise NotImplementedError


class KinesisOutputStream(OutputStream):
    """Configuration used for a Kinesis output stream.

    :param stream_name: Name of the Kinesis stream.
    :param region: AWS region of the stream, e.g: "us-west-2".
    :param options: A map of additional Spark readStream options. Only `roleArn` is supported.
    :param include_features: Return feature values in addition to entity keys. Not supported for window aggregate Feature Views.
    """

    stream_name: str
    region: str
    options: Optional[Dict[str, str]] = None
    include_features: bool = False

    def _to_proto(self) -> feature_view_pb2.OutputStream:
        args = data_source_pb2.KinesisDataSourceArgs(
            stream_name=self.stream_name,
            region=self.region,
        )
        options = self.options or {}
        for key in sorted(options.keys()):
            option = data_source_pb2.Option(
                key=key,
                value=options[key],
            )
            args.options.append(option)

        return feature_view_pb2.OutputStream(
            include_features=self.include_features,
            kinesis=args,
        )

    @classmethod
    def from_proto(cls, proto: feature_view_pb2.OutputStream):
        raw_options = proto.kinesis.options
        if raw_options:
            options = {option.key: option.value for option in raw_options}
        else:
            options = None
        return cls(
            stream_name=proto.kinesis.stream_name,
            region=proto.kinesis.region,
            options=options,
            include_features=proto.include_features,
        )


class KafkaOutputStream(OutputStream):
    """Configuration used for a Kafka output stream.

    :param kafka_bootstrap_servers: The list of bootstrap servers for your Kafka brokers, e.g: "abc.xyz.com:xxxx,abc2.xyz.com:xxxx".
    :param topics: A comma-separated list of Kafka topics the record will be appended to. Currently only supports one topic.
    :param options: A map of additional Spark readStream options. Only `roleArn` is supported at the moment.
    :param include_features: Return feature values in addition to entity keys. Not supported for window aggregate Feature Views.
    """

    kafka_bootstrap_servers: str
    topics: str
    options: Optional[Dict[str, str]] = None
    include_features: bool = False

    def _to_proto(self) -> feature_view_pb2.OutputStream:
        args = data_source_pb2.KafkaDataSourceArgs(
            kafka_bootstrap_servers=self.kafka_bootstrap_servers,
            topics=self.topics,
        )
        options = self.options or {}
        for key in sorted(options.keys()):
            option = data_source_pb2.Option(
                key=key,
                value=options[key],
            )
            args.options.append(option)

        return feature_view_pb2.OutputStream(
            include_features=self.include_features,
            kafka=args,
        )

    @classmethod
    def from_proto(cls, proto: feature_view_pb2.OutputStream):
        raw_options = proto.kafka.options
        if raw_options:
            options = {option.key: option.value for option in raw_options}
        else:
            options = None

        return cls(
            kafka_bootstrap_servers=proto.kafka.kafka_bootstrap_servers,
            topics=proto.kafka.topics,
            options=options,
            include_features=proto.include_features,
        )


class DatetimePartitionColumn(StrictModel):
    """Helper class to tell Tecton how underlying flat files are date/time partitioned for Hive/Glue data sources. This can translate into a significant performance increase.

    You will generally include an object of this class in the `datetime_partition_columns` option in a `HiveConfig` object.

    Example definitions: Assume you have an S3 bucket with parquet files stored in the following structure: `s3://mybucket/2022/05/04/<multiple parquet files>` , where `2022` is the year, `05` is the month, and `04` is the day of the month. In this scenario, you could use the following definition:

    ```python
    datetime_partition_columns = [
        DatetimePartitionColumn(column_name="partition_0", datepart="year", zero_padded=True),
        DatetimePartitionColumn(column_name="partition_1", datepart="month", zero_padded=True),
        DatetimePartitionColumn(column_name="partition_2", datepart="day", zero_padded=True),
    ]
    batch_config = HiveConfig(
        database='my_db',
        table='my_table',
        timestamp_field='timestamp',
        datetime_partition_columns=datetime_partition_columns,
    )
    ```

    ```python
    datetime_partition_columns = [
        DatetimePartitionColumn(column_name="partition_1", datepart="month", format_string="%Y-%m"),
    ]
    ```

    :param column_name: The name of the column in the Glue/Hive schema that corresponds to the underlying date/time partition folder. Note that if you do not explicitly specify a name in your partition folders, Glue will name the column of the form `partition_0`.
    :param datepart: The part of the date that this column specifies. Can be one of "year", "month", "day", "hour", or the full "date". If used with `format_string`, this should be the size of partition being represented, e.g. `datepart="month"` for `format_string="%Y-%m"`.
    :param zero_padded: Whether the `datepart` has a leading zero if less than two digits. This must be set to True if `datepart="date"`. (Should not be set if `format_string` is set.)
    :param format_string: A `datetime.strftime` format string override for "non-default" partition columns formats. E.g. `"%Y%m%d"` for `datepart="date"` instead of the Tecton default `"%Y-%m-%d"`, or `"%Y-%m"` for `datepart="month"` instead of the Tecton default `"%m"`.
    """

    #: The name of the column in the Glue/Hive schema that corresponds to the underlying date/time partition folder.
    column_name: Optional[str]

    #: The part of the date that this column specifies. Can be one of "year", "month", "day", "hour", or the full "date".
    datepart: str

    #: Whether the `datepart` has a leading zero if less than two digits.
    zero_padded: bool = False

    #: A `datetime.strftime` format string override for "non-default" partition columns formats.
    format_string: Optional[str] = None


DEFAULT_REQUEST_SOURCE_NAME = "request_source"


class RequestSource(StrictModel):
    """Declare a `RequestSource`, for using request-time data in an `RealtimeFeatureView`.

    Example of a RequestSource declaration:
    ```python
    from tecton import RequestSource
    from tecton.types import Field, Float64

    schema = [Field('amount', Float64)]
    transaction_request = RequestSource(schema=schema)
    ```

    Attributes:
        name: Unique, human friendly name that identifies the RequestSource.
        schema: The schema of this Request Source.
    """

    # Use schema_ with an alias to avoid conflicting with a Pydantic BaseModel method schema(). Shadow that method with
    # a schema property so that callers can access the field intuitively.
    schema_: Tuple[Field, ...] = pydantic_v1.Field(alias="schema")
    name: Optional[str] = DEFAULT_REQUEST_SOURCE_NAME

    def __init__(self, schema: Sequence[Field], name: Optional[str] = DEFAULT_REQUEST_SOURCE_NAME):
        """
        :param schema: The schema of this Request Source.
        :param name: Optional name for the request source.
        """
        super().__init__(schema=tuple(schema), name=name)

    @property
    def schema(self) -> Tuple[Field, ...]:
        return self.schema_


# TODO(jake): Should inherit from StrictModel.
class BaseStreamConfig:
    def _merge_stream_args(self, data_source_args: virtual_data_source_pb2.VirtualDataSourceArgs):
        raise NotImplementedError


# TODO(jake): Should inherit from StrictModel.
class BaseBatchConfig:
    @property
    def data_delay(self) -> datetime.timedelta:
        raise NotImplementedError

    def _merge_batch_args(self, data_source_args: virtual_data_source_pb2.VirtualDataSourceArgs):
        raise NotImplementedError


class FileConfig(BaseBatchConfig):
    """
    Configuration used to reference a file or directory (S3, etc.)

    The FileConfig class is used to create a reference to a file or directory of files in S3,
    HDFS, or DBFS.

    The schema of the data source is inferred from the underlying file(s). It can also be modified using the
    `post_processor` parameter.

    This class is used as an input to a `DataSource`'s parameter `batch_config`. Declaring this configuration class alone
    will not register a Data Source. Instead, declare as a part of `BatchSource` that takes this configuration class
    instance as a parameter.
    """

    def __init__(
        self,
        uri: str,
        file_format: str,
        timestamp_field: Optional[str] = None,
        timestamp_format: Optional[str] = None,
        datetime_partition_columns: Optional[List[DatetimePartitionColumn]] = None,
        post_processor: Optional[Callable] = None,
        schema_uri: Optional[str] = None,
        schema_override: Optional[StructType] = None,
        data_delay: datetime.timedelta = datetime.timedelta(seconds=0),
    ):
        """
        Instantiates a new FileConfig.

        Example of a FileConfig declaration:

        ```python
        from tecton import FileConfig, BatchSource

        # Define a post-processor function to convert the temperature from Celsius to Fahrenheit
        def convert_temperature(df):
            from pyspark.sql.functions import udf,col
            from pyspark.sql.types import DoubleType

            udf_convert = udf(lambda x: x * 1.8 + 32.0, DoubleType())
            converted_df = df.withColumn("Fahrenheit", udf_convert(col("Temperature"))).drop("Temperature")
            return converted_df

        # Declare a FileConfig, which can be used as a parameter to a `BatchSource`
        ad_impressions_file_config = FileConfig(uri="s3://tecton.ai.public/data/ad_impressions_sample.parquet",
                                                file_format="parquet",
                                                timestamp_field="timestamp",
                                                post_processor=convert_temperature)

        # This FileConfig can then be included as a parameter for a BatchSource declaration.
        # For example,
        ad_impressions_batch = BatchSource(name="ad_impressions_batch",
                                           batch_config=ad_impressions_file_config)
        ```

        :param uri: S3 or HDFS path to file(s).
        :param file_format: File format. "json", "parquet", or "csv"
        :param timestamp_field: The timestamp column in this data source that should be used for time-based filtering. Required unless this source is used in Feature Views only with `unfiltered()`.
        :param timestamp_format: Format of string-encoded timestamp column (e.g. "yyyy-MM-dd'T'hh:mm:ss.SSS'Z'").
                                 If the timestamp string cannot be parsed with this format, Tecton will fallback and attempt to
                                 use the default timestamp parser.
        :param datetime_partition_columns: List of DatetimePartitionColumn the raw data is partitioned by, otherwise None.
        :param post_processor: Python user defined function `f(DataFrame) -> DataFrame` that takes in raw
                                     Pyspark data source DataFrame and translates it to the DataFrame to be
                                     consumed by the Feature View.
        :param schema_uri: A file or subpath of "uri" that can be used for fast schema inference.
                           This is useful for speeding up plan computation for highly partitioned data sources containing many files.
        :param schema_override: A pyspark.sql.types.StructType object that will be used as the schema when
                                reading from the file. If omitted, the schema will be inferred automatically.
        :param data_delay: This parameter configures how long materialization jobs wait after the end
                                of the batch schedule period before starting, typically to ensure that all data has landed.
                                For example, if a feature view has a `batch_schedule` of 1 day and one of
                                the data source inputs has `data_delay=timedelta(hours=1)` set, then
                                incremental materialization jobs will run at `01:00` UTC.
        :return: A `FileConfig` class instance.
        """
        self._args = data_source_pb2.FileDataSourceArgs()
        self._args.uri = uri
        self._args.file_format = file_format
        if schema_uri is not None:
            self._args.schema_uri = schema_uri
        if datetime_partition_columns:
            for column in datetime_partition_columns:
                column_args = data_source_pb2.DatetimePartitionColumnArgs()
                column_args.datepart = column.datepart
                column_args.zero_padded = column.zero_padded
                if column.column_name:
                    column_args.column_name = column.column_name
                if column.format_string:
                    column_args.format_string = column.format_string
                self._args.datetime_partition_columns.append(column_args)
        if post_processor is not None and function_serialization.should_serialize_function(post_processor):
            self._args.common_args.post_processor.CopyFrom(function_serialization.to_proto(post_processor))
        if timestamp_field:
            self._args.common_args.timestamp_field = timestamp_field
        if timestamp_format:
            self._args.timestamp_format = timestamp_format
        if schema_override:
            self._args.schema_override.CopyFrom(spark_schema_wrapper.SparkSchemaWrapper(schema_override).to_proto())

        self._args.common_args.data_delay.FromTimedelta(data_delay)
        self._data_delay = data_delay
        self.post_processor = post_processor

    @property
    def data_delay(self) -> datetime.timedelta:
        """Returns the duration that materialization jobs wait after the batch_schedule before starting, typically to ensure that all data has landed."""
        return self._data_delay

    def _merge_batch_args(self, data_source_args: virtual_data_source_pb2.VirtualDataSourceArgs):
        data_source_args.file_ds_config.CopyFrom(self._args)


class KafkaConfig(BaseStreamConfig):
    """
    The KafkaConfig class is used to create a reference to a Kafka stream.

    This class is used as an input to a `StreamSource`'s parameter `stream_config`. Declaring this configuration
    class alone will not register a Data Source. Instead, declare as a part of `StreamSource` that takes this configuration
    class instance as a parameter.

    ```python
        import datetime
        import pyspark
        from tecton import KafkaConfig


        def raw_data_deserialization(df: pyspark.sql.DataFrame) -> pyspark.sql.DataFrame:
            from pyspark.sql.functions import from_json, col
            from pyspark.sql.types import StringType, TimestampType

            PAYLOAD_SCHEMA = StructType().add("accountId", StringType(), False).add("transaction_id", StringType(), False)

            EVENT_ENVELOPE_SCHEMA = StructType().add("timestamp", TimestampType(), False).add("payload", PAYLOAD_SCHEMA, False)

            value = col("value").cast("string")
            df = df.withColumn("event", from_json(value, EVENT_ENVELOPE_SCHEMA))
            df = df.withColumn("accountId", col("event.payload.accountId"))
            df = df.withColumn("transaction_id", col("event.payload.transaction_id"))
            df = df.withColumn("timestamp", col("event.timestamp"))

            return df


        # Declare Kafka Config instance object that can be used as an argument in StreamSource
        click_stream_kafka_ds = KafkaConfig(
            kafka_bootstrap_servers="127.0.0.1:12345",
            topics="click-events-json",
            timestamp_field="click_event_timestamp",
            post_processor=raw_data_deserialization,
        )
    ```
    """

    def __init__(
        self,
        kafka_bootstrap_servers: str,
        topics: str,
        post_processor,
        timestamp_field: str,
        watermark_delay_threshold: datetime.timedelta = datetime.timedelta(hours=24),
        options: Optional[Dict[str, str]] = None,
        ssl_keystore_location: Optional[str] = None,
        ssl_keystore_password_secret_id: Optional[str] = None,
        ssl_truststore_location: Optional[str] = None,
        ssl_truststore_password_secret_id: Optional[str] = None,
        security_protocol: Optional[str] = None,
        deduplication_columns: Optional[List[str]] = None,
    ):
        """
        Instantiates a new KafkaConfig.

        :param kafka_bootstrap_servers: A comma-separated list of the Kafka bootstrap server addresses. Passed directly
                                        to the Spark `kafka.bootstrap.servers` option.
        :param topics: A comma-separated list of Kafka topics to subscribe to. Passed directly to the Spark `subscribe`
                       option.
        :param post_processor: Python user defined function `f(DataFrame) -> DataFrame` that takes in raw
                                      Pyspark data source DataFrame and translates it to the DataFrame to be
                                      consumed by the Feature View. See an example of
                                      post_processor in the [User Guide](https://docs.tecton.ai/docs/defining-features/data-sources/creating-a-data-source/creating-and-testing-a-streaming-data-source#write-the-stream-message-post-processor-function).
        :param timestamp_field: Name of the column containing timestamp for watermarking.
        :param watermark_delay_threshold: Watermark time interval, e.g: timedelta(hours=36), used by Spark Structured Streaming to account for late-arriving data. See: [Productionizing a Stream](https://docs.tecton.ai/docs/defining-features/feature-views/stream-feature-view#productionizing-a-stream). defaults to `24h`.
        :param options: A map of additional Spark readStream options
        :param ssl_keystore_location: An DBFS (Databricks only) or S3 URI that points to the keystore file that should be used for SSL brokers. Note for S3 URIs, this must be configured by your Tecton representative.
            Example: `s3://tecton-<deployment name>/kafka-credentials/kafka_client_keystore.jks`
            Example: `dbfs:/kafka-credentials/kafka_client_keystore.jks`
        :param ssl_keystore_password_secret_id: The config key for the password for the Keystore.
            Should start with `SECRET_`, example: `SECRET_KAFKA_PRODUCTION`.
        :param ssl_truststore_location: An DBFS (Databricks only) or S3 URI that points to the truststore file that should be used for SSL brokers. Note for S3 URIs, this must be configured by your Tecton representative. If not provided, the default truststore for your compute provider will be used. Note that this is required for AWS-signed keystores on Databricks.
            Example: `s3://tecton-<deployment name>/kafka-credentials/kafka_client_truststore.jks`
            Example: `dbfs:/kafka-credentials/kafka_client_truststore.jks`
        :param ssl_truststore_password_secret_id: The config key for the password for the Truststore.
            Should start with `SECRET_`, example: `SECRET_KAFKA_PRODUCTION`.
        :param security_protocol: Security protocol passed to kafka.security.protocol. See Kafka documentation for valid values.
        :param deduplication_columns: Columns in the stream data that uniquely identify data records.
                                        Used for de-duplicating. Spark will drop rows if there are duplicates in the deduplication_columns, but only within the watermark delay window.

        :return: A KafkaConfig class instance.
        """
        self._args = args = data_source_pb2.KafkaDataSourceArgs()
        args.kafka_bootstrap_servers = kafka_bootstrap_servers
        args.topics = topics
        if function_serialization.should_serialize_function(post_processor):
            args.common_args.post_processor.CopyFrom(function_serialization.to_proto(post_processor))
        args.common_args.timestamp_field = timestamp_field
        if watermark_delay_threshold:
            args.common_args.watermark_delay_threshold.FromTimedelta(watermark_delay_threshold)
        for key in sorted((options or {}).keys()):
            option = data_source_pb2.Option()
            option.key = key
            option.value = options[key]
            args.options.append(option)
        if ssl_keystore_location:
            args.ssl_keystore_location = ssl_keystore_location
        if ssl_keystore_password_secret_id:
            args.ssl_keystore_password_secret_id = ssl_keystore_password_secret_id
        if ssl_truststore_location:
            args.ssl_truststore_location = ssl_truststore_location
        if ssl_truststore_password_secret_id:
            args.ssl_truststore_password_secret_id = ssl_truststore_password_secret_id
        if security_protocol:
            args.security_protocol = security_protocol
        if deduplication_columns:
            for column_name in deduplication_columns:
                args.common_args.deduplication_columns.append(column_name)

        self.post_processor = post_processor

    def _merge_stream_args(self, data_source_args: virtual_data_source_pb2.VirtualDataSourceArgs):
        data_source_args.kafka_ds_config.CopyFrom(self._args)


class KinesisConfig(BaseStreamConfig):
    """
    The KinesisConfig class is used to create a reference to an AWS Kinesis stream.

    This class is used as an input to a `StreamSource`'s parameter `stream_config`. Declaring this configuration
    class alone will not register a Data Source. Instead, declare as a part of `StreamSource` that takes this configuration
    class instance as a parameter.

    ```python
    import pyspark
    from tecton import KinesisConfig


    # Define our deserialization raw stream translator
    def raw_data_deserialization(df: pyspark.sql.DataFrame) -> pyspark.sql.DataFrame:
        from pyspark.sql.functions import col, from_json, from_utc_timestamp
        from pyspark.sql.types import StructType, StringType

        payload_schema = (
            StructType()
            .add("amount", StringType(), False)
            .add("isFraud", StringType(), False)
            .add("timestamp", StringType(), False)
        )

        return (
            df.selectExpr("cast (data as STRING) jsonData")
            .select(from_json("jsonData", payload_schema).alias("payload"))
            .select(
                col("payload.amount").cast("long").alias("amount"),
                col("payload.isFraud").cast("long").alias("isFraud"),
                from_utc_timestamp("payload.timestamp", "UTC").alias("timestamp"),
            )
        )


    # Declare KinesisConfig instance object that can be used as argument in `StreamSource`
    stream_config = KinesisConfig(
        stream_name="transaction_events",
        region="us-west-2",
        initial_stream_position="latest",
        timestamp_field="timestamp",
        post_processor=raw_data_deserialization,
        options={"roleArn": "arn:aws:iam::472542229217:role/demo-cross-account-kinesis-ro"},
    )
    ```
    """

    def __init__(
        self,
        stream_name: str,
        region: str,
        post_processor,
        timestamp_field: str,
        initial_stream_position: str,
        watermark_delay_threshold: datetime.timedelta = datetime.timedelta(hours=24),
        deduplication_columns: Optional[List[str]] = None,
        options: Optional[Dict[str, str]] = None,
    ):
        """
        Instantiates a new KinesisConfig.

        :param stream_name: Name of the Kinesis stream.
        :param region: AWS region of the stream, e.g: "us-west-2".
        :param post_processor: Python user defined function `f(DataFrame) -> DataFrame` that takes in raw
                                      Pyspark data source DataFrame and translates it to the DataFrame to be
                                      consumed by the Feature View. See an example of
                                      post_processor in the [User Guide](https://docs.tecton.ai/docs/defining-features/data-sources/creating-a-data-source/creating-and-testing-a-streaming-data-source#write-the-stream-message-post-processor-function).
        :param timestamp_field: Name of the column containing timestamp for watermarking.
        :param initial_stream_position: Initial position in stream, e.g: "latest" or "trim_horizon".
                                                More information available in [Spark Kinesis Documentation](https://spark.apache.org/docs/latest/streaming-kinesis-integration.html).
        :param watermark_delay_threshold: Watermark time interval, e.g: timedelta(hours=36), used by Spark Structured Streaming to account for late-arriving data. See: [Productionizing a Stream](https://docs.tecton.ai/docs/defining-features/feature-views/stream-feature-view#productionizing-a-stream). defaults to `24h`.
        :param deduplication_columns: Columns in the stream data that uniquely identify data records.
                                        Used for de-duplicating.
        :param options: A map of additional Spark readStream options

        :return: A KinesisConfig class instance.
        """
        args = data_source_pb2.KinesisDataSourceArgs()
        args.stream_name = stream_name
        args.region = region
        if function_serialization.should_serialize_function(post_processor):
            args.common_args.post_processor.CopyFrom(function_serialization.to_proto(post_processor))
        args.common_args.timestamp_field = timestamp_field
        if initial_stream_position:
            args.initial_stream_position = data_source_helper.INITIAL_STREAM_POSITION_STR_TO_ENUM[
                initial_stream_position
            ]
        if watermark_delay_threshold:
            args.common_args.watermark_delay_threshold.FromTimedelta(watermark_delay_threshold)
        if deduplication_columns:
            for column_name in deduplication_columns:
                args.common_args.deduplication_columns.append(column_name)
        options_ = options or {}
        for key in sorted(options_.keys()):
            option = data_source_pb2.Option()
            option.key = key
            option.value = options_[key]
            args.options.append(option)

        self._args = args
        self.post_processor = post_processor

    def _merge_stream_args(self, data_source_args: virtual_data_source_pb2.VirtualDataSourceArgs):
        data_source_args.kinesis_ds_config.CopyFrom(self._args)


class PushConfig(BaseStreamConfig):
    """
    The PushConfig class is used to configure the [Stream Ingest API](https://docs.tecton.ai/docs/defining-features/feature-views/stream-feature-view/stream-feature-view-with-rift) to allow ingestion of
    records via the Stream Ingest API.

    Declaring this configuration class alone will not register a Data Source. Instead, declare as a part of
    `StreamSource` that takes this configuration class instance as a parameter.

    ```python
    from tecton import PushConfig

    stream_config = PushConfig(log_offline=False)
    ```
    """

    def __init__(
        self,
        log_offline: bool = False,
        post_processor: Optional[
            Union[Callable[[Dict], Optional[Dict]], Callable[[pandas.DataFrame], Optional[pandas.DataFrame]]]
        ] = None,
        post_processor_mode: Optional[str] = None,
        input_schema: Optional[List[types.Field]] = None,
        timestamp_field: Optional[str] = None,
        ingest_server_group: Optional[str] = None,
        transform_server_group: Optional[str] = None,
    ):
        """
        Instantiates a new PushConfig.

        :param log_offline: If set to True, the [Stream Ingest API](https://docs.tecton.ai/docs/defining-features/feature-views/stream-feature-view/stream-feature-view-with-rift) will log the incoming records for the push source to an offline table.
        :param post_processor: A user-defined function that processes records coming from the source; the output of the `post_processor` is used in subsequent stages.
        :param post_processor_mode: Execution mode for the `post_processor`, must be one of `python` or `pandas`
        :param input_schema: Input schema for the `post_processor`
        :param timestamp_field: Name of the timestamp column which Tecton uses for watermarking.
        :param ingest_server_group: The Ingest Server Group responsible for handling requests for this Push Stream Source. Note: This feature is currently in Preview.
        :param transform_server_group: The Transform Server Group to use for running stream feature view transformations. This will be used as the default transform_server_group for any stream feature views that use this stream source and don't specify their own transform_server_group.

        :return: A PushConfig class instance.
        """
        # TODO: Remove offline logging in 1.2
        if log_offline:
            logger.warning(
                "Deprecation Warning: Tecton-managed offline logging (i.e. stream_config=PushConfig(log_offline=True)) in a StreamSource is deprecated and will be removed in Tecton 1.3. This change affects all existing Tecton-managed offline logging configurations, which will need to be migrated to a self-managed offline event log by specifying a batch_config on a StreamSource for training data generation: https://docs.tecton.ai/docs/beta/defining-features/data-sources/creating-a-data-source/creating-and-testing-a-push-source#example-of-a-stream-source-with-a-self-managed-offline-event-log"
            )

        _mode = (
            get_transformation_mode_enum(mode=post_processor_mode, name="PushConfig") if post_processor_mode else None
        )
        if post_processor is not None and function_serialization.should_serialize_function(post_processor):
            _post_processor_function = function_serialization.to_proto(post_processor)
        else:
            _post_processor_function = None

        tecton_schema = type_utils.to_tecton_schema(input_schema) if input_schema else None

        self._args = data_source_pb2.PushSourceArgs(
            log_offline=log_offline,
            post_processor=_post_processor_function,
            post_processor_mode=_mode,
            input_schema=tecton_schema,
            timestamp_field=timestamp_field,
            ingest_server_group=ingest_server_group,
            transform_server_group=transform_server_group,
        )

    def _merge_stream_args(self, data_source_args: virtual_data_source_pb2.VirtualDataSourceArgs):
        data_source_args.push_config.CopyFrom(self._args)


class HiveConfig(BaseBatchConfig):
    """
    The HiveConfig class is used to create a reference to a Hive Table.

    This class is used as an input to a `BatchSource`'s parameter `batch_config`. Declaring this configuration
    class alone will not register a Data Source. Instead, declare as a part of `BatchSource` that takes this configuration
    class instance as a parameter.
    """

    def __init__(
        self,
        table: str,
        database: str,
        timestamp_field: Optional[str] = None,
        timestamp_format: Optional[str] = None,
        datetime_partition_columns: Optional[List[DatetimePartitionColumn]] = None,
        post_processor: Optional[Callable] = None,
        data_delay: datetime.timedelta = datetime.timedelta(seconds=0),
    ):
        """
        Instantiates a new HiveConfig.

                Example of a HiveConfig declaration:

        ```python
        from tecton import HiveConfig
        import pyspark

        def convert_temperature(df: pyspark.sql.DataFrame) -> pyspark.sql.DataFrame:
            from pyspark.sql.functions import udf,col
            from pyspark.sql.types import DoubleType

            # Convert the incoming PySpark DataFrame temperature Celsius to Fahrenheit
            udf_convert = udf(lambda x: x * 1.8 + 32.0, DoubleType())
            converted_df = df.withColumn("Fahrenheit", udf_convert(col("Temperature"))).drop("Temperature")
            return converted_df

        # declare a HiveConfig instance, which can be used as a parameter to a BatchSource
        batch_config=HiveConfig(database='global_temperatures',
                                    table='us_cities',
                                    timestamp_field='timestamp',
                                    post_processor=convert_temperature)
        ```

        :param table: A table registered in Hive MetaStore.
        :param database: A database registered in Hive MetaStore.
        :param timestamp_field: The timestamp column in this data source that should be used for time-based filtering. Required unless this source is used in Feature Views only with `unfiltered()`.
        :param timestamp_format: Format of string-encoded timestamp column (e.g. "yyyy-MM-dd'T'hh:mm:ss.SSS'Z'").
                                 If the timestamp string cannot be parsed with this format, Tecton will fallback and attempt to
                                 use the default timestamp parser.
        :param datetime_partition_columns: List of DatetimePartitionColumn the raw data is partitioned by, otherwise None.
        :param post_processor: Python user defined function `f(DataFrame) -> DataFrame` that takes in raw
                                     PySpark data source DataFrame and translates it to the DataFrame to be
                                     consumed by the Feature View.
        :param data_delay: By default, incremental materialization jobs run immediately at the end of the
                                    batch schedule period. This parameter configures how long they wait after the end
                                    of the period before starting, typically to ensure that all data has landed.
                                    For example, if a feature view has a `batch_schedule` of 1 day and one of
                                    the data source inputs has `data_delay=timedelta(hours=1)` set, then
                                    incremental materialization jobs will run at `01:00` UTC.

        :return: A HiveConfig class instance.
        """
        self._args = data_source_pb2.HiveDataSourceArgs()
        self._args.table = table
        self._args.database = database
        if timestamp_field:
            self._args.common_args.timestamp_field = timestamp_field
        if timestamp_format:
            self._args.timestamp_format = timestamp_format

        if datetime_partition_columns:
            for column in datetime_partition_columns:
                column_args = data_source_pb2.DatetimePartitionColumnArgs()
                column_args.column_name = column.column_name
                column_args.datepart = column.datepart
                column_args.zero_padded = column.zero_padded
                if column.format_string:
                    column_args.format_string = column.format_string
                self._args.datetime_partition_columns.append(column_args)
        if post_processor is not None and function_serialization.should_serialize_function(post_processor):
            self._args.common_args.post_processor.CopyFrom(function_serialization.to_proto(post_processor))

        self._args.common_args.data_delay.FromTimedelta(data_delay)
        self._data_delay = data_delay
        self.post_processor = post_processor

    @property
    def data_delay(self):
        return self._data_delay

    def _merge_batch_args(self, data_source_args: virtual_data_source_pb2.VirtualDataSourceArgs):
        data_source_args.hive_ds_config.CopyFrom(self._args)


class UnityConfig(BaseBatchConfig):
    """
    The UnityConfig class is used to create a reference to a Unity Table.

    This class is used as an input to a `BatchSource`'s parameter `batch_config`. Declaring this configuration
    class alone will not register a Data Source. Instead, declare as a part of `BatchSource` that takes this configuration
    class instance as a parameter.
    """

    def __init__(
        self,
        catalog: str,
        schema: str,
        table: str,
        timestamp_field: Optional[str] = None,
        timestamp_format: Optional[str] = None,
        datetime_partition_columns: Optional[List[DatetimePartitionColumn]] = None,
        post_processor: Optional[Callable] = None,
        data_delay: datetime.timedelta = datetime.timedelta(seconds=0),
        access_mode: UnityCatalogAccessMode = None,
    ):
        """
        Instantiates a new UnityConfig.

        :param catalog: A catalog registered in Unity
        :param schema: A schema registered in Unity
        :param table: A table registered in Unity
        :param timestamp_field: The timestamp column in this data source that should be used for time-based filtering. Required unless this source is used in Feature Views only with `unfiltered()`.
        :param timestamp_format: Format of string-encoded timestamp column (e.g. "yyyy-MM-dd'T'hh:mm:ss.SSS'Z'").
                                 If the timestamp string cannot be parsed with this format, Tecton will fallback and attempt to
                                 use the default timestamp parser.
        :param datetime_partition_columns: List of DatetimePartitionColumn the raw data is partitioned by, otherwise None.
        :param post_processor: Python user defined function `f(DataFrame) -> DataFrame` that takes in raw
                                     PySpark data source DataFrame and translates it to the DataFrame to be
                                     consumed by the Feature View.
        :param data_delay: By default, incremental materialization jobs run immediately at the end of the
                                    batch schedule period. This parameter configures how long they wait after the end
                                    of the period before starting, typically to ensure that all data has landed.
                                    For example, if a feature view has a `batch_schedule` of 1 day and one of
                                    the data source inputs has `data_delay=timedelta(hours=1)` set, then
                                    incremental materialization jobs will run at `01:00` UTC.
        :param access_mode: The Unity Catalog Access Mode for the Unity table. If not specified, uses the Single User
                                    Access Mode as default.

        :return: A UnityConfig class instance.

        """
        self._args = data_source_pb2.UnityDataSourceArgs(
            catalog=catalog,
            schema=schema,
            table=table,
            timestamp_format=timestamp_format,
            common_args=data_source_pb2.BatchDataSourceCommonArgs(
                data_delay=time_utils.timedelta_to_proto(data_delay),
                timestamp_field=timestamp_field,
            ),
            access_mode=access_mode.value if access_mode is not None else UnityCatalogAccessMode.SINGLE_USER.value,
        )

        if datetime_partition_columns:
            for column in datetime_partition_columns:
                column_args = data_source_pb2.DatetimePartitionColumnArgs(
                    column_name=column.column_name,
                    datepart=column.datepart,
                    zero_padded=column.zero_padded,
                    format_string=column.format_string,
                )
                self._args.datetime_partition_columns.append(column_args)
        if post_processor is not None and function_serialization.should_serialize_function(post_processor):
            self._args.common_args.post_processor.CopyFrom(function_serialization.to_proto(post_processor))

        self._data_delay = data_delay
        self.post_processor = post_processor

    @property
    def data_delay(self):
        return self._data_delay

    def _merge_batch_args(self, data_source_args: virtual_data_source_pb2.VirtualDataSourceArgs):
        data_source_args.unity_ds_config.CopyFrom(self._args)


class SnowflakeConfig(BaseBatchConfig):
    """
    Configuration used to reference a Snowflake table or query.

    The SnowflakeConfig class is used to create a reference to a Snowflake table. You can also create a
    reference to a query on one or more tables, which will be registered in Tecton in a similar way as a view
    is registered in other data systems.

    This class is used as an input to a `BatchSource`'s parameter `batch_config`. Declaring this configuration
    class alone will not register a Data Source. Instead, declare as a part of `BatchSource` that takes this configuration
    class instance as a parameter.
    """

    def __init__(
        self,
        *,
        database: Optional[str] = None,
        schema: Optional[str] = None,
        warehouse: Optional[str] = None,
        url: Optional[str] = None,
        role: Optional[str] = None,
        table: Optional[str] = None,
        query: Optional[str] = None,
        timestamp_field: Optional[str] = None,
        post_processor: Optional[Callable] = None,
        data_delay: datetime.timedelta = datetime.timedelta(seconds=0),
        user: Union[str, Secret, None] = None,
        password: Union[str, Secret, None] = None,
        private_key: Union[str, Secret, None] = None,
        private_key_passphrase: Union[str, Secret, None] = None,
    ):
        """
        Instantiates a new SnowflakeConfig. One of table and query should be specified when creating this file.

        Example of a SnowflakeConfig declaration:

        ```python
        from tecton import SnowflakeConfig, BatchSource

        # Declare SnowflakeConfig instance object that can be used as an argument in BatchSource
        snowflake_ds_config = SnowflakeConfig(
                                          url="https://<your-cluster>.eu-west-1.snowflakecomputing.com/",
                                          database="CLICK_STREAM_DB",
                                          schema="CLICK_STREAM_SCHEMA",
                                          warehouse="COMPUTE_WH",
                                          table="CLICK_STREAM_FEATURES",
                                          query="SELECT timestamp as ts, created, user_id, clicks, click_rate"
                                                 "FROM CLICK_STREAM_DB.CLICK_STREAM_FEATURES")

        # Use in the BatchSource
        snowflake_ds = BatchSource(name="click_stream_snowflake_ds",
                                       batch_config=snowflake_ds_config)
        ```

        :param database: The Snowflake database for this Data source.
        :param schema: The Snowflake schema for this Data source.
        :param warehouse: The Snowflake warehouse for this Data source.
        :param url: The connection URL to Snowflake, which contains account information (e.g. https://xy12345.eu-west-1.snowflakecomputing.com).
        :param role: The Snowflake role that should be used for this Data source.

        :param table: The table for this Data source. Only one of `table` and `query` must be specified. If using Rift,
                                    this table name cannot include quotation marks. For example, the
                                    table name 'foo"bar' is not supported.
        :param query: The query for this Data source. Only one of `table` and `query` must be specified.
        :param timestamp_field: The timestamp column in this data source that should be used for time-based filtering. Required unless this source is used in Feature Views only with `unfiltered()`.
        :param post_processor: (Only supported in Spark) Python user defined function `f(DataFrame) -> DataFrame` that takes in raw
                                     PySpark data source DataFrame and translates it to the DataFrame to be
                                     consumed by the Feature View.
        :param data_delay: By default, incremental materialization jobs run immediately at the end of the
                                    batch schedule period. This parameter configures how long they wait after the end
                                    of the period before starting, typically to ensure that all data has landed.
                                    For example, if a feature view has a `batch_schedule` of 1 day and one of
                                    the data source inputs has `data_delay=timedelta(hours=1)` set, then
                                    incremental materialization jobs will run at `01:00` UTC.
        :param user: (Only supported in Rift) The user used to connect to Snowflake.
                     This can be a string or a `Secret`. If unset SNOWFLAKE_USER from the environment is used.
        :param password: (Only supported in Rift) The password used to connect to Snowflake.
                         This can be a string or a `Secret`. If unset SNOWFLAKE_PASSWORD from the environment is used.
                         Deprecated: Use private_key authentication instead.
        :param private_key: (Only supported in Rift) The private key used to connect to Snowflake for key-pair authentication.
                           This can be a string or a `Secret`. If unset SNOWFLAKE_PRIVATE_KEY from the environment is used.
                           Recommended over password authentication.
        :param private_key_passphrase: (Only supported in Rift) The passphrase for the private key used to connect to Snowflake.
                                      This can be a string or a `Secret`. If unset SNOWFLAKE_PRIVATE_KEY_PASSPHRASE from the environment is used.
                                      Optional, only needed if the private key is encrypted.

        :return: A SnowflakeConfig class instance.
        """
        # Rift does not allow snowflake tables to have double quotes in the table name
        #
        # See https://tecton.atlassian.net/browse/TEC-17715 for more details.
        # Checking the table first and then the batch compute mode is done for the sake of
        # SDK tests which do not set
        batch_compute_mode = default_batch_compute_mode()
        if batch_compute_mode == BatchComputeMode.RIFT:
            if table and '"' in table:
                msg = "Rift does not support Snowflake table names containing double quotation marks."
                raise TectonValidationError(msg)
            msg = "Parameter {parameter_name} not supported in SnowflakeConfig with compute mode Rift"
            if post_processor is not None:
                raise TectonValidationError(msg.format(parameter_name="post_processor"))

        self._args = args = data_source_pb2.SnowflakeDataSourceArgs(
            database=database,
            schema=schema,
            warehouse=warehouse,
            url=url,
            role=role,
            table=table,
            query=query,
            user=convert_secret_to_sanitized_reference(user) if user else None,
            password=convert_secret_to_sanitized_reference(password) if password else None,
            private_key=convert_secret_to_sanitized_reference(private_key) if private_key else None,
            private_key_passphrase=convert_secret_to_sanitized_reference(private_key_passphrase)
            if private_key_passphrase
            else None,
        )

        if post_processor is not None and function_serialization.should_serialize_function(post_processor):
            args.common_args.post_processor.CopyFrom(function_serialization.to_proto(post_processor))
        if timestamp_field:
            args.common_args.timestamp_field = timestamp_field

        args.common_args.data_delay.FromTimedelta(data_delay)
        self._data_delay = data_delay
        self.post_processor = post_processor

    @property
    def data_delay(self):
        return self._data_delay

    def _merge_batch_args(self, data_source_args: virtual_data_source_pb2.VirtualDataSourceArgs):
        data_source_args.snowflake_ds_config.CopyFrom(self._args)


class RedshiftConfig(BaseBatchConfig):
    """
    Configuration used to reference a Redshift table or query.

    The RedshiftConfig class is used to create a reference to a Redshift table. You can also create a
    reference to a query on one or more tables, which will be registered in Tecton in a similar way as a view
    is registered in other data systems.

    This class used as an input to a `BatchSource`'s parameter `batch_config`. This class is not
    a Tecton Object: it is a grouping of parameters. Declaring this class alone will not register a data source.
    Instead, declare as part of `BatchSource` that takes this configuration class instance as a parameter.
    """

    def __init__(
        self,
        endpoint: str,
        table: Optional[str] = None,
        post_processor: Optional[Callable] = None,
        query: Optional[str] = None,
        timestamp_field: Optional[str] = None,
        data_delay: datetime.timedelta = datetime.timedelta(seconds=0),
    ):
        """
        Instantiates a new RedshiftConfig. One of table and query should be specified when creating this file.

        Example of a RedshiftConfig declaration:

        ```python
        from tecton import RedshiftConfig

        # Declare RedshiftConfig instance object that can be used as an argument in BatchSource
        redshift_ds_config = RedshiftConfig(endpoint="cluster-1.us-west-2.redshift.amazonaws.com:5439/dev",
                                              query="SELECT timestamp as ts, created, user_id, ad_id, duration"
                                                    "FROM ad_serving_features")
        ```

        :param endpoint: The connection endpoint to Redshift
                         (e.g. redshift-cluster-1.cigcwzsdltjs.us-west-2.redshift.amazonaws.com:5439/dev).
        :param table: The Redshift table for this Data source. Only one of table and query should be specified.
        :param post_processor: Python user defined function `f(DataFrame) -> DataFrame` that takes in raw
                                     PySpark data source DataFrame and translates it to the DataFrame to be
                                     consumed by the Feature View.
        :param query: A Redshift query for this Data source. Only one of table and query should be specified.
        :param timestamp_field: The timestamp column in this data source that should be used for time-based filtering. Required unless this source is used in Feature Views only with `unfiltered()`.
        :param data_delay: By default, incremental materialization jobs run immediately at the end of the
                                    batch schedule period. This parameter configures how long they wait after the end
                                    of the period before starting, typically to ensure that all data has landed.
                                    For example, if a feature view has a `batch_schedule` of 1 day and one of
                                    the data source inputs has `data_delay=timedelta(hours=1)` set, then
                                    incremental materialization jobs will run at `01:00` UTC.

        :return: A RedshiftConfig class instance.
        """
        self._args = args = data_source_pb2.RedshiftDataSourceArgs()
        args.endpoint = endpoint

        if table and query:
            msg = "Should only specify one of table and query sources for redshift"
            raise AssertionError(msg)
        if not table and not query:
            msg = "Missing both table and query sources for redshift, exactly one must be present"
            raise AssertionError(msg)

        if table:
            args.table = table
        else:
            args.query = query

        if post_processor is not None and function_serialization.should_serialize_function(post_processor):
            args.common_args.post_processor.CopyFrom(function_serialization.to_proto(post_processor))
        if timestamp_field:
            args.common_args.timestamp_field = timestamp_field

        args.common_args.data_delay.FromTimedelta(data_delay)
        self._data_delay = data_delay
        self.post_processor = post_processor

    @property
    def data_delay(self):
        return self._data_delay

    def _merge_batch_args(self, data_source_args: virtual_data_source_pb2.VirtualDataSourceArgs):
        data_source_args.redshift_ds_config.CopyFrom(self._args)


class BigQueryConfig(BaseBatchConfig):
    """
    Configuration used to reference a BigQuery table or query.

    The BigQueryConfig class is used to create a reference to a BigQuery table. You can also create a
    reference to a query on one or more tables, which will be registered in Tecton in a similar way as a view
    is registered in other data systems.

    This class is used as an input to a `BatchSource`'s parameter `batch_config`. Declaring this configuration
    class alone will not register a Data Source. Instead, declare as a part of `BatchSource` that takes this
    configuration class instance as a parameter.

    NOTE: Named BigQueryConfig instead of BigqueryConfig because that's more consistent with the brand naming
    and other Python libraries using the BigQuery notation.
    Internal Tecton code will ignore the branding capitalization, e.g. use "Bigquery".
    """

    def __init__(
        self,
        *,
        project_id: Optional[str] = None,
        dataset: Optional[str] = None,
        location: Optional[str] = None,
        table: Optional[str] = None,
        query: Optional[str] = None,
        timestamp_field: Optional[str] = None,
        data_delay: datetime.timedelta = datetime.timedelta(seconds=0),
        credentials: Optional[Secret] = None,
    ):
        """
        Instantiates a new BigQueryConfig. One of table and query should be specified when creating this file.

        :param project_id: The BigQuery Project ID for this Data source.
        :param dataset: The BigQuery Dataset for this Data source.
        :param location: Optional geographic location of the dataset, such as "US" or "EU".
                         This is for ensuring that queries are run in the same location as the data.
        :param table: The table for this Data source. Only one of `table` and `query` must be specified.
        :param query: The query for this Data source. Only one of `table` and `query` must be specified.
        :param timestamp_field: The timestamp column in this data source that should be used for time-based filtering. Required unless this source is used in Feature Views only with `unfiltered()`.
        :param data_delay: This parameter configures how long jobs wait after the end of the batch_schedule period before
                           starting, typically to ensure that all data has landed.
                           For example, if a feature view has a `batch_schedule` of 1 day and one of
                           the data source inputs has `data_delay=timedelta(hours=1)` set, then
                           incremental materialization jobs will run at `01:00` UTC.
        :param credentials: Optional service account credentials used to connect to BigQuery.

        :return: A BigQueryConfig class instance.
        """
        self._args = args = data_source_pb2.BigqueryDataSourceArgs(
            project_id=project_id,
            dataset=dataset,
            location=location,
            table=table,
            query=query,
            credentials=convert_secret_to_sanitized_reference(credentials) if credentials else None,
        )

        if timestamp_field:
            args.common_args.timestamp_field = timestamp_field

        args.common_args.data_delay.FromTimedelta(data_delay)
        self._data_delay = data_delay
        self.post_processor = None

    @property
    def data_delay(self):
        """
        How long they wait after the end of the batch schedule period before starting,
        typically to ensure that all data has landed.
        """
        return self._data_delay

    def _merge_batch_args(self, data_source_args: virtual_data_source_pb2.VirtualDataSourceArgs):
        data_source_args.bigquery_ds_config.CopyFrom(self._args)


class SparkBatchConfig(BaseBatchConfig):
    """
    Configuration used to define a batch source using a Data Source Function.

    The `SparkBatchConfig` class is used to configure a batch source using a user defined Data Source Function.

    This class is used as an input to a `BatchSource`'s parameter `batch_config`. Declaring this configuration
    class alone will not register a Data Source. Instead, declare as a part of `BatchSource` that takes this configuration
    class instance as a parameter.

    **Do not instantiate this class directly.** Use `tecton.spark_batch_config` instead.
    """

    def __init__(
        self,
        data_source_function: Union[
            Callable[[SparkSession], DataFrame], Callable[[SparkSession, FilterContext], DataFrame]
        ],
        data_delay: datetime.timedelta = datetime.timedelta(seconds=0),
        supports_time_filtering: bool = False,
    ):
        """
        Instantiates a new SparkBatchConfig.

        :param data_source_function: User defined Data Source Function that takes in a `SparkSession` and an optional
                                    `tecton.FilterContext`, if `supports_time_filtering=True`. Returns a `DataFrame`.
        :param data_delay: By default, incremental materialization jobs run immediately at the end of the
                                    batch schedule period. This parameter configures how long they wait after the end
                                    of the period before starting, typically to ensure that all data has landed.
                                    For example, if a feature view has a `batch_schedule` of 1 day and one of
                                    the data source inputs has a `data_delay` of 1 hour, then
                                    incremental materialization jobs will run at `01:00` UTC.
        :param supports_time_filtering: When set to `True`, the Data Source Function must take the `filter_context` parameter and implement time filtering logic. `supports_time_filtering` must be set to `True` if `<data source>.get_dataframe()` is called with `start_time` or `end_time`, or if using time filtering with a Data Source when defining a `FeatureView` which has time filtering enabled by default. To use a Data Source without time filtering, call `.unfiltered()` on the Data Source. The `FeatureView` will call the Data Source Function with the `tecton.FilterContext`, which has the `start_time` and `end_time` set.

        :return: A SparkBatchConfig class instance.
        """
        params = list(inspect.signature(data_source_function).parameters)
        function_name = data_source_function.__name__
        if supports_time_filtering and params != ["spark", "filter_context"]:
            msg = f"Data Source Function {function_name}'s required signature is `{function_name}(spark, filter_context)` when supports_time_filtering is True"
            raise AssertionError(msg)
        elif not supports_time_filtering and params != ["spark"]:
            msg = f"Data Source Function {function_name}'s required signature is `{function_name}(spark)`"
            raise AssertionError(msg)

        self._args = data_source_pb2.SparkBatchConfigArgs()
        if function_serialization.should_serialize_function(data_source_function):
            self._args.data_source_function.CopyFrom(function_serialization.to_proto(data_source_function))
        self._args.data_delay.FromTimedelta(data_delay)
        self._args.supports_time_filtering = supports_time_filtering
        self._data_delay = data_delay
        self.data_source_function = data_source_function

    @property
    def data_delay(self) -> datetime.timedelta:
        return self._data_delay

    def _merge_batch_args(self, data_source_args: virtual_data_source_pb2.VirtualDataSourceArgs):
        data_source_args.spark_batch_config.CopyFrom(self._args)

    def __call__(self, *args, **kwargs):
        return self.data_source_function(*args, **kwargs)


@typechecked
def spark_batch_config(
    *,
    data_delay: Optional[datetime.timedelta] = datetime.timedelta(seconds=0),
    supports_time_filtering: Optional[bool] = False,
):
    """
    Declare a `tecton.SparkBatchConfig` for configuring a Batch Source with a Data Source Function.
    The function takes in a `SparkSession` and an optional `tecton.FilterContext`, if `supports_time_filtering=True`. Returns a `DataFrame`.

    Example defining a Data Source Function using `spark_batch_config`:

    ```python
    from tecton import spark_batch_config

    @spark_batch_config(supports_time_filtering=True)
    def redshift_data_source_function(spark, filter_context):
        spark_format = "com.databricks.spark.redshift"
        params = {
            "user": "<user name>",
            "password": os.environ["redshift_password"]
        }
        endpoint = "<redshift endpoint>"
        full_connection_string = f"jdbc:redshift://{endpoint};user={params['user']};password={params['password']}"
        df_reader = (
            spark.read.format(spark_format)
            .option("url", full_connection_string)
            .option("forward_spark_s3_credentials", "true")
        )
        df_reader = df_reader.option("dbtable", "your_table_name")
        df = df_reader_load()
        ts_column = "timestamp"
        df = df.withColumn(ts_column, col(ts_column).cast("timestamp"))
        # Handle time filtering
        if filter_context:
            if filter_context.start_time:
                df = df.where(col(ts_column) >= filter_context.start_time)
            if filter_context.end_time:
                df = df.where(col(ts_column) < filter_context.end_time)
        return df
    ```

    :param data_delay: By default, incremental materialization jobs run immediately at the end of the
                                batch schedule period. This parameter configures how long they wait after the end
                                of the period before starting, typically to ensure that all data has landed.
                                For example, if a feature view has a `batch_schedule` of 1 day and one of
                                the data source inputs has `data_delay=timedelta(hours=1)` set, then
                                incremental materialization jobs will run at `01:00` UTC.
    :param supports_time_filtering: When set to `True`, the Data Source Function must take the `filter_context` parameter and implement time filtering logic. `supports_time_filtering` must be set to `True` if `<data source>.get_dataframe()` is called with `start_time` or `end_time`, or if using time filtering with a Data Source when defining a `FeatureView` which has time filtering enabled by default. To use a Data Source without time filtering, call `.unfiltered()` on the Data Source. The `FeatureView` will call the Data Source Function with the `tecton.FilterContext`, which has the `start_time` and `end_time` set.
    """

    def decorator(data_source_function):
        batch_config = SparkBatchConfig(
            data_source_function=data_source_function,
            data_delay=data_delay,
            supports_time_filtering=supports_time_filtering,
        )
        functools.update_wrapper(wrapper=batch_config, wrapped=data_source_function)
        return batch_config

    return decorator


class SparkStreamConfig(BaseStreamConfig):
    """
    Configuration used to define a stream source using a Data Source Function.

    The `SparkStreamConfig` class is used to configure a stream source using a user defined Data Source Function.

    This class is used as an input to a `StreamSource`'s parameter `stream_config`. Declaring this configuration
    class alone will not register a Data Source. Instead, declare as a part of `StreamSource` that takes this configuration
    class instance as a parameter.

    **Do not instantiate this class directly.** Use :`tecton.spark_stream_config` instead.
    """

    def __init__(self, data_source_function: Callable[[SparkSession], DataFrame]):
        """
        Instantiates a new SparkBatchConfig.

        :param data_source_function: User-defined Data Source Function that takes in a `SparkSession` and returns
                    a streaming `DataFrame`.

        :return: A SparkStreamConfig class instance.
        """
        params = list(inspect.signature(data_source_function).parameters)
        function_name = data_source_function.__name__
        if params != ["spark"]:
            msg = f"Data Source Function {function_name}'s required signature is `{function_name}(spark)`"
            raise AssertionError(msg)

        self._args = data_source_pb2.SparkStreamConfigArgs()
        if function_serialization.should_serialize_function(data_source_function):
            self._args.data_source_function.CopyFrom(function_serialization.to_proto(data_source_function))
        self.data_source_function = data_source_function

    def _merge_stream_args(self, data_source_args: virtual_data_source_pb2.VirtualDataSourceArgs):
        data_source_args.spark_stream_config.CopyFrom(self._args)

    def __call__(self, *args, **kwargs):
        return self.data_source_function(*args, **kwargs)


def spark_stream_config():
    """
    Declare a `tecton.SparkStreamConfig` for configuring a Stream Source with a Data Source Function. The function takes in a `SparkSession` returns a streaming `DataFrame`.

    Example defining a Data Source Function using `spark_stream_config`:

    ```python
    from tecton import spark_stream_config

    def raw_data_deserialization(df):
        from pyspark.sql.functions import col, from_json, from_utc_timestamp, when
        from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType, BooleanType, IntegerType
        payload_schema = StructType([
            StructField("user_id", StringType(), False),
            StructField("transaction_id", StringType(), False),
            StructField("category", StringType(), False),
            StructField("amt", StringType(), False),
            StructField("timestamp", StringType(), False),
        ])
        return (
            df.selectExpr("cast (data as STRING) jsonData")
            .select(from_json("jsonData", payload_schema).alias("payload"))
            .select(
                col("payload.user_id").alias("user_id"),
                col("payload.transaction_id").alias("transaction_id"),
                col("payload.category").alias("category"),
                col("payload.amt").cast("double").alias("amt"),
                from_utc_timestamp("payload.timestamp", "UTC").alias("timestamp")
            )
        )

    @spark_stream_config()
    def kinesis_data_source_function(spark):
        options = {
            "streamName": "<stream name>",
            "roleArn": "<role ARN>",
            "region": "<region>",
            "shardFetchInterval": "30s",
            "initialPosition": "latest"
        }
        reader = spark.readStream.format("kinesis").options(**options)
        df = reader.load()
        df = raw_data_deserialization(df)
        watermark = "{} seconds".format(timedelta(hours=24).seconds)
        df = df.withWatermark("timestamp", watermark)
        return df
    ```
    """

    def decorator(data_source_function):
        stream_config = SparkStreamConfig(
            data_source_function=data_source_function,
        )
        functools.update_wrapper(wrapper=stream_config, wrapped=data_source_function)
        return stream_config

    return decorator


class PandasBatchConfig(BaseBatchConfig):
    """
    Configuration used to define a batch source using a Pandas Data Source Function.
    The `PandasBatchConfig` class is used to configure a batch source using a user defined Data Source Function.
    This class is used as an input to a `BatchSource`'s parameter `batch_config`. Declaring this configuration
    class alone will not register a Data Source. Instead, declare as a part of `BatchSource` that takes this configuration
    class instance as a parameter.
    **Do not instantiate this class directly.** Use :`tecton.pandas_batch_config` instead.
    """

    class PandasDataSourceFunctionType1(Protocol):
        def __call__(self) -> DataFrame: ...

    class PandasDataSourceFunctionType2(Protocol):
        def __call__(self, filter_context: FilterContext) -> DataFrame: ...

    class PandasDataSourceFunctionType3(Protocol):
        def __call__(self, secrets_context: Mapping[str, str]) -> DataFrame: ...

    class PandasDataSourceFunctionType4(Protocol):
        def __call__(self, filter_context: FilterContext, secrets_context: Mapping[str, str]) -> DataFrame: ...

    PandasDataSourceFunctionType = Union[
        PandasDataSourceFunctionType1,
        PandasDataSourceFunctionType2,
        PandasDataSourceFunctionType3,
        PandasDataSourceFunctionType4,
    ]

    def __init__(
        self,
        data_source_function: PandasDataSourceFunctionType,
        data_delay: datetime.timedelta = datetime.timedelta(seconds=0),
        supports_time_filtering: bool = False,
        secrets: Optional[Dict[str, Union[Secret, str]]] = None,
    ):
        """
        Instantiates a new PandasBatchConfig.

        :param data_source_function: User defined Data Source Function that takes in an optional `tecton.FilterContext`, if `supports_time_filtering=True`. Returns a `pandas.DataFrame`.
        :param data_delay: By default, incremental materialization jobs run immediately at the end of the batch
        schedule period. This parameter configures how long they wait after the end of the period before starting,
        typically to ensure that all data has landed. For example, if a feature view has a `batch_schedule` of 1 day
        and one of the data source inputs has a `data_delay` of 1 hour, then incremental materialization jobs will
        run at `01:00` UTC.
        :param supports_time_filtering: When set to `True`, the Data Source Function must take the `filter_context` parameter and implement time filtering logic. `supports_time_filtering` must be set to `True` if `<data source>.get_dataframe()` is called with `start_time` or `end_time`, or if using time filtering with a Data Source when defining a `FeatureView` which has time filtering enabled by default. To use a Data Source without time filtering, call `.unfiltered()` on the Data Source. The `FeatureView` will call the Data Source Function with the `tecton.FilterContext`, which has the `start_time` and `end_time` set.
        :param secrets: A dictionary of Secret references that will be resolved and provided to the Data Source Function at runtime. During local
        development and testing, strings may be used instead Secret references.

        :return: A PandasBatchConfig class instance.
        """
        self._check_function_signature(data_source_function, supports_time_filtering, use_secrets=bool(secrets))
        self._args = data_source_pb2.PandasBatchConfigArgs()
        if function_serialization.should_serialize_function(data_source_function):
            self._args.data_source_function.CopyFrom(function_serialization.to_proto(data_source_function))
        self._args.data_delay.FromTimedelta(data_delay)
        self._args.supports_time_filtering = supports_time_filtering
        if secrets:
            for name, secret in secrets.items():
                self._args.secrets[name].CopyFrom(convert_secret_to_sanitized_reference(secret))
        self._data_delay = data_delay
        self.data_source_function = data_source_function

    @property
    def data_delay(self) -> datetime.timedelta:
        return self._data_delay

    def _merge_batch_args(self, data_source_args: virtual_data_source_pb2.VirtualDataSourceArgs):
        data_source_args.pandas_batch_config.CopyFrom(self._args)

    def __call__(self, *args, **kwargs):
        return self.data_source_function(*args, **kwargs)

    @staticmethod
    def _check_function_signature(data_source_function: Callable, supports_time_filtering: bool, use_secrets: bool):
        function_name = data_source_function.__name__
        params = list(inspect.signature(data_source_function).parameters)
        if supports_time_filtering and use_secrets:
            if params != ["filter_context", "secrets"]:
                msg = f"Data Source Function {function_name}'s required signature is `{function_name}(filter_context, secrets)` when supports_time_filtering is True and secrets are used"
                raise AssertionError(msg)
        elif supports_time_filtering:
            if params != ["filter_context"]:
                msg = f"Data Source Function {function_name}'s required signature is `{function_name}(filter_context)` when supports_time_filtering is True"
                raise AssertionError(msg)
        elif use_secrets:
            if params != ["secrets"]:
                msg = f"Data Source Function {function_name}'s required signature is `{function_name}(secrets)` when secrets are used"
                raise AssertionError(msg)
        elif params:
            msg = f"Data Source Function {function_name}'s required signature is `{function_name}()`"
            raise AssertionError(msg)


@typechecked
def pandas_batch_config(
    *,
    data_delay: Optional[datetime.timedelta] = datetime.timedelta(seconds=0),
    supports_time_filtering: Optional[bool] = False,
    secrets: Optional[Dict[str, Union[Secret, str]]] = None,
):
    """
    Declare a `tecton.PandasBatchConfig` for configuring a Batch Source with a Data Source Function.
    The function takes in an optional `tecton.FilterContext`, if `supports_time_filtering=True`.

        Example defining a Data Source Function using `pandas_batch_config`:
    ```python
    from tecton import pandas_batch_config, Secret
    @pandas_batch_config(
      supports_time_filtering=True,
      secrets={"s3_bucket": Secret(scope="dev", key="user_data_s3_bucket")}
    )
    def parquet_data_source_function(filter_context, secrets):
        import pyarrow.parquet as pq
        from pyarrow.fs import S3FileSystem
        filters=None
        # Handle time filtering, ideally using partition keys
        if filter_context:
            filters = []
            if filter_context.start_time:
                filters.append(("created_at", ">=", filter_context.start_time.replace(tzinfo=None)))
            if filter_context.end_time:
                filters.append(("created_at", "<", filter_context.end_time.replace(tzinfo=None)))

        s3_bucket = secrets["s3_bucket"]
        dataset = pq.ParquetDataset(
            f"s3://{s3_bucket}/path/to/data.pq",
            filesystem=S3FileSystem(),
            use_legacy_dataset=False,
            filters=filters if len(filters) > 0 else None
        )
        return dataset.read_pandas().to_pandas()
    ```

    :param data_delay: By default, incremental materialization jobs run immediately at the end of the batch schedule period. This parameter configures how long they wait after the end of the period before starting, typically to ensure that all data has landed. For example, if a feature view has a `batch_schedule` of 1 day and one of the data source inputs has `data_delay=timedelta(hours=1)` set, then incremental materialization jobs will run at `01:00` UTC.
    :param supports_time_filtering: When set to `True`, the Data Source Function must take the `filter_context` parameter and implement time filtering logic. `supports_time_filtering` must be set to `True` if `<data source>.get_dataframe()` is called with `start_time` or `end_time`, or if using time filtering with a Data Source when defining a `FeatureView` which has time filtering enabled by default. To use a Data Source without time filtering, call `.unfiltered()` on the Data Source. The `FeatureView` will call the Data Source Function with the `tecton.FilterContext`, which has the `start_time` and `end_time` set.
    :param secrets: A dictionary of Secret references that will be resolved and provided to the Data Source Function at runtime. During local development and testing, strings may be used instead Secret references.

    :return:  Returns a `pandas.DataFrame`.
    """

    def decorator(data_source_function):
        batch_config = PandasBatchConfig(
            data_source_function=data_source_function,
            data_delay=data_delay,
            supports_time_filtering=supports_time_filtering,
            secrets=secrets,
        )
        functools.update_wrapper(wrapper=batch_config, wrapped=data_source_function)
        return batch_config

    return decorator


class PyArrowBatchConfig(BaseBatchConfig):
    """
    Configuration used to define a batch source using a PyArrow Data Source Function.
    The `PyArrowBatchConfig` class is used to configure a batch source using a user defined Data Source Function.
    This class is used as an input to a `BatchSource`'s parameter `batch_config`. Declaring this configuration
    class alone will not register a Data Source. Instead, declare as a part of `BatchSource` that takes this configuration
    class instance as a parameter.
    **Do not instantiate this class directly.** Use :`tecton.pyarrow_batch_config` instead.
    """

    class PyArrowDataSourceFunctionType1(Protocol):
        def __call__(self) -> Union[pyarrow.Table, pyarrow.RecordBatchReader]: ...

    class PyArrowDataSourceFunctionType2(Protocol):
        def __call__(self, filter_context: FilterContext) -> Union[pyarrow.Table, pyarrow.RecordBatchReader]: ...

    class PyArrowDataSourceFunctionType3(Protocol):
        def __call__(self, secrets_context: Mapping[str, str]) -> Union[pyarrow.Table, pyarrow.RecordBatchReader]: ...

    class PyArrowDataSourceFunctionType4(Protocol):
        def __call__(
            self, filter_context: FilterContext, secrets_context: Mapping[str, str]
        ) -> Union[pyarrow.Table, pyarrow.RecordBatchReader]: ...

    PyArrowDataSourceFunctionType = Union[
        PyArrowDataSourceFunctionType1,
        PyArrowDataSourceFunctionType2,
        PyArrowDataSourceFunctionType3,
        PyArrowDataSourceFunctionType4,
    ]

    def __init__(
        self,
        data_source_function: PyArrowDataSourceFunctionType,
        data_delay: datetime.timedelta = datetime.timedelta(seconds=0),
        supports_time_filtering: bool = False,
        secrets: Optional[Dict[str, Union[Secret, str]]] = None,
    ):
        """
        Instantiates a new PyArrowBatchConfig.

        :param data_source_function: User defined Data Source Function that takes in an optional `tecton.FilterContext`, if `supports_time_filtering=True`. Returns a ` pyarrow.RecordBatchReader`.
        :param data_delay: By default, incremental materialization jobs run immediately at the end of the batch
        schedule period. This parameter configures how long they wait after the end of the period before starting,
        typically to ensure that all data has landed. For example, if a feature view has a `batch_schedule` of 1 day
        and one of the data source inputs has a `data_delay` of 1 hour, then incremental materialization jobs will
        run at `01:00` UTC.
        :param supports_time_filtering: When set to `True`, the Data Source Function must take the `filter_context` parameter and implement time filtering logic. `supports_time_filtering` must be set to `True` if `<data source>.get_dataframe()` is called with `start_time` or `end_time`, or if using time filtering with a Data Source when defining a `FeatureView` which has time filtering enabled by default. To use a Data Source without time filtering, call `.unfiltered()` on the Data Source. The `FeatureView` will call the Data Source Function with the `tecton.FilterContext`, which has the `start_time` and `end_time` set.
        :param secrets: A dictionary of Secret references that will be resolved and provided to the Data Source Function at runtime. During local
        development and testing, strings may be used instead Secret references.

        :return: A PyArrowBatchConfig class instance.
        """
        self._check_function_signature(data_source_function, supports_time_filtering, use_secrets=bool(secrets))
        self._args = data_source_pb2.PyArrowBatchConfigArgs()
        if function_serialization.should_serialize_function(data_source_function):
            self._args.data_source_function.CopyFrom(function_serialization.to_proto(data_source_function))
        self._args.data_delay.FromTimedelta(data_delay)
        self._args.supports_time_filtering = supports_time_filtering
        if secrets:
            for name, secret in secrets.items():
                self._args.secrets[name].CopyFrom(convert_secret_to_sanitized_reference(secret))
        self._data_delay = data_delay
        self.data_source_function = data_source_function

    @property
    def data_delay(self) -> datetime.timedelta:
        return self._data_delay

    def _merge_batch_args(self, data_source_args: virtual_data_source_pb2.VirtualDataSourceArgs):
        data_source_args.pyarrow_batch_config.CopyFrom(self._args)

    def __call__(self, *args, **kwargs):
        return self.data_source_function(*args, **kwargs)

    @staticmethod
    def _check_function_signature(data_source_function: Callable, supports_time_filtering: bool, use_secrets: bool):
        function_name = data_source_function.__name__
        params = list(inspect.signature(data_source_function).parameters)
        if supports_time_filtering and use_secrets:
            if params != ["filter_context", "secrets"]:
                msg = f"Data Source Function {function_name}'s required signature is `{function_name}(filter_context, secrets)` when supports_time_filtering is True and secrets are used"
                raise AssertionError(msg)
        elif supports_time_filtering:
            if params != ["filter_context"]:
                msg = f"Data Source Function {function_name}'s required signature is `{function_name}(filter_context)` when supports_time_filtering is True"
                raise AssertionError(msg)
        elif use_secrets:
            if params != ["secrets"]:
                msg = f"Data Source Function {function_name}'s required signature is `{function_name}(secrets)` when secrets are used"
                raise AssertionError(msg)
        elif params:
            msg = f"Data Source Function {function_name}'s required signature is `{function_name}()`"
            raise AssertionError(msg)


@typechecked
def pyarrow_batch_config(
    *,
    data_delay: Optional[datetime.timedelta] = datetime.timedelta(seconds=0),
    supports_time_filtering: Optional[bool] = False,
    secrets: Optional[Dict[str, Union[Secret, str]]] = None,
):
    """
    Declare a `tecton.PyArrowBatchConfig` for configuring a Batch Source with a Data Source Function.
    The function takes in an optional `tecton.FilterContext`, if `supports_time_filtering=True`.

        Example defining a Data Source Function using `pyarrow_batch_config`:
    ```python
    from tecton import pyarrow_batch_config, Secret
    @pyarrow_batch_config(
      supports_time_filtering=True,
      secrets={"s3_bucket": Secret(scope="dev", key="user_data_s3_bucket")}
    )
    def parquet_data_source_function(filter_context, secrets):
        import pyarrow.parquet as pq
        from pyarrow.fs import S3FileSystem
        filters=None
        # Handle time filtering, ideally using partition keys
        if filter_context:
            filters = []
            if filter_context.start_time:
                filters.append(("created_at", ">=", filter_context.start_time.replace(tzinfo=None)))
            if filter_context.end_time:
                filters.append(("created_at", "<", filter_context.end_time.replace(tzinfo=None)))

        s3_bucket = secrets["s3_bucket"]
        dataset = pq.ParquetDataset(
            f"s3://{s3_bucket}/path/to/data.pq",
            filesystem=S3FileSystem(),
            use_legacy_dataset=False,
            filters=filters if len(filters) > 0 else None
        )
        return dataset.read()
    ```

    :param data_delay: By default, incremental materialization jobs run immediately at the end of the batch schedule period. This parameter configures how long they wait after the end of the period before starting, typically to ensure that all data has landed. For example, if a feature view has a `batch_schedule` of 1 day and one of the data source inputs has `data_delay=timedelta(hours=1)` set, then incremental materialization jobs will run at `01:00` UTC.
    :param supports_time_filtering: When set to `True`, the Data Source Function must take the `filter_context` parameter and implement time filtering logic. `supports_time_filtering` must be set to `True` if `<data source>.get_dataframe()` is called with `start_time` or `end_time`, or if using time filtering with a Data Source when defining a `FeatureView` which has time filtering enabled by default. To use a Data Source without time filtering, call `.unfiltered()` on the Data Source.. The `FeatureView` will call the Data Source Function with the `tecton.FilterContext`, which has the `start_time` and `end_time` set.
    :param secrets: A dictionary of Secret references that will be resolved and provided to the Data Source Function at runtime. During local development and testing, strings may be used instead Secret references.

    :return:  Returns a `pyarrow.Table` or `pyarrow.RecordBatchReader`.
    """

    def decorator(data_source_function):
        batch_config = PyArrowBatchConfig(
            data_source_function=data_source_function,
            data_delay=data_delay,
            supports_time_filtering=supports_time_filtering,
            secrets=secrets,
        )
        functools.update_wrapper(wrapper=batch_config, wrapped=data_source_function)
        return batch_config

    return decorator


class LifetimeWindow(StrictModel):
    """Configures a lifetime window.

    This class has no attributes. When used, the aggregation will be specified from the `lifetime_start_time` until the aggregation reference point.
    """

    def _to_proto(self) -> time_window_pb2.LifetimeWindow:
        return time_window_pb2.LifetimeWindow()

    # TODO(jake): This is an unusual pattern to convert a config object to a spec like. Do not replicate without a good
    # reason. This is needed because Aggregations have not been fully migrated onto specs.
    def _to_spec(self) -> specs.LifetimeWindowSpec:
        return specs.LifetimeWindowSpec()

    @classmethod
    def _from_spec(cls):
        return cls()


class TimeWindow(StrictModel):
    """Configuration for specifying a TimeWindow that is applied in an Aggregation within a Batch or Stream Feature View.

    This class describes the attributes of a time window to aggregate over which includes the size of the time window
    and the offset of the window's end time from a given reference point(end of aggregation window, spine timestamp, or the current time).

    :param window_size: The size of the window, expressed as a positive `datetime.timedelta`
    :param offset: The relative end time of the window, expressed as a negative `datetime.timedelta`
    """

    window_size: datetime.timedelta
    offset: datetime.timedelta = datetime.timedelta(seconds=0)

    def _to_proto(self) -> feature_view_pb2.TimeWindow:
        return feature_view_pb2.TimeWindow(
            window_duration=time_utils.timedelta_to_proto(self.window_size),
            offset=time_utils.timedelta_to_proto(self.offset),
        )

    # TODO(jake): This is an unusual pattern to convert a config object to a spec like. Do not replicate without a good
    # reason. This is needed because Aggregations have not been fully migrated onto specs.
    def _to_spec(self) -> specs.RelativeTimeWindowSpec:
        return specs.RelativeTimeWindowSpec.from_args_proto(self._to_proto())

    @classmethod
    def _from_spec(cls, spec: specs.RelativeTimeWindowSpec):
        return cls(window_size=spec.window_duration, offset=spec.offset)


class TimeWindowSeries(StrictModel):
    """Configuration used to specify an aggregation time window series.

    This class describes the attributes of a time window series of multiple time windows to aggregate over. This includes
    the start of the first time window, the size of each time window, the step size between each time window start time, and
    the end of the last time window end.

    :param window_size: The size of the window to aggregate over, specified as a datetime.timedelta. `datetime.timedelta(days=30)`
    :param step_size: The step size between each time window start time, specified as a datetime.timedelta. `datetime.timedelta(days=1)`
    :param series_start: The negative start of the first time window in the series.
    :param series_end: The negative end of the last time window end in the series.
    """

    series_start: datetime.timedelta
    series_end: datetime.timedelta = datetime.timedelta(seconds=0)
    step_size: Optional[datetime.timedelta] = None
    window_size: datetime.timedelta

    def _to_proto(self) -> feature_view_pb2.TimeWindowSeries:
        step_size = self.step_size
        if step_size is None:
            step_size = self.window_size
        return feature_view_pb2.TimeWindowSeries(
            series_start=time_utils.timedelta_to_proto(self.series_start),
            series_end=time_utils.timedelta_to_proto(self.series_end),
            step_size=time_utils.timedelta_to_proto(step_size),
            window_duration=time_utils.timedelta_to_proto(self.window_size),
        )

    # TODO(jake): This is an unusual pattern to convert a config object to a spec like. Do not replicate without a good
    # reason. This is needed because Aggregations have not been fully migrated onto specs.
    def _to_spec(self) -> specs.TimeWindowSeriesSpec:
        return specs.TimeWindowSeriesSpec.from_args_proto(self._to_proto())

    @classmethod
    def _from_spec(cls, spec: specs.TimeWindowSeriesSpec):
        return cls(
            series_start=spec.window_series_start,
            series_end=spec.window_series_end,
            step_size=spec.step_size,
            window_size=spec.window_duration,
        )


class CacheConfig(StrictModel):
    """Configuration object for feature view online caching.

    :param max_age_seconds: The maximum time in seconds that features from this feature view can be cached. Must be
        between one minute (60s) and one day (86_400s).
    """

    max_age_seconds: int

    def _to_proto(self) -> feature_view_pb2.CacheConfig:
        return feature_view_pb2.CacheConfig(
            max_age_seconds=self.max_age_seconds,
        )

    @classmethod
    def from_proto(cls, proto: feature_view_pb2.CacheConfig):
        return cls(max_age_seconds=proto.max_age_seconds)


class Aggregation(StrictModel):
    """
    This class describes a single aggregation that is applied in a batch or stream feature view.

    `function` can be one of predefined numeric aggregation functions, namely `"count"`, `"sum"`, `"mean"`, `"min"`, `"max"`, `"var_samp"`, `"var_pop"`, `"variance"` - alias for `"var_samp"`, `"stddev_samp"`, `"stddev_pop"`, `"stddev"` - alias for `"stddev_samp"`. For
    these numeric aggregations, you can pass the name of it as a string. Nulls are handled like Spark SQL `Function(column)`, e.g. SUM/MEAN/MIN/MAX/VAR_SAMP/VAR_POP/VAR/STDDEV_SAMP/STDDEV_POP/STDDEV of all nulls is null and COUNT of all nulls is 0.

    In addition to numeric aggregations, `Aggregation` supports the last non-distinct and distinct N aggregation that will compute the last N non-distinct and distinct values for the column by timestamp. Right now only string column is supported as input to this aggregation, i.e., the resulting feature value will be a list of strings. The order of the value in the list is ascending based on the timestamp. Nulls are not included in the aggregated list.

    You can use it via the `last()` and  `last_distinct()` helper function like this:

    ```python
    from tecton.aggregation_functions import last_distinct, last

    @batch_feature_view(
    ...
    aggregations=[
        Aggregation(
            column='my_column',
            function=last_distinct(15),
            time_window=datetime.timedelta(days=7)),
        Aggregation(
            column='my_column',
            function=last(15),
            time_window=datetime.timedelta(days=7)),
        ],
    ...
    )
    def my_fv(data_source):
        pass
    ```

    :param column: Column name of the feature we are aggregating.
    :param function: One of the built-in aggregation functions.
    :param time_window: Duration to aggregate over. Example: `datetime.timedelta(days=30)`.
    :param name: The name of this feature. Defaults to an autogenerated name, e.g. transaction_count_7d_1d.
    :param description: A human-readable description of the feature
    :param tags: Tags associated with the feature (key-value pairs of arbitrary metadata).
    """

    column: str
    function: AggregationFunction
    time_window: Union[LifetimeWindow, TimeWindow, TimeWindowSeries]
    name: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[Dict[str, str]] = None

    @pydantic_v1.validator("time_window", pre=True)
    def timedelta_to_time_window(cls, v):
        if isinstance(v, datetime.timedelta):
            return TimeWindow(window_size=v)
        return v

    @pydantic_v1.validator("function", pre=True)
    def str_to_aggregation_function(cls, v):
        if isinstance(v, str):
            return AggregationFunction(base_name=v, resolved_name=v, params=MappingProxyType({}))
        return v

    def __init__(
        self,
        column: str,
        function: Union[str, AggregationFunction],
        time_window: Union[TimeWindow, LifetimeWindow, datetime.timedelta],
        name: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
    ):
        super().__init__(
            column=column, function=function, time_window=time_window, name=name, description=description, tags=tags
        )

    def _to_proto(
        self,
        aggregation_interval: datetime.timedelta,
        is_continuous: bool,
        compaction_enabled: bool = False,
        is_streaming_fv: bool = False,
    ):
        return build_aggregation_proto(
            self.name,
            self.column,
            self.function,
            self.time_window,
            aggregation_interval,
            is_continuous,
            compaction_enabled,
            is_streaming_fv,
            self.description,
            self.tags,
        )

    def _default_name(
        self, aggregation_interval: datetime.timedelta, is_continuous: bool, compaction_enabled: bool
    ) -> str:
        return build_aggregation_default_name(
            self.column, self.time_window, self.function, aggregation_interval, is_continuous, compaction_enabled
        )


class AutoscalingConfig(StrictModel):
    """
    Configuration for autoscaling of server groups.

    :param min_nodes: The minimum number of nodes to scale down to.
    :param max_nodes: The maximum number of nodes to scale up to.
    """

    min_nodes: Optional[int] = None
    max_nodes: Optional[int] = None

    def _to_proto(self):
        if self.min_nodes is None:
            msg = "Missing required parameter `min_nodes` for AutoscalingConfig"
            raise TectonValidationError(msg)
        if self.max_nodes is None:
            msg = "Missing required parameter `max_nodes` for AutoscalingConfig"
            raise TectonValidationError(msg)
        return scaling_config_pb2.AutoscalingConfig(
            min_nodes=self.min_nodes,
            max_nodes=self.max_nodes,
        )


class ProvisionedScalingConfig(StrictModel):
    """
    Configuration for provisioned scaling of server groups.

    :param desired_nodes: The desired number of nodes to provision.
    """

    desired_nodes: Optional[int] = None

    def _to_proto(self):
        if self.desired_nodes is None:
            msg = "Missing required parameter `desired_nodes` for ProvisionedScalingConfig"
            raise TectonValidationError(msg)
        return scaling_config_pb2.ProvisionedScalingConfig(
            desired_nodes=self.desired_nodes,
        )


# Composite types.
OnlineStoreTypes = Union[DynamoConfig, RedisConfig, BigtableConfig]
ComputeConfigTypes = Union[
    _DefaultClusterConfig,
    DatabricksClusterConfig,
    EMRClusterConfig,
    DatabricksJsonClusterConfig,
    EMRJsonClusterConfig,
    RiftBatchConfig,
]


def _compute_batch_sawtooth_tile_size(
    time_window: Union[TimeWindow, TimeWindowSeries, LifetimeWindow],
) -> Optional[datetime.timedelta]:
    if isinstance(time_window, (LifetimeWindow, TimeWindowSeries)):
        return None
    else:
        # See RFC for stream compaction to understand why we chose these defaults https://www.notion.so/tecton/RFC-Stream-Compaction-e4cb1a0dc28549348ae42f07aebca27a?pvs=4#451917f6f7f74a6e814fd9d8aa0e1b6b
        if time_window.window_size < datetime.timedelta(days=2):
            return None
        elif time_window.window_size <= datetime.timedelta(days=10):
            return datetime.timedelta(hours=1)
        else:
            return datetime.timedelta(days=1)


# TODO(TEC-19301): Ideally this util can live in a seprate util module but we need to break `configs` into mutiple
# modules to avoid cyclic imports. See the ticket for details.
def build_aggregation_proto(
    name: Optional[str],
    column: str,
    function: AggregationFunction,
    time_window: Union[TimeWindow, TimeWindowSeries, LifetimeWindow],
    aggregation_interval: datetime.timedelta,
    is_continuous: bool,
    compaction_enabled: bool,
    is_streaming_fv: bool,
    description: Optional[str],
    tags: Optional[Dict[str, str]],
) -> feature_view_pb2.FeatureAggregation:
    batch_sawtooth_tile_size = None
    if compaction_enabled and is_streaming_fv:
        batch_sawtooth_tile_size = _compute_batch_sawtooth_tile_size(time_window)
    proto = feature_view_pb2.FeatureAggregation(
        name=name
        if name
        else build_aggregation_default_name(
            column, time_window, function, aggregation_interval, is_continuous, compaction_enabled
        ),
        column=column,
        function=function.base_name,
        batch_sawtooth_tile_size=time_utils.timedelta_to_proto(batch_sawtooth_tile_size)
        if batch_sawtooth_tile_size
        else None,
        description=description,
        tags=tags,
    )

    for k, v in function.params.items():
        if isinstance(v, int):
            proto.function_params[k].CopyFrom(feature_view_pb2.ParamValue(int64_value=v))
        else:
            proto.function_params[k].CopyFrom(feature_view_pb2.ParamValue(double_value=v))

    if isinstance(time_window, TimeWindow):
        proto.time_window.CopyFrom(time_window._to_proto())
    elif isinstance(time_window, LifetimeWindow):
        proto.lifetime_window.CopyFrom(time_window._to_proto())
    elif isinstance(time_window, TimeWindowSeries):
        proto.time_window_series.CopyFrom(time_window._to_proto())
    else:
        msg = f"Invalid time_window type: {type(time_window)}"
        raise TypeError(msg)

    return proto


# TODO(TEC-19301): Ideally this util can live in a seprate util module but we need to break `configs` into mutiple
# modules to avoid cyclic imports. See the ticket for details.
def build_aggregation_default_name(
    column: str,
    time_window: Union[TimeWindow, TimeWindowSeries, LifetimeWindow],
    function: AggregationFunction,
    aggregation_interval: datetime.timedelta,
    is_continuous: bool,
    compaction_enabled: bool,
) -> str:
    window_spec = time_window._to_spec()
    column_name = f"{column}_{function.resolved_name}_{window_spec.window_duration_string()}"

    if not compaction_enabled:
        agg_interval_name = feature_view_utils.construct_aggregation_interval_name(
            time_utils.timedelta_to_proto(aggregation_interval), is_continuous
        )
        column_name = f"{column_name}_{agg_interval_name}"

    if isinstance(time_window, TimeWindowSeries):
        column_name = f"{column_name}_series_{window_spec.window_series_start_string()}_{window_spec.window_series_end_string()}_{window_spec.step_size_string()}"
    else:
        if window_spec.offset_string():
            column_name = f"{column_name}_{window_spec.offset_string()}"
    column_name = column_name.replace(" ", "")

    return column_name


def _build_pretty_string_from_supported_versions(supported_versions) -> str:
    return ", ".join(version.value for version in supported_versions)
