"""Load and query easymode profile definitions."""

import asyncio
import html
from importlib.resources import files
import json
import math
from typing import Any
from urllib.parse import unquote

from aiohomematic_config.const import DEFAULT_LOCALE
from aiohomematic_config.profile_data import ChannelProfileSet, ProfileDef, ProfileParamConstraint, ResolvedProfile


class ProfileStore:
    """Load and query easymode profile definitions."""

    __slots__ = ("_cache",)

    def __init__(self) -> None:
        """Initialize the profile store."""
        self._cache: dict[str, dict[str, ChannelProfileSet]] = {}

    async def get_profiles(
        self,
        *,
        receiver_channel_type: str,
        sender_channel_type: str,
        locale: str = DEFAULT_LOCALE,
    ) -> list[ResolvedProfile] | None:
        """Return resolved profiles for a channel type pair, or None if unavailable."""
        profile_set = await self._load_profile_set(
            receiver_channel_type=receiver_channel_type,
            sender_channel_type=sender_channel_type,
        )
        if profile_set is None:
            return None

        return [_resolve_profile(profile=p, locale=locale) for p in profile_set.profiles]

    async def match_active_profile(
        self,
        *,
        receiver_channel_type: str,
        sender_channel_type: str,
        current_values: dict[str, Any],
    ) -> int:
        """
        Return the ID of the currently active profile (0 = Expert fallback).

        When multiple profiles match, the most specific one wins.
        Specificity is determined by the number of "fixed" constraints.
        """
        profile_set = await self._load_profile_set(
            receiver_channel_type=receiver_channel_type,
            sender_channel_type=sender_channel_type,
        )
        if profile_set is None:
            return 0

        best_id = 0
        best_score: float = -math.inf

        for profile in profile_set.profiles:
            if profile.id == 0 or not profile.params:
                continue
            if (
                _matches_profile(params=profile.params, current_values=current_values)
                and (score := _profile_specificity(params=profile.params)) > best_score
            ):
                best_score = score
                best_id = profile.id

        return best_id

    async def _load_profile_set(
        self,
        *,
        receiver_channel_type: str,
        sender_channel_type: str,
    ) -> ChannelProfileSet | None:
        """Load profile set from JSON, with caching."""
        if receiver_channel_type not in self._cache:
            self._cache[receiver_channel_type] = await asyncio.to_thread(
                _load_receiver_profiles,
                receiver_channel_type=receiver_channel_type,
            )
        return self._cache[receiver_channel_type].get(sender_channel_type)


def _load_receiver_profiles(
    *,
    receiver_channel_type: str,
) -> dict[str, ChannelProfileSet]:
    """Load all sender profiles for a receiver type from JSON resource."""
    try:
        data_file = files("aiohomematic_config.profiles").joinpath(f"{receiver_channel_type}.json")
        raw = json.loads(data_file.read_text(encoding="utf-8"))
    except FileNotFoundError, ModuleNotFoundError:
        return {}

    return {sender_type: ChannelProfileSet.model_validate(sender_data) for sender_type, sender_data in raw.items()}


def _matches_profile(
    *,
    params: dict[str, ProfileParamConstraint],
    current_values: dict[str, Any],
) -> bool:
    """Check if current values match all profile constraints."""
    for param_id, constraint in params.items():
        if (current := current_values.get(param_id)) is None:
            continue

        try:
            current_num = float(current)
        except ValueError, TypeError:
            return False

        if constraint.constraint_type == "fixed":
            if constraint.value is not None and current_num != constraint.value:
                return False
        elif constraint.constraint_type == "list":
            if constraint.values is not None and current_num not in constraint.values:
                return False
        elif (
            constraint.constraint_type == "range"
            and constraint.min_value is not None
            and constraint.max_value is not None
            and not (constraint.min_value <= current_num <= constraint.max_value)
        ):
            return False
    return True


def _profile_specificity(*, params: dict[str, ProfileParamConstraint]) -> int:
    """
    Score a profile by how specific its constraints are.

    A profile with only "fixed" constraints is more specific than one with
    "list" or "range" constraints. Non-fixed constraints are penalized
    heavily so that an all-fixed profile always wins over one with loose
    constraints, regardless of the total number of parameters.
    """
    fixed_count = 0
    loose_count = 0
    for constraint in params.values():
        if constraint.constraint_type == "fixed":
            fixed_count += 1
        else:
            loose_count += 1
    return fixed_count - loose_count * 100


def _resolve_profile(*, profile: ProfileDef, locale: str) -> ResolvedProfile:
    """Resolve a profile definition to a locale-specific representation."""
    editable: list[str] = []
    fixed: dict[str, float] = {}
    defaults: dict[str, float] = {}

    for param_id, constraint in profile.params.items():
        if constraint.constraint_type == "range":
            editable.append(param_id)
            if constraint.default is not None:
                defaults[param_id] = constraint.default
        elif constraint.constraint_type == "fixed" and constraint.value is not None:
            fixed[param_id] = constraint.value

    raw_name = profile.name.get(locale) or profile.name.get("en", f"Profile {profile.id}")
    raw_description = profile.description.get(locale) or profile.description.get("en", "")

    return ResolvedProfile(
        id=profile.id,
        name=html.unescape(unquote(raw_name, encoding="iso-8859-1")),
        description=html.unescape(unquote(raw_description, encoding="iso-8859-1")),
        editable_params=editable,
        fixed_params=fixed,
        default_values=defaults,
    )
