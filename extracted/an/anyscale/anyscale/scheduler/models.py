from dataclasses import dataclass, field, fields
from datetime import datetime
from decimal import Decimal
import math
from typing import (
    Any,
    ClassVar,
    Dict,
    get_args,
    get_origin,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
)

from anyscale._private.models import ModelBase, ModelEnum


# Quota values are fractional but capped at this many decimal places.
_MAX_QUOTA_DECIMAL_PLACES = 3

# Resource axes the scheduler understands; covered_resources must use these.
_ALLOWED_RESOURCE_NAMES = frozenset({"cpu", "memory_gb", "gpu", "tpu"})


# --- Enum helpers ---


def _docs_by_name_and_value(pairs):
    """Build a __docstrings__ dict keyed by both the enum name and its wire value.

    The metaclass check (`ModelEnumType.__new__`) requires every enum value to
    be a key; the docgen generator iterates `__members__` (names) and looks up
    by name. Aligning both lets enums whose name != value pass both checks.
    """
    out: Dict[str, str] = {}
    for name, value, doc in pairs:
        out[name] = doc
        out[value] = doc
    return out


def _validate_lowercase_enum(cls, value):
    """Look up an enum by its lowercase wire value rather than the upper-case name.

    The parent `ModelEnum.validate()` uppercases the input and looks up by name
    (e.g. `cls(value.upper())`), which only works when name == value. The GRS
    enums use lowercase wire values for backend compatibility, so we look up
    by value directly.
    """
    if isinstance(value, cls):
        return value
    if isinstance(value, str):
        try:
            return cls(value)
        except ValueError:
            pass
    allowed = [m.value for m in cls]
    raise ValueError(f"'{value}' is not a valid {cls.__name__}. Allowed: {allowed}.")


# --- Enums ---
#
# Wire values mirror the openapi_client and backend pydantic enums. Drift
# between this layer and the openapi_client is guarded by
# TestEnumDriftFromGeneratedClient.


class Operator(ModelEnum):
    """Operator used in a match expression."""

    IN = "in"
    NOT_IN = "not_in"
    EXISTS = "exists"
    DOES_NOT_EXIST = "does_not_exist"

    __docstrings__: ClassVar[Dict[str, str]] = _docs_by_name_and_value(
        [
            ("IN", "in", "Key's value is in the supplied values list."),
            ("NOT_IN", "not_in", "Key's value is not in the supplied values list."),
            (
                "EXISTS",
                "exists",
                "Key is present on the request (values must be empty).",
            ),
            (
                "DOES_NOT_EXIST",
                "does_not_exist",
                "Key is absent from the request (values must be empty).",
            ),
        ]
    )

    @classmethod
    def validate(cls, value) -> "Operator":
        return _validate_lowercase_enum(cls, value)


class OnViolationAction(ModelEnum):
    """Action to take when a request priority is outside the policy's [min, max]."""

    REJECT = "reject"
    FORCE_UPDATE = "force_update"

    __docstrings__: ClassVar[Dict[str, str]] = _docs_by_name_and_value(
        [
            (
                "REJECT",
                "reject",
                "Reject the request when its priority is outside [min, max].",
            ),
            (
                "FORCE_UPDATE",
                "force_update",
                "Clamp the priority to the nearest in-range value and continue.",
            ),
        ]
    )

    @classmethod
    def validate(cls, value) -> "OnViolationAction":
        return _validate_lowercase_enum(cls, value)


class PreemptionPolicyWithinResourceQueue(ModelEnum):
    """Preemption behavior for requests within the same resource queue."""

    NEVER = "never"
    LOWER_PRIORITY = "lower_priority"

    __docstrings__: ClassVar[Dict[str, str]] = _docs_by_name_and_value(
        [
            ("NEVER", "never", "Never preempt requests within the same queue."),
            (
                "LOWER_PRIORITY",
                "lower_priority",
                "Preempt strictly lower-priority requests in the same queue.",
            ),
        ]
    )

    @classmethod
    def validate(cls, value) -> "PreemptionPolicyWithinResourceQueue":
        return _validate_lowercase_enum(cls, value)


class PreemptionPolicyReclaimWithinCohort(ModelEnum):
    """Whether this queue may evict workloads on cohort peers that are borrowing its quota."""

    NEVER = "never"
    LOWER_PRIORITY = "lower_priority"
    ANY = "any"

    __docstrings__: ClassVar[Dict[str, str]] = _docs_by_name_and_value(
        [
            ("NEVER", "never", "Never reclaim; wait for borrowers to finish."),
            (
                "LOWER_PRIORITY",
                "lower_priority",
                "Reclaim by preempting strictly lower-priority borrowers on peer queues.",
            ),
            (
                "ANY",
                "any",
                "Reclaim by preempting borrowers on peer queues regardless of priority.",
            ),
        ]
    )

    @classmethod
    def validate(cls, value) -> "PreemptionPolicyReclaimWithinCohort":
        return _validate_lowercase_enum(cls, value)


class PreemptionPolicyBorrowWithinCohort(ModelEnum):
    """Whether this queue may evict workloads on cohort peers in order to borrow."""

    NEVER = "never"
    LOWER_PRIORITY = "lower_priority"

    __docstrings__: ClassVar[Dict[str, str]] = _docs_by_name_and_value(
        [
            ("NEVER", "never", "Only borrow quota that is idle; never preempt to borrow."),
            (
                "LOWER_PRIORITY",
                "lower_priority",
                "Preempt strictly lower-priority workloads on peer queues to borrow their quota.",
            ),
        ]
    )

    @classmethod
    def validate(cls, value) -> "PreemptionPolicyBorrowWithinCohort":
        return _validate_lowercase_enum(cls, value)


# --- Shared helpers ---


def _validate_non_negative_int(name: str, value: Optional[int]):
    if value is not None:
        if not isinstance(value, int) or isinstance(value, bool):
            raise TypeError(f"'{name}' must be an integer.")
        if value < 0:
            raise ValueError(f"'{name}' must be >= 0.")


def _validate_non_negative_quota(name: str, value: Optional[float]):
    """Non-negative number with at most _MAX_QUOTA_DECIMAL_PLACES decimals; rejects bool."""
    if value is None:
        return
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise TypeError(f"'{name}' must be a number.")
    if not math.isfinite(value):
        raise ValueError(f"'{name}' must be a finite number.")
    if value < 0:
        raise ValueError(f"'{name}' must be >= 0.")
    # For finite values .exponent is an int (= -decimal_places).
    exponent = Decimal(str(value)).as_tuple().exponent
    if isinstance(exponent, int) and -exponent > _MAX_QUOTA_DECIMAL_PLACES:
        raise ValueError(f"'{name}' supports at most {_MAX_QUOTA_DECIMAL_PLACES} decimal places.")


def _coerce_list(name: str, value, item_cls):
    """Validate a list and return a new list with dict items coerced to item_cls."""
    if value is None:
        return None
    if not isinstance(value, list):
        raise TypeError(f"'{name}' must be a list.")
    result = []
    for item in value:
        if isinstance(item, dict):
            result.append(item_cls.from_dict(item))
        elif isinstance(item, item_cls):
            result.append(item)
        else:
            raise TypeError(f"'{name}' entries must be {item_cls.__name__} or dict.")
    return result


