from types import MappingProxyType
from typing import Mapping
from typing import Tuple

from typeguard import typechecked

from tecton_core import data_types
from tecton_core import schema
from tecton_core.specs import tecton_object_spec
from tecton_core.specs import utils
from tecton_proto.args import entity__client_pb2 as entity__args_pb2
from tecton_proto.data import entity__client_pb2 as entity__data_pb2
from tecton_proto.validation import validator__client_pb2 as validator_pb2


__all__ = [
    "EntitySpec",
]


@utils.frozen_strict
class EntitySpec(tecton_object_spec.TectonObjectSpec):
    join_keys: Tuple[schema.Column, ...]
    options: Mapping[str, str]
    prevent_destroy: bool

    @classmethod
    @typechecked
    def from_data_proto(cls, proto: entity__data_pb2.Entity) -> "EntitySpec":
        return cls(
            metadata=tecton_object_spec.TectonObjectMetadataSpec.from_data_proto(proto.entity_id, proto.fco_metadata),
            join_keys=tuple(
                schema.Column(name=join_key.name, dtype=data_types.data_type_from_proto(join_key.offline_data_type))
                for join_key in proto.join_keys
            ),
            validation_args=validator_pb2.FcoValidationArgs(entity=proto.validation_args),
            options=MappingProxyType(proto.options),
            prevent_destroy=proto.validation_args.args.prevent_destroy,
        )

    @classmethod
    @typechecked
    def from_args_proto(cls, proto: entity__args_pb2.EntityArgs) -> "EntitySpec":
        join_keys = tuple(
            schema.Column(name=join_key.name, dtype=data_types.data_type_from_proto(join_key.offline_data_type))
            for join_key in proto.join_keys
        )
        return cls(
            metadata=tecton_object_spec.TectonObjectMetadataSpec.from_args_proto(
                proto.entity_id, proto.info, proto.version
            ),
            join_keys=join_keys,
            validation_args=None,
            options=MappingProxyType(proto.options),
            prevent_destroy=proto.prevent_destroy,
        )

    @property
    def join_key_names(self) -> Tuple[str, ...]:
        return tuple(join_key.name for join_key in self.join_keys)
