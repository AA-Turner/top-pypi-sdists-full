import datetime
import logging
from typing import Dict
from typing import Optional
from typing import Set

import attrs
from typeguard import typechecked

from tecton._internals import sdk_decorators
from tecton._internals.errors import VALIDATION_UPON_OBJECT_CREATION_VALIDATE_DEPRECATED
from tecton._internals.sdk_decorators import deprecated
from tecton_core import id_helper
from tecton_core import specs
from tecton_core.feature_definition_wrapper import FrameworkVersion
from tecton_proto.args import basic_info__client_pb2 as basic_info_pb2
from tecton_proto.args import fco_args__client_pb2 as fco_args_pb2
from tecton_proto.args import repo_metadata__client_pb2 as repo_metadata_pb2
from tecton_proto.common import id__client_pb2 as id_pb2
from tecton_proto.validation import validator__client_pb2 as validator_pb2


logger = logging.getLogger(__name__)

_LOCAL_TECTON_OBJECTS: Set["BaseTectonObject"] = set()


@attrs.frozen
class TectonObjectInfo:
    """A public SDK dataclass containing common metadata used for all Tecton Objects."""

    id: str
    name: str
    description: Optional[str]
    tags: Dict[str, str]
    owner: Optional[str]
    workspace: Optional[str]
    created_at: Optional[datetime.datetime] = attrs.field(repr=False)
    defined_in: Optional[str] = attrs.field(repr=False)
    _is_local_object: bool = attrs.field(repr=False)

    @classmethod
    @typechecked
    def from_args_proto(cls, basic_info: basic_info_pb2.BasicInfo, id: id_pb2.Id) -> "TectonObjectInfo":
        return cls(
            id=id_helper.IdHelper.to_string(id),
            name=basic_info.name,
            description=basic_info.description if basic_info.HasField("description") else None,
            tags=dict(basic_info.tags),
            owner=basic_info.owner if basic_info.HasField("owner") else None,
            created_at=None,  # created_at is only filled for remote (i.e. applied) Tecton objects.
            workspace=None,  # workspace is only filled for remote (i.e. applied) Tecton objects.
            defined_in=None,  # defined_in is only filled for remote (i.e. applied) Tecton objects.
            is_local_object=True,
        )

    @classmethod
    @typechecked
    def from_spec(cls, spec: specs.TectonObjectSpec) -> "TectonObjectInfo":
        return cls(
            id=spec.id,
            name=spec.name,
            description=spec.metadata.description,
            tags=spec.metadata.tags,
            owner=spec.metadata.owner,
            created_at=spec.metadata.created_at,
            workspace=spec.workspace,
            defined_in=spec.metadata.defined_in,
            is_local_object=spec.is_local_object,
        )

    @property
    def _id_proto(self) -> id_pb2.Id:
        return id_helper.IdHelper.from_string(self.id)


@attrs.define(eq=False)
class BaseTectonObject:
    """The base class for all Tecton Objects, e.g. Entities, Data Sources, and Feature Views.

    Attributes:
        info: A dataclass containing basic info about this Tecton Object.
    """

    info: TectonObjectInfo = attrs.field(on_setattr=attrs.setters.frozen)

    # Metadata about where this object was defined in the repo, e.g. the filename and line number. Only set if this
    # object was defined locally.
    _source_info: Optional[repo_metadata_pb2.SourceInfo] = attrs.field(repr=False, on_setattr=attrs.setters.frozen)

    _framework_version = FrameworkVersion.FWV6

    def _validate(self) -> None:
        """Internal validation API."""
        raise NotImplementedError

    @deprecated(
        version="1.0",
        reason="As of Tecton version 1.0 objects are validated upon object creation, so `validate()` is unnecessary.",
        warning_message=VALIDATION_UPON_OBJECT_CREATION_VALIDATE_DEPRECATED,
    )
    @sdk_decorators.sdk_public_method
    def validate(self) -> None:
        """Method is deprecated and will be removed in a future version. As of Tecton version 1.0, objects are validated upon object creation, so validation is unnecessary."""
        # TODO(TEC-19865): revisit what to do with this function as part of schema validation
        return

    def _build_and_resolve_args(self, objects) -> fco_args_pb2.FcoArgs:
        """Returns a copy of the args as a FcoArgs proto for plan/apply logic."""
        raise NotImplementedError

    def _build_fco_validation_args(self) -> validator_pb2.FcoValidationArgs:
        """Returns a copy of the args as a FcoValidationArgs proto for validation logic."""
        raise NotImplementedError

    @property
    def name(self) -> str:
        """Returns the name of the Tecton object."""
        return self.info.name

    @property
    def id(self) -> str:
        """Returns the unique id of the Tecton object."""
        return self.info.id

    @property
    def description(self) -> Optional[str]:
        """Returns the description of the Tecton object."""
        return self.info.description

    @property
    def tags(self) -> Dict[str, str]:
        """Returns the tags of the Tecton object."""
        return self.info.tags

    @property
    def owner(self) -> Optional[str]:
        """Returns the owner of the Tecton object."""
        return self.info.owner

    @property
    def workspace(self) -> Optional[str]:
        """Returns the workspace that this Tecton object belongs to. `None` for locally defined objects."""
        return self.info.workspace

    @property
    def created_at(self) -> Optional[datetime.datetime]:
        """Returns the time that this Tecton object was created or last updated. `None` for locally defined objects."""
        return self.info.created_at

    @property
    def defined_in(self) -> Optional[str]:
        """The repo filename where this object was declared. `None` for locally defined objects."""
        return self.info.defined_in

    @property
    def _is_local_object(self) -> bool:
        """Returns True if the object was defined locally, i.e. was not applied and fetched from the Tecton backend."""
        return self.info._is_local_object

    @property
    def _id_proto(self) -> id_pb2.Id:
        """Returns the proto version of the Tecton object id."""
        return self.info._id_proto


def _register_local_object(obj: BaseTectonObject) -> None:
    """Register the tecton object to the set of global tecton objects.

    The global set is used to collect objects during `tecton apply`.
    """
    _LOCAL_TECTON_OBJECTS.add(obj)
