"""Rank EC2 instance types for SPOT use by interruption frequency.

    pysae-ai-tools aws spot-advisor --region eu-west-3 --cpu 4 --ram 32
    pysae-ai-tools aws spot-advisor -r "Europe/Paris" --cpu 4 --ram 16 --json

Uses AWS's public **Spot Instance Advisor** dataset
(``https://spot-bid-advisor.s3.amazonaws.com/spot-advisor-data.json``, no
credentials needed). For a region and an exact sizing (vCPU + RAM), it lists
every matching instance type with its published spot interruption frequency
(``<5%`` … ``>20%``) and savings vs on-demand, ranked most-reliable first.

The goal is **spot pool diversification**: feed a managed node group several
low-interruption types of the *same shape* so AWS's ``capacity-optimized``
allocation always has a healthy pool to fall back on, instead of churning when
one or two pools tighten. The ``--json`` output is the list of recommended
types, ready to paste into a Terraform ``instance_types`` argument.

Burstable (``t*``) and accelerated/GPU families (``g/p/inf/trn/dl/vt/f``) are
excluded by default — they are rarely the right fit for a homogeneous,
sustained-load node group. Use ``--family`` to whitelist prefixes explicitly or
``--all-families`` to keep everything.
"""

import json
import re
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from tempfile import gettempdir
from typing import Annotated, Any

import typer

SPOT_ADVISOR_URL = "https://spot-bid-advisor.s3.amazonaws.com/spot-advisor-data.json"
_CACHE_PATH = Path(gettempdir()) / "pysae-spot-advisor-data.json"
_CACHE_TTL_SECONDS = 6 * 3600

# Human-friendly region aliases → AWS region codes. Unknown values pass through
# unchanged (assumed to already be a region code like ``us-east-2``).
REGION_ALIASES: dict[str, str] = {
    "europe/paris": "eu-west-3",
    "paris": "eu-west-3",
    "europe/ireland": "eu-west-1",
    "ireland": "eu-west-1",
    "dublin": "eu-west-1",
    "europe/london": "eu-west-2",
    "london": "eu-west-2",
    "europe/frankfurt": "eu-central-1",
    "frankfurt": "eu-central-1",
    "europe/zurich": "eu-central-2",
    "zurich": "eu-central-2",
    "europe/stockholm": "eu-north-1",
    "stockholm": "eu-north-1",
    "europe/milan": "eu-south-1",
    "milan": "eu-south-1",
    "europe/spain": "eu-south-2",
    "spain": "eu-south-2",
    "us/virginia": "us-east-1",
    "virginia": "us-east-1",
    "us/ohio": "us-east-2",
    "ohio": "us-east-2",
    "us/oregon": "us-west-2",
    "oregon": "us-west-2",
}

# Families excluded by default (prefix match on the part before the size).
_BURSTABLE_PREFIXES = ("t",)
_ACCELERATED_PREFIXES = ("g", "p", "inf", "trn", "dl", "vt", "f", "gr")

# Interruption rate index (the dataset's ``r`` field) → display label + emoji.
_RATE_LABEL = {0: "<5%", 1: "5-10%", 2: "10-15%", 3: "15-20%", 4: ">20%"}
_RATE_EMOJI = {0: "✅", 1: "🟡", 2: "🟠", 3: "🟠", 4: "❌"}
# --max-interruption value (percent) → worst acceptable rate index.
_MAX_INTERRUPTION_TO_INDEX = {5: 0, 10: 1, 15: 2, 20: 3, 100: 4}


@dataclass
class InstanceAdvice:
    """One instance type's spot profile for a region/OS and a target sizing."""

    instance_type: str
    cores: int
    ram_gb: float
    rate_index: int
    savings_pct: int

    @property
    def family(self) -> str:
        """The family prefix, e.g. ``r7i`` for ``r7i.xlarge``."""
        return self.instance_type.split(".", 1)[0]

    @property
    def rate_label(self) -> str:
        return _RATE_LABEL.get(self.rate_index, "?")

    @property
    def rate_emoji(self) -> str:
        return _RATE_EMOJI.get(self.rate_index, "?")


def resolve_region(region: str) -> str:
    """Map a region alias (e.g. ``Europe/Paris``) to its AWS code, else pass through."""
    return REGION_ALIASES.get(region.strip().lower(), region.strip())


def is_arm64(instance_type: str) -> bool:
    """True when the family is AWS Graviton (arm64).

    EC2 marks Graviton with a ``g`` immediately after the generation number
    (``m7g``, ``c7gn``, ``r6gd``, ``t4g``, ``x2gd``…). A ``g`` that *leads* the
    family (``g4dn`` GPU) is not the arch marker, so we look only after the
    generation digits.
    """
    family = instance_type.split(".", 1)[0]
    match = re.match(r"^[a-z]+(\d+)(.*)$", family)
    if not match:
        return False
    return bool(match.group(2).startswith("g"))


