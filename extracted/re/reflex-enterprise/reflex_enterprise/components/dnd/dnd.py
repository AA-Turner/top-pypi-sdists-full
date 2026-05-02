"""Drag and Drop component for Reflex."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any, ClassVar, TypedDict, TypeVar

import reflex as rx
from reflex.components.component import Component, MemoizationLeaf
from reflex.components.el.elements import Div
from reflex.constants import Hooks
from reflex.utils.format import to_snake_case
from reflex.vars.base import Var, VarData

from reflex_enterprise.components.component import ComponentEnterprise
from reflex_enterprise.utils import get_hook_deps
from reflex_enterprise.vars import static

# Common type aliases for the DnD components.
JsObj = Mapping[str, Any] | Var[Mapping[str, Any]] | None
ITEM_T = TypeVar("ITEM_T", bound=JsObj)
COLLECT_PARAMS_T = TypeVar(
    "COLLECT_PARAMS_T", bound=rx.vars.ObjectVar[Mapping[str, Any]]
)

# Represents any type of draggable item.
ANY_TYPE = Var.create("Any")
# Placeholder to be replaced with the actual dependency array.
DEP_ARRAY = Var.create(["DEP_ARRAY"])

# Underlying `useDrag` wrapper provided by react-dnd
USE_DRAG = "useDrag"
_use_drag = rx.vars.FunctionStringVar(
    _js_expr=USE_DRAG,
    _var_data=VarData(
        imports={
            "react-dnd": [USE_DRAG],
        },
    ),
)
# Underlying `useDrop` wrapper provided by react-dnd
USE_DROP = "useDrop"
_use_drop = rx.vars.FunctionStringVar(
    _js_expr=USE_DROP,
    _var_data=VarData(
        imports={
            "react-dnd": [USE_DROP],
        },
    ),
)

# Backends for drag and drop
HTML5_BACKEND = "HTML5Backend"
HTML5Backend = Var(
    HTML5_BACKEND,
    _var_data=VarData(
        imports={
            "react-dnd-html5-backend": [HTML5_BACKEND],
        },
    ),
)
# See available options at https://react-dnd.github.io/react-dnd/docs/backends/touch#options
TOUCH_BACKEND = "TouchBackend"
TouchBackend = Var(
    TOUCH_BACKEND,
    _var_data=VarData(
        imports={
            "react-dnd-touch-backend": [TOUCH_BACKEND],
        },
    ),
)


class DnDProvider(ComponentEnterprise):
    """Provides a context for all Drag and Drop operations.

    When using the high-level Draggable and DropTarget components, this will
    automatically be included as an AppWrap component.

    It must be included in the app or page explicitly when using the low-level
    useDrag and useDrop hooks.
    """

    library = "react-dnd"

    tag = "DndProvider"

    backend: Var[str] = HTML5Backend

    # Backend context used to configure the backend
    context: Var[dict[str, Any]]

    # Options object used for configuring the backend
    options: Var[dict[str, Any]]


class BaseDnDDiv(Div, MemoizationLeaf):
    """Base class for DnD components."""

    @staticmethod
    def _get_app_wrap_components() -> dict[tuple[int, str], Component]:
        """Add wrap components for Draggable component."""
        return {
            (30, "DnDProvider"): DnDProvider.create(),
        }


def _get_dep_array(code: Var) -> list[Var]:
    """Get const declarations from useDrag and useDrop hook code.

    When these states change, the dnd hook must be re-evaluated to take into
    account the new values.

    Args:
        code: The code to parse.

    Returns:
        A list of dependencies for the useDrag or useDrop hook.
    """
    deps = []
    var_data = code._get_all_var_data()
    if var_data:
        for hook in var_data.hooks:
            deps.extend(Var(d) for d in get_hook_deps(hook))
    return deps


def _with_dep_array(code: Var, pattern: str = str(DEP_ARRAY)) -> Var:
    """Update the code to include the dependency array.

    To maximize compatibility, the resulting hook will be marked POST_TRIGGER to
    ensure it can access memoized event triggers.

    Args:
        code: The code to update.
        pattern: The pattern to replace with the dependency array.

    Returns:
        The updated code with the dependency array replaced in for the given pattern.
    """
    dep_array = Var.create(_get_dep_array(code))
    return code._replace(
        _js_expr=str(code).replace(pattern, str(dep_array)),
        merge_var_data=VarData(position=Hooks.HookPosition.POST_TRIGGER),
    )


class MonitorBase(Var):
    """Common methods for DragSourceMonitor and DropTargetMonitor."""

    def get_item_type(self) -> rx.vars.StringVar | Var[None]:
        """Returns a string or a symbol identifying the type of the current dragged item. Returns None if no item is being dragged."""
        return self.getItemType()  # type: ignore[return-value]

    def get_item(self) -> rx.vars.ObjectVar[dict[str, Any]] | Var[None]:
        """Returns a plain object representing the currently dragged item. Returns None if no item is being dragged."""
        return self.getItem()  # type: ignore[return-value]

    def get_drop_result(self) -> rx.Var:
        """Returns a plain object representing the last recorded drop result. Returns None if called outside endDrag()."""
        return self.getDropResult()  # type: ignore[return-value]

    def did_drop(self) -> rx.vars.BooleanVar:
        """Returns True if some drop target has handled the drop event, False otherwise."""
        return self.didDrop()  # type: ignore[return-value]

    def get_initial_client_offset(
        self,
    ) -> rx.vars.ObjectVar[dict[str, int]] | Var[None]:
        """Returns the {x, y} client offset of the pointer at the time when the current drag operation has started. Returns None if no item is being dragged."""
        return self.getInitialClientOffset()  # type: ignore[return-value]

    def get_initial_source_client_offset(
        self,
    ) -> rx.vars.ObjectVar[dict[str, int]] | Var[None]:
        """Returns the {x, y} client offset of the drag source component's root DOM node at the time when the current drag operation has started. Returns None if no item is being dragged."""
        return self.getInitialSourceClientOffset()  # type: ignore[return-value]

    def get_client_offset(self) -> rx.vars.ObjectVar[dict[str, int]] | Var[None]:
        """Returns the last recorded {x, y} client offset of the pointer while a drag operation is in progress. Returns None if no item is being dragged."""
        return self.getClientOffset()  # type: ignore[return-value]

    def get_difference_from_initial_offset(
        self,
    ) -> rx.vars.ObjectVar[dict[str, int]] | Var[None]:
        """Returns the {x, y} difference between the last recorded client offset of the pointer and the client offset when the current drag operation has started. Returns None if no item is being dragged."""
        return self.getDifferenceFromInitialOffset()  # type: ignore[return-value]

    def get_source_client_offset(self) -> rx.vars.ObjectVar[dict[str, int]] | Var[None]:
        """Returns the projected {x, y} client offset of the drag source component's root DOM node, based on its position at the time when the current drag operation has started, and the movement difference. Returns None if no item is being dragged."""
        return self.getSourceClientOffset()  # type: ignore[return-value]

    def __getattr__(self, name: str) -> rx.vars.FunctionVar:
        """Handle corresponding camelCase names as JS functions."""
        # Check to make sure corresponding snake case function exists.
        super().__getattribute__(to_snake_case(name))
        return rx.vars.FunctionVar(
            _js_expr=f"{self._js_expr}.{name}",
            _var_data=self._get_all_var_data(),
        )


