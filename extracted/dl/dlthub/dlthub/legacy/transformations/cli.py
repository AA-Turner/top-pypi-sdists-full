"""Cli for transformations"""

import os
import argparse

from dlt.common.schema.utils import to_pretty_yaml
from dlt._workspace.cli import SupportsCliCommand, echo as fmt

from dlthub.common.cli import add_project_opts
from dlthub.project.pipeline_manager import EntityFactory
from dlthub.project.cli.helpers import project_from_args_with_cli_output


class TransformationCommand(SupportsCliCommand):
    command = "transformation"
    help_string = "Run dbt transformations for dlthub project. Experimental."
    description = """
Commands to run dbt transformations on local cache in dlthub projects

**This is an experimental feature and will change substantially in the future.**

**Do not use in production.**
"""

    def configure_parser(self, parser: argparse.ArgumentParser) -> None:
        self.parser = parser
        add_project_opts(parser)

        parser.add_argument(
            "pond_name",
            help="Name of the transformation, use '.' for the first one found in project.",
        )

        operation_parser = parser.add_subparsers(
            title="Available subcommands",
            dest="operation",
            required=True,
        )

        # add all ops
        operation_parser.add_parser(
            "list", help="List all transformations discovered in this directory"
        )

        operation_parser.add_parser(
            "info", help="Transformation info: locations, cache status etc."
        )

        operation_parser.add_parser(
            "run", help="Sync cache, run transformation and commit the outputs"
        )

        operation_parser.add_parser(
            "verify-inputs",
            help="Verify that cache can connect to all defined inputs and that tables "
            + "declared are available",
        )

        operation_parser.add_parser(
            "verify-outputs",
            help="Verify that the output cache dataset contains all tables declared",
        )

        operation_parser.add_parser("populate", help="Sync data from inputs to input cache dataset")

        operation_parser.add_parser("flush", help="Flush data from output cache dataset to outputs")

        operation_parser.add_parser(
            "transform",
            help="Run transformations on input cache dataset and write to output cache dataset",
        )

        operation_parser.add_parser(
            "populate-state", help="Populate transformation state from defined output"
        )
        operation_parser.add_parser(
            "flush-state", help="Flush transformation state to defined output"
        )

        operation_parser.add_parser(
            "render-t-layer", help="Render a starting point for the t-layer"
        )

    def execute(self, args: argparse.Namespace) -> None:
        run_context = project_from_args_with_cli_output(args)

        factory = EntityFactory(run_context.project)
        # list
        if args.operation == "list":
            # _import_ponds()
            available_transformations = list(run_context.project.transformations)
            fmt.echo(f"Available transformations: {available_transformations}")

        # individual pond ops
        transformation = factory.get_transformation(args.pond_name)
        if args.operation == "run":
            transformation.run()
        elif args.operation == "verify-inputs":
            transformation.cache.verify_inputs()
        elif args.operation == "verify-outputs":
            transformation.cache.verify_outputs()
        elif args.operation == "transform":
            transformation.transform()
        elif args.operation == "populate":
            transformation.cache.populate()
        elif args.operation == "flush":
            transformation.cache.flush()
        elif args.operation == "populate-state":
            transformation.populate_state()
        elif args.operation == "flush-state":
            transformation.flush_state()
        elif args.operation == "render-t-layer":
            transformation.render_transformation_layer()
        elif args.operation == "info":
            fmt.echo("Engine: %s" % fmt.bold(transformation.config["engine"]))
            t_package_path = transformation.transformation_layer_path
            fmt.echo("Transformation location: %s" % fmt.bold(t_package_path))
            fmt.echo("Config:")
            fmt.echo(to_pretty_yaml(transformation.config))  # type: ignore[arg-type]
            if os.path.exists(t_package_path):
                pass
            else:
                fmt.warning("t-layer not yet rendered")
        # elif args.operation == "show-inputs":
        #     from dlt._workspace.cli.pipeline_command import pipeline_command
        #     pipeline = pond._get_input_pipeline(pond.config["inputs"][0])
        #     pipeline.sync_destination()
        #     pipeline_command("show", pipeline.pipeline_name, pipeline.pipelines_dir, 0)
        # elif args.operation == "show-outputs":
        #     from dlt._workspace.cli.pipeline_command import pipeline_command
        #     pipeline = pond._get_output_pipeline(pond.config["outputs"][0])
        #     pipeline.sync_destination()
        #     # os.environ["CREDENTIALS"] = pond.cache_location
        #     pipeline_command("show", pipeline.pipeline_name, pipeline.pipelines_dir, 0)
