#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from __future__ import annotations

import pathlib
import typing

import rich
import rich.progress
import rich.prompt
import typer
from rich.table import Column, Table, box
from typer import Exit, Typer

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
    # collect model resources by enumerating list pointers; for each
    # model we also want to know the status to render
    models: list[Model] = []
    r: ListObject[Model] = ctx.obj["client"].generator.models.list()
    models.extend(r.data)
    while len(models) < limit:
        r = ctx.obj["client"].generator.models.list(created_after=models[-1].id)
        models.extend(r.data)
        if not r.has_more:
            break
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
    output_file: typing.Annotated[
        pathlib.Path,
        typer.Option(
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
    samples: typing.Annotated[
        int,
        typer.Option(
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
    append_flag: typing.Annotated[
        bool,
        typer.Option(
            "-a",
            "--append",
            help=("Append to the output file without prompting."),
        ),
    ] = False,
    model_id: typing.Annotated[
        str | None,
        typer.Option(
            "--model",
            "-m",
            help=(
                "Model id to use for generation. If unspecified, "
                "uses any available generator model for sampling."
            ),
        ),
    ] = None,
):
    # validate output file and append flags to correctly prepare where
    # sampled molecules are written with an output io wrapper flag
    output_file_flag: str = "w"
    prompt: str = f"[warn]? Would you like to overwrite the file: {output_file.name}"
    if output_file.exists() and append_flag:
        cout.print(f"[warn]! Appending results to file: {output_file.name}")
        output_file_flag = "a"
    elif output_file.exists() and not rich.prompt.Confirm.ask(prompt, console=cout):
        cout.print(f"[warn]! See --append for appending to file: {output_file.name}")
        raise typer.Exit(0)
    writer: typing.Any = output_file.open(output_file_flag)

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
                ctx.obj["client"].generator.generate.call(id=model_id, n=500).smiles
            )
            sample: set[str] = set(result) - all_samples
            output: list[str] = [x + "\n" for x in sample][: samples - len(all_samples)]
            all_samples = all_samples.union(output)
            writer.writelines(output)
            progress.update(task, completed=len(all_samples))

    cout.print(f"[success]Sampled {len(all_samples)} molecules: {output_file.name}")