class DragSourceMonitor(MonitorBase):
    """Monitor for useDrag hook methods."""

    def can_drag(self) -> rx.vars.BooleanVar:
        """Returns True if no drag operation is in progress, and the owner's canDrag() returns True or is not defined."""
        return self.canDrag()  # type: ignore[return-value]

    def is_dragging(self) -> rx.vars.BooleanVar:
        """Returns True if a drag operation is in progress, and either the owner initiated the drag, or its isDragging() is defined and returns True."""
        return self.isDragging()  # type: ignore[return-value]


class DropTargetMonitor(MonitorBase):
    """Monitor for useDrop hook methods."""

    def can_drop(self) -> rx.vars.BooleanVar:
        """Returns True if there is a drag operation in progress, and the owner's canDrop() returns True or is not defined."""
        return self.canDrop()  # type: ignore[return-value]

    def is_over(
        self,
        options: rx.vars.ObjectVar[dict[str, Any]] = Var.create({}),
    ) -> rx.vars.BooleanVar:
        """Returns True if there is a drag operation in progress, and the owner is the drop target that is currently being hovered.

        Args:
            options: Optional dictionary to strictly check whether only the owner is being hovered (e.g., shallow check).

        Returns:
            BooleanVar indicating whether the drop target is being hovered.
        """
        return self.isOver(options)  # type: ignore[return-value]


