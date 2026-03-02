from typing import Optional

import os

from dlt import Pipeline, Schema
from dlt.common.schema.utils import has_table_seen_data
from dlt.common.configuration import resolve_configuration
from dlt.common.configuration.specs import configspec, BaseConfiguration

TESTS_FOLDER = "tests"
MACROS_FOLDER = "macros"
ANALYSIS_FOLDER = "analysis"
MODELS_FOLDER = "models"

STAGING_MODELS_FOLDER = "staging"
MARTS_MODELS_FOLDER = "marts"


@configspec
class DbtGeneratorConfig(BaseConfiguration):
    base_folder: str = os.curdir

    include_dlt_tables: bool = False
    fact_table: Optional[str] = ""
    force: bool = False
    """Allows overwrite without question"""
    mart_table_prefix: Optional[str] = ""
    """prefix for the mart tables"""
    fact_table_render_all_columns: bool = False
    """render all columns in fact table"""
    table_type_separator: str = "_"
    """character that separates table type from name"""
    render_readme_file: bool = True
    """wether to render a readme file in the project"""
    render_run_script: bool = True
    """wether to render the main run script of the dbt project"""
    enable_load_id_incremental: bool = True
    """whether to enable the mechanism that runs incrementally by load id"""
    package_name: str = None
    """package name for dbt project"""
    # TODO: move venv_location to DBTRunnerConfiguration
    venv_location: str = "dbt"
    """location of the virtual environment with dbt dependencies.
    use relative path to place it in pipeline folder."""

    # TODO: this should update from dataset, not Pipeline
    def update_from_pipeline(self, pipeline: Pipeline, schema: Optional[Schema] = None) -> None:
        self.project_name = pipeline.pipeline_name
        self.schema = schema or pipeline.default_schema
        self.naming = self.schema.naming

        self.destination = pipeline.destination.to_name(pipeline.destination)
        self.package_name = self.package_name or f"dbt_{self.project_name}"
        self.package_root_folder = os.path.join(self.base_folder, self.package_name)
        self.main_file_name = f"run_{self.project_name}_dbt.py"

        # TODO: allow for pipelines with many schemas by
        # adding separate marts folder per schema name
        self.mart_folder = os.path.join(self.package_root_folder, MODELS_FOLDER)
        self.staging_models_folder = os.path.join(self.mart_folder, STAGING_MODELS_FOLDER)
        self.mart_models_folder = os.path.join(self.mart_folder, MARTS_MODELS_FOLDER)

        # filter eligible tables, _dlt_loads_id must always be included
        self.tables_to_render = {
            name: table
            for name, table in self.schema.tables.items()
            if (has_table_seen_data(table) and not name.startswith(self.schema._dlt_tables_prefix))
            or (name == self.schema.loads_table_name and self.enable_load_id_incremental)
            or (self.include_dlt_tables and name.startswith(self.schema._dlt_tables_prefix))
        }

    __section__ = "dbt_generator"


def resolve_dbt_configuration(config: DbtGeneratorConfig) -> DbtGeneratorConfig:
    # TODO: we should do this automatically on all functions that use config...
    # TODO: we should place this in context of other configs ie. transformations
    return resolve_configuration(config, sections=("transformations",))
