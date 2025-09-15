#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from __future__ import annotations

import pathlib
import typing
from typing import Annotated

import rich
import rich.progress
import rich.prompt
from rich.table import Column, Table, box
from typer import Exit, Option, Typer

from pendingai.api_resources.object import ListObject
from pendingai.cli.console import Console
from pendingai.cli.context import PendingAiContext
from pendingai.cli.shared import JsonOption, LimitOption
from pendingai.cli.utils import catch_exception
from pendingai.services.generator.models import Model

cout = Console()
app = Typer(
    name="generator",
    help=(
        "Powerful and efficient solution for creating novel, diverse, drug-like "
        "molecules. For more information refer to the documentation with "
        "<pendingai docs>."
    ),
    short_help="Generative solution for molecules.",
    no_args_is_help=True,
)


# region command: models -----------------------------------------------


@app.command(
    "models",
    help=("List available molecule generator models."),
    short_help="List molecule generator models.",
)
@catch_exception()
def models(ctx: PendingAiContext, json: JsonOption = False, limit: LimitOption = 100):
    # List available generator models with a limit parameter on returned
    # model resources; default limit is 100 but can be increased to make
    # repeated calls until the requested number of models is met.
    models: list[Model] = []
    next_page_cursor: str | None = None
    while len(models) < limit:
        model_list: ListObject[Model] = ctx.obj["client"].generator.models.list(
            limit=min(100, limit - len(models)),
            next_page=next_page_cursor,
        )
        models.extend(model_list.data)
        if len(models) >= limit or not model_list.has_more:
            break
        next_page_cursor = model_list.data[-1].id

    # Retrieve the status for each model and prepare results for
    # output to the console; if no models are available then print
    # a warning and exit with a non-zero status code.
    res: list = [
        (model, ctx.obj["client"].generator.models.status(model.id).status)
        for model in models[:limit]
    ]
    if len(res) == 0:
        cout.print("[warn]! No generator models available.")
        raise Exit(1)
    if json:
        cout.print_json(data=res)
    else:
        t = Table("ID", "Name", Column("Version", style="dim"), "Status", box=box.SQUARE)
        for model, status in res:
            t.add_row(
                model.id,
                model.name if model.name else "[dim i]unknown",
                model.version if model.version else "[dim i]unknown",
                status.title(),
            )
        cout.print(t)


# region command: sample -----------------------------------------------


def _generate_sample_output_file() -> pathlib.Path:
    fix: str = "pendingai_generator_sample"
    cwd: pathlib.Path = pathlib.Path.cwd()
    matches: list = sorted([x for x in cwd.iterdir() if x.name.startswith(fix)])
    count: int = (
        int(matches[-1].with_suffix("").name.split("_")[-1]) if len(matches) else 0
    )
    return cwd / f"{fix}_{count + 1:>03d}.smi"


@app.command(
    "sample",
    help=(
        "Sample molecule SMILES from a generator model and output "
        "results to a file. Select a model for sampling by its "
        "unique id."
    ),
    short_help="Sample molecules from a generator model.",
)
@catch_exception()
def sample(
    ctx: PendingAiContext,
    path: Annotated[
        pathlib.Path,
        Option(
            "-o",
            "--output-file",
            default_factory=_generate_sample_output_file,
            show_default=False,
            help=(
                "Output filepath to store SMILES. "
                "Defaults to 'pendingai_generator_sample_XXX.smi' in "
                "the current working directory."
            ),
            writable=True,
            dir_okay=False,
            file_okay=True,
            resolve_path=True,
        ),
    ],
    samples: Annotated[
        int,
        Option(
            "-n",
            "--num-samples",
            help="Number of samples to generate. Defaults to 500.",
            show_choices=False,
            show_default=False,
            metavar="INTEGER",
            min=1,
            max=1_000_000,
        ),
    ] = 500,
    file_append: Annotated[
        bool,
        Option(
            "-a",
            "--append",
            help=("Append to the output file without prompting."),
        ),
    ] = False,
    model_id: Annotated[
        str | None,
        Option(
            "--model",
            "-m",
            help=(
                "Model id to use for generation. If unspecified, "
                "uses any available generator model for sampling."
            ),
        ),
    ] = None,
    file_overwrite: Annotated[
        bool,
        Option(
            "-f",
            "--force",
            help="Force overwrite of the output file without being prompted.",
        ),
    ] = False,
):
    # Detect if the output file exists and set the correct write flag to
    # either append to file or overwrite the file contents; requires the
    # user to specify overwrite if the file exists without a flag.
    flag: str = "w"
    if path.exists() and file_overwrite:
        flag = "w"
    elif path.exists() and file_append and not file_overwrite:
        flag = "a"
    elif path.exists():
        prompt: str = f"[warn]? Would you like to overwrite the file: {path.name}"
        if not rich.prompt.Confirm.ask(prompt, console=cout):
            cout.print(f"[warn]! See --append for appending to file: {path.name}")
            raise Exit()
        flag = "w"

    # Validate the provided model id exists and is ready for sampling;
    # when no model id is provided, check that at least one model is
    # available and ready for sampling.
    if model_id:
        try:
            status: str = ctx.obj["client"].generator.models.status(model_id).status
        except Exception:
            cout.print(f"[fail]! Model does not exist: '{model_id}'")
            raise Exit(1)
        if status != "online":
            cout.print(f"[fail]! Model is not ready for sampling: '{model_id}'")
            raise Exit(1)

    else:
        models: list[Model] = ctx.obj["client"].generator.models.list(limit=100).data
        if len(models) == 0:
            cout.print("[fail]! No models available for sampling.")
            raise Exit(1)
        for model in models:
            status = ctx.obj["client"].generator.models.status(model.id).status
            if status == "online":
                cout.print(f"[info]  Selected model '{model.id}' for sampling.")
                model_id = model.id
                break
        else:
            cout.print("[fail]! No models are ready for sampling.")
            raise Exit(1)

    # Open the output file for writing sampled SMILES; use a set to
    # track unique samples and a progress bar to track sampling
    # progress until the requested number of samples is reached.
    writer: typing.Any = path.open(flag)

    # build progress bar to track sampling progress, note that file
    # content is being written on each iteration and does not need to
    # wait until the iteration loop is complete
    progress: rich.progress.Progress = rich.progress.Progress(
        rich.progress.SpinnerColumn(finished_text=""),
        *rich.progress.Progress.get_default_columns(),
        rich.progress.TimeElapsedColumn(),
        transient=True,
    )

    # perform sampling until the requested number of samples is finished
    # and uniquely written to file in minibatches
    all_samples: set[str] = set()
    with progress:
        task: rich.progress.TaskID = progress.add_task("Sampling...", total=samples)
        while not progress.finished:
            result: list[str] = (
                ctx.obj["client"].generator.samples.create(size=500).smiles
            )
            sample: set[str] = set(result) - all_samples
            output: list[str] = [x + "\n" for x in sample][: samples - len(all_samples)]
            all_samples = all_samples.union(output)
            writer.writelines(output)
            progress.update(task, completed=len(all_samples))

    cout.print(f"[success]Sampled {len(all_samples)} molecules: {path.name}")
