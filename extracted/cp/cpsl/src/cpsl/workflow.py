"""Workflow primitive — session-backed structured surfaces.

A workflow is a named surface that appears in the subdomain sidebar and owns
its own DSL launcher UI, start handler, optional named action handlers, and
an ongoing message handler.  Under the hood each workflow instance is backed
by a regular ``Session``, so ``session.show_browser()``, task cards, streaming
replies, and the full chat transport continue to work.

Each launch creates a new session instance.  If the workflow defines a
``@workflow.ui()`` launcher, the user fills out the form and submits to
start a run.  If no UI is defined, clicking the workflow in the sidebar
opens a plain chat session tagged with the workflow identity.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, TypeVar

from .constants import VALID_WORKFLOW_SCOPES, WorkflowScope

F = TypeVar("F", bound=Callable)


@dataclass
class WorkflowInput:
    """Normalized payload delivered to ``@workflow.start()`` and
    ``@workflow.action()`` handlers.

    Behaves like a dict but also supports attribute-style access for
    convenience.  File uploads arrive as ``FileUpload`` instances.
    """

    _data: dict[str, Any] = field(default_factory=dict, repr=False)

    def __init__(self, data: dict[str, Any] | None = None) -> None:
        object.__setattr__(self, "_data", dict(data or {}))

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __getattr__(self, key: str) -> Any:
        try:
            return self._data[key]
        except KeyError:
            raise AttributeError(key) from None

    def __contains__(self, key: str) -> bool:
        return key in self._data

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()

    def items(self):
        return self._data.items()

    def to_dict(self) -> dict[str, Any]:
        return dict(self._data)

    def __repr__(self) -> str:
        return f"WorkflowInput({self._data!r})"


class Workflow:
    """A named workflow definition created via ``app.workflow(...)``.

    The returned object is used as a decorator target for handler
    registration::

        wf = app.workflow("My Workflow", scope="user")

        @wf.ui()
        def my_ui():
            return ui.WorkflowShell(...)

        @wf.start()
        async def on_start(session, input): ...

        @wf.action("do_thing")
        async def on_do_thing(session, input): ...

        @wf.message()
        async def on_message(session, msg): ...
    """

    def __init__(
        self,
        name: str,
        *,
        scope: WorkflowScope = "user",
        icon: str = "workflow",
        description: str = "",
    ) -> None:
        if scope not in VALID_WORKFLOW_SCOPES:
            raise ValueError(f"workflow scope must be one of {VALID_WORKFLOW_SCOPES}, got {scope!r}")

        self.name = name
        self.scope = scope
        self.icon = icon
        self.description = description

        self._ui_tree: dict[str, Any] | None = None
        self._start_handler: Callable | None = None
        self._message_handler: Callable | None = None
        self._action_handlers: dict[str, Callable] = {}

    # -- decorator: ui -------------------------------------------------------

    def ui(self) -> Callable[[F], F]:
        """Register the workflow's DSL launcher UI.

        The decorated function must return a ``ui.WorkflowShell`` widget tree.
        It is evaluated once at registration time (like ``@app.page``).
        """
        def decorator(fn: F) -> F:
            tree = fn()
            if not hasattr(tree, "to_dict"):
                raise TypeError(
                    f"@workflow.ui() handler must return a ui.WorkflowShell widget, "
                    f"got {type(tree).__name__}"
                )
            self._ui_tree = tree.to_dict()
            return fn
        return decorator

    # -- decorator: start ----------------------------------------------------

    def start(self) -> Callable[[F], F]:
        """Register the handler called when a new workflow instance is started.

        Signature: ``async def handler(session: Session, input: WorkflowInput)``
        """
        def decorator(fn: F) -> F:
            self._start_handler = fn
            return fn
        return decorator

    # -- decorator: action ---------------------------------------------------

    def action(self, name: str) -> Callable[[F], F]:
        """Register a named action handler for structured follow-up submits.

        Signature: ``async def handler(session: Session, input: WorkflowInput)``
        """
        def decorator(fn: F) -> F:
            self._action_handlers[name] = fn
            return fn
        return decorator

    # -- decorator: message --------------------------------------------------

    def message(self) -> Callable[[F], F]:
        """Register the freeform chat handler for an active workflow session.

        Signature: ``async def handler(session: Session, msg: Message)``
        """
        def decorator(fn: F) -> F:
            self._message_handler = fn
            return fn
        return decorator

    # -- serialization -------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        """Serialize the workflow definition for introspect / deploy metadata."""
        d: dict[str, Any] = {
            "name": self.name,
            "scope": self.scope,
            "icon": self.icon,
            "actions": list(self._action_handlers.keys()),
        }
        if self.description:
            d["description"] = self.description
        if self._ui_tree:
            d["widget_tree"] = self._ui_tree
        return d
