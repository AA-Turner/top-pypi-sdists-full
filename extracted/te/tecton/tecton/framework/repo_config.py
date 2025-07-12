"""Data models related to the Repo Config (i.e. the repo.yaml file).

See PRD: https://www.notion.so/tecton/PRD-Repo-Config-725bd10a7ce6422eaedaf8786869ea35
"""

import logging
from typing import Optional
from typing import Union

from tecton._internals.tecton_pydantic import StrictModel
from tecton._internals.tecton_pydantic import pydantic_v1
from tecton.framework import configs
from tecton_core import conf


logger = logging.getLogger(__name__)


def _number_to_string(value):
    if isinstance(value, (int, float)):
        return str(value)
    return value


class BatchFeatureViewDefaults(StrictModel):
    tecton_materialization_runtime: Optional[str] = None
    # TODO(jake): The online store default is currently set at data proto creation time based on backend state. This
    # is a very fragile, inconsistent approach that we should reconsider.
    online_store: Optional[configs.OnlineStoreTypes] = pydantic_v1.Field(default=None, discriminator="kind")
    # TODO(jake): Pydantic has several "union modes" - we should strongly prefer discriminated (i.e. using
    #  discriminator) unions because they have better error messages and make that the default or enforce in tests.
    offline_store: Union[configs.OfflineStoreConfig, configs.DeltaConfig, configs.ParquetConfig] = pydantic_v1.Field(
        default_factory=configs.OfflineStoreConfig, discriminator="kind"
    )
    batch_compute: configs.ComputeConfigTypes = pydantic_v1.Field(
        default_factory=configs._DefaultClusterConfig, discriminator="kind"
    )
    environment: Optional[str] = None

    @property
    def offline_store_config(self) -> configs.OfflineStoreConfig:
        if isinstance(self.offline_store, (configs.DeltaConfig, configs.ParquetConfig)):
            return configs.OfflineStoreConfig(staging_table_format=self.offline_store)
        else:
            return self.offline_store


class StreamFeatureViewDefaults(BatchFeatureViewDefaults):
    stream_compute: configs.ComputeConfigTypes = pydantic_v1.Field(
        default_factory=configs._DefaultClusterConfig, discriminator="kind"
    )
    # Defaults for the leading aggregation edge configuration for all stream feature views in the feature repo.
    aggregation_leading_edge: Optional[configs.AggregationLeadingEdgeTypes] = pydantic_v1.Field(
        default=configs.WallClockTime, discriminator="kind"
    )


class FeatureTableDefaults(BatchFeatureViewDefaults):
    pass  # Currently the same as BatchFeatureViewDefaults.


class FeatureServiceDefaults(StrictModel):
    realtime_environment: Optional[str] = None
    transform_server_group: Optional[str] = None
    feature_server_group: Optional[str] = None


class PushConfigDefaults(StrictModel):
    transform_server_group: Optional[str] = None
    ingest_server_group: Optional[str] = None


class StreamSourceDefaults(StrictModel):
    push_config: Optional[PushConfigDefaults] = None


class TectonObjectDefaults(StrictModel):
    batch_feature_view: Optional[BatchFeatureViewDefaults] = None
    stream_feature_view: Optional[StreamFeatureViewDefaults] = None
    feature_table: Optional[FeatureTableDefaults] = None
    feature_service: Optional[FeatureServiceDefaults] = None
    stream_source: Optional[StreamSourceDefaults] = None


class TectonConfSettings(StrictModel):
    isolate_function_deserialization: Optional[bool] = None


class RepoConfig(StrictModel):
    """The data model for the repo config (i.e. the repo.yaml) file."""

    defaults: Optional[TectonObjectDefaults] = None
    repo_options: Optional[TectonConfSettings] = None


# Singleton Repo Config.
_repo_config: Optional[RepoConfig] = None


def set_repo_config(repo_config: RepoConfig) -> None:
    """Set the singleton instance of the repo config."""
    global _repo_config
    if _repo_config is not None:
        logger.warning("Overwriting Tecton repo config that was already set.")
    _repo_config = repo_config
    if repo_config.repo_options is not None:
        conf.REPO_CONFIG.set_all(dict(repo_config.repo_options))


def get_repo_config() -> Optional[RepoConfig]:
    """Get the singleton instance of the repo config. None if it has not been set.

    The repo config is expected to be None in non-plan/apply environments (e.g. notebooks) or if no config is found
    during plan/apply.
    """
    return _repo_config


def get_feature_service_defaults() -> FeatureServiceDefaults:
    """Get the user-specified Feature Service defaults or a default instance if the user did not specify defaults."""
    if _repo_config is None or _repo_config.defaults is None or _repo_config.defaults.feature_service is None:
        return FeatureServiceDefaults()

    return _repo_config.defaults.feature_service


def get_batch_feature_view_defaults() -> BatchFeatureViewDefaults:
    """Get the user-specified Batch FV defaults or a default instance if the user did not specify defaults."""
    if _repo_config is None or _repo_config.defaults is None or _repo_config.defaults.batch_feature_view is None:
        return BatchFeatureViewDefaults()

    return _repo_config.defaults.batch_feature_view


def get_stream_feature_view_defaults() -> StreamFeatureViewDefaults:
    """Get the user-specified Stream FV defaults or a default instance if the user did not specify defaults."""
    if _repo_config is None or _repo_config.defaults is None or _repo_config.defaults.stream_feature_view is None:
        return StreamFeatureViewDefaults()

    return _repo_config.defaults.stream_feature_view


def get_feature_table_defaults() -> FeatureTableDefaults:
    """Get the user-specified Feature Table defaults or a default instance if the user did not specify defaults."""
    if _repo_config is None or _repo_config.defaults is None or _repo_config.defaults.feature_table is None:
        return FeatureTableDefaults()

    return _repo_config.defaults.feature_table


def get_stream_source_defaults() -> StreamSourceDefaults:
    """Get the user-specified Stream Source defaults or a default instance if the user did not specify defaults."""
    if _repo_config is None or _repo_config.defaults is None or _repo_config.defaults.stream_source is None:
        return StreamSourceDefaults()

    return _repo_config.defaults.stream_source
