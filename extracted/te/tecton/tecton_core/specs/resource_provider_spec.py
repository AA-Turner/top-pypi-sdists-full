from typing import Callable
from typing import Mapping
from typing import Optional

import attrs
from typeguard import typechecked

from tecton_core import function_deserialization
from tecton_core.specs import tecton_object_spec
from tecton_core.specs import utils
from tecton_core.specs.secret_spec import SecretSpec
from tecton_proto.args import resource_provider__client_pb2 as resource_provider__arg_pb2
from tecton_proto.common import framework_version__client_pb2 as framework_version_pb2
from tecton_proto.data import resource_provider__client_pb2 as resource_provider__data_pb2
from tecton_proto.validation import validator__client_pb2 as validator_pb2


@utils.frozen_strict
class ResourceProviderSpec(tecton_object_spec.TectonObjectSpec):
    """Base class for resource provider specs."""

    secrets: Optional[Mapping[str, SecretSpec]]
    function: Callable = attrs.field(metadata={utils.LOCAL_REMOTE_DIVERGENCE_ALLOWED: True})

    @classmethod
    @typechecked
    def from_data_proto(cls, proto: resource_provider__data_pb2.ResourceProvider) -> "ResourceProviderSpec":
        function = function_deserialization.from_proto(proto.function)
        return cls(
            metadata=tecton_object_spec.TectonObjectMetadataSpec.from_data_proto(
                proto.resource_provider_id, proto.fco_metadata
            ),
            secrets={key: SecretSpec.from_proto(value) for (key, value) in proto.secrets.items()},
            function=function,
            validation_args=validator_pb2.FcoValidationArgs(resource_provider=proto.validation_args),
        )

    @classmethod
    @typechecked
    def from_args_proto(
        cls, proto: resource_provider__arg_pb2.ResourceProviderArgs, function: Optional[Callable]
    ) -> "ResourceProviderSpec":
        # If a function was serialized for this resource (e.g. because it was defined in a repo), then prefer to
        # use the serialized function over directly using the Python function.
        if proto.HasField("function"):
            function = function_deserialization.from_proto(proto.function)
        return cls(
            metadata=tecton_object_spec.TectonObjectMetadataSpec.from_args_proto(
                proto.resource_provider_id, proto.info, framework_version_pb2.FrameworkVersion.FWV6
            ),
            secrets={key: SecretSpec.from_proto(value) for (key, value) in proto.secrets.items()},
            function=function,
            validation_args=None,
        )
