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
from collections.abc import Iterable, Iterator, Mapping, Sequence
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Literal
from urllib.parse import SplitResult, urlsplit

import yaml
from airbyte_cdk.sources.declarative.interpolation.jinja import JinjaInterpolation
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
# One key of a partition reference: `['downloadUrl']`, `.get('downloadUrl')`
# or `.downloadUrl`.
_PARTITION_KEY = (
    r"""\s*(?:\[\s*['"](\w+)['"]\s*\]|\.get\(\s*['"](\w+)['"]\s*\)|\.(\w+))"""
)
# An expression that is nothing but a partition value:
# `{{ stream_partition['extra_fields']['downloadUrl'] }}`.
_PARTITION_REFERENCE = re.compile(
    rf"\{{\{{\s*(?:stream_partition|stream_slice)(?:{_PARTITION_KEY})*\s*\}}\}}"
)
# Parent-record fields a twin fills in itself, so a case's dataset cannot point
# them elsewhere: the youtube_analytics twin builds each report's `downloadUrl`
# on its own host when a job is created (`twin.py`), and report templates only
# carry times.
_TWIN_GENERATED_URL_FIELDS = {"youtube_analytics": frozenset({"downloadUrl"})}


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
    # An authenticator's token endpoint, which twins may serve without listing
    # it as an operation.
    token_endpoint: bool = False
    # From one branch of a SelectiveAuthenticator, which config may not pick.
    optional: bool = False
    warnings: list[str] = field(default_factory=list)


@dataclass
class SupportReport:
    result: Support
    provider: str | None = None
    operations: list[OperationNeed] = field(default_factory=list)
    reasons: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _manifest_paths(connector_name: str) -> list[str]:
    """Where a connector's declarative manifest may live, relative to its directory.

    A manifest-only connector keeps it at the root. A hybrid low-code/Python
    connector (source-github 2.x) keeps it inside its Python package.
    """
    return ["manifest.yaml", f"{connector_name.replace('-', '_')}/manifest.yaml"]


def load_connector_files(
    connector_dir: Path,
) -> tuple[dict[str, Any], dict[str, Any] | None]:
    """A connector's metadata and its declarative manifest, if it has one."""
    metadata = yaml.safe_load((connector_dir / "metadata.yaml").read_text()) or {}
    repository = str(metadata.get("data", metadata).get("dockerRepository") or "")
    # The directory may be any checkout path; the image names the connector.
    name = repository.rsplit("/", 1)[-1] or connector_dir.name
    for relative in _manifest_paths(name):
        manifest_path = connector_dir / relative
        if manifest_path.exists():
            return metadata, yaml.safe_load(manifest_path.read_text())
    return metadata, None


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
    metadata = yaml.safe_load(metadata_text) or {}
    for relative in _manifest_paths(connector_name):
        manifest_text = get_file_contents_at_ref(
            "airbytehq", "airbyte", f"{base}/{relative}", ref, token
        )
        if manifest_text is not None:
            return metadata, yaml.safe_load(manifest_text)
    return metadata, None


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


def _matching_providers(
    allowed: Sequence[str], providers: Sequence[Mapping[str, Any]]
) -> list[dict[str, Any]]:
    """Every provider serving an allowed host, in discovery order."""
    patterns = [
        compiled for compiled in map(_host_pattern, allowed) if compiled is not None
    ]
    matching = []
    for provider in providers:
        hosts = [str(host).lower() for host in provider.get("hosts", [])]
        if any(pattern.fullmatch(host) for pattern in patterns for host in hosts):
            matching.append(dict(provider))
    return matching


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


def _extra_fields(retriever: Mapping[str, Any]) -> set[str]:
    """The `extra_fields` keys parent records fill in the partition (`downloadUrl`)."""
    routers = retriever.get("partition_router") or []
    routers = routers if isinstance(routers, list) else [routers]
    return {
        # The CDK keys each field by its dot-joined path.
        ".".join(map(str, path))
        for router in routers
        if isinstance(router, dict)
        for config in router.get("parent_stream_configs", []) or []
        if isinstance(config, dict)
        for path in config.get("extra_fields") or []
        if isinstance(path, list)
    }