def _filter_known(cls, d: Dict[str, Any]) -> Dict[str, Any]:
    """Keep only keys that match a declared field on cls.

    Used by `from_api_dict` to tolerate backend schema fields that aren't
    part of our V1 user-facing surface. `from_dict` stays strict for user
    input so YAML typos still error loudly.
    """
    known = {f.name for f in fields(cls)}
    return {k: v for k, v in d.items() if k in known}


# --- Match expressions ---


@dataclass(frozen=True)
class MatchExpression(ModelBase):
    """A structured label-match used in scheduling-rule and flavor selectors."""

    __doc_py_example__ = """\
from anyscale.scheduler.models import MatchExpression, Operator

expr = MatchExpression(key="team", operator=Operator.IN, values=["research", "ml"])
"""

    key: str = field(metadata={"docstring": "Label key to match against."})

    def _validate_key(self, key: str):
        if not isinstance(key, str) or not key.strip():
            raise ValueError("'key' must be a non-empty string.")

    operator: Operator = field(
        metadata={"docstring": "Match operator: 'in', 'not_in', 'exists', or 'does_not_exist'."}
    )

    def _validate_operator(self, operator: Operator) -> Operator:
        return Operator.validate(operator)

    values: Optional[List[str]] = field(
        default=None,
        metadata={
            "docstring": "Values for 'in'/'not_in' (must be non-empty). Must be empty or omitted for 'exists'/'does_not_exist'."
        },
    )

    def _validate_values(self, values: Optional[List[str]]):
        if values is not None and (
            not isinstance(values, list) or not all(isinstance(v, str) for v in values)
        ):
            raise TypeError("'values' must be a list of strings.")
        # Operator runs before values in declaration order, so self.operator is
        # already coerced to an Operator instance at this point.
        op = self.operator
        has_values = bool(values)
        if op in (Operator.IN, Operator.NOT_IN) and not has_values:
            raise ValueError(f"'values' must be non-empty for operator '{op.value}'.")
        if op in (Operator.EXISTS, Operator.DOES_NOT_EXIST) and has_values:
            raise ValueError(f"'values' must be empty for operator '{op.value}'.")

    @classmethod
    def from_api_dict(cls, d: Dict[str, Any]) -> "MatchExpression":
        return cls(**_filter_known(cls, d))


# --- Nested config models ---


@dataclass(frozen=True)
class ResourceFlavor(ModelBase):
    """A named flavor with an optional match-expression selector and advanced launch overrides."""

    __doc_py_example__ = """\
from anyscale.scheduler.models import ResourceFlavor, MatchExpression, Operator

flavor = ResourceFlavor(
    name="spot",
    selector=[
        MatchExpression(key="market-type", operator=Operator.IN, values=["SPOT"]),
    ],
)
"""

    name: str = field(metadata={"docstring": "Unique name for this resource flavor."})

    def _validate_name(self, name: str):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("'name' must be a non-empty string.")

    selector: Optional[List[MatchExpression]] = field(
        default=None,
        metadata={
            "docstring": "Match expressions describing which instances satisfy this flavor."
        },
    )

    def _validate_selector(
        self, selector: Optional[List[MatchExpression]]
    ) -> Optional[List[MatchExpression]]:
        return _coerce_list("selector", selector, MatchExpression)

    advanced_instance_config: Optional[Dict[str, Any]] = field(
        default=None,
        metadata={
            "docstring": "Cloud-provider-specific advanced launch overrides for instances of this flavor."
        },
    )

    def _validate_advanced_instance_config(
        self, advanced_instance_config: Optional[Dict[str, Any]]
    ):
        if advanced_instance_config is not None and not isinstance(advanced_instance_config, dict):
            raise TypeError("'advanced_instance_config' must be a dict.")

    @classmethod
    def from_api_dict(cls, d: Dict[str, Any]) -> "ResourceFlavor":
        filtered = _filter_known(cls, d)
        sel = filtered.get("selector")
        if isinstance(sel, list):
            filtered["selector"] = [
                MatchExpression.from_api_dict(r) if isinstance(r, dict) else r for r in sel
            ]
        return cls(**filtered)


@dataclass(frozen=True)
class ResourceQuotaSpec(ModelBase):
    """Quota for a single resource (e.g. gpu, cpu) within a flavor."""

    __doc_py_example__ = """\
from anyscale.scheduler.models import ResourceQuotaSpec

quota = ResourceQuotaSpec(name="gpu", nominal_quota=64)
"""

    name: str = field(metadata={"docstring": "Resource name (e.g. 'gpu', 'cpu')."})

    def _validate_name(self, name: str):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("'name' must be a non-empty string.")

    nominal_quota: Optional[float] = field(
        default=None,
        metadata={
            "docstring": "Guaranteed capacity for this queue+flavor+resource "
            "(up to 3 decimal places). Omit for unlimited quota; an explicit 0 blocks it."
        },
    )

    def _validate_nominal_quota(self, nominal_quota: Optional[float]):
        _validate_non_negative_quota("nominal_quota", nominal_quota)

    lending_limit: Optional[float] = field(
        default=None,
        metadata={
            "docstring": "How much of the nominal quota cohort peers may borrow while this queue "
            "is not using it. Must not exceed `nominal_quota`. Omit to lend all unused "
            "nominal quota. Only valid on a queue with a `cohort_name`."
        },
    )

    def _validate_lending_limit(self, lending_limit: Optional[float]):
        _validate_non_negative_quota("lending_limit", lending_limit)
        if (
            lending_limit is not None
            and self.nominal_quota is not None
            and lending_limit > self.nominal_quota
        ):
            raise ValueError(
                f"'lending_limit' ({lending_limit}) must be <= 'nominal_quota' ({self.nominal_quota})."
            )

    borrowing_limit: Optional[float] = field(
        default=None,
        metadata={
            "docstring": "How far above the nominal quota this queue may go by borrowing unused "
            "quota from cohort peers. Omit for no limit. "
            "Only valid on a queue with a `cohort_name`."
        },
    )

    def _validate_borrowing_limit(self, borrowing_limit: Optional[float]):
        _validate_non_negative_quota("borrowing_limit", borrowing_limit)

    def has_cohort_limits(self) -> bool:
        return self.lending_limit is not None or self.borrowing_limit is not None

    @classmethod
    def from_api_dict(cls, d: Dict[str, Any]) -> "ResourceQuotaSpec":
        return cls(**_filter_known(cls, d))


@dataclass(frozen=True)
class FlavorQuota(ModelBase):
    """Per-flavor quota specs within a resource group."""

    __doc_py_example__ = """\
from anyscale.scheduler.models import FlavorQuota, ResourceQuotaSpec

flavor_quota = FlavorQuota(
    name="spot",
    resources=[ResourceQuotaSpec(name="gpu", nominal_quota=64)],
)
"""

    name: str = field(metadata={"docstring": "Name of the resource flavor this quota applies to."})

    def _validate_name(self, name: str):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("'name' must be a non-empty string.")

    resources: Optional[List[ResourceQuotaSpec]] = field(
        default=None,
        metadata={
            "docstring": "Per-resource quotas (e.g. one entry per covered resource). "
            "A covered resource omitted here (or an empty list) gets unlimited quota."
        },
    )

    def _validate_resources(
        self, resources: Optional[List[ResourceQuotaSpec]]
    ) -> Optional[List[ResourceQuotaSpec]]:
        return _coerce_list("resources", resources, ResourceQuotaSpec)

    @classmethod
    def from_api_dict(cls, d: Dict[str, Any]) -> "FlavorQuota":
        filtered = _filter_known(cls, d)
        resources = filtered.get("resources")
        if isinstance(resources, list):
            filtered["resources"] = [
                ResourceQuotaSpec.from_api_dict(r) if isinstance(r, dict) else r for r in resources
            ]
        return cls(**filtered)