def _letter_prefix(instance_type: str) -> str:
    """Leading alphabetic part of the family, e.g. ``inf`` for ``inf2.xlarge``."""
    family = instance_type.split(".", 1)[0]
    letters = ""
    for ch in family:
        if ch.isalpha():
            letters += ch
        else:
            break
    return letters


def is_excluded_family(instance_type: str, allowed_prefixes: list[str], all_families: bool) -> bool:
    """Decide whether ``instance_type`` is filtered out.

    With ``allowed_prefixes`` set, only types whose family starts with one of
    them survive. Otherwise, burstable, flex and accelerated families are dropped
    unless ``all_families`` is set.
    """
    family = instance_type.split(".", 1)[0]
    if allowed_prefixes:
        return not any(family.startswith(p) for p in allowed_prefixes)
    if all_families:
        return False
    if "-flex" in family:  # CPU-throttled under sustained load, like burstable
        return True
    letters = _letter_prefix(instance_type)
    return letters in _BURSTABLE_PREFIXES or letters in _ACCELERATED_PREFIXES


def is_accelerated_family(instance_type: str) -> bool:
    """True for GPU/accelerated families (``g/p/inf/trn/dl/vt/f/gr``).

    These are never a meaningful substitute for a general-purpose CPU node group
    (you would pay for an accelerator you do not use), so they are dropped from
    the compatible field entirely rather than just flagged.
    """
    return _letter_prefix(instance_type) in _ACCELERATED_PREFIXES


def _load_json(text: str) -> dict[str, Any]:
    data: dict[str, Any] = json.loads(text)
    return data


def load_dataset(timeout: int = 20, *, force_refresh: bool = False) -> dict[str, Any]:
    """Return the Spot Advisor dataset, using a short-lived local cache.

    Fetches over HTTPS (no AWS credentials). On a network failure, falls back to
    a stale cache when present; otherwise raises the original error.
    """
    if not force_refresh and _CACHE_PATH.is_file():
        age = time.time() - _CACHE_PATH.stat().st_mtime
        if age < _CACHE_TTL_SECONDS:
            return _load_json(_CACHE_PATH.read_text(encoding="utf-8"))
    try:
        with urllib.request.urlopen(SPOT_ADVISOR_URL, timeout=timeout) as resp:  # noqa: S310 (trusted AWS URL)
            raw = resp.read().decode("utf-8")
    except (urllib.error.URLError, TimeoutError) as exc:
        if _CACHE_PATH.is_file():
            return _load_json(_CACHE_PATH.read_text(encoding="utf-8"))
        raise RuntimeError(f"could not fetch the Spot Advisor dataset and no cache is available: {exc}") from exc
    try:
        _CACHE_PATH.write_text(raw, encoding="utf-8")
    except OSError:
        pass  # cache is best-effort
    return _load_json(raw)


def advise(
    dataset: dict[str, Any],
    region: str,
    cpu: int,
    ram: int,
    *,
    os_name: str = "Linux",
    allowed_prefixes: list[str] | None = None,
    all_families: bool = False,
    arch: str = "x86_64",
) -> list[InstanceAdvice]:
    """Return matching instance types ranked by reliability then savings.

    A type qualifies when it has exactly ``cpu`` cores, ``ram`` GiB (rounded),
    spot data for ``region``/``os_name``, the requested ``arch``
    (``x86_64``/``arm64`` — Graviton is filtered out for x86 to avoid proposing
    instances that can't run an x86 image), and is not filtered out by family.
    Sorted by interruption rate (ascending) then savings (descending).
    """
    instance_types: dict[str, dict[str, Any]] = dataset.get("instance_types", {})
    region_data = dataset.get("spot_advisor", {}).get(region, {}).get(os_name, {})
    allowed = allowed_prefixes or []

    out: list[InstanceAdvice] = []
    for itype, spot in region_data.items():
        spec = instance_types.get(itype)
        if not spec:
            continue
        if spec.get("cores") != cpu or round(float(spec.get("ram_gb", 0))) != ram:
            continue
        if is_arm64(itype) != (arch == "arm64"):
            continue
        if is_excluded_family(itype, allowed, all_families):
            continue
        out.append(
            InstanceAdvice(
                instance_type=itype,
                cores=int(spec["cores"]),
                ram_gb=float(spec["ram_gb"]),
                rate_index=int(spot.get("r", 4)),
                savings_pct=int(spot.get("s", 0)),
            )
        )
    out.sort(key=lambda a: (a.rate_index, -a.savings_pct, a.instance_type))
    return out


