"""Parse Python CDK source files into typed `CdkConstruct` records.

Walks `.py` files under a workspace, parses each via the stdlib `ast`
module, and looks for invocations of supported `aws_cdk.aws_<service>.<Construct>`
classes. Each invocation becomes a `CdkConstruct` carrying the
construct's CFN-equivalent type, the kwargs the customer passed, and
crucially a `source_line` pointing back to the `.py` file — the
source-mode value proposition.

What we look for at v0.1.126 (Stage 1):

    from aws_cdk import aws_s3 as s3
    bucket = s3.Bucket(self, "MyBucket", encryption=s3.BucketEncryption.UNENCRYPTED)

The parser handles both `from ... import aws_<service> as <alias>` and
`from aws_cdk.aws_<service> import <Construct>` import styles, and
records the alias-to-canonical mapping per file so a `Bucket(...)` call
elsewhere in the file is recognized as `aws_cdk.aws_s3.Bucket`.

Anything we don't recognize is silently skipped (mirrors the CFN
parser's content-sniff posture). Soft schema drift: parse failures on a
single file produce a `CdkParseFailure` and the walker continues.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from efterlev.errors import DetectorError

# Each entry maps `(module_suffix, ClassName)` → CFN type. The module
# suffix is the part after `aws_cdk.`, e.g. `aws_s3` for buckets.
#
# v0.1.126 (Stage 1): just S3 Bucket — architecture-validation slice.
# v0.1.127 (Stage 2): KMS Key, EC2 SecurityGroup, IAM Role, CloudTrail
#   Trail — covers KSI families CMA, ELP, CNA-RNT, CMT alongside the
#   v0.1.126 CNA storage coverage. Mirrors v0.1.74-77 CFN
#   property-mapping batches: each new construct = one line here +
#   fixture + test, same shape every time.
# Stage 3+ continues to expand. Property-shape translation for L2
# construct semantics (e.g. `encryption=BucketEncryption.S3_MANAGED`
# → CFN `BucketEncryption: {ServerSideEncryptionConfiguration: [...]}`)
# is deferred to Stage N (post-validation).
_SUPPORTED_CONSTRUCTS: dict[tuple[str, str], str] = {
    ("aws_s3", "Bucket"): "AWS::S3::Bucket",
    # v0.1.127 (Stage 2):
    ("aws_kms", "Key"): "AWS::KMS::Key",
    ("aws_ec2", "SecurityGroup"): "AWS::EC2::SecurityGroup",
    ("aws_iam", "Role"): "AWS::IAM::Role",
    ("aws_cloudtrail", "Trail"): "AWS::CloudTrail::Trail",
    # v0.1.128 (Stage 3) — compute + data + observability:
    ("aws_lambda", "Function"): "AWS::Lambda::Function",
    ("aws_rds", "DatabaseInstance"): "AWS::RDS::DBInstance",
    ("aws_dynamodb", "Table"): "AWS::DynamoDB::Table",
    ("aws_logs", "LogGroup"): "AWS::Logs::LogGroup",
    # v0.1.129 (Stage 4) — finisher batch covering remaining common
    # AWS service families. Same shape as Stage 2/3; mirrors CFN
    # gamma.2 batch 8 v0.1.93 finisher pattern. Coverage now spans
    # 27 supported constructs across most KSI families — enough
    # surface area for a labeled-fixture validation pass in Stage 5+.
    ("aws_sns", "Topic"): "AWS::SNS::Topic",
    ("aws_sqs", "Queue"): "AWS::SQS::Queue",
    ("aws_efs", "FileSystem"): "AWS::EFS::FileSystem",
    ("aws_eks", "Cluster"): "AWS::EKS::Cluster",
    ("aws_ec2", "Vpc"): "AWS::EC2::VPC",
    ("aws_secretsmanager", "Secret"): "AWS::SecretsManager::Secret",
    ("aws_apigateway", "RestApi"): "AWS::ApiGateway::RestApi",
    ("aws_apigatewayv2", "HttpApi"): "AWS::ApiGatewayV2::Api",
    ("aws_autoscaling", "AutoScalingGroup"): "AWS::AutoScaling::AutoScalingGroup",
    (
        "aws_elasticloadbalancingv2",
        "ApplicationLoadBalancer",
    ): "AWS::ElasticLoadBalancingV2::LoadBalancer",
    ("aws_cloudwatch", "Alarm"): "AWS::CloudWatch::Alarm",
    ("aws_events", "Rule"): "AWS::Events::Rule",
    ("aws_backup", "BackupVault"): "AWS::Backup::BackupVault",
    ("aws_backup", "BackupPlan"): "AWS::Backup::BackupPlan",
    ("aws_iam", "User"): "AWS::IAM::User",
    ("aws_iam", "Group"): "AWS::IAM::Group",
    ("aws_kinesis", "Stream"): "AWS::Kinesis::Stream",
    ("aws_opensearchservice", "Domain"): "AWS::OpenSearchService::Domain",
}


@dataclass(frozen=True)
class CdkConstruct:
    """One CDK construct invocation parsed from Python source.

    Carries the construct's CFN-equivalent type so downstream code can
    reuse the existing CloudFormation adapter + Terraform-shape detector
    pipeline. The `source_line` field is the source-mode value
    proposition: it points back to the `.py` file the customer wrote,
    not the CFN the generated artifact.
    """

    construct_id: str
    """The CDK logical id (the second positional arg to the construct call)."""
    cfn_type: str
    """The equivalent `AWS::<Service>::<Resource>` CFN type."""
    kwargs: dict[str, Any]
    """Keyword arguments passed to the construct, as raw AST literals where parseable."""
    source_file: Path
    """Source `.py` file the construct was parsed from."""
    source_line: int
    """1-indexed line number of the construct invocation in `source_file`."""


@dataclass(frozen=True)
class CdkParseFailure:
    """One `.py` file the parser couldn't read."""

    file: Path
    reason: str


