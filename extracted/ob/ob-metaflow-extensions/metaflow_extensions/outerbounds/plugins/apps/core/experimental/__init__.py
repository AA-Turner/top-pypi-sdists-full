import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..app_config import AppConfig

DEFAULT_BRANCH = "test"


# Account for project / branch and the capsule input.
def capsule_input_overrides(app_config: "AppConfig", capsule_input: dict):
    project = app_config.get_state("project", None)
    # Update the project/branch related configurations.
    if project is not None:
        branch = app_config.get_state("branch", DEFAULT_BRANCH)
        capsule_input["tags"].extend(
            [dict(key="project", value=project), dict(key="branch", value=branch)]
        )

    persistence = app_config.get_state("persistence", None)
    if persistence is not None and persistence != "none":
        capsule_input["persistence"] = persistence

    capsule_input["generateStaticUrl"] = app_config.get_state(
        "generate_static_url", False
    )

    model_asset_conf = app_config.get_state("models", None)
    data_asset_conf = app_config.get_state("data", None)
    code_info = _code_info(app_config)
    # todo:fix me
    _objects_key = "associatedObjects"
    if model_asset_conf or data_asset_conf or code_info:
        capsule_input[_objects_key] = {}

        if model_asset_conf:
            capsule_input[_objects_key]["models"] = [
                {"assetId": x["asset_id"], "assetInstanceId": x["asset_instance_id"]}
                for x in model_asset_conf
            ]
        if data_asset_conf:
            capsule_input[_objects_key]["data"] = [
                {"assetId": x["asset_id"], "assetInstanceId": x["asset_instance_id"]}
                for x in data_asset_conf
            ]
        if code_info:
            capsule_input[_objects_key]["code"] = code_info

    return capsule_input


def _code_info(app_config: "AppConfig"):
    from metaflow.metaflow_git import get_repository_info

    try:
        from metaflow.metaflow_git import _call_git  # type: ignore
    except ImportError:
        # Fallback if _call_git is not available
        def _call_git(args, path=None):
            return "", 1, True

    package_dirs = app_config.get_state("packaging_directories")
    if package_dirs is None:
        return None
    for directory in package_dirs:
        repo_info = get_repository_info(directory)
        if len(repo_info) == 0:
            continue
        git_log_info, returncode, failed = _call_git(
            ["log", "-1", "--pretty=%B"],
            path=directory,
        )
        repo_url = repo_info["repo_url"]
        if isinstance(repo_url, str):
            _url = (
                repo_url if not repo_url.endswith(".git") else repo_url.rstrip(".git")
            )
        else:
            _url = str(repo_url)
        _code_info = {
            "commitId": repo_info["commit_sha"],
            "commitLink": os.path.join(_url, "commit", str(repo_info["commit_sha"])),
        }
        if not failed and returncode == 0 and isinstance(git_log_info, str):
            _code_info["commitMessage"] = git_log_info.strip()

        return _code_info

    return None
