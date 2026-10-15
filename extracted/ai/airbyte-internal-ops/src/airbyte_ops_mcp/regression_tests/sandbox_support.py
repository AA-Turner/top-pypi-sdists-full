# Copyright (c) 2026 Airbyte, Inc., all rights reserved.
"""Static check: can a SaaS Sandbox twin stand in for a connector's provider?

The first, cheap gate before a reproduction case is authored. It reads the
connector's `metadata.yaml` and declarative `manifest.yaml` and the sandbox's
packaged discovery data (`sandbox ... --offline`, no server), and answers
`supported`, `unsupported` or `unknown` with reasons:

1. **Provider match** -- the connector's `allowedHosts` against the sandbox
   providers' hosts.
2. **Operation coverage** -- every HTTP operation the requested streams and
   their parent streams call, the query parameters they send and their page
   size, against the twin catalog.
3. **Dataset coverage** -- optional `entity.field` needs named by the caller,
   against the twin's dataset entities and schemas.

A connector without a declarative manifest, or a stream whose requests cannot
be read from it, is `unknown` rather than guessed. Requests a custom component
makes on its own are invisible here; they are reported as warnings, and the
case lane's twin-gap gate is the authoritative check for them.
"""

from __future__ import annotations

import copy
import json
import re
import shutil
import subprocess
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Literal
from urllib.parse import SplitResult, urlsplit

import yaml
from airbyte_cdk.sources.declarative.parsers.manifest_component_transformer import (
    ManifestComponentTransformer,
)
from airbyte_cdk.sources.declarative.parsers.manifest_reference_resolver import (
    ManifestReferenceResolver,
)

from airbyte_ops_mcp.github_api import (
    get_file_contents_at_ref,
    resolve_default_github_token,
)

Support = Literal["supported", "unsupported", "unknown"]

DISCOVERY_TIMEOUT_SECONDS = 60
_PARAMETER_REFERENCE = re.compile(
    r"\{\{\s*parameters(?:\[\s*['\"](\w+)['\"]\s*\]|\.(\w+))\s*\}\}"
)
_TEMPLATE = re.compile(r"\{\{.*?\}\}")
_CONFIG_PLACEHOLDER = re.compile(r"\$\{[^}]*\}")


class SandboxDiscoveryError(RuntimeError):
    """The sandbox CLI's offline discovery could not be read."""


class SandboxDiscovery:
    """The sandbox's packaged discovery data, read with `--offline` commands."""

    def __init__(self, executable: str = "sandbox") -> None:
        resolved = shutil.which(executable)
        if resolved is None:
            raise SandboxDiscoveryError(f"`{executable}` CLI not found on PATH")
        self.executable = resolved

    def _run(self, *arguments: str) -> Any:
        command = [self.executable, *arguments, "--offline"]
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=DISCOVERY_TIMEOUT_SECONDS,
            )
        except (OSError, subprocess.SubprocessError) as exc:
            raise SandboxDiscoveryError(
                f"`sandbox {' '.join(arguments)}`: {exc}"
            ) from exc
        if result.returncode != 0:
            raise SandboxDiscoveryError(
                f"`sandbox {' '.join(arguments)} --offline` exited "
                f"{result.returncode}: {result.stderr.strip()[-300:]}"
            )
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            raise SandboxDiscoveryError(
                f"`sandbox {' '.join(arguments)} --offline` printed no JSON"
            ) from exc

    def _items(self, key: str, *arguments: str) -> list[dict[str, Any]]:
        payload = self._run(*arguments)
        items = payload.get(key) if isinstance(payload, dict) else None
        if not isinstance(items, list):
            raise SandboxDiscoveryError(
                f"`sandbox {' '.join(arguments)} --offline` has no {key!r} list"
            )
        return [item for item in items if isinstance(item, dict)]

    def providers(self) -> list[dict[str, Any]]:
        return self._items("providers", "providers")

    def operations(self, provider: str) -> list[dict[str, Any]]:
        return self._items("operations", "operations", provider)

    def entities(self, provider: str) -> list[str]:
        return [
            entity["name"]
            for entity in self._items("entities", "entities", provider)
            if "name" in entity
        ]

    def entity_fields(self, provider: str, entity: str) -> set[str]:
        """Field names a dataset can set on one entity (its `apply` input schema)."""
        document = self._run("schema", provider, entity)
        inputs = document.get("inputs", {}) if isinstance(document, dict) else {}
        schema = (inputs.get("apply") or {}).get("schema") or {}
        reference = schema.get("$ref", "")
        if isinstance(reference, str) and reference.startswith("#/$defs/"):
            schema = (schema.get("$defs") or {}).get(reference.split("/")[-1]) or {}
        return set((schema.get("properties") or {}).keys())


