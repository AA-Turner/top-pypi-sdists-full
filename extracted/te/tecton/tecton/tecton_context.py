import logging
from typing import Any
from typing import Dict
from typing import Optional

from tecton._internals.sdk_decorators import sdk_public_method
from tecton._internals.spark_utils import get_or_create_spark_session
from tecton._internals.spark_utils import log_spark_env
from tecton_core import conf
from tecton_core import spark_type_annotations


logger = logging.getLogger(__name__)


class TectonContext:
    """
    Execute Spark SQL queries; access various utils.
    """

    _current_context_instance: Optional["TectonContext"] = None
    _config: Dict[str, Any] = {}

    def __init__(self, spark: spark_type_annotations.SparkSession):
        log_spark_env(spark)
        self._spark = spark

    @classmethod
    def _set_config(cls, custom_spark_options=None):
        """
        Sets the configs for TectonContext instance.
        To take effect it must be called before any calls to TectonContext.get_instance().

        :param custom_spark_options: If spark session gets created by TectonContext, custom spark options/
        """
        cls._config = {"custom_spark_options": custom_spark_options}

    @classmethod
    @sdk_public_method
    def get_instance(cls) -> "TectonContext":
        """
        Get the singleton instance of TectonContext.
        """
        # If the instance doesn't exist, creates a new TectonContext from
        # an existing Spark context. Alternatively, creates a new Spark context on the fly.
        if cls._current_context_instance is not None:
            return cls._current_context_instance
        else:
            return cls._generate_and_set_new_instance()

    @classmethod
    def set_global_instance(cls, instance: Optional["TectonContext"]):
        """
        Create the singleton instance of TectonContext from the provided spark session.
        """
        cls._current_context_instance = instance

    @classmethod
    def _generate_and_set_new_instance(cls) -> "TectonContext":
        logger.debug("Generating new Spark session")
        spark = get_or_create_spark_session(
            cls._config.get("custom_spark_options"),
        )
        cls._current_context_instance = cls(spark)
        return cls._current_context_instance

    def _get_spark(self) -> spark_type_annotations.SparkSession:
        return self._spark


@sdk_public_method
def set_tecton_spark_session(spark: spark_type_annotations.PySparkSession):
    """
    Configure Tecton to use the provided SparkSession instead of its default.

    :param spark: Spark instance
    """
    TectonContext.set_global_instance(TectonContext(spark))


@sdk_public_method
def get_current_workspace() -> Optional[str]:
    """
    Gets the current workspace set by the "TECTON_WORKSPACE" environment variable,
    Tecton config file, or `tecton workspace select` command.
    When running `tecton plan` or `tecton apply` Tecton uses the workspace returned by this method.
    """
    return conf.get_or_none("TECTON_WORKSPACE")
