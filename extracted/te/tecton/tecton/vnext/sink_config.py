import datetime
import inspect
from typing import Callable
from typing import Dict
from typing import Optional
from typing import Union

from typing_extensions import Literal

from tecton._internals import errors
from tecton._internals.repo import function_serialization
from tecton.framework.configs import Secret
from tecton.framework.configs import convert_secret_to_sanitized_reference
from tecton_core import time_utils
from tecton_proto.args import feature_view__client_pb2 as feature_view__args_pb2
from tecton_proto.args import transformation__client_pb2 as transformation_pb2
from tecton_proto.args.feature_view__client_pb2 import DataLakeConfig
from tecton_proto.args.feature_view__client_pb2 import DeltaConfig


class SinkConfig:
    """
    The `SinkConfig` represents a post materialization hook that will be run after offline materialization.
    """

    name: str
    mode: str
    function: Callable
    secrets: Optional[Dict[str, Union[Secret, str]]] = (None,)

    def __init__(
        self, name: str, mode: str, function: Callable, secrets: Optional[Dict[str, Union[Secret, str]]] = None
    ):
        self.name = name
        self.mode = mode
        self.function = function

        # Validate function parameters
        parameters = inspect.signature(function).parameters.keys()
        if not (set(parameters) == {"df"} or set(parameters) == {"df", "context"}):
            raise errors.INVALID_SINK_CONFIG_SIGNATURE(name)

        self.secrets = secrets

    def _to_proto(self) -> feature_view__args_pb2.SinkConfig:
        self.secret_references = {}
        if self.secrets:
            for secret_name, secret in self.secrets.items():
                self.secret_references[secret_name] = convert_secret_to_sanitized_reference(secret)
        serialized_function = None
        if function_serialization.should_serialize_function(self.function):
            serialized_function = function_serialization.to_proto(self.function)
        return feature_view__args_pb2.SinkConfig(
            name=self.name,
            mode=self._convert_mode_to_transformation_mode(self.mode),
            function=serialized_function,
            secrets=self.secret_references,
        )

    def _convert_mode_to_transformation_mode(self, mode_string: str) -> transformation_pb2.TransformationMode:
        supported_modes_to_proto = {
            "pandas": transformation_pb2.TransformationMode.TRANSFORMATION_MODE_PANDAS,
            "pyspark": transformation_pb2.TransformationMode.TRANSFORMATION_MODE_PYSPARK,
            "pyarrow": transformation_pb2.TransformationMode.TRANSFORMATION_MODE_PYARROW,
        }
        if mode_string in supported_modes_to_proto:
            return supported_modes_to_proto[mode_string]
        msg = f"Sink mode: `{mode_string}` is invalid. Supported mode(s) for sink_config are: {list(supported_modes_to_proto.keys())}'"
        raise TypeError(msg)


def sink_config(
    *,
    mode: str,
    name: Optional[str] = None,
    secrets: Optional[Dict[str, Union[Secret, str]]] = None,
):
    """
    Declare a SinkConfig which represents a post materialization hook that will be run after offline materialization.

    ```python
    from tecton import Embedding, batch_feature_view
    from tecton.types import String


    @sink_config(
        mode = "pandas",
        secrets = {"secret1": Secret(scope='prod', key='my_key')},
    )
    def sample_sink(df, context):
        ...
    ```

    :param name: The name of the sink. defaults to name of function.
    :param secrets: A dictionary of Secret references that will be resolved and provided to the transformation function at runtime. During local development and testing, strings may be used instead Secret references.
    :param mode: (Required) The compute mode for the transformation body

    :return: An object of type `SinkConfig`
    """

    def decorator(function):
        return SinkConfig(name or function.__name__, mode, function, secrets)

    return decorator


class PublishFeaturesConfig:
    """
    Configuration options to specify how a Feature View should publish features post-materialization

    :param publish_sink: If provided, Tecton will additionally run sink function post materialization.
    :param publish_offline: If True, Tecton will publish a full feature values to a separate table after
        materialization jobs to the staging table have completed. Users can query these feature values directly
        without further transformations or aggregations.
    :param publish_start_time: If set, Tecton will publish features starting from the feature time. If not set,
        Tecton will default to the Feature View's feature_start_time.
    """

    kind: Literal["PublishFeaturesConfig"] = (
        "PublishFeaturesConfig"  # Used for YAML parsing as a Pydantic discriminator.
    )
    publish_offline: bool = False
    publish_sink: Optional[SinkConfig] = None
    publish_start_time: Optional[datetime.datetime] = None

    def __init__(
        self,
        publish_start_time: Optional[datetime.datetime] = None,
        publish_offline: bool = False,
        publish_sink: Optional[SinkConfig] = None,
    ):
        self.publish_sink = publish_sink
        self.publish_offline = publish_offline
        # Not required, defaults to feature start time
        self.publish_start_time = publish_start_time

    def _to_proto(self):
        publish_features_config = []
        if self.publish_offline:
            publish_features_config.append(
                feature_view__args_pb2.PublishFeaturesConfig(
                    publish_start_time=time_utils.datetime_to_proto(self.publish_start_time),
                    data_lake_config=DataLakeConfig(delta=DeltaConfig()),
                )
            )
        if self.publish_sink:
            publish_features_config.append(
                feature_view__args_pb2.PublishFeaturesConfig(
                    publish_start_time=time_utils.datetime_to_proto(self.publish_start_time),
                    sink_config=self.publish_sink._to_proto(),
                )
            )
        return publish_features_config
