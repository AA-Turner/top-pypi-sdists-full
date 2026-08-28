from chalk._gen.chalk.artifacts.v1 import dashboard_pb2 as _dashboard_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from google.protobuf import field_mask_pb2 as _field_mask_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Iterable as _Iterable,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class DashboardAnnotation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DASHBOARD_ANNOTATION_UNSPECIFIED: _ClassVar[DashboardAnnotation]
    DASHBOARD_ANNOTATION_INCIDENT_MARKERS: _ClassVar[DashboardAnnotation]
    DASHBOARD_ANNOTATION_INCIDENT_RANGES: _ClassVar[DashboardAnnotation]
    DASHBOARD_ANNOTATION_DEPLOYMENT_MARKERS: _ClassVar[DashboardAnnotation]

class DashboardSortColumn(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DASHBOARD_SORT_COLUMN_UNSPECIFIED: _ClassVar[DashboardSortColumn]
    DASHBOARD_SORT_COLUMN_NAME: _ClassVar[DashboardSortColumn]
    DASHBOARD_SORT_COLUMN_CREATED_AT: _ClassVar[DashboardSortColumn]
    DASHBOARD_SORT_COLUMN_UPDATED_AT: _ClassVar[DashboardSortColumn]

class DashboardSortOrder(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DASHBOARD_SORT_ORDER_UNSPECIFIED: _ClassVar[DashboardSortOrder]
    DASHBOARD_SORT_ORDER_DESC: _ClassVar[DashboardSortOrder]
    DASHBOARD_SORT_ORDER_ASC: _ClassVar[DashboardSortOrder]

DASHBOARD_ANNOTATION_UNSPECIFIED: DashboardAnnotation
DASHBOARD_ANNOTATION_INCIDENT_MARKERS: DashboardAnnotation
DASHBOARD_ANNOTATION_INCIDENT_RANGES: DashboardAnnotation
DASHBOARD_ANNOTATION_DEPLOYMENT_MARKERS: DashboardAnnotation
DASHBOARD_SORT_COLUMN_UNSPECIFIED: DashboardSortColumn
DASHBOARD_SORT_COLUMN_NAME: DashboardSortColumn
DASHBOARD_SORT_COLUMN_CREATED_AT: DashboardSortColumn
DASHBOARD_SORT_COLUMN_UPDATED_AT: DashboardSortColumn
DASHBOARD_SORT_ORDER_UNSPECIFIED: DashboardSortOrder
DASHBOARD_SORT_ORDER_DESC: DashboardSortOrder
DASHBOARD_SORT_ORDER_ASC: DashboardSortOrder

class DashboardControls(_message.Message):
    __slots__ = ("default_range_preset_id", "annotations")
    DEFAULT_RANGE_PRESET_ID_FIELD_NUMBER: _ClassVar[int]
    ANNOTATIONS_FIELD_NUMBER: _ClassVar[int]
    default_range_preset_id: str
    annotations: _containers.RepeatedScalarFieldContainer[DashboardAnnotation]
    def __init__(
        self,
        default_range_preset_id: _Optional[str] = ...,
        annotations: _Optional[_Iterable[_Union[DashboardAnnotation, str]]] = ...,
    ) -> None: ...

class CreateDashboardRequest(_message.Message):
    __slots__ = ("dashboard", "controls")
    DASHBOARD_FIELD_NUMBER: _ClassVar[int]
    CONTROLS_FIELD_NUMBER: _ClassVar[int]
    dashboard: _dashboard_pb2.Dashboard
    controls: DashboardControls
    def __init__(
        self,
        dashboard: _Optional[_Union[_dashboard_pb2.Dashboard, _Mapping]] = ...,
        controls: _Optional[_Union[DashboardControls, _Mapping]] = ...,
    ) -> None: ...

class CreateDashboardResponse(_message.Message):
    __slots__ = ("dashboard", "controls")
    DASHBOARD_FIELD_NUMBER: _ClassVar[int]
    CONTROLS_FIELD_NUMBER: _ClassVar[int]
    dashboard: _dashboard_pb2.Dashboard
    controls: DashboardControls
    def __init__(
        self,
        dashboard: _Optional[_Union[_dashboard_pb2.Dashboard, _Mapping]] = ...,
        controls: _Optional[_Union[DashboardControls, _Mapping]] = ...,
    ) -> None: ...

class GetDashboardRequest(_message.Message):
    __slots__ = ("dashboard_id", "read_mask")
    DASHBOARD_ID_FIELD_NUMBER: _ClassVar[int]
    READ_MASK_FIELD_NUMBER: _ClassVar[int]
    dashboard_id: str
    read_mask: _field_mask_pb2.FieldMask
    def __init__(
        self,
        dashboard_id: _Optional[str] = ...,
        read_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...,
    ) -> None: ...

class GetDashboardResponse(_message.Message):
    __slots__ = ("dashboard", "controls")
    DASHBOARD_FIELD_NUMBER: _ClassVar[int]
    CONTROLS_FIELD_NUMBER: _ClassVar[int]
    dashboard: _dashboard_pb2.Dashboard
    controls: DashboardControls
    def __init__(
        self,
        dashboard: _Optional[_Union[_dashboard_pb2.Dashboard, _Mapping]] = ...,
        controls: _Optional[_Union[DashboardControls, _Mapping]] = ...,
    ) -> None: ...

class ListDashboardsRequest(_message.Message):
    __slots__ = ("limit", "cursor", "read_mask", "search", "created_by", "sort_column", "sort_order")
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    READ_MASK_FIELD_NUMBER: _ClassVar[int]
    SEARCH_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    SORT_COLUMN_FIELD_NUMBER: _ClassVar[int]
    SORT_ORDER_FIELD_NUMBER: _ClassVar[int]
    limit: int
    cursor: str
    read_mask: _field_mask_pb2.FieldMask
    search: str
    created_by: _containers.RepeatedScalarFieldContainer[str]
    sort_column: DashboardSortColumn
    sort_order: DashboardSortOrder
    def __init__(
        self,
        limit: _Optional[int] = ...,
        cursor: _Optional[str] = ...,
        read_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...,
        search: _Optional[str] = ...,
        created_by: _Optional[_Iterable[str]] = ...,
        sort_column: _Optional[_Union[DashboardSortColumn, str]] = ...,
        sort_order: _Optional[_Union[DashboardSortOrder, str]] = ...,
    ) -> None: ...

class ListDashboardsResponse(_message.Message):
    __slots__ = ("dashboards", "next_cursor")
    DASHBOARDS_FIELD_NUMBER: _ClassVar[int]
    NEXT_CURSOR_FIELD_NUMBER: _ClassVar[int]
    dashboards: _containers.RepeatedCompositeFieldContainer[_dashboard_pb2.Dashboard]
    next_cursor: str
    def __init__(
        self,
        dashboards: _Optional[_Iterable[_Union[_dashboard_pb2.Dashboard, _Mapping]]] = ...,
        next_cursor: _Optional[str] = ...,
    ) -> None: ...

class UpdateDashboardRequest(_message.Message):
    __slots__ = ("dashboard", "controls", "update_mask")
    DASHBOARD_FIELD_NUMBER: _ClassVar[int]
    CONTROLS_FIELD_NUMBER: _ClassVar[int]
    UPDATE_MASK_FIELD_NUMBER: _ClassVar[int]
    dashboard: _dashboard_pb2.Dashboard
    controls: DashboardControls
    update_mask: _field_mask_pb2.FieldMask
    def __init__(
        self,
        dashboard: _Optional[_Union[_dashboard_pb2.Dashboard, _Mapping]] = ...,
        controls: _Optional[_Union[DashboardControls, _Mapping]] = ...,
        update_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...,
    ) -> None: ...

class UpdateDashboardResponse(_message.Message):
    __slots__ = ("dashboard", "controls")
    DASHBOARD_FIELD_NUMBER: _ClassVar[int]
    CONTROLS_FIELD_NUMBER: _ClassVar[int]
    dashboard: _dashboard_pb2.Dashboard
    controls: DashboardControls
    def __init__(
        self,
        dashboard: _Optional[_Union[_dashboard_pb2.Dashboard, _Mapping]] = ...,
        controls: _Optional[_Union[DashboardControls, _Mapping]] = ...,
    ) -> None: ...

class DeleteDashboardRequest(_message.Message):
    __slots__ = ("dashboard_id",)
    DASHBOARD_ID_FIELD_NUMBER: _ClassVar[int]
    dashboard_id: str
    def __init__(self, dashboard_id: _Optional[str] = ...) -> None: ...

class DeleteDashboardResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ExportDashboardRequest(_message.Message):
    __slots__ = ("dashboard_id",)
    DASHBOARD_ID_FIELD_NUMBER: _ClassVar[int]
    dashboard_id: str
    def __init__(self, dashboard_id: _Optional[str] = ...) -> None: ...

class ExportDashboardResponse(_message.Message):
    __slots__ = ("dashboard_json_string",)
    DASHBOARD_JSON_STRING_FIELD_NUMBER: _ClassVar[int]
    dashboard_json_string: str
    def __init__(self, dashboard_json_string: _Optional[str] = ...) -> None: ...

class ImportDashboardRequest(_message.Message):
    __slots__ = ("dashboard_json_string", "name", "dry_run")
    DASHBOARD_JSON_STRING_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DRY_RUN_FIELD_NUMBER: _ClassVar[int]
    dashboard_json_string: str
    name: str
    dry_run: bool
    def __init__(
        self, dashboard_json_string: _Optional[str] = ..., name: _Optional[str] = ..., dry_run: bool = ...
    ) -> None: ...

class ImportDashboardResponse(_message.Message):
    __slots__ = ("dashboard",)
    DASHBOARD_FIELD_NUMBER: _ClassVar[int]
    dashboard: _dashboard_pb2.Dashboard
    def __init__(self, dashboard: _Optional[_Union[_dashboard_pb2.Dashboard, _Mapping]] = ...) -> None: ...
