from dataclasses import dataclass, field, fields
from datetime import datetime
from decimal import Decimal
from typing import Any, ClassVar, Dict, List, Optional

from anyscale._private.models import ModelBase, ModelEnum


# Quota values are fractional but capped at this many decimal places.
_MAX_QUOTA_DECIMAL_PLACES = 3


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
    if value < 0:
        raise ValueError(f"'{name}' must be >= 0.")
    # For finite values .exponent is an int (= -decimal_places).
    exponent = Decimal(str(value)).as_tuple().exponent
    if isinstance(exponent, int) and -exponent > _MAX_QUOTA_DECIMAL_PLACES:
        raise ValueError(
            f"'{name}' supports at most {_MAX_QUOTA_DECIMAL_PLACES} decimal places."
        )


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
        metadata={
            "docstring": "Match operator: 'in', 'not_in', 'exists', or 'does_not_exist'."
        }
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
        MatchExpression(key="market", operator=Operator.IN, values=["spot"]),
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
        if advanced_instance_config is not None and not isinstance(
            advanced_instance_config, dict
        ):
            raise TypeError("'advanced_instance_config' must be a dict.")

    @classmethod
    def from_api_dict(cls, d: Dict[str, Any]) -> "ResourceFlavor":
        filtered = _filter_known(cls, d)
        sel = filtered.get("selector")
        if isinstance(sel, list):
            filtered["selector"] = [
                MatchExpression.from_api_dict(r) if isinstance(r, dict) else r
                for r in sel
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

    nominal_quota: float = field(
        metadata={
            "docstring": "Guaranteed capacity for this queue+flavor+resource. "
            "Fractional values are allowed (up to 3 decimal places)."
        }
    )

    def _validate_nominal_quota(self, nominal_quota: float):
        _validate_non_negative_quota("nominal_quota", nominal_quota)

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

    name: str = field(
        metadata={"docstring": "Name of the resource flavor this quota applies to."}
    )

    def _validate_name(self, name: str):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("'name' must be a non-empty string.")

    resources: Optional[List[ResourceQuotaSpec]] = field(
        default=None,
        metadata={
            "docstring": "Per-resource quotas (e.g. one entry for 'gpu', one for 'cpu')."
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
                ResourceQuotaSpec.from_api_dict(r) if isinstance(r, dict) else r
                for r in resources
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
            "docstring": "Resources covered by this group (e.g. ['gpu'] or ['cpu', 'memory'])."
        }
    )

    def _validate_covered_resources(self, covered_resources: List[str]):
        if (
            not isinstance(covered_resources, list)
            or not covered_resources
            or not all(isinstance(x, str) and x.strip() for x in covered_resources)
        ):
            raise ValueError("'covered_resources' must be a non-empty list of strings.")
        if len(covered_resources) != len(set(covered_resources)):
            raise ValueError("'covered_resources' must not contain duplicates.")

    flavors: List[FlavorQuota] = field(
        metadata={
            "docstring": "Flavor-level quotas for the resources in covered_resources."
        }
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
                FlavorQuota.from_api_dict(f) if isinstance(f, dict) else f
                for f in flavors
            ]
        return cls(**filtered)


@dataclass(frozen=True)
class PreemptionPolicy(ModelBase):
    """Preemption settings for a resource queue."""

    __doc_py_example__ = """\
from anyscale.scheduler.models import (
    PreemptionPolicy,
    PreemptionPolicyWithinResourceQueue,
)

policy = PreemptionPolicy(
    within_resource_queue=PreemptionPolicyWithinResourceQueue.LOWER_PRIORITY,
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

    @classmethod
    def from_api_dict(cls, d: Dict[str, Any]) -> "PreemptionPolicy":
        return cls(**_filter_known(cls, d))


@dataclass(frozen=True)
class ResourceQueue(ModelBase):
    """A queue requests are routed to. Carries optional preemption and per-flavor quotas."""

    __doc_py_example__ = """\
from anyscale.scheduler.models import ResourceQueue

queue = ResourceQueue(name="research")
"""

    name: str = field(metadata={"docstring": "Unique name for this resource queue."})

    def _validate_name(self, name: str):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("'name' must be a non-empty string.")

    preemption: Optional[PreemptionPolicy] = field(
        default=None, metadata={"docstring": "Preemption settings for this queue."},
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

    @classmethod
    def from_api_dict(cls, d: Dict[str, Any]) -> "ResourceQueue":
        filtered = _filter_known(cls, d)
        pre = filtered.get("preemption")
        if isinstance(pre, dict):
            filtered["preemption"] = PreemptionPolicy.from_api_dict(pre)
        groups = filtered.get("resource_groups")
        if isinstance(groups, list):
            filtered["resource_groups"] = [
                ResourceGroup.from_api_dict(g) if isinstance(g, dict) else g
                for g in groups
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
        default=None, metadata={"docstring": "Minimum allowed priority."},
    )

    def _validate_min(self, min: Optional[int]):  # noqa: A002
        _validate_non_negative_int("min", min)

    max: Optional[int] = field(  # noqa: A003
        default=None, metadata={"docstring": "Maximum allowed priority."},
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
        metadata={
            "docstring": "Name of the queue requests matching this rule are routed to."
        }
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
        metadata={
            "docstring": "Priority bounds applied to requests matched by this rule."
        },
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
                MatchExpression.from_api_dict(s) if isinstance(s, dict) else s
                for s in sel
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
      - key: market
        operator: in
        values: [spot]
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
                ResourceFlavor.from_api_dict(f) if isinstance(f, dict) else f
                for f in flavors
            ]
        queues = filtered.get("resource_queues")
        if isinstance(queues, list):
            filtered["resource_queues"] = [
                ResourceQueue.from_api_dict(q) if isinstance(q, dict) else q
                for q in queues
            ]
        rules = filtered.get("scheduling_rules")
        if isinstance(rules, list):
            filtered["scheduling_rules"] = [
                SchedulingRule.from_api_dict(r) if isinstance(r, dict) else r
                for r in rules
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

    version: int = field(
        metadata={"docstring": "Monotonic version number for this config."}
    )

    def _validate_version(self, version: int):
        if not isinstance(version, int) or isinstance(version, bool):
            raise TypeError("'version' must be an integer.")

    is_active: bool = field(
        metadata={"docstring": "Whether this is the currently active config."}
    )

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
