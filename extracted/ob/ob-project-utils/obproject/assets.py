import json
import re
import requests
from typing import Dict, List, Optional, Any


def _make_request(
    base_url: str,
    service_headers: Dict[str, str],
    method: str,
    endpoint: str,
    data: Optional[Dict] = None,
) -> Dict[str, Any]:
    """Make HTTP request to API."""
    url = f"{base_url.rstrip('/')}{endpoint}"

    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    headers.update(service_headers)

    response = requests.request(method, url, headers=headers, json=data)
    try:
        response.raise_for_status()
        return response.json()
    except:
        print("Asset error", response.text)
        raise


def register_asset(
    base_url: str,
    service_headers: Dict[str, str],
    *,
    perimeter: str,
    project: str,
    branch: str,
    name: str,
    kind: str,
    entity_ref: Dict[str, str],
    description: str,
    data_asset_kind: Optional[str] = None,
    model_asset_kind: Optional[str] = None,
    blobs: Optional[List[str]] = None,
    annotations: Optional[Dict[str, str]] = None,
    tags: Optional[dict] = None,
) -> Dict[str, Any]:
    """Register a new asset. You can call this multiple times.
    The asset will be created if it does not exist, otherwise it will be updated.
    """
    endpoint = (
        f"/v1/perimeters/{perimeter}/projects/{project}/branches/{branch}/{kind}/{name}"
    )

    assert (
        data_asset_kind is not None or model_asset_kind is not None
    ), "Either data_asset_kind or model_asset_kind must be provided"
    assert kind in ["data", "models"], "kind must be either 'data' or 'models'"

    payload = {"entity_ref": entity_ref}
    if description:
        payload["description"] = description
    if data_asset_kind:
        payload["data_asset_kind"] = data_asset_kind
    if model_asset_kind:
        payload["model_asset_kind"] = model_asset_kind
    # NOTE: we check "is not None" explicitly to allow for empty lists and dicts
    if tags is not None:
        payload["tags"] = [{"key": k, "value": v} for k, v in tags.items()]
    if blobs is not None:
        payload["blobs"] = blobs
    if annotations is not None:
        payload["annotations"] = annotations

    return _make_request(base_url, service_headers, "PATCH", endpoint, payload)


def get_data_asset(
    base_url: str,
    service_headers: Dict[str, str],
    *,
    perimeter: str,
    project: str,
    branch: str,
    asset: str,
    instance: str,
) -> Dict[str, Any]:
    """
    Get a data asset instance. This is a 'peek' API that is it does not track usage.
    """
    endpoint = f"/v1/perimeters/{perimeter}/projects/{project}/branches/{branch}/data/{asset}/instances/{instance}"
    return _make_request(base_url, service_headers, "GET", endpoint)


def consume_data_asset(
    base_url: str,
    service_headers: Dict[str, str],
    *,
    perimeter: str,
    project: str,
    branch: str,
    asset: str,
    entity_ref: Dict[str, str],
    instance: str,
) -> Dict[str, Any]:
    """Consume a data asset instance. Same as get_data_asset but tracks usage."""
    endpoint = f"/v1/perimeters/{perimeter}/projects/{project}/branches/{branch}/data/{asset}/instances/{instance}"
    return _make_request(
        base_url, service_headers, "PUT", endpoint, {"entity_ref": entity_ref}
    )


def get_model_asset(
    base_url: str,
    service_headers: Dict[str, str],
    *,
    perimeter: str,
    project: str,
    branch: str,
    asset: str,
    instance: str,
) -> Dict[str, Any]:
    """Get a model asset instance. This is a 'peek' API that is it does not track usage."""
    endpoint = f"/v1/perimeters/{perimeter}/projects/{project}/branches/{branch}/models/{asset}/instances/{instance}"
    return _make_request(base_url, service_headers, "GET", endpoint)


def consume_model_asset(
    base_url: str,
    service_headers: Dict[str, str],
    *,
    perimeter: str,
    project: str,
    branch: str,
    asset: str,
    entity_ref: Dict[str, str],
    instance: str,
) -> Dict[str, Any]:
    """Consume a model asset instance. Same as get_model_asset but tracks usage."""
    endpoint = f"/v1/perimeters/{perimeter}/projects/{project}/branches/{branch}/models/{asset}/instances/{instance}"
    return _make_request(
        base_url, service_headers, "PUT", endpoint, {"entity_ref": entity_ref}
    )


def list_model_assets(
    base_url: str,
    service_headers: Dict[str, str],
    *,
    perimeter: str,
    project: str,
    branch: str,
) -> Dict[str, Any]:
    """List model assets with the latest instance."""
    endpoint = f"/v1/perimeters/{perimeter}/projects/{project}/branches/{branch}/models"
    return _make_request(base_url, service_headers, "GET", endpoint)


