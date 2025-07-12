from types import MappingProxyType
from typing import Dict
from typing import Mapping
from typing import Tuple

import attrs
from typeguard import typechecked

from tecton_core import id_helper
from tecton_core.specs import feature_view_spec
from tecton_core.specs import tecton_object_spec
from tecton_core.specs import utils
from tecton_proto.args import feature_service__client_pb2 as feature_service__args_pb2
from tecton_proto.args import server_group__client_pb2 as server_group__args_pb2
from tecton_proto.data import feature_service__client_pb2 as feature_service__data_pb2
from tecton_proto.data import server_group__client_pb2 as server_group__data_pb2
from tecton_proto.validation import validator__client_pb2 as validator_pb2


__all__ = [
    "FeatureServiceSpec",
    "FeatureServiceSpecArgsSupplement",
    "FeatureViewSelectionSpec",
]


@utils.frozen_strict
class FeatureServiceSpec(tecton_object_spec.TectonObjectSpec):
    feature_view_selection_specs: Tuple["FeatureViewSelectionSpec", ...]
    online_serving_enabled: bool
    enable_online_caching: bool
    prevent_destroy: bool
    options: Mapping[str, str]
    transform_server_group: "ServerGroupReferenceSpec"
    feature_server_group: "ServerGroupReferenceSpec"

    @classmethod
    @typechecked
    def from_data_proto(cls, proto: feature_service__data_pb2.FeatureService) -> "FeatureServiceSpec":
        return cls(
            metadata=tecton_object_spec.TectonObjectMetadataSpec.from_data_proto(
                proto.feature_service_id, proto.fco_metadata
            ),
            feature_view_selection_specs=tuple(
                FeatureViewSelectionSpec.from_data_proto(item) for item in proto.feature_set_items
            ),
            online_serving_enabled=proto.online_serving_enabled,
            validation_args=validator_pb2.FcoValidationArgs(feature_service=proto.validation_args),
            enable_online_caching=proto.enable_online_caching,
            prevent_destroy=proto.validation_args.args.prevent_destroy,
            options=MappingProxyType(proto.options),
            transform_server_group=ServerGroupReferenceSpec.from_data_proto(proto.transform_server_group),
            feature_server_group=ServerGroupReferenceSpec.from_data_proto(proto.feature_server_group),
        )

    @classmethod
    @typechecked
    def from_args_proto(
        cls, proto: feature_service__args_pb2.FeatureServiceArgs, supplement: "FeatureServiceSpecArgsSupplement"
    ) -> "FeatureServiceSpec":
        return cls(
            metadata=tecton_object_spec.TectonObjectMetadataSpec.from_args_proto(
                proto.feature_service_id, proto.info, proto.version
            ),
            feature_view_selection_specs=tuple(
                FeatureViewSelectionSpec.from_args_proto(fp, supplement) for fp in proto.feature_references
            ),
            online_serving_enabled=proto.online_serving_enabled,
            enable_online_caching=proto.enable_online_caching,
            prevent_destroy=proto.prevent_destroy,
            validation_args=None,
            options=MappingProxyType(proto.options),
            transform_server_group=ServerGroupReferenceSpec.from_args_proto(proto.transform_server_group),
            feature_server_group=ServerGroupReferenceSpec.from_args_proto(proto.feature_server_group),
        )


@attrs.define
class FeatureServiceSpecArgsSupplement:
    """A data class used for supplementing args protos during FeatureServiceSpec construction.

    This Python data class can be used to include data that is not included in args protos (e.g. schemas) into the
    FeatureServiceSpec constructor.
    """

    ids_to_feature_views: Dict[str, feature_view_spec.FeatureViewSpec]


@utils.frozen_strict
class ServerGroupReferenceSpec:
    server_group_id: str
    name: str

    @classmethod
    @typechecked
    def from_data_proto(cls, proto: server_group__data_pb2.ServerGroup) -> "ServerGroupReferenceSpec":
        return cls(
            server_group_id=id_helper.IdHelper.to_string(proto.server_group_id),
            name=proto.fco_metadata.name,
        )

    @classmethod
    @typechecked
    def from_args_proto(cls, proto: server_group__args_pb2.ServerGroupReference) -> "ServerGroupReferenceSpec":
        return cls(
            server_group_id=id_helper.IdHelper.to_string(proto.server_group_id),
            name=proto.name,
        )