@dataclass(frozen=True)
class ResourceGroup(ModelBase):
    """A group of flavors that share the same set of covered resources."""

    __doc_py_example__ = """\
from anyscale.scheduler.models import ResourceGroup, FlavorQuota, ResourceQuotaSpec

group = ResourceGroup(
    covered_resources=["gpu"],
    flavors=[
        FlavorQuota(
            name="spot",
            resources=[ResourceQuotaSpec(name="gpu", nominal_quota=64)],
        ),
    ],
)
"""

    covered_resources: List[str] = field(
        metadata={
            "docstring": "Resources covered by this group (e.g. ['gpu'] or ['cpu', 'memory_gb'])."
        }
    )

    def _validate_covered_resources(self, covered_resources: List[str]) -> List[str]:
        if (
            not isinstance(covered_resources, list)
            or not covered_resources
            or not all(isinstance(x, str) and x.strip() for x in covered_resources)
        ):
            raise ValueError("'covered_resources' must be a non-empty list of strings.")
        normalized = [x.strip() for x in covered_resources]
        if len(normalized) != len(set(normalized)):
            raise ValueError("'covered_resources' must not contain duplicates.")
        invalid = sorted(set(normalized) - _ALLOWED_RESOURCE_NAMES)
        if invalid:
            raise ValueError(
                f"'covered_resources' contains unsupported resource name(s) {invalid}; "
                f"allowed: {sorted(_ALLOWED_RESOURCE_NAMES)}."
            )
        return normalized

    flavors: List[FlavorQuota] = field(
        metadata={"docstring": "Flavor-level quotas for the resources in covered_resources."}
    )

    def _validate_flavors(self, flavors: List[FlavorQuota]) -> List[FlavorQuota]:
        if not isinstance(flavors, list) or not flavors:
            raise ValueError("'flavors' must be a non-empty list.")
        return _coerce_list("flavors", flavors, FlavorQuota)

    @classmethod
    def from_api_dict(cls, d: Dict[str, Any]) -> "ResourceGroup":
        filtered = _filter_known(cls, d)
        flavors = filtered.get("flavors")
        if isinstance(flavors, list):
            filtered["flavors"] = [
                FlavorQuota.from_api_dict(f) if isinstance(f, dict) else f for f in flavors
            ]
        return cls(**filtered)


@dataclass(frozen=True)
class PreemptionPolicy(ModelBase):
    """Preemption settings for a resource queue."""

    __doc_py_example__ = """\
from anyscale.scheduler.models import (
    PreemptionPolicy,
    PreemptionPolicyReclaimWithinCohort,
    PreemptionPolicyWithinResourceQueue,
)

policy = PreemptionPolicy(
    within_resource_queue=PreemptionPolicyWithinResourceQueue.LOWER_PRIORITY,
    reclaim_within_cohort=PreemptionPolicyReclaimWithinCohort.LOWER_PRIORITY,
)
"""

    within_resource_queue: Optional[PreemptionPolicyWithinResourceQueue] = field(
        default=None,
        metadata={
            "docstring": "Whether to preempt strictly lower-priority requests within this queue."
        },
    )

    def _validate_within_resource_queue(
        self, within_resource_queue: Optional[PreemptionPolicyWithinResourceQueue]
    ) -> Optional[PreemptionPolicyWithinResourceQueue]:
        if within_resource_queue is None:
            return None
        return PreemptionPolicyWithinResourceQueue.validate(within_resource_queue)

    reclaim_within_cohort: Optional[PreemptionPolicyReclaimWithinCohort] = field(
        default=None,
        metadata={
            "docstring": "Whether this queue may preempt workloads on cohort peers that are above "
            "their nominal quota, to take back its own nominal. Only meaningful on a queue with "
            "a `cohort_name`."
        },
    )

    def _validate_reclaim_within_cohort(
        self, reclaim_within_cohort: Optional[PreemptionPolicyReclaimWithinCohort]
    ) -> Optional[PreemptionPolicyReclaimWithinCohort]:
        if reclaim_within_cohort is None:
            return None
        return PreemptionPolicyReclaimWithinCohort.validate(reclaim_within_cohort)

    borrow_within_cohort: Optional[PreemptionPolicyBorrowWithinCohort] = field(
        default=None,
        metadata={
            "docstring": "Whether this queue may preempt lower-priority workloads on cohort peers "
            "that are above their nominal quota, in order to borrow. Requires "
            "`reclaim_within_cohort` to be `lower_priority` or `any`. Only meaningful on a "
            "queue with a `cohort_name`."
        },
    )

    def _validate_borrow_within_cohort(
        self, borrow_within_cohort: Optional[PreemptionPolicyBorrowWithinCohort]
    ) -> Optional[PreemptionPolicyBorrowWithinCohort]:
        if borrow_within_cohort is None:
            return None
        borrow = PreemptionPolicyBorrowWithinCohort.validate(borrow_within_cohort)
        if (
            borrow is not PreemptionPolicyBorrowWithinCohort.NEVER
            and self.reclaim_within_cohort
            in (
                None,
                PreemptionPolicyReclaimWithinCohort.NEVER,
            )
        ):
            raise ValueError(
                "'borrow_within_cohort' requires 'reclaim_within_cohort' to be "
                "'lower_priority' or 'any'."
            )
        return borrow

    @classmethod
    def from_api_dict(cls, d: Dict[str, Any]) -> "PreemptionPolicy":
        return cls(**_filter_known(cls, d))