@dataclass
class OperationNeed:
    """One HTTP operation a stream (or its parent) makes, as the manifest declares it."""

    stream: str
    method: str
    host: str
    path: str
    parameters: list[str] = field(default_factory=list)
    page_size: int | None = None
    # A page size expression the check could not resolve, if any.
    unread_page_size: str | None = None
    twin_operation: str | None = None
    # The matched twin operation's maximum page size, if it declares one.
    page_size_limit: int | None = None
    problems: list[str] = field(default_factory=list)
    ambiguous: list[str] = field(default_factory=list)


@dataclass
class SupportReport:
    result: Support
    provider: str | None = None
    operations: list[OperationNeed] = field(default_factory=list)
    reasons: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def load_connector_files(
    connector_dir: Path,
) -> tuple[dict[str, Any], dict[str, Any] | None]:
    """A connector's metadata and its declarative manifest, if it has one."""
    metadata = yaml.safe_load((connector_dir / "metadata.yaml").read_text()) or {}
    manifest_path = connector_dir / "manifest.yaml"
    manifest = (
        yaml.safe_load(manifest_path.read_text()) if manifest_path.exists() else None
    )
    return metadata, manifest


def fetch_connector_files(
    connector_name: str, ref: str, token: str | None
) -> tuple[dict[str, Any], dict[str, Any] | None]:
    """The same files read from airbytehq/airbyte at `ref`, without a checkout."""
    base = f"airbyte-integrations/connectors/{connector_name}"
    metadata_text = get_file_contents_at_ref(
        "airbytehq", "airbyte", f"{base}/metadata.yaml", ref, token
    )
    if metadata_text is None:
        raise FileNotFoundError(f"{base}/metadata.yaml not found at {ref}")
    manifest_text = get_file_contents_at_ref(
        "airbytehq", "airbyte", f"{base}/manifest.yaml", ref, token
    )
    return (
        yaml.safe_load(metadata_text) or {},
        yaml.safe_load(manifest_text) if manifest_text is not None else None,
    )


def _allowed_hosts(metadata: Mapping[str, Any]) -> list[str]:
    data = metadata.get("data", metadata)
    hosts = ((data.get("allowedHosts") or {}).get("hosts")) or []
    return [str(host).lower() for host in hosts]


def _host_pattern(pattern: str) -> re.Pattern[str] | None:
    """A host pattern as a regex; `None` when it is a placeholder from config.

    `allowedHosts` uses `*.` wildcards and `${...}` labels filled from the
    connection config (`${subdomain}.zendesk.com`). A pattern that is nothing
    but a placeholder (`${api_url}`) could be any host.
    """
    if _CONFIG_PLACEHOLDER.fullmatch(pattern):
        return None
    regex = re.escape(pattern)
    regex = regex.replace(r"\*\.", r"(?:[^.]+\.)*")
    regex = _CONFIG_PLACEHOLDER.sub(
        "[^.]+", regex.replace(r"\$\{", "${").replace(r"\}", "}")
    )
    return re.compile(regex)


