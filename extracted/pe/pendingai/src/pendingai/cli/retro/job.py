#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from __future__ import annotations

import enum
import json
import os
import pathlib
import re
import typing
import webbrowser
from datetime import datetime

import rich
import rich.progress
import rich.prompt
import rich.table
import typer
from typer import BadParameter, Typer

from pendingai import config
from pendingai.api_resources.object import ListObject
from pendingai.cli.console import Console
from pendingai.cli.context import PendingAiContext
from pendingai.cli.retro.generate_html import generate_html_report
from pendingai.cli.shared import JsonOption
from pendingai.cli.utils import catch_exception
from pendingai.services.retrosynthesis.jobs import Job
from pendingai.utils import formatters, regex_patterns

cout = Console()
cerr = Console(stderr=True)
app = Typer(
    name="job",
    help=(
        "Operations working on individual retrosynthesis jobs referred to by "
        "their id."
        "\n\nMost commands operate on single jobs only. <result> and <depict> "
        "are capable of processing multiple jobs."
    ),
    short_help="Operations working on individual retrosynthesis jobs.",
)

# region callbacks -----------------------------------------------------


@catch_exception()
def callback_engine(ctx: PendingAiContext, id: str | None) -> str:
    if id:
        try:
            assert id in [x.id for x in ctx.obj["client"].retrosynthesis.engines.list()]
        except Exception:
            raise BadParameter("Retrosynthesis engine was not found.")
    else:
        return ctx.obj["client"].retrosynthesis.engines.list()[0].id
    return id


@catch_exception()
def callback_libraries(ctx: PendingAiContext, ids: list[str] | None) -> list[str]:
    libs: list[str] = [x.id for x in ctx.obj["client"].retrosynthesis.libraries.list()]
    if ids:
        for id in ids:
            if id not in libs:
                raise BadParameter(f"Building block library was not found: '{id}'.")
    else:
        return libs
    return ids


@catch_exception()
def callback_id(id: str | None) -> str | None:
    if id and regex_patterns.JOB_ID_PATTERN.match(id) is None:
        raise BadParameter(f"Invalid job ID format: '{id}'.")
    return id


@catch_exception()
def _job_ids_file_callback(job_ids_file: pathlib.Path | None) -> pathlib.Path | None:
    """
    Validate an optional input filepath containing line-delimited job
    ids and has all entries following the required regex.

    Args:
        job_ids_file (pathlib.Path, optional): Input filepath.

    Raises:
        typer.BadParameter: A job ID does not follow the required regex.

    Returns:
        pathlib.Path: Input filepath.
    """
    if job_ids_file:
        for i, job_id in enumerate(job_ids_file.open("r").readlines(), 1):
            job_id = job_id.strip()
            if regex_patterns.JOB_ID_PATTERN.match(job_id) is None:
                raise typer.BadParameter(f"Invalid job ID format: {job_id} (line {i})")
    return job_ids_file


@catch_exception()
def _output_dir_callback(output_dir: pathlib.Path) -> pathlib.Path:
    """
    Given an output directory optional parameter, if the path does not
    yet exist then confirm with the user and give standard out feedback.

    Args:
        output_dir (pathlib.Path): Output directory to check exists.

    Returns:
        pathlib.Path: Output directory that exists.
    """
    if not output_dir.exists():
        output_dir.mkdir(parents=True)
        cout.print(f"[success]✓ Directory created successfully: {output_dir}")
    else:
        raise typer.Exit(1)
    return output_dir


@catch_exception()
def _get_default_depict_output_dir() -> pathlib.Path:
    """
    Determines the default output directory for the depict command.
    The directory is named 'depict_XXX' where XXX is an incrementing number.
    """
    cwd: pathlib.Path = pathlib.Path.cwd()
    pattern: re.Pattern[str] = re.compile(r"^depict_(\d{3})$")
    max_num: int = 0

    for path in cwd.iterdir():
        if path.is_dir():
            match = pattern.match(path.name)
            if match:
                num = int(match.group(1))
                if num > max_num:
                    max_num = num

    next_num: int = max_num + 1

    if next_num > 999:
        raise typer.BadParameter(
            "Cannot create new 'depict_XXX' directory. Maximum limit of 999 reached."
        )

    return cwd / f"depict_{next_num:03d}"


