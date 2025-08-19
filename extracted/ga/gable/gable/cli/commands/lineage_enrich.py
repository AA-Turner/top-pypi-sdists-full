import json
import os
import subprocess
import sys

import click
from click.core import Context as ClickContext


@click.command(
    add_help_option=False,
    name="enrich",
)
@click.option(
    "--model",
    type=str,
    default="gpt-4o",
    help="The model to use for the enrichment.",
)
@click.option(
    "--project-root",
    help="The root directory of the project that will be analyzed.",
    type=click.Path(exists=True),
    required=True,
)
@click.option(
    "--sca-results-file",
    type=click.Path(exists=True),
    help="The path to the SCA results file.",
    required=True,
    default=os.path.join(os.getcwd(), "gable_lineage_scan_results.json"),
)
@click.option(
    "--output",
    type=click.Path(exists=False, file_okay=True, dir_okay=False),
    help="File path to output results.",
    required=False,
    default=os.path.join(os.getcwd(), "gable_lineage_scan_results_enriched.json"),
)
@click.option(
    "--field-mapping",
    is_flag=True,
    help="Whether to use field mapping.",
    default=False,
)
@click.pass_context
def lineage_enrich(
    ctx: ClickContext,
    project_root: str,
    model: str,
    sca_results_file: str,
    output: str,
    field_mapping: bool,
):
    """Enrich lineage with AI"""

    run_ai_enrichment(
        project_root,
        model,
        sca_results_file,
        "transform_summaries.json",
        field_mapping,
    )
    result_file = os.path.join(os.getcwd(), "transform_summaries.json")
    results = json.loads(open(result_file).read())["results"]
    paths = json.loads(open(sca_results_file).read())["paths"]
    if len(paths) != len(results):
        raise ValueError("Number of paths and results do not match")

    for path, summary in zip(paths, results):
        path["transformation_summary"] = summary["transform_summary"]
        path["ingress"]["description"] = summary["ingress_point"]["description"]
        path["egress"]["description"] = summary["egress_point"]["description"]

    final_result = {"paths": paths}
    open(output, "w").write(json.dumps(final_result, indent=4))


def run_ai_enrichment(
    project_root: str,
    model: str,
    sca_results_file: str,
    output: str,
    field_mapping: bool,
):
    # Construct the path to the gable-ai executable
    venv_bin_dir = os.path.join(os.getcwd(), ".venv", "bin")
    gable_ai_executable = os.path.join(venv_bin_dir, "gable-ai")

    # Ensure the executable exists
    if not os.path.exists(gable_ai_executable):
        click.echo(
            f"Error: gable-ai executable not found at {gable_ai_executable}", err=True
        )
        sys.exit(1)

    # Build the command arguments
    cmd = [gable_ai_executable, "transform-summaries"]

    # Add all the options
    cmd.extend(["--model", model])
    cmd.extend(["--project-root", project_root])
    cmd.extend(["--input", sca_results_file])
    cmd.extend(["--output", output])

    if field_mapping:
        cmd.append("--field-mapping")

    # Execute the command
    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        return result.returncode
    except subprocess.CalledProcessError as e:
        click.echo(f"Error executing gable-ai: {e}", err=True)
        return e.returncode
    except FileNotFoundError:
        click.echo(
            f"Error: gable-ai executable not found at {gable_ai_executable}", err=True
        )
        return 1
