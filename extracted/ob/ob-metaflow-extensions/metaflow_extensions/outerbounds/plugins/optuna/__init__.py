import os
import json

__mf_promote_submodules__ = ["plugins.optuna"]


def auth():
    from metaflow.metaflow_config_funcs import init_config

    conf = init_config()
    if conf:
        headers = {"x-api-key": conf["METAFLOW_SERVICE_AUTH_KEY"]}
    else:
        headers = json.loads(os.environ["METAFLOW_SERVICE_HEADERS"])
    return headers


def get_deployment_db_access_endpoint(
    name: str, project: str = None, branch: str = None
):
    from ..apps.core.deployer import AppDeployer

    apps = AppDeployer.list_deployments(
        name=name,
        project=project,
        branch=branch,
    )
    if not apps:
        raise Exception(f"No app deployment found with name `{name}`")

    deployment_info = apps[0].info()

    if (
        "status" in deployment_info
        and "accessInfo" in deployment_info["status"]
        and "extraAccessUrls" in deployment_info["status"]["accessInfo"]
    ):
        for extra_url in deployment_info["status"]["accessInfo"]["extraAccessUrls"]:
            if extra_url["name"] == "in_cluster_db_access":
                db_url = extra_url["url"].replace("http://", "")
                return db_url

    raise Exception(f"No db access endpoint found for deployment `{name}`")


def get_db_url(app_name: str, project: str = None, branch: str = None):
    """
    Example usage:
        >>> from metaflow.plugins.optuna import get_db_url
        >>> s = optuna.create_study(..., storage=get_db_url("optuna-dashboard"))
    """
    mf_token = auth()["x-api-key"]
    app_url = get_deployment_db_access_endpoint(
        app_name, project=project, branch=branch
    )
    return f"postgresql://userspace_default:{mf_token}@{app_url}/userspace_default?sslmode=disable"