@catch_exception()
def _default_output_file(suffix: str = ".json") -> pathlib.Path:
    """
    Callable default generator for an output filename for an option.
    Provides an isoformat datetime file name with given suffix in the
    current working directory of the user.

    Args:
        suffix (str, optional): File suffix. Defaults to ".json".

    Returns:
        pathlib.Path: Generated output filename.
    """
    p: pathlib.Path = pathlib.Path.cwd() / datetime.now().isoformat(timespec="seconds")
    return p.with_suffix(suffix)


# region command: submit -----------------------------------------------


@app.command(
    "submit",
    help=(
        "Submit a job to a retrosynthesis engine.\n\n"
        "NOTE: Jobs including their results will be automatically deleted "
        "30 days after completion.\n\n"
        "Building block libraries are repeatable:\n\n"
        "\t<pendingai retro job submit SMILES --library lib1 --library lib2>"
    ),
    short_help="Submit a job to a retrosynthesis engine.",
    no_args_is_help=True,
)
@catch_exception()
def submit(
    ctx: PendingAiContext,
    smiles: typing.Annotated[
        str,
        typer.Argument(
            help="Query molecule smiles.",
            metavar="SMILES",
        ),
    ],
    retrosynthesis_engine: typing.Annotated[
        str | None,
        typer.Option(
            "--engine",
            help="Retrosynthesis engine id. Defaults to primary engine.",
            callback=callback_engine,
        ),
    ] = None,
    building_block_libraries: typing.Annotated[
        list[str] | None,
        typer.Option(
            "--library",
            help="Building block library ids. Defaults to all available libraries.",
            callback=callback_libraries,
        ),
    ] = [],
    number_of_routes: typing.Annotated[
        int,
        typer.Option(
            "--num-routes",
            help="Maximum number of retrosynthetic routes to generate. Defaults to 20.",
            show_default=False,
            metavar="INTEGER",
            min=1,
            max=50,
        ),
    ] = 20,
    processing_time: typing.Annotated[
        int,
        typer.Option(
            "--time-limit",
            help="Maximum processing time in seconds. Defaults to 300.",
            show_default=False,
            metavar="INTEGER",
            min=60,
            max=600,
        ),
    ] = 300,
    reaction_limit: typing.Annotated[
        int,
        typer.Option(
            "--reaction-limit",
            help=(
                "Maximum number of times a specific reaction can "
                "appear in generated retrosynthetic routes. Defaults "
                "to 3."
            ),
            show_default=False,
            metavar="INTEGER",
            min=1,
            max=20,
        ),
    ] = 3,
    building_block_limit: typing.Annotated[
        int,
        typer.Option(
            "--block-limit",
            help=(
                "Maximum number of times a building block can appear "
                "in a single retrosynthetic route. Default to 3."
            ),
            show_default=False,
            metavar="INTEGER",
            min=1,
            max=20,
        ),
    ] = 3,
    render_json: typing.Annotated[
        bool,
        typer.Option(
            "--json",
            help="Render output as JSON.",
        ),
    ] = False,
):
    job: Job = ctx.obj["client"].retrosynthesis.jobs.create(
        smiles,
        retrosynthesis_engine,  # type: ignore
        building_block_libraries,  # type: ignore
        number_of_routes=number_of_routes,
        processing_time=processing_time,
        reaction_limit=reaction_limit,
        building_block_limit=building_block_limit,
    )
    if render_json:
        cout.print_json(data={"job_id": job.id})
    else:
        cout.print(f"[success]✓ Retrosynthesis job submitted with ID: {job.id}")


