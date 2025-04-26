from typing import Dict
from typing import List
from typing import Mapping
from typing import Optional

import attrs
from typeguard import typechecked

from tecton._internals import display
from tecton._internals import metadata_service
from tecton._internals import sdk_decorators
from tecton._internals import validations_api
from tecton.framework import base_tecton_object
from tecton.types import Field
from tecton_core import conf
from tecton_core import id_helper
from tecton_core import specs
from tecton_core.repo_file_handler import construct_fco_source_info
from tecton_core.schema import Column
from tecton_proto.args import basic_info__client_pb2 as basic_info_pb2
from tecton_proto.args import entity__client_pb2 as entity__args_pb2
from tecton_proto.args import fco_args__client_pb2 as fco_args_pb2
from tecton_proto.common import fco_locator__client_pb2 as fco_locator_pb2
from tecton_proto.common import schema__client_pb2 as schema_pb2
from tecton_proto.metadataservice import metadata_service__client_pb2 as metadata_service_pb2
from tecton_proto.validation import validator__client_pb2 as validator_pb2


@attrs.define(eq=False)
class Entity(base_tecton_object.BaseTectonObject):
    """A Tecton Entity, used to organize and join features.

    An Entity is a class that represents an Entity that is being modeled in Tecton. Entities are used to index and
    organize features - a `FeatureView` contains at least one Entity.

    Entities contain metadata about *join keys*, which represent the columns that are used to join features together.

    ```python
    from tecton import Entity
    from tecton.types import Field, String

    customer = Entity(
        name='customer',
        join_keys=[Field('customer_id', String)],
        description='A customer subscribing to a Sports TV subscription service',
        owner='matt@tecton.ai',
        tags={'release': 'development'}
    ```
    """

    # An entity spec, i.e. a dataclass representation of the Tecton object that is used in most functional use cases,
    # e.g. constructing queries.
    _spec: Optional[specs.EntitySpec] = attrs.field(repr=False)

    # A Tecton "args" proto. Only set if this object was defined locally, i.e. this object was not applied and fetched
    # from the Tecton backend.
    _args: Optional[entity__args_pb2.EntityArgs] = attrs.field(repr=False, on_setattr=attrs.setters.frozen)

    @typechecked
    def __init__(
        self,
        *,
        name: str,
        description: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        owner: Optional[str] = None,
        prevent_destroy: bool = False,
        join_keys: Optional[List[Field]] = None,
        options: Optional[Dict[str, str]] = None,
    ):
        """Declare a new Entity.

        :param name: Unique name for the new entity.
        :param description: Short description of the new entity.
        :param tags: Tags associated with this Tecton Object (key-value pairs of arbitrary metadata).
        :param owner: Owner name (typically the email of the primary maintainer).
        :param prevent_destroy: If True, this Tecton object will be blocked from being deleted or re-created (i.e. a
            destructive update) during tecton plan/apply. To remove or update this object, `prevent_destroy` must be
            set to False via the same tecton apply or a separate tecton apply. `prevent_destroy` can be used to prevent accidental changes
            such as inadvertantly deleting a Feature Service used in production or recreating a Feature View that
            triggers expensive rematerialization jobs. `prevent_destroy` also blocks changes to dependent Tecton objects
            that would trigger a recreate of the tagged object, e.g. if `prevent_destroy` is set on a Feature Service,
            that will also prevent deletions or re-creates of Feature Views used in that service. `prevent_destroy` is
            only enforced in live (i.e. non-dev) workspaces.
        :param join_keys: Field objects corresponding to the entity's unique identifiers which will be used for aggregations
        :param options: Additional options to configure the Entity. Used for advanced use cases and beta features.

        :raises TectonValidationError: if the input non-parameters are invalid.
        """
        args = entity__args_pb2.EntityArgs(
            entity_id=id_helper.IdHelper.generate_id(),
            info=basic_info_pb2.BasicInfo(name=name, description=description, tags=tags, owner=owner),
            version=self._framework_version.value,
            prevent_destroy=prevent_destroy,
            options=options,
        )

        resolved_join_keys = [Column(join_key.name, join_key.dtype.tecton_type) for join_key in join_keys]
        args.join_keys.extend(
            [
                schema_pb2.Column(name=join_key.name, offline_data_type=join_key.dtype.proto)
                for join_key in resolved_join_keys
            ]
        )

        info = base_tecton_object.TectonObjectInfo.from_args_proto(args.info, args.entity_id)
        source_info = construct_fco_source_info(args.entity_id)
        self.__attrs_init__(info=info, spec=None, args=args, source_info=source_info)

        if not conf.get_bool("TECTON_SKIP_OBJECT_VALIDATION"):
            self._validate()
        self._spec = specs.EntitySpec.from_args_proto(self._args)
        base_tecton_object._register_local_object(self)

    @classmethod
    @typechecked
    def _from_spec(cls, spec: specs.EntitySpec) -> "Entity":
        """Create an Entity from directly from a spec. Specs are assumed valid and will not be re-validated."""
        info = base_tecton_object.TectonObjectInfo.from_spec(spec)

        # override the framework version class attribute to be the framework version set by the spec
        class EntityFromSpec(cls):
            _framework_version = spec.metadata.framework_version

        obj = EntityFromSpec.__new__(EntityFromSpec)
        obj.__attrs_init__(info=info, spec=spec, args=None, source_info=None)
        return obj

    @sdk_decorators.assert_local_object
    def _build_and_resolve_args(self, objects) -> fco_args_pb2.FcoArgs:
        return fco_args_pb2.FcoArgs(entity=self._args)

    def _build_fco_validation_args(self) -> validator_pb2.FcoValidationArgs:
        if self.info._is_local_object:
            return validator_pb2.FcoValidationArgs(
                entity=validator_pb2.EntityValidationArgs(
                    args=self._args,
                )
            )
        else:
            return self._spec.validation_args

    # TODO(jiadong): Figure out if we should change this property to return List[Field] or have a new property to do so.
    @property
    def join_keys(self) -> List[str]:
        """Join keys of the entity."""
        return list(self._spec.join_key_names)

    @property
    def prevent_destroy(self) -> bool:
        """Return whether entity has prevent_destroy flagged"""
        return self._spec.prevent_destroy

    @property
    def _options(self) -> Mapping[str, str]:
        """Return options set on initialization used for configuration. Advanced use cases and beta features."""
        return self._spec.options

    def _validate(self) -> None:
        validations_api.run_backend_validation_and_assert_valid(
            self,
            validator_pb2.ValidationRequest(validation_args=[self._build_fco_validation_args()]),
        )

        self._spec = specs.EntitySpec.from_args_proto(self._args)

    @sdk_decorators.sdk_public_method
    @sdk_decorators.assert_remote_object
    def summary(self) -> display.Displayable:
        """Displays a human-readable summary."""
        request = metadata_service_pb2.GetEntitySummaryRequest(
            fco_locator=fco_locator_pb2.FcoLocator(id=self._spec.id_proto, workspace=self._spec.workspace)
        )
        response = metadata_service.instance().GetEntitySummary(request)
        return display.Displayable.from_fco_summary(response.fco_summary)

    @sdk_decorators.assert_local_object
    def _create_unvalidated_spec(self) -> specs.EntitySpec:
        """Create an unvalidated spec. Used for user unit testing, where backend validation is unavailable."""
        return specs.EntitySpec.from_args_proto(self._args)