def use_drag(
    type: str | Var[str],
    item: ITEM_T | Callable[[DragSourceMonitor], ITEM_T] = None,
    preview_options: JsObj = None,
    options: JsObj = None,
    end: Callable[[ITEM_T, DragSourceMonitor], None]
    | Var[Callable[[ITEM_T, DragSourceMonitor], None]]
    | None = None,
    can_drag: Callable[[DragSourceMonitor], bool | Var[bool]]
    | Var[Callable[[DragSourceMonitor], bool | Var[bool]]]
    | None = None,
    is_dragging: Callable[[DragSourceMonitor], bool | Var[bool]]
    | Var[Callable[[DragSourceMonitor], bool | Var[bool]]]
    | None = None,
    collect: Callable[[DragSourceMonitor], COLLECT_PARAMS_T]
    | Var[Callable[[DragSourceMonitor], COLLECT_PARAMS_T]]
    | None = None,
    _collected_params: Var[COLLECT_PARAMS_T] | None = None,
    _drag_ref: Var | None = None,
    _drag_preview_ref: Var | None = None,
) -> tuple[
    COLLECT_PARAMS_T,  # collected params
    rx.Var,  # drag ref
    rx.Var,  # drag preview ref
]:
    """Wrapper for the useDrag hook, for advanced use cases.

    Note the functions passed to this hook are NOT event handlers in state, they
    must be provided as LambdaVar-able functions that accept Var-type arguments
    and return Var-type values. To use event handlers instead, consider using
    the high-level APIs `on_end` provided by the `Draggable` component.

    To make an element into a drag source, assign the returned drag_ref as the
    `ref` of some component:

    ```python
        collected_params, drag_ref, drag_preview_ref = use_drag(...)
        return rx.el.div(
            rx.text("Drag me"),
            custom_attrs={"ref": drag_ref},
        )
    ```

    The returned `collected_params` can be used to access the value returned by
    the `collect` function while rendering the component.

    For example, to access the `is_dragging` value:

    ```python
        collected_params, drag_ref, drag_preview_ref = use_drag(
            collect=lambda monitor: {
                "is_dragging": monitor.is_dragging(),
            }
        )
        return rx.el.div(
            rx.text("Drag me"),
            custom_attrs={"ref": drag_ref},
            opacity=rx.cond(collected_params.is_dragging, 0.5, 1),
        )
    ```

    Args:
        type: The type of the item to be dragged.
        item: The item representation, recommended to simply include an identifier.
        preview_options: Options for the drag preview.
        options: Options for the drag source ("dropEffect").
        end: Function to be called when the drag operation ends.
        can_drag: Function to determine if the item can be dragged.
        is_dragging: Function to override if a drag is in progress.
        collect: Function to collect properties to be accessed in the rendered component.
        _collected_params: Use this var for collected params instead of auto generating.
        _drag_ref: Use this var for the drag ref instead of auto generating.
        _drag_preview_ref: Use this var for the drag preview ref instead of auto generating.

    Returns:
        A tuple containing the collected params, drag ref, and drag preview ref.
    """
    spec: dict[str, Var] = {"type": Var.create(type)}
    if item is not None:
        spec["item"] = Var.create(item)
    if preview_options is not None:
        spec["previewOptions"] = Var.create(preview_options)
    if options is not None:
        spec["options"] = Var.create(options)
    if end is not None:
        spec["end"] = Var.create(end)
    if can_drag is not None:
        spec["canDrag"] = Var.create(can_drag)
    if is_dragging is not None:
        spec["isDragging"] = Var.create(is_dragging)
    if collect is not None:
        spec["collect"] = Var.create(collect)

    collected_params = (
        _collected_params
        if _collected_params is not None
        else rx.vars.ObjectVar(
            f"collected_params_{rx.vars.get_unique_variable_name()}",
            _var_type=Mapping[str, Any],
        )
    )
    drag_ref = (
        _drag_ref
        if _drag_ref is not None
        else Var(f"drag_ref_{rx.vars.get_unique_variable_name()}")
    )
    drag_preview_ref = (
        _drag_preview_ref
        if _drag_preview_ref is not None
        else Var(f"drag_preview_ref_{rx.vars.get_unique_variable_name()}")
    )
    code = _with_dep_array(
        Var(
            f"const [{collected_params}, {drag_ref}, {drag_preview_ref}] = "
            f"{_use_drag(Var.create(spec), DEP_ARRAY)};"
        )
    )
    _var_data = VarData.merge(
        code._get_all_var_data(),  # merge hook dependencies first for < 0.7.11 compat
        VarData(
            hooks={str(code): code._get_all_var_data()},
            position=Hooks.HookPosition.POST_TRIGGER,
        ),
    )
    return (
        collected_params._replace(merge_var_data=_var_data),  # type: ignore[reportReturnType]
        drag_ref._replace(merge_var_data=_var_data),
        drag_preview_ref._replace(merge_var_data=_var_data),
    )