# region command: status -----------------------------------------------


@app.command("status", help="Get the status of a retrosynthesis job.")
@catch_exception()
def status(
    ctx: PendingAiContext,
    id: typing.Annotated[
        str | None,
        typer.Argument(
            help="Specify a single job ID to generate route depictions.",
            callback=callback_id,
            metavar="[JOB_ID]",
        ),
    ],
    output_json: JsonOption = False,
):
    status: str = ctx.obj["client"].retrosynthesis.jobs.retrieve(id).status  # type: ignore
    if output_json:
        cout.print_json(data={"status": status})
    else:
        if status == "completed":
            cout.print(f"[success]✓ Retrosynthesis job is complete: {id}")
        elif status == "failed":
            cout.print(f"[red]! Retrosynthesis job failed: {id}")
        elif status == "processing":
            cout.print(f"[warn]! Retrosynthesis job is in progress: {id}")
        else:
            cout.print(f"[warn]! Preparing retrosynthesis job: {id}")

    return status


# region command: result -----------------------------------------------


@app.command(
    "result",
    help=(
        "Retrieve results for one or more retrosynthesis jobs by ID. The command "
        "is slower than batch-based screening and retrieves results individually. "
        "Results are written to file as JSON.\n\n"
        "NOTE: Provide either a single [JOB_ID] or --input-file argument."
    ),
    short_help="Retrieve results for one or more retrosynthesis jobs.",
    no_args_is_help=True,
)
@catch_exception()
def result(
    ctx: PendingAiContext,
    output_file: typing.Annotated[
        pathlib.Path,
        typer.Option(
            "--output-file",
            "-o",
            default_factory=_default_output_file,
            show_default=False,
            help=(
                "Specified JSON output file for writing results to. Defaults to "
                "an ISO-8601 formatted filename in the working directory."
            ),
            writable=True,
            dir_okay=False,
            file_okay=True,
            resolve_path=True,
        ),
    ],
    job_id: typing.Annotated[
        str | None,
        typer.Argument(
            help="Specify a single job ID to generate route depictions.",
            callback=callback_id,
            metavar="[JOB_ID]",
        ),
    ] = None,
    input_file: typing.Annotated[
        pathlib.Path | None,
        typer.Option(
            "--input-file",
            "-i",
            help="Input file of line-delimited job IDs to retrieve results for.",
            callback=_job_ids_file_callback,
            dir_okay=False,
            file_okay=True,
            exists=True,
            resolve_path=True,
        ),
    ] = None,
):
    # xor on the input file and job id parameters to enforce only either
    # a mini-batch operation or a single job lookup to get results.
    if (job_id and input_file) or (not job_id and not input_file):
        raise typer.BadParameter('Provide one of "--input-file" or "[JOB_ID]".')

    # confirm the operation if the output path already exists and is ok
    # with overwriting the filepath.
    if output_file.exists():
        prompt: str = f"[warn]! Do you want to overwrite the file: {output_file}?"
        if not rich.prompt.Confirm.ask(prompt, console=cout):
            raise typer.Exit(0)

    # prepare all job ids from the mini-batch or single argument input as
    # a list of job ids to build a progress bar for retrieving results.
    ids: list[str] = [job_id] if job_id else []
    if input_file:
        ids = list(set([x.strip() for x in input_file.open().readlines()]))
        cout.print(f"[success][not b]✓ Found {len(ids)} unique job id(s).")

    # iterate over each job id and collect the id and optional result as
    # a tuple pair; provide feedback on any results that were missing
    # or possibly incomplete.
    results: list[tuple[str, dict | None]] = []
    with rich.progress.Progress(transient=True) as progress:
        for x in progress.track(ids, description="Retrieving results"):
            result: dict | None = ctx.obj["client"].retrosynthesis.jobs.retrieve(x)
            results.append((x, result))
    for x in [job_id for job_id, result in results if result is None]:
        cout.print(f"[not b][warn]! Retrosynthesis job not found or incomplete: {x}")

    # output a final completion summary of collected jobs that were
    # completed with results and write json to the output file.
    if len(completed := [x for _, x in results if x is not None]) > 0:
        cout.print(f"[success][not b]✓ Found {len(completed)} completed job(s).")
        json.dump(completed, output_file.open("w"), indent=2)
        filesize: str = formatters.format_filesize(os.path.getsize(output_file))
        cout.print(f"[success][not b]✓ Results saved to {output_file} ({filesize})")
    else:
        cout.print("[warn]! Found 0 completed job(s).")


