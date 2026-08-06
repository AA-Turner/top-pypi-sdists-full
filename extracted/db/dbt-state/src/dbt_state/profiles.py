from __future__ import annotations

import typing as t
from functools import cached_property

from dbt.config import Profile
from dbt.config.profile import read_profile
from dbt.config.renderer import ProfileRenderer
from dbt.config.runtime import RuntimeConfig

from dbt_state.config import RunCacheConfig


class Profiles:
    def __init__(
        self,
        raw_profiles: t.Dict[str, t.Any],
        profile_name: str,
        current_target_name: str,
        defer_to_target_name: str,
        cli_vars: t.Dict[str, t.Any],
    ) -> None:
        self._raw_profiles = raw_profiles
        self._profile_name = profile_name
        self._current_target_name = current_target_name
        self._defer_to_target_name = defer_to_target_name
        self._cli_vars = cli_vars

    @classmethod
    def from_config(cls, config: RuntimeConfig, run_cache_config: RunCacheConfig) -> Profiles:
        raw_profiles = read_profile(config.args.profiles_dir)
        return cls(
            raw_profiles,
            config.profile_name,
            config.target_name,
            run_cache_config.defer_to,
            config.cli_vars,
        )

    @property
    def is_defer_to_profile(self) -> bool:
        """Returns True if the current target is the same as the defer_to target."""
        return self._current_target_name == self._defer_to_target_name

    @cached_property
    def has_defer_to_profile(self) -> bool:
        profile = self._raw_profiles.get(self._profile_name, {})
        outputs = profile.get("outputs", {})
        return self._defer_to_target_name in outputs

    @cached_property
    def defer_to_profile(self) -> Profile:
        return Profile.from_raw_profiles(
            raw_profiles=self._raw_profiles,
            profile_name=self._profile_name,
            renderer=ProfileRenderer(cli_vars=self._cli_vars),
            target_override=self._defer_to_target_name,
        )
