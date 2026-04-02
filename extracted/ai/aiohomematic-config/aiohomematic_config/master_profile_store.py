"""Load and query MASTER paramset easymode profiles."""

import inspect
import math
from typing import Any

from aiohomematic.easymode_data import MasterProfileDef, get_channel_metadata
from pydantic import BaseModel

from aiohomematic_config.const import DEFAULT_LOCALE


class ResolvedMasterProfile(BaseModel):
    """A MASTER profile resolved for a specific locale."""

    id: int
    name: str
    description: str
    editable_params: list[str]
    fixed_params: dict[str, float | int | str]
    default_values: dict[str, float | int]
    visible_params: list[str] | None = None
    hidden_params: list[str] | None = None


class MasterProfileStore:
    """Load and query MASTER paramset easymode profile definitions."""

    __slots__ = ()

    def get_profiles(
        self,
        *,
        channel_type: str,
        sender_type: str,
        locale: str = DEFAULT_LOCALE,
    ) -> list[ResolvedMasterProfile] | None:
        """Return resolved MASTER profiles for a channel/sender pair, or None."""
        if not (metadata := get_channel_metadata(channel_type=channel_type)):
            return None

        st_meta = metadata.sender_types.get(sender_type)
        if not st_meta or not st_meta.profiles:
            return None

        return [_resolve_master_profile(profile=p, locale=locale) for p in st_meta.profiles]

    def match_active_profile(
        self,
        *,
        channel_type: str,
        sender_type: str,
        current_values: dict[str, Any],
    ) -> int:
        """
        Return the ID of the currently active MASTER profile (0 = Expert).

        Match current parameter values against profile constraints.
        The most specific matching profile wins.
        """
        if not (metadata := get_channel_metadata(channel_type=channel_type)):
            return 0

        st_meta = metadata.sender_types.get(sender_type)
        if not st_meta or not st_meta.profiles:
            return 0

        best_id = 0
        best_score = -1

        for profile in st_meta.profiles:
            if profile.id == 0:
                continue  # Expert is always fallback

            if not profile.params:
                continue

            score = _score_profile(
                profile=profile,
                current_values=current_values,
            )
            if score is not None and score > best_score:
                best_score = score
                best_id = profile.id

        return best_id


def _resolve_master_profile(
    *,
    profile: MasterProfileDef,
    locale: str,
) -> ResolvedMasterProfile:
    """Resolve a profile definition for a specific locale."""
    editable: list[str] = []
    fixed: dict[str, float | int | str] = {}
    defaults: dict[str, float | int] = {}

    for param_name, constraint in profile.params.items():
        if constraint.constraint_type == "fixed":
            if constraint.value is not None:
                fixed[param_name] = constraint.value
        elif constraint.constraint_type == "range":
            editable.append(param_name)
            if constraint.default is not None:
                defaults[param_name] = constraint.default
        elif constraint.constraint_type == "list":
            editable.append(param_name)

    return ResolvedMasterProfile(
        id=profile.id,
        name=profile.name_key,
        description=profile.description,
        editable_params=editable,
        fixed_params=fixed,
        default_values=defaults,
        visible_params=list(profile.visible_params) if profile.visible_params else None,
        hidden_params=list(profile.hidden_params) if profile.hidden_params else None,
    )


def _score_profile(
    *,
    profile: MasterProfileDef,
    current_values: dict[str, Any],
) -> int | None:
    """Score how well current values match a profile. None = no match."""
    fixed_count = 0

    for param_name, constraint in profile.params.items():
        if (current := current_values.get(param_name)) is None:
            continue

        if constraint.constraint_type == "fixed":
            if constraint.value is not None:
                if not _values_match(a=current, b=constraint.value):
                    return None  # Mismatch
                fixed_count += 1

        elif constraint.constraint_type == "list":
            if constraint.values and current not in constraint.values:
                return None

        elif constraint.constraint_type == "range":
            if (
                constraint.min_value is not None
                and isinstance(current, (int, float))
                and current < constraint.min_value
            ):
                return None
            if (
                constraint.max_value is not None
                and isinstance(current, (int, float))
                and current > constraint.max_value
            ):
                return None

    return fixed_count


def _values_match(*, a: Any, b: Any) -> bool:
    """Check if two values match, with float tolerance."""
    if isinstance(a, float) and isinstance(b, float):
        return math.isclose(a, b, rel_tol=1e-6)
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return math.isclose(float(a), float(b), rel_tol=1e-6)
    return bool(a == b)


__all__ = tuple(
    sorted(
        name
        for name, obj in globals().items()
        if not name.startswith("_")
        and (name.isupper() or inspect.isfunction(obj) or inspect.isclass(obj))
        and getattr(obj, "__module__", __name__) == __name__
    )
)
