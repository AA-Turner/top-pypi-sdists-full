# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations

from collections.abc import Iterable

import contrast_fireball

from contrast import AGENT_CURR_WORKING_DIR
from contrast.agent.agent_lib.input_tracing import InputAnalysisResult
from contrast.agent.policy.patch_location_policy import PatchLocationPolicy
from contrast.agent.protect.rule.base_rule import BaseRule
from contrast.utils.decorators import fail_quietly

PARENT_CHECK = ".."
SLASH = "/"
SAFE_PATHS = ["tmp", "public", "docs", "static", "template", "templates"]
WRITE_OPTIONS = ["w", "a"]


class PathTraversal(BaseRule):
    RULE_NAME = "path-traversal"
    FIREBALL_RULE = contrast_fireball.PathTraversal

    def build_sample(
        self,
        evaluation: InputAnalysisResult | None,
        candidate_string: str | None,
        outcome: contrast_fireball.ProtectEventOutcome,
        **kwargs,
    ) -> contrast_fireball.ProtectEventSample:
        assert evaluation is not None

        sample = self.build_base_sample(
            evaluation,
            outcome=outcome,
            rule=self.FIREBALL_RULE(
                details=contrast_fireball.PathTraversalDetails(
                    path=path,
                )
                if (path := candidate_string)
                else None
            ),
        )
        return sample

    @fail_quietly(
        "Failed to run path traversal skip_protect_analysis", return_value=False
    )
    def skip_protect_analysis(
        self, user_input: object, args: tuple, kwargs: dict[str, object]
    ) -> bool:
        write = possible_write(args, kwargs)
        if write:
            # any write is a risk so we should not skip analysis
            return False

        return not actionable_path(user_input)

    def infilter_kwargs(self, user_input: str, patch_policy: PatchLocationPolicy):
        return dict(method=patch_policy.method_name)


def possible_write(args: tuple, kwargs: dict[str, object]):
    return _possible_write_kwargs(kwargs) or _possible_write_args(args)


def _possible_write_kwargs(kwargs: dict[str, object]) -> bool:
    mode = kwargs.get("mode", "")

    if not isinstance(mode, str):
        return False

    return bool(mode and any([x in mode for x in WRITE_OPTIONS]))


def _possible_write_args(args: tuple) -> bool:
    if not isinstance(args, Iterable):
        return False

    return (
        len(args) > 1
        and args[1] is not None
        and isinstance(args[1], Iterable)
        and any([x in args[1] for x in WRITE_OPTIONS])
    )


def actionable_path(path: object) -> bool:
    if not path or not isinstance(path, str):
        return False

    # moving up directory structure is a risk and hence actionable
    if path.find(PARENT_CHECK) > 1:
        return True

    if "/contrast/" in path or "/site-packages/" in path:
        return False

    if path.startswith(SLASH):
        for prefix in _safer_abs_paths():
            if path.startswith(prefix):
                return False
    else:
        for prefix in SAFE_PATHS:
            if path.startswith(prefix):
                return False

    return True


def _safer_abs_paths() -> list[str]:
    return (
        [f"{AGENT_CURR_WORKING_DIR}/{item}" for item in SAFE_PATHS]
        if AGENT_CURR_WORKING_DIR
        else []
    )