@dataclass(frozen=True)
class _ConfigValues:
    """The connector config a host is rendered with, as far as it is known."""

    values: dict[str, Any]
    # Keys set to something the check cannot read (`${SANDBOX_CREDENTIAL}`).
    unreadable: frozenset[str] = frozenset()
    # The values are a case's whole config, so a key it leaves out is absent
    # and `config.get(key, fallback)` returns the fallback, as in the
    # connector. Without a case they are only the spec's defaults.
    complete: bool = False


class _KnownConfig(Mapping[str, Any]):
    """Config for rendering a url_base, noting reads of values it does not know.

    Rendering with such a value says nothing about the host: the CDK would
    render it empty or "None", and a condition on it
    (`'https://sandbox...' if config['is_sandbox'] else ...`) could pick either
    branch. Such a render counts as unreadable.
    """

    def __init__(self, config: _ConfigValues) -> None:
        self._config = config
        self.unset_read = False

    def _known(self, key: object) -> bool:
        known = key in self._config.values
        self.unset_read = self.unset_read or not known
        return known

    def __getitem__(self, key: str) -> Any:
        return self._config.values[key] if self._known(key) else ""

    # Whole-config reads (`not config`, `config|length`, `config.items()`) go
    # through these two; the case's other keys would decide them, so they
    # count as unreadable too.
    def __iter__(self) -> Iterator[str]:
        self.unset_read = True
        return iter(self._config.values)

    def __len__(self) -> int:
        self.unset_read = True
        return len(self._config.values)

    def __contains__(self, key: object) -> bool:
        if self._config.complete and key not in self._config.unreadable:
            return key in self._config.values
        return self._known(key)

    def get(self, key: object, *default: Any) -> Any:
        if (
            default
            and self._config.complete
            and key not in self._config.values
            and key not in self._config.unreadable
        ):
            return default[0]
        return self._config.values.get(key) if self._known(key) else None


def _is_literal(value: Any) -> bool:
    """A plain scalar, not a placeholder (`${SANDBOX_CREDENTIAL}`) or a template."""
    if isinstance(value, str):
        return bool(value) and not any(mark in value for mark in ("${", "{{", "{%"))
    return isinstance(value, (int, float, bool))


def _render_config(
    manifest: Mapping[str, Any] | None, config: Mapping[str, Any] | None
) -> _ConfigValues:
    """What a url_base read from config renders with.

    With a case, its literal values: the case run passes its config to the
    connector as is, and the CDK fills in no spec defaults. Without one, the
    spec's defaults. Only scalars are kept, since reads inside an object would
    go unnoticed.
    """
    if config is None:
        defaults = _spec_defaults(manifest) if manifest is not None else {}
        return _ConfigValues({k: v for k, v in defaults.items() if _is_literal(v)})
    return _ConfigValues(
        values={k: v for k, v in config.items() if _is_literal(v)},
        unreadable=frozenset(k for k, v in config.items() if not _is_literal(v)),
        complete=True,
    )


def _host_config(
    manifest: Mapping[str, Any] | None, config: Mapping[str, Any] | None
) -> dict[str, Any]:
    """Config values `${field}` allowedHosts are filled from.

    The case's literal value, else the spec's default: this only picks the
    provider, whose requests are checked against the url_base. A key the case
    sets to anything but a literal stays unfilled.
    """
    defaults = _spec_defaults(manifest) if manifest is not None else {}
    known = {key: value for key, value in defaults.items() if _is_literal(value)}
    for key, value in (config or {}).items():
        if _is_literal(value):
            known[key] = value
        else:
            known.pop(key, None)
    return known


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


@dataclass
class _RecordHost:
    """A stream whose url_base is taken from its parent streams' records."""

    stream: str
    url_base: str
    fields: list[str]
    parents: list[str]


