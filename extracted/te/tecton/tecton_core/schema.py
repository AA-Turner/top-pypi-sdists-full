from typing import Dict
from typing import List
from typing import Tuple

import attrs

from tecton_core import data_types as tecton_types
from tecton_core.data_types import DataType
from tecton_core.data_types import data_type_from_proto
from tecton_core.errors import TectonValidationError
from tecton_proto.common import schema__client_pb2 as schema_pb2


@attrs.frozen
class Schema:
    proto: schema_pb2.Schema

    def __repr__(self) -> str:
        # NOTE: this __repr__ affects what is printed for spec parity tests.
        # If you are debugging a test failure that you suspect its schema diff related,
        # we recommend commenting out this override so that the full proto is printed.
        return str(self.column_name_and_data_types())

    # TODO(jake): Remove this method. Just access proto attr directly.
    def to_proto(self) -> schema_pb2.Schema:
        return self.proto

    def column_names(self) -> List[str]:
        return [c.name for c in self.proto.columns]

    def column_name_and_data_types(self) -> List[Tuple[str, DataType]]:
        return [(c.name, data_type_from_proto(c.offline_data_type)) for c in self.proto.columns]

    def to_dict(self) -> Dict[str, DataType]:
        return dict(self.column_name_and_data_types())

    def is_equivalent(self, other_schema: "Schema") -> bool:
        """Checks if this schema is equivalent to another schema, ignoring column order.

        Only compares offline data types. Other fields are ignored.
        """
        return self.to_dict() == other_schema.to_dict()

    @classmethod
    def from_dict(cls, schema_dict: Dict[str, DataType]) -> "Schema":
        schema_proto = schema_pb2.Schema()
        for col_name, col_type in schema_dict.items():
            col = schema_proto.columns.add()
            col.CopyFrom(column_from_tecton_data_type(col_type))
            col.name = col_name
        return cls(proto=schema_proto)  # type: ignore

    def __len__(self):
        return len(self.proto.columns)

    def __add__(self, other: "Schema") -> "Schema":
        if other is None:
            return self
        self_dict = self.to_dict()
        other_dict = other.to_dict()

        # Check if two schema share any column name with different types. This should never happen theoretically.
        shared_col_name = set(self_dict.keys()).intersection(set(other_dict.keys()))
        for col_name in shared_col_name:
            if self_dict[col_name] != other_dict[col_name]:
                msg = f"Column name '{col_name} has different data types: {str(self_dict[col_name])} VS {str(other_dict[col_name])}"
                raise TectonValidationError(msg)

        self_dict.update(other_dict)
        return self.from_dict(self_dict)


@attrs.frozen
class Column:
    name: str
    dtype: DataType

    @classmethod
    def from_proto(cls, proto: schema_pb2.Column) -> "Column":
        return cls(name=proto.name, dtype=tecton_types.data_type_from_proto(proto.offline_data_type))

    def to_proto(self) -> schema_pb2.Column:
        return schema_pb2.Column(name=self.name, offline_data_type=self.dtype.proto)


def get_feature_server_data_type(offline_data_type: tecton_types.DataType) -> tecton_types.DataType:
    if offline_data_type == tecton_types.Int32Type():
        return tecton_types.Int64Type()
    return offline_data_type


def column_from_tecton_data_type(offline_data_type: tecton_types.DataType) -> schema_pb2.Column:
    return schema_pb2.Column(
        offline_data_type=offline_data_type.proto,
        feature_server_data_type=get_feature_server_data_type(offline_data_type).proto,
    )
