import json
import re
import requests
from datetime import datetime, timezone
from typing import Dict, Iterator, List, Optional, Any, NamedTuple


class InvalidAssetInstanceError(Exception):
    """Raised when an asset instance response cannot be parsed."""
    pass


class EntityRef(NamedTuple):
    entity_kind: str
    entity_id: str


class AssetInstance(NamedTuple):
    """A specific version of an asset."""
    id: str
    created_at: datetime
    created_by: EntityRef
    annotations: Dict[str, str]
    tags: Dict[str, str]
    blobs: List[str]
    kind: str
    asset_kind: str


_RFC3339_RE = re.compile(
    r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})(?:\.(\d+))?(Z|[+-]\d{2}:\d{2})"
)


def _parse_rfc3339(s: str) -> datetime:
    """Parse an RFC 3339 timestamp as emitted by the Go backend.

    Go marshals time.Time with nanosecond precision; old versions
    of Python can't handle this.

    With Python >= 3.11 this entire function can be replaced with
    datetime.fromisoformat(s) which properly handles RFC 3339 timestamps.
    """
    m = _RFC3339_RE.fullmatch(s)
    if not m:
        raise ValueError(f"Unexpected timestamp format: {s}")
    base, frac, tz = m.group(1), m.group(2), m.group(3)
    offset = "+00:00" if tz == "Z" else tz
    iso = f"{base}.{frac[:6]}{offset}" if frac else f"{base}{offset}"
    return datetime.fromisoformat(iso)


def _parse_instance(raw: Dict[str, Any]) -> AssetInstance:
    """Convert a raw API response dict into a typed AssetInstance.

    Raises InvalidAssetInstanceError if the instance data is invalid.
    """
    try:
        instance_id = raw["id"]
        asset_info = raw["asset"]
        kind = asset_info["kind"]
        created_at = _parse_rfc3339(raw["created_at"])
    except (KeyError, ValueError) as e:
        raise InvalidAssetInstanceError(f"bad instance data: {e}") from e

    created_by_raw = raw.get("created_by", {})
    created_by = EntityRef(
        entity_kind=created_by_raw.get("entity_kind", ""),
        entity_id=created_by_raw.get("entity_id", ""),
    )
    props = raw.get("data_properties") or raw.get("model_properties") or {}
    tags_list = raw.get("tags") or []
    tags = {t["key"]: t["value"] for t in tags_list}

    return AssetInstance(
        id=instance_id,
        created_at=created_at,
        created_by=created_by,
        annotations=props.get("annotations") or {},
        tags=tags,
        blobs=props.get("blobs") or [],
        kind=kind,
        asset_kind=props.get("data_kind") or props.get("model_kind") or "",
    )


def _sanitize_branch_name(branch: str) -> str:
    """
    Sanitize branch name for asset API compatibility.

    The asset API only accepts lowercase letters, numbers, hyphens, and underscores.
    Metaflow branch names may contain @ and . characters (e.g., user.alice@company.com).

    Args:
        branch: Raw Metaflow branch name

    Returns:
        Sanitized branch name safe for asset API
    """
    # Replace @ with _at_ for readability
    sanitized = branch.replace("@", "_at_")
    # Replace hyphens, slashes, and any other invalid characters with underscores.
    # This matches the branch normalization in deploy_obproject.py.
    sanitized = re.sub(r"[^a-z0-9_]", "_", sanitized.lower())
    # Collapse multiple underscores
    sanitized = re.sub(r"_+", "_", sanitized)
    # Remove leading/trailing underscores
    sanitized = sanitized.strip("_")
    return sanitized


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
        payload["tags"] = [{"key": k, "value": str(v)} for k, v in tags.items()]
    if blobs is not None:
        payload["blobs"] = blobs
    if annotations is not None:
        # Convert all annotation values to strings for API compatibility
        payload["annotations"] = {k: str(v) for k, v in annotations.items()}

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
    Get a data asset instance without tracking consumption.

    Args:
        instance: "latest" for the newest version, a specific instance ID,
            or an alias reference like "@staging".
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
    """Consume a data asset instance, recording the consumption in the lineage graph.

    Args:
        instance: "latest" for the newest version, a specific instance ID,
            or an alias reference like "@staging".
    """
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
    """Get a model asset instance without tracking consumption.

    Args:
        instance: "latest" for the newest version, a specific instance ID,
            or an alias reference like "@staging".
    """
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
    """Consume a model asset instance, recording the consumption in the lineage graph.

    Args:
        instance: "latest" for the newest version, a specific instance ID,
            or an alias reference like "@staging".
    """
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


