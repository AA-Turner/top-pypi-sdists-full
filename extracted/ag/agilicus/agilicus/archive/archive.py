"""Archive every object that belongs to an organisation.

This is the SDK equivalent of ``kubectl get all -A -o json``: given an
organisation id it walks the organisation tree (the org itself plus every
sub-organisation, recursively) and writes every object it can find to disk as
JSON, one file per object, grouped under ``<directory>/org-<org-id>/<type>/``
and named after the object's globally unique id (guid). Prefixing the
per-organisation directory with ``org-`` keeps a plain ``ls`` readable and
keeps each organisation self-contained.

The set of object types is described by :class:`Collector` entries. A
collector is intentionally small: it names the API accessor and the list
method to call for one organisation. A handful of types cannot be listed at
organisation scope (multi-factor enrolments are per user, connector services
are per connector, ...); those are handled by the fan-out collectors below,
which expand a parent collection (users, connectors, applications, issuer
policies) into per-child list calls.

Every collector is best-effort. A failure to read one type (for example
because the caller is not permitted, or the endpoint does not exist on this
deployment) is recorded in the manifest and the archive continues.
"""

import datetime
import hashlib
import json
import os
import re
import threading
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Iterable, List, Optional

from agilicus import context
from agilicus.agilicus_api import ApiException
from agilicus.input_helpers import get_org_from_input_or_ctx, strip_none
from agilicus.output import output_if_console

DEFAULT_PAGE_SIZE = 500
UNSAFE_FILENAME = re.compile(r"[^A-Za-z0-9._-]+")