class Draggable(BaseDnDDiv):
    """Draggable component wrapper around use_drag."""

    # Type of the draggable item. Checked by the drop target `accept` prop.
    type: Var[str]

    # The item representations, recommended to simply include an identifier.
    item: Var[JsObj | Callable[[DragSourceMonitor], JsObj]]
    # Options for the drag preview.
    preview_options: Var[JsObj]
    # Options for the drag source ("dropEffect").
    options: Var[JsObj]

    # An event handler to call when the drag operation ends.
    on_end: rx.EventHandler[rx.event.passthrough_event_spec(dict[str, Any])]

    # These are used to attach the hook to the DOM node.
    drag_ref: Var[Any]
    drag_preview_ref: Var[Any]

    # NOTE: These callables are NOT event handlers in state, they must be LambdaVar
    # Function to be called when the drag operation ends (supersedes on_end).
    end: Var[Callable[[JsObj, DragSourceMonitor], None]]
    # Predicate function to determine if the item can be dragged.
    can_drag: Var[Callable[[DragSourceMonitor], bool | Var[bool]]]
    # Predicate function to override if a drag is in progress.
    is_dragging: Var[Callable[[DragSourceMonitor], bool | Var[bool]]]
    # Function to collect properties to be accessed in the rendered component (prefer subclassing and overriding `collect_hook`).
    collect: Var[Callable[[DragSourceMonitor], JsObj]]

    def _exclude_props(self) -> list[str]:
        """Exclude props from being passed to the component."""
        return ["drag_ref", "drag_preview_ref", "on_end"]

    @classmethod
    def create(cls, *children, **props) -> Component:
        """Create a Draggable component.

        Will use the `collect_hook` to collect the params if
        not provided, which is represented by the `Draggable.CollectedParams`
        type and accessed via `Draggable.collected_params`.
        """
        if "on_end" in props:
            props.setdefault(
                "end",
                rx.EventChain.create(
                    props["on_end"],
                    args_spec=rx.event.passthrough_event_spec(dict[str, Any]),
                    key="on_end",
                ),
            )
        (
            params,
            props["drag_ref"],
            props["drag_preview_ref"],
        ) = use_drag(
            type=props.pop("type", ANY_TYPE),
            item=props.pop("item", None),
            preview_options=props.pop("preview_options", None),
            options=props.pop("options", None),
            end=props.pop("end", None),
            can_drag=props.pop("can_drag", None),
            is_dragging=props.pop("is_dragging", None),
            collect=props.pop(
                "collect",
                Var.create(
                    cls.collect_hook,
                ),
            ),
            _collected_params=props.pop(
                "_collected_params",
                cls.collected_params,
            ),
            _drag_ref=props.pop("drag_ref", None),
            _drag_preview_ref=props.pop("drag_preview_ref", None),
        )
        props.setdefault("custom_attrs", {})["ref"] = props["drag_ref"]

        return super().create(
            *children,
            **props,
            opacity=rx.cond(params.is_dragging, 0.5, 1),
        )

    class CollectedParams(TypedDict):
        """Collected params for the Draggable component."""

        is_dragging: bool
        can_drag: bool

    @staticmethod
    @static
    def collect_hook(
        monitor: DragSourceMonitor,
    ) -> rx.Var[Draggable.CollectedParams]:
        """Default collect hook for the Draggable component.

        Args:
            monitor: The drag source monitor.

        Returns:
            A dictionary with the collected properties.
        """
        return rx.Var.create(
            {
                "is_dragging": monitor.is_dragging().bool(),
                "can_drag": monitor.can_drag(),
            },
        ).to(Draggable.CollectedParams)

    # For accessing the default collected params for the Draggable component.
    collected_params: ClassVar[rx.vars.ObjectVar[Draggable.CollectedParams]] = (
        rx.vars.ObjectVar("draggableCollectedParams", _var_type=CollectedParams)
    )


