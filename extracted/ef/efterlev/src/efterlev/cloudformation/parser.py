"""Parse CloudFormation YAML/JSON templates into typed `CfnTemplate` objects.

Per DECISIONS 2026-05-12 (Tier 5 #1, "CloudFormation/CDK synth-mode
support"), v1 scope is: read CFN JSON or YAML — whether hand-authored
or `cdk synth`-generated — and emit resource records the existing
detector library can consume via the adapter shim in `adapter.py`.

CFN YAML uses non-standard `!Tag` syntax for intrinsic functions
(`!Ref`, `!Sub`, `!GetAtt`, `!Join`, etc.) that PyYAML's standard
loader rejects. This module installs a custom loader that converts
each intrinsic to its long-form dict representation:

    !Ref MyBucket          → {"Ref": "MyBucket"}
    !Sub "${X}-bar"        → {"Fn::Sub": "${X}-bar"}
    !GetAtt MyBucket.Arn   → {"Fn::GetAtt": ["MyBucket", "Arn"]}

The long-form is what `cdk synth` JSON output emits natively, so the
JSON path and the YAML path produce structurally identical dicts
downstream. The adapter then handles the long-form intrinsics
uniformly when extracting property values.

CFN-template detection: a file is CFN if its top-level mapping
contains either `AWSTemplateFormatVersion` or `Resources`. Other
YAML/JSON files (configs, k8s manifests, npm package.json, etc.)
are skipped silently per the existing scan-policy pattern.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from efterlev.errors import DetectorError


@dataclass(frozen=True)
class CfnResource:
    """One CloudFormation resource — `LogicalId` + `Type` + `Properties`.

    Stored in long-form (intrinsic functions resolved to dict shape).
    The adapter in `adapter.py` converts this to a `TerraformResource`-
    shaped object the detector library can consume.
    """

    logical_id: str
    """The resource's name in the template (CFN's `LogicalId`)."""
    type: str
    """The CFN resource type (e.g. `AWS::S3::Bucket`)."""
    properties: dict[str, Any]
    """The resource's `Properties` block as a Python dict."""
    file: Path
    """Source file the resource was parsed from."""


@dataclass(frozen=True)
class CfnParseFailure:
    """One file the parser couldn't read."""

    file: Path
    reason: str


@dataclass(frozen=True)
class CfnParseResult:
    """Output of `parse_cfn_tree`: successful resources + per-file failures.

    Partial-success semantics mirror `parse_terraform_tree` — one
    weird file should not block detection on the other 1800.
    """

    resources: list[CfnResource]
    parse_failures: list[CfnParseFailure]
    files_scanned: int
    """Count of files that were inspected (including non-CFN YAML/JSON
    that were content-sniffed and skipped). Useful for the scan-output
    summary."""


# --- YAML loader with CFN intrinsic-function support ------------------------


class _CfnSafeLoader(yaml.SafeLoader):
    """A SafeLoader subclass we install CFN-tag constructors on.

    We subclass rather than mutating PyYAML's global SafeLoader so the
    CFN-specific tag handling doesn't leak into other YAML use elsewhere
    in efterlev (the manifest loader, the docs-build, etc.).
    """


def _ref_constructor(loader: yaml.Loader, node: yaml.Node) -> dict[str, Any]:
    """`!Ref X` → `{"Ref": "X"}` (or scalar/sequence forms preserved)."""
    return {"Ref": loader.construct_scalar(node)}  # type: ignore[arg-type]


def _short_form_intrinsic(name: str) -> Any:
    """Build a constructor that converts `!<short>` → `{"Fn::<name>": ...}`.

    PyYAML node types determine the constructor mode:
      - scalar  → `{"Fn::<name>": "value"}`  (the common single-arg form)
      - sequence → `{"Fn::<name>": [...]}`
      - mapping  → `{"Fn::<name>": {...}}`
    """

    long_form_key = f"Fn::{name}"

    def _ctor(loader: yaml.Loader, node: yaml.Node) -> dict[str, Any]:
        if isinstance(node, yaml.ScalarNode):
            value: Any = loader.construct_scalar(node)
        elif isinstance(node, yaml.SequenceNode):
            value = loader.construct_sequence(node, deep=True)
        elif isinstance(node, yaml.MappingNode):
            value = loader.construct_mapping(node, deep=True)
        else:
            raise DetectorError(f"unexpected YAML node type {type(node).__name__} for !{name}")
        return {long_form_key: value}

    return _ctor


def _getatt_constructor(loader: yaml.Loader, node: yaml.Node) -> dict[str, Any]:
    """`!GetAtt LogicalId.Attr` → `{"Fn::GetAtt": ["LogicalId", "Attr"]}`.

    GetAtt's short form is `LogicalId.AttrName` (a dotted scalar) while
    its long form is a 2-element list. Normalize to the long form so
    downstream consumers see one shape.
    """
    if isinstance(node, yaml.ScalarNode):
        scalar = loader.construct_scalar(node)
        # `!GetAtt MyBucket.Arn` → ["MyBucket", "Arn"]; the no-attr edge
        # case `!GetAtt MyBucket` passes through as 1-element list.
        parts = scalar.split(".", 1) if "." in scalar else [scalar]
        return {"Fn::GetAtt": parts}
    if isinstance(node, yaml.SequenceNode):
        return {"Fn::GetAtt": loader.construct_sequence(node, deep=True)}
    raise DetectorError(f"unexpected YAML node type for !GetAtt: {type(node).__name__}")


