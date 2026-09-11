"""Backward-compatibility shim — config logic now lives in spark_config_builder.

Names are re-exported here for callers/tests that still import from this module.
They are declared in ``__all__`` so linters treat them as intentional re-exports
rather than unused imports; this is stable across black/isort reformatting,
unlike per-line ``# noqa: F401`` markers which can detach when imports are wrapped.
"""

from sagemaker_studio import Project
from sagemaker_studio.utils.spark.session.spark_config_builder import (
    CATALOG_LIMIT,
    DEFAULT_SPARK_PROPS,
    _generate_irc_spark_configs,
    _generate_s3tables_spark_configs,
    _generate_spark_catalog_spark_configs,
    _get_account_id_from_arn,
)
from sagemaker_studio.utils.spark.session.spark_config_builder import _region as region
from sagemaker_studio.utils.spark.session.spark_config_builder import _stage as stage
from sagemaker_studio.utils.spark.session.spark_config_builder import (
    _utils,
    generate_spark_configs,
    logger,
)

__all__ = [
    "CATALOG_LIMIT",
    "DEFAULT_SPARK_PROPS",
    "_generate_irc_spark_configs",
    "_generate_s3tables_spark_configs",
    "_generate_spark_catalog_spark_configs",
    "_get_account_id_from_arn",
    "region",
    "stage",
    "_utils",
    "generate_spark_configs",
    "logger",
    "Project",
]
