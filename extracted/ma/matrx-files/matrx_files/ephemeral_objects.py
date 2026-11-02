"""Named lifecycle policies for row-less ephemeral storage objects."""

from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Sequence
from urllib.parse import urlencode


EPHEMERAL_LIFECYCLE_TAG_KEY = "matrx-ephemeral-kind"


@dataclass(frozen=True, slots=True)
class EphemeralObjectPolicy:
    """Storage and lifecycle contract for one class of row-less scratch object."""

    name: str
    tag_value: str
    expiration_days: int
    lifecycle_rule_id: str

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("ephemeral policy name must not be empty")
        if not self.tag_value.strip():
            raise ValueError("ephemeral policy tag_value must not be empty")
        if self.expiration_days < 1:
            raise ValueError("ephemeral policy expiration_days must be at least 1")
        if not self.lifecycle_rule_id.strip():
            raise ValueError("ephemeral policy lifecycle_rule_id must not be empty")

    @property
    def object_tags(self) -> dict[str, str]:
        """Exact tag set stamped atomically whenever this scratch object is written."""
        return {EPHEMERAL_LIFECYCLE_TAG_KEY: self.tag_value}

    @property
    def s3_tagging_query(self) -> str:
        """URL-encoded tag set accepted by S3 PutObject and multipart initiation."""
        return urlencode(sorted(self.object_tags.items()))

    def s3_lifecycle_rule(self) -> dict[str, object]:
        """Return the tag-scoped S3 lifecycle rule for this policy."""
        return {
            "ID": self.lifecycle_rule_id,
            "Filter": {
                "Tag": {
                    "Key": EPHEMERAL_LIFECYCLE_TAG_KEY,
                    "Value": self.tag_value,
                }
            },
            "Status": "Enabled",
            "Expiration": {"Days": self.expiration_days},
        }


PREVIEW_RENDER_POLICY = EphemeralObjectPolicy(
    name="preview_render",
    tag_value="preview-render",
    expiration_days=1,
    lifecycle_rule_id="matrx-expire-preview-render-scratch",
)

EPHEMERAL_OBJECT_POLICIES: tuple[EphemeralObjectPolicy, ...] = (
    PREVIEW_RENDER_POLICY,
)


def validate_ephemeral_object_policies(
    policies: Sequence[EphemeralObjectPolicy],
) -> None:
    """Reject identifiers whose collision would merge unrelated retention classes."""
    for attribute in ("name", "tag_value", "lifecycle_rule_id"):
        values = [getattr(policy, attribute) for policy in policies]
        duplicates = sorted({value for value in values if values.count(value) > 1})
        if duplicates:
            raise ValueError(
                f"ephemeral object policies have duplicate {attribute}: {duplicates}"
            )


validate_ephemeral_object_policies(EPHEMERAL_OBJECT_POLICIES)


def get_ephemeral_object_policy(name: str) -> EphemeralObjectPolicy:
    """Resolve a registered ephemeral-object policy by its stable name."""
    for policy in EPHEMERAL_OBJECT_POLICIES:
        if policy.name == name:
            return policy
    known = ", ".join(policy.name for policy in EPHEMERAL_OBJECT_POLICIES)
    raise KeyError(f"unknown ephemeral object policy {name!r}; registered policies: {known}")


def require_registered_ephemeral_object_policy(
    policy: EphemeralObjectPolicy,
) -> None:
    """Reject ad hoc or stale policies whose lifecycle rule is not owned here."""
    try:
        registered = get_ephemeral_object_policy(policy.name)
    except KeyError as exc:
        raise ValueError(
            f"ephemeral object policy {policy.name!r} is not registered; "
            "add it to EPHEMERAL_OBJECT_POLICIES before writing objects"
        ) from exc
    if registered != policy:
        raise ValueError(
            f"ephemeral object policy {policy.name!r} differs from the registered policy"
        )


def s3_ephemeral_lifecycle_rules() -> list[dict[str, object]]:
    """Build all tag-scoped S3 rules owned by the ephemeral-object registry."""
    return [policy.s3_lifecycle_rule() for policy in EPHEMERAL_OBJECT_POLICIES]