@dataclass
class _Walk:
    """What walking the selected streams needs besides the report."""

    # What a url_base read from config renders with.
    config: _ConfigValues
    seen: set[int] = field(default_factory=set)
    record_hosts: list[_RecordHost] = field(default_factory=list)
    # Streams whose own request host could not be read.
    unread: list[str] = field(default_factory=list)


def _stream_name(stream: Mapping[str, Any]) -> str:
    return str(stream.get("name") or stream.get("$parameters", {}).get("name") or "?")


def _config_url(url_base: str, config: _ConfigValues) -> SplitResult | None:
    """A url_base that only reads config, rendered with the known config values.

    GitHub's `{{ config.get('api_url', 'https://api.github.com').rstrip('/') }}`
    renders to the case's `api_url`, or else to its fallback (to the spec's
    default without a case). `None` when it reads anything but config (the
    CDK rejects undeclared variables), reads a value that is not known, or
    renders to no host.
    """
    known = _KnownConfig(config)
    try:
        rendered = JinjaInterpolation().eval(url_base, config=known)
        # The CDK hands back a template it could not render (a TypeError) as is.
        if not isinstance(rendered, str) or known.unset_read or "{" in rendered:
            return None
        split = urlsplit(rendered)
    except Exception:
        return None
    if not split.hostname or "" in split.hostname.split("."):
        return None
    return split


def _record_fields(url_base: str, extra_fields: set[str]) -> list[str]:
    """The parent-record fields a url_base is built from, when it reads nothing else.

    `{{ stream_partition['extra_fields']['downloadUrl'] }}` -> `["downloadUrl"]`
    when a parent stream config declares that extra field. Any other expression
    (a literal host, config, a filter, another partition key such as the
    parent's id) gives `[]`.
    """
    # The URL must start with the value: `files.example.com/{{ ... }}` names its
    # own host. A path after it is fine.
    reference = _PARTITION_REFERENCE.match(url_base.strip())
    if reference is None or _TEMPLATE.search(url_base.strip()[reference.end() :]):
        return []
    keys = [
        next(part for part in key if part)
        for key in re.findall(_PARTITION_KEY, reference.group(0))
    ]
    if len(keys) != 2 or keys[0] != "extra_fields" or keys[1] not in extra_fields:
        return []
    return [keys[1]]


def _unread_host(report: SupportReport, walk: _Walk, stream: str, reason: str) -> None:
    """A stream whose own request host cannot be read: undecidable, and unread."""
    _unknown(report, f"{stream}: {reason}")
    walk.unread.append(stream)


