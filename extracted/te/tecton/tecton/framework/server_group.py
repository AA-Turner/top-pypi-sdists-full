from typing import Dict
from typing import Optional
from typing import Union

import attrs
from typeguard import typechecked

from tecton._internals import sdk_decorators
from tecton._internals import validations_api
from tecton.framework import base_tecton_object
from tecton.framework import configs
from tecton_core import conf
from tecton_core import id_helper
from tecton_core import specs
from tecton_core.repo_file_handler import construct_fco_source_info
from tecton_proto.args import basic_info__client_pb2 as basic_info_pb2
from tecton_proto.args import fco_args__client_pb2 as fco_args_pb2
from tecton_proto.args import server_group__client_pb2 as server_group_pb2
from tecton_proto.common import server_group_type__client_pb2 as server_group_type_pb2
from tecton_proto.validation import validator__client_pb2 as validator_pb2


@attrs.define(eq=False)
class BaseServerGroup(base_tecton_object.BaseTectonObject):
    """Base class for server groups."""

    _args: Optional[server_group_pb2.ServerGroupArgs] = attrs.field(repr=False, on_setattr=attrs.setters.frozen)
    scaling_config: Optional[Union[configs.AutoscalingConfig, configs.ProvisionedScalingConfig]] = attrs.field(
        repr=False
    )
    _spec: Optional[specs.FeatureServerGroupSpec] = attrs.field(repr=False)

    @sdk_decorators.assert_local_object
    def _build_and_resolve_args(self, objects) -> fco_args_pb2.FcoArgs:
        return fco_args_pb2.FcoArgs(server_group=self._args)

    @classmethod
    @typechecked
    def _from_spec(cls, spec: specs.FeatureServerGroupSpec) -> "FeatureServerGroup":
        """Create a Feature Service from directly from a spec. Specs are assumed valid and will not be re-validated."""
        info = base_tecton_object.TectonObjectInfo.from_spec(spec)
        obj = cls.__new__(cls)
        obj.__attrs_init__(
            info=info,
            spec=spec,
            args=None,
            source_info=None,
            scaling_config=specs.scaling_config,
        )
        return obj

    def _build_fco_validation_args(self) -> validator_pb2.FcoValidationArgs:
        if self.info._is_local_object:
            return validator_pb2.FcoValidationArgs(
                server_group=validator_pb2.ServerGroupValidationArgs(
                    args=self._args,
                )
            )
        else:
            return self._spec.validation_args

    def _validate(self) -> None:
        validations_api.run_backend_validation_and_assert_valid(
            self,
            validator_pb2.ValidationRequest(
                validation_args=[self._build_fco_validation_args()],
            ),
        )


@attrs.define(eq=False)
class FeatureServerGroup(BaseServerGroup):
    """
    Configuration used to specify the options for provisioning a server group for the feature server.
    """

    def __init__(
        self,
        *,
        name: str,
        scaling_config: Optional[Union[configs.AutoscalingConfig, configs.ProvisionedScalingConfig]],
        description: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        owner: Optional[str] = None,
        prevent_destroy: bool = False,
        options: Optional[Dict[str, str]] = None,
    ):
        """
        Configuration used to specify the feature server group options.

        :param name: A unique name for the Feature Server Group.
        :param description: A human-readable description.
        :param tags: Tags associated with this Tecton Object (key-value pairs of arbitrary metadata).
        :param owner: Owner name (typically the email of the primary maintainer).
        :param prevent_destroy: If True, this Tecton object will be blocked from being deleted or re-created (i.e. a
            destructive update) during tecton plan/apply. To remove or update this object, `prevent_destroy` must be set to False
            via the same tecton apply or a separate tecton apply. `prevent_destroy` can be used to prevent accidental changes
            such as inadvertantly deleting a Feature Service used in production or recreating a Feature View that
            triggers expensive rematerialization jobs. `prevent_destroy` also blocks changes to dependent Tecton objects
            that would trigger a recreate of the tagged object, e.g. if `prevent_destroy` is set on a Feature Service,
            that will also prevent deletions or re-creates of Feature Views used in that service. `prevent_destroy` is
            only enforced in live (i.e. non-dev) workspaces.
        :param scaling_config: A configuration for creating an autoscaling or provisioned server group.
        :param options: Additional options to configure the Feature Server Group. Used for advanced use cases and beta features.
        """
        args = server_group_pb2.ServerGroupArgs(
            server_group_id=id_helper.IdHelper.generate_id(),
            info=basic_info_pb2.BasicInfo(name=name, description=description, tags=tags, owner=owner),
            prevent_destroy=prevent_destroy,
            feature_server_group_args=server_group_pb2.FeatureServerGroupArgs(),
            server_group_type=server_group_type_pb2.SERVER_GROUP_TYPE_FEATURE_SERVER_GROUP,
            options=options,
        )
        if isinstance(scaling_config, configs.AutoscalingConfig):
            args.autoscaling_config.CopyFrom(scaling_config._to_proto())
        elif isinstance(scaling_config, configs.ProvisionedScalingConfig):
            args.provisioned_scaling_config.CopyFrom(scaling_config._to_proto())
        else:
            msg = f"Invalid scaling config type: {type(scaling_config)}"
            raise TypeError(msg)
        info = base_tecton_object.TectonObjectInfo.from_args_proto(args.info, args.server_group_id)
        source_info = construct_fco_source_info(args.server_group_id)
        self.__attrs_init__(
            info=info,
            args=args,
            spec=None,
            source_info=source_info,
            scaling_config=scaling_config,
        )
        self._spec = specs.FeatureServerGroupSpec.from_args_proto(self._args)
        if not conf.get_bool("TECTON_SKIP_OBJECT_VALIDATION"):
            self._validate()
        base_tecton_object._register_local_object(self)


