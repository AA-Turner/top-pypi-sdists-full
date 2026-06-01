"""CDK Python source-mode parser — parses Python CDK source files directly.

Why source-mode (vs the existing `cdk synth → CFN → scan` synth-mode that
graduated at v0.1.99-102): synth-mode loses source-level traceability.
The customer's reviewer sees `Resources.MyBucketF68F3FF0` in the
synthesized CFN but doesn't know that line 42 of `infra/storage_stack.py`
is where the bucket's `encryption=BucketEncryption.UNENCRYPTED` lives.
Source-mode preserves the .py file:line citation through the Evidence
record, so Gap Agent narratives + remediation diffs land in the
customer's actual code rather than CDK's generated artifact.

Scope at v0.1.126 (Stage 1 of the CDK source-mode arc):
- **Python CDK only.** TypeScript (the ~70% majority) is Stage 2+ —
  Python's stdlib `ast` keeps the architecture-validation parser
  trivial; once the source-mode pipeline is proven, TS adds a
  parser layer reusing everything downstream.
- **One construct: `aws_cdk.aws_s3.Bucket`.** Stage 2+ expands the
  construct table mechanically (same shape as the v0.1.74-93 CFN
  property-mapping batches).
- **Behind `--allow-cdk-py` opt-in flag** (mirrors `--allow-cfn` and
  `--allow-import` pre-graduation patterns). Removed at end of arc
  when source-mode is validated against a labeled fixture.
"""

from __future__ import annotations

from efterlev.cdk_python.adapter import (
    adapt_cdk_construct_to_terraform,
    adapt_cdk_constructs,
)
from efterlev.cdk_python.parser import (
    CdkConstruct,
    CdkParseFailure,
    parse_cdk_python_file,
    parse_cdk_python_tree,
)

__all__ = [
    "CdkConstruct",
    "CdkParseFailure",
    "adapt_cdk_construct_to_terraform",
    "adapt_cdk_constructs",
    "parse_cdk_python_file",
    "parse_cdk_python_tree",
]