@dataclass(frozen=True)
class ResourceQueue(ModelBase):
    """A queue requests are routed to. Carries optional preemption, per-flavor quotas, and an
    optional cohort for borrowing quota between queues."""

    __doc_py_example__ = """\
from anyscale.scheduler.models import ResourceQueue

queue = ResourceQueue(name="research")
"""

    name: str = field(metadata={"docstring": "Unique name for this resource queue."})

    def _validate_name(self, name: str):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("'name' must be a non-empty string.")

    preemption: Optional[PreemptionPolicy] = field(
        default=None,
        metadata={"docstring": "Preemption settings for this queue."},
    )

    def _validate_preemption(
        self, preemption: Optional[PreemptionPolicy]
    ) -> Optional[PreemptionPolicy]:
        if preemption is None:
            return None
        if isinstance(preemption, dict):
            return PreemptionPolicy.from_dict(preemption)
        if not isinstance(preemption, PreemptionPolicy):
            raise TypeError("'preemption' must be a PreemptionPolicy or dict.")
        return preemption

    resource_groups: Optional[List[ResourceGroup]] = field(
        default=None,
        metadata={
            "docstring": "Quota groups, one per set of covered resources, with per-flavor capacity."
        },
    )

    def _validate_resource_groups(
        self, resource_groups: Optional[List[ResourceGroup]]
    ) -> Optional[List[ResourceGroup]]:
        return _coerce_list("resource_groups", resource_groups, ResourceGroup)

    cohort_name: Optional[str] = field(
        default=None,
        metadata={
            "docstring": "Queues sharing a cohort_name pool their unused nominal quota: a queue "
            "at its nominal may borrow a peer's idle quota, and the peer reclaims it per its "
            "preemption policy. Requires resource_groups."
        },
    )

    def _validate_cohort_name(self, cohort_name: Optional[str]):
        if cohort_name is not None:
            if not isinstance(cohort_name, str) or not cohort_name.strip():
                raise ValueError("'cohort_name' must be a non-empty string.")
            if not self.resource_groups:
                raise ValueError(
                    f"Resource queue '{self.name}' has no resource_groups (passthrough) and "
                    "cannot declare a cohort_name."
                )
            return
        for group in self.resource_groups or []:
            for flavor in group.flavors or []:
                for spec in flavor.resources or []:
                    if spec.has_cohort_limits():
                        raise ValueError(
                            f"Resource queue '{self.name}', flavor '{flavor.name}', resource "
                            f"'{spec.name}': lending_limit and borrowing_limit require a "
                            "cohort_name on the queue."
                        )

    @classmethod
    def from_api_dict(cls, d: Dict[str, Any]) -> "ResourceQueue":
        filtered = _filter_known(cls, d)
        pre = filtered.get("preemption")
        if isinstance(pre, dict):
            filtered["preemption"] = PreemptionPolicy.from_api_dict(pre)
        groups = filtered.get("resource_groups")
        if isinstance(groups, list):
            filtered["resource_groups"] = [
                ResourceGroup.from_api_dict(g) if isinstance(g, dict) else g for g in groups
            ]
        return cls(**filtered)


@dataclass(frozen=True)
class PriorityPolicy(ModelBase):
    """Priority bounds applied to requests matched by a scheduling rule."""

    __doc_py_example__ = """\
from anyscale.scheduler.models import PriorityPolicy, OnViolationAction

policy = PriorityPolicy(default=50, min=0, max=100, on_violation=OnViolationAction.REJECT)
"""

    default: Optional[int] = field(
        default=None,
        metadata={"docstring": "Default priority assigned to matching requests."},
    )

    def _validate_default(self, default: Optional[int]):
        _validate_non_negative_int("default", default)

    min: Optional[int] = field(  # noqa: A003
        default=None,
        metadata={"docstring": "Minimum allowed priority."},
    )

    def _validate_min(self, min: Optional[int]):  # noqa: A002
        _validate_non_negative_int("min", min)

    max: Optional[int] = field(  # noqa: A003
        default=None,
        metadata={"docstring": "Maximum allowed priority."},
    )

    def _validate_max(self, max: Optional[int]):  # noqa: A002
        _validate_non_negative_int("max", max)

    on_violation: Optional[OnViolationAction] = field(
        default=None,
        metadata={
            "docstring": "Action when a request's priority is outside [min, max]: 'reject' rejects, 'force_update' clamps."
        },
    )

    def _validate_on_violation(
        self, on_violation: Optional[OnViolationAction]
    ) -> Optional[OnViolationAction]:
        if on_violation is None:
            return None
        return OnViolationAction.validate(on_violation)

    @classmethod
    def from_api_dict(cls, d: Dict[str, Any]) -> "PriorityPolicy":
        return cls(**_filter_known(cls, d))


@dataclass(frozen=True)
class SchedulingRule(ModelBase):
    """Routes incoming requests to a queue based on a structured label selector."""

    __doc_py_example__ = """\
from anyscale.scheduler.models import SchedulingRule, MatchExpression, Operator

rule = SchedulingRule(
    resource_queue="research",
    selector=[MatchExpression(key="team", operator=Operator.IN, values=["research"])],
)
"""

    resource_queue: str = field(
        metadata={"docstring": "Name of the queue requests matching this rule are routed to."}
    )

    def _validate_resource_queue(self, resource_queue: str):
        if not isinstance(resource_queue, str) or not resource_queue.strip():
            raise ValueError("'resource_queue' must be a non-empty string.")

    selector: Optional[List[MatchExpression]] = field(
        default=None,
        metadata={
            "docstring": "Match expressions evaluated against request labels. Omit to match all requests not matched by an earlier rule."
        },
    )

    def _validate_selector(
        self, selector: Optional[List[MatchExpression]]
    ) -> Optional[List[MatchExpression]]:
        return _coerce_list("selector", selector, MatchExpression)

    priority_policy: Optional[PriorityPolicy] = field(
        default=None,
        metadata={"docstring": "Priority bounds applied to requests matched by this rule."},
    )

    def _validate_priority_policy(
        self, priority_policy: Optional[PriorityPolicy]
    ) -> Optional[PriorityPolicy]:
        if priority_policy is None:
            return None
        if isinstance(priority_policy, dict):
            return PriorityPolicy.from_dict(priority_policy)
        if not isinstance(priority_policy, PriorityPolicy):
            raise TypeError("'priority_policy' must be a PriorityPolicy or dict.")
        return priority_policy

    @classmethod
    def from_api_dict(cls, d: Dict[str, Any]) -> "SchedulingRule":
        filtered = _filter_known(cls, d)
        sel = filtered.get("selector")
        if isinstance(sel, list):
            filtered["selector"] = [
                MatchExpression.from_api_dict(s) if isinstance(s, dict) else s for s in sel
            ]
        pp = filtered.get("priority_policy")
        if isinstance(pp, dict):
            filtered["priority_policy"] = PriorityPolicy.from_api_dict(pp)
        return cls(**filtered)


# --- Top-level config ---


