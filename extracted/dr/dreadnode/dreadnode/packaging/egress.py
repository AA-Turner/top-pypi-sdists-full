"""Author-side egress target grammar (WP1-93).

Mirrors the platform's ``app.sandboxes.egress`` target grammar so author-side
validation predicts platform ingest, the way ``task_validation`` already mirrors
``model_roles.normalize_models`` for ``models`` (ENG-7241).

The mirror is deliberate duplication, not a shared package: the SDK ships to
users and cannot import the API. What it buys is that
``specs/tasks/contract.md``'s Validation Severities table stays true — an
``error`` is rejected on both sides, so ``dn task validate`` predicts ingest.
The SDK<->API parity suite (``specs/tasks/validation-parity/``) runs the same
fixtures through both validators and fails CI if the two drift.

Only the *grammar* lives here (``TSK-EGR-002``). Whether a target is reachable
is a property of the deployment's egress floor, and a task published on one
deployment may be run on another, so that check belongs at provision
(``TSK-EGR-005``) and is not something the SDK can predict.

This module is also the grammar behind the runner-facing ``--egress`` flags on
``dn evaluation create`` and ``dn runtime create``: a target means the same
thing wherever it is written (``TSK-EGR-007``, ``RT-SBX-006``).
"""

import ipaddress
import re
import typing as t

# Mirrors the platform's ``MAX_EGRESS_TARGETS``.
MAX_EGRESS_TARGETS = 50

# Domain labels: alphanumeric, internal hyphens allowed. A domain target must
# carry at least one dot -- a single-label name is not an FQDN, and under the
# cluster's ``ndots:5`` a client resolving one queries the search-suffixed form
# first, so a short-name rule never matches the query actually made.
_LABEL = r"[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?"
_DOMAIN_RE = re.compile(rf"^{_LABEL}(?:\.{_LABEL})+$")


class EgressTargetError(ValueError):
    """A target that is not a well-formed FQDN, wildcard, IP, or CIDR."""


def _try_parse_ip(value: str) -> object | None:
    try:
        return ipaddress.ip_address(value)
    except ValueError:
        return None


def _looks_like_cidr(value: str) -> bool:
    """Whether a slashed target is aiming at a CIDR, however badly.

    Deliberately loose: ``1.2.3.4/x`` should be told it is a malformed CIDR,
    not that it looks like a URL.
    """
    head, _, tail = value.partition("/")
    return bool(tail) and _try_parse_ip(head) is not None


def validate_target(value: t.Any, *, where: str = "egress target") -> str:
    """Validate and canonicalize one target. Raises ``EgressTargetError``.

    Canonicalization is lowercase for names and ``ip_network`` normal form for
    addresses, so two spellings of one destination compare equal.
    """
    if not isinstance(value, str):
        raise EgressTargetError(f"{where} must be a string")
    stripped = value.strip()
    if not stripped:
        raise EgressTargetError(f"{where} must be a non-empty target")
    if any(ch.isspace() for ch in stripped):
        raise EgressTargetError(f"{where} {value!r} must not contain whitespace")

    # Catch the shapes people reach for that are not targets, before the
    # grammar rejects them with a less useful message.
    if "://" in stripped or ("/" in stripped and not _looks_like_cidr(stripped)):
        raise EgressTargetError(f"{where} {value!r} must be a bare host, not a URL or path")
    if stripped == "*":
        raise EgressTargetError(
            f"{where} may not be a bare '*'. It requests the floor's own "
            "default rather than declaring a scope, and the enforcement "
            "backend matches it against nothing."
        )

    lowered = stripped.lower()

    if lowered.startswith("*."):
        base = lowered[2:]
        if not _DOMAIN_RE.fullmatch(base):
            raise EgressTargetError(f"{where} {value!r} must be '*.' followed by a dotted domain")
        return lowered

    # A bare address keeps its bare spelling. It is exactly a /32 or /128, but
    # an error that quotes back something the author did not write costs more
    # than the uniformity is worth.
    bare_address = _try_parse_ip(lowered)
    if bare_address is not None:
        return str(bare_address)

    if "/" in lowered:
        head, _, bits = lowered.partition("/")
        if _try_parse_ip(head) is None or not bits.isdigit():
            raise EgressTargetError(
                f"{where} {value!r} is not a valid CIDR: expected <address>/<prefix length>"
            )
        try:
            # strict: a CIDR carrying host bits is ambiguous, and masking it
            # quietly hands back a different range than the one written.
            return str(ipaddress.ip_network(lowered, strict=True))
        except ValueError as exc:
            raise EgressTargetError(f"{where} {value!r} is not a valid CIDR: {exc}") from exc

    if _DOMAIN_RE.fullmatch(lowered):
        return lowered

    raise EgressTargetError(
        f"{where} {value!r} must be a dotted FQDN, a '*.suffix' wildcard, an IP address, or a CIDR"
    )


def validate_target_list(raw: t.Any, *, where: str) -> list[str]:
    """Validate a list of targets, deduped, order preserved."""
    if raw is None:
        return []
    if isinstance(raw, str) or not isinstance(raw, (list, tuple)):
        raise EgressTargetError(f"{where} must be a list of targets")

    out: list[str] = []
    for entry in raw:
        target = validate_target(entry, where=f"{where} entry")
        if target not in out:
            out.append(target)
    if len(out) > MAX_EGRESS_TARGETS:
        raise EgressTargetError(f"{where} may declare at most {MAX_EGRESS_TARGETS} targets")
    return out


def normalize_declaration(raw: t.Any) -> list[str] | None:
    """Parse ``task.yaml``'s ``egress:`` block into a canonical allow list.

    Returns ``None`` when no ``egress`` key is present and ``[]`` when one is
    present but empty -- the two differ, and the difference flips the effective
    default action (``TSK-EGR-003``).
    """
    if raw is None:
        return None
    if isinstance(raw, list):
        raise EgressTargetError("egress must be an object with an 'allow' list, not a bare list")
    if not isinstance(raw, dict):
        raise EgressTargetError("egress must be an object with an 'allow' list")

    unknown = sorted(set(raw) - {"allow"})
    if unknown:
        # There is no ``deny`` key by design: a task's deny is either redundant
        # with the floor or expressible by omission, since declaring anything
        # flips the default to deny (``TSK-EGR-001``).
        hint = (
            " There is no 'deny' key: declaring an allow list already excludes "
            "everything it does not name."
            if "deny" in unknown
            else ""
        )
        raise EgressTargetError(f"egress has unknown key(s): {', '.join(unknown)}.{hint}")

    if "allow" not in raw:
        raise EgressTargetError("egress must declare an 'allow' list")

    return validate_target_list(raw["allow"], where="egress.allow")


def merge_targets(
    existing: t.Sequence[str] | None,
    extra: t.Sequence[str] | None,
) -> list[str] | None:
    """Union CLI-supplied targets onto any loaded from a manifest.

    A ``--egress`` flag adds to an ``egress_overrides`` (or
    ``sandbox.egress.allow``) block loaded from ``--file`` rather than replacing
    it, mirroring how ``--env-model`` merges per role instead of replacing the
    whole ``model_overrides`` block.

    Returns ``None`` when neither source declared anything, which is distinct
    from an empty list: absent inherits the operator's floor, while an empty
    declaration restricts the sandbox to the platform destinations derived for
    it (``TSK-EGR-003``, ``RT-SBX-009``).
    """
    if existing is None and extra is None:
        return None
    merged: list[str] = list(existing or [])
    for target in extra or []:
        if target not in merged:
            merged.append(target)
    return merged