# ---------------------------------------------------------------------------
# Model / response helpers
# ---------------------------------------------------------------------------
def _to_dict(obj: Any) -> Any:
    """Convert a generated API model (or collection thereof) to plain data."""
    if obj is None:
        return None
    if isinstance(obj, dict):
        return {k: _to_dict(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_to_dict(item) for item in obj]
    to_dict = getattr(obj, "to_dict", None)
    if callable(to_dict):
        try:
            return _to_dict(to_dict())
        except Exception:
            pass
    if hasattr(obj, "__dict__"):
        return {
            k: _to_dict(v)
            for k, v in vars(obj).items()
            if not k.startswith("_") and k != "local_vars_configuration"
        }
    return obj


def _get(obj: Any, name: str) -> Any:
    """Fetch *name* from a model or dict without assuming either shape."""
    getter = getattr(obj, "get", None)
    if callable(getter):
        try:
            return getter(name)
        except Exception:
            pass
    return getattr(obj, name, None)


def _first_list(response: Any) -> List[Any]:
    """Return the first list-valued field of a generated list response."""
    if response is None:
        return []
    if isinstance(response, (list, tuple)):
        return list(response)
    attribute_map = getattr(response, "attribute_map", None)
    if attribute_map is None and isinstance(response, dict):
        attribute_map = list(response.keys())
    if attribute_map:
        for name in attribute_map:
            value = _get(response, name)
            if isinstance(value, (list, tuple)):
                return list(value)
    return []


def _supports(method: Any, name: str) -> bool:
    params = getattr(method, "params_map", None) or {}
    return name in (params.get("all") or [])


def list_all(method: Callable, **params: Any) -> List[Any]:
    """Call a generated list endpoint and return every page of results.

    The generated client exposes three pagination styles. Newer endpoints get
    an ``auto_paging_iter`` (injected by the SDK patches); older ones page with
    ``page_at_id`` or ``previous_email``. We pick whichever the endpoint
    supports, and fall back to a single call when it supports none.
    """
    params = strip_none(params)

    if (
        _supports(method, "limit")
        and _supports(method, "page_on")
        and hasattr(method, "auto_paging_iter")
    ):
        try:
            return list(method.auto_paging_iter(page_size=100, **params).all())
        except NotImplementedError:
            pass
        except ApiException:
            pass
        except TypeError:
            # A malformed/partial response body can defeat the generated
            # model's required fields; fall back to a raw call below.
            pass

    call_params = dict(params)
    if _supports(method, "limit"):
        call_params["limit"] = DEFAULT_PAGE_SIZE
    response = _call_endpoint(method, call_params)
    items = _first_list(response)

    if _supports(method, "limit"):
        page_field = _resolve_page_field(method, response)
        if page_field is not None:
            items = _paginate_by(method, response, items, params, *page_field)
    return items


def _call_endpoint(method: Callable, params: Dict[str, Any]) -> Any:
    """Call a list endpoint, tolerating a response the model cannot parse.

    Some generated response models declare fields as required (for example
    ``ListRoles.limit``) even though the server may omit them. That makes the
    generated client raise a ``TypeError`` while building the model. In that
    case we re-issue the request with ``_preload_content=False`` and decode the
    JSON ourselves, so the archive still captures the data.
    """
    try:
        return method(**params)
    except TypeError as exc:
        message = str(exc)
        if (
            "_from_openapi_data" not in message
            and "required positional argument" not in message
        ):
            raise
        raw = method(_preload_content=False, **params)
        return _decode_raw(raw)


def _decode_raw(raw: Any) -> Any:
    data = getattr(raw, "data", None)
    if data is None and hasattr(raw, "read"):
        data = raw.read()
    if isinstance(data, (bytes, bytearray)):
        data = data.decode("utf-8", errors="replace")
    if not data:
        return {}
    try:
        return json.loads(data)
    except (TypeError, ValueError):
        return {}


def _response_fields(response: Any) -> set:
    attribute_map = getattr(response, "attribute_map", None)
    if attribute_map:
        return set(attribute_map)
    if isinstance(response, dict):
        return set(response.keys())
    return set()


# Request pagination parameter -> the response field that carries the next
# token. Not every endpoint names them the same way, and the token can be a
# generated model (for example ``NextPageEmail``) rather than a plain string.
_PAGE_REQUEST_KEYS = (
    "page_at_id",
    "previous_email",
    "page_at_name",
    "page_at_created_date",
    "page_at_version",
    "previous_created_time",
)
_PAGE_RESPONSE_KEY = {
    "previous_email": "next_page_email",
    "previous_created_time": "page_at_created_time",
}


def _resolve_page_field(method: Callable, response: Any) -> Optional[tuple]:
    """Find the (request param, response field) pair this endpoint pages with."""
    supported = set(getattr(method, "params_map", {}).get("all", []))
    fields = _response_fields(response)
    for request_key in _PAGE_REQUEST_KEYS:
        if request_key not in supported:
            continue
        response_key = _PAGE_RESPONSE_KEY.get(request_key, request_key)
        if response_key in fields:
            return request_key, response_key
    return None


def _page_token(value: Any) -> Optional[str]:
    """A hashable, comparable representation of a pagination token.

    Generated primitive models (``NextPageEmail``, ...) define ``__eq__``
    without ``__hash__`` and so cannot be used in a set directly.
    """
    if value is None:
        return None
    if isinstance(value, (str, int, float, bool)):
        return str(value)
    to_str = getattr(value, "to_str", None)
    if callable(to_str):
        try:
            return str(to_str())
        except Exception:
            pass
    inner = getattr(value, "value", None)
    if isinstance(inner, (str, int, float, bool)):
        return str(inner)
    return repr(value)


def _page_value(value: Any) -> Any:
    """The value to send back for the next page.

    A generated wrapper model cannot always be passed back to the endpoint
    (``previous_email`` is typed ``Email`` but the response carries a
    ``NextPageEmail``). The server accepts the primitive value, so unwrap it.
    """
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    to_str = getattr(value, "to_str", None)
    if callable(to_str):
        try:
            return str(to_str())
        except Exception:
            pass
    inner = getattr(value, "value", None)
    if isinstance(inner, (str, int, float, bool)):
        return inner
    return value


def _paginate_by(
    method: Callable,
    response: Any,
    items: List[Any],
    params: Dict[str, Any],
    request_key: str,
    response_key: Optional[str] = None,
) -> List[Any]:
    response_key = response_key or request_key
    collected = list(items)
    seen = set()
    while items:
        page = _get(response, response_key)
        token = _page_token(page)
        if token is None or token == "" or token in seen:
            break
        seen.add(token)
        call_params = dict(params)
        call_params[request_key] = _page_value(page)
        call_params["limit"] = DEFAULT_PAGE_SIZE
        response = _call_endpoint(method, call_params)
        items = _first_list(response)
        collected.extend(items)
    return collected


_ID_PATHS = (
    ("id",),
    ("metadata", "id"),
    ("spec", "id"),
    ("guid",),
    ("metadata", "name"),
    ("spec", "name"),
    ("name",),
    ("role",),
    ("spec", "resource_role_name"),
    ("user_id",),
    ("spec", "user_id"),
)


def _dig(obj: Any, path: Iterable[str]) -> Any:
    current = obj
    for part in path:
        current = _get(current, part)
        if current is None:
            return None
    return current


def object_id(obj: Any) -> Optional[str]:
    """Best-effort extraction of an object's guid."""
    for path in _ID_PATHS:
        value = _dig(obj, path)
        if isinstance(value, str) and value:
            return value
    return None


def _sanitize(name: str) -> str:
    cleaned = UNSAFE_FILENAME.sub("_", name).strip("._")
    return cleaned[:200] or "object"


def _fallback_name(obj: Any) -> str:
    payload = json.dumps(obj, sort_keys=True, default=str)
    digest = hashlib.sha1(payload.encode("utf-8")).hexdigest()
    return "sha1-{}".format(digest[:40])


def object_filename(obj: Any) -> str:
    """The on-disk base name for an object: its guid, else a content hash."""
    identifier = object_id(obj)
    if identifier:
        return _sanitize(identifier)
    return _fallback_name(obj)


# ---------------------------------------------------------------------------
# Collectors
# ---------------------------------------------------------------------------
@dataclass
class Collector:
    """A listable, organisation-scoped object type."""

    name: str
    api: str
    method: str
    org_param: str = "org_id"

    def fetch(self, apiclient: Any, org_id: str) -> List[Any]:
        target = getattr(getattr(apiclient, self.api), self.method)
        params: Dict[str, Any] = {}
        if self.org_param:
            params[self.org_param] = org_id
        return list_all(target, **params)


# Object types that can be listed directly for an organisation.
ORG_COLLECTORS: List[Collector] = [
    Collector("users", "user_api", "list_users"),
    Collector("groups", "groups_api", "list_groups"),
    Collector("service-accounts", "user_api", "list_service_accounts"),
    Collector("user-metadata", "user_api", "list_user_metadata"),
    Collector("user-roles", "user_api", "list_org_user_roles"),
    Collector(
        "org-upstream-user-identities",
        "user_api",
        "list_org_upstream_user_identity",
    ),
    Collector("applications", "application_api", "list_applications"),
    Collector("application-services", "app_services_api", "list_application_services"),
    Collector("desktop-resources", "app_services_api", "list_desktop_resources"),
    Collector("ssh-resources", "app_services_api", "list_ssh_resources"),
    Collector("file-share-services", "app_services_api", "list_file_share_services"),
    Collector("printers", "app_services_api", "list_printers"),
    Collector("service-forwarders", "app_services_api", "list_service_forwarders"),
    Collector("database-resources", "app_services_api", "list_database_resources"),
    Collector("external-networks", "app_services_api", "list_external_networks"),
    Collector("resources", "resources_api", "list_resources"),
    Collector("resource-permissions", "permissions_api", "list_resource_permissions"),
    Collector("resource-roles", "permissions_api", "list_resource_roles"),
    Collector("issuers", "issuers_api", "list_issuers"),
    Collector("issuer-clients", "issuers_api", "list_clients"),
    Collector("issuer-policies", "issuers_api", "list_policies"),
    Collector("issuer-upstreams", "issuers_api", "list_issuer_upstreams"),
    Collector("firewall-rules", "rules_api", "list_standalone_rules"),
    Collector("firewall-rulesets", "rules_api", "list_standalone_rulesets"),
    Collector(
        "firewall-ruleset-bundles", "rules_api", "list_standalone_ruleset_bundles"
    ),
    Collector("firewall-rule-trees", "rules_api", "list_standalone_rule_trees"),
    Collector("firewall-rule-policies", "rules_api", "list_standalone_rule_policies"),
    Collector("combined-application-rules", "application_api", "list_combined_rules"),
    Collector(
        "combined-resource-rules", "resources_api", "list_combined_resource_rules"
    ),
    Collector("connectors", "connectors_api", "list_connector"),
    Collector("agent-connectors", "connectors_api", "list_agent_connector"),
    Collector("ipsec-connectors", "connectors_api", "list_ipsec_connector"),
    Collector("connector-proxies", "connectors_api", "list_proxies"),
    Collector("api-keys", "tokens_api", "list_api_keys"),
    Collector("trusted-certs", "trusted_certs_api", "list_trusted_certs"),
    Collector("trusted-cert-bundles", "trusted_certs_api", "list_bundles"),
    Collector("launchers", "launchers_api", "list_launchers"),
    Collector("files", "files_api", "list_files"),
    Collector("file-templates", "files_api", "list_file_templates"),
    Collector("hosts", "hosts_api", "list_hosts"),
    Collector("host-bundles", "hosts_api", "list_host_bundles"),
    Collector("host-labels", "hosts_api", "list_host_labels"),
    Collector("certificates", "certificates_api", "list_certs"),
    Collector("certificate-trackers", "certificates_api", "list_cert_trackers"),
    Collector("labels", "labels_api", "list_object_labels"),
    Collector(
        "policy-template-instances",
        "policy_templates_api",
        "list_policy_template_instances",
    ),
    Collector("deployments", "deployments_api", "list_deployments"),
    Collector("deployment-templates", "deployments_api", "list_deployment_templates"),
    Collector("deployment-instances", "deployments_api", "list_deployment_instances"),
    Collector("email-domains", "org_api", "list_email_domains"),
]


@dataclass
class FanoutCollector:
    """A type listed per child of another collection.

    ``parent`` names one of the organisation collectors above; ``child_param``
    is the argument the list method needs (for example ``connector_id``);
    ``child_field`` is how to read that value out of the parent object.
    """

    name: str
    api: str
    method: str
    parent: str
    child_param: str
    child_field: str
    org_param: Optional[str] = "org_id"


FANOUT_COLLECTORS: List[FanoutCollector] = [
    # Application firewall rules and roles, per application.
    FanoutCollector(
        "application-roles",
        "application_api",
        "list_roles",
        parent="applications",
        child_param="app_id",
        child_field="id",
    ),
    FanoutCollector(
        "application-rules",
        "application_api",
        "list_rules",
        parent="applications",
        child_param="app_id",
        child_field="id",
    ),
    # Authentication policy rules, per authentication policy.
    FanoutCollector(
        "issuer-policy-rules",
        "issuers_api",
        "list_policy_rules",
        parent="issuer-policies",
        child_param="policy_id",
        child_field="id",
    ),
    # Connector sub-resources, per connector.
    FanoutCollector(
        "connector-instances",
        "connectors_api",
        "list_instances",
        parent="connectors",
        child_param="connector_id",
        child_field="metadata.id",
    ),
    FanoutCollector(
        "connector-services",
        "connectors_api",
        "list_services",
        parent="connectors",
        child_param="connector_id",
        child_field="metadata.id",
    ),
    FanoutCollector(
        "connector-transfers",
        "connectors_api",
        "list_transfers",
        parent="connectors",
        child_param="connector_id",
        child_field="metadata.id",
    ),
    # Multi-factor enrolments, per user.
    FanoutCollector(
        "totp-enrollments",
        "challenges_api",
        "list_totp_enrollment",
        parent="users",
        child_param="user_id",
        child_field="id",
        org_param=None,
    ),
    FanoutCollector(
        "webauthn-enrollments",
        "challenges_api",
        "list_webauthn_enrollments",
        parent="users",
        child_param="user_id",
        child_field="id",
        org_param=None,
    ),
]


# Organisation-level singletons, fetched as a single object per org.
ORG_SINGLETONS = (
    ("system-options", "org_api", "get_system_options"),
    ("org-features", "org_api", "get_org_features"),
    ("org-status", "org_api", "get_org_status"),
    ("org-capabilities", "org_api", "get_inherent_capabilities"),
)

MFA_TYPES = {"totp-enrollments", "webauthn-enrollments"}


# ---------------------------------------------------------------------------
# Writer
# ---------------------------------------------------------------------------
class ArchiveWriter:
    """Writes objects as ``<directory>/org-<org-id>/<type>/<guid>.json``.

    Each organisation gets its own top-level directory (prefixed with ``org-``
    so a plain ``ls`` reads clearly). That keeps a sub-organisation's objects
    self-contained while still grouping them by type.
    """

    ORG_PREFIX = "org-"

    def __init__(self, directory: str):
        self.directory = os.path.abspath(directory)

    def org_directory(self, org_id: str) -> str:
        return os.path.join(self.directory, self.ORG_PREFIX + _sanitize(org_id))

    def _path(self, org_id: str, type_name: str, base_name: str) -> str:
        type_dir = os.path.join(self.org_directory(org_id), type_name)
        path = os.path.join(type_dir, base_name + ".json")
        suffix = 1
        while os.path.exists(path):
            path = os.path.join(type_dir, "{}-{}.json".format(base_name, suffix))
            suffix += 1
        return path

    def write(self, org_id: str, type_name: str, obj: Any) -> str:
        data = _to_dict(obj)
        return self.write_named(org_id, type_name, object_filename(data), data)

    def write_named(self, org_id: str, type_name: str, base_name: str, obj: Any) -> str:
        data = _to_dict(obj)
        path = self._path(org_id, type_name, _sanitize(base_name))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2, default=str)
        return path

    def write_document(self, relative_path: str, document: Any) -> str:
        path = os.path.join(self.directory, relative_path)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(
                _to_dict(document),
                handle,
                ensure_ascii=False,
                indent=2,
                default=str,
            )
        return path


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------
@dataclass
class ArchiveResult:
    directory: str
    org_id: str
    counts: Dict[str, int] = field(default_factory=dict)
    org_counts: Dict[str, Dict[str, int]] = field(default_factory=dict)
    errors: List[Dict[str, Any]] = field(default_factory=list)
    organisations: List[Dict[str, Any]] = field(default_factory=list)
    visited: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        organisations = []
        for org in self.organisations:
            entry = dict(org)
            entry["directory"] = ArchiveWriter.ORG_PREFIX + _sanitize(
                str(org.get("id", ""))
            )
            entry["counts"] = self.org_counts.get(str(org.get("id", "")), {})
            organisations.append(entry)
        return {
            "org_id": self.org_id,
            "directory": self.directory,
            "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "organisations": organisations,
            "organisations_visited": list(self.visited),
            "counts": self.counts,
            "errors": self.errors,
            "total": sum(self.counts.values()),
        }


