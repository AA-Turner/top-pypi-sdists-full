import dlt

from dlthub.legacy.transformations.base_transformation import Transformation
from dlthub.dbt_generator.config import DbtGeneratorConfig, resolve_dbt_configuration
from dlthub.dbt_generator.render import render_dbt_project, render_mart

ALLOWED_DBT_VERSION = ">=1.9,<1.12"


class DbtTransformation(Transformation):
    def _get_dbt_generator_config(
        self, cache_pipeline: dlt.Pipeline, schema: dlt.Schema = None, force: bool = False
    ) -> DbtGeneratorConfig:
        config = DbtGeneratorConfig(
            base_folder=self.transformations_path,
            render_readme_file=False,
            render_run_script=False,
            package_name=self.config["package_name"],
            force=force,
        )
        config.update_from_pipeline(cache_pipeline, schema)
        return resolve_dbt_configuration(config)

    def render_transformation_layer(self, force: bool = False) -> None:
        """Renders a starting point for the t-layer"""
        schema = self.cache.discover_input_schema()
        cache_pipeline = self.cache.get_cache_pipeline_for_dbt(self.cache.get_cache_dataset())
        config = self._get_dbt_generator_config(cache_pipeline, schema, force)
        render_dbt_project(config)
        render_mart(config)

    def _do_transform(self) -> None:
        cache_pipeline = self.cache.get_cache_pipeline_for_dbt(self.cache.get_cache_dataset())
        # TODO: we do this only to get venv_location. this will be moved to OSS
        config = resolve_dbt_configuration(
            DbtGeneratorConfig(
                base_folder=self.transformations_path,
                package_name=self.config["package_name"],
            )
        )
        venv = dlt.dbt.get_venv(
            cache_pipeline, venv_path=config.venv_location, dbt_version=ALLOWED_DBT_VERSION
        )
        dbt = dlt.dbt.package(cache_pipeline, self.transformation_layer_path, venv=venv)

        # run transformations
        dbt.run_all(
            # add any additional vars you need in dbt here
            additional_vars={},
            # change this to save your transformation results into another dataset
            destination_dataset_name=self.cache.config["transformed_dataset_name"],
        )
