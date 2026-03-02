import argparse
import dlt

from dlt._workspace.cli import echo, SupportsCliCommand

from dlt.pipeline.exceptions import CannotRestorePipelineException
from dlthub.common.license import require_license


class DbtCommand(SupportsCliCommand):
    command = "dbt"
    help_string = "dlthub dbt transformation generator"
    description = None
    docs_url = None

    def configure_parser(self, parser: argparse.ArgumentParser) -> None:
        self.parser = parser

        subparsers = parser.add_subparsers(
            title="Available subcommands", dest="dbt_command", required=True
        )
        gen_parser = subparsers.add_parser("generate", help="Generate dbt project")

        gen_parser.add_argument("pipeline_name", help="The pipeline to create a dbt project for")
        gen_parser.add_argument(
            "--include_dlt_tables",
            help="Do not render _dlt tables",
            action="store_true",
            default=False,
        )
        gen_parser.add_argument(
            "--fact", help="Create a fact table for a given table", default=None, nargs="?"
        )
        gen_parser.add_argument(
            "--force", help="Force overwrite of existing files", action="store_true", default=False
        )
        gen_parser.add_argument(
            "--mart_table_prefix", help="Prefix for mart tables", default="", nargs="?"
        )

    @require_license(scope="dlthub.dbt_generator")
    def execute(self, args: argparse.Namespace) -> None:
        from dlthub.dbt_generator.render import (
            render_dbt_project,
            render_fact_table,
            render_mart,
        )
        from dlthub.dbt_generator.config import DbtGeneratorConfig, resolve_dbt_configuration

        if args.dbt_command == "generate":
            echo.echo(f"Starting dbt_generator for pipeline '{args.pipeline_name}'")

            try:
                pipeline = dlt.attach(pipeline_name=args.pipeline_name)
            except CannotRestorePipelineException:
                echo.error("Could not attach to pipeline. Exiting...")
                exit(1)

            schema = pipeline.default_schema

            config = DbtGeneratorConfig(
                include_dlt_tables=args.include_dlt_tables,
                fact_table=args.fact,
                force=args.force,
                mart_table_prefix=args.mart_table_prefix,
            )
            config.update_from_pipeline(pipeline)
            config = resolve_dbt_configuration(config)

            echo.echo(
                f"Found default schema with name '{schema.name}' and "
                + f"{len(schema.tables)} tables."
            )

            if args.fact:
                echo.echo(
                    f"Will create fact table {args.fact} for existing project for "
                    + f"dataset '{pipeline.dataset_name}' "
                    + f"at '{pipeline.destination.to_name(pipeline.destination)}'."
                )
                table_name = render_fact_table(config=config)
                echo.echo(f"fact table created at {table_name}")

            else:
                echo.echo(
                    f"Will create dbt project to connect to dataset '{pipeline.dataset_name}' "
                    + f"at '{pipeline.destination.to_name(pipeline.destination)}'."
                )

                package_path = render_dbt_project(config=config)
                mart_path = render_mart(config=config)

                echo.echo(f"dbt project created at {package_path}. Mart created in {mart_path}")
