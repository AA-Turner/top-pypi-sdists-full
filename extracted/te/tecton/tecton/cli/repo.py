import io
import os
import sys
import tarfile
from pathlib import Path

import click
import requests

from tecton import tecton_context
from tecton._internals import metadata_service
from tecton.cli import cli_utils
from tecton.cli import printer
from tecton.cli import repo_config
from tecton.cli.command import TectonCommand
from tecton_core import http
from tecton_core import repo_file_handler
from tecton_proto.metadataservice import metadata_service__client_pb2 as metadata_service_pb2


def init_feature_repo() -> None:
    if Path().resolve() == Path.home():
        printer.safe_print("You cannot set feature repository root to the home directory", file=sys.stderr)
        sys.exit(1)

    # If .tecton exists in a parent or child directory, error out.
    repo_root = repo_file_handler._maybe_get_repo_root()
    if repo_root not in [Path().resolve(), None]:
        printer.safe_print(".tecton already exists in a parent directory:", repo_root)
        sys.exit(1)

    child_dir_matches = list(Path().rglob("*/.tecton"))
    if len(child_dir_matches) > 0:
        dirs_str = "\n\t".join((str(c.parent.resolve()) for c in child_dir_matches))
        printer.safe_print(f".tecton already exists in child directories:\n\t{dirs_str}")
        sys.exit(1)

    dot_tecton = Path(".tecton")
    if not dot_tecton.exists():
        dot_tecton.touch()

        default_repo_config = Path("repo.yaml")
        if default_repo_config.exists():
            printer.safe_print(f"Found a repo config at {default_repo_config}. Skipping creating a new repo config.")
        else:
            repo_config.create_starter_repo_config(config_path=default_repo_config)

        msgs = [
            f"Local feature repository root set to {Path().resolve()}",
            "",
            "💡 We recommend tracking these files in git:",
            f"     {dot_tecton.resolve()}",
            f"     {default_repo_config.resolve()}",
            "",
            "💡 Run `tecton apply` to apply the feature repository to the Tecton cluster.",
        ]
        printer.safe_print("\n".join(msgs), file=sys.stderr)
    else:
        printer.safe_print("Feature repository is already set to", Path().resolve(), file=sys.stderr)


@click.command(uses_workspace=True, cls=TectonCommand)
@click.argument("commit_id", required=False)
@click.option("--yes", "-y", is_flag=True, default=False, help="Skip all confirmation prompts.")
def restore(commit_id, yes):
    """Restore local Tecton Workspace state to a previous version.

    The commit to restore can either be passed as COMMIT_ID, or the latest commit for the currently selected workspace will be used.

    Also restores the repo config used for the apply to the default repo config path at REPO_ROOT/repo.yaml.
    """
    # Get the repo download URL from the metadata service.
    request = metadata_service_pb2.GetRestoreInfoRequest(workspace=tecton_context.get_current_workspace())
    if commit_id:
        request.commit_id = commit_id
    response = metadata_service.instance().GetRestoreInfo(request)

    # Download the repo.
    url = response.signed_url_for_repo_download
    commit_id = response.commit_id
    sdk_version = response.sdk_version
    # TODO: always print this message once enough customers are on new sdk versions
    sdk_version_msg = f"applied by SDK version {sdk_version}" if sdk_version else ""
    printer.safe_print(f"Restoring from commit {commit_id} {sdk_version_msg}")
    try:
        tar_response = http.session().get(url)
        tar_response.raise_for_status()
    except requests.RequestException as e:
        raise SystemExit(e)

    # Find the repo root or initialize a default repo if not in a repo.
    root = repo_file_handler._maybe_get_repo_root()
    if not root:
        init_feature_repo()
        root = Path().resolve()
    repo_file_handler.ensure_prepare_repo()

    # Get user confirmation for files that may be modified (all eligible python files or the default repo config path).
    existing_files = repo_file_handler.repo_files()

    default_repo_path = repo_config.get_default_repo_config_path()
    if default_repo_path.exists():
        existing_files.append(default_repo_path)

    if len(existing_files) > 0:
        if not yes:
            for f in existing_files:
                printer.safe_print(f)
            cli_utils.confirm_or_exit("This operation may delete or modify the above files. Ok?")
        for f in existing_files:
            os.remove(f)

    # Extract the feature repo.
    with tarfile.open(fileobj=io.BytesIO(tar_response.content), mode="r|gz") as tar:
        for entry in tar:
            if os.path.isabs(entry.name) or ".." in entry.name:
                msg = "Illegal tar archive entry"
                raise ValueError(msg)
            elif os.path.exists(root / Path(entry.name)):
                msg = f"tecton restore would overwrite an unexpected file: {entry.name}"
                raise ValueError(msg)
            tar.extract(entry, path=root)
    printer.safe_print("Success")


@click.command(requires_auth=False, cls=TectonCommand, is_main_command=True)
def init() -> None:
    """Initialize feature repo."""
    init_feature_repo()