@dataclass(frozen=True)
class SchedulerConfig(ModelBase):
    """Top-level Global Resource Scheduler config.

    A scheduler config is org-scoped. Apply to create a new active version;
    previous versions remain queryable.
    """

    __doc_py_example__ = """\
import anyscale
from anyscale.scheduler.models import SchedulerConfig

# Load from a YAML file
config = SchedulerConfig.from_yaml("scheduler-config.yaml")

# Or build programmatically
config = SchedulerConfig(
    resource_flavors=[...],
    resource_queues=[...],
    scheduling_rules=[...],
)

anyscale.scheduler.apply_config(config)
"""

    __doc_yaml_example__ = """\
resource_flavors:
  - name: spot
    selector:
      - key: market-type
        operator: in
        values: [SPOT]
resource_queues:
  - name: research
    preemption:
      within_resource_queue: lower_priority
    resource_groups:
      - covered_resources: [gpu]
        flavors:
          - name: spot
            resources:
              - name: gpu
                nominal_quota: 64
scheduling_rules:
  - resource_queue: research
    selector:
      - key: team
        operator: in
        values: [research]
    priority_policy:
      default: 50
      min: 0
      max: 100
      on_violation: reject
"""

    resource_flavors: Optional[List[ResourceFlavor]] = field(
        default=None,
        metadata={
            "docstring": "Named flavors describing which instances satisfy each flavor (via match expressions) plus optional advanced launch overrides."
        },
    )

    def _validate_resource_flavors(
        self, resource_flavors: Optional[List[ResourceFlavor]]
    ) -> Optional[List[ResourceFlavor]]:
        return _coerce_list("resource_flavors", resource_flavors, ResourceFlavor)

    resource_queues: Optional[List[ResourceQueue]] = field(
        default=None,
        metadata={
            "docstring": "Queues requests land in. Each carries optional preemption and per-flavor quotas."
        },
    )

    def _validate_resource_queues(
        self, resource_queues: Optional[List[ResourceQueue]]
    ) -> Optional[List[ResourceQueue]]:
        return _coerce_list("resource_queues", resource_queues, ResourceQueue)

    scheduling_rules: Optional[List[SchedulingRule]] = field(
        default=None,
        metadata={
            "docstring": "Rules routing incoming requests to a queue based on a structured label selector."
        },
    )

    def _validate_scheduling_rules(
        self, scheduling_rules: Optional[List[SchedulingRule]]
    ) -> Optional[List[SchedulingRule]]:
        return _coerce_list("scheduling_rules", scheduling_rules, SchedulingRule)

    @classmethod
    def from_api_dict(cls, d: Dict[str, Any]) -> "SchedulerConfig":
        filtered = _filter_known(cls, d)
        flavors = filtered.get("resource_flavors")
        if isinstance(flavors, list):
            filtered["resource_flavors"] = [
                ResourceFlavor.from_api_dict(f) if isinstance(f, dict) else f for f in flavors
            ]
        queues = filtered.get("resource_queues")
        if isinstance(queues, list):
            filtered["resource_queues"] = [
                ResourceQueue.from_api_dict(q) if isinstance(q, dict) else q for q in queues
            ]
        rules = filtered.get("scheduling_rules")
        if isinstance(rules, list):
            filtered["scheduling_rules"] = [
                SchedulingRule.from_api_dict(r) if isinstance(r, dict) else r for r in rules
            ]
        return cls(**filtered)


# --- Read-side response models ---


@dataclass(frozen=True)
class SchedulerConfigVersion(ModelBase):
    """A specific version of a scheduler config (active or historical)."""

    __doc_py_example__ = """\
import anyscale

version = anyscale.scheduler.get_config()
print(version.version, version.is_active, version.config)
"""

    version: int = field(metadata={"docstring": "Monotonic version number for this config."})

    def _validate_version(self, version: int):
        if not isinstance(version, int) or isinstance(version, bool):
            raise TypeError("'version' must be an integer.")

    is_active: bool = field(metadata={"docstring": "Whether this is the currently active config."})

    def _validate_is_active(self, is_active: bool):
        if not isinstance(is_active, bool):
            raise TypeError("'is_active' must be a boolean.")

    created_at: datetime = field(
        metadata={"docstring": "Timestamp at which this version was applied."}
    )

    def _validate_created_at(self, created_at: datetime):
        if not isinstance(created_at, datetime):
            raise TypeError("'created_at' must be a datetime.")

    creator_id: str = field(
        metadata={"docstring": "User ID of the principal that applied this version."}
    )

    def _validate_creator_id(self, creator_id: str):
        if not isinstance(creator_id, str):
            raise TypeError("'creator_id' must be a string.")

    config: SchedulerConfig = field(
        metadata={"docstring": "The full scheduler config for this version."}
    )

    def _validate_config(self, config: SchedulerConfig) -> SchedulerConfig:
        if isinstance(config, dict):
            return SchedulerConfig.from_dict(config)
        if not isinstance(config, SchedulerConfig):
            raise TypeError("'config' must be a SchedulerConfig or dict.")
        return config


@dataclass(frozen=True)
class SchedulerConfigVersionSummary(ModelBase):
    """Metadata-only summary of a scheduler config version (used by `list`)."""

    __doc_py_example__ = """\
import anyscale

for v in anyscale.scheduler.list_config_versions():
    print(v.version, v.created_at, v.creator_id)
"""

    version: int = field(metadata={"docstring": "Monotonic version number."})

    def _validate_version(self, version: int):
        if not isinstance(version, int) or isinstance(version, bool):
            raise TypeError("'version' must be an integer.")

    created_at: datetime = field(
        metadata={"docstring": "Timestamp at which this version was applied."}
    )

    def _validate_created_at(self, created_at: datetime):
        if not isinstance(created_at, datetime):
            raise TypeError("'created_at' must be a datetime.")

    creator_id: str = field(
        metadata={"docstring": "User ID of the principal that applied this version."}
    )

    def _validate_creator_id(self, creator_id: str):
        if not isinstance(creator_id, str):
            raise TypeError("'creator_id' must be a string.")


# --- Live queue state (read-only) ---
#
# What `anyscale scheduler queue ...`, `overview` and `top-consumers` return: the
# scheduler's point-in-time view of queues and workloads, as the console's Utilization tab
# shows it. Every model carries the API's fields under the API's names, in the API's order.


def _is_optional(annotation: Any) -> bool:
    return get_origin(annotation) is Union and type(None) in get_args(annotation)


_TReadModel = TypeVar("_TReadModel", bound="_ReadModel")


class _ReadModel(ModelBase):
    """Base of the models the scheduler's read APIs return.

    `from_dict` accepts both the API's response and a model's own `to_dict()`:

    - These models keep the API's field order, so an optional field can sit before a
      required one and has no default. `to_dict()` leaves out a field that is None, so a
      missing optional field is read as None.
    - A key the model does not declare is skipped, so a field a newer backend adds does
      not break an older CLI.
    """

    @classmethod
    def from_dict(cls: Type[_TReadModel], d: Dict[str, Any]) -> _TReadModel:
        declared = fields(cls)  # type: ignore[arg-type]
        names = {f.name for f in declared}
        kwargs = {key: value for key, value in d.items() if key in names}
        for f in declared:
            if f.name not in kwargs and _is_optional(f.type):
                kwargs[f.name] = None
        return cls(**kwargs)


def _coerce_model(name: str, value: Any, model_cls: Type[ModelBase]):
    """Return `value` as a `model_cls`, building it from a dict when needed."""
    if isinstance(value, model_cls):
        return value
    if isinstance(value, dict):
        return model_cls.from_dict(value)
    raise TypeError(f"'{name}' must be a {model_cls.__name__} or dict.")


def _coerce_optional_model(name: str, value: Any, model_cls: Type[ModelBase]):
    return None if value is None else _coerce_model(name, value, model_cls)


def _validate_int(name: str, value: int):
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"'{name}' must be an integer.")


def _validate_number(name: str, value: float):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"'{name}' must be a number.")


def _validate_str(name: str, value: str):
    if not isinstance(value, str):
        raise TypeError(f"'{name}' must be a string.")


def _validate_optional_str(name: str, value: Optional[str]):
    if value is not None and not isinstance(value, str):
        raise TypeError(f"'{name}' must be a string or None.")


def _validate_optional_datetime(name: str, value: Optional[datetime]):
    if value is not None and not isinstance(value, datetime):
        raise TypeError(f"'{name}' must be a datetime or None.")


class WorkloadState(ModelEnum):
    """Which side of a queue to list: the workloads waiting, or the ones admitted."""

    PENDING = "pending"
    RUNNING = "running"

    __docstrings__: ClassVar[Dict[str, str]] = _docs_by_name_and_value(
        [
            (
                "PENDING",
                "pending",
                "Workloads waiting for admission. One row per queued request, so a cluster "
                "with several queued requests is listed several times.",
            ),
            (
                "RUNNING",
                "running",
                "Workloads that hold capacity: admitted or running. One row per cluster.",
            ),
        ]
    )

    @classmethod
    def validate(cls, value) -> "WorkloadState":
        return _validate_lowercase_enum(cls, value.lower() if isinstance(value, str) else value)