def use_drop(
    accept: str | Var[str],
    options: JsObj = None,
    drop: Callable[[dict[str, Any], DropTargetMonitor], None]
    | Var[Callable[[dict[str, Any], DropTargetMonitor], None]]
    | None = None,
    hover: Callable[[dict[str, Any], DropTargetMonitor], None]
    | Var[Callable[[dict[str, Any], DropTargetMonitor], None]]
    | None = None,
    can_drop: Callable[[DropTargetMonitor], bool | Var[bool]]
    | Var[Callable[[DropTargetMonitor], bool | Var[bool]]]
    | None = None,
    collect: Callable[[DropTargetMonitor], COLLECT_PARAMS_T]
    | Var[Callable[[DropTargetMonitor], COLLECT_PARAMS_T]]
    | None = None,
    _collected_params: COLLECT_PARAMS_T | None = None,
    _drop_ref: Var | None = None,
) -> tuple[
    COLLECT_PARAMS_T,  # collected params
    rx.Var,  # drop ref
]:
    """Wrapper for the useDrop hook, for advanced use cases.

    Note the functions passed to this hook are NOT event handlers in state, they
    must be provided as LambdaVar-able functions that accept Var-type arguments
    and return Var-type values. To use event handlers instead, consider using
    the high-level APIs `on_drop` and `on_hover` provided by the `DropTarget`
    component.

    To make an element into a drop target, assign the returned drop_ref as the
    `ref` of some component:

    ```python
        collected_params, drop_ref = use_drop(...)
        return rx.el.div(
            rx.text("Drop here"),
            custom_attrs={"ref": drop_ref},
        )
    ```

    The returned `collected_params` can be used to access the value returned by
    the `collect` function while rendering the component.

    For example, to access the `is_over` value:

    ```python
        collected_params, drop_ref = use_drop(
            collect=lambda monitor: {
                "is_over": monitor.is_over(),
            }
        )
        return rx.el.div(
            rx.text("Drop here"),
            custom_attrs={"ref": drop_ref},
            background_color=rx.cond(collected_params.is_over, "green", "blue"),
        )
    ```

    Args:
        accept: The type of the item to accept.
        options: Options for the drop target.
        drop: Function to be called when an item is dropped.
        hover: Function to be called when an item is hovered.
        can_drop: Function to determine if the item can be dropped.
        collect: Function to collect properties to be accessed in the rendered component.
        _collected_params: Use this var for collected params instead of auto generating.
        _drop_ref: Use this var for the drop ref instead of auto generating.

    Returns:
        A tuple containing the collected params and the drop ref.
    """
    spec: dict[str, Var] = {"accept": Var.create(accept)}
    if options is not None:
        spec["options"] = Var.create(options)
    if drop is not None:
        spec["drop"] = Var.create(drop)
    if hover is not None:
        spec["hover"] = Var.create(hover)
    if can_drop is not None:
        spec["canDrop"] = Var.create(can_drop)
    if collect is not None:
        spec["collect"] = Var.create(collect)

    collected_params = (
        _collected_params
        if _collected_params is not None
        else rx.vars.ObjectVar(
            f"collected_params_{rx.vars.get_unique_variable_name()}",
            _var_type=Mapping[str, Any],
        )
    )
    drop_ref = (
        _drop_ref
        if _drop_ref is not None
        else Var(f"drop_ref_{rx.vars.get_unique_variable_name()}")
    )
    code = _with_dep_array(
        Var(
            f"const [{collected_params}, {drop_ref}] = "
            f"{_use_drop(Var.create(spec), DEP_ARRAY)};"
        )
    )
    _var_data = VarData.merge(
        code._get_all_var_data(),  # merge hook dependencies first for < 0.7.11 compat
        VarData(
            hooks={str(code): code._get_all_var_data()},
            position=Hooks.HookPosition.POST_TRIGGER,
        ),
    )
    return (
        collected_params._replace(merge_var_data=_var_data),  # type: ignore[reportReturnType]
        drop_ref._replace(merge_var_data=_var_data),
    )