def _render_table(items: list[InstanceAdvice], recommended: set[str]) -> None:
    """Print an aligned, emoji-annotated table to stdout."""
    type_w = max((len(a.instance_type) for a in items), default=10)
    header = f"  {'Instance':<{type_w}}  {'vCPU':>4}  {'RAM':>7}  {'Interruption':<16}  {'Savings':>8}  Reco"
    typer.secho(header, bold=True)
    typer.echo("  " + "─" * (len(header) - 2))
    for a in items:
        star = "★" if a.instance_type in recommended else ""
        rate = f"{a.rate_emoji} {a.rate_label}"
        row = (
            f"  {a.instance_type:<{type_w}}  {a.cores:>4}  {a.ram_gb:>5.0f}Gi  "
            f"{rate:<16}  {'−' + str(a.savings_pct) + '%':>8}  {star}"
        )
        color = (
            typer.colors.GREEN
            if a.rate_index == 0
            else typer.colors.YELLOW if a.rate_index in (1, 2, 3) else typer.colors.RED
        )
        typer.secho(row, fg=color if a.instance_type in recommended else None)


def main(
    cpu: Annotated[int, typer.Option("--cpu", help="Exact vCPU count to match (e.g. 4).")],
    ram: Annotated[int, typer.Option("--ram", help="Exact RAM in GiB to match (e.g. 32).")],
    region: Annotated[
        str,
        typer.Option("--region", "-r", help="AWS region code or alias (default eu-west-3)."),
    ] = "eu-west-3",
    os_name: Annotated[
        str,
        typer.Option("--os", help="Operating system: Linux or Windows."),
    ] = "Linux",
    family: Annotated[
        list[str] | None,
        typer.Option("--family", help="Only keep these family prefixes (repeatable, e.g. --family r --family m)."),
    ] = None,
    all_families: Annotated[
        bool,
        typer.Option("--all-families", help="Include burstable (t*) and accelerated/GPU families too."),
    ] = False,
    arch: Annotated[
        str,
        typer.Option("--arch", help="CPU architecture: x86_64 (default) or arm64 (Graviton)."),
    ] = "x86_64",
    max_interruption: Annotated[
        int,
        typer.Option(
            "--max-interruption",
            help="Worst interruption bucket allowed in the recommended set: 5, 10, 15, 20, or 100 (%).",
        ),
    ] = 5,
    as_json: Annotated[
        bool,
        typer.Option("--json", help="Emit only the recommended instance_types as a JSON array (for Terraform)."),
    ] = False,
    refresh: Annotated[
        bool,
        typer.Option("--refresh", help="Bypass the local cache and re-download the dataset."),
    ] = False,
) -> None:
    """Rank EC2 instance types for SPOT use by interruption frequency."""
    if max_interruption not in _MAX_INTERRUPTION_TO_INDEX:
        typer.secho(
            f"✗ --max-interruption must be one of {sorted(_MAX_INTERRUPTION_TO_INDEX)} (got {max_interruption}).",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(code=1)
    if os_name not in ("Linux", "Windows"):
        typer.secho(f"✗ --os must be 'Linux' or 'Windows' (got {os_name!r}).", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)
    if arch not in ("x86_64", "arm64"):
        typer.secho(f"✗ --arch must be 'x86_64' or 'arm64' (got {arch!r}).", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)

    resolved = resolve_region(region)
    try:
        dataset = load_dataset(force_refresh=refresh)
    except RuntimeError as exc:
        typer.secho(f"✗ {exc}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc

    if resolved not in dataset.get("spot_advisor", {}):
        available = ", ".join(sorted(dataset.get("spot_advisor", {})))
        typer.secho(
            f"✗ No spot data for region {resolved!r} (from {region!r}). Available regions: {available}",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(code=1)

    items = advise(
        dataset,
        resolved,
        cpu,
        ram,
        os_name=os_name,
        allowed_prefixes=family,
        all_families=all_families,
        arch=arch,
    )
    max_index = _MAX_INTERRUPTION_TO_INDEX[max_interruption]
    recommended = [a for a in items if a.rate_index <= max_index]
    recommended_types = [a.instance_type for a in recommended]

    if as_json:
        sys.stdout.write(json.dumps(recommended_types, indent=2))
        sys.stdout.write("\n")
        return

    if not items:
        typer.secho(
            f"No instance type matches {cpu} vCPU / {ram} GiB in {resolved} ({os_name}) with the current filters. "
            f"Try --all-families or a different sizing.",
            fg=typer.colors.YELLOW,
        )
        raise typer.Exit(code=0)

    alias_note = f" ({region})" if resolve_region(region) != region.strip() else ""
    typer.secho(
        f"\nSpot Instance Advisor — {resolved}{alias_note} · {os_name} · {cpu} vCPU / {ram} GiB\n",
        bold=True,
    )
    _render_table(items, set(recommended_types))

    typer.echo()
    if recommended_types:
        typer.secho(
            f"✓ {len(recommended_types)} type(s) at ≤{_RATE_LABEL[max_index]} interruption "
            f"→ diversify the node group across all of them (more pools = fewer preemptions).",
            fg=typer.colors.GREEN,
        )
        typer.echo("\nTerraform-ready instance_types (copy/paste):\n")
        typer.echo(json.dumps(recommended_types, indent=2))
    else:
        typer.secho(
            f"⚠ No type meets the ≤{max_interruption}% interruption bar — "
            f"relax --max-interruption or reconsider the sizing/region.",
            fg=typer.colors.YELLOW,
        )