def _child_value(obj: Any, field_path: str) -> Optional[str]:
    return _dig(obj, field_path.split("."))


def archive_org(
    ctx,
    org_id: str,
    directory: str,
    recursive: bool = True,
    workers: int = 8,
    include_types: Optional[Iterable[str]] = None,
    exclude_types: Optional[Iterable[str]] = None,
    include_mfa: bool = True,
) -> ArchiveResult:
    """Archive *org_id* and (optionally) its sub-organisations into *directory*."""
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)
    if not org_id:
        raise ValueError(
            "an organisation id is required (pass it as an argument or --org-id)"
        )

    include = set(include_types) if include_types else None
    exclude = set(exclude_types or ())

    # A fan-out type needs its parent collection (users, connectors, ...) even
    # when the caller only asked for the child.
    if include is not None:
        for fanout in FANOUT_COLLECTORS:
            if fanout.name in include:
                include.add(fanout.parent)

    def wanted(name: str) -> bool:
        if include is not None and name not in include:
            return False
        return name not in exclude

    collectors = [c for c in ORG_COLLECTORS if wanted(c.name)]
    fanouts = [c for c in FANOUT_COLLECTORS if wanted(c.name)]
    if not include_mfa:
        fanouts = [c for c in fanouts if c.name not in MFA_TYPES]
    singletons = [entry for entry in ORG_SINGLETONS if wanted(entry[0])]

    apiclient = context.get_apiclient(ctx)
    writer = ArchiveWriter(directory)
    result = ArchiveResult(directory=writer.directory, org_id=org_id)
    lock = threading.Lock()

    pending = [org_id]
    visited = set()
    while pending:
        current = pending.pop(0)
        if current in visited:
            continue
        visited.add(current)
        output_if_console(ctx, "Archiving organisation {}".format(current))

        org_record = _collect_org_record(apiclient, writer, current, result, lock)
        if org_record is not None:
            with lock:
                result.organisations.append(org_record)
        with lock:
            result.visited.append(current)

        _collect_singletons(apiclient, writer, singletons, current, result, lock)

        fanout_parents = {c.parent for c in fanouts}
        fanout_sources: Dict[str, List[Any]] = {}
        for collector in collectors:
            objects = _run_collector(
                ctx, apiclient, writer, collector, current, result, lock
            )
            if collector.name in fanout_parents:
                fanout_sources[collector.name] = objects

        for fanout in fanouts:
            parents = fanout_sources.get(fanout.parent, [])
            _run_fanout(
                ctx,
                apiclient,
                writer,
                fanout,
                current,
                parents,
                workers,
                result,
                lock,
            )

        if recursive:
            pending.extend(_sub_org_ids(apiclient, current, result, lock))

    writer.write_document("manifest.json", result.to_dict())
    return result


