"""ag-grid rx.model wrapper."""

from __future__ import annotations

import datetime
import enum
import json
from typing import Any, ClassVar, Generic, Sequence, Type, get_args

import reflex as rx
from reflex.event import EventCallback, EventSpec
from reflex.utils import console
from reflex.utils.serializers import serialize
from reflex.utils.types import is_optional, is_union
from reflex.vars.function import FunctionStringVar
from sqlalchemy.inspection import inspect
from sqlmodel import col, func, select
from starlette.requests import Request
from starlette.responses import JSONResponse

from reflex_enterprise.components.ag_grid import ag_grid
from reflex_enterprise.components.ag_grid.datasource import (
    DATASOURCE_PARAMS,
    Datasource,
    DatasourceParams,
    LoadSuccessParams,
    SSRMDatasource,
    SSRMDatasourceRequestParams,
)
from reflex_enterprise.components.ag_grid.handlers import (
    M,
    apply_filter_model,
    apply_sort_model,
)
from reflex_enterprise.components.ag_grid.resources import ColumnDef


class ReflexJSONResponse(JSONResponse):
    """Custom JSONResponse that uses Reflex's serializer."""

    def render(self, content: Any) -> bytes:
        """Render content using Reflex's serializer."""
        return json.dumps(content, default=serialize).encode("utf-8")


def _value_setter_signature(
    params: rx.Var[dict[str, Any]],
) -> tuple[rx.Var[dict], rx.Var[str], rx.Var[Any]]:
    return (
        params["data"],  # pyright: ignore [reportIndexIssue]
        params["colDef"].to(dict)["field"],  # pyright: ignore [reportIndexIssue]
        params["newValue"],  # pyright: ignore [reportIndexIssue]
    )


def get_default_column_def(
    field: str,
    ftype: Type,
    value_setter: rx.EventHandler | EventCallback | None = None,
    **cdef_kwargs,
) -> ColumnDef:
    """Get a default column definition for a given field type.

    Args:
        field: The field name.
        ftype: The field type.
        value_setter: The value setter event handler.
        **cdef_kwargs: Additional ColumnDef keyword arguments.

    Returns:
        The column definition.
    """
    _cdef_kwargs = {
        "sortable": True,
        "filter": True,
        "editable": value_setter is not None,
        "cell_editor": ag_grid.editors.text,
    }
    _cdef_kwargs.update(cdef_kwargs)
    cdef = ag_grid.column_def(
        field=field,
        **_cdef_kwargs,
    )
    if is_optional(ftype):
        ftype = get_args(ftype)[0]
    if ftype in (int, float, bool):
        cdef.type = "numericColumn"
        cdef.filter = ag_grid.filters.number
        cdef.cell_editor = ag_grid.editors.number
        cdef.cell_data_type = "number"
    if ftype is bool:
        cdef.cell_renderer = ag_grid.renderers.checkbox_cell
        cdef.cell_editor = ag_grid.editors.checkbox
        cdef.cell_data_type = "boolean"
    if ftype is datetime.datetime:
        cdef.filter = ag_grid.filters.date
        cdef.cell_editor = ag_grid.editors.date
    if value_setter is not None:
        cdef.value_setter = rx.EventChain(
            events=[
                rx.event.call_event_handler(
                    value_setter,  # pyright: ignore [reportArgumentType]
                    _value_setter_signature,
                ),
            ],
            args_spec=_value_setter_signature,
            # XXX: hacks to queue events from call_script eval context
            invocation=rx.vars.function.ArgsFunctionOperation.create(
                args_names=["events"],
                return_expr=rx.Var(
                    "queueEvents(events, {current: socket}, false, navigate, params)"
                ),
            ),
        )
    return cdef