@dataclass
class _CdkAliasResolver(ast.NodeVisitor):
    """Walks a module's import statements to map aliases → canonical names.

    Handles both styles seen in real CDK code:

        # Style A — module alias
        from aws_cdk import aws_s3 as s3
        # → records: alias_to_module["s3"] = "aws_s3"

        # Style B — direct construct import
        from aws_cdk.aws_s3 import Bucket
        # → records: direct_construct["Bucket"] = ("aws_s3", "Bucket")
    """

    alias_to_module: dict[str, str] = field(default_factory=dict)
    """Maps `s3` → `aws_s3` for `from aws_cdk import aws_s3 as s3`."""
    direct_construct: dict[str, tuple[str, str]] = field(default_factory=dict)
    """Maps `Bucket` → `("aws_s3", "Bucket")` for `from aws_cdk.aws_s3 import Bucket`."""

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.module is None:
            return
        if node.module == "aws_cdk":
            # Style A: `from aws_cdk import aws_s3 as s3`
            for alias in node.names:
                if alias.name.startswith("aws_"):
                    name = alias.asname or alias.name
                    self.alias_to_module[name] = alias.name
        elif node.module.startswith("aws_cdk."):
            # Style B: `from aws_cdk.aws_s3 import Bucket`
            module_suffix = node.module.removeprefix("aws_cdk.")
            for alias in node.names:
                local = alias.asname or alias.name
                self.direct_construct[local] = (module_suffix, alias.name)
        # We intentionally do NOT visit children — top-level imports only.


def _kwarg_to_python(node: ast.expr) -> Any:
    """Best-effort conversion of an AST keyword-arg value to a Python literal.

    For Stage 1 we care about constants (strings, numbers, booleans, None)
    and attribute access (`s3.BucketEncryption.UNENCRYPTED`). Anything
    else (function calls, list comprehensions, f-strings) returns a
    sentinel `<expr>` string so the property is recorded as
    "explicitly-set, opaque value" rather than missing — matters for
    presence-vs-absence detector logic.
    """
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Attribute):
        # Render `s3.BucketEncryption.UNENCRYPTED` as a dotted string.
        parts: list[str] = []
        current: ast.expr = node
        while isinstance(current, ast.Attribute):
            parts.append(current.attr)
            current = current.value
        if isinstance(current, ast.Name):
            parts.append(current.id)
        return ".".join(reversed(parts))
    if isinstance(node, ast.List | ast.Tuple):
        return [_kwarg_to_python(elt) for elt in node.elts]
    return "<expr>"