# region command: list -------------------------------------------------


# status enum is required when specifying valid options for a string
# typer option parameter.
class Status(str, enum.Enum):
    """Status enumeration."""

    COMPLETED = "completed"
    FAILED = "failed"
    SUBMITTED = "submitted"
    PROCESSING = "processing"


@app.command(
    "list",
    help=(
        "Retrieve a page of retrosynthesis jobs. Displays select search "
        "parameters and a binary synthesizability flag. Use <pendingai "
        "retro job result> to retrieve retrosynthetic routes of completed jobs."
    ),
    short_help="Retrieve a page of retrosynthesis jobs.",
)
@catch_exception()
def _list(
    ctx: PendingAiContext,
    page: typing.Annotated[
        int,
        typer.Option(
            "--page",
            help="Page number being fetched.",
            show_choices=False,
            show_default=False,
            metavar="INTEGER",
            min=1,
        ),
    ] = 1,
    page_size: typing.Annotated[
        int,
        typer.Option(
            "--page-size",
            help="Number of results per page.",
            show_default=False,
            metavar="INTEGER",
            min=1,
            max=25,
        ),
    ] = 10,
    filter_status: typing.Annotated[
        Status | None,
        typer.Option(
            "--status",
            help="Optional filter for matching status.",
        ),
    ] = None,
    render_json: JsonOption = False,
):
    page_data: ListObject[Job] = ctx.obj["client"].retrosynthesis.jobs.list(
        page=page, size=page_size, status=filter_status.value if filter_status else None
    )

    # capture the case where the page limit has been exceeded by --page
    # or if the page data contains no job results; exit both with non-
    # zero exit status.
    if len(page_data.data) == 0:
        cout.print("[yellow]! No results found with the given filter.")
        raise typer.Exit(1)

    if render_json:
        cout.print_json(data=page_data.data)  # type: ignore

    else:
        # instantiate the table of results to display to the user; add
        # all columns and global column formatting; avoid adding width
        # constraints to impact when smaller screens are used.
        table = rich.table.Table(
            rich.table.Column("ID"),
            rich.table.Column("Created"),
            rich.table.Column("Molecule", max_width=50),
            rich.table.Column("Status"),
            rich.table.Column("Synthesizable", justify="right"),
            box=rich.table.box.SQUARE,
            caption=f"Page {page} of {'many' if page_data.has_more else page}",
        )

        for result in page_data.data:
            # map the status value into a colour; map synthesis outcome
            # depending on whether the job is complete and add colour.
            synthesizable: str = (
                "[green]Yes"
                if len(result.routes) > 0
                else ("[red]No" if result.status == "completed" else "[dim i]n/a")
            )
            result.status = {
                "completed": "[reverse green]",
                "failed": "[reverse red]",
                "processing": "[reverse yellow]",
                "submitted": "[reverse]",
            }[result.status] + result.status.title()
            table.add_row(
                result.id,
                formatters.localize_datetime(result.created).isoformat(" ", "seconds"),
                result.query,
                result.status,
                synthesizable,
            )

        cout.print(table)


# region command: delete ----------------------------------------------