def get_data_asset_summary(
    base_url: str,
    service_headers: Dict[str, str],
    *,
    perimeter: str,
    project: str,
    branch: str,
    asset: str,
) -> Dict[str, Any]:
    """
    Get a data asset summary including recent instances and lineage.

    Returns an AssetSummary with recent_instances,
    recently_produced_by, and recently_consumed_by.
    """
    endpoint = f"/v1/perimeters/{perimeter}/projects/{project}/branches/{branch}/data/{asset}"
    return _make_request(base_url, service_headers, "GET", endpoint)


def get_model_asset_summary(
    base_url: str,
    service_headers: Dict[str, str],
    *,
    perimeter: str,
    project: str,
    branch: str,
    asset: str,
) -> Dict[str, Any]:
    """
    Get a model asset summary including recent instances and lineage.

    Returns an AssetSummary with recent_instances,
    recently_produced_by, and recently_consumed_by.
    """
    endpoint = f"/v1/perimeters/{perimeter}/projects/{project}/branches/{branch}/models/{asset}"
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
            branch = current.branch_name
        # Always sanitize branch name for API compatibility
        branch = _sanitize_branch_name(branch)
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
            integrations_url = os.environ.get("OBP_INTEGRATIONS_URL")
            if integrations_url:
                self.base_url = os.path.dirname(integrations_url)
            else:
                raise RuntimeError(
                    "Cannot determine asset API server.\n"
                    f"  OBP_API_SERVER in metaflow config: {conf.get('OBP_API_SERVER', '<not set>')}\n"
                    f"  OBP_INTEGRATIONS_URL env var: {integrations_url!r}\n"
                    f"  OBP_PERIMETER in metaflow config: {conf.get('OBP_PERIMETER', '<not set>')}\n"
                    f"  Metaflow config keys: {list(conf.keys())}"
                )

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

    def list_data_assets(self, tags=None):
        """
        List data assets, optionally filtered by tags.

        Args:
            tags: Dict of tag key-value pairs to filter by (client-side filtering)

        Returns:
            List of data asset metadata
        """
        assets = list_data_assets(
            self.base_url,
            self.service_headers,
            perimeter=self.perimeter,
            project=self.project,
            branch=self.branch,
        )
        if tags:
            # Client-side filtering by tags
            filtered = []
            for asset in assets.get("data", []):
                asset_tags = {t["key"]: t["value"] for t in asset.get("tags", [])}
                if all(asset_tags.get(k) == v for k, v in tags.items()):
                    filtered.append(asset)
            return {"data": filtered}
        return assets

    def list_model_assets(self, tags=None):
        """
        List model assets, optionally filtered by tags.

        Args:
            tags: Dict of tag key-value pairs to filter by (client-side filtering)

        Returns:
            List of model asset metadata
        """
        assets = list_model_assets(
            self.base_url,
            self.service_headers,
            perimeter=self.perimeter,
            project=self.project,
            branch=self.branch,
        )
        if tags:
            # Client-side filtering by tags
            filtered = []
            for asset in assets.get("models", []):
                asset_tags = {t["key"]: t["value"] for t in asset.get("tags", [])}
                if all(asset_tags.get(k) == v for k, v in tags.items()):
                    filtered.append(asset)
            return {"models": filtered}
        return assets

    def _iter_asset_instances(self, kind, name) -> Iterator[AssetInstance]:
        """
        Yield AssetInstance objects for the given asset. Currently returns
        up to 50 instances from a single backend call. The generator shape
        allows adding transparent pagination here later without changing
        the public API.
        """
        fn = get_data_asset_summary if kind == "data" else get_model_asset_summary
        summary = fn(
            self.base_url,
            self.service_headers,
            perimeter=self.perimeter,
            project=self.project,
            branch=self.branch,
            asset=name,
        )
        for raw in summary.get("recent_instances", []):
            try:
                yield _parse_instance(raw)
            except InvalidAssetInstanceError:
                # Should never happen with a healthy backend; skip bad entries
                continue

    def list_data_asset_instances(self, name) -> Iterator[AssetInstance]:
        """
        Iterate over recent instances of a data asset, newest first.

        Args:
            name: Asset name/id

        Returns:
            Iterator of AssetInstance named tuples.
        """
        return self._iter_asset_instances("data", name)

    def list_model_asset_instances(self, name) -> Iterator[AssetInstance]:
        """
        Iterate over recent instances of a model asset, newest first.

        Args:
            name: Asset name/id

        Returns:
            Iterator of AssetInstance named tuples.
        """
        return self._iter_asset_instances("models", name)

    def peek_data_asset(self, name, instance="latest"):
        """
        Get a data asset instance without tracking consumption.

        Args:
            name: Asset name/id
            instance: Instance to retrieve. Use "latest" (default) for the most
                recent version, a specific instance ID (as returned by
                list_data_asset_instances), or an alias like "@staging".
        """
        return get_data_asset(
            self.base_url, self.service_headers,
            perimeter=self.perimeter, project=self.project,
            branch=self.branch, asset=name, instance=instance,
        )

    def peek_model_asset(self, name, instance="latest"):
        """
        Get a model asset instance without tracking consumption.

        Args:
            name: Asset name/id
            instance: Instance to retrieve. Use "latest" (default) for the most
                recent version, a specific instance ID (as returned by
                list_model_asset_instances), or an alias like "@staging".
        """
        return get_model_asset(
            self.base_url, self.service_headers,
            perimeter=self.perimeter, project=self.project,
            branch=self.branch, asset=name, instance=instance,
        )

    def consume_data_asset(self, name, instance="latest"):
        """
        Consume a data asset instance, recording the consumption in the lineage graph.

        Args:
            name: Asset name/id
            instance: Instance to retrieve. Use "latest" (default) for the most
                recent version, a specific instance ID (as returned by
                list_data_asset_instances), or an alias like "@staging".
        """
        common = {
            "perimeter": self.perimeter,
            "project": self.project,
            "branch": self.branch,
            "asset": name,
            "instance": instance,
        }
        args = (self.base_url, self.service_headers)
        if self.read_only:
            return get_data_asset(*args, **common)
        else:
            return consume_data_asset(*args, **common, entity_ref=self.entity_ref)

    def consume_model_asset(self, name, instance="latest"):
        """
        Consume a model asset instance, recording the consumption in the lineage graph.

        Args:
            name: Asset name/id
            instance: Instance to retrieve. Use "latest" (default) for the most
                recent version, a specific instance ID (as returned by
                list_model_asset_instances), or an alias like "@staging".
        """
        common = {
            "perimeter": self.perimeter,
            "project": self.project,
            "branch": self.branch,
            "asset": name,
            "instance": instance,
        }
        args = (self.base_url, self.service_headers)
        if self.read_only:
            return get_model_asset(*args, **common)
        else:
            return consume_model_asset(*args, **common, entity_ref=self.entity_ref)

    def _set_alias(self, branch, name, kind, instance_id, alias):
        """Set an alias on a specific instance."""
        base = (f"/v1/perimeters/{self.perimeter}/projects/{self.project}"
                f"/branches")
        _make_request(
            self.base_url, self.service_headers, "PUT",
            f"{base}/{branch}/{kind}/{name}/aliases/{alias}",
            {
                "instance_id": instance_id,
                "entity_ref": dict(self.entity_ref),
            },
        )

    def _promote_single(self, source_branch, target_branch, name, kind,
                        instance="latest", with_aliases=False, alias=None):
        """
        Internal: promote one asset instance from source to target branch.
        Both branches must be pre-sanitized.
        """
        # Read from source
        if kind == "data":
            src = get_data_asset(
                self.base_url, self.service_headers,
                perimeter=self.perimeter, project=self.project,
                branch=source_branch, asset=name, instance=instance,
            )
            props = src.get("data_properties", {})
            asset_kind = props.get("data_kind")
        else:
            src = get_model_asset(
                self.base_url, self.service_headers,
                perimeter=self.perimeter, project=self.project,
                branch=source_branch, asset=name, instance=instance,
            )
            props = src.get("model_properties", {})
            asset_kind = props.get("model_kind")

        annotations = dict(props.get("annotations") or {})
        blobs = props.get("blobs") or []
        tags_list = src.get("tags") or []
        tags = {t["key"]: t["value"] for t in tags_list}
        description = src.get("asset", {}).get("description", "")
        source_id = src.get("id", "")

        # Add promotion lineage
        annotations["promoted_from_branch"] = source_branch
        annotations["promoted_from_instance"] = source_id

        result = register_asset(
            self.base_url,
            self.service_headers,
            perimeter=self.perimeter,
            project=self.project,
            branch=target_branch,
            name=name,
            kind=kind,
            entity_ref=self.entity_ref,
            description=description,
            data_asset_kind=asset_kind if kind == "data" else None,
            model_asset_kind=asset_kind if kind == "models" else None,
            blobs=blobs,
            annotations=annotations,
            tags=tags if tags else None,
        )

        # Read back the new instance ID if we need to set aliases
        new_instance_id = None
        if with_aliases or alias:
            # register_asset doesn't return the new instance ID,
            # so read it back from the target branch
            if kind == "data":
                new = get_data_asset(
                    self.base_url, self.service_headers,
                    perimeter=self.perimeter, project=self.project,
                    branch=target_branch, asset=name, instance="latest",
                )
            else:
                new = get_model_asset(
                    self.base_url, self.service_headers,
                    perimeter=self.perimeter, project=self.project,
                    branch=target_branch, asset=name, instance="latest",
                )
            new_instance_id = new.get("id", "")

        if with_aliases:
            self._copy_aliases(source_branch, target_branch, name, kind,
                               new_instance_id)

        if alias and new_instance_id:
            self._set_alias(target_branch, name, kind, new_instance_id, alias)

        return result

    def _copy_aliases(self, source_branch, target_branch, name, kind,
                      target_instance_id):
        """Copy all aliases from source branch to target, pointing to the promoted instance."""
        base = (f"/v1/perimeters/{self.perimeter}/projects/{self.project}"
                f"/branches")
        try:
            aliases_resp = _make_request(
                self.base_url, self.service_headers, "GET",
                f"{base}/{source_branch}/{kind}/{name}/aliases",
            )
        except Exception:
            return

        for alias in aliases_resp.get("aliases", []):
            try:
                _make_request(
                    self.base_url, self.service_headers, "PUT",
                    f"{base}/{target_branch}/{kind}/{name}/aliases/{alias['name']}",
                    {
                        "instance_id": target_instance_id,
                        "entity_ref": dict(self.entity_ref),
                    },
                )
            except Exception:
                pass  # best-effort


