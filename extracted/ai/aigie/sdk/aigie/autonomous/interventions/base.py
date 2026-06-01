"""Intervention ABCs — typed views over a Directive.

`Intervention` is intentionally lightweight: `__init__(self, directive)` and
properties exposing `directive.action_params`. No dataclass, no factory.

Two subclasses split the dispatch fan-out:
- `CallIntervention` — produces a `PostCallResult` synchronously (inline).
- `WorkflowIntervention` — applied via `FrameworkAdapter.apply()` between steps.
"""

from __future__ import annotations

import abc
from typing import TYPE_CHECKING, Any

from aigie.autonomous.adapters import ActionType
from aigie.autonomous.directives import Directive

if TYPE_CHECKING:
    from aigie.interceptor.protocols import InterceptionContext, PostCallResult


class Intervention(abc.ABC):
    """Typed view over a Directive.

    Subclasses expose `action_params` entries via properties so callers never
    poke into the raw dict. Adapters should prefer the `action_params`
    property over reaching through `directive.action_params`.
    """

    def __init__(self, directive: Directive) -> None:
        self.directive = directive

    @property
    def action_type(self) -> ActionType:
        return self.directive.action_type

    @property
    def action_params(self) -> dict[str, Any]:
        """Preferred adapter surface for the directive's action params dict."""
        return self.directive.action_params or {}


class CallIntervention(Intervention):
    """In-frame interventions (retry, rewrite args, block, modify response).

    The dispatcher consumes the returned `PostCallResult` directly; the call
    never reaches `FrameworkAdapter.apply()`.
    """

    @abc.abstractmethod
    def to_post_call_result(self, ctx: InterceptionContext) -> PostCallResult:
        """Produce the chain's response for this directive."""


class WorkflowIntervention(Intervention):
    """Between-step interventions (inject message, break loop, rewrite output).

    Adapter handles application via `FrameworkAdapter.apply()`.
    """
