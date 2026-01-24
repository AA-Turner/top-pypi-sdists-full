import click

import coiled
from coiled.filestore import FilestoreManager

from .cluster.utils import find_cluster
from .utils import CONTEXT_SETTINGS


@click.command(
    context_settings=CONTEXT_SETTINGS,
)
@click.argument("cluster", default="", required=False)
@click.option(
    "--workspace",
    default=None,
    help="Coiled workspace (uses default workspace if not specified).",
)
@click.option(
    "--filestore",
    default=None,
    help="Name of filestore (optional).",
)
@click.option(
    "--filter",
    "name_includes",
    default=None,
    help="Filter on file paths and/or names to download (optional).",
)
@click.option("--into", default=".")
def download(cluster, workspace, filestore, name_includes, into):
    if filestore:
        filestores = FilestoreManager.get_filestore(name=filestore) or []
        if not filestores:
            print(f"{filestore} filestore not found")

        for fs in filestores:
            coiled.filestore.download_from_filestore_with_ui(
                fs=fs,
                into=into,
                name_includes=name_includes,
            )

    else:
        with coiled.Cloud(workspace=workspace) as cloud:
            cluster_info = find_cluster(cloud, cluster)
            cluster_id = cluster_info["id"]
            attachments = FilestoreManager.get_cluster_attachments(cluster_id)
        if not attachments:
            print(f"No filestore found for {cluster_info['name']} ({cluster_info['id']})")

        # TODO (possible enhancement) if there are multiple output filestores, let user pick which to download
        for attachment in attachments:
            if attachment["output"]:
                coiled.filestore.download_from_filestore_with_ui(
                    fs=attachment["filestore"],
                    into=into,
                    name_includes=name_includes,
                )


@click.command(
    context_settings=CONTEXT_SETTINGS,
)
@click.argument("cluster", default="", required=False)
@click.option(
    "--workspace",
    default=None,
    help="Coiled workspace (uses default workspace if not specified).",
)
@click.option(
    "--filestore",
    default=None,
    help="Name of filestore (optional).",
)
@click.option(
    "--filter",
    "name_includes",
    default=None,
    help="Filter on file paths and/or names to download (optional).",
)
def list_files(cluster, workspace, filestore, name_includes):
    if filestore:
        filestores = FilestoreManager.get_filestore(name=filestore) or []
        if not filestores:
            print(f"{filestore} filestore not found")

        for fs in filestores:
            coiled.filestore.list_files_ui(
                fs=fs,
                name_includes=name_includes,
            )

    else:
        with coiled.Cloud(workspace=workspace) as cloud:
            cluster_info = find_cluster(cloud, cluster)
            cluster_id = cluster_info["id"]
            attachments = FilestoreManager.get_cluster_attachments(cluster_id)
        if not attachments:
            print(f"No filestore found for {cluster_info['name']} ({cluster_info['id']})")

        # TODO (possible enhancement) if there are multiple output filestores, let user pick which to download
        for attachment in attachments:
            if attachment["output"]:
                coiled.filestore.list_files_ui(
                    fs=attachment["filestore"],
                    name_includes=name_includes,
                )


@click.group(name="file", context_settings=CONTEXT_SETTINGS)
def file_group(): ...


file_group.add_command(download)
file_group.add_command(list_files, "list")
