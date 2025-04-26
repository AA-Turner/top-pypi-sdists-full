from typing import List

import attrs
from pypika import Field
from pypika.terms import Term

from tecton_core.compute_mode import ComputeMode
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.query.calculation_sql_builder import CalculationSqlBuilderFactory
from tecton_core.query.column_reference_resolver import ColumnReferenceResolver


@attrs.define(init=False)
class FeatureExtractionSqlBuilder:
    """A class that generates pypika query representations of Calculation and Attribute Features."""

    _column_reference_resolver: ColumnReferenceResolver
    _compute_mode: ComputeMode
    _use_namespace_feature_prefix: bool = True

    def __init__(
        self,
        events_df_timestamp_field: str,
        input_node_column_names: List[str],
        compute_mode: ComputeMode,
        use_namespace_feature_prefix: bool,
    ) -> None:
        self._column_reference_resolver = ColumnReferenceResolver(events_df_timestamp_field, input_node_column_names)
        self._compute_mode = compute_mode
        self._use_namespace_feature_prefix = use_namespace_feature_prefix

    def _extract_calculations(self, fdw: FeatureDefinitionWrapper, namespace: str) -> List[Term]:
        separator = fdw.namespace_separator
        calculation_sql_builder = CalculationSqlBuilderFactory.create_builder(
            fdw, self._column_reference_resolver, self._compute_mode
        )
        calculation_query_terms = []
        for calc in fdw.fv_spec.calculation_features:
            output_column = f"{namespace}{separator}{calc.name}" if self._use_namespace_feature_prefix else calc.name
            calculation_query_term = calculation_sql_builder.ast_node_to_query_term(calc.root).as_(output_column)
            calculation_query_terms.append(calculation_query_term)
        return calculation_query_terms

    def _extract_attributes(self, fdw: FeatureDefinitionWrapper, namespace: str) -> List[Term]:
        separator = fdw.namespace_separator
        attribute_query_terms = []
        for attribute in fdw.fv_spec.attribute_features:
            internal_column_name = self._column_reference_resolver.get_internal_column_name(attribute.name, fdw)
            output_column = (
                f"{namespace}{separator}{attribute.name}" if self._use_namespace_feature_prefix else attribute.name
            )
            attribute_query_term = Field(internal_column_name).as_(output_column)
            attribute_query_terms.append(attribute_query_term)
        return attribute_query_terms

    def extract_rtfv_features(self, fdw: FeatureDefinitionWrapper, namespace: str) -> List[Term]:
        feature_query_terms = []
        if fdw.fv_spec.attribute_features:
            feature_query_terms.extend(self._extract_attributes(fdw, namespace))
        if fdw.fv_spec.calculation_features:
            feature_query_terms.extend(self._extract_calculations(fdw, namespace))
        return feature_query_terms