class AbstractWrapper(rx.ComponentState, Generic[DATASOURCE_PARAMS]):
    """Abstract class for wrapping ag-grid for infinite data model."""

    _grid_component: ClassVar[rx.Component | None] = None
    _selected_items: list[Any] = []

    __data_route__: ClassVar[str] = "/abstract-wrapper-data"
    __get_data_kwargs__: ClassVar[dict[str, Any]] = {
        "state": lambda self: self.get_full_name()
    }
    __data_source_params_class__: Type[DATASOURCE_PARAMS] = DatasourceParams  # pyright: ignore [reportAssignmentType]

    @classmethod
    def _add_data_route(cls):
        """Add the backend __data_route__ that responds to ag-grid data requests.

        The backend route will call the _get_data method to fetch the data.
        """
        app = rx.utils.prerequisites.get_app().app  # pyright: ignore [reportAttributeAccessIssue]

        # Check if route already exists
        for route in app._api.router.routes:
            if hasattr(route, "path") and route.path == cls.__data_route__:
                return

        async def get_data(request: Request):
            # Extract state from query params
            state = request.query_params.get("state", "")

            try:
                client_token = request.headers["X-Reflex-Client-Token"]
            except KeyError:
                return ReflexJSONResponse([])
            state_cls = rx.State.get_class_substate(tuple(state.split(".")))
            # Get the correct params class from the actual state class, not the closure
            params = state_cls.__data_source_params_class__.from_request(  # pyright: ignore [reportAttributeAccessIssue, reportArgumentType]
                request.query_params
            )
            token = rx.BaseStateToken(ident=client_token, cls=state_cls)
            async with app.modify_state(token) as _state:
                s_instance = await _state.get_state(state_cls)
                result = s_instance._get_data(params)
                if hasattr(result, "__await__"):
                    result = await result
                return ReflexJSONResponse(result)

        # Add route using Starlette's add_route method
        app._api.add_route(cls.__data_route__, get_data, methods=["GET"])

    def _get_datasource_kwargs(self) -> dict[str, Any]:
        """Get additional kwargs to pass in the datasource URI -- accessed during on_mount."""
        return {
            key: value if not callable(value) else value(self)
            for key, value in self.__get_data_kwargs__.items()
        }

    async def _set_datasource(self) -> EventSpec:
        """Set the datasource for the grid.

        This is called during on_mount.
        """
        ds = Datasource(
            endpoint_uri=self.__data_route__,
            endpoint_kwargs=self._get_datasource_kwargs(),
            rowCount=await self._row_count(),
        )
        return self._grid_component.api.set_grid_option(  # pyright: ignore [reportAttributeAccessIssue, reportOptionalMemberAccess]
            "datasource", ds
        )

    @rx.event
    async def on_mount(self):
        """Perform post-hydration grid initialization.

        Set up column defs and data source to fetch infinite row data.
        """
        return [
            self._grid_component.api.set_grid_option(  # pyright: ignore [reportAttributeAccessIssue, reportOptionalMemberAccess]
                "columnDefs", self._get_column_defs()
            ),
            await self._set_datasource(),
        ]

    @rx.event
    async def refresh(self):
        """Refresh the grid data."""
        return await self.on_mount()

    @rx.event
    def on_selection_changed(self, rows: list[dict], source: dict, type: str):
        """Handle selection changed event."""
        self._selected_items = rows

    @rx.event
    def on_value_setter(self, row_data: dict[str, Any], field_name: str, value: Any):
        """Handle setting value in the model."""
        raise NotImplementedError("Handle setting value in the model.")

    def _get_column_defs(self) -> list[ColumnDef]:
        """Get the column definitions for the grid, must be overridden."""
        raise NotImplementedError("Handle fetching column definitions.")

    def _get_data(
        self,
        params: DATASOURCE_PARAMS,
    ) -> list[dict[str, Any]]:
        """Get the data for the grid, must be overridden."""
        raise NotImplementedError("Handle fetching data from the model.")

    async def _row_count(self) -> int:
        """Get the total row count for the grid, must be overridden."""
        raise NotImplementedError("Handle fetching row count.")

    @classmethod
    def _default_grid_props(cls) -> dict[str, Any]:
        return {
            "id": f"ag-grid-{cls.get_full_name()}",
            "default_col_def": {"flex": 1},
            "max_blocks_in_cache": 4,
            "cache_block_size": 50,
            "group_default_expanded": None,
            "row_model_type": "infinite",
        }

    @classmethod
    def get_component(cls, *children, **props) -> rx.Component:
        """Return the Ag-Grid component linked to the wrapper state.

        Args:
            children: The children components passed to ag_grid, typically not used.
            **props: Additional props for the ag_grid component.

        Note that "column_defs", "row_model_type", "on_mount", and
        "on_selection_changed" cannot be passed here.

        Returns:
            The Ag-Grid component.
        """
        _props = cls._default_grid_props()
        _props.update(props)
        return ag_grid.root(
            *children,
            on_mount=cls.on_mount,
            on_selection_changed=cls.on_selection_changed,  # pyright: ignore [reportArgumentType]
            **_props,
        )

    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        """Create the ComponentState instance.

        Args:
            children: The children components passed to ag_grid, typically not used.
            **props: Additional props for the ag_grid component.

        Note that "column_defs", "row_model_type", "on_mount", and
        "on_selection_change" cannot be passed here.

        Returns:
            The Ag-Grid component linked to the wrapper state.
        """
        comp = super().create(*children, **props)
        comp.State._grid_component = comp  # pyright: ignore [reportAttributeAccessIssue, reportOptionalMemberAccess]
        comp.State._add_data_route()  # pyright: ignore [reportAttributeAccessIssue, reportOptionalMemberAccess]
        return comp