class DropTarget(BaseDnDDiv):
    """Droppable component wrapper around use_drop."""

    # Acceptable types for the drop target
    accept: Var[str | list[str]]

    # Options for the drop target.
    options: Var[JsObj]

    # Event handler to be called when an item is dropped.
    on_drop: rx.EventHandler[rx.event.passthrough_event_spec(dict[str, Any])]

    # Event handler to be called when an item is hovered.
    on_hover: rx.EventHandler[rx.event.passthrough_event_spec(dict[str, Any])]

    # These are used to attach the hook to the DOM node, override the auto-generated value.
    drop_ref: Var[Any]

    # NOTE: These callables are NOT event handlers in state, they must be LambdaVar
    # Advanced: Function to be called when an item is dropped (supersedes on_drop)
    drop: Var[Callable[[dict[str, Any], DropTargetMonitor], None]]
    # Advanced: Function to be called when an item is hovered (supersedes on_hover)
    hover: Var[Callable[[dict[str, Any], DropTargetMonitor], None]]
    # Function to determine if the item can be dropped (must return bool).
    can_drop: Var[Callable[[dict[str, Any], DropTargetMonitor], bool | Var[bool]]]
    # Function to collect properties to be accessed in the rendered component (prefer subclassing and overriding `collect_hook`).
    collect: Var[Callable[[DropTargetMonitor], JsObj]]

    def _exclude_props(self) -> list[str]:
        """Exclude props from being passed to the component."""
        return ["drop_ref", "on_drop", "on_hover"]

    @classmethod
    def create(cls, *children, **props) -> Component:
        """Create a Droppable component.

        Will use the class `collect_hook` to collect the params if
        not provided, which is represented by the `DropTarget.CollectedParams`
        type and accessed via `DropTarget.collected_params` var.
        """
        if "on_drop" in props:
            props.setdefault(
                "drop",
                rx.EventChain.create(
                    props["on_drop"],
                    args_spec=rx.event.passthrough_event_spec(dict[str, Any]),
                    key="on_drop",
                ),
            )
        if "on_hover" in props:
            props.setdefault(
                "hover",
                rx.EventChain.create(
                    props["on_hover"],
                    args_spec=rx.event.passthrough_event_spec(dict[str, Any]),
                    key="on_hover",
                ),
            )
        (
            _,
            props["drop_ref"],
        ) = use_drop(
            accept=props.pop("accept", ANY_TYPE),
            options=props.pop("options", None),
            drop=props.pop("drop", None),
            hover=props.pop("hover", None),
            can_drop=props.pop("can_drop", None),
            collect=props.pop(
                "collect",
                Var.create(
                    cls.collect_hook,
                ),
            ),
            _collected_params=props.pop(
                "_collected_params",
                cls.collected_params,
            ),
            _drop_ref=props.pop("drop_ref", None),
        )
        props.setdefault("custom_attrs", {})["ref"] = props["drop_ref"]
        return super().create(
            *children,
            **props,
        )

    class CollectedParams(TypedDict):
        """Collected params for the DropTarget component."""

        is_over: bool
        can_drop: bool
        item: dict[str, Any] | None

    @staticmethod
    @static
    def collect_hook(
        monitor: DropTargetMonitor,
    ) -> rx.Var[DropTarget.CollectedParams]:
        """Default collect hook for the DropTarget component.

        Args:
            monitor: The drop target monitor.

        Returns:
            A dictionary with the collected properties.
        """
        return rx.Var.create(
            {
                "is_over": monitor.is_over(),
                "can_drop": monitor.can_drop(),
                "item": monitor.get_item(),
            },
        ).to(DropTarget.CollectedParams)

    # For accessing the default collected params for the DropTarget component.
    collected_params: ClassVar[rx.vars.ObjectVar[DropTarget.CollectedParams]] = (
        rx.vars.ObjectVar("dropTargetCollectedParams", _var_type=CollectedParams)
    )


class DnDNamespace(rx.ComponentNamespace):
    """Namespace for DnD components."""

    HTML5Backend: ... = HTML5Backend
    TouchBackend: ... = TouchBackend
    provider = staticmethod(DnDProvider.create)

    Draggable: type[Draggable] = Draggable
    draggable = staticmethod(Draggable.create)
    use_drag = staticmethod(use_drag)
    DragSourceMonitor: type[DragSourceMonitor] = DragSourceMonitor

    DropTarget: type[DropTarget] = DropTarget
    drop_target = staticmethod(DropTarget.create)
    use_drop = staticmethod(use_drop)
    DropTargetMonitor: type[DropTargetMonitor] = DropTargetMonitor


dnd: DnDNamespace = DnDNamespace()
