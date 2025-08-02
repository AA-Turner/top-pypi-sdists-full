from collections.abc import Mapping

import polars as pl
from tqdm import tqdm

from ..analysis.cohort import create_cohorts
from ..config.config import Config, load_config
from ..data.loading import load_all_register_data, load_icd10_codes, process_all_data
from ..data.table_creation import link_children_to_parents, prepare_income_data
from ..data.transformation import transform_data
from ..data.validation import check_logical_consistency, check_missing_values, check_outliers
from ..utils.logger import setup_colored_logger
from ..utils.pipeline import Pipeline
from ..utils.reports import (
    generate_demographic_report,
    generate_economic_report,
    generate_health_report,
    generate_integrated_analysis_report,
)


class DataProcessor:
    def __init__(self, config_path: str):
        self.config: Config = load_config(config_path)
        self.register_data: Mapping[str, pl.LazyFrame | None] = {}
        self.tables: dict[str, pl.LazyFrame | None] = {}  # Changed from Mapping to dict

        self.pipeline = Pipeline()
        self.icd10_codes = load_icd10_codes(self.config)
        self.logger = setup_colored_logger(__name__)
        self._setup_pipeline()

    def _setup_pipeline(self) -> None:
        self.pipeline.add_step(self.load_data)
        self.pipeline.add_step(self.process_data)
        self.pipeline.add_step(self.validate_data)
        self.pipeline.add_step(self.transform_data)
        self.pipeline.add_step(self.create_cohorts)
        self.pipeline.add_step(self.prepare_data_for_analysis)
        self.pipeline.add_step(self.generate_reports)
        self.pipeline.add_step(self.analyze_data)

    def run(self) -> None:
        total_steps = len(self.pipeline.steps)
        with tqdm(total=total_steps, desc="Overall Progress") as pbar:
            for step in self.pipeline.steps:
                step()
                pbar.update(1)

    def load_data(self) -> None:
        self.logger.info("Loading data from registers")
        self.register_data = load_all_register_data(self.config)
        for register, data in self.register_data.items():
            if data is not None:
                self.logger.info(
                    f"Loaded {data.select(pl.count()).collect().item()} rows for {register}"
                )
            else:
                self.logger.warning(f"No data loaded for register {register}")
        self.logger.info("Data loaded successfully from all registers")

    def process_data(self) -> None:
        self.logger.info("Processing data")
        self.tables = dict(process_all_data(dict(self.register_data)))  # Ensure it's a dict
        for name, table in self.tables.items():
            if table is not None:
                self.logger.info(
                    f"Created {name} table with {table.select(pl.count()).collect().item()} rows"
                )
            else:
                self.logger.warning(f"Failed to create {name} table")
        self.logger.info("Data processed successfully")

    def transform_data(self) -> None:
        self.logger.info("Applying data transformations")
        self.tables = dict(transform_data(dict(self.tables), self.config))  # Ensure it's a dict
        self.logger.info("Data transformations applied successfully")

    def validate_data(self) -> None:
        self.logger.info("Validating data")
        for name, df in tqdm(self.tables.items(), desc="Validating Data"):
            if df is not None:
                self.logger.info(f"Validating {name} table")
                check_missing_values(df, name)
                check_outliers(df, name, self.config.NUMERIC_COLS)
                check_logical_consistency(df, name)
            else:
                self.logger.warning(f"Skipping validation for {name} table as it is None")
        self.logger.info("Data validation completed")

    def create_cohorts(self) -> None:
        self.logger.info("Creating cohorts")
        diagnosis_table = self.tables.get("Diagnosis")
        child_table = self.tables.get("Child")

        if diagnosis_table is None:
            raise ValueError("Diagnosis table is missing")
        if child_table is None:
            raise ValueError("Child table is missing")

        self.logger.info(f"Diagnosis table schema: {diagnosis_table.collect_schema()}")
        self.logger.info(f"Child table schema: {child_table.collect_schema()}")

        self.logger.info(
            f"Diagnosis table has {diagnosis_table.select(pl.count()).collect().item()} rows"
        )
        self.logger.info(f"Child table has {child_table.select(pl.count()).collect().item()} rows")

        exposed_cohort, unexposed_cohort = create_cohorts(
            self.tables, self.config, self.icd10_codes
        )

        self.logger.info(
            f"Created exposed cohort with {exposed_cohort.select(pl.count()).collect().item()} children"
        )
        self.logger.info(
            f"Created unexposed cohort with {unexposed_cohort.select(pl.count()).collect().item()} children"
        )

        self.tables["ExposedCohort"] = exposed_cohort
        self.tables["UnexposedCohort"] = unexposed_cohort
        self.logger.info("Cohorts created and saved successfully")

    def prepare_data_for_analysis(self) -> None:
        self.logger.info("Preparing data for analysis")

        child_table = self.tables.get("Child")
        person_table = self.tables.get("Person")
        income_table = self.tables.get("Income")

        if child_table is None or person_table is None or income_table is None:
            self.logger.error("Missing required tables for analysis preparation")
            return

        parent_child_links = link_children_to_parents(child_table, person_table)
        self.logger.info(
            f"Linked {parent_child_links.select(pl.count()).collect().item()} children to parents"
        )

        prepared_income_data = prepare_income_data(income_table, parent_child_links)
        self.logger.info(
            f"Prepared income data for {prepared_income_data.select(pl.count()).collect().item()} child-years"
        )

        self.tables["PreparedIncomeData"] = prepared_income_data

    def generate_reports(self) -> None:
        self.logger.info("Generating reports")
        reports = [
            generate_health_report,
            generate_economic_report,
            generate_demographic_report,
            generate_integrated_analysis_report,
        ]
        for report in tqdm(reports, desc="Generating Reports"):
            report(self.tables)
        self.logger.info("Reports generated successfully")

    def analyze_data(self) -> None:
        self.logger.info("Performing data analysis")

        exposed_cohort = self.tables.get("ExposedCohort")
        unexposed_cohort = self.tables.get("UnexposedCohort")
        prepared_income_data = self.tables.get("PreparedIncomeData")

        if exposed_cohort is None or unexposed_cohort is None or prepared_income_data is None:
            self.logger.error("Missing required data for analysis")
            return

        # Example analysis (you should replace this with your actual analysis)
        exposed_income = (
            prepared_income_data.join(exposed_cohort, on="child_id")
            .group_by("year")
            .agg([pl.col("parental_total_income").mean().alias("avg_income_exposed")])
        )

        unexposed_income = (
            prepared_income_data.join(unexposed_cohort, on="child_id")
            .group_by("year")
            .agg([pl.col("parental_total_income").mean().alias("avg_income_unexposed")])
        )

        income_comparison = exposed_income.join(unexposed_income, on="year")

        self.logger.info("Income comparison by year:")
        self.logger.info(income_comparison.collect().to_pandas().to_string())

        self.logger.info("Data analysis completed")