def _collect_org_record(
    apiclient, writer: ArchiveWriter, org_id, result, lock
) -> Optional[Dict[str, Any]]:
    try:
        org = apiclient.org_api.get_org(org_id=org_id)
    except Exception as exc:  # noqa: BLE001 - best-effort archive
        _record_error(result, "organisations", org_id, exc)
        return None
    data = _to_dict(org)
    with lock:
        writer.write(org_id, "organisations", data)
        _bump(result, org_id, "organisations")
    return {
        "id": org_id,
        "organisation": _get(data, "organisation"),
        "parent_id": _get(data, "parent_id"),
        "root_org_id": _get(data, "root_org_id"),
    }


def _collect_singletons(apiclient, writer, singletons, org_id, result, lock):
    for name, api, method in singletons:
        try:
            obj = getattr(getattr(apiclient, api), method)(org_id=org_id)
        except Exception as exc:  # noqa: BLE001
            _record_error(result, name, org_id, exc)
            continue
        if obj is None:
            continue
        with lock:
            writer.write_named(org_id, name, org_id, obj)
            _bump(result, org_id, name)


def _run_collector(
    ctx, apiclient, writer, collector: Collector, org_id, result, lock
) -> List[Any]:
    try:
        objects = collector.fetch(apiclient, org_id)
    except Exception as exc:  # noqa: BLE001
        _record_error(result, collector.name, org_id, exc)
        return []
    with lock:
        for obj in objects:
            writer.write(org_id, collector.name, obj)
        _bump(result, org_id, collector.name, len(objects))
    output_if_console(ctx, "  {}: {}".format(collector.name, len(objects)))
    return [_to_dict(o) for o in objects]