class WorkloadStatus(ModelEnum):
    """The admission status of a workload in a queue."""

    UNSPECIFIED = "UNSPECIFIED"
    QUEUED = "QUEUED"
    REQUEUED = "REQUEUED"
    ADMITTED = "ADMITTED"
    RUNNING = "RUNNING"

    __docstrings__: ClassVar[Dict[str, str]] = {
        UNSPECIFIED: "The scheduler reported no status, or one this version does not know.",
        QUEUED: "Waiting for admission, for the first time.",
        REQUEUED: "Waiting for admission again, after it was put back in the queue.",
        ADMITTED: "Admitted against the queue's quota. Its instances are launching.",
        RUNNING: "Admitted, and its instances are launched.",
    }


@dataclass(frozen=True)
class NodeCounts(_ReadModel):
    """Node counts as the scheduler tracks them. They follow the scheduler's last pass, so
    they can lag the nodes that are alive right now."""

    __doc_py_example__ = """\
import anyscale

nodes = anyscale.scheduler.get_overview().totals.nodes
print(nodes.running, nodes.admitted, nodes.pending)
"""

    running: int = field(metadata={"docstring": "Nodes that are launched."})

    def _validate_running(self, running: int):
        _validate_int("running", running)

    admitted: int = field(
        metadata={"docstring": "Nodes admitted against quota that are not launched yet."}
    )

    def _validate_admitted(self, admitted: int):
        _validate_int("admitted", admitted)

    pending: int = field(metadata={"docstring": "Nodes requested that are waiting for admission."})

    def _validate_pending(self, pending: int):
        _validate_int("pending", pending)


@dataclass(frozen=True)
class WorkloadCounts(_ReadModel):
    """Workload (cluster) counts. A cluster with both admitted and queued requests counts
    in both."""

    __doc_py_example__ = """\
import anyscale

workloads = anyscale.scheduler.get_queue("research").workloads
print(workloads.running, workloads.pending)
"""

    running: int = field(metadata={"docstring": "Workloads that hold capacity."})

    def _validate_running(self, running: int):
        _validate_int("running", running)

    pending: int = field(metadata={"docstring": "Workloads waiting for admission."})

    def _validate_pending(self, pending: int):
        _validate_int("pending", pending)


@dataclass(frozen=True)
class MarketBreakdown(_ReadModel):
    """Running and admitted nodes split by purchase market. The three counts add up to
    running + admitted."""

    __doc_py_example__ = """\
import anyscale

market = anyscale.scheduler.get_overview().totals.market
print(market.spot, market.on_demand, market.unspecified)
"""

    spot: int = field(metadata={"docstring": "Spot nodes."})

    def _validate_spot(self, spot: int):
        _validate_int("spot", spot)

    on_demand: int = field(metadata={"docstring": "On-demand nodes."})

    def _validate_on_demand(self, on_demand: int):
        _validate_int("on_demand", on_demand)

    unspecified: int = field(
        metadata={
            "docstring": "Nodes whose market is not known at admission: Kubernetes nodes, "
            "spot with on-demand fallback, and requests without a market label."
        }
    )

    def _validate_unspecified(self, unspecified: int):
        _validate_int("unspecified", unspecified)


@dataclass(frozen=True)
class ResourceUsage(_ReadModel):
    """Use of one resource of one flavor against its quota."""

    __doc_py_example__ = """\
import anyscale

for usage in anyscale.scheduler.get_queue("research").quota:
    print(usage.flavor, usage.resource, usage.used, usage.ceiling, usage.utilization)
"""

    flavor: str = field(metadata={"docstring": "Name of the resource flavor."})

    def _validate_flavor(self, flavor: str):
        _validate_str("flavor", flavor)

    resource: str = field(metadata={"docstring": "Name of the resource, e.g. gpu or cpu."})

    def _validate_resource(self, resource: str):
        _validate_str("resource", resource)

    used: float = field(metadata={"docstring": "Amount in use."})

    def _validate_used(self, used: float):
        _validate_number("used", used)

    ceiling: float = field(
        metadata={"docstring": "The nominal quota for this flavor and resource."}
    )

    def _validate_ceiling(self, ceiling: float):
        _validate_number("ceiling", ceiling)

    headroom: float = field(
        metadata={"docstring": "Amount left under the ceiling: ceiling - used, never below 0."}
    )

    def _validate_headroom(self, headroom: float):
        _validate_number("headroom", headroom)

    utilization: float = field(
        metadata={"docstring": "used / ceiling, as a fraction. 0 when the ceiling is 0."}
    )

    def _validate_utilization(self, utilization: float):
        _validate_number("utilization", utilization)


@dataclass(frozen=True)
class ResourceQueueStatus(_ReadModel):
    """The live state of one active resource queue: its workloads, nodes and quota use.

    `ResourceQueue` is the queue as configured. This is the queue as it runs.
    """

    __doc_py_example__ = """\
import anyscale

queue = anyscale.scheduler.get_queue("research")
print(queue.queue_id, queue.workloads.pending, queue.nodes.running)
for usage in queue.quota:
    print(usage.flavor, usage.resource, usage.utilization)
"""

    queue_id: str = field(metadata={"docstring": "ID of the queue."})

    def _validate_queue_id(self, queue_id: str):
        _validate_str("queue_id", queue_id)

    queue: str = field(metadata={"docstring": "Name of the queue, as in the scheduler config."})

    def _validate_queue(self, queue: str):
        _validate_str("queue", queue)

    cohort: Optional[str] = field(
        metadata={
            "docstring": "Name of the cohort the queue borrows and lends quota in. None when "
            "the queue is in no cohort."
        }
    )

    def _validate_cohort(self, cohort: Optional[str]):
        _validate_optional_str("cohort", cohort)

    workloads: WorkloadCounts = field(
        metadata={"docstring": "Running and pending workloads in the queue."}
    )

    def _validate_workloads(self, workloads: WorkloadCounts) -> WorkloadCounts:
        return _coerce_model("workloads", workloads, WorkloadCounts)

    nodes: NodeCounts = field(
        metadata={"docstring": "Running, admitted and pending nodes in the queue."}
    )

    def _validate_nodes(self, nodes: NodeCounts) -> NodeCounts:
        return _coerce_model("nodes", nodes, NodeCounts)

    quota: List[ResourceUsage] = field(
        metadata={
            "docstring": "Quota use, one entry per flavor and resource the queue has a quota for."
        }
    )

    def _validate_quota(self, quota: List[ResourceUsage]) -> List[ResourceUsage]:
        return _coerce_list("quota", quota if quota is not None else [], ResourceUsage)

    market: Optional[MarketBreakdown] = field(
        metadata={"docstring": "The queue's nodes split by spot and on-demand."}
    )

    def _validate_market(self, market: Optional[MarketBreakdown]) -> Optional[MarketBreakdown]:
        return _coerce_optional_model("market", market, MarketBreakdown)