def _stream_needs(
    stream: Mapping[str, Any], report: SupportReport, walk: _Walk
) -> list[OperationNeed]:
    """The operations one stream and its parents make, recursively."""
    if id(stream) in walk.seen:
        return []
    walk.seen.add(id(stream))
    name = _stream_name(stream)
    if stream.get("type") == "StateDelegatingStream":
        # It reads with one of two complete streams depending on state.
        return [
            need
            for key in ("full_refresh_stream", "incremental_stream")
            if isinstance(stream.get(key), dict)
            for need in _stream_needs(stream[key], report, walk)
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
        _unread_host(report, walk, name, "the manifest declares no url_base/path")
        return []
    url_base = _render_parameters(url_base, parameters)
    path = _render_parameters(path, parameters)
    split = _split_url(url_base)
    host = split.netloc.rsplit("@", 1)[-1].lower()
    if not host or _TEMPLATE.fullmatch(host.strip()):
        rendered = _config_url(url_base, walk.config)
        parents = _parent_streams(retriever)
        fields = _record_fields(url_base, _extra_fields(retriever))
        if rendered is not None:
            split = rendered
            host = split.netloc.rsplit("@", 1)[-1].lower()
        elif fields and parents:
            # The host is only known from the parents' records at run time;
            # whether that is acceptable is decided once the parents are checked.
            walk.record_hosts.append(
                _RecordHost(name, url_base, fields, [_stream_name(p) for p in parents])
            )
            needs = _token_endpoint_needs(requester.get("authenticator"), walk.config)
            for parent in parents:
                needs += _stream_needs(parent, report, walk)
            return needs
        else:
            _unread_host(
                report, walk, name, f"url_base {url_base!r} has no static host"
            )
            return []
    elif _TEMPLATE.search(host) and walk.config.complete:
        # A templated label (`{{ config['subdomain'] }}.zendesk.com`): the
        # case's value decides the host. Without a case it matches any label.
        rendered = _config_url(f"https://{split.netloc}", walk.config)
        if (
            rendered is None
            or rendered.path not in ("", "/")
            or rendered.query
            or rendered.fragment
            or "@" in rendered.netloc
        ):
            # A value with a path or userinfo would move the request too.
            _unread_host(
                report,
                walk,
                name,
                f"url_base {url_base!r} has a host label the case's config does "
                "not set to a plain host name",
            )
            return []
        host = rendered.netloc.lower()
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
    needs = [need, *_token_endpoint_needs(requester.get("authenticator"), walk.config)]
    for parent in _parent_streams(retriever):
        needs += _stream_needs(parent, report, walk)
    return needs


def _token_endpoint_needs(
    authenticator: Any, config: _ConfigValues, optional: bool = False
) -> list[OperationNeed]:
    """`POST` needs for the OAuth token endpoints an authenticator refreshes against."""
    if not isinstance(authenticator, dict):
        return []
    nested = authenticator.get("authenticators")
    if isinstance(nested, dict):
        # A SelectiveAuthenticator picks one of these from config.
        return [
            need
            for inner in nested.values()
            for need in _token_endpoint_needs(inner, config, optional=True)
        ]
    endpoint = authenticator.get("token_refresh_endpoint")
    if not isinstance(endpoint, str):
        return []
    split = _split_url(endpoint)
    host = split.netloc.rsplit("@", 1)[-1].lower()
    if not host:
        return []
    if _TEMPLATE.search(host) and config.complete:
        # A case's value names the host (`{{ config['subdomain'] }}.zendesk.com`).
        rendered = _config_url(f"https://{split.netloc}", config)
        if rendered is not None and "@" not in rendered.netloc:
            host = rendered.netloc.lower()
    return [
        OperationNeed(
            stream="authenticator",
            method="POST",
            host=host,
            path="/" + split.path.strip("/"),
            token_endpoint=True,
            optional=optional,
        )
    ]


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


def _host_served(host: str, provider: Mapping[str, Any]) -> bool:
    # A templated label (`{{ config['subdomain'] }}.zendesk.com`) matches any
    # single label of a twin host.
    host_pattern = re.compile(
        _TEMPLATE.sub(
            "[^.]+", re.escape(host).replace(r"\{\{", "{{").replace(r"\}\}", "}}")
        )
    )
    return any(
        host_pattern.fullmatch(str(candidate).lower())
        for candidate in provider.get("hosts", [])
    )


def _check_operation(
    need: OperationNeed,
    catalog: Sequence[Mapping[str, Any]],
    provider: Mapping[str, Any],
) -> None:
    if not _host_served(need.host, provider):
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
        if need.token_endpoint:
            need.warnings.append(
                f"the twin lists no operation for the token endpoint {need.method} "
                f"{need.path}; the case lane's twin-gap gate covers it"
            )
            return
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
    check_streams: bool = False,
    host_only: bool = False,
    config: Mapping[str, Any] | None = None,
) -> SupportReport:
    """Decide whether a twin covers what the named streams need.

    Args:
        config: The case's connector config. Hosts read from config use its
            literal values, then the spec's defaults; without it (no case),
            only the spec's defaults.
        check_streams: Check the streams the manifest's CHECK reads instead of
            `streams` (which stay the fallback when it names none).
        host_only: Only match the provider: a twin serving an allowed host
            that, when the manifest's request hosts can be read, also serves
            one of them (see `_host_only_report`). No operation is checked.
    """
    report = SupportReport(result="supported")
    data = metadata.get("data", metadata)
    if manifest is None and data.get("connectorSubtype") == "database":
        return SupportReport(
            result="unsupported",
            reasons=["database (JDBC) sources are not served by HTTP twins"],
        )
    allowed = _resolve_host_placeholders(
        _allowed_hosts(metadata), _host_config(manifest, config)
    )
    if not allowed:
        return SupportReport(
            result="unknown", reasons=["metadata.yaml declares no allowedHosts"]
        )
    candidates = _matching_providers(allowed, discovery.providers())
    if not candidates:
        configured = [host for host in allowed if _CONFIG_PLACEHOLDER.search(host)]
        return SupportReport(
            # A host taken from config could still be one a twin serves.
            result="unknown" if configured else "unsupported",
            reasons=[f"no sandbox provider serves {', '.join(allowed)}"],
        )
    if host_only:
        return _host_only_report(candidates, manifest, config)
    # A wrong provider is rejected below by its operation checks.
    provider = candidates[0]
    report.provider = str(provider.get("id"))
    if manifest is None:
        report.result = "unknown"
        report.reasons.append(
            "the connector has no declarative manifest, so its requests cannot "
            "be read statically"
        )
        return report

    if "language:manifest-only" not in (data.get("tags") or []):
        report.warnings.append(
            "the connector is not manifest-only, so its Python code may define "
            "streams or make requests the manifest does not show; the case "
            "lane's twin-gap gate covers them"
        )
    resolved = _resolve_manifest(manifest)
    if resolved.get("dynamic_streams") and not streams:
        _unknown(report, "dynamic_streams are not inspected")
    by_name = {
        str(stream.get("name")): stream
        for stream in resolved.get("streams", [])
        if isinstance(stream, dict)
    }
    selected = list(streams) or list(by_name)
    if check_streams:
        selected = _check_stream_names(resolved) or selected
    missing = [name for name in selected if name not in by_name]
    if missing:
        report.result = "unknown"
        report.reasons.append(f"streams not in the manifest: {', '.join(missing)}")
    walk = _Walk(config=_render_config(manifest, config))
    for name in selected:
        if name not in by_name:
            continue
        report.operations += _stream_needs(by_name[name], report, walk)
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
            # Required by any stream means required.
            kept.optional = kept.optional and need.optional
    report.operations = list(unique.values())

    catalog = discovery.operations(report.provider)
    for need in report.operations:
        _check_operation(need, catalog, provider)
        if need.optional:
            # An authenticator option config need not pick: a case using it
            # fails at run time as a twin gap.
            need.warnings += [
                f"{need.stream} {need.method} {need.path}: {problem} (one "
                "authenticator option; a case must configure another option)"
                for problem in [
                    *need.problems,
                    *(
                        [
                            f"matches several twin operations ({', '.join(need.ambiguous)})"
                        ]
                        if need.ambiguous
                        else []
                    ),
                ]
            ]
            need.problems, need.ambiguous = [], []
        for problem in need.problems:
            report.reasons.append(f"{need.stream} {need.method} {need.path}: {problem}")
        report.warnings += need.warnings
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
    for record_host in walk.record_hosts:
        _check_record_host(record_host, report, provider)
    if any(need.problems for need in report.operations):
        report.result = "unsupported"
    if dataset_needs:
        check_dataset_needs(dataset_needs, report.provider, discovery, report)
    report.reasons = list(dict.fromkeys(report.reasons))
    report.warnings = list(dict.fromkeys(report.warnings))
    return report