def _match_provider(
    allowed: Sequence[str], providers: Sequence[Mapping[str, Any]]
) -> dict[str, Any] | None:
    patterns = [
        compiled for compiled in map(_host_pattern, allowed) if compiled is not None
    ]
    for provider in providers:
        hosts = [str(host).lower() for host in provider.get("hosts", [])]
        if any(pattern.fullmatch(host) for pattern in patterns for host in hosts):
            return dict(provider)
    return None


def _resolve_manifest(manifest: Mapping[str, Any]) -> dict[str, Any]:
    resolved = ManifestReferenceResolver().preprocess_manifest(
        copy.deepcopy(dict(manifest))
    )
    return ManifestComponentTransformer().propagate_types_and_parameters(
        "", resolved, {}
    )


def _render_parameters(value: str, parameters: Mapping[str, Any]) -> str:
    def substitute(match: re.Match[str]) -> str:
        name = match.group(1) or match.group(2)
        return str(parameters.get(name, match.group(0)))

    return _PARAMETER_REFERENCE.sub(substitute, value)


def _request_option_names(component: Any, parameters: Mapping[str, Any]) -> list[str]:
    """Query-parameter names a component injects through `RequestOption`s.

    Authenticators are included: an API key injected as a query parameter is
    sent like any other.
    """
    names: list[str] = []
    if isinstance(component, dict):
        if (
            component.get("type") == "RequestOption"
            and component.get("inject_into") == "request_parameter"
            and isinstance(component.get("field_name"), str)
        ):
            names.append(_render_parameters(component["field_name"], parameters))
        for key, value in component.items():
            # Parent streams are walked as streams of their own.
            if key in ("stream", "$parameters"):
                continue
            names += _request_option_names(value, parameters)
    elif isinstance(component, list):
        for item in component:
            names += _request_option_names(item, parameters)
    return names


def _parent_streams(retriever: Mapping[str, Any]) -> list[dict[str, Any]]:
    routers = retriever.get("partition_router") or []
    routers = routers if isinstance(routers, list) else [routers]
    return [
        config["stream"]
        for router in routers
        if isinstance(router, dict)
        for config in router.get("parent_stream_configs", []) or []
        if isinstance(config, dict) and isinstance(config.get("stream"), dict)
    ]


def _request_making_components(retriever: Mapping[str, Any]) -> set[str]:
    """Custom classes that could issue requests of their own.

    Record extraction, transformations and state migrations never make
    requests, so only the retriever and what it uses to request are inspected.
    Parent streams are inspected as streams of their own.
    """
    found: set[str] = set()
    routers = retriever.get("partition_router")
    parts = [
        retriever,
        retriever.get("requester"),
        retriever.get("paginator"),
        *(routers if isinstance(routers, list) else [routers]),
    ]
    for part in parts:
        if isinstance(part, dict) and isinstance(part.get("class_name"), str):
            found.add(part["class_name"])
    return found


