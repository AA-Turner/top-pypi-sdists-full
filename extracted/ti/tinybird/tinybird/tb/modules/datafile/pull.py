from pathlib import Path
from typing import Any, Optional

import click

from tinybird.tb.client import AuthNoTokenException, TinyB
from tinybird.tb.modules.datafile.format_datasource import format_datasource
from tinybird.tb.modules.datafile.format_pipe import format_pipe
from tinybird.tb.modules.feedback_manager import FeedbackManager


def folder_pull(
    client: TinyB,
    folder: str,
    force: bool,
    only_vendored: bool,
    verbose: bool = True,
    progress_bar: bool = False,
    fmt: bool = False,
) -> list[str]:
    def get_file_folder(extension: str, resource_type: Optional[str]):
        if extension == "datasource":
            return "datasources"
        if extension == "connection":
            return "connections"
        if resource_type == "endpoint":
            return "endpoints"
        if resource_type == "sink":
            return "sinks"
        if resource_type == "copy":
            return "copies"
        if resource_type == "materialized":
            return "materializations"
        if extension == "pipe":
            return "pipes"
        return None

    def write_files(
        resources: list[dict[str, Any]],
        extension: str,
        get_resource_function: str,
        progress_bar: bool = False,
        fmt: bool = False,
    ) -> list[Path]:
        def write_resource(k: dict[str, Any]) -> Optional[Path]:
            name = f"{k['name']}.{extension}"
            try:
                resource = getattr(client, get_resource_function)(k["name"])
                resource_to_write = resource

                if fmt:
                    if extension == "datasource":
                        resource_to_write = format_datasource(name, content=resource)
                    elif extension == "pipe":
                        resource_to_write = format_pipe(name, content=resource)

                dest_folder = folder
                if "." in k["name"]:
                    dest_folder = Path(folder) / "vendor" / k["name"].split(".", 1)[0]
                    name = f"{k['name'].split('.', 1)[1]}.{extension}"

                file_folder = get_file_folder(extension, k.get("type"))
                f = Path(dest_folder) / file_folder if file_folder is not None else Path(dest_folder)

                if not f.exists():
                    f.mkdir(parents=True)

                f = f / name

                if verbose:
                    click.echo(FeedbackManager.info_writing_resource(resource=f))
                if not f.exists() or force:
                    with open(f, "w") as fd:
                        if resource_to_write:
                            fd.write(resource_to_write)
                            return f
                elif verbose:
                    click.echo(FeedbackManager.info_skip_already_exists())
                return None
            except Exception as e:
                raise click.ClickException(FeedbackManager.error_exception(error=e))

        if progress_bar:
            written_files = []
            with click.progressbar(resources, label=f"Pulling {extension}s") as resources:  # type: ignore
                for k in resources:
                    written_file = write_resource(k)
                    if written_file:
                        written_files.append(written_file)
        else:
            written_files = list(filter(None, (write_resource(k) for k in resources)))

        return written_files

    try:
        datasources = client.datasources()
        pipes = client.pipes()
        connections = client.connections()

        if only_vendored:
            written_files = write_files(
                resources=[ds for ds in datasources if "shared_from" in ds],
                extension="datasource",
                get_resource_function="datasource_file",
                progress_bar=progress_bar,
                fmt=fmt,
            )
        else:
            written_files = []
            written_files.extend(
                write_files(
                    resources=datasources,
                    extension="datasource",
                    get_resource_function="datasource_file",
                    progress_bar=progress_bar,
                    fmt=fmt,
                )
            )
            written_files.extend(
                write_files(
                    resources=pipes,
                    extension="pipe",
                    get_resource_function="pipe_file",
                    progress_bar=progress_bar,
                    fmt=fmt,
                )
            )
            written_files.extend(
                write_files(
                    resources=connections,
                    extension="connection",
                    get_resource_function="connection_file",
                    progress_bar=progress_bar,
                    fmt=fmt,
                )
            )
        return [str(wf) for wf in written_files]

    except AuthNoTokenException:
        raise
    except Exception as e:
        raise click.ClickException(FeedbackManager.error_pull(error=str(e)))