@dataclass(frozen=True)
class ResourceQueueStatusPage(ModelBase):
    """One page of resource queues, and the token that fetches the next page."""

    __doc_py_example__ = """\
import anyscale

page = anyscale.scheduler.list_queues(max_items=50)
for queue in page.results:
    print(queue.queue, queue.workloads.running, queue.workloads.pending)
if page.next_page_token is not None:
    page = anyscale.scheduler.list_queues(max_items=50, page_token=page.next_page_token)
"""

    results: List[ResourceQueueStatus] = field(metadata={"docstring": "The queues of this page."})

    def _validate_results(self, results: List[ResourceQueueStatus]) -> List[ResourceQueueStatus]:
        return _coerce_list("results", results if results is not None else [], ResourceQueueStatus)

    next_page_token: Optional[str] = field(
        default=None,
        metadata={
            "docstring": "Pass this as page_token to get the next page. None when there are "
            "no more queues."
        },
    )

    def _validate_next_page_token(self, next_page_token: Optional[str]):
        _validate_optional_str("next_page_token", next_page_token)


@dataclass(frozen=True)
class WorkloadNodes(_ReadModel):
    """The nodes of one workload: what it asked for and what it has."""

    __doc_py_example__ = """\
import anyscale

for workload in anyscale.scheduler.list_queue_workloads("research", state="running").results:
    print(workload.cluster_id, workload.nodes.requested, workload.nodes.running)
"""

    requested: int = field(metadata={"docstring": "Nodes the workload asked for."})

    def _validate_requested(self, requested: int):
        _validate_int("requested", requested)

    admitted: int = field(
        metadata={"docstring": "Nodes admitted against quota that are not launched yet."}
    )

    def _validate_admitted(self, admitted: int):
        _validate_int("admitted", admitted)

    running: int = field(metadata={"docstring": "Nodes that are launched."})

    def _validate_running(self, running: int):
        _validate_int("running", running)

    pending: int = field(metadata={"docstring": "Nodes waiting for admission."})

    def _validate_pending(self, pending: int):
        _validate_int("pending", pending)


@dataclass(frozen=True)
class QueueWorkload(_ReadModel):
    """One workload in a resource queue.

    The running list has one row per cluster. The pending list has one row per queued
    request, so a cluster with several queued requests is listed several times.
    """

    __doc_py_example__ = """\
import anyscale

page = anyscale.scheduler.list_queue_workloads("research", state="pending")
for workload in page.results:
    print(workload.queue_position, workload.name, workload.status, workload.requested_resources)
"""

    cluster_id: str = field(metadata={"docstring": "ID of the workload's cluster."})

    def _validate_cluster_id(self, cluster_id: str):
        _validate_str("cluster_id", cluster_id)

    name: Optional[str] = field(
        metadata={"docstring": "Name of the workload. None until the scheduler knows it."}
    )

    def _validate_name(self, name: Optional[str]):
        _validate_optional_str("name", name)

    type: Optional[str] = field(
        metadata={"docstring": "Kind of workload, as the scheduler labels it."}
    )

    def _validate_type(self, type: Optional[str]):  # noqa: A002
        _validate_optional_str("type", type)

    project: Optional[str] = field(metadata={"docstring": "Name of the workload's project."})

    def _validate_project(self, project: Optional[str]):
        _validate_optional_str("project", project)

    priority: int = field(metadata={"docstring": "Scheduling priority of the workload."})

    def _validate_priority(self, priority: int):
        _validate_int("priority", priority)

    nodes: WorkloadNodes = field(
        metadata={"docstring": "Requested, admitted, running and pending nodes."}
    )

    def _validate_nodes(self, nodes: WorkloadNodes) -> WorkloadNodes:
        return _coerce_model("nodes", nodes, WorkloadNodes)

    flavors: List[str] = field(
        metadata={"docstring": "Names of the resource flavors the workload uses."}
    )

    def _validate_flavors(self, flavors: List[str]) -> List[str]:
        flavors = [] if flavors is None else flavors
        if not isinstance(flavors, list) or not all(isinstance(f, str) for f in flavors):
            raise TypeError("'flavors' must be a list of strings.")
        return flavors

    cloud_id: str = field(metadata={"docstring": "ID of the cloud the workload runs in."})

    def _validate_cloud_id(self, cloud_id: str):
        _validate_str("cloud_id", cloud_id)

    created_at: Optional[datetime] = field(
        metadata={
            "docstring": "Running list: when the workload started. Pending list: when this "
            "request was queued."
        }
    )

    def _validate_created_at(self, created_at: Optional[datetime]):
        _validate_optional_datetime("created_at", created_at)

    status: WorkloadStatus = field(
        metadata={"docstring": "Admission status of the workload. See WorkloadStatus."}
    )

    def _validate_status(self, status: WorkloadStatus) -> WorkloadStatus:
        return WorkloadStatus.validate(status)

    plan_id: str = field(
        metadata={
            "docstring": "ID of the queued request. Set on the pending list, empty on the "
            "running list."
        }
    )

    def _validate_plan_id(self, plan_id: str):
        _validate_str("plan_id", plan_id)

    queue_position: int = field(
        metadata={
            "docstring": "Place in line on the pending list, where 1 is next to be admitted. "
            "0 on the running list."
        }
    )

    def _validate_queue_position(self, queue_position: int):
        _validate_int("queue_position", queue_position)

    requested_resources: Dict[str, float] = field(
        metadata={
            "docstring": "Resources the queued request asks for, e.g. gpu, cpu and "
            "memory_gb. Set on the pending list, empty on the running list."
        }
    )

    def _validate_requested_resources(
        self, requested_resources: Dict[str, float]
    ) -> Dict[str, float]:
        requested_resources = {} if requested_resources is None else requested_resources
        if not isinstance(requested_resources, dict) or not all(
            isinstance(key, str)
            and isinstance(value, (int, float))
            and not isinstance(value, bool)
            for key, value in requested_resources.items()
        ):
            raise TypeError("'requested_resources' must be a dict of str to number.")
        return requested_resources

    url: Optional[str] = field(
        metadata={
            "docstring": "Path of the workload's page in the console, relative to the "
            "console host. None when the scheduler cannot tell which page it is."
        }
    )

    def _validate_url(self, url: Optional[str]):
        _validate_optional_str("url", url)


@dataclass(frozen=True)
class QueueWorkloadList(ModelBase):
    """Workloads of a resource queue, and how many there are in total."""

    __doc_py_example__ = """\
import anyscale

page = anyscale.scheduler.list_queue_workloads("research", state="pending", max_items=20)
print(f"{len(page.results)} of {page.total}")
"""

    results: List[QueueWorkload] = field(
        metadata={"docstring": "The workloads, in the scheduler's order. See QueueWorkload."}
    )

    def _validate_results(self, results: List[QueueWorkload]) -> List[QueueWorkload]:
        return _coerce_list("results", results if results is not None else [], QueueWorkload)

    total: int = field(
        metadata={
            "docstring": "How many workloads match, which can be more than len(results) "
            "when max_items cut the list short."
        }
    )

    def _validate_total(self, total: int):
        _validate_int("total", total)
        if total < 0:
            raise ValueError("'total' must be >= 0.")


