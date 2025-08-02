import difflib
import os
from os import getcwd
from pathlib import Path
from typing import Any, Dict, Generator, Iterable, List, Optional

try:
    from colorama import Back, Fore, Style, init

    init()
except ImportError:  # fallback so that the imported classes always exist

    class ColorFallback:
        def __getattr__(self, name):
            return ""

    Fore = Back = Style = ColorFallback()


import shutil
import sys

import click

from tinybird.datafile.common import get_name_version, get_project_filenames, is_file_a_datasource, peek
from tinybird.sql_template_fmt import DEFAULT_FMT_LINE_LENGTH
from tinybird.tb.client import TinyB
from tinybird.tb.modules.datafile.format_datasource import format_datasource
from tinybird.tb.modules.datafile.format_pipe import format_pipe
from tinybird.tb.modules.datafile.pull import folder_pull
from tinybird.tb.modules.feedback_manager import FeedbackManager


def diff_files(
    from_file: str,
    to_file: str,
    from_file_suffix: str = "[remote]",
    to_file_suffix: str = "[local]",
    with_format: bool = True,
    with_color: bool = False,
    client: Optional[TinyB] = None,
    for_deploy: bool = False,
):
    def file_lines(filename):
        with open(filename) as file:
            return file.readlines()

    def parse(filename, with_format=True, unroll_includes=False):
        extensions = Path(filename).suffixes
        lines = None
        if is_file_a_datasource(filename):
            lines = (
                format_datasource(
                    filename,
                    unroll_includes=unroll_includes,
                    for_diff=True,
                    client=client,
                    replace_includes=True,
                    for_deploy_diff=for_deploy,
                )
                if with_format
                else file_lines(filename)
            )
        elif (".pipe" in extensions) or (".incl" in extensions):
            lines = (
                format_pipe(
                    filename,
                    DEFAULT_FMT_LINE_LENGTH,
                    unroll_includes=unroll_includes,
                    replace_includes=True,
                    for_deploy_diff=for_deploy,
                )
                if with_format
                else file_lines(filename)
            )
        else:
            click.echo(f"Unsupported file type: {filename}")
        if lines:
            return [f"{l}\n" for l in lines.split("\n")] if with_format else lines  # noqa: E741

    try:
        lines1 = parse(from_file, with_format)
        lines2 = parse(to_file, with_format, unroll_includes=True)
    except FileNotFoundError as e:
        filename = os.path.basename(str(e)).strip("'")
        raise click.ClickException(FeedbackManager.error_diff_file(filename=filename))

    if not lines1 or not lines2:
        return

    diff = difflib.unified_diff(
        lines1, lines2, fromfile=f"{Path(from_file).name} {from_file_suffix}", tofile=f"{to_file} {to_file_suffix}"
    )

    if with_color:
        diff = color_diff(diff)

    return diff


def diff_command(
    filenames: Optional[List[str]],
    fmt: bool,
    client: TinyB,
    no_color: Optional[bool] = False,
    with_print: Optional[bool] = True,
    verbose: Optional[bool] = None,
    clean_up: Optional[bool] = False,
    progress_bar: bool = False,
    for_deploy: bool = False,
):
    def is_shared_datasource(name):
        return "." in name

    with_explicit_filenames = filenames
    verbose = True if verbose is None else verbose

    target_dir = getcwd() + os.path.sep + ".diff_tmp"
    Path(target_dir).mkdir(parents=True, exist_ok=True)

    if filenames:
        if len(filenames) == 1:
            filenames = [filenames[0], *get_project_filenames(filenames[0])]
        folder_pull(client, target_dir, True, verbose=False)
    else:
        filenames = get_project_filenames(".")
        if verbose:
            click.echo("Saving remote resources in .diff_tmp folder.\n")
        folder_pull(client, target_dir, True, verbose=verbose, progress_bar=progress_bar)

    remote_datasources: List[Dict[str, Any]] = client.datasources()
    remote_pipes: List[Dict[str, Any]] = client.pipes()

    local_resources = {
        Path(file).resolve().stem: file
        for file in filenames
        if (".datasource" in file or ".pipe" in file) and ".incl" not in file
    }

    changed = {}
    for resource in remote_datasources + remote_pipes:
        properties: Dict[str, Any] = get_name_version(resource["name"])
        name = properties.get("name", None)
        if name:
            (rfilename, file) = next(
                ((rfilename, file) for (rfilename, file) in local_resources.items() if name == rfilename),
                ("", None),
            )
            if not file:
                if not with_explicit_filenames:
                    if with_print:
                        click.echo(f"{resource['name']} only exists remotely\n")
                    if is_shared_datasource(resource["name"]):
                        changed[resource["name"]] = "shared"
                    else:
                        changed[resource["name"]] = "remote"
                continue

            suffix = ".datasource" if ".datasource" in file else ".pipe"
            target = target_dir + os.path.sep + rfilename + suffix

            diff_lines = diff_files(
                target, file, with_format=fmt, with_color=(not no_color), client=client, for_deploy=for_deploy
            )
            not_empty, diff_lines = peek(diff_lines)
            changed[rfilename] = not_empty
            if not_empty and with_print:
                sys.stdout.writelines(diff_lines)
                click.echo("")

    for rfilename, _ in local_resources.items():
        if rfilename not in changed:
            for resource in remote_datasources + remote_pipes:
                properties = get_name_version(resource["name"])
                name = properties.get("name", None)
                if name and name == rfilename:
                    break

                if with_print and rfilename not in changed:
                    click.echo(f"{rfilename} only exists locally\n")
                changed[rfilename] = "local"
    if clean_up:
        shutil.rmtree(target_dir)

    return changed


def color_diff(diff: Iterable[str]) -> Generator[str, Any, None]:
    for line in diff:
        if line.startswith("+"):
            yield Fore.GREEN + line + Fore.RESET
        elif line.startswith("-"):
            yield Fore.RED + line + Fore.RESET
        elif line.startswith("^"):
            yield Fore.BLUE + line + Fore.RESET
        else:
            yield line
