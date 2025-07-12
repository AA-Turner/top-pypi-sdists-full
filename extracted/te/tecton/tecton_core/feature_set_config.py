import functools
import logging
import operator
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

import attrs

from tecton_core import specs
from tecton_core.errors import TectonValidationError
from tecton_core.fco_container import FcoContainer
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.query_consts import udf_internal
from tecton_core.schema import Schema
from tecton_core.specs.feature_spec import FeatureMetadataSpec
from tecton_proto.args import pipeline__client_pb2 as pipeline_pb2
from tecton_proto.common import schema__client_pb2 as schema_pb2


logger = logging.getLogger(__name__)


@attrs.frozen
class _Key:
    name: str
    namespace: str


@attrs.frozen
class FeatureDefinitionAndJoinConfig:
    """
    A Feature Definition Wrapper and its associated join configuration,
    potentially sub-selecting output features based on a FeatureSetItem spec
    (from the feature service).

    :param feature_definition: A FeatureDefinitionWrapper, reflecting the
        underlying spec.
    :param name: The name of the feature definition.
    :param join_keys: The mapping from FeatureService's join keys to
        FeatureView/FeatureTable's join keys.
    :param namespace: The namespace.
    :param features: The output features. Note this can differ from the
        FeatureDefinitionWrapper's features if the FeatureService sub-selects
        features from the feature view.
    """

    feature_definition: FeatureDefinitionWrapper
    name: str
    # Not a dict to account for multi mapping, though we may not handle multi mapping properly everywhere
    join_keys: List[Tuple[str, str]]
    namespace: str
    features: List[str]
    # List of transformation input names that use this feature definition.
    input_names: List[str] = attrs.field(factory=list)

    @classmethod
    def from_feature_definition(cls, feature_definition: FeatureDefinitionWrapper) -> "FeatureDefinitionAndJoinConfig":
        join_keys = [(join_key, join_key) for join_key in feature_definition.join_keys]
        return cls(
            feature_definition=feature_definition,
            name=feature_definition.name,
            join_keys=join_keys,
            namespace=feature_definition.name,
            features=feature_definition.features,
        )

    @property
    def feature_metadata(self):
        return build_feature_metadata(feature_names=self.features, feature_definition=self.feature_definition)

    @classmethod
    def from_feature_view_selection_spec(
        cls, feature_view_selection_spec: specs.FeatureViewSelectionSpec, fco_container: FcoContainer
    ) -> "FeatureDefinitionAndJoinConfig":
        """
        :param feature_view_selection_spec: A FeatureViewSelectionSpec spec.
        :param fco_container: Contains all FSI dependencies (transitively), e.g., FV, Entities, DS-es, Transformations
        """

        join_keys = [
            (i.spine_column_name, i.feature_view_column_name) for i in feature_view_selection_spec.join_key_mappings
        ]
        fv_spec = fco_container.get_by_id(feature_view_selection_spec.feature_view_id)
        feature_definition = FeatureDefinitionWrapper(fv_spec, fco_container)
        return cls(
            feature_definition=feature_definition,
            name=feature_definition.name,
            join_keys=join_keys,
            namespace=feature_view_selection_spec.namespace,
            features=list(feature_view_selection_spec.feature_columns),
        )

    def _key(self) -> _Key:
        return _Key(namespace=self.namespace or "", name=self.name)

    # Returns the spine schema of this FeatureDefinitionAndJoinConfig. It collects the join key schema and request
    # context schema from its FeatureDefinitionWrapper.
    @property
    def spine_schema(self) -> Schema:
        spine_schema_dict = self.feature_definition.spine_schema.to_dict()
        return Schema.from_dict(
            {
                spine_key: spine_schema_dict[fd_key]
                for spine_key, fd_key in self.join_keys
                if fd_key != self.feature_definition.wildcard_join_key
            }
        )


