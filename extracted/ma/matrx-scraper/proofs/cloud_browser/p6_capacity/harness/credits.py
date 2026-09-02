"""Burstable-host CPU credit sampling. Phase-0 proof harness (NOT shipped code).

PLAN.md: "Run steady-state tests long enough to expose T3 CPU-credit behavior,
including a minimum six-hour soak on burstable hosts, and record credit balance
alongside CPU."

Credit balance is NOT readable from inside the instance. There is no /proc for it and no
IMDS field for it -- it exists only as the CloudWatch metric `CPUCreditBalance` in the
`AWS/EC2` namespace. So this module has exactly two honest modes:

  source="cloudwatch"  the aws CLI is present, credentialed, and the host is a
                       burstable instance -> the real balance, sampled per step.
  source="steal_proxy" no CloudWatch reach -> we record /proc/stat steal% instead and
                       label it a PROXY. Sustained non-zero steal on a t-family host
                       means credits are exhausted and the instance is being throttled.
                       That is evidence of throttling; it is NOT a credit balance, and
                       the report must not print it as one.

Never invent a balance. A missing balance is reported as null with a reason.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import urllib.error
import urllib.request
from datetime import UTC, datetime, timedelta

BURSTABLE_PREFIXES = ("t2.", "t3.", "t3a.", "t4g.")
_IMDS = "http://169.254.169.254/latest"


def _imds(path: str, token: str | None, timeout: float = 0.7) -> str | None:
    req = urllib.request.Request(f"{_IMDS}{path}")
    if token:
        req.add_header("X-aws-ec2-metadata-token", token)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode().strip()
    except (urllib.error.URLError, OSError, ValueError):
        return None


def imds_identity(timeout: float = 0.7) -> dict[str, str | None]:
    """Best-effort EC2 identity. All-None off EC2 (a VPS, a laptop, this container)."""
    token = None
    try:
        req = urllib.request.Request(
            f"{_IMDS}/api/token",
            method="PUT",
            headers={"X-aws-ec2-metadata-token-ttl-seconds": "60"},
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            token = resp.read().decode().strip()
    except (urllib.error.URLError, OSError, ValueError):
        token = None
    return {
        "instance_id": _imds("/meta-data/instance-id", token, timeout),
        "instance_type": _imds("/meta-data/instance-type", token, timeout),
        "availability_zone": _imds("/meta-data/placement/availability-zone", token, timeout),
    }


def is_burstable(instance_type: str | None) -> bool:
    return bool(instance_type) and instance_type.startswith(BURSTABLE_PREFIXES)


class CreditProbe:
    """Resolve once, then `.sample()` per step."""

    def __init__(self, force_burstable: bool = False, imds_timeout: float = 0.7) -> None:
        self.identity = imds_identity(imds_timeout)
        self.instance_type = self.identity.get("instance_type")
        self.burstable = force_burstable or is_burstable(self.instance_type)
        self.region = None
        az = self.identity.get("availability_zone")
        if az:
            self.region = az[:-1]
        self.source = "unavailable"
        self.reason: str | None = None
        if not self.burstable:
            self.reason = (
                "host is not a detected burstable instance "
                f"(instance_type={self.instance_type!r}); credit balance does not apply"
            )
        elif not shutil.which("aws"):
            self.source = "steal_proxy"
            self.reason = "aws CLI not on PATH; recording steal%% as a throttling PROXY only"
        elif not self.identity.get("instance_id"):
            self.source = "steal_proxy"
            self.reason = "no IMDS instance-id; recording steal%% as a throttling PROXY only"
        else:
            self.source = "cloudwatch"

    def sample(self) -> dict[str, object]:
        out: dict[str, object] = {
            "burstable": self.burstable,
            "instance_type": self.instance_type,
            "source": self.source,
            "reason": self.reason,
            "cpu_credit_balance": None,
            "cpu_surplus_credit_balance": None,
        }
        if self.source != "cloudwatch":
            return out
        for metric, key in (
            ("CPUCreditBalance", "cpu_credit_balance"),
            ("CPUSurplusCreditBalance", "cpu_surplus_credit_balance"),
        ):
            value = self._cloudwatch(metric)
            out[key] = value
        if out["cpu_credit_balance"] is None and out["reason"] is None:
            out["reason"] = "aws cloudwatch call returned no datapoint (IAM or metric lag)"
        return out

    def _cloudwatch(self, metric: str) -> float | None:
        # The AWS CLI expects ISO-8601 timestamps here.  Strings such as
        # ``-30 minutes`` and ``now`` look convenient but are rejected by the
        # CLI before CloudWatch is called.
        end = datetime.now(UTC)
        start = end - timedelta(minutes=30)
        cmd = [
            "aws",
            "cloudwatch",
            "get-metric-statistics",
            "--namespace",
            "AWS/EC2",
            "--metric-name",
            metric,
            "--dimensions",
            f"Name=InstanceId,Value={self.identity['instance_id']}",
            "--period",
            "300",
            "--statistics",
            "Average",
            "--start-time",
            start.isoformat(),
            "--end-time",
            end.isoformat(),
            "--output",
            "json",
        ]
        if self.region:
            cmd += ["--region", self.region]
        try:
            raw = subprocess.run(cmd, capture_output=True, text=True, timeout=25)
        except (OSError, subprocess.SubprocessError):
            return None
        if raw.returncode != 0:
            return None
        try:
            points = json.loads(raw.stdout).get("Datapoints", [])
        except json.JSONDecodeError:
            return None
        if not points:
            return None
        points.sort(key=lambda p: p.get("Timestamp", ""))
        return float(points[-1].get("Average"))
