from types import MappingProxyType
from typing import Mapping
from typing import Union

from typeguard import typechecked

from tecton_core.specs import tecton_object_spec
from tecton_core.specs import utils
from tecton_proto.args import server_group__client_pb2 as server_group__arg_pb2
from tecton_proto.common import framework_version__client_pb2 as framework_version_pb2
from tecton_proto.common import scaling_config__client_pb2 as scaling_config_pb2
from tecton_proto.data import server_group__client_pb2 as server_group__data_pb2
from tecton_proto.validation import validator__client_pb2 as validator_pb2


__all__ = [
    "FeatureServerGroupSpec",
    "TransformServerGroupSpec",
]


@utils.frozen_strict
class FeatureServerGroupSpec(tecton_object_spec.TectonObjectSpec):
    """Base class for feature server group specs."""

    scaling_config: Union[scaling_config_pb2.AutoscalingConfig, scaling_config_pb2.ProvisionedScalingConfig]
    options: Mapping[str, str]

    @classmethod
    @typechecked
    def from_data_proto(cls, proto: server_group__data_pb2.ServerGroup) -> "FeatureServerGroupSpec":
        return cls(
            metadata=tecton_object_spec.TectonObjectMetadataSpec.from_data_proto(
                proto.server_group_id, proto.fco_metadata
            ),
            scaling_config=get_scaling_config(proto),
            validation_args=validator_pb2.FcoValidationArgs(server_group=proto.validation_args),
            options=MappingProxyType(proto.options),
        )

    @classmethod
    @typechecked
    def from_args_proto(cls, proto: server_group__arg_pb2.ServerGroupArgs) -> "FeatureServerGroupSpec":
        return cls(
            metadata=tecton_object_spec.TectonObjectMetadataSpec.from_args_proto(
                proto.server_group_id, proto.info, framework_version_pb2.FrameworkVersion.FWV6
            ),
            scaling_config=get_scaling_config(proto),
            validation_args=None,
            options=MappingProxyType(proto.options),
        )


@utils.frozen_strict
class TransformServerGroupSpec(tecton_object_spec.TectonObjectSpec):
    """Base class for feature server group specs."""

    scaling_config: Union[scaling_config_pb2.AutoscalingConfig, scaling_config_pb2.ProvisionedScalingConfig]
    environment: str
    options: Mapping[str, str]

    @classmethod
    @typechecked
    def from_data_proto(cls, proto: server_group__data_pb2.ServerGroup) -> "TransformServerGroupSpec":
        return cls(
            metadata=tecton_object_spec.TectonObjectMetadataSpec.from_data_proto(
                proto.server_group_id, proto.fco_metadata
            ),
            scaling_config=get_scaling_config(proto),
            environment=proto.transform_server_group.environment_name,
            validation_args=validator_pb2.FcoValidationArgs(server_group=proto.validation_args),
            options=MappingProxyType(proto.options),
        )

    @classmethod
    @typechecked
    def from_args_proto(cls, proto: server_group__arg_pb2.ServerGroupArgs) -> "TransformServerGroupSpec":
        return cls(
            metadata=tecton_object_spec.TectonObjectMetadataSpec.from_args_proto(
                proto.server_group_id, proto.info, framework_version_pb2.FrameworkVersion.FWV6
            ),
            scaling_config=get_scaling_config(proto),
            environment=proto.transform_server_group_args.environment,
            validation_args=None,
            options=MappingProxyType(proto.options),
        )


def get_scaling_config(
    proto: Union[server_group__arg_pb2.ServerGroupArgs, server_group__data_pb2.ServerGroup],
) -> Union[scaling_config_pb2.AutoscalingConfig, scaling_config_pb2.ProvisionedScalingConfig]:
    if proto.HasField("autoscaling_config"):
        return proto.autoscaling_config
    elif proto.HasField("provisioned_scaling_config"):
        return proto.provisioned_scaling_config
    else:
        msg = f"Unexpected scaling config type: {proto}"
        raise ValueError(msg)