@attrs.define
class FeatureSetConfig:
    """A wrapper over a list of FeatureDefinitionAndJoinConfigs.

    Used for Feature Service and Feature Definition query construction. Needed for Feature Definition queries because
    some Feature Definitions (namely ODFVs with FV inputs) may require specs from multiple Feature Definitions to
    construct queries.
    """

    definitions_and_configs: List[FeatureDefinitionAndJoinConfig] = attrs.field(factory=list)

    @property  # type: ignore
    def feature_definitions(self) -> List[FeatureDefinitionWrapper]:
        """
        Returns the FeatureViews/FeatureTables enclosed in this FeatureSetConfig.
        """
        return [config.feature_definition for config in self.definitions_and_configs]

    @property
    def features(self) -> List[str]:
        """
        Returns the names of features generated by the enclosed feature definitions.
        """
        return [
            features
            for config in self.definitions_and_configs
            for features in FeatureSetConfig._get_full_feature_names(config)
        ]

    @property
    def feature_metadata(self) -> List[FeatureMetadataSpec]:
        """
        Returns FeatureMetadataSpec of the feature generated by the enclosed feature definitions
        """
        return [
            FeatureMetadataSpec(
                name=FeatureSetConfig._get_full_feature_name_for_feature(config, feature_metadatum.name),
                dtype=feature_metadatum.dtype,
                description=feature_metadatum.description,
                tags=feature_metadatum.tags,
            )
            for config in self.definitions_and_configs
            for feature_metadatum in config.feature_metadata
        ]

    @property
    def join_keys(self) -> List[str]:
        """
        Returns the join keys used across all feature definitions.
        """
        keys = set()
        for dac in self.definitions_and_configs:
            for jk_pair in dac.join_keys:
                service_key = jk_pair[0]
                if service_key not in keys:
                    keys.add(service_key)
        return list(keys)

    @property
    def request_context_keys(self) -> List[str]:
        all_keys = functools.reduce(operator.iadd, [fd.request_context_keys for fd in self.feature_definitions], [])
        unique_keys = list(set(all_keys))
        return unique_keys

    @property
    def spine_schema(self) -> Schema:
        spine_schema = Schema(schema_pb2.Schema())
        for dac in self.definitions_and_configs:
            try:
                spine_schema += dac.spine_schema
            except TectonValidationError as e:
                err = f"Tecton Schema Error: {e}"
                raise TectonValidationError(err)
            spine_schema += dac.spine_schema
        return spine_schema

    @staticmethod
    def _get_full_feature_names(config: FeatureDefinitionAndJoinConfig) -> List[str]:
        return [
            FeatureSetConfig._get_full_feature_name_for_feature(config, feature_name)
            for feature_name in config.features
        ]

    @staticmethod
    def _get_full_feature_name_for_feature(config: FeatureDefinitionAndJoinConfig, feature_name: str) -> str:
        return (
            config.namespace + config.feature_definition.namespace_separator + feature_name
            if config.namespace
            else feature_name
        )

    @classmethod
    def from_feature_definition(cls, feature_definition: FeatureDefinitionWrapper) -> "FeatureSetConfig":
        definitions_and_configs = [FeatureDefinitionAndJoinConfig.from_feature_definition(feature_definition)]

        if feature_definition.is_rtfv:
            inputs = find_dependent_feature_set_items(
                feature_definition.fco_container,
                feature_definition.pipeline.root,
                visited_inputs={},
                fv_id=feature_definition.id,
            )
            definitions_and_configs.extend(inputs)

        return FeatureSetConfig(definitions_and_configs=definitions_and_configs)

    @classmethod
    def from_feature_service_spec(
        cls, feature_service_spec: specs.FeatureServiceSpec, fco_container: FcoContainer
    ) -> "FeatureSetConfig":
        """
        :param feature_service_spec: A feature service spec.
        :param fco_container: Contains all FSI dependencies (transitively), e.g., FVs, Entities, DS-es, Transformations
        """

        definitions_and_configs = [
            FeatureDefinitionAndJoinConfig.from_feature_view_selection_spec(feature_view_selection_spec, fco_container)
            for feature_view_selection_spec in feature_service_spec.feature_view_selection_specs
        ]

        # Add dependent feature views into the FeatureSetConfig, uniquely per odfv
        # The namespaces of the dependencies have _udf_internal in the name and are filtered out before
        # being returned by TectonContext.execute()
        visited_feature_view_ids = set()
        for feature_view_selection_spec in feature_service_spec.feature_view_selection_specs:
            if feature_view_selection_spec.feature_view_id in visited_feature_view_ids:
                continue
            visited_feature_view_ids.add(feature_view_selection_spec.feature_view_id)

            fv_spec = fco_container.get_by_id(feature_view_selection_spec.feature_view_id)
            if not isinstance(fv_spec, specs.FeatureViewSpec):
                TypeError(f"Expected a feature view type. {fv_spec}")

            if isinstance(fv_spec, specs.RealtimeFeatureViewSpec):
                dependent_items = find_dependent_feature_set_items(
                    fco_container,
                    fv_spec.pipeline.root,
                    visited_inputs={},
                    fv_id=fv_spec.id,
                )
                definitions_and_configs.extend(dependent_items)

        return cls(definitions_and_configs=definitions_and_configs)