def _stream_needs(
    stream: Mapping[str, Any], report: SupportReport, seen: set[int]
) -> list[OperationNeed]:
    """The operations one stream and its parents make, recursively."""
    if id(stream) in seen:
        return []
    seen.add(id(stream))
    name = str(stream.get("name") or stream.get("$parameters", {}).get("name") or "?")
    if stream.get("type") == "StateDelegatingStream":
        # It reads with one of two complete streams depending on state.
        return [
            need
            for key in ("full_refresh_stream", "incremental_stream")
            if isinstance(stream.get(key), dict)
            for need in _stream_needs(stream[key], report, seen)
        ]
    retriever = stream.get("retriever") or {}
    for class_name in sorted(_request_making_components(retriever)):
        report.warnings.append(
            f"{name}: custom component {class_name} may make requests not visible "
            "here; the case lane's twin-gap gate covers them"
        )
    requester = retriever.get("requester") or {}
    parameters = {
        **(stream.get("$parameters") or {}),
        **(requester.get("$parameters") or {}),
    }
    url_base = requester.get("url_base")
    path = requester.get("path", "")
    if not isinstance(url_base, str) or not isinstance(path, str):
        _unknown(report, f"{name}: the manifest declares no url_base/path")
        return []
    url_base = _render_parameters(url_base, parameters)
    path = _render_parameters(path, parameters)
    split = _split_url(url_base)
    host = split.netloc.rsplit("@", 1)[-1].lower()
    if not host or _TEMPLATE.fullmatch(host.strip()):
        _unknown(report, f"{name}: url_base {url_base!r} has no static host")
        return []
    full_path = "/" + "/".join(
        part for part in (split.path.strip("/"), path.strip("/")) if part
    )
    request_parameters = requester.get("request_parameters") or {}
    if not isinstance(request_parameters, dict):
        _unknown(
            report,
            f"{name}: request_parameters is an interpolated expression, so the "
            "parameter names it sends cannot be read",
        )
        request_parameters = {}
    names = [_render_parameters(str(key), parameters) for key in request_parameters]
    for component in (
        retriever.get("paginator"),
        stream.get("incremental_sync"),
        retriever.get("partition_router"),
        requester.get("authenticator"),
    ):
        names += _request_option_names(component or {}, parameters)
    for parameter in names:
        if _TEMPLATE.search(parameter):
            _unknown(report, f"{name}: parameter name {parameter!r} is interpolated")
    strategy = (retriever.get("paginator") or {}).get("pagination_strategy") or {}
    page_size = _page_size(strategy.get("page_size"), parameters)
    unread = (
        repr(strategy.get("page_size"))
        if strategy.get("page_size") is not None and page_size is None
        else None
    )
    need = OperationNeed(
        stream=name,
        method=str(requester.get("http_method", "GET")).upper(),
        host=host,
        path=full_path,
        parameters=sorted(set(names)),
        page_size=page_size,
        unread_page_size=unread,
    )
    needs = [need]
    for parent in _parent_streams(retriever):
        needs += _stream_needs(parent, report, seen)
    return needs


def _split_url(url: str) -> SplitResult:
    """`urlsplit` for a URL that may contain Jinja expressions.

    `urlsplit` validates bracketed hosts as IP literals, which a templated label
    such as `{{ config['subdomain'] }}` is not, so expressions are masked while
    splitting and restored afterwards.
    """
    expressions: list[str] = []

    def mask(match: re.Match[str]) -> str:
        expressions.append(match.group(0))
        return f"jinja{len(expressions) - 1}x"

    def unmask(value: str) -> str:
        return re.sub(r"jinja(\d+)x", lambda m: expressions[int(m.group(1))], value)

    split = urlsplit(_TEMPLATE.sub(mask, url))
    return split._replace(netloc=unmask(split.netloc), path=unmask(split.path))


def _page_size(value: Any, parameters: Mapping[str, Any]) -> int | None:
    if isinstance(value, str):
        value = _render_parameters(value, parameters).strip()
        return int(value) if value.isdigit() else None
    return value if type(value) is int else None


def _unknown(report: SupportReport, reason: str) -> None:
    """Record why the result cannot be decided; a definite `unsupported` wins."""
    report.reasons.append(reason)
    if report.result == "supported":
        report.result = "unknown"


def _match_score(manifest_path: str, catalog_path: str) -> int | None:
    """How many wildcard segments a match needs, or `None` when it fails."""
    left = manifest_path.strip("/").split("/")
    right = catalog_path.strip("/").split("/")
    if len(left) != len(right):
        return None
    wildcards = 0
    for a, b in zip(left, right):
        if a == b:
            continue
        if _TEMPLATE.search(a) is not None or b.startswith("{"):
            wildcards += 1
            continue
        return None
    return wildcards


