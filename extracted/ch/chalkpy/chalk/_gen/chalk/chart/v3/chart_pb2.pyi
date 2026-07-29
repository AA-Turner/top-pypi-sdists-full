from chalk._gen.chalk.arrow.v1 import arrow_pb2 as _arrow_pb2
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

class AxisKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    AXIS_KIND_UNSPECIFIED: _ClassVar[AxisKind]
    AXIS_KIND_LINEAR: _ClassVar[AxisKind]
    AXIS_KIND_LOG: _ClassVar[AxisKind]
    AXIS_KIND_SYMLOG: _ClassVar[AxisKind]
    AXIS_KIND_TIME: _ClassVar[AxisKind]
    AXIS_KIND_CATEGORY: _ClassVar[AxisKind]

class AxisPosition(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    AXIS_POSITION_UNSPECIFIED: _ClassVar[AxisPosition]
    AXIS_POSITION_BOTTOM: _ClassVar[AxisPosition]
    AXIS_POSITION_LEFT: _ClassVar[AxisPosition]
    AXIS_POSITION_RIGHT: _ClassVar[AxisPosition]
    AXIS_POSITION_TOP: _ClassVar[AxisPosition]

class DrawStyle(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DRAW_STYLE_UNSPECIFIED: _ClassVar[DrawStyle]
    DRAW_STYLE_LINE: _ClassVar[DrawStyle]
    DRAW_STYLE_BARS: _ClassVar[DrawStyle]
    DRAW_STYLE_POINTS: _ClassVar[DrawStyle]

class StackingMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STACKING_MODE_UNSPECIFIED: _ClassVar[StackingMode]
    STACKING_MODE_NONE: _ClassVar[StackingMode]
    STACKING_MODE_ZERO: _ClassVar[StackingMode]
    STACKING_MODE_NORMALIZE: _ClassVar[StackingMode]
    STACKING_MODE_CENTER: _ClassVar[StackingMode]

class NullValueMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NULL_VALUE_MODE_UNSPECIFIED: _ClassVar[NullValueMode]
    NULL_VALUE_MODE_GAP: _ClassVar[NullValueMode]
    NULL_VALUE_MODE_CONNECTED: _ClassVar[NullValueMode]
    NULL_VALUE_MODE_AS_ZERO: _ClassVar[NullValueMode]

class LineInterpolation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LINE_INTERPOLATION_UNSPECIFIED: _ClassVar[LineInterpolation]
    LINE_INTERPOLATION_LINEAR: _ClassVar[LineInterpolation]
    LINE_INTERPOLATION_SMOOTH: _ClassVar[LineInterpolation]
    LINE_INTERPOLATION_STEP_BEFORE: _ClassVar[LineInterpolation]
    LINE_INTERPOLATION_STEP_AFTER: _ClassVar[LineInterpolation]

class Orientation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ORIENTATION_UNSPECIFIED: _ClassVar[Orientation]
    ORIENTATION_VERTICAL: _ClassVar[Orientation]
    ORIENTATION_HORIZONTAL: _ClassVar[Orientation]

class LegendPlacement(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LEGEND_PLACEMENT_UNSPECIFIED: _ClassVar[LegendPlacement]
    LEGEND_PLACEMENT_BOTTOM: _ClassVar[LegendPlacement]
    LEGEND_PLACEMENT_RIGHT: _ClassVar[LegendPlacement]
    LEGEND_PLACEMENT_HIDDEN: _ClassVar[LegendPlacement]

AXIS_KIND_UNSPECIFIED: AxisKind
AXIS_KIND_LINEAR: AxisKind
AXIS_KIND_LOG: AxisKind
AXIS_KIND_SYMLOG: AxisKind
AXIS_KIND_TIME: AxisKind
AXIS_KIND_CATEGORY: AxisKind
AXIS_POSITION_UNSPECIFIED: AxisPosition
AXIS_POSITION_BOTTOM: AxisPosition
AXIS_POSITION_LEFT: AxisPosition
AXIS_POSITION_RIGHT: AxisPosition
AXIS_POSITION_TOP: AxisPosition
DRAW_STYLE_UNSPECIFIED: DrawStyle
DRAW_STYLE_LINE: DrawStyle
DRAW_STYLE_BARS: DrawStyle
DRAW_STYLE_POINTS: DrawStyle
STACKING_MODE_UNSPECIFIED: StackingMode
STACKING_MODE_NONE: StackingMode
STACKING_MODE_ZERO: StackingMode
STACKING_MODE_NORMALIZE: StackingMode
STACKING_MODE_CENTER: StackingMode
NULL_VALUE_MODE_UNSPECIFIED: NullValueMode
NULL_VALUE_MODE_GAP: NullValueMode
NULL_VALUE_MODE_CONNECTED: NullValueMode
NULL_VALUE_MODE_AS_ZERO: NullValueMode
LINE_INTERPOLATION_UNSPECIFIED: LineInterpolation
LINE_INTERPOLATION_LINEAR: LineInterpolation
LINE_INTERPOLATION_SMOOTH: LineInterpolation
LINE_INTERPOLATION_STEP_BEFORE: LineInterpolation
LINE_INTERPOLATION_STEP_AFTER: LineInterpolation
ORIENTATION_UNSPECIFIED: Orientation
ORIENTATION_VERTICAL: Orientation
ORIENTATION_HORIZONTAL: Orientation
LEGEND_PLACEMENT_UNSPECIFIED: LegendPlacement
LEGEND_PLACEMENT_BOTTOM: LegendPlacement
LEGEND_PLACEMENT_RIGHT: LegendPlacement
LEGEND_PLACEMENT_HIDDEN: LegendPlacement

class TabularData(_message.Message):
    __slots__ = ("arrow_ipc",)
    ARROW_IPC_FIELD_NUMBER: _ClassVar[int]
    arrow_ipc: bytes
    def __init__(self, arrow_ipc: _Optional[bytes] = ...) -> None: ...

class Axis(_message.Message):
    __slots__ = (
        "id",
        "kind",
        "position",
        "label",
        "unit",
        "soft_min",
        "soft_max",
        "log_base",
        "symlog_threshold",
        "offset",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    UNIT_FIELD_NUMBER: _ClassVar[int]
    SOFT_MIN_FIELD_NUMBER: _ClassVar[int]
    SOFT_MAX_FIELD_NUMBER: _ClassVar[int]
    LOG_BASE_FIELD_NUMBER: _ClassVar[int]
    SYMLOG_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    id: str
    kind: AxisKind
    position: AxisPosition
    label: str
    unit: str
    soft_min: float
    soft_max: float
    log_base: float
    symlog_threshold: float
    offset: int
    def __init__(
        self,
        id: _Optional[str] = ...,
        kind: _Optional[_Union[AxisKind, str]] = ...,
        position: _Optional[_Union[AxisPosition, str]] = ...,
        label: _Optional[str] = ...,
        unit: _Optional[str] = ...,
        soft_min: _Optional[float] = ...,
        soft_max: _Optional[float] = ...,
        log_base: _Optional[float] = ...,
        symlog_threshold: _Optional[float] = ...,
        offset: _Optional[int] = ...,
    ) -> None: ...

class Stacking(_message.Message):
    __slots__ = ("group", "mode")
    GROUP_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    group: str
    mode: StackingMode
    def __init__(self, group: _Optional[str] = ..., mode: _Optional[_Union[StackingMode, str]] = ...) -> None: ...

class BinnedX(_message.Message):
    __slots__ = ("x_min_column", "x_max_column", "expected_step")
    X_MIN_COLUMN_FIELD_NUMBER: _ClassVar[int]
    X_MAX_COLUMN_FIELD_NUMBER: _ClassVar[int]
    EXPECTED_STEP_FIELD_NUMBER: _ClassVar[int]
    x_min_column: str
    x_max_column: str
    expected_step: float
    def __init__(
        self,
        x_min_column: _Optional[str] = ...,
        x_max_column: _Optional[str] = ...,
        expected_step: _Optional[float] = ...,
    ) -> None: ...

class GroupTag(_message.Message):
    __slots__ = ("group_key", "value")
    GROUP_KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    group_key: str
    value: _arrow_pb2.ScalarValue
    def __init__(
        self, group_key: _Optional[str] = ..., value: _Optional[_Union[_arrow_pb2.ScalarValue, _Mapping]] = ...
    ) -> None: ...

class LineStyle(_message.Message):
    __slots__ = ("width", "fill_opacity", "interpolation", "show_points", "connect_gap_limit")
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    FILL_OPACITY_FIELD_NUMBER: _ClassVar[int]
    INTERPOLATION_FIELD_NUMBER: _ClassVar[int]
    SHOW_POINTS_FIELD_NUMBER: _ClassVar[int]
    CONNECT_GAP_LIMIT_FIELD_NUMBER: _ClassVar[int]
    width: float
    fill_opacity: float
    interpolation: LineInterpolation
    show_points: bool
    connect_gap_limit: float
    def __init__(
        self,
        width: _Optional[float] = ...,
        fill_opacity: _Optional[float] = ...,
        interpolation: _Optional[_Union[LineInterpolation, str]] = ...,
        show_points: bool = ...,
        connect_gap_limit: _Optional[float] = ...,
    ) -> None: ...

class BarStyle(_message.Message):
    __slots__ = ("width_factor", "max_width_px")
    WIDTH_FACTOR_FIELD_NUMBER: _ClassVar[int]
    MAX_WIDTH_PX_FIELD_NUMBER: _ClassVar[int]
    width_factor: float
    max_width_px: float
    def __init__(self, width_factor: _Optional[float] = ..., max_width_px: _Optional[float] = ...) -> None: ...

class Series(_message.Message):
    __slots__ = (
        "id",
        "label",
        "x_axis_id",
        "y_axis_id",
        "x_column",
        "x_binned",
        "y_column",
        "draw_style",
        "stacking",
        "null_value_mode",
        "line",
        "bar",
        "unit",
        "decimals",
        "color_index",
        "group_tags",
        "hide_from_legend",
        "hide_from_tooltip",
        "hide_from_viz",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    X_AXIS_ID_FIELD_NUMBER: _ClassVar[int]
    Y_AXIS_ID_FIELD_NUMBER: _ClassVar[int]
    X_COLUMN_FIELD_NUMBER: _ClassVar[int]
    X_BINNED_FIELD_NUMBER: _ClassVar[int]
    Y_COLUMN_FIELD_NUMBER: _ClassVar[int]
    DRAW_STYLE_FIELD_NUMBER: _ClassVar[int]
    STACKING_FIELD_NUMBER: _ClassVar[int]
    NULL_VALUE_MODE_FIELD_NUMBER: _ClassVar[int]
    LINE_FIELD_NUMBER: _ClassVar[int]
    BAR_FIELD_NUMBER: _ClassVar[int]
    UNIT_FIELD_NUMBER: _ClassVar[int]
    DECIMALS_FIELD_NUMBER: _ClassVar[int]
    COLOR_INDEX_FIELD_NUMBER: _ClassVar[int]
    GROUP_TAGS_FIELD_NUMBER: _ClassVar[int]
    HIDE_FROM_LEGEND_FIELD_NUMBER: _ClassVar[int]
    HIDE_FROM_TOOLTIP_FIELD_NUMBER: _ClassVar[int]
    HIDE_FROM_VIZ_FIELD_NUMBER: _ClassVar[int]
    id: str
    label: str
    x_axis_id: str
    y_axis_id: str
    x_column: str
    x_binned: BinnedX
    y_column: str
    draw_style: DrawStyle
    stacking: Stacking
    null_value_mode: NullValueMode
    line: LineStyle
    bar: BarStyle
    unit: str
    decimals: int
    color_index: int
    group_tags: _containers.RepeatedCompositeFieldContainer[GroupTag]
    hide_from_legend: bool
    hide_from_tooltip: bool
    hide_from_viz: bool
    def __init__(
        self,
        id: _Optional[str] = ...,
        label: _Optional[str] = ...,
        x_axis_id: _Optional[str] = ...,
        y_axis_id: _Optional[str] = ...,
        x_column: _Optional[str] = ...,
        x_binned: _Optional[_Union[BinnedX, _Mapping]] = ...,
        y_column: _Optional[str] = ...,
        draw_style: _Optional[_Union[DrawStyle, str]] = ...,
        stacking: _Optional[_Union[Stacking, _Mapping]] = ...,
        null_value_mode: _Optional[_Union[NullValueMode, str]] = ...,
        line: _Optional[_Union[LineStyle, _Mapping]] = ...,
        bar: _Optional[_Union[BarStyle, _Mapping]] = ...,
        unit: _Optional[str] = ...,
        decimals: _Optional[int] = ...,
        color_index: _Optional[int] = ...,
        group_tags: _Optional[_Iterable[_Union[GroupTag, _Mapping]]] = ...,
        hide_from_legend: bool = ...,
        hide_from_tooltip: bool = ...,
        hide_from_viz: bool = ...,
    ) -> None: ...

class Legend(_message.Message):
    __slots__ = ("placement",)
    PLACEMENT_FIELD_NUMBER: _ClassVar[int]
    placement: LegendPlacement
    def __init__(self, placement: _Optional[_Union[LegendPlacement, str]] = ...) -> None: ...

class TabularChart(_message.Message):
    __slots__ = ("title", "description", "data", "axes", "series", "orientation", "legend", "schema_version")
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    AXES_FIELD_NUMBER: _ClassVar[int]
    SERIES_FIELD_NUMBER: _ClassVar[int]
    ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    LEGEND_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_VERSION_FIELD_NUMBER: _ClassVar[int]
    title: str
    description: str
    data: TabularData
    axes: _containers.RepeatedCompositeFieldContainer[Axis]
    series: _containers.RepeatedCompositeFieldContainer[Series]
    orientation: Orientation
    legend: Legend
    schema_version: int
    def __init__(
        self,
        title: _Optional[str] = ...,
        description: _Optional[str] = ...,
        data: _Optional[_Union[TabularData, _Mapping]] = ...,
        axes: _Optional[_Iterable[_Union[Axis, _Mapping]]] = ...,
        series: _Optional[_Iterable[_Union[Series, _Mapping]]] = ...,
        orientation: _Optional[_Union[Orientation, str]] = ...,
        legend: _Optional[_Union[Legend, _Mapping]] = ...,
        schema_version: _Optional[int] = ...,
    ) -> None: ...