@attrs.define(eq=False)
class TransformServerGroup(BaseServerGroup):
    """
    Configuration used to specify the options for provisioning a server group for the transform server.
    """

    environment: str = attrs.field(repr=False)

    def __init__(
        self,
        *,
        name: str,
        scaling_config: Optional[Union[configs.AutoscalingConfig, configs.ProvisionedScalingConfig]],
        description: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        owner: Optional[str] = None,
        prevent_destroy: bool = False,
        environment: Optional[str] = None,
        options: Optional[Dict[str, str]] = None,
    ):
        """
        Instantiates a new TransformServerGroup.

        :param name: A unique name for the Transform Server Group.
        :param description: A human-readable description.
        :param tags: Tags associated with this Tecton Object (key-value pairs of arbitrary metadata).
        :param owner: Owner name (typically the email of the primary maintainer).
        :param prevent_destroy: If True, this Tecton object will be blocked from being deleted or re-created (i.e. a
            destructive update) during tecton plan/apply. To remove or update this object, `prevent_destroy` must be set to False
            via the same tecton apply or a separate tecton apply. `prevent_destroy` can be used to prevent accidental changes
            such as inadvertantly deleting a Feature Service used in production or recreating a Feature View that
            triggers expensive rematerialization jobs. `prevent_destroy` also blocks changes to dependent Tecton objects
            that would trigger a recreate of the tagged object, e.g. if `prevent_destroy` is set on a Feature Service,
            that will also prevent deletions or re-creates of Feature Views used in that service. `prevent_destroy` is
            only enforced in live (i.e. non-dev) workspaces.
        :param scaling_config: A configuration for creating an autoscaling or provisioned server group.
        :param environment: The name of the Python environment.
        :param options: Additional options to configure the Transform Server Group. Used for advanced use cases and beta features.
        """
        args = server_group_pb2.ServerGroupArgs(
            server_group_id=id_helper.IdHelper.generate_id(),
            info=basic_info_pb2.BasicInfo(name=name, description=description, tags=tags, owner=owner),
            prevent_destroy=prevent_destroy,
            transform_server_group_args=server_group_pb2.TransformServerGroupArgs(environment=environment),
            server_group_type=server_group_type_pb2.SERVER_GROUP_TYPE_TRANSFORM_SERVER_GROUP,
            options=options,
        )

        if isinstance(scaling_config, configs.AutoscalingConfig):
            args.autoscaling_config.CopyFrom(scaling_config._to_proto())
        elif isinstance(scaling_config, configs.ProvisionedScalingConfig):
            args.provisioned_scaling_config.CopyFrom(scaling_config._to_proto())
        else:
            msg = f"Invalid scaling config type: {type(scaling_config)}"
            raise TypeError(msg)
        info = base_tecton_object.TectonObjectInfo.from_args_proto(args.info, args.server_group_id)
        source_info = construct_fco_source_info(args.server_group_id)
        self.__attrs_init__(
            info=info,
            args=args,
            spec=None,
            source_info=source_info,
            scaling_config=scaling_config,
            environment=environment,
        )
        self._spec = specs.TransformServerGroupSpec.from_args_proto(self._args)
        if not conf.get_bool("TECTON_SKIP_OBJECT_VALIDATION"):
            self._validate()
        base_tecton_object._register_local_object(self)