@dataclass(frozen=True)
class SchedulerTotals(_ReadModel):
    """Org-wide node and workload totals."""

    __doc_py_example__ = """\
import anyscale

totals = anyscale.scheduler.get_overview().totals
print(totals.nodes.running, totals.workloads.running, totals.workloads.pending)
"""

    nodes: NodeCounts = field(metadata={"docstring": "Running, admitted and pending nodes."})

    def _validate_nodes(self, nodes: NodeCounts) -> NodeCounts:
        return _coerce_model("nodes", nodes, NodeCounts)

    active_workloads: int = field(
        metadata={
            "docstring": "Deprecated by the API in favor of `workloads`. Workloads that are "
            "not finished."
        }
    )

    def _validate_active_workloads(self, active_workloads: int):
        _validate_int("active_workloads", active_workloads)

    workloads: Optional[WorkloadCounts] = field(
        default=None, metadata={"docstring": "Running and pending workloads."}
    )

    def _validate_workloads(self, workloads: Optional[WorkloadCounts]) -> Optional[WorkloadCounts]:
        return _coerce_optional_model("workloads", workloads, WorkloadCounts)

    market: Optional[MarketBreakdown] = field(
        default=None, metadata={"docstring": "Nodes split by spot and on-demand."}
    )

    def _validate_market(self, market: Optional[MarketBreakdown]) -> Optional[MarketBreakdown]:
        return _coerce_optional_model("market", market, MarketBreakdown)


@dataclass(frozen=True)
class CloudRollup(_ReadModel):
    """Node and workload totals of one cloud."""

    __doc_py_example__ = """\
import anyscale

for cloud in anyscale.scheduler.get_overview().clouds:
    print(cloud.cloud_id, cloud.nodes.running)
"""

    cloud_id: str = field(metadata={"docstring": "ID of the cloud."})

    def _validate_cloud_id(self, cloud_id: str):
        _validate_str("cloud_id", cloud_id)

    nodes: NodeCounts = field(metadata={"docstring": "Running, admitted and pending nodes."})

    def _validate_nodes(self, nodes: NodeCounts) -> NodeCounts:
        return _coerce_model("nodes", nodes, NodeCounts)

    workloads: Optional[WorkloadCounts] = field(
        default=None, metadata={"docstring": "Running and pending workloads."}
    )

    def _validate_workloads(self, workloads: Optional[WorkloadCounts]) -> Optional[WorkloadCounts]:
        return _coerce_optional_model("workloads", workloads, WorkloadCounts)

    market: Optional[MarketBreakdown] = field(
        default=None, metadata={"docstring": "Nodes split by spot and on-demand."}
    )

    def _validate_market(self, market: Optional[MarketBreakdown]) -> Optional[MarketBreakdown]:
        return _coerce_optional_model("market", market, MarketBreakdown)


@dataclass(frozen=True)
class TopologySummary(_ReadModel):
    """How much the active scheduler config defines."""

    __doc_py_example__ = """\
import anyscale

topology = anyscale.scheduler.get_overview().topology
print(topology.config_version, topology.active_queues, topology.active_flavors)
"""

    active_queues: int = field(metadata={"docstring": "Number of active resource queues."})

    def _validate_active_queues(self, active_queues: int):
        _validate_int("active_queues", active_queues)

    active_flavors: int = field(metadata={"docstring": "Number of active resource flavors."})

    def _validate_active_flavors(self, active_flavors: int):
        _validate_int("active_flavors", active_flavors)

    active_rules: int = field(metadata={"docstring": "Number of active scheduling rules."})

    def _validate_active_rules(self, active_rules: int):
        _validate_int("active_rules", active_rules)

    active_cohorts: int = field(metadata={"docstring": "Number of active cohorts."})

    def _validate_active_cohorts(self, active_cohorts: int):
        _validate_int("active_cohorts", active_cohorts)

    config_version: int = field(metadata={"docstring": "Version of the active scheduler config."})

    def _validate_config_version(self, config_version: int):
        _validate_int("config_version", config_version)

    config_updated_at: Optional[datetime] = field(
        default=None, metadata={"docstring": "When the active scheduler config was applied."}
    )

    def _validate_config_updated_at(self, config_updated_at: Optional[datetime]):
        _validate_optional_datetime("config_updated_at", config_updated_at)


@dataclass(frozen=True)
class SchedulerOverview(_ReadModel):
    """The org-wide scheduler rollup: totals, quota use, per-cloud totals and topology."""

    __doc_py_example__ = """\
import anyscale

overview = anyscale.scheduler.get_overview()
print(overview.totals.nodes.running, overview.topology.active_queues)
for usage in overview.utilization:
    print(usage.flavor, usage.resource, usage.utilization)
"""

    totals: SchedulerTotals = field(metadata={"docstring": "Org-wide node and workload totals."})

    def _validate_totals(self, totals: SchedulerTotals) -> SchedulerTotals:
        return _coerce_model("totals", totals, SchedulerTotals)

    utilization: List[ResourceUsage] = field(
        metadata={"docstring": "Org-wide quota use, one entry per flavor and resource."}
    )

    def _validate_utilization(self, utilization: List[ResourceUsage]) -> List[ResourceUsage]:
        return _coerce_list(
            "utilization", utilization if utilization is not None else [], ResourceUsage
        )

    clouds: List[CloudRollup] = field(metadata={"docstring": "The same totals, per cloud."})

    def _validate_clouds(self, clouds: List[CloudRollup]) -> List[CloudRollup]:
        return _coerce_list("clouds", clouds if clouds is not None else [], CloudRollup)

    topology: TopologySummary = field(
        metadata={"docstring": "How much the active scheduler config defines."}
    )

    def _validate_topology(self, topology: TopologySummary) -> TopologySummary:
        return _coerce_model("topology", topology, TopologySummary)


@dataclass(frozen=True)
class TopConsumer(_ReadModel):
    """One of the clusters that hold the most nodes."""

    __doc_py_example__ = """\
import anyscale

for consumer in anyscale.scheduler.list_top_consumers(max_items=5):
    print(consumer.cluster_id, consumer.name, consumer.nodes, consumer.duration_seconds)
"""

    cluster_id: str = field(metadata={"docstring": "ID of the cluster."})

    def _validate_cluster_id(self, cluster_id: str):
        _validate_str("cluster_id", cluster_id)

    name: Optional[str] = field(
        metadata={"docstring": "Name of the workload. None until the scheduler knows it."}
    )

    def _validate_name(self, name: Optional[str]):
        _validate_optional_str("name", name)

    project: Optional[str] = field(metadata={"docstring": "Name of the workload's project."})

    def _validate_project(self, project: Optional[str]):
        _validate_optional_str("project", project)

    nodes: int = field(metadata={"docstring": "Nodes the cluster holds."})

    def _validate_nodes(self, nodes: int):
        _validate_int("nodes", nodes)

    duration_seconds: int = field(
        metadata={
            "docstring": "Approximate run time in seconds, counted from when the cluster's "
            "first successful request was created."
        }
    )

    def _validate_duration_seconds(self, duration_seconds: int):
        _validate_int("duration_seconds", duration_seconds)

    url: Optional[str] = field(
        metadata={
            "docstring": "Path of the workload's page in the console, relative to the "
            "console host. None when the scheduler cannot tell which page it is."
        }
    )

    def _validate_url(self, url: Optional[str]):
        _validate_optional_str("url", url)
