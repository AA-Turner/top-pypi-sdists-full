"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
Generated by https://github.com/foxglove/schemas"""

import builtins
import collections.abc
from . import PackedElementField_pb2 as foxglove_PackedElementField_pb2
from . import Pose_pb2 as foxglove_Pose_pb2
from . import Vector2_pb2 as foxglove_Vector2_pb2
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import google.protobuf.timestamp_pb2
import typing

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class Grid(google.protobuf.message.Message):
    """A 2D grid of data"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    TIMESTAMP_FIELD_NUMBER: builtins.int
    FRAME_ID_FIELD_NUMBER: builtins.int
    POSE_FIELD_NUMBER: builtins.int
    COLUMN_COUNT_FIELD_NUMBER: builtins.int
    CELL_SIZE_FIELD_NUMBER: builtins.int
    ROW_STRIDE_FIELD_NUMBER: builtins.int
    CELL_STRIDE_FIELD_NUMBER: builtins.int
    FIELDS_FIELD_NUMBER: builtins.int
    DATA_FIELD_NUMBER: builtins.int
    frame_id: builtins.str
    """Frame of reference"""
    column_count: builtins.int
    """Number of grid columns"""
    row_stride: builtins.int
    """Number of bytes between rows in `data`"""
    cell_stride: builtins.int
    """Number of bytes between cells within a row in `data`"""
    data: builtins.bytes
    """Grid cell data, interpreted using `fields`, in row-major (y-major) order"""
    @property
    def timestamp(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """Timestamp of grid"""

    @property
    def pose(self) -> foxglove_Pose_pb2.Pose:
        """Origin of grid's corner relative to frame of reference; grid is positioned in the x-y plane relative to this origin"""

    @property
    def cell_size(self) -> foxglove_Vector2_pb2.Vector2:
        """Size of single grid cell along x and y axes, relative to `pose`"""

    @property
    def fields(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[foxglove_PackedElementField_pb2.PackedElementField]:
        """Fields in `data`. `red`, `green`, `blue`, and `alpha` are optional for customizing the grid's color."""

    def __init__(
        self,
        *,
        timestamp: google.protobuf.timestamp_pb2.Timestamp | None = ...,
        frame_id: builtins.str = ...,
        pose: foxglove_Pose_pb2.Pose | None = ...,
        column_count: builtins.int = ...,
        cell_size: foxglove_Vector2_pb2.Vector2 | None = ...,
        row_stride: builtins.int = ...,
        cell_stride: builtins.int = ...,
        fields: collections.abc.Iterable[foxglove_PackedElementField_pb2.PackedElementField] | None = ...,
        data: builtins.bytes = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["cell_size", b"cell_size", "pose", b"pose", "timestamp", b"timestamp"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["cell_size", b"cell_size", "cell_stride", b"cell_stride", "column_count", b"column_count", "data", b"data", "fields", b"fields", "frame_id", b"frame_id", "pose", b"pose", "row_stride", b"row_stride", "timestamp", b"timestamp"]) -> None: ...

global___Grid = Grid