class ModelWrapperActionType(enum.Enum):
    """ModelWrapper action types."""

    SELECT = "select"
    INSERT = "insert"
    UPDATE = "update"
    DELETE = "delete"


class ModelWrapperBase(
    AbstractWrapper[DATASOURCE_PARAMS], Generic[DATASOURCE_PARAMS, M]
):
    """Ag-Grid wrapper for arbitrary rx.Model class."""

    _model_class: ClassVar[Type[M] | None] = None  # pyright: ignore [reportGeneralTypeIssues]
    _primary_key: ClassVar[tuple[str, ...]] = ("id",)
    _selected_items: list[M] = []
    add_dialog_is_open: bool = False

    @rx.event
    def set_add_dialog_is_open(self, value: bool):
        """Set whether the add dialog is open."""
        self.add_dialog_is_open = value

    async def _is_authorized(
        self,
        action: ModelWrapperActionType,
        action_data: Sequence[M] | dict[str, Any] | None,
    ) -> bool:
        """Check if the user is authorized to perform the action.

        For SELECT, action_data is None.
        For INSERT, action_data is a dictionary of the new row data.
        For UPDATE, action data is a dictionary of updated row data.
        For DELETE, action data is a list of model objects to delete.

        Args:
            action: The action type.
            action_data: The data associated with the action.

        Returns:
            True if authorized, False otherwise.
        """
        return True

    @rx.event
    def on_selection_changed(self, rows: list[dict], source: Any, type: Any):
        """Handle selection changed event."""
        if self._model_class:
            self._selected_items = [self._model_class(**row) for row in rows]

    @classmethod
    def _annotation_for(cls, fname: str) -> Type:
        if cls._model_class is None:
            return type(None)
        field = cls._model_class.__fields__[fname]
        type_ = field.type_ if hasattr(field, "type_") else field.annotation  # pyright: ignore [reportAttributeAccessIssue]
        if is_optional(type_) or is_union(type_):
            type_ = get_args(type_)[0]
        return type_  # pyright: ignore [reportReturnType]

    @classmethod
    def _default_sort_model(cls) -> list[dict[str, str]]:
        return [{"colId": pkf, "sort": "asc"} for pkf in cls._primary_key]

    @rx.event
    async def on_value_setter(
        self, row_data: dict[str, Any], field_name: str, value: Any
    ):
        """Handles setting a value in the model."""
        if not self._model_class:
            return

        if not await self._is_authorized(
            ModelWrapperActionType.UPDATE, row_data | {field_name: value}
        ):
            return
        try:
            if self._annotation_for(field_name) == datetime.datetime:
                value = datetime.datetime.fromisoformat(value)
        except KeyError:
            pass

        async with rx.asession() as session:
            item_orm = await session.get(
                self._model_class,
                tuple(
                    self._annotation_for(pkf)(row_data[pkf])
                    for pkf in self._primary_key
                ),
            )
            if item_orm is not None:
                setattr(item_orm, field_name, value)
                session.add(item_orm)
                await session.commit()
                return await self.refresh()

    @rx.event
    async def on_add(self, row_data: dict[str, Any]):
        """Handles submitting a new row to the model."""
        if not self._model_class:
            return
        if not await self._is_authorized(ModelWrapperActionType.INSERT, row_data):
            return
        async with rx.asession() as session:
            item = self._model_class(**row_data)
            session.add(item)
            await session.commit()
            self.add_dialog_is_open = False
            return await self.refresh()

    @rx.event
    async def delete_selected(self):
        """Handles deleting selected rows from the model."""
        if not self._model_class:
            return
        if not await self._is_authorized(
            ModelWrapperActionType.DELETE, self._selected_items
        ):
            return
        async with rx.asession() as session:
            for item in self._selected_items:
                item = await session.get(
                    self._model_class,
                    tuple(getattr(item, pkf) for pkf in self._primary_key),
                )  # pyright: ignore [reportAttributeAccessIssue, reportOptionalMemberAccess]
                await session.delete(item)
            await session.commit()
            self._selected_items = []  # they're deleted now.
            return [
                self._grid_component.api.deselect_all(),  # pyright: ignore [reportAttributeAccessIssue, reportOptionalMemberAccess]
                await self.refresh(),
            ]

    def _get_column_defs(self) -> list[ColumnDef]:
        if not self._model_class:
            return []
        return [
            get_default_column_def(
                field=field.name if hasattr(field, "name") else field_name,  # pyright: ignore [reportAttributeAccessIssue]
                ftype=field.type_ if hasattr(field, "type_") else field.annotation,  # pyright: ignore [reportAttributeAccessIssue,reportArgumentType]
                value_setter=type(self).on_value_setter,
                editable=field_name not in self._primary_key,
            )
            for field_name, field in self._model_class.__fields__.items()
        ]

    async def _row_count(self) -> int:
        if not self._model_class:
            return 0
        async with rx.asession() as session:
            return (
                await session.exec(
                    select(
                        func.count(
                            col(getattr(self._model_class, self._primary_key[0]))
                        )
                    )
                )
            ).one()

    @rx.var(interval=10, auto_deps=False, initial_value=0)
    async def row_count_cached(self) -> int:
        """Get the cached row count for the grid."""
        return await self._row_count()

    @classmethod
    def _add_dialog_field(cls, field: str, ftype: Type) -> rx.Component:
        comp = rx.input(name=field)
        orig_type_str = str(ftype)
        if is_optional(ftype):
            ftype = get_args(ftype)[0]
        if ftype in (int, float):
            comp = rx.input(
                name=field,
                type="number",
            )
        if ftype is bool:
            comp = rx.checkbox(id=field)
        return rx.table.row(
            rx.table.cell(rx.text(field)),
            rx.table.cell(comp),
            rx.table.cell(rx.text(f"({orig_type_str})")),
        )

    @classmethod
    def _add_dialog(cls) -> rx.Component:
        """Create the dialog for adding a new row."""
        if not cls._model_class:
            return rx.text("No model class specified.")
        return rx.dialog.root(
            rx.dialog.trigger(
                rx.icon_button("plus"),
            ),
            rx.dialog.content(
                rx.dialog.title(f"Add new {cls._model_class.__name__}"),
                rx.form(
                    rx.table.root(
                        *[
                            cls._add_dialog_field(
                                field.name if hasattr(field, "name") else field_name,  # pyright: ignore [reportAttributeAccessIssue]
                                field.type_  # pyright: ignore [reportAttributeAccessIssue,reportArgumentType]
                                if hasattr(field, "type_")
                                else field.annotation,  # pyright: ignore [reportAttributeAccessIssue]
                            )
                            for field_name, field in cls._model_class.__fields__.items()
                            if field_name not in cls._primary_key
                        ]
                    ),
                    rx.button("Add", margin="5px"),
                    on_submit=cls.on_add,
                ),
            ),
            open=cls.add_dialog_is_open,
            on_open_change=cls.set_add_dialog_is_open,
        )

    @classmethod
    def _delete_button(cls) -> rx.Component:
        """Create the delete button."""
        return rx.icon_button(
            "trash-2",
            on_click=cls.delete_selected,
        )

    @classmethod
    def _top_toolbar(cls) -> rx.Component:
        """Create the top toolbar."""
        return rx.hstack(
            cls._delete_button(),
            cls._add_dialog(),
            justify="end",
            margin="5px",
        )

    @classmethod
    def get_component(cls, *children, model_class: Type[M], **props) -> rx.Component:
        """Get the component for the specified model class."""
        cls._model_class = model_class  # pyright: ignore [reportAttributeAccessIssue, reportOptionalMemberAccess]
        cls._primary_key = tuple(  # pyright: ignore [reportAttributeAccessIssue]
            key.name
            for key in inspect(model_class).primary_key  # pyright: ignore [reportOptionalMemberAccess]
        )
        return super().get_component(*children, **props)

    @classmethod
    def create(cls, *children, model_class: Type[M], **props) -> rx.Component:
        """Create the Wrapper instance."""
        comp = super().create(*children, model_class=model_class, **props)
        if not comp.State:
            console.debug(
                f"No State class found for ModelWrapper of {model_class.__class__.__name__}"
            )
            return comp
        frag = rx.fragment(
            comp.State._top_toolbar(),  # pyright: ignore [reportAttributeAccessIssue]
            comp,
            State=comp.State,
        )
        frag.api = comp.api  # pyright: ignore [reportAttributeAccessIssue, reportOptionalMemberAccess]
        return frag