# Register every CFN intrinsic. Source: AWS CloudFormation Intrinsic Function
# reference (the documented short-form tags). New intrinsics added by AWS in
# the future can be added here; the long-form key is always `Fn::<name>`
# except for `!Ref` which has no `Fn::` prefix.
#
# Rules-section intrinsics (ValueOf, ValueOfAll, RefAll, EachMemberEquals,
# EachMemberIn, Contains) added v0.1.103 after a real-world CFN template
# (aws-quickstart/quickstart-aws-aurora-postgresql) failed to parse on
# `!ValueOf` in its `Rules:` block — silently producing zero resources.
# These intrinsics only appear in `Rules:` (parameter-validation pre-flight)
# and don't affect resource extraction; the parser just needs to recognize
# the tags so the YAML load doesn't crash.
_CFN_INTRINSICS: tuple[str, ...] = (
    "Base64",
    "Cidr",
    "FindInMap",
    "Join",
    "Length",
    "Select",
    "Split",
    "Sub",
    "Transform",
    "And",
    "Or",
    "Not",
    "Equals",
    "If",
    "Condition",
    "ForEach",
    "ToJsonString",
    "ImportValue",
    # Rules-section intrinsics (parameter validation pre-flight; v0.1.103):
    "Contains",
    "EachMemberEquals",
    "EachMemberIn",
    "RefAll",
    "ValueOf",
    "ValueOfAll",
)

_CfnSafeLoader.add_constructor("!Ref", _ref_constructor)  # type: ignore[arg-type]
_CfnSafeLoader.add_constructor("!GetAtt", _getatt_constructor)  # type: ignore[arg-type]
for _intrinsic in _CFN_INTRINSICS:
    _CfnSafeLoader.add_constructor(  # type: ignore[arg-type]
        f"!{_intrinsic}", _short_form_intrinsic(_intrinsic)
    )


# --- File-level parsers ----------------------------------------------------


def _looks_like_cfn(top_level: Any) -> bool:
    """Return True when a parsed top-level dict has CFN-template shape.

    Per DECISIONS 2026-05-12 (Decision #3): content-sniff for
    `AWSTemplateFormatVersion` or `Resources` at the top level.
    """
    if not isinstance(top_level, dict):
        return False
    return "AWSTemplateFormatVersion" in top_level or "Resources" in top_level


def _parse_yaml(text: str) -> Any:
    """Parse CFN YAML using the intrinsic-aware loader.

    `_CfnSafeLoader` is a SafeLoader subclass (see class definition
    above). Bandit's B506 rule treats any `yaml.load(...)` call as
    unsafe; here it's a false positive — the SafeLoader-derived
    loader doesn't allow arbitrary-object instantiation, only the
    19 CFN intrinsic tags we explicitly registered. nosec annotation
    pins this exception.
    """
    return yaml.load(text, Loader=_CfnSafeLoader)  # nosec B506


def _parse_json(text: str) -> Any:
    """Parse CFN JSON using the standard json loader."""
    return json.loads(text)


def parse_cfn_file(path: Path) -> list[CfnResource]:
    """Parse a single CFN file and return its resources.

    Returns an empty list if the file doesn't have CFN-template shape
    (per `_looks_like_cfn`); raises `DetectorError` only on actual
    parse errors (malformed YAML/JSON).

    Caller is responsible for the partial-success collect-and-continue
    pattern across many files; this function is single-file.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as e:
        raise DetectorError(f"failed to read CFN file at {path}: {e}") from e

    # .yaml / .yml → CFN intrinsic-aware YAML loader.
    # .json → standard json.loads (faster + stricter than YAML for
    # JSON-shaped content).
    try:
        data = _parse_json(text) if path.suffix.lower() == ".json" else _parse_yaml(text)
    except (yaml.YAMLError, json.JSONDecodeError) as e:
        raise DetectorError(f"CFN parse error in {path}: {e}") from e

    if not _looks_like_cfn(data):
        return []

    resources_block = data.get("Resources")
    if not isinstance(resources_block, dict):
        return []

    out: list[CfnResource] = []
    for logical_id, resource_block in resources_block.items():
        if not isinstance(resource_block, dict):
            continue
        rtype = resource_block.get("Type")
        if not isinstance(rtype, str):
            continue
        properties = resource_block.get("Properties") or {}
        if not isinstance(properties, dict):
            properties = {}
        out.append(
            CfnResource(
                logical_id=str(logical_id),
                type=rtype,
                properties=properties,
                file=path,
            )
        )
    return out


def parse_cfn_tree(target_dir: Path) -> CfnParseResult:
    """Walk `target_dir` for CFN templates and parse each.

    Walks for `*.yaml`, `*.yml`, `*.json` files. Each is content-sniffed
    via `_looks_like_cfn`; non-CFN YAML/JSON (k8s manifests, configs,
    package.json, etc.) is skipped silently. Parse errors on actual
    CFN-shaped files are collected as `CfnParseFailure` records (the
    partial-success pattern).
    """
    if not target_dir.is_dir():
        raise DetectorError(f"target directory not found: {target_dir}")

    resources: list[CfnResource] = []
    failures: list[CfnParseFailure] = []
    files_scanned = 0

    candidates = (
        list(target_dir.rglob("*.yaml"))
        + list(target_dir.rglob("*.yml"))
        + list(target_dir.rglob("*.json"))
    )
    for path in sorted(candidates):
        # Skip files under hidden dirs (.git, .efterlev, etc.) — same
        # walk-policy as parse_terraform_tree.
        if any(part.startswith(".") for part in path.relative_to(target_dir).parts[:-1]):
            continue
        files_scanned += 1
        try:
            file_resources = parse_cfn_file(path)
        except DetectorError as e:
            failures.append(CfnParseFailure(file=path, reason=str(e)))
            continue
        resources.extend(file_resources)

    return CfnParseResult(
        resources=resources,
        parse_failures=failures,
        files_scanned=files_scanned,
    )