_ALLOWED_HOSTS_ONLY = "so the provider was matched on allowedHosts only"
_UNREAD_NAMES_SHOWN = 5


def _request_hosts(
    manifest: Mapping[str, Any], config: Mapping[str, Any] | None
) -> tuple[list[str], list[str]]:
    """The hosts a manifest's streams request, and the streams whose host is unread.

    Every stream is walked as the full check walks it, and so are dynamic
    streams' templates and component resolvers, which make requests too.
    Token endpoints are left out: a twin that serves only a shared one
    (`oauth2.googleapis.com`) does not serve the connector.
    """
    resolved = _resolve_manifest(manifest)
    # The walk's reasons and warnings concern operations, which are not checked.
    scratch = SupportReport(result="supported")
    walk = _Walk(config=_render_config(manifest, config))
    streams = [s for s in resolved.get("streams") or [] if isinstance(s, dict)]
    for entry in resolved.get("dynamic_streams") or []:
        if not isinstance(entry, dict):
            continue
        if isinstance(entry.get("stream_template"), dict):
            streams.append(entry["stream_template"])
        resolver = entry.get("components_resolver")
        retriever = resolver.get("retriever") if isinstance(resolver, dict) else None
        if isinstance(retriever, dict):
            name = f"{entry.get('name') or 'dynamic_streams'} resolver"
            streams.append({"name": name, "retriever": retriever})
    needs = [
        need for stream in streams for need in _stream_needs(stream, scratch, walk)
    ]
    hosts = sorted({need.host for need in needs if not need.token_endpoint})
    return hosts, list(dict.fromkeys(walk.unread))


