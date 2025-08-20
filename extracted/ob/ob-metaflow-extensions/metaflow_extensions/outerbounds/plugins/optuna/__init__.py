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


def get_deployment_db_access_endpoint(name: str):
    from ..apps.core.perimeters import PerimeterExtractor
    from ..apps.core.capsule import CapsuleApi

    perimeter, cap_url = PerimeterExtractor.during_metaflow_execution()
    deployment = CapsuleApi(cap_url, perimeter).get_by_name(name)
    if not deployment:
        raise Exception(f"No app deployment found with name `{name}`")

    if (
        "status" in deployment
        and "accessInfo" in deployment["status"]
        and "extraAccessUrls" in deployment["status"]["accessInfo"]
    ):
        for extra_url in deployment["status"]["accessInfo"]["extraAccessUrls"]:
            if extra_url["name"] == "in_cluster_db_access":
                db_url = extra_url["url"].replace("http://", "")
                return db_url

    raise Exception(f"No db access endpoint found for deployment `{name}`")


def get_db_url(app_name: str):
    """
    Example usage:
        >>> from metaflow.plugins.optuna import get_db_url
        >>> s = optuna.create_study(..., storage=get_db_url("optuna-dashboard"))
    """
    mf_token = auth()["x-api-key"]
    app_url = get_deployment_db_access_endpoint(app_name)
    return f"postgresql://userspace_default:{mf_token}@{app_url}/userspace_default?sslmode=disable"