def _run_fanout(
    ctx,
    apiclient,
    writer,
    fanout: FanoutCollector,
    org_id,
    parents: List[Any],
    workers: int,
    result,
    lock,
):
    targets = [
        value
        for value in (_child_value(parent, fanout.child_field) for parent in parents)
        if value
    ]
    if not targets:
        return

    method = getattr(getattr(apiclient, fanout.api), fanout.method)

    def fetch(target):
        params: Dict[str, Any] = {fanout.child_param: target}
        if fanout.org_param:
            params[fanout.org_param] = org_id
        return list_all(method, **params)

    written = 0
    errors = []

    def store(objects):
        nonlocal written
        with lock:
            for obj in objects:
                writer.write(org_id, fanout.name, obj)
            written += len(objects)

    if workers and workers > 1 and len(targets) > 1:
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures = {pool.submit(fetch, target): target for target in targets}
            for future, target in futures.items():
                try:
                    store(future.result())
                except Exception as exc:  # noqa: BLE001
                    errors.append((target, exc))
    else:
        for target in targets:
            try:
                store(fetch(target))
            except Exception as exc:  # noqa: BLE001
                errors.append((target, exc))

    with lock:
        _bump(result, org_id, fanout.name, written)
    for target, exc in errors:
        _record_error(result, "{}[{}]".format(fanout.name, target), org_id, exc)
    output_if_console(ctx, "  {}: {}".format(fanout.name, written))