def _host_only_report(
    candidates: Sequence[Mapping[str, Any]],
    manifest: Mapping[str, Any] | None,
    config: Mapping[str, Any] | None,
) -> SupportReport:
    """Pick the provider among those serving an allowed host.

    Without a manifest, or when no request host can be read from it, the
    first one wins. Otherwise it must also serve a host the streams request,
    since twins list shared hosts (youtube_analytics `oauth2.googleapis.com`)
    that many other connectors allow.
    """
    first = str(candidates[0].get("id"))
    if manifest is None:
        return SupportReport(
            result="supported",
            provider=first,
            warnings=[
                f"the connector has no declarative manifest, {_ALLOWED_HOSTS_ONLY}"
            ],
        )
    hosts, unread = _request_hosts(manifest, config)
    if not hosts:
        return SupportReport(
            result="supported",
            provider=first,
            warnings=[
                "no stream's request host could be read from the manifest, "
                + _ALLOWED_HOSTS_ONLY
            ],
        )
    for provider in candidates:
        if any(_host_served(host, provider) for host in hosts):
            return SupportReport(result="supported", provider=str(provider.get("id")))
    reason = (
        f"allowedHosts match {', '.join(str(p.get('id')) for p in candidates)}, "
        f"but no stream requests a host they serve (requests go to {', '.join(hosts)})"
    )
    if not unread:
        return SupportReport(result="unsupported", reasons=[reason])
    shown = ", ".join(unread[:_UNREAD_NAMES_SHOWN])
    if len(unread) > _UNREAD_NAMES_SHOWN:
        shown += ", ..."
    # An unread host could be one a twin serves.
    return SupportReport(
        result="unknown",
        reasons=[
            f"{reason}; the host of {len(unread)} stream(s) could not be read ({shown})"
        ],
    )


def _check_stream_names(manifest: Mapping[str, Any]) -> list[str]:
    check = manifest.get("check") or {}
    names = check.get("stream_names") if isinstance(check, dict) else None
    return [str(name) for name in names] if isinstance(names, list) else []


def _check_record_host(
    record_host: _RecordHost, report: SupportReport, provider: Mapping[str, Any]
) -> None:
    """Accept a url_base taken from parent records the twin itself fills in.

    The twin, not the case's dataset, has to produce that URL, or a case could
    point the connector at a host the twin does not serve: `sandbox run` gives
    the connector no egress, so such a request fails inside the sandbox
    without being traced as a twin gap.
    """
    parents = ", ".join(record_host.parents)
    prefix = (
        f"{record_host.stream}: url_base {record_host.url_base!r} takes its host "
        f"from {parents} records ({', '.join(record_host.fields)})"
    )
    generated = _TWIN_GENERATED_URL_FIELDS.get(str(provider.get("id")), frozenset())
    if not set(record_host.fields) <= generated:
        _unknown(report, f"{prefix}, which the twin is not known to generate")
        return
    for parent in record_host.parents:
        needs = [need for need in report.operations if need.stream == parent]
        if not needs or not all(_host_served(n.host, provider) for n in needs):
            _unknown(report, f"{prefix}, and not every parent is served by the twin")
            return
    report.warnings.append(
        f"{prefix}, so its requests were not checked here. The case lane's "
        "twin-gap gate covers them when they reach the twin; a URL on a host "
        "the twin does not serve fails inside the sandbox (no egress) and is "
        "not reported as a twin gap"
    )


