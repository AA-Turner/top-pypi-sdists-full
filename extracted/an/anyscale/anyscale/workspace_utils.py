import os

from click import ClickException
import yaml

from anyscale.project_utils import ANYSCALE_PROJECT_FILE, find_project_root


def write_workspace_id_to_disk(workspace_id: str, directory: str) -> None:
    with open(os.path.join(directory, ANYSCALE_PROJECT_FILE), "w") as f:
        f.write("{}".format(f"workspace_id: {workspace_id}"))


def get_workspace_root_or_throw() -> str:
    root_dir = find_project_root(os.getcwd())
    if not root_dir:
        raise ClickException(
            "No directory with .anyscale.yaml file found. Please make sure you are running the command in a cloned workspace directory."
        )
    return os.path.join(root_dir, "")


def load_workspace_id_or_throw() -> str:
    # First check if there is a .anyscale.yaml.
    root_dir = get_workspace_root_or_throw()

    anyscale_yaml = os.path.join(root_dir, ANYSCALE_PROJECT_FILE)
    if os.path.exists(anyscale_yaml):
        with open(anyscale_yaml) as f:
            config = yaml.safe_load(f)
            return config["workspace_id"]
    else:
        raise ClickException(
            "No .anyscale.yaml file found. Please make sure you are running the command in a cloned workspace directory."
        )