def list_data_assets(
    base_url: str,
    service_headers: Dict[str, str],
    *,
    perimeter: str,
    project: str,
    branch: str,
) -> Dict[str, Any]:
    """List data assets with the latest instance."""
    endpoint = f"/v1/perimeters/{perimeter}/projects/{project}/branches/{branch}/data"
    return _make_request(base_url, service_headers, "GET", endpoint)


# Helper functions
def entity_ref(kind: str, entity_id: str) -> Dict[str, str]:
    """Create entity reference."""
    return {"entity_kind": kind, "entity_id": entity_id}


def task_ref(flow: str, run_id: str, step: str, task_id: str) -> Dict[str, str]:
    """Create task entity reference."""
    return entity_ref("task", f"{flow}/{run_id}/{step}/{task_id}")


def user_ref(user_id: str) -> Dict[str, str]:
    """Create user entity reference."""
    return entity_ref("user", user_id)


class Asset:
    def __init__(self, project=None, branch=None, entity_ref=None, read_only=False):
        from metaflow_extensions.outerbounds.remote_config import init_config
        import metaflow.metaflow_config
        from metaflow import current
        import os

        if project is None:
            project = current.project_name
        if branch is None:
            branch = re.sub(r"[^a-z0-9_-]", "-", current.branch_name.lower())
        if entity_ref is None:
            entity_ref = {"entity_kind": "task", "entity_id": current.pathspec}

        self.project = project
        self.branch = branch
        self.entity_ref = entity_ref
        self.read_only = read_only

        self.service_headers = metaflow.metaflow_config.SERVICE_HEADERS
        conf = init_config()

        if "OBP_PERIMETER" in conf:
            self.perimeter = conf["OBP_PERIMETER"]
        else:
            # if the perimeter is not in metaflow config, try to get it from the environment
            self.perimeter = os.environ.get("OBP_PERIMETER", "")
        if "OBP_API_SERVER" in conf:
            server = conf["OBP_API_SERVER"]
            self.base_url = f"https://{server}"
        else:
            self.base_url = os.path.dirname(os.environ.get("OBP_INTEGRATIONS_URL"))

    @property
    def meta(self):
        return {
            "project": self.project,
            "branch": self.branch,
            "entity_reg": self.entity_ref,
        }

    def _register(
        self,
        kind,
        name,
        description=None,
        annotations=None,
        blobs=None,
        tags=None,
        data_asset_kind=None,
        model_asset_kind=None,
    ):
        if not self.read_only:
            register_asset(
                self.base_url,
                self.service_headers,
                perimeter=self.perimeter,
                project=self.project,
                branch=self.branch,
                name=name,
                kind=kind,
                entity_ref=self.entity_ref,
                description=description,
                data_asset_kind=data_asset_kind,
                model_asset_kind=model_asset_kind,
                annotations=annotations,
                blobs=blobs,
                tags=tags,
            )

    def register_model_asset(
        self, name, description=None, kind=None, blobs=None, annotations=None, tags=None
    ):
        self._register(
            "models",
            name,
            description=description,
            blobs=blobs,
            tags=tags,
            annotations=annotations,
            model_asset_kind=kind,
        )

    def register_data_asset(
        self, name, description=None, kind=None, blobs=None, annotations=None, tags=None
    ):
        self._register(
            "data",
            name,
            description=description,
            blobs=blobs,
            tags=tags,
            annotations=annotations,
            data_asset_kind=kind,
        )

    def list_data_assets(self):
        return list_data_assets(
            self.base_url,
            self.service_headers,
            perimeter=self.perimeter,
            project=self.project,
            branch=self.branch,
        )

    def list_model_assets(self):
        return list_model_assets(
            self.base_url,
            self.service_headers,
            perimeter=self.perimeter,
            project=self.project,
            branch=self.branch,
        )

    def consume_data_asset(self, name):
        common = {
            "perimeter": self.perimeter,
            "project": self.project,
            "branch": self.branch,
            "asset": name,
            "instance": "latest",
        }
        args = (self.base_url, self.service_headers)
        if self.read_only:
            return get_data_asset(*args, **common)
        else:
            return consume_data_asset(*args, **common, entity_ref=self.entity_ref)

    def consume_model_asset(self, name):
        common = {
            "perimeter": self.perimeter,
            "project": self.project,
            "branch": self.branch,
            "asset": name,
            "instance": "latest",
        }
        args = (self.base_url, self.service_headers)
        if self.read_only:
            return get_model_asset(*args, **common)
        else:
            return consume_model_asset(*args, **common, entity_ref=self.entity_ref)