@app.command("delete", help="Delete a retrosynthesis job.")
@catch_exception()
def delete_job(
    ctx: PendingAiContext,
    job_id: typing.Annotated[
        str | None,
        typer.Argument(
            help="Specify a single job ID to generate route depictions.",
            callback=callback_id,
            metavar="[JOB_ID]",
        ),
    ],
    render_json: JsonOption = False,
) -> None:
    """
    Delete a retrosynthesis job by id and provide the feedback in a
    readable format to the user; capture when the job id does not exist
    or if the delete command fails.

    Args:
        context (Context): App runtime context.
        job_id (str): Retrosynthesis job id to delete.
        render_json (bool, optional): Render output as json.

    Raises:
        typer.Exit: Retrosynthesis job id was not found.
    """
    ctx.obj["client"].retrosynthesis.jobs.delete(job_id)  # type: ignore

    if render_json:
        cout.print_json(data={"success": True})
    else:
        cout.print(f"[success]✓ Retrosynthesis job deleted successfully: {job_id}")


# region command: depict -----------------------------------------------


@app.command("routes", help="Visualize generated routes in Pending AI Labs.")
@catch_exception()
def open_routes_in_browser(
    ctx: PendingAiContext,
    job_id: typing.Annotated[
        str,
        typer.Argument(
            help="Specify a single job ID to visualize.",
            callback=callback_id,
            metavar="[JOB_ID]",
        ),
    ],
):
    # redirect to jobs page
    url: str = config.PENDINGAI_LABS_URL[ctx.obj["client"]._context._environment.value]
    webbrowser.open(f"{url}synthesisJob/{job_id}/")


# region command: depict -----------------------------------------------


@app.command(
    "depict",
    help=(
        "Generate depictions of retrosynthetic routes for jobs. "
        "Specify either a [JOB_ID] or --input-file containing job IDs. "
        "HTML files are saved in a specified output directory (or 'depict_XXX' "
        "by default). The web browser will then open automatically."
    ),
    short_help="Get route depictions for one or more retrosynthesis jobs.",
    no_args_is_help=True,
)
@catch_exception()
def depict_retrosynthesis_results(
    ctx: PendingAiContext,
    output_directory: typing.Annotated[
        pathlib.Path,
        typer.Option(
            "--output-dir",
            "-o",
            help="Directory where generated files with depictions will be saved.",
            callback=_output_dir_callback,
            default_factory=_get_default_depict_output_dir,
            show_default=False,
            file_okay=False,
            dir_okay=True,
        ),
    ],
    job_id: typing.Annotated[
        str | None,
        typer.Argument(
            help="Specify a single job ID to generate route depictions.",
            callback=callback_id,
            metavar="[JOB_ID]",
        ),
    ] = None,
    job_ids_file: typing.Annotated[
        pathlib.Path | None,
        typer.Option(
            "--input-file",
            "-i",
            help="Path to a file containing multiple job IDs (one per line) to process.",
            callback=_job_ids_file_callback,
            resolve_path=True,
            file_okay=True,
            dir_okay=False,
            exists=True,
        ),
    ] = None,
) -> None:
    if (job_id and job_ids_file) or (not job_id and not job_ids_file):
        raise typer.BadParameter('Provide one of "--input-file" or "[JOB_ID]".')

    ids: list[str] = [job_id] if job_id else []
    if job_ids_file:
        ids = list(set([x.strip() for x in job_ids_file.open().readlines()]))
        cout.print(f"[success][not b]✓ Found {len(ids)} unique job id(s).")

    jobs: list[Job] = []
    for id in ids:
        with cout.status(f"Retrieving results for job with ID: '{id}'."):
            try:
                job: Job = ctx.obj["client"].retrosynthesis.jobs.retrieve(id)
                assert len(job.routes)
                jobs.append(job)
            except Exception:
                cout.print(f"[warn]! Job contains no results: {id}")
    if len(jobs):
        generate_html_report(output_directory, *jobs)
        cout.print(f"[success]✓ Generated HTML output in directory: {output_directory}")
        webbrowser.open_new_tab(f"file://{output_directory.resolve()}/index.html")
    else:
        cout.print("[success]✓ No synthesizable jobs found")