def _construct_call_to_record(
    call: ast.Call,
    aliases: _CdkAliasResolver,
    source_file: Path,
) -> CdkConstruct | None:
    """Inspect a `Call` node and return a `CdkConstruct` if it's a supported
    CDK construct invocation, else None.
    """
    func = call.func
    # Style A: `s3.Bucket(...)` — Attribute on a Name we've aliased to a module.
    if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
        alias = func.value.id
        class_name = func.attr
        module_suffix = aliases.alias_to_module.get(alias)
        if module_suffix is None:
            return None
        cfn_type = _SUPPORTED_CONSTRUCTS.get((module_suffix, class_name))
        if cfn_type is None:
            return None
    # Style B: `Bucket(...)` — bare Name we've recorded as a direct import.
    elif isinstance(func, ast.Name):
        direct = aliases.direct_construct.get(func.id)
        if direct is None:
            return None
        module_suffix, class_name = direct
        cfn_type = _SUPPORTED_CONSTRUCTS.get((module_suffix, class_name))
        if cfn_type is None:
            return None
    else:
        return None

    # CDK constructs take `(scope, id, **kwargs)` — id is the second positional.
    if len(call.args) < 2 or not isinstance(call.args[1], ast.Constant):
        return None
    construct_id = call.args[1].value
    if not isinstance(construct_id, str):
        return None

    kwargs: dict[str, Any] = {}
    for kw in call.keywords:
        if kw.arg is None:  # **expanded — skip silently
            continue
        kwargs[kw.arg] = _kwarg_to_python(kw.value)

    return CdkConstruct(
        construct_id=construct_id,
        cfn_type=cfn_type,
        kwargs=kwargs,
        source_file=source_file,
        source_line=call.lineno,
    )


def parse_cdk_python_file(path: Path) -> list[CdkConstruct]:
    """Parse one `.py` file and return supported CDK construct invocations.

    Files that import nothing from `aws_cdk` (the vast majority of `.py`
    files in any project) return an empty list immediately — the import
    walk is the cheap content-sniff. Syntax errors raise `DetectorError`.
    """
    try:
        source = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        raise DetectorError(f"cannot read CDK Python source {path}: {e}") from e
    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError as e:
        raise DetectorError(f"cannot parse {path} as Python: {e}") from e

    aliases = _CdkAliasResolver()
    aliases.visit(tree)
    if not aliases.alias_to_module and not aliases.direct_construct:
        return []  # No CDK imports, no constructs.

    constructs: list[CdkConstruct] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            record = _construct_call_to_record(node, aliases, path)
            if record is not None:
                constructs.append(record)
    return constructs


def parse_cdk_python_tree(
    target_dir: Path,
) -> tuple[list[CdkConstruct], list[CdkParseFailure]]:
    """Walk `target_dir` for `.py` files and parse each.

    Skips `.venv`, `node_modules`, `.git`, `__pycache__`, `cdk.out`, and
    `.pytest_cache` — same exclusion list as `scan_terraform`.
    Returns `(parsed_constructs, parse_failures)`. A parse failure on one
    file does not abort the walk — the rest of the tree continues.
    """
    excluded = {".venv", "node_modules", ".git", "__pycache__", "cdk.out", ".pytest_cache"}
    constructs: list[CdkConstruct] = []
    failures: list[CdkParseFailure] = []
    for py in target_dir.rglob("*.py"):
        if any(part in excluded for part in py.parts):
            continue
        try:
            constructs.extend(parse_cdk_python_file(py))
        except DetectorError as e:
            failures.append(CdkParseFailure(file=py, reason=str(e)))
    return constructs, failures