DEFAULT_PROMOTION_ALIASES = ["candidate", "validated", "production"]


def promote_assets(project, source, target, kinds=None, asset=None,
                   instance="latest", with_aliases=True, alias="candidate"):
    """
    Promote assets from one branch to another.

    Reads asset instances from `source` branch and re-registers them on
    `target` branch with the same blob references, annotations, and tags.
    The underlying data (S3 objects, Metaflow artifacts) is NOT copied --
    only the metadata pointer is created on the target branch.

    Args:
        project: Project name
        source: Source branch name (will be sanitized)
        target: Target branch name (will be sanitized)
        kinds: List of asset types to promote, e.g. ["data", "models"].
               Defaults to both.
        asset: If set, promote only this specific asset name.
               Otherwise promotes all assets on the source branch.
        instance: Which instance to promote ("latest", instance ID,
                  or "@alias"). Defaults to "latest".
        with_aliases: If True, copy aliases from the source branch that
                  point to the promoted instance. Default False.
        alias: Alias to set on the promoted instance on the target branch.
               Defaults to "candidate". Must be one of the allowed promotion
               aliases (default: candidate, validated, production). Set to
               None to skip alias creation. Configure allowed aliases in
               obproject.toml under [promotion] aliases.

    Returns:
        Dict with "promoted" (list of dicts) and "errors" (list of dicts)

    Example::

        from obproject.assets import promote_assets

        # Promote with @candidate alias (default)
        result = promote_assets('my_project', source='feature-v2', target='main')

        # Promote with @validated alias after quality gates pass
        result = promote_assets('my_project', source='main', target='main',
                                asset='classifier', instance='@candidate',
                                alias='validated')

        # Promote to @production after approval
        result = promote_assets('my_project', source='main', target='main',
                                asset='classifier', instance='@validated',
                                alias='production')
    """
    source = _sanitize_branch_name(source)
    target = _sanitize_branch_name(target)
    if kinds is None:
        kinds = ["data", "models"]

    # Validate alias against allowed promotion aliases
    allowed_aliases = DEFAULT_PROMOTION_ALIASES
    try:
        import os
        toml_path = os.path.join(os.getcwd(), "obproject.toml")
        if os.path.exists(toml_path):
            try:
                import tomllib as toml
            except ImportError:
                import toml
            with open(toml_path, "rb") as f:
                cfg = toml.load(f) if hasattr(toml, 'load') else toml.loads(f.read().decode())
            configured = cfg.get("promotion", {}).get("aliases")
            if configured:
                allowed_aliases = configured
    except Exception:
        pass

    if alias is not None and alias not in allowed_aliases:
        raise ValueError(
            f"Alias '{alias}' is not in the allowed promotion aliases: {allowed_aliases}. "
            f"Configure [promotion] aliases in obproject.toml to customize."
        )

    entity_ref = {"entity_kind": "task", "entity_id": "obproject/promote"}
    client = Asset(project=project, branch=target, entity_ref=entity_ref)

    promoted = []
    errors = []

    if asset:
        # Promote a single named asset — try each requested kind
        for kind in kinds:
            try:
                client._promote_single(source, target, asset, kind, instance,
                                       with_aliases=with_aliases, alias=alias)
                promoted.append({"kind": kind, "name": asset, "alias": alias})
            except Exception as e:
                errors.append({"kind": kind, "name": asset, "error": str(e)})
        return {"promoted": promoted, "errors": errors}

    # Promote all assets on the source branch
    for kind in kinds:
        try:
            if kind == "data":
                result = list_data_assets(
                    client.base_url, client.service_headers,
                    perimeter=client.perimeter, project=project,
                    branch=source,
                )
            else:
                result = list_model_assets(
                    client.base_url, client.service_headers,
                    perimeter=client.perimeter, project=project,
                    branch=source,
                )
        except Exception as e:
            errors.append({"kind": kind, "error": str(e)})
            continue

        assets = result.get("items", [])
        for entry in assets:
            asset_info = entry.get("asset", entry)
            asset_name = asset_info.get("name") or asset_info.get("id")
            if not asset_name:
                continue
            try:
                client._promote_single(source, target, asset_name, kind, instance,
                                       with_aliases=with_aliases, alias=alias)
                promoted.append({"kind": kind, "name": asset_name, "alias": alias})
            except Exception as e:
                errors.append({"kind": kind, "name": asset_name, "error": str(e)})

    if not promoted and not errors:
        import warnings
        warnings.warn(
            f"No assets found on source branch '{source}'. "
            f"Was teardown-branch already run? "
            f"Promotion must happen before teardown."
        )

    return {"promoted": promoted, "errors": errors}