def _check_operation(
    need: OperationNeed,
    catalog: Sequence[Mapping[str, Any]],
    provider: Mapping[str, Any],
) -> None:
    # A templated label (`{{ config['subdomain'] }}.zendesk.com`) matches any
    # single label of a twin host.
    host_pattern = re.compile(
        _TEMPLATE.sub(
            "[^.]+", re.escape(need.host).replace(r"\{\{", "{{").replace(r"\}\}", "}}")
        )
    )
    allowed_hosts = [str(host).lower() for host in provider.get("hosts", [])]
    if not any(host_pattern.fullmatch(host) for host in allowed_hosts):
        need.problems.append(f"host {need.host} is not served by the twin")
        return
    candidates = sorted(
        (
            (score, str(item.get("id")), item)
            for item in catalog
            if item.get("method") == need.method
            and (score := _match_score(need.path, str(item.get("path", ""))))
            is not None
        ),
        # Never compare the operation dicts themselves on a tie.
        key=lambda candidate: candidate[:2],
    )
    if not candidates:
        need.problems.append(f"no twin operation for {need.method} {need.path}")
        return
    if len(candidates) > 1 and candidates[0][0] == candidates[1][0]:
        need.ambiguous = [
            candidate[1] for candidate in candidates if candidate[0] == candidates[0][0]
        ]
        return
    operation = candidates[0][2]
    need.twin_operation = str(operation.get("id"))
    if operation.get("status") == "unsupported":
        need.problems.append(f"twin operation {need.twin_operation} is unsupported")
        return
    if provider.get("unknown_parameters") != "ignore":
        declared = {
            parameter.get("name")
            for parameter in operation.get("parameters", [])
            if isinstance(parameter, dict)
        }
        for name in need.parameters:
            if name not in declared:
                need.problems.append(f"parameter {name!r} is not declared by the twin")
    pagination = operation.get("pagination") or {}
    maximum = pagination.get("max_limit")
    need.page_size_limit = maximum if isinstance(maximum, int) else None
    if (
        need.page_size is not None
        and isinstance(maximum, int)
        and need.page_size > maximum
    ):
        need.problems.append(
            f"page size {need.page_size} exceeds the twin's maximum {maximum}"
        )


def check_dataset_needs(
    needs: Iterable[str],
    provider: str,
    discovery: SandboxDiscovery,
    report: SupportReport,
) -> None:
    """Check `entity` or `entity.field` needs against the twin's dataset schemas."""
    entities = set(discovery.entities(provider))
    for need in needs:
        entity, _, field_name = need.partition(".")
        if entity not in entities:
            report.reasons.append(f"dataset: the twin has no {entity!r} entity")
            report.result = "unsupported"
        elif field_name and field_name not in discovery.entity_fields(provider, entity):
            report.reasons.append(f"dataset: {entity} has no {field_name!r} field")
            report.result = "unsupported"


