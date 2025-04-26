import typing
from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union

import attrs
from typeguard import typechecked

from tecton_core import specs
from tecton_core.id_helper import IdHelper
from tecton_proto.common import id__client_pb2 as id_pb2
from tecton_proto.data import fco__client_pb2 as fco_pb2
from tecton_proto.data.entity__client_pb2 import Entity as EntityProto
from tecton_proto.data.feature_view__client_pb2 import FeatureView as FeatureViewProto
from tecton_proto.data.resource_provider__client_pb2 import ResourceProvider as ResourceProviderProto
from tecton_proto.data.transformation__client_pb2 import Transformation
from tecton_proto.data.virtual_data_source__client_pb2 import VirtualDataSource as DataSourceProto


@attrs.frozen
class FcoContainer:
    """A wrapper class for FcoContainer proto, contains convenience accessors."""

    _root_ids: Tuple[str]
    _id_to_spec: Dict[str, specs.TectonObjectSpec]

    @classmethod
    @typechecked
    def from_proto(cls, proto: fco_pb2.FcoContainer, include_main_variables_in_scope: bool = False) -> "FcoContainer":
        """Construct an FcoContainer from an FcoContainer proto."""
        root_ids = [IdHelper.to_string(id) for id in proto.root_ids]
        specs = [_spec_from_fco_data_proto(fco, include_main_variables_in_scope) for fco in proto.fcos]
        id_to_spec = {spec.id: spec for spec in specs}
        return cls(root_ids=root_ids, id_to_spec=id_to_spec)  # type: ignore

    @classmethod
    @typechecked
    def from_specs(cls, specs: Sequence[specs.TectonObjectSpec], root_ids: Sequence[str]) -> "FcoContainer":
        """Construct an FcoContainer from a set of specs."""
        id_to_spec = {spec.id: spec for spec in specs}
        return cls(root_ids=tuple(root_ids), id_to_spec=id_to_spec)  # type: ignore

    @typechecked
    def get_by_id(self, id: str) -> specs.TectonObjectSpec:
        """
        :return: The TectonObjectSpec with the provided `id`.
        """
        return self._id_to_spec[id]

    @typechecked
    def get_by_id_proto(self, id_proto: id_pb2.Id) -> specs.TectonObjectSpec:
        """
        :return: The TectonObjectSpec with the provided `id` proto.
        """
        id_string = IdHelper.to_string(id_proto)
        return self._id_to_spec[id_string]

    @typechecked
    def get_by_ids(self, ids: Sequence[str]) -> List[specs.TectonObjectSpec]:
        """
        :return: The TectonObjectSpec with the provided `ids`.
        """

        return [self.get_by_id(id) for id in ids]

    @typechecked
    def get_single_root(self) -> Optional[specs.TectonObjectSpec]:
        """
        :return: The root TectonObjectSpec for the container or None. Errors if len(root_ids) > 1
        """

        num_root_ids = len(self._root_ids)
        if num_root_ids == 0:
            return None
        elif num_root_ids > 1:
            msg = f"Expected a single result but got {num_root_ids}"
            raise ValueError(msg)
        else:
            return self.get_by_id(self._root_ids[0])

    @typechecked
    def get_root_fcos(self) -> List[specs.TectonObjectSpec]:
        """
        :return: All root TectonObjectSpec for the container.
        """

        return [self.get_by_id(id) for id in self._root_ids]


FCO_CONTAINER_EMTPY = FcoContainer.from_proto(fco_pb2.FcoContainer())


def _spec_from_fco_data_proto(fco: fco_pb2.Fco, include_main_variables_in_scope: bool) -> specs.TectonObjectSpec:
    if fco.HasField("virtual_data_source"):
        return specs.DataSourceSpec.from_data_proto(fco.virtual_data_source, include_main_variables_in_scope)
    elif fco.HasField("entity"):
        return specs.EntitySpec.from_data_proto(fco.entity)
    elif fco.HasField("transformation"):
        return specs.TransformationSpec.from_data_proto(fco.transformation, include_main_variables_in_scope)
    elif fco.HasField("feature_view"):
        return specs.create_feature_view_spec_from_data_proto(fco.feature_view)
    elif fco.HasField("feature_service"):
        return specs.FeatureServiceSpec.from_data_proto(fco.feature_service)
    elif fco.HasField("resource_provider"):
        return specs.ResourceProviderSpec.from_data_proto(fco.resource_provider)
    else:
        msg = f"Unexpected fco type: {fco}"
        raise ValueError(msg)


DataProto = Union[DataSourceProto, Transformation, FeatureViewProto, EntityProto, ResourceProviderProto]


def _wrap_data_fco(inner_proto: DataProto) -> fco_pb2.Fco:
    fco = fco_pb2.Fco()
    if isinstance(inner_proto, DataSourceProto):
        fco.virtual_data_source.CopyFrom(inner_proto)
    elif isinstance(inner_proto, Transformation):
        fco.transformation.CopyFrom(inner_proto)
    elif isinstance(inner_proto, FeatureViewProto):
        fco.feature_view.CopyFrom(inner_proto)
    elif isinstance(inner_proto, EntityProto):
        fco.entity.CopyFrom(inner_proto)
    elif isinstance(inner_proto, ResourceProviderProto):
        fco.resource_provider.CopyFrom(inner_proto)
    else:
        raise Exception("Unsupported type " + str(type(inner_proto)))
    return fco


def create_fco_container(
    fco_protos: typing.Iterable[DataProto], include_main_variables_in_scope: bool = False
) -> FcoContainer:
    proto = fco_pb2.FcoContainer()
    for inner_fco_proto in fco_protos:
        wrapped_fco_proto = _wrap_data_fco(inner_fco_proto)
        proto.fcos.append(wrapped_fco_proto)
    return FcoContainer.from_proto(proto, include_main_variables_in_scope=include_main_variables_in_scope)
