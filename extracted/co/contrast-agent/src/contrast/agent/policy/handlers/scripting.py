# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations

from sys import _getframe as getframe
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping

    from contrast.agent.policy.handlers import EventDict

NOT_SCRIPTING_CALLERS = frozenset(
    {
        # Imports execute each module's code.
        "importlib._bootstrap",
        "zipimport",
        "contrast_rewriter",
        # Annotations and signatures written in source code are evaluated by
        # typing.get_type_hints (typing on 3.12-3.13, annotationlib on 3.14+),
        # inspect.get_annotations, and inspect.signature for builtins.
        "typing",
        "annotationlib",
        "inspect",
        # Code is generated from validated identifiers or tokens: dataclass methods,
        # collections.namedtuple, gettext plural forms, and hashlib's constructors when
        # it's imported (3.15+).
        "dataclasses",
        "collections",
        "gettext",
        "hashlib",
    }
)


def shield_permissions_builder(
    event_dict: EventDict,
) -> Callable[[Mapping[str, object]], tuple[str, ...]]:
    """
    Builds a function that maps a call to exec or eval to the CVE shield permission
    (capability) it uses: scripting, unless it's called from one of
    NOT_SCRIPTING_CALLERS.
    """
    # registry_v2 imports this module
    from contrast.agent.policy.registry_v2 import caller_frame

    def shield_permissions(args: Mapping[str, object]) -> tuple[str, ...]:
        frame = caller_frame(getframe(1))
        try:
            caller = frame.f_globals.get("__name__")
        finally:
            del frame
        return () if caller in NOT_SCRIPTING_CALLERS else ("scripting",)

    return shield_permissions