def find_dependent_feature_set_items(
    fco_container: FcoContainer, node: pipeline_pb2.PipelineNode, visited_inputs: Dict[str, bool], fv_id: str
) -> List[FeatureDefinitionAndJoinConfig]:
    if node.HasField("feature_view_node"):
        if node.feature_view_node.input_name in visited_inputs:
            return []
        visited_inputs[node.feature_view_node.input_name] = True

        fv_spec = fco_container.get_by_id_proto(node.feature_view_node.feature_view_id)
        fd = FeatureDefinitionWrapper(fv_spec, fco_container)

        join_keys = []
        overrides = {
            colpair.feature_column: colpair.spine_column
            for colpair in node.feature_view_node.feature_reference.override_join_keys
        }
        for join_key in fd.join_keys:
            potentially_overriden_key = overrides.get(join_key, join_key)
            join_keys.append((potentially_overriden_key, join_key))

        input_name = node.feature_view_node.input_name or fd.name
        cfg = FeatureDefinitionAndJoinConfig(
            feature_definition=fd,
            name=fd.name,
            join_keys=join_keys,
            namespace=f"{udf_internal()}_{input_name}_{fv_id}",
            features=list(node.feature_view_node.feature_reference.features) or fd.features,
            input_names=[input_name],
        )

        return [cfg]
    elif node.HasField("transformation_node"):
        ret: List[FeatureDefinitionAndJoinConfig] = []
        for child in node.transformation_node.inputs:
            ret = ret + find_dependent_feature_set_items(fco_container, child.node, visited_inputs, fv_id)
        return ret
    elif node.HasField("join_inputs_node"):
        ret: List[FeatureDefinitionAndJoinConfig] = []
        for node in node.join_inputs_node.nodes:
            ret = ret + find_dependent_feature_set_items(fco_container, node, visited_inputs, fv_id)
        return ret
    return []


def build_feature_metadata(
    feature_names: List[str], feature_definition: FeatureDefinitionWrapper
) -> Optional[List[FeatureMetadataSpec]]:
    feature_metadata = feature_definition.feature_metadata
    if feature_metadata is None:
        return None

    result: List[FeatureMetadataSpec] = []
    feature_metadata_dict = {metadata.name: metadata for metadata in feature_metadata}

    for name in feature_names:
        if name in feature_metadata_dict:
            result.append(feature_metadata_dict[name])
        else:
            msg = f"{name} not found in Feature Metadata from Feature Definition of {feature_definition.name}."
            raise ValueError(msg)
    return result