@utils.frozen_strict
class FeatureViewSelectionSpec:
    """A specification class that represents a set of features from a single feature view in a feature service.

    This class is a Python wrapper around the FeatureSetItem proto message, providing a more descriptive
    name and type-safe interface for working with feature view selections in feature services. It defines
    which features from a feature view should be included in a feature service, along with how they should
    be joined with the spine data.

    Note: This class was formerly called FeatureSetItemSpec. The underlying proto message remains
    FeatureSetItem for backward compatibility.

    Attributes:
        feature_view_id (str): The unique identifier of the feature view from which features are being selected.
        namespace (str): An optional namespace to group features from this feature view. Used to avoid naming
            conflicts when the same feature view is included multiple times in a feature service.
        feature_columns (Tuple[str, ...]): The list of feature columns to include from the feature view.
            If empty, all features from the feature view will be included.
        join_key_mappings (Tuple[utils.JoinKeyMappingSpec, ...]): A tuple of mappings that define how the
            feature view's join keys map to the spine's join keys. This allows for renaming and remapping
            of join keys when joining the feature view with the spine data.
    """

    feature_view_id: str
    namespace: str
    feature_columns: Tuple[str, ...]
    # Mapping from spine join key to the Feature View join keys.  Not a dict to account for multi-mapping.
    join_key_mappings: Tuple["utils.JoinKeyMappingSpec", ...]

    @classmethod
    @typechecked
    def from_data_proto(cls, proto: feature_service__data_pb2.FeatureSetItem) -> "FeatureViewSelectionSpec":
        """Creates a FeatureViewSelectionSpec from a FeatureSetItem protocol buffer.

        Args:
            proto: The FeatureSetItem protocol buffer containing the feature set configuration.

        Returns:
            A new FeatureViewSelectionSpec instance with the configuration from the proto.
        """
        join_key_mappings = []
        for join_configuration_item in proto.join_configuration_items:
            join_key_mappings.append(
                utils.JoinKeyMappingSpec(
                    spine_column_name=join_configuration_item.spine_column_name,
                    feature_view_column_name=join_configuration_item.package_column_name,
                )
            )

        return cls(
            feature_view_id=id_helper.IdHelper.to_string(proto.feature_view_id),
            namespace=utils.get_field_or_none(proto, "namespace"),
            feature_columns=utils.get_tuple_from_repeated_field(proto.feature_columns),
            join_key_mappings=tuple(join_key_mappings),
        )

    @classmethod
    @typechecked
    def from_args_proto(
        cls, proto: feature_service__args_pb2.FeatureReference, supplement: FeatureServiceSpecArgsSupplement
    ) -> "FeatureViewSelectionSpec":
        """Creates a FeatureViewSelectionSpec from a FeatureReference proto and supplementary data.

        This method handles both the basic feature set configuration and any join key overrides specified
        in the feature reference.

        Args:
            proto: The FeatureReference protocol buffer containing the feature set configuration.
            supplement: Additional data needed to construct the spec, including feature view information.

        Returns:
            A new FeatureViewSelectionSpec instance with the configuration from the proto and supplement.
        """
        feature_view_id = id_helper.IdHelper.to_string(proto.feature_view_id)
        fv_spec = supplement.ids_to_feature_views[feature_view_id]

        override_mapping = {
            column_pair.feature_column: column_pair.spine_column for column_pair in proto.override_join_keys
        }
        join_key_mappings = []
        for join_key in fv_spec.join_keys:
            if join_key in override_mapping:
                join_key_mappings.append(
                    utils.JoinKeyMappingSpec(
                        spine_column_name=override_mapping[join_key],
                        feature_view_column_name=join_key,
                    )
                )
            else:
                join_key_mappings.append(
                    utils.JoinKeyMappingSpec(
                        spine_column_name=join_key,
                        feature_view_column_name=join_key,
                    )
                )

        if len(proto.features) > 0:
            # Use a subset of the features from the feature view.
            features = utils.get_tuple_from_repeated_field(proto.features)
        else:
            features = tuple(fv_spec.features)

        return cls(
            feature_view_id=feature_view_id,
            namespace=utils.get_field_or_none(proto, "namespace"),
            feature_columns=features,
            join_key_mappings=tuple(join_key_mappings),
        )


# Resolve forward type declarations.
attrs.resolve_types(FeatureServiceSpec, locals(), globals())
attrs.resolve_types(FeatureViewSelectionSpec, locals(), globals())