def _sub_org_ids(apiclient, org_id, result, lock) -> List[str]:
    try:
        sub_orgs = list_all(apiclient.org_api.list_sub_orgs, org_id=org_id)
    except Exception as exc:  # noqa: BLE001
        _record_error(result, "sub-organisations", org_id, exc)
        return []
    ids = []
    for sub in sub_orgs:
        sub_id = object_id(_to_dict(sub))
        if sub_id:
            ids.append(sub_id)
    return ids


def _bump(result: ArchiveResult, org_id: str, name: str, count: int = 1) -> None:
    result.counts[name] = result.counts.get(name, 0) + count
    per_org = result.org_counts.setdefault(str(org_id), {})
    per_org[name] = per_org.get(name, 0) + count


def _describe_error(exc: Exception) -> str:
    """A short, single-line description of a failure.

    Generated ``ApiException`` strings embed the full HTTP headers and body,
    which makes the manifest (and console output) unreadable. Prefer the
    status and reason.
    """
    status = getattr(exc, "status", None)
    reason = getattr(exc, "reason", None)
    if status is not None or reason:
        parts = [str(part) for part in (status, reason) if part]
        text = " ".join(parts)
    else:
        text = str(exc)
    text = " ".join(text.split())
    if len(text) > 300:
        text = text[:300] + "..."
    return "{}: {}".format(type(exc).__name__, text)


def _record_error(result: ArchiveResult, name: str, org_id: str, exc: Exception) -> None:
    result.errors.append(
        {
            "type": name,
            "org_id": org_id,
            "status": getattr(exc, "status", None),
            "error": _describe_error(exc),
        }
    )