class ModelWrapper(ModelWrapperBase[DatasourceParams, M], Generic[M]):
    """Wrapper for arbitrary rx.Model class with infinite row model."""

    @rx.event
    async def refresh(self):
        """Refresh the grid data."""
        if not self._model_class:
            return
        return self._grid_component.api.refreshInfiniteCache()  # pyright: ignore [reportAttributeAccessIssue, reportOptionalMemberAccess]

    async def _get_data(
        self,
        params: DatasourceParams,
    ) -> Sequence[M] | tuple[Sequence[M], int]:
        if not self._model_class:
            return []
        if not await self._is_authorized(ModelWrapperActionType.SELECT, None):
            return []
        async with rx.asession() as session:
            result = await session.exec(  # pyright: ignore [reportReturnType]
                apply_sort_model(
                    model=self._model_class,
                    query=apply_filter_model(
                        model=self._model_class,
                        filter_model=params.filterModel or {},
                    ),
                    sort_model=params.sortModel or self._default_sort_model(),
                )
                .offset(params.startRow)
                .limit(params.endRow - params.startRow)
            )
            return result.all(), await self.row_count_cached


class ModelWrapperSSRM(ModelWrapperBase[SSRMDatasourceRequestParams, M], Generic[M]):
    """Wrapper for arbitrary rx.Model class with SSRM."""

    __data_source_params_class__: DATASOURCE_PARAMS = SSRMDatasourceRequestParams  # pyright: ignore [reportIncompatibleVariableOverride, reportGeneralTypeIssues]

    @classmethod
    def _default_grid_props(cls) -> dict[str, Any]:
        row_id_parts = [f"${{params.data['{key}']}}" for key in cls._primary_key]
        return {
            **super()._default_grid_props(),
            "row_model_type": "serverSide",
            "get_row_id": FunctionStringVar(f"(params) => `{''.join(row_id_parts)}`"),
            "enterprise_modules": {
                "ServerSideRowModelModule",
                "ServerSideRowModelApiModule",
            },
        }

    async def _set_datasource(self) -> EventSpec:
        return self._grid_component.api.set_grid_option(  # pyright: ignore [reportAttributeAccessIssue, reportOptionalMemberAccess]
            "serverSideDatasource",
            SSRMDatasource(
                endpoint_uri=self.__data_route__,
                endpoint_kwargs=self._get_datasource_kwargs(),
                rowCount=0,
            ),
        )

    @rx.event
    async def refresh(self):
        """Refresh the grid data."""
        if not self._model_class:
            return
        return self._grid_component.api.refreshServerSide()  # pyright: ignore [reportAttributeAccessIssue, reportOptionalMemberAccess]

    async def _get_data(
        self,
        params: SSRMDatasourceRequestParams,
    ) -> Sequence[M] | LoadSuccessParams[M]:
        if not self._model_class:
            return []
        if not await self._is_authorized(ModelWrapperActionType.SELECT, None):
            return []
        async with rx.asession() as session:
            result = await session.exec(  # pyright: ignore [reportReturnType]
                apply_sort_model(
                    model=self._model_class,
                    query=apply_filter_model(
                        model=self._model_class,
                        filter_model=params.filterModel or {},
                    ),
                    sort_model=params.sortModel or self._default_sort_model(),
                )
                .offset(params.start_row)
                .limit(params.end_row - params.start_row)
            )
            return {
                "rowData": result.all(),
                "rowCount": await self.row_count_cached,
            }


model_wrapper = ModelWrapper.create
model_wrapper_ssrm = ModelWrapperSSRM.create