def check_sandbox_support(
    metadata: Mapping[str, Any],
    manifest: Mapping[str, Any] | None,
    discovery: SandboxDiscovery,
    *,
    streams: Sequence[str] = (),
    dataset_needs: Sequence[str] = (),
) -> SupportReport:
    """Decide whether a twin covers what the named streams need."""
    report = SupportReport(result="supported")
    allowed = _allowed_hosts(metadata)
    if not allowed:
        return SupportReport(
            result="unknown", reasons=["metadata.yaml declares no allowedHosts"]
        )
    provider = _match_provider(allowed, discovery.providers())
    if provider is None:
        configured = [host for host in allowed if _CONFIG_PLACEHOLDER.search(host)]
        return SupportReport(
            # A host taken from config could still be one a twin serves.
            result="unknown" if configured else "unsupported",
            reasons=[f"no sandbox provider serves {', '.join(allowed)}"],
        )
    report.provider = str(provider.get("id"))
    if manifest is None:
        report.result = "unknown"
        report.reasons.append(
            "the connector has no declarative manifest, so its requests cannot "
            "be read statically"
        )
        return report

    resolved = _resolve_manifest(manifest)
    if resolved.get("dynamic_streams") and not streams:
        _unknown(report, "dynamic_streams are not inspected")
    by_name = {
        str(stream.get("name")): stream
        for stream in resolved.get("streams", [])
        if isinstance(stream, dict)
    }
    selected = list(streams) or list(by_name)
    missing = [name for name in selected if name not in by_name]
    if missing:
        report.result = "unknown"
        report.reasons.append(f"streams not in the manifest: {', '.join(missing)}")
    seen: set[int] = set()
    for name in selected:
        if name not in by_name:
            continue
        report.operations += _stream_needs(by_name[name], report, seen)
    # A parent shared by several streams is one set of requests, checked once.
    # Needs that share an operation but differ (a StateDelegatingStream's two
    # inner streams) are merged, so every parameter and the largest page size
    # are still checked.
    unique: dict[tuple[str, str, str, str], OperationNeed] = {}
    for need in report.operations:
        key = (need.stream, need.method, need.host, need.path)
        kept = unique.setdefault(key, need)
        if kept is not need:
            kept.parameters = list(dict.fromkeys([*kept.parameters, *need.parameters]))
            sizes = [size for size in (kept.page_size, need.page_size) if size]
            kept.page_size = max(sizes) if sizes else None
            kept.unread_page_size = kept.unread_page_size or need.unread_page_size
    report.operations = list(unique.values())

    catalog = discovery.operations(report.provider)
    for need in report.operations:
        _check_operation(need, catalog, provider)
        for problem in need.problems:
            report.reasons.append(f"{need.stream} {need.method} {need.path}: {problem}")
        if need.unread_page_size is not None:
            prefix = (
                f"{need.stream} {need.method} {need.path}: page size "
                f"{need.unread_page_size} could not be read"
            )
            # Undecidable only when the twin has a maximum it might exceed.
            if need.page_size_limit is not None:
                _unknown(
                    report,
                    f"{prefix}, so the twin's maximum {need.page_size_limit} "
                    "was not checked",
                )
            else:
                report.warnings.append(f"{prefix}; the twin declares no maximum")
        if need.ambiguous:
            _unknown(
                report,
                f"{need.stream} {need.method} {need.path}: matches several twin "
                f"operations equally ({', '.join(need.ambiguous)})",
            )
    if any(need.problems for need in report.operations):
        report.result = "unsupported"
    if dataset_needs:
        check_dataset_needs(dataset_needs, report.provider, discovery, report)
    report.reasons = list(dict.fromkeys(report.reasons))
    report.warnings = list(dict.fromkeys(report.warnings))
    return report


def run_sandbox_support_check(
    *,
    connector_name: str,
    streams: Sequence[str] = (),
    dataset_needs: Sequence[str] = (),
    connector_dir: Path | None = None,
    ref: str = "master",
    discovery: SandboxDiscovery | None = None,
) -> dict[str, Any]:
    """Load the connector and run the check; failures become an `unknown` report."""
    try:
        if connector_dir is not None:
            metadata, manifest = load_connector_files(connector_dir)
        else:
            metadata, manifest = fetch_connector_files(
                connector_name, ref, resolve_default_github_token(allow_none=True)
            )
        report = check_sandbox_support(
            metadata,
            manifest,
            discovery or SandboxDiscovery(),
            streams=streams,
            dataset_needs=dataset_needs,
        )
    # The check is advisory and the run-time gate is authoritative, so anything
    # it cannot handle -- a broken manifest $ref, odd discovery output -- is an
    # `unknown`, never a crash in the CLI.
    except Exception as exc:
        report = SupportReport(
            result="unknown", reasons=[f"check could not run: {exc}"]
        )
    return {"connector": connector_name, **report.to_dict()}