def _spec_defaults(manifest: Mapping[str, Any]) -> dict[str, Any]:
    """The top-level defaults of the manifest's connection specification."""
    spec = manifest.get("spec")
    spec = spec.get("connection_specification") if isinstance(spec, dict) else None
    properties = spec.get("properties") if isinstance(spec, dict) else None
    if not isinstance(properties, dict):
        return {}
    return {
        name: schema["default"]
        for name, schema in properties.items()
        if isinstance(schema, dict) and "default" in schema
    }


def _resolve_host_placeholders(
    allowed: Sequence[str], known: Mapping[str, Any]
) -> list[str]:
    """Fill `${field}` host placeholders (GitHub `${api_url}`) from known config."""

    def known_host(match: re.Match[str]) -> str:
        value = known.get(match.group(0)[2:-1])
        if not isinstance(value, str):
            return match.group(0)
        split = urlsplit(value if "//" in value else f"//{value}")
        return (split.hostname or match.group(0)).lower()

    return [_CONFIG_PLACEHOLDER.sub(known_host, host) for host in allowed]


def connector_files(
    connector_name: str, ref: str, connector_dir: Path | None = None
) -> tuple[dict[str, Any], dict[str, Any] | None]:
    """A connector's metadata and manifest, from `connector_dir` or GitHub at `ref`."""
    if connector_dir is not None:
        return load_connector_files(connector_dir)
    return fetch_connector_files(
        connector_name, ref, resolve_default_github_token(allow_none=True)
    )


def manifest_stream_names(
    metadata: Mapping[str, Any], manifest: Mapping[str, Any] | None
) -> set[str] | None:
    """Every stream a manifest-only connector defines; None for any other connector.

    Raises:
        ValueError: The manifest has `dynamic_streams`, whose names it cannot list.
    """
    data = metadata.get("data", metadata)
    if manifest is None or "language:manifest-only" not in (data.get("tags") or []):
        # A connector with Python streams defines streams no manifest lists.
        return None
    resolved = _resolve_manifest(manifest)
    if resolved.get("dynamic_streams"):
        raise ValueError("the manifest has dynamic_streams, whose names it cannot list")
    return {
        str(stream["name"])
        for stream in resolved.get("streams", [])
        if isinstance(stream, dict) and stream.get("name")
    }


def run_sandbox_support_check(
    *,
    connector_name: str,
    streams: Sequence[str] = (),
    dataset_needs: Sequence[str] = (),
    connector_dir: Path | None = None,
    ref: str = "master",
    discovery: SandboxDiscovery | None = None,
    check_streams: bool = False,
    host_only: bool = False,
    files: tuple[dict[str, Any], dict[str, Any] | None] | None = None,
    config: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Load the connector and run the check; failures become an `unknown` report.

    Args:
        files: The connector's metadata and manifest, when the caller has them.
        config: The case's connector config (see `check_sandbox_support`).
    """
    try:
        metadata, manifest = files or connector_files(
            connector_name, ref, connector_dir
        )
        report = check_sandbox_support(
            metadata,
            manifest,
            discovery or SandboxDiscovery(),
            streams=streams,
            dataset_needs=dataset_needs,
            check_streams=check_streams,
            host_only=host_only,
            config=config,
        )
    # The check is advisory and the run-time gate is authoritative, so anything
    # it cannot handle -- a broken manifest $ref, odd discovery output -- is an
    # `unknown`, never a crash in the CLI.
    except Exception as exc:
        report = SupportReport(
            result="unknown", reasons=[f"check could not run: {exc}"]
        )
    return {"connector": connector_name, **report.to_dict()}
