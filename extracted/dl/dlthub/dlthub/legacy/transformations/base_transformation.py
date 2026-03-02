import os

from dlt import Pipeline
from dlt.common.exceptions import DltException
from dlt.common.utils import custom_environ

from dlthub.legacy.transformations.const import PROCESSED_LOAD_IDS_TABLE
from dlthub.cache.cache import Cache


from dlthub.legacy.transformations.config import TransformationConfig, set_defaults_and_validate


class TransformationException(DltException):
    pass


class Transformation:
    def __init__(self, config: TransformationConfig) -> None:
        self.config = set_defaults_and_validate(config)

    #
    # Main flow
    #
    def run(self, drop_cache: bool = False) -> None:
        """Runs the full transformation including cache populate and flush"""
        if drop_cache:
            self.cache.drop()
        self.populate_state()
        self.cache.populate()
        self.transform()
        self.cache.flush()
        # write state to the output dataset
        self.flush_state()

    @property
    def cache(self) -> Cache:
        cache = self.config.get("cache")
        if not isinstance(cache, Cache):
            raise Exception("Cache config is missing or unresolved")
        return cache

    def populate_state(self) -> None:
        """Loads processed load ids from the warehouse into the output dataset of the cache"""
        if not self.state_output_pipeline:
            return

        with self.state_output_pipeline.destination_client() as client:
            if not client.is_storage_initialized():
                return

        # load states
        process_loads_relation = self.state_output_pipeline.dataset()(
            f"SELECT load_id, inserted_at FROM {PROCESSED_LOAD_IDS_TABLE}", _execute_raw_query=True
        )
        cache_output_dataset = self.cache.get_cache_dataset(True)
        # make sure that _dlt_id and _load_id are never added here
        # NOTE: actually this is a hack. PROCESSED_LOAD_IDS_TABLE is sometimes created externally
        # ie by dbt
        with custom_environ({
            "NORMALIZE__PARQUET_NORMALIZER__ADD_DLT_LOAD_ID": "FALSE",
            "NORMALIZE__PARQUET_NORMALIZER__ADD_DLT_ID": "FALSE",
        }):
            cache_output_dataset.save(
                process_loads_relation.iter_arrow(chunk_size=50000),
                table_name=PROCESSED_LOAD_IDS_TABLE,
                write_disposition="replace",
            )

    def flush_state(self) -> None:
        """Writes the state to the output dataset of the cache"""
        if not self.state_output_pipeline:
            return
        cache_output_dataset = self.cache.get_cache_dataset(True)
        with custom_environ({
            "NORMALIZE__PARQUET_NORMALIZER__ADD_DLT_LOAD_ID": "FALSE",
            "NORMALIZE__PARQUET_NORMALIZER__ADD_DLT_ID": "FALSE",
        }):
            self.state_output_pipeline.run(
                cache_output_dataset(
                    f"SELECT load_id, inserted_at FROM {PROCESSED_LOAD_IDS_TABLE}",
                    _execute_raw_query=True,
                ).iter_arrow(50000),
                table_name=PROCESSED_LOAD_IDS_TABLE,
                write_disposition="replace",
            )

    #
    # Transformation layer
    #
    def render_transformation_layer(self, force: bool = False) -> None:
        pass

    def transform(self) -> None:
        """Runs the transform step"""

        if not self.transformation_layer_exists():
            raise TransformationException(
                "Trying to run transform layer, but no project found in "
                f"{self.transformation_layer_path}. Have you created one?"
            )

        # create output dataset in cache
        with self.cache.get_cache_dataset(transformed_data=True).destination_client as client:
            client.initialize_storage()

        with self.cache.with_persistent_secrets():
            self._do_transform()

    def _do_transform(self) -> None:
        pass

    @property
    def state_output_pipeline(self) -> Pipeline:
        """pipeline with dataset that the transformation state is written to"""
        # TODO: make configurable in which output to look for the state
        if not self.cache.config["outputs"]:
            return None
        return self.cache.get_binding_pipeline(self.cache.config["outputs"][0])

    @property
    def transformation_layer_path(self) -> str:
        # make it abs path
        return os.path.join(self.transformations_path, self.config["package_name"])

    @property
    def transformations_path(self) -> str:
        # TODO: we need this only to render and find t layer
        # create object model for transformations and remove from pond
        # like we have resource decoupled from pipeline

        return self.config.get("location")

    def transformation_layer_exists(self) -> bool:
        return os.path.exists(self.transformation_layer_path)
