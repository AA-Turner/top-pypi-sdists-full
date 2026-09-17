"""How a stored Bedrock credential value becomes client auth for ``CachingAwsBedrock``.

The platform stores one string per Bedrock credential. Three shapes are accepted:

- a bare token -> per-client bearer auth (``aws_bearer_token``);
- a bare IAM role ARN (the app's "IAM role" method) -> STS AssumeRole from the runtime's own
  identity, as refreshable credentials on a boto3 session;
- a JSON document ``{"role_arn": ..., "external_id"?: ..., "aws_region"?: ...}`` or
  ``{"bearer_token": ...}`` (the same shape the agent-controller's LLM proxy accepts).

Nothing here touches ``os.environ``: a process-level write would hand one tenant's credential to
every other task in a shared worker. Mirror of ``services/agent-controller/src/utils/bedrock_creds.py``
in xpander-mono, which the SDK cannot import.
"""

from __future__ import annotations

import json
import re
from os import getenv
from dataclasses import dataclass
from typing import Any, Dict, Optional

_ROLE_ARN_RE = re.compile(r"^arn:aws(?:-[a-z]+)*:iam::\d{12}:role/[\w+=,.@/-]+$")
_AWS_REGION_RE = re.compile(r"^[a-z]{2}(?:-[a-z]+)+-\d+$")
_DEFAULT_ROLE_SESSION_NAME = "xpander-bedrock"


def is_role_arn(value: Optional[str]) -> bool:
    return bool(value) and _ROLE_ARN_RE.fullmatch(value.strip()) is not None


@dataclass(frozen=True)
class BedrockCredential:
    """One resolved credential: either a bearer token or a role to assume; ``region`` only when the doc named one."""

    bearer_token: Optional[str] = None
    role_arn: Optional[str] = None
    external_id: Optional[str] = None
    role_session_name: Optional[str] = None
    region: Optional[str] = None


def parse_bedrock_credential(value: Optional[str]) -> Optional[BedrockCredential]:
    """The stored string as a credential, or None when it is empty or names nothing usable."""
    raw = (value or "").strip()
    if not raw:
        return None
    if is_role_arn(raw):
        return BedrockCredential(role_arn=raw)
    if raw[0] not in "{[":
        return BedrockCredential(bearer_token=raw)
    try:
        doc = json.loads(raw)
    except ValueError:
        return None
    if not isinstance(doc, dict):
        return None
    region = str(doc.get("aws_region") or doc.get("region") or "").strip() or None
    if region and not _AWS_REGION_RE.fullmatch(region):
        # the region lands in the bedrock-runtime hostname; refuse anything that is not a plain region name
        return None
    if bearer := str(doc.get("bearer_token") or "").strip():
        return BedrockCredential(bearer_token=bearer, region=region)
    if role_arn := str(doc.get("role_arn") or "").strip():
        return BedrockCredential(
            role_arn=role_arn,
            external_id=str(doc.get("external_id") or "").strip() or None,
            role_session_name=str(doc.get("role_session_name") or "").strip() or None,
            region=region,
        )
    return None


def assume_role_session(credential: BedrockCredential, region: Optional[str]):
    """A boto3 Session whose credentials are the assumed role's, refreshed before expiry on every client build."""
    import boto3
    import botocore.session
    from botocore.credentials import RefreshableCredentials

    # STS needs a region to resolve its endpoint; fall back the way the rest of the SDK does
    sts_region = (
        region or getenv("AWS_REGION") or getenv("AWS_DEFAULT_REGION") or "us-east-1"
    )
    sts = boto3.session.Session().client("sts", region_name=sts_region)
    params: Dict[str, Any] = {
        "RoleArn": credential.role_arn,
        "RoleSessionName": credential.role_session_name or _DEFAULT_ROLE_SESSION_NAME,
    }
    if credential.external_id:
        params["ExternalId"] = credential.external_id

    def _fetch() -> Dict[str, str]:
        creds = sts.assume_role(**params)["Credentials"]
        return {
            "access_key": creds["AccessKeyId"],
            "secret_key": creds["SecretAccessKey"],
            "token": creds["SessionToken"],
            "expiry_time": creds["Expiration"].isoformat(),
        }

    refreshable = RefreshableCredentials.create_from_metadata(
        metadata=_fetch(), refresh_using=_fetch, method="sts-assume-role"
    )
    botocore_session = botocore.session.get_session()
    botocore_session._credentials = refreshable
    return boto3.session.Session(botocore_session=botocore_session, region_name=region)


def bedrock_auth_kwargs(
    value: Optional[str], *, region: Optional[str] = None
) -> Dict[str, Any]:
    """``CachingAwsBedrock`` constructor kwargs for a stored credential value.

    Empty -> nothing (the pod's default chain). Bearer -> ``aws_bearer_token``. Role -> ``session``.
    Never both: with both set the client would send the bearer header and ignore the session.
    """
    credential = parse_bedrock_credential(value)
    if credential is None:
        return {}
    effective_region = credential.region or region
    if credential.bearer_token:
        kwargs: Dict[str, Any] = {"aws_bearer_token": credential.bearer_token}
    else:
        kwargs = {"session": assume_role_session(credential, effective_region)}
    if effective_region:
        kwargs["aws_region"] = effective_region
    return kwargs
